#!/usr/bin/env bash
# Exports the same narrative to PDF, Word and llms.txt.
#
# input/pagecontent/*.md is the single source: the IG Publisher renders it into
# the site, pandoc renders it into the downloadable forms. Two adjustments are
# needed because the site keeps information outside the Markdown:
#
#   - The page title and its place in the hierarchy live in `pages:` in
#     sushi-config.yaml, and the publisher renders the title as the page's
#     heading. Pandoc never sees it, so it is prepended here: `#` for a volume,
#     `##` for a chapter, which leaves the `###` inside a page as the third
#     level -- the same shape the site shows.
#   - Kramdown block attributes ({:.grid} and friends) are stripped; pandoc
#     would print them verbatim.
#
# The page design is theme/hix.typ (PDF) and theme/reference.docx (Word).
set -euo pipefail

cd "$(dirname "$0")/.."
mkdir -p dist
work=$(mktemp -d)
trap 'rm -rf "$work"' EXIT

python3 _scripts/assemble.py "$work"

mapfile -t pages < "$work/order.txt"
mapfile -t meta < "$work/meta.txt"
title="${meta[0]}"; version="${meta[1]}"; status="${meta[2]}"; canonical="${meta[3]}"
today=$(date +%Y-%m-%d)

echo "==> PDF"
pandoc "${pages[@]}" \
  --from=gfm --pdf-engine=typst \
  -V template=theme/hix.typ \
  -V section-numbering=1.1.1 \
  -M title="$title" \
  -M subtitle="Specification of the hix document sharing community" \
  -M author="Meddyg" \
  -M date="$today" \
  --toc --toc-depth=3 --number-sections \
  --pdf-engine-opt="--input=version=$version" \
  --pdf-engine-opt="--input=status=$status" \
  --pdf-engine-opt="--input=canonical=$canonical" \
  -o dist/hix-specification.pdf

echo "==> DOCX"
pandoc "${pages[@]}" \
  --from=gfm --reference-doc=theme/reference.docx \
  -M title="$title" -M author="Meddyg" -M date="$today" \
  --toc --toc-depth=3 --number-sections \
  -o dist/hix-specification.docx

echo "==> llms.txt"
python3 _scripts/llms.py "$work"

echo
echo "dist/hix-specification.pdf"
echo "dist/hix-specification.docx"
echo "dist/llms.txt"
echo "dist/llms-full.txt"
echo "dist/md/            one Markdown file per page"
