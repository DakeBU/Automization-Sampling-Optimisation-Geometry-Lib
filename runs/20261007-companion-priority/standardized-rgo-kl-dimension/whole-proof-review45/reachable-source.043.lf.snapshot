import Mathlib.MeasureTheory.Measure.Prod

/-!
# Couplings and transport foundations

Small measure-level interfaces shared by optimal transport and coupling proofs
for sampling algorithms. Algorithmic costs and Wasserstein optimization remain
separate layers.
-/

namespace AutoSamplingTheory
namespace TechnicalLemmas
namespace Measure
namespace Transport

open MeasureTheory
open scoped ENNReal

/-- A measure on a product space couples two marginals when its first and
second marginals are the specified measures. Probability normalization remains
visible through the marginal measures' typeclass assumptions at consumers. -/
def IsCoupling {α β : Type*} [MeasurableSpace α] [MeasurableSpace β]
    (γ : Measure (α × β)) (μ : Measure α) (ν : Measure β) : Prop :=
  γ.fst = μ ∧ γ.snd = ν

/-- The feasible set of couplings with prescribed marginals. -/
def couplingSet {α β : Type*} [MeasurableSpace α] [MeasurableSpace β]
    (μ : Measure α) (ν : Measure β) : Set (Measure (α × β)) :=
  {γ | IsCoupling γ μ ν}

/-- Chewi Definition 1.3.1 and display (1.3.2): the Kantorovich
transport cost for an extended nonnegative cost function.

Measurability and lower semicontinuity of `c` are not needed to state the
extended-real infimum.  They enter the later existence theorem. -/
noncomputable def transportCost {α β : Type*} [MeasurableSpace α] [MeasurableSpace β]
    (c : α × β → ℝ≥0∞) (μ : Measure α) (ν : Measure β) : ℝ≥0∞ :=
  sInf {r : ℝ≥0∞ | ∃ γ ∈ couplingSet μ ν, r = ∫⁻ z, c z ∂γ}

/-- Source-facing expansion of the Kantorovich value in display (1.3.2). -/
theorem transportCost_eq_sInf
    {α β : Type*} [MeasurableSpace α] [MeasurableSpace β]
    (c : α × β → ℝ≥0∞) (μ : Measure α) (ν : Measure β) :
    transportCost c μ ν =
      sInf {r : ℝ≥0∞ | ∃ γ ∈ couplingSet μ ν, r = ∫⁻ z, c z ∂γ} :=
  rfl

/-- Every feasible coupling gives an upper bound on the Kantorovich optimum.

This is the basic `sInf <= candidate` edge used repeatedly when a concrete
coupling is constructed (for example from a displacement interpolation or a
Markovian coupling).  It does not require existence of an optimizer. -/
theorem transportCost_le_lintegral_of_isCoupling
    {α β : Type*} [MeasurableSpace α] [MeasurableSpace β]
    (c : α × β → ℝ≥0∞) (μ : Measure α) (ν : Measure β)
    (γ : Measure (α × β)) (hγ : IsCoupling γ μ ν) :
    transportCost c μ ν ≤ ∫⁻ z, c z ∂γ := by
  rw [transportCost_eq_sInf]
  exact sInf_le ⟨γ, hγ, rfl⟩

/-- Strictly above the Kantorovich infimum, one can select an actual feasible
coupling whose cost is already below that threshold.

This is the reusable `sInf` near-optimal-selection edge.  It makes no optimizer
existence claim: the threshold must be strictly larger than the infimum. -/
theorem exists_isCoupling_lintegral_lt_of_transportCost_lt
    {α β : Type*} [MeasurableSpace α] [MeasurableSpace β]
    (c : α × β → ℝ≥0∞) (μ : Measure α) (ν : Measure β)
    {r : ℝ≥0∞}
    (h : transportCost c μ ν < r) :
    ∃ γ : Measure (α × β),
      IsCoupling γ μ ν ∧ (∫⁻ z, c z ∂γ) < r := by
  rw [transportCost_eq_sInf, sInf_lt_iff] at h
  rcases h with ⟨q, ⟨γ, hγ, hq⟩, hqr⟩
  subst q
  exact ⟨γ, hγ, hqr⟩

/-- A prescribed probability marginal forces the joint coupling measure to
have total mass one. This recovers the probability-measure interface required
by expectations and transport costs from the marginal contract. -/
theorem isProbabilityMeasure_of_isCoupling_left
    {α β : Type*} [MeasurableSpace α] [MeasurableSpace β]
    {γ : Measure (α × β)} {μ : Measure α} {ν : Measure β}
    [IsProbabilityMeasure μ] (hγ : IsCoupling γ μ ν) :
    IsProbabilityMeasure γ := by
  constructor
  rw [← Measure.fst_univ, hγ.1, measure_univ]

/-- The independent product measure is a coupling of two probability measures.
This supplies the canonical nonemptiness witness for the Kantorovich feasible
set in Chewi, Definition 1.3.1. -/
theorem isCoupling_prod {α β : Type*} [MeasurableSpace α] [MeasurableSpace β]
    (μ : Measure α) (ν : Measure β) [IsProbabilityMeasure μ] [IsProbabilityMeasure ν] :
    IsCoupling (μ.prod ν) μ ν := by
  constructor <;> simp

/-- The feasible set in the Kantorovich problem is nonempty for probability
marginals. -/
theorem couplingSet_nonempty
    {α β : Type*} [MeasurableSpace α] [MeasurableSpace β]
    (μ : Measure α) (ν : Measure β) [IsProbabilityMeasure μ] [IsProbabilityMeasure ν] :
    (couplingSet μ ν).Nonempty :=
  ⟨μ.prod ν, isCoupling_prod μ ν⟩

end Transport
end Measure
end TechnicalLemmas
end AutoSamplingTheory
