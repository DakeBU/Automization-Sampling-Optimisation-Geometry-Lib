import GC44Compression
import GC44Concentration
import Mathlib.Probability.HasLaw

/-!
# Uniform bound on the random block Krylov space (Lemma 4.4)

The cosine projection reproduces the Gram forms. Its rows have squared norm
and maximum entry bounded by 2(2q+1)/d. The same bounds survive the signed
cosine weights, so one finite-net probability estimate controls both forms.
-/
noncomputable section
open MeasureTheory ProbabilityTheory Matrix
open scoped Matrix.Norms.L2Operator
open AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumTargetEvent
open AutoSamplingTheory.ExampleCases.GaussianComplexity.CosineProjection
namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumKrylov

private theorem enough_modes {d q : ℕ} (hq : 2*q+1<d) (ht : queryThreshold 2048 d q ≤ 1/2) :
    2*(2*q)+1 < d := by
  have hd2 : 2 ≤ (d : ℝ) := by exact_mod_cast (show 2 ≤ d by omega)
  have hd : 0 < (d : ℝ) := by linarith
  have hlog2 : (1/2 : ℝ) ≤ Real.log 2 := by
    have h := Real.log_le_sub_one_of_pos (show 0 < (2 : ℝ)⁻¹ by norm_num)
    rw [Real.log_inv] at h
    norm_num at h
    linarith
  have hlog := hlog2.trans (Real.log_le_log (by norm_num) hd2)
  let r : ℝ := (q : ℝ)+1
  have hr : 1 ≤ r := by dsimp [r]; linarith [Nat.cast_nonneg (α := ℝ) q]
  have hrest : 0 ≤ r * Real.sqrt (Real.log (d : ℝ)/(d : ℝ)) := by dsimp [r]; positivity
  change 2048*(r * Real.sqrt (Real.log (d : ℝ)/(d : ℝ)) +
    (r*(r+Real.log (d : ℝ))*Real.log (d : ℝ))/(d : ℝ)) ≤ 1/2 at ht
  have hsmall : (r*(r+Real.log (d : ℝ))*Real.log (d : ℝ))/(d : ℝ) ≤ 1/4096 := by linarith
  have hmul := (div_le_iff₀ hd).mp hsmall
  have hbound : r*(1:ℝ)*(1/2) ≤ r*(r+Real.log (d : ℝ))*Real.log (d : ℝ) := by
    gcongr; linarith
  have hreal : 4*(q : ℝ)+1 < d := by dsimp [r] at hbound; linarith
  exact_mod_cast (show 2*(2*(q : ℝ))+1 < d by linarith)

/-- Probability of the joint operator-norm bounds at the source threshold. -/
theorem simultaneous_gram_concentration {d q : ℕ} (hq : 2*q+1<d)
    (ht : queryThreshold 2048 d q ≤ 1/2) :
    (199/200 : ℝ) ≤ (gaussianStarts d q).real (gramGood d q (queryThreshold 2048 d q)) := by
  let P := projection d (2*q)
  let w (b : Bool) (i j : Fin d) := if b then P i j * frequencyWeight d q j else P i j
  have hf := enough_modes hq ht
  have hcos (j : Fin d) : |frequencyWeight d q j| ≤ 1 := Real.abs_cos_le_one _
  have hw (b : Bool) (i : Fin d) : (∀ j, |w b i j| ≤ 2*(2*(q:ℝ)+1)/(d:ℝ)) ∧
      ∑ j,(w b i j)^2 ≤ 2*(2*(q:ℝ)+1)/(d:ℝ) := by
    have he := projection_bounds hf i
    push_cast at he
    cases b
    · exact he
    · refine ⟨fun j => ?_, le_trans (Finset.sum_le_sum (fun j _ => ?_)) he.2⟩
      · change |P i j * frequencyWeight d q j| ≤ _
        rw [abs_mul]
        exact (mul_le_of_le_one_right (abs_nonneg _) (hcos j)).trans (he.1 j)
      · change (P i j * frequencyWeight d q j)^2 ≤ (P i j)^2
        rw [mul_pow]
        exact mul_le_of_le_one_right (sq_nonneg _) (Real.cos_sq_le_one _)
  have h := simultaneous_weighted_row_bounds hq w hw
  apply h.trans
  refine measureReal_mono ?_ (measure_ne_top _ _)
  intro g hg
  have hd : 0 ≤ Real.log (d : ℝ) := Real.log_nonneg (by exact_mod_cast (show 1 ≤ d by omega))
  apply gram_of_small_symbols hf g (show 0 ≤ queryThreshold 2048 d q by unfold queryThreshold; positivity)
  · intro i
    exact hg false i
  · intro i
    have eq : symbol (fun j => frequencyWeight d q j • (rowGram g j - 1)) i =
        weightedRowMatrix g (w true i) := by
      unfold symbol weightedRowMatrix
      apply Finset.sum_congr rfl
      intro j _
      rw [smul_smul]
      rfl
    rw [eq]
    exact hg true i

/-- For independent standard Gaussian starts, with probability at least
0.99 the quadratic-form estimate holds for every vector in the Krylov space. -/
theorem uniform_krylov_bound {d q : ℕ} {κ : ℝ} (hκ : 2 ≤ κ) (hq : 2*q+1<d)
    (ht : queryThreshold 2048 d q ≤ 1/2) :
    ∃ G : Set (Starts d q), MeasurableSet G ∧ (99/100 : ℝ) ≤ (gaussianStarts d q).real G ∧
      ∀ g ∈ G, ∀ u ∈ krylov d q κ g,
      |u ⬝ᵥ (cosineDiag d q *ᵥ u)| ≤ 2*queryThreshold 2048 d q*‖WithLp.toLp 2 u‖^2 := by
  refine ⟨gramGood d q _, measurableSet_gramGood .., ?_, fun _ hg _ hu => bound_on_krylov hκ hq ht hg hu⟩
  exact (by norm_num : (99/100:ℝ) ≤ 199/200).trans (simultaneous_gram_concentration hq ht)

/-- Lemma 4.4 on any experiment carrying independent standard Gaussian starts. -/
theorem uniform_bound_independent_gaussian_starts {d q : ℕ} {κ : ℝ} (hκ : 2 ≤ κ)
    (hq : 2*q+1 < d) (ht : queryThreshold 2048 d q ≤ 1/2)
    {Ω : Type*} [MeasurableSpace Ω] (μ : Measure Ω)
    (g : Fin (q+1) → Ω → Space d)
    (hg : ∀ a, MeasurePreserving (g a) μ (stdGaussian (Space d))) (hi : iIndepFun g μ) :
    ∃ G : Set Ω, MeasurableSet G ∧ (99/100 : ℝ) ≤ μ.real G ∧
      ∀ ω ∈ G, ∀ u ∈ krylov d q κ (fun a => g a ω),
        |u ⬝ᵥ (cosineDiag d q *ᵥ u)| ≤ 2*queryThreshold 2048 d q*‖WithLp.toLp 2 u‖^2 := by
  obtain ⟨S,hS,hm,hb⟩ := uniform_krylov_bound hκ hq ht
  let f (ω : Ω) : Starts d q := fun a => g a ω
  have hf : MeasurePreserving f μ (gaussianStarts d q) := by
    refine ⟨measurable_pi_lambda _ (fun a => (hg a).measurable), ?_⟩
    change μ.map (fun ω a => g a ω) = _
    rw [hi.map_fun_eq_pi_map (fun a => (hg a).measurable.aemeasurable)]
    simp_rw [fun a => (hg a).map_eq]
    rfl
  exact ⟨f ⁻¹' S, hf.measurable hS, (hf.measureReal_preimage hS.nullMeasurableSet).symm ▸ hm,
    fun ω hω => hb (f ω) hω⟩

#print axioms uniform_bound_independent_gaussian_starts
#print axioms simultaneous_gram_concentration
#print axioms uniform_krylov_bound

end AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumKrylov
