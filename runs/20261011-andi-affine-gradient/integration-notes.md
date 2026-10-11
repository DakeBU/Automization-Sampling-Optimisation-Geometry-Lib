# Affine gradient prerequisite — recoverable local checkpoint

Owner: `andi-affine-root`; contribution branch: `codex/andi-boumal-affine-gradient`.
Parent main: `c05de12e6a8ca7af8ce2df8608836f8d4e90f617`.

One canonical theorem derives the genuine gradient of `v ↦ f(a + v)` on a
complete real subspace with inherited inner product. It projects the ambient
gradient into the direction space. The translation is never added to the
gradient vector. The statement seal predates the proof and the independent
source-only topology review predates implementation.

Focused checks passed on Lean 4.33.0 / pinned Mathlib
`db584cd6d46c92f209a44c0f1c829460d327499d`:

- `lake build AutoSamplingTheory.TechnicalLemmas.Geometry.AffineGradient`
- `lake build Tests.Shared.AffineGradient`: actual translated linear objective
  and elimination of an ambient normal gradient.
- `#print axioms`: only `propext`, `Classical.choice`, `Quot.sound`.

This checkpoint is **locally compiled, review pending**, not independently
verified or ready to merge. Publication binds the theorem as a **prerequisite**
for Boumal §3.8; no Proposition 3.61 proof progress is awarded. The Hilbert-space
and pointwise-regularity generalizations are explicit. Nonlinear tangent-space
identification, differential restriction, extension independence, and smooth
gradient fields remain open. No unanchored Chewi consumer is claimed.

Independent decoder and source review evidence will be saved from real runs.
The audit is honestly `draft` at this checkpoint. Reader/graph rendering,
visual inspection, strict changed-declaration gates and the full ASTIS gate
are pending.

The existing global stabilization lane belongs to
`ASTIS-SA-20261005-SPHMCImplementedPhaseKernel`. Consequently this owner has not
changed shared root imports, `Tests.lean`, Registry or canonical site/graph
aggregations. Before final integration the sole stabilization owner must add
`import Tests.Shared.AffineGradient` to `Tests.lean` (and the shared module to
the appropriate umbrella), then run the full gates. A standalone green build
does not mean root CI exercises the test.

The pre-existing `.DS_Store` files and optimisation reuse-audit note are
preserved and excluded from this contribution.

## Independent review checkpoint

The anonymous decoder `/root/affine_blind_decoder` received only the statement
and approved definition context. The anti-anchored source/mathematical reviewer
`/root/affine_source_proof_review` inspected the official source, exact module,
candidate lesson and blind reconstruction; it independently compiled the tests
and checked the production/test bytes against `943666064`.

Actual packets and outputs are retained here, with canonical input/output
hashes and explicit digest boundaries. The review accepts the **affine
prerequisite only**. Its full-source verdict is `domain-mismatch`, and three
blocking deltas forbid full Proposition 3.61 equivalence/completion. No repairs
to Boumal, historical evidence or exact/equivalent verdict were fabricated.
The reviewer itself appended `VERIFIED` to the SAU ledger. Semantic and
diff-aware publication gates passed; this does not confer source assimilation.

The source-only topology review also located a concrete application in Boumal
§2.1, printed4–5: affine-constrained localization. A feasible base point and
the actual objective consumer remain separate work; no Chewi consumer has
been invented.

## Actual reader inspection and remaining integration work

Opened generated `libraries/riemannian-optimization/chapter-03.html` in the
browser. The formula and three mathematical proof steps render legibly;
statement/proof disclosures begin closed; unfolding reveals the exact theorem
and scoped-context module link. The source/hypothesis differences are visible.

The shared renderer still puts the exact Lean statement after the proof, while
the user requires it directly below the mathematical statement. Per-step
disclosures presently contain correspondence explanations rather than exact
code slices. The chapter's introductory map is still generic workflow text,
not a mathematical knowledge map. These are genuine reader delivery gaps,
reserved for the single stabilization lane; no `PUBLISHED` or `PURIFIED`
status is claimed. Do not merely set those flags to bypass this inspection.

Root aggregation must import the focused test and shared module before final
integration. Local focused compilation, independent verification and a green
metadata gate do not erase that missing CI coverage. The full root gate is
running against the current root coverage; it must be distinguished from
integration of this new module. Generated `_site/` files are preview outputs
and are not committed.

## Gate and graph closeout for this verified checkpoint

`tools/astis.py check` completed successfully on `c69b25b78`: the main library,
root `Tests` (9425 jobs), pinned ATLAS check (36469 declarations / 26 books)
and forbidden-closure scan passed. The new focused test had already passed
separately, twice including the independent reviewer. **Its root import remains
pending**; the aggregate result does not claim that the root imports it.

Contributor contract (`--base origin/main`), Frontier Cell, semantic registry,
diff-aware publication, generated site and affected `graph-check` gates passed.
The Harness suite ran 296 tests: 284 passed, six Windows-only tests skipped,
and six localhost-service tests initially failed only because the sandbox
denied port binding. Those exact six were re-run with localhost permission and
all passed. No production fix or weakened assertion was used.

Actual graph inspection: searching the canonical declaration produced five
nodes and four edges. The declaration remains `partial` with “compiled badge
not inferred” until Registry/root integration. The audit inspector visibly
shows `FIDELITY-MISMATCH`, the real `domain-mismatch` verdict, all seven semantic
slots and three blockers against full-source equivalence. Module ownership is
solid; source correspondence is not a Lean dependency. No Functor edge was
invented. The graph's reference scan is explicitly incomplete; it is not an
exported, elaborated proof-dependency certificate.

The official source PDF checksum was captured after proof/review and is
recorded with that honest timing in `statement-seal.json`; no earlier checksum
is fabricated and the PDF itself is not distributed.

Next mathematical candidate: use genuine affine-restriction derivatives and
Mathlib's `HasGradientAt.congr_of_eventuallyEq` / `HasGradientAt.unique` to show
that agreeing neighborhood extensions have identical projected gradients.
First inspect existing interfaces and the source-independent graph for Boumal
Proposition3.35/(3.28); claim only a bounded, source-present consumer edge,
not full nonlinear Proposition3.61. This is a candidate, not a claimed SAU.

The overall Chewi/Boumal Goal stays active. This single verified interface does
not complete a chapter, either book, reader purification or repository integration.
