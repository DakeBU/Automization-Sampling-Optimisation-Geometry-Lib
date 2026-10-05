# Optimisation contributor protocol audit

Current-version audit, 2026-09-14. Remote baseline `ba5a58c`; current integration includes the still-unpublished uniform regularization result. No historical worker execution is reconstructed or certified.

## Scope and findings

Git-touched production modules for author `andyjm3`, excluding aggregators and Registry metadata, contain 44 public declarations (43 theorems and one interpreter definition), matching all 44 optimisation publication bindings across 21 source items. This is contribution scope, not a claim that every original proof was authored by this contributor. It includes the earlier reused first-order result.

- All 44 currently have authored declaration lessons and publication bindings. No missing current lesson or source mapping was found.
- Before this audit, 42 had retained decoder and source-review artifacts with matching raw hashes, packet hashes and current binding/context hashes. The independent historical provenance report records its evidentiary limits; hashes do not prove an unretained actor session occurred.
- Two StrongConvexFirstOrder declarations retain `legacy_audit_debt` tied to the exact historical module hash and migration base. Historical Lean/maintainer/CI review is not relabelled as a blind semantic round trip.
- All 44 lacked the newly introduced explicit `reuse_plan`, `reader_contract`, and `graph_contribution` fields. Those fields are recorded now with their current commit and migration scope. Existing search evidence is retained, not claimed as a newly executed upstream search. Planned source/frontier consumers remain distinct from reviewed Lean consumers.
- The common reader grouped all assumption comparisons before all lessons. It now keeps each declaration’s proof, closed Lean statement/proof, assumption comparison, semantic evidence and external provenance adjacent. All source chapters using this shared renderer receive the same behavior; no optimisation-only rendering path was introduced.
- Latest fetched main did not contain `.agents/prompts/collaborator-contribution.md`. AGENTS.md, CONTRIBUTING.md, contributor-codex-contract.md and theorem-publication-protocol.md were read. The user-provided historical-debt instruction governs the missing prompt’s relevant scope.

Historical snapshot check: at each declaration’s first recorded code commit, 4/44 lacked its current-path lesson and 17/44 lacked its current publication binding. These are explicitly intermediate code snapshots, not claims that a merged release was approved without checks. The exact commit/path/presence flags are retained in `inventory.json`; subsequent admission evidence is assessed separately. No missing snapshot is filled with an invented historical worker record.

## Current remediation and limits

The two new audits `ASTIS-RT-ANDI-CURRENT-FirstOrder` and `ASTIS-RT-ANDI-CURRENT-GradientMonotonicity` are current-version runs. Historical `legacy_audit_debt` remains visible separately. Distinct current workers `legacy_current_blind` and `legacy_current_source` completed both new audits. The reviewer accepted each scoped proof edge, with `lean-weakened-conclusion` against the full source equivalence. The exact Chewi source and pinned Optlib source were inspected. These current reviews are not backdated. Current aggregate and site acceptance passed; final independent integration review is recorded below. The original Lean proof files and authored mathematical lessons are unchanged.

The 42 existing accepted audit payloads are reused unchanged. No source-complete chapter status is inferred from compilation, an audit, a metadata migration or a graph edge. Solid graph edges remain module/import structure; scanner/source/semantic overlays remain dashed. The publication migration discovers no new conceptual transport and preserves the Discovery Ledger and Functor Hypergraph.

## Declaration inventory

All rows have a current lesson and publication binding. Original history is retained in `runs/semantic-roundtrip/andi-opt-contributor-audit/inventory.json`. “Retained audit” means repository-backed matching evidence, not retroactive certification of historical sessions.

| Declaration | First declaration commit | Audit at start |
|---|---|---|
| `ConvexGradientGapSharpness.quadratic_gap_lower_bound` | `001c58d3` | retained audit |
| `ConvexSmoothGradient.gradient_gap_sq_le_bregman` | `04ad482f` | retained audit |
| `ConvexSmoothGradient.gradient_cocoercive` | `04ad482f` | retained audit |
| `ConvexSmoothGradient.gradient_lipschitz` | `04ad482f` | retained audit |
| `ConvexityC1.sub_eq_integral_gradient` | `7616533a` | retained audit |
| `ConvexityC1.strongConvexOn_univ_of_gradient_mono_integral` | `7616533a` | retained audit |
| `ConvexityC1.convexity_equivalences` | `7616533a` | retained audit |
| `ConvexityC2.gradient_sub_inner_eq_integral_fderiv2` | `724e90f5` | retained audit |
| `ConvexityC2.gradient_mono_iff_fderiv2_lower` | `724e90f5` | retained audit |
| `ConvexityC2.strongConvexOn_iff_fderiv2_lower` | `724e90f5` | retained audit |
| `GradientDescentBasic.gradient_step_descent_of_quadratic_upper_bound` | `16dcffe4` | retained audit |
| `GradientDescentComplexity.distance_le_of_log_bound` | `e5d9ad0d` | retained audit |
| `GradientDescentContraction.gradient_step_contraction` | `b965cafb` | retained audit |
| `GradientDescentContraction.gradient_descent_distance_bound` | `b965cafb` | retained audit |
| `GradientDescentOptimalStep.gradient_step_endpoint_bound` | `4faed08f` | retained audit |
| `GradientDescentOptimalStep.optimal_gradient_step` | `4faed08f` | retained audit |
| `GradientDescentPL.gradient_descent_pl_value_bound` | `16dcffe4` | retained audit |
| `GradientDescentRates.convex_value_le` | `e48916e8` | retained audit |
| `GradientDescentRates.strongly_convex_value_le` | `e48916e8` | retained audit |
| `GradientDescentSharpness.exists_quadratic_worst_case` | `b6bac3b1` | retained audit |
| `GradientDescentStationarity.gradient_descent_sum_sq_bound` | `c592c86b` | retained audit |
| `GradientDescentStationarity.exists_gradient_descent_norm_le` | `c592c86b` | retained audit |
| `GradientDescentValue.gradient_step_energy_bound` | `417d096d` | retained audit |
| `GradientDescentValue.gradient_descent_weighted_value_bound` | `417d096d` | retained audit |
| `GradientFlowContraction.norm_sub_le` | `262ceaf5` | retained audit |
| `GradientFlowLastIterate.lyapunov_and_rates` | `98b2ee7d` | retained audit |
| `GradientFlowPL.dissipation_and_decay` | `72b56d03` | retained audit |
| `GradientFlowStationarity.exists_min_norm_le` | `ca8905c3` | retained audit |
| `GradientFlowValue.value_le` | `e15a55bf` | retained audit |
| `QuadraticGradientDescent.quadratic_gradient_iterate` | `14b1bcff` | retained audit |
| `QuadraticGradientDescent.quadratic_eigenmode` | `14b1bcff` | retained audit |
| `QuadraticRegularizationFirstOrder.curvature_gradient_and_smoothness` | `1cd2154e` | retained audit |
| `QuadraticRegularizationOracle.run` | `d6b012ce` | retained audit |
| `QuadraticRegularizationOracle.simulate_regularized` | `d6b012ce` | retained audit |
| `QuadraticRegularizationTransfer.exists_minimizer_radius_and_accuracy` | `6a15c4f8` | retained audit |
| `RestartLogComplexity.logarithmic_accuracy_and_cost` | `2700b79d` | retained audit |
| `RestartReduction.radius_accuracy_and_cost` | `1dd6f2a1` | retained audit |
| `SmoothnessEquivalences.upper_model_iff_gradient_upper` | `54349443` | retained audit |
| `SmoothnessEquivalences.upper_model_iff_fderiv2_upper` | `54349443` | retained audit |
| `StrongConvexFirstOrder.firstOrder_lower_bound_of_strongConvexOn` | `6b132f97` | legacy_audit_debt |
| `StrongConvexFirstOrder.gradient_inner_lower_bound_of_strongConvexOn` | `b75159d2` | legacy_audit_debt |
| `StrongConvexGradientConverse.strongConvexOn_of_gradient_inner_lower_bound` | `e84cd69e` | retained audit |
| `StrongConvexPLPullback.exists_minimizer_and_pl` | `7dc67252` | retained audit |
| `UniformRegularization.uniform_accuracy_and_query_bound` | `f13b4aa0` | retained audit |

## Acceptance evidence

- Canonical `website/scripts/lean_gate.py` completed the full ASTIS gate at `4bbdc7e0e3ffde53821a8aff0289fc5197c9e904`, source digest `17a8cf47b9a46dd9a5c45d715db223c2373223d743a54574a4bbe6848cf3747f`; 9248 Lean jobs. Root `lake build Tests` also passed at this current source state. Exact gate artifact is retained alongside the audit evidence.
- Publication PASS94 source items; semantic PASS121 audits/8 repairs; Frontier PASS127 cells. Contributor contract passed both the actual diff and an explicit all44-target audit. The 42 publication regression tests passed, including per-proof condition association, closed Lean, retained historical debt and nested-repair-safe boundaries.
- Full Harness suite PASS257 tests (6 configured skips) using the pinned Lean PATH and local test-server permissions. Initial sandbox port failures and a missing-toolchain-PATH503 were diagnosed and resolved; no tests were disabled or weakened.
- Site build/check PASS:12 chapters,437 compiled local Registry leaves,716 modules,4027 declarations,77 reviewed teaching declarations. Mechanical `graph_report` passed for all44 optimisation cells. Existing scanned links remain dashed and incomplete; chapter placements remain partial.
- Root actually inspected the Chapter1.3 reference and the changed Chapter1 source/formulas/proof/closed Lean/own assumption ledger/current-vs-historical review at1280x900 and390x844. Live DOM verified matching lesson/comparison counts in Chapters1–4:11/6/20/7 (44 total), with no association mismatch observed in the checked blocks. No MathJax errors were observed; long tables/equations use existing local scroll containers rather than overflowing the page. The Chapter4 uniform reduction was also visually checked with its formula→closedLean→assumption order.
- Root inspected the first-order graph focus:52 nodes/101 edges/14 highlighted direct relations, the dashed current-audit overlay and compiled selected declaration. Dense overview labels require existing zoom; mobile selected-node details wrap at390px. Desktop/mobile page widths matched viewport1280/390. This is representative visual inspection plus all44 mechanical graph checks, not a claim of44 separate screenshot reviews.
- Preservation check passed:unchanged Lean, all authored mathematical lessons,42 previous audits, historical debt objects, source obligations, append-only ledgers and shared graph-family truth. Only the two new current audit links were added to the existing source item. Cell migration is additive and explicitly dated to this current audit.
- Independent historical provenance reviewer:`pl_pullback_review`; independent shared-renderer reviewer:`uniform_source`; fresh decoder:`legacy_current_blind`; fresh source reviewer:`legacy_current_source`. The exact pinned Optlib source was inspected during the new review; no new upstream code was imported.
- Final independent integration review accepted the frozen candidate and evidence-only closeout, with no unresolved findings; retained as `runs/semantic-roundtrip/andi-opt-contributor-audit/integration-review.json`. No claim of a historical encoder/decoder run has been added.

Integrated and pushed to main at `5e469a7617914272b003409345145d8a74845753` under standing user authorization, together with the previously reviewed uniform regularization advance. This is the publication receipt, not a historical review backfill. Remote CI/deployment remains distinct from the passed local gates.

## Alignment with canonical collaborator bootstrap — 2026-09-14

Working-tree candidate based on `6a09b64d294540aa6b05de287de3342906b74716`.
The earlier uncommitted 13-file strict-mode/hook draft was backed up with
per-file SHA-256 verification before a safe fast-forward from `d08fd4f8`.
That draft was not published. Its installed local hook settings were removed;
no collaborator files were overwritten. The upstream AGENTS, CONTRIBUTING,
collaborator/optimisation prompts, theorem-publication protocol and root ASTIS
check remain unchanged by this candidate.

The retained repair has five files: `tools/astis_contributor_contract.py`,
`tools/tests/test_astis_contributor_contract.py`,
`.github/workflows/contributor-contract.yml`,
`docs/contributor-codex-contract.md`, and this existing receipt. It keeps the
canonical `--base` / `--ci` interface with no `--strict` flag or local push hook.
It rejects a missing comparison scope, reports an empty mathematical scope as
N/A, selects metadata-only changes including deletions, and tests this in CI.
The small documentation correction places `reader_contract` in the bound
Frontier Cell, matching the implementation. Reader ordering is unchanged.

| Required report | Result |
|---|---|
| Source statements | N/A: tool/protocol repair; no textbook/paper statement changed. |
| Lean declarations | None added, changed or generalized; no theorem/SAU progress claimed. |
| Hidden/API-only assumptions | No mathematical assumption changes. |
| External dependencies | Existing Python/Git and production/publication inventory APIs; no Lean or package dependency change. |
| Semantic and independent review | Existing registry and publication checks passed; no new worker runs were needed or fabricated. |
| Reuse and consumers | Existing `changed_declarations` inventory reused; contributor CLI and CI consume the same metadata scope validator. No new Lean helper. |
| Lean/Overview/Functor graphs | No graph/reader facts changed. Site generation and graph/site checks passed; no new visual review claimed. |
| Boundary/debt | Incremental contract success is not full historical compliance. The previously identified 72 SampleWiki metadata gaps and two historical audit records remain unchanged. The new CI workflow has not yet run remotely. |

Validation on this local candidate:

- Contributor `check --base 6a09b64d294540aa6b05de287de3342906b74716` and
  `check --ci` with that `PUBLICATION_BASE`: exit 0, explicitly N/A mathematical
  scope (0 declarations / 0 cells), not a whole-inventory PASS.
- `python3 tools/astis.py harness-test`: PASS, 275 tests, 6 platform skips,
  including 18 new scope regressions; run with the required local-server
  permission and pinned Lean PATH.
- `python3 website/scripts/lean_gate.py`: PASS, canonical ASTIS check including
  full Lake build, root Tests, ATLAS memory and fake-closure checks. Current
  source-bound evidence is `.astis/site-lean-gate.json`.
- Publication check against `6a09b64d`: PASS, 94 source items; semantic check:
  PASS, 121 audits / 8 repairs; Frontier Cell check: PASS, 127 cells.
- Site build/check: PASS, 12 chapters, 437 compiled local leaves, 716 modules,
  4027 declarations and 77 reviewed teaching declarations.
- Workflow YAML parsing and `git diff --check`: PASS.

No commit, push or remote CI acceptance is claimed. Before any future push,
review the actual outgoing diff/base and rerun the relevant canonical checks.

### Final pre-push recheck

The user subsequently authorized review, commit and push. The reviewed base
remains `6a09b64d294540aa6b05de287de3342906b74716`. Final review found and fixed
one additional scope boundary: only the Frontier Cell loader excludes
underscore-prefixed/schema JSON names; lesson/publication files with those names
must still be checked. A regression now covers both cases.

The final candidate passed 276 Harness tests (6 platform skips; 19 new scope
regressions), the full canonical Lean/root Tests/ATLAS gate, publication (94
items), semantic registry (121 audits / 8 repairs), Frontier Cells (127), and
site generation/graph/site checks. Both contributor `--base` and `--ci` forms
reported the honest empty mathematical scope. Workflow YAML and whitespace
checks passed. The eight-part boundary report above remains unchanged: no Lean,
source, semantic-audit or graph metadata changed. This entry records pre-commit
validation; the resulting Git commit identifies the exact published five-file
candidate. Remote CI results are not inferred from these local checks.
