import AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoCellMultiplier
import Mathlib.MeasureTheory.Function.SimpleFuncDenseLp

/-! # Bounded past weights in completed cell integrals -/

namespace AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoBoundedCellMultiplier

open Filter MeasureTheory Set
open scoped NNReal ENNReal BigOperators
open BrownianMotion ElementaryItoIntegral ElementaryItoL2 ProgressiveL2
  ItoIntegralProcess ItoTerminalCompletion ItoCellMultiplier

private noncomputable def multiplyPast
    {Omega : Type*} {m : MeasurableSpace Omega}
    {filtration : Filtration ℝ≥0 m} {mu : Measure Omega} {T s : ℝ≥0}
    (base : ProgressiveL2Integrand filtration mu T)
    (hZero : ∀ r ≤ s, ∀ omega, base.process r omega = 0)
    (w : Omega → ℝ) (hw : StronglyMeasurable[filtration s] w)
    {C : ℝ} (hC : ∀ omega, |w omega| ≤ C) :
    ProgressiveL2Integrand filtration mu T where
  process := fun r omega => w omega * base.process r omega
  progressive := by
    intro r
    by_cases hr : s ≤ r
    · exact ((hw.mono (filtration.mono hr)).comp_measurable measurable_snd).mul
        (base.progressive r)
    · have hEq : (fun p : Set.Iic r × Omega => w p.2 * base.process p.1 p.2) =
          fun _ => (0 : ℝ) := by
        funext p
        rw [hZero p.1 (p.1.property.trans (le_of_not_ge hr)), mul_zero]
      change StronglyMeasurable[Subtype.instMeasurableSpace.prod (filtration r)]
        (fun p : Set.Iic r × Omega => w p.2 * base.process p.1 p.2)
      rw [hEq]
      exact stronglyMeasurable_const
  memLp := by
    have hW : MemLp (fun z : Omega × ℝ≥0 => w z.1) ∞ (processTimeMeasure mu T) :=
      memLp_top_of_bound
        (((hw.mono (filtration.le s)).comp_measurable measurable_fst).aestronglyMeasurable)
        C (Eventually.of_forall fun z => by simpa only [Real.norm_eq_abs] using hC z.1)
    exact base.memLp.mul' hW

private theorem simple_cell_multiplier
    {Omega : Type*} {m : MeasurableSpace Omega}
    {filtration : Filtration ℝ≥0 m} {mu : Measure Omega} [IsFiniteMeasure mu]
    {T : ℝ≥0} {B : ℝ≥0 → Omega → ℝ}
    (eta : ProgressiveL2Integrand filtration mu T) (hT : 0 < T)
    (hB : IsBrownianMotionWithFiltration B filtration mu)
    (hUsual : SatisfiesUsualConditions filtration mu)
    {s t : ℝ≥0} (hst : s ≤ t) (htT : t ≤ T)
    (w : @SimpleFunc Omega (filtration s) ℝ) :
    ∃ theta : ProgressiveL2Integrand filtration mu T,
      (∀ (r : ℝ≥0) (omega : Omega),
        theta.process r omega = if s < r ∧ r ≤ t then w omega * eta.process r omega else 0) ∧
      itoIntegralProcess theta hT hB hUsual T =ᵐ[mu]
        fun omega => w omega * (itoIntegralProcess eta hT hB hUsual t omega -
          itoIntegralProcess eta hT hB hUsual s omega) := by
  classical
  let I := fun f u omega => itoIntegralProcess f hT hB hUsual u omega
  let D := fun omega => I eta t omega - I eta s omega
  let entry := fun c r omega =>
    if w omega = c ∧ s < r ∧ r ≤ t then c * eta.process r omega else 0
  let value := fun c omega => if w omega = c then c * D omega else 0
  have hEntry (c : ℝ) : ∃ p : ProgressiveL2Integrand filtration mu T,
      (∀ r omega, p.process r omega = entry c r omega) ∧
        I p T =ᵐ[mu] value c := by
    have hFibre : MeasurableSet[filtration s] (w ⁻¹' {c}) := by
      let : MeasurableSpace Omega := filtration s
      exact w.measurableSet_preimage {c}
    obtain ⟨p, hp, hi⟩ := itoIntegralProcess_event_cell_multiplier
      eta hT hB hUsual hst htT (w ⁻¹' {c}) hFibre
    refine ⟨ProgressiveL2Algebra.smul c p, ?_, ?_⟩
    · intro r omega
      change c * p.process r omega = _
      rw [hp]
      by_cases he : w omega = c ∧ s < r ∧ r ≤ t <;> simp [entry, he]
    · filter_upwards [itoIntegralProcess_smul c p hT hB hUsual (le_refl T), hi T (le_refl T)]
        with omega hScale hEval
      change itoIntegralProcess (ProgressiveL2Algebra.smul c p) hT hB hUsual T omega = _
      rw [hScale, hEval]
      by_cases he : w omega = c <;>
        simp [value, D, I, he, min_eq_left htT, min_eq_left (hst.trans htT)]
  have hSum (S : Finset ℝ) : ∃ p : ProgressiveL2Integrand filtration mu T,
      (∀ r omega, p.process r omega = ∑ c ∈ S, entry c r omega) ∧
        I p T =ᵐ[mu] fun omega => ∑ c ∈ S, value c omega := by
    induction S using Finset.induction_on with
    | empty =>
      refine ⟨ProgressiveL2Algebra.zero, by simp, ?_⟩
      simpa only [I, Finset.sum_empty] using itoIntegralProcess_zero hT hB hUsual (le_refl T)
    | insert c S hc ih =>
      obtain ⟨p, hp, hIp⟩ := hEntry c
      obtain ⟨q, hq, hIq⟩ := ih
      refine ⟨ProgressiveL2Algebra.add p q, ?_, ?_⟩
      · intro r omega
        change p.process r omega + q.process r omega = _
        rw [hp, hq, Finset.sum_insert hc]
      · filter_upwards [itoIntegralProcess_add p q hT hB hUsual (le_refl T), hIp, hIq]
          with omega hadd hp hq
        rw [Finset.sum_insert hc]
        exact hadd.trans (congrArg₂ (· + ·) hp hq)
  let values : Finset ℝ := by
    letI : MeasurableSpace Omega := filtration s
    exact w.range
  have hMem (omega : Omega) : w omega ∈ values := by
    let : MeasurableSpace Omega := filtration s
    exact w.mem_range_self omega
  obtain ⟨theta, hInput, hOutput⟩ := hSum values
  refine ⟨theta, ?_, ?_⟩
  · intro r omega
    rw [hInput, Finset.sum_eq_single (w omega)]
    · simp [entry]
    · intro c _ hc
      simp [entry, Ne.symm hc]
    · exact fun h => (h (hMem omega)).elim
  · filter_upwards [hOutput] with omega homega
    change I theta T omega = w omega * D omega
    rw [homega, Finset.sum_eq_single (w omega)]
    · simp [value]
    · intro c _ hc
      simp [value, Ne.symm hc]
    · exact fun h => (h (hMem omega)).elim

/-- A bounded real random variable known at the left endpoint can be
pulled out of the completed Itô integral over that cell. -/
theorem itoIntegralProcess_bounded_past_cell_multiplier
    {Omega : Type*} {m : MeasurableSpace Omega}
    {filtration : Filtration ℝ≥0 m} {mu : Measure Omega} [IsFiniteMeasure mu]
    {T : ℝ≥0} {B : ℝ≥0 → Omega → ℝ}
    (eta : ProgressiveL2Integrand filtration mu T) (hT : 0 < T)
    (hB : IsBrownianMotionWithFiltration B filtration mu)
    (hUsual : SatisfiesUsualConditions filtration mu)
    {s t : ℝ≥0} (hst : s ≤ t) (htT : t ≤ T)
    (w : Omega → ℝ) (hw : StronglyMeasurable[filtration s] w)
    {C : ℝ} (hC : ∀ omega, |w omega| ≤ C) :
    ∃ theta : ProgressiveL2Integrand filtration mu T,
      (∀ (r : ℝ≥0) (omega : Omega),
        theta.process r omega = if s < r ∧ r ≤ t then w omega * eta.process r omega else 0) ∧
      itoIntegralProcess theta hT hB hUsual T =ᵐ[mu]
        fun omega => w omega * (itoIntegralProcess eta hT hB hUsual t omega -
          itoIntegralProcess eta hT hB hUsual s omega) := by
  classical
  obtain ⟨base, hBase, _⟩ := itoIntegralProcess_event_cell_multiplier
    eta hT hB hUsual hst htT Set.univ (@MeasurableSet.univ Omega (filtration s))
  have hZero (r : ℝ≥0) (hr : r ≤ s) (omega : Omega) : base.process r omega = 0 := by
    rw [hBase, if_neg (fun h => (not_lt.mpr hr) h.2.1)]
  let theta := multiplyPast base hZero w hw hC
  have hTheta (r : ℝ≥0) (omega : Omega) :
      theta.process r omega = if s < r ∧ r ≤ t then w omega * eta.process r omega else 0 := by
    change w omega * base.process r omega = _
    rw [hBase]
    by_cases hr : s < r ∧ r ≤ t <;> simp [hr]
  refine ⟨theta, hTheta, ?_⟩
  let R := |C|
  let S := Set.Icc (-R) R
  have h0 : (0 : ℝ) ∈ S := ⟨neg_nonpos.mpr (abs_nonneg _), abs_nonneg _⟩
  let W (n : ℕ) : @SimpleFunc Omega (filtration s) ℝ := by
    letI : MeasurableSpace Omega := filtration s
    exact SimpleFunc.approxOn w hw.measurable S 0 h0 n
  have hLim (omega : Omega) : Tendsto (fun n => W n omega) atTop (nhds (w omega)) := by
    let : MeasurableSpace Omega := filtration s
    exact SimpleFunc.tendsto_approxOn hw.measurable h0
      (subset_closure (abs_le.mp ((hC omega).trans (le_abs_self _))))
  have hBound (n : ℕ) (omega : Omega) : |W n omega| ≤ R := by
    let : MeasurableSpace Omega := filtration s
    exact abs_le.mpr (SimpleFunc.approxOn_mem hw.measurable h0 n omega)
  choose approx hApprox hApproxIto using
    fun n => simple_cell_multiplier eta hT hB hUsual hst htT (W n)
  let u := processFunction base.process
  let F (n : ℕ) (z : Omega × ℝ≥0) := ((W n z.1 - w z.1) * u z)^2
  have hPoint (n : ℕ) (z : Omega × ℝ≥0) :
      (processFunction (approx n).process z - processFunction theta.process z)^2 = F n z := by
    simp only [processFunction, hApprox, hTheta, F, u, hBase, Set.mem_univ, true_and]
    by_cases hz : s < z.2 ∧ z.2 ≤ t <;> simp [hz, sub_mul]
  let hMeasure := processTimeMeasure mu T
  have hInt (n : ℕ) : Integrable (F n) hMeasure := by
    exact ((approx n).memLp.sub theta.memLp).integrable_sq.congr
      (Eventually.of_forall (hPoint n))
  have hDom (n : ℕ) (z : Omega × ℝ≥0) : ‖F n z‖ ≤ (2 * R)^2 * (u z)^2 := by
    have hA : |W n z.1 - w z.1| ≤ 2 * R := by
      have h : |W n z.1 - w z.1| ≤ |W n z.1| + |w z.1| := by
        simpa only [sub_eq_add_neg, abs_neg] using abs_add_le (W n z.1) (-w z.1)
      have hW := hBound n z.1
      have hw' := (hC z.1).trans (le_abs_self _)
      dsimp [R] at *
      linarith
    have hA2 : (W n z.1 - w z.1)^2 ≤ (2 * R)^2 := by
      have h := pow_le_pow_left₀ (abs_nonneg _) hA 2
      simpa only [← abs_pow, abs_of_nonneg (sq_nonneg (W n z.1 - w z.1))] using h
    rw [Real.norm_eq_abs, abs_of_nonneg (show 0 ≤ F n z from sq_nonneg _)]
    dsimp only [F]
    rw [mul_pow]
    exact mul_le_mul_of_nonneg_right hA2 (sq_nonneg _)
  have hLimSq : Tendsto (fun n => ∫ z, F n z ∂hMeasure) atTop (nhds 0) := by
    have h :=
      tendsto_integral_of_dominated_convergence (μ := hMeasure) (F := F)
        (f := fun _ => (0 : ℝ)) (fun z => (2 * R)^2 * (u z)^2)
        (fun n => (hInt n).aestronglyMeasurable) (base.memLp.integrable_sq.const_mul _)
        (fun n => Eventually.of_forall (hDom n)) (Eventually.of_forall fun z => by
          simpa [F, sub_self] using (((hLim z.1).sub
            (tendsto_const_nhds (x := w z.1))).mul
              (tendsto_const_nhds (x := u z))).pow 2)
    simpa using h
  have hNorm (n : ℕ) : ‖(approx n).toLp - theta.toLp‖^2 = ∫ z, F n z ∂hMeasure := by
    calc
      _ = ∫ z, (processFunction (approx n).process z - processFunction theta.process z)^2 ∂hMeasure := by
        have h := norm_sq_toLp_eq_integral_sq ((approx n).memLp.sub theta.memLp)
        rw [MemLp.toLp_sub] at h
        exact h
      _ = _ := integral_congr_ae (Eventually.of_forall (hPoint n))
  have hLp : Tendsto (fun n => (approx n).toLp) atTop (nhds theta.toLp) := by
    apply tendsto_iff_norm_sub_tendsto_zero.mpr
    have h := Real.continuous_sqrt.continuousAt.tendsto.comp hLimSq
    simpa only [Function.comp_def, ← hNorm, Real.sqrt_sq (norm_nonneg _), Real.sqrt_zero] using h
  have hTerminal : Tendsto (fun n => itoIntegralTerminal (approx n) hT hB) atTop
      (nhds (itoIntegralTerminal theta hT hB)) := by
    apply tendsto_iff_norm_sub_tendsto_zero.mpr
    simpa only [itoIntegralTerminal_isometry_sub, integrandToLp] using
      (tendsto_iff_norm_sub_tendsto_zero.mp hLp)
  let D := fun omega => itoIntegralProcess eta hT hB hUsual t omega -
    itoIntegralProcess eta hT hB hUsual s omega
  have hIto : TendstoInMeasure mu (fun n => itoIntegralProcess (approx n) hT hB hUsual T)
      atTop (itoIntegralProcess theta hT hB hUsual T) :=
    (tendstoInMeasure_of_tendsto_Lp hTerminal).congr
      (fun n => (itoIntegralProcess_terminal_eq (approx n) hT hB hUsual).symm)
      (itoIntegralProcess_terminal_eq theta hT hB hUsual).symm
  have hRhs : TendstoInMeasure mu (fun n omega => W n omega * D omega)
      atTop (fun omega => w omega * D omega) := by
    apply tendstoInMeasure_of_tendsto_ae
    · intro n
      exact ((itoIntegralProcess_stronglyAdapted (approx n) hT hB hUsual T).mono
        (filtration.le _)).aestronglyMeasurable.congr (hApproxIto n)
    · exact Eventually.of_forall fun omega => (hLim omega).mul_const (D omega)
  exact tendstoInMeasure_ae_unique (hIto.congr_left hApproxIto) hRhs

#print axioms itoIntegralProcess_bounded_past_cell_multiplier

end AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoBoundedCellMultiplier
