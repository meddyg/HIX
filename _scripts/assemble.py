"""Copies the pages into a work directory in the shape pandoc needs."""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import pageorder

ROOT = Path(__file__).resolve().parent.parent
work = Path(sys.argv[1])
cfg = pageorder.config()

DEPENDENCY_TABLE = "\n".join(
    ["| Paquete | Versión | Aporta |", "| --- | --- | --- |"]
    + [f"| {name} | {version} | {reason} |" for name, version, reason in pageorder.dependencies(cfg)]
)

names = []
for name, title, depth in pageorder.pages(cfg):
    body = (ROOT / "input" / "pagecontent" / name).read_text()
    body = re.sub(r"^\{:.*\}$", "", body, flags=re.M)
    # kramdown abbreviations (`*[PMIR]: ...`) become tooltips on the site; pandoc has no equivalent
    body = re.sub(r"^\*\[[^\]]+\]: .*$", "", body, flags=re.M)
    # The dependency table is a fragment the publisher generates and Jekyll
    # includes. Pandoc gets the same rows straight from sushi-config.yaml.
    body = body.replace("{% include dependency-table.xhtml %}", DEPENDENCY_TABLE)

    # The publisher copies input/images/ to the root of the site, so a page
    # refers to a figure by its bare name. Pandoc runs from the repository and
    # needs the real path.
    body = re.sub(r"\]\((?!\w+:)([^)/]+\.svg)\)", r"](input/images/\1)", body)

    # A page's content starts at ### because the site renders the title as the
    # h2. A top-level page becomes an h1 here, so its content moves up one level
    # too -- otherwise pandoc numbers it 1.0.1 instead of 1.1.
    level = "#" if depth == 1 else "##"
    if depth == 1:
        body = re.sub(r"^#(#{2,})", r"\1", body, flags=re.M)

    (work / name).write_text(f"{level} {title}\n\n{body}")
    names.append(str(work / name))

(work / "order.txt").write_text("\n".join(names))
(work / "meta.txt").write_text("\n".join([
    pageorder.scalar("title", cfg),
    pageorder.scalar("version", cfg),
    pageorder.scalar("status", cfg),
    pageorder.scalar("canonical", cfg),
]))
