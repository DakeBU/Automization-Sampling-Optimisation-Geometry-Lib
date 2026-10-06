import AutoSamplingTheory.ExampleCases.ProximalBPS.ConditionalCenteredResolventLimit
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Deriv
import Mathlib.Analysis.InnerProductSpace.PiL2
set_option autoImplicit false
noncomputable section
open MeasureTheory Filter InnerProductSpace
open scoped Topology RealInnerProductSpace ContDiff
open ProbabilityTheory
open scoped NNReal
namespace Tests.ScaledResolventLimit

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





theorem actual_nonquadratic_centered_resolvent :
    let η : ℝ := 1/2
    let μ := (volume : Measure ℝ).tilted (fun x => -potential x)
    let J := Measure.map (fun p : ℝ × ℝ => (p.1,p.1+Real.sqrt η • p.2)) (μ.prod (stdGaussian ℝ))
    let W := fun y u : ℝ => potential ((1/2:ℝ) • (y+u))+‖u-y‖^2/(8*η)
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
          ∀ f : Lp ℝ 2 (S y), (∫ x, f x ∂S y)=0 →
          ∀ (ε : ℕ → ℝ), (∀ n, 0 < ε n) → Tendsto ε atTop (𝓝 0) →
          ∃ u : ℕ → D.closure.domain,
            (∀ n, ∀ v : D.closure.domain,
              ε n*inner ℝ (u n : Lp ℝ 2 (S y)) (v : Lp ℝ 2 (S y))+
                inner ℝ (D.closure (u n)) (D.closure v)=inner ℝ f (v : Lp ℝ 2 (S y))) ∧
            Tendsto (fun n => ε n • (u n : Lp ℝ 2 (S y))) atTop (𝓝 0) := by
  have hV : ContDiff ℝ 2 potential := by unfold potential; fun_prop
  have hh : ∀ x v : ℝ, ((1/2:ℝ≥0):ℝ)*‖v‖^2 ≤ fderiv ℝ (fderiv ℝ potential) x v v ∧
      fderiv ℝ (fderiv ℝ potential) x v v ≤ ((1:ℝ≥0):ℝ)*‖v‖^2 := by
    intro x v
    simpa using potential_curvature x v
  exact AutoSamplingTheory.ExampleCases.ProximalBPS.ConditionalCenteredResolventLimit.conditional_centered_resolvent_sequence
    (α := (1/2:NNReal)) (β := (1:NNReal)) (η := (1/2:ℝ))
    (by norm_num) (by norm_num) hV hh (by norm_num) (by norm_num)

abbrev E0 := EuclideanSpace ℝ (Fin 0)
private def W0 (_ : E0) : ℝ := 7
theorem actual_zero_dim_centered_resolvent :
    let μ := (volume : Measure E0).tilted (fun x => -W0 x)
    μ Set.univ=1 ∧
    ∃ D : Lp ℝ 2 μ →ₗ.[ℝ] Lp E0 2 μ,
      Dense (D.domain : Set (Lp ℝ 2 μ)) ∧ D.IsClosable ∧ D.closure.IsClosed ∧
      (∀ (a : Lp ℝ 2 μ) (G : Lp E0 2 μ), (a,G) ∈ D.graph ↔
        ∃ φ : E0 → ℝ, ContDiff ℝ ∞ φ ∧ HasCompactSupport φ ∧
          a =ᵐ[μ] φ ∧ G =ᵐ[μ] gradient φ) ∧
      ∀ f : Lp ℝ 2 μ, (∫ x, f x ∂μ)=0 →
      ∀ (ε : ℕ → ℝ), (∀ n, 0 < ε n) → Tendsto ε atTop (𝓝 0) →
      Integrable (fun x => f x) μ ∧
      ∃ u : ℕ → D.closure.domain,
        (∀ n, ∀ v : D.closure.domain,
          ε n*inner ℝ (u n : Lp ℝ 2 μ) (v : Lp ℝ 2 μ)+
            inner ℝ (D.closure (u n)) (D.closure v)=inner ℝ f (v : Lp ℝ 2 μ)) ∧
        Tendsto (fun n => ε n • (u n : Lp ℝ 2 μ)) atTop (𝓝 0) := by
  have hW : ContDiff ℝ 1 W0 := contDiff_const
  have hI : Integrable (fun x : E0 => Real.exp (-W0 x)) volume := by
    simpa only [W0] using (integrable_const (Real.exp (-(7:ℝ))) :
      Integrable (fun _ : E0 => Real.exp (-(7:ℝ))) volume)
  let μ := (volume : Measure E0).tilted (fun x => -W0 x)
  have : IsProbabilityMeasure μ := isProbabilityMeasure_tilted hI
  obtain ⟨D,hd,hD,hDc,hgraph⟩ :=
    AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.WeightedGradient.compact_gradient_closable W0 hW hI
  dsimp only
  refine ⟨measure_univ,D,hd,hD,hDc,hgraph,?_⟩
  intro f hf ε hε hε0
  obtain ⟨hi,u,hu,ht⟩ :=
    AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.CenteredGibbsResolventLimit.gibbs_centered_resolvent_sequence
      W0 hW hI D hD hgraph f hf ε hε hε0
  exact ⟨hi,u,fun n => (hu n).1,ht⟩

private def zeroOperator : ℝ →ₗ.[ℝ] ℝ := (0 : ℝ →ₗ[ℝ] ℝ).toPMap ⊤
theorem zeroOperator_isClosed : zeroOperator.IsClosed :=
  zeroOperator.graph.closed_of_finiteDimensional
theorem noncentered_constant_residual (ε : ℝ) (hε : 0 < ε) :
    let u : zeroOperator.domain := ⟨7/ε,Submodule.mem_top⟩
    (∀ v : zeroOperator.domain,
      ε*inner ℝ (u : ℝ) (v : ℝ)+inner ℝ (zeroOperator u) (zeroOperator v)=
        inner ℝ (7:ℝ) (v : ℝ)) ∧ ε • (u : ℝ)=7 := by
  dsimp only
  constructor
  · intro v
    simp [zeroOperator]
    field_simp
  · change ε*(7/ε)=7
    field_simp

theorem noncentered_residual_does_not_tendsto_zero :
    ¬Tendsto (fun _ : ℕ => (7:ℝ)) atTop (𝓝 0) := by
  intro ht
  have h := tendsto_nhds_unique (tendsto_const_nhds (x:=(7:ℝ))) ht
  norm_num at h

#print axioms actual_nonquadratic_centered_resolvent
#print axioms actual_zero_dim_centered_resolvent
#print axioms noncentered_constant_residual
#print axioms zeroOperator_isClosed
#print axioms noncentered_residual_does_not_tendsto_zero
#print axioms AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.ScaledClosedGraphResolvent.scaled_resolvent_sequence_tendsto_zero
#print axioms AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.CenteredGibbsResolventLimit.gibbs_centered_resolvent_sequence
#print axioms AutoSamplingTheory.ExampleCases.ProximalBPS.ConditionalCenteredResolventLimit.conditional_centered_resolvent_sequence
end Tests.ScaledResolventLimit
