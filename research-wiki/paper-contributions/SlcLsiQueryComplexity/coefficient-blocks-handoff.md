# Joint Gaussian coefficient blocks

The §4.1.1 post-Eq15 construction now has one compiled law:
`CoefficientBlocks.jointCoefficientBlocks_hasLaw`. It groups the ordered
coordinates of the actual unconditioned joint standard Gaussian and obtains
the product of the block standard Gaussian measures. This is the inverse
direction of the source's collection of independent standard blocks, not a
new law assumption. The underlying geometric norm is the ℓ² direct sum;
the Lean target dependent function space is used as a measurable product.

The exact signature was sealed at `66d288898` before proof, following the
independent source-only refinement. The checked Lean candidate is
`dac19f45c`; `lake build Tests.SlcLsiCoefficientBlocks` passed3182 jobs.
The focused test derives all block marginals and mutual independence from
the new theorem on the exact carriers. Only the three usual Lean axioms
appear. No separate wrapper or leaf is added for the test consequences.

Read the canonical Cell `ASTIS-SW-SLC-LSI-coefficient-blocks`, source
publication binding and semantic audit for current evidence state. Local
compilation, independent post-proof review, stabilization, merge and reader
purification are separate. Exploration did not touch the aggregators or
Registry while PR396 held the lane.

## Local integration

PR396 merged and its exact public site was verified. The independent
compiler/source review admitted this coefficient theorem at unchanged
`dac19f45c`, including the fresh module, exact marginal/independence test
and accepted packet-bound reader. The exact inverse-law scope needs no
source repair. See `runs/20261109-slc-lsi-coefficient-blocks/`.

After taking the stabilization lane, root Tests passed9642 jobs and the
full ASTIS gate passed at Registry613. The publication, contributor,
semantic and Frontier checks, site build/check, focused graph-check and
actual desktop/mobile Edge checks passed. The theorem gets one canonical
blue node; source and review links are distinct from compiler structure.
Both adjacent Lean disclosures work and long formulae scroll; the proof
and graph PNGs were actually inspected. No new Functor transport or
existing consumer call is asserted. Remote merge, deployment and
post-merge purification are not consequences of these local checks.

## Main integration

[PR #397](https://github.com/DakeBU/Automization-Sampling-Optimisation-Geometry-Lib/pull/397)
merged at `584af6b3` after all exact-head checks passed.
Its signed main merge tree is byte-identical to the tested integration tree.
The merge does not establish deployment or close the radial and conditional
obligations. The next checked consumer is the actual fixed-level angular sum.

## Next dependency-ready mathematical edge

Combine this joint law with the earlier checked angular component law at
one fixed level and deterministic unit direction tuple. Map each actual
block by its exact polynomial, restrict to the allowed degree labels for the
level, then sum; the variance must be the sum of the exact per-degree
variances, not a fresh estimate or an assumed Gaussian law.

Reuse candidates in pinned Mathlib: `HasLaw.fun_comp`,
`iIndepFun.hasGaussianLaw_fun_sum`, `IndepFun.variance_sum`, and the Gaussian
characterization by mean and variance. The sum still needs its own sealed
carrier and statement, including scalar square-integrability derived from
the component laws. Do not add a generic convolution wrapper if these
APIs suffice. Radial cutoffs and zero blocks, the prefix/earlier-level
filtration, conditional laws, normalizer moments, admissibility, and all
three main query lower bounds remain separate.
