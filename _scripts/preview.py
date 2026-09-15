#!/usr/bin/env python3
"""Fast preview for writing prose.

The IG Publisher takes about half a minute per build, which is fine for
verifying a page and useless for writing one. This renders the same Markdown
with pandoc into the site's own CSS in well under a second, watches the sources,
and reloads the browser when one changes.

It is a writing aid, not the build. It does not run SUSHI, does not validate,
and does not produce the artifact pages. Run ./_genonce.sh before trusting what
you see.

    ./_scripts/preview.py        # http://localhost:4000
"""
import http.server
import json
import re
import socketserver
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
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




def render(name, title, prefix, pages, numbers):
    src = (PAGES / name).read_text()
    src = re.sub(r"^\{:.*\}$", "", src, flags=re.M)
    offset = ",".join(prefix.split("."))
    body = subprocess.run(
        ["pandoc", "--from=gfm", "--to=html", "--no-highlight",
         "--number-sections", f"--number-offset={offset}"],
        input=src, capture_output=True, text=True, check=True).stdout
    # every table in this specification is a grid table on the site
    body = body.replace("<table>", '<table class="grid">')

    nav = "\n".join(
        f'<li{" class=\"active\"" if n == name else ""}>'
        f'<a href="/{n[:-3]}.html">{numbers[n]} {t}</a></li>'
        for n, t, _d in pages)

    return f"""<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">
<title>{title} — hix (preview)</title>
<link href="/fhir.css" rel="stylesheet"><link href="/assets/css/bootstrap-fhir.css" rel="stylesheet">
<link href="/assets/css/project.css" rel="stylesheet"><link href="/assets/css/hix.css" rel="stylesheet">
<style>
  #wrap {{ display: flex; align-items: flex-start; gap: 24px; padding: 12px 24px; }}
  #side {{ width: 300px; flex: none; font-size: 12px; position: sticky; top: 12px;
           max-height: 92vh; overflow: auto; border-right: 1px solid #ddd; padding-right: 12px; }}
  #side ul {{ list-style: none; padding: 0; margin: 0; }}
  #side li a {{ display: block; padding: 3px 6px; border-radius: 3px; }}
  #side li.active a {{ background: #0e3a4f; color: #fff; }}
  #main {{ flex: 1; min-width: 0; background: #fff; padding: 0 8px 60px; }}
  #banner {{ background: #fff3cd; border: 1px solid #e0c97f; padding: 6px 10px;
             font-size: 12px; margin-bottom: 14px; }}
  h1, h2, h3, h4 {{ color: #0e3a4f; }}
</style></head><body>
<div id="wrap">
  <nav id="side"><ul>{nav}</ul></nav>
  <div id="main">
    <div id="banner"><b>Preview</b> — pandoc rendering for writing. Not the
      publisher's output: no validation, no artifact pages. Run
      <code>make site</code> to see the real site.</div>
    <h1>{prefix} {title}</h1>
    {body}
  </div>
</div>
<script src="/assets/js/jquery.js"></script>
<script src="/assets/js/bootstrap.min.js"></script>{RELOAD_JS}</body></html>"""


def fingerprint():
    # a re-rendered diagram (make diagrams) reloads the page too
    watched = list(PAGES.glob("*.md")) + list(IMAGES.glob("*.svg")) + [CONFIG]
    return json.dumps(sorted((str(p), p.stat().st_mtime_ns) for p in watched))


class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/__version":
            return self.send_text(fingerprint())
        if self.path.startswith("/assets/") or self.path == "/fhir.css":
            target = ASSETS / self.path.lstrip("/")
            if not target.exists():
                return self.send_error(404, "Run 'make site' once to produce the stylesheets and scripts")
            self.send_response(200)
            ctype = {".js": "text/javascript", ".map": "application/json"}.get(target.suffix, "text/css")
            self.send_header("Content-Type", ctype)
            # `make site` and `make diagrams` rewrite these under the same URL
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            return self.wfile.write(target.read_bytes())

        if self.path.endswith(".svg"):
            target = IMAGES / self.path.lstrip("/")
            if not target.exists():
                return self.send_error(404, f"{target.name} is not in input/images")
            self.send_response(200)
            self.send_header("Content-Type", "image/svg+xml")
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            return self.wfile.write(target.read_bytes())

        pages = pageorder.pages()
        numbers = pageorder.numbers(pages)
        want = self.path.lstrip("/") or "index.html"
        name = want[:-5] + ".md"
        match = next((p for p in pages if p[0] == name), None)
        if match is None:
            return self.send_error(404, f"{name} is not in sushi-config.yaml")
        html = render(match[0], match[1], numbers[name], pages, numbers)
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
