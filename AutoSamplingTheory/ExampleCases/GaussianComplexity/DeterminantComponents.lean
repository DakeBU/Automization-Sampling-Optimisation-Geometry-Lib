import AutoSamplingTheory.TechnicalLemmas.Probability.OrthogonalHaar
import Mathlib.MeasureTheory.Measure.Real
import Mathlib.Tactic.FunProp
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.NormNum

/-!
# Actual determinant-component Haar probabilities

Zhou--Suzuki arXiv:2610.20492v1, Appendix B.2.2 first proof paragraph
before Eq20. The source asserts half-mass without spelling out its elementary
symmetry proof. This supplies that background and literal restriction-law
normalization, explicitly generalized from the application n>=3 to n>=1.
Actual Gaussian target mixtures, TV and both query lower bounds remain separate.
-/

open Matrix MeasureTheory Set
open scoped ENNReal
open AutoSamplingTheory.TechnicalLemmas.Probability.OrthogonalHaar

namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.DeterminantComponents

theorem component_probabilities {n : ℕ} (hn : 0 < n) :
    let μ := orthogonalHaar n
    let Cpos : Set (Matrix.orthogonalGroup (Fin n) ℝ) :=
      {O | (O : Matrix (Fin n) (Fin n) ℝ).det = 1}
    let Cneg : Set (Matrix.orthogonalGroup (Fin n) ℝ) :=
      {O | (O : Matrix (Fin n) (Fin n) ℝ).det = -1}
    μ Cpos = (2 : ℝ≥0∞)⁻¹ ∧ μ Cneg = (2 : ℝ≥0∞)⁻¹ ∧
    IsProbabilityMeasure ((2 : ℝ≥0∞) • μ.restrict Cpos) ∧
    IsProbabilityMeasure ((2 : ℝ≥0∞) • μ.restrict Cneg) := by
  classical
  dsimp only
  let μ := orthogonalHaar n
  let G := Matrix.orthogonalGroup (Fin n) ℝ
  let Cpos : Set G := {O | (O : Matrix (Fin n) (Fin n) ℝ).det = 1}
  let Cneg : Set G := {O | (O : Matrix (Fin n) (Fin n) ℝ).det = -1}
  let := (orthogonalHaar_spec n).1
  have hcont : Continuous (fun O : G => (O : Matrix (Fin n) (Fin n) ℝ).det) := by
    fun_prop
  have hpos : MeasurableSet Cpos := (isClosed_eq hcont continuous_const).measurableSet
  have hsign (O : G) : (O : Matrix (Fin n) (Fin n) ℝ).det = 1 ∨
      (O : Matrix (Fin n) (Fin n) ℝ).det = -1 := by
    have h := congrArg Matrix.det
      ((Matrix.mem_orthogonalGroup_iff (Fin n) ℝ).mp O.property)
    rw [Matrix.det_mul, Matrix.det_transpose, Matrix.det_one] at h
    exact mul_self_eq_one_iff.mp h
  let i : Fin n := ⟨0, hn⟩
  let R : G := ⟨Matrix.diagonal (fun j => if j = i then (-1 : ℝ) else 1), by
    apply (Matrix.mem_orthogonalGroup_iff (Fin n) ℝ).2
    rw [Matrix.diagonal_transpose, Matrix.diagonal_mul_diagonal]
    have heq : (fun j : Fin n => (if j = i then (-1 : ℝ) else 1) *
        (if j = i then (-1 : ℝ) else 1)) = fun _ => (1 : ℝ) := by
      funext j
      by_cases hj : j = i <;> simp [hj]
    rw [heq, Matrix.diagonal_one]⟩
  have hR : (R : Matrix (Fin n) (Fin n) ℝ).det = -1 := by
    simp [R, Matrix.det_diagonal]
  have hswap : (fun O : G => R * O) ⁻¹' Cpos = Cneg := by
    ext O
    change ((R : Matrix (Fin n) (Fin n) ℝ) *
      (O : Matrix (Fin n) (Fin n) ℝ)).det = 1 ↔
        (O : Matrix (Fin n) (Fin n) ℝ).det = -1
    rw [Matrix.det_mul, hR, neg_one_mul]
    constructor <;> intro h <;> linarith
  have hequal : μ Cpos = μ Cneg := by
    calc
      μ Cpos = (μ.map (fun O : G => R * O)) Cpos := by
        rw [orthogonalHaar_map_mul_left]
      _ = μ ((fun O : G => R * O) ⁻¹' Cpos) :=
        Measure.map_apply (by fun_prop) hpos
      _ = μ Cneg := by rw [hswap]
  have hcompl : Cposᶜ = Cneg := by
    ext O
    change ¬ (O : Matrix (Fin n) (Fin n) ℝ).det = 1 ↔
      (O : Matrix (Fin n) (Fin n) ℝ).det = -1
    rcases hsign O with h | h <;> norm_num [h]
  have hadd : μ Cpos + μ Cneg = 1 := by
    rw [← hcompl, measure_add_measure_compl hpos]
    exact measure_univ
  have hp : μ Cpos = (2 : ℝ≥0∞)⁻¹ := by
    apply (ENNReal.toReal_eq_toReal_iff' (measure_ne_top μ Cpos) (by simp)).mp
    have h := congrArg ENNReal.toReal hadd
    rw [ENNReal.toReal_add (measure_ne_top μ Cpos) (measure_ne_top μ Cneg),
      ← hequal] at h
    norm_num at h ⊢
    linarith
  have hm : μ Cneg = (2 : ℝ≥0∞)⁻¹ := hequal.symm.trans hp
  refine ⟨hp, hm, ⟨?_⟩, ⟨?_⟩⟩
  · rw [Measure.smul_apply, Measure.restrict_apply_univ, hp]
    exact ENNReal.mul_inv_cancel (by norm_num) (by norm_num)
  · rw [Measure.smul_apply, Measure.restrict_apply_univ, hm]
    exact ENNReal.mul_inv_cancel (by norm_num) (by norm_num)

end AutoSamplingTheory.ExampleCases.GaussianComplexity.DeterminantComponents
