          simpa only [add_sub_cancel_left] using J1
        _ = 4 * (1 / 2) ^ e * (1 / 2) ^ (m + 2) := by ring
        _ ≤ 4 * (1 / 2) ^ e * ‖y‖ := by gcongr
    -- use the previous estimates to see that `f (x + y) - f x - f' y` is small.
    calc
      ‖f (x + y) - f x - f' y‖ = ‖f (x + y) - f x - L e (n e) m y + (L e (n e) m - f') y‖ :=
        congr_arg _ (by simp)
      _ ≤ 4 * (1 / 2) ^ e * ‖y‖ + 12 * ‖c‖ * (1 / 2) ^ e * ‖y‖ :=
        norm_add_le_of_le J2 <| (le_opNorm _ _).trans <| by gcongr; exact Lf' _ _ m_ge
      _ = (4 + 12 * ‖c‖) * ‖y‖ * (1 / 2) ^ e := by ring
      _ ≤ (4 + 12 * ‖c‖) * ‖y‖ * (ε / (4 + 12 * ‖c‖)) := by gcongr
      _ = ε * ‖y‖ := by field
  rw [← this.fderiv] at f'K
  exact ⟨this.differentiableAt, f'K⟩

theorem differentiable_set_eq_D (hK : IsComplete K) :
    { x | DifferentiableAt 𝕜 f x ∧ fderiv 𝕜 f x ∈ K } = D f K :=
  Subset.antisymm (differentiable_set_subset_D _) (D_subset_differentiable_set hK)

end FDerivMeasurableAux

open FDerivMeasurableAux

variable [MeasurableSpace E] [OpensMeasurableSpace E]
variable (𝕜 f)

/-- The set of differentiability points of a function, with derivative in a given complete set,
is Borel-measurable. -/
theorem measurableSet_of_differentiableAt_of_isComplete {K : Set (E →L[𝕜] F)} (hK : IsComplete K) :
    MeasurableSet { x | DifferentiableAt 𝕜 f x ∧ fderiv 𝕜 f x ∈ K } := by
  simp only [D, differentiable_set_eq_D K hK]
  aesop
    (add safe apply [MeasurableSet.iUnion, MeasurableSet.iInter, isOpen_B])
    (add unsafe IsOpen.measurableSet)

variable [CompleteSpace F]

/-- The set of differentiability points of a function taking values in a complete space is
Borel-measurable. -/
theorem measurableSet_of_differentiableAt : MeasurableSet { x | DifferentiableAt 𝕜 f x } := by
  have : IsComplete (univ : Set (E →L[𝕜] F)) := isComplete_univ
  convert! measurableSet_of_differentiableAt_of_isComplete 𝕜 f this
  simp

@[fun_prop]
theorem measurable_fderiv : Measurable (fderiv 𝕜 f) := by
