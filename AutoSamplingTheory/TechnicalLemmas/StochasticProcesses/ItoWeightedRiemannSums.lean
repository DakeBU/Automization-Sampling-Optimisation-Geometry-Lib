import AutoSamplingTheory.TechnicalLemmas.Analysis.PrefixIntegral
import AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoBoundedCellMultiplier
import AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.DyadicElementaryRefinement
import Mathlib.Topology.EMetricSpace.BoundedVariation

/-! # Weighted dyadic sums for time and completed Itô integrals -/

namespace AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoWeightedRiemannSums

open Filter MeasureTheory Set
open scoped NNReal ENNReal BigOperators
open AutoSamplingTheory.TechnicalLemmas.Analysis.PrefixIntegral
open FiniteTimeGrid SampledElementaryApproximation DyadicElementaryRefinement
open BrownianMotion ElementaryItoIntegral ElementaryItoL2 ProgressiveL2
  ItoIntegralProcess ItoTerminalCompletion ItoBoundedCellMultiplier

private noncomputable def grid (T : ℝ≥0) (level : ℕ) :=
  regularGridTimes (dyadicMesh T level) (2 ^ level)

private theorem grid_mono {T : ℝ≥0} (hT : 0 < T) (level : ℕ) : Monotone (grid T level) :=
  (regularGridTimes_strictMono (dyadicMesh_pos hT level) _).monotone

private theorem grid_le {T : ℝ≥0} (hT : 0 < T) (level : ℕ)
    (k : Fin (2 ^ level + 1)) : grid T level k ≤ T :=
  (grid_mono hT level (Fin.le_last k)).trans_eq (regularDyadic_last_time T level)

private noncomputable def sample (w : ℝ≥0 → ℝ) (T : ℝ≥0) (level : ℕ) (r : ℝ≥0) : ℝ :=
  ∑ i : Fin (2 ^ level), if r ∈ Ioc (grid T level i.castSucc) (grid T level i.succ)
    then w (grid T level i.castSucc) else 0

private theorem sample_value (w : ℝ≥0 → ℝ) {T : ℝ≥0} (hT : 0 < T)
    (level : ℕ) {r : ℝ≥0} {i : Fin (2 ^ level)}
    (hi : r ∈ Ioc (grid T level i.castSucc) (grid T level i.succ)) :
    sample w T level r = w (grid T level i.castSucc) := by
  have hr : 0 < r := (bot_le : 0 ≤ grid T level i.castSucc).trans_lt hi.1
  have hrT : r ≤ T := hi.2.trans (grid_le hT level i.succ)
  obtain ⟨j, _, hUnique⟩ := dyadic_activeCell hT level hr hrT
  rw [sample, Finset.sum_eq_single i]
  · exact if_pos hi
  · intro k _ hki
    apply if_neg
    intro hk
    exact hki ((hUnique k hk).trans (hUnique i hi).symm)
  · simp

private theorem sample_measurable (w : ℝ≥0 → ℝ) (T : ℝ≥0) (level : ℕ) :
    Measurable (sample w T level) := by
  unfold sample
  exact Finset.measurable_sum _ fun _ _ =>
    Measurable.ite measurableSet_Ioc measurable_const measurable_const

private theorem sample_bound (w : ℝ≥0 → ℝ) {T : ℝ≥0} (hT : 0 < T)
    (level : ℕ) {r : ℝ≥0} (hr : r ∈ Ioc 0 T)
    {C : ℝ} (hC : ∀ t ≤ T, |w t| ≤ C) : |sample w T level r| ≤ C := by
  obtain ⟨i, hi, _⟩ := dyadic_activeCell hT level hr.1 hr.2
  rw [sample_value w hT level hi]
  exact hC _ (grid_le hT level i.castSucc)

private theorem tendsto_sample (w : ℝ≥0 → ℝ) {T : ℝ≥0} (hT : 0 < T)
    (hw : ContinuousOn w (Icc 0 T)) {r : ℝ≥0} (hr : r ∈ Ioc 0 T) :
    Tendsto (fun level => sample w T level r) atTop (nhds (w r)) := by
  have hExists (level : ℕ) : ∃ i : Fin (2 ^ level),
      r ∈ Ioc (grid T level i.castSucc) (grid T level i.succ) :=
    (dyadic_activeCell hT level hr.1 hr.2).exists
  choose i hi using hExists
  let left (level : ℕ) := grid T level (i level).castSucc
  have hd (level : ℕ) : dist (left level) r ≤ (dyadicMesh T level : ℝ) := by
    have hright : grid T level (i level).succ = left level + dyadicMesh T level :=
      dyadic_activeCell_right (i level)
    have hl : left level ≤ r := (hi level).1.le
    have hup : r ≤ left level + dyadicMesh T level := (hi level).2.trans_eq hright
    rw [dist_comm, NNReal.dist_eq, abs_of_nonneg (sub_nonneg.mpr (by exact_mod_cast hl))]
    apply sub_le_iff_le_add.mpr
    exact_mod_cast (add_comm (left level) (dyadicMesh T level) ▸ hup)
  have hLeft : Tendsto left atTop (nhds r) := by
    rw [Metric.tendsto_nhds]
    intro epsilon he
    filter_upwards [eventually_dyadicMesh_lt T he] with level hmesh
    exact (hd level).trans_lt hmesh
  have hWithin : Tendsto left atTop (nhdsWithin r (Icc 0 T)) :=
    tendsto_nhdsWithin_iff.2 ⟨hLeft, Eventually.of_forall fun level =>
      ⟨bot_le, grid_le hT level (i level).castSucc⟩⟩
  have hW := (hw r ⟨hr.1.le, hr.2⟩).tendsto.comp hWithin
  refine (tendsto_congr' (Eventually.of_forall fun level => ?_)).2 hW
  exact sample_value w hT level (hi level)

private theorem prefix_sub_eq_Ioc {T s t : ℝ≥0} {b : ℝ≥0 → ℝ}
    (hb : Integrable b (TimeMeasure.upTo T)) (hst : s ≤ t) (htT : t ≤ T) :
    prefixIntegral b T t - prefixIntegral b T s =
      ∫ r in Ioc s t, b r ∂(TimeMeasure.upTo T) := by
  rw [prefixIntegral_eq_setIntegral, prefixIntegral_eq_setIntegral,
    min_eq_left htT, min_eq_left (hst.trans htT)]
  rw [← setIntegral_sdiff measurableSet_Iio hb.integrableOn (Iio_subset_Iio hst)]
  have hIco : Iio t \ Iio s = Ico s t := by
    ext r
    simp only [Set.mem_sdiff, mem_Iio, mem_Ico, not_lt]
    exact and_comm
  rw [hIco]
  apply setIntegral_congr_set
  have hne (a : ℝ≥0) : ∀ᵐ r ∂TimeMeasure.upTo T, r ≠ a := by
    rw [ae_iff]
    simp
  filter_upwards [hne s, hne t] with r hrs hrt
  exact propext ⟨fun h => ⟨lt_of_le_of_ne h.1 (Ne.symm hrs), h.2.le⟩,
    fun h => ⟨h.1.le, lt_of_le_of_ne h.2 hrt⟩⟩

/-- The variation of an integrable time primitive is bounded by the
terminal integral of the absolute density. -/
theorem boundedVariationOn_prefixIntegral
    {T : ℝ≥0} {b : ℝ≥0 → ℝ} (hb : Integrable b (TimeMeasure.upTo T)) :
    BoundedVariationOn (prefixIntegral b T) (Set.Icc 0 T) := by
  unfold BoundedVariationOn
  let P := prefixIntegral b T
  let V := prefixIntegral (fun t => |b t|) T
  refine ne_top_of_le_ne_top (b := ENNReal.ofReal (V T)) ENNReal.ofReal_ne_top ?_
  unfold eVariationOn
  apply iSup_le
  rintro ⟨n, u, hu, hmem⟩
  have hinc (i : ℕ) : 0 ≤ V (u (i + 1)) - V (u i) :=
    sub_nonneg.mpr (prefixIntegral_mono hb.abs (fun _ => abs_nonneg _) (hu (Nat.le_succ i)))
  have hcell (i : ℕ) : edist (P (u (i + 1))) (P (u i)) ≤
      ENNReal.ofReal (V (u (i + 1)) - V (u i)) := by
    have hmono := hu (Nat.le_succ i)
    have hT := (hmem (i + 1)).2
    rw [edist_dist, Real.dist_eq]
    apply ENNReal.ofReal_le_ofReal
    dsimp only [P, V]
    rw [prefix_sub_eq_Ioc hb hmono hT, prefix_sub_eq_Ioc hb.abs hmono hT]
    simpa only [Real.norm_eq_abs] using
      norm_integral_le_integral_norm b (μ := (TimeMeasure.upTo T).restrict (Ioc (u i) (u (i + 1))))
  have hV0 : 0 ≤ V (u 0) := by
    have h : V (0 : ℝ≥0) ≤ V (u 0) :=
      prefixIntegral_mono hb.abs (fun _ => abs_nonneg _) (show (0 : ℝ≥0) ≤ u 0 from bot_le)
    simpa only [V, prefixIntegral_zero] using h
  calc
    _ ≤ ∑ i ∈ Finset.range n, ENNReal.ofReal (V (u (i + 1)) - V (u i)) :=
      Finset.sum_le_sum (fun i _ => hcell i)
    _ = ENNReal.ofReal (∑ i ∈ Finset.range n, (V (u (i + 1)) - V (u i))) :=
      (ENNReal.ofReal_sum_of_nonneg (fun i _ => hinc i)).symm
    _ = ENNReal.ofReal (V (u n) - V (u 0)) := by
      rw [Finset.sum_range_sub (fun i => V (u i))]
    _ ≤ ENNReal.ofReal (V T) :=
      ENNReal.ofReal_le_ofReal ((sub_le_self _ hV0).trans
        (prefixIntegral_mono hb.abs (fun _ => abs_nonneg _) (hmem n).2))

#print axioms boundedVariationOn_prefixIntegral

/-- Left endpoint weights against actual prefix increments converge to the
time integral of the weighted density. -/
theorem tendsto_dyadic_weighted_prefixIntegral_sums
    (w b : ℝ≥0 → ℝ) (T : ℝ≥0) (hT : 0 < T)
    (hw : ContinuousOn w (Set.Icc 0 T))
    (hb : Integrable b (TimeMeasure.upTo T)) :
    Tendsto (fun level : ℕ =>
      let times := regularGridTimes (dyadicMesh T level) (2 ^ level)
      ∑ i : Fin (2 ^ level), w (times i.castSucc) *
        (prefixIntegral b T (times i.succ) - prefixIntegral b T (times i.castSucc)))
      atTop (nhds (∫ t, w t * b t ∂(TimeMeasure.upTo T))) := by
  obtain ⟨C, hC⟩ := isCompact_Icc.bddAbove_image hw.abs
  have hBound (r : ℝ≥0) (hr : r ≤ T) : |w r| ≤ C :=
    hC ⟨r, ⟨bot_le, hr⟩, rfl⟩
  let F (level : ℕ) (r : ℝ≥0) := sample w T level r * b r
  have hLim : Tendsto (fun level => ∫ r, F level r ∂(TimeMeasure.upTo T))
      atTop (nhds (∫ r, w r * b r ∂(TimeMeasure.upTo T))) := by
    refine tendsto_integral_of_dominated_convergence (fun r => C * |b r|)
      (fun level => (sample_measurable w T level).aestronglyMeasurable.mul hb.aestronglyMeasurable)
      (hb.abs.const_mul C) ?_ ?_
    · intro level
      filter_upwards [TimeMeasure.ae_mem_Ioc_zero_upTo T] with r hr
      rw [Real.norm_eq_abs, show F level r = sample w T level r * b r from rfl, abs_mul]
      exact mul_le_mul_of_nonneg_right (sample_bound w hT level hr hBound) (abs_nonneg _)
    · filter_upwards [TimeMeasure.ae_mem_Ioc_zero_upTo T] with r hr
      exact (tendsto_sample w hT hw hr).mul_const (b r)
  refine (tendsto_congr' (Eventually.of_forall fun level => ?_)).2 hLim
  let cell := fun (i : Fin (2 ^ level)) => Ioc (grid T level i.castSucc) (grid T level i.succ)
  let part := fun (i : Fin (2 ^ level)) =>
    (cell i).indicator (fun r => w (grid T level i.castSucc) * b r)
  have hpart (i : Fin (2 ^ level)) : Integrable (part i) (TimeMeasure.upTo T) :=
    (hb.const_mul _).indicator measurableSet_Ioc
  have hF (r : ℝ≥0) : F level r = ∑ i : Fin (2 ^ level), part i r := by
    dsimp only [F, sample]
    rw [Finset.sum_mul]
    apply Finset.sum_congr rfl
    intro i _
    change (if r ∈ cell i then w (grid T level i.castSucc) else 0) * b r = part i r
    by_cases hr : r ∈ cell i
    · rw [if_pos hr]
      exact (Set.indicator_of_mem hr (fun r => w (grid T level i.castSucc) * b r)).symm
    · rw [if_neg hr, zero_mul]
      exact (Set.indicator_of_notMem hr (fun r => w (grid T level i.castSucc) * b r)).symm
  simp_rw [hF]
  rw [integral_finsetSum _ (fun i _ => hpart i)]
  apply Finset.sum_congr rfl
  intro i _
  change w (grid T level i.castSucc) *
    (prefixIntegral b T (grid T level i.succ) - prefixIntegral b T (grid T level i.castSucc)) =
    ∫ r, part i r ∂(TimeMeasure.upTo T)
  rw [prefix_sub_eq_Ioc hb (grid_mono hT level (Fin.castSucc_le_succ i)) (grid_le hT level i.succ)]
  rw [show part i = (cell i).indicator (fun r => w (grid T level i.castSucc) * b r) from rfl,
    integral_indicator (show MeasurableSet (cell i) from measurableSet_Ioc), integral_const_mul]

#print axioms tendsto_dyadic_weighted_prefixIntegral_sums

private theorem assemble_integrands
    {Omega K : Type*} {m : MeasurableSpace Omega} [DecidableEq K]
    {filtration : Filtration ℝ≥0 m} {mu : Measure Omega} [IsFiniteMeasure mu]
    {T : ℝ≥0} {B : ℝ≥0 → Omega → ℝ} (hT : 0 < T)
    (hB : IsBrownianMotionWithFiltration B filtration mu)
    (hUsual : SatisfiesUsualConditions filtration mu)
    (f : K → ProgressiveL2Integrand filtration mu T) (S : Finset K) :
    ∃ g : ProgressiveL2Integrand filtration mu T,
      (∀ r omega, g.process r omega = ∑ i ∈ S, (f i).process r omega) ∧
      itoIntegralProcess g hT hB hUsual T =ᵐ[mu]
        fun omega => ∑ i ∈ S, itoIntegralProcess (f i) hT hB hUsual T omega := by
  induction S using Finset.induction_on with
  | empty =>
    refine ⟨ProgressiveL2Algebra.zero, by simp, ?_⟩
    simpa only [Finset.sum_empty] using itoIntegralProcess_zero hT hB hUsual (le_refl T)
  | insert i S hi ih =>
    obtain ⟨g, hg, hIto⟩ := ih
    refine ⟨ProgressiveL2Algebra.add (f i) g, ?_, ?_⟩
    · intro r omega
      change (f i).process r omega + g.process r omega = _
      rw [hg, Finset.sum_insert hi]
    · filter_upwards [itoIntegralProcess_add (f i) g hT hB hUsual (le_refl T), hIto]
        with omega hAdd hG
      rw [Finset.sum_insert hi]
      exact hAdd.trans (congrArg₂ (· + ·) rfl hG)

/-- The exact completed integral of a bounded progressive product is the
limit in measure of its left-weighted completed dyadic increments. -/
theorem tendstoInMeasure_dyadic_weighted_ito_sums
    {Omega : Type*} {m : MeasurableSpace Omega}
    {filtration : Filtration ℝ≥0 m} {mu : Measure Omega} [IsFiniteMeasure mu]
    {T : ℝ≥0} {B : ℝ≥0 → Omega → ℝ}
    (eta : ProgressiveL2Integrand filtration mu T) (hT : 0 < T)
    (hB : IsBrownianMotionWithFiltration B filtration mu)
    (hUsual : SatisfiesUsualConditions filtration mu)
    (w : ℝ≥0 → Omega → ℝ) (hw : IsStronglyProgressive filtration w)
    (hCont : ∀ᵐ omega ∂mu, ContinuousOn (fun t => w t omega) (Set.Icc 0 T))
    {C : ℝ} (hBound : ∀ t ≤ T, ∀ omega, |w t omega| ≤ C) :
    ∃ theta : ProgressiveL2Integrand filtration mu T,
      (∀ (t : ℝ≥0) (omega : Omega), theta.process t omega = w t omega * eta.process t omega) ∧
      let I := itoIntegralProcess eta hT hB hUsual
      TendstoInMeasure mu
        (fun level omega =>
          let times := regularGridTimes (dyadicMesh T level) (2 ^ level)
          ∑ i : Fin (2 ^ level), w (times i.castSucc) omega *
            (I (times i.succ) omega - I (times i.castSucc) omega))
        atTop (itoIntegralProcess theta hT hB hUsual T) := by
  classical
  let pm := processTimeMeasure mu T
  have hTime : ∀ᵐ z : Omega × ℝ≥0 ∂pm, z.2 ∈ Ioc 0 T :=
    Measure.quasiMeasurePreserving_snd.ae (TimeMeasure.ae_mem_Ioc_zero_upTo T)
  have hLift : @Measurable (Omega × ℝ≥0) (Set.Iic T × Omega) _
      (Subtype.instMeasurableSpace.prod (filtration T))
      (fun z : Omega × ℝ≥0 => ((⟨min z.2 T, Set.mem_Iic.2 (min_le_right _ _)⟩ : Set.Iic T), z.1)) :=
    ((measurable_snd.min measurable_const).subtype_mk).prodMk
      (measurable_fst.mono le_rfl (filtration.le T))
  have hW : MemLp (processFunction w) ∞ pm := by
    have hm : StronglyMeasurable (fun z : Omega × ℝ≥0 => w (min z.2 T) z.1) :=
      (hw T).comp_measurable hLift
    refine (memLp_congr_ae ?_).1 (memLp_top_of_bound hm.aestronglyMeasurable C ?_)
    · filter_upwards [hTime] with z hz
      simp [processFunction, min_eq_left hz.2]
    · exact Eventually.of_forall fun z => by
        simpa only [Real.norm_eq_abs] using hBound (min z.2 T) (min_le_right _ _) z.1
  let theta : ProgressiveL2Integrand filtration mu T :=
    ⟨fun r omega => w r omega * eta.process r omega, hw.mul eta.progressive, eta.memLp.mul' hW⟩
  refine ⟨theta, fun _ _ => rfl, ?_⟩
  let I := itoIntegralProcess eta hT hB hUsual
  have hApprox (level : ℕ) : ∃ g : ProgressiveL2Integrand filtration mu T,
      (∀ r omega, g.process r omega = sample (fun t => w t omega) T level r * eta.process r omega) ∧
      itoIntegralProcess g hT hB hUsual T =ᵐ[mu] fun omega =>
        ∑ i : Fin (2 ^ level), w (grid T level i.castSucc) omega *
          (I (grid T level i.succ) omega - I (grid T level i.castSucc) omega) := by
    have hCell (i : Fin (2 ^ level)) :=
      itoIntegralProcess_bounded_past_cell_multiplier eta hT hB hUsual
        (grid_mono hT level (Fin.castSucc_le_succ (i := i))) (grid_le hT level i.succ)
        (w (grid T level i.castSucc)) (hw.stronglyAdapted _)
        (hBound _ (grid_le hT level i.castSucc))
    choose cell hCellValue hCellIto using hCell
    obtain ⟨g, hg, hG⟩ := assemble_integrands hT hB hUsual cell Finset.univ
    refine ⟨g, ?_, ?_⟩
    · intro r omega
      rw [hg, sample, Finset.sum_mul]
      apply Finset.sum_congr rfl
      intro i _
      rw [hCellValue]
      by_cases h : grid T level i.castSucc < r ∧ r ≤ grid T level i.succ <;>
        simp [Set.mem_Ioc, h]
    · filter_upwards [hG, ae_all_iff.2 hCellIto] with omega hSum hCoord
      exact hSum.trans (Finset.sum_congr rfl (fun i _ => hCoord i))
  choose approx hApp hAppIto using hApprox
  let F (level : ℕ) (z : Omega × ℝ≥0) :=
    (processFunction (approx level).process z - processFunction theta.process z)^2
  have hF (level : ℕ) (z : Omega × ℝ≥0) :
      F level z = ((sample (fun t => w t z.1) T level z.2 - w z.2 z.1) *
        processFunction eta.process z)^2 := by
    simp only [F, processFunction, hApp, theta, sub_mul]
  let K := |C|
  have hDom (level : ℕ) : ∀ᵐ z ∂pm, ‖F level z‖ ≤ (2 * K)^2 * (processFunction eta.process z)^2 := by
    filter_upwards [hTime] with z hz
    let error := sample (fun t => w t z.1) T level z.2 - w z.2 z.1
    have he : |error| ≤ 2 * K := by
      have ha := sample_bound (fun t => w t z.1) hT level hz (fun t ht => hBound t ht z.1)
      have hb := hBound z.2 hz.2 z.1
      have hc : |error| ≤ |sample (fun t => w t z.1) T level z.2| + |w z.2 z.1| := by
        simpa only [error, sub_eq_add_neg, abs_neg] using
          abs_add_le (sample (fun t => w t z.1) T level z.2) (-w z.2 z.1)
      dsimp [K]
      linarith [le_abs_self C]
    have hsq : error^2 ≤ (2 * K)^2 := by
      simpa only [← abs_pow, abs_of_nonneg (sq_nonneg error)] using
        pow_le_pow_left₀ (abs_nonneg error) he 2
    rw [hF, Real.norm_eq_abs, abs_of_nonneg (sq_nonneg _), mul_pow]
    exact mul_le_mul_of_nonneg_right hsq (sq_nonneg _)
  have hPt : ∀ᵐ z ∂pm, Tendsto (fun level => F level z) atTop (nhds 0) := by
    have hC : ∀ᵐ z : Omega × ℝ≥0 ∂pm, ContinuousOn (fun t => w t z.1) (Icc 0 T) :=
      Measure.quasiMeasurePreserving_fst.ae hCont
    filter_upwards [hTime, hC] with z hz hc
    have h := (((tendsto_sample (fun t => w t z.1) hT hc hz).sub
      (tendsto_const_nhds (x := w z.2 z.1))).mul_const (processFunction eta.process z)).pow 2
    simpa only [hF, sub_self, zero_mul, zero_pow (by decide : (2 : ℕ) ≠ 0)] using h
  have hSq : Tendsto (fun level => ∫ z, F level z ∂pm) atTop (nhds 0) := by
    have h := tendsto_integral_of_dominated_convergence (μ := pm) (F := F) (f := fun _ => (0 : ℝ))
      (fun z => (2 * K)^2 * (processFunction eta.process z)^2)
      (fun level => ((approx level).memLp.sub theta.memLp).integrable_sq.aestronglyMeasurable)
      (eta.memLp.integrable_sq.const_mul _) hDom hPt
    simpa only [integral_zero] using h
  have hNorm (level : ℕ) : ‖(approx level).toLp - theta.toLp‖^2 = ∫ z, F level z ∂pm := by
    have h := norm_sq_toLp_eq_integral_sq ((approx level).memLp.sub theta.memLp)
    rw [MemLp.toLp_sub] at h
    exact h
  have hLp : Tendsto (fun level => (approx level).toLp) atTop (nhds theta.toLp) := by
    apply tendsto_iff_norm_sub_tendsto_zero.mpr
    have h := Real.continuous_sqrt.continuousAt.tendsto.comp hSq
    simpa only [Function.comp_def, ← hNorm, Real.sqrt_sq (norm_nonneg _), Real.sqrt_zero] using h
  have hTerminal : Tendsto (fun level => itoIntegralTerminal (approx level) hT hB) atTop
      (nhds (itoIntegralTerminal theta hT hB)) := by
    apply tendsto_iff_norm_sub_tendsto_zero.mpr
    simpa only [itoIntegralTerminal_isometry_sub, integrandToLp] using
      (tendsto_iff_norm_sub_tendsto_zero.mp hLp)
  have hIto : TendstoInMeasure mu (fun level => itoIntegralProcess (approx level) hT hB hUsual T)
      atTop (itoIntegralProcess theta hT hB hUsual T) :=
    (tendstoInMeasure_of_tendsto_Lp hTerminal).congr
      (fun level => (itoIntegralProcess_terminal_eq (approx level) hT hB hUsual).symm)
      (itoIntegralProcess_terminal_eq theta hT hB hUsual).symm
  exact hIto.congr_left hAppIto

#print axioms tendstoInMeasure_dyadic_weighted_ito_sums

end AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoWeightedRiemannSums
