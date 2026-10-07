import AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Cutoff
import AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.LineDeriv
import Mathlib.Analysis.Calculus.BumpFunction.FiniteDimension
import Mathlib.Analysis.Calculus.FDeriv.WithLp
import Mathlib.Analysis.Normed.Operator.BoundedLinearMaps
import Mathlib.MeasureTheory.Integral.DivergenceTheorem

/-!
# Coordinate divergence

This file gives ASTIS a small finite-dimensional coordinate-divergence
interface for pointwise Langevin calculations.

The definition follows the coordinate expression used in Mathlib's
`BoxIntegral` divergence theorem, but it is only a pointwise coordinate sum of
line derivatives.  It does not prove an integration theorem, integration by
parts, no-boundary term, semigroup-generator statement, invariant law, or
reversibility.
-/

namespace AutoSamplingTheory
namespace TechnicalLemmas
namespace Analysis
namespace Calculus
namespace Divergence

open scoped BigOperators RealInnerProductSpace
open Set MeasureTheory Filter Topology

/-- Pointwise coordinate divergence of a finite-dimensional Euclidean vector
field.

For `F : EuclideanSpace ℝ ι → EuclideanSpace ℝ ι`, this is the coordinate sum
`∑ᵢ ∂ᵢ Fᵢ`, expressed using Mathlib's `lineDeriv` and the coordinate unit
`EuclideanSpace.single i 1`.  It is deliberately a local pointwise definition:
IBP, divergence theorem, boundary decay, domains, and invariant-law results
remain separate obligations. -/
noncomputable def coordinateDivergence
    {ι : Type*} [Fintype ι] [DecidableEq ι]
    (F : EuclideanSpace ℝ ι → EuclideanSpace ℝ ι)
    (x : EuclideanSpace ℝ ι) : ℝ :=
  ∑ i, lineDeriv ℝ (fun y : EuclideanSpace ℝ ι => F y i) x
    (EuclideanSpace.single i (1 : ℝ))

/-- Unfold the ASTIS pointwise coordinate-divergence definition. -/
theorem coordinateDivergence_eq_sum_lineDeriv
    {ι : Type*} [Fintype ι] [DecidableEq ι]
    (F : EuclideanSpace ℝ ι → EuclideanSpace ℝ ι)
    (x : EuclideanSpace ℝ ι) :
    coordinateDivergence F x =
      ∑ i, lineDeriv ℝ (fun y : EuclideanSpace ℝ ι => F y i) x
        (EuclideanSpace.single i (1 : ℝ)) := rfl

/-- If a vector field has Frechet derivative `F'` at `x`, then the ASTIS
coordinate divergence is the coordinate trace-style sum `∑ᵢ (F' eᵢ)ᵢ`.

This matches the pointwise divergence summand shape used by Mathlib's
box-integral divergence theorem.  It is still not an integration theorem or an
integration-by-parts result. -/
theorem coordinateDivergence_eq_sum_fderiv_apply_of_hasFDerivAt
    {ι : Type*} [Fintype ι] [DecidableEq ι]
    {F : EuclideanSpace ℝ ι → EuclideanSpace ℝ ι}
    {F' : EuclideanSpace ℝ ι →L[ℝ] EuclideanSpace ℝ ι}
    {x : EuclideanSpace ℝ ι}
    (hF : HasFDerivAt F F' x) :
    coordinateDivergence F x =
      ∑ i, F' (EuclideanSpace.single i (1 : ℝ)) i := by
  dsimp [coordinateDivergence]
  refine Finset.sum_congr rfl ?_
  intro i _hi
  let pr : EuclideanSpace ℝ ι →L[ℝ] ℝ :=
    PiLp.proj (p := 2) (𝕜 := ℝ) (fun _ : ι => ℝ) i
  have hcomp : HasFDerivAt (fun y : EuclideanSpace ℝ ι => F y i)
      (pr.comp F') x := by
    simpa [pr, Function.comp_def] using (pr.hasFDerivAt.comp x hF)
  have hline := hcomp.hasLineDerivAt (EuclideanSpace.single i (1 : ℝ))
  simpa [pr] using hline.lineDeriv

/-- If a vector field is differentiable at `x`, then the ASTIS coordinate
divergence is the Mathlib divergence-theorem summand with `fderiv ℝ F x`.

This is the pointwise bridge needed before instantiating Mathlib's integral
divergence theorem.  It does not assert integrability, face terms, boundary
decay, integration by parts, generator domains, or invariant-law consequences. -/
theorem coordinateDivergence_eq_sum_fderiv_apply_of_differentiableAt
    {ι : Type*} [Fintype ι] [DecidableEq ι]
    {F : EuclideanSpace ℝ ι → EuclideanSpace ℝ ι}
    {x : EuclideanSpace ℝ ι}
    (hF : DifferentiableAt ℝ F x) :
    coordinateDivergence F x =
      ∑ i, fderiv ℝ F x (EuclideanSpace.single i (1 : ℝ)) i :=
  coordinateDivergence_eq_sum_fderiv_apply_of_hasFDerivAt hF.hasFDerivAt

/-- The `PiLp` continuous linear equivalence sends the Euclidean coordinate
unit to the corresponding Pi-space coordinate function. -/
theorem continuousLinearEquiv_apply_euclideanSpace_single
    {ι : Type*} [Fintype ι] [DecidableEq ι] (i : ι) :
    (PiLp.continuousLinearEquiv 2 ℝ (fun _ : ι => ℝ))
      (EuclideanSpace.single i (1 : ℝ)) = Pi.single i (1 : ℝ) := by
  ext j
  rw [PiLp.continuousLinearEquiv_apply]
  simp [EuclideanSpace.single]
  by_cases h : j = i
  · subst h
    simp [Pi.single]
  · simp [Pi.single, h]

/-- The derivative of the Euclidean radial cutoff transports to raw finite Pi
space through `WithLp.toLp 2` by the chain rule.

This is the cutoff-side `HasFDerivAt` producer consumed by the finite-box
cutoff-smul route.  It is pointwise and proves no support containment,
integrability, tail limit, or integration-by-parts identity. -/
theorem hasFDerivAt_radialSmoothCutoff_comp_toLp
    {n : ℕ} {R : ℝ} (hR : 0 < R) (x : Fin (n + 1) → ℝ) :
    HasFDerivAt
      (fun z => Cutoff.radialSmoothCutoff R
        (WithLp.toLp 2 z : EuclideanSpace ℝ (Fin (n + 1))))
      ((fderiv ℝ
          (Cutoff.radialSmoothCutoff R :
            EuclideanSpace ℝ (Fin (n + 1)) → ℝ)
          (WithLp.toLp 2 x)).comp
        (PiLp.continuousLinearEquiv
          2 ℝ (fun _ : Fin (n + 1) => ℝ)).symm.toContinuousLinearMap)
      x := by
  let e : EuclideanSpace ℝ (Fin (n + 1)) ≃L[ℝ] (Fin (n + 1) → ℝ) :=
    PiLp.continuousLinearEquiv 2 ℝ (fun _ : Fin (n + 1) => ℝ)
  have htoLp : HasFDerivAt
      (fun z : Fin (n + 1) → ℝ =>
        (WithLp.toLp 2 z : EuclideanSpace ℝ (Fin (n + 1))))
      e.symm.toContinuousLinearMap x := by
    simpa [e] using
      (PiLp.hasFDerivAt_toLp (𝕜 := ℝ)
        (E := fun _ : Fin (n + 1) => ℝ) 2 x)
  have hcutoff : HasFDerivAt
      (Cutoff.radialSmoothCutoff R :
        EuclideanSpace ℝ (Fin (n + 1)) → ℝ)
      (fderiv ℝ
        (Cutoff.radialSmoothCutoff R :
          EuclideanSpace ℝ (Fin (n + 1)) → ℝ)
        (WithLp.toLp 2 x))
      (WithLp.toLp 2 x) :=
    ((Cutoff.radialSmoothCutoff_contDiff hR).differentiable
      (WithTop.coe_ne_zero.mpr WithTop.top_ne_zero)
      (WithLp.toLp 2 x)).hasFDerivAt
  simpa [Function.comp_def, e] using hcutoff.comp x htoLp

/-- For an integrable finite Pi-space vector field, the `L¹` norm of the
radial-cutoff gradient applied to that field vanishes as the cutoff scale tends
to infinity.

The domination retains the operator norm of the inverse `PiLp` equivalence:
the raw Pi norm is not identified with the Euclidean `L²` norm.  This theorem
only controls the cutoff-gradient cross term; it proves no source-field
integrability, main-term convergence, integration by parts, or invariant-law
statement. -/
theorem tendsto_integral_norm_fderiv_radialSmoothCutoff_comp_toLp_apply
    {n : ℕ} {μ : Measure (Fin (n + 1) → ℝ)}
    {G : (Fin (n + 1) → ℝ) → Fin (n + 1) → ℝ}
    (hG : Integrable G μ) :
    Tendsto
      (fun R : ℝ =>
        ∫ x, ‖fderiv ℝ
          (fun z => Cutoff.radialSmoothCutoff R
            (WithLp.toLp 2 z : EuclideanSpace ℝ (Fin (n + 1))))
          x (G x)‖ ∂μ)
      atTop (𝓝 0) := by
  let e : EuclideanSpace ℝ (Fin (n + 1)) ≃L[ℝ] (Fin (n + 1) → ℝ) :=
    PiLp.continuousLinearEquiv 2 ℝ (fun _ : Fin (n + 1) => ℝ)
  obtain ⟨C, hC_pos, hC⟩ :=
    Cutoff.radialSmoothCutoff_fderiv_bound
      (E := EuclideanSpace ℝ (Fin (n + 1)))
  let bound : (Fin (n + 1) → ℝ) → ℝ :=
    fun x => (C * ‖e.symm.toContinuousLinearMap‖) * ‖G x‖
  have hbound_integrable : Integrable bound μ := by
    exact (hG.norm.const_mul (C * ‖e.symm.toContinuousLinearMap‖))
  have hmeas :
      ∀ᶠ R : ℝ in atTop,
        AEStronglyMeasurable
          (fun x => ‖fderiv ℝ
            (fun z => Cutoff.radialSmoothCutoff R
              (WithLp.toLp 2 z : EuclideanSpace ℝ (Fin (n + 1))))
            x (G x)‖) μ := by
    filter_upwards [eventually_gt_atTop (0 : ℝ)] with R hR
    have hsmooth :
        ContDiff ℝ (⊤ : ℕ∞)
          (fun z : Fin (n + 1) → ℝ =>
            Cutoff.radialSmoothCutoff R
              (WithLp.toLp 2 z : EuclideanSpace ℝ (Fin (n + 1)))) :=
      (Cutoff.radialSmoothCutoff_contDiff hR).comp
        (PiLp.contDiff_toLp (𝕜 := ℝ) (E := fun _ : Fin (n + 1) => ℝ))
    have hderiv :
        AEStronglyMeasurable
          (fun x => fderiv ℝ
            (fun z : Fin (n + 1) → ℝ =>
              Cutoff.radialSmoothCutoff R
                (WithLp.toLp 2 z : EuclideanSpace ℝ (Fin (n + 1))))
            x) μ :=
      (hsmooth.continuous_fderiv
        (WithTop.coe_ne_zero.mpr WithTop.top_ne_zero)).aestronglyMeasurable
    let eval :
        ((Fin (n + 1) → ℝ) →L[ℝ] ℝ) →L[ℝ]
          (Fin (n + 1) → ℝ) →L[ℝ] ℝ :=
      ContinuousLinearMap.flip (ContinuousLinearMap.apply ℝ ℝ)
    exact
      (eval.aestronglyMeasurable_comp₂
        hderiv hG.aestronglyMeasurable).norm
  have hdom :
      ∀ᶠ R : ℝ in atTop, ∀ᵐ x ∂μ,
        ‖(fun x => ‖fderiv ℝ
          (fun z => Cutoff.radialSmoothCutoff R
            (WithLp.toLp 2 z : EuclideanSpace ℝ (Fin (n + 1))))
          x (G x)‖) x‖ ≤ bound x := by
    filter_upwards [eventually_ge_atTop (1 : ℝ)] with R hR
    filter_upwards with x
    have hR_pos : 0 < R := lt_of_lt_of_le zero_lt_one hR
    have hfderiv :
        fderiv ℝ
          (fun z => Cutoff.radialSmoothCutoff R
            (WithLp.toLp 2 z : EuclideanSpace ℝ (Fin (n + 1))))
          x =
        (fderiv ℝ
          (Cutoff.radialSmoothCutoff R :
            EuclideanSpace ℝ (Fin (n + 1)) → ℝ)
          (WithLp.toLp 2 x)).comp e.symm.toContinuousLinearMap :=
      (hasFDerivAt_radialSmoothCutoff_comp_toLp hR_pos x).fderiv
    rw [norm_norm, hfderiv]
    calc
      ‖((fderiv ℝ
          (Cutoff.radialSmoothCutoff R :
            EuclideanSpace ℝ (Fin (n + 1)) → ℝ)
          (WithLp.toLp 2 x)).comp e.symm.toContinuousLinearMap) (G x)‖
          ≤ ‖(fderiv ℝ
              (Cutoff.radialSmoothCutoff R :
                EuclideanSpace ℝ (Fin (n + 1)) → ℝ)
              (WithLp.toLp 2 x)).comp e.symm.toContinuousLinearMap‖ * ‖G x‖ :=
        ContinuousLinearMap.le_opNorm _ _
      _ ≤ ((C / R) * ‖e.symm.toContinuousLinearMap‖) * ‖G x‖ := by
        gcongr
        exact (ContinuousLinearMap.opNorm_comp_le _ _).trans
          (mul_le_mul_of_nonneg_right
            (hC R hR_pos (WithLp.toLp 2 x)) (norm_nonneg _))
      _ ≤ bound x := by
        dsimp [bound]
        gcongr
        exact div_le_self hC_pos.le hR
  have hpoint :
      ∀ᵐ x ∂μ,
        Tendsto
          (fun R : ℝ => ‖fderiv ℝ
            (fun z => Cutoff.radialSmoothCutoff R
              (WithLp.toLp 2 z : EuclideanSpace ℝ (Fin (n + 1))))
            x (G x)‖)
          atTop (𝓝 0) := by
    filter_upwards with x
    refine squeeze_zero'
      (g := fun R =>
        ((C / R) * ‖e.symm.toContinuousLinearMap‖) * ‖G x‖) ?_ ?_ ?_
    · exact Filter.Eventually.of_forall fun R => norm_nonneg _
    · filter_upwards [eventually_gt_atTop (0 : ℝ)] with R hR
      have hfderiv :
          fderiv ℝ
            (fun z => Cutoff.radialSmoothCutoff R
              (WithLp.toLp 2 z : EuclideanSpace ℝ (Fin (n + 1))))
            x =
          (fderiv ℝ
            (Cutoff.radialSmoothCutoff R :
              EuclideanSpace ℝ (Fin (n + 1)) → ℝ)
            (WithLp.toLp 2 x)).comp e.symm.toContinuousLinearMap :=
        (hasFDerivAt_radialSmoothCutoff_comp_toLp hR x).fderiv
      rw [hfderiv]
      calc
        ‖((fderiv ℝ
            (Cutoff.radialSmoothCutoff R :
              EuclideanSpace ℝ (Fin (n + 1)) → ℝ)
            (WithLp.toLp 2 x)).comp e.symm.toContinuousLinearMap) (G x)‖
            ≤ ‖(fderiv ℝ
                  (Cutoff.radialSmoothCutoff R :
                    EuclideanSpace ℝ (Fin (n + 1)) → ℝ)
                  (WithLp.toLp 2 x)).comp e.symm.toContinuousLinearMap‖ *
                  ‖G x‖ := ContinuousLinearMap.le_opNorm _ _
        _ ≤ ((C / R) * ‖e.symm.toContinuousLinearMap‖) * ‖G x‖ := by
          gcongr
          exact (ContinuousLinearMap.opNorm_comp_le _ _).trans
            (mul_le_mul_of_nonneg_right
              (hC R hR (WithLp.toLp 2 x)) (norm_nonneg _))
    · simpa [mul_assoc] using
        (tendsto_const_nhds.div_atTop tendsto_id).mul_const
          (‖e.symm.toContinuousLinearMap‖ * ‖G x‖)
  have hDCT :=
    MeasureTheory.tendsto_integral_filter_of_dominated_convergence
      (μ := μ) (l := atTop)
      (F := fun R x => ‖fderiv ℝ
        (fun z => Cutoff.radialSmoothCutoff R
          (WithLp.toLp 2 z : EuclideanSpace ℝ (Fin (n + 1))))
        x (G x)‖)
      (f := fun _ => (0 : ℝ)) bound hmeas hdom hbound_integrable hpoint
  simpa using hDCT

/-- Multiplication by the PiLp-wrapped radial cutoff converges to the identity
under integration for every integrable real normed-space-valued source field.

The statement is measure-generic and uses only integrability of the source.
It proves the cutoff main-term limit, but no Gibbs-specific integrability,
cutoff-gradient estimate, integration by parts, generator-domain result, or
invariant-law statement. -/
theorem tendsto_integral_radialSmoothCutoff_comp_toLp_smul
    {n : ℕ} {F : Type*} [NormedAddCommGroup F] [NormedSpace ℝ F]
    {μ : Measure (Fin (n + 1) → ℝ)}
    {H : (Fin (n + 1) → ℝ) → F}
    (hH : Integrable H μ) :
    Tendsto
      (fun R : ℝ => ∫ x,
        Cutoff.radialSmoothCutoff R
          (WithLp.toLp 2 x : EuclideanSpace ℝ (Fin (n + 1))) • H x ∂μ)
      atTop (𝓝 (∫ x, H x ∂μ)) := by
  have hmeas :
      ∀ᶠ R : ℝ in atTop,
        AEStronglyMeasurable
          (fun x : Fin (n + 1) → ℝ =>
            Cutoff.radialSmoothCutoff R
              (WithLp.toLp 2 x : EuclideanSpace ℝ (Fin (n + 1))) • H x) μ := by
    filter_upwards [eventually_gt_atTop (0 : ℝ)] with R hR
    exact
      (((Cutoff.radialSmoothCutoff_contDiff hR).continuous.comp
        (PiLp.continuous_toLp 2 _)).aestronglyMeasurable).smul
        hH.aestronglyMeasurable
  have hdom :
      ∀ᶠ R : ℝ in atTop, ∀ᵐ x ∂μ,
        ‖Cutoff.radialSmoothCutoff R
            (WithLp.toLp 2 x : EuclideanSpace ℝ (Fin (n + 1))) • H x‖ ≤
          ‖H x‖ := by
    filter_upwards with R
    filter_upwards with x
    have hcutoff :=
      Cutoff.radialSmoothCutoff_mem_Icc R
        (WithLp.toLp 2 x : EuclideanSpace ℝ (Fin (n + 1)))
    rw [norm_smul, Real.norm_eq_abs, abs_of_nonneg hcutoff.1]
    exact mul_le_of_le_one_left (norm_nonneg _) hcutoff.2
  have hpoint :
      ∀ᵐ x ∂μ,
        Tendsto
          (fun R : ℝ =>
            Cutoff.radialSmoothCutoff R
              (WithLp.toLp 2 x : EuclideanSpace ℝ (Fin (n + 1))) • H x)
          atTop (𝓝 (H x)) := by
    filter_upwards with x
    simpa using
      (Cutoff.radialSmoothCutoff_tendsto_one
        (WithLp.toLp 2 x : EuclideanSpace ℝ (Fin (n + 1)))).smul_const (H x)
  exact MeasureTheory.tendsto_integral_filter_of_dominated_convergence
    (μ := μ) (l := atTop)
    (F := fun R x =>
      Cutoff.radialSmoothCutoff R
        (WithLp.toLp 2 x : EuclideanSpace ℝ (Fin (n + 1))) • H x)
    (f := H) (fun x => ‖H x‖) hmeas hdom hH.norm hpoint

/-- The `L¹` norm of an integrable field on the complement of an expanding
Euclidean ball tends to zero, expressed in raw finite-Pi coordinates.

The tail sets are `R ≤ ‖WithLp.toLp 2 x‖`.  They form an antitone family with
empty intersection, so Mathlib's antitone set-integral convergence theorem
applies to `‖H‖`.  This is measure-generic and contains no Gibbs, generator,
integration-by-parts, or invariance semantics. -/
theorem tendsto_setIntegral_norm_norm_ge_comp_toLp
    {n : ℕ} {F : Type*} [NormedAddCommGroup F] [NormedSpace ℝ F]
    {μ : Measure (Fin (n + 1) → ℝ)}
    {H : (Fin (n + 1) → ℝ) → F}
    (hH : Integrable H μ) :
    Tendsto
      (fun R : ℝ => ∫ x in
        {x : Fin (n + 1) → ℝ |
          R ≤ ‖(WithLp.toLp 2 x : EuclideanSpace ℝ (Fin (n + 1)))‖},
        ‖H x‖ ∂μ)
      atTop (𝓝 0) := by
  let s : ℝ → Set (Fin (n + 1) → ℝ) :=
    fun R => {x | R ≤ ‖(WithLp.toLp 2 x : EuclideanSpace ℝ (Fin (n + 1)))‖}
  have hs_measurable : ∀ R, MeasurableSet (s R) := by
    intro R
    exact measurableSet_le measurable_const
      ((continuous_norm.comp (PiLp.continuous_toLp 2 _)).measurable)
  have hs_antitone : Antitone s := by
    intro R S hRS x hx
    exact hRS.trans hx
  have hs_iInter : ⋂ R : ℝ, s R = ∅ := by
    apply Set.Subset.antisymm
    · intro x hx
      have hx' := Set.mem_iInter.mp hx
        (‖(WithLp.toLp 2 x : EuclideanSpace ℝ (Fin (n + 1)))‖ + 1)
      simp only [s, Set.mem_ofPred_eq] at hx'
      linarith
    · exact Set.empty_subset _
  have htail := tendsto_setIntegral_of_antitone
    hs_measurable hs_antitone ⟨0, hH.norm.integrableOn⟩
  simpa [s, hs_iInter] using htail

/-- The trace contribution of `χ'.smulRight G` over the standard finite Pi
basis is exactly the scalar derivative `χ'` applied to `G`.

This is pure finite-dimensional linear algebra.  It identifies the cutoff
cross term used by the divergence product rule but proves no measurability,
integrability, convergence, or boundary result. -/
theorem sum_smulRight_apply_pi_single_eq_apply
    {ι : Type*} [Fintype ι] [DecidableEq ι]
    (χ' : (ι → ℝ) →L[ℝ] ℝ) (G : ι → ℝ) :
    ∑ i, ((χ'.smulRight G) (Pi.single i (1 : ℝ))) i = χ' G := by
  calc
    ∑ i, ((χ'.smulRight G) (Pi.single i (1 : ℝ))) i =
        ∑ i, χ' ((G i) • Pi.single (M := fun _ : ι => ℝ) i (1 : ℝ)) := by
      apply Finset.sum_congr rfl
      intro i _hi
      simp [ContinuousLinearMap.smulRight_apply, Pi.smul_apply, smul_eq_mul,
        mul_comm]
    _ = χ' (∑ i, (G i) • Pi.single (M := fun _ : ι => ℝ) i (1 : ℝ)) := by
      rw [map_sum]
    _ = χ' G := by rw [← pi_eq_sum_univ' G]

/-- Pointwise bridge from Mathlib's Pi-space derivative to ASTIS
`EuclideanSpace` coordinate divergence for a wrapped vector field.

This is the pointwise core needed to discharge the `hdiv_ae` assumption in the
box face-term wrapper when differentiability is available almost everywhere.
It does not prove that differentiability holds a.e. on a box, prove
integrability, prove boundary-null facts, perform integration by parts, or
prove invariant-law consequences. -/
theorem coordinateDivergence_wrapped_toPi_trace_of_hasFDerivAt
    {ι : Type*} [Fintype ι] [DecidableEq ι]
    {F : (ι → ℝ) → ι → ℝ}
    {F' : (ι → ℝ) →L[ℝ] (ι → ℝ)}
    {x : ι → ℝ}
    (hF : HasFDerivAt F F' x) :
    coordinateDivergence
        (fun y : EuclideanSpace ℝ ι =>
          (WithLp.toLp 2 (F (WithLp.ofLp y)) : EuclideanSpace ℝ ι))
        (WithLp.toLp 2 x : EuclideanSpace ℝ ι) =
      ∑ i, F' (Pi.single i (1 : ℝ)) i := by
  let e : EuclideanSpace ℝ ι ≃L[ℝ] (ι → ℝ) :=
    PiLp.continuousLinearEquiv 2 ℝ (fun _ : ι => ℝ)
  have hofLp : HasFDerivAt (fun y : EuclideanSpace ℝ ι => WithLp.ofLp y)
      e.toContinuousLinearMap (WithLp.toLp 2 x : EuclideanSpace ℝ ι) := by
    simpa [e] using
      (PiLp.hasFDerivAt_ofLp (𝕜 := ℝ) (E := fun _ : ι => ℝ) 2
        (WithLp.toLp 2 x : EuclideanSpace ℝ ι))
  have hF_ofLp : HasFDerivAt (fun y : EuclideanSpace ℝ ι => F (WithLp.ofLp y))
      (F'.comp e.toContinuousLinearMap) (WithLp.toLp 2 x : EuclideanSpace ℝ ι) := by
    simpa [Function.comp_def] using hF.comp (WithLp.toLp 2 x : EuclideanSpace ℝ ι) hofLp
  have htoLp : HasFDerivAt (fun z : ι → ℝ =>
        (WithLp.toLp 2 z : EuclideanSpace ℝ ι))
      e.symm.toContinuousLinearMap (F x) := by
    simpa [e] using
      (PiLp.hasFDerivAt_toLp (𝕜 := ℝ) (E := fun _ : ι => ℝ) 2 (F x))
  have hwrapped : HasFDerivAt
      (fun y : EuclideanSpace ℝ ι =>
        (WithLp.toLp 2 (F (WithLp.ofLp y)) : EuclideanSpace ℝ ι))
      (e.symm.toContinuousLinearMap.comp (F'.comp e.toContinuousLinearMap))
      (WithLp.toLp 2 x : EuclideanSpace ℝ ι) := by
    simpa [Function.comp_def] using htoLp.comp (WithLp.toLp 2 x : EuclideanSpace ℝ ι)
      hF_ofLp
  have htrace := coordinateDivergence_eq_sum_fderiv_apply_of_hasFDerivAt hwrapped
  trans ∑ i, (e.symm.toContinuousLinearMap.comp (F'.comp e.toContinuousLinearMap))
      (EuclideanSpace.single i (1 : ℝ)) i
  · exact htrace
  · refine Finset.sum_congr rfl ?_
    intro i _hi
    have hsingle : e (EuclideanSpace.single i (1 : ℝ)) = Pi.single i (1 : ℝ) := by
      simpa [e] using continuousLinearEquiv_apply_euclideanSpace_single (ι := ι) i
    simp [ContinuousLinearMap.comp_apply, hsingle, e]

/-- If two functions on a finite-dimensional box agree on the open box away
from a countable exceptional set, then they agree a.e. on the closed box with
respect to restricted volume.

This is a reusable measure-theoretic transfer leaf.  It packages Mathlib's
fact that the open Pi-box is a.e. equal to the closed Pi-box, plus countable
sets have zero volume. -/
theorem eventuallyEq_restrict_Icc_of_eqOn_univ_pi_Ioo_diff_countable
    {n : ℕ} {β : Type*}
    {a b : Fin (n + 1) → ℝ}
    {f g : (Fin (n + 1) → ℝ) → β}
    {s : Set (Fin (n + 1) → ℝ)}
    (hs : s.Countable)
    (hfg : ∀ x ∈ (Set.univ.pi fun i => Set.Ioo (a i) (b i)) \ s, f x = g x) :
    f =ᵐ[volume.restrict (Set.Icc a b)] g := by
  have hIoo : (Set.univ.pi fun i => Set.Ioo (a i) (b i)) =ᵐ[volume]
      Set.Icc a b := by
    rw [volume_pi]
    exact Measure.univ_pi_Ioo_ae_eq_Icc
  rw [Filter.EventuallyEq, ae_restrict_iff' measurableSet_Icc]
  filter_upwards [hIoo, hs.ae_notMem volume] with x hxIoo hxnot hxIcc
  exact hfg x ⟨hxIoo.mpr hxIcc, hxnot⟩

/-- A.e. bridge from ASTIS wrapped coordinate divergence to Mathlib's Pi-space
trace summand, assuming the Pi-space derivative exists a.e. on the restricted
box.

This theorem intentionally does not derive the a.e. differentiability
assumption from an open-box/off-countable hypothesis.  Boundary-null and
countable-null transfers are separate analytic leaves. -/
theorem coordinateDivergence_wrapped_toPi_trace_ae_of_ae_hasFDerivAt
    {n : ℕ}
    (a b : Fin (n + 1) → ℝ)
    (F : (Fin (n + 1) → ℝ) → Fin (n + 1) → ℝ)
    (F' : (Fin (n + 1) → ℝ) →
      (Fin (n + 1) → ℝ) →L[ℝ] (Fin (n + 1) → ℝ))
    (hF_ae : ∀ᵐ x ∂volume.restrict (Set.Icc a b), HasFDerivAt F (F' x) x) :
      (fun x => coordinateDivergence
        (fun y : EuclideanSpace ℝ (Fin (n + 1)) =>
          (WithLp.toLp 2 (F (WithLp.ofLp y)) :
            EuclideanSpace ℝ (Fin (n + 1))))
        (WithLp.toLp 2 x : EuclideanSpace ℝ (Fin (n + 1))))
      =ᵐ[volume.restrict (Set.Icc a b)]
      fun x => ∑ i, F' x (Pi.single i (1 : ℝ)) i := by
  filter_upwards [hF_ae] with x hx
  exact coordinateDivergence_wrapped_toPi_trace_of_hasFDerivAt (ι := Fin (n + 1)) hx

/-- A.e. bridge from an open-box/off-countable `HasFDerivAt` hypothesis to the
`hdiv_ae` shape required by the finite-box face-term wrapper.

This discharges only the a.e. equality assumption.  It does not prove
integrability of the divergence integrand, weighted IBP, no-boundary limits, or
invariant-law consequences. -/
theorem coordinateDivergence_wrapped_toPi_trace_ae_of_hasFDerivAt_off_countable
    {n : ℕ}
    (a b : Fin (n + 1) → ℝ)
    (F : (Fin (n + 1) → ℝ) → Fin (n + 1) → ℝ)
    (F' : (Fin (n + 1) → ℝ) →
      (Fin (n + 1) → ℝ) →L[ℝ] (Fin (n + 1) → ℝ))
    (s : Set (Fin (n + 1) → ℝ)) (hs : s.Countable)
    (Hd : ∀ x ∈ (Set.univ.pi fun i => Set.Ioo (a i) (b i)) \ s,
      HasFDerivAt F (F' x) x) :
      (fun x => coordinateDivergence
        (fun y : EuclideanSpace ℝ (Fin (n + 1)) =>
          (WithLp.toLp 2 (F (WithLp.ofLp y)) :
            EuclideanSpace ℝ (Fin (n + 1))))
        (WithLp.toLp 2 x : EuclideanSpace ℝ (Fin (n + 1))))
      =ᵐ[volume.restrict (Set.Icc a b)]
      fun x => ∑ i, F' x (Pi.single i (1 : ℝ)) i :=
  eventuallyEq_restrict_Icc_of_eqOn_univ_pi_Ioo_diff_countable
    (a := a) (b := b) (s := s) hs fun x hx =>
      coordinateDivergence_wrapped_toPi_trace_of_hasFDerivAt (ι := Fin (n + 1)) (Hd x hx)

/-- Transfer box integrability from Mathlib's Pi-space trace summand to the
ASTIS wrapped coordinate-divergence integrand.

This closes only the representation mismatch between the two integrands.  The
trace integrability hypothesis is still an explicit analytic assumption; this
theorem does not prove integrability of any concrete Langevin vector field,
weighted IBP, boundary cancellation, generator domains, or invariant-law
consequences. -/
theorem integrableOn_coordinateDivergence_wrapped_of_integrableOn_trace_of_hasFDerivAt_off_countable
    {n : ℕ}
    (a b : Fin (n + 1) → ℝ)
    (F : (Fin (n + 1) → ℝ) → Fin (n + 1) → ℝ)
    (F' : (Fin (n + 1) → ℝ) →
      (Fin (n + 1) → ℝ) →L[ℝ] (Fin (n + 1) → ℝ))
    (s : Set (Fin (n + 1) → ℝ)) (hs : s.Countable)
    (Hd : ∀ x ∈ (Set.univ.pi fun i => Set.Ioo (a i) (b i)) \ s,
      HasFDerivAt F (F' x) x)
    (Hi_trace : IntegrableOn (fun x => ∑ i, F' x (Pi.single i (1 : ℝ)) i)
      (Set.Icc a b) volume) :
    IntegrableOn
      (fun x => coordinateDivergence
        (fun y : EuclideanSpace ℝ (Fin (n + 1)) =>
          (WithLp.toLp 2 (F (WithLp.ofLp y)) :
            EuclideanSpace ℝ (Fin (n + 1))))
        (WithLp.toLp 2 x : EuclideanSpace ℝ (Fin (n + 1))))
      (Set.Icc a b) volume := by
  have hdiv_ae := coordinateDivergence_wrapped_toPi_trace_ae_of_hasFDerivAt_off_countable
    a b F F' s hs Hd
  exact Hi_trace.congr_fun_ae hdiv_ae.symm

/-- Box-level signed-face divergence theorem wrapper for ASTIS coordinate
divergence.

Mathlib's Bochner divergence theorem is stated on `Fin (n + 1) → ℝ`; ASTIS
finite Euclidean pointwise calculations use `EuclideanSpace ℝ (Fin (n + 1))`.
This theorem only bridges those interfaces under an explicit a.e. equality
`hdiv_ae` between the ASTIS coordinate-divergence integrand and Mathlib's trace
summand.  The conclusion is exactly Mathlib's signed face-term formula.

It does not derive `hdiv_ae`, prove box integrability, take a whole-space
limit, prove boundary cancellation, perform weighted integration by parts,
establish generator domains, or prove invariant/reversible Gibbs laws. -/
theorem integral_coordinateDivergence_toPi_box_of_hasFDerivAt_off_countable
    {n : ℕ}
    (a b : Fin (n + 1) → ℝ) (hle : a ≤ b)
    (F : (Fin (n + 1) → ℝ) → Fin (n + 1) → ℝ)
    (F' : (Fin (n + 1) → ℝ) →
      (Fin (n + 1) → ℝ) →L[ℝ] (Fin (n + 1) → ℝ))
    (s : Set (Fin (n + 1) → ℝ)) (hs : s.Countable)
    (Hc : ContinuousOn F (Set.Icc a b))
    (Hd : ∀ x ∈ (Set.univ.pi fun i => Set.Ioo (a i) (b i)) \ s,
      HasFDerivAt F (F' x) x)
    (hdiv_ae :
      (fun x => coordinateDivergence
        (fun y : EuclideanSpace ℝ (Fin (n + 1)) =>
          (WithLp.toLp 2 (F (WithLp.ofLp y)) :
            EuclideanSpace ℝ (Fin (n + 1))))
        (WithLp.toLp 2 x : EuclideanSpace ℝ (Fin (n + 1))))
      =ᵐ[volume.restrict (Set.Icc a b)]
      fun x => ∑ i, F' x (Pi.single i (1 : ℝ)) i)
    (Hi : IntegrableOn
      (fun x => coordinateDivergence
        (fun y : EuclideanSpace ℝ (Fin (n + 1)) =>
          (WithLp.toLp 2 (F (WithLp.ofLp y)) :
            EuclideanSpace ℝ (Fin (n + 1))))
        (WithLp.toLp 2 x : EuclideanSpace ℝ (Fin (n + 1))))
      (Set.Icc a b) volume) :
    ∫ x in Set.Icc a b, coordinateDivergence
        (fun y : EuclideanSpace ℝ (Fin (n + 1)) =>
          (WithLp.toLp 2 (F (WithLp.ofLp y)) :
            EuclideanSpace ℝ (Fin (n + 1))))
        (WithLp.toLp 2 x : EuclideanSpace ℝ (Fin (n + 1))) =
      ∑ i : Fin (n + 1),
        ((∫ x in Set.Icc (a ∘ i.succAbove) (b ∘ i.succAbove),
            F (i.insertNth (b i) x) i) -
          ∫ x in Set.Icc (a ∘ i.succAbove) (b ∘ i.succAbove),
            F (i.insertNth (a i) x) i) := by
  have Hi_trace : IntegrableOn (fun x => ∑ i, F' x (Pi.single i (1 : ℝ)) i)
      (Set.Icc a b) volume :=
    Hi.congr_fun_ae hdiv_ae
  calc
    (∫ x in Set.Icc a b, coordinateDivergence
        (fun y : EuclideanSpace ℝ (Fin (n + 1)) =>
          (WithLp.toLp 2 (F (WithLp.ofLp y)) :
            EuclideanSpace ℝ (Fin (n + 1))))
        (WithLp.toLp 2 x : EuclideanSpace ℝ (Fin (n + 1)))) =
        ∫ x in Set.Icc a b, ∑ i, F' x (Pi.single i (1 : ℝ)) i := by
          exact MeasureTheory.integral_congr_ae hdiv_ae
    _ = ∑ i : Fin (n + 1),
        ((∫ x in Set.Icc (a ∘ i.succAbove) (b ∘ i.succAbove),
            F (i.insertNth (b i) x) i) -
          ∫ x in Set.Icc (a ∘ i.succAbove) (b ∘ i.succAbove),
            F (i.insertNth (a i) x) i) := by
          exact MeasureTheory.integral_divergence_of_hasFDerivAt_off_countable
            (a := a) (b := b) hle F F' s hs Hc Hd Hi_trace

/-- Box-level signed-face divergence theorem wrapper for ASTIS coordinate
divergence, using Mathlib's trace-integrability hypothesis directly.

Compared with `integral_coordinateDivergence_toPi_box_of_hasFDerivAt_off_countable`,
this version no longer asks callers to provide the `hdiv_ae` representation
bridge or coordinate-divergence integrability.  Both are derived from the
open-box/off-countable derivative hypothesis and the explicit trace-integrability
assumption.

It still proves only the finite-box signed face-term formula.  It does not
prove trace integrability for a concrete vector field, whole-space/no-boundary
limits, weighted IBP, generator domains, invariant Gibbs law, reversibility,
stationarity, or KL/FI dissipation. -/
theorem integral_coordinateDivergence_toPi_box_of_integrableOn_trace_of_hasFDerivAt_off_countable
    {n : ℕ}
    (a b : Fin (n + 1) → ℝ) (hle : a ≤ b)
    (F : (Fin (n + 1) → ℝ) → Fin (n + 1) → ℝ)
    (F' : (Fin (n + 1) → ℝ) →
      (Fin (n + 1) → ℝ) →L[ℝ] (Fin (n + 1) → ℝ))
    (s : Set (Fin (n + 1) → ℝ)) (hs : s.Countable)
    (Hc : ContinuousOn F (Set.Icc a b))
    (Hd : ∀ x ∈ (Set.univ.pi fun i => Set.Ioo (a i) (b i)) \ s,
      HasFDerivAt F (F' x) x)
    (Hi_trace : IntegrableOn (fun x => ∑ i, F' x (Pi.single i (1 : ℝ)) i)
      (Set.Icc a b) volume) :
    ∫ x in Set.Icc a b, coordinateDivergence
        (fun y : EuclideanSpace ℝ (Fin (n + 1)) =>
          (WithLp.toLp 2 (F (WithLp.ofLp y)) :
            EuclideanSpace ℝ (Fin (n + 1))))
        (WithLp.toLp 2 x : EuclideanSpace ℝ (Fin (n + 1))) =
      ∑ i : Fin (n + 1),
        ((∫ x in Set.Icc (a ∘ i.succAbove) (b ∘ i.succAbove),
            F (i.insertNth (b i) x) i) -
          ∫ x in Set.Icc (a ∘ i.succAbove) (b ∘ i.succAbove),
            F (i.insertNth (a i) x) i) := by
  have hdiv_ae := coordinateDivergence_wrapped_toPi_trace_ae_of_hasFDerivAt_off_countable
    a b F F' s hs Hd
  have Hi_coord :=
    integrableOn_coordinateDivergence_wrapped_of_integrableOn_trace_of_hasFDerivAt_off_countable
    a b F F' s hs Hd Hi_trace
  exact integral_coordinateDivergence_toPi_box_of_hasFDerivAt_off_countable
    a b hle F F' s hs Hc Hd hdiv_ae Hi_coord

/-- If the normal component of a Pi-space vector field vanishes on every
lower and upper face of a finite box, then Mathlib's signed face-term sum is
zero.

This is a boundary-value producer for the finite-box divergence route.  It only
turns explicit componentwise zero boundary values into a zero signed face term;
it does not prove compact support, tail decay, weighted integration by parts,
whole-space limits, generator domains, invariant laws, or reversibility. -/
theorem signedFaceTermSum_eq_zero_of_boundary_component_eq_zero
    {n : ℕ}
    (a b : Fin (n + 1) → ℝ)
    (F : (Fin (n + 1) → ℝ) → Fin (n + 1) → ℝ)
    (hupper : ∀ (i : Fin (n + 1)) (x : Fin n → ℝ),
      F (i.insertNth (b i) x) i = 0)
    (hlower : ∀ (i : Fin (n + 1)) (x : Fin n → ℝ),
      F (i.insertNth (a i) x) i = 0) :
    ∑ i : Fin (n + 1),
        ((∫ x in Set.Icc (a ∘ i.succAbove) (b ∘ i.succAbove),
            F (i.insertNth (b i) x) i) -
          ∫ x in Set.Icc (a ∘ i.succAbove) (b ∘ i.succAbove),
            F (i.insertNth (a i) x) i) = 0 := by
  simp [hupper, hlower]

/-- Version of `signedFaceTermSum_eq_zero_of_boundary_component_eq_zero`
with boundary values expressed by `Function.update`.

This is often the more convenient shape for later support or cutoff lemmas:
if replacing coordinate `i` by either endpoint forces the `i`-th component of
`F` to vanish, then the signed face-term sum vanishes.  This still assumes the
boundary values directly; compact-support and tail-decay proofs remain
separate obligations. -/
theorem signedFaceTermSum_eq_zero_of_update_boundary_component_eq_zero
    {n : ℕ}
    (a b : Fin (n + 1) → ℝ)
    (F : (Fin (n + 1) → ℝ) → Fin (n + 1) → ℝ)
    (hupper : ∀ (i : Fin (n + 1)) (x : Fin (n + 1) → ℝ),
      F (Function.update x i (b i)) i = 0)
    (hlower : ∀ (i : Fin (n + 1)) (x : Fin (n + 1) → ℝ),
      F (Function.update x i (a i)) i = 0) :
    ∑ i : Fin (n + 1),
        ((∫ x in Set.Icc (a ∘ i.succAbove) (b ∘ i.succAbove),
            F (i.insertNth (b i) x) i) -
          ∫ x in Set.Icc (a ∘ i.succAbove) (b ∘ i.succAbove),
            F (i.insertNth (a i) x) i) = 0 :=
  signedFaceTermSum_eq_zero_of_boundary_component_eq_zero a b F
    (fun i x => by
      simpa [Function.update_eq_self] using hupper i (i.insertNth (b i) x))
    (fun i x => by
      simpa [Function.update_eq_self] using hlower i (i.insertNth (a i) x))

/-- If a Pi-space vector field vanishes outside the open box
`Set.univ.pi (fun i => Set.Ioo (a i) (b i))`, then its normal components
vanish after updating any coordinate to either endpoint.

This is a direct boundary producer for later compact-support or cutoff
arguments: those arguments can prove the off-open-box vanishing hypothesis,
and this leaf converts it into the update-boundary hypotheses used by the
finite-box face-term lemmas.  It does not prove compact support, tail decay,
whole-space limits, weighted integration by parts, generator domains, invariant
laws, or reversibility. -/
theorem update_boundary_component_eq_zero_of_eq_zero_off_univ_pi_Ioo
    {n : ℕ}
    (a b : Fin (n + 1) → ℝ)
    (F : (Fin (n + 1) → ℝ) → Fin (n + 1) → ℝ)
    (hoff : ∀ x ∉ (Set.univ.pi fun i => Set.Ioo (a i) (b i)), F x = 0) :
    (∀ (i : Fin (n + 1)) (x : Fin (n + 1) → ℝ),
        F (Function.update x i (b i)) i = 0) ∧
      (∀ (i : Fin (n + 1)) (x : Fin (n + 1) → ℝ),
        F (Function.update x i (a i)) i = 0) := by
  constructor
  · intro i x
    have hxnot : Function.update x i (b i) ∉
        (Set.univ.pi fun j => Set.Ioo (a j) (b j)) := by
      intro hx
      have hlt : b i < b i := by
        simpa using (hx i (Set.mem_univ _)).2
      exact (lt_irrefl (b i)) hlt
    exact congrArg (fun y => y i) (hoff (Function.update x i (b i)) hxnot)
  · intro i x
    have hxnot : Function.update x i (a i) ∉
        (Set.univ.pi fun j => Set.Ioo (a j) (b j)) := by
      intro hx
      have hlt : a i < a i := by
        simpa using (hx i (Set.mem_univ _)).1
      exact (lt_irrefl (a i)) hlt
    exact congrArg (fun y => y i) (hoff (Function.update x i (a i)) hxnot)

/-- Off-open-box vanishing implies Mathlib's finite-box signed face-term sum
is zero.

This composes `update_boundary_component_eq_zero_of_eq_zero_off_univ_pi_Ioo`
with the update-shaped face-term producer.  It still does not prove how the
off-open-box vanishing hypothesis arises; compact support and tail decay remain
separate leaves. -/
theorem signedFaceTermSum_eq_zero_of_eq_zero_off_univ_pi_Ioo
    {n : ℕ}
    (a b : Fin (n + 1) → ℝ)
    (F : (Fin (n + 1) → ℝ) → Fin (n + 1) → ℝ)
    (hoff : ∀ x ∉ (Set.univ.pi fun i => Set.Ioo (a i) (b i)), F x = 0) :
    ∑ i : Fin (n + 1),
        ((∫ x in Set.Icc (a ∘ i.succAbove) (b ∘ i.succAbove),
            F (i.insertNth (b i) x) i) -
          ∫ x in Set.Icc (a ∘ i.succAbove) (b ∘ i.succAbove),
            F (i.insertNth (a i) x) i) = 0 := by
  have hbdry := update_boundary_component_eq_zero_of_eq_zero_off_univ_pi_Ioo a b F hoff
  exact signedFaceTermSum_eq_zero_of_update_boundary_component_eq_zero a b F hbdry.1 hbdry.2

/-- If the support of a Pi-space vector field is contained in the open box,
then the field vanishes outside that open box.

This is a support-to-boundary staging leaf.  It uses plain
`Function.support`; it does not assert compactness of the support and does not
construct a cutoff. -/
theorem eq_zero_off_univ_pi_Ioo_of_support_subset_univ_pi_Ioo
    {n : ℕ}
    (a b : Fin (n + 1) → ℝ)
    (F : (Fin (n + 1) → ℝ) → Fin (n + 1) → ℝ)
    (hsupp : Function.support F ⊆ (Set.univ.pi fun i => Set.Ioo (a i) (b i))) :
    ∀ x ∉ (Set.univ.pi fun i => Set.Ioo (a i) (b i)), F x = 0 := by
  intro x hx
  by_contra hne
  exact hx (hsupp hne)

/-- Smooth finite-dimensional cutoff localized inside a Pi-open box.

For any point of `Set.univ.pi (fun i => Set.Ioo (a i) (b i))`, Mathlib's
finite-dimensional bump theorem supplies a smooth real-valued cutoff whose
topological support is contained in the open box, has compact support, takes
values in `[0, 1]`, and is equal to `1` at the chosen point.

This is only the local smooth-cutoff existence leaf.  It does not choose an
exhausting family of boxes, prove derivative formulas for a specific cutoff,
perform a tail limit, or prove weighted integration by parts/invariance. -/
theorem exists_contDiff_cutoff_tsupport_subset_univ_pi_Ioo
    {n : ℕ} {a b x : Fin (n + 1) → ℝ}
    (hx : x ∈ Set.univ.pi fun i => Set.Ioo (a i) (b i)) :
    ∃ χ : (Fin (n + 1) → ℝ) → ℝ,
      tsupport χ ⊆ Set.univ.pi (fun i => Set.Ioo (a i) (b i)) ∧
      HasCompactSupport χ ∧
      ContDiff ℝ (⊤ : ℕ∞) χ ∧
      Set.range χ ⊆ Set.Icc 0 1 ∧
      χ x = 1 := by
  have hopen : IsOpen (Set.univ.pi fun i => Set.Ioo (a i) (b i)) := by
    exact isOpen_set_pi Set.finite_univ fun _ _ => isOpen_Ioo
  exact exists_contDiff_tsupport_subset (n := (⊤ : ℕ∞)) (hopen.mem_nhds hx)

/-- Topological-support containment implies plain function-support containment
inside a finite Pi-open box.

This is the bridge needed by the finite-box cutoff route: Mathlib's smooth
cutoff theorem naturally returns `tsupport`, while the already-compiled
zero-face handoffs are phrased using `Function.support`.  The lemma is only a
support-API conversion; it does not construct a cutoff or prove any derivative,
tail, or whole-space integration-by-parts statement. -/
theorem support_subset_univ_pi_Ioo_of_tsupport_subset_univ_pi_Ioo
    {n : ℕ} {a b : Fin (n + 1) → ℝ}
    {χ : (Fin (n + 1) → ℝ) → ℝ}
    (hχ : tsupport χ ⊆ Set.univ.pi (fun i => Set.Ioo (a i) (b i))) :
    Function.support χ ⊆ Set.univ.pi (fun i => Set.Ioo (a i) (b i)) := by
  exact (subset_tsupport χ).trans hχ

/-- Smooth finite-dimensional cutoff localized inside a Pi-open box, with both
topological-support and plain function-support conclusions.

This packages `exists_contDiff_cutoff_tsupport_subset_univ_pi_Ioo` with
`support_subset_univ_pi_Ioo_of_tsupport_subset_univ_pi_Ioo`, so downstream
finite-box support lemmas can consume the cutoff directly.  It remains local:
no exhausting cutoff family, derivative bookkeeping, tail limit, weighted IBP,
generator-domain theorem, invariant law, or reversibility is asserted. -/
theorem exists_contDiff_cutoff_support_subset_univ_pi_Ioo
    {n : ℕ} {a b x : Fin (n + 1) → ℝ}
    (hx : x ∈ Set.univ.pi fun i => Set.Ioo (a i) (b i)) :
    ∃ χ : (Fin (n + 1) → ℝ) → ℝ,
      Function.support χ ⊆ Set.univ.pi (fun i => Set.Ioo (a i) (b i)) ∧
      tsupport χ ⊆ Set.univ.pi (fun i => Set.Ioo (a i) (b i)) ∧
      HasCompactSupport χ ∧
      ContDiff ℝ (⊤ : ℕ∞) χ ∧
      Set.range χ ⊆ Set.Icc 0 1 ∧
      χ x = 1 := by
  rcases exists_contDiff_cutoff_tsupport_subset_univ_pi_Ioo hx with
    ⟨χ, hχtsupp, hχcompact, hχsmooth, hχrange, hχone⟩
  exact ⟨χ,
    support_subset_univ_pi_Ioo_of_tsupport_subset_univ_pi_Ioo hχtsupp,
    hχtsupp, hχcompact, hχsmooth, hχrange, hχone⟩

/-- Smooth nonnegative bump whose plain support is exactly a finite Pi-open box.

This is the finite-box specialization of Mathlib's
`IsOpen.exists_contDiff_support_eq`.  It is useful when a later cutoff argument
needs nonvanishing throughout an open box.  Unlike the local cutoff leaves
above, this theorem does not assert compact support, topological-support
containment, equality to `1` on an inner closed box, an exhausting family, tail
decay, weighted IBP, generator domains, invariant law, or reversibility. -/
theorem exists_contDiff_support_eq_univ_pi_Ioo
    {n : ℕ} (a b : Fin (n + 1) → ℝ) :
    ∃ χ : (Fin (n + 1) → ℝ) → ℝ,
      Function.support χ = Set.univ.pi (fun i => Set.Ioo (a i) (b i)) ∧
      ContDiff ℝ (⊤ : ℕ∞) χ ∧
      Set.range χ ⊆ Set.Icc 0 1 := by
  have hopen : IsOpen (Set.univ.pi fun i => Set.Ioo (a i) (b i)) := by
    exact isOpen_set_pi Set.finite_univ fun _ _ => isOpen_Ioo
  exact hopen.exists_contDiff_support_eq (n := (⊤ : ℕ∞))

/-- A `[0,1]`-valued function whose support is exactly a finite Pi-open box is
strictly positive at every point of that box.

This is only a support/range consequence.  It does not construct a compactly
supported cutoff, prove a plateau on an inner closed box, choose an exhaustion,
or prove any boundary/tail/integration-by-parts statement. -/
theorem positive_on_univ_pi_Ioo_of_support_eq_univ_pi_Ioo
    {n : ℕ} {a b : Fin (n + 1) → ℝ}
    {χ : (Fin (n + 1) → ℝ) → ℝ}
    (hχsupp : Function.support χ = Set.univ.pi (fun i => Set.Ioo (a i) (b i)))
    (hχrange : Set.range χ ⊆ Set.Icc 0 1)
    {x : Fin (n + 1) → ℝ}
    (hx : x ∈ Set.univ.pi (fun i => Set.Ioo (a i) (b i))) :
    0 < χ x := by
  have hxmem : x ∈ Function.support χ := by
    simpa [hχsupp] using hx
  have hxne : χ x ≠ 0 := hxmem
  have hnonneg : 0 ≤ χ x := (hχrange ⟨x, rfl⟩).1
  exact lt_of_le_of_ne hnonneg (Ne.symm hxne)

/-- A closed inner Pi-box is contained in a strictly larger open Pi-box.

This is a bookkeeping leaf for exhaustion arguments.  It only proves the
coordinate set inclusion needed to feed local cutoff construction; it does not
choose an exhausting sequence or construct a cutoff. -/
theorem Icc_subset_univ_pi_Ioo_of_strict_bounds
    {n : ℕ} {a b A B : Fin (n + 1) → ℝ}
    (hA : ∀ i, A i < a i)
    (hB : ∀ i, b i < B i) :
    Set.Icc a b ⊆ Set.univ.pi (fun i => Set.Ioo (A i) (B i)) := by
  intro x hx i _hi
  exact ⟨lt_of_lt_of_le (hA i) (hx.1 i), lt_of_le_of_lt (hx.2 i) (hB i)⟩

/-- Smooth plateau for a finite closed Pi-box inside a strictly larger open
Pi-box.

The extra hypothesis `a ≤ b` records that the inner box is nonempty in the
intended exhaustion use.  The construction comes from the generic
compact-in-open plateau theorem in `Analysis.Calculus.Cutoff`; it gives both
plain- and topological-support containment, compact support, smoothness,
`[0, 1]` range, and equality to one on the whole inner box.

This is one chosen cutoff, not yet an exhausting family with derivative
bounds.  Tail passage, whole-space weighted integration by parts, generator
domains, invariant Gibbs law, reversibility, and KL/FI dissipation remain
separate obligations. -/
theorem exists_contDiff_cutoff_eq_one_on_Icc_tsupport_subset_outer_univ_pi_Ioo
    {n : ℕ} {a b A B : Fin (n + 1) → ℝ}
    (hab : a ≤ b)
    (hA : ∀ i, A i < a i)
    (hB : ∀ i, b i < B i) :
    ∃ χ : (Fin (n + 1) → ℝ) → ℝ,
      Function.support χ ⊆ Set.univ.pi (fun i => Set.Ioo (A i) (B i)) ∧
      tsupport χ ⊆ Set.univ.pi (fun i => Set.Ioo (A i) (B i)) ∧
      HasCompactSupport χ ∧
      ContDiff ℝ (⊤ : ℕ∞) χ ∧
      Set.range χ ⊆ Set.Icc 0 1 ∧
      Set.EqOn χ 1 (Set.Icc a b) := by
  have _hinner : (Set.Icc a b).Nonempty := ⟨a, le_rfl, hab⟩
  have hopen : IsOpen (Set.univ.pi fun i => Set.Ioo (A i) (B i)) := by
    exact isOpen_set_pi Set.finite_univ fun _ _ => isOpen_Ioo
  exact Cutoff.exists_contDiff_eq_one_tsupport_subset
    isCompact_Icc hopen (Icc_subset_univ_pi_Ioo_of_strict_bounds hA hB)

/-- Local smooth cutoff for a point in an inner closed Pi-box, supported in a
strictly larger open Pi-box.

This packages the closed-box-to-open-box inclusion with
`exists_contDiff_cutoff_support_subset_univ_pi_Ioo`.  It is a local cutoff at a
single point of the inner box; it does not construct one cutoff equal to `1` on
the whole inner box, choose an exhausting family, prove derivative bounds, or
pass to whole-space limits. -/
theorem exists_contDiff_cutoff_support_subset_outer_univ_pi_Ioo_of_mem_Icc
    {n : ℕ} {a b A B x : Fin (n + 1) → ℝ}
    (hA : ∀ i, A i < a i)
    (hB : ∀ i, b i < B i)
    (hx : x ∈ Set.Icc a b) :
    ∃ χ : (Fin (n + 1) → ℝ) → ℝ,
      Function.support χ ⊆ Set.univ.pi (fun i => Set.Ioo (A i) (B i)) ∧
      tsupport χ ⊆ Set.univ.pi (fun i => Set.Ioo (A i) (B i)) ∧
      HasCompactSupport χ ∧
      ContDiff ℝ (⊤ : ℕ∞) χ ∧
      Set.range χ ⊆ Set.Icc 0 1 ∧
      χ x = 1 :=
  exists_contDiff_cutoff_support_subset_univ_pi_Ioo
    (Icc_subset_univ_pi_Ioo_of_strict_bounds hA hB hx)

/-- Support contained in the open box implies Mathlib's finite-box signed
face-term sum is zero.

This is still only a finite-box support-to-face producer.  It does not prove
that a concrete Langevin/cutoff vector field has this support, and it does not
prove whole-space integration by parts or stationarity. -/
theorem signedFaceTermSum_eq_zero_of_support_subset_univ_pi_Ioo
    {n : ℕ}
    (a b : Fin (n + 1) → ℝ)
    (F : (Fin (n + 1) → ℝ) → Fin (n + 1) → ℝ)
    (hsupp : Function.support F ⊆ (Set.univ.pi fun i => Set.Ioo (a i) (b i))) :
    ∑ i : Fin (n + 1),
        ((∫ x in Set.Icc (a ∘ i.succAbove) (b ∘ i.succAbove),
            F (i.insertNth (b i) x) i) -
          ∫ x in Set.Icc (a ∘ i.succAbove) (b ∘ i.succAbove),
            F (i.insertNth (a i) x) i) = 0 :=
  signedFaceTermSum_eq_zero_of_eq_zero_off_univ_pi_Ioo a b F
    (eq_zero_off_univ_pi_Ioo_of_support_subset_univ_pi_Ioo a b F hsupp)

/-- If a scalar cutoff vanishes outside the open Pi-box, then multiplying any
Pi-space vector field by this cutoff gives a vector field supported in the open
Pi-box.

This is a plain support-containment leaf for finite-box boundary staging.  It
does not construct a smooth cutoff, prove topological compact support, or
discharge any differentiability/integrability hypotheses for the cutoff-smul
field. -/
theorem support_smul_subset_univ_pi_Ioo_of_eq_zero_off_univ_pi_Ioo
    {n : ℕ}
    (a b : Fin (n + 1) → ℝ)
    (χ : (Fin (n + 1) → ℝ) → ℝ)
    (G : (Fin (n + 1) → ℝ) → Fin (n + 1) → ℝ)
    (hχ : ∀ x ∉ (Set.univ.pi fun i => Set.Ioo (a i) (b i)), χ x = 0) :
    Function.support (fun x => χ x • G x) ⊆
      (Set.univ.pi fun i => Set.Ioo (a i) (b i)) := by
  intro x hx
  by_contra hxbox
  have hχ0 : χ x = 0 := hχ x hxbox
  have hzero : χ x • G x = 0 := by simp [hχ0]
  exact hx hzero

/-- If a scalar cutoff is supported in the open Pi-box, then multiplying any
Pi-space vector field by this cutoff gives a vector field supported in the open
Pi-box.

This only uses `Function.support`; it is not a `HasCompactSupport` theorem and
does not build a cutoff. -/
theorem support_smul_subset_univ_pi_Ioo_of_scalar_support_subset_univ_pi_Ioo
    {n : ℕ}
    (a b : Fin (n + 1) → ℝ)
    (χ : (Fin (n + 1) → ℝ) → ℝ)
    (G : (Fin (n + 1) → ℝ) → Fin (n + 1) → ℝ)
    (hχsupp : Function.support χ ⊆
      (Set.univ.pi fun i => Set.Ioo (a i) (b i))) :
    Function.support (fun x => χ x • G x) ⊆
      (Set.univ.pi fun i => Set.Ioo (a i) (b i)) := by
  exact support_smul_subset_univ_pi_Ioo_of_eq_zero_off_univ_pi_Ioo a b χ G
    (by
      intro x hxbox
      by_contra hχne
      exact hxbox (hχsupp hχne))

/-- If the topological support of a scalar cutoff is contained in the open
Pi-box, then multiplying any vector field by that cutoff is plain-supported in
the same open box.

This is the direct consumer-facing bridge from Mathlib's `tsupport` cutoff
output to the cutoff-smul support hypothesis used by the finite-box zero-face
route.  It does not prove cutoff construction, regularity of the smul field,
tail decay, or whole-space integration by parts. -/
theorem support_smul_subset_univ_pi_Ioo_of_scalar_tsupport_subset_univ_pi_Ioo
    {n : ℕ}
    (a b : Fin (n + 1) → ℝ)
    (χ : (Fin (n + 1) → ℝ) → ℝ)
    (G : (Fin (n + 1) → ℝ) → Fin (n + 1) → ℝ)
    (hχtsupp : tsupport χ ⊆
      Set.univ.pi (fun i => Set.Ioo (a i) (b i))) :
    Function.support (fun x => χ x • G x) ⊆
      (Set.univ.pi fun i => Set.Ioo (a i) (b i)) :=
  support_smul_subset_univ_pi_Ioo_of_scalar_support_subset_univ_pi_Ioo a b χ G
    (support_subset_univ_pi_Ioo_of_tsupport_subset_univ_pi_Ioo hχtsupp)

/-- Closed-box continuity for a scalar cutoff times a Pi-space vector field.

This packages Mathlib's `ContinuousOn.smul` in the exact finite-box shape used
by the cutoff-smul divergence-theorem route.  It does not prove smooth cutoff
construction, differentiability, trace integrability, or any boundary result. -/
theorem continuousOn_smul_vectorField_of_continuousOn
    {n : ℕ}
    (a b : Fin (n + 1) → ℝ)
    (χ : (Fin (n + 1) → ℝ) → ℝ)
    (G : (Fin (n + 1) → ℝ) → Fin (n + 1) → ℝ)
    (hχ : ContinuousOn χ (Set.Icc a b))
    (hG : ContinuousOn G (Set.Icc a b)) :
    ContinuousOn (fun x => χ x • G x) (Set.Icc a b) :=
  hχ.smul hG

/-- Pointwise Frechet derivative for a scalar cutoff times a Pi-space vector
field.

The derivative is exactly the Mathlib product-rule derivative
`χ x • G' + χ'.smulRight (G x)`.  This is only a pointwise derivative leaf; it
does not prove continuity, trace integrability, boundary cancellation, or
weighted integration by parts. -/
theorem hasFDerivAt_smul_vectorField_of_hasFDerivAt
    {n : ℕ}
    (χ : (Fin (n + 1) → ℝ) → ℝ)
    (χ' : (Fin (n + 1) → ℝ) →L[ℝ] ℝ)
    (G : (Fin (n + 1) → ℝ) → Fin (n + 1) → ℝ)
    (G' : (Fin (n + 1) → ℝ) →L[ℝ] (Fin (n + 1) → ℝ))
    (x : Fin (n + 1) → ℝ)
    (hχ : HasFDerivAt χ χ' x)
    (hG : HasFDerivAt G G' x) :
    HasFDerivAt (fun y => χ y • G y)
      (χ x • G' + χ'.smulRight (G x)) x := by
  simpa using hχ.smul hG

/-- Open-box/off-countable Frechet derivative wrapper for a scalar cutoff times
a Pi-space vector field.

This derives the `Hd` shape required by the finite-box divergence-theorem
handoffs from separate derivative hypotheses for the scalar cutoff and the
vector field on the same open-box minus exceptional set.  It still does not
prove trace integrability or any no-boundary conclusion. -/
theorem hasFDerivAt_smul_vectorField_off_countable
    {n : ℕ}
    (a b : Fin (n + 1) → ℝ)
    (χ : (Fin (n + 1) → ℝ) → ℝ)
    (χ' : (Fin (n + 1) → ℝ) → (Fin (n + 1) → ℝ) →L[ℝ] ℝ)
    (G : (Fin (n + 1) → ℝ) → Fin (n + 1) → ℝ)
    (G' : (Fin (n + 1) → ℝ) →
      (Fin (n + 1) → ℝ) →L[ℝ] (Fin (n + 1) → ℝ))
    (s : Set (Fin (n + 1) → ℝ))
    (hχ : ∀ x ∈ (Set.univ.pi fun i => Set.Ioo (a i) (b i)) \ s,
      HasFDerivAt χ (χ' x) x)
    (hG : ∀ x ∈ (Set.univ.pi fun i => Set.Ioo (a i) (b i)) \ s,
      HasFDerivAt G (G' x) x) :
    ∀ x ∈ (Set.univ.pi fun i => Set.Ioo (a i) (b i)) \ s,
      HasFDerivAt (fun y => χ y • G y)
        (χ x • G' x + (χ' x).smulRight (G x)) x := by
  intro x hx
  exact hasFDerivAt_smul_vectorField_of_hasFDerivAt χ (χ' x) G (G' x) x
    (hχ x hx) (hG x hx)

/-- Closed-box continuity of the cutoff-smul product-rule trace from only the
coordinate component continuity needed by the trace summand.

The expanded summand is
`χ x * (G' x eᵢ)ᵢ + (χ' x eᵢ) * (G x)ᵢ`.  This leaf therefore assumes
continuity of exactly these component functions.  It does not prove that `χ'`
or `G'` are derivative fields, does not construct cutoffs, and does not prove
boundary cancellation or weighted integration by parts. -/
theorem continuousOn_smul_vectorField_trace_of_component_continuousOn
    {n : ℕ}
    (a b : Fin (n + 1) → ℝ)
    (χ : (Fin (n + 1) → ℝ) → ℝ)
    (χ' : (Fin (n + 1) → ℝ) → (Fin (n + 1) → ℝ) →L[ℝ] ℝ)
    (G : (Fin (n + 1) → ℝ) → Fin (n + 1) → ℝ)
    (G' : (Fin (n + 1) → ℝ) →
      (Fin (n + 1) → ℝ) →L[ℝ] (Fin (n + 1) → ℝ))
    (hχ : ContinuousOn χ (Set.Icc a b))
    (hG : ∀ i, ContinuousOn (fun x => G x i) (Set.Icc a b))
    (hχ' : ∀ i, ContinuousOn
      (fun x => χ' x (Pi.single i (1 : ℝ))) (Set.Icc a b))
    (hG' : ∀ i, ContinuousOn
      (fun x => (G' x (Pi.single i (1 : ℝ))) i) (Set.Icc a b)) :
    ContinuousOn
      (fun x => ∑ i, ((χ x • G' x + (χ' x).smulRight (G x))
        (Pi.single i (1 : ℝ))) i)
      (Set.Icc a b) := by
  refine continuousOn_finsetSum Finset.univ ?_
  intro i _hi
  have hscalar : ContinuousOn
      (fun x => χ x * ((G' x (Pi.single i (1 : ℝ))) i) +
        (χ' x (Pi.single i (1 : ℝ))) * G x i)
      (Set.Icc a b) :=
    (hχ.mul (hG' i)).add ((hχ' i).mul (hG i))
  simpa [add_apply, ContinuousLinearMap.smulRight_apply, Pi.smul_apply,
    smul_eq_mul] using hscalar

/-- Closed-box continuity of the cutoff-smul product-rule trace from component
continuity of the cutoff, cutoff derivative field, vector field, and vector
field derivative.

This only assembles continuity of the trace expression
`∑ i, ((χ x • G' x + (χ' x).smulRight (G x)) eᵢ)ᵢ`.  It does not prove that
`χ'` or `G'` are actual derivatives, does not identify the product-rule
operator with a canonical `fderiv`, and does not prove cutoff construction,
tail decay, weighted IBP, or invariant laws. -/
theorem continuousOn_smul_vectorField_trace_of_components
    {n : ℕ}
    (a b : Fin (n + 1) → ℝ)
    (χ : (Fin (n + 1) → ℝ) → ℝ)
    (χ' : (Fin (n + 1) → ℝ) → (Fin (n + 1) → ℝ) →L[ℝ] ℝ)
    (G : (Fin (n + 1) → ℝ) → Fin (n + 1) → ℝ)
    (G' : (Fin (n + 1) → ℝ) →
      (Fin (n + 1) → ℝ) →L[ℝ] (Fin (n + 1) → ℝ))
    (hχc : ContinuousOn χ (Set.Icc a b))
    (hχ'c : ContinuousOn χ' (Set.Icc a b))
    (hGc : ContinuousOn G (Set.Icc a b))
    (hG'c : ContinuousOn G' (Set.Icc a b)) :
    ContinuousOn
      (fun x => ∑ i, ((χ x • G' x + (χ' x).smulRight (G x))
        (Pi.single i (1 : ℝ))) i)
      (Set.Icc a b) := by
  exact continuousOn_smul_vectorField_trace_of_component_continuousOn a b χ χ' G G' hχc
    (fun i => (continuous_apply i).comp_continuousOn hGc)
    (fun i => hχ'c.clm_apply continuousOn_const)
    (fun i =>
      (continuous_apply i).comp_continuousOn
        (hG'c.clm_apply continuousOn_const))

/-- Closed-box integrability for the trace of the cutoff-smul product-rule
derivative, assuming that trace expression is continuous on the closed box.

This is a compact-box integrability handoff only.  It does not prove continuity
of the trace from component assumptions, construct a smooth cutoff, prove tail
decay, or pass from finite boxes to whole-space weighted integration by parts. -/
theorem integrableOn_smul_vectorField_trace_of_continuousOn
    {n : ℕ}
    (a b : Fin (n + 1) → ℝ)
    (χ : (Fin (n + 1) → ℝ) → ℝ)
    (χ' : (Fin (n + 1) → ℝ) → (Fin (n + 1) → ℝ) →L[ℝ] ℝ)
    (G : (Fin (n + 1) → ℝ) → Fin (n + 1) → ℝ)
    (G' : (Fin (n + 1) → ℝ) →
      (Fin (n + 1) → ℝ) →L[ℝ] (Fin (n + 1) → ℝ))
    (htrace : ContinuousOn
      (fun x => ∑ i, ((χ x • G' x + (χ' x).smulRight (G x))
        (Pi.single i (1 : ℝ))) i)
      (Set.Icc a b)) :
    IntegrableOn
      (fun x => ∑ i, ((χ x • G' x + (χ' x).smulRight (G x))
        (Pi.single i (1 : ℝ))) i)
      (Set.Icc a b) volume :=
  htrace.integrableOn_compact isCompact_Icc

/-- Scalar cutoff vanishing outside the open Pi-box implies Mathlib's finite-box
signed face-term sum is zero for the cutoff-smul vector field.

Regularity of the cutoff-smul field is not addressed here; this is only the
finite-box support-to-face producer. -/
theorem signedFaceTermSum_smul_eq_zero_of_cutoff_eq_zero_off_univ_pi_Ioo
    {n : ℕ}
    (a b : Fin (n + 1) → ℝ)
    (χ : (Fin (n + 1) → ℝ) → ℝ)
    (G : (Fin (n + 1) → ℝ) → Fin (n + 1) → ℝ)
    (hχ : ∀ x ∉ (Set.univ.pi fun i => Set.Ioo (a i) (b i)), χ x = 0) :
    ∑ i : Fin (n + 1),
        ((∫ x in Set.Icc (a ∘ i.succAbove) (b ∘ i.succAbove),
            (χ (i.insertNth (b i) x) • G (i.insertNth (b i) x)) i) -
          ∫ x in Set.Icc (a ∘ i.succAbove) (b ∘ i.succAbove),
            (χ (i.insertNth (a i) x) • G (i.insertNth (a i) x)) i) = 0 :=
  signedFaceTermSum_eq_zero_of_support_subset_univ_pi_Ioo a b (fun x => χ x • G x)
    (support_smul_subset_univ_pi_Ioo_of_eq_zero_off_univ_pi_Ioo a b χ G hχ)

/-- Scalar cutoff support contained in the open Pi-box implies Mathlib's
finite-box signed face-term sum is zero for the cutoff-smul vector field.

This is still a finite-box support-to-face producer, not a smooth-cutoff
construction or whole-space no-boundary theorem. -/
theorem signedFaceTermSum_smul_eq_zero_of_scalar_support_subset_univ_pi_Ioo
    {n : ℕ}
    (a b : Fin (n + 1) → ℝ)
    (χ : (Fin (n + 1) → ℝ) → ℝ)
    (G : (Fin (n + 1) → ℝ) → Fin (n + 1) → ℝ)
    (hχsupp : Function.support χ ⊆
      (Set.univ.pi fun i => Set.Ioo (a i) (b i))) :
    ∑ i : Fin (n + 1),
        ((∫ x in Set.Icc (a ∘ i.succAbove) (b ∘ i.succAbove),
            (χ (i.insertNth (b i) x) • G (i.insertNth (b i) x)) i) -
          ∫ x in Set.Icc (a ∘ i.succAbove) (b ∘ i.succAbove),
            (χ (i.insertNth (a i) x) • G (i.insertNth (a i) x)) i) = 0 :=
  signedFaceTermSum_eq_zero_of_support_subset_univ_pi_Ioo a b (fun x => χ x • G x)
    (support_smul_subset_univ_pi_Ioo_of_scalar_support_subset_univ_pi_Ioo a b χ G hχsupp)

/-- Scalar cutoff topological support contained in the open Pi-box implies
Mathlib's finite-box signed face-term sum is zero for the cutoff-smul vector
field.

This is a direct `tsupport`-API handoff for the local smooth-cutoff route.  It
does not construct the cutoff, prove regularity of the cutoff-smul field, pass
to a whole-space limit, or prove weighted integration by parts. -/
theorem signedFaceTermSum_smul_eq_zero_of_scalar_tsupport_subset_univ_pi_Ioo
    {n : ℕ}
    (a b : Fin (n + 1) → ℝ)
    (χ : (Fin (n + 1) → ℝ) → ℝ)
    (G : (Fin (n + 1) → ℝ) → Fin (n + 1) → ℝ)
    (hχtsupp : tsupport χ ⊆
      Set.univ.pi (fun i => Set.Ioo (a i) (b i))) :
    ∑ i : Fin (n + 1),
        ((∫ x in Set.Icc (a ∘ i.succAbove) (b ∘ i.succAbove),
            (χ (i.insertNth (b i) x) • G (i.insertNth (b i) x)) i) -
          ∫ x in Set.Icc (a ∘ i.succAbove) (b ∘ i.succAbove),
            (χ (i.insertNth (a i) x) • G (i.insertNth (a i) x)) i) = 0 :=
  signedFaceTermSum_smul_eq_zero_of_scalar_support_subset_univ_pi_Ioo a b χ G
    (support_subset_univ_pi_Ioo_of_tsupport_subset_univ_pi_Ioo hχtsupp)

/-- Finite-box zero-face corollary for ASTIS coordinate divergence.

This is the smallest finite-box integration-by-parts handoff: once the signed
face term from Mathlib's divergence theorem is explicitly known to vanish, the
box integral of the coordinate divergence is zero.

It does not prove that the face term vanishes, does not pass to whole space,
and does not state a Langevin invariant law. -/
theorem integral_coordinateDivergence_toPi_box_eq_zero_of_integrableOn_trace_of_hasFDerivAt_off_countable
    {n : ℕ}
    (a b : Fin (n + 1) → ℝ) (hle : a ≤ b)
    (F : (Fin (n + 1) → ℝ) → Fin (n + 1) → ℝ)
    (F' : (Fin (n + 1) → ℝ) →
      (Fin (n + 1) → ℝ) →L[ℝ] (Fin (n + 1) → ℝ))
    (s : Set (Fin (n + 1) → ℝ)) (hs : s.Countable)
    (Hc : ContinuousOn F (Set.Icc a b))
    (Hd : ∀ x ∈ (Set.univ.pi fun i => Set.Ioo (a i) (b i)) \ s,
      HasFDerivAt F (F' x) x)
    (Hi_trace : IntegrableOn (fun x => ∑ i, F' x (Pi.single i (1 : ℝ)) i)
      (Set.Icc a b) volume)
    (hfaces :
      ∑ i : Fin (n + 1),
        ((∫ x in Set.Icc (a ∘ i.succAbove) (b ∘ i.succAbove),
            F (i.insertNth (b i) x) i) -
          ∫ x in Set.Icc (a ∘ i.succAbove) (b ∘ i.succAbove),
            F (i.insertNth (a i) x) i) = 0) :
    ∫ x in Set.Icc a b, coordinateDivergence
        (fun y : EuclideanSpace ℝ (Fin (n + 1)) =>
          (WithLp.toLp 2 (F (WithLp.ofLp y)) :
            EuclideanSpace ℝ (Fin (n + 1))))
        (WithLp.toLp 2 x : EuclideanSpace ℝ (Fin (n + 1))) = 0 := by
  rw [integral_coordinateDivergence_toPi_box_of_integrableOn_trace_of_hasFDerivAt_off_countable
    a b hle F F' s hs Hc Hd Hi_trace, hfaces]

/-- Finite-box coordinate-divergence integral vanishes when the vector field's
normal component is explicitly zero on every lower and upper face.

This composes the finite-box signed-face divergence theorem with the
componentwise boundary-value producer
`signedFaceTermSum_eq_zero_of_boundary_component_eq_zero`.  It is still a
finite-box conditional result: it does not derive compact support or tail
decay, does not pass to whole space, and does not state a Langevin invariant
law. -/
theorem integral_coordinateDivergence_toPi_box_eq_zero_of_boundary_component_eq_zero
    {n : ℕ}
    (a b : Fin (n + 1) → ℝ) (hle : a ≤ b)
    (F : (Fin (n + 1) → ℝ) → Fin (n + 1) → ℝ)
    (F' : (Fin (n + 1) → ℝ) →
      (Fin (n + 1) → ℝ) →L[ℝ] (Fin (n + 1) → ℝ))
    (s : Set (Fin (n + 1) → ℝ)) (hs : s.Countable)
    (Hc : ContinuousOn F (Set.Icc a b))
    (Hd : ∀ x ∈ (Set.univ.pi fun i => Set.Ioo (a i) (b i)) \ s,
      HasFDerivAt F (F' x) x)
    (Hi_trace : IntegrableOn (fun x => ∑ i, F' x (Pi.single i (1 : ℝ)) i)
      (Set.Icc a b) volume)
    (hupper : ∀ (i : Fin (n + 1)) (x : Fin n → ℝ),
      F (i.insertNth (b i) x) i = 0)
    (hlower : ∀ (i : Fin (n + 1)) (x : Fin n → ℝ),
      F (i.insertNth (a i) x) i = 0) :
    ∫ x in Set.Icc a b, coordinateDivergence
        (fun y : EuclideanSpace ℝ (Fin (n + 1)) =>
          (WithLp.toLp 2 (F (WithLp.ofLp y)) :
            EuclideanSpace ℝ (Fin (n + 1))))
        (WithLp.toLp 2 x : EuclideanSpace ℝ (Fin (n + 1))) = 0 := by
  exact integral_coordinateDivergence_toPi_box_eq_zero_of_integrableOn_trace_of_hasFDerivAt_off_countable
    a b hle F F' s hs Hc Hd Hi_trace
    (signedFaceTermSum_eq_zero_of_boundary_component_eq_zero a b F hupper hlower)

/-- Finite-box coordinate-divergence integral vanishes from `Function.update`
boundary-value hypotheses.

This is the `Function.update`-shaped companion to
`integral_coordinateDivergence_toPi_box_eq_zero_of_boundary_component_eq_zero`.
It is intended as a staging point for later compact-support or cutoff leaves.
It still does not prove compact support, tail decay, whole-space weighted IBP,
generator domains, invariant laws, or reversibility. -/
theorem integral_coordinateDivergence_toPi_box_eq_zero_of_update_boundary_component_eq_zero
    {n : ℕ}
    (a b : Fin (n + 1) → ℝ) (hle : a ≤ b)
    (F : (Fin (n + 1) → ℝ) → Fin (n + 1) → ℝ)
    (F' : (Fin (n + 1) → ℝ) →
      (Fin (n + 1) → ℝ) →L[ℝ] (Fin (n + 1) → ℝ))
    (s : Set (Fin (n + 1) → ℝ)) (hs : s.Countable)
    (Hc : ContinuousOn F (Set.Icc a b))
    (Hd : ∀ x ∈ (Set.univ.pi fun i => Set.Ioo (a i) (b i)) \ s,
      HasFDerivAt F (F' x) x)
    (Hi_trace : IntegrableOn (fun x => ∑ i, F' x (Pi.single i (1 : ℝ)) i)
      (Set.Icc a b) volume)
    (hupper : ∀ (i : Fin (n + 1)) (x : Fin (n + 1) → ℝ),
      F (Function.update x i (b i)) i = 0)
    (hlower : ∀ (i : Fin (n + 1)) (x : Fin (n + 1) → ℝ),
      F (Function.update x i (a i)) i = 0) :
    ∫ x in Set.Icc a b, coordinateDivergence
        (fun y : EuclideanSpace ℝ (Fin (n + 1)) =>
          (WithLp.toLp 2 (F (WithLp.ofLp y)) :
            EuclideanSpace ℝ (Fin (n + 1))))
        (WithLp.toLp 2 x : EuclideanSpace ℝ (Fin (n + 1))) = 0 := by
  exact integral_coordinateDivergence_toPi_box_eq_zero_of_integrableOn_trace_of_hasFDerivAt_off_countable
    a b hle F F' s hs Hc Hd Hi_trace
    (signedFaceTermSum_eq_zero_of_update_boundary_component_eq_zero a b F hupper hlower)

/-- Finite-box coordinate-divergence integral vanishes when the vector field
vanishes outside the open Pi-box.

This is still a finite-box conditional theorem: it assumes the trace
integrability and open-box/off-countable differentiability required by the
divergence theorem wrapper.  It does not pass to whole space, prove compact
support or tail decay, or state stationarity/invariance. -/
theorem integral_coordinateDivergence_toPi_box_eq_zero_of_eq_zero_off_univ_pi_Ioo
    {n : ℕ}
    (a b : Fin (n + 1) → ℝ) (hle : a ≤ b)
    (F : (Fin (n + 1) → ℝ) → Fin (n + 1) → ℝ)
    (F' : (Fin (n + 1) → ℝ) →
      (Fin (n + 1) → ℝ) →L[ℝ] (Fin (n + 1) → ℝ))
    (s : Set (Fin (n + 1) → ℝ)) (hs : s.Countable)
    (Hc : ContinuousOn F (Set.Icc a b))
    (Hd : ∀ x ∈ (Set.univ.pi fun i => Set.Ioo (a i) (b i)) \ s,
      HasFDerivAt F (F' x) x)
    (Hi_trace : IntegrableOn (fun x => ∑ i, F' x (Pi.single i (1 : ℝ)) i)
      (Set.Icc a b) volume)
    (hoff : ∀ x ∉ (Set.univ.pi fun i => Set.Ioo (a i) (b i)), F x = 0) :
    ∫ x in Set.Icc a b, coordinateDivergence
        (fun y : EuclideanSpace ℝ (Fin (n + 1)) =>
          (WithLp.toLp 2 (F (WithLp.ofLp y)) :
            EuclideanSpace ℝ (Fin (n + 1))))
        (WithLp.toLp 2 x : EuclideanSpace ℝ (Fin (n + 1))) = 0 := by
  exact integral_coordinateDivergence_toPi_box_eq_zero_of_integrableOn_trace_of_hasFDerivAt_off_countable
    a b hle F F' s hs Hc Hd Hi_trace
    (signedFaceTermSum_eq_zero_of_eq_zero_off_univ_pi_Ioo a b F hoff)

/-- Finite-box coordinate-divergence integral vanishes when the vector field's
support is contained in the open Pi-box.

This composes the support-to-face producer with the finite-box divergence
wrapper.  It is not a compact-support theorem, a cutoff construction, a
whole-space integration-by-parts theorem, or an invariant-law result. -/
theorem integral_coordinateDivergence_toPi_box_eq_zero_of_support_subset_univ_pi_Ioo
    {n : ℕ}
    (a b : Fin (n + 1) → ℝ) (hle : a ≤ b)
    (F : (Fin (n + 1) → ℝ) → Fin (n + 1) → ℝ)
    (F' : (Fin (n + 1) → ℝ) →
      (Fin (n + 1) → ℝ) →L[ℝ] (Fin (n + 1) → ℝ))
    (s : Set (Fin (n + 1) → ℝ)) (hs : s.Countable)
    (Hc : ContinuousOn F (Set.Icc a b))
    (Hd : ∀ x ∈ (Set.univ.pi fun i => Set.Ioo (a i) (b i)) \ s,
      HasFDerivAt F (F' x) x)
    (Hi_trace : IntegrableOn (fun x => ∑ i, F' x (Pi.single i (1 : ℝ)) i)
      (Set.Icc a b) volume)
    (hsupp : Function.support F ⊆ (Set.univ.pi fun i => Set.Ioo (a i) (b i))) :
    ∫ x in Set.Icc a b, coordinateDivergence
        (fun y : EuclideanSpace ℝ (Fin (n + 1)) =>
          (WithLp.toLp 2 (F (WithLp.ofLp y)) :
            EuclideanSpace ℝ (Fin (n + 1))))
        (WithLp.toLp 2 x : EuclideanSpace ℝ (Fin (n + 1))) = 0 := by
  exact integral_coordinateDivergence_toPi_box_eq_zero_of_integrableOn_trace_of_hasFDerivAt_off_countable
    a b hle F F' s hs Hc Hd Hi_trace
    (signedFaceTermSum_eq_zero_of_support_subset_univ_pi_Ioo a b F hsupp)

/-- Finite-box coordinate-divergence integral vanishes for a cutoff-smul vector
field when the scalar cutoff vanishes outside the open Pi-box.

This preserves the existing divergence-theorem hypotheses for the cutoff-smul
field: continuity on the closed box, off-countable Frechet differentiability,
and trace integrability are still explicit assumptions. -/
theorem integral_coordinateDivergence_toPi_box_eq_zero_of_cutoff_eq_zero_off_univ_pi_Ioo
    {n : ℕ}
    (a b : Fin (n + 1) → ℝ) (hle : a ≤ b)
    (χ : (Fin (n + 1) → ℝ) → ℝ)
    (G : (Fin (n + 1) → ℝ) → Fin (n + 1) → ℝ)
    (F' : (Fin (n + 1) → ℝ) →
      (Fin (n + 1) → ℝ) →L[ℝ] (Fin (n + 1) → ℝ))
    (s : Set (Fin (n + 1) → ℝ)) (hs : s.Countable)
    (Hc : ContinuousOn (fun x => χ x • G x) (Set.Icc a b))
    (Hd : ∀ x ∈ (Set.univ.pi fun i => Set.Ioo (a i) (b i)) \ s,
      HasFDerivAt (fun x => χ x • G x) (F' x) x)
    (Hi_trace : IntegrableOn (fun x => ∑ i, F' x (Pi.single i (1 : ℝ)) i)
      (Set.Icc a b) volume)
    (hχ : ∀ x ∉ (Set.univ.pi fun i => Set.Ioo (a i) (b i)), χ x = 0) :
    ∫ x in Set.Icc a b, coordinateDivergence
        (fun y : EuclideanSpace ℝ (Fin (n + 1)) =>
          (WithLp.toLp 2 ((χ (WithLp.ofLp y)) • G (WithLp.ofLp y)) :
            EuclideanSpace ℝ (Fin (n + 1))))
        (WithLp.toLp 2 x : EuclideanSpace ℝ (Fin (n + 1))) = 0 := by
  exact integral_coordinateDivergence_toPi_box_eq_zero_of_support_subset_univ_pi_Ioo
    a b hle (fun x => χ x • G x) F' s hs Hc Hd Hi_trace
    (support_smul_subset_univ_pi_Ioo_of_eq_zero_off_univ_pi_Ioo a b χ G hχ)

/-- Finite-box coordinate-divergence integral vanishes for a cutoff-smul vector
field when the scalar cutoff support is contained in the open Pi-box.

This is not a compact-support or whole-space IBP result; it simply feeds the
cutoff support condition into the finite-box zero-face handoff. -/
theorem integral_coordinateDivergence_toPi_box_eq_zero_of_scalar_support_subset_univ_pi_Ioo
    {n : ℕ}
    (a b : Fin (n + 1) → ℝ) (hle : a ≤ b)
    (χ : (Fin (n + 1) → ℝ) → ℝ)
    (G : (Fin (n + 1) → ℝ) → Fin (n + 1) → ℝ)
    (F' : (Fin (n + 1) → ℝ) →
      (Fin (n + 1) → ℝ) →L[ℝ] (Fin (n + 1) → ℝ))
    (s : Set (Fin (n + 1) → ℝ)) (hs : s.Countable)
    (Hc : ContinuousOn (fun x => χ x • G x) (Set.Icc a b))
    (Hd : ∀ x ∈ (Set.univ.pi fun i => Set.Ioo (a i) (b i)) \ s,
      HasFDerivAt (fun x => χ x • G x) (F' x) x)
    (Hi_trace : IntegrableOn (fun x => ∑ i, F' x (Pi.single i (1 : ℝ)) i)
      (Set.Icc a b) volume)
    (hχsupp : Function.support χ ⊆
      (Set.univ.pi fun i => Set.Ioo (a i) (b i))) :
    ∫ x in Set.Icc a b, coordinateDivergence
        (fun y : EuclideanSpace ℝ (Fin (n + 1)) =>
          (WithLp.toLp 2 ((χ (WithLp.ofLp y)) • G (WithLp.ofLp y)) :
            EuclideanSpace ℝ (Fin (n + 1))))
        (WithLp.toLp 2 x : EuclideanSpace ℝ (Fin (n + 1))) = 0 := by
  exact integral_coordinateDivergence_toPi_box_eq_zero_of_support_subset_univ_pi_Ioo
    a b hle (fun x => χ x • G x) F' s hs Hc Hd Hi_trace
    (support_smul_subset_univ_pi_Ioo_of_scalar_support_subset_univ_pi_Ioo a b χ G hχsupp)

/-- Finite-box coordinate-divergence integral vanishes for a cutoff-smul vector
field when the scalar cutoff's topological support is contained in the open
Pi-box.

This is a `tsupport`-API variant of the scalar-support finite-box handoff.  It
still assumes the cutoff-smul field's closed-box continuity, off-countable
Frechet differentiability, and trace integrability; it does not construct a
cutoff family, prove tail decay, or derive whole-space weighted IBP. -/
theorem integral_coordinateDivergence_toPi_box_eq_zero_of_scalar_tsupport_subset_univ_pi_Ioo
    {n : ℕ}
    (a b : Fin (n + 1) → ℝ) (hle : a ≤ b)
    (χ : (Fin (n + 1) → ℝ) → ℝ)
    (G : (Fin (n + 1) → ℝ) → Fin (n + 1) → ℝ)
    (F' : (Fin (n + 1) → ℝ) →
      (Fin (n + 1) → ℝ) →L[ℝ] (Fin (n + 1) → ℝ))
    (s : Set (Fin (n + 1) → ℝ)) (hs : s.Countable)
    (Hc : ContinuousOn (fun x => χ x • G x) (Set.Icc a b))
    (Hd : ∀ x ∈ (Set.univ.pi fun i => Set.Ioo (a i) (b i)) \ s,
      HasFDerivAt (fun x => χ x • G x) (F' x) x)
    (Hi_trace : IntegrableOn (fun x => ∑ i, F' x (Pi.single i (1 : ℝ)) i)
      (Set.Icc a b) volume)
    (hχtsupp : tsupport χ ⊆ Set.univ.pi (fun i => Set.Ioo (a i) (b i))) :
    ∫ x in Set.Icc a b, coordinateDivergence
        (fun y : EuclideanSpace ℝ (Fin (n + 1)) =>
          (WithLp.toLp 2 ((χ (WithLp.ofLp y)) • G (WithLp.ofLp y)) :
            EuclideanSpace ℝ (Fin (n + 1))))
        (WithLp.toLp 2 x : EuclideanSpace ℝ (Fin (n + 1))) = 0 :=
  integral_coordinateDivergence_toPi_box_eq_zero_of_scalar_support_subset_univ_pi_Ioo
    a b hle χ G F' s hs Hc Hd Hi_trace
    (support_subset_univ_pi_Ioo_of_tsupport_subset_univ_pi_Ioo hχtsupp)

/-- Finite-box coordinate-divergence integral vanishes for a cutoff-smul vector
field, deriving the continuity and off-countable Frechet differentiability
hypotheses from separate cutoff and vector-field regularity assumptions.

The trace integrability of the product-rule derivative remains an explicit
assumption.  This theorem is still finite-box only: it does not prove smooth
cutoff construction, tail limits, whole-space weighted IBP, generator domains,
invariant laws, reversibility, or KL/FI. -/
theorem integral_coordinateDivergence_toPi_box_eq_zero_of_cutoff_eq_zero_off_univ_pi_Ioo_of_regularity
    {n : ℕ}
    (a b : Fin (n + 1) → ℝ) (hle : a ≤ b)
    (χ : (Fin (n + 1) → ℝ) → ℝ)
    (χ' : (Fin (n + 1) → ℝ) → (Fin (n + 1) → ℝ) →L[ℝ] ℝ)
    (G : (Fin (n + 1) → ℝ) → Fin (n + 1) → ℝ)
    (G' : (Fin (n + 1) → ℝ) →
      (Fin (n + 1) → ℝ) →L[ℝ] (Fin (n + 1) → ℝ))
    (s : Set (Fin (n + 1) → ℝ)) (hs : s.Countable)
    (hχc : ContinuousOn χ (Set.Icc a b))
    (hGc : ContinuousOn G (Set.Icc a b))
    (hχd : ∀ x ∈ (Set.univ.pi fun i => Set.Ioo (a i) (b i)) \ s,
      HasFDerivAt χ (χ' x) x)
    (hGd : ∀ x ∈ (Set.univ.pi fun i => Set.Ioo (a i) (b i)) \ s,
      HasFDerivAt G (G' x) x)
    (Hi_trace : IntegrableOn
      (fun x => ∑ i, ((χ x • G' x + (χ' x).smulRight (G x))
        (Pi.single i (1 : ℝ))) i)
      (Set.Icc a b) volume)
    (hχzero : ∀ x ∉ (Set.univ.pi fun i => Set.Ioo (a i) (b i)), χ x = 0) :
    ∫ x in Set.Icc a b, coordinateDivergence
        (fun y : EuclideanSpace ℝ (Fin (n + 1)) =>
          (WithLp.toLp 2 ((χ (WithLp.ofLp y)) • G (WithLp.ofLp y)) :
            EuclideanSpace ℝ (Fin (n + 1))))
        (WithLp.toLp 2 x : EuclideanSpace ℝ (Fin (n + 1))) = 0 := by
  exact integral_coordinateDivergence_toPi_box_eq_zero_of_cutoff_eq_zero_off_univ_pi_Ioo
    a b hle χ G (fun x => χ x • G' x + (χ' x).smulRight (G x)) s hs
    (continuousOn_smul_vectorField_of_continuousOn a b χ G hχc hGc)
    (hasFDerivAt_smul_vectorField_off_countable a b χ χ' G G' s hχd hGd)
    Hi_trace hχzero

/-- Finite-box coordinate-divergence integral vanishes for a cutoff-smul vector
field when the scalar cutoff vanishes outside the open Pi-box, deriving the
regularity hypotheses from separate cutoff/vector-field assumptions and deriving
the product-rule trace integrability from a closed-box trace-continuity
hypothesis.

This closes only the compact-box trace-integrability side condition for the
cutoff-smul route.  It still does not construct a smooth cutoff, prove tail
limits, whole-space weighted IBP, generator domains, invariant laws,
reversibility, or KL/FI. -/
theorem integral_coordinateDivergence_toPi_box_eq_zero_of_cutoff_eq_zero_off_univ_pi_Ioo_of_trace_continuous
    {n : ℕ}
    (a b : Fin (n + 1) → ℝ) (hle : a ≤ b)
    (χ : (Fin (n + 1) → ℝ) → ℝ)
    (χ' : (Fin (n + 1) → ℝ) → (Fin (n + 1) → ℝ) →L[ℝ] ℝ)
    (G : (Fin (n + 1) → ℝ) → Fin (n + 1) → ℝ)
    (G' : (Fin (n + 1) → ℝ) →
      (Fin (n + 1) → ℝ) →L[ℝ] (Fin (n + 1) → ℝ))
    (s : Set (Fin (n + 1) → ℝ)) (hs : s.Countable)
    (hχc : ContinuousOn χ (Set.Icc a b))
    (hGc : ContinuousOn G (Set.Icc a b))
    (hχd : ∀ x ∈ (Set.univ.pi fun i => Set.Ioo (a i) (b i)) \ s,
      HasFDerivAt χ (χ' x) x)
    (hGd : ∀ x ∈ (Set.univ.pi fun i => Set.Ioo (a i) (b i)) \ s,
      HasFDerivAt G (G' x) x)
    (htrace : ContinuousOn
      (fun x => ∑ i, ((χ x • G' x + (χ' x).smulRight (G x))
        (Pi.single i (1 : ℝ))) i)
      (Set.Icc a b))
    (hχzero : ∀ x ∉ (Set.univ.pi fun i => Set.Ioo (a i) (b i)), χ x = 0) :
    ∫ x in Set.Icc a b, coordinateDivergence
        (fun y : EuclideanSpace ℝ (Fin (n + 1)) =>
          (WithLp.toLp 2 ((χ (WithLp.ofLp y)) • G (WithLp.ofLp y)) :
            EuclideanSpace ℝ (Fin (n + 1))))
        (WithLp.toLp 2 x : EuclideanSpace ℝ (Fin (n + 1))) = 0 := by
  exact integral_coordinateDivergence_toPi_box_eq_zero_of_cutoff_eq_zero_off_univ_pi_Ioo_of_regularity
    a b hle χ χ' G G' s hs hχc hGc hχd hGd
    (integrableOn_smul_vectorField_trace_of_continuousOn a b χ χ' G G' htrace)
    hχzero

/-- Component-continuity version of
`integral_coordinateDivergence_toPi_box_eq_zero_of_cutoff_eq_zero_off_univ_pi_Ioo_of_trace_continuous`.

It derives closed-box trace continuity from separate continuity assumptions on
`χ`, `χ'`, `G`, and `G'`, then discharges compact-box trace integrability.  It
still assumes the derivative hypotheses and cutoff vanishing needed by the
finite-box zero-face handoff, and remains below smooth cutoff construction,
tail limits, weighted IBP, generator domains, invariant laws, and reversibility. -/
theorem integral_coordinateDivergence_toPi_box_eq_zero_of_cutoff_eq_zero_off_univ_pi_Ioo_of_component_continuous
    {n : ℕ}
    (a b : Fin (n + 1) → ℝ) (hle : a ≤ b)
    (χ : (Fin (n + 1) → ℝ) → ℝ)
    (χ' : (Fin (n + 1) → ℝ) → (Fin (n + 1) → ℝ) →L[ℝ] ℝ)
    (G : (Fin (n + 1) → ℝ) → Fin (n + 1) → ℝ)
    (G' : (Fin (n + 1) → ℝ) →
      (Fin (n + 1) → ℝ) →L[ℝ] (Fin (n + 1) → ℝ))
    (s : Set (Fin (n + 1) → ℝ)) (hs : s.Countable)
    (hχc : ContinuousOn χ (Set.Icc a b))
    (hGc : ContinuousOn G (Set.Icc a b))
    (hχ'c : ∀ i, ContinuousOn
      (fun x => χ' x (Pi.single i (1 : ℝ))) (Set.Icc a b))
    (hG'c : ∀ i, ContinuousOn
      (fun x => (G' x (Pi.single i (1 : ℝ))) i) (Set.Icc a b))
    (hχd : ∀ x ∈ (Set.univ.pi fun i => Set.Ioo (a i) (b i)) \ s,
      HasFDerivAt χ (χ' x) x)
    (hGd : ∀ x ∈ (Set.univ.pi fun i => Set.Ioo (a i) (b i)) \ s,
      HasFDerivAt G (G' x) x)
    (hχzero : ∀ x ∉ (Set.univ.pi fun i => Set.Ioo (a i) (b i)), χ x = 0) :
    ∫ x in Set.Icc a b, coordinateDivergence
        (fun y : EuclideanSpace ℝ (Fin (n + 1)) =>
          (WithLp.toLp 2 ((χ (WithLp.ofLp y)) • G (WithLp.ofLp y)) :
            EuclideanSpace ℝ (Fin (n + 1))))
        (WithLp.toLp 2 x : EuclideanSpace ℝ (Fin (n + 1))) = 0 := by
  exact integral_coordinateDivergence_toPi_box_eq_zero_of_cutoff_eq_zero_off_univ_pi_Ioo_of_trace_continuous
    a b hle χ χ' G G' s hs hχc hGc hχd hGd
    (continuousOn_smul_vectorField_trace_of_component_continuousOn a b χ χ' G G' hχc
      (fun i => (continuous_apply i).comp_continuousOn hGc) hχ'c hG'c)
    hχzero

/-- Scalar-support version of
`integral_coordinateDivergence_toPi_box_eq_zero_of_cutoff_eq_zero_off_univ_pi_Ioo_of_regularity`.

It derives the cutoff-smul continuity and open-box/off-countable derivative
hypotheses, but still assumes trace integrability for the product-rule trace
and remains a finite-box handoff only. -/
theorem integral_coordinateDivergence_toPi_box_eq_zero_of_scalar_support_subset_univ_pi_Ioo_of_regularity
    {n : ℕ}
    (a b : Fin (n + 1) → ℝ) (hle : a ≤ b)
    (χ : (Fin (n + 1) → ℝ) → ℝ)
    (χ' : (Fin (n + 1) → ℝ) → (Fin (n + 1) → ℝ) →L[ℝ] ℝ)
    (G : (Fin (n + 1) → ℝ) → Fin (n + 1) → ℝ)
    (G' : (Fin (n + 1) → ℝ) →
      (Fin (n + 1) → ℝ) →L[ℝ] (Fin (n + 1) → ℝ))
    (s : Set (Fin (n + 1) → ℝ)) (hs : s.Countable)
    (hχc : ContinuousOn χ (Set.Icc a b))
    (hGc : ContinuousOn G (Set.Icc a b))
    (hχd : ∀ x ∈ (Set.univ.pi fun i => Set.Ioo (a i) (b i)) \ s,
      HasFDerivAt χ (χ' x) x)
    (hGd : ∀ x ∈ (Set.univ.pi fun i => Set.Ioo (a i) (b i)) \ s,
      HasFDerivAt G (G' x) x)
    (Hi_trace : IntegrableOn
      (fun x => ∑ i, ((χ x • G' x + (χ' x).smulRight (G x))
        (Pi.single i (1 : ℝ))) i)
      (Set.Icc a b) volume)
    (hχsupp : Function.support χ ⊆
      (Set.univ.pi fun i => Set.Ioo (a i) (b i))) :
    ∫ x in Set.Icc a b, coordinateDivergence
        (fun y : EuclideanSpace ℝ (Fin (n + 1)) =>
          (WithLp.toLp 2 ((χ (WithLp.ofLp y)) • G (WithLp.ofLp y)) :
            EuclideanSpace ℝ (Fin (n + 1))))
        (WithLp.toLp 2 x : EuclideanSpace ℝ (Fin (n + 1))) = 0 := by
  exact integral_coordinateDivergence_toPi_box_eq_zero_of_scalar_support_subset_univ_pi_Ioo
    a b hle χ G (fun x => χ x • G' x + (χ' x).smulRight (G x)) s hs
    (continuousOn_smul_vectorField_of_continuousOn a b χ G hχc hGc)
    (hasFDerivAt_smul_vectorField_off_countable a b χ χ' G G' s hχd hGd)
    Hi_trace hχsupp

/-- Canonical-`fderiv` scalar-support version of the cutoff-smul finite-box
zero integral handoff.

This removes only the supplied derivative-field parameter `G'`, replacing it
by `fderiv ℝ G` under open-box differentiability of `G`.  It remains a
finite-box handoff and does not construct a cutoff, prove trace integrability,
pass to whole space, prove weighted integration by parts, or prove an invariant
law. -/
theorem integral_coordinateDivergence_toPi_box_eq_zero_of_scalar_support_subset_univ_pi_Ioo_of_fderiv
    {n : ℕ}
    (a b : Fin (n + 1) → ℝ) (hle : a ≤ b)
    (χ : (Fin (n + 1) → ℝ) → ℝ)
    (χ' : (Fin (n + 1) → ℝ) → (Fin (n + 1) → ℝ) →L[ℝ] ℝ)
    (G : (Fin (n + 1) → ℝ) → Fin (n + 1) → ℝ)
    (s : Set (Fin (n + 1) → ℝ)) (hs : s.Countable)
    (hχc : ContinuousOn χ (Set.Icc a b))
    (hGc : ContinuousOn G (Set.Icc a b))
    (hχd : ∀ x ∈ (Set.univ.pi fun i => Set.Ioo (a i) (b i)) \ s,
      HasFDerivAt χ (χ' x) x)
    (hGd : ∀ x ∈ (Set.univ.pi fun i => Set.Ioo (a i) (b i)) \ s,
      DifferentiableAt ℝ G x)
    (Hi_trace : IntegrableOn
      (fun x => ∑ i, ((χ x • fderiv ℝ G x + (χ' x).smulRight (G x))
        (Pi.single i (1 : ℝ))) i)
      (Set.Icc a b) volume)
    (hχsupp : Function.support χ ⊆
      (Set.univ.pi fun i => Set.Ioo (a i) (b i))) :
    ∫ x in Set.Icc a b, coordinateDivergence
        (fun y : EuclideanSpace ℝ (Fin (n + 1)) =>
          (WithLp.toLp 2 ((χ (WithLp.ofLp y)) • G (WithLp.ofLp y)) :
            EuclideanSpace ℝ (Fin (n + 1))))
        (WithLp.toLp 2 x : EuclideanSpace ℝ (Fin (n + 1))) = 0 := by
  exact integral_coordinateDivergence_toPi_box_eq_zero_of_scalar_support_subset_univ_pi_Ioo_of_regularity
    a b hle χ χ' G (fun x => fderiv ℝ G x) s hs hχc hGc hχd
    (fun x hx => (hGd x hx).hasFDerivAt) Hi_trace hχsupp

/-- Scalar-support version of
`integral_coordinateDivergence_toPi_box_eq_zero_of_cutoff_eq_zero_off_univ_pi_Ioo_of_trace_continuous`.

It uses closed-box continuity of the product-rule trace to discharge the
compact-box trace-integrability side condition, but remains only a finite-box
cutoff-smul handoff. -/
theorem integral_coordinateDivergence_toPi_box_eq_zero_of_scalar_support_subset_univ_pi_Ioo_of_trace_continuous
    {n : ℕ}
    (a b : Fin (n + 1) → ℝ) (hle : a ≤ b)
    (χ : (Fin (n + 1) → ℝ) → ℝ)
    (χ' : (Fin (n + 1) → ℝ) → (Fin (n + 1) → ℝ) →L[ℝ] ℝ)
    (G : (Fin (n + 1) → ℝ) → Fin (n + 1) → ℝ)
    (G' : (Fin (n + 1) → ℝ) →
      (Fin (n + 1) → ℝ) →L[ℝ] (Fin (n + 1) → ℝ))
    (s : Set (Fin (n + 1) → ℝ)) (hs : s.Countable)
    (hχc : ContinuousOn χ (Set.Icc a b))
    (hGc : ContinuousOn G (Set.Icc a b))
    (hχd : ∀ x ∈ (Set.univ.pi fun i => Set.Ioo (a i) (b i)) \ s,
      HasFDerivAt χ (χ' x) x)
    (hGd : ∀ x ∈ (Set.univ.pi fun i => Set.Ioo (a i) (b i)) \ s,
      HasFDerivAt G (G' x) x)
    (htrace : ContinuousOn
      (fun x => ∑ i, ((χ x • G' x + (χ' x).smulRight (G x))
        (Pi.single i (1 : ℝ))) i)
      (Set.Icc a b))
    (hχsupp : Function.support χ ⊆
      (Set.univ.pi fun i => Set.Ioo (a i) (b i))) :
    ∫ x in Set.Icc a b, coordinateDivergence
        (fun y : EuclideanSpace ℝ (Fin (n + 1)) =>
          (WithLp.toLp 2 ((χ (WithLp.ofLp y)) • G (WithLp.ofLp y)) :
            EuclideanSpace ℝ (Fin (n + 1))))
        (WithLp.toLp 2 x : EuclideanSpace ℝ (Fin (n + 1))) = 0 := by
  exact integral_coordinateDivergence_toPi_box_eq_zero_of_scalar_support_subset_univ_pi_Ioo_of_regularity
    a b hle χ χ' G G' s hs hχc hGc hχd hGd
    (integrableOn_smul_vectorField_trace_of_continuousOn a b χ χ' G G' htrace)
    hχsupp

/-- Component-continuity scalar-support version of the cutoff-smul finite-box
trace handoff.

It derives the trace-continuity input from separate continuity assumptions on
`χ`, `χ'`, `G`, and `G'`, then applies the scalar-support zero-face handoff.
It is still finite-box only. -/
theorem integral_coordinateDivergence_toPi_box_eq_zero_of_scalar_support_subset_univ_pi_Ioo_of_component_continuous
    {n : ℕ}
    (a b : Fin (n + 1) → ℝ) (hle : a ≤ b)
    (χ : (Fin (n + 1) → ℝ) → ℝ)
    (χ' : (Fin (n + 1) → ℝ) → (Fin (n + 1) → ℝ) →L[ℝ] ℝ)
    (G : (Fin (n + 1) → ℝ) → Fin (n + 1) → ℝ)
    (G' : (Fin (n + 1) → ℝ) →
      (Fin (n + 1) → ℝ) →L[ℝ] (Fin (n + 1) → ℝ))
    (s : Set (Fin (n + 1) → ℝ)) (hs : s.Countable)
    (hχc : ContinuousOn χ (Set.Icc a b))
    (hGc : ContinuousOn G (Set.Icc a b))
    (hχ'c : ∀ i, ContinuousOn
      (fun x => χ' x (Pi.single i (1 : ℝ))) (Set.Icc a b))
    (hG'c : ∀ i, ContinuousOn
      (fun x => (G' x (Pi.single i (1 : ℝ))) i) (Set.Icc a b))
    (hχd : ∀ x ∈ (Set.univ.pi fun i => Set.Ioo (a i) (b i)) \ s,
      HasFDerivAt χ (χ' x) x)
    (hGd : ∀ x ∈ (Set.univ.pi fun i => Set.Ioo (a i) (b i)) \ s,
      HasFDerivAt G (G' x) x)
    (hχsupp : Function.support χ ⊆
      (Set.univ.pi fun i => Set.Ioo (a i) (b i))) :
    ∫ x in Set.Icc a b, coordinateDivergence
        (fun y : EuclideanSpace ℝ (Fin (n + 1)) =>
          (WithLp.toLp 2 ((χ (WithLp.ofLp y)) • G (WithLp.ofLp y)) :
            EuclideanSpace ℝ (Fin (n + 1))))
        (WithLp.toLp 2 x : EuclideanSpace ℝ (Fin (n + 1))) = 0 := by
  exact integral_coordinateDivergence_toPi_box_eq_zero_of_scalar_support_subset_univ_pi_Ioo_of_trace_continuous
    a b hle χ χ' G G' s hs hχc hGc hχd hGd
    (continuousOn_smul_vectorField_trace_of_component_continuousOn a b χ χ' G G' hχc
      (fun i => (continuous_apply i).comp_continuousOn hGc) hχ'c hG'c)
    hχsupp

/-- The whole-space coordinate-divergence integral of a compactly supported
`C¹` vector field is zero.

The field is represented in raw finite-Pi coordinates, while
`coordinateDivergence` is evaluated after the canonical `PiLp` transport to
Euclidean space.  The proof encloses `tsupport F` in a strict finite box,
derives trace integrability from `C¹` regularity, invokes Mathlib's finite-box
divergence theorem through the ASTIS zero-face wrapper, and then removes the
box because the derivative vanishes off `tsupport F`.

This is a reusable whole-space no-boundary leaf.  It contains no Gibbs,
Langevin, generator-domain, semigroup, or invariant-measure semantics. -/
theorem integral_coordinateDivergence_wrapped_eq_zero_of_contDiff_of_hasCompactSupport
    {n : ℕ}
    (F : (Fin (n + 1) → ℝ) → Fin (n + 1) → ℝ)
    (hF : ContDiff ℝ 1 F)
    (hF_support : HasCompactSupport F) :
    ∫ x : Fin (n + 1) → ℝ,
        coordinateDivergence
          (fun y : EuclideanSpace ℝ (Fin (n + 1)) =>
            (WithLp.toLp 2 (F (WithLp.ofLp y)) :
              EuclideanSpace ℝ (Fin (n + 1))))
          (WithLp.toLp 2 x : EuclideanSpace ℝ (Fin (n + 1))) = 0 := by
  obtain ⟨R, hR, htsupport_ball⟩ :=
    hF_support.isCompact.isBounded.subset_ball_lt 0
      (0 : Fin (n + 1) → ℝ)
  let a : Fin (n + 1) → ℝ := fun _ => -R
  let b : Fin (n + 1) → ℝ := fun _ => R
  have hab : a ≤ b := by
    intro i
    dsimp [a, b]
    linarith
  have hopen_closed :
      (Set.univ.pi fun i => Set.Ioo (a i) (b i)) ⊆ Set.Icc a b := by
    intro x hx
    rw [Set.mem_pi] at hx
    exact Set.mem_Icc.2 ⟨fun i => (hx i (Set.mem_univ i)).1.le,
      fun i => (hx i (Set.mem_univ i)).2.le⟩
  have hball_open : Metric.ball (0 : Fin (n + 1) → ℝ) R ⊆
      (Set.univ.pi fun i => Set.Ioo (a i) (b i)) := by
    intro x hxball
    have hxnorm : ‖x‖ < R := by
      simpa [Metric.mem_ball, dist_zero_right] using hxball
    rw [Set.mem_pi]
    intro i _hi
    have hxi : |x i| < R := by
      calc
        |x i| = ‖x i‖ := (Real.norm_eq_abs _).symm
        _ ≤ ‖x‖ := norm_le_pi_norm x i
        _ < R := hxnorm
    simpa [a, b] using (abs_lt.mp hxi)
  have hsupport : Function.support F ⊆
      (Set.univ.pi fun i => Set.Ioo (a i) (b i)) := by
    intro x hx
    exact hball_open (htsupport_ball (subset_tsupport F hx))
  have htrace_cont : Continuous
      (fun x : Fin (n + 1) → ℝ =>
        ∑ i, fderiv ℝ F x (Pi.single i (1 : ℝ)) i) := by
    apply continuous_finsetSum
    intro i _hi
    exact (continuous_apply i).comp
      (hF.continuous_fderiv one_ne_zero |>.clm_apply continuous_const)
  have hbox :
      ∫ x in Set.Icc a b,
          coordinateDivergence
            (fun y : EuclideanSpace ℝ (Fin (n + 1)) =>
              (WithLp.toLp 2 (F (WithLp.ofLp y)) :
                EuclideanSpace ℝ (Fin (n + 1))))
            (WithLp.toLp 2 x : EuclideanSpace ℝ (Fin (n + 1))) = 0 := by
    apply integral_coordinateDivergence_toPi_box_eq_zero_of_support_subset_univ_pi_Ioo
      a b hab F (fun x => fderiv ℝ F x) ∅ Set.countable_empty
    · exact hF.continuous.continuousOn
    · intro x _hx
      exact (hF.differentiable one_ne_zero x).hasFDerivAt
    · exact htrace_cont.continuousOn.integrableOn_compact isCompact_Icc
    · exact hsupport
  calc
    ∫ x : Fin (n + 1) → ℝ,
        coordinateDivergence
          (fun y : EuclideanSpace ℝ (Fin (n + 1)) =>
            (WithLp.toLp 2 (F (WithLp.ofLp y)) :
              EuclideanSpace ℝ (Fin (n + 1))))
          (WithLp.toLp 2 x : EuclideanSpace ℝ (Fin (n + 1))) =
        ∫ x in Set.Icc a b,
          coordinateDivergence
            (fun y : EuclideanSpace ℝ (Fin (n + 1)) =>
              (WithLp.toLp 2 (F (WithLp.ofLp y)) :
                EuclideanSpace ℝ (Fin (n + 1))))
            (WithLp.toLp 2 x : EuclideanSpace ℝ (Fin (n + 1))) := by
      symm
      apply setIntegral_eq_integral_of_forall_compl_eq_zero
      intro x hx
      have hxtsupport : x ∉ tsupport F := by
        intro hxt
        exact hx (hopen_closed (hball_open (htsupport_ball hxt)))
      have hzero := coordinateDivergence_wrapped_toPi_trace_of_hasFDerivAt
        (ι := Fin (n + 1)) (HasFDerivAt.of_notMem_tsupport ℝ hxtsupport)
      simpa using hzero
    _ = 0 := hbox

end Divergence
end Calculus
end Analysis
end TechnicalLemmas
end AutoSamplingTheory
