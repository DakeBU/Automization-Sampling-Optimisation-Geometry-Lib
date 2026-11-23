import GC31Mixture
import GC31ZeroQuery
import GC31Budget

/-!
# Gaussian sampling query lower bound

Zhou–Suzuki, *On Complexity of Gaussian Sampling*, equations (2) and (3).
Each feasible budget is a deterministic cap, with accuracy measured on the
seed-averaged output separately for every admissible input precision. The
query complexity is the infimum of the feasible natural caps in the extended
nonnegative reals. Seed and state types may have arbitrary measurable spaces.
-/

open MeasureTheory
open scoped ENNReal

namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.FirstOrderIndistinguishability

universe u v

/-- A feasible natural query cap in the infimum of equation (2). -/
def FeasibleBudget (d : ℕ) (κ ε : ℝ) (T : ℕ) : Prop :=
  ∃ (Seed : Type u) (State : Type v) (_ : MeasurableSpace Seed) (_ : MeasurableSpace State)
    (ρ : Measure Seed) (_ : IsProbabilityMeasure ρ) (alg : Algorithm d Seed State),
    ∀ A, Admissible κ A → eventTV (alg.outputLaw ρ T A) (targetLaw A) ≤ ε

/-- The infimum ranges over natural budgets for algorithms uniformly accurate on
the entire precision class, with the usual extended-real convention for an empty set. -/
noncomputable def gaussianQueryComplexity (d : ℕ) (κ ε : ℝ) : ℝ≥0∞ :=
  ⨅ t : {T : ℕ // FeasibleBudget.{u,v} d κ ε T}, (t.val : ℝ≥0∞)

/-- Equation (3) for each individual randomized first-order algorithm. -/
theorem algorithm_query_lower_bound {d T : ℕ} {κ ε : ℝ}
    (hd : 1 ≤ d) (hκ : 4 ≤ κ) (hε : 0 < ε) (hsmall : ε ≤ 1/16)
    {Seed State : Type*} [MeasurableSpace Seed] [MeasurableSpace State]
    (ρ : Measure Seed) [IsProbabilityMeasure ρ] (alg : Algorithm d Seed State)
    (hacc : ∀ A, Admissible κ A → eventTV (alg.outputLaw ρ T A) (targetLaw A) ≤ ε) :
    (1/256 : ℝ) * min (d : ℝ) (Real.sqrt κ * Real.log (1 + (d : ℝ)/(Real.sqrt κ * ε))) ≤
      (T : ℝ) := by
  have hT := positive_budget_of_accuracy hd hκ hsmall ρ alg hacc
  apply query_budget_of_separation hT hκ hε hsmall
  intro hfit
  have hn : 3 ≤ 2*T+1 := by omega
  exact (averaged_target_separation hn hfit hκ).trans
    (target_separation_le_twice_accuracy hn hfit hκ (by omega) ρ alg hacc)

/-- Theorem 3.1, equation (3), for the query complexity of equation (2). -/
theorem gaussian_query_complexity_lower_bound {d : ℕ} {κ ε : ℝ}
    (hd : 1 ≤ d) (hκ : 4 ≤ κ) (hε : 0 < ε) (hsmall : ε ≤ 1/16) :
    ENNReal.ofReal ((1/256 : ℝ) * min (d : ℝ)
      (Real.sqrt κ * Real.log (1 + (d : ℝ)/(Real.sqrt κ * ε)))) ≤
      gaussianQueryComplexity.{u,v} d κ ε := by
  apply le_iInf
  intro t
  obtain ⟨Seed, State, mSeed, mState, ρ, hp, alg, hacc⟩ := t.property
  exact ENNReal.ofReal_le_natCast.mpr (algorithm_query_lower_bound hd hκ hε hsmall ρ alg hacc)

#print axioms algorithm_query_lower_bound
#print axioms gaussian_query_complexity_lower_bound

end AutoSamplingTheory.ExampleCases.GaussianComplexity.FirstOrderIndistinguishability
