# Formal round 23: three log-Sobolev cutoff limits

`sogb-052` is an original paired question about a density prerequisite of
[Chewi §2.1.1](https://chewisinho.github.io/main.pdf#page=60).
It shares the existing Exercise 1.7 public-development family, but is not a
new numbered exercise, a complete form-domain extension, or another proof
of log-Sobolev implying Poincaré. The fixed Lean conclusion is just the
three integrals' convergence. Local derivative agreement, the three
envelopes, and the later use of finite dimension are explained in prose.

The [first source review](superseded-draft/source-review.json) asked us to
state the cutoff's smoothness and not score an unasked observation about a
later theorem. The [revised five-point draft](five-point-accepted-draft/source-review.json)
passed independent source review but could not satisfy the catalogue's
four-point rubric contract. Both full snapshots remain nested review
history, not separate admissions or exports.

The [four-point review](source-review.json) checked the same proof and
the same Lean target, but asked that the energy criterion not prescribe
the product rule. The [exact scoring proposal](packets/repair-input.json)
leaves the question, proofs, family, and other three criteria unchanged.
The [independent repair decision](repair-review.json) accepted it. The
criterion gives credit to any valid integrable energy envelope and
convergence argument. The [anonymous packet](packets/anonymous-input.json) and
[independent reconstruction](decoder.json) are identical in all three
rounds. Formal coverage is conclusion-only; L4/L4 is provisional.

The fixed task imports the real cutoff and gradient infrastructure, not
the target owner. Four earlier private proofs appear only in the trusted
reference. No production Lean, proof graph, Registry or textbook-progress
status changes.
