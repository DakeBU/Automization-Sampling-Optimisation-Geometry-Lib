import AutoSamplingTheory.ExampleCases.ProximalBPS.ConditionalScoreVariance
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Deriv
import Mathlib.Analysis.InnerProductSpace.PiL2
set_option autoImplicit false
noncomputable section
open MeasureTheory Filter InnerProductSpace ProbabilityTheory
open scoped Topology RealInnerProductSpace ContDiff NNReal
namespace Tests.CenteredPoincare
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





theorem actual_nonquadratic_poincare_and_score_variance :
    let μ := (volume : Measure ℝ).tilted (fun x => -potential x)
    let J := Measure.map (fun p : ℝ × ℝ => (p.1,p.1+Real.sqrt (1/2:ℝ) • p.2))
      (μ.prod (stdGaussian ℝ))
    let W := fun y u : ℝ => potential ((1/2:ℝ) • (y+u))+‖u-y‖^2/(8*(1/2:ℝ))
    let s := fun y u : ℝ => -(1/2:ℝ) • fderiv ℝ potential ((1/2:ℝ) • (y+u)) -
      (1/(4*(1/2:ℝ))) • innerSL ℝ (y-u)
    ∃ R S : Kernel ℝ ℝ, IsMarkovKernel R ∧ IsMarkovKernel S ∧
      (J.map Prod.swap).IsCondKernel R ∧
      (∀ y, S y=(R y).map (fun x => (2:ℝ) • x-y)) ∧
      ∀ y, S y=(volume : Measure ℝ).tilted (fun u => -W y u) ∧
        ContDiff ℝ 2 (W y) ∧ Integrable (fun u => Real.exp (-W y u)) ∧
        0 < ∫ u, Real.exp (-W y u) ∧
        ∃ D : Lp ℝ 2 (S y) →ₗ.[ℝ] Lp ℝ 2 (S y),
          Dense (D.domain : Set (Lp ℝ 2 (S y))) ∧ D.IsClosable ∧ D.closure.IsClosed ∧
          (∀ (a : Lp ℝ 2 (S y)) (G : Lp ℝ 2 (S y)), (a,G) ∈ D.graph ↔
            ∃ φ : ℝ → ℝ, ContDiff ℝ ∞ φ ∧ HasCompactSupport φ ∧
              a =ᵐ[S y] φ ∧ G =ᵐ[S y] gradient φ) ∧
          (∀ z : D.closure.domain, (∫ x, (z : Lp ℝ 2 (S y)) x ∂S y)=0 →
            (5/8:ℝ)*‖(z : Lp ℝ 2 (S y))‖^2 ≤ ‖D.closure z‖^2) ∧
          ∀ a : ℝ,
            AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.Poincare.Admissible
              (S y) (fun u => s y u a) ∧
            AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.Poincare.variance
              (S y) (fun u => s y u a) ≤
                (9/40:ℝ)*‖a‖^2 := by
  have hV : ContDiff ℝ 2 potential := by unfold potential; fun_prop
  have hh : ∀ x a : ℝ, ((1/2:NNReal):ℝ)*‖a‖^2 ≤ fderiv ℝ (fderiv ℝ potential) x a a ∧
      fderiv ℝ (fderiv ℝ potential) x a a ≤ ((1:NNReal):ℝ)*‖a‖^2 := by
    intro x a
    simpa using potential_curvature x a
  have h := AutoSamplingTheory.ExampleCases.ProximalBPS.ConditionalScoreVariance.conditional_centered_domain_and_score_variance
    (α := (1/2:NNReal)) (β := (1:NNReal)) (η := (1/2:ℝ))
    (by norm_num) (by norm_num) hV hh (by norm_num) (by norm_num)
  norm_num at h ⊢
  exact h

abbrev E0 := EuclideanSpace ℝ (Fin 0)
private def W0 (_ : E0) : ℝ := 7
theorem actual_zero_dim_poincare_and_noncentered_failure :
    let μ := (volume : Measure E0).tilted (fun x => -W0 x)
    μ Set.univ=1 ∧
    ∃ D : Lp ℝ 2 μ →ₗ.[ℝ] Lp E0 2 μ,
      Dense (D.domain : Set (Lp ℝ 2 μ)) ∧ D.IsClosable ∧ D.closure.IsClosed ∧
      (∀ (a : Lp ℝ 2 μ) (G : Lp E0 2 μ), (a,G) ∈ D.graph ↔
        ∃ φ : E0 → ℝ, ContDiff ℝ ∞ φ ∧ HasCompactSupport φ ∧
          a =ᵐ[μ] φ ∧ G =ᵐ[μ] gradient φ) ∧
      (∀ z : D.closure.domain, (∫ x, (z:Lp ℝ 2 μ) x ∂μ)=0 →
        (2:ℝ)*‖(z:Lp ℝ 2 μ)‖^2 ≤ ‖D.closure z‖^2) ∧
      ∃ u : D.closure.domain, (u:Lp ℝ 2 μ) =ᵐ[μ] (fun _ => (7:ℝ)) ∧
        D.closure u=0 ∧ ¬(2:ℝ)*‖(u:Lp ℝ 2 μ)‖^2 ≤ ‖D.closure u‖^2 := by
  have hW : ContDiff ℝ 2 W0 := contDiff_const
  have hI : Integrable (fun x : E0 => Real.exp (-W0 x)) volume := by
    simpa only [W0] using (integrable_const (Real.exp (-(7:ℝ))) :
      Integrable (fun _ : E0 => Real.exp (-(7:ℝ))) volume)
  have hZ : 0 < ∫ x, Real.exp (-W0 x) := integral_exp_pos hI
  have hl : ∀ x a : E0, (2:ℝ)*‖a‖^2 ≤ fderiv ℝ (fderiv ℝ W0) x a a := by
    intro x a
    simp [Subsingleton.elim a 0]
  have hu : ∀ x a : E0, fderiv ℝ (fderiv ℝ W0) x a a ≤ (3:ℝ)*‖a‖^2 := by
    intro x a
    simp [Subsingleton.elim a 0]
  let μ := (volume : Measure E0).tilted (fun x => -W0 x)
  let : IsProbabilityMeasure μ := isProbabilityMeasure_tilted hI
  obtain ⟨D,hd,hD,hDc,hgraph⟩ :=
    AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.WeightedGradient.compact_gradient_closable
      W0 (hW.of_le (by norm_num)) hI
  obtain ⟨u,ha,hDu⟩ :=
    AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.WeightedC1GradientDomain.constants_in_closed_gradient
      μ D hD hgraph 7
  have hn : ‖(u:Lp ℝ 2 μ)‖^2=49 := by
    rw [← real_inner_self_eq_norm_sq,L2.inner_def]
    calc
      _ = ∫ x, inner ℝ (7:ℝ) (7:ℝ) ∂μ := by
        apply integral_congr_ae
        filter_upwards [ha] with x hx
        rw [hx]
      _ = 49 := by norm_num [integral_const,measureReal_def]
  dsimp only
  refine ⟨measure_univ,D,hd,hD,hDc,hgraph,?_,u,ha,hDu,?_⟩
  · exact AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.CenteredDomainPoincare.gibbs_centered_domain_poincare
      W0 hW hI hZ 2 3 (by norm_num) (by norm_num) hl hu D hD hgraph
  · rw [hn,hDu]
    norm_num

#print axioms AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.CenteredDomainPoincare.gibbs_centered_domain_poincare

#print axioms AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.GibbsC1Poincare.gibbs_c1_variance_poincare

#print axioms AutoSamplingTheory.ExampleCases.ProximalBPS.ConditionalScoreVariance.conditional_centered_domain_and_score_variance

#print axioms actual_nonquadratic_poincare_and_score_variance

#print axioms actual_zero_dim_poincare_and_noncentered_failure

end Tests.CenteredPoincare
