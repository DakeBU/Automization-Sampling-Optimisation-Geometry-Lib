# SampleWiki paper-first reader contract

The landing page is a directory, not a concatenation of every project update.
Its first mathematical entry is the current paper route. The four-paper order
is projected from `execution.phase_order` in
`website/content/samplewiki_companion_frontiers.json`; `reader_label` and
`reader_summary` are presentation only. Keep all other source cases intact.
Cross-library pointers, including quantum/PDE state preparation, belong in
secondary closed disclosures rather than above the sampling papers.

Each paper has three depths:

1. A short introduction and source statements, with assumptions and rendered
   mathematics. Supporting statements and source conventions can be expanded.
2. Source-linked calculations, initially folded. Each step has its own adjacent
   Lean disclosure. A source proof route is not a completed Lean proof.
3. A compact index of source-mapped declarations and independent reviews,
   projected from the existing publication bindings. Expand one exact proof
   or follow its focused reader page; do not maintain a second status list.

The exact authored publication and declaration-lesson content is retained.
Navigation/layout changes must not rewrite reviewed proofs, expand statements,
merge red obligations or imply that a paper is complete. Source statement
notation may be typeset by a literal presentation substitution, never by an
unreviewed inference. Deep links reveal their folded target and ancestors.

Maintenance:

- Edit `samplewiki_navigation.py`, companion/reader generators and the small
  `samplewiki-paper-navigation.css`/`.js` assets, not generated HTML.
- Run `python -m unittest tools.tests.test_samplewiki_navigation
  tools.tests.test_samplewiki_companions tools.tests.test_samplewiki_reader_contract`
  as one command, followed by the canonical site build and `check_site.py`.
- Actually inspect all four paper pages: MathJax output/errors, statement/proof
  navigation, an adjacent Lean fold and the reviewed-work index. Check the
  narrow single-column layout and reset temporary viewport overrides.
- Save the actual screenshot and report its scope. Link/static validation alone
  is not evidence that formulas or hierarchy render correctly in a browser.

This is a presentation contract, not an additional cycle, theorem registry,
review role or publication gate duplicating the existing protocol.
