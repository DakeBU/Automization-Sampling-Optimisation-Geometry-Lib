import AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.EuclideanBrownianCoordinates
import AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoIntegralProcess
import Mathlib.Analysis.Normed.Lp.MeasurableSpace

namespace AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoEuclideanRowRegularity

open Filter MeasureTheory Set
open scoped BigOperators NNReal
open BrownianMotion ProgressiveL2 EuclideanBrownianCoordinates ItoIntegralProcess

/-- Actual completed coordinate rows with continuous drifts have measurable
vector slices and almost surely continuous vector paths on the horizon. -/
theorem measurable_continuousOn_euclidean_ito_rows
    {Ω I J : Type*} [MeasurableSpace Ω] [Fintype I] [Fintype J] [DecidableEq J]
    {filtration : Filtration ℝ≥0 (inferInstance : MeasurableSpace Ω)}
    {μ : Measure Ω} [IsFiniteMeasure μ] {T : ℝ≥0}
    {B : ℝ≥0 → Ω → EuclideanSpace ℝ J}
    (hB : IsStandardBrownianMotionWithFiltration B filtration μ) (hT : 0 < T)
    (hUsual : SatisfiesUsualConditions filtration μ)
    (η : I → J → ProgressiveL2Integrand filtration μ T) (A : I → ℝ≥0 → Ω → ℝ)
    (hAmeas : ∀ i t, t ≤ T → AEStronglyMeasurable (A i t) μ)
    (hA : ∀ i, ∀ᵐ ω ∂μ, ContinuousOn (fun t => A i t ω) (Icc 0 T)) :
    let X := fun (t : ℝ≥0) (ω : Ω) => WithLp.toLp 2 (fun i : I => A i t ω + ∑ j : J,
      itoIntegralProcess (η i j) hT ((coordinateFamily hB).isBrownian j) hUsual t ω)
    (∀ t ≤ T, Measurable (X t)) ∧ (∀ᵐ ω ∂μ, ContinuousOn (fun t => X t ω) (Icc 0 T)) := by
  intro X
  let M (i : I) (j : J) := itoIntegralProcess (η i j) hT ((coordinateFamily hB).isBrownian j) hUsual
  let _ : μ.IsComplete := Measure.isComplete_iff.2
    (fun s hs => filtration.le 0 _ (hUsual.completeAt 0 s hs))
  constructor
  · intro t ht
    have hM (i : I) : AEStronglyMeasurable (fun ω => ∑ j : J, M i j t ω) μ :=
      (Finset.aestronglyMeasurable_sum Finset.univ fun j _ =>
        (((itoIntegralProcess_stronglyAdapted (η i j) hT
          ((coordinateFamily hB).isBrownian j) hUsual) t).mono
            (filtration.le t)).aestronglyMeasurable).congr
        (Eventually.of_forall fun ω => by simp only [Finset.sum_apply, M])
    have hRow (i : I) : Measurable (fun ω => A i t ω + ∑ j : J, M i j t ω) :=
      ((hAmeas i t ht).add (hM i)).aemeasurable.nullMeasurable.measurable_of_complete
    exact (MeasurableEquiv.toLp 2 (I → ℝ)).measurable.comp (measurable_pi_lambda _ hRow)
  · filter_upwards [ae_all_iff.2 hA] with ω hω
    have hRow (i : I) : ContinuousOn (fun t => A i t ω + ∑ j : J, M i j t ω) (Icc 0 T) :=
      (hω i).add (continuousOn_finsetSum _ fun j _ =>
        itoIntegralProcess_continuousOn (η i j) hT ((coordinateFamily hB).isBrownian j) hUsual ω)
    exact (PiLp.continuous_toLp 2 (fun _ : I => ℝ)).comp_continuousOn (continuousOn_pi.2 hRow)

end AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoEuclideanRowRegularity
