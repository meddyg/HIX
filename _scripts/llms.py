"""Writes dist/llms.txt and dist/llms-full.txt.

llms.txt is a convention, not a pandoc output format: a Markdown index an LLM
can read to find the specification, and a full-text companion beside it.
See https://llmstxt.org.
"""
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

index = [
    f"# {title}",
    "",
    f"> {pageorder.folded('description', cfg)}",
    "",
    f"Version {version} ({status}). This specification implements the IHE MHDS "
    "profile and the profiles it builds on. It is not an IHE publication and is "
    "not endorsed by IHE.",
    "",
    "## Pages",
    "",
]
for name, page_title, depth in page_list:
    indent = "" if depth == 1 else "  "
    index.append(f"{indent}- [{page_title}]({canonical}/{name[:-3]}.html)")

index += ["", "## Full text", "", f"- [Complete specification]({canonical}/llms-full.txt)"]
(ROOT / "dist" / "llms.txt").write_text("\n".join(index) + "\n")

full = [f"# {title}", "", f"Version {version} ({status}) - {canonical}", ""]
for path in (work / "order.txt").read_text().split("\n"):
    full.append(Path(path).read_text().rstrip())
    full.append("")
    
(ROOT / "dist" / "llms-full.txt").write_text("\n".join(full) + "\n")
