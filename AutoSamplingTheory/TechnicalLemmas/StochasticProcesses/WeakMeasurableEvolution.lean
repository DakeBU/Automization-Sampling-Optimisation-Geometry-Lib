import AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.WeakDiffusionLaw
import Mathlib.MeasureTheory.Integral.IntervalIntegral.LebesgueDifferentiationThm
import Mathlib.MeasureTheory.Function.AbsolutelyContinuous

namespace AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.WeakMeasurableEvolution

open Filter MeasureTheory ProbabilityTheory Set
open scoped NNReal Topology
open AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.WeakDiffusionLaw

/-- Centered pathwise balances on every horizon give the two-time marginal
balance and the almost-everywhere weak derivative for a measurable generator
that is uniformly bounded in state on each finite time interval. -/
theorem marginal_balance_of_locally_bounded_generator
    {Ω S : Type*} [MeasurableSpace Ω] [TopologicalSpace S] [CompactSpace S]
    [SecondCountableTopology S] [MeasurableSpace S] [BorelSpace S]
    (P : ProbabilityMeasure Ω) (X : ℝ≥0 → Ω → S)
    (hX : Measurable (Function.uncurry X))
    (g : S → ℝ) (hg : Continuous g)
    (A : ℝ≥0 → S → ℝ) (hA : Measurable (Function.uncurry A))
    (hBound : ∀ T : ℝ≥0, ∃ C : ℝ, ∀ t ≤ T, ∀ w, ‖A t w‖ ≤ C)
    (hbalance : ∀ t : ℝ≥0, ∃ Z : Ω → ℝ, Integrable Z (P : Measure Ω) ∧
      (∫ ω, Z ω ∂(P : Measure Ω)) = 0 ∧
      (∀ᵐ ω ∂(P : Measure Ω), g (X t ω) - g (X 0 ω) =
        (∫ v in (0 : ℝ)..(t : ℝ), A v.toNNReal (X v.toNNReal ω)) + Z ω)) :
    let hSlice (t : ℝ≥0) : Measurable (X t) := hX.comp (measurable_const.prodMk measurable_id)
    let ρ (t : ℝ≥0) := P.map (hSlice t).aemeasurable
    let F (t : ℝ) := ∫ w, g w ∂(ρ t.toNNReal : Measure S)
    let B (t : ℝ) := ∫ w, A t.toNNReal w ∂(ρ t.toNNReal : Measure S)
    LocallyIntegrable B volume ∧
      (∀ a b : ℝ≥0, F b - F a = ∫ v in (a : ℝ)..(b : ℝ), B v) ∧
      (∀ T : ℝ≥0, AbsolutelyContinuousOnInterval F 0 (T : ℝ)) ∧
      (∀ᵐ t ∂volume.restrict (Ioi (0 : ℝ)), HasDerivAt F (B t) t) := by
  intro hSlice ρ F B
  let Y (t : ℝ) := X t.toNNReal
  let A' (t : ℝ) := A t.toNNReal
  have hY (t : ℝ) : Measurable (Y t) := hSlice t.toNNReal
  have hYpair : Measurable (Function.uncurry Y) :=
    hX.comp ((continuous_real_toNNReal.measurable.comp measurable_fst).prodMk measurable_snd)
  have hA' : Measurable (Function.uncurry A') :=
    hA.comp ((continuous_real_toNNReal.measurable.comp measurable_fst).prodMk measurable_snd)
  have hAsection (t : ℝ) : Measurable (A' t) :=
    hA'.comp (measurable_const.prodMk measurable_id)
  have hG : Measurable (Function.uncurry fun v ω => A' v (Y v ω)) :=
    hA'.comp (measurable_fst.prodMk hYpair)
  have hBmap (t : ℝ) : B t = ∫ ω, A' t (Y t ω) ∂(P : Measure Ω) := by
    change (∫ w, A' t w ∂(ρ t.toNNReal : Measure S)) = _
    rw [show (ρ t.toNNReal : Measure S) = (P : Measure Ω).map (Y t) from
      ProbabilityMeasure.toMeasure_map ..]
    exact integral_map (hY t).aemeasurable (hAsection t).aestronglyMeasurable
  have hBm : Measurable B := by
    rw [funext hBmap]
    exact hG.stronglyMeasurable.integral_prod_right.measurable
  have hBbound (T : ℝ≥0) : ∃ C : ℝ≥0, ∀ t : ℝ, t.toNNReal ≤ T → ‖B t‖ ≤ C := by
    obtain ⟨C, hC⟩ := hBound T
    refine ⟨C.toNNReal, fun t ht => ?_⟩
    rw [hBmap]
    have hnorm := norm_integral_le_of_norm_le_const (μ := (P : Measure Ω))
      (Eventually.of_forall fun ω => hC t.toNNReal ht (Y t ω))
    exact (show ‖∫ ω, A' t (Y t ω) ∂(P : Measure Ω)‖ ≤ C from by simpa using hnorm).trans
      (Real.le_coe_toNNReal C)
  have hLoc : LocallyIntegrable B volume := by
    rw [locallyIntegrable_iff]
    intro K hK
    obtain ⟨r, hr⟩ := hK.bddAbove
    obtain ⟨C, hC⟩ := hBbound r.toNNReal
    letI : IsFiniteMeasure (volume.restrict K) := isFiniteMeasure_restrict.2 (hK.measure_lt_top (μ := volume)).ne
    apply Integrable.of_bound hBm.aestronglyMeasurable (C : ℝ)
    filter_upwards [ae_restrict_mem hK.measurableSet] with t ht
    exact hC t (Real.toNNReal_le_toNNReal (hr ht))
  have hInt (a b : ℝ) : IntervalIntegrable B volume a b :=
    intervalIntegrable_iff.mpr
      ((hLoc.integrableOn_isCompact isCompact_uIcc).mono_set uIoc_subset_uIcc)
  let gB := BoundedContinuousFunction.mkOfCompact ⟨g, hg⟩
  have hgi (t : ℝ) : Integrable (fun ω => g (Y t ω)) (P : Measure Ω) :=
    Integrable.of_bound (hg.measurable.comp (hY t)).aestronglyMeasurable ‖gB‖
      (Eventually.of_forall fun ω => gB.norm_coe_le_norm (Y t ω))
  have hBase (t : ℝ≥0) : F t = F 0 + ∫ v in (0 : ℝ)..(t : ℝ), B v := by
    let ν := volume.restrict (uIoc (0 : ℝ) (t : ℝ))
    have : IsFiniteMeasure ν := by
      apply isFiniteMeasure_restrict.2
      rw [Real.volume_uIoc]
      exact ENNReal.ofReal_ne_top
    obtain ⟨C, hC⟩ := hBound t
    have hGi : Integrable (Function.uncurry fun v ω => A' v (Y v ω)) (ν.prod (P : Measure Ω)) := by
      apply Integrable.of_bound hG.aestronglyMeasurable C
      have hν : ∀ᵐ v ∂ν, v ∈ uIoc (0 : ℝ) (t : ℝ) := ae_restrict_mem measurableSet_uIoc
      filter_upwards [Measure.quasiMeasurePreserving_fst.ae hν] with z hz
      rw [uIoc_of_le t.coe_nonneg] at hz
      exact hC z.1.toNNReal (by simpa using Real.toNNReal_le_toNNReal hz.2) (Y z.1 z.2)
    obtain ⟨Z, hZi, hmean, hZ⟩ := hbalance t
    have hinc : ∀ᵐ ω ∂(P : Measure Ω),
        g (Y t ω) - g (Y 0 ω) =
          (∫ v in (0 : ℝ)..(t : ℝ), A' v (Y v ω)) + Z ω := by
      simpa [Y, A'] using hZ
    have h := weak_integral_balance_of_centered_increment P Y hY hg.measurable hAsection
      0 (t : ℝ) (hgi 0) (hgi t) hGi hZi hmean hinc
    exact eq_add_of_sub_eq' h
  have hTwo (a b : ℝ≥0) : F b - F a = ∫ v in (a : ℝ)..(b : ℝ), B v := by
    rw [← intervalIntegral.integral_interval_sub_left (hInt 0 b) (hInt 0 a), hBase a, hBase b]
    ring
  refine ⟨hLoc, hTwo, ?_, ?_⟩
  · intro T
    obtain ⟨C, hC⟩ := hBbound T
    have hLip : LipschitzOnWith C F (Icc (0 : ℝ) (T : ℝ)) := by
      rw [lipschitzOnWith_iff_dist_le_mul]
      intro x hx y hy
      have h := hTwo y.toNNReal x.toNNReal
      rw [Real.coe_toNNReal y hy.1, Real.coe_toNNReal x hx.1] at h
      have hBoundI : ∀ v ∈ uIoc y x, ‖B v‖ ≤ C := by
        intro v hv
        have hu : v ∈ uIcc y x := uIoc_subset_uIcc hv
        have hvT : v ≤ (T : ℝ) := hu.2.trans (max_le hy.2 hx.2)
        exact hC v (by simpa using Real.toNNReal_le_toNNReal hvT)
      rw [Real.dist_eq, h, ← Real.norm_eq_abs, Real.dist_eq]
      exact intervalIntegral.norm_integral_le_of_norm_le_const hBoundI
    apply LipschitzOnWith.absolutelyContinuousOnInterval
    rwa [uIcc_of_le T.coe_nonneg]
  · have hPositive : ∀ᵐ t ∂volume.restrict (Ioi (0 : ℝ)), 0 < t :=
      ae_restrict_mem measurableSet_Ioi
    filter_upwards [ae_restrict_of_ae (LocallyIntegrable.ae_hasDerivAt_integral hLoc), hPositive] with t ht ht0
    apply ((ht 0).const_add (F 0)).congr_of_eventuallyEq
    filter_upwards [Ioi_mem_nhds ht0] with r hr
    have h := hBase r.toNNReal
    simpa only [Real.coe_toNNReal r hr.le] using h

end AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.WeakMeasurableEvolution
