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
