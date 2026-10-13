import AutoSamplingTheory.ExampleCases.ProximalBPS.ActualEndpointTimeReversal
import Mathlib.Analysis.InnerProductSpace.Calculus
import Mathlib.MeasureTheory.Integral.IntervalIntegral.FundThmCalculus

namespace AutoSamplingTheory.ExampleCases.ProximalBPS.ActualPrescribedGibbsSurvival
open MeasureTheory InnerProductSpace
open scoped ContDiff NNReal ENNReal Classical
noncomputable section
set_option autoImplicit false

private theorem actual_arc_energy
    {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]
    {V : E → ℝ} {α β : ℝ≥0} {η : ℝ}
    (hα : 0 < (α : ℝ)) (hαβ : α ≤ β) (hV : ContDiff ℝ 2 V)
    (hH : ∀ x v : E,
      (α : ℝ) * ‖v‖ ^ 2 ≤ (fderiv ℝ (fderiv ℝ V) x v) v ∧
      (fderiv ℝ (fderiv ℝ V) x v) v ≤ (β : ℝ) * ‖v‖ ^ 2)
    (hη : 0 < η) (hβη : (β : ℝ) * η ≤ 1) :
    let c : E → E → E := fun y r => y - η • gradient V r
    let Φ : E → E → ℝ → (E × E) → (E × E) := fun y r t z =>
      (c y r + Real.cos t • (z.1 - c y r) +
          (Real.sqrt η * Real.sin t) • z.2,
       (-Real.sin t / Real.sqrt η) • (z.1 - c y r) + Real.cos t • z.2)
    let R : E × E → E × E := fun z => (z.1, -z.2)
    let rate : E → E × E → ℝ := fun r z =>
      Real.sqrt η * max 0 (inner ℝ z.2 (gradient V z.1 - gradient V r))
    let U : E → E × E → ℝ := fun y z =>
      V z.1 + ‖z.1 - y‖ ^ 2 / (2 * η) + ‖z.2‖ ^ 2 / 2
    ∀ y r : E, ∀ z : E × E,
      (∀ s : ℝ, HasDerivAt (fun t => U y (Φ y r t z))
        (rate r (Φ y r s z) - rate r (R (Φ y r s z))) s) ∧
      (∀ a b : ℝ,
        IntervalIntegrable (fun s => rate r (Φ y r s z)) volume a b ∧
        IntervalIntegrable (fun s => rate r (R (Φ y r s z))) volume a b ∧
        U y (Φ y r b z) - U y (Φ y r a z) =
          (∫ s in a..b, rate r (Φ y r s z)) -
          (∫ s in a..b, rate r (R (Φ y r s z)))) := by
  intro c Φ R rate U y r z
  letI : CompleteSpace E := FiniteDimensional.complete ℝ E
  have hf := AutoSamplingTheory.ExampleCases.ProximalBPS.ActualHarmonicFlow.actual_harmonic_flow_laws
    hα hαβ hV hH hη hβη
  rcases hf with ⟨hc, _, _, _, _, ho, _⟩
  have hb := AutoSamplingTheory.ExampleCases.ProximalBPS.ActualBounceRate.actual_bounce_rate_energy_laws
    hα hαβ hV hH hη hβη
  have hrate : Continuous (fun q : E × (E × E) => rate q.1 q.2) := hb.2.1
  have hphi : Continuous (fun t => Φ y r t z) :=
    hc.comp ((continuous_const (y := (y,r))).prodMk
      (continuous_id.prodMk (continuous_const (y := z))))
  have hp : Continuous (fun t => rate r (Φ y r t z)) :=
    hrate.comp (continuous_const.prodMk hphi)
  have hm : Continuous (fun t => rate r (R (Φ y r t z))) :=
    hrate.comp (continuous_const.prodMk (hphi.fst.prodMk hphi.snd.neg))
  have hdiff (q : E × E) : rate r q - rate r (R q) =
      Real.sqrt η * inner ℝ q.2 (gradient V q.1 - gradient V r) := by
    dsimp [rate, R]
    rw [inner_neg_left]
    by_cases h : 0 ≤ inner ℝ q.2 (gradient V q.1 - gradient V r)
    · rw [max_eq_right h, max_eq_left (neg_nonpos.mpr h)]
      ring
    · rw [max_eq_left (le_of_not_ge h), max_eq_right (neg_nonneg.mpr (le_of_not_ge h))]
      ring
  have hd (s : ℝ) : HasDerivAt (fun t => U y (Φ y r t z))
      (rate r (Φ y r s z) - rate r (R (Φ y r s z))) s := by
    obtain ⟨hx, hv⟩ := ho y r s z
    have hx' : HasDerivAt (fun t => (Φ y r t z).1) (Real.sqrt η • (Φ y r s z).2) s := hx
    have hv' : HasDerivAt (fun t => (Φ y r t z).2)
        (-(Real.sqrt η)⁻¹ • ((Φ y r s z).1 - y) - Real.sqrt η • gradient V r) s := hv
    have hVd := ((hV.differentiable (by norm_num)).differentiableAt.hasGradientAt.hasFDerivAt).comp_hasDerivAt s hx'
    have hd0 := (hVd.add ((hx'.sub_const y).norm_sq.div_const (2 * η))).add
      (hv'.norm_sq.div_const 2)
    apply hd0.congr_deriv
    rw [hdiff]
    simp only [InnerProductSpace.toDual_apply_apply, real_inner_smul_right, real_inner_smul_left,
      inner_sub_right, inner_sub_left, real_inner_comm]
    have hs : (Real.sqrt η) ^ 2 = η := Real.sq_sqrt hη.le
    have hs0 : Real.sqrt η ≠ 0 := ne_of_gt (Real.sqrt_pos.mpr hη)
    field_simp [hs0, hη.ne']
    simp only [hs]
    ring
  refine ⟨hd, ?_⟩
  intro a b
  have hi : IntervalIntegrable (fun s => rate r (Φ y r s z)) volume a b := hp.intervalIntegrable a b
  have hj : IntervalIntegrable (fun s => rate r (R (Φ y r s z))) volume a b := hm.intervalIntegrable a b
  refine ⟨hi, hj, ?_⟩
  rw [← intervalIntegral.integral_sub hi hj]
  exact (intervalIntegral.integral_eq_sub_of_hasDerivAt (fun s _ => hd s) (hi.sub hj)).symm


/-- Integrable adjacent differences telescope across an energy grid. The
    pointwise path may jump; only endpoint energies need to match. -/
private theorem finite_energy_balance (n : ℕ) (a u : Fin (n+1) → ℝ)
    (f g : ℝ → ℝ)
    (hf : ∀ j : Fin n, IntervalIntegrable f volume (a j.castSucc) (a j.succ))
    (hg : ∀ j : Fin n, IntervalIntegrable g volume (a j.castSucc) (a j.succ))
    (hstep : ∀ j : Fin n,
      (∫ s in a j.castSucc..a j.succ, f s) -
        (∫ s in a j.castSucc..a j.succ, g s) = u j.succ - u j.castSucc) :
    IntervalIntegrable f volume (a 0) (a (Fin.last n)) ∧
    IntervalIntegrable g volume (a 0) (a (Fin.last n)) ∧
    u (Fin.last n) - u 0 =
      (∫ s in a 0..a (Fin.last n), f s) -
        (∫ s in a 0..a (Fin.last n), g s) := by
  induction n with
  | zero => simp
  | succ n ih =>
    have hh := ih (fun i => a i.castSucc) (fun i => u i.castSucc)
      (fun j => hf j.castSucc) (fun j => hg j.castSucc)
      (fun j => by simpa only [Fin.succ_castSucc] using hstep j.castSucc)
    have hfl := hf (Fin.last n)
    have hgl := hg (Fin.last n)
    have hs := hstep (Fin.last n)
    refine ⟨hh.1.trans hfl, hh.2.1.trans hgl, ?_⟩
    have hfi := intervalIntegral.integral_add_adjacent_intervals hh.1 hfl
    have hgi := intervalIntegral.integral_add_adjacent_intervals hh.2.1 hgl
    simp only [Fin.succ_last, Fin.castSucc_zero] at hh hs hfi hgi
    linarith [hh.2.2]


open Set
set_option maxRecDepth 4000
set_option maxHeartbeats 1600000

private def actual_prescribed_gibbs_survival_statement
    {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]
    {V : E → ℝ} {α β : ℝ≥0} {η : ℝ}
    (hα : 0 < (α : ℝ)) (hαβ : α ≤ β) (hV : ContDiff ℝ 2 V)
    (hH : ∀ x v : E,
      (α : ℝ) * ‖v‖ ^ 2 ≤ (fderiv ℝ (fderiv ℝ V) x v) v ∧
      (fderiv ℝ (fderiv ℝ V) x v) v ≤ (β : ℝ) * ‖v‖ ^ 2)
    (hη : 0 < η) (hβη : (β : ℝ) * η ≤ 1) : Prop := by
  classical
  exact
    let c : E → E → E := fun y xRef => y - η • gradient V xRef
    let Φ : E → E → ℝ → (E × E) → (E × E) := fun y xRef t z =>
      (c y xRef + Real.cos t • (z.1 - c y xRef) +
          (Real.sqrt η * Real.sin t) • z.2,
       (-Real.sin t / Real.sqrt η) • (z.1 - c y xRef) + Real.cos t • z.2)
    let S : E → (E × E) → (E × E) := fun xRef z =>
      (z.1, z.2 - (2 * inner ℝ z.2 (gradient V z.1 - gradient V xRef) /
        ‖gradient V z.1 - gradient V xRef‖ ^ 2) • (gradient V z.1 - gradient V xRef))
    let Rec := (ℝ≥0 × (E × E)) ⊕ Unit
    let Hist : ℕ → Type _ := fun n => Fin (n + 1) → Rec
    let Δ : (n : ℕ) → ℝ≥0 → Set (Fin n → ℝ) := fun n T =>
      {t | StrictMono (Fin.cons (0 : ℝ) t) ∧ ∀ i, t i < (T : ℝ)}
    let Prefix : (n : ℕ) → ℝ≥0 → Type := fun n T => {t : Fin n → ℝ // t ∈ Δ n T}
    let m : (n : ℕ) → (T : ℝ≥0) → Measure (Prefix n T) := fun n T =>
      Measure.comap (fun t : Prefix n T => t.val) (volume : Measure (Fin n → ℝ))
    let zAt : E → E → (E × E) → (n : ℕ) → (T : ℝ≥0) →
        Prefix n T → Fin (n + 1) → (E × E) := fun y xRef z₀ n T t =>
      Fin.induction z₀ (fun i z =>
        S xRef (Φ y xRef (t.val i - (Fin.cons (0 : ℝ) (t.val : Fin n → ℝ) : Fin (n + 1) → ℝ) i.castSucc) z))
    let K : E → E → (E × E) → (n : ℕ) → (T : ℝ≥0) →
        Prefix n T → Hist n := fun y xRef z₀ n T t j =>
      Sum.inl (Real.toNNReal ((Fin.cons (0 : ℝ) (t.val : Fin n → ℝ) : Fin (n + 1) → ℝ) j), zAt y xRef z₀ n T t j)
    let Path : ℝ≥0 → Type _ := fun T => {s : ℝ≥0 // s ≤ T} → E × E
    let Ψ : E → E → (E × E) → (n : ℕ) → (T : ℝ≥0) → Hist n → Path T :=
      fun y xRef z₀ n T h s =>
        Fin.foldl (n + 1) (fun z j => (h j).elim
          (fun a => if a.1 ≤ s.val then Φ y xRef ((s.val - a.1 : ℝ≥0) : ℝ) a.2 else z)
          (fun _ => z)) z₀
    let Γ : E → E → (E × E) → (n : ℕ) → (T : ℝ≥0) → Prefix n T → Path T :=
      fun y xRef z₀ n T t => Ψ y xRef z₀ n T (K y xRef z₀ n T t)
    let R : E × E → E × E := fun z => (z.1, -z.2)
    let rate : E → E × E → ℝ := fun r z =>
      Real.sqrt η * max 0 (inner ℝ z.2 (gradient V z.1 - gradient V r))
    let U : E → E × E → ℝ := fun y z =>
      V z.1 + ‖z.1 - y‖ ^ 2 / (2 * η) + ‖z.2‖ ^ 2 / 2
    ∀ y r : E, ∀ z : E × E, ∀ n : ℕ, ∀ T : ℝ≥0, ∀ t : Prefix n T,
      let gamma : ℝ → E × E := fun s =>
        Γ y r z n T t ⟨min (Real.toNNReal s) T, min_le_right _ _⟩
      let A : E × E := Γ y r z n T t ⟨T, le_rfl⟩
      let Iplus : ℝ := ∫ s in (0 : ℝ)..(T : ℝ), rate r (gamma s)
      let Iminus : ℝ := ∫ s in (0 : ℝ)..(T : ℝ), rate r (R (gamma s))
      IntervalIntegrable (fun s => rate r (gamma s)) volume 0 (T : ℝ) ∧
      IntervalIntegrable (fun s => rate r (R (gamma s))) volume 0 (T : ℝ) ∧
      U y A - U y z = Iplus - Iminus ∧
      Real.exp (-U y z) * Real.exp (-Iplus) = Real.exp (-U y A) * Real.exp (-Iminus)

/-- Actual finite prescribed target-energy and Gibbs/survival identity under the six source hypotheses. -/
theorem actual_prescribed_gibbs_survival_balance
    {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]
    {V : E → ℝ} {α β : ℝ≥0} {η : ℝ}
    (hα : 0 < (α : ℝ)) (hαβ : α ≤ β) (hV : ContDiff ℝ 2 V)
    (hH : ∀ x v : E,
      (α : ℝ) * ‖v‖ ^ 2 ≤ (fderiv ℝ (fderiv ℝ V) x v) v ∧
      (fderiv ℝ (fderiv ℝ V) x v) v ≤ (β : ℝ) * ‖v‖ ^ 2)
    (hη : 0 < η) (hβη : (β : ℝ) * η ≤ 1) :
    actual_prescribed_gibbs_survival_statement hα hαβ hV hH hη hβη := by
  unfold actual_prescribed_gibbs_survival_statement
  intro c Φ S Rec Hist Δ Prefix m zAt K Path Ψ Γ R rate U y r z n T t gamma A Iplus Iminus
  let a : Fin (n+1) → ℝ := Fin.cons 0 t.val
  let grid : Fin (n+2) → ℝ := Fin.snoc a (T : ℝ)
  let u : Fin (n+2) → ℝ := Fin.snoc (fun j => U y (zAt y r z n T t j)) (U y A)
  have hflow := AutoSamplingTheory.ExampleCases.ProximalBPS.ActualHarmonicFlow.actual_harmonic_flow_laws
    hα hαβ hV hH hη hβη
  have hzero : ∀ q : E × E, Φ y r 0 q = q := hflow.2.2.1 y r
  have hb := AutoSamplingTheory.ExampleCases.ProximalBPS.ActualBounceRate.actual_bounce_rate_energy_laws
    hα hαβ hV hH hη hβη
  have hsU (q : E × E) : U y (S r q) = U y q := by
    have hn := (hb.2.2.2.2.1 (gradient V q.1 - gradient V r) q.2).2.1
    change V q.1 + ‖q.1 - y‖ ^ 2 / (2 * η) + _ / 2 = _
    rw [show ‖(S r q).2‖ = ‖q.2‖ from hn]
  have hRate : Continuous (fun q : E × (E × E) => rate q.1 q.2) := hb.2.1
  have hPhi : Continuous (fun q : (E × E) × ℝ × (E × E) => Φ q.1.1 q.1.2 q.2.1 q.2.2) := hflow.1
  have ham : StrictMono a := t.property.1
  have haT : ∀ j, a j ≤ (T : ℝ) := by
    intro j
    refine Fin.cases ?_ (fun i => ?_) j
    · simpa [a] using T.coe_nonneg
    · exact (t.property.2 i).le
  have hgrid : Monotone grid := by
    intro i j hij
    induction i using Fin.lastCases with
    | last =>
      have hj : j = Fin.last (n+1) := le_antisymm (Fin.le_last j) hij
      subst j
      exact le_rfl
    | cast i =>
      induction j using Fin.lastCases with
      | last => simpa [grid] using haT i
      | cast j => simpa [grid] using ham.monotone (show i ≤ j from hij)
  have hg0 : grid 0 = 0 := by simp [grid, a]
  have hgT : grid (Fin.last (n+1)) = (T : ℝ) := by simp [grid]
  obtain ⟨Z, _, _, _, _, hlaw⟩ :=
    AutoSamplingTheory.ExampleCases.ProximalBPS.ActualFiniteCountPath.actual_finite_count_path_law
      hα hαβ hV hH hη hβη
  have harc := ((hlaw n T).2.2.2 y r z).2.2.2.2.1
  have heq (j : Fin (n+1)) : EqOn gamma
      (fun s => Φ y r (s - grid j.castSucc) (zAt y r z n T t j))
      (Ioo (grid j.castSucc) (grid j.succ)) := by
    intro s hs
    have hs0 : 0 ≤ s := by
      have := hgrid (show (0 : Fin (n+2)) ≤ j.castSucc from Fin.zero_le _)
      rw [hg0] at this
      exact this.trans hs.1.le
    have hsT : s ≤ (T : ℝ) := by
      have := hgrid (Fin.le_last j.succ)
      rw [hgT] at this
      exact hs.2.le.trans this
    have hclip : min (Real.toNNReal s) T = Real.toNNReal s :=
      min_eq_left (by exact_mod_cast (Real.toNNReal_le_iff_le_coe).2 hsT)
    have hclipcoe : ((min (Real.toNNReal s) T : ℝ≥0) : ℝ) = s := by
      rw [hclip, Real.coe_toNNReal s hs0]
    have hstart : a j ≤ s := by simpa [grid] using hs.1.le
    have hafter : ∀ k : Fin (n+1), j < k → s < a k := by
      intro k hjk
      have hidx : j.succ ≤ k.castSucc := by exact_mod_cast hjk
      exact hs.2.trans_le (by simpa [grid] using hgrid hidx)
    have hh := harc t ⟨min (Real.toNNReal s) T, min_le_right _ _⟩ j
      (by simpa only [hclipcoe] using hstart)
      (by simpa only [hclipcoe] using hafter)
    change gamma s = Φ y r (((min (Real.toNNReal s) T : ℝ≥0) : ℝ) - a j)
      (zAt y r z n T t j) at hh
    simpa only [hclipcoe, grid, Fin.snoc_castSucc] using hh
  obtain ⟨rho, _, _, _, _, hend, _⟩ :=
    AutoSamplingTheory.ExampleCases.ProximalBPS.ActualEndpointTimeReversal.actual_endpoint_time_reversal_laws
      hα hαβ hV hH hη hβη n T
  have hterminal : A = Φ y r ((T : ℝ) - a (Fin.last n)) (zAt y r z n T t (Fin.last n)) :=
    hend y r z t
  have hnext (i : Fin n) : zAt y r z n T t i.succ =
      S r (Φ y r (t.val i - a i.castSucc) (zAt y r z n T t i.castSucc)) := by
    simp only [zAt, Fin.induction_succ]
    rfl
  have hEnd (j : Fin (n+1)) :
      U y (Φ y r (grid j.succ - grid j.castSucc) (zAt y r z n T t j)) = u j.succ := by
    induction j using Fin.lastCases with
    | last =>
      simpa only [Fin.succ_last, grid, u, Fin.snoc_last, Fin.snoc_castSucc] using
        (congrArg (U y) hterminal).symm
    | cast i =>
      simp only [Fin.succ_castSucc, u, Fin.snoc_castSucc]
      rw [hnext]
      simpa only [grid, Fin.succ_castSucc, Fin.snoc_castSucc, a, Fin.cons_succ] using
        (hsU (Φ y r (t.val i - a i.castSucc) (zAt y r z n T t i.castSucc))).symm
  have hstep (j : Fin (n+1)) :
      IntervalIntegrable (fun s => rate r (gamma s)) volume (grid j.castSucc) (grid j.succ) ∧
      IntervalIntegrable (fun s => rate r (R (gamma s))) volume (grid j.castSucc) (grid j.succ) ∧
      (∫ s in grid j.castSucc..grid j.succ, rate r (gamma s)) -
        (∫ s in grid j.castSucc..grid j.succ, rate r (R (gamma s))) = u j.succ - u j.castSucc := by
    let q : ℝ → E × E := fun s => Φ y r (s - grid j.castSucc) (zAt y r z n T t j)
    have harg : Continuous (fun s : ℝ => ((y,r),(s - grid j.castSucc),zAt y r z n T t j)) :=
      continuous_const.prodMk ((continuous_id.sub continuous_const).prodMk continuous_const)
    have hq : Continuous q := hPhi.comp harg
    have hp : Continuous (fun s : ℝ => rate r (q s)) :=
      hRate.comp ((continuous_const (y := r)).prodMk hq)
    have hm : Continuous (fun s : ℝ => rate r (R (q s))) :=
      hRate.comp ((continuous_const (y := r)).prodMk (hq.fst.prodMk hq.snd.neg))
    have hle := hgrid (Fin.castSucc_le_succ j)
    have hip : IntervalIntegrable (fun s => rate r (q s)) volume (grid j.castSucc) (grid j.succ) := hp.intervalIntegrable _ _
    have him : IntervalIntegrable (fun s => rate r (R (q s))) volume (grid j.castSucc) (grid j.succ) := hm.intervalIntegrable _ _
    have hep : EqOn (fun s => rate r (gamma s)) (fun s => rate r (q s)) (Ioo (grid j.castSucc) (grid j.succ)) :=
      fun s hs => congrArg (rate r) (heq j hs)
    have hem : EqOn (fun s => rate r (R (gamma s))) (fun s => rate r (R (q s))) (Ioo (grid j.castSucc) (grid j.succ)) :=
      fun s hs => congrArg (fun w => rate r (R w)) (heq j hs)
    refine ⟨hip.congr_uIoo (by simpa only [uIoo_of_le hle] using hep.symm),
      him.congr_uIoo (by simpa only [uIoo_of_le hle] using hem.symm), ?_⟩
    rw [intervalIntegral.integral_congr_Ioo_of_le hle hep,
      intervalIntegral.integral_congr_Ioo_of_le hle hem, ← intervalIntegral.integral_sub hip him]
    have hd (s : ℝ) : HasDerivAt (fun w => U y (q w))
        (rate r (q s) - rate r (R (q s))) s := by
      have hh : HasDerivAt (fun w => U y (Φ y r w (zAt y r z n T t j)))
          (rate r (q s) - rate r (R (q s))) (s - grid j.castSucc) :=
        (actual_arc_energy hα hαβ hV hH hη hβη y r (zAt y r z n T t j)).1 (s - grid j.castSucc)
      simpa only [Function.comp_def, id_eq, one_smul] using
        hh.scomp s ((hasDerivAt_id s).sub_const (grid j.castSucc))
    rw [intervalIntegral.integral_eq_sub_of_hasDerivAt (fun s _ => hd s) (hip.sub him)]
    change U y (Φ y r (grid j.succ - grid j.castSucc) (zAt y r z n T t j)) -
      U y (Φ y r (grid j.castSucc - grid j.castSucc) (zAt y r z n T t j)) = _
    rw [hEnd, sub_self, hzero]
    simp only [u, Fin.snoc_castSucc]
  have hf := finite_energy_balance (n+1) grid u
    (fun s => rate r (gamma s)) (fun s => rate r (R (gamma s)))
    (fun j => (hstep j).1) (fun j => (hstep j).2.1) (fun j => (hstep j).2.2)
  have hi : IntervalIntegrable (fun s => rate r (gamma s)) volume 0 (T : ℝ) := by
    simpa only [hg0, hgT] using hf.1
  have hj : IntervalIntegrable (fun s => rate r (R (gamma s))) volume 0 (T : ℝ) := by
    simpa only [hg0, hgT] using hf.2.1
  have henergy : U y A - U y z = Iplus - Iminus := by
    simpa [u, zAt, hg0, hgT] using hf.2.2
  refine ⟨hi, hj, henergy, ?_⟩
  rw [← Real.exp_add, ← Real.exp_add]
  congr 1
  linarith


end
end AutoSamplingTheory.ExampleCases.ProximalBPS.ActualPrescribedGibbsSurvival
#print axioms AutoSamplingTheory.ExampleCases.ProximalBPS.ActualPrescribedGibbsSurvival.actual_prescribed_gibbs_survival_balance
