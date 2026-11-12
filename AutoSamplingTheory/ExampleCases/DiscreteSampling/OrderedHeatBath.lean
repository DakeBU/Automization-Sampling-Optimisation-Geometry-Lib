import AutoSamplingTheory.TechnicalLemmas.Probability.KernelReversibility
import Mathlib.Probability.Kernel.Composition.MeasureComp
import Mathlib.Tactic.NormNum

/-!
# An ordered two-bit heat bath need not be reversible

An original full-support counterexample to preservation of reversibility by
composition. The first step refreshes the first bit, the second refreshes the
second using the updated first bit. Each step is exactly a conditional Gibbs
update for the same probability. One Markov time unit here is a full sweep.

Background: Chen–Štefankovič–Vigoda, arXiv:2307.13826v4 §1.3, and He–De Sa–
Mitliagkas–Ré, arXiv:1606.03432v1 §5. Neither source is claimed to state this
particular example or any conclusion about its mixing time.
-/

noncomputable section

namespace AutoSamplingTheory.ExampleCases.DiscreteSampling.OrderedHeatBath

open MeasureTheory ProbabilityTheory
open scoped ENNReal ProbabilityTheory

private abbrev State := Bool × Bool

private def target : Measure State :=
  (3 / 8 : ℝ≥0∞) • Measure.dirac (false, false) +
  (1 / 8 : ℝ≥0∞) • Measure.dirac (false, true) +
  (1 / 8 : ℝ≥0∞) • Measure.dirac (true, false) +
  (3 / 8 : ℝ≥0∞) • Measure.dirac (true, true)

private def refreshFirst : Kernel State State :=
  Kernel.ofFunOfCountable fun x =>
    (3 / 4 : ℝ≥0∞) • Measure.dirac (x.2, x.2) +
    (1 / 4 : ℝ≥0∞) • Measure.dirac (!x.2, x.2)

private def refreshSecond : Kernel State State :=
  Kernel.ofFunOfCountable fun x =>
    (3 / 4 : ℝ≥0∞) • Measure.dirac (x.1, x.1) +
    (1 / 4 : ℝ≥0∞) • Measure.dirac (x.1, !x.1)

open AutoSamplingTheory.TechnicalLemmas.Probability.KernelReversibility

local macro "finite_ennreal_rat" : tactic =>
  `(tactic|
    (simp (disch := norm_num) only [← ENNReal.ofReal_ofNat, ← ENNReal.ofReal_one,
      ← ENNReal.ofReal_div_of_pos, ← ENNReal.ofReal_inv_of_pos,
      ← ENNReal.ofReal_add, ← ENNReal.ofReal_mul,
      ENNReal.ofReal_pos, ENNReal.ofReal_lt_ofReal_iff_of_nonneg] <;> norm_num))

private theorem target_mass (x : State) :
    target {x} = if x.1 = x.2 then (3 / 8 : ℝ≥0∞) else 1 / 8 := by
  rcases x with ⟨a, b⟩
  cases a <;> cases b <;>
    simp [target, Measure.add_apply, Measure.smul_apply, smul_eq_mul]

private theorem target_probability : IsProbabilityMeasure target := by
  constructor
  simp [target, Measure.add_apply, Measure.smul_apply, smul_eq_mul]
  finite_ennreal_rat

private theorem target_fibers (b : Bool) :
    target {z | z.2 = b} = 1 / 2 ∧ target {z | z.1 = b} = 1 / 2 := by
  cases b <;> constructor <;>
    simp [target, Measure.add_apply, Measure.smul_apply, smul_eq_mul] <;>
    finite_ennreal_rat

private theorem first_markov : IsMarkovKernel refreshFirst := by
  constructor
  intro x
  constructor
  simp [refreshFirst, Kernel.ofFunOfCountable, Measure.add_apply, Measure.smul_apply, smul_eq_mul]
  finite_ennreal_rat

private theorem second_markov : IsMarkovKernel refreshSecond := by
  constructor
  intro x
  constructor
  simp [refreshSecond, Kernel.ofFunOfCountable, Measure.add_apply, Measure.smul_apply, smul_eq_mul]
  finite_ennreal_rat

private theorem first_conditional (x y : State) :
    refreshFirst x {y} = if y.2 = x.2 then 2 * target {y} else 0 := by
  have hSame : (3 / 4 : ℝ≥0∞) = 2 * (3 / 8) := by finite_ennreal_rat
  have hDiff : (1 / 4 : ℝ≥0∞) = 2 * (1 / 8) := by finite_ennreal_rat
  rcases x with ⟨a,b⟩
  rcases y with ⟨c,d⟩
  cases a <;> cases b <;> cases c <;> cases d <;>
    simp [refreshFirst, Kernel.ofFunOfCountable, Measure.add_apply, Measure.smul_apply,
      smul_eq_mul, target_mass, hSame, hDiff]

private theorem second_conditional (x y : State) :
    refreshSecond x {y} = if y.1 = x.1 then 2 * target {y} else 0 := by
  have hSame : (3 / 4 : ℝ≥0∞) = 2 * (3 / 8) := by finite_ennreal_rat
  have hDiff : (1 / 4 : ℝ≥0∞) = 2 * (1 / 8) := by finite_ennreal_rat
  rcases x with ⟨a,b⟩
  rcases y with ⟨c,d⟩
  cases a <;> cases b <;> cases c <;> cases d <;>
    simp [refreshSecond, Kernel.ofFunOfCountable, Measure.add_apply, Measure.smul_apply,
      smul_eq_mul, target_mass, hSame, hDiff]

private theorem reversible_of_fiber (K : Kernel State State) (retain : State → Bool)
    (h : ∀ x y : State, K x {y} = if retain y = retain x then 2 * target {y} else 0) :
    K.IsReversible target := by
  apply isReversible_of_singleton_balance
  intro x y
  rw [h x y, h y x]
  by_cases hxy : retain y = retain x
  · rw [if_pos hxy, if_pos hxy.symm]
    ac_rfl
  · rw [if_neg hxy, if_neg (Ne.symm hxy), mul_zero, mul_zero]

private theorem sweep_singleton (x y : State) :
    (refreshSecond ∘ₖ refreshFirst) x {y} =
      (3 / 4 : ℝ≥0∞) * refreshSecond (x.2, x.2) {y} +
        (1 / 4 : ℝ≥0∞) * refreshSecond (!x.2, x.2) {y} := by
  rw [Kernel.comp_apply' _ _ _ (measurableSet_singleton y)]
  change (∫⁻ z : State, refreshSecond z {y} ∂
    ((3 / 4 : ℝ≥0∞) • Measure.dirac (x.2, x.2) +
      (1 / 4 : ℝ≥0∞) • Measure.dirac (!x.2, x.2))) = _
  simp only [lintegral_add_measure, lintegral_smul_measure, lintegral_dirac, smul_eq_mul]

private theorem sweep_fluxes :
    target {(false, false)} * (refreshSecond ∘ₖ refreshFirst) (false, false) {(false, true)} =
      (9 / 128 : ℝ≥0∞) ∧
    target {(false, true)} * (refreshSecond ∘ₖ refreshFirst) (false, true) {(false, false)} =
      (3 / 128 : ℝ≥0∞) := by
  have hSame : (2 : ℝ≥0∞) * (3 / 8) = 3 / 4 := by finite_ennreal_rat
  constructor <;>
    simp [sweep_singleton, second_conditional, target_mass, hSame] <;>
    finite_ennreal_rat

/-- A genuine ordered heat-bath sweep preserves a full-support target but
is not reversible, even though both coordinate kernels are reversible. -/
theorem ordered_heat_bath_invariant_not_reversible :
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
    ¬ Kernel.IsReversible (Q ∘ₖ P) π := by
  change
    IsProbabilityMeasure target ∧
    (∀ x : State, 0 < target {x}) ∧
    IsMarkovKernel refreshFirst ∧ IsMarkovKernel refreshSecond ∧
    (∀ b : Bool, target {z | z.2 = b} = 1 / 2 ∧ target {z | z.1 = b} = 1 / 2) ∧
    (∀ x y : State, refreshFirst x {y} = if y.2 = x.2 then 2 * target {y} else 0) ∧
    (∀ x y : State, refreshSecond x {y} = if y.1 = x.1 then 2 * target {y} else 0) ∧
    Kernel.IsReversible refreshFirst target ∧ Kernel.IsReversible refreshSecond target ∧
    (refreshSecond ∘ₖ refreshFirst).Invariant target ∧
    ¬ Kernel.IsReversible (refreshSecond ∘ₖ refreshFirst) target
  have hfirst : refreshFirst.IsReversible target :=
    reversible_of_fiber refreshFirst Prod.snd first_conditional
  have hsecond : refreshSecond.IsReversible target :=
    reversible_of_fiber refreshSecond Prod.fst second_conditional
  have hinvFirst := @Kernel.IsReversible.invariant _ _ _ first_markov _ hfirst
  have hinvSecond := @Kernel.IsReversible.invariant _ _ _ second_markov _ hsecond
  refine ⟨target_probability, ?_, first_markov, second_markov,
    target_fibers, first_conditional, second_conditional, hfirst, hsecond,
    hinvSecond.comp hinvFirst, ?_⟩
  · intro x
    rw [target_mass]
    split <;> finite_ennreal_rat
  · intro hr
    have h := hr (measurableSet_singleton ((false, false) : State))
      (measurableSet_singleton ((false, true) : State))
    simp only [Measure.restrict_singleton, lintegral_smul_measure, lintegral_dirac,
      smul_eq_mul] at h
    rw [sweep_fluxes.1, sweep_fluxes.2] at h
    have hlt : (3 / 128 : ℝ≥0∞) < 9 / 128 := by finite_ennreal_rat
    exact hlt.ne h.symm

end AutoSamplingTheory.ExampleCases.DiscreteSampling.OrderedHeatBath
