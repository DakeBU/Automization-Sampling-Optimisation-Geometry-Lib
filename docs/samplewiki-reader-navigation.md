# SampleWiki unified research-reader contract

The landing page is a directory, not a concatenation of every project update.
Its primary, immediately visible entry is **Browse sampling regimes**: the seven
canonical assumption/oracle/accuracy settings. Do not fold this directory or
rename it "other" regimes. Specific papers/case studies come below it as
selected research projects. The sidebar follows the same order. Proof-work
scheduling priority is not reader-navigation priority.
SampleWiki itself is the home of Sampling research problems and new results.
Do not add another researcher-facing `Frontier`, `Companion-paper frontiers`,
or `Sampling papers` level. All source cases, including Gaussian Complexity,
belong to the same directory. The active four-paper scheduling order comes from
`execution.phase_order` in `website/content/samplewiki_companion_frontiers.json`;
it determines ordering, never library membership or exclusive visibility.
`reader_label`, `reader_summary` and `reader_links` are presentation only.
Keep the 34 source-index cases and their source/proof boundaries intact.
Quantum/PDE state preparation belongs to its own library, not this directory.
Legacy frontier/companion index URLs redirect to the single SampleWiki home.
Shared foundations and textbook extended chapters remain linked lower-level
homes for reusable lemmas, not competing classifications for a research result.
The generated textbook research-extension shelf links the existing reviewed
publication bindings, exact declaration graph locations and chapter reading
contexts. These are navigation/source overlays, never new Lean dependency
edges, source-text chapter theorems or chapter-completion credit. Keep proofs
in the canonical authored lesson; do not duplicate them to obtain placement.

Each paper has three depths:

1. A short introduction and source statements, with assumptions and rendered
   mathematics. Supporting statements and source conventions can be expanded.
2. Source-linked calculations, initially folded. Each step has its own adjacent
   Lean disclosure. A source proof route is not a completed Lean proof.
3. A compact index of source-mapped declarations and independent reviews,
   projected from the existing publication bindings. Link each item to its
   focused source/proof reader; do not embed hundreds of full proof units in a
   closed disclosure. Hidden DOM still loads and renders its formulas. Every
   focused reader retains the complete source, assumption ledger, authored
   formula proof, semantic evidence and adjacent folded Lean. The static gate
   checks all targets; browser checks exercise representative full readers.

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
- Actually inspect affected research pages: MathJax output/errors, statement/proof
  navigation, an adjacent Lean fold and the reviewed-work index. Check the
  narrow single-column layout and reset temporary viewport overrides.
- Save the actual screenshot and report its scope. Link/static validation alone
  is not evidence that formulas or hierarchy render correctly in a browser.

This is a presentation contract, not an additional cycle, theorem registry,
review role or publication gate duplicating the existing protocol.
