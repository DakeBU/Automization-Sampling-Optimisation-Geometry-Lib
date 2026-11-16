import AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.WeakDiffusionLaw
import Mathlib.Probability.Martingale.Basic

namespace AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.WeakMartingaleEvolution

open Filter MeasureTheory ProbabilityTheory Set
open scoped NNReal Topology
open AutoSamplingTheory.TechnicalLemmas.Measure.WeakProbabilityIntegral
open AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.WeakDiffusionLaw

/-- The expectation of a continuous test of a compact-state process satisfies
the weak forward derivative when its pathwise increment has a continuous
drift and a centered integrable residual. The residual may be chosen separately
at each horizon. At time zero the derivative is from the right. -/
theorem hasDerivWithinAt_expectation_of_centered_balance
    {Ω E : Type*} [MeasurableSpace Ω] [TopologicalSpace E] [CompactSpace E]
    [SecondCountableTopology E] [MeasurableSpace E] [BorelSpace E]
    (P : ProbabilityMeasure Ω) (X : ℝ≥0 → Ω → E)
    (hX : Measurable (Function.uncurry X))
    (hpaths : ∀ᵐ ω ∂(P : Measure Ω), Continuous (fun t => X t ω))
    (g : E → ℝ) (hg : Continuous g)
    (A : ℝ≥0 → E → ℝ) (hA : Continuous (Function.uncurry A))
    (hbalance : ∀ t : ℝ≥0, ∃ Z : Ω → ℝ, Integrable Z (P : Measure Ω) ∧
      (∫ ω, Z ω ∂(P : Measure Ω)) = 0 ∧
      (∀ᵐ ω ∂(P : Measure Ω), g (X t ω) - g (X 0 ω) =
        (∫ v in (0 : ℝ)..(t : ℝ), A v.toNNReal (X v.toNNReal ω)) + Z ω))
    (s : ℝ≥0) :
    HasDerivWithinAt (fun t : ℝ => ∫ ω, g (X t.toNNReal ω) ∂(P : Measure Ω))
      (∫ ω, A s (X s ω) ∂(P : Measure Ω)) (Ici 0) (s : ℝ) := by
  let Y (t : ℝ) := X t.toNNReal
  let A' (t : ℝ) := A t.toNNReal
  have hY (t : ℝ) : Measurable (Y t) :=
    hX.comp (measurable_const.prodMk measurable_id)
  have hYpair : Measurable (Function.uncurry Y) :=
    hX.comp ((continuous_real_toNNReal.measurable.comp measurable_fst).prodMk measurable_snd)
  have hYpaths : ∀ᵐ ω ∂(P : Measure Ω), Continuous (fun t => Y t ω) :=
    hpaths.mono fun _ hω => hω.comp continuous_real_toNNReal
  have hA' : Continuous (Function.uncurry A') :=
    hA.comp ((continuous_real_toNNReal.comp continuous_fst).prodMk continuous_snd)
  have hAsection (t : ℝ) : Measurable (A' t) :=
    hA'.measurable.comp (measurable_const.prodMk measurable_id)
  let ν (t : ℝ) := P.map (hY t).aemeasurable
  have hν : Continuous ν := continuous_marginal_law_of_ae_continuous P Y hY hYpaths
  let F (t : ℝ) := ∫ ω, g (Y t ω) ∂(P : Measure Ω)
  let B (t : ℝ) := ∫ x, A' t x ∂(ν t : Measure E)
  have hB : Continuous B := continuous_integral_of_compact hA' hν
  have hmap (t : ℝ) {f : E → ℝ} (hf : Measurable f) :
      (∫ x, f x ∂(ν t : Measure E)) = ∫ ω, f (Y t ω) ∂(P : Measure Ω) := by
    rw [show (ν t : Measure E) = (P : Measure Ω).map (Y t) from ProbabilityMeasure.toMeasure_map ..]
    exact integral_map (hY t).aemeasurable hf.aestronglyMeasurable
  let gB := BoundedContinuousFunction.mkOfCompact ⟨g, hg⟩
  have hgi (t : ℝ) : Integrable (fun ω => g (Y t ω)) (P : Measure Ω) :=
    Integrable.of_bound (hg.measurable.comp (hY t)).aestronglyMeasurable ‖gB‖
      (ae_of_all _ fun ω => gB.norm_coe_le_norm (Y t ω))
  have hF (t : ℝ≥0) : F t = F 0 + ∫ v in (0 : ℝ)..(t : ℝ), B v := by
    let q := volume.restrict (uIoc (0 : ℝ) (t : ℝ))
    have : IsFiniteMeasure q := by
      apply isFiniteMeasure_restrict.2
      rw [Real.volume_uIoc]
      exact ENNReal.ofReal_ne_top
    have hcompact : IsCompact (uIcc (0 : ℝ) (t : ℝ) ×ˢ (univ : Set E)) :=
      isCompact_uIcc.prod isCompact_univ
    obtain ⟨C, hC⟩ := hcompact.bddAbove_image hA'.norm.continuousOn
    have hd : Integrable (Function.uncurry fun v ω => A' v (Y v ω)) (q.prod (P : Measure Ω)) := by
      have hm : Measurable (Function.uncurry fun v ω => A' v (Y v ω)) :=
        hA'.measurable.comp (measurable_fst.prodMk hYpair)
      apply Integrable.of_bound hm.aestronglyMeasurable C
      have hq : ∀ᵐ v ∂q, v ∈ uIoc (0 : ℝ) (t : ℝ) := ae_restrict_mem measurableSet_uIoc
      filter_upwards [Measure.quasiMeasurePreserving_fst.ae hq] with p hp
      exact hC ⟨(p.1, Y p.1 p.2), ⟨uIoc_subset_uIcc hp, mem_univ _⟩, rfl⟩
    obtain ⟨Z, hZi, hmean, hZ⟩ := hbalance t
    have hinc : ∀ᵐ ω ∂(P : Measure Ω),
        g (Y t ω) - g (Y 0 ω) =
          (∫ v in (0 : ℝ)..(t : ℝ), A' v (Y v ω)) + Z ω := by
      simpa [Y, A'] using hZ
    have h := weak_integral_balance_of_centered_increment P Y hY hg.measurable hAsection
      0 (t : ℝ) (hgi 0) (hgi t) hd hZi hmean hinc
    rw [hmap _ hg.measurable, hmap _ hg.measurable] at h
    exact eq_add_of_sub_eq' h
  have hF' (t : ℝ) (ht : t ∈ Ici (0 : ℝ)) : F t = F 0 + ∫ v in 0..t, B v := by
    have h := hF t.toNNReal
    rwa [Real.coe_toNNReal t ht] at h
  have hD := intervalIntegral.integral_hasDerivAt_right (hB.intervalIntegrable 0 (s : ℝ))
    hB.stronglyMeasurable.stronglyMeasurableAtFilter hB.continuousAt
  have hderiv : HasDerivWithinAt F (B s) (Ici 0) (s : ℝ) :=
    (hD.const_add (F 0)).hasDerivWithinAt.congr hF' (hF' _ s.coe_nonneg)
  have hvalue : B s = ∫ ω, A s (X s ω) ∂(P : Measure Ω) := by
    rw [show B s = ∫ x, A' s x ∂(ν s : Measure E) from rfl, hmap _ (hAsection _)]
    simp [Y, A']
  rw [hvalue] at hderiv
  exact hderiv

/-- The expectation of a continuous test of a compact-state process satisfies
the weak forward derivative when its pathwise increment has a continuous
drift and the increment of a martingale. -/
theorem hasDerivWithinAt_expectation_of_martingale_balance
    {Ω E : Type*} [MeasurableSpace Ω] [TopologicalSpace E] [CompactSpace E]
    [SecondCountableTopology E] [MeasurableSpace E] [BorelSpace E]
    (P : ProbabilityMeasure Ω) (X : ℝ≥0 → Ω → E)
    (hX : Measurable (Function.uncurry X))
    (hpaths : ∀ᵐ ω ∂(P : Measure Ω), Continuous (fun t => X t ω))
    (g : E → ℝ) (hg : Continuous g)
    (A : ℝ≥0 → E → ℝ) (hA : Continuous (Function.uncurry A))
    {ℱ : Filtration ℝ≥0 (inferInstance : MeasurableSpace Ω)}
    {M : ℝ≥0 → Ω → ℝ} (hM : Martingale M ℱ (P : Measure Ω))
    (hbalance : ∀ t : ℝ≥0, ∀ᵐ ω ∂(P : Measure Ω),
      g (X t ω) - g (X 0 ω) =
        (∫ v in (0 : ℝ)..(t : ℝ), A v.toNNReal (X v.toNNReal ω)) +
          (M t ω - M 0 ω))
    (s : ℝ≥0) :
    HasDerivWithinAt (fun t : ℝ => ∫ ω, g (X t.toNNReal ω) ∂(P : Measure Ω))
      (∫ ω, A s (X s ω) ∂(P : Measure Ω)) (Ici 0) (s : ℝ) := by
  refine hasDerivWithinAt_expectation_of_centered_balance P X hX hpaths g hg A hA ?_ s
  intro t
  have hMi := hM.integrable t
  have hM0 := hM.integrable 0
  refine ⟨fun ω => M t ω - M 0 ω, hMi.sub hM0, ?_, hbalance t⟩
  have hsame := hM.setIntegral_eq (show 0 ≤ t from bot_le) MeasurableSet.univ
  rw [Measure.restrict_univ] at hsame
  rw [integral_sub hMi hM0, hsame, sub_self]

end AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.WeakMartingaleEvolution
