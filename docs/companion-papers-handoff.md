# Companion-paper formalization handoff

## Resumed checkpoint — 2026-09-13

The current project is **Automization-Sampling-Optimisation-Geometry-Lib**;
Samplinglib is the reader-facing library. The September 10 pause and counts below
are historical, not the current frontier. Main was safely updated to collaborator
commit `08b7eb3913ea7423f2cec34cfa1f68ac28ffd30c`. Preserve the pre-existing
line-ending-only modification to `TechnicalLemmas/Measure.lean`.

The current owner resumed the two-paper priority in this thread. One active Goal
remains; neither complete paper is proved. No detached ASTIS session is running.
Read current Frontier Cells and the bounded harness capsule rather than treating
the old thirteen-result count or old next-step description as live state.

Collaborator results now include actual parameterized proximal Gaussian estimator
construction, Gibbs position moments, and further recursive execution/finite-output
KL results. PBPS already includes its actual macroscopic representative. The old
claim that this representative still needs construction is superseded.

Current local packet: `ASTIS-SW-SPHMC-proximal-estimator-lipschitz`, with source
and proof blueprint `proof-blueprints/SPHMC-proximal-estimator-lipschitz.md`.
Focused compilation, including an actual zero-dimensional/eta=1/2 constructor
test, passes. Independent proof/source and commit-bound admission passed at
`4b75ac75c484c82385455d73b24d8e1dc60c9d41`; the source verdict is explicitly
`lean-strengthened-assumptions`, not unrestricted source equivalence. Local
integration passed root Tests (9218 jobs), canonical ASTIS check, publication,
site and graph checks. Root inspected rendered desktop/mobile proof and graph
PNGs. Exact evidence is in the cell and `runs/20260913-companion-priority/`.
Two subsequent safe GitHub fetches failed (connection reset, then port443
connection failure). Do not assume a push or deployment has occurred.

This packet derives actual proximal nonexpansiveness and estimator input bounds
with constants 1 and sqrt(eta). Its 0<eta<=1/2 domain is inherited from the
existing constructor, not a mathematical necessity or source correction.
Bias, Gaussian concentration, smoothing regularity, Picard accuracy and total
cost remain separate. The source-facing decoder/reviewer protocol remains required.

PBPS weighted compact-test identity is now compiled and independently VERIFIED
at `019b4d68024c0498e90402d8a6db35e51e87d1bc`: see
`ASTIS-SW-PBPS-closed-gradient-weak-identity`. It retains the **same closed-gradient
graph**, proves both integrabilities and extends the actual compact-test identity
by continuous L2 pairings. Focused tests pass (3032 jobs), including the real
gradient constructor on every member of its closure domain. Independent blind
and source review accepts it as an elaborated analytic prerequisite only.
The seven-step lesson includes formulas and separate collapsed Lean disclosures.
Exact local integration at `2c20567436ebbfe1351d4f01b4c94236f1c53366` passed
build9031, Tests9220, canonical ASTIS/ATLAS gates, site/graph checks and actual
desktop/mobile/graph visual review. The final independent integration record is
`runs/20260913-companion-priority/closed-gradient-weak.integration-admission.json`.
The local stabilization lane is released, not MERGED. Later evidence-only commits
do not claim a new gate execution; these acceptance results and the generated
site snapshot are pinned to the named mathematical integration commit. Before
remote delivery, fetch safely, check divergence and regenerate/gate the actual
delivery revision. Prior normal fetch and push attempts failed with GitHub
connection errors, not evidence of an authentication problem. Technical Registry
remains 425 compiled leaves; route publication inventory is a separate measure.

The next PBPS bridge is now independently VERIFIED at
`767058015387071c7d7907dbc5f3eeb293c11945`: see
`ASTIS-SW-PBPS-gradient-distributional`. It establishes local volume integrability
for both L2 representatives and the ordinary weak gradient identity against C1
compact tests, including both product integrabilities. The same D.closure is
retained. Focused PASS3033, independent full proof/lesson review and source-blind
round trip passed; source acceptance is for the authored prerequisite only.
The six-step reader lesson is `pbps-gradient-distributional`. Aggregate and
website acceptance must be read from the exact subsequent integration evidence;
proof admission alone does not assert that those gates ran.

The latest bounded, noninteractive HTTP/1.1 fetch also failed with a GitHub
low-speed timeout. No remote update, push or deployment is claimed; preserve
all local commits and fetch/check divergence before delivery.

Next PBPS dependency-ready candidate: embed genuine smooth compact tests into
the SAME closed-gradient domain and turn its existing weak resolvent identity
into the weighted divergence-form distributional PDE, using actual L2 pairing
integrabilities. Do not use exp(W)*psi as a C-infinity core test when W is only
C1/C2. That would require a separate test-domain extension. Reuse
WeightedGradientDistribution, ConditionalGradient and ConditionalResolvent. A gradient
graph core is not an operator core for D*D; elliptic regularity, operator-core
approximation, mean-zero resolvent limits, Poincare and macroscopic coercivity
must remain separate. Do not increase the source C2 hypothesis silently.

## Historical checkpoint — 2026-09-10

Updated: 2026-09-10. Project: **Auto-Sampling-Theory-In-Sleep (ASTIS)**.

The owner requested an immediate push and a pause because their usage allowance
is nearly exhausted. Do not interpret this pause as completion or a mathematical
blocker. This document is intended for collaborators' Codex/Claude sessions and
for reading directly through GitHub or ChatGPT.

## Exact checkpoint

- Branch: `main`.
- Latest mathematical proof commit:
  `51b3b91334b9d73e4741d1b8847a7576846edc3d`.
- Independent-admission/frontier commit:
  `ec33034d17061e8d91d3948dbf8e03d5ac4526ba`.
- This handoff is a later documentation-only commit. Use the actual current
  remote HEAD when beginning work; never reconstruct a SHA from an abbreviation.
- Preserve the owner's pre-existing local modification to
  `AutoSamplingTheory/TechnicalLemmas/Measure.lean`. It had no textual diff
  (line endings only), was not authored here and was not staged.
- No reset credit was used. No detached ASTIS process was started. The running
  foreground aggregate gate was explicitly interrupted at the owner's stop
  request; no local gate process is intentionally retained.

## Priority and honest completion boundary

Faithfully formalize the two pinned papers by Fan Chen, Sinho Chewi, Jianfeng Lu
and Matthew S. Zhang:

1. [PBPS, arXiv:2609.06905v1](https://arxiv.org/abs/2609.06905v1):
   *Accelerated High-Accuracy Sampling from a Warm Start via the Proximal
   Bouncy Particle Sampler*.
2. [SPHMC, arXiv:2609.06906v1](https://arxiv.org/abs/2609.06906v1):
   *Smoothed Picard Hamiltonian Monte Carlo*.

**Neither full paper is formalized.** Actual algorithms/processes, main
convergence/error theorems, and expected query costs for their actual inputs
remain open. Partial scalar or kernel facts do not establish those claims.
The older Chewi 8.4.1 representative/score frontier and all previous cycle
memory remain preserved; do not restart Cycle 26 from historical chat text.

The legacy Registry count remains **396**. There are now **13 separately
inventoried, focused-tested, independently reviewed companion/shared results**.
Do not add these numbers to manufacture a new Registry count, or confuse
declaration counts with completed paper theorems.

## What is available for reuse

Exact names, files, tests and admission evidence are in the linked Frontier
Cells and generated declaration inventory. The compact result sequence is:

| Result | Owning module / proof component |
|---|---|
| 1 | SPHMC `RecursiveCondition.contraction_bounds`: ill-conditioned scalar update |
| 2 | PBPS `GaussianReflection.reflection_preserves_augmentation` |
| 3 | SPHMC `RGOClosure.quadratic_tilt_tilt`: normalized quadratic tilt composition |
| 4 | `Measure.IsotropicGaussianDensity.map_sqrt_smul_stdGaussian_eq_withDensity` |
| 5 | PBPS `GaussianAugmentation.augmentation_eq_withDensity` |
| 6 | `Analysis.StrongConvexGibbsIntegrability.integrable_exp_neg_of_strongConvexOn` |
| 7 | `Analysis.HessianStrongConvexity.strongConvexOn_univ_of_fderiv2_lower` |
| 8 | PBPS `GibbsAugmentation.normalized_augmentation_density` |
| 9 | `Analysis.QuadraticRegularization.strongConvexOn_and_lipschitzWith_gradient_add_quadratic` |
| 10 | `Probability.KernelTotalVariation.abs_real_comp_sub_le` |
| 11 | `Probability.GaussianConditionalKernel.exists_tilted_isCondKernel` |
| 12 | SPHMC `RGOCalculus.rgo_calculus`: Lemma 6.4 source integration |
| 13 | SPHMC `RecursiveVariance.variance_update_bounds`: selected Lemma 6.6(ii) step |

Use `website/content/samplewiki_companion_frontiers.json` →
`execution.result_cells` to find the canonical records; this table is a
retrieval aid, not another completion-status source.

## Latest result: exact mathematical scope

Production:
`AutoSamplingTheory/ExampleCases/SmoothedPicardHMC/RecursiveVariance.lean`.

Test: `Tests/SmoothedPicardRecursiveVariance.lean`.

Exact declaration:
`AutoSamplingTheory.ExampleCases.SmoothedPicardHMC.RecursiveVariance.variance_update_bounds`.

For real `r ≥ 0` and `0 < h ≤ c`, define

\[
a=\frac{h+c}{1+r},\qquad r^+=r+a^{-1},\qquad
A^+=(r^+)^{-1},\qquad \rho=\frac{2c}{1+2c}.
\]

The theorem proves `r⁺ > 0`, `0 < A⁺ ≤ 2c`, `0 < ρ < 1`, and
`r > 0 → A⁺ ≤ ρ/r`. The proof uses

\[
A^+=\frac{t}{D},\quad t=h+c,\quad D=1+r+rt\ge1,
\qquad 2cD-rt(1+2c)=2c+r(2c-t)\ge0.
\]

Important boundaries:

- `r=0` represents the source's initial `A=∞`; then the updated parameter
  equals `h+c`. Real `0⁻¹=0` is never treated as infinity.
- “Variance” here is an RGO regularization parameter, **not Gibbs covariance**.
- The branch has already selected `τ=c`. Branch selection, persistence,
  sequences, termination, sampling error and cost are not conclusions.
- The source requires `c<1/4`; this scalar proof does not need it. This is
  explicitly recorded as a valid generalization, not permission to enlarge
  the algorithm's schedule.
- A genuine Gibbs consumer test uses the same `a,r⁺,w` with
  `RGOCalculus.rgo_calculus`, obtaining updated-target probability without
  supplying integrability, a normalizer or a probability premise.
- Production imports only Mathlib arithmetic; the Gibbs connection belongs
  in the consumer test, not in a fabricated production dependency.

The four-step English/formula lesson and per-statement/per-proof folded Lean
are driven by `website/content/declaration_lessons/sphmc-recursive-variance.json`
and `website/content/publications/sphmc-recursive-variance.json`.

## Verification and publication: do not conflate these

Completed for result 13:

- Focused `lake build Tests.SmoothedPicardRecursiveVariance`: PASS, 2945 jobs.
- Standard axioms only: `propext`, `Classical.choice`, `Quot.sound`.
- Independent mathematical/commit reviewer: `rgo_independent_verifier`.
- Source-blind decoder: `heatbath_exposition_research`.
- Independent source reviewer: `publication_gate_review`.
- Publication metadata check: PASS, 14 source items.
- Semantic registry check: PASS, 17 audits and one preserved older repair.
- Frontier Cell check: PASS, 25 cells.
- `git diff --check`: PASS.

Canonical cell:
`research-wiki/frontier-cells/ASTIS-SW-SPHMC-recursive-variance-contraction.json`.

Canonical audit: `ASTIS-RT-20260910-SPHMCRecursiveVariance` in
`research-wiki/semantic-roundtrip/registry.json`.

The reviewer accepted the **selected specialization**, with final verdict
`domain-mismatch` and `domains.relation=stronger-in-lean` because the formal
parameter range is genuinely broader. The original review and signed amendment
are both preserved in
`runs/20260910-companion-priority/recursive-variance.source-review-result.json`.
Do not relabel this unrestricted statement as globally source-equivalent.

Commit-bound evidence:
`runs/20260910-companion-priority/recursive-variance.commit-verification.json`.

**Pending for result 13 at the owner's stop request:** aggregate Lean/ASTIS
gate, source-bound site build/check, generated branch/reader visual inspection,
and confirmation of online deployment. The local final-gate command was
interrupted before it returned a pass. Do not reuse the old gate JSON as new
evidence.

The last confirmed published source is
`26eb51a602f9976a4eae769be1b811582951ec4a` (result 12).
Its GitHub site and formalization workflows both completed successfully.
Its site snapshot had 12 chapters, 546 modules and 3640 inventoried declarations;
those are the **previous release's** counts, not a new site-build claim.
The new push triggers the repository's normal CI/Pages workflow; inspect its
actual status before claiming result 13 is visible online.

## First actions for the next collaborator

1. Read `AGENTS.md`, then this handoff and the bounded current Frontier Cell.
   Follow the required substantive-advance and semantic-roundtrip skills.
2. Fetch safely; inspect branch, commit, status and incoming changes.
   Do not reset, clean, overwrite local edits or create a parallel clone.
3. Finish result 13's aggregate and publication checks before opening a new
   proof packet. Reuse unchanged source/decoder/reviewer hashes.
4. Inspect the affected proof reader and one-hop graph, including the positive
   parameter boundary and the disclosed source-domain difference.
5. Continue the next dependency-ready mathematical edge below.

Pinned toolchain: `leanprover/lean4:v4.33.0`.
Mathlib commit: `db584cd6d46c92f209a44c0f1c829460d327499d`.
On the owner's machine an inherited Lean 4.29.1 setting is wrong; explicitly
use the repository toolchain and a conservative two-thread build.

Run in the repository (Linux-compatible command forms):

```bash
lake build Tests.SmoothedPicardRecursiveVariance
python3 website/scripts/lean_gate.py
python3 tools/astis_publication.py check --base 0c5f911b4f39d7204aee2efe5ef8640c5649806e
python3 tools/astis_semantic_roundtrip.py check
python3 tools/astis_frontier_cells.py check
python3 -m py_compile tools/astis.py
python3 website/scripts/build_site.py
python3 tools/astis_publication.py graph-check --cell ASTIS-SW-SPHMC-recursive-variance-contraction
python3 website/scripts/check_site.py
git diff --check
```

The official site Lean gate runs `tools/astis.py check`, including aggregate
Lake/Tests and fake-closure checks, and generates real source/commit-bound
evidence. Freeze the candidate before running it; do not hand-edit its pass,
commit or digest, or rerun the whole build after every lesson sentence.

## Next mathematical edge, not yet proved

Use the actual Lemma 6.4 ratio update to establish persistence of the
well-conditioned regime, then derive the finite-depth threshold needed after
SPHMC equation (6.4). Preserve both regimes, schedule hypotheses, strict positive
precision after the first step, and exact stage indexing.

A bounded search found existing Mathlib `le_geom` and
`tendsto_pow_atTop_nhds_zero_of_lt_one` in
`Mathlib/Analysis/SpecificLimits/Basic.lean`; inspect exact signatures and reuse
them rather than formalizing geometric-sequence facts again. This is retrieval
evidence, **not** a frozen packet or a compiled recursion theorem.

Keep these red boundaries independent: recursive probability error, terminal
FORS algorithm/work, actual-input query costs, PBPS event-process
nonexplosion/invariance, discrete hypocoercivity and complete mixing guarantees.
TV proximity does not transfer unbounded expected costs.

Use one sole writer per bounded SAU, exact source anchors, early focused tests
and independent source/commit admission. Reuse local dependency slices; avoid
whole-site scans, full transcript replay, duplicate wrappers and graph-only
agents. Keep the full two-paper objective unfinished until it is actually proved.
