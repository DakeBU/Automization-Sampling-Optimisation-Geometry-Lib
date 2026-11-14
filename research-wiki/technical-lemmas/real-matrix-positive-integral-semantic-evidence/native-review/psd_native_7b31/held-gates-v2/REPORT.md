# Final held-metadata gates v2 — four actual zero exits

Verifier: `psd_native_7b31`. Held HEAD: `5f69ac83737e497210d8d8ad9628c45d83089458`. Parent failed held HEAD: `7d6d61f298e882f54c4bc36b1fb67502d2801e77`. Unchanged mathematical candidate: `9964c33c4599f85d27dc8687e8bd6fdb5c44ff49`. Gate comparison base: `441d54ee96a6182374d2df3bf4d2fb096d5b7e14`.

**Result: PASS for the four requested metadata gates on this exact held HEAD.** Publication, semantic, contributor and frontier were each executed exactly once in this v2 phase, in that order; all four actually exited 0, with empty stderr. This report grants no independent source-fidelity verdict, normalV, T/R9, serialized integration, full-site or whole-Goal credit.

## Held input and custody verification

The exact held HEAD, its direct parent `7d6d61f...`, and tracked-clean working tree were actually checked. After all four gates, HEAD was still the exact held HEAD and tracked status remained clean.

The sole modified existing tracked file is `research-wiki/frontier-cells/ASTIS-SW-GAUSSIAN-COMPLEXITY-source-matrix-variance.json`. A recursive JSON comparison verifies that its only changed value is `/shared_floor_audit/canonical_declaration`, restored from dependency S to the cell's own exact public P declaration:

```text
old: AutoSamplingTheory.TechnicalLemmas.Probability.RealMatrixPositiveIntegral.integral_posSemidef
new: AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumSourceMatrixVariance.actual_source_truncated_matrix_second_moments
```

Every other JSON value is unchanged, including status and reuse fields. The working file exactly matches the held-commit blob. The before/after committed bytes are preserved as raw `parent-C22` and `held-C22` receipts.

The other commit changes are additions: **171 v1 originals**, all actually hash/byte matched to this verifier's local sealed originals and post-seal envelope, plus the original pre-correction C22 snapshot and ROOT's failure/correction diagnosis. The pre-correction snapshot exactly equals the parent commit's C22 bytes. The full diff inventory is preserved without relying on the truncated console display; `preflight-results.json` lists every copied v1 artifact's actual SHA-256 and byte count.

Both S/P Lean modules, the focused test, both authored lessons, both publication JSON files, `lean-toolchain` and `lake-manifest.json` still exactly match the original native mathematical snapshot (9 files). Diff inventory confirms no production/author/source/decoder/manifest/ledger change in this metadata correction commit. The actual Lean executable path, binary SHA-256, Lean 4.33.0 arm64 version, toolchain and manifest hashes match that native snapshot. All 9 dependency HEADs match the fixed manifest and native snapshot; all 9 working trees are clean.

The selected source-admission files are unchanged from v1; both retain top-level `state="source-reviewed"` and child `source_review.state="accepted"`. They were checked only as current admission metadata. No source mathematics or reviewer verdict was re-derived. The original native seal and the v1 failure seal were rehashed unchanged. This verifier changed no canonical file.

## Actual gate results

| Order | Exact invocation | Exit | Raw receipt |
| --- | --- | --- | --- |
| 1 | `python3 -B tools/astis_publication.py check --base 441d54ee96a6182374d2df3bf4d2fb096d5b7e14` | **0** | `receipts/20261112T161317339945Z-FINAL-GATE-publication.json` |
| 2 | `python3 -B tools/astis_semantic_roundtrip.py check` | **0** | `receipts/20261112T161320607877Z-FINAL-GATE-semantic.json` |
| 3 | `python3 -B tools/astis_contributor_contract.py check --base 441d54ee96a6182374d2df3bf4d2fb096d5b7e14` | **0** | `receipts/20261112T161320886566Z-FINAL-GATE-contributor.json` |
| 4 | `python3 -B tools/astis_frontier_cells.py check` | **0** | `receipts/20261112T161323830871Z-FINAL-GATE-frontier.json` |

Every command's before and after HEAD is exactly `5f69ac83737e497210d8d8ad9628c45d83089458`. Each receipt records the real argv, cwd, effective environment, start/end timestamps, exit status, separate original stdout/stderr paths, byte counts and hashes. All raw files were rehashed before reporting.

The publication tool reports PASS for 386 source items, with legacy audit debt still explicit. The semantic tool reports a structurally valid registry of 468 audits and 8 repair proposals. The contributor tool resolves the exact requested base and held HEAD and identifies exactly the S/P declarations and their two cells, then reports PASS for affected metadata. The frontier tool reports protocol PASS for 466 registered cells. These are actual tool outputs and their protocol scope; they do not independently re-certify the mathematics or source fidelity of every historical record.

## Failure history retained

This success does **not** erase the prior failures or describe the overall history as failure-free:

1. At held v1 `7d6d61f...`, publication really exited 1 because ROOT's metadata update had pointed C22's own-publication canonical target at dependency S. Its exact error was `Frontier Cell canonical declaration does not match`. The v1 phase stopped immediately; the other three gates were never run there.
2. Before that real v1 gate, this verifier's local preflight script had incorrectly asserted top-level `audit.state == "accepted"`. The actual protocol uses top-level `source-reviewed` and child `source_review.state == "accepted"`. The original failing script, raw error, corrected preflight and `IMPLEMENTATION_FAILED` diagnosis remain in the sealed v1 originals.

The publication input actually changed in v2 through the single pointer repair, so publication was rechecked once. Semantic, contributor and frontier were run for the first time in this final held-gates sequence. No gate was retried within v2. No native compilation, kernel check, browser run or source mathematical review was repeated.

The sealed v1 result remains `FAIL_STOPPED_AT_PUBLICATION`, with seal SHA-256 `676e7ebdf582a7a87321937450dbd94dce7e3ccdfb161d9e2d48a4a8f1404320`. The original independent native seal remains `03dfe1607d2f63743999d17087070253fc05df0a5dafa48161d6974e812e8585`.

## Delivery and stop boundary

All v2 original scripts, preflight/custody results, complete receipts, raw outputs and final report are in this separate `held-gates-v2/` phase. The portable manifest maps every transferable original to `research-wiki/technical-lemmas/real-matrix-positive-integral-semantic-evidence/native-review/psd_native_7b31/held-gates-v2/` with exact source, destination, bytes and SHA-256. The manifest/seal generation's post-seal command receipt and raw output form a separately transferable envelope to avoid recursive self-hashing.

No full site/global graph/root Tests or state transition was run. The four-zero-exit fact may be consumed by the separately designated normal verifier, which must make its own authorized decision. This role does not perform normalV. The phase is now stopped and sealed.
