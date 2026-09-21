# Health Information Exchange (HIX) Integration Guide

The HIX specification as a FHIR Implementation Guide: the HL7 IG Publisher
builds the site, and pandoc turns the same Markdown into PDF, Word and llms.txt.

## Requires

| | why |
| --- | --- |
| Java | runs the IG Publisher |
| Ruby + Jekyll | the publisher renders every page through Jekyll |
| SUSHI (`fsh-sushi`) | the publisher invokes it from `PATH`, so `pnpm dlx` will not do |
| pandoc | PDF, Word and the preview |
| Typst | the PDF engine pandoc drives |

## Commands

```sh
make tools     # downloads the publisher jar, once
make preview   # write with this            http://localhost:4000
make site      # build the site             dist/site/index.html
make docs      # PDF, DOCX, llms.txt        dist/
make all       # site + docs
make clean     # remove everything generated
```

Write against `make preview` (0.16s per page, reloads on save); verify with
`make site` (~30s), which is the build that counts.

The preview also marks what the page has gained, lost or had rewritten since
HEAD, word by word. The banner switches the marks off to go back to writing, and
switches the comparison to `main` to review the whole branch.

## Layout

```
input/pagecontent/   what you write
sushi-config.yaml    page order, titles, menu
template-local/      the site's look        theme/   the PDF and Word look
_scripts/            what the Makefile calls
dist/                what you publish       .work/   everything generated
```

## Authors

- Juan Esteban Sanchez
- Alejandro Benavides
