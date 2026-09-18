import AutoSamplingTheory.ExampleCases.SmoothedPicardHMC.ApproximateProximalExecution

open AutoSamplingTheory.ExampleCases.SmoothedPicardHMC.ApproximateProximalExecution
open InnerProductSpace MeasureTheory
open scoped NNReal

#check approximate_proximal_execution
#print axioms approximate_proximal_execution

example : proximalQuery (fun x : ℝ => x) (3/4) (1/10) 0 0 0 = none := rfl

-- Final check counts, even with zero residual and eta>1/2.
example : proximalQuery (fun x : ℝ => x) (3/4) (1/10) 0 1 0 = some (0,1) := by
  norm_num [proximalQuery]

-- Return x_2=3, not x_3=5/2; three actual gradient tests.
example : proximalQuery (fun x : ℝ => x) (1/2) 1 4 3 4 = some (3,3) := by
  norm_num [proximalQuery, Real.norm_eq_abs]

example : proximalQuery (fun x : ℝ => x) (1/2) 1 4 2 4 = none := by
  norm_num [proximalQuery, Real.norm_eq_abs]

example {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [CompleteSpace E] [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]
    {V : E → ℝ} {κ : ℝ≥0} (hκ : 1 ≤ κ) (hV : ContDiff ℝ 2 V)
    (hH : ∀ x v : E, (κ : ℝ)⁻¹*‖v‖^2 ≤ (fderiv ℝ (fderiv ℝ V) x v) v ∧
      (fderiv ℝ (fderiv ℝ V) x v) v ≤ ‖v‖^2) :
    ∃ p : E → E, ∃ N : E → ℕ, Measurable p ∧ Measurable N ∧
      ∀ y, ∃ out : E, proximalQuery (gradient V) (3/4) (1/10) y (N y+1) y =
        some (out,N y+1) ∧ ‖out-p y‖ ≤ 1/10 ∧
        (∀ z, V z+(3/4 : ℝ)⁻¹/2*‖z-y‖^2 ≤
          V (p y)+(3/4 : ℝ)⁻¹/2*‖p y-y‖^2 ↔ z=p y) := by
  obtain ⟨p,N,hp,hN,_,hall⟩ := approximate_proximal_execution hκ hV hH
    (eta := 3/4) (c := 7/8) (eps := 1/10) (by norm_num) (by norm_num)
    (by norm_num) (by norm_num)
  refine ⟨p,N,hp,hN,fun y => ?_⟩
  obtain ⟨_,hmin,_,_,herror,_,hrun⟩ := hall y
  exact ⟨_,hrun,herror,fun z => (hmin z).2⟩
