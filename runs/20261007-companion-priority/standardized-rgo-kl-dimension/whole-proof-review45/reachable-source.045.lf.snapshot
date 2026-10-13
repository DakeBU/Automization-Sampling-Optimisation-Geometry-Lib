import AutoSamplingTheory.TechnicalLemmas.Measure.Transport
import Mathlib.Analysis.SpecialFunctions.Pow.NNReal
import Mathlib.MeasureTheory.Measure.Haar.InnerProductSpace
import Mathlib.MeasureTheory.Integral.Bochner.Basic

/-!
# Measure classes for Wasserstein space

This module begins the measure-theoretic layer of Chewi's Wasserstein-space
development.  It isolates Definition 1.3.12 from optimal-plan existence,
metric-space structure, and Otto calculus.
-/

namespace AutoSamplingTheory
namespace TechnicalLemmas
namespace Measure
namespace WassersteinSpace

open MeasureTheory
open scoped ENNReal

/-- Squared Euclidean transport cost as an extended nonnegative function. -/
def quadraticCost
    {E : Type*} [NormedAddCommGroup E] : E × E → ℝ≥0∞ :=
  fun z => ENNReal.ofReal (‖z.1 - z.2‖ ^ 2)

/-- Chewi Definition 1.3.4: the 2-Wasserstein distance is the positive
square root of the quadratic Kantorovich transport cost. -/
noncomputable def wassersteinDistance
    {E : Type*} [NormedAddCommGroup E] [MeasurableSpace E]
    (μ ν : Measure E) : ℝ≥0∞ :=
  (Transport.transportCost (quadraticCost (E := E)) μ ν) ^ (1 / 2 : ℝ)

/-- Chewi display (1.3.5): the square of `W₂` is the infimum of the
quadratic costs over all couplings. -/
theorem wassersteinDistance_sq
    {E : Type*} [NormedAddCommGroup E] [MeasurableSpace E]
    (μ ν : Measure E) :
    wassersteinDistance μ ν ^ 2 =
      Transport.transportCost (quadraticCost (E := E)) μ ν := by
  rw [wassersteinDistance, ← ENNReal.rpow_two, ← ENNReal.rpow_mul]
  norm_num

/-- Every concrete coupling bounds the squared Wasserstein distance from
above by its quadratic transport cost.

This is the source-facing bridge used before proving optimal-plan existence or
constant-speed displacement geodesics. -/
theorem wassersteinDistance_sq_le_lintegral_of_isCoupling
    {E : Type*} [NormedAddCommGroup E] [MeasurableSpace E]
    (μ ν : Measure E) (γ : Measure (E × E))
    (hγ : Transport.IsCoupling γ μ ν) :
    wassersteinDistance μ ν ^ 2 ≤
      ∫⁻ z, quadraticCost (E := E) z ∂γ := by
  rw [wassersteinDistance_sq]
  exact Transport.transportCost_le_lintegral_of_isCoupling
    (quadraticCost (E := E)) μ ν γ hγ

/-- Every concrete coupling also bounds the Wasserstein distance directly by
the square root of its quadratic cost. -/
theorem wassersteinDistance_le_sqrt_lintegral_of_isCoupling
    {E : Type*} [NormedAddCommGroup E] [MeasurableSpace E]
    (μ ν : Measure E) (γ : Measure (E × E))
    (hγ : Transport.IsCoupling γ μ ν) :
    wassersteinDistance μ ν ≤
      (∫⁻ z, quadraticCost (E := E) z ∂γ) ^ (1 / (2 : ℝ)) := by
  unfold wassersteinDistance
  exact ENNReal.rpow_le_rpow
    (Transport.transportCost_le_lintegral_of_isCoupling
      (quadraticCost (E := E)) μ ν γ hγ)
    (by norm_num)

/-- Strictly above the Wasserstein distance, one can choose an actual coupling
whose quadratic `L²` cost has square root below the same threshold.

This is the distance-level form of `Transport`'s strict `sInf` selection
lemma.  No optimal coupling existence is asserted. -/
theorem exists_isCoupling_sqrt_lintegral_lt_of_wassersteinDistance_lt
    {E : Type*} [NormedAddCommGroup E] [MeasurableSpace E]
    (μ ν : Measure E) {r : ℝ≥0∞}
    (h : wassersteinDistance μ ν < r) :
    ∃ γ : Measure (E × E),
      Transport.IsCoupling γ μ ν ∧
        (∫⁻ z, quadraticCost (E := E) z ∂γ) ^ (1 / (2 : ℝ)) < r := by
  let C : ℝ≥0∞ :=
    Transport.transportCost (quadraticCost (E := E)) μ ν
  have hsqrt_sq : (C ^ (1 / (2 : ℝ))) ^ (2 : ℝ) = C := by
    rw [← ENNReal.rpow_mul]
    norm_num
  have hcost : C < r ^ (2 : ℝ) := by
    have hsquare := ENNReal.rpow_lt_rpow h (z := (2 : ℝ)) (by norm_num)
    change (C ^ (1 / (2 : ℝ))) ^ (2 : ℝ) < r ^ (2 : ℝ) at hsquare
    rw [hsqrt_sq] at hsquare
    exact hsquare
  rcases
      Transport.exists_isCoupling_lintegral_lt_of_transportCost_lt
        (quadraticCost (E := E)) μ ν hcost with
    ⟨γ, hγ, hγcost⟩
  refine ⟨γ, hγ, ?_⟩
  have hsqrt :=
    ENNReal.rpow_lt_rpow hγcost (z := (1 / (2 : ℝ))) (by norm_num)
  have hr_sq_sqrt : (r ^ (2 : ℝ)) ^ (1 / (2 : ℝ)) = r := by
    rw [← ENNReal.rpow_mul]
    norm_num
  rw [hr_sq_sqrt] at hsqrt
  exact hsqrt

/-- Chewi Definition 1.3.12: a probability measure in `P₂,ac` has finite
second moment and is absolutely continuous with respect to Lebesgue volume.

The generic finite-dimensional real inner-product space specializes to
Euclidean `R^d` in the source. -/
def IsAbsolutelyContinuousFiniteSecondMoment
    {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]
    (μ : Measure E) : Prop :=
  IsProbabilityMeasure μ ∧
    μ ≪ (volume : Measure E) ∧
    Integrable (fun x : E => ‖x‖ ^ 2) μ

/-- Expansion of the three conditions in the `P₂,ac` definition. -/
theorem isAbsolutelyContinuousFiniteSecondMoment_iff
    {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]
    (μ : Measure E) :
    IsAbsolutelyContinuousFiniteSecondMoment μ ↔
      IsProbabilityMeasure μ ∧
        μ ≪ (volume : Measure E) ∧
        Integrable (fun x : E => ‖x‖ ^ 2) μ :=
  Iff.rfl

end WassersteinSpace
end Measure
end TechnicalLemmas
end AutoSamplingTheory