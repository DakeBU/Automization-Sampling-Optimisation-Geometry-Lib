import Mathlib.Analysis.Distribution.Sobolev

set_option autoImplicit false
noncomputable section
open ENNReal MeasureTheory FourierTransform TemperedDistribution
open scoped SchwartzMap BoundedContinuousFunction
open scoped Topology Laplacian LineDeriv
open InnerProductSpace LineDeriv
namespace BoundedSpectralPrototype
variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
  [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]

private def actualMul (g : Lp ℂ ∞ (volume : Measure E)) :
    Lp ℂ 2 (volume : Measure E) →L[ℂ] Lp ℂ 2 (volume : Measure E) :=
  ((ContinuousLinearMap.lsmul ℂ ℂ).holderL volume ∞ 2 2) g

private theorem actualMul_eq (g : Lp ℂ ∞ (volume : Measure E))
    (f : Lp ℂ 2 (volume : Measure E)) : actualMul g f = g • f := by
  apply Lp.ext
  filter_upwards [((ContinuousLinearMap.lsmul ℂ ℂ).coeFn_holder (r := 2) g f),
    Lp.coeFn_lpSMul (r := 2) g f] with x hx hy
  exact hx.trans hy.symm

theorem actual_bounded_multiplier (g : E → ℂ) (hg : g.HasTemperateGrowth)
    (C : ℝ) (hC : ∀ x, ‖g x‖ ≤ C) :
    ∃ A : Lp ℂ 2 (volume : Measure E) →L[ℂ] Lp ℂ 2 (volume : Measure E),
      ∀ f, Lp.toTemperedDistribution (A f) =
        TemperedDistribution.fourierMultiplierCLM ℂ g (Lp.toTemperedDistribution f) := by
  let gc : E →ᵇ ℂ := BoundedContinuousFunction.ofNormedAddCommGroup g hg.1.continuous C hC
  let gl : Lp ℂ ∞ (volume : Measure E) := gc.memLp_top.toLp g (μ := volume)
  let A : Lp ℂ 2 (volume : Measure E) →L[ℂ] Lp ℂ 2 (volume : Measure E) :=
    fourierInvCLM ℂ _ ∘L actualMul gl ∘L fourierCLM ℂ _
  refine ⟨A,?_⟩
  intro f
  change Lp.toTemperedDistribution (𝓕⁻ (actualMul gl (𝓕 f))) = _
  rw [actualMul_eq,← Lp.fourierInv_toTemperedDistribution_eq,
    Lp.toTemperedDistribution_smul_eq hg gc.memLp_top]
  rw [← Lp.fourier_toTemperedDistribution_eq]
  rfl

private theorem lp_td_injective : Function.Injective
    (Lp.toTemperedDistribution : Lp ℂ 2 (volume : Measure E) → 𝓢'(E,ℂ)) := by
  exact LinearMap.ker_eq_bot.mp (Lp.ker_toTemperedDistributionCLM_eq_bot
    (F := ℂ) (μ := volume) (p := 2))

theorem actual_bounded_multiplier_schwartz (g : E → ℂ) (hg : g.HasTemperateGrowth)
    (C : ℝ) (hC : ∀ x, ‖g x‖ ≤ C) :
    ∃ A : Lp ℂ 2 (volume : Measure E) →L[ℂ] Lp ℂ 2 (volume : Measure E),
      (∀ f, Lp.toTemperedDistribution (A f) =
        TemperedDistribution.fourierMultiplierCLM ℂ g (Lp.toTemperedDistribution f)) ∧
      ∀ φ : SchwartzMap E ℂ, A (φ.toLp 2) =
        (SchwartzMap.fourierMultiplierCLM ℂ g φ).toLp 2 := by
  obtain ⟨A,hA⟩ := actual_bounded_multiplier g hg C hC
  refine ⟨A,hA,?_⟩
  intro φ
  apply lp_td_injective
  rw [hA,Lp.toTemperedDistribution_toLp_eq,
    TemperedDistribution.fourierMultiplierCLM_toTemperedDistributionCLM_eq hg,
    Lp.toTemperedDistribution_toLp_eq]

theorem actual_bounded_multiplier_norm (g : E → ℂ) (hg : g.HasTemperateGrowth)
    (C : ℝ) (hC : ∀ x, ‖g x‖ ≤ C) :
    ∃ A : Lp ℂ 2 (volume : Measure E) →L[ℂ] Lp ℂ 2 (volume : Measure E),
      (∀ f, ‖A f‖ ≤ C * ‖f‖) ∧
      (∀ f, Lp.toTemperedDistribution (A f) =
        TemperedDistribution.fourierMultiplierCLM ℂ g (Lp.toTemperedDistribution f)) ∧
      ∀ φ : SchwartzMap E ℂ, A (φ.toLp 2) =
        (SchwartzMap.fourierMultiplierCLM ℂ g φ).toLp 2 := by
  let gc : E →ᵇ ℂ := BoundedContinuousFunction.ofNormedAddCommGroup g hg.1.continuous C hC
  let gl : Lp ℂ ∞ (volume : Measure E) := gc.memLp_top.toLp g (μ := volume)
  let A : Lp ℂ 2 (volume : Measure E) →L[ℂ] Lp ℂ 2 (volume : Measure E) :=
    fourierInvCLM ℂ _ ∘L actualMul gl ∘L fourierCLM ℂ _
  have hA : ∀ f, Lp.toTemperedDistribution (A f) =
      TemperedDistribution.fourierMultiplierCLM ℂ g (Lp.toTemperedDistribution f) := by
    intro f
    change Lp.toTemperedDistribution (𝓕⁻ (actualMul gl (𝓕 f))) = _
    rw [actualMul_eq, ← Lp.fourierInv_toTemperedDistribution_eq,
      Lp.toTemperedDistribution_smul_eq hg gc.memLp_top,
      ← Lp.fourier_toTemperedDistribution_eq]
    rfl
  refine ⟨A,?_,hA,?_⟩
  · intro f
    have hC0 : 0 ≤ C := (norm_nonneg (g 0)).trans (hC 0)
    have hgl : ‖gl‖ ≤ C := by
      change ‖gc.memLp_top.toLp g (μ := volume)‖ ≤ C
      rw [Lp.norm_toLp (μ := (volume : Measure E)) g gc.memLp_top]
      exact (ENNReal.toReal_mono (by finiteness)
        (eLpNormEssSup_le_of_ae_bound (Filter.Eventually.of_forall hC))).trans_eq
        (ENNReal.toReal_ofReal hC0)
    change ‖𝓕⁻ (actualMul gl (𝓕 f))‖ ≤ _
    have hn : ‖𝓕⁻ (actualMul gl (𝓕 f))‖ = ‖actualMul gl (𝓕 f)‖ := by
      simpa using (Lp.norm_fourier_eq (𝓕⁻ (actualMul gl (𝓕 f)))).symm
    rw [hn,actualMul_eq]
    exact (Lp.norm_smul_le (r := 2) gl (𝓕 f)).trans
      (by simpa using mul_le_mul_of_nonneg_right hgl (norm_nonneg (𝓕 f)))
  · intro φ
    apply lp_td_injective
    rw [hA,Lp.toTemperedDistribution_toLp_eq,
      TemperedDistribution.fourierMultiplierCLM_toTemperedDistributionCLM_eq hg,
      Lp.toTemperedDistribution_toLp_eq]

private def mzero (x : E) : ℂ := ((1+‖x‖^2)^(-1:ℝ) : ℝ)
private def mlap (x : E) : ℂ := (‖x‖^2 * (1+‖x‖^2)^(-1:ℝ) : ℝ)
private def mdir (a : E) (x : E) : ℂ := (inner ℝ x a * (1+‖x‖^2)^(-1:ℝ) : ℝ)

private theorem mzero_growth : (mzero : E → ℂ).HasTemperateGrowth := by
  unfold mzero; fun_prop
private theorem mlap_growth : (mlap : E → ℂ).HasTemperateGrowth := by
  unfold mlap; fun_prop
private theorem mdir_growth (a : E) : (mdir a).HasTemperateGrowth := by
  unfold mdir; fun_prop
private theorem mzero_bound (x : E) : ‖mzero x‖ ≤ 1 := by
  simp only [mzero,Real.rpow_neg_one,Complex.norm_real,Real.norm_eq_abs,
    abs_of_nonneg (by positivity : 0 ≤ (1+‖x‖^2)⁻¹)]
  exact (inv_le_one₀ (by positivity)).mpr (by nlinarith [sq_nonneg ‖x‖])
private theorem mlap_bound (x : E) : ‖mlap x‖ ≤ 1 := by
  simp only [mlap,Real.rpow_neg_one,Complex.norm_real,Real.norm_eq_abs,
    abs_of_nonneg (by positivity : 0 ≤ ‖x‖^2*(1+‖x‖^2)⁻¹)]
  rw [mul_inv_le_iff₀ (by positivity)]
  linarith
private theorem mdir_bound (a x : E) : ‖mdir a x‖ ≤ ‖a‖ := by
  simp only [mdir,Real.rpow_neg_one,Complex.norm_real,Real.norm_eq_abs,
    abs_mul,abs_of_nonneg (by positivity : 0 ≤ (1+‖x‖^2)⁻¹)]
  rw [mul_inv_le_iff₀ (by positivity)]
  have h : ‖x‖ ≤ 1+‖x‖^2 := by nlinarith [sq_nonneg (‖x‖-1)]
  exact (abs_real_inner_le_norm x a).trans (by nlinarith [norm_nonneg a])

private theorem inverse_lap (t : 𝓢'(E,ℂ)) :
    Δ (TemperedDistribution.fourierMultiplierCLM ℂ (mzero : E → ℂ) t) =
      ((-(2*Real.pi)^2 : ℝ) : ℂ) • TemperedDistribution.fourierMultiplierCLM ℂ mlap t := by
  rw [TemperedDistribution.laplacian_eq_fourierMultiplierCLM,
    TemperedDistribution.fourierMultiplierCLM_fourierMultiplierCLM_apply
      mzero_growth (by fun_prop)]
  have hm : (mzero * fun x : E => ((‖x‖^2 : ℝ) : ℂ)) = mlap := by
    funext x; simp [mzero,mlap,Pi.mul_def,mul_comm]
  rw [hm,Complex.coe_smul]

private theorem inverse_dir (a : E) (t : 𝓢'(E,ℂ)) :
    ∂_{a} (TemperedDistribution.fourierMultiplierCLM ℂ (mzero : E → ℂ) t) =
      (2*Real.pi*Complex.I) • TemperedDistribution.fourierMultiplierCLM ℂ (mdir a) t := by
  rw [TemperedDistribution.lineDeriv_eq_fourierMultiplierCLM,
    TemperedDistribution.fourierMultiplierCLM_fourierMultiplierCLM_apply
      mzero_growth (by fun_prop)]
  have hm : (mzero * fun x : E => (inner ℝ x a : ℂ)) = mdir a := by
    funext x; simp [mzero,mdir,Pi.mul_def,mul_comm]
  rw [hm]

private theorem schwartz_approx (w : Lp ℂ 2 (volume : Measure E)) :
    ∃ q : ℕ → SchwartzMap E ℂ,
      Filter.Tendsto (fun n => (q n).toLp 2 volume) Filter.atTop (𝓝 w) := by
  have hd := SchwartzMap.denseRange_toLpCLM (F := ℂ) (p := 2)
    (μ := (volume : Measure E)) ENNReal.ofNat_ne_top
  obtain ⟨r,hr,ht⟩ := mem_closure_iff_seq_limit.mp (hd w)
  choose q hq using hr
  refine ⟨q,?_⟩
  have hrq : r = fun n => (q n).toLp 2 volume := by
    funext n; exact (hq n).symm
  simpa only [hrq] using ht

private theorem spectral_graph (vc Fc : Lp ℂ 2 (volume : Measure E))
    (hs : MemSobolev 2 2 (Lp.toTemperedDistribution vc))
    (hl : Δ (Lp.toTemperedDistribution vc) = Lp.toTemperedDistribution Fc) :
    ∃ s : ℕ → SchwartzMap E ℂ,
      Filter.Tendsto (fun n => (s n).toLp 2 volume) Filter.atTop (𝓝 vc) ∧
      Filter.Tendsto (fun n => (Δ (s n)).toLp 2 volume) Filter.atTop (𝓝 Fc) ∧
      ∀ a : E, ∃ ga : Lp ℂ 2 (volume : Measure E),
        Lp.toTemperedDistribution ga = ∂_{a} (Lp.toTemperedDistribution vc) ∧
        Filter.Tendsto (fun n => (∂_{a} (s n)).toLp 2 volume)
          Filter.atTop (𝓝 ga) := by
  obtain ⟨w,hw⟩ := hs
  obtain ⟨A0,h0norm,h0td,h0s⟩ :=
    actual_bounded_multiplier_norm (E := E) mzero mzero_growth 1 mzero_bound
  have hz : Lp.toTemperedDistribution (A0 w) = Lp.toTemperedDistribution vc := by
    rw [h0td]
    have hb := (besselPotential_neg_apply_eq_iff 2 (Lp.toTemperedDistribution w)
      (Lp.toTemperedDistribution vc)).mpr hw
    change (TemperedDistribution.fourierMultiplierCLM ℂ
      (fun x : E => (((1+‖x‖^2)^(-1:ℝ) : ℝ) : ℂ)))
      (Lp.toTemperedDistribution w) = _
    simpa only [besselPotential,show (-(2:ℝ))/2 = -1 by norm_num] using hb
  have hv : A0 w = vc := lp_td_injective hz
  obtain ⟨AL,hLnorm,hLtd,hLs⟩ :=
    actual_bounded_multiplier_norm (E := E) mlap mlap_growth 1 mlap_bound
  have hLF : ((-(2*Real.pi)^2 : ℝ) : ℂ) • AL w = Fc := by
    apply lp_td_injective
    rw [← hl, ← hz, h0td, inverse_lap]
    change (Lp.toTemperedDistributionCLM ℂ volume 2)
      (((-(2*Real.pi)^2 : ℝ) : ℂ) • AL w) = _
    rw [map_smul,Lp.toTemperedDistributionCLM_apply,hLtd]
  obtain ⟨q,hq⟩ := schwartz_approx w
  let s : ℕ → SchwartzMap E ℂ := fun n => SchwartzMap.fourierMultiplierCLM ℂ mzero (q n)
  have hs0 : ∀ n, (s n).toLp 2 volume = A0 ((q n).toLp 2 volume) := by
    intro n; exact (h0s (q n)).symm
  have hsL : ∀ n, (Δ (s n)).toLp 2 volume =
      ((-(2*Real.pi)^2 : ℝ) : ℂ) • AL ((q n).toLp 2 volume) := by
    intro n
    apply lp_td_injective
    rw [Lp.toTemperedDistribution_toLp_eq,
      ← TemperedDistribution.laplacian_toTemperedDistributionCLM_eq]
    rw [← Lp.toTemperedDistribution_toLp_eq (p := 2) (s n)]
    rw [hs0,h0td,inverse_lap]
    change _ = (Lp.toTemperedDistributionCLM ℂ volume 2)
      (((-(2*Real.pi)^2 : ℝ) : ℂ) • AL ((q n).toLp 2 volume))
    rw [map_smul,Lp.toTemperedDistributionCLM_apply,hLtd]
  refine ⟨s,?_,?_,?_⟩
  · simpa only [hs0,hv,Function.comp_def] using A0.continuous.continuousAt.tendsto.comp hq
  · rw [← hLF]
    simpa only [hsL,Function.comp_def] using
      (AL.continuous.continuousAt.tendsto.comp hq).const_smul ((-(2*Real.pi)^2 : ℝ) : ℂ)
  · intro a
    obtain ⟨AD,hDnorm,hDtd,hDs⟩ :=
      actual_bounded_multiplier_norm (mdir a) (mdir_growth a) ‖a‖ (mdir_bound a)
    let ga := (2*Real.pi*Complex.I) • AD w
    have hg : Lp.toTemperedDistribution ga = ∂_{a} (Lp.toTemperedDistribution vc) := by
      rw [← hz,h0td,inverse_dir]
      change (Lp.toTemperedDistributionCLM ℂ volume 2)
        ((2*Real.pi*Complex.I) • AD w) = _
      rw [map_smul,Lp.toTemperedDistributionCLM_apply,hDtd]
    have hsD : ∀ n, (∂_{a} (s n)).toLp 2 volume =
        (2*Real.pi*Complex.I) • AD ((q n).toLp 2 volume) := by
      intro n
      apply lp_td_injective
      rw [Lp.toTemperedDistribution_toLp_eq,
        ← TemperedDistribution.lineDerivOp_toTemperedDistributionCLM_eq]
      rw [← Lp.toTemperedDistribution_toLp_eq (p := 2) (s n)]
      rw [hs0,h0td,inverse_dir]
      change _ = (Lp.toTemperedDistributionCLM ℂ volume 2)
        ((2*Real.pi*Complex.I) • AD ((q n).toLp 2 volume))
      rw [map_smul,Lp.toTemperedDistributionCLM_apply,hDtd]
    refine ⟨ga,hg,?_⟩
    simpa only [hsD,ga,Function.comp_def] using
      (AD.continuous.continuousAt.tendsto.comp hq).const_smul (2*Real.pi*Complex.I)

#print axioms spectral_graph
#print axioms inverse_lap
#print axioms inverse_dir
#print axioms actual_bounded_multiplier
#print axioms actual_bounded_multiplier_schwartz
#print axioms actual_bounded_multiplier_norm
end BoundedSpectralPrototype
