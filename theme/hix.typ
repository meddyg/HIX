// Typst theme for the hix specification PDF.
//
// pandoc's default typst template ends in `#show: doc => conf(...)`. Passing
// `-V template=theme/hix.typ` makes it import this file's `conf` instead of the
// built-in one, so the whole page design lives here and the template stays
// pandoc's own.

#let navy = rgb("#0e3a4f")
#let accent = rgb("#34799a")
#let rule = rgb("#c9d4da")
#let soft = rgb("#f2f6f8")

#let conf(
  title: none,
  subtitle: none,
  authors: (),
  keywords: (),
  date: none,
  lang: "en",
  region: "US",
  abstract: none,
  abstract-title: none,
  thanks: none,
  margin: (top: 2.6cm, bottom: 2.2cm, x: 2.3cm),
  paper: "a4",
  font: ("Liberation Sans",),
  fontsize: 10pt,
  mathfont: none,
  codefont: ("Liberation Mono",),
  linestretch: 1.2,
  sectionnumbering: "1.1.1",
  pagenumbering: "1",
  linkcolor: none,
  citecolor: none,
  filecolor: none,
  cols: 1,
  doc,
) = {
  set document(title: if title != none { title } else { "" })

  set text(font: font, size: fontsize, lang: lang, hyphenate: false)
  set par(justify: false, leading: 0.62em, spacing: 1.1em)
  show raw: set text(font: codefont, size: 0.92em)

  // ── cover ────────────────────────────────────────────────────────────────
  set page(paper: paper, margin: margin, header: none, footer: none)

  block(inset: (bottom: 2.4cm))[
    #image("../template-local/content/assets/images/logos/hix-logo.svg", width: 5.2cm)
  ]

  v(3.2cm)

  block(width: 100%)[
    #text(size: 30pt, weight: "bold", fill: navy)[#title]
    #if subtitle != none [
      #v(0.4cm)
      #text(size: 15pt, fill: accent)[#subtitle]
    ]
  ]

  v(0.9cm)
  line(length: 100%, stroke: 2pt + accent)
  v(0.5cm)

  grid(
    columns: (auto, 1fr),
    row-gutter: 0.42em,
    column-gutter: 1.1em,
    ..(
      ("Version", sys.inputs.at("version", default: "")),
      ("Status", sys.inputs.at("status", default: "")),
      ("Date", if date != none { date } else { "" }),
      ("Canonical", raw(sys.inputs.at("canonical", default: ""))),
    ).map(((k, v)) => (text(fill: accent, weight: "bold")[#k], [#v])).flatten()
  )

  v(1fr)

  block(
    width: 100%,
    fill: soft,
    inset: 12pt,
    radius: 2pt,
    stroke: (left: 3pt + accent),
    text(size: 9pt)[
      This specification describes an implementation of the IHE MHDS profile and
      the profiles it builds on. It is *not* an IHE publication, is not endorsed
      by IHE, and carries no normative authority of its own. The published IHE
      profiles remain the normative source.
    ],
  )

  v(0.6cm)
  text(size: 9pt, fill: accent)[#authors.map(a => a.name).join(", ")]

  pagebreak()

  // ── body ─────────────────────────────────────────────────────────────────
  set page(
    paper: paper,
    margin: margin,
    numbering: pagenumbering,
    header: context {
      let here-page = here().page()
      if here-page <= 1 { return }
      let heads = query(selector(heading.where(level: 1)).before(here()))
        .filter(h => h.numbering != none)
      let current = if heads.len() > 0 { heads.last().body } else { [] }
      set text(size: 8pt, fill: accent)
      grid(
        columns: (1fr, auto),
        align(left)[#title],
        align(right)[#current],
      )
      v(-0.42em)
      line(length: 100%, stroke: 0.5pt + rule)
    },
    footer: context {
      set text(size: 8.5pt, fill: accent)
      align(center)[#counter(page).display(pagenumbering)]
    },
  )
  counter(page).update(1)

  set heading(numbering: sectionnumbering)

  show heading: set text(fill: navy)
  show heading.where(level: 1): it => {
    pagebreak(weak: true)
    block(above: 0em, below: 1.1em)[
      #text(size: 21pt, weight: "bold")[#it]
      #v(-0.5em)
      #line(length: 100%, stroke: 1.5pt + accent)
    ]
  }
  show heading.where(level: 2): set text(size: 15pt)
  show heading.where(level: 3): set text(size: 12.5pt)
  show heading.where(level: 4): set text(size: 11pt)

  show link: set text(fill: accent)

  // Tables read like the `grid` class on the site: thin rules, shaded header.
  set table(stroke: 0.5pt + rule, inset: 7pt)
  show figure.where(kind: table): set align(left)
  show table: set align(left)
  show table.cell.where(y: 0): set text(weight: "bold", fill: navy)
  show table.cell.where(y: 0): set block(fill: soft)

  show outline.entry.where(level: 1): it => {
    v(0.5em, weak: true)
    text(weight: "bold", fill: navy)[#it]
  }

  doc
}
