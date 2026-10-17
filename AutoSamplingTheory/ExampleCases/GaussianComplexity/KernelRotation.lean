import AutoSamplingTheory.ExampleCases.GaussianComplexity.DeterminantFamily
import AutoSamplingTheory.TechnicalLemmas.Probability.OrthogonalHaar
import Mathlib.MeasureTheory.Function.LocallyIntegrable
import Mathlib.Tactic.FunProp
import Mathlib.Tactic.Ring

/-!
# Rotation invariance of the literal signed Gaussian kernel average

Zhou--Suzuki arXiv:2610.20492v1, Appendix B.2.2 p4.1, the fixed-Q
conjugation step underlying Ex58. The displayed kernel is literal; its
identification as the density of an actual Gaussian law is a separate obligation.
Orthogonal transitivity, the norm-axis identity, spatial Fubini and TV are separate.
-/

open Matrix MeasureTheory Set TopologicalSpace
open AutoSamplingTheory.TechnicalLemmas.Probability.OrthogonalHaar
open AutoSamplingTheory.ExampleCases.GaussianComplexity.DeterminantFamily

namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.KernelRotation

private lemma haar_conjugation {n : ℕ} (Q : Matrix.orthogonalGroup (Fin n) ℝ) :
    (orthogonalHaar n).map (fun O => Q * O * Q⁻¹) = orthogonalHaar n := by
  let := (orthogonalHaar_spec n).1
  let := (orthogonalHaar_spec n).2.1
  have hr : (orthogonalHaar n).map (fun O => O * Q⁻¹) = orthogonalHaar n := by
    apply (orthogonalHaar_spec n).2.2
    · exact Measure.isProbabilityMeasure_map (by fun_prop)
    · infer_instance
  have heq : (fun O => Q * O * Q⁻¹) =
      (fun O => Q * O) ∘ (fun O => O * Q⁻¹) := by
    funext O
    exact mul_assoc Q O Q⁻¹
  rw [heq, ← Measure.map_map (by fun_prop) (by fun_prop), hr,
    orthogonalHaar_map_mul_left]

private lemma conjugation_algebra {n : ℕ} (κ : ℝ)
    (Q O : Matrix.orthogonalGroup (Fin n) ℝ) :
    singleBlockPrecision κ (Q * O * Q⁻¹) =
        (Q : Matrix (Fin n) (Fin n) ℝ) * singleBlockPrecision κ O *
          (Q : Matrix (Fin n) (Fin n) ℝ).transpose ∧
    ((Q * O * Q⁻¹ : Matrix.orthogonalGroup (Fin n) ℝ) : Matrix (Fin n) (Fin n) ℝ).det =
      (O : Matrix (Fin n) (Fin n) ℝ).det ∧
    (singleBlockPrecision κ (Q * O * Q⁻¹)).det = (singleBlockPrecision κ O).det ∧
    ∀ x : Fin n → ℝ,
      ((Q : Matrix (Fin n) (Fin n) ℝ) *ᵥ x) ⬝ᵥ
        (singleBlockPrecision κ (Q * O * Q⁻¹) *ᵥ
          ((Q : Matrix (Fin n) (Fin n) ℝ) *ᵥ x)) =
      x ⬝ᵥ (singleBlockPrecision κ O *ᵥ x) := by
  have hQ : (Q : Matrix (Fin n) (Fin n) ℝ) *
      (Q : Matrix (Fin n) (Fin n) ℝ).transpose = 1 :=
    (Matrix.mem_orthogonalGroup_iff (Fin n) ℝ).mp Q.property
  have hQt : (Q : Matrix (Fin n) (Fin n) ℝ).transpose *
      (Q : Matrix (Fin n) (Fin n) ℝ) = 1 :=
    (Matrix.mem_orthogonalGroup_iff' (Fin n) ℝ).mp Q.property
  have hinv : ((Q⁻¹ : Matrix.orthogonalGroup (Fin n) ℝ) : Matrix (Fin n) (Fin n) ℝ) =
      (Q : Matrix (Fin n) (Fin n) ℝ).transpose := by ext i j; rfl
  have hcoe : ((Q * O * Q⁻¹ : Matrix.orthogonalGroup (Fin n) ℝ) :
      Matrix (Fin n) (Fin n) ℝ) =
      (Q : Matrix (Fin n) (Fin n) ℝ) * (O : Matrix (Fin n) (Fin n) ℝ) *
        (Q : Matrix (Fin n) (Fin n) ℝ).transpose := by
    simp only [Matrix.UnitaryGroup.mul_val, hinv]
  have hA : singleBlockPrecision κ (Q * O * Q⁻¹) =
      (Q : Matrix (Fin n) (Fin n) ℝ) * singleBlockPrecision κ O *
        (Q : Matrix (Fin n) (Fin n) ℝ).transpose := by
    simp only [singleBlockPrecision, hcoe, Matrix.transpose_mul, Matrix.transpose_transpose,
      Matrix.mul_sub, Matrix.sub_mul, Matrix.mul_smul, Matrix.smul_mul,
      Matrix.mul_add, Matrix.add_mul, Matrix.mul_one, Matrix.mul_assoc, hQ]
  have hd : (Q : Matrix (Fin n) (Fin n) ℝ).det *
      (Q : Matrix (Fin n) (Fin n) ℝ).det = 1 := by
    simpa only [Matrix.det_mul, Matrix.det_transpose, Matrix.det_one] using congrArg Matrix.det hQ
  have hdet (M : Matrix (Fin n) (Fin n) ℝ) :
      ((Q : Matrix (Fin n) (Fin n) ℝ) * M *
        (Q : Matrix (Fin n) (Fin n) ℝ).transpose).det = M.det := by
    simp only [Matrix.det_mul, Matrix.det_transpose]
    calc
      _ = M.det * ((Q : Matrix (Fin n) (Fin n) ℝ).det *
        (Q : Matrix (Fin n) (Fin n) ℝ).det) := by ring
      _ = M.det := by rw [hd, mul_one]
  refine ⟨hA, by rw [hcoe, hdet], by rw [hA, hdet], ?_⟩
  intro x
  rw [hA]
  have hm : ((Q : Matrix (Fin n) (Fin n) ℝ) * singleBlockPrecision κ O *
      (Q : Matrix (Fin n) (Fin n) ℝ).transpose) *ᵥ
        ((Q : Matrix (Fin n) (Fin n) ℝ) *ᵥ x) =
      (Q : Matrix (Fin n) (Fin n) ℝ) *ᵥ (singleBlockPrecision κ O *ᵥ x) := by
    simp only [Matrix.mulVec_mulVec, Matrix.mul_assoc, hQt, Matrix.mul_one]
  rw [hm, dotProduct_comm, ← Matrix.dotProduct_transpose_mulVec,
    Matrix.mulVec_mulVec, hQt, Matrix.one_mulVec, dotProduct_comm]

theorem signed_kernel_rotation_invariant {n : ℕ} (_hn : 3 ≤ n) {κ : ℝ}
    (_hκ : 4 ≤ κ) :
    let p : Matrix.orthogonalGroup (Fin n) ℝ → (Fin n → ℝ) → ℝ :=
      fun O x => Real.sqrt (singleBlockPrecision κ O).det /
        (2 * Real.pi) ^ ((n : ℝ) / 2) *
          Real.exp (-(x ⬝ᵥ (singleBlockPrecision κ O *ᵥ x)) / 2)
    (∀ x : Fin n → ℝ, Integrable (fun O : Matrix.orthogonalGroup (Fin n) ℝ =>
      (O : Matrix (Fin n) (Fin n) ℝ).det * p O x) (orthogonalHaar n)) ∧
    ∀ (Q : Matrix.orthogonalGroup (Fin n) ℝ) (x : Fin n → ℝ),
      (∫ O : Matrix.orthogonalGroup (Fin n) ℝ,
        (O : Matrix (Fin n) (Fin n) ℝ).det *
          p O ((Q : Matrix (Fin n) (Fin n) ℝ) *ᵥ x) ∂orthogonalHaar n) =
      (∫ O : Matrix.orthogonalGroup (Fin n) ℝ,
        (O : Matrix (Fin n) (Fin n) ℝ).det * p O x ∂orthogonalHaar n) := by
  classical
  let p : Matrix.orthogonalGroup (Fin n) ℝ → (Fin n → ℝ) → ℝ :=
    fun O x => Real.sqrt (singleBlockPrecision κ O).det /
      (2 * Real.pi) ^ ((n : ℝ) / 2) *
        Real.exp (-(x ⬝ᵥ (singleBlockPrecision κ O *ᵥ x)) / 2)
  change (∀ x : Fin n → ℝ, Integrable (fun O : Matrix.orthogonalGroup (Fin n) ℝ =>
      (O : Matrix (Fin n) (Fin n) ℝ).det * p O x) (orthogonalHaar n)) ∧ _
  have hAc : Continuous (fun O : Matrix.orthogonalGroup (Fin n) ℝ => singleBlockPrecision κ O) := by
    unfold singleBlockPrecision
    exact continuous_const.sub
      ((continuous_subtype_val.add continuous_subtype_val.matrix_transpose).const_smul ((κ - 1) / 4))
  have hcont (x : Fin n → ℝ) : Continuous (fun O : Matrix.orthogonalGroup (Fin n) ℝ =>
      (O : Matrix (Fin n) (Fin n) ℝ).det * p O x) := by
    dsimp only [p]
    fun_prop
  have hL1 (x : Fin n → ℝ) : Integrable (fun O : Matrix.orthogonalGroup (Fin n) ℝ =>
      (O : Matrix (Fin n) (Fin n) ℝ).det * p O x) (orthogonalHaar n) := by
    let := (orthogonalHaar_spec n).1
    exact (hcont x).integrable_of_hasCompactSupport (isClosed_tsupport _).isCompact
  refine ⟨hL1, ?_⟩
  intro Q x
  have hcov (O : Matrix.orthogonalGroup (Fin n) ℝ) :
      ((Q * O * Q⁻¹ : Matrix.orthogonalGroup (Fin n) ℝ) : Matrix (Fin n) (Fin n) ℝ).det *
        p (Q * O * Q⁻¹) ((Q : Matrix (Fin n) (Fin n) ℝ) *ᵥ x) =
      (O : Matrix (Fin n) (Fin n) ℝ).det * p O x := by
    obtain ⟨_, hd, hA, hquad⟩ := conjugation_algebra κ Q O
    dsimp only [p]
    rw [hd, hA, hquad]
  have hemb : MeasurableEmbedding (fun O : Matrix.orthogonalGroup (Fin n) ℝ => Q * O * Q⁻¹) :=
    ((Homeomorph.mulLeft Q).trans (Homeomorph.mulRight Q⁻¹)).measurableEmbedding
  calc
    _ = ∫ O : Matrix.orthogonalGroup (Fin n) ℝ,
        ((Q * O * Q⁻¹ : Matrix.orthogonalGroup (Fin n) ℝ) : Matrix (Fin n) (Fin n) ℝ).det *
          p (Q * O * Q⁻¹) ((Q : Matrix (Fin n) (Fin n) ℝ) *ᵥ x) ∂orthogonalHaar n := by
      have hmp : MeasurePreserving
          (fun O : Matrix.orthogonalGroup (Fin n) ℝ => Q * O * Q⁻¹)
          (orthogonalHaar n) (orthogonalHaar n) :=
        ⟨hemb.measurable, haar_conjugation Q⟩
      exact (hmp.integral_comp hemb (fun O : Matrix.orthogonalGroup (Fin n) ℝ =>
        (O : Matrix (Fin n) (Fin n) ℝ).det *
          p O ((Q : Matrix (Fin n) (Fin n) ℝ) *ᵥ x))).symm
    _ = _ := by apply integral_congr_ae; exact Filter.Eventually.of_forall hcov

end AutoSamplingTheory.ExampleCases.GaussianComplexity.KernelRotation
