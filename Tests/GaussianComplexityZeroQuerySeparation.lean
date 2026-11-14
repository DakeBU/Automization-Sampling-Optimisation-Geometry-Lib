import AutoSamplingTheory.ExampleCases.GaussianComplexity.ZeroQuerySeparation
import Mathlib.MeasureTheory.Measure.ProbabilityMeasure

open Matrix MeasureTheory ProbabilityTheory Set
set_option autoImplicit false

/-!
Actual arbitrary-common-output probability-law consumer of the Gaussian event
gap. The real event-supremum TV is bounded internally from probability masses;
the new producer is genuinely used in the endpoint contradiction. An actual
Borel zero-query algorithm/seed/deterministic-cap adapter remains separate.
-/
namespace AutoSamplingTheory.Tests.GaussianComplexityZeroQuerySeparation

private theorem no_common_zero_query_output {d : ℕ} (hd : 1 ≤ d)
    {κ : ℝ} (hκ : 4 ≤ κ) (ρ : ProbabilityMeasure (EuclideanSpace ℝ (Fin d))) :
  let A₁ : Matrix (Fin d) (Fin d) ℝ :=
    Matrix.diagonal (fun i => if i.val = 0 then κ else 1)
  let ν₀ : Measure (EuclideanSpace ℝ (Fin d)) :=
    multivariateGaussian (0 : EuclideanSpace ℝ (Fin d))
      (1 : Matrix (Fin d) (Fin d) ℝ)⁻¹
  let ν₁ : Measure (EuclideanSpace ℝ (Fin d)) :=
    multivariateGaussian (0 : EuclideanSpace ℝ (Fin d)) A₁⁻¹
  let Δ : Measure (EuclideanSpace ℝ (Fin d)) →
      Measure (EuclideanSpace ℝ (Fin d)) → ℝ := fun μ ν =>
    sSup {z : ℝ | ∃ B : Set (EuclideanSpace ℝ (Fin d)),
      MeasurableSet B ∧ z = |μ.real B - ν.real B|}
  ¬ (Δ (ρ : Measure (EuclideanSpace ℝ (Fin d))) ν₀ ≤ (1 : ℝ) / 16 ∧
    Δ (ρ : Measure (EuclideanSpace ℝ (Fin d))) ν₁ ≤ (1 : ℝ) / 16)
:= by
  classical
  dsimp only
  let E := EuclideanSpace ℝ (Fin d)
  let A₁ : Matrix (Fin d) (Fin d) ℝ :=
    Matrix.diagonal (fun i => if i.val = 0 then κ else 1)
  let ν₀ : Measure E := multivariateGaussian (0 : E) (1 : Matrix (Fin d) (Fin d) ℝ)⁻¹
  let ν₁ : Measure E := multivariateGaussian (0 : E) A₁⁻¹
  let B : Set E := {x | |WithLp.ofLp x (⟨0, hd⟩ : Fin d)| ≤ (1 : ℝ) / 2}
  let Δ : Measure E → Measure E → ℝ := fun μ ν =>
    sSup {z : ℝ | ∃ C : Set E, MeasurableSet C ∧ z = |μ.real C - ν.real C|}
  have hgap : (1 : ℝ) / 8 < ν₁.real B - ν₀.real B :=
    AutoSamplingTheory.ExampleCases.GaussianComplexity.ZeroQuerySeparation.actual_zero_query_gaussian_event_gap hd hκ
  have hB : MeasurableSet B := by
    change MeasurableSet {x : EuclideanSpace ℝ (Fin d) |
      |x (⟨0, hd⟩ : Fin d)| ≤ (1 : ℝ) / 2}
    exact measurableSet_le (by fun_prop) measurable_const
  have hbounded (μ ν : Measure E) [IsProbabilityMeasure μ] [IsProbabilityMeasure ν] :
      BddAbove {z : ℝ | ∃ C : Set E, MeasurableSet C ∧ z = |μ.real C - ν.real C|} := by
    refine ⟨1, ?_⟩
    rintro z ⟨C, _, rfl⟩
    have hμ0 : 0 ≤ μ.real C := measureReal_nonneg
    have hν0 : 0 ≤ ν.real C := measureReal_nonneg
    have hμ1 : μ.real C ≤ 1 := measureReal_le_one
    have hν1 : ν.real C ≤ 1 := measureReal_le_one
    exact abs_le.mpr ⟨by linarith, by linarith⟩
  have hsup₀ : |(ρ : Measure E).real B - ν₀.real B| ≤ Δ (ρ : Measure E) ν₀ :=
    le_csSup (hbounded _ _) ⟨B, hB, rfl⟩
  have hsup₁ : |(ρ : Measure E).real B - ν₁.real B| ≤ Δ (ρ : Measure E) ν₁ :=
    le_csSup (hbounded _ _) ⟨B, hB, rfl⟩
  change ¬ (Δ (ρ : Measure E) ν₀ ≤ (1 : ℝ) / 16 ∧
    Δ (ρ : Measure E) ν₁ ≤ (1 : ℝ) / 16)
  intro h
  have h₀ := (abs_le.mp (hsup₀.trans h.1)).2
  have h₁ := (abs_le.mp (hsup₁.trans h.2)).1
  linarith

end AutoSamplingTheory.Tests.GaussianComplexityZeroQuerySeparation
