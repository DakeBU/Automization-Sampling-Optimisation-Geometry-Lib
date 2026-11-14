import AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumFirstOrder
import AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumAffine

open Matrix InnerProductSpace
set_option autoImplicit false

/- The existing SAME-O reference2 precision reply now reconstructs the actual
kappa potential/gradient. Neither a derivative nor an affine identity is an input.
This is pointwise source mathematics, not an operational query-budget theorem. -/
private theorem actual_reference_precision_first_order_consumer {d : ℕ} (hd : 2 ≤ d)
    {κ : ℝ} (hκ : 2 ≤ κ)
    (O : Matrix.orthogonalGroup (Fin d) ℝ) :
    let θ : Fin d → ℝ := fun i => ((i.val : ℝ) + 1 / 2) * Real.pi / (d : ℝ)
    let A : ℝ → Matrix (Fin d) (Fin d) ℝ := fun η =>
      (O : Matrix (Fin d) (Fin d) ℝ) *
        Matrix.diagonal (fun i => (η + 1) / 2 + (η - 1) / 2 * Real.cos (θ i)) *
        (O : Matrix (Fin d) (Fin d) ℝ).transpose
    let f : EuclideanSpace ℝ (Fin d) → ℝ := fun x =>
      (WithLp.ofLp x) ⬝ᵥ (A κ *ᵥ WithLp.ofLp x) / 2
    let referenceQuery : EuclideanSpace ℝ (Fin d) → EuclideanSpace ℝ (Fin d) :=
      fun x => WithLp.toLp 2 (A 2 *ᵥ WithLp.ofLp x)
    let reconstructed : EuclideanSpace ℝ (Fin d) → EuclideanSpace ℝ (Fin d) :=
      fun x => (κ - 1) • referenceQuery x - (κ - 2) • x
    ∀ x : EuclideanSpace ℝ (Fin d),
      HasGradientAt f (reconstructed x) x ∧
      (f x, gradient f x) = (inner ℝ x (reconstructed x) / 2, reconstructed x) := by
  classical
  dsimp only
  let θ : Fin d → ℝ := fun i => ((i.val : ℝ) + 1 / 2) * Real.pi / (d : ℝ)
  let A : ℝ → Matrix (Fin d) (Fin d) ℝ := fun η =>
    (O : Matrix (Fin d) (Fin d) ℝ) *
      Matrix.diagonal (fun i => (η + 1) / 2 + (η - 1) / 2 * Real.cos (θ i)) *
      (O : Matrix (Fin d) (Fin d) ℝ).transpose
  let f : EuclideanSpace ℝ (Fin d) → ℝ := fun x =>
    (WithLp.ofLp x) ⬝ᵥ (A κ *ᵥ WithLp.ofLp x) / 2
  let referenceQuery : EuclideanSpace ℝ (Fin d) → EuclideanSpace ℝ (Fin d) :=
    fun x => WithLp.toLp 2 (A 2 *ᵥ WithLp.ofLp x)
  let reconstructed : EuclideanSpace ℝ (Fin d) → EuclideanSpace ℝ (Fin d) :=
    fun x => (κ - 1) • referenceQuery x - (κ - 2) • x
  intro x
  have hforward : WithLp.toLp 2 (A κ *ᵥ WithLp.ofLp x) = reconstructed x :=
    (AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumAffine.actual_affine_precision_query
      hd hκ O x).1
  have hfirst : HasGradientAt f (WithLp.toLp 2 (A κ *ᵥ WithLp.ofLp x)) x ∧
      (f x, gradient f x) =
        (inner ℝ x (WithLp.toLp 2 (A κ *ᵥ WithLp.ofLp x)) / 2,
          WithLp.toLp 2 (A κ *ᵥ WithLp.ofLp x)) :=
    AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumFirstOrder.actual_first_order_query
      hd hκ O x
  simpa only [hforward] using hfirst

#print axioms AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumFirstOrder.actual_first_order_query
#print axioms actual_reference_precision_first_order_consumer
