"""What changed in a page, marked up so the preview can show it.

git holds the version to compare against; difflib finds the blocks that differ
and, inside a rewritten one, the words. The marks are HTML that pandoc's gfm
reader passes straight through: a <div> closed by a blank line still lets the
Markdown inside it parse as Markdown, and <ins>/<del> are inline, so a sentence
that gained a link still gets one. Nothing here renders -- it returns Markdown
for preview.py to hand to pandoc.
"""
import difflib
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGES = "input/pagecontent"

# What has to stay at the head of its line to go on working: quote markers, list
# bullets, a heading's hashes. An <ins> in front of any of them kills it.
LEADIN = re.compile(r"^[ \t]*(?:>[ \t]*)*(?:[-*+][ \t]+|\d+[.)][ \t]+|#{1,6}[ \t]+)?")
# `| --- | :--: |`, the row that makes a table a table
RULER = re.compile(r"^[ \t]*\|?[\s:|-]+\|?[ \t]*$")
HEADING = re.compile(r"^#{1,6}[ \t]+(.*)$", re.M)
NOTE = re.compile(r"^\[\^[^\]\n]+\]:")
NOTEREF = re.compile(r"\[\^[^\]\n]+\]")
# a <del> that lands in front of a line's marker takes the line's meaning with it
ORPHAN = re.compile(r"(?m)^((?:<del>.*?</del>[ \t]*)+)((?:[-*+]|\d+[.)]|#{1,6}|>)[ \t]+)")
# Anything a mark would ruin by landing in the middle of it counts as one word:
# a link cut in two stops being a link.
WHOLE = "|".join((
    r"\[[^\]\n]*\]\([^)\n]*\)",   # a link, text and target together
    r"\[\^[^\]\n]*\]",            # a footnote reference
    r"`[^`\n]*`",                 # code
    r"\*\*[^*\n]+\*\*",           # bold
    r"\*[^*\n]+\*",               # italics
    r"_[^_\n]+_",                 # italics again
))
# A word is one of those, a run of space, or a run of anything else that stops
# the moment one of those starts -- otherwise the `(` in `([MHDS ...](...))`
# takes the link's opening bracket with it and the link comes apart.
ATOM = re.compile(rf"{WHOLE}|\s+|(?:(?!{WHOLE})\S)+")
# how alike two blocks must be before diffing them word by word tells you anything
AKIN = 0.3


def git(*args):
    """What the git command printed, or None when it had nothing to say."""
    done = subprocess.run(("git", *args), cwd=ROOT, capture_output=True, text=True)
    return done.stdout if done.returncode == 0 else None


def ref(base):
    """The commit to compare against: HEAD, or where this branch left main."""
    if base != "main":
        return "HEAD"
    out = git("merge-base", "main", "HEAD")
    return out.strip() if out else "main"


def changed(base):
    """The filenames of the pages that differ from the base."""
    out = git("diff", "--name-only", ref(base), "--", PAGES)
    return {Path(line).name for line in out.split("\n") if line} if out else set()


def source(name, base):
    """The page as the base has it, "" if the base predates the page, None when
    git cannot answer at all -- no repository, no such commit."""
    commit = ref(base)
    out = git("show", f"{commit}:{PAGES}/{name}")
    if out is not None:
        return out
    return "" if git("rev-parse", "--verify", "--quiet", commit) else None


def blocks(text):
    """The text as [block, gap, block, gap, ...]; "".join puts it back exactly."""
    return re.split(r"(\n[ \t]*\n)", text)


def kind(block):
    head = block.lstrip()
    if NOTE.match(head):
        return "note"
    return {"#": "heading", "|": "table"}.get(head[:1], "text")


def match(a, b):
    return difflib.SequenceMatcher(None, a, b, autojunk=False)


def align(was, now):
    """Which block that went and which that came are the same block rewritten.
    Position alone mispairs as soon as one block is dropped in the middle, so
    each block that came looks for its likeliest counterpart instead. Returns
    the pairings, and which of the blocks that went found nobody."""
    taken, pairs = set(), {}
    for j, after in enumerate(now):
        best, score = None, AKIN
        for i, before in enumerate(was):
            if i in taken or kind(before) != kind(after):
                continue
            ratio = match(before, after).ratio()
            if ratio > score:
                best, score = i, ratio
        if best is not None:
            taken.add(best)
            pairs[j] = best
    return pairs, [i for i in range(len(was)) if i not in taken]


def mark(old, new):
    """`new`, with every block the base does not have marked up. Returns the
    marked Markdown and how many blocks carry a mark; an untouched page comes
    back byte for byte as it went in."""
    parts = blocks(new)
    kept, gaps = parts[::2], parts[1::2]
    # compared stripped: the blank line a dropped attribute leaves behind must
    # not make two identical blocks look like two different ones
    was, now = [b.strip() for b in blocks(old)[::2]], [b.strip() for b in kept]

    out, gone, count = list(kept), {}, 0
    for tag, i1, i2, j1, j2 in match(was, now).get_opcodes():
        if tag == "equal":
            continue
        pairs, spare = align(was[i1:i2], now[j1:j2])
        for j in range(j1, j2):
            after = now[j]
            # footnote definitions are plumbing, and a mark in front of one
            # stops it being one; pandoc renumbers them all anyway
            if not after or kind(after) == "note":
                continue
            i = pairs.get(j - j1)
            if i is None:
                out[j] = box("d-new", after)
            elif kind(after) == "table":
                out[j] = box("d-chg", rows(was[i1 + i], after))
            else:
                out[j] = box("d-chg", words(was[i1 + i], after))
            count += 1
        for i in spare:
            before = was[i1 + i]
            if not before or kind(before) == "note":
                continue
            # shown where the next surviving block puts it
            later = [j for j, pick in pairs.items() if pick > i]
            gone.setdefault(j1 + min(later) if later else j2, []).append(before)
            count += 1

    pieces = []
    for k, block in enumerate(out):
        for lost in gone.get(k, []):
            pieces += [box("d-del", HEADING.sub(r"**\1**", lost)), "\n\n"]
        pieces.append(block)
        if k < len(gaps):
            pieces.append(gaps[k])
    for lost in gone.get(len(out), []):
        pieces += ["\n\n", box("d-del", HEADING.sub(r"**\1**", lost))]

    return "".join(pieces), count


def box(cls, block):
    """A block inside a div. The blank lines are what keep pandoc reading the
    Markdown inside it as Markdown rather than as raw HTML."""
    return f'<div class="{cls}">\n\n{block.strip()}\n\n</div>'


def words(before, after):
    """`after`, with what it gained in <ins> and what it lost in <del>."""
    was, now = split_words(before), split_words(after)
    out = []
    for tag, i1, i2, j1, j2 in match(was, now).get_opcodes():
        if tag in ("delete", "replace"):
            out.append(struck("".join(was[i1:i2])))
        if tag in ("insert", "replace"):
            out.append(added("".join(now[j1:j2])))
        if tag == "equal":
            out.append("".join(now[j1:j2]))
    # the words it lost move behind the marker, never in front of it
    return ORPHAN.sub(r"\2\1", "".join(out))


def split_words(text):
    return ATOM.findall(text)


def added(text):
    """`text` marked as new, one <ins> per line and never in front of the
    markers -- bullets, hashes, quotes -- that give the line its meaning."""
    out = []
    for line in text.splitlines(keepends=True):
        lead = LEADIN.match(line).group(0)
        rest = line[len(lead):]
        if not rest.strip():
            out.append(line)
            continue
        tail = rest[len(rest.rstrip()):]
        out.append(f"{lead}<ins>{rest.strip()}</ins>{tail}")
    return "".join(out)


def struck(text):
    """Text the page no longer has, folded onto one line: it is being shown for
    reference, and its old line breaks and bullets would only reshape the new
    block it now sits in."""
    loose = re.sub(r"(?m)^[ \t]*(?:>[ \t]*)*(?:[-*+]|\d+[.)])[ \t]+", "", text)
    body = " ".join(NOTEREF.sub("", loose).split())
    if not body:
        return text
    head = " " if text[:1].isspace() else ""
    tail = " " if text[-1:].isspace() else ""
    return f"{head}<del>{body}</del>{tail}"


def rows(before, after):
    """A changed table, marked row by row and cell by cell. Every pipe stays
    outside the marks, which is what keeps the table a table."""
    was, now = before.split("\n"), after.split("\n")
    out, dropped = list(now), {}
    for tag, i1, i2, j1, j2 in match([r.strip() for r in was],
                                     [r.strip() for r in now]).get_opcodes():
        if tag == "equal":
            continue
        for k in range(max(i2 - i1, j2 - j1)):
            old_row = was[i1 + k] if i1 + k < i2 else None
            new_row = now[j1 + k] if j1 + k < j2 else None
            if new_row is None:
                if old_row.strip() and not RULER.match(old_row):
                    dropped.setdefault(j2, []).append(cells(old_row, gone=True))
            elif new_row.strip() and not RULER.match(new_row):
                out[j1 + k] = cells(new_row, old_row)

    lines = []
    for k, row in enumerate(out):
        lines += dropped.get(k, [])
        lines.append(row)
    return "\n".join(lines + dropped.get(len(out), []))


def cells(row, against=None, gone=False):
    """One table row: each cell diffed against the cell that stood there, marked
    whole when the row is new, struck when the row itself is what went away."""
    now = row.split("|")
    was = against.split("|") if against and not RULER.match(against) else None
    if was is not None and len(was) != len(now):
        was = None

    out = []
    for i, cell in enumerate(now):
        body = cell.strip()
        if not body:
            out.append(cell)
        elif gone:
            out.append(pad(cell, f"<del>{body}</del>"))
        elif was is None:
            out.append(pad(cell, added(body)))
        elif was[i].strip() == body:
            out.append(cell)
        else:
            out.append(pad(cell, words(was[i].strip(), body)))
    return "|".join(out)


def pad(cell, body):
    """`body` back in the cell, with the spacing the cell had around it."""
    head = cell[:len(cell) - len(cell.lstrip())]
    return f"{head}{body}{cell[len(cell.rstrip()):]}"
