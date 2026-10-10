import AutoSamplingTheory.ExampleCases.ProximalBPS.RealDefectRootUnique

open MeasureTheory ProbabilityTheory
open scoped ContDiff NNReal ENNReal Topology
set_option autoImplicit false
set_option maxHeartbeats 1000000

/- Actual original-binder consumer: the produced positive real defect root
   is unique; every positive alternative with the same square has the same full scalar energy and is a contraction. This supplies no full-space
   inverse, strict centered bound, joint GammaP or paper-completion certificate. -/
example
    {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]
    {V : E → ℝ} {α β : ℝ≥0} {η : ℝ}
    (hα : 0 < (α : ℝ)) (hαβ : α ≤ β) (hV : ContDiff ℝ 2 V)
    (hH : ∀ x v : E,
      (α : ℝ)*‖v‖^2 ≤ (fderiv ℝ (fderiv ℝ V) x v) v ∧
      (fderiv ℝ (fderiv ℝ V) x v) v ≤ (β : ℝ)*‖v‖^2)
    (hη : 0 < η) (hβη : (β : ℝ)*η ≤ 1) :
    let μ := (volume : Measure E).tilted (fun x => -V x)
    let J := (μ.prod (stdGaussian E)).map
      (fun p : E × E => (p.1,p.1+Real.sqrt η • p.2))
    let ν := J.snd
    ∃ T : Lp ℝ 2 ν →L[ℝ] Lp ℝ 2 ν,
      ∃ Γ : Lp ℝ 2 ν →L[ℝ] Lp ℝ 2 ν,
        Γ.IsPositive ∧ Γ*Γ = ((1 : Lp ℝ 2 ν →L[ℝ] Lp ℝ 2 ν)-T*T) ∧
        ∀ Γ' : Lp ℝ 2 ν →L[ℝ] Lp ℝ 2 ν,
          Γ'.IsPositive → Γ'*Γ' = ((1 : Lp ℝ 2 ν →L[ℝ] Lp ℝ 2 ν)-T*T) →
          Γ'=Γ ∧ ∀ u : Lp ℝ 2 ν, ‖Γ' u‖ ≤ ‖u‖ ∧ ‖Γ' u‖^2 = ‖u‖^2-‖T u‖^2 := by
  dsimp only
  obtain ⟨hμ,hJ,hν,S,hS,hSd,hSc,hSf,hSs,T,hTs,hAll,hD,Γ,hΓ,hΓSq,hEnergy,hUnique⟩ :=
    AutoSamplingTheory.ExampleCases.ProximalBPS.RealDefectRootUnique.actual_unique_positive_real_defect_root
      hα hαβ hV hH hη hβη
  refine ⟨T,Γ,hΓ,hΓSq,?_⟩
  intro Γ' hΓ' hΓ'Sq
  have heq := hUnique Γ' hΓ' hΓ'Sq
  refine ⟨heq,?_⟩
  rw [heq]
  intro u
  refine ⟨?_,hEnergy u⟩
  have he := hEnergy u
  nlinarith [norm_nonneg (Γ u),norm_nonneg u,sq_nonneg ‖T u‖]

#check AutoSamplingTheory.TechnicalLemmas.Measure.L2RealSquareRootUnique.positive_square_roots_unique
#check AutoSamplingTheory.ExampleCases.ProximalBPS.RealDefectRootUnique.actual_unique_positive_real_defect_root
