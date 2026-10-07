Admissibility is deliberately separate because the Bochner integral is
totalized outside its integrable domain. -/
noncomputable def variance (μ : Measure E) (f : E → ℝ) : ℝ :=
  ∫ x, (f x - ∫ y, f y ∂μ) ^ 2 ∂μ

/-- The Euclidean/inner-product Dirichlet energy of a test function. -/
noncomputable def dirichletEnergy (μ : Measure E) (f : E → ℝ) : ℝ :=
  ∫ x, ‖gradient f x‖ ^ 2 ∂μ

/-- Exact integrability domain used by the local Poincare interface. -/
def Admissible (μ : Measure E) (f : E → ℝ) : Prop :=
  Integrable f μ ∧
    Integrable (fun x => (f x - ∫ y, f y ∂μ) ^ 2) μ ∧
    Integrable (fun x => ‖gradient f x‖ ^ 2) μ

/-- A measure satisfies the Poincare inequality with constant `C` on an
explicit test class.

The convention is `Var_μ(f) ≤ C * E_μ(f)`.  Probability normalization is
part of the contract rather than an implicit convention. -/
def Satisfies (μ : Measure E) (tests : Set (E → ℝ)) (C : ℝ) : Prop :=
  IsProbabilityMeasure μ ∧ 0 ≤ C ∧
    ∀ f ∈ tests, Admissible μ f → variance μ f ≤ C * dirichletEnergy μ f
