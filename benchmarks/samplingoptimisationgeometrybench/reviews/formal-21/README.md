# Formal round 21: constant-step lower-bound witness

`sogb-046` reuses the selected fixed-step distance component of [Chewi's
Optimization Exercises 3.2–3.3](https://arxiv.org/html/2605.07006v1#S3).
It is a method-specific sharpness question, not all of Exercise 3.3 and not
an oracle lower bound for adaptive or general first-order methods.

- [Anonymous Lean input](packets/anonymous-input.json) and [independent
  reconstruction](decoder.json) pin the seven semantic slots without source identity.
- [Source review](source-review.json) confirmed the mathematical and formal
  scope, exact trusted-reference compilation, and unavailable answer owner
  under the fixed imports. It required a rubric-only repair: the original
  fourth point would penalize a correct scope explanation for not restating
  a supplied fact about class curvature bounds.
- [Exact proposal](packets/repair-input.json) and [independent repair
  decision](repair-review.json) accept changing only that fourth criterion.
  The earlier report remains immutable. The fixed Lean code, question,
  assumptions, proof prose, provisional L3/L3 levels and family are unchanged.

Current admission is `accepted-after-repair` only while the repaired
question and import context match. Lean proves the stated existence,
admissibility and iterate bounds, not the explanatory comparison with
adaptive algorithms. No new library theorem, graph task, full numbered
exercise credit, private split or measured score is claimed.
