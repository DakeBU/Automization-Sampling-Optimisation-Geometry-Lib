import AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.CompactWeakPoissonSobolev
import AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.GradientAlgebra

set_option autoImplicit false
noncomputable section
open ENNReal MeasureTheory FourierTransform TemperedDistribution
open scoped SchwartzMap BoundedContinuousFunction
open scoped Topology Laplacian LineDeriv
open InnerProductSpace LineDeriv
namespace AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.CompactPoissonSmoothGraph
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

private theorem lp_td_injective : Function.Injective
    (Lp.toTemperedDistribution : Lp ℂ 2 (volume : Measure E) → 𝓢'(E,ℂ)) := by
  exact LinearMap.ker_eq_bot.mp (Lp.ker_toTemperedDistributionCLM_eq_bot
    (F := ℂ) (μ := volume) (p := 2))

private theorem actual_bounded_multiplier_norm (g : E → ℂ) (hg : g.HasTemperateGrowth)
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

omit [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E] in
private theorem mzero_growth : (mzero : E → ℂ).HasTemperateGrowth := by
  unfold mzero; fun_prop
omit [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E] in
private theorem mlap_growth : (mlap : E → ℂ).HasTemperateGrowth := by
  unfold mlap; fun_prop
omit [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E] in
private theorem mdir_growth (a : E) : (mdir a).HasTemperateGrowth := by
  unfold mdir; fun_prop
omit [InnerProductSpace ℝ E] [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E] in
private theorem mzero_bound (x : E) : ‖mzero x‖ ≤ 1 := by
  simp only [mzero,Real.rpow_neg_one,Complex.norm_real,Real.norm_eq_abs,
    abs_of_nonneg (by positivity : 0 ≤ (1+‖x‖^2)⁻¹)]
  exact (inv_le_one₀ (by positivity)).mpr (by nlinarith [sq_nonneg ‖x‖])
omit [InnerProductSpace ℝ E] [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E] in
private theorem mlap_bound (x : E) : ‖mlap x‖ ≤ 1 := by
  simp only [mlap,Real.rpow_neg_one,Complex.norm_real,Real.norm_eq_abs,
    abs_of_nonneg (by positivity : 0 ≤ ‖x‖^2*(1+‖x‖^2)⁻¹)]
  rw [mul_inv_le_iff₀ (by positivity)]
  linarith
omit [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E] in
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
    funext x; simp [mzero,mlap,mul_comm]
  rw [hm,Complex.coe_smul]

private theorem inverse_dir (a : E) (t : 𝓢'(E,ℂ)) :
    ∂_{a} (TemperedDistribution.fourierMultiplierCLM ℂ (mzero : E → ℂ) t) =
      (2*Real.pi*Complex.I) • TemperedDistribution.fourierMultiplierCLM ℂ (mdir a) t := by
  rw [TemperedDistribution.lineDeriv_eq_fourierMultiplierCLM,
    TemperedDistribution.fourierMultiplierCLM_fourierMultiplierCLM_apply
      mzero_growth (by fun_prop)]
  have hm : (mzero * fun x : E => (inner ℝ x a : ℂ)) = mdir a := by
    funext x; simp [mzero,mdir,mul_comm]
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

omit [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E] in
private theorem real_postcomp_derivative (ψ : SchwartzMap E ℝ) (a : E) :
    ∂_{a} (ψ.postcompCLM Complex.ofRealCLM) =
      (∂_{a} ψ).postcompCLM Complex.ofRealCLM := by
  ext x
  simp only [SchwartzMap.lineDerivOp_apply_eq_fderiv, SchwartzMap.postcompCLM_apply]
  change (fderiv ℝ (Complex.ofRealCLM ∘ (ψ : E → ℝ)) x) a =
    Complex.ofRealCLM ((fderiv ℝ (ψ : E → ℝ) x) a)
  exact congrArg (fun L : E →L[ℝ] ℂ => L a)
    ((Complex.ofRealCLM.hasFDerivAt.comp x (ψ.hasFDerivAt x)).fderiv)

private theorem identify_real_gradient (v : E → ℝ) (G : E → E)
    (hG : MemLp G 2 volume)
    (vc ga : Lp ℂ 2 (volume : Measure E))
    (hvc : vc =ᵐ[volume] (fun x => (v x : ℂ))) (a : E)
    (hga : Lp.toTemperedDistribution ga = ∂_{a} (Lp.toTemperedDistribution vc))
    (hd : ∀ ψ : E → ℝ, ContDiff ℝ 1 ψ → HasCompactSupport ψ →
      Integrable (fun x => ψ x * inner ℝ (G x) a) volume ∧
      Integrable (fun x => v x * fderiv ℝ ψ x a) volume ∧
      (∫ x, ψ x * inner ℝ (G x) a) = -∫ x, v x * fderiv ℝ ψ x a) :
    (fun x => (ga x).re) =ᵐ[volume] (fun x => inner ℝ (G x) a) := by
  have hreal : MemLp (fun x => (ga x).re) 2 volume :=
    (Lp.memLp ga).continuousLinearMap_comp Complex.reCLM
  have hinner : MemLp (fun x => inner ℝ (G x) a) 2 volume := by
    simpa only [innerSL_apply_apply,real_inner_comm] using
      hG.continuousLinearMap_comp (innerSL ℝ a)
  apply ae_eq_of_integral_contDiff_smul_eq
    (hreal.locallyIntegrable (by norm_num)) (hinner.locallyIntegrable (by norm_num))
  intro φ hφ hc
  let ψ : SchwartzMap E ℝ := hc.toSchwartzMap hφ
  let ψC : SchwartzMap E ℂ := ψ.postcompCLM Complex.ofRealCLM
  have hψ : (ψ : E → ℝ) = φ := rfl
  have hweak := hd φ (contDiff_infty.mp hφ 1) hc
  have hcomplex : Integrable (fun x => ψC x * ga x) volume :=
    (ψC.memLp 2 volume).integrable_mul (Lp.memLp ga)
  have hpair := congrArg (fun T : 𝓢'(E,ℂ) => T ψC) hga
  rw [TemperedDistribution.lineDerivOp_apply_apply,
    Lp.toTemperedDistribution_apply,Lp.toTemperedDistribution_apply] at hpair
  have hder : ∂_{a} ψC = (∂_{a} ψ).postcompCLM Complex.ofRealCLM :=
    real_postcomp_derivative ψ a
  have hright : (∫ x, (-∂_{a} ψC) x • vc x) =
      -((∫ x, v x * fderiv ℝ φ x a : ℝ) : ℂ) := by
    simp only [neg_apply,neg_smul,integral_neg]
    congr 1
    calc
      _ = ∫ x, ((∂_{a} ψ) x : ℂ) * (v x : ℂ) := by
        apply integral_congr_ae
        filter_upwards [hvc] with x hx
        simp only [hder,hx,SchwartzMap.postcompCLM_apply,
          Complex.ofRealCLM_apply,smul_eq_mul]
      _ = _ := by
        simp only [SchwartzMap.lineDerivOp_apply_eq_fderiv,hψ,
          ← Complex.ofReal_mul,mul_comm]
        exact integral_ofReal
  rw [hright] at hpair
  have hh := congrArg Complex.re hpair
  rw [show (fun x => ψC x • ga x) = (fun x => ψC x * ga x) from rfl] at hh
  have hre := integral_re hcomplex
  simp only [RCLike.re_to_complex] at hre
  rw [← hre] at hh
  have heq : (∫ x, φ x * (ga x).re) = -∫ x, v x * fderiv ℝ φ x a := by
    simpa only [Complex.ofReal_re,Complex.neg_re,SchwartzMap.postcompCLM_apply,
      Complex.ofRealCLM_apply,Complex.mul_re,Complex.ofReal_im,zero_mul,sub_zero,
      ψC,hψ] using hh
  simpa only [smul_eq_mul] using heq.trans hweak.2.2.symm


private theorem real_projection_toLp (ψ : SchwartzMap E ℂ) :
    Complex.reCLM.compLpL 2 volume (ψ.toLp 2 volume) =
      (ψ.postcompCLM Complex.reCLM).toLp 2 volume := by
  apply Lp.ext
  filter_upwards [Complex.reCLM.coeFn_compLpL (ψ.toLp 2 volume),
    ψ.coeFn_toLp 2 volume,(ψ.postcompCLM Complex.reCLM).coeFn_toLp 2 volume]
    with x hx hy hz
  simp only [SchwartzMap.postcompCLM_apply] at hz
  exact hx.trans ((congrArg Complex.reCLM hy).trans hz.symm)

omit [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E] in
private theorem real_projection_line (ψ : SchwartzMap E ℂ) (a : E) :
    ∂_{a} (ψ.postcompCLM Complex.reCLM) =
      (∂_{a} ψ).postcompCLM Complex.reCLM := by
  ext x
  simp only [SchwartzMap.lineDerivOp_apply_eq_fderiv,SchwartzMap.postcompCLM_apply]
  change (fderiv ℝ (Complex.reCLM ∘ (ψ : E → ℂ)) x) a =
    Complex.reCLM ((fderiv ℝ (ψ : E → ℂ) x) a)
  exact congrArg (fun L : E →L[ℝ] ℝ => L a)
    ((Complex.reCLM.hasFDerivAt.comp x (ψ.hasFDerivAt x)).fderiv)

omit [MeasurableSpace E] [BorelSpace E] in
private theorem real_projection_lap (ψ : SchwartzMap E ℂ) :
    Δ (ψ.postcompCLM Complex.reCLM) = (Δ ψ).postcompCLM Complex.reCLM := by
  ext x
  simp only [SchwartzMap.laplacian_apply,SchwartzMap.postcompCLM_apply]
  change Laplacian.laplacian (Complex.reCLM ∘ (ψ : E → ℂ)) x =
    Complex.reCLM (Laplacian.laplacian (ψ : E → ℂ) x)
  exact (ψ.contDiffAt 2).laplacian_CLM_comp_left (l := Complex.reCLM)

private def schwartz_gradient (ψ : SchwartzMap E ℝ) : SchwartzMap E E :=
  (SchwartzMap.fderivCLM ℝ E ℝ ψ).postcompCLM
    (toDual ℝ E).symm.toContinuousLinearEquiv.toContinuousLinearMap

omit [MeasurableSpace E] [BorelSpace E] in
private theorem schwartz_gradient_apply (ψ : SchwartzMap E ℝ) (x : E) :
    schwartz_gradient ψ x = gradient (ψ : E → ℝ) x := rfl

private theorem real_projection_class (v : E → ℝ) (hv : MemLp v 2 volume)
    (vc : Lp ℂ 2 (volume : Measure E))
    (hvc : vc =ᵐ[volume] (fun x => (v x : ℂ))) :
    Complex.reCLM.compLpL 2 volume vc = hv.toLp v := by
  apply Lp.ext
  filter_upwards [Complex.reCLM.coeFn_compLpL vc,hvc,hv.coeFn_toLp] with x hx hy hz
  calc
    _ = Complex.reCLM (vc x) := hx
    _ = v x := by simp only [hy,Complex.reCLM_apply,Complex.ofReal_re]
    _ = _ := hz.symm

private theorem finite_gradient_reconstruction (ψ : SchwartzMap E ℝ) :
    (schwartz_gradient ψ).toLp 2 volume =
      ∑ i, ((ContinuousLinearMap.toSpanSingleton ℝ ((stdOrthonormalBasis ℝ E) i)).compLpL
        2 volume) ((∂_{(stdOrthonormalBasis ℝ E) i} ψ).toLp 2 volume) := by
  let b := stdOrthonormalBasis ℝ E
  have hg : ∀ x, schwartz_gradient ψ x = ∑ i, fderiv ℝ (ψ : E → ℝ) x (b i) • b i := by
    intro x
    rw [schwartz_gradient_apply]
    simpa only [inner_gradient_right,conj_trivial,← inner_gradient_left] using
      (b.sum_repr' (gradient (ψ : E → ℝ) x)).symm
  apply Lp.ext
  have hsum := Lp.coeFn_fun_finsetSum Finset.univ
    (fun i => ((ContinuousLinearMap.toSpanSingleton ℝ (b i)).compLpL
      2 volume) ((∂_{b i} ψ).toLp 2 volume))
  have hzall : ∀ᵐ x ∂(volume : Measure E), ∀ i,
      ((ContinuousLinearMap.toSpanSingleton ℝ (b i)).compLpL 2 volume
        ((∂_{b i} ψ).toLp 2 volume)) x =
          (ContinuousLinearMap.toSpanSingleton ℝ (b i)) (((∂_{b i} ψ).toLp 2 volume) x) :=
    Filter.eventually_all.mpr (fun i => by
      exact ContinuousLinearMap.coeFn_compLpL
        (ContinuousLinearMap.toSpanSingleton ℝ (b i))
        ((∂_{b i} ψ).toLp 2 (volume : Measure E)))
  have htall : ∀ᵐ x ∂(volume : Measure E), ∀ i,
      ((∂_{b i} ψ).toLp 2 volume) x = (∂_{b i} ψ) x :=
    Filter.eventually_all.mpr (fun i => (∂_{b i} ψ).coeFn_toLp 2 volume)
  filter_upwards [(schwartz_gradient ψ).coeFn_toLp 2 volume,hsum,
    hzall,htall] with x hx hy hz ht
  rw [hx,hg,hy]
  apply Finset.sum_congr rfl
  intro i _
  simpa only [ht i,SchwartzMap.lineDerivOp_apply_eq_fderiv,
    ContinuousLinearMap.toSpanSingleton_apply] using (hz i).symm

private theorem real_schwartz_graph (v F : E → ℝ) (G : E → E)
    (hv : MemLp v 2 volume) (hF : MemLp F 2 volume) (hG : MemLp G 2 volume)
    (vc Fc : Lp ℂ 2 (volume : Measure E))
    (hvc : vc =ᵐ[volume] (fun x => (v x : ℂ)))
    (hFc : Fc =ᵐ[volume] (fun x => (F x : ℂ)))
    (hs : MemSobolev 2 2 (Lp.toTemperedDistribution vc))
    (hl : Δ (Lp.toTemperedDistribution vc) = Lp.toTemperedDistribution Fc)
    (hd : ∀ ψ : E → ℝ, ContDiff ℝ 1 ψ → HasCompactSupport ψ → ∀ a : E,
      Integrable (fun x => ψ x * inner ℝ (G x) a) volume ∧
      Integrable (fun x => v x * fderiv ℝ ψ x a) volume ∧
      (∫ x, ψ x * inner ℝ (G x) a) = -∫ x, v x * fderiv ℝ ψ x a) :
    ∃ r : ℕ → SchwartzMap E ℝ,
      Filter.Tendsto (fun n => (r n).toLp 2 volume) Filter.atTop (𝓝 (hv.toLp v)) ∧
      Filter.Tendsto (fun n => (schwartz_gradient (r n)).toLp 2 volume)
        Filter.atTop (𝓝 (hG.toLp G)) ∧
      Filter.Tendsto (fun n => (Δ (r n)).toLp 2 volume)
        Filter.atTop (𝓝 (hF.toLp F)) := by
  obtain ⟨s,hsv,hsF,hsG⟩ := spectral_graph vc Fc hs hl
  let R : Lp ℂ 2 (volume : Measure E) →L[ℝ] Lp ℝ 2 (volume : Measure E) :=
    Complex.reCLM.compLpL 2 volume
  let r : ℕ → SchwartzMap E ℝ := fun n => (s n).postcompCLM Complex.reCLM
  let b := stdOrthonormalBasis ℝ E
  choose ga hga hgat using (fun i : Fin (Module.finrank ℝ E) => hsG (b i))
  have hreal (i : Fin (Module.finrank ℝ E)) :
      (R (ga i) : E → ℝ) =ᵐ[volume] fun x => inner ℝ (G x) (b i) := by
    have hi := identify_real_gradient v G hG vc (ga i) hvc (b i) (hga i)
      (fun ψ hψ hc => hd ψ hψ hc (b i))
    exact (Complex.reCLM.coeFn_compLpL (ga i)).trans hi
  have hdir (i : Fin (Module.finrank ℝ E)) :
      Filter.Tendsto (fun n => (∂_{b i} (r n)).toLp 2 volume)
        Filter.atTop (𝓝 (R (ga i))) := by
    simpa only [R,Function.comp_def,real_projection_toLp,← real_projection_line,r] using
      R.continuous.continuousAt.tendsto.comp (hgat i)
  have hsumG : (∑ i, ((ContinuousLinearMap.toSpanSingleton ℝ (b i)).compLpL 2 volume)
      (R (ga i))) = hG.toLp G := by
    apply Lp.ext
    have hsum := Lp.coeFn_fun_finsetSum Finset.univ
      (fun i => ((ContinuousLinearMap.toSpanSingleton ℝ (b i)).compLpL 2 volume) (R (ga i)))
    have hmaps : ∀ᵐ x ∂(volume : Measure E), ∀ i,
        (((ContinuousLinearMap.toSpanSingleton ℝ (b i)).compLpL 2 volume)
          (R (ga i))) x = (R (ga i) x) • b i :=
      Filter.eventually_all.mpr (fun i => by
        filter_upwards [(ContinuousLinearMap.toSpanSingleton ℝ (b i)).coeFn_compLpL
          (R (ga i))] with x hx
        exact hx)
    filter_upwards [hsum,hmaps,Filter.eventually_all.mpr hreal,hG.coeFn_toLp]
      with x hx hy hz ht
    rw [hx,ht]
    calc
      _ = ∑ i, inner ℝ (G x) (b i) • b i := by
        apply Finset.sum_congr rfl
        intro i _; rw [hy i,hz i]
      _ = G x := by simpa only [real_inner_comm] using b.sum_repr' (G x)
  refine ⟨r,?_,?_,?_⟩
  · rw [← real_projection_class v hv vc hvc]
    simpa only [R,Function.comp_def,real_projection_toLp,r] using
      R.continuous.continuousAt.tendsto.comp hsv
  · rw [← hsumG]
    have ht := tendsto_finsetSum Finset.univ (fun i _ =>
      ((ContinuousLinearMap.toSpanSingleton ℝ (b i)).compLpL 2 volume).continuous.continuousAt.tendsto.comp
        (hdir i))
    simpa only [Function.comp_def,← finite_gradient_reconstruction,b] using ht
  · rw [← real_projection_class F hF Fc hFc]
    simpa only [R,Function.comp_def,real_projection_toLp,← real_projection_lap,r] using
      R.continuous.continuousAt.tendsto.comp hsF


/- The source-localization module has no public Laplacian product API.
These private C2 trace identities reuse its audited proof route; no new public
background node or graph-density assumption is introduced. -/
omit [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E] in
private theorem directional_second (f : E → ℝ) (hf : ContDiff ℝ 2 f) (x v : E) :
    fderiv ℝ (fun z => fderiv ℝ f z v) x v = fderiv ℝ (fderiv ℝ f) x v v := by
  have hd := ((hf.fderiv_right (m := 1) (by norm_num)).differentiable one_ne_zero x).hasFDerivAt
  simpa using congrArg (fun T : E →L[ℝ] ℝ => T v)
    (hd.clm_apply (hasFDerivAt_const v x)).fderiv

omit [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E] in
private theorem first_product (χ φ : E → ℝ) (hχ : ContDiff ℝ 1 χ)
    (hφ : ContDiff ℝ 1 φ) (x v : E) :
    fderiv ℝ (fun z => χ z * φ z) x v =
      χ x * fderiv ℝ φ x v + φ x * fderiv ℝ χ x v := by
  have hd := (hχ.differentiable one_ne_zero x).hasFDerivAt.mul
    (hφ.differentiable one_ne_zero x).hasFDerivAt
  rw [show fderiv ℝ (fun z => χ z * φ z) x = _ from hd.fderiv]
  simp only [add_apply, smul_apply, smul_eq_mul]

omit [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E] in
private theorem second_product (χ φ : E → ℝ) (hχ : ContDiff ℝ 2 χ)
    (hφ : ContDiff ℝ 2 φ) (x v : E) :
    fderiv ℝ (fderiv ℝ (fun z => χ z * φ z)) x v v =
      χ x * fderiv ℝ (fderiv ℝ φ) x v v +
      2 * (fderiv ℝ χ x v * fderiv ℝ φ x v) +
      φ x * fderiv ℝ (fderiv ℝ χ) x v v := by
  have hχ1 : ContDiff ℝ 1 χ := hχ.of_le (by norm_num)
  have hφ1 : ContDiff ℝ 1 φ := hφ.of_le (by norm_num)
  have hχd : ContDiff ℝ 1 (fun z => fderiv ℝ χ z v) :=
    (hχ.fderiv_right (m := 1) (by norm_num)).clm_apply contDiff_const
  have hφd : ContDiff ℝ 1 (fun z => fderiv ℝ φ z v) :=
    (hφ.fderiv_right (m := 1) (by norm_num)).clm_apply contDiff_const
  have he : (fun z => fderiv ℝ (fun w => χ w * φ w) z v) =
      fun z => χ z * fderiv ℝ φ z v + φ z * fderiv ℝ χ z v := by
    funext z; exact first_product χ φ hχ1 hφ1 z v
  rw [← directional_second _ (hχ.mul hφ), he]
  have hd := ((hχ1.differentiable one_ne_zero x).hasFDerivAt.mul
    (hφd.differentiable one_ne_zero x).hasFDerivAt).add
    ((hφ1.differentiable one_ne_zero x).hasFDerivAt.mul
      (hχd.differentiable one_ne_zero x).hasFDerivAt)
  rw [show fderiv ℝ (fun z => χ z * fderiv ℝ φ z v + φ z * fderiv ℝ χ z v) x = _ from hd.fderiv]
  simp only [add_apply, smul_apply, smul_eq_mul]
  rw [directional_second _ hφ, directional_second _ hχ]
  ring

omit [MeasurableSpace E] [BorelSpace E] in
private theorem laplacian_trace (f : E → ℝ) (x : E) :
    Laplacian.laplacian f x = ∑ i, fderiv ℝ (fderiv ℝ f) x
      ((stdOrthonormalBasis ℝ E) i) ((stdOrthonormalBasis ℝ E) i) := by
  rw [InnerProductSpace.laplacian_eq_iteratedFDeriv_stdOrthonormalBasis]
  apply Finset.sum_congr rfl
  intro i _
  rw [iteratedFDeriv_two_apply]
  rfl

omit [MeasurableSpace E] [BorelSpace E] in
private theorem laplacian_product (χ φ : E → ℝ) (hχ : ContDiff ℝ 2 χ)
    (hφ : ContDiff ℝ 2 φ) (x : E) :
    Laplacian.laplacian (fun z => χ z * φ z) x =
      χ x * Laplacian.laplacian φ x +
      2 * inner ℝ (gradient χ x) (gradient φ x) +
      φ x * Laplacian.laplacian χ x := by
  have hi : inner ℝ (gradient χ x) (gradient φ x) =
      ∑ i, fderiv ℝ χ x ((stdOrthonormalBasis ℝ E) i) *
        fderiv ℝ φ x ((stdOrthonormalBasis ℝ E) i) := by
    rw [← (stdOrthonormalBasis ℝ E).sum_inner_mul_inner (gradient χ x) (gradient φ x)]
    simp only [inner_gradient_left, inner_gradient_right, conj_trivial]
  rw [laplacian_trace, laplacian_trace, laplacian_trace, hi]
  simp_rw [second_product χ φ hχ hφ]
  simp only [Finset.sum_add_distrib, ← Finset.mul_sum]



omit [MeasurableSpace E] [BorelSpace E] in
private theorem outer_plateau (K : Set E) (hK : IsCompact K) :
    ∃ θ : SchwartzMap E ℝ, HasCompactSupport (θ : E → ℝ) ∧
      ∀ x ∈ K, (θ : E → ℝ) =ᶠ[𝓝 x] (fun _ => 1) := by
  obtain ⟨R,hR,hKR⟩ := hK.isBounded.subset_ball_lt 0 (0:E)
  let b : ContDiffBump (0:E) :=
    {rIn := R,rOut := R+1,rIn_pos := hR,rIn_lt_rOut := by linarith}
  let θ : SchwartzMap E ℝ := b.hasCompactSupport.toSchwartzMap b.contDiff
  refine ⟨θ,b.hasCompactSupport,?_⟩
  intro x hx
  exact b.eventuallyEq_one_of_mem_ball (hKR hx)

private theorem coeff_holder_ae {F H O : Type*}
    [NormedAddCommGroup F] [NormedSpace ℝ F]
    [NormedAddCommGroup H] [NormedSpace ℝ H]
    [NormedAddCommGroup O] [NormedSpace ℝ O]
    (B : F →L[ℝ] H →L[ℝ] O) (u : SchwartzMap E F)
    (f : Lp H 2 (volume : Measure E)) :
    ((B.holderL volume ∞ 2 2) (u.toLp ∞ volume) f : E → O) =ᵐ[volume]
      fun x => B (u x) (f x) := by
  change (B.holder 2 (u.toLp ∞ volume) f : E → O) =ᵐ[volume] _
  filter_upwards [B.coeFn_holder (r := 2) (u.toLp ∞ volume) f,
    u.coeFn_toLp ∞ volume] with x hx hu
  exact hx.trans (by rw [hu])

omit [MeasurableSpace E] [BorelSpace E] in
private theorem plateau_point_identities (v F : E → ℝ) (G : E → E) (K : Set E)
    (hv : tsupport v ⊆ K) (hF : tsupport F ⊆ K) (hG : tsupport G ⊆ K)
    (θ : SchwartzMap E ℝ)
    (hθ : ∀ x ∈ K, (θ : E → ℝ) =ᶠ[𝓝 x] (fun _ => 1)) (x : E) :
    θ x * v x = v x ∧ θ x • G x = G x ∧ θ x * F x = F x ∧
      v x • schwartz_gradient θ x = 0 ∧
      inner ℝ (schwartz_gradient θ x) (G x) = 0 ∧ (Δ θ) x * v x = 0 := by
  by_cases hx : x ∈ K
  · have hone : θ x = 1 := (hθ x hx).eq_of_nhds
    have hgrad : schwartz_gradient θ x = 0 := by
      rw [schwartz_gradient_apply,(hθ x hx).gradient_eq]
      simp [gradient]
    have hlap : (Δ θ) x = 0 := by
      rw [SchwartzMap.laplacian_apply,(laplacian_congr_nhds (hθ x hx)).eq_of_nhds]
      simp
    simp [hone,hgrad,hlap]
  · have hvx : v x = 0 := image_eq_zero_of_notMem_tsupport (fun hh => hx (hv hh))
    have hFx : F x = 0 := image_eq_zero_of_notMem_tsupport (fun hh => hx (hF hh))
    have hGx : G x = 0 := image_eq_zero_of_notMem_tsupport (fun hh => hx (hG hh))
    simp [hvx,hFx,hGx]

private theorem coeff_holder_class {F H O : Type*}
    [NormedAddCommGroup F] [NormedSpace ℝ F]
    [NormedAddCommGroup H] [NormedSpace ℝ H]
    [NormedAddCommGroup O] [NormedSpace ℝ O]
    (B : F →L[ℝ] H →L[ℝ] O) (u : SchwartzMap E F)
    (f : E → H) (k : E → O) (hf : MemLp f 2 volume) (hk : MemLp k 2 volume)
    (heq : ∀ x, B (u x) (f x) = k x) :
    (B.holderL volume ∞ 2 2) (u.toLp ∞ volume) (hf.toLp f) = hk.toLp k := by
  apply Lp.ext
  filter_upwards [coeff_holder_ae B u (hf.toLp f),hf.coeFn_toLp,hk.coeFn_toLp]
    with x hx hy hz
  calc
    _ = B (u x) ((hf.toLp f) x) := hx
    _ = B (u x) (f x) := congrArg (B (u x)) hy
    _ = k x := heq x
    _ = _ := hz.symm

private theorem cutoff_schwartz_graph (v F : E → ℝ) (G : E → E) (K : Set E)
    (hK : IsCompact K) (hv : tsupport v ⊆ K) (hF : tsupport F ⊆ K)
    (hG : tsupport G ⊆ K) (hv2 : MemLp v 2 volume)
    (hF2 : MemLp F 2 volume) (hG2 : MemLp G 2 volume)
    (r : ℕ → SchwartzMap E ℝ)
    (hrv : Filter.Tendsto (fun n => (r n).toLp 2 volume) Filter.atTop (𝓝 (hv2.toLp v)))
    (hrG : Filter.Tendsto (fun n => (schwartz_gradient (r n)).toLp 2 volume)
      Filter.atTop (𝓝 (hG2.toLp G)))
    (hrF : Filter.Tendsto (fun n => (Δ (r n)).toLp 2 volume)
      Filter.atTop (𝓝 (hF2.toLp F))) :
    ∃ K' : Set E, IsCompact K' ∧ ∃ q : ℕ → SchwartzMap E ℝ,
      (∀ n, tsupport (q n) ⊆ K') ∧
      Filter.Tendsto (fun n => (q n).toLp 2 volume) Filter.atTop (𝓝 (hv2.toLp v)) ∧
      Filter.Tendsto (fun n => (schwartz_gradient (q n)).toLp 2 volume)
        Filter.atTop (𝓝 (hG2.toLp G)) ∧
      Filter.Tendsto (fun n => (Δ (q n)).toLp 2 volume)
        Filter.atTop (𝓝 (hF2.toLp F)) := by
  obtain ⟨θ,hθc,hθone⟩ := outer_plateau K hK
  let q : ℕ → SchwartzMap E ℝ := fun n =>
    (hθc.mul_right : HasCompactSupport (fun x => θ x * r n x)).toSchwartzMap
      ((θ.smooth ⊤).mul ((r n).smooth ⊤))
  have hq (n : ℕ) : (q n : E → ℝ) = fun x => θ x * r n x := rfl
  let MV : Lp ℝ 2 (volume : Measure E) →L[ℝ] Lp ℝ 2 (volume : Measure E) :=
    (ContinuousLinearMap.lsmul ℝ ℝ).holderL volume ∞ 2 2 (θ.toLp ∞ volume)
  let MG : Lp E 2 (volume : Measure E) →L[ℝ] Lp E 2 (volume : Measure E) :=
    (ContinuousLinearMap.lsmul ℝ ℝ (E := E)).holderL volume ∞ 2 2 (θ.toLp ∞ volume)
  let C : Lp ℝ 2 (volume : Measure E) →L[ℝ] Lp E 2 (volume : Measure E) :=
    (ContinuousLinearMap.lsmul ℝ ℝ (E := E)).flip.holderL volume ∞ 2 2
      ((schwartz_gradient θ).toLp ∞ volume)
  let I : Lp E 2 (volume : Measure E) →L[ℝ] Lp ℝ 2 (volume : Measure E) :=
    (innerSL ℝ).holderL volume ∞ 2 2 ((schwartz_gradient θ).toLp ∞ volume)
  let L : Lp ℝ 2 (volume : Measure E) →L[ℝ] Lp ℝ 2 (volume : Measure E) :=
    (ContinuousLinearMap.lsmul ℝ ℝ).holderL volume ∞ 2 2 ((Δ θ).toLp ∞ volume)
  have hi := plateau_point_identities v F G K hv hF hG θ hθone
  have hMV : MV (hv2.toLp v) = hv2.toLp v :=
    coeff_holder_class (ContinuousLinearMap.lsmul ℝ ℝ) θ v v hv2 hv2 (fun x => (hi x).1)
  have hMF : MV (hF2.toLp F) = hF2.toLp F :=
    coeff_holder_class (ContinuousLinearMap.lsmul ℝ ℝ) θ F F hF2 hF2 (fun x => (hi x).2.2.1)
  have hMG : MG (hG2.toLp G) = hG2.toLp G :=
    coeff_holder_class (ContinuousLinearMap.lsmul ℝ ℝ (E := E)) θ G G hG2 hG2 (fun x => (hi x).2.1)
  have hC : C (hv2.toLp v) = 0 := by
    exact (coeff_holder_class (ContinuousLinearMap.lsmul ℝ ℝ (E := E)).flip (schwartz_gradient θ)
      v (fun _ : E => (0 : E)) hv2 MemLp.zero (fun x => (hi x).2.2.2.1)).trans (MemLp.toLp_zero _)
  have hI : I (hG2.toLp G) = 0 := by
    exact (coeff_holder_class (innerSL ℝ) (schwartz_gradient θ)
      G (fun _ : E => (0 : ℝ)) hG2 MemLp.zero (fun x => (hi x).2.2.2.2.1)).trans (MemLp.toLp_zero _)
  have hL : L (hv2.toLp v) = 0 := by
    exact (coeff_holder_class (ContinuousLinearMap.lsmul ℝ ℝ) (Δ θ)
      v (fun _ : E => (0 : ℝ)) hv2 MemLp.zero (fun x => (hi x).2.2.2.2.2)).trans (MemLp.toLp_zero _)
  have hqV (n : ℕ) : (q n).toLp 2 volume = MV ((r n).toLp 2 volume) := by
    apply Lp.ext
    filter_upwards [(q n).coeFn_toLp 2 volume,
      coeff_holder_ae (ContinuousLinearMap.lsmul ℝ ℝ) θ ((r n).toLp 2 volume),
      (r n).coeFn_toLp 2 volume] with x hx hy hz
    rw [hz] at hy
    exact hx.trans hy.symm
  have hqG (n : ℕ) : (schwartz_gradient (q n)).toLp 2 volume =
      MG ((schwartz_gradient (r n)).toLp 2 volume) + C ((r n).toLp 2 volume) := by
    apply Lp.ext
    filter_upwards [(schwartz_gradient (q n)).coeFn_toLp 2 volume,
      Lp.coeFn_add (MG ((schwartz_gradient (r n)).toLp 2 volume)) (C ((r n).toLp 2 volume)),
      coeff_holder_ae (ContinuousLinearMap.lsmul ℝ ℝ (E := E)) θ ((schwartz_gradient (r n)).toLp 2 volume),
      coeff_holder_ae (ContinuousLinearMap.lsmul ℝ ℝ (E := E)).flip (schwartz_gradient θ) ((r n).toLp 2 volume),
      (schwartz_gradient (r n)).coeFn_toLp 2 volume,(r n).coeFn_toLp 2 volume]
      with x hx hy hz ht hu hw
    rw [hx,hy]
    simp only [Pi.add_apply]
    rw [hz,ht,hu,hw,schwartz_gradient_apply,schwartz_gradient_apply,
      schwartz_gradient_apply]
    change gradient (q n : E → ℝ) x =
      θ x • gradient (r n : E → ℝ) x + r n x • gradient (θ : E → ℝ) x
    rw [hq]
    exact AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.GradientAlgebra.gradient_mul_eq_of_differentiableAt
      θ.differentiableAt (r n).differentiableAt
  have hqF (n : ℕ) : (Δ (q n)).toLp 2 volume = MV ((Δ (r n)).toLp 2 volume) +
      (2:ℝ) • I ((schwartz_gradient (r n)).toLp 2 volume) + L ((r n).toLp 2 volume) := by
    apply Lp.ext
    filter_upwards [(Δ (q n)).coeFn_toLp 2 volume,
      Lp.coeFn_add (MV ((Δ (r n)).toLp 2 volume) + (2:ℝ) • I ((schwartz_gradient (r n)).toLp 2 volume))
        (L ((r n).toLp 2 volume)),
      Lp.coeFn_add (MV ((Δ (r n)).toLp 2 volume)) ((2:ℝ) • I ((schwartz_gradient (r n)).toLp 2 volume)),
      Lp.coeFn_smul (2:ℝ) (I ((schwartz_gradient (r n)).toLp 2 volume)),
      coeff_holder_ae (ContinuousLinearMap.lsmul ℝ ℝ) θ ((Δ (r n)).toLp 2 volume),
      coeff_holder_ae (innerSL ℝ) (schwartz_gradient θ) ((schwartz_gradient (r n)).toLp 2 volume),
      coeff_holder_ae (ContinuousLinearMap.lsmul ℝ ℝ) (Δ θ) ((r n).toLp 2 volume),
      (Δ (r n)).coeFn_toLp 2 volume,(schwartz_gradient (r n)).coeFn_toLp 2 volume,
      (r n).coeFn_toLp 2 volume] with x hx hy hz ht hu hw hA hB hC hD
    rw [hx,hy]
    simp only [Pi.add_apply]
    rw [hz]
    simp only [Pi.add_apply]
    rw [ht]
    simp only [Pi.smul_apply]
    rw [hu,hw,hA,hB,hC,hD]
    have heinner : ((innerSL ℝ) (schwartz_gradient θ x)) (schwartz_gradient (r n) x) =
        inner ℝ (schwartz_gradient θ x) (schwartz_gradient (r n) x) := rfl
    rw [heinner]
    simp only [SchwartzMap.laplacian_apply,schwartz_gradient_apply,
      ContinuousLinearMap.lsmul_apply,smul_eq_mul]
    change Laplacian.laplacian (q n : E → ℝ) x =
      θ x * Laplacian.laplacian (r n : E → ℝ) x +
      2 * inner ℝ (gradient (θ : E → ℝ) x) (gradient (r n : E → ℝ) x) +
      Laplacian.laplacian (θ : E → ℝ) x * r n x
    rw [hq]
    simpa only [mul_comm] using
      laplacian_product (θ : E → ℝ) (r n : E → ℝ) (θ.smooth 2) ((r n).smooth 2) x
  refine ⟨tsupport θ,hθc,q,?_,?_,?_,?_⟩
  · intro n
    rw [hq]
    exact tsupport_mul_subset_left
  · rw [← hMV]
    simpa only [hqV,Function.comp_def] using MV.continuous.continuousAt.tendsto.comp hrv
  · have ht := (MG.continuous.continuousAt.tendsto.comp hrG).add
      (C.continuous.continuousAt.tendsto.comp hrv)
    simpa only [hqG,Function.comp_def,hMG,hC,add_zero] using ht
  · have ht := ((MV.continuous.continuousAt.tendsto.comp hrF).add
      ((I.continuous.continuousAt.tendsto.comp hrG).const_smul (2:ℝ))).add
      (L.continuous.continuousAt.tendsto.comp hrv)
    simpa only [hqF,Function.comp_def,hMF,hI,hL,smul_zero,add_zero] using ht

theorem compact_weak_poisson_smooth_graph_approximation
    (v F : E → ℝ) (G : E → E) (K : Set E) (hK : IsCompact K)
    (hv : tsupport v ⊆ K) (hF : tsupport F ⊆ K) (hG : tsupport G ⊆ K)
    (hv2 : MemLp v 2 volume) (hF2 : MemLp F 2 volume) (hG2 : MemLp G 2 volume)
    (hd : ∀ ψ : E → ℝ, ContDiff ℝ 1 ψ → HasCompactSupport ψ → ∀ a : E,
      Integrable (fun x => ψ x * inner ℝ (G x) a) volume ∧
      Integrable (fun x => v x * fderiv ℝ ψ x a) volume ∧
      (∫ x, ψ x * inner ℝ (G x) a) = -∫ x, v x * fderiv ℝ ψ x a)
    (hweak : ∀ ψ : E → ℝ, ContDiff ℝ 2 ψ → HasCompactSupport ψ →
      Integrable (fun x => v x * (Δ ψ) x) volume ∧
      Integrable (fun x => F x * ψ x) volume ∧
      (∫ x, v x * (Δ ψ) x) = ∫ x, F x * ψ x) :
    ∃ K' : Set E, IsCompact K' ∧ ∃ φ : ℕ → SchwartzMap E ℝ,
      (∀ n, tsupport (φ n) ⊆ K') ∧
      Filter.Tendsto (fun n => (φ n).toLp 2 volume) Filter.atTop (𝓝 (hv2.toLp v)) ∧
      ∃ hφG : ∀ n, MemLp (gradient (φ n : E → ℝ)) 2 volume,
        Filter.Tendsto (fun n => (hφG n).toLp (gradient (φ n : E → ℝ)))
          Filter.atTop (𝓝 (hG2.toLp G)) ∧
        Filter.Tendsto (fun n => (Δ (φ n)).toLp 2 volume)
          Filter.atTop (𝓝 (hF2.toLp F)) := by
  obtain ⟨vc,Fc,hvc,hFc,_,hl,hs⟩ :=
    CompactWeakPoissonSobolev.compact_weak_poisson_sobolev v F K hK hv hF hv2 hF2 hweak
  obtain ⟨r,hrv,hrG,hrF⟩ := real_schwartz_graph v F G hv2 hF2 hG2 vc Fc hvc hFc hs hl hd
  obtain ⟨K',hK',φ,hφs,hφv,hφG,hφF⟩ :=
    cutoff_schwartz_graph v F G K hK hv hF hG hv2 hF2 hG2 r hrv hrG hrF
  have hφgrad (n : ℕ) : MemLp (gradient (φ n : E → ℝ)) 2 volume := by
    have he : (schwartz_gradient (φ n) : E → E) = gradient (φ n : E → ℝ) := by
      funext x; exact schwartz_gradient_apply (φ n) x
    rw [← he]
    exact (schwartz_gradient (φ n)).memLp 2 volume
  have heq (n : ℕ) : (hφgrad n).toLp (gradient (φ n : E → ℝ)) =
      (schwartz_gradient (φ n)).toLp 2 volume := by
    apply Lp.ext
    filter_upwards [(hφgrad n).coeFn_toLp,(schwartz_gradient (φ n)).coeFn_toLp 2 volume]
      with x hx hy
    rw [hx,hy,schwartz_gradient_apply]
  exact ⟨K',hK',φ,hφs,hφv,hφgrad,by simpa only [heq] using hφG,hφF⟩

end AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.CompactPoissonSmoothGraph
