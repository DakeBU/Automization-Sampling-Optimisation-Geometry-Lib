import AutoSamplingTheory.TechnicalLemmas.Measure.WeakProbabilityIntegral
import Mathlib.MeasureTheory.Function.ConvergenceInDistribution
import Mathlib.MeasureTheory.Integral.IntervalIntegral.FundThmCalculus
import Mathlib.MeasureTheory.Integral.Prod

namespace AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.WeakDiffusionLaw

open Filter MeasureTheory
open scoped Topology
open AutoSamplingTheory.TechnicalLemmas.Measure.WeakProbabilityIntegral

/-- Almost surely continuous paths give weakly continuous marginal laws. -/
theorem continuous_marginal_law_of_ae_continuous
    {T Ω E : Type*} [TopologicalSpace T] [FirstCountableTopology T]
    [MeasurableSpace Ω] [TopologicalSpace E] [MeasurableSpace E] [OpensMeasurableSpace E]
    (μ : ProbabilityMeasure Ω) (X : T → Ω → E) (hX : ∀ t, Measurable (X t))
    (hpaths : ∀ᵐ ω ∂(μ : Measure Ω), Continuous (fun t => X t ω)) :
    Continuous (fun t => μ.map (hX t).aemeasurable) := by
  rw [continuous_iff_continuousAt]
  intro t
  have hae : ∀ᵐ ω ∂(μ : Measure Ω),
      Tendsto (fun u => X u ω) (𝓝 t) (𝓝 (X t ω)) :=
    hpaths.mono fun _ hω => hω.continuousAt.tendsto
  exact (tendstoInDistribution_of_ae_tendsto
    (fun u => (hX u).aemeasurable) (hX t).aemeasurable hae).tendsto

/-- Taking expectations in an almost-sure observable increment identity with
an integrable, centered residual gives the weak marginal integral balance. -/
theorem weak_integral_balance_of_centered_increment
    {Ω E : Type*} [MeasurableSpace Ω] [MeasurableSpace E]
    (μ : ProbabilityMeasure Ω) (X : ℝ → Ω → E) (hX : ∀ t, Measurable (X t))
    {g : E → ℝ} (hg : Measurable g) {A : ℝ → E → ℝ}
    (hA : ∀ v, Measurable (A v)) (a b : ℝ)
    (hga : Integrable (fun ω => g (X a ω)) (μ : Measure Ω))
    (hgb : Integrable (fun ω => g (X b ω)) (μ : Measure Ω))
    (hdrift : Integrable (Function.uncurry fun v ω => A v (X v ω))
      ((volume.restrict (Set.uIoc a b)).prod (μ : Measure Ω)))
    {Z : Ω → ℝ} (hZ : Integrable Z (μ : Measure Ω))
    (hmean : ∫ ω, Z ω ∂(μ : Measure Ω) = 0)
    (hinc : ∀ᵐ ω ∂(μ : Measure Ω),
      g (X b ω) - g (X a ω) = (∫ v in a..b, A v (X v ω)) + Z ω) :
    (∫ x, g x ∂(μ.map (hX b).aemeasurable : Measure E)) -
      (∫ x, g x ∂(μ.map (hX a).aemeasurable : Measure E)) =
      ∫ v in a..b, ∫ x, A v x ∂(μ.map (hX v).aemeasurable : Measure E) := by
  have hmap (v : ℝ) {f : E → ℝ} (hf : Measurable f) :
      (∫ x, f x ∂(μ.map (hX v).aemeasurable : Measure E)) =
        ∫ ω, f (X v ω) ∂(μ : Measure Ω) := by
    rw [ProbabilityMeasure.toMeasure_map]
    exact integral_map (hX v).aemeasurable hf.aestronglyMeasurable
  let D : Ω → ℝ := fun ω => ∫ v in a..b, A v (X v ω)
  have hD : Integrable D (μ : Measure Ω) := by
    have hI := hdrift.swap.integral_prod_left
    change Integrable (fun ω => ∫ v in Set.uIoc a b, A v (X v ω)) (μ : Measure Ω) at hI
    by_cases hab : a ≤ b
    · simpa only [D, intervalIntegral.integral_of_le hab, Set.uIoc_of_le hab] using hI
    · have hba : b ≤ a := le_of_not_ge hab
      simpa only [D, intervalIntegral.integral_of_ge hba, Set.uIoc_of_ge hba] using hI.fun_neg
  rw [hmap b hg, hmap a hg, ← integral_sub hgb hga, integral_congr_ae hinc,
    integral_add hD hZ, hmean, add_zero]
  simp_rw [hmap _ (hA _)]
  exact (intervalIntegral_integral_swap hdrift).symm

/-- A local weak integral evolution identity yields the weak forward
derivative for the fixed test observable. -/
theorem hasDerivAt_weak_observable_of_integral_balance
    {E : Type*} [TopologicalSpace E] [CompactSpace E]
    [MeasurableSpace E] [OpensMeasurableSpace E]
    {μ : ℝ → ProbabilityMeasure E} (hμ : Continuous μ)
    (g : E → ℝ) {A : ℝ → E → ℝ}
    (hA : Continuous (fun p : ℝ × E => A p.1 p.2))
    {s : ℝ}
    (hbalance : ∀ᶠ u in 𝓝 s,
      (∫ x, g x ∂(μ u : Measure E)) - (∫ x, g x ∂(μ s : Measure E)) =
        ∫ v in s..u, ∫ x, A v x ∂(μ v : Measure E)) :
    HasDerivAt (fun u => ∫ x, g x ∂(μ u : Measure E))
      (∫ x, A s x ∂(μ s : Measure E)) s := by
  let B := fun v => ∫ x, A v x ∂(μ v : Measure E)
  have hB : Continuous B := continuous_integral_of_compact hA hμ
  have hprimitive : HasDerivAt (fun u => ∫ v in s..u, B v) (B s) s :=
    intervalIntegral.integral_hasDerivAt_right (hB.intervalIntegrable s s)
      hB.stronglyMeasurable.stronglyMeasurableAtFilter hB.continuousAt
  apply (hprimitive.const_add (∫ x, g x ∂(μ s : Measure E))).congr_of_eventuallyEq
  filter_upwards [hbalance] with u hu
  change (∫ x, g x ∂(μ u : Measure E)) =
    (∫ x, g x ∂(μ s : Measure E)) + ∫ v in s..u, B v
  exact eq_add_of_sub_eq' hu

end AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.WeakDiffusionLaw
