import AutoSamplingTheory.TechnicalLemmas.Measure.ContinuousCostWeakLowerSemicontinuity
import AutoSamplingTheory.TechnicalLemmas.Measure.DisplacementInterpolation
import AutoSamplingTheory.TechnicalLemmas.Measure.ProbabilityCouplingCompactness

/-!
# Existence of a quadratic optimal coupling

This is the direct-method assembly node for the quadratic Kantorovich problem.
The analytical and topological work lives in separate reusable parents:

* `Transport.isCoupling_prod` gives a canonical feasible coupling;
* `ProbabilityCouplingCompactness.isCompact_probabilityCouplingSet` gives weak
  compactness of the fixed-marginal feasible set;
* `ContinuousCostWeakLowerSemicontinuity.lowerSemicontinuous_quadraticCostFunctional`
  gives weak lower semicontinuity of the quadratic objective;
* Mathlib's `LowerSemicontinuousOn.exists_isMinOn` attains the minimum.

No finite-second-moment assumption is required merely to attain the
extended-nonnegative quadratic optimum. If every feasible coupling has infinite
quadratic cost, the minimum is still attained. Moment assumptions enter later
when a consumer needs the optimal value to be finite and to identify it with a
finite `W₂` distance.

## Source boundary

This is a reusable Kantorovich existence theorem, not the full source-facing
Brenier theorem. It proves neither uniqueness of the optimal plan, existence of
an inducing map, nor convex-gradient identification. Those remain separate
nodes in the formal graph.
-/

namespace AutoSamplingTheory
namespace TechnicalLemmas
namespace Measure
namespace QuadraticOptimalCouplingExistence

open MeasureTheory Set Topology
open ContinuousCostWeakLowerSemicontinuity
open DisplacementInterpolation ProbabilityCouplingCompactness
open Transport WassersteinSpace
open scoped ENNReal

noncomputable section

variable {E : Type*} [NormedAddCommGroup E] [CompleteSpace E]
  [MeasurableSpace E] [BorelSpace E] [SecondCountableTopology E]

/-- The weak-topology fixed-marginal feasible set is nonempty. The independent
product coupling is the canonical witness. -/
theorem probabilityCouplingSet_nonempty
    (mu nu : ProbabilityMeasure E) :
    (probabilityCouplingSet mu nu).Nonempty := by
  let gammaRaw : Measure (E × E) := (mu : Measure E).prod (nu : Measure E)
  have hgammaRaw :
      IsCoupling gammaRaw (mu : Measure E) (nu : Measure E) := by
    simpa [gammaRaw] using
      (isCoupling_prod (mu : Measure E) (nu : Measure E))
  let gamma : ProbabilityMeasure (E × E) :=
    ⟨gammaRaw, isProbabilityMeasure_of_isCoupling_left hgammaRaw⟩
  refine ⟨gamma, ?_⟩
  apply isProbabilityCoupling_iff_isCoupling_toMeasure.mpr
  simpa [gamma] using hgammaRaw

/-- The quadratic objective on weak probability measures. -/
noncomputable def quadraticObjective
    (gamma : ProbabilityMeasure (E × E)) : ℝ≥0∞ :=
  ∫⁻ z, quadraticCost (E := E) z ∂(gamma : Measure (E × E))

/-- The quadratic objective attains a minimum on the compact fixed-marginal
probability-coupling set. -/
theorem exists_isMinOn_quadraticObjective
    (mu nu : ProbabilityMeasure E) :
    ∃ gamma ∈ probabilityCouplingSet mu nu,
      IsMinOn (quadraticObjective (E := E))
        (probabilityCouplingSet mu nu) gamma := by
  have hnonempty : (probabilityCouplingSet mu nu).Nonempty :=
    probabilityCouplingSet_nonempty mu nu
  have hcompact : IsCompact (probabilityCouplingSet mu nu) :=
    isCompact_probabilityCouplingSet mu nu
  have hlsc : LowerSemicontinuous (quadraticObjective (E := E)) := by
    simpa [quadraticObjective] using
      (lowerSemicontinuous_quadraticCostFunctional (E := E))
  exact LowerSemicontinuousOn.exists_isMinOn
    hnonempty hcompact
    (hlsc.lowerSemicontinuousOn (probabilityCouplingSet mu nu))

/-- Probability-measure form of quadratic Kantorovich optimizer existence. -/
theorem exists_quadraticOptimalCoupling_probabilityMeasure
    (mu nu : ProbabilityMeasure E) :
    ∃ gamma : ProbabilityMeasure (E × E),
      IsQuadraticOptimalCoupling (gamma : Measure (E × E))
        (mu : Measure E) (nu : Measure E) := by
  rcases exists_isMinOn_quadraticObjective mu nu with
    ⟨gamma, hgamma_mem, hgamma_min⟩
  have hgamma_coupling :
      IsCoupling (gamma : Measure (E × E))
        (mu : Measure E) (nu : Measure E) :=
    isProbabilityCoupling_iff_isCoupling_toMeasure.mp hgamma_mem
  refine ⟨gamma, hgamma_coupling, ?_⟩
  apply le_antisymm
  · rw [transportCost_eq_sInf]
    apply le_sInf
    intro r hr
    rcases hr with ⟨rho, hrho, rfl⟩
    change IsCoupling rho (mu : Measure E) (nu : Measure E) at hrho
    let rhoP : ProbabilityMeasure (E × E) :=
      ⟨rho, isProbabilityMeasure_of_isCoupling_left hrho⟩
    have hrhoP_mem : rhoP ∈ probabilityCouplingSet mu nu := by
      apply isProbabilityCoupling_iff_isCoupling_toMeasure.mpr
      simpa [rhoP] using hrho
    have hle := hgamma_min rhoP hrhoP_mem
    simpa [quadraticObjective, rhoP] using hle
  · exact transportCost_le_lintegral_of_isCoupling
      (quadraticCost (E := E)) (mu : Measure E) (nu : Measure E)
      (gamma : Measure (E × E)) hgamma_coupling

/-- Raw-measure wrapper: every pair of probability measures on the ambient
Polish normed group admits a quadratic-optimal coupling. -/
theorem exists_quadraticOptimalCoupling
    (mu nu : Measure E)
    [IsProbabilityMeasure mu] [IsProbabilityMeasure nu] :
    ∃ gamma : Measure (E × E),
      IsQuadraticOptimalCoupling gamma mu nu := by
  let muP : ProbabilityMeasure E := ⟨mu, inferInstance⟩
  let nuP : ProbabilityMeasure E := ⟨nu, inferInstance⟩
  rcases exists_quadraticOptimalCoupling_probabilityMeasure muP nuP with
    ⟨gamma, hgamma⟩
  refine ⟨(gamma : Measure (E × E)), ?_⟩
  simpa [muP, nuP] using hgamma

end

end QuadraticOptimalCouplingExistence
end Measure
end TechnicalLemmas
end AutoSamplingTheory
