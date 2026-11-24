import GC44Uniform

/-! Fact C.6 throughout the range `2*q+1 < d`. A grid projection reproduces
the products of cosine features when there are sufficiently many grid points.
For the remaining dimensions the identity kernel already has the required row bounds. -/
noncomputable section
open MeasureTheory ProbabilityTheory Matrix
open scoped BigOperators Matrix.Norms.L2Operator
open AutoSamplingTheory.ExampleCases.GaussianComplexity.CosineProjection
open AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumTargetEvent
namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumKrylov

private theorem exists_reproducing_kernel {d q : ℕ} (hq : 2*q+1 < d) :
    ∃ P : Matrix (Fin d) (Fin d) ℝ,
      (∀ i, (∀ j, |P i j| ≤ 2*(2*(q:ℝ)+1)/(d:ℝ)) ∧
        ∑ j,(P i j)^2 ≤ 2*(2*(q:ℝ)+1)/(d:ℝ)) ∧
      ∀ H : Fin d → Small q, energyLift (fun i => ∑ j, P i j • H j) = energyLift H := by
  by_cases hf : 2*(2*q)+1 < d
  · refine ⟨projection d (2*q), fun i => ?_, lift_symbol hf⟩
    simpa only [Nat.cast_mul, Nat.cast_ofNat] using projection_bounds hf i
  · have hd : 0 < (d : ℝ) := by exact_mod_cast (show 0 < d by omega)
    have hbound : 1 ≤ 2*(2*(q:ℝ)+1)/(d:ℝ) := by
      rw [le_div_iff₀ hd,one_mul]
      exact_mod_cast (show d ≤ 2*(2*q+1) by omega)
    refine ⟨1,fun i => ⟨fun j => ?_,?_⟩,fun H => ?_⟩
    · by_cases h : i = j
      · simpa [Matrix.one_apply,h] using hbound
      · simpa [Matrix.one_apply,h] using (zero_le_one.trans hbound)
    · simpa [Matrix.one_apply] using hbound
    · simp [Matrix.one_apply]

private theorem gram_from_weights {d q : ℕ} (hq : 2*q+1 < d) (g : Starts d q)
    (P : Matrix (Fin d) (Fin d) ℝ)
    (hr : ∀ H : Fin d → Small q, energyLift (fun i => ∑ j, P i j • H j) = energyLift H)
    {τ : ℝ} (ht : 0 ≤ τ)
    (hb : ∀ (b : Bool) (i : Fin d), ‖weightedRowMatrix g
       (fun j => if b then P i j * frequencyWeight d q j else P i j)‖ ≤ τ) : g ∈ gramGood d q τ := by
  let B := feature d q g
  let W := cosineDiag d q
  have h1 : energyLift (fun j => rowGram g j - 1) = B.transpose * B - 1 := by
    have h := lift_rowGram g (fun _ => (1 : ℝ))
    simp only [one_smul,Matrix.diagonal_one,Matrix.mul_one] at h
    rw [lift_sub,h,lift_one hq]
  have h2 : energyLift (fun j => frequencyWeight d q j • (rowGram g j - 1)) =
      B.transpose * W * B := by
    simp only [smul_sub]
    rw [lift_sub,lift_rowGram,lift_frequency_identity hq,sub_zero]
    rfl
  have hs (w : Fin d → ℝ) : (B.transpose * Matrix.diagonal w * B).IsHermitian := by
    rw [Matrix.isHermitian_iff_isSymm]
    unfold Matrix.IsSymm
    simp [Matrix.transpose_mul,Matrix.mul_assoc]
  have hs1 : (B.transpose * B - 1).IsHermitian := by
    have h := hs (fun _ => 1)
    simp only [Matrix.diagonal_one,Matrix.mul_one] at h
    exact h.sub Matrix.isHermitian_one
  constructor
  · rw [← h1, ← hr]
    apply norm_lift_le hq _ ht
    · rw [hr,h1]
      exact hs1
    · exact hb false
  · rw [← h2, ← hr]
    apply norm_lift_le hq _ ht
    · rw [hr,h2]
      exact hs _
    · intro i
      simpa [weightedRowMatrix, rowGram, smul_smul] using hb true i

/-- At the source threshold the centered Gram and signed Gram bounds hold jointly
with probability at least 0.995 for every source dimension and query count. -/
theorem simultaneous_gram_concentration_full {d q : ℕ} (hq : 2*q+1 < d) :
    (199/200 : ℝ) ≤ (gaussianStarts d q).real (gramGood d q (queryThreshold 2048 d q)) := by
  obtain ⟨P, hP, hr⟩ := exists_reproducing_kernel hq
  let w (b : Bool) (i j : Fin d) := if b then P i j * frequencyWeight d q j else P i j
  have hw (b : Bool) (i : Fin d) : (∀ j, |w b i j| ≤ 2*(2*(q:ℝ)+1)/(d:ℝ)) ∧
      ∑ j,(w b i j)^2 ≤ 2*(2*(q:ℝ)+1)/(d:ℝ) := by
    cases b
    · exact hP i
    · refine ⟨fun j => ?_, le_trans (Finset.sum_le_sum (fun j _ => ?_)) (hP i).2⟩
      · change |P i j * frequencyWeight d q j| ≤ _
        rw [abs_mul]
        exact (mul_le_of_le_one_right (abs_nonneg _) (Real.abs_cos_le_one _)).trans ((hP i).1 j)
      · change (P i j * frequencyWeight d q j)^2 ≤ (P i j)^2
        rw [mul_pow]
        exact mul_le_of_le_one_right (sq_nonneg _) (Real.cos_sq_le_one _)
  apply (simultaneous_weighted_row_bounds hq w hw).trans
  refine measureReal_mono (fun g hg => ?_) (measure_ne_top _ _)
  have hl := Real.log_nonneg (show 1 ≤ (d:ℝ) by exact_mod_cast (show 1 ≤ d by omega))
  exact gram_from_weights hq g P hr (by unfold queryThreshold; positivity) hg

/-- Fact C.6 on any probability space carrying the independent standard Gaussian starts. -/
theorem gram_concentration_independent_starts {d q : ℕ} (hq : 2*q+1 < d)
    {Ω : Type*} [MeasurableSpace Ω] (μ : Measure Ω)
    (g : Fin (q+1) → Ω → Space d)
    (hg : ∀ a, MeasurePreserving (g a) μ (stdGaussian (Space d))) (hi : iIndepFun g μ) :
    (199/200 : ℝ) ≤ μ.real {ω | (fun a => g a ω) ∈ gramGood d q (queryThreshold 2048 d q)} := by
  let f (ω : Ω) : Starts d q := fun a => g a ω
  have hf : MeasurePreserving f μ (gaussianStarts d q) := by
    refine ⟨measurable_pi_lambda _ (fun a => (hg a).measurable), ?_⟩
    change μ.map (fun ω a => g a ω) = _
    rw [hi.map_fun_eq_pi_map (fun a => (hg a).measurable.aemeasurable)]
    simp_rw [fun a => (hg a).map_eq]
    rfl
  exact (hf.measureReal_preimage (measurableSet_gramGood d q _).nullMeasurableSet).symm ▸
    simultaneous_gram_concentration_full hq

#print axioms gram_concentration_independent_starts
#print axioms simultaneous_gram_concentration_full
end AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumKrylov
