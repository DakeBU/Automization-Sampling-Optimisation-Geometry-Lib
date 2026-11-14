# Final held-metadata gate report — stopped on actual publication failure

Verifier: `psd_native_7b31`. Held HEAD: `7d6d61f298e882f54c4bc36b1fb67502d2801e77`. Unchanged mathematical candidate: `9964c33c4599f85d27dc8687e8bd6fdb5c44ff49`. Comparison base: `441d54ee96a6182374d2df3bf4d2fb096d5b7e14`.

**Result: FAIL / STOPPED AT PUBLICATION.** The first real gate exited 1. The other three gates were not executed. No gate was retried and no canonical file was modified. This is a metadata admission failure, not a new mathematical or source-fidelity judgment. It does not satisfy the four-zero-exit prerequisite for a subsequent independent normalV decision.

## Preflight facts

The exact held HEAD and tracked-clean working tree were confirmed before and after the attempted gate. Both S/P production Lean modules, the focused test, both authored lessons, both publication JSON files, `lean-toolchain` and `lake-manifest.json` (9 files) are byte-identical among the mathematical commit, held commit, actual working tree and this verifier's original native snapshot.

The actual Lean executable path, binary SHA-256, Lean 4.33.0 arm64 version, toolchain and manifest hashes match the original independent native snapshot. All 9 dependency HEADs still match both the manifest and native snapshot, and all dependency working trees are clean. Exact receipts and all hashes are in `preflight-results.json` and `receipts/`.

Only current selected admission metadata was read: both canonical audits have top-level `state="source-reviewed"` and child `source_review.state="accepted"`. The current S audit file SHA-256 is `f8c75ec84e532ccebf2d4ca736d340f4e53c99452c334a96b8a0f5c5e1c86401`; P's is `49884675030b178d6c085df74a1b3be64297f8553c5ae40c41a623b7d16dc509`. These are existing admission states, not this verifier's source verdict. Native compilation, browser checks and source mathematics were not rerun.

## Exact real gate outcome

| Gate | Actual invocation | Result |
| --- | --- | --- |
| publication | `python3 -B tools/astis_publication.py check --base 441d54ee96a6182374d2df3bf4d2fb096d5b7e14` | executed once, exit **1** |
| semantic | `python3 -B tools/astis_semantic_roundtrip.py check` | **NOT RUN** after gate 1 failure |
| contributor | `python3 -B tools/astis_contributor_contract.py check --base 441d54ee96a6182374d2df3bf4d2fb096d5b7e14` | **NOT RUN** after gate 1 failure |
| frontier | `python3 -B tools/astis_frontier_cells.py check` | **NOT RUN** after gate 1 failure |

The publication gate's stdout is empty. Its complete original stderr is:

```text
AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumSourceMatrixVariance.actual_source_truncated_matrix_second_moments: Frontier Cell canonical declaration does not match
```

Its actual receipt is `receipts/20261112T160717443736Z-FINAL-GATE-publication.json`, with the separate original `.stdout` and `.stderr` files beside it. Both command HEAD observations are the exact held HEAD. `gate-results.json` has only this single actual gate record; absent gates are not fabricated as successful or failed executions.

The sequential driver deliberately stops at the first gate failure. ROOT and the separately assigned normal verifier were immediately informed of the actual failure and missing four-zero-exit condition. This verifier did not investigate or repair canonical metadata after the failure.

## Preserved verifier implementation failure

Before any real gate ran, the original local `preflight.py` incorrectly asserted that the top-level audit state was `accepted`. It failed after all source/environment comparisons had already succeeded. The actual schema puts `accepted` in `source_review.state` and uses `source-reviewed` at the top level.

This is explicitly classified `IMPLEMENTATION_FAILED`, scoped to this verifier's preflight assertion. The original script and its raw failing driver receipt `receipts/20261112T160557119162Z-preflight-driver.json` remain unchanged. `selected-admission-schema` records the actual schema. `complete_preflight.py` validates the correct two-level states and rechecks the already captured successful preflight receipts and their raw hashes, rather than repeating the environment/build checks. The corrected preflight passed before the real gate was attempted. `preflight-implementation-failure-diagnosis.json` preserves this distinction. This phase is not described as having zero failures.

## Custody and boundary

All phase scripts, successful and failed receipts, raw stdout/stderr, effective environments, argv/cwd/HEAD/exit metadata, preflight facts, report and seal are inside this new `held-gates/` phase directory. The portable manifest maps each original to `research-wiki/technical-lemmas/real-matrix-positive-integral-semantic-evidence/native-review/psd_native_7b31/held-gates/` with exact source, destination, byte count and SHA-256. The final manifest/seal generation envelope is excluded from recursive self-hashing and is separately transferable.

The previous native report, originals manifest and seal hashes were independently rechecked unchanged. No previous sealed native artifact was edited. No native/browser rerun, full site build, global graph check, root Tests, source re-review, state transition, normalV, publication, T/R9 or whole-Goal credit was performed or granted.

The phase is stopped and sealed with a real failed gate. A future repaired HEAD would require a separate explicit phase; this phase's failure must remain intact.
