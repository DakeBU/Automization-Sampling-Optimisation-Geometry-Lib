# Initial anonymous staging for the geometry/kernel batch

`/root/sog_blind_4` saw only `packets/anonymous-input.json` and wrote its own `decoder.json`. This directory has no source-review decision and admits no QA.

Before source review, a dependency bibliography typo was corrected: the symmetric quadratic derivative belongs to `LinearMap.IsSymmetric`, not `ContinuousLinearMap.IsSymmetric`. The kernel component's Mathlib references were also expanded to their checked canonical namespaces. No theorem, binder, proof, mathematical question, rubric or decoder definition changed.

The corrected coordinator bindings live in [formal-5](../formal-5/README.md). Its anonymous input is byte-identical to this one, and the actual decoder output is reused byte-for-byte under the same input hash. Original records remain intact. Never infer acceptance from this staging directory or modify its mapping to match later metadata.
