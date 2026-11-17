import AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoCompactEuclideanFormula
import AutoSamplingTheory.TechnicalLemmas.Geometry.SphereDiffusionGenerator
import Mathlib.MeasureTheory.Function.LocallyIntegrable

namespace AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.SphereItoFormula

open Filter MeasureTheory ProbabilityTheory Set
open scoped BigOperators NNReal
open BrownianMotion ProgressiveL2 EuclideanBrownianCoordinates ItoIntegralProcess
  ProgressiveDriftIntegral ItoInitializedDrift ItoEuclideanRowRegularity ItoCompactEuclideanFormula
open AutoSamplingTheory.TechnicalLemmas.Geometry.SphereProjectedNoise
  AutoSamplingTheory.TechnicalLemmas.Geometry.SphereDiffusionGenerator

/-- Apply the compact Euclidean Itô formula to an actual process on the unit
sphere and identify its generator from the projected columns and radial drift. -/
theorem ito_formula_sphere_at_horizon
    {Ω I : Type*} [MeasurableSpace Ω] [Fintype I] [DecidableEq I]
    {filtration : Filtration ℝ≥0 (inferInstance : MeasurableSpace Ω)}
    {μ : Measure Ω} [IsFiniteMeasure μ] {T : ℝ≥0}
    {B : ℝ≥0 → Ω → EuclideanSpace ℝ I}
    (hB : IsStandardBrownianMotionWithFiltration B filtration μ) (hT : 0 < T)
    (hUsual : SatisfiesUsualConditions filtration μ)
    (η : I → I → ProgressiveL2Integrand filtration μ T)
    (x : Ω → I → ℝ) (hx : ∀ i, StronglyMeasurable[filtration 0] (fun ω => x ω i))
    (b : I → ℝ≥0 → Ω → ℝ) (hb : ∀ i, IsStronglyProgressive filtration (b i))
    (hbi : ∀ i, ∀ᵐ ω ∂μ, Integrable (fun s => b i s ω) (TimeMeasure.upTo T))
    (fallback : Metric.sphere (0 : EuclideanSpace ℝ I) 1)
    (f : EuclideanSpace ℝ I → ℝ)
    (hf : ∀ w ∈ Metric.sphere (0 : EuclideanSpace ℝ I) 1, ContDiffAt ℝ 2 f w)
    (u : ℝ≥0 → Ω → EuclideanSpace ℝ I)
    (hu : ∀ᵐ ω ∂μ, ContinuousOn (fun s => u s ω) (Icc 0 T))
    (temperature : ℝ≥0 → ℝ) (hTemperature : ContinuousOn temperature (Icc 0 T))
    (hNonneg : ∀ t ≤ T, 0 ≤ temperature t) :
    let A := fun (i : I) (t : ℝ≥0) (ω : Ω) => x ω i + prefixIntegralProcess (b i) t ω
    let X := fun (t : ℝ≥0) (ω : Ω) => WithLp.toLp 2 (fun i : I => A i t ω + ∑ j : I,
      itoIntegralProcess (η i j) hT ((coordinateFamily hB).isBrownian j) hUsual t ω)
    (∀ᵐ ω ∂μ, ∀ t ≤ T, X t ω ∈ Metric.sphere 0 1) →
    (∀ᵐ ω ∂μ, ∀ t ≤ T, WithLp.toLp 2 (fun i => b i t ω) =
      -u t ω - (temperature t * ((Fintype.card I - 1 : ℕ) : ℝ)) • X t ω) →
    (∀ᵐ ω ∂μ, ∀ t ≤ T, ∀ j : I, WithLp.toLp 2 (fun i => (η i j).process t ω) =
      Real.sqrt (2 * temperature t) • projectedNoiseColumn j (X t ω)) →
    ∃ M : ℝ≥0 → Ω → ℝ, Martingale M filtration μ ∧ (∀ ω, M 0 ω = 0) ∧
      (∀ᵐ ω ∂μ, f (X T ω) - f (X 0 ω) =
        (∫ s, -fderiv ℝ f (X s ω) (u s ω) + temperature s * sphereLaplacian f (X s ω)
          ∂(TimeMeasure.upTo T)) + M T ω) := by
  intro A X hSphere hDrift hColumns
  have hK := isCompact_sphere (0 : EuclideanSpace ℝ I) 1
  obtain ⟨θ, _, hM, hM0, hIto⟩ :=
    ito_formula_compact_euclidean_at_horizon hB hT hUsual η x hx b hb hbi hK fallback f hf hSphere
  let M (s : ℝ≥0) (ω : Ω) := ∑ q : I × I,
    itoIntegralProcess (θ q) hT ((coordinateFamily hB).isBrownian q.2) hUsual s ω
  refine ⟨M, hM, hM0, ?_⟩
  have hA (i : I) := initialized_drift_progressive_continuous_boundedVariation
    (fun ω => x ω i) (hx i) (b i) (hb i) (hbi i)
  have hAmeas (i : I) (s : ℝ≥0) (_ : s ≤ T) : AEStronglyMeasurable (A i s) μ :=
    (((hA i).1.stronglyAdapted s).mono (filtration.le s)).aestronglyMeasurable
  obtain ⟨_, hXc⟩ := measurable_continuousOn_euclidean_ito_rows hB hT hUsual η A hAmeas
    (fun i => (hA i).2.2.mono fun _ h => h.1)
  filter_upwards [hIto, hSphere, hDrift, hColumns, hXc, hu] with ω hω hS hbω hηω hcX hU
  let ν := TimeMeasure.upTo T
  let v (s : ℝ≥0) := WithLp.toLp 2 (fun i => b i s ω)
  let σ (j : I) (s : ℝ≥0) := WithLp.toLp 2 (fun i => (η i j).process s ω)
  let D (s : ℝ≥0) := fderiv ℝ f (X s ω) (v s)
  let Q (s : ℝ≥0) := (1 / 2 : ℝ) * ∑ j : I,
    fderiv ℝ (fderiv ℝ f) (X s ω) (σ j s) (σ j s)
  have hMem : ∀ᵐ s ∂ν, s ∈ Icc (0 : ℝ≥0) T :=
    (TimeMeasure.ae_mem_Ioc_zero_upTo T).mono fun _ hs => ⟨hs.1.le, hs.2⟩
  have hRest : ν.restrict (Icc 0 T) = ν := Measure.restrict_eq_self_of_ae_mem hMem
  have hMaps : MapsTo (fun s => X s ω) (Icc 0 T) (Metric.sphere 0 1) :=
    fun _ hs => hS _ hs.2
  have hFirst : ContinuousOn (fun s => fderiv ℝ f (X s ω)) (Icc 0 T) :=
    (show ContinuousOn (fderiv ℝ f) (Metric.sphere 0 1) from fun w hw =>
      ((hf w hw).continuousAt_fderiv (by decide)).continuousWithinAt).comp hcX hMaps
  have hSecond : ContinuousOn (fun s => fderiv ℝ (fderiv ℝ f) (X s ω)) (Icc 0 T) :=
    (show ContinuousOn (fderiv ℝ (fderiv ℝ f)) (Metric.sphere 0 1) from fun w hw =>
      (((hf w hw).fderiv_right (m := 1) (by decide)).continuousAt_fderiv
        (by decide)).continuousWithinAt).comp hcX hMaps
  have hV : ContinuousOn v (Icc 0 T) := by
    have hDim : ContinuousOn (fun _ : ℝ≥0 => ((Fintype.card I - 1 : ℕ) : ℝ))
        (Icc 0 T) := continuousOn_const
    refine (hU.neg.sub ((hTemperature.mul hDim).smul hcX)).congr ?_
    exact fun s hs => hbω s hs.2
  have hσ (j : I) : ContinuousOn (σ j) (Icc 0 T) := by
    have hCol : ContinuousOn (fun s => projectedNoiseColumn j (X s ω)) (Icc 0 T) := by
      let L : EuclideanSpace ℝ I →L[ℝ] ℝ := PiLp.proj (p := 2) (𝕜 := ℝ)
        (β := fun _ : I => ℝ) j
      exact continuousOn_const.sub ((L.continuous.comp_continuousOn hcX).smul hcX)
    have hRoot : ContinuousOn (fun s => Real.sqrt (2 * temperature s)) (Icc 0 T) :=
      Real.continuous_sqrt.comp_continuousOn ((continuousOn_const (c := (2 : ℝ))).mul hTemperature)
    exact (hRoot.smul hCol).congr fun s hs => hηω s hs.2 j
  have hD : Integrable D ν := by
    rw [← hRest]
    exact (hFirst.clm_apply hV).integrableOn_compact isCompact_Icc
  have hQ : Integrable Q ν := by
    rw [← hRest]
    exact ((continuousOn_const (c := (1 / 2 : ℝ))).mul (continuousOn_finsetSum _ fun j _ =>
      (hSecond.clm_apply (hσ j)).clm_apply (hσ j))).integrableOn_compact isCompact_Icc
  change f (X T ω) - f (X 0 ω) =
    (∫ s, D s ∂ν) + (∫ s, Q s ∂ν) + M T ω at hω
  rw [hω, ← integral_add hD hQ]
  apply congrArg (· + M T ω)
  apply integral_congr_ae
  filter_upwards [hMem] with s hs
  have hUnit : ‖X s ω‖ = 1 := mem_sphere_zero_iff_norm.1 (hS s hs.2)
  simp only [D, Q, v, σ, hbω s hs.2, hηω s hs.2]
  exact ito_generator_eq_sphereLaplacian f hUnit (u s ω) (hNonneg s hs.2)

end AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.SphereItoFormula
