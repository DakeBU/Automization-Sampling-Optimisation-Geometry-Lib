# Next bounded edge: the actual averaged half-turn is reversible

Planning checkpoint, 2026-10-17. This is NOT a Statement Seal, proof, new Goal,
claimed Frontier Cell, or completion badge. Finish the existing kernel/L2 review
and the sole continuity stabilization first. Preserve the four-paper priority.

## Shortest useful target

Close Proposition 3.2 for the actual Algorithm 1 returned-position kernel,
not another abstract self-adjoint-operator wrapper. Reuse the existing
`IdealHalfTurnKernel.ideal_half_turn_returned_position_kernel` joint measurable
kernel and identify its literal process witness with the accepted actual
process. The source is arXiv:2609.06905v1, Appendix A.2, proof of Proposition 3.2,
HTML lines 832--841. Proposition A.1(iii), lines 828--831, supplies the
fixed-reference Gaussian averaging argument; A.2 lines 843--858 distinguishes
joint kernel measurability from the later augmented-space L2 operator.

For fixed y write q_y(dx) proportional to
exp(-V(x)-||x-y||^2/(2 eta)) dx, gamma=stdGaussian(E),
P=Exp(1)^N, and use the already constructed actual process Z. The existing law is

    H(y,x) = map((r,p,w) -> fst(Z(y,r,(x,p),pi,w)))
                 (q_y x gamma x P).

The desired NEW conclusion is exact detailed balance:

    integral_A H(y,x)(B) q_y(dx) = integral_B H(y,x)(A) q_y(dx)

for every measurable A,B and every y. Use Mathlib `Kernel.IsReversible` on the
state section x -> H(y,x); its existing `IsReversible.invariant` supplies the
invariant law without another custom wrapper. Retain the same six analytic
standing hypotheses and the existing probability/joint-measurability facts.
All normalization, measurability, integrability and independence are produced
internally, not supplied as convenience binders.

## Candidate proof architecture, before signature elaboration

1. Reuse actual phase construction, bounded signed momentum-flip duality,
   Gaussian normalization and the existing exact returned-position kernel.
   Identify existential Z witnesses from their raw arc/fallback prescriptions;
   do not identify them just because their descriptions look similar.
2. Lift bounded measurable f,g on position to phase by composition with fst.
   Momentum flip disappears from both tests. Derive fixed-reference symmetric
   Gaussian/clock expectations using the actual bounded phase duality.
3. Average over r with q_y, independent of the input x. Derive the joint-product
   integrability bounds first; use signed Fubini only with those bounds.
4. Specialize to measurable indicators. Convert real indicator integrals to
   the ENNReal set-lintegrals used by `Kernel.IsReversible`, with finite
   probability mass and nonnegativity explicit.
5. Identify the resulting law with the SAME H from the exact raw fiber equation.
   The intended consumer is the actual augmented half-turn operator used by
   the paper's discrete hypocoercive contraction, not an invented current use.

## Reuse versus unnecessary intermediate work

The existing ideal kernel already proves joint measurability, probability mass,
initialization and a literal half-turn law. Do not reprove those as new leaves.
The accepted actual Gaussian L2 averaging already proves self-adjointness and
contraction; do not count a restatement as progress. If direct bounded-test
reversibility closes the actual H using these parents, a separate fixed-reference
position-kernel packaging theorem is unnecessary. No generic shared adapter is
created until a second real consumer warrants it.

Before implementation: search the exact pinned Mathlib indicator/lintegral and
product-integral APIs, elaborate the final complete signature, audit binders and
definitions, seal it, and independently review source coverage/topology. A
missing API is not a reason to add reversibility or integrability as a premise.

## Strict exclusions and subsequent order

This edge does not prove process restart, Chapman--Kolmogorov, a phase semigroup,
generator/domain statements, or the augmented-space all-L2 operator by itself.
It does not prove hypocoercive rates, capped implementation errors, actual-input
expected costs, warm-start initialization, composition, or a complete paper.
Next choose the shortest dependency-ready actual operator/hypocoercivity edge;
keep the hard memoryless-restart edge independently visible. SPHMC real RGO
transport/Fisher/Wp/proxy-warmness and actual costs remain separate. Then follow
the existing Gaussian Cloud Section6 and Midpoint phases, not four simultaneous
paper implementation lanes.

## Dependency-ready consumer audit after the actual H proof (2026-10-17)

The smallest concrete paper consumer to audit next is Proposition3.4, not a
second fixed-reference kernel wrapper. Equation(3.11) first sends
`(x,y)` to `(x,2*x-y)`, then mixes exact conditional resampling with the SAME
actual returned-position kernel. At `y'=2*x-y` its exact output law must be

    K((x,y),.) = (rho*q_y' + (1-rho)*H(y',x)).prod(dirac y').

The proposed mathematical delta is construction/probability/exact-law and
invariance of this actual augmented one-step kernel for the actual normalized
augmentation J. Do not supply invariance, conditional identification, or a
different unspecified H as a public premise. Retain the original six analytic
inputs and the source resampling regime `0<rho<1`. This is an audit/route, NOT
a frozen Lean signature or completed proposition.

Reuse search already found these exact owned interfaces:

- `GibbsAugmentation.normalized_augmentation_density`: genuine positive Gibbs
  normalization and the source joint density, derived from Hessian regularity.
- `GaussianReflection.reflection_preserves_augmentation`: the exact auxiliary
  reflection preserves the generative J. No new reflection wrapper is needed.
- `TechnicalLemmas.Probability.GaussianConditionalKernel.exists_tilted_isCondKernel`:
  an everywhere-defined normalized quadratic tilt disintegrates `J.map Prod.swap`.
- `ActualHalfTurnReversibility.actual_half_turn_reversible`: the local compiled
  H result; independent source/compiler admission and VERIFIED are now complete.
- `TechnicalLemmas.Probability.KernelMixture.finiteMixture_isMarkovKernel` and
  `finiteMixture_invariant`: reuse the fixed finite mixture, not a new ad hoc
  sum-kernel implementation.
- `TechnicalLemmas.Probability.KernelTransport.invariant_map_comap` and pinned
  Mathlib `Measure.IsCondKernel.disintegrate`, `Measure.compProd_apply`,
  `Kernel.IsReversible.invariant`: existing transport/disintegration contracts.

The real adapter still to check is conditional-fiber invariance -> invariance
of the retained-coordinate joint update. Work in `(y,x)` order using the SAME
conditional version, then transport by `Prod.swap` and compose with reflection.
The Gaussian conditional producer initially gives a tilt of the Gibbs input
measure, whereas H uses the volume tilt of the summed potential: identify these
exactly with `tilted_tilted` and the already derived positive Gibbs integral.
Do not equate arbitrary regular conditional versions pointwise on null fibers.
Tonelli is available for nonnegative set integrals; any signed/L2 claim needs
its own integrability/representative adapter. Search for an existing general
retained-coordinate theorem before making this adapter public; with one actual
consumer it can remain private rather than inflate the Registry.

Only after exact signature elaboration, binder/definition audit and source-first
review may implementation begin. Prop3.4 does not close temporal phase restart,
the augmented L2 realization, hypocoercivity, implementation error or actual
expected cost, initialization, composition, or any full paper.
