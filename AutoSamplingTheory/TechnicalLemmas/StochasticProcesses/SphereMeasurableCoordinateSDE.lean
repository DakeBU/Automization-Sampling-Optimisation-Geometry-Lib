import AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ProgressiveCoefficientBounds
import AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.SphereCoordinateSDE
import AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.SphereMeasurableWeakForward

namespace AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.SphereMeasurableCoordinateSDE

open Filter MeasureTheory ProbabilityTheory Set
open scoped BigOperators NNReal Topology
open BrownianMotion ProgressiveL2 EuclideanBrownianCoordinates ItoIntegralProcess
  ProgressiveDriftIntegral SphereCoordinateSDE SphereMeasurableWeakForward ProgressiveCoefficientBounds
open AutoSamplingTheory.TechnicalLemmas.Geometry.SphereProjectedNoise
  AutoSamplingTheory.TechnicalLemmas.Geometry.SphereDiffusionGenerator

variable {I : Type*} [Fintype I] [DecidableEq I]
local notation "E" => EuclideanSpace ℝ I
local notation "S" => Metric.sphere (0 : E) 1

/-- The progressive square-integrable representative of the projected
coordinate noise on a finite horizon. -/
noncomputable def sphereMeasurableNoiseIntegrand
    {Ω : Type*} [MeasurableSpace Ω]
    {filtration : Filtration ℝ≥0 (inferInstance : MeasurableSpace Ω)}
    {μ : Measure Ω} [IsFiniteMeasure μ] (T : ℝ≥0)
    (X : ℝ≥0 → Ω → S) (hX : Measurable (Function.uncurry X))
    (hProgressive : IsStronglyProgressive filtration X)
    (temperature : ℝ≥0 → ℝ) (hTemperature : Measurable temperature)
    (hBound : ∃ C : ℝ, ∀ t ≤ T, ‖temperature t‖ ≤ C) (i j : I) :
    ProgressiveL2Integrand filtration μ T := by
  let L (k : I) : E →L[ℝ] ℝ := PiLp.proj (p := 2) (𝕜 := ℝ) (β := fun _ : I => ℝ) k
  let c₀ (w : S) : ℝ := (projectedNoiseColumn j (w : E)) i
  let c (q : ℝ≥0 × S) : ℝ := Real.sqrt (2 * temperature q.1) * c₀ q.2
  have hState : Continuous (fun w : S => (w : E)) := continuous_subtype_val
  have hProjected : Continuous (fun w : S => projectedNoiseColumn j (w : E)) :=
    continuous_const.sub (((L j).continuous.comp hState).smul hState)
  have hC₀ : Continuous c₀ := (L i).continuous.comp hProjected
  have hRoot : Measurable (fun q : ℝ≥0 × S => Real.sqrt (2 * temperature q.1)) :=
    Real.continuous_sqrt.measurable.comp (measurable_const.mul (hTemperature.comp measurable_fst))
  have hc : Measurable c := hRoot.mul (hC₀.measurable.comp measurable_snd)
  have hCompact : IsCompact (univ : Set S) :=
    (isCompact_iff_compactSpace.mp (isCompact_sphere (0 : E) 1)).isCompact_univ
  have hC : ∃ C : ℝ, ∀ t ≤ T, ∀ w, ‖c (t, w)‖ ≤ C := by
    obtain ⟨C₁, h₁⟩ := hBound
    obtain ⟨C₂, h₂⟩ := hCompact.bddAbove_image hC₀.norm.continuousOn
    refine ⟨Real.sqrt (2 * C₁) * C₂, fun t ht w => ?_⟩
    have htemp : temperature t ≤ C₁ :=
      (le_abs_self (temperature t)).trans (by simpa only [Real.norm_eq_abs] using h₁ t ht)
    have hs : ‖Real.sqrt (2 * temperature t)‖ ≤ Real.sqrt (2 * C₁) := by
      rw [Real.norm_of_nonneg (Real.sqrt_nonneg _)]
      exact Real.sqrt_le_sqrt (by linarith)
    change ‖Real.sqrt (2 * temperature t) * c₀ w‖ ≤ _
    rw [norm_mul]
    exact mul_le_mul hs (h₂ ⟨w, mem_univ w, rfl⟩) (norm_nonneg _) (Real.sqrt_nonneg _)
  have h := bounded_measurable_coefficient_along_progressive_process
    (μ := μ) X hX hProgressive c hc T 2 hC
  exact ⟨fun t ω => c (t, X t ω), h.1, h.2.2⟩

/-- The constructed integrand has the specified coordinate coefficient at
every time and sample. -/
theorem sphereMeasurableNoiseIntegrand_process
    {Ω : Type*} [MeasurableSpace Ω]
    {filtration : Filtration ℝ≥0 (inferInstance : MeasurableSpace Ω)}
    {μ : Measure Ω} [IsFiniteMeasure μ] (T : ℝ≥0)
    (X : ℝ≥0 → Ω → S) (hX : Measurable (Function.uncurry X))
    (hProgressive : IsStronglyProgressive filtration X)
    (temperature : ℝ≥0 → ℝ) (hTemperature : Measurable temperature)
    (hBound : ∃ C : ℝ, ∀ t ≤ T, ‖temperature t‖ ≤ C)
    (i j : I) (t : ℝ≥0) (ω : Ω) :
    (sphereMeasurableNoiseIntegrand (μ := μ) T X hX hProgressive temperature hTemperature hBound i j).process t ω =
      Real.sqrt (2 * temperature t) * (projectedNoiseColumn j (X t ω : E)) i :=
  rfl

/-- The canonical coordinate equations of a supplied sphere diffusion
imply the weak integral balance and almost-everywhere derivative of the
marginal expectation for a locally bounded measurable temperature. -/
theorem sphere_marginal_balance_of_measurable_temperature_equations
    {Ω : Type*} [MeasurableSpace Ω]
    {filtration : Filtration ℝ≥0 (inferInstance : MeasurableSpace Ω)}
    (P : ProbabilityMeasure Ω) {B : ℝ≥0 → Ω → E}
    (hB : IsStandardBrownianMotionWithFiltration B filtration (P : Measure Ω))
    (hUsual : SatisfiesUsualConditions filtration (P : Measure Ω))
    (X : ℝ≥0 → Ω → S) (hX : Measurable (Function.uncurry X))
    (hProgressive : IsStronglyProgressive filtration X)
    (u : ℝ≥0 → S → E) (hu : Continuous (Function.uncurry u))
    (temperature : ℝ≥0 → ℝ) (hTemperature : Measurable temperature)
    (hTemperatureBound : ∀ T : ℝ≥0, ∃ C : ℝ, ∀ t ≤ T, ‖temperature t‖ ≤ C)
    (hNonneg : ∀ t, 0 ≤ temperature t)
    (hEquation : ∀ (T : ℝ≥0) (hT : 0 < T), ∀ᵐ ω ∂(P : Measure Ω), ∀ t ≤ T, ∀ i : I,
      (X t ω : E) i = (X 0 ω : E) i +
        prefixIntegralProcess (fun v a => sphereDriftCoordinate u temperature i v (X v a)) t ω +
        ∑ j : I, itoIntegralProcess
          (sphereMeasurableNoiseIntegrand (μ := (P : Measure Ω)) T X hX hProgressive
            temperature hTemperature (hTemperatureBound T) i j) hT ((coordinateFamily hB).isBrownian j) hUsual t ω)
    (f : E → ℝ) (hf : ∀ w ∈ S, ContDiffAt ℝ 2 f w) :
    let hSlice (t : ℝ≥0) : Measurable (X t) := hX.comp (measurable_const.prodMk measurable_id)
    let ρ (t : ℝ≥0) := P.map (hSlice t).aemeasurable
    let F (t : ℝ) := ∫ w : S, f w ∂(ρ t.toNNReal : Measure S)
    let B (t : ℝ) := ∫ w : S, -fderiv ℝ f w (u t.toNNReal w) +
      temperature t.toNNReal * sphereLaplacian f w ∂(ρ t.toNNReal : Measure S)
    LocallyIntegrable B volume ∧
      (∀ a b : ℝ≥0, F b - F a = ∫ v in (a : ℝ)..(b : ℝ), B v) ∧
      (∀ T : ℝ≥0, AbsolutelyContinuousOnInterval F 0 (T : ℝ)) ∧
      (∀ᵐ t ∂volume.restrict (Ioi (0 : ℝ)), HasDerivAt F (B t) t) := by
  apply sphere_marginal_balance_of_measurable_temperature_rows P hB hUsual X hX
    u hu temperature hTemperature hTemperatureBound hNonneg ?_ f hf
  intro T hT
  let η (i j : I) := sphereMeasurableNoiseIntegrand (μ := (P : Measure Ω)) T X hX hProgressive
    temperature hTemperature (hTemperatureBound T) i j
  let b (i : I) (t : ℝ≥0) (ω : Ω) := sphereDriftCoordinate u temperature i t (X t ω)
  let L (i : I) : E →L[ℝ] ℝ := PiLp.proj (p := 2) (𝕜 := ℝ) (β := fun _ : I => ℝ) i
  have : CompactSpace S := isCompact_iff_compactSpace.mp (isCompact_sphere _ _)
  have hDrift (i : I) :
      IsStronglyProgressive filtration (b i) ∧
        ∀ ω, Integrable (fun t => b i t ω) (TimeMeasure.upTo T) := by
    let c (q : ℝ≥0 × S) := sphereDriftCoordinate u temperature i q.1 q.2
    let c₀ (q : ℝ≥0 × S) := (L i) (u q.1 q.2)
    let c₁ (w : S) := ((Fintype.card I - 1 : ℕ) : ℝ) * (L i) (w : E)
    have h₀ : Continuous c₀ := (L i).continuous.comp hu
    have h₁ : Continuous c₁ :=
      continuous_const.mul ((L i).continuous.comp continuous_subtype_val)
    have heq : c = fun q => -c₀ q - temperature q.1 * c₁ q.2 := by
      funext q
      simp only [c, c₀, c₁, sphereDriftCoordinate, PiLp.sub_apply, PiLp.neg_apply,
        PiLp.smul_apply, smul_eq_mul, mul_assoc]
      rfl
    have hc : Measurable c := by
      rw [heq]
      exact h₀.measurable.neg.sub ((hTemperature.comp measurable_fst).mul
        (h₁.measurable.comp measurable_snd))
    have hcompact : IsCompact (Icc (0 : ℝ≥0) T ×ˢ (univ : Set S)) :=
      isCompact_Icc.prod isCompact_univ
    obtain ⟨C₀, hC₀⟩ := hcompact.bddAbove_image h₀.norm.continuousOn
    obtain ⟨C₁, hC₁⟩ := (isCompact_univ (X := S)).bddAbove_image h₁.norm.continuousOn
    obtain ⟨C₂, hC₂⟩ := hTemperatureBound T
    have hC₂pos : 0 ≤ C₂ := (norm_nonneg _).trans (hC₂ 0 bot_le)
    have hBound : ∃ C : ℝ, ∀ t ≤ T, ∀ w, ‖c (t, w)‖ ≤ C := by
      refine ⟨C₀ + C₂ * C₁, fun t ht w => ?_⟩
      rw [heq]
      calc
        ‖-c₀ (t, w) - temperature t * c₁ w‖ ≤
            ‖c₀ (t, w)‖ + ‖temperature t‖ * ‖c₁ w‖ := by
          simpa only [norm_neg, norm_mul] using norm_sub_le (-c₀ (t, w)) (temperature t * c₁ w)
        _ ≤ C₀ + C₂ * C₁ :=
          add_le_add (hC₀ ⟨(t,w), ⟨⟨bot_le, ht⟩, mem_univ w⟩, rfl⟩)
            (mul_le_mul (hC₂ t ht) (hC₁ ⟨w, mem_univ w, rfl⟩) (norm_nonneg _) hC₂pos)
    have h := bounded_measurable_coefficient_along_progressive_process
      (μ := (P : Measure Ω)) X hX hProgressive c hc T 1 hBound
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

end AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.SphereMeasurableCoordinateSDE
