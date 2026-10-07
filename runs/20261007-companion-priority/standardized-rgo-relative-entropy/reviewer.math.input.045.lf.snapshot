import AutoSamplingTheory.TechnicalLemmas.Measure.WassersteinSpace
import AutoSamplingTheory.TechnicalLemmas.Measure.WassersteinTriangleMarginals
import Mathlib.MeasureTheory.Measure.Prod
import Mathlib.Tactic

/-!
# Wasserstein contraction under common additive noise

Adding the same independent noise to both coordinates of a coupling does not
change their pairwise displacement.  Pushing a near-optimal coupling through
this synchronous-noise construction therefore gives the general contraction

`W₂(μ * κ, ν * κ) ≤ W₂(μ,ν)`,

where `* κ` is represented explicitly as the law of `X + Z` for independent
`X` and `Z ~ κ`.

Gaussian heat-flow contraction is a later specialization of this theorem.  The
proof itself is purely transport-theoretic and does not use Gaussian structure.
-/

namespace AutoSamplingTheory
namespace TechnicalLemmas
namespace Measure
namespace CommonNoiseContraction

open MeasureTheory
open scoped ENNReal

noncomputable section

variable {E : Type*} [NormedAddCommGroup E]
  [MeasurableSpace E] [BorelSpace E] [SecondCountableTopology E]

/-- Law of an independent sample from `μ` plus an independent noise sample from
`κ`. -/
noncomputable def addNoise (μ κ : Measure E) : Measure E :=
  Measure.map (fun p : E × E => p.1 + p.2) (μ.prod κ)

@[fun_prop]
theorem measurable_addPair : Measurable (fun p : E × E => p.1 + p.2) := by
  fun_prop

/-- Synchronous-noise map on an endpoint coupling and one common noise sample. -/
def synchronousNoiseMap : ((E × E) × E) → E × E :=
  fun p => (p.1.1 + p.2, p.1.2 + p.2)

@[fun_prop]
theorem measurable_synchronousNoiseMap :
    Measurable (synchronousNoiseMap (E := E)) := by
  unfold synchronousNoiseMap
  fun_prop

/-- Add one common independent noise sample to both coordinates of a coupling. -/
noncomputable def synchronousNoiseCoupling
    (γ : Measure (E × E)) (κ : Measure E) : Measure (E × E) :=
  Measure.map (synchronousNoiseMap (E := E)) (γ.prod κ)

private def pairLeft : ((E × E) × E) → E × E := fun p => (p.1.1, p.2)
private def pairRight : ((E × E) × E) → E × E := fun p => (p.1.2, p.2)

private theorem measurable_pairLeft : Measurable (pairLeft (E := E)) := by
  unfold pairLeft
  fun_prop

private theorem measurable_pairRight : Measurable (pairRight (E := E)) := by
  unfold pairRight
  fun_prop

/-- The `(left endpoint, noise)` marginal of `γ ⊗ κ` is `μ ⊗ κ` whenever
`γ` couples `μ` and `ν`. -/
theorem map_pairLeft_prod_eq
    {μ ν κ : Measure E} {γ : Measure (E × E)}
    [IsProbabilityMeasure μ] [IsProbabilityMeasure κ]
    (hγ : Transport.IsCoupling γ μ ν) :
    Measure.map (pairLeft (E := E)) (γ.prod κ) = μ.prod κ := by
  letI : IsProbabilityMeasure γ :=
    Transport.isProbabilityMeasure_of_isCoupling_left hγ
  have hfst : Measure.map Prod.fst γ = μ := by
    simpa [Measure.fst] using hγ.1
  calc
    Measure.map (pairLeft (E := E)) (γ.prod κ) =
        Measure.map (Prod.map Prod.fst id) (γ.prod κ) := by rfl
    _ = (Measure.map Prod.fst γ).prod (Measure.map id κ) := by
      symm
      exact Measure.map_prod_map γ κ measurable_fst measurable_id
    _ = μ.prod κ := by
      rw [hfst]
      simp

/-- The `(right endpoint, noise)` marginal is `ν ⊗ κ`. -/
theorem map_pairRight_prod_eq
    {μ ν κ : Measure E} {γ : Measure (E × E)}
    [IsProbabilityMeasure μ] [IsProbabilityMeasure κ]
    (hγ : Transport.IsCoupling γ μ ν) :
    Measure.map (pairRight (E := E)) (γ.prod κ) = ν.prod κ := by
  letI : IsProbabilityMeasure γ :=
    Transport.isProbabilityMeasure_of_isCoupling_left hγ
  have hsnd : Measure.map Prod.snd γ = ν := by
    simpa [Measure.snd] using hγ.2
  calc
    Measure.map (pairRight (E := E)) (γ.prod κ) =
        Measure.map (Prod.map Prod.snd id) (γ.prod κ) := by rfl
    _ = (Measure.map Prod.snd γ).prod (Measure.map id κ) := by
      symm
      exact Measure.map_prod_map γ κ measurable_snd measurable_id
    _ = ν.prod κ := by
      rw [hsnd]
      simp

/-- Synchronous common noise sends a coupling of `μ,ν` to a coupling of their
additive-noise laws. -/
theorem isCoupling_synchronousNoiseCoupling
    {μ ν κ : Measure E} {γ : Measure (E × E)}
    [IsProbabilityMeasure μ] [IsProbabilityMeasure κ]
    (hγ : Transport.IsCoupling γ μ ν) :
    Transport.IsCoupling
      (synchronousNoiseCoupling γ κ) (addNoise μ κ) (addNoise ν κ) := by
  letI : IsProbabilityMeasure γ :=
    Transport.isProbabilityMeasure_of_isCoupling_left hγ
  constructor
  · rw [Measure.fst, synchronousNoiseCoupling]
    rw [Measure.map_map measurable_fst measurable_synchronousNoiseMap]
    change Measure.map (fun p : ((E × E) × E) => p.1.1 + p.2) (γ.prod κ) = addNoise μ κ
    unfold addNoise
    calc
      Measure.map (fun p : ((E × E) × E) => p.1.1 + p.2) (γ.prod κ) =
          Measure.map (fun q : E × E => q.1 + q.2)
            (Measure.map (pairLeft (E := E)) (γ.prod κ)) := by
        rw [Measure.map_map measurable_addPair measurable_pairLeft]
        rfl
      _ = Measure.map (fun q : E × E => q.1 + q.2) (μ.prod κ) := by
        rw [map_pairLeft_prod_eq hγ]
  · rw [Measure.snd, synchronousNoiseCoupling]
    rw [Measure.map_map measurable_snd measurable_synchronousNoiseMap]
    change Measure.map (fun p : ((E × E) × E) => p.1.2 + p.2) (γ.prod κ) = addNoise ν κ
    unfold addNoise
    calc
      Measure.map (fun p : ((E × E) × E) => p.1.2 + p.2) (γ.prod κ) =
          Measure.map (fun q : E × E => q.1 + q.2)
            (Measure.map (pairRight (E := E)) (γ.prod κ)) := by
        rw [Measure.map_map measurable_addPair measurable_pairRight]
        rfl
      _ = Measure.map (fun q : E × E => q.1 + q.2) (ν.prod κ) := by
        rw [map_pairRight_prod_eq hγ]

/-- Common translation preserves the pointwise quadratic transport cost. -/
theorem quadraticCost_synchronousNoiseMap
    (p : ((E × E) × E)) :
    WassersteinSpace.quadraticCost (E := E) (synchronousNoiseMap p) =
      WassersteinSpace.quadraticCost (E := E) p.1 := by
  unfold WassersteinSpace.quadraticCost synchronousNoiseMap
  have hsub : (p.1.1 + p.2) - (p.1.2 + p.2) = p.1.1 - p.1.2 := by
    abel
  rw [hsub]

/-- The synchronous-noise coupling has exactly the same quadratic cost as the
original endpoint coupling. -/
theorem lintegral_quadraticCost_synchronousNoiseCoupling
    (γ : Measure (E × E)) (κ : Measure E) [IsProbabilityMeasure κ] [SFinite γ] :
    (∫⁻ z, WassersteinSpace.quadraticCost (E := E) z
      ∂synchronousNoiseCoupling γ κ) =
      ∫⁻ z, WassersteinSpace.quadraticCost (E := E) z ∂γ := by
  rw [synchronousNoiseCoupling]
  rw [lintegral_map
    WassersteinTriangleMarginals.measurable_quadraticCost
    measurable_synchronousNoiseMap]
  simp_rw [quadraticCost_synchronousNoiseMap]
  calc
    (∫⁻ p : (E × E) × E,
        WassersteinSpace.quadraticCost (E := E) p.1 ∂γ.prod κ) =
      ∫⁻ z, WassersteinSpace.quadraticCost (E := E) z
        ∂Measure.map Prod.fst (γ.prod κ) := by
      exact (lintegral_map
        WassersteinTriangleMarginals.measurable_quadraticCost measurable_fst).symm
    _ = ∫⁻ z, WassersteinSpace.quadraticCost (E := E) z ∂γ := by
      rw [Measure.map_fst_prod, measure_univ, one_smul]

/-- Wasserstein distance contracts under adding one common independent noise
law.  No moment or Gaussian assumption is needed: if the original distance is
infinite the claim is automatic, while the finite branch is obtained from
strictly near-optimal plans. -/
theorem wassersteinDistance_addNoise_le
    (μ ν κ : Measure E)
    [IsProbabilityMeasure μ] [IsProbabilityMeasure ν] [IsProbabilityMeasure κ] :
    WassersteinSpace.wassersteinDistance (addNoise μ κ) (addNoise ν κ) ≤
      WassersteinSpace.wassersteinDistance μ ν := by
  apply ENNReal.le_of_forall_pos_le_add
  intro ε hε hfinite
  have hεne : (ε : ℝ≥0∞) ≠ 0 := by
    exact_mod_cast (ne_of_gt hε)
  have hstrict :
      WassersteinSpace.wassersteinDistance μ ν <
        WassersteinSpace.wassersteinDistance μ ν + (ε : ℝ≥0∞) :=
    ENNReal.lt_add_right hfinite.ne hεne
  rcases
      WassersteinSpace.exists_isCoupling_sqrt_lintegral_lt_of_wassersteinDistance_lt
        μ ν hstrict with
    ⟨γ, hγ, hcost⟩
  letI : IsProbabilityMeasure γ :=
    Transport.isProbabilityMeasure_of_isCoupling_left hγ
  have hsync := isCoupling_synchronousNoiseCoupling (κ := κ) hγ
  calc
    WassersteinSpace.wassersteinDistance (addNoise μ κ) (addNoise ν κ) ≤
        (∫⁻ z, WassersteinSpace.quadraticCost (E := E) z
          ∂synchronousNoiseCoupling γ κ) ^ (1 / (2 : ℝ)) :=
      WassersteinSpace.wassersteinDistance_le_sqrt_lintegral_of_isCoupling
        (addNoise μ κ) (addNoise ν κ) (synchronousNoiseCoupling γ κ) hsync
    _ = (∫⁻ z, WassersteinSpace.quadraticCost (E := E) z ∂γ) ^
          (1 / (2 : ℝ)) := by
      rw [lintegral_quadraticCost_synchronousNoiseCoupling]
    _ ≤ WassersteinSpace.wassersteinDistance μ ν + (ε : ℝ≥0∞) := hcost.le

end

end CommonNoiseContraction
end Measure
end TechnicalLemmas
end AutoSamplingTheory
