import AutoSamplingTheory.ExampleCases.SlcLsiQueryComplexity.EnergyTruncation

open MeasureTheory ProbabilityTheory
open scoped NNReal
open AutoSamplingTheory.ExampleCases.SlcLsiQueryComplexity.EnergyTruncation

-- Exact arbitrary-space interface: no supplied oddness or integrability.
example {Ω : Type*} [MeasurableSpace Ω] (P : Measure Ω) (n : ℕ+)
    (β lam : {r : ℝ // 0 < r}) {Y : Ω → ℝ} (v : ℝ≥0)
    (hY : HasLaw Y (gaussianReal 0 v) P) {a : ℝ} (ha : a ∈ Set.Icc (0 : ℝ) 1) :
    Integrable (fun ω ↦ Real.exp (-a * energyTruncation n β lam (Y ω))) P ∧
      (∫ ω, Real.exp (-a * energyTruncation n β lam (Y ω)) ∂P) ≤
        Real.exp ((β : ℝ) ^ 2 * variance Y P / 2) :=
  energyTruncation_gaussian_bound P n β lam v hY ha

-- Gate one, concrete positive parameters, and every variance (including zero).
example (v : ℝ≥0) :
    Integrable (fun y ↦ Real.exp (-energyTruncation 1 ⟨2, by norm_num⟩ ⟨1, by norm_num⟩ y))
        (gaussianReal 0 v) ∧
      (∫ y, Real.exp (-energyTruncation 1 ⟨2, by norm_num⟩ ⟨1, by norm_num⟩ y)
        ∂gaussianReal 0 v) ≤ Real.exp (4 * (v : ℝ) / 2) := by
  have hY : HasLaw (fun y : ℝ ↦ y) (gaussianReal 0 v) (gaussianReal 0 v) :=
    ⟨aemeasurable_id, by simp⟩
  simpa [show (2 : ℝ) ^ 2 = 4 by norm_num] using energyTruncation_gaussian_bound (gaussianReal 0 v) 1
    ⟨2, by norm_num⟩ ⟨1, by norm_num⟩ v hY (a := 1) (by norm_num)

-- Degenerate law and gate zero on an arbitrary measurable probability space.
example {Ω : Type*} [MeasurableSpace Ω] (P : Measure Ω) {Y : Ω → ℝ}
    (hY : HasLaw Y (gaussianReal 0 0) P) (n : ℕ+) (β lam : {r : ℝ // 0 < r}) :
    Integrable (fun ω ↦ Real.exp (-0 * energyTruncation n β lam (Y ω))) P ∧
      (∫ ω, Real.exp (-0 * energyTruncation n β lam (Y ω)) ∂P) ≤
        Real.exp ((β : ℝ) ^ 2 * variance Y P / 2) :=
  energyTruncation_gaussian_bound P n β lam 0 hY (by norm_num)

#print axioms energyTruncation_gaussian_bound
#check @energyTruncation
#check @energyTruncation_gaussian_bound
