# Paper reader QA — 17 October 2026

Scope: SampleWiki landing page and the four priority companion pages; no
reviewed mathematical statement, authored proof lesson or source binding was
changed for presentation. This is a browser inspection, not a proof audit.

- Four direct paper cards precede secondary sampling and cross-library links.
  Quantum/PDE state preparation remains available in an initially closed fold.
- Paper sidebars link directly to all four readers. Source statements, proof
  routes and checked work have separate navigation. Proof links actually open
  their folded destination; checked-work navigation opens its compact index.
- PBPS:1200 rendered MathJax containers,0 errors; proof-route navigation opened
  the right four-step calculation, with all six adjacent Lean folds closed.
- SPHMC:977 containers,0 errors; source Wasserstein/query formula visually read.
- Gaussian Cloud:72 containers,0 errors; Section6 ledger expanded, eight rows
  retained, source-only red SVG and separate call/error ledgers visually read.
- Midpoint:44 containers,0 errors; separate upper/lower source statements and
  displayed upper bounds retained. Remaining ASCII prose notation was then
  given additional literal-only typesetting substitutions.
- One actual reviewed L2 proof was opened from the124-item PBPS index; full
  statement, assumptions, formulas, folded Lean and dedicated proof link remain.
  The dedicated reader has30 MathJax containers,0 errors; its first Lean step
  opens the exact source code, not a newly authored approximation.
- Desktop has no horizontal page overflow. Requested390x844 viewport override
  produced585 CSS-pixel width on this display; the paper cards became one
  column with no page overflow. Override reset. This is not a physical-phone or
  all-device certification.

Regression tests cover canonical execution-order projection, preservation of
the fifth source case, direct links, secondary folds, adjacent Lean, exact
source-card retention, escaping and canonical/late sidebar templates.
The static build, site link/status checker and contributor contract also pass.
Screenshots are retained with this chat's workspace, including the final
SampleWiki overview and focused L2 graph; no local absolute paths are published
in the generated site.

Known boundary: long checked-work indexes are deliberately collapsed and link
to focused readers; their ordering is still publication order, not a fully
curated pedagogical prerequisite tree. Source proof routes are outlines, not a
claim that every cited argument or any complete paper is formalized.
