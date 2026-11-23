import GC44Symbol

/-! Identify the two original Gram operators with compressed weighted
Gaussian row matrices, before applying the scalar probability bounds. -/
noncomputable section
open Matrix
open scoped BigOperators Matrix.Norms.L2Operator
open AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumRotation
open AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumKrylov
namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.CosineProjection

def rowGram {d q : ℕ} (g : Starts d q) (i : Fin d) : Small q :=
  Matrix.vecMulVec (fun a => g a i) (fun a => g a i)

def frequencyWeight (d q : ℕ) (i : Fin d) : ℝ := mode d (2*q+1) i

private theorem feature_entry {d q : ℕ} (g : Starts d q) (i : Fin d) (a : Indices q) :
    feature d q g i a = (Real.sqrt (d : ℝ))⁻¹ * g a.1 i * frame d q i a.2 := by
  rw [frame_entry]
  rfl

theorem lift_rowGram {d q : ℕ} (g : Starts d q) (w : Fin d → ℝ) :
    energyLift (fun i => w i • rowGram g i) =
      (feature d q g).transpose * Matrix.diagonal w * feature d q g := by
  ext a b
  change (∑ i, frame d q i a.2 * frame d q i b.2 * (w i * (g a.1 i * g b.1 i))) / (d : ℝ) = _
  rw [Finset.sum_div]
  rw [Matrix.mul_apply]
  simp only [Matrix.mul_diagonal,Matrix.transpose_apply,feature_entry]
  apply Finset.sum_congr rfl
  intro i _
  have h : (Real.sqrt (d : ℝ))⁻¹ * (Real.sqrt (d : ℝ))⁻¹ = (d : ℝ)⁻¹ := by
    rw [← mul_inv, Real.mul_self_sqrt (Nat.cast_nonneg _)]
  simp only [div_eq_mul_inv]
  linear_combination -(frame d q i a.2 * frame d q i b.2 * w i * g a.1 i * g b.1 i) * h

theorem lift_sub {d q : ℕ} (H J : Fin d → Small q) :
    energyLift (fun i => H i - J i) = energyLift H - energyLift J := by
  ext a b
  simp [energyLift,mul_sub,Finset.sum_sub_distrib,sub_div]

theorem lift_frequency_identity {d q : ℕ} (hf : 2*q+1 < d) :
    energyLift (fun i => frequencyWeight d q i • (1 : Small q)) = 0 := by
  have h := (FixedSpectrumCosineGram.actual_cosine_frame_gram hf).2.1
  have he : frame d q = (fun i k => if k.val = 0 then 1 else Real.sqrt 2 *
      Real.cos ((k.val : ℝ) * gridAngle d i)) := funext fun i => funext (frame_entry d q i)
  have hg : (frame d q).transpose * Matrix.diagonal (frequencyWeight d q) * frame d q = 0 := by
    rw [he]
    exact h
  ext a b
  have e := congrArg (fun M : Small q => M a.2 b.2) hg
  change (((frame d q).transpose * Matrix.diagonal (frequencyWeight d q)) * frame d q) a.2 b.2 = 0 at e
  rw [Matrix.mul_apply] at e
  simp only [Matrix.mul_diagonal, Matrix.transpose_apply] at e
  change (∑ i, frame d q i a.2 * frame d q i b.2 * (frequencyWeight d q i * (1 : Small q) a.1 b.1)) /
    (d : ℝ) = 0
  calc
    _ = (∑ i, frame d q i a.2 * frequencyWeight d q i * frame d q i b.2) *
        (1 : Small q) a.1 b.1 / (d : ℝ) := by
      rw [Finset.sum_mul]
      congr 1
      apply Finset.sum_congr rfl
      intro i _
      ring
    _ = _ := by rw [e]; simp

theorem gram_of_small_symbols {d q : ℕ} (hf : 2*(2*q)+1 < d) (g : Starts d q)
    {τ : ℝ} (ht : 0 ≤ τ)
    (hu : ∀ i, ‖symbol (fun j => rowGram g j - 1) i‖ ≤ τ)
    (hw : ∀ i, ‖symbol (fun j => frequencyWeight d q j • (rowGram g j - 1)) i‖ ≤ τ) :
    g ∈ gramGood d q τ := by
  let B := feature d q g
  let W := cosineDiag d q
  have hq : 2*q+1 < d := by omega
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
    simp only [Matrix.diagonal_one, Matrix.mul_one] at h
    exact h.sub Matrix.isHermitian_one
  constructor
  · rw [← h1, ← lift_symbol hf]
    apply norm_lift_le hq _ ht _ hu
    rw [lift_symbol hf,h1]
    exact hs1
  · rw [← h2, ← lift_symbol hf]
    apply norm_lift_le hq _ ht _ hw
    rw [lift_symbol hf,h2]
    exact hs _

#print axioms gram_of_small_symbols
end AutoSamplingTheory.ExampleCases.GaussianComplexity.CosineProjection
