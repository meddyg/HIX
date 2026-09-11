# hix specification IG.
#
# Everything generated lands in dist/ (what you publish) or .work/ (scratch).
# fsh-generated/ and template/ are the IG Publisher's own; it will not put them
# anywhere else.

.DEFAULT_GOAL := help
.PHONY: help preview site docs all format tools clean

help:
	@echo "make preview   write, with live reload      http://localhost:4000"
	@echo "make site      build the site               dist/site/index.html"
	@echo "make docs      build PDF, DOCX, llms.txt    dist/"
	@echo "make all       site + docs"
	@echo "make format    format the pages             input/pagecontent/"
	@echo "make tools     download the IG Publisher    .work/tools/"
	@echo "make clean     remove everything generated"

preview:
	@_scripts/preview.py

site:
	@_scripts/build-site.sh

docs:
	@_scripts/build-docs.sh

all: site docs

# Fixes blank lines, list markers, heading and emphasis style, trailing spaces;
# reports what it cannot fix. The rules are in .markdownlint.jsonc.
format:
	@pnpm dlx markdownlint-cli2@0.23.2 --fix "input/pagecontent/**/*.md"

tools:
	@_scripts/update-publisher.sh

clean:   # keeps .work/tools -- the publisher jar is a 200 MB download
	rm -rf dist fsh-generated template input-cache output
	rm -rf .work/temp .work/qa .work/txcache .work/schemas
	rm -rf .work/fsh-generated .work/template
