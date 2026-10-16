import AutoSamplingTheory.ExampleCases.GaussianComplexity.DeterminantCancellation
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.NormNum.RealSqrt

open Matrix MeasureTheory Set
open AutoSamplingTheory.TechnicalLemmas.Probability.OrthogonalHaar
open AutoSamplingTheory.ExampleCases.GaussianComplexity.DeterminantFamily
open AutoSamplingTheory.ExampleCases.GaussianComplexity.DeterminantCancellation

private noncomputable def negativeIdentity (n : ℕ) : Matrix.orthogonalGroup (Fin n) ℝ :=
  ⟨-1, by
    apply (Matrix.mem_orthogonalGroup_iff (Fin n) ℝ).2
    simp⟩

private lemma mean_entry_zero {n : ℕ} (j : Fin n) :
    (∫ O : Matrix.orthogonalGroup (Fin n) ℝ,
      (O : Matrix (Fin n) (Fin n) ℝ) j j ∂orthogonalHaar n) = 0 := by
  let F (O : Matrix.orthogonalGroup (Fin n) ℝ) : ℝ :=
    (O : Matrix (Fin n) (Fin n) ℝ) j j
  have hodd : ∀ O, F (negativeIdentity n * O) = -F O := by
    intro O
    change (((-1 : Matrix (Fin n) (Fin n) ℝ) * (O : Matrix (Fin n) (Fin n) ℝ)) j j) = _
    simp [F]
  have hemb : MeasurableEmbedding
      (fun O : Matrix.orthogonalGroup (Fin n) ℝ => negativeIdentity n * O) :=
    (MeasurableEquiv.mulLeft (negativeIdentity n)).measurableEmbedding
  have hi : (∫ O, F (negativeIdentity n * O) ∂orthogonalHaar n) =
      ∫ O, F O ∂orthogonalHaar n := by
    rw [← hemb.integral_map, orthogonalHaar_map_mul_left]
  have he : -(∫ O, F O ∂orthogonalHaar n) = ∫ O, F O ∂orthogonalHaar n := by
    simpa only [hodd, integral_neg] using hi
  change (∫ O, F O ∂orthogonalHaar n) = 0
  linarith

private lemma integrable_entry {n : ℕ} (j : Fin n) :
    Integrable (fun O : Matrix.orthogonalGroup (Fin n) ℝ =>
      (O : Matrix (Fin n) (Fin n) ℝ) j j) (orthogonalHaar n) := by
  let := (orthogonalHaar_spec n).1
  have hc : Continuous (fun O : Matrix.orthogonalGroup (Fin n) ℝ =>
      (O : Matrix (Fin n) (Fin n) ℝ) j j) := continuous_subtype_val.matrix_elem j j
  exact (integrable_const (1 : ℝ)).mono' hc.measurable.aestronglyMeasurable
    (Filter.Eventually.of_forall fun O => entry_norm_bound_of_unitary O.property j j)

private lemma affine_entry_average {n : ℕ} (j : Fin n) (a b : ℝ) :
    (∫ O : Matrix.orthogonalGroup (Fin n) ℝ,
      (a * (O : Matrix (Fin n) (Fin n) ℝ) j j + b) * 1 ∂orthogonalHaar n) = b := by
  let := (orthogonalHaar_spec n).1
  simp only [mul_one]
  rw [integral_add ((integrable_entry j).const_mul a) (integrable_const b),
    integral_const_mul, mean_entry_zero]
  simp

/- The empty-minor contribution survives: these exact signed averages are
nonzero and have opposite parity in dimensions three and four. -/
example : (∫ O : Matrix.orthogonalGroup (Fin 3) ℝ,
    (O : Matrix (Fin 3) (Fin 3) ℝ).det * Real.sqrt (singleBlockPrecision (4 : ℝ) O).det
      ∂orthogonalHaar 3) = -1 / 8 := by
  let := (orthogonalHaar_spec 3).1
  have hb := signed_sqrt_det_integral (by decide : 3 ≤ 3) (by norm_num : 4 ≤ (4 : ℝ))
    (fun _ => 1) measurable_const (integrable_const 1)
  have ha := affine_entry_average (0 : Fin 3) 3 (-1)
  have ha' : (∫ O : Matrix.orthogonalGroup (Fin 3) ℝ,
      3 * (O : Matrix (Fin 3) (Fin 3) ℝ) 0 0 - 1 ∂orthogonalHaar 3) = -1 := by
    simpa only [mul_one, sub_eq_add_neg] using ha
  norm_num at hb
  rw [ha'] at hb
  norm_num at hb
  simpa only [neg_div] using hb

example : (∫ O : Matrix.orthogonalGroup (Fin 4) ℝ,
    (O : Matrix (Fin 4) (Fin 4) ℝ).det * Real.sqrt (singleBlockPrecision (4 : ℝ) O).det
      ∂orthogonalHaar 4) = 1 / 16 := by
  let := (orthogonalHaar_spec 4).1
  have hb := signed_sqrt_det_integral (by decide : 3 ≤ 4) (by norm_num : 4 ≤ (4 : ℝ))
    (fun _ => 1) measurable_const (integrable_const 1)
  have ha := affine_entry_average (0 : Fin 4) 3 (-1)
  have ha' : (∫ O : Matrix.orthogonalGroup (Fin 4) ℝ,
      3 * (O : Matrix (Fin 4) (Fin 4) ℝ) 0 0 - 1 ∂orthogonalHaar 4) = -1 := by
    simpa only [mul_one, sub_eq_add_neg] using ha
  norm_num at hb
  rw [ha'] at hb
  norm_num at hb
  exact hb

/- h(t)=t is globally unbounded. Its actual Haar composition is L1 internally,
and the non-first one-by-one principal minor still cancels. -/
example : (∫ O : Matrix.orthogonalGroup (Fin 3) ℝ,
    ((O : Matrix (Fin 3) (Fin 3) ℝ).submatrix
      (Subtype.val : ({1} : Finset (Fin 3)) → Fin 3)
      (Subtype.val : ({1} : Finset (Fin 3)) → Fin 3)).det *
      (O : Matrix (Fin 3) (Fin 3) ℝ) 0 0 ∂orthogonalHaar 3) = 0 := by
  exact (principalMinor_weighted_integral_eq_zero (by decide : 3 ≤ 3) {1} 1
    (by simp) (by decide) id measurable_id (integrable_entry 0)).2

#print axioms principalMinor_weighted_integral_eq_zero
#print axioms signed_sqrt_det_integral
