# Bounded centered perturbation: actual law and finite canonical KL

Statement seal v1, 2026-11-04. One canonical shared node, not a completed exercise.

Source: Chewi, *Log-Concave Sampling*, August 20 2026, Exercise 1.7 / (1.E.1),
printed p.43 / PDF p.55; also the explicit use in Corollary 2.1.2,
printed p.50 / PDF p.62. Pinned PDF SHA256:
`8818e8fb40c07bd70651bafe10e8ec4500197c836928330b90025ca47da52fae`.
Reuse the accepted source-only topology v2, without treating it as proof.

## Exact public signature (frozen before proof search)

```lean
theorem eventually_isProbabilityMeasure_and_klDiv_eq_one_add_mul
    {X : Type*} [MeasurableSpace X] (mu : Measure X) [IsProbabilityMeasure mu]
    (f : X → ℝ) (hf : AEStronglyMeasurable f mu) {M : ℝ}
    (hbound : ∀ᵐ x ∂mu, |f x| ≤ M) (hcenter : (∫ x, f x ∂mu) = 0) :
    ∀ᶠ e : ℝ in 𝓝 (0 : ℝ),
      (∀ᵐ x ∂mu, (1 : ℝ) / 2 ≤ 1 + e * f x) ∧
      IsProbabilityMeasure (mu.withDensity (fun x => ENNReal.ofReal (1 + e * f x))) ∧
      InformationTheory.klDiv
        (mu.withDensity (fun x => ENNReal.ofReal (1 + e * f x))) mu =
        ENNReal.ofReal (∫ x, InformationTheory.klFun (1 + e * f x) ∂mu)
```

Namespace: `AutoSamplingTheory.TechnicalLemmas.InformationTheory.BoundedPerturbationLaw`.
Owning file: `AutoSamplingTheory/TechnicalLemmas/InformationTheory/BoundedPerturbationLaw.lean`.
Focused test: `Tests/Shared/BoundedPerturbationLaw.lean`.
Expected imports: canonical Mathlib KL Basic, Bochner Basic, normed-group
compact boundedness and the minimal tactics needed by the actual implementation.

All assumptions are intrinsic to this generic infrastructure statement:
measurable carrier, probability law, a.e. strong measurability, a.e. uniform
boundedness and zero mean. No desired mass, Radon--Nikodym identity, entropy
integrability or finite KL is supplied as a premise. Compact smooth source
tests produce these inputs later; their producers are separate obligations.
`ofReal` is the literal nonnegative-density API; the proved eventual lower
bound prevents clipping in the source regime, including M=0 and e=0.

## Reuse and proof architecture

Search performed: existing KLDensity/TiltedKL/BoundedDensityPerturbation;
SPHMC private quadratic KL bound; pinned Mathlib KL Basic/KLFun, WithDensity,
Lebesgue decomposition and Bochner integrals. TiltedKL concerns exponential
tilts and assumes integrability of its log ratio; it is not this construction.
No public local bounded affine-density law adapter was found.

1. Choose the actual neighborhood `|e|*|M| < 1/2`, without division by M.
2. Derive integrability of f and of the affine density, positivity and mass one.
3. Construct the literal `withDensity` probability law, not an abstract witness.
4. Obtain its a.e. RN derivative via `Measure.rnDeriv_withDensity₀`.
5. Derive entropy integrability from continuity of klFun on the compact
   density interval [1/2,3/2]; no supplied entropy estimate is allowed.
6. Use canonical `integrable_klFun_rnDeriv_iff` and KL formula to identify
   the ENNReal divergence itself with `ofReal` of the real integral.

Equality with `ofReal` proves actual finiteness; a `toReal` identity alone would
not, since `toReal ∞ = 0`. The new node will feed the already compiled
compensated integral limit, but this packet does not itself claim the complete
probability-KL limit, Fisher limit, LSI domain extension, Poincare or Bench QA.
No new conceptual/Functor transport is asserted. Private implementation helpers
have one public owner and receive no extra leaf credit.

One writer; focused elaboration first; independent anonymous decoding and
anti-anchored source/code/exposition review before VERIFIED. No root imports,
Registry, chapter badge or global graph changes outside the stabilization lane.
After repeated identical failures, audit the statement/API instead of replaying
tactics. New source corrections require a versioned successor, not a silent edit.
