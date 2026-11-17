import AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.CompactStateRepresentative
import AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoEuclideanRowRegularity
import AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoIntegralProcessAfterHorizon
import Mathlib.Analysis.Calculus.ContDiff.Comp

namespace AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoEuclideanGradientWeights

open Filter MeasureTheory Set
open scoped BigOperators NNReal
open BrownianMotion ProgressiveL2 EuclideanBrownianCoordinates ItoIntegralProcess
  ItoIntegralProcessAfterHorizon ItoEuclideanRowRegularity

open CompactStateRepresentative

/-- Evaluating the derivative on a coordinate basis vector along the clipped
actual process gives a bounded progressive weight with continuous paths. -/
theorem euclidean_ito_gradient_weight_progressive_bounded
    {Ω I J : Type*} [MeasurableSpace Ω] [Fintype I] [DecidableEq I] [Fintype J] [DecidableEq J]
    {filtration : Filtration ℝ≥0 (inferInstance : MeasurableSpace Ω)}
    {μ : Measure Ω} [IsFiniteMeasure μ] {T : ℝ≥0}
    {B : ℝ≥0 → Ω → EuclideanSpace ℝ J}
    (hB : IsStandardBrownianMotionWithFiltration B filtration μ) (hT : 0 < T)
    (hUsual : SatisfiesUsualConditions filtration μ)
    (η : I → J → ProgressiveL2Integrand filtration μ T) (A : I → ℝ≥0 → Ω → ℝ)
    (hAp : ∀ i, IsStronglyProgressive filtration (A i))
    (hAc : ∀ i, ∀ᵐ ω ∂μ, ContinuousOn (fun t => A i t ω) (Icc 0 T))
    {K : Set (EuclideanSpace ℝ I)} (hK : IsCompact K) (fallback : K) (f : EuclideanSpace ℝ I → ℝ)
    (hf : ∀ x ∈ K, ContDiffAt ℝ 1 f x) (i : I) :
    let X := fun (t : ℝ≥0) (ω : Ω) => WithLp.toLp 2 (fun k : I => A k t ω + ∑ j : J,
      itoIntegralProcess (η k j) hT ((coordinateFamily hB).isBrownian j) hUsual t ω)
    let W := fun (t : ℝ≥0) (ω : Ω) =>
      fderiv ℝ f (restrictState fallback (X (min t T) ω) : EuclideanSpace ℝ I) (EuclideanSpace.basisFun I ℝ i)
    (∀ᵐ ω ∂μ, ∀ t ≤ T, X t ω ∈ K) →
      IsStronglyProgressive filtration W ∧
      (∀ᵐ ω ∂μ, ContinuousOn (fun t => W t ω) (Icc 0 T)) ∧
      (∃ C : ℝ, ∀ t ≤ T, ∀ ω, |W t ω| ≤ C) := by
  intro X W hRange
  let e := EuclideanSpace.basisFun I ℝ i
  let D (x : EuclideanSpace ℝ I) := fderiv ℝ f x e
  have hD : ContinuousOn D K :=
    (show ContinuousOn (fderiv ℝ f) K from fun x hx =>
      ((hf x hx).continuousAt_fderiv (by decide)).continuousWithinAt).clm_apply continuousOn_const
  let M (k : I) (j : J) := itoIntegralProcess (η k j) hT ((coordinateFamily hB).isBrownian j) hUsual
  have hM (k : I) (j : J) : IsStronglyProgressive filtration (M k j) :=
    (itoIntegralProcess_stronglyAdapted (η k j) hT ((coordinateFamily hB).isBrownian j)
      hUsual).isStronglyProgressive_of_continuous
        (itoIntegralProcess_continuous (η k j) hT ((coordinateFamily hB).isBrownian j) hUsual)
  have hRow (k : I) : IsStronglyProgressive filtration
      (fun t ω => A k t ω + ∑ j : J, M k j t ω) :=
    (hAp k).add (IsStronglyProgressive.finsetSum (s := Finset.univ) (fun j _ => hM k j))
  have hAmeas (k : I) (t : ℝ≥0) (_ : t ≤ T) : AEStronglyMeasurable (A k t) μ :=
    (((hAp k).stronglyAdapted t).mono (filtration.le t)).aestronglyMeasurable
  obtain ⟨_, hXc⟩ := measurable_continuousOn_euclidean_ito_rows
    hB hT hUsual η A hAmeas hAc
  refine ⟨?_, ?_, ?_⟩
  · intro t
    let _ : MeasurableSpace Ω := filtration t
    let cut (p : Iic t × Ω) : Iic t × Ω :=
      (⟨min (p.1 : ℝ≥0) T, mem_Iic.2
        ((min_le_left (p.1 : ℝ≥0) T).trans (mem_Iic.1 p.1.property))⟩, p.2)
    have hcut : Measurable cut :=
      ((measurable_subtype_coe.comp measurable_fst).min measurable_const).subtype_mk.prodMk
        measurable_snd
    have hMeas : Measurable (fun p : Iic t × Ω => X (min (p.1 : ℝ≥0) T) p.2) := by
      apply (MeasurableEquiv.toLp 2 (I → ℝ)).measurable.comp
      apply measurable_pi_lambda
      intro k
      exact ((hRow k t).comp_measurable hcut).measurable
    let Y (p : Iic t × Ω) : K := restrictState fallback (X (min (p.1 : ℝ≥0) T) p.2)
    have hY : Measurable Y := (measurable_restrictState hK.isClosed.measurableSet fallback).comp hMeas
    exact (hD.domRestrict.measurable.comp hY).stronglyMeasurable
  · filter_upwards [hXc, hRange] with ω hω hr
    have hComp := hD.comp hω (fun t ht => hr t ht.2)
    refine hComp.congr fun t ht => ?_
    change D (restrictState fallback (X (min t T) ω) : EuclideanSpace ℝ I) = D (X t ω)
    rw [min_eq_left ht.2, coe_restrictState_of_mem fallback (hr t ht.2)]
  · obtain ⟨C, hC⟩ := hK.bddAbove_image hD.abs
    exact ⟨C, fun t _ ω => hC ⟨restrictState fallback (X (min t T) ω), (restrictState fallback _).property, rfl⟩⟩

end AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoEuclideanGradientWeights
