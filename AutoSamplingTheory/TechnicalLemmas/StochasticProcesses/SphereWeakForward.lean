import AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.SphereItoFormula
import AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.TimeMeasureRealBridge
import AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.WeakMartingaleEvolution

namespace AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.SphereWeakForward

open Filter MeasureTheory ProbabilityTheory Set
open scoped BigOperators NNReal
open BrownianMotion ProgressiveL2 EuclideanBrownianCoordinates ItoIntegralProcess
  ProgressiveDriftIntegral SphereItoFormula TimeMeasureRealBridge WeakMartingaleEvolution
open AutoSamplingTheory.TechnicalLemmas.Geometry.SphereProjectedNoise
  AutoSamplingTheory.TechnicalLemmas.Geometry.SphereDiffusionGenerator

/-- A sphere-valued process with the specified integrated Brownian equations
on each positive horizon satisfies the weak forward equation for smooth tests. -/
theorem hasDerivWithinAt_sphere_expectation_of_ito_rows
    {Ω I : Type*} [MeasurableSpace Ω] [Fintype I] [DecidableEq I]
    {filtration : Filtration ℝ≥0 (inferInstance : MeasurableSpace Ω)}
    (P : ProbabilityMeasure Ω) {B : ℝ≥0 → Ω → EuclideanSpace ℝ I}
    (hB : IsStandardBrownianMotionWithFiltration B filtration (P : Measure Ω))
    (hUsual : SatisfiesUsualConditions filtration (P : Measure Ω))
    (X : ℝ≥0 → Ω → Metric.sphere (0 : EuclideanSpace ℝ I) 1)
    (hX : Measurable (Function.uncurry X))
    (hPaths : ∀ᵐ ω ∂(P : Measure Ω), Continuous (fun t => X t ω))
    (u : ℝ≥0 → Metric.sphere (0 : EuclideanSpace ℝ I) 1 → EuclideanSpace ℝ I)
    (hu : Continuous (Function.uncurry u))
    (temperature : ℝ≥0 → ℝ) (hTemperature : Continuous temperature)
    (hNonneg : ∀ t, 0 ≤ temperature t)
    (hEquation : ∀ (T : ℝ≥0) (hT : 0 < T),
      ∃ (η : I → I → ProgressiveL2Integrand filtration (P : Measure Ω) T)
        (x : Ω → I → ℝ) (b : I → ℝ≥0 → Ω → ℝ),
        (∀ i, StronglyMeasurable[filtration 0] (fun ω => x ω i)) ∧
        (∀ i, IsStronglyProgressive filtration (b i)) ∧
        (∀ i, ∀ᵐ ω ∂(P : Measure Ω), Integrable (fun t => b i t ω) (TimeMeasure.upTo T)) ∧
        (∀ᵐ ω ∂(P : Measure Ω), ∀ t ≤ T,
          (WithLp.toLp 2 (fun i : I => x ω i + prefixIntegralProcess (b i) t ω +
            ∑ j : I, itoIntegralProcess (η i j) hT ((coordinateFamily hB).isBrownian j) hUsual t ω) :
              EuclideanSpace ℝ I) = (X t ω : EuclideanSpace ℝ I)) ∧
        (∀ᵐ ω ∂(P : Measure Ω), ∀ t ≤ T, WithLp.toLp 2 (fun i => b i t ω) =
          -u t (X t ω) - (temperature t * ((Fintype.card I - 1 : ℕ) : ℝ)) •
            (X t ω : EuclideanSpace ℝ I)) ∧
        (∀ᵐ ω ∂(P : Measure Ω), ∀ t ≤ T, ∀ j : I, WithLp.toLp 2 (fun i => (η i j).process t ω) =
          Real.sqrt (2 * temperature t) • projectedNoiseColumn j (X t ω)))
    (f : EuclideanSpace ℝ I → ℝ)
    (hf : ∀ w ∈ Metric.sphere (0 : EuclideanSpace ℝ I) 1, ContDiffAt ℝ 2 f w)
    (s : ℝ≥0) :
    HasDerivWithinAt (fun t : ℝ => ∫ ω, f (X t.toNNReal ω) ∂(P : Measure Ω))
      (∫ ω, -fderiv ℝ f (X s ω) (u s (X s ω)) + temperature s * sphereLaplacian f (X s ω)
        ∂(P : Measure Ω)) (Ici 0) (s : ℝ) := by
  obtain ⟨ω₀⟩ := nonempty_of_isProbabilityMeasure (P : Measure Ω)
  let E := EuclideanSpace ℝ I
  let S := Metric.sphere (0 : E) 1
  have : CompactSpace S := isCompact_iff_compactSpace.mp (isCompact_sphere _ _)
  let A (t : ℝ≥0) (w : S) : ℝ :=
    -fderiv ℝ f w (u t w) + temperature t * sphereLaplacian f w
  have hg : Continuous (fun w : S => f (w : E)) := continuous_iff_continuousAt.2 fun w =>
    (hf w w.property).continuousAt.comp continuous_subtype_val.continuousAt
  have hD : Continuous (fun w : S => fderiv ℝ f (w : E)) :=
    continuous_iff_continuousAt.2 fun w =>
      ((hf w w.property).continuousAt_fderiv (by decide)).comp continuous_subtype_val.continuousAt
  have hH : Continuous (fun w : S => fderiv ℝ (fderiv ℝ f) (w : E)) :=
    continuous_iff_continuousAt.2 fun w =>
      (((hf w w.property).fderiv_right (m := 1) (by decide)).continuousAt_fderiv
        (by decide)).comp continuous_subtype_val.continuousAt
  have hTrace : Continuous (fun w : S => ∑ j : I,
      fderiv ℝ (fderiv ℝ f) (w : E) (projectedNoiseColumn j w) (projectedNoiseColumn j w)) := by
    apply continuous_finsetSum
    intro j _
    let L : E →L[ℝ] ℝ := PiLp.proj (p := 2) (𝕜 := ℝ) (β := fun _ : I => ℝ) j
    have hp : Continuous (fun w : S => projectedNoiseColumn j (w : E)) :=
      continuous_const.sub ((L.continuous.comp continuous_subtype_val).smul continuous_subtype_val)
    exact (hH.clm_apply hp).clm_apply hp
  have hLap : Continuous (fun w : S => sphereLaplacian f (w : E)) := by
    refine (hTrace.sub ((continuous_const (y := ((Fintype.card I - 1 : ℕ) : ℝ))).mul
      (hD.clm_apply continuous_subtype_val))).congr ?_
    intro w
    change (∑ j : I, fderiv ℝ (fderiv ℝ f) (w : E)
      (projectedNoiseColumn j w) (projectedNoiseColumn j w)) -
      ((Fintype.card I - 1 : ℕ) : ℝ) * fderiv ℝ f (w : E) (w : E) = _
    rw [sum_hessian_projectedNoiseColumn f (mem_sphere_zero_iff_norm.1 w.property)]
    rfl
  have hA : Continuous (Function.uncurry A) :=
    ((hD.comp continuous_snd).clm_apply hu).neg.add
      ((hTemperature.comp continuous_fst).mul (hLap.comp continuous_snd))
  apply hasDerivWithinAt_expectation_of_centered_balance P X hX hPaths
    (fun w : S => f (w : E)) hg A hA
  intro T
  by_cases hT : T = 0
  · subst T
    exact ⟨0, integrable_zero Ω ℝ _, integral_zero _ _,
      Eventually.of_forall fun _ => by simp⟩
  have hPos : 0 < T := bot_lt_iff_ne_bot.mpr hT
  obtain ⟨η, x, b, hx, hb, hbi, hEq, hbEq, hηEq⟩ := hEquation T hPos
  let Y (t : ℝ≥0) (ω : Ω) : E := WithLp.toLp 2 (fun i : I =>
    x ω i + prefixIntegralProcess (b i) t ω +
      ∑ j : I, itoIntegralProcess (η i j) hPos ((coordinateFamily hB).isBrownian j) hUsual t ω)
  have hYEq : ∀ᵐ ω ∂(P : Measure Ω), ∀ t ≤ T, Y t ω = (X t ω : E) := hEq
  have hSphere : ∀ᵐ ω ∂(P : Measure Ω), ∀ t ≤ T, Y t ω ∈ S :=
    hYEq.mono fun ω heq t ht => (heq t ht).symm ▸ (X t ω).property
  have hU : ∀ᵐ ω ∂(P : Measure Ω), ContinuousOn (fun t => u t (X t ω)) (Icc 0 T) :=
    hPaths.mono fun _ hω => (hu.comp (continuous_id.prodMk hω)).continuousOn
  have hDrift : ∀ᵐ ω ∂(P : Measure Ω), ∀ t ≤ T, WithLp.toLp 2 (fun i => b i t ω) =
      -u t (X t ω) - (temperature t * ((Fintype.card I - 1 : ℕ) : ℝ)) • Y t ω := by
    filter_upwards [hYEq, hbEq] with ω heq hcoeff t ht
    rw [heq t ht]
    exact hcoeff t ht
  have hColumns : ∀ᵐ ω ∂(P : Measure Ω), ∀ t ≤ T, ∀ j : I,
      WithLp.toLp 2 (fun i => (η i j).process t ω) =
      Real.sqrt (2 * temperature t) • projectedNoiseColumn j (Y t ω) := by
    filter_upwards [hYEq, hηEq] with ω heq hcoeff t ht j
    rw [heq t ht]
    exact hcoeff t ht j
  obtain ⟨M, hM, hM0, hIto⟩ := ito_formula_sphere_at_horizon hB hPos hUsual η x hx b hb hbi
    (X 0 ω₀) f hf (fun t ω => u t (X t ω)) hU temperature hTemperature.continuousOn
    (fun t _ => hNonneg t) hSphere hDrift hColumns
  have hmean := hM.setIntegral_eq (show 0 ≤ T from bot_le) MeasurableSet.univ
  rw [Measure.restrict_univ] at hmean
  simp only [hM0, integral_zero] at hmean
  refine ⟨M T, hM.integrable T, hmean.symm, ?_⟩
  filter_upwards [hYEq, hIto] with ω heq hω
  change f (Y T ω) - f (Y 0 ω) =
    (∫ t, -fderiv ℝ f (Y t ω) (u t (X t ω)) + temperature t * sphereLaplacian f (Y t ω)
      ∂(TimeMeasure.upTo T)) + M T ω at hω
  rw [heq T le_rfl, heq 0 bot_le] at hω
  rw [hω]
  apply congrArg (· + M T ω)
  calc
    _ = ∫ t, A t (X t ω) ∂(TimeMeasure.upTo T) := by
      apply integral_congr_ae
      filter_upwards [TimeMeasure.ae_mem_Ioc_zero_upTo T] with t ht
      simp only [heq t ht.2, A]
    _ = _ := by
      rw [← TimeMeasure.restrict_upTo_Ioc_zero T,
        integral_upTo_restrict_Ioc_eq_real (fun t => A t (X t ω)) (show 0 ≤ T from bot_le) le_rfl]
      apply intervalIntegral.integral_congr
      intro r hr
      change r ∈ uIcc (0 : ℝ) (T : ℝ) at hr
      rw [uIcc_of_le T.coe_nonneg] at hr
      simp only [realZeroExtension, if_pos hr.1]

end AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.SphereWeakForward
