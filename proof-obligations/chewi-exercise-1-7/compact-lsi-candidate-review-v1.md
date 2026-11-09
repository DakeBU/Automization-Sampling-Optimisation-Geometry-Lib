# Compact-LSI candidate: independent local review

Verdict: **ACCEPT the local candidate; no repair finding.** This is a draft
evidence receipt by `agent-task:/root/compact_lsi_candidate_review`, not a
Source Seal, formal VERIFIED state, or claim of Exercise 1.7 completion.

Reviewed commit: `9cb00e7ab1652e3a343091de63e433ae1088b5d5`.
Baseline commit: `6c61cb13dcf3c96c7c4d84246327aa42e18a6746`.

| Inspected input | Git blob |
| --- | --- |
| Candidate `AutoSamplingTheory/TechnicalLemmas/FunctionalInequalities/LogSobolevCutoff.lean` | `3b7ca423679854a3e776f7bc016360251b04b470` |
| Candidate `AutoSamplingTheory/TechnicalLemmas/FunctionalInequalities/GaussianLogSobolev.lean` | `792f9f809a8614574d659cb5d1d2993b2e98efa4` |
| Candidate `Tests/Shared/LogSobolevCutoff.lean` | `58f027720cd7bc5abc082fe71ae1634f4f256b74` |
| Baseline `AutoSamplingTheory/TechnicalLemmas/FunctionalInequalities/GaussianLogSobolev.lean` | `d3c5cb6f91443d3371f279d6db828cc2bf3814c8` |
| `compact-lsi-extension-plan-v1.md` | `01464a6be006661f6f9db5808e4f6593fb0a0d51` |
| `compact-lsi-signatures-v1.lean.txt` | `217752efc0ab1a5dde81e3b37275f13e6509112e` |

The Gaussian public declaration, including its proof text, matches the
baseline after normalizing line endings. The moved cutoff region matches
after accounting for the new public visibility, removal of the unused
finite-dimensional scope, and the new documentation. A tracked source
declaration search found just one candidate provider for each of the two
shared theorems. Both the Gaussian theorem and the new compact-test
extension use the shared cutoff limits.

The extension retains the compact smooth test class and the original
constant, without adding a finite-measure, probability, positivity,
positive-mass, or sign-of-constant assumption. The mass, entropy, and energy
convergence arguments use integrable envelopes. The normalization passes
through the continuous function `q * log q`, including at zero. The
gradient estimate uses differentiability and the product rule; eventual
gradient equality follows from local equality of the cutoff product with
the original function. Neither step substitutes a totalized value for a
missing analytic fact.

The test invokes the extension on `u = sqrt(1 + e * f)` itself, with the
domain facts provided by the existing perturbation theorem and gradient
square integrability obtained from the Frechet derivative via the Riesz
isometry. The finite-measure assumption belongs to that test's perturbation
inputs, not the shared extension. The test does not assume compact support
or gradient integrability of `u` from its caller.

The attribution matches the reviewed plan: Chewi's density-extension step
and reuse of the existing ASTIS Gaussian cutoff proof. The relocation is
not new cutoff mathematics. This review does not certify the full PI
argument, any Cell or ledger status, or any source-bound publication,
semantic-audit, or benchmark gate.
