import AutoSamplingTheory.TechnicalLemmas.Probability.OrthogonalHaar
import Mathlib.Tactic.FunProp
import Mathlib.Tactic.NormNum

open Matrix MeasureTheory Set
open AutoSamplingTheory.TechnicalLemmas.Probability.OrthogonalHaar

/- A genuine single-row reflection, not a restriction to SO(n). -/
private noncomputable def rowReflection {n : ℕ} (i : Fin n) :
    Matrix.orthogonalGroup (Fin n) ℝ :=
  ⟨Matrix.diagonal (fun j => if j = i then (-1 : ℝ) else 1), by
    apply (Matrix.mem_orthogonalGroup_iff (Fin n) ℝ).2
    rw [Matrix.diagonal_transpose, Matrix.diagonal_mul_diagonal]
    have h : (fun j : Fin n => (if j = i then (-1 : ℝ) else 1) *
        (if j = i then (-1 : ℝ) else 1)) = fun _ => (1 : ℝ) := by
      funext j
      by_cases hj : j = i <;> simp [hj]
    rw [h, Matrix.diagonal_one]⟩

/- The zero-dimensional group is included; no assertion about two components. -/
example : (orthogonalHaar 0) univ = 1 :=
  (orthogonalHaar_spec 0).1.measure_univ

/- Importing the shared node exposes the actual canonical Borel space and a
measurable, measure-preserving single-row reflection in dimension three. -/
example : MeasurePreserving
    (fun O : Matrix.orthogonalGroup (Fin 3) ℝ => rowReflection 1 * O)
    (orthogonalHaar 3) (orthogonalHaar 3) where
  measurable := by fun_prop
  map_eq := orthogonalHaar_map_mul_left 3 (rowReflection 1)

example : (rowReflection (1 : Fin 3) : Matrix (Fin 3) (Fin 3) ℝ) 0 0 = 1 := by
  norm_num [rowReflection, Matrix.diagonal_apply]

example : (rowReflection (1 : Fin 3) : Matrix (Fin 3) (Fin 3) ℝ) 1 1 = -1 := by
  norm_num [rowReflection, Matrix.diagonal_apply]

example : (rowReflection (1 : Fin 3) : Matrix (Fin 3) (Fin 3) ℝ).det = -1 := by
  norm_num [rowReflection, Matrix.det_diagonal, Fin.prod_univ_succ]

#print axioms existsUnique_orthogonalHaar
#print axioms orthogonalHaar_spec
#print axioms orthogonalHaar_map_mul_left
