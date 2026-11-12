# Full random-scan reversibility: independent paired review

The [blind input](packets/anonymous-input.json), [blind reconstruction](decoder.json),
[source input](packets/reviewer-input.json) and [source verdict](source-review.json)
are bound to the exact candidate. The [L4 proposal](preflight-l4/source-review.json)
and its inputs stay intact. It found correct mathematics but required lowering
the Lean level: the finite proof requires several steps, not a new analytic
adapter. A distinct reviewer checked both L3 labels against the same anonymous
statement. This is editorial difficulty, not empirical calibration.

The [exact rubric repair](packets/repair-input.json) and
[independent acceptance](repair-review.json) allow an equivalent symmetric
conditional pair proof of the null-atom cases, without losing the requirement
to cover them. The source, proposition, other rubric rows and proof stayed fixed.

The published task uses the same public-dev family as `sogb-006` but asks for the
full positive-positive fiber identity and atomic-to-kernel lift in addition to
the null cases. The exact Lean 4.33.0 source tests and answer-owner-free reference
passed. The aligned Lean target is only reversibility; the invariance and
two-bit nonconvergence explanation are not additional fixed goals. This is
reuse of original Apache-2.0 project work, not a new theorem, hidden test
family, native runtime result, or model result.
