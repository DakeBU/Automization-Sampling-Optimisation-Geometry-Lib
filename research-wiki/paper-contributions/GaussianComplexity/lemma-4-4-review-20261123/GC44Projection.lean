import GC41Target
import AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumCosineGram
import Mathlib.Tactic

/-! On the midpoint grid, the orthogonal projection onto cosine modes up to
degree 2q reproduces products of two degree-q modes. Its rows provide the
scalar weights for testing the smaller matrices on the Gaussian-start index. -/
noncomputable section
open Matrix
open scoped BigOperators
open AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumRotation
namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.CosineProjection

def scale (k : ℕ) : ℝ := if k = 0 then 1 else Real.sqrt 2
def mode (d k : ℕ) (i : Fin d) : ℝ := Real.cos ((k : ℝ) * gridAngle d i)
def frame (d m : ℕ) : Matrix (Fin d) (Fin (m+1)) ℝ := fun i a => scale a.val * mode d a.val i
def projection (d m : ℕ) : Matrix (Fin d) (Fin d) ℝ :=
  (d : ℝ)⁻¹ • (frame d m * (frame d m).transpose)

theorem frame_entry (d m : ℕ) (i : Fin d) (a : Fin (m+1)) :
    frame d m i a = if a.val = 0 then 1 else Real.sqrt 2 * Real.cos ((a.val : ℝ) * gridAngle d i) := by
  by_cases h : a.val = 0 <;> simp [frame,scale,mode,h]

theorem frame_data {d m : ℕ} (h : 2*m+1 < d) :
    (frame d m).transpose * frame d m = (d : ℝ) • 1 ∧
    ∀ i, ∑ k, (frame d m i k)^2 ≤ 2*((m : ℝ)+1) := by
  have t := FixedSpectrumCosineGram.actual_cosine_frame_gram h
  have hf : frame d m = (fun i k => if k.val = 0 then 1 else Real.sqrt 2 *
      Real.cos ((k.val : ℝ) * gridAngle d i)) := funext fun i => funext (frame_entry d m i)
  rw [hf]
  exact ⟨t.1,t.2.2⟩

theorem projection_transpose (d m : ℕ) : (projection d m).transpose = projection d m := by
  simp [projection,Matrix.transpose_mul]

theorem projection_times_frame {d m : ℕ} (h : 2*m+1 < d) :
    projection d m * frame d m = frame d m := by
  have hd : (d : ℝ) ≠ 0 := by exact_mod_cast (show d ≠ 0 by omega)
  rw [projection, Matrix.smul_mul, Matrix.mul_assoc, (frame_data h).1, Matrix.mul_smul,
    Matrix.mul_one, smul_smul, inv_mul_cancel₀ hd, one_smul]

theorem projection_bounds {d m : ℕ} (h : 2*m+1 < d) (i : Fin d) :
    (∀ j, |projection d m i j| ≤ 2*((m : ℝ)+1)/(d : ℝ)) ∧
    ∑ j, (projection d m i j)^2 ≤ 2*((m : ℝ)+1)/(d : ℝ) := by
  have hd : 0 < (d : ℝ) := by exact_mod_cast (show 0 < d by omega)
  have hnorm := (frame_data h).2
  have symm (j : Fin d) : projection d m j i = projection d m i j :=
    congrArg (fun M : Matrix (Fin d) (Fin d) ℝ => M i j) (projection_transpose d m)
  have diag : projection d m i i ≤ 2*((m : ℝ)+1)/(d : ℝ) := by
    change (d : ℝ)⁻¹ * (∑ k, frame d m i k * frame d m i k) ≤ _
    simpa only [← sq, div_eq_inv_mul] using
      (mul_le_mul_of_nonneg_left (hnorm i) (inv_nonneg.mpr hd.le))
  constructor
  · intro j
    change |(d : ℝ)⁻¹ * (∑ k, frame d m i k * frame d m j k)| ≤ _
    rw [abs_mul, abs_of_nonneg (inv_nonneg.mpr hd.le), div_eq_inv_mul]
    apply mul_le_mul_of_nonneg_left _ (inv_nonneg.mpr hd.le)
    calc
      _ ≤ ∑ k, |frame d m i k * frame d m j k| := Finset.abs_sum_le_sum_abs _ _
      _ ≤ ∑ k, ((frame d m i k)^2 + (frame d m j k)^2)/2 := by
        apply Finset.sum_le_sum
        intro k _
        rw [abs_mul]
        nlinarith [sq_nonneg (|frame d m i k| - |frame d m j k|),
          sq_abs (frame d m i k), sq_abs (frame d m j k)]
      _ ≤ _ := by rw [← Finset.sum_div, Finset.sum_add_distrib]; linarith [hnorm i, hnorm j]
  · have idemp : projection d m * projection d m = projection d m := by
      conv_lhs => arg 2; unfold projection
      rw [Matrix.mul_smul, ← Matrix.mul_assoc, projection_times_frame h]
      rfl
    have eq := congrArg (fun M : Matrix (Fin d) (Fin d) ℝ => M i i) idemp
    change (∑ j, projection d m i j * projection d m j i) = _ at eq
    simpa only [symm, ← sq] using eq.le.trans diag

/-- Every mode in the projection range is fixed, including the constant mode. -/
theorem fix_mode {d m : ℕ} (h : 2*m+1 < d) {k : ℕ} (hk : k ≤ m) (i : Fin d) :
    ∑ j, projection d m i j * mode d k j = mode d k i := by
  let a : Fin (m+1) := ⟨k, by omega⟩
  have he := congrArg (fun M : Matrix (Fin d) (Fin (m+1)) ℝ => M i a) (projection_times_frame h)
  change ∑ j, projection d m i j * (scale k * mode d k j) = scale k * mode d k i at he
  have hs : scale k ≠ 0 := by unfold scale; split_ifs <;> positivity
  apply mul_left_cancel₀ hs
  rw [Finset.mul_sum]
  simpa only [mul_left_comm] using he

private theorem cos_pair {d a b : ℕ} (hab : b ≤ a) (i : Fin d) :
    mode d a i * mode d b i = (mode d (a-b) i + mode d (a+b) i)/2 := by
  unfold mode
  rw [Nat.cast_sub hab, Nat.cast_add, add_mul, sub_mul]
  linarith [Real.two_mul_cos_mul_cos ((a : ℝ) * gridAngle d i) ((b : ℝ) * gridAngle d i)]

theorem reproduce_product {d q : ℕ} (h : 2*(2*q)+1 < d) (i : Fin d) (a b : Fin (q+1)) :
    ∑ j, projection d (2*q) i j * (frame d q j a * frame d q j b) =
      frame d q i a * frame d q i b := by
  suffices hx : ∑ j, projection d (2*q) i j * (mode d a.val j * mode d b.val j) =
      mode d a.val i * mode d b.val i by
    calc
      _ = (scale a.val * scale b.val) * ∑ j, projection d (2*q) i j *
          (mode d a.val j * mode d b.val j) := by
        rw [Finset.mul_sum]
        apply Finset.sum_congr rfl
        intro j _
        dsimp [frame]
        ring
      _ = _ := by rw [hx]; dsimp [frame]; ring
  have ordered (u v : Fin (q+1)) (hv : v.val ≤ u.val) :
      ∑ j, projection d (2*q) i j * (mode d u.val j * mode d v.val j) =
        mode d u.val i * mode d v.val i := by
    simp_rw [cos_pair hv, mul_div_assoc', mul_add]
    rw [← Finset.sum_div, Finset.sum_add_distrib, fix_mode h (by omega), fix_mode h (by omega)]
  rcases le_total b.val a.val with hba | hab
  · exact ordered a b hba
  · simpa only [mul_comm (mode d b.val _) (mode d a.val _)] using ordered b a hab

end AutoSamplingTheory.ExampleCases.GaussianComplexity.CosineProjection
