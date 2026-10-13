import AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.CompactPoissonSmoothGraph
import Mathlib.MeasureTheory.Function.LpSeminorm.Indicator
import AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.WeightedBochner
import Mathlib.Analysis.InnerProductSpace.LinearPMap
import Mathlib.MeasureTheory.Measure.Tilted

set_option autoImplicit false
open MeasureTheory Filter
open ENNReal
open scoped Topology
noncomputable section
namespace AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.CompactWeightedPoissonCoercivity
variable {E F : Type*} [MeasurableSpace E] [NormedAddCommGroup F]

private theorem memLp_compact_domination (μ ν : Measure E) (K : Set E)
    (hK : MeasurableSet K) (c : ℝ≥0∞) (hc : c ≠ ∞)
    (hdom : μ.restrict K ≤ c • ν) (f : E → F)
    (hs : Function.support f ⊆ K) (hf : MemLp f 2 ν) : MemLp f 2 μ := by
  have hm : MemLp f 2 (μ.restrict K) := hf.of_measure_le_smul hc hdom
  have hi : MemLp (K.indicator f) 2 μ := (memLp_indicator_iff_restrict hK).mpr hm
  have he : K.indicator f = f := by
    funext x
    by_cases hx : x ∈ K
    · simp [hx]
    · have hz : f x = 0 := by
        by_contra hn
        exact hx (hs hn)
      simp [hx,hz]
  rwa [he] at hi

private theorem norm_compact_domination (μ ν : Measure E) (K : Set E)
    (c : ℝ≥0∞) (hc : c ≠ ∞) (hdom : μ.restrict K ≤ c • ν)
    (f : E → F) (hs : Function.support f ⊆ K)
    (hfμ : MemLp f 2 μ) (hfν : MemLp f 2 ν) :
    ‖hfμ.toLp f‖ ≤ (c ^ ((1 / (2 : ℝ≥0∞)).toReal)).toReal * ‖hfν.toLp f‖ := by
  rw [Lp.norm_toLp (μ := μ), Lp.norm_toLp (μ := ν)]
  have he : eLpNorm f 2 μ ≤ c ^ ((1 / (2 : ℝ≥0∞)).toReal) * eLpNorm f 2 ν := by
    rw [← eLpNorm_restrict_eq_of_support_subset hs]
    exact eLpNorm_le_of_measure_le_smul hdom
  have ht : c ^ ((1 / (2 : ℝ≥0∞)).toReal) * eLpNorm f 2 ν ≠ ∞ :=
    ENNReal.mul_ne_top (ENNReal.rpow_ne_top_of_nonneg ENNReal.toReal_nonneg hc) hfν.2.ne
  simpa only [ENNReal.toReal_mul] using ENNReal.toReal_mono ht he

private theorem compact_convergence (μ ν : Measure E) (K : Set E)
    (hK : MeasurableSet K) (c : ℝ≥0∞) (hc : c ≠ ∞)
    (hdom : μ.restrict K ≤ c • ν) (f : E → F) (fn : ℕ → E → F)
    (hs : Function.support f ⊆ K) (hsn : ∀ n, Function.support (fn n) ⊆ K)
    (hf : MemLp f 2 ν) (hfn : ∀ n, MemLp (fn n) 2 ν)
    (ht : Tendsto (fun n => (hfn n).toLp (fn n)) atTop (𝓝 (hf.toLp f))) :
    ∃ hfμ : MemLp f 2 μ, ∃ hfnμ : ∀ n, MemLp (fn n) 2 μ,
      Tendsto (fun n => (hfnμ n).toLp (fn n)) atTop (𝓝 (hfμ.toLp f)) := by
  have hfμ := memLp_compact_domination μ ν K hK c hc hdom f hs hf
  have hfnμ (n : ℕ) := memLp_compact_domination μ ν K hK c hc hdom (fn n) (hsn n) (hfn n)
  refine ⟨hfμ,hfnμ,?_⟩
  apply tendsto_iff_norm_sub_tendsto_zero.mpr
  have hsD (n : ℕ) : Function.support (fun x => fn n x-f x) ⊆ K := by
    intro x hx
    by_contra hn
    have h1 : fn n x = 0 := by by_contra h; exact hn (hsn n h)
    have h2 : f x = 0 := by by_contra h; exact hn (hs h)
    exact hx (by simp [h1,h2])
  have hbound (n : ℕ) : ‖(hfnμ n).toLp (fn n)-hfμ.toLp f‖ ≤
      (c ^ ((1 / (2 : ℝ≥0∞)).toReal)).toReal * ‖(hfn n).toLp (fn n)-hf.toLp f‖ := by
    change ‖((hfnμ n).sub hfμ).toLp (fn n-f)‖ ≤
      (c ^ ((1 / (2 : ℝ≥0∞)).toReal)).toReal * ‖((hfn n).sub hf).toLp (fn n-f)‖
    exact norm_compact_domination μ ν K c hc hdom
      (fun x => fn n x-f x) (hsD n) ((hfnμ n).sub hfμ) ((hfn n).sub hf)
  have hn := tendsto_iff_norm_sub_tendsto_zero.mp ht
  have hh := hn.const_mul ((c ^ ((1 / (2 : ℝ≥0∞)).toReal)).toReal)
  have hh0 : Tendsto (fun n => (c ^ ((1 / (2 : ℝ≥0∞)).toReal)).toReal *
      ‖(hfn n).toLp (fn n)-hf.toLp f‖) atTop (𝓝 0) := by simpa only [mul_zero] using hh
  exact squeeze_zero (fun _ => norm_nonneg _) hbound hh0


section Hilbert
variable [NormedAddCommGroup E] [InnerProductSpace ℝ E]
  [FiniteDimensional ℝ E] [BorelSpace E]
open InnerProductSpace
open scoped RealInnerProductSpace ContDiff

private theorem compact_weight_bound (W : E → ℝ) (hW : Continuous W)
    (K : Set E) (hK : IsCompact K) :
    ∃ c : ℝ≥0∞, c ≠ (∞ : ℝ≥0∞) ∧
      ((volume : Measure E).tilted (fun x => -W x)).restrict K ≤ c • volume := by
  let ρ := fun x => Real.exp (-W x)/(∫ z, Real.exp (-W z))
  have hρ : Continuous ρ := (Real.continuous_exp.comp hW.neg).div_const _
  obtain ⟨b,hb⟩ := hK.bddAbove_image hρ.continuousOn
  refine ⟨ENNReal.ofReal b,ENNReal.ofReal_ne_top,?_⟩
  rw [Measure.tilted,restrict_withDensity hK.measurableSet]
  calc
    _ ≤ (volume.restrict K).withDensity (fun _ => ENNReal.ofReal b) := by
      apply withDensity_mono
      filter_upwards [ae_restrict_mem hK.measurableSet] with x hx
      exact ENNReal.ofReal_le_ofReal (hb (Set.mem_image_of_mem ρ hx))
    _ = ENNReal.ofReal b • volume.restrict K := by rw [withDensity_const]
    _ ≤ ENNReal.ofReal b • volume := by
      gcongr
      exact Measure.restrict_le_self

omit [MeasurableSpace E] [BorelSpace E] in
private theorem compact_drift_bound (W : E → ℝ) (hW : ContDiff ℝ 2 W)
    (K : Set E) (hK : IsCompact K) :
    ∃ M : ℝ, 0 ≤ M ∧ ∀ x ∈ K, ‖gradient W x‖ ≤ M := by
  have hg : Continuous (gradient W) :=
    (toDual ℝ E).symm.continuous.comp
      ((hW.of_le (by norm_num : (1 : ℕ∞ω) ≤ 2)).continuous_fderiv one_ne_zero)
  obtain ⟨b,hb⟩ := hK.bddAbove_image hg.norm.continuousOn
  exact ⟨max b 0,le_max_right _ _,fun x hx =>
    (hb (Set.mem_image_of_mem _ hx)).trans (le_max_left _ _)⟩

private theorem drift_memLp (μ : Measure E) (W : E → ℝ)
    (hW : ContDiff ℝ 2 W) (K : Set E) (M : ℝ)
    (hb : ∀ x ∈ K, ‖gradient W x‖ ≤ M)
    (G : E → E) (hs : Function.support G ⊆ K) (hG : MemLp G 2 μ) :
    MemLp (fun x => inner ℝ (gradient W x) (G x)) 2 μ := by
  have hg : Continuous (gradient W) :=
    (toDual ℝ E).symm.continuous.comp
      ((hW.of_le (by norm_num : (1 : ℕ∞ω) ≤ 2)).continuous_fderiv one_ne_zero)
  apply hG.of_le_mul (hg.aestronglyMeasurable.inner hG.aestronglyMeasurable)
  filter_upwards [] with x
  by_cases hx : x ∈ K
  · exact (norm_inner_le_norm _ _).trans
      (mul_le_mul_of_nonneg_right (hb x hx) (norm_nonneg _))
  · have hz : G x = 0 := by by_contra hn; exact hx (hs hn)
    simp [hz]

omit [BorelSpace E] in
private theorem drift_norm_bound (μ : Measure E) (W : E → ℝ)
    (K : Set E) (M : ℝ) (hM : 0 ≤ M)
    (hb : ∀ x ∈ K, ‖gradient W x‖ ≤ M)
    (G : E → E) (hs : Function.support G ⊆ K) (hG : MemLp G 2 μ)
    (hA : MemLp (fun x => inner ℝ (gradient W x) (G x)) 2 μ) :
    ‖hA.toLp _‖ ≤ M * ‖hG.toLp G‖ := by
  rw [Lp.norm_toLp (μ := μ),Lp.norm_toLp (μ := μ)]
  have he : eLpNorm (fun x => inner ℝ (gradient W x) (G x)) 2 μ ≤
      ENNReal.ofReal M * eLpNorm G 2 μ := by
    apply eLpNorm_le_mul_eLpNorm_of_ae_le_mul
    filter_upwards [] with x
    by_cases hx : x ∈ K
    · exact (norm_inner_le_norm _ _).trans
        (mul_le_mul_of_nonneg_right (hb x hx) (norm_nonneg _))
    · have hz : G x = 0 := by by_contra hn; exact hx (hs hn)
      simp [hz]
  have ht : ENNReal.ofReal M * eLpNorm G 2 μ ≠ (∞ : ℝ≥0∞) :=
    ENNReal.mul_ne_top ENNReal.ofReal_ne_top hG.2.ne
  simpa only [ENNReal.toReal_mul,ENNReal.toReal_ofReal hM] using ENNReal.toReal_mono ht he

private theorem drift_convergence (μ : Measure E) (W : E → ℝ) (hW : ContDiff ℝ 2 W)
    (K : Set E) (M : ℝ) (hM : 0 ≤ M)
    (hb : ∀ x ∈ K, ‖gradient W x‖ ≤ M)
    (G : E → E) (Gn : ℕ → E → E)
    (hs : Function.support G ⊆ K) (hsn : ∀ n, Function.support (Gn n) ⊆ K)
    (hG : MemLp G 2 μ) (hGn : ∀ n, MemLp (Gn n) 2 μ)
    (ht : Tendsto (fun n => (hGn n).toLp (Gn n)) atTop (𝓝 (hG.toLp G))) :
    ∃ hA : MemLp (fun x => inner ℝ (gradient W x) (G x)) 2 μ,
      ∃ hAn : ∀ n, MemLp (fun x => inner ℝ (gradient W x) (Gn n x)) 2 μ,
        Tendsto (fun n => (hAn n).toLp _) atTop (𝓝 (hA.toLp _)) := by
  have hA := drift_memLp μ W hW K M hb G hs hG
  have hAn (n : ℕ) := drift_memLp μ W hW K M hb (Gn n) (hsn n) (hGn n)
  refine ⟨hA,hAn,tendsto_iff_norm_sub_tendsto_zero.mpr ?_⟩
  have hsD (n : ℕ) : Function.support (fun x => Gn n x-G x) ⊆ K := by
    intro x hx
    by_contra hn
    have h1 : Gn n x = 0 := by by_contra h; exact hn (hsn n h)
    have h2 : G x = 0 := by by_contra h; exact hn (hs h)
    exact hx (by simp [h1,h2])
  have hbound (n : ℕ) : ‖(hAn n).toLp _-hA.toLp _‖ ≤ M * ‖(hGn n).toLp _-hG.toLp _‖ := by
    have hdiff := drift_memLp μ W hW K M hb (fun x => Gn n x-G x) (hsD n) ((hGn n).sub hG)
    have hz := drift_norm_bound μ W K M hM hb (fun x => Gn n x-G x) (hsD n)
      ((hGn n).sub hG) hdiff
    have hid : hdiff.toLp _ = (hAn n).toLp _-hA.toLp _ := by
      apply Lp.ext
      filter_upwards [hdiff.coeFn_toLp,(hAn n).coeFn_toLp,hA.coeFn_toLp,
        Lp.coeFn_sub ((hAn n).toLp _) (hA.toLp _)] with x hx hy hz hw
      rw [hx,hw]
      change inner ℝ (gradient W x) (Gn n x-G x) =
        ((hAn n).toLp _) x-(hA.toLp _) x
      rw [hy,hz,inner_sub_right]
    rw [hid] at hz
    exact hz
  have hn := tendsto_iff_norm_sub_tendsto_zero.mp ht
  have hh : Tendsto (fun n => M * ‖(hGn n).toLp _-hG.toLp _‖) atTop (𝓝 0) := by
    simpa only [mul_zero] using hn.const_mul M
  exact squeeze_zero (fun _ => norm_nonneg _) hbound hh

omit [MeasurableSpace E] [BorelSpace E] in
private theorem gradient_support (f : E → ℝ) :
    Function.support (gradient f) ⊆ tsupport f := by
  intro x hx
  by_contra hn
  exact hx (by simp [gradient,fderiv_of_notMem_tsupport ℝ hn])

omit [MeasurableSpace E] [BorelSpace E] in
private theorem laplacian_support (f : E → ℝ) :
    Function.support (Laplacian.laplacian f) ⊆ tsupport f := by
  intro x hx
  by_contra hn
  have h1 : x ∉ tsupport (fderiv ℝ f) := fun h => hn (tsupport_fderiv_subset ℝ h)
  have h2 := fderiv_of_notMem_tsupport ℝ h1
  apply hx
  rw [InnerProductSpace.laplacian_eq_iteratedFDeriv_stdOrthonormalBasis]
  apply Finset.sum_eq_zero
  intro i _
  rw [iteratedFDeriv_two_apply,h2]
  simp

omit [NormedAddCommGroup E] [InnerProductSpace ℝ E] [FiniteDimensional ℝ E] [BorelSpace E] in
private theorem norm_sq_integral {H : Type*} [NormedAddCommGroup H] [InnerProductSpace ℝ H]
    (μ : Measure E) (f : E → H) (hf : MemLp f 2 μ) :
    ‖hf.toLp f‖^2 = ∫ x, ‖f x‖^2 ∂μ := by
  rw [← real_inner_self_eq_norm_sq, L2.inner_def]
  apply integral_congr_ae
  filter_upwards [hf.coeFn_toLp] with x hx
  rw [hx,real_inner_self_eq_norm_sq]

private theorem compact_normalized_bochner (W f : E → ℝ) (hW : ContDiff ℝ 2 W)
    (hZ : 0 < ∫ x, Real.exp (-W x))
    (hf : ContDiff ℝ ∞ f) (hc : HasCompactSupport f) (m : ℝ)
    (hl : ∀ x a, m * ‖a‖^2 ≤ fderiv ℝ (fderiv ℝ W) x a a)
    (hG : MemLp (gradient f) 2 ((volume : Measure E).tilted (fun x => -W x)))
    (hA : MemLp (fun x => inner ℝ (gradient W x) (gradient f x)-Laplacian.laplacian f x)
      2 ((volume : Measure E).tilted (fun x => -W x))) :
    m * ‖hG.toLp _‖^2 ≤ ‖hA.toLp _‖^2 := by
  obtain ⟨_,_,_,_,_,hb⟩ := WeightedBochner.integrated_bochner_identity W f hW hf hc
  have htilt (g : E → ℝ) : (∫ x, g x ∂(volume : Measure E).tilted (fun x => -W x)) =
      (∫ x, Real.exp (-W x))⁻¹ * ∫ x, Real.exp (-W x)*g x := by
    rw [integral_tilted,← integral_const_mul]
    apply integral_congr_ae
    filter_upwards [] with x
    change (Real.exp (-W x)/(∫ z, Real.exp (-W z))) • g x = _
    simp only [smul_eq_mul,div_eq_mul_inv]
    ring
  rw [norm_sq_integral,norm_sq_integral,htilt,htilt]
  have he (x : E) : ‖inner ℝ (gradient W x) (gradient f x)-Laplacian.laplacian f x‖^2 =
      (Laplacian.laplacian f x-inner ℝ (gradient W x) (gradient f x))^2 := by
    rw [Real.norm_eq_abs,sq_abs]; ring
  simp_rw [he]
  calc
    _ = (∫ x, Real.exp (-W x))⁻¹ * (m * ∫ x, Real.exp (-W x)*‖gradient f x‖^2) := by ring
    _ ≤ _ := mul_le_mul_of_nonneg_left (hb m hl) (inv_nonneg.mpr hZ.le)

open TemperedDistribution Laplacian
open scoped SchwartzMap

/-- Produce actual normalized Gibbs representatives, membership in the same original
closed gradient graph, and compact scalar coercivity from true ordinary weak data.
The simultaneous smooth approximation is derived, rather than supplied. -/
theorem compact_weak_poisson_weighted_coercivity
    (W : E → ℝ) (hW : ContDiff ℝ 2 W)
    (hI : Integrable (fun x => Real.exp (-W x))) (hZ : 0 < ∫ x, Real.exp (-W x))
    (m : ℝ) (hl : ∀ x a, m * ‖a‖^2 ≤ fderiv ℝ (fderiv ℝ W) x a a)
    (μ : Measure E) (hμ : μ = (volume : Measure E).tilted (fun x => -W x))
    (D : Lp ℝ 2 μ →ₗ.[ℝ] Lp E 2 μ)
    (hD : D.IsClosable)
    (hgraph : ∀ a H, (a,H) ∈ D.graph ↔
      ∃ ψ : E → ℝ, ContDiff ℝ ∞ ψ ∧ HasCompactSupport ψ ∧
        a =ᵐ[μ] ψ ∧ H =ᵐ[μ] gradient ψ)
    (v F : E → ℝ) (G : E → E) (K : Set E) (hK : IsCompact K)
    (hv : tsupport v ⊆ K) (hF : tsupport F ⊆ K) (hG : tsupport G ⊆ K)
    (hv2 : MemLp v 2 volume) (hF2 : MemLp F 2 volume) (hG2 : MemLp G 2 volume)
    (hd : ∀ ψ : E → ℝ, ContDiff ℝ 1 ψ → HasCompactSupport ψ → ∀ a : E,
      Integrable (fun x => ψ x * inner ℝ (G x) a) volume ∧
      Integrable (fun x => v x * fderiv ℝ ψ x a) volume ∧
      (∫ x, ψ x * inner ℝ (G x) a) = -∫ x, v x * fderiv ℝ ψ x a)
    (hweak : ∀ ψ : E → ℝ, ContDiff ℝ 2 ψ → HasCompactSupport ψ →
      Integrable (fun x => v x * Laplacian.laplacian ψ x) volume ∧
      Integrable (fun x => F x * ψ x) volume ∧
      (∫ x, v x * Laplacian.laplacian ψ x) = ∫ x, F x * ψ x) :
    let A := fun x => inner ℝ (gradient W x) (G x)-F x
    MemLp v 2 μ ∧ MemLp G 2 μ ∧ MemLp A 2 μ ∧
    ∃ vW AW : Lp ℝ 2 μ, ∃ GW : Lp E 2 μ,
      vW =ᵐ[μ] v ∧ AW =ᵐ[μ] A ∧ GW =ᵐ[μ] G ∧
      (vW,GW) ∈ D.closure.graph ∧ m * ‖GW‖^2 ≤ ‖AW‖^2 := by
  subst μ
  let μ := (volume : Measure E).tilted (fun x => -W x)
  let : IsProbabilityMeasure μ := isProbabilityMeasure_tilted hI
  obtain ⟨K',hK',φ,hφs,hφv,hφG,hφgrad,hφF⟩ :=
    CompactPoissonSmoothGraph.compact_weak_poisson_smooth_graph_approximation
      v F G K hK hv hF hG hv2 hF2 hG2 hd hweak
  let Kbar := K ∪ K'
  have hKb : IsCompact Kbar := hK.union hK'
  obtain ⟨c,hc,hdom⟩ := compact_weight_bound W hW.continuous Kbar hKb
  obtain ⟨M,hM,hMb⟩ := compact_drift_bound W hW Kbar hKb
  have hvs : Function.support v ⊆ Kbar := (subset_tsupport v).trans (hv.trans Set.subset_union_left)
  have hFs : Function.support F ⊆ Kbar := (subset_tsupport F).trans (hF.trans Set.subset_union_left)
  have hGs : Function.support G ⊆ Kbar := (subset_tsupport G).trans (hG.trans Set.subset_union_left)
  have hps (n : ℕ) : Function.support (φ n : E → ℝ) ⊆ Kbar :=
    (subset_tsupport _).trans ((hφs n).trans Set.subset_union_right)
  have hpgs (n : ℕ) : Function.support (gradient (φ n : E → ℝ)) ⊆ Kbar :=
    (gradient_support _).trans ((hφs n).trans Set.subset_union_right)
  have hpls (n : ℕ) : Function.support (Laplacian.laplacian (φ n : E → ℝ)) ⊆ Kbar :=
    (laplacian_support _).trans ((hφs n).trans Set.subset_union_right)
  have hpl2 (n : ℕ) : MemLp (Laplacian.laplacian (φ n : E → ℝ)) 2 volume := by
    have he : ((Δ (φ n) : SchwartzMap E ℝ) : E → ℝ) =
        Laplacian.laplacian (φ n : E → ℝ) := by
      funext x; exact SchwartzMap.laplacian_apply (φ n) x
    rw [← he]
    exact (Δ (φ n)).memLp 2 volume
  have hplT : Tendsto (fun n => (hpl2 n).toLp _) atTop (𝓝 (hF2.toLp F)) := by
    have he (n : ℕ) : (hpl2 n).toLp _ = (Δ (φ n)).toLp 2 volume := by
      apply Lp.ext
      filter_upwards [(hpl2 n).coeFn_toLp,(Δ (φ n)).coeFn_toLp 2 volume] with x hx hy
      rw [hx,hy,SchwartzMap.laplacian_apply]
    simpa only [he] using hφF
  obtain ⟨hvW,hpW,hpT⟩ := compact_convergence μ volume Kbar hKb.measurableSet c hc hdom
    v (fun n => (φ n : E → ℝ)) hvs hps hv2 (fun n => (φ n).memLp 2 volume) hφv
  obtain ⟨hGW,hpgW,hpgT⟩ := compact_convergence μ volume Kbar hKb.measurableSet c hc hdom
    G (fun n => gradient (φ n : E → ℝ)) hGs hpgs hG2 hφG hφgrad
  obtain ⟨hFW,hplW,hplWT⟩ := compact_convergence μ volume Kbar hKb.measurableSet c hc hdom
    F (fun n => Laplacian.laplacian (φ n : E → ℝ)) hFs hpls hF2 hpl2 hplT
  obtain ⟨hB,hBn,hBT⟩ := drift_convergence μ W hW Kbar M hM hMb
    G (fun n => gradient (φ n : E → ℝ)) hGs hpgs hGW hpgW hpgT
  have hAW : MemLp (fun x => inner ℝ (gradient W x) (G x)-F x) 2 μ := hB.sub hFW
  have hAn (n : ℕ) : MemLp (fun x => inner ℝ (gradient W x) (gradient (φ n : E → ℝ) x)-
      Laplacian.laplacian (φ n : E → ℝ) x) 2 μ := (hBn n).sub (hplW n)
  have hAT : Tendsto (fun n => (hAn n).toLp _) atTop (𝓝 (hAW.toLp _)) := by
    change Tendsto (fun n => (hBn n).toLp _-(hplW n).toLp _) atTop
      (𝓝 (hB.toLp _-hFW.toLp _))
    exact hBT.sub hplWT
  dsimp only
  refine ⟨hvW,hGW,hAW,hvW.toLp _,hAW.toLp _,hGW.toLp _,
    hvW.coeFn_toLp,hAW.coeFn_toLp,hGW.coeFn_toLp,?_,?_⟩
  · rw [← hD.graph_closure_eq_closure_graph]
    apply D.graph.isClosed_topologicalClosure.mem_of_tendsto (hpT.prodMk_nhds hpgT)
    filter_upwards [] with n
    apply D.graph.le_topologicalClosure
    exact (hgraph _ _).mpr ⟨φ n,(φ n).smooth ⊤,HasCompactSupport.of_support_subset_isCompact
      hK' ((subset_tsupport _).trans (hφs n)),(hpW n).coeFn_toLp,(hpgW n).coeFn_toLp⟩
  · apply le_of_tendsto_of_tendsto (hpgT.norm.pow 2 |>.const_mul m) (hAT.norm.pow 2)
    filter_upwards [] with n
    exact compact_normalized_bochner W (φ n : E → ℝ) hW hZ ((φ n).smooth ⊤)
      (HasCompactSupport.of_support_subset_isCompact hK' ((subset_tsupport _).trans (hφs n)))
      m hl (hpgW n) (hAn n)

end Hilbert
end AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.CompactWeightedPoissonCoercivity
