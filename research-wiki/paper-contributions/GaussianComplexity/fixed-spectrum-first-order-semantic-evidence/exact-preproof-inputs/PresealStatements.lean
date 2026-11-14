import Mathlib.LinearAlgebra.UnitaryGroup
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Basic
import Mathlib.Analysis.Calculus.Gradient.Basic
import Mathlib.Analysis.InnerProductSpace.PiL2

open Matrix InnerProductSpace
set_option autoImplicit false

/- Meaning-only proposition definitions. No claim below is proved. -/
namespace GaussianComplexityFixedSpectrumFirstOrderPreseal

noncomputable def ProducerStatement : Prop :=
  ∀ {d : ℕ}, 2 ≤ d → ∀ {κ : ℝ}, 2 ≤ κ →
    ∀ O : Matrix.orthogonalGroup (Fin d) ℝ,
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

noncomputable def ActualAffineFirstOrderConsumerStatement : Prop :=
  ∀ {d : ℕ}, 2 ≤ d → ∀ {κ : ℝ}, 2 ≤ κ →
    ∀ O : Matrix.orthogonalGroup (Fin d) ℝ,
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
      (f x, gradient f x) = (inner ℝ x (reconstructed x) / 2, reconstructed x)

#check ProducerStatement
#check ActualAffineFirstOrderConsumerStatement
#print ProducerStatement
#print ActualAffineFirstOrderConsumerStatement
end GaussianComplexityFixedSpectrumFirstOrderPreseal
