import AutoSamplingTheory.ExampleCases.DiscreteSampling.OrderedHeatBath

open MeasureTheory ProbabilityTheory
open scoped ENNReal ProbabilityTheory

-- The actual ordered kernel and both conditional laws are fixed by the
-- executable statement, not supplied as proof premises.
example :
    let π : Measure (Bool × Bool) :=
      (3 / 8 : ℝ≥0∞) • Measure.dirac (false, false) +
      (1 / 8 : ℝ≥0∞) • Measure.dirac (false, true) +
      (1 / 8 : ℝ≥0∞) • Measure.dirac (true, false) +
      (3 / 8 : ℝ≥0∞) • Measure.dirac (true, true)
    let P : Kernel (Bool × Bool) (Bool × Bool) :=
      Kernel.ofFunOfCountable fun x =>
        (3 / 4 : ℝ≥0∞) • Measure.dirac (x.2, x.2) +
        (1 / 4 : ℝ≥0∞) • Measure.dirac (!x.2, x.2)
    let Q : Kernel (Bool × Bool) (Bool × Bool) :=
      Kernel.ofFunOfCountable fun x =>
        (3 / 4 : ℝ≥0∞) • Measure.dirac (x.1, x.1) +
        (1 / 4 : ℝ≥0∞) • Measure.dirac (x.1, !x.1)
    IsProbabilityMeasure π ∧
    (∀ x : Bool × Bool, 0 < π {x}) ∧
    IsMarkovKernel P ∧ IsMarkovKernel Q ∧
    (∀ b : Bool, π {z | z.2 = b} = 1 / 2 ∧ π {z | z.1 = b} = 1 / 2) ∧
    (∀ x y : Bool × Bool, P x {y} = if y.2 = x.2 then 2 * π {y} else 0) ∧
    (∀ x y : Bool × Bool, Q x {y} = if y.1 = x.1 then 2 * π {y} else 0) ∧
    Kernel.IsReversible P π ∧ Kernel.IsReversible Q π ∧
    (Q ∘ₖ P).Invariant π ∧
    ¬ Kernel.IsReversible (Q ∘ₖ P) π :=
  AutoSamplingTheory.ExampleCases.DiscreteSampling.OrderedHeatBath.ordered_heat_bath_invariant_not_reversible

#print axioms AutoSamplingTheory.ExampleCases.DiscreteSampling.OrderedHeatBath.ordered_heat_bath_invariant_not_reversible
