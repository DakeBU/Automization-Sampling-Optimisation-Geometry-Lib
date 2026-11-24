import GC47Rank

/-! Boundary checks for the hypotheses on the cosine-grid Krylov formula. -/
noncomputable section
open Matrix
open AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumRotation
namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumKrylov

/-- With zero queries the unique start is the only generator for every spectrum. -/
theorem krylov_zero_query (d : ℕ) (κ : ℝ) (g : Starts d 0) :
    krylov d 0 κ g = Submodule.span ℝ {WithLp.ofLp (g 0)} := by
  unfold krylov
  congr 1
  ext x
  constructor
  · rintro ⟨⟨a,j⟩,rfl⟩
    have ha : a = 0 := Fin.ext (by omega)
    have hj : j = 0 := Fin.ext (by omega)
    rw [ha,hj]
    simp
  · intro h
    refine ⟨(0,0),?_⟩
    simpa using h.symm

/-- Scalar precision prevents the claimed full dimension at d=4, q=1 for every choice of starts. -/
theorem unit_condition_strict (g : Starts 4 1) :
    Module.finrank ℝ (krylov 4 1 1 g) < min 4 ((1+1)^2) := by
  rw [krylov_one]
  have h := finrank_range_le_card (R := ℝ) (fun a => WithLp.ofLp (g a))
  exact lt_of_le_of_lt h (by decide : Fintype.card (Fin (1+1)) < min 4 ((1+1)^2))

/-- The minor size and true dimension both vanish in the empty coordinate space. -/
example (q : ℕ) (κ : ℝ) (g : Starts 0 q) : Module.finrank ℝ (krylov 0 q κ g) = 0 := by
  simpa using finrank_krylov_le 0 q κ g

end AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumKrylov
