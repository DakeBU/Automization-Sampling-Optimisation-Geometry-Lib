import AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.CompactC1GradientDomain
import AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Cutoff
import Mathlib.MeasureTheory.Integral.DominatedConvergence

/-! Actual finite-measure C1 function/gradient L2 pair enters the SAME original compact-smooth closed gradient by genuine smooth cutoff exhaustion and weighted quotient limits. Finite-measure constants are actual domain elements with zero output, including dimension0. PBPS2609.06905v1 AppendixC.1 original-domain prerequisite; no spatial moment, spectral gap, Poincare/BL or core is assumed. -/
set_option autoImplicit false
noncomputable section
open MeasureTheory Filter InnerProductSpace
open scoped Topology RealInnerProductSpace ContDiff
namespace AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.WeightedC1GradientDomain
variable {E F : Type*} [MeasurableSpace E] [NormedAddCommGroup F]
private theorem bounded_coefficient_memLp [NormedSpace ℝ F] (μ : Measure E) (c : E → ℝ)
    (f : E → F) (hc : AEStronglyMeasurable c μ) (hf : MemLp f 2 μ)
    (M : ℝ) (hb : ∀ᵐ x ∂μ, ‖c x‖ ≤ M) : MemLp (fun x => c x • f x) 2 μ := by
  apply hf.of_le_mul (c := M) (hc.smul hf.aestronglyMeasurable)
  filter_upwards [hb] with x hx
  change ‖c x • f x‖ ≤ M * ‖f x‖
  rw [norm_smul]
  exact mul_le_mul_of_nonneg_right hx (norm_nonneg _)

private theorem norm_sq_integral [InnerProductSpace ℝ F]
    (μ : Measure E) (f : E → F) (hf : MemLp f 2 μ) :
    ‖hf.toLp f‖^2 = ∫ x, ‖f x‖^2 ∂μ := by
  rw [← real_inner_self_eq_norm_sq, L2.inner_def]
  apply integral_congr_ae
  filter_upwards [hf.coeFn_toLp] with x hx
  rw [hx,real_inner_self_eq_norm_sq]

private theorem bounded_coefficient_tendsto_zero [InnerProductSpace ℝ F]
    (μ : Measure E) (cn : ℕ → E → ℝ) (f : E → F)
    (hcn : ∀ n, AEStronglyMeasurable (cn n) μ) (hf : MemLp f 2 μ)
    (M : ℝ) (hM : 0 ≤ M) (hb : ∀ n, ∀ᵐ x ∂μ, ‖cn n x‖ ≤ M)
    (ht : ∀ᵐ x ∂μ, Tendsto (fun n => cn n x) atTop (𝓝 0)) :
    ∃ hn : ∀ n, MemLp (fun x => cn n x • f x) 2 μ,
      Tendsto (fun n => (hn n).toLp _) atTop (𝓝 0) := by
  have hn (n : ℕ) := bounded_coefficient_memLp μ (cn n) f (hcn n) hf M (hb n)
  refine ⟨hn,?_⟩
  have hi : Integrable (fun x => ‖f x‖^2) μ :=
    (memLp_two_iff_integrable_sq_norm hf.aestronglyMeasurable).mp hf
  have hsq : Tendsto (fun n => ∫ x, ‖cn n x • f x‖^2 ∂μ) atTop (𝓝 0) := by
    have hh := tendsto_integral_of_dominated_convergence (μ := μ)
      (F := fun n x => ‖cn n x • f x‖^2) (f := fun _ => (0 : ℝ))
      (fun x => M^2 * ‖f x‖^2)
      (fun n => ((hn n).aestronglyMeasurable.norm.aemeasurable.pow_const 2).aestronglyMeasurable)
      (hi.const_mul (M^2))
      (fun n => by
        filter_upwards [hb n] with x hx
        rw [Real.norm_eq_abs,abs_of_nonneg (sq_nonneg _),norm_smul,mul_pow]
        exact mul_le_mul_of_nonneg_right
          ((sq_le_sq₀ (norm_nonneg _) hM).mpr hx) (sq_nonneg _))
      (by
        filter_upwards [ht] with x hx
        have hh := (hx.smul (tendsto_const_nhds (x := f x))).norm.pow 2
        simpa only [zero_smul,norm_zero,zero_pow (by norm_num : (2:ℕ)≠0)] using hh)
    simpa only [integral_zero] using hh
  have hsqN : Tendsto (fun n => ‖(hn n).toLp _‖^2) atTop (𝓝 0) := by
    simpa only [norm_sq_integral] using hsq
  have hsqrt := (Real.continuous_sqrt.tendsto (0 : ℝ)).comp hsqN
  have hn0 : Tendsto (fun n => ‖(hn n).toLp _‖) atTop (𝓝 0) := by
    simpa only [Function.comp_def,Real.sqrt_sq (norm_nonneg _),Real.sqrt_zero] using hsqrt
  exact tendsto_zero_iff_norm_tendsto_zero.mpr hn0

private theorem dominated_L2_tendsto_zero [InnerProductSpace ℝ F]
    (μ : Measure E) (fn : ℕ → E → F) (f : E → ℝ)
    (hfn : ∀ n, AEStronglyMeasurable (fn n) μ) (hf : MemLp f 2 μ)
    (M : ℝ) (hM : 0 ≤ M) (hb : ∀ n, ∀ᵐ x ∂μ, ‖fn n x‖ ≤ M * ‖f x‖)
    (ht : ∀ᵐ x ∂μ, Tendsto (fun n => fn n x) atTop (𝓝 0)) :
    ∃ hn : ∀ n, MemLp (fn n) 2 μ,
      Tendsto (fun n => (hn n).toLp _) atTop (𝓝 0) := by
  have hn (n : ℕ) : MemLp (fn n) 2 μ := hf.of_le_mul (c := M) (hfn n) (hb n)
  refine ⟨hn,?_⟩
  have hi : Integrable (fun x => ‖f x‖^2) μ :=
    (memLp_two_iff_integrable_sq_norm hf.aestronglyMeasurable).mp hf
  have hsq : Tendsto (fun n => ∫ x, ‖fn n x‖^2 ∂μ) atTop (𝓝 0) := by
    have hh := tendsto_integral_of_dominated_convergence (μ := μ)
      (F := fun n x => ‖fn n x‖^2) (f := fun _ => (0 : ℝ))
      (fun x => M^2 * ‖f x‖^2)
      (fun n => ((hn n).aestronglyMeasurable.norm.aemeasurable.pow_const 2).aestronglyMeasurable)
      (hi.const_mul (M^2))
      (fun n => by
        filter_upwards [hb n] with x hx
        rw [Real.norm_eq_abs,abs_of_nonneg (sq_nonneg _),← mul_pow]
        exact (sq_le_sq₀ (norm_nonneg _) (mul_nonneg hM (norm_nonneg _))).mpr hx)
      (by
        filter_upwards [ht] with x hx
        simpa only [norm_zero,zero_pow (by norm_num : (2:ℕ)≠0)] using hx.norm.pow 2)
    simpa only [integral_zero] using hh
  have hsqN : Tendsto (fun n => ‖(hn n).toLp _‖^2) atTop (𝓝 0) := by
    simpa only [norm_sq_integral] using hsq
  have hsqrt := (Real.continuous_sqrt.tendsto (0 : ℝ)).comp hsqN
  apply tendsto_zero_iff_norm_tendsto_zero.mpr
  simpa only [Function.comp_def,Real.sqrt_sq (norm_nonneg _),Real.sqrt_zero] using hsqrt


variable [NormedAddCommGroup E] [InnerProductSpace ℝ E] [FiniteDimensional ℝ E] [BorelSpace E]
omit [FiniteDimensional ℝ E] in
private theorem actual_cutoff_function_convergence [InnerProductSpace ℝ F]
    (μ : Measure E) (f : E → F) (hf : MemLp f 2 μ) :
    let χ := fun n : ℕ =>
      (AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Cutoff.radialSmoothCutoff
        ((n:ℝ)+1) : E → ℝ)
    ∃ hn : ∀ n, MemLp (fun x => χ n x • f x) 2 μ,
      Tendsto (fun n => (hn n).toLp _) atTop (𝓝 (hf.toLp f)) := by
  let χ := fun n : ℕ =>
    (AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Cutoff.radialSmoothCutoff
      ((n:ℝ)+1) : E → ℝ)
  have hχ (n : ℕ) : Continuous (χ n) :=
    (AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Cutoff.radialSmoothCutoff_contDiff
      (by positivity : (0:ℝ)<(n:ℝ)+1)).continuous
  have hχb (n : ℕ) (x : E) : χ n x ∈ Set.Icc (0:ℝ) 1 :=
    AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Cutoff.radialSmoothCutoff_mem_Icc _ _
  have hχabs (n : ℕ) (x : E) : ‖χ n x‖ ≤ (1:ℝ) := by
    rw [Real.norm_eq_abs,abs_of_nonneg (hχb n x).1]
    exact (hχb n x).2
  have hn (n : ℕ) := bounded_coefficient_memLp μ (χ n) f
    (hχ n).aestronglyMeasurable hf 1 (Eventually.of_forall (hχabs n))
  let c := fun n x => χ n x-1
  have hcb (n : ℕ) (x : E) : ‖c n x‖ ≤ (1:ℝ) := by
    rw [Real.norm_eq_abs,abs_le]
    exact ⟨by have h := (hχb n x).1; dsimp [c]; linarith,
      by have h := (hχb n x).2; dsimp [c]; linarith⟩
  have hct (x : E) : Tendsto (fun n => c n x) atTop (𝓝 0) := by
    have hR : Tendsto (fun n : ℕ => (n:ℝ)+1) atTop atTop :=
      tendsto_atTop_add_const_right atTop (1:ℝ) tendsto_natCast_atTop_atTop
    have h :=
      (AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Cutoff.radialSmoothCutoff_tendsto_one x).comp hR
    simpa only [Function.comp_def, c, χ, sub_self] using h.sub_const 1
  obtain ⟨hd,hdt⟩ := bounded_coefficient_tendsto_zero μ c f
    (fun n => ((hχ n).sub continuous_const).aestronglyMeasurable) hf 1 zero_le_one
    (fun n => Eventually.of_forall (hcb n)) (Eventually.of_forall hct)
  refine ⟨hn,tendsto_iff_norm_sub_tendsto_zero.mpr ?_⟩
  have he (n : ℕ) : (hn n).toLp _-hf.toLp f = (hd n).toLp _ := by
    apply Lp.ext
    filter_upwards [(hn n).coeFn_toLp,hf.coeFn_toLp,(hd n).coeFn_toLp,
      Lp.coeFn_sub ((hn n).toLp _) (hf.toLp f)] with x hx hy hz hw
    rw [hw]
    change ((hn n).toLp _) x-(hf.toLp f) x = ((hd n).toLp _) x
    rw [hx,hy,hz]
    dsimp [c]
    simp [sub_smul]
  have htNorm : Tendsto (fun n => ‖(hd n).toLp _‖) atTop (𝓝 0) := by
    simpa only [norm_zero] using hdt.norm
  change Tendsto (fun n => ‖(hn n).toLp _-hf.toLp f‖) atTop (𝓝 0)
  exact (tendsto_congr (fun n => congrArg norm (he n))).mpr htNorm


theorem c1_in_closed_gradient (μ : Measure E) [IsFiniteMeasure μ]
    (D : Lp ℝ 2 μ →ₗ.[ℝ] Lp E 2 μ) (hD : D.IsClosable)
    (hgraph : ∀ (a : Lp ℝ 2 μ) (H : Lp E 2 μ), (a,H) ∈ D.graph ↔
      ∃ φ : E → ℝ, ContDiff ℝ ∞ φ ∧ HasCompactSupport φ ∧
        a =ᵐ[μ] φ ∧ H =ᵐ[μ] gradient φ)
    {f : E → ℝ} (hf : ContDiff ℝ 1 f)
    (hp : MemLp f 2 μ) (hq : MemLp (gradient f) 2 μ) :
    (hp.toLp f,hq.toLp (gradient f)) ∈ D.closure.graph := by
  classical
  let χ := fun n : ℕ =>
    (AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Cutoff.radialSmoothCutoff
      ((n:ℝ)+1) : E → ℝ)
  have hχ (n : ℕ) : ContDiff ℝ 1 (χ n) :=
    (AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Cutoff.radialSmoothCutoff_contDiff
      (by positivity : (0:ℝ)<(n:ℝ)+1)).of_le
        (WithTop.coe_le_coe.mpr (le_top : (1:ℕ∞)≤⊤))
  have hc (n : ℕ) : HasCompactSupport (χ n) :=
    AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Cutoff.radialSmoothCutoff_hasCompactSupport
      (by positivity)
  obtain ⟨hfn,hfnt⟩ := actual_cutoff_function_convergence μ f hp
  obtain ⟨hGn,hGnt⟩ := actual_cutoff_function_convergence μ (gradient f) hq
  obtain ⟨C,hC,hCb⟩ :=
    AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Cutoff.radialSmoothCutoff_fderiv_bound
      (E := E)
  have hgrad (n : ℕ) : Continuous (gradient (χ n)) :=
    (toDual ℝ E).symm.continuous.comp ((hχ n).continuous_fderiv one_ne_zero)
  have hgb (n : ℕ) (x : E) : ‖gradient (χ n) x‖ ≤ C/((n:ℝ)+1) := by
    simpa only [gradient, LinearIsometryEquiv.norm_map] using
      hCb ((n:ℝ)+1) (by positivity) x
  have hgradt (x : E) : Tendsto (fun n => gradient (χ n) x) atTop (𝓝 0) := by
    apply tendsto_zero_iff_norm_tendsto_zero.mpr
    apply squeeze_zero (fun n => norm_nonneg _) (fun n => hgb n x)
    simpa only [div_eq_mul_inv,mul_zero,Function.comp_def] using
      (tendsto_inv_atTop_zero.comp
        (tendsto_atTop_add_const_right atTop (1:ℝ) tendsto_natCast_atTop_atTop)).const_mul C
  obtain ⟨hen,hent⟩ := dominated_L2_tendsto_zero μ
    (fun n x => f x • gradient (χ n) x) f
    (fun n => hf.continuous.aestronglyMeasurable.smul (hgrad n).aestronglyMeasurable)
    hp C hC.le (fun n => Eventually.of_forall (fun x => by
      rw [norm_smul]
      have hb : C/((n:ℝ)+1) ≤ C := by
        apply (div_le_iff₀ (by positivity : (0:ℝ)<(n:ℝ)+1)).mpr
        nlinarith [Nat.cast_nonneg (α:=ℝ) n]
      calc ‖f x‖*‖gradient (χ n) x‖ ≤ ‖f x‖*C :=
             mul_le_mul_of_nonneg_left ((hgb n x).trans hb) (norm_nonneg _)
           _ = C*‖f x‖ := mul_comm _ _))
    (Eventually.of_forall (fun x => by
      simpa only [smul_zero] using (hgradt x).const_smul (f x)))
  let hqn := fun n => (hGn n).add (hen n)
  have hqnt : Tendsto (fun n => (hqn n).toLp _) atTop (𝓝 (hq.toLp (gradient f))) := by
    change Tendsto (fun n => (hGn n).toLp _+(hen n).toLp _)
      atTop (𝓝 (hq.toLp (gradient f)))
    simpa only [add_zero] using hGnt.add hent
  have hproduct (n : ℕ) (x : E) :
      gradient (fun z => χ n z*f z) x = χ n x • gradient f x+f x • gradient (χ n) x := by
    rw [gradient, fderiv_fun_mul ((hχ n).differentiable_one x) (hf.differentiable_one x)]
    simp only [map_add,map_smul,gradient]
  have hgn (n : ℕ) : ((hfn n).toLp _,(hqn n).toLp _) ∈ D.closure.graph := by
    obtain ⟨hnp,hnq,hn⟩ :=
      AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.CompactC1GradientDomain.compact_c1_in_closed_gradient
        μ D hD hgraph ((hχ n).mul hf) (hc n).mul_right
    have hidp : hnp.toLp (fun z => χ n z*f z) = (hfn n).toLp _ := by
      apply Lp.ext
      filter_upwards [hnp.coeFn_toLp,(hfn n).coeFn_toLp] with x hx hy
      rw [hx,hy]; rfl
    have hidq : hnq.toLp (gradient (fun z => χ n z*f z)) = (hqn n).toLp _ := by
      apply Lp.ext
      filter_upwards [hnq.coeFn_toLp,(hqn n).coeFn_toLp] with x hx hy
      rw [hx,hy,hproduct]; rfl
    rwa [hidp,hidq] at hn
  have hclosed : IsClosed (D.closure.graph : Set (Lp ℝ 2 μ × Lp E 2 μ)) := by
    rw [← hD.graph_closure_eq_closure_graph]
    exact D.graph.isClosed_topologicalClosure
  exact hclosed.mem_of_tendsto (hfnt.prodMk_nhds hqnt) (Eventually.of_forall hgn)


theorem constants_in_closed_gradient (μ : Measure E) [IsFiniteMeasure μ]
    (D : Lp ℝ 2 μ →ₗ.[ℝ] Lp E 2 μ) (hD : D.IsClosable)
    (hgraph : ∀ (a : Lp ℝ 2 μ) (H : Lp E 2 μ), (a,H) ∈ D.graph ↔
      ∃ φ : E → ℝ, ContDiff ℝ ∞ φ ∧ HasCompactSupport φ ∧
        a =ᵐ[μ] φ ∧ H =ᵐ[μ] gradient φ) (c : ℝ) :
    ∃ u : D.closure.domain, (u : Lp ℝ 2 μ) =ᵐ[μ] (fun _ => c) ∧ D.closure u=0 := by
  have hp : MemLp (fun _ : E => c) 2 μ := memLp_const c
  have hg : gradient (fun _ : E => c) = (fun _ => (0:E)) := by
    funext x
    simp [gradient,fderiv_const_apply]
  have hq : MemLp (gradient (fun _ : E => c)) 2 μ := by rw [hg]; exact memLp_const (0:E)
  have hm := c1_in_closed_gradient μ D hD hgraph contDiff_const hp hq
  have hz : hq.toLp (gradient (fun _ : E => c)) = 0 := by
    apply Lp.ext
    filter_upwards [hq.coeFn_toLp,Lp.coeFn_zero (E:=E) (p:=2) (μ:=μ)] with x hx hy
    rw [hx,hy,hg]; rfl
  rw [hz] at hm
  obtain ⟨u,hu,huz⟩ := (D.closure.mem_graph_iff).mp hm
  refine ⟨u,?_,huz⟩
  rw [hu]
  exact hp.coeFn_toLp



end AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.WeightedC1GradientDomain
