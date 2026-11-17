import AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.CompactProgressiveCoefficients
import AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.SphereWeakForward

namespace AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.SphereCoordinateSDE

open Filter MeasureTheory ProbabilityTheory Set
open scoped BigOperators NNReal
open BrownianMotion ProgressiveL2 EuclideanBrownianCoordinates ItoIntegralProcess
  ProgressiveDriftIntegral SphereWeakForward CompactProgressiveCoefficients
open AutoSamplingTheory.TechnicalLemmas.Geometry.SphereProjectedNoise
  AutoSamplingTheory.TechnicalLemmas.Geometry.SphereDiffusionGenerator

variable {I : Type*} [Fintype I] [DecidableEq I]
local notation "E" => EuclideanSpace ℝ I
local notation "S" => Metric.sphere (0 : E) 1

/-- The drift coordinate for the unit-sphere equation in ambient space. -/
noncomputable def sphereDriftCoordinate
    (u : ℝ≥0 → S → E) (temperature : ℝ≥0 → ℝ) (i : I) (t : ℝ≥0) (w : S) : ℝ :=
  (-u t w - (temperature t * ((Fintype.card I - 1 : ℕ) : ℝ)) • (w : E)) i

/-- The progressive square-integrable representative of the projected
coordinate noise on a finite horizon. -/
noncomputable def sphereNoiseIntegrand
    {Ω : Type*} [MeasurableSpace Ω]
    {filtration : Filtration ℝ≥0 (inferInstance : MeasurableSpace Ω)}
    {μ : Measure Ω} [IsFiniteMeasure μ] (T : ℝ≥0)
    (X : ℝ≥0 → Ω → S) (hX : Measurable (Function.uncurry X))
    (hProgressive : IsStronglyProgressive filtration X)
    (temperature : ℝ≥0 → ℝ) (hTemperature : Continuous temperature) (i j : I) :
    ProgressiveL2Integrand filtration μ T := by
  let L (k : I) : E →L[ℝ] ℝ := PiLp.proj (p := 2) (𝕜 := ℝ) (β := fun _ : I => ℝ) k
  let c (q : ℝ≥0 × S) : ℝ :=
    Real.sqrt (2 * temperature q.1) * (projectedNoiseColumn j (q.2 : E)) i
  have hState : Continuous (fun q : ℝ≥0 × S => (q.2 : E)) :=
    continuous_subtype_val.comp continuous_snd
  have hProjected : Continuous (fun q : ℝ≥0 × S => projectedNoiseColumn j (q.2 : E)) :=
    continuous_const.sub (((L j).continuous.comp hState).smul hState)
  have hScale : Continuous (fun q : ℝ≥0 × S => Real.sqrt (2 * temperature q.1)) :=
    Real.continuous_sqrt.comp ((continuous_const (y := (2 : ℝ))).mul
      (hTemperature.comp continuous_fst))
  have hc : Continuous c := hScale.mul ((L i).continuous.comp hProjected)
  letI : CompactSpace S := isCompact_iff_compactSpace.mp (isCompact_sphere _ _)
  have h := continuous_coefficient_along_compact_process (μ := μ) X hX hProgressive c hc T 2
  exact ⟨fun t ω => c (t, X t ω), h.1, h.2.2⟩

/-- The constructed integrand has the specified coordinate coefficient at
every time and sample. -/
theorem sphereNoiseIntegrand_process
    {Ω : Type*} [MeasurableSpace Ω]
    {filtration : Filtration ℝ≥0 (inferInstance : MeasurableSpace Ω)}
    {μ : Measure Ω} [IsFiniteMeasure μ] (T : ℝ≥0)
    (X : ℝ≥0 → Ω → S) (hX : Measurable (Function.uncurry X))
    (hProgressive : IsStronglyProgressive filtration X)
    (temperature : ℝ≥0 → ℝ) (hTemperature : Continuous temperature)
    (i j : I) (t : ℝ≥0) (ω : Ω) :
    (sphereNoiseIntegrand (μ := μ) T X hX hProgressive temperature hTemperature i j).process t ω =
      Real.sqrt (2 * temperature t) * (projectedNoiseColumn j (X t ω : E)) i :=
  rfl

/-- The canonical coordinate equations of a supplied sphere diffusion
imply the weak evolution of the expectation of every smooth test. -/
theorem hasDerivWithinAt_sphere_expectation_of_coordinate_equations
    {Ω : Type*} [MeasurableSpace Ω]
    {filtration : Filtration ℝ≥0 (inferInstance : MeasurableSpace Ω)}
    (P : ProbabilityMeasure Ω) {B : ℝ≥0 → Ω → E}
    (hB : IsStandardBrownianMotionWithFiltration B filtration (P : Measure Ω))
    (hUsual : SatisfiesUsualConditions filtration (P : Measure Ω))
    (X : ℝ≥0 → Ω → S) (hX : Measurable (Function.uncurry X))
    (hProgressive : IsStronglyProgressive filtration X)
    (hPaths : ∀ᵐ ω ∂(P : Measure Ω), Continuous (fun t => X t ω))
    (u : ℝ≥0 → S → E) (hu : Continuous (Function.uncurry u))
    (temperature : ℝ≥0 → ℝ) (hTemperature : Continuous temperature)
    (hNonneg : ∀ t, 0 ≤ temperature t)
    (hEquation : ∀ (T : ℝ≥0) (hT : 0 < T), ∀ᵐ ω ∂(P : Measure Ω), ∀ t ≤ T, ∀ i : I,
      (X t ω : E) i = (X 0 ω : E) i +
        prefixIntegralProcess (fun v a => sphereDriftCoordinate u temperature i v (X v a)) t ω +
        ∑ j : I, itoIntegralProcess
          (sphereNoiseIntegrand (μ := (P : Measure Ω)) T X hX hProgressive
            temperature hTemperature i j) hT ((coordinateFamily hB).isBrownian j) hUsual t ω)
    (f : E → ℝ) (hf : ∀ w ∈ S, ContDiffAt ℝ 2 f w) (s : ℝ≥0) :
    HasDerivWithinAt (fun t : ℝ => ∫ ω, f (X t.toNNReal ω) ∂(P : Measure Ω))
      (∫ ω, -fderiv ℝ f (X s ω) (u s (X s ω)) + temperature s * sphereLaplacian f (X s ω)
        ∂(P : Measure Ω)) (Ici 0) (s : ℝ) := by
  apply hasDerivWithinAt_sphere_expectation_of_ito_rows P hB hUsual X hX hPaths
    u hu temperature hTemperature hNonneg ?_ f hf s
  intro T hT
  let η (i j : I) := sphereNoiseIntegrand (μ := (P : Measure Ω)) T X hX hProgressive
    temperature hTemperature i j
  let b (i : I) (t : ℝ≥0) (ω : Ω) := sphereDriftCoordinate u temperature i t (X t ω)
  let L (i : I) : E →L[ℝ] ℝ := PiLp.proj (p := 2) (𝕜 := ℝ) (β := fun _ : I => ℝ) i
  letI : CompactSpace S := isCompact_iff_compactSpace.mp (isCompact_sphere _ _)
  have hDrift (i : I) :
      IsStronglyProgressive filtration (b i) ∧
        ∀ ω, Integrable (fun t => b i t ω) (TimeMeasure.upTo T) := by
    let c (q : ℝ≥0 × S) := sphereDriftCoordinate u temperature i q.1 q.2
    have hState : Continuous (fun q : ℝ≥0 × S => (q.2 : E)) :=
      continuous_subtype_val.comp continuous_snd
    have hTemperatureFactor : Continuous (fun q : ℝ≥0 × S =>
        temperature q.1 * ((Fintype.card I - 1 : ℕ) : ℝ)) :=
      (hTemperature.comp continuous_fst).mul continuous_const
    have hc : Continuous c :=
      (L i).continuous.comp (hu.neg.sub (hTemperatureFactor.smul hState))
    have h := continuous_coefficient_along_compact_process
      (μ := (P : Measure Ω)) X hX hProgressive c hc T 1
    exact ⟨h.1, h.2.1⟩
  refine ⟨η, (fun ω i => (X 0 ω : E) i), b, ?_, (fun i => (hDrift i).1),
    (fun i => Eventually.of_forall (hDrift i).2), ?_, ?_, ?_⟩
  · intro i
    exact ((L i).continuous.comp continuous_subtype_val).comp_stronglyMeasurable
      (hProgressive.stronglyAdapted 0)
  · filter_upwards [hEquation T hT] with ω hω t ht
    ext i
    exact (hω t ht i).symm
  · exact Eventually.of_forall fun ω t _ => by
      ext i
      rfl
  · exact Eventually.of_forall fun ω t _ j => by
      ext i
      change (η i j).process t ω = Real.sqrt (2 * temperature t) *
        (projectedNoiseColumn j (X t ω : E)) i
      rfl

end AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.SphereCoordinateSDE
