theorem integral_condExpL2_eq (hm : m ≤ m0) (f : Lp E' 2 μ) (hs : MeasurableSet[m] s)
    (hμs : μ s ≠ ∞) : ∫ x in s, (condExpL2 E' 𝕜 hm f : α → E') x ∂μ = ∫ x in s, f x ∂μ := by
  rw [← sub_eq_zero, ←
    integral_sub' (integrableOn_Lp_of_measure_ne_top _ fact_one_le_two_ennreal.elim hμs)
      (integrableOn_Lp_of_measure_ne_top _ fact_one_le_two_ennreal.elim hμs)]
  refine integral_eq_zero_of_forall_integral_inner_eq_zero 𝕜 _ ?_ ?_
  · rw [integrable_congr (ae_restrict_of_ae (Lp.coeFn_sub (↑(condExpL2 E' 𝕜 hm f)) f).symm)]
