"""Writes dist/llms.txt, dist/llms-full.txt and one Markdown file per page.

llms.txt is a convention, not a pandoc output format: a Markdown index an
implementer hands to an agent, which reads it and fetches only the pages it
needs. So every link says what its page covers and points at clean Markdown
instead of the site's HTML; llms-full.txt is the whole text for those who
prefer one fetch. See https://llmstxt.org.
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import pageorder

ROOT = Path(__file__).resolve().parent.parent
work = Path(sys.argv[1])
cfg = pageorder.config()

title = pageorder.scalar("title", cfg)
canonical = pageorder.scalar("canonical", cfg)
version = pageorder.scalar("version", cfg)
status = pageorder.scalar("status", cfg)
page_list = pageorder.pages(cfg)


def plain(text):
    """Markdown down to the words: no emphasis, links as their text, no footnote marks."""
    text = re.sub(r"\[\^[^\]]+\]", "", text)
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)
    text = re.sub(r"\s+\(\s*\)", "", text)  # a citation that was only a link
    return re.sub(r"[*`]", "", text).strip()


def published(md):
    """The page as it is served: beside the site, so figures are siblings again."""
    return md.replace("](input/images/", "](")


bodies = {name: (work / name).read_text() for name, _t, _d in page_list}

# A volume tells its reader what each of its pages is for ("Cómo leer este
# volumen"). Those sentences are the descriptions; a page without one gives its
# own first sentence.
described = {}
for body in bodies.values():
    for m in re.finditer(r"^- \*\*\[?([^\]*]+?)\]?(?:\([^)]*\))?\*\* (.+)$", body, re.M):
        described[plain(m.group(1))] = plain(m.group(2))


def description(name, page_title):
    if page_title in described:
        text = described[page_title]
        return text[0].upper() + text[1:]
    paragraphs = [b for b in re.split(r"\n\s*\n", bodies[name]) if b.strip() and not b.startswith("#")]
    first = plain(paragraphs[0]) if paragraphs else ""
    return re.split(r"(?<=[.!?])\s", first, maxsplit=1)[0]


index = [
    f"# {title}",
    "",
    f"> {pageorder.folded('description', cfg)}",
    "",
    f"Version {version} ({status}). This specification takes IHE MHDS as its "
    "reference architecture and does not claim conformance to it. It is not an "
    "IHE publication and is not endorsed by IHE. It is written in Spanish. The "
    f"site is {canonical}/ and every page below is its Markdown source.",
    "",
    "## Pages",
    "",
]
out = ROOT / "dist"
(out / "md").mkdir(parents=True, exist_ok=True)
for name, page_title, depth in page_list:
    indent = "" if depth == 1 else "  "
    index.append(f"{indent}- [{page_title}]({canonical}/{name[:-3]}.html.md): {description(name, page_title)}")
    # the llms.txt convention: a page's Markdown lives at its URL plus ".md"
    (out / "md" / f"{name[:-3]}.html.md").write_text(published(bodies[name]))

index += ["", "## Full text", "", f"- [Complete specification]({canonical}/llms-full.txt): every page above in one file"]
(out / "llms.txt").write_text("\n".join(index) + "\n")

full = [f"# {title}", "", f"Version {version} ({status}) - {canonical}", ""]
for name, _t, _d in page_list:
    full.append(published(bodies[name]).rstrip())
    full.append("")

(out / "llms-full.txt").write_text("\n".join(full) + "\n")
