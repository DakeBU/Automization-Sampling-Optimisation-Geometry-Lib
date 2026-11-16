import AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.DyadicCutoffIncrements
import AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoFiniteVariationQV

namespace AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoDyadicPrefixQV

open Filter MeasureTheory Set
open scoped BigOperators NNReal
open BrownianMotion ProgressiveL2 StoppingTime ElementaryItoIntegral
  SampledElementaryApproximation DyadicElementaryRefinement EuclideanBrownianCoordinates
  ItoIntegralProcess ItoFiniteVariationQV DyadicCutoffIncrements

/-- Quadratic variation along the prefix of the fine grid ending at a
fixed coarse dyadic cutoff. -/
theorem tendstoInMeasure_dyadic_prefix_sq_increments_of_ito_row
    {Ω J : Type*} [MeasurableSpace Ω] [Fintype J] [DecidableEq J]
    {filtration : Filtration ℝ≥0 (inferInstance : MeasurableSpace Ω)}
    {μ : Measure Ω} [IsFiniteMeasure μ] {T : ℝ≥0}
    {B : ℝ≥0 → Ω → EuclideanSpace ℝ J}
    (hB : IsStandardBrownianMotionWithFiltration B filtration μ) (hT : 0 < T)
    (hUsual : SatisfiesUsualConditions filtration μ)
    (η : J → ProgressiveL2Integrand filtration μ T)
    (A : ℝ≥0 → Ω → ℝ) (hAmeas : ∀ t ≤ T, AEStronglyMeasurable (A t) μ)
    (hA : ∀ᵐ ω ∂μ, ContinuousOn (fun t => A t ω) (Icc 0 T) ∧
      BoundedVariationOn (fun t => A t ω) (Icc 0 T))
    (m : ℕ) (k : Fin (2 ^ m + 1)) :
    let τ := regularGridTimes (dyadicMesh T m) (2 ^ m) k
    let X := fun t ω => A t ω + ∑ j : J,
      itoIntegralProcess (η j) hT ((coordinateFamily hB).isBrownian j) hUsual t ω
    TendstoInMeasure μ (fun n ω =>
      let t := regularGridTimes (dyadicMesh T n) (2 ^ n)
      ∑ i : Fin (2 ^ n), if t i.succ ≤ τ then
        (X (t i.succ) ω - X (t i.castSucc) ω) ^ 2 else 0) atTop
      (fun ω => ∑ j : J, ∫ s in Iic τ, (η j).process s ω ^ 2 ∂(TimeMeasure.upTo T)) := by
  intro τ X
  have hτ : τ ≤ T :=
    ((regularGridTimes_strictMono (dyadicMesh_pos hT m) _).monotone (Fin.le_last k)).trans_eq
      (regularDyadic_last_time T m)
  let S (t : ℝ≥0) := min τ t
  let A₀ (t : ℝ≥0) := A (S t)
  have hA₀ (t : ℝ≥0) (_ht : t ≤ T) : AEStronglyMeasurable (A₀ t) μ :=
    hAmeas _ ((min_le_left τ t).trans hτ)
  have hmaps : MapsTo S (Icc 0 T) (Icc 0 T) := fun t _ =>
    ⟨bot_le, (min_le_left τ t).trans hτ⟩
  have hmono : Monotone S := fun _ _ ht => min_le_min_left τ ht
  have hcont : Continuous S := continuous_const.min continuous_id
  have hA₀path : ∀ᵐ ω ∂μ, ContinuousOn (fun t => A₀ t ω) (Icc 0 T) ∧
      BoundedVariationOn (fun t => A₀ t ω) (Icc 0 T) := by
    filter_upwards [hA] with ω hω
    refine ⟨hω.1.comp hcont.continuousOn hmaps, ?_⟩
    exact ne_top_of_le_ne_top hω.2
      (eVariationOn.comp_le_of_monotoneOn (fun t => A t ω) S (hmono.monotoneOn _) hmaps)
  have h := tendstoInMeasure_dyadic_sq_increments_stopped_ito_add_boundedVariation
    hB hT hUsual η (fun _ => τ) (isChewiStoppingTime_const filtration τ) (fun _ => hτ)
    A₀ hA₀ hA₀path
  refine TendstoInMeasure.congr' ?_ EventuallyEq.rfl h
  filter_upwards [eventually_ge_atTop m] with n hn
  exact Eventually.of_forall fun ω => by
    simpa only [pow_two, X, A₀, S] using
      dyadic_sum_mul_stopped_increments_eq_prefix hT hn k (fun t => X t ω) (fun t => X t ω)

end AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoDyadicPrefixQV
