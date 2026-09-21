#!/usr/bin/env python3
"""Fast preview for writing prose.

The IG Publisher takes about half a minute per build, which is fine for
verifying a page and useless for writing one. This renders the same Markdown
with pandoc into the site's own CSS in well under a second, watches the sources,
and reloads the browser when one changes.

It is a writing aid, not the build. It does not run SUSHI, does not validate,
and does not produce the artifact pages. Run ./_genonce.sh before trusting what
you see.

It doubles as a review aid: every block the page has gained, lost or had
rewritten since HEAD -- or since the branch left main -- is marked in place,
word by word. The banner turns the marks off to go back to writing.

    ./_scripts/preview.py        # http://localhost:4000
"""
import http.server
import json
import re
import socketserver
import subprocess
import sys
from pathlib import Path
from urllib.parse import parse_qs

sys.path.insert(0, str(Path(__file__).resolve().parent))
import pagediff
import pageorder

ROOT = Path(__file__).resolve().parent.parent
PAGES = ROOT / "input" / "pagecontent"
CONFIG = ROOT / "sushi-config.yaml"
IMAGES = ROOT / "input" / "images"
# The publisher writes the real stylesheets and scripts here; the preview borrows them.
ASSETS = ROOT / "dist" / "site"
PORT = 4000

RELOAD_JS = """
<script>
let seen = null;
setInterval(async () => {
  try {
    const v = await (await fetch('/__version')).text();
    if (seen === null) seen = v; else if (v !== seen) location.reload();
  } catch (e) {}
}, 400);
</script>
"""

# Read before the page paints, so a reader who muted the marks never sees them
# flash, and a reader reviewing the branch never renders HEAD first.
SETUP_JS = """
<script>
try {
  const m = localStorage.getItem('marks');
  document.documentElement.className =
    'marks-' + (['off', 'bars', 'words'].includes(m) ? m : 'words');
  if (!location.search.includes('base=') && localStorage.getItem('base') === 'main')
    location.replace(location.pathname + '?base=main');
} catch (e) {}
</script>
"""

CONTROLS_JS = """
<script>
const MODES = ['off', 'bars', 'words'], root = document.documentElement;
const mode = () => MODES.find(m => root.classList.contains('marks-' + m)) || 'words';
const wear = m => {
  root.className = 'marks-' + m;
  document.querySelector('#modes input[value="' + m + '"]').checked = true;
  try { localStorage.setItem('marks', m); } catch (e) {}
};
wear(mode());
document.querySelectorAll('#modes input').forEach(i => { i.onchange = () => wear(i.value); });
// d cycles them, so the control is never worth reaching for
addEventListener('keydown', e => {
  if (e.key !== 'd' || e.metaKey || e.ctrlKey || e.altKey) return;
  if (/^(INPUT|SELECT|TEXTAREA)$/.test(e.target.tagName)) return;
  wear(MODES[(MODES.indexOf(mode()) + 1) % MODES.length]);
});
const pick = document.getElementById('base');
pick.onchange = () => {
  try { localStorage.setItem('base', pick.value); } catch (e) {}
  location.search = pick.value === 'main' ? '?base=main' : '';
};
</script>
"""


def clean(src):
    """The page without what pandoc cannot do anything with."""
    src = re.sub(r"^\{:.*\}$", "", src, flags=re.M)
    # kramdown abbreviations (`*[PMIR]: ...`) become tooltips on the site; pandoc has no equivalent
    return re.sub(r"^\*\[[^\]]+\]: .*$", "", src, flags=re.M)


def render(name, title, prefix, pages, numbers, base, touched):
    src = clean((PAGES / name).read_text())
    # both sides cleaned the same way, so a stripped attribute never reads as an edit
    was = pagediff.source(name, base)
    count = 0
    if was is not None:
        src, count = pagediff.mark(clean(was), src)
    offset = ",".join(prefix.split("."))
    body = subprocess.run(
        ["pandoc", "--from=gfm", "--to=html", "--no-highlight",
         "--number-sections", f"--number-offset={offset}"],
        input=src, capture_output=True, text=True, check=True).stdout
    # every table in this specification is a grid table on the site
    body = body.replace("<table>", '<table class="grid">')

    # the base has to survive a click, so it travels in the links
    query = "?base=main" if base == "main" else ""
    nav = "\n".join(
        f'<li class="{"active " if n == name else ""}{"chg" if n in touched else ""}">'
        f'<a href="/{n[:-3]}.html{query}">{numbers[n]} {t}</a></li>'
        for n, t, _d in pages)
    choice = "".join(f'<option{" selected" if b == base else ""}>{b}</option>'
                     for b in ("HEAD", "main"))
    modes = "".join(f'<label><input type="radio" name="marks" value="{v}"><span>{t}</span></label>'
                    for v, t in (("off", "none"), ("bars", "bar"), ("words", "words")))
    tally = f"{count} block{'' if count == 1 else 's'}" if count else "unchanged"

    return f"""<!DOCTYPE html><html lang="en" class="marks-words"><head><meta charset="utf-8">
<title>{title} — hix (preview)</title>
<link href="/fhir.css" rel="stylesheet"><link href="/assets/css/bootstrap-fhir.css" rel="stylesheet">
<link href="/assets/css/project.css" rel="stylesheet"><link href="/assets/css/hix.css" rel="stylesheet">
<style>
  #wrap {{ display: flex; align-items: flex-start; gap: 24px; padding: 12px 24px; }}
  #side {{ width: 300px; flex: none; font-size: 12px; position: sticky; top: 12px;
           max-height: 92vh; display: flex; flex-direction: column;
           border-right: 1px solid #ddd; padding-right: 12px; }}
  /* only the page list scrolls, so the switch is there however far down you are */
  #side ul {{ list-style: none; padding: 0; margin: 0; overflow: auto; min-height: 0; }}
  #side li a {{ display: block; padding: 3px 6px; border-radius: 3px; }}
  #side li.active a {{ background: #0e3a4f; color: #fff; }}
  #main {{ flex: 1; min-width: 0; background: #fff; padding: 0 8px 60px; }}
  #banner {{ background: #fff3cd; border: 1px solid #e0c97f; padding: 6px 10px;
             font-size: 12px; margin-bottom: 14px; }}
  h1, h2, h3, h4 {{ color: #0e3a4f; }}
  #switch {{ flex: none; padding-bottom: 8px; margin-bottom: 8px;
             border-bottom: 1px solid #ddd; }}
  #switch select {{ font-size: 12px; height: 20px; padding: 0; vertical-align: baseline; }}
  #tally {{ color: #7a6a3a; }}
  #modes {{ display: flex; margin: 4px 0 6px; }}
  #modes label {{ flex: 1; margin: 0; font-weight: normal; }}
  #modes input {{ position: absolute; width: 0; opacity: 0; }}
  #modes span {{ display: block; text-align: center; padding: 3px 0; cursor: pointer;
                 background: #f7f7f7; border: 1px solid #ccc; border-left-width: 0; }}
  #modes label:first-child span {{ border-left-width: 1px; border-radius: 3px 0 0 3px; }}
  #modes label:last-child span {{ border-radius: 0 3px 3px 0; }}
  #modes input:checked + span {{ background: #0e3a4f; color: #fff; border-color: #0e3a4f; }}
  .d-new, .d-chg, .d-del {{ border-left: 3px solid #2f7d32; padding-left: 11px; margin-left: -14px; }}
  .d-chg {{ border-left-color: #b8860b; }}
  .d-del {{ border-left-color: #a94442; color: #999; text-decoration: line-through; }}
  ins {{ background: #e3f2e5; text-decoration: none; border-bottom: 1px solid #9ccfa5; }}
  del {{ background: #fbe4e4; color: #8a4a4a; }}
  /* a word swapped for another reads as one word unless they are kept apart */
  ins, del {{ padding: 0 2px; border-radius: 2px; }}
  del + ins {{ margin-left: 3px; }}
  #side li.chg > a::after {{ content: "•"; color: #b8860b; margin-left: 5px; }}
  /* bars: where the page changed, while it still reads as the site will publish
     it -- so nothing it no longer says is on screen */
  .marks-bars ins {{ background: none; border-bottom: 0; }}
  .marks-bars .d-del, .marks-bars del {{ display: none; }}
  /* off: writing again, and the page is the page */
  .marks-off .d-new, .marks-off .d-chg {{ border-left: 0; padding-left: 0; margin-left: 0; }}
  .marks-off .d-del, .marks-off del {{ display: none; }}
  .marks-off ins {{ background: none; border-bottom: 0; }}
  .marks-off #side li.chg > a::after {{ content: none; }}
</style>{SETUP_JS}</head><body>
<div id="wrap">
  <nav id="side">
    <div id="switch">changes <span id="tally">{tally}</span>
      <div id="modes">{modes}</div>
      vs <select id="base">{choice}</select> · <kbd>d</kbd> cycles
    </div>
    <ul>{nav}</ul>
  </nav>
  <div id="main">
    <div id="banner"><b>Preview</b> — pandoc rendering for writing. Not the
      publisher's output: no validation, no artifact pages. Run
      <code>make site</code> to see the real site.</div>
    <h1>{prefix} {title}</h1>
    {body}
  </div>
</div>
<script src="/assets/js/jquery.js"></script>
<script src="/assets/js/bootstrap.min.js"></script>{CONTROLS_JS}{RELOAD_JS}</body></html>"""


def fingerprint():
    # a re-rendered diagram (make diagrams) reloads the page too
    watched = list(PAGES.glob("*.md")) + list(IMAGES.glob("*.svg")) + [CONFIG]
    return json.dumps(sorted((str(p), p.stat().st_mtime_ns) for p in watched))


class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        path, _, query = self.path.partition("?")
        if path == "/__version":
            return self.send_text(fingerprint())
        if path.startswith("/assets/") or path == "/fhir.css":
            target = ASSETS / path.lstrip("/")
            if not target.exists():
                return self.send_error(404, "Run 'make site' once to produce the stylesheets and scripts")
            self.send_response(200)
            ctype = {".js": "text/javascript", ".map": "application/json"}.get(target.suffix, "text/css")
            self.send_header("Content-Type", ctype)
            # `make site` and `make diagrams` rewrite these under the same URL
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            return self.wfile.write(target.read_bytes())

        if path.endswith(".svg"):
            target = IMAGES / path.lstrip("/")
            if not target.exists():
                return self.send_error(404, f"{target.name} is not in input/images")
            self.send_response(200)
            self.send_header("Content-Type", "image/svg+xml")
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            return self.wfile.write(target.read_bytes())

        base = "main" if parse_qs(query).get("base") == ["main"] else "HEAD"
        pages = pageorder.pages()
        numbers = pageorder.numbers(pages)
        want = path.lstrip("/") or "index.html"
        name = want[:-5] + ".md"
        match = next((p for p in pages if p[0] == name), None)
        if match is None:
            return self.send_error(404, f"{name} is not in sushi-config.yaml")
        html = render(match[0], match[1], numbers[name], pages, numbers,
                      base, pagediff.changed(base))
        return self.send_text(html, "text/html")

    def send_text(self, text, ctype="text/plain"):
        payload = text.encode()
        self.send_response(200)
        self.send_header("Content-Type", f"{ctype}; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(payload)

    def log_message(self, *args):
        pass


if __name__ == "__main__":
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("127.0.0.1", PORT), Handler) as httpd:
        print(f"Preview on http://localhost:{PORT}  (Ctrl-C to stop)")
        httpd.serve_forever()
