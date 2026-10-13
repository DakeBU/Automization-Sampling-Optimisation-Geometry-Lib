import AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.WeightedGradientWeak
import Mathlib.MeasureTheory.Function.LocallyIntegrable

/-!
# Distributional meaning of the same weighted gradient closure

PBPS arXiv:2609.06905v1 Appendix C.1 analytic prerequisite, continuing the
weighted compact-test identity. Inverse positive Gibbs weights give local
volume integrability and genuine ordinary weak derivatives of L2 classes.
This is not the converse domain characterization, H2 regularity, an operator
core of D*D, a Poincare theorem or full paper completion.
-/

namespace AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.WeightedGradientDistribution

open MeasureTheory InnerProductSpace
open scoped RealInnerProductSpace ContDiff Topology

variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
  [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]

private theorem lp_locallyIntegrable_volume {F : Type*} [NormedAddCommGroup F]
    [NormedSpace ℝ F] (W : E → ℝ) (hW : Continuous W)
    (hI : Integrable (fun x => Real.exp (-W x)))
    (f : Lp F 2 ((volume : Measure E).tilted (fun x => -W x))) :
    LocallyIntegrable (fun x => f x) := by
  let μ := (volume : Measure E).tilted (fun x => -W x)
  let : IsProbabilityMeasure μ := isProbabilityMeasure_tilted hI
  have hi : Integrable (fun x => f x) μ :=
    MemLp.integrable (by norm_num : (1 : ENNReal) ≤ 2) (Lp.memLp f)
  have hr : Integrable (fun x => Real.exp (-W x) • f x) :=
    (integrable_tilted_iff hI _).mp hi
  have hl : LocallyIntegrable (fun x => Real.exp (W x) •
      (Real.exp (-W x) • f x)) (volume : Measure E) :=
    LocallyIntegrable.continuous_smul (μ := (volume : Measure E))
      (Real.continuous_exp.comp hW) hr.locallyIntegrable
  simpa only [smul_smul, ← Real.exp_add, add_neg_cancel, Real.exp_zero, one_smul] using hl

/-- Elements of the same closed weighted gradient graph have locally integrable
volume representatives and satisfy the ordinary weak gradient identity, with
both test products integrable. No differentiability of L2 representatives is
assumed, and no reverse characterization of the closure domain is asserted. -/
theorem closed_gradient_distributional (W : E → ℝ) (hW : ContDiff ℝ 1 W)
    (hI : Integrable (fun x => Real.exp (-W x))) :
    let μ := (volume : Measure E).tilted (fun x => -W x)
    ∀ (D : Lp ℝ 2 μ →ₗ.[ℝ] Lp E 2 μ), D.IsClosable →
      (∀ (u : Lp ℝ 2 μ) (G : Lp E 2 μ), (u,G) ∈ D.graph ↔
        ∃ f : E → ℝ, ContDiff ℝ ∞ f ∧ HasCompactSupport f ∧
          u =ᵐ[μ] f ∧ G =ᵐ[μ] gradient f) →
      ∀ (u : Lp ℝ 2 μ) (G : Lp E 2 μ), (u,G) ∈ D.closure.graph →
        LocallyIntegrable (fun x => u x) ∧ LocallyIntegrable (fun x => G x) ∧
        ∀ (ψ : E → ℝ), ContDiff ℝ 1 ψ → HasCompactSupport ψ → ∀ v : E,
          Integrable (fun x => ψ x * inner ℝ (G x) v) ∧
          Integrable (fun x => u x * fderiv ℝ ψ x v) ∧
          (∫ x, ψ x * inner ℝ (G x) v) = - ∫ x, u x * fderiv ℝ ψ x v := by
  let μ := (volume : Measure E).tilted (fun x => -W x)
  dsimp only
  intro D hD hgraph u G hu
  refine ⟨lp_locallyIntegrable_volume W hW.continuous hI u,
    lp_locallyIntegrable_volume W hW.continuous hI G, ?_⟩
  intro ψ hψ hc v
  let φ := fun x => Real.exp (W x) * ψ x
  have hφ : ContDiff ℝ 1 φ := hW.exp.mul hψ
  have hφc : HasCompactSupport φ := hc.mul_left
  have hq (x : E) : fderiv ℝ φ x v - φ x * fderiv ℝ W x v =
      Real.exp (W x) * fderiv ℝ ψ x v := by
    have hd := ((hW.differentiable one_ne_zero x).hasFDerivAt.exp).mul
      (hψ.differentiable one_ne_zero x).hasFDerivAt
    rw [show fderiv ℝ φ x = _ from hd.fderiv]
    simp only [add_apply, smul_apply, smul_eq_mul]
    dsimp [φ]
    ring
  have hcancel (x : E) : Real.exp (-W x) * Real.exp (W x) = 1 := by
    rw [← Real.exp_add]
    simp
  have hl (x : E) : Real.exp (-W x) * (φ x * inner ℝ (G x) v) =
      ψ x * inner ℝ (G x) v := by
    dsimp only [φ]
    rw [← mul_assoc, ← mul_assoc, hcancel, one_mul]
  have hr (x : E) : Real.exp (-W x) *
      (u x * (fderiv ℝ φ x v - φ x * fderiv ℝ W x v)) = u x * fderiv ℝ ψ x v := by
    rw [hq]
    calc
      _ = (Real.exp (-W x) * Real.exp (W x)) * (u x * fderiv ℝ ψ x v) := by ring
      _ = _ := by rw [hcancel, one_mul]
  obtain ⟨hleft,hright,he⟩ := WeightedGradientWeak.closed_gradient_weighted_ibp
    W hW hI D hD hgraph u G hu φ hφ hφc v
  have hli := (integrable_tilted_iff hI _).mp hleft
  have hri := (integrable_tilted_iff hI _).mp hright
  simp only [smul_eq_mul, hl, hr] at hli hri
  refine ⟨hli,hri,?_⟩
  have ht (g : E → ℝ) : (∫ x, g x ∂μ) =
      (∫ x, Real.exp (-W x))⁻¹ * ∫ x, Real.exp (-W x) * g x := by
    rw [show μ = (volume : Measure E).tilted (fun x => -W x) from rfl, integral_tilted]
    rw [← integral_const_mul]
    apply integral_congr_ae
    filter_upwards [] with x
    change (Real.exp (-W x) / (∫ z, Real.exp (-W z))) • g x = _
    simp only [smul_eq_mul, div_eq_mul_inv]
    ring
  change (∫ x, φ x * inner ℝ (G x) v ∂μ) =
    -∫ x, u x * (fderiv ℝ φ x v - φ x * fderiv ℝ W x v) ∂μ at he
  rw [ht, ht] at he
  simp only [hl, hr, ← mul_neg] at he
  exact mul_left_cancel₀ (inv_ne_zero (integral_exp_pos hI).ne') he

end AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.WeightedGradientDistribution
