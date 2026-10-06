import AutoSamplingTheory.ExampleCases.ProximalBPS.ConditionalC1Resolvent
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Deriv
import Mathlib.Analysis.InnerProductSpace.NormPow
import Mathlib.Analysis.Calculus.BumpFunction.Convolution

set_option autoImplicit false
set_option backward.isDefEq.respectTransparency false
noncomputable section
open Set MeasureTheory ProbabilityTheory InnerProductSpace
open scoped NNReal ContDiff RealInnerProductSpace Topology
namespace Tests.CompactC1GradientDomain

private def potential (x : ℝ) : ℝ := (3/8)*x^2 + (1/8)*Real.sin x
private theorem potential_curvature :
    ∀ z v : ℝ, (1/(2*(1:ℝ)))*‖v‖^2 ≤ (fderiv ℝ (fderiv ℝ potential) z v) v ∧
      (fderiv ℝ (fderiv ℝ potential) z v) v ≤ ‖v‖^2 := by
  have hder (z : ℝ) : HasDerivAt potential ((3/4)*z+(1/8)*Real.cos z) z := by
    convert (((hasDerivAt_id z).pow 2).const_mul (3/8)).add
      ((Real.hasDerivAt_sin z).const_mul (1/8)) using 1 <;> first | rfl | (simp [potential, Pi.add_apply, mul_comm]; ring)
  have hD : fderiv ℝ potential = fun z =>
      ((3/4)*z+(1/8)*Real.cos z) • ContinuousLinearMap.id ℝ ℝ := by
    funext z
    ext
    rw [fderiv_eq_smul_deriv, (hder z).deriv]
    simp
  have hDD (z v : ℝ) : (fderiv ℝ (fderiv ℝ potential) z v) v =
      ((3/4)-(1/8)*Real.sin z)*v^2 := by
    have hd : HasDerivAt (fun w : ℝ => (3/4)*w+(1/8)*Real.cos w)
        ((3/4)-(1/8)*Real.sin z) z := by
      convert ((hasDerivAt_id z).const_mul (3/4)).add
        ((Real.hasDerivAt_cos z).const_mul (1/8)) using 1 <;> (try dsimp only [id]) <;> first | rfl | ring
    rw [hD, fderiv_eq_smul_deriv,
      (hd.smul_const (ContinuousLinearMap.id ℝ ℝ)).deriv]
    simp
    ring
  intro z v
  rw [hDD]
  simp only [Real.norm_eq_abs, sq_abs]
  constructor <;> nlinarith [Real.sin_le_one z, Real.neg_one_le_sin z, sq_nonneg v]



-- A real C1 compact observable uses norm^(3/2), rather than assuming
-- every legitimate source inverseweight test is compact smooth.
theorem actual_nonconstant_source {η : ℝ} (hη : 0<η) (hη1 : η≤1) :
    let φ : ContDiffBump (0:ℝ) := {rIn:=1,rOut:=2,rIn_pos:=by norm_num,rIn_lt_rOut:=by norm_num}
    let ψ : ℝ → ℝ := fun x => φ.normed (volume : Measure ℝ) x * ‖x‖^(3/2:ℝ)
    ContDiff ℝ 1 ψ ∧ HasCompactSupport ψ ∧
    let μ := (volume : Measure ℝ).tilted (fun x => -potential x)
    let J := Measure.map (fun p : ℝ × ℝ => (p.1,p.1+Real.sqrt η • p.2)) (μ.prod (stdGaussian ℝ))
    let W := fun y u : ℝ => potential ((1/2:ℝ) • (y+u)) + ‖u-y‖^2/(8*η)
    ∃ R S : Kernel ℝ ℝ, IsMarkovKernel R ∧ IsMarkovKernel S ∧
      (J.map Prod.swap).IsCondKernel R ∧
      (∀ y, S y = (R y).map (fun x => (2:ℝ) • x-y)) ∧
      ∀ y, S y = (volume : Measure ℝ).tilted (fun u => -W y u) ∧
        ContDiff ℝ 2 (W y) ∧ Integrable (fun u => Real.exp (-W y u)) ∧
        0 < (∫ u, Real.exp (-W y u)) ∧
        ∃ D : Lp ℝ 2 (S y) →ₗ.[ℝ] Lp ℝ 2 (S y),
          Dense (D.domain : Set (Lp ℝ 2 (S y))) ∧ D.IsClosable ∧ D.closure.IsClosed ∧
          (∀ (u : Lp ℝ 2 (S y)) (v : Lp ℝ 2 (S y)), (u,v) ∈ D.graph ↔
            ∃ f : ℝ → ℝ, ContDiff ℝ ∞ f ∧ HasCompactSupport f ∧
              u =ᵐ[S y] f ∧ v =ᵐ[S y] gradient f) ∧
      ∀ (ε : ℝ), 0 < ε → ∀ f : Lp ℝ 2 (S y),
      ∃ u : D.closure.domain,
        (∀ v : D.closure.domain,
          ε * ⟪(u : Lp ℝ 2 (S y)), (v : Lp ℝ 2 (S y))⟫ +
            ⟪D.closure u, D.closure v⟫ = ⟪f, (v : Lp ℝ 2 (S y))⟫) ∧
        LocallyIntegrable (fun x => (u : Lp ℝ 2 (S y)) x) ∧
        LocallyIntegrable (fun x => D.closure u x) ∧
        (∀ ψ : ℝ → ℝ, ContDiff ℝ 1 ψ → HasCompactSupport ψ → ∀ v : ℝ,
          Integrable (fun x => ψ x * inner ℝ (D.closure u x) v) ∧
          Integrable (fun x => (u : Lp ℝ 2 (S y)) x * fderiv ℝ ψ x v) ∧
          (∫ x, ψ x * inner ℝ (D.closure u x) v) =
            - ∫ x, (u : Lp ℝ 2 (S y)) x * fderiv ℝ ψ x v) ∧
        ∀ ψ : ℝ → ℝ, ContDiff ℝ 1 ψ → HasCompactSupport ψ →
          Integrable (fun x => Real.exp (-W y x) * ((u : Lp ℝ 2 (S y)) x * ψ x)) ∧
          Integrable (fun x => Real.exp (-W y x) * inner ℝ (D.closure u x) (gradient ψ x)) ∧
          Integrable (fun x => Real.exp (-W y x) * (f x * ψ x)) ∧
          ε * (∫ x, Real.exp (-W y x) * ((u : Lp ℝ 2 (S y)) x * ψ x)) +
            (∫ x, Real.exp (-W y x) * inner ℝ (D.closure u x) (gradient ψ x)) =
            ∫ x, Real.exp (-W y x) * (f x * ψ x) := by
  let φ : ContDiffBump (0:ℝ) := {rIn:=1,rOut:=2,rIn_pos:=by norm_num,rIn_lt_rOut:=by norm_num}
  let ψ : ℝ → ℝ := fun x => φ.normed (volume : Measure ℝ) x * ‖x‖^(3/2:ℝ)
  have hψ : ContDiff ℝ 1 ψ :=
    (contDiff_infty.mp φ.contDiff_normed 1).mul (contDiff_norm_rpow (by norm_num : (1:ℝ)<3/2))
  have hc : HasCompactSupport ψ := φ.hasCompactSupport_normed.mul_right
  refine ⟨hψ,hc,?_⟩
  have hf : ContDiff ℝ 2 potential := by unfold potential;fun_prop
  have hh : ∀ x v : ℝ, ((1/2:ℝ≥0):ℝ)*‖v‖^2 ≤ fderiv ℝ (fderiv ℝ potential) x v v ∧
      fderiv ℝ (fderiv ℝ potential) x v v ≤ ((1:ℝ≥0):ℝ)*‖v‖^2 := by
    intro x v
    simpa using potential_curvature x v
  exact AutoSamplingTheory.ExampleCases.ProximalBPS.ConditionalC1Resolvent.conditional_c1_resolvent
    (by norm_num : (0:ℝ≥0)<1/2) (by norm_num : (1/2:ℝ≥0)≤1) hf hh hη (by simpa using hη1)

#print axioms AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.CompactC1GradientDomain.compact_c1_in_closed_gradient
#print axioms AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.WeightedResolventC1.weak_resolvent_c1
#print axioms AutoSamplingTheory.ExampleCases.ProximalBPS.ConditionalC1Resolvent.conditional_c1_resolvent
#print axioms actual_nonconstant_source
end Tests.CompactC1GradientDomain
