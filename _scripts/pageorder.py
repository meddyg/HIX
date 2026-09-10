"""Reads `pages:` from sushi-config.yaml -- the single source of page order."""
import re
from pathlib import Path

CONFIG = Path(__file__).resolve().parent.parent / "sushi-config.yaml"


def config():
    return CONFIG.read_text()


def scalar(key, cfg=None):
    cfg = cfg if cfg is not None else config()
    m = re.search(rf"^{key}:\s*(.+?)\s*$", cfg, re.M)

    return m.group(1).strip("\"'") if m else ""


def folded(key, cfg=None):
    """A `key: >-` folded block, joined back into one line."""
    cfg = cfg if cfg is not None else config()
    m = re.search(rf"^{key}: >-\n((?:  .+\n)+)", cfg, re.M)
    if not m:
        return ""

    return " ".join(line.strip() for line in m.group(1).split("\n") if line.strip())


def pages(cfg=None):
    """(filename, title, depth) in declaration order; depth 1 = top level."""
    cfg = cfg if cfg is not None else config()
    block = re.search(r"^pages:\n(.*?)(?=^\w)", cfg, re.S | re.M).group(1)

    out, current = [], None
    for line in block.split("\n"):
        m = re.match(r"^(\s+)([\w.-]+\.md):\s*$", line)
        if m:
            current = (len(m.group(1)), m.group(2))
            continue
        m = re.match(r"^\s+title:\s*(.+?)\s*$", line)
        if m and current:
            indent, name = current
            out.append((name, m.group(1).strip("\"'"), 1 if indent == 2 else 2))
            current = None

    return out


def numbers(page_list):
    """Section numbers, the way the publisher derives them from the nesting."""
    result, top, sub = {}, 0, 0
    for name, _title, depth in page_list:
        if depth == 1:
            top += 1
            sub = 0
            result[name] = str(top)
        else:
            sub += 1
            result[name] = f"{top}.{sub}"
    return result
