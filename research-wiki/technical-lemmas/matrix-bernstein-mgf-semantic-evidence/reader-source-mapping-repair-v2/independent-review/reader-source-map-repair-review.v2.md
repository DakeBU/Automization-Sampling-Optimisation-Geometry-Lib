# Independent review of the exact reader/source-map repair v2

Reviewer: `mgf_fresh_source_5b7e`.
Decision: **ACCEPTED for this versioned authored reader/source-map repair.**

This accepts the corrected stored mathematical prose, source correspondence and exact locators at the already reviewed single-matrix MGF layer. It is not a theorem repair, canonical round-trip verdict, native/build acceptance, renderer/runtime acceptance, publication transition or whole-consumer completion.

## Exact inputs actually read

| Candidate file | SHA-256 |
| --- | --- |
| `repair-proposal.v2.json` | `0a5139cf4b55fcbb09ec3ddfc9fbd220de1bada94c238b384600a072550775d5` |
| `lesson.v2.json` | `d88b96ad5397be27a9f234a6b3ac993a236267591dd4c922c7ba7aa1915f28c0` |
| `publication.v2.json` | `51580fc5033dcfb049ab5e1bc8754f42666f27bdedd65eda60029f40b2d96e1c` |
| `source-lean-map.authored-v2.json` | `0fd137f4acf020ffca3629be8875a030e80d54ca9101a630efd52422600ea74d` |

These files were copied from the specified candidate directory into this reviewer's `phase3_v2/originals/` and checked against the supplied hashes. The repair's `before` hashes match the frozen original v1 lesson/publication, and all `after` hashes match the actual v2 files.

The mathematical proof tree remains commit `4869db55d340cee39f0ba4d49fb0a7a4309ba2d6`. P remains SHA `b46bb5a3eabbcadf31fee93d48c1fbabf9b5b42cf717a8a17c8c8cfdd210a3f3`, and T remains SHA `42f372143ffe52e4372271d09fbc6b67391739f2fe2a5fbfffe6cd9fa586936e`.

## Exact scope of the change

The complete parsed diff against the archived v1 has only these paths:

- Lesson `/units/0/assumptions/2`.
- Lesson `/units/0/sources`.
- Lesson `/units/0/steps/3/source_attribution`.
- Publication `/items/0/assumptions/2`.
- Publication `/items/0/bindings/0/assumption_deltas/1/reason`.

All six step titles, mathematical explanations and formulas are unchanged. All six literal Lean fold strings, source paths, code locators and hashes are unchanged. The public mathematical statement/formula and remaining boundary are unchanged. The authored source-to-code map agrees exactly with each lesson step's source list and Lean locator.

The public publication still has exactly the four P assumption entries, equal to the first four P entries of the lesson. The private Gaussian assumptions remain in the lesson's separate private-application portion and have not become premises of generic P.

## Closure of the v1 findings

The corrected step-4 source map now directly locates:

| Original source anchor | Actual content and v2 role |
| --- | --- |
| `A3.Ex85` | The literal feature vector t_i and physical row gamma_i definitions. |
| `A3.SS2.p1.2` | Independent standard Gaussian row statement and B's row construction, with no conditioned replacement experiment. |
| `A3.SS2.p4.1` | The recalled exact midpoint-angle convention theta_i=(i-1/2)pi/d. |
| `A3.SS2.p10.1` | Exact L and row squared-radius definitions. |
| `A3.Ex107` | Only the inclusive-cutoff Kronecker formula for Y_i, now labelled at its actual scope. |
| `A3.SS2.p13.1` | Actual centering Z_i=Y_i-E Y_i. |
| `A3.Ex111` | Operator-norm bounds for Y_i and its actual expectation, no longer mislabelled as the centering definition. |
| `A3.Ex112` | The centered source radius R_star=2r(L+1)/d. |

Each newly supplied element was checked against the already pinned original HTML for its actual content, id, file hash, decoded-character interval, UTF8-byte interval, slice hash and containing LF lines. Its role matches that exact element. The lesson's direct `sources` links now locate the row/features, row law, threshold, centering and angle definitions, and Ex107's scope is narrowed to its actual Y_i formula.

Removing Ex108/109/110 from this step's approximate direct attribution is correct. Their original radial moment, bias and summed-expectation statements remain untouched, and the source mean/radius work still has its genuine canonical dependency drill-down. The repair does not erase those original obligations, claim new coverage of them, or turn background source facts into new public hypotheses.

The regularity explanation is now self-contained: Tropp section 2.2 is the mathematical source for the measurable/integrable expectation conditions; the exponential integrability is derived from the cap. The reader no longer uses a prior preproof admission as the explanation for those assumptions. The revised publication delta reason states the same mathematical justification.

The resulting map is self-contained and complete for the specific definitions, analytic adapters and actual use context represented by these six authored steps. It is not an exhaustive source-proof graph for C.2, and it makes no such claim.

## Independent checks

`diff-and-locator-checks.json` records 30 checks, all passing:

- Every changed field stays within the requested reader/source-map repair scope.
- Every literal fold remains exactly the corresponding immutable P/T slice.
- All code char/UTF8/line/start-column/end-column/hash locators remain correct and equal to the prior exact-fold locator document.
- The folds still reconstruct the complete P 121-line and T 159-line Git blobs with no gaps or duplication.
- Both public and private statement locators remain exact.
- All supplied source spans and PDF/source hashes validate.
- The source-to-code map matches the lesson step by step.
- Before/after input hashes and public-versus-private assumption scope validate.

The complete source and whole-code conclusions of phases 1-2 are unchanged: a real normalized one-matrix MGF and its original-law signed-cosine normalized private application, for all s>0 and including q=0. Tropp remains independently matching background rather than an explicit Gaussian-paper citation. No sum-MGF, complete variance chain, two-sided tail, Fact C.6, Lemma 4.4, main lower bound, runtime/site or purification acceptance is inferred.

## Preserved evidence and review limits

The v1 report is preserved unchanged at `phase3/authored-reader-review.final-v1.md`, SHA `4bd37799377af0eac7b99e908f2cb3e0d2ff263184b6fbe637d4b669e0c8d846`. Its revision request applies to those v1 bytes; this report accepts the exact successor v2 above and does not rewrite the historical finding.

The supplied authored source-map file contains a `preproof_admission` metadata field. I did not open the linked earlier file, verify that decision, or use it as source-truth evidence. This review relies on the original source, previously frozen independent code review and the actual v2 diff/locators.

ROOT reported an initial generator guard-assertion failure before production writes. The failed generator was not needed for the mathematical/source-map judgment and was not inspected; it is not negative mathematical evidence. The actual v2 output bytes were checked independently rather than accepted because a generator reported success.

No original candidate or production file was modified by this reviewer. No build, browser, network call, decoder reading, normal API transition or renderer execution occurred. Actual reader/runtime checks and the fresh canonical seven-slot comparison remain separate pending work.
