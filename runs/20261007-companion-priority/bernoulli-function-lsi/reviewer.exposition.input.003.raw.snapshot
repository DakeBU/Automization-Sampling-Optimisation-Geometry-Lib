import AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.BernoulliLogSobolev

noncomputable section
set_option backward.isDefEq.respectTransparency false
open MeasureTheory Real
open scoped ENNReal BigOperators
open AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities
namespace Tests.BernoulliLogSobolev

private def law (n : ℕ) : Measure (Fin n → Bool) :=
  (Fintype.card (Fin n → Bool) : ℝ≥0∞)⁻¹ • Measure.count

private theorem integral_one (f : (Fin 1 → Bool) → ℝ) :
    (∫ x, f x ∂law 1) = (f (fun _ => true) + f (fun _ => false))/2 := by
  unfold law
  rw [integral_smul_measure, integral_fintype (Integrable.of_finite)]
  simp only [Fintype.card_fun, Fintype.card_fin, Fintype.card_bool,
    pow_one, count_real_singleton, one_mul, smul_eq_mul]
  have he : (∑ x : Fin 1 → Bool, f x) =
      f (fun _ => true) + f (fun _ => false) := by
    calc
      _ = ∑ b : Bool, f ((Equiv.funUnique (Fin 1) Bool).symm b) :=
        (Fintype.sum_equiv (Equiv.funUnique (Fin 1) Bool).symm
          (fun b => f ((Equiv.funUnique (Fin 1) Bool).symm b)) f (fun _ => rfl)).symm
      _ = _ := by
        simp only [Fintype.sum_bool]
        change f (uniqueElim true) + f (uniqueElim false) = _
        have ht : (uniqueElim true : Fin 1 → Bool) = (fun _ => true) := by
          funext i
          exact uniqueElim_const true i
        have hf : (uniqueElim false : Fin 1 → Bool) = (fun _ => false) := by
          funext i
          exact uniqueElim_const false i
        rw [ht, hf]
  rw [he]
  norm_num
  ring

/-- A nonconstant actual two-point law gives log(2) ≤ 1 via the LSI producer. -/
theorem indicator_entropy : Real.log 2 ≤ 1 := by
  let h : (Fin 1 → Bool) → ℝ := fun x => if x 0 then 1 else 0
  have hp := BernoulliLogSobolev.bernoulli_function_logSobolev 1 h
  change IsProbabilityMeasure (law 1) ∧ _ at hp
  have hi := hp.2.2.2.2
  change (∫ x, h x^2 * log (h x^2) ∂law 1) -
    (∫ x, h x^2 ∂law 1) * log (∫ x, h x^2 ∂law 1) ≤
    (1/2 : ℝ) * ∫ x, ∑ j : Fin 1, (h x - h (Function.update x j (!x j)))^2 ∂law 1 at hi
  rw [integral_one, integral_one, integral_one] at hi
  norm_num [h, Fin.sum_univ_one, Function.update] at hi
  have hlog : log (1/2 : ℝ) = -log 2 := by
    rw [log_div (by norm_num : (1 : ℝ) ≠ 0) (by norm_num : (2 : ℝ) ≠ 0)]
    simp
  rw [hlog] at hi
  linarith

/-- Zero-dimensional actual law has no flip energy, including a negative constant. -/
theorem zero_dimension :
    (∫ x : Fin 0 → Bool, (-(3:ℝ))^2 * log ((-(3:ℝ))^2) ∂law 0) -
      (∫ _x : Fin 0 → Bool, (-(3:ℝ))^2 ∂law 0) *
        log (∫ _x : Fin 0 → Bool, (-(3:ℝ))^2 ∂law 0) ≤ 0 := by
  have hp := BernoulliLogSobolev.bernoulli_function_logSobolev 0 (fun _ => -(3:ℝ))
  have hi := hp.2.2.2.2
  simpa only [law, Finset.univ_eq_empty, Finset.sum_empty, integral_zero, mul_zero] using hi

/-- Signed and zero-valued inputs exercise the genuine upper-bound direction. -/
theorem signed_two_point :
    ((-2 : ℝ)^2 * log ((-2 : ℝ)^2) + (0 : ℝ)^2 * log ((0 : ℝ)^2))/2 -
      (((-2 : ℝ)^2 + (0 : ℝ)^2)/2) * log (((-2 : ℝ)^2+(0 : ℝ)^2)/2) ≤
        ((-2 : ℝ)-(0 : ℝ))^2/2 :=
  TwoPointEntropy.two_point_squared_entropy_le_half_sq_sub (-2) 0

private def normalizedTwo (x : Fin 2 → Bool) : ℝ :=
  ((if x 0 then 1 else -1) + (if x 1 then 1 else -1))/sqrt 2

/-- Genuine normalized Rademacher sum: its full-flip energy is exactly four. -/
theorem normalized_two_coordinate_entropy :
    (∫ x, normalizedTwo x^2 * log (normalizedTwo x^2) ∂law 2) -
      (∫ x, normalizedTwo x^2 ∂law 2) * log (∫ x, normalizedTwo x^2 ∂law 2) ≤ 2 := by
  have hp := BernoulliLogSobolev.bernoulli_function_logSobolev 2 normalizedTwo
  have hprob : IsProbabilityMeasure (law 2) := hp.1
  letI := hprob
  have hD : (fun x => ∑ j : Fin 2,
      (normalizedTwo x-normalizedTwo (Function.update x j (!x j)))^2) =
      (fun _ : Fin 2 → Bool => (4 : ℝ)) := by
    funext x
    have hs : sqrt (2 : ℝ) ≠ 0 := sqrt_ne_zero'.mpr (by norm_num)
    have hs2 : sqrt (2 : ℝ)^2 = 2 := sq_sqrt (by norm_num)
    cases h0 : x 0 <;> cases h1 : x 1 <;>
      norm_num [normalizedTwo, Fin.sum_univ_two, Function.update, h0, h1] <;>
      field_simp <;> nlinarith
  have hi := hp.2.2.2.2
  rw [hD] at hi
  change (∫ x, normalizedTwo x^2 * log (normalizedTwo x^2) ∂law 2) -
    (∫ x, normalizedTwo x^2 ∂law 2) * log (∫ x, normalizedTwo x^2 ∂law 2) ≤
      (1/2 : ℝ) * ∫ _x : Fin 2 → Bool, (4 : ℝ) ∂law 2 at hi
  have he : (∫ _x : Fin 2 → Bool, (4 : ℝ) ∂law 2) = 4 := by simp
  rw [he] at hi
  rw [show (1/2 : ℝ)*4 = 2 by norm_num] at hi
  exact hi

end Tests.BernoulliLogSobolev

#print axioms AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.TwoPointEntropy.two_point_squared_entropy_le_half_sq_sub
#print axioms AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.BernoulliLogSobolev.bernoulli_function_logSobolev
#print axioms Tests.BernoulliLogSobolev.indicator_entropy
#print axioms Tests.BernoulliLogSobolev.zero_dimension
#print axioms Tests.BernoulliLogSobolev.signed_two_point
#print axioms Tests.BernoulliLogSobolev.normalized_two_coordinate_entropy
