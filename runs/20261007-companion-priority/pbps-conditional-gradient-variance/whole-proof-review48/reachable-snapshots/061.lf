import AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.Langevin
import AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.WeakGenerator
import AutoSamplingTheory.TechnicalLemmas.Measure.GibbsIntegral

/-!
# Langevin generator core contracts

This file separates the formal Langevin differential expression from an
operator's declared domain.  It defines the compactly supported `C²` test core
used by the Chapter 1 integration-by-parts theorem and a contract saying that
a candidate generator domain contains that core and agrees there with the
displayed Langevin operator.

The contract does not construct a closed operator, prove closability, or show
that an SDE semigroup has this generator.  Those are downstream declarations.
-/

namespace AutoSamplingTheory
namespace TechnicalLemmas
namespace StochasticProcesses
namespace LangevinGenerator

open scoped RealInnerProductSpace
open Set MeasureTheory

/-- The compactly supported twice continuously differentiable test core used
for the finite-dimensional Langevin generator. -/
def CompactlySupportedC2
    {n : ℕ} (f : EuclideanSpace ℝ (Fin (n + 1)) → ℝ) : Prop :=
  ContDiff ℝ 2 f ∧ HasCompactSupport f

/-- The displayed overdamped Langevin differential operator associated with
the potential `V`. -/
noncomputable def operator
    {n : ℕ} (V f : EuclideanSpace ℝ (Fin (n + 1)) → ℝ) :
    EuclideanSpace ℝ (Fin (n + 1)) → ℝ :=
  fun x =>
    Laplacian.laplacian f x - inner ℝ (gradient V x) (gradient f x)

/-- An explicit domain contract for a candidate Langevin generator.

`domain` is kept separate from the operator action: the first field requires
the whole `C_c²` test core to belong to the candidate domain, while the second
field requires the candidate action to equal the displayed Langevin operator
on that core.  This avoids identifying a formal differential expression with
a semigroup generator without domain evidence. -/
structure CoreContract
    {n : ℕ}
    (V : EuclideanSpace ℝ (Fin (n + 1)) → ℝ)
    (generator :
      (EuclideanSpace ℝ (Fin (n + 1)) → ℝ) →
        EuclideanSpace ℝ (Fin (n + 1)) → ℝ)
    (domain : Set (EuclideanSpace ℝ (Fin (n + 1)) → ℝ)) : Prop where
  core_mem_domain : ∀ f, CompactlySupportedC2 f → f ∈ domain
  generator_eq_operator_on_core :
    ∀ f, CompactlySupportedC2 f → generator f = operator V f

/-- The normalized Gibbs measure annihilates the displayed Langevin operator
on the compactly supported `C²` core.

This is a normalized-measure corollary of the whole-space weighted-IBP theorem.
It is a core-level infinitesimal stationarity statement, not semigroup
invariance: extending it to a semigroup-stable generator domain requires an
additional closure/core theorem or a separate martingale-problem argument. -/
theorem integral_operator_normalizedGibbs_eq_zero_on_compactlySupportedC2
    {n : ℕ}
    {V f : EuclideanSpace ℝ (Fin (n + 1)) → ℝ}
    (hV : ContDiff ℝ 1 V)
    (hf : CompactlySupportedC2 f) :
    ∫ x, operator V f x ∂volume.withDensity
        (fun x =>
          (∫⁻ y, Measure.Gibbs.gibbsDensityENNReal V y ∂volume)⁻¹ *
            Measure.Gibbs.gibbsDensityENNReal V x) = 0 := by
  rw [TechnicalLemmas.Measure.GibbsIntegral.integral_withDensity_lintegral_inv_mul_gibbsDensityENNReal_eq_integral_lintegral_inv_mul_exp_smul_of_neZero
    volume hV.continuous.measurable.aemeasurable]
  simp_rw [operator, smul_eq_mul, mul_assoc]
  rw [integral_const_mul]
  rw [Langevin.integral_expNeg_langevinGenerator_rhs_eq_zero_of_contDiff_of_hasCompactSupport
    hV hf.1 hf.2]
  simp

/-- A semigroup satisfying the integrated-generator contract on the
compactly supported `C²` core preserves normalized Gibbs expectations on that
core.

This theorem composes the concrete Gibbs integration-by-parts identity with
the abstract semigroup-to-invariance bridge.  The semigroup contract remains
an explicit hypothesis: no Langevin SDE, Markov semigroup, core closure, or
measure-determining extension is constructed here. -/
theorem isInvariantOn_normalizedGibbs_on_compactlySupportedC2
    {n : ℕ}
    {V : EuclideanSpace ℝ (Fin (n + 1)) → ℝ}
    {P : ℝ →
      (EuclideanSpace ℝ (Fin (n + 1)) → ℝ) →
        EuclideanSpace ℝ (Fin (n + 1)) → ℝ}
    {generator :
      (EuclideanSpace ℝ (Fin (n + 1)) → ℝ) →
        EuclideanSpace ℝ (Fin (n + 1)) → ℝ}
    (hV : ContDiff ℝ 1 V)
    (hcore : CoreContract V generator (Set.ofPred CompactlySupportedC2))
    (hsemigroup : WeakGenerator.IntegratedSemigroupGeneratorContract
      P generator (Set.ofPred CompactlySupportedC2)
      (volume.withDensity
        (fun x =>
          (∫⁻ y, Measure.Gibbs.gibbsDensityENNReal V y ∂volume)⁻¹ *
            Measure.Gibbs.gibbsDensityENNReal V x))) :
    WeakGenerator.IsInvariantOn P
      (volume.withDensity
        (fun x =>
          (∫⁻ y, Measure.Gibbs.gibbsDensityENNReal V y ∂volume)⁻¹ *
            Measure.Gibbs.gibbsDensityENNReal V x))
      (Set.ofPred CompactlySupportedC2) := by
  refine WeakGenerator.isInvariantOn_of_integral_generator_eq_zero hsemigroup ?_
  intro f hf
  rw [hcore.generator_eq_operator_on_core f hf]
  exact integral_operator_normalizedGibbs_eq_zero_on_compactlySupportedC2 hV hf

end LangevinGenerator
end StochasticProcesses
end TechnicalLemmas
end AutoSamplingTheory
