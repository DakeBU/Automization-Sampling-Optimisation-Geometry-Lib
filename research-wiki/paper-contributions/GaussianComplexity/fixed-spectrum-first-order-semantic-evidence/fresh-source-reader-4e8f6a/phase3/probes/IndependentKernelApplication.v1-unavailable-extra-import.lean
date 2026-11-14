import Tests.GaussianComplexityFixedSpectrumFirstOrder
import Mathlib.Data.Matrix.Notation
import Mathlib.Tactic.FinCases
import Lean.Util.CollectAxioms

open Matrix InnerProductSpace Lean Elab Command
set_option autoImplicit false
set_option maxRecDepth 4096

theorem sourceReviewerAnonymousApplication :
∀ {d : ℕ} (hd : 2 ≤ d)
    {κ : ℝ} (hκ : 2 ≤ κ)
    (O : Matrix.orthogonalGroup (Fin d) ℝ),
    let θ : Fin d → ℝ := fun i => ((i.val : ℝ) + 1 / 2) * Real.pi / (d : ℝ)
    let A : Matrix (Fin d) (Fin d) ℝ :=
      (O : Matrix (Fin d) (Fin d) ℝ) *
        Matrix.diagonal (fun i => (κ + 1) / 2 + (κ - 1) / 2 * Real.cos (θ i)) *
        (O : Matrix (Fin d) (Fin d) ℝ).transpose
    let f : EuclideanSpace ℝ (Fin d) → ℝ := fun x =>
      (WithLp.ofLp x) ⬝ᵥ (A *ᵥ WithLp.ofLp x) / 2
    let query : EuclideanSpace ℝ (Fin d) → EuclideanSpace ℝ (Fin d) :=
      fun x => WithLp.toLp 2 (A *ᵥ WithLp.ofLp x)
    ∀ x : EuclideanSpace ℝ (Fin d),
      HasGradientAt f (query x) x ∧
      (f x, gradient f x) = (inner ℝ x (query x) / 2, query x)
 := by
  exact @AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumFirstOrder.actual_first_order_query

def sourceReviewerReflectionMatrix : Matrix (Fin 2) (Fin 2) ℝ := !![-1, 0; 0, 1]
def sourceReviewerReflection : Matrix.orthogonalGroup (Fin 2) ℝ :=
  ⟨sourceReviewerReflectionMatrix, by
    apply (Matrix.mem_orthogonalGroup_iff (n := Fin 2) (R := ℝ)).mpr
    ext i j
    fin_cases i <;> fin_cases j <;>
      norm_num [sourceReviewerReflectionMatrix, Matrix.mul_apply, Fin.sum_univ_two]⟩

example : Matrix.det (sourceReviewerReflection : Matrix (Fin 2) (Fin 2) ℝ) = -1 := by
  norm_num [sourceReviewerReflection, sourceReviewerReflectionMatrix, Matrix.det_fin_two]

example : Matrix.det ((1 : Matrix.orthogonalGroup (Fin 2) ℝ) : Matrix (Fin 2) (Fin 2) ℝ) = 1 := by
  simp

theorem sourceReviewerDeterminantMinusOneApplication :
    let d : ℕ := 2
    let κ : ℝ := 2
    let O : Matrix.orthogonalGroup (Fin d) ℝ := sourceReviewerReflection
    let θ : Fin d → ℝ := fun i => ((i.val : ℝ) + 1 / 2) * Real.pi / (d : ℝ)
    let A : Matrix (Fin d) (Fin d) ℝ :=
      (O : Matrix (Fin d) (Fin d) ℝ) *
        Matrix.diagonal (fun i => (κ + 1) / 2 + (κ - 1) / 2 * Real.cos (θ i)) *
        (O : Matrix (Fin d) (Fin d) ℝ).transpose
    let f : EuclideanSpace ℝ (Fin d) → ℝ := fun x =>
      (WithLp.ofLp x) ⬝ᵥ (A *ᵥ WithLp.ofLp x) / 2
    let query : EuclideanSpace ℝ (Fin d) → EuclideanSpace ℝ (Fin d) :=
      fun x => WithLp.toLp 2 (A *ᵥ WithLp.ofLp x)
    ∀ x : EuclideanSpace ℝ (Fin d),
      HasGradientAt f (query x) x ∧
      (f x, gradient f x) = (inner ℝ x (query x) / 2, query x) := by
  exact AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumFirstOrder.actual_first_order_query
    (d := 2) (by decide) (κ := 2) (by norm_num) sourceReviewerReflection

theorem sourceReviewerDeterminantPlusOneApplication :
    let d : ℕ := 2
    let κ : ℝ := 2
    let O : Matrix.orthogonalGroup (Fin d) ℝ := 1
    let θ : Fin d → ℝ := fun i => ((i.val : ℝ) + 1 / 2) * Real.pi / (d : ℝ)
    let A : Matrix (Fin d) (Fin d) ℝ :=
      (O : Matrix (Fin d) (Fin d) ℝ) *
        Matrix.diagonal (fun i => (κ + 1) / 2 + (κ - 1) / 2 * Real.cos (θ i)) *
        (O : Matrix (Fin d) (Fin d) ℝ).transpose
    let f : EuclideanSpace ℝ (Fin d) → ℝ := fun x =>
      (WithLp.ofLp x) ⬝ᵥ (A *ᵥ WithLp.ofLp x) / 2
    let query : EuclideanSpace ℝ (Fin d) → EuclideanSpace ℝ (Fin d) :=
      fun x => WithLp.toLp 2 (A *ᵥ WithLp.ofLp x)
    ∀ x : EuclideanSpace ℝ (Fin d),
      HasGradientAt f (query x) x ∧
      (f x, gradient f x) = (inner ℝ x (query x) / 2, query x) := by
  exact AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumFirstOrder.actual_first_order_query
    (d := 2) (by decide) (κ := 2) (by norm_num) (1 : Matrix.orthogonalGroup (Fin 2) ℝ)

run_cmd do
  let producer := `AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumFirstOrder.actual_first_order_query
  let admissibility := `AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumAdmissibility.actual_precision_admissible
  let affine := `AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumAffine.actual_affine_precision_query
  let consumer := Name.mkSimple "_private.Tests.GaussianComplexityFixedSpectrumFirstOrder.0.actual_reference_precision_first_order_consumer"
  for (target, expected) in [(producer, #[admissibility]), (consumer, #[producer, affine])] do
    let info ← getConstInfo target
    let some value := info.value? true | throwError "No actual proof value: {target}"
    let direct := value.getUsedConstants.filter (fun n => n.toString.startsWith "AutoSamplingTheory.")
    logInfo m!"REVIEW_DIRECT_ASTIS_PARENTS {target}: {direct}"
    unless direct.size == expected.size && expected.all direct.contains do
      throwError "Unexpected direct actual ASTIS parents for {target}"
    let axioms ← Lean.collectAxioms target
    logInfo m!"REVIEW_AXIOMS {target}: {axioms}"
    unless axioms.size == 3 && #[`propext, `Classical.choice, `Quot.sound].all axioms.contains do
      throwError "Nonstandard or missing axiom accounting for {target}"
    logInfo m!"REVIEW_KERNEL_TYPE {target}: {info.type}"
  for target in [admissibility, affine] do
    let axioms ← Lean.collectAxioms target
    logInfo m!"REVIEW_ANCESTOR_AXIOMS {target}: {axioms}"
    unless axioms.size == 3 && #[`propext, `Classical.choice, `Quot.sound].all axioms.contains do
      throwError "Unexpected ancestor axioms {target}"
  logInfo "REVIEW_REFLECTION_ASSERTIONS_PASSED"

#print axioms sourceReviewerAnonymousApplication
#print axioms sourceReviewerDeterminantMinusOneApplication
#print axioms sourceReviewerDeterminantPlusOneApplication
