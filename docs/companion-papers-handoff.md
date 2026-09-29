# Companion-paper formalization handoff

## Shared progress checkpoint — 2026-09-19

The two-paper Goal is active. Neither complete paper or final sampling-complexity
theorem is formalized yet. Main contains 438 Registry leaves across the project,
not 438 completed paper theorems. PR310's local-L2 prerequisite is merged.

Latest SPHMC work is publicly pushed on `codex/sphmc-proximal-execution-20260918`
at `2a043a5d`: actual Algorithm D.2 execution and Lemma D.3's pointwise accuracy
and logarithmic gradient-query count, including measurable first stopping/output
and the final successful query. Focused compilation and independent source-blind
and source reviews passed. Its SAU is PROVED_LOCAL; commit-bound verification,
root/site integration and aggregate acceptance remain pending. This is not D.4's
expected run-wide cost or the full SPHMC theorem. See that branch's proof blueprint,
Frontier Cells and round-trip artifacts for exact evidence.

Remaining work includes PBPS process/operator/hypocoercivity and implementation
guarantees, SPHMC smoothing/concentration/Picard and sampling-error guarantees,
and actual-input expected costs and composition. No reliable completion date is
established. Do not substitute a calendar promise for dependency-level evidence.
The project author and organizer lists are maintained on the public citation and site surfaces;
primary-source author attribution remains preserved separately.

## Protocol refresh and continuation — 2026-09-18

The September 13 batch was successfully pushed to main at `9729cf5`; its failed-push
notes below are historical. This continuation safely fast-forwarded 47 commits
to `238ab415` and read the current AGENTS, CONTRIBUTING, collaborator bootstrap,
contributor contract, publication protocol and optimisation prompt. The new
incremental contributor gate, reuse_plan, reader_contract and graph_contribution
are binding; metadata-only changes are within scope too. Registry baseline: 437.
The unrelated pre-existing Measure.lean line-ending modification is preserved.

Issue #309 and branch `codex/pbps-local-l2-20260918` own the next single shared cell,
ASTIS-SHARED-gibbs-local-l2. At proof commit c856bb09c3940555fd7a48f467c01fde0ccff337,
WeightedLocalL2.lp_locallyMemLp_volume proves local volume-integrability of squared
norms and compact-restricted L2 for every Gibbs L2 representative, with only
continuous W and integrable exp(-W); the target is any normed additive group.
Focused Tests.WeightedLocalL2 passed3036 jobs/standard3 axioms. The test constructs
an actual same-operator resolvent and applies the leaf to u, its gradient and f,
retaining the weak PDE. Static independent proof/lesson review passed; fresh
source-blind reconstruction and anti-anchored source review are recorded under
runs/20260918-companion-priority. Read the current cell/audit for admission state,
not this checkpoint as a claim of acceptance. Five authored formula steps and
adjacent collapsed Lean are in the new gibbs-local-l2 lesson/publication.

The integration candidate `59807460bcccecf284d019bd86a8139be80449b9` passed
the canonical Lean/ASTIS gate (Tests: 9,250 jobs), 276 harness tests, publication,
contributor, semantic and Frontier Cell checks. Registry: **438** compiled leaves.
The site build/check passed with 12 chapters, 718 modules, 4,028 declarations and
77 reviewed teaching declarations. Root and the independent verifier inspected
desktop/mobile formula proofs and the local graph. Five proof steps have adjacent
folded Lean, six formulas render without errors, and graph ownership edges remain
distinct from source/audit overlays. Independent stabilization acceptance is in
`runs/20260918-companion-priority/gibbs-local-l2.integration-review.json`.
Any later receipt-only commit is not the revision on which these builds ran.
PR #310 subsequently passed remote Lean, reader and contributor CI and merged
as `bbd66fd17fe1670255abd2b9ed7b61bee227952f` on September 18. This is a merge
receipt, not a deployment-success or whole-paper-completion claim.

The app Goal was observed paused; no new Goal or detached harness was started.
Work here follows the existing two-paper objective. Neither paper is complete;
H2 regularity, operator core, Poincare and all other open paper boundaries remain.

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

Resumed SPHMC packet: `ASTIS-SW-SPHMC-proximal-estimator-lipschitz`, with source
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
The six-step reader lesson is `pbps-gradient-distributional`. Exact local
integration at `6d21910fa55d6b8e294abacafa613e0347d72293` passed build9032,
Tests9222, canonical ASTIS/ATLAS, site/graph and actual desktop/mobile/graph
visual checks. Independent acceptance and lane release are recorded in
`runs/20260913-companion-priority/gradient-distributional.integration-admission.json`.
The generated snapshot contains 12 chapters, 691 modules and 4012 indexed
declarations; technical Registry remains 425, a distinct curated metric.
Subsequent evidence-only commits do not assert a fresh gate or remote merge.

The latest bounded, noninteractive HTTP/1.1 fetch also failed with a GitHub
low-speed timeout. No remote update, push or deployment is claimed; preserve
all local commits and fetch/check divergence before delivery.

The weighted resolvent PDE bridge is now independently VERIFIED at
`86e334d2abd4f046ce9f7f069f5b133459a97308`: see
`ASTIS-SW-PBPS-resolvent-distributional`. Production constructs one actual
resolvent witness in the same gradient domain, proves the genuine compact smooth
test embedding and all three weighted-volume integrabilities, and retains its
all-domain equation and ordinary weak gradient. Focused PASS3035, full proof/
lesson review and independent blind/source acceptance passed. No separately
chosen conditional solution is definitionally identified; that would use
uniqueness. Root aggregate/publication acceptance is separate from this proof
commit and must be read from subsequent exact integration evidence.

Network recovered on the next bounded fetch. Collaborator main
`83a40eb8b8f50917845e3dce940973bccba08e82` adds three reviewed optimisation
gradient-flow results and updates technical Registry to428. It was merged at
`cf9e2de9986c0a54e0bb51b966b952d10cbfd436`, preserving both histories. The only
conflict was the append-only SAU ledger: both sides' exact record union and its
650-row count were checked before removing markers. Merged semantic registry
passes108 audits/7repairs and cells116. Earlier connection failures below/above
are historical; this fetch/merge does not itself assert a successful push or
deployment. The pre-existing Measure.lean modification remains untouched.

Final delivery candidate: `b4750e1d3922e43382b429240b87aea8a11adc2c` also preserves
the next four collaborator commits through `bce39f7` (normalized gradient-descent
rates). The lossless ledger union now has657 distinct rows. At this exact
candidate, the canonical gate passed build9037, Tests9232, ASTIS and ATLAS;
source digest `6121aa7d252c98f5fa18d9386d214164024d85e689d169de5b0c66783b7e3c6d`.
Publication check against bce39f7 passes91 source items; semantic checks pass110
audits/8repairs and Frontier Cells118. Site build/check passes12 chapters,
430 Registry leaves,701 modules,4018 indexed declarations and77 reviewed teaching
declarations. These are distinct inventory metrics, not completed-paper counts.
The unchanged resolvent lesson has six formula-proof steps with per-step collapsed
Lean; root and independent reviewer inspected desktop/mobile/graph PNGs at the
preceding f6479e4 candidate. That precise acceptance is persisted separately.

Remote delivery is still pending: the first ordinary push after this final merge
failed a15-second low-speed timeout; one bounded retry failed with connection
reset. No authentication failure, successful push or deployment is inferred.
Keep these local commits and use a safe fetch/divergence check before retrying.
Do not rerun unchanged global builds merely to update an evidence-only receipt.
The canonical gate above belongs to the named candidate, not later receipt commits.

Next PBPS dependency-ready candidate: establish local square integrability for
every Gibbs L2 representative, applying it to the same u,G,f before invoking any
L2 interior regularity. The bounded reviewed API route is in
`proof-blueprints/PBPS-resolvent-distributional.md`: squared-norm integrability,
positive inverse-weight local multiplication, compact restrictions, and explicit
representative measurability transfer. Keep the PDE in divergence form. Do not
use exp(W)*psi as a C-infinity core test when W is only C1/C2; that requires a
separate test-domain extension. A gradient
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
