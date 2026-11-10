# Fixed-level angular sum on the actual coefficient law

Zhou–Suzuki [§4.1.1, Eq. (14)–(15)](https://arxiv.org/html/2611.05813v1#S4.E15)
specifies the uncut degree sum and adjacent one-block and joint Gaussian laws.
The new theorem reconstructs their unnumbered scalar consequence: at fixed
deterministic unit trailing directions, the actual level sum has mean zero
and variance `n * ∑ p, aᵢₚ²`. It does not assert the radial variance
calculation before Eq. (51).

## What is new in the graph

- Actual model parents: `AngularDegree.angularDegreeComponent_hasLaw` and
  `CoefficientBlocks.jointCoefficientBlocks_hasLaw`, both called by
  `AngularDegreeSum.angularDegreeSum_hasLaw`. The literal component definition
  is also used directly. There is one proposed Registry theorem, no added
  public definition, generic Gaussian wrapper, or Functor transport.
- Mathlib supplies product evaluation, measurable preservation of independence,
  the independent Gaussian finite sum and addition of variances. The Lean proof
  derives all moment and measurability obligations; these are not new binders.
- This is a continuous general-oracle hard-family ingredient. It is neither a
  MALA/HMC/midpoint-specific lower bound nor an algorithm-agnostic rate by itself.

The exact signature/source topology were sealed at
`b9f2f4356`. Candidate
`3292867e2` passed
`lake build Tests.SlcLsiAngularDegreeSum` (3188 jobs), checking the literal
sum's expectation and variance and only the standard axioms. The Cell
`ASTIS-SW-SLC-LSI-angular-degree-sum`, publication binding and round-trip
audit are canonical for independent review and integration. Local compilation
does not imply Registry admission, deployment or purification.

## Integration candidate

On actual main `584af6b3`, the independently verified declaration adds one
Registry leaf (614 in the candidate). The root Lean/ASTIS gate, Tests9644,
publication/contributor/semantic checks, site build/check and focused graph
check passed. Desktop and mobile browser checks exercised MathJax and both
adjacent Lean folds; actual proof and graph PNGs were inspected. The separate
radial field is not part of this batch. Remote CI, merge, deployment and
postmerge purification are not inferred from local acceptance.

## Main integration and purification

[PR #398](https://github.com/DakeBU/Automization-Sampling-Optimisation-Geometry-Lib/pull/398)
merged at `cdd03014` after all seven exact-head checks passed. The exact
merge tree preserves both the tested proof packet and the nonoverlapping
Bench update. Independent postmerge `ACCEPT_NO_CHANGE` seals the existing
three-move reader and exact Lean folds; it does not itself verify deployment.

## Next dependency-ready boundary

Specialize the uncut law to the paper's actual radial pullback at a
deterministic location. On nonzero trailing blocks, normalize each direction
and multiply by the exact common radial factor; on a zero trailing block
use the paper's zero-extension convention, with the corresponding degenerate
Gaussian. The goal is the fixed-location law with variance
`n * C_i(x)^2 * v_i`, not full joint-in-location Gaussianity or derivative
covariance. The cutoff definition and its source support semantics need their
own audit. Use that radial law, not the uncut theorem directly, in the
application of Fact 10 below §6.2. Earlier-level conditioning and iteration,
normalizer estimates, admissibility and all three main bounds stay independent.
