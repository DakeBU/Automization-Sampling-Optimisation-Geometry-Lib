# Fact 12: first checked edge, not a query lower bound

The four subject readers and the source-first paper route were merged in PR #389
at `95322cd2c762e5969c560815a803c4e15a424007`; all five public entries returned
HTTP 200 with that deployed commit. Existing four-paper, Gaussian Complexity,
Optimisation and Bench ownership is unchanged (coordination issue #388).

## Mathematical delta

Zhou–Suzuki, arXiv:2611.05813v1, Section 6.4, Fact 12 / equation (60):
for nonnegative real `g,b` with `g+b>0`,
`b/(g+b) ≤ b+(1-sqrt(g))² ≤ b+(1-g)²`.
The sole declaration is
`AutoSamplingTheory.TechnicalLemmas.Analysis.NormalizedMass.bad_mass_ratio_bounds`.
It includes either individual zero case. The source's redundant `b≥0` premise
is retained and explained; no probability or moment premise was introduced.

The module and anonymous exact-proposition tests compiled independently at
`32c6bb6bedbedf05a5ae0e64794df019bf36440c` under Lean 4.33.0 and the pinned Mathlib.
The independent decoder and anti-anchored source review accepted all seven
semantic slots. Their original reports, hashes and reviewer-authored VERIFIED
transition are retained; this note is not a substitute certificate.

## Reader and graph placement

- Paper: `example-cases/samplewiki/companions/slc-lsi-query-complexity.html`.
- Focused proof: `proofs/source-slc-lsi-normalized-mass.html`.
- Generic owner: the existing Analysis technical-lemma layer, not a duplicate
  definition in a paper module or in Log-Concave Sampling.
- Graph: one exact declaration node, its module's solid `declares` edge,
  dashed source-correspondence edge to the paper and semantic-audit overlay.
  The planned Theorem 7 consumer is not a compiled Lean dependency.
- No new Functor transport: the conceptual-mirror audit is `none-found`.

The generated desktop/mobile proof screenshots and bounded graph screenshot
were actually inspected. Three readable formula steps, adjacent closed Lean
statement/proof, step-level Lean explanations and source assumptions were
exercised. The four subject entries and paper navigation also passed browser QA;
there was no MathJax error or page-wide horizontal overflow. Long graph names
wrap within the nodes. The red source outline remains a section-level outline,
not an exhaustive or compiled proof graph.

## Acceptance boundary and next work

Focused Lake build, independent direct compilation, semantic, publication,
contributor and Frontier Cell checks passed. The integration tree also passed
`python tools/astis.py check`: root Lake build (9283 jobs), root Tests (9634 jobs,
including the Registry count 609), pinned ATLAS inventory and fake-closure scan.
Final site/CI acceptance is recorded in the PR, not inferred from focused checks.
An initial uncached parallel root build exhausted local memory and was stopped;
only this worktree's build was stopped. The retry uses isolated copies of the
pinned dependency and existing build caches, with one Lean runtime thread.
No collaborator source, process or cache was modified.

This is one selected Registry leaf (609 entries after integration), not paper
completion. Theorem 7 still needs the actual normalizers, positivity, first and
second moments, measurable random variables and justified expectation step.
Theorems 4, 8 and 9, their real oracle algorithms, admissibility, warm-start
information and expected-cost conversion all remain open.

Next scheduling should inspect the actual Theorem 7 normalization/moment
consumer and its ready dependencies. Do not make those missing estimates public
hypotheses of the paper theorem or count a generic expectation wrapper as the
paper result. Recheck collaborator ownership before claiming its next Cell.
Post-merge purification and the Exposition Seal remain separate work.

## Post-merge receipt (2026-11-09)

PR #392 merged at `6c61cb13dcf3c96c7c4d84246327aa42e18a6746` after all six
exact-`c5a55a84` CI workflows passed. The merge tree is identical to that head.
Independent post-merge review accepted no-change purification and an Exposition
Seal, preserving the two source regions and all three reader moves. Its immutable
report is `runs/20261109-slc-lsi-fact12/postmerge-purification.json`.
The report explicitly distinguishes prior accepted graph/PNG evidence from the
now-stale generated graph in the follow-up Gaussian worktree. Regenerate the
follow-up tree before its own acceptance; do not call that staleness check a pass.
Fresh main deployment remains a separately observed event, not implied by merge.
