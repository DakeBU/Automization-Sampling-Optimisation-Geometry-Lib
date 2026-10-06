import AutoSamplingTheory.TechnicalLemmas.Probability.GaussianLipschitzExponential
import Mathlib.MeasureTheory.Function.L2Space
import AutoSamplingTheory.TechnicalLemmas.Analysis.QuadraticRegularization
import AutoSamplingTheory.TechnicalLemmas.Analysis.SmoothnessEquivalences
import AutoSamplingTheory.TechnicalLemmas.Analysis.GradientDescentContraction
import Mathlib.Topology.MetricSpace.Contracting
import Mathlib.MeasureTheory.Constructions.BorelSpace.Metrizable
import AutoSamplingTheory.TechnicalLemmas.Measure.GaussianSmoothing
import Mathlib.Tactic

/-!
# Actual source-range proximal Gaussian oracle

SPHMC arXiv:2609.06906v1, (2.1), (3.2), and Lemma 4.2 (4.4)-(4.5), plus necessary (4.3) domains.
The exact source signature and source-only topology were independently sealed
before this implementation. The numerical oracle's separate eta<=1/(2 beta)
call/cost boundary does not become a full-range implementation guarantee.

The Gaussian gradient-output law is distinct from the RGO posterior and HMC
transition. Genuine output first moments and signed centered exponential domains are produced
below. The sharp MGF coefficient, bias, standardized posterior transport, Wp, histories, numerical
queries, main results and composition remain separate obligations.
-/

noncomputable section
open MeasureTheory ProbabilityTheory InnerProductSpace Filter Topology
open scoped RealInnerProductSpace NNReal ENNReal
open AutoSamplingTheory.TechnicalLemmas.Analysis

namespace AutoSamplingTheory.ExampleCases.SmoothedPicardHMC.FullRangeProximalGaussianOracle

private theorem actual_gradient_bounds
    {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E] [CompleteSpace E]
    {V : E → ℝ} {κ : ℝ} (hκ : 1 ≤ κ) (hV : ContDiff ℝ 2 V)
    (hH : ∀ x v : E, κ⁻¹*‖v‖^2 ≤ fderiv ℝ (fderiv ℝ V) x v v ∧
      fderiv ℝ (fderiv ℝ V) x v v ≤ ‖v‖^2) :
    LipschitzWith 1 (gradient V) ∧
      LipschitzWith 1 (fun x => x-gradient V x) ∧
      StrongConvexOn Set.univ κ⁻¹ V ∧
      ∀ x z, 0 ≤ inner ℝ (gradient V x-gradient V z) (x-z) := by
  have hκ0 : 0 < κ := lt_of_lt_of_le zero_lt_one hκ
  have hα : 0 ≤ κ⁻¹ := (inv_pos.mpr hκ0).le
  have hH' : ∀ x v : E,
      ((Real.toNNReal κ⁻¹ : ℝ≥0) : ℝ)*‖v‖^2 ≤ fderiv ℝ (fderiv ℝ V) x v v ∧
      fderiv ℝ (fderiv ℝ V) x v v ≤ (1 : ℝ≥0)*‖v‖^2 := by
    simpa only [Real.coe_toNNReal _ hα, NNReal.coe_one, one_mul] using hH
  have hLip : LipschitzWith 1 (gradient V) := by
    simpa using (QuadraticRegularization.strongConvexOn_and_lipschitzWith_gradient_add_quadratic
      (r := 0) hV hH' (0:E)).2
  have hsc : StrongConvexOn Set.univ κ⁻¹ V :=
    HessianStrongConvexity.strongConvexOn_univ_of_fderiv2_lower hV (fun x v => (hH x v).1)
  have hsc0 : StrongConvexOn Set.univ 0 V :=
    HessianStrongConvexity.strongConvexOn_univ_of_fderiv2_lower hV (by
        intro x v
        simpa only [zero_mul] using
          (mul_nonneg hα (sq_nonneg ‖v‖)).trans (hH x v).1)
  have hu : ∀ x z, V z ≤ V x+inner ℝ (gradient V x) (z-x)+1/2*‖z-x‖^2 :=
    (SmoothnessEquivalences.upper_model_iff_fderiv2_upper hV).mpr (by
        intro x v
        simpa only [one_mul] using (hH x v).2)
  have hMinus : LipschitzWith 1 (fun x => x-gradient V x) := by
    apply LipschitzWith.of_dist_le_mul
    intro x z
    have h := GradientDescentContraction.gradient_step_contraction (h := 1)
      (hV.of_le (by norm_num)) hsc0
        (by norm_num) (by norm_num) (by norm_num) (by norm_num) hu z x
    simpa only [one_smul, zero_mul, sub_zero, Real.sqrt_one,
      NNReal.coe_one, one_mul, dist_eq_norm] using h
  refine ⟨hLip,hMinus,hsc,fun x z => ?_⟩
  have h := StrongConvexFirstOrder.gradient_inner_lower_bound_of_strongConvexOn
    (x := z) (y := x) hsc
      (fun w _ => (hV.differentiable (by norm_num) w).hasGradientAt)
      (Set.mem_univ z) (Set.mem_univ x)
  exact (mul_nonneg hα (sq_nonneg ‖x-z‖)).trans h

private theorem parameterized_damped_point
    {E S : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [CompleteSpace E] [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]
    [MeasurableSpace S] {g : E → E}
    (hg : LipschitzWith 1 (fun x => x-g x))
    {eta : S → ℝ} {y : S → E} (heta : Measurable eta) (hy : Measurable y)
    (hpos : ∀ s, 0 < eta s) :
    ∃ p : S → E, Measurable p ∧ ∀ s, p s+eta s • g (p s)=y s := by
  let f : S → E → E := fun s x => (1+eta s)⁻¹ • (y s+eta s • (x-g x))
  have hsum (s : S) : 0 < 1+eta s := by linarith [hpos s]
  let c : S → ℝ≥0 := fun s => ⟨(1+eta s)⁻¹*eta s,
    mul_nonneg (inv_pos.mpr (hsum s)).le (hpos s).le⟩
  have hc (s : S) : ContractingWith (c s) (f s) := by
    refine ⟨?_,LipschitzWith.of_dist_le_mul fun x z => ?_⟩
    · change (1+eta s)⁻¹*eta s < 1
      rw [← div_eq_inv_mul]
      apply (div_lt_iff₀ (hsum s)).mpr
      linarith
    · have h := hg.dist_le_mul x z
      simp only [NNReal.coe_one,one_mul,dist_eq_norm] at h
      have hid : f s x-f s z = (1+eta s)⁻¹ •
          (eta s • ((x-g x)-(z-g z))) := by
        dsimp only [f]
        rw [← smul_sub]
        congr 1
        module
      rw [dist_eq_norm,hid,norm_smul,norm_smul,Real.norm_eq_abs,Real.norm_eq_abs,
        abs_of_pos (inv_pos.mpr (hsum s)),abs_of_pos (hpos s)]
      simp only [dist_eq_norm]
      change (1+eta s)⁻¹*(eta s*‖(x-g x)-(z-g z)‖) ≤
        ((1+eta s)⁻¹*eta s)*‖x-z‖
      calc
        (1+eta s)⁻¹*(eta s*‖(x-g x)-(z-g z)‖) =
            ((1+eta s)⁻¹*eta s)*‖(x-g x)-(z-g z)‖ := by ring
        _ ≤ ((1+eta s)⁻¹*eta s)*‖x-z‖ :=
          mul_le_mul_of_nonneg_left h (mul_nonneg (inv_pos.mpr (hsum s)).le (hpos s).le)
  let p : S → E := fun s => (hc s).fixedPoint (f s)
  have hit (n : ℕ) : Measurable (fun s => (f s)^[n] (0 : E)) := by
    induction n with
    | zero => simpa only [Function.iterate_zero,id_eq] using
        (measurable_const : Measurable (fun _ : S => (0:E)))
    | succ n ih =>
      simp only [Function.iterate_succ_apply']
      exact (measurable_const.add heta).inv.smul
        (hy.add (heta.smul (hg.continuous.measurable.comp ih)))
  have hp : Measurable p := measurable_of_tendsto_metrizable hit
    (tendsto_pi_nhds.mpr (fun s => (hc s).tendsto_iterate_fixedPoint 0))
  refine ⟨p,hp,fun s => ?_⟩
  have heq : f s (p s)=p s := (hc s).fixedPoint_isFixedPt
  have hs := congrArg (fun x : E => (1+eta s) • x) heq
  simp only [f,smul_smul,mul_inv_cancel₀ (ne_of_gt (hsum s)),one_smul] at hs
  calc
    p s+eta s • g (p s) = (1+eta s) • p s-eta s • (p s-g (p s)) := by module
    _ = y s := by rw [← hs]; module

private theorem actual_quadratic_minimum
    {E S : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E] [CompleteSpace E]
    {V : E → ℝ} {κ : ℝ} (hκ : 1 ≤ κ) (hV : ContDiff ℝ 2 V)
    (hH : ∀ x v : E, κ⁻¹*‖v‖^2 ≤ fderiv ℝ (fderiv ℝ V) x v v ∧
      fderiv ℝ (fderiv ℝ V) x v v ≤ ‖v‖^2)
    {eta : S → ℝ} {y p : S → E} (hpos : ∀ s, 0 < eta s)
    (heq : ∀ s, p s+eta s • gradient V (p s)=y s) :
    let F := fun s x => V x+(eta s)⁻¹/2*‖x-y s‖^2
    ∀ s z, F s (p s)+(κ⁻¹+(eta s)⁻¹)/2*‖z-p s‖^2 ≤ F s z ∧
      (F s z ≤ F s (p s) ↔ z=p s) := by
  let F := fun s x => V x+(eta s)⁻¹/2*‖x-y s‖^2
  have hα : 0 ≤ κ⁻¹ := (inv_pos.mpr (lt_of_lt_of_le zero_lt_one hκ)).le
  have hH' : ∀ x v : E,
      ((Real.toNNReal κ⁻¹ : ℝ≥0) : ℝ)*‖v‖^2 ≤ fderiv ℝ (fderiv ℝ V) x v v ∧
      fderiv ℝ (fderiv ℝ V) x v v ≤ (1 : ℝ≥0)*‖v‖^2 := by
    simpa only [Real.coe_toNNReal _ hα,NNReal.coe_one,one_mul] using hH
  change ∀ s z, F s (p s)+(κ⁻¹+(eta s)⁻¹)/2*‖z-p s‖^2 ≤ F s z ∧
    (F s z ≤ F s (p s) ↔ z=p s)
  intro s z
  have hd : Differentiable ℝ V := hV.differentiable (by norm_num)
  have hq (x : E) : HasFDerivAt (fun w => (eta s)⁻¹/2*‖w-y s‖^2)
      ((eta s)⁻¹ • innerSL ℝ (x-y s)) x := by
    convert (((hasFDerivAt_id x).sub_const (y s)).norm_sq).const_mul ((eta s)⁻¹/2)
      using 1 <;> first | rfl | (ext v; simp; ring)
  have hFd (x : E) : DifferentiableAt ℝ (F s) x :=
    (hd x).add (hq x).differentiableAt
  have hg (x : E) : gradient (F s) x = gradient V x+(eta s)⁻¹ • (x-y s) := by
    apply HasGradientAt.gradient
    rw [hasGradientAt_iff_hasFDerivAt]
    change HasFDerivAt (fun w => V w+(eta s)⁻¹/2*‖w-y s‖^2)
      ((toDual ℝ E) (gradient V x+(eta s)⁻¹ • (x-y s))) x
    convert! (hd x).hasGradientAt.hasFDerivAt.add (hq x) using 1
    simp only [map_add,map_smul]
    rfl
  have hz : gradient (F s) (p s)=0 := by
    rw [hg]
    have hs : p s-y s=-(eta s • gradient V (p s)) := by rw [← heq s]; abel
    rw [hs,smul_neg,smul_smul,inv_mul_cancel₀ (ne_of_gt (hpos s)),one_smul,add_neg_cancel]
  have hsc : StrongConvexOn Set.univ (κ⁻¹+(eta s)⁻¹) (F s) := by
    have hb := QuadraticRegularization.strongConvexOn_and_lipschitzWith_gradient_add_quadratic
      (r := Real.toNNReal ((eta s)⁻¹)) hV hH' (y s)
    simpa [F,Real.coe_toNNReal _ hα,Real.coe_toNNReal _ (inv_nonneg.mpr (hpos s).le)] using hb.1
  have hbound := StrongConvexFirstOrder.firstOrder_lower_bound_of_strongConvexOn hsc
    (fun x _ => (hFd x).hasGradientAt) (x := p s) (y := z)
    (Set.mem_univ _) (Set.mem_univ _)
  rw [hz,inner_zero_left,add_zero] at hbound
  refine ⟨hbound,⟨fun hle => ?_,fun he => by rw [he]⟩⟩
  have ha : 0 < (κ⁻¹+(eta s)⁻¹)/2 :=
    div_pos (add_pos_of_nonneg_of_pos hα (inv_pos.mpr (hpos s))) (by norm_num)
  have hnonpos : (κ⁻¹+(eta s)⁻¹)/2*‖z-p s‖^2 ≤ 0 := by linarith
  have hn : ‖z-p s‖^2=0 :=
    le_antisymm (nonpos_of_mul_nonpos_right hnonpos ha) (sq_nonneg _)
  exact sub_eq_zero.mp (norm_eq_zero.mp (sq_eq_zero_iff.mp hn))

set_option maxHeartbeats 800000 in
theorem full_range_proximal_gaussian_oracle
    {E S : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [CompleteSpace E] [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]
    [MeasurableSpace S] {V : E → ℝ} {κ : ℝ}
    (hκ : 1 ≤ κ) (hV : ContDiff ℝ 2 V)
    (hH : ∀ x v : E, κ⁻¹*‖v‖^2 ≤ fderiv ℝ (fderiv ℝ V) x v v ∧
      fderiv ℝ (fderiv ℝ V) x v v ≤ ‖v‖^2)
    {eta : S → ℝ} {y : S → E} (heta : Measurable eta) (hy : Measurable y)
    (hpos : ∀ s, 0 < eta s) :
    let F := fun s x => V x + (eta s)⁻¹/2*‖x-y s‖^2
    ∃ p : S → E, Measurable p ∧
      (∀ s, p s + eta s • gradient V (p s) = y s) ∧
      (∀ s z, F s (p s) + (κ⁻¹+(eta s)⁻¹)/2*‖z-p s‖^2 ≤ F s z ∧
        (F s z ≤ F s (p s) ↔ z=p s)) ∧
      (∀ s t, eta s = eta t → ‖p s-p t‖ ≤ ‖y s-y t‖) ∧
      let G := fun q : S × E => gradient V (p q.1+Real.sqrt (eta q.1) • q.2)
      Measurable G ∧
      (∀ s t z w, eta s = eta t →
        ‖G (s,z)-G (t,w)‖ ≤ ‖y s-y t‖+Real.sqrt (eta s)*‖z-w‖) ∧
      ∃ K : ProbabilityTheory.Kernel S E, ProbabilityTheory.IsMarkovKernel K ∧
        (∀ s, K s = (ProbabilityTheory.stdGaussian E).map (fun z => G (s,z))) ∧
        ∀ s, MeasureTheory.Integrable (fun w : E => w) (K s) ∧
          ∀ (a : E) (t : ℝ), MeasureTheory.Integrable
            (fun w => Real.exp (t * inner ℝ a (w - ∫ v, v ∂K s))) (K s) ∧
            (∫ w, Real.exp (t * inner ℝ a (w - ∫ v, v ∂K s)) ∂K s) ≤
              Real.exp (eta s * t^2 * ‖a‖^2 / 2) := by
  let F := fun s x => V x+(eta s)⁻¹/2*‖x-y s‖^2
  obtain ⟨hLip,hMinus,_hsc,hmono⟩ := actual_gradient_bounds hκ hV hH
  obtain ⟨p,hp,heq⟩ := parameterized_damped_point hMinus heta hy hpos
  have hmin := actual_quadratic_minimum hκ hV hH hpos heq
  have hnexp : ∀ s t, eta s=eta t → ‖p s-p t‖ ≤ ‖y s-y t‖ := by
    intro s t ht
    have hsub : y s-y t=(p s-p t)+eta s • (gradient V (p s)-gradient V (p t)) := by
      rw [← heq s,← heq t,← ht]
      module
    have hpair : ‖p s-p t‖^2 ≤ inner ℝ (y s-y t) (p s-p t) := by
      calc
        _ ≤ ‖p s-p t‖^2+eta s*inner ℝ (gradient V (p s)-gradient V (p t)) (p s-p t) :=
          le_add_of_nonneg_right (mul_nonneg (hpos s).le (hmono (p s) (p t)))
        _ = _ := by
          rw [hsub,inner_add_left,real_inner_smul_left,real_inner_self_eq_norm_sq]
    have hb := hpair.trans (real_inner_le_norm (y s-y t) (p s-p t))
    by_cases hz : ‖p s-p t‖=0
    · simpa only [hz] using norm_nonneg (y s-y t)
    · have hpositive : 0 < ‖p s-p t‖ := lt_of_le_of_ne (norm_nonneg _) (Ne.symm hz)
      nlinarith
  refine ⟨p,hp,heq,hmin,hnexp,?_⟩
  let G := fun q : S × E => gradient V (p q.1+Real.sqrt (eta q.1) • q.2)
  have hG : Measurable G := hLip.continuous.measurable.comp
    ((hp.comp measurable_fst).add ((heta.comp measurable_fst).sqrt.smul measurable_snd))
  have hGLip : ∀ s t z w, eta s=eta t →
      ‖G (s,z)-G (t,w)‖ ≤ ‖y s-y t‖+Real.sqrt (eta s)*‖z-w‖ := by
    intro s t z w ht
    have h := hLip.dist_le_mul (p s+Real.sqrt (eta s) • z) (p t+Real.sqrt (eta t) • w)
    simp only [NNReal.coe_one,one_mul,dist_eq_norm] at h
    have hdiff : (p s+Real.sqrt (eta s) • z)-(p t+Real.sqrt (eta t) • w) =
        (p s-p t)+Real.sqrt (eta s) • (z-w) := by rw [← ht]; module
    calc
      _ ≤ ‖(p s+Real.sqrt (eta s) • z)-(p t+Real.sqrt (eta t) • w)‖ := h
      _ = ‖(p s-p t)+Real.sqrt (eta s) • (z-w)‖ := by rw [hdiff]
      _ ≤ ‖p s-p t‖+‖Real.sqrt (eta s) • (z-w)‖ := norm_add_le _ _
      _ ≤ ‖y s-y t‖+Real.sqrt (eta s)*‖z-w‖ := by
        rw [norm_smul,Real.norm_eq_abs,abs_of_nonneg (Real.sqrt_nonneg _)]
        exact add_le_add (hnexp s t ht) le_rfl
  let K := (Kernel.id ×ₖ Kernel.const S (stdGaussian E)).map G
  have hK : IsMarkovKernel K := Kernel.IsMarkovKernel.map _ hG
  have hKs (s : S) : K s=(stdGaussian E).map (fun z => G (s,z)) := by
    dsimp only [K]
    rw [Kernel.map_apply _ hG,Kernel.prod_apply,Kernel.id_apply,Kernel.const_apply,
      Measure.dirac_prod,Measure.map_map hG (by fun_prop)]
    rfl
  have hGm (s : S) : Measurable (fun z => G (s,z)) :=
    hG.comp (measurable_const.prodMk measurable_id)
  have hGi (s : S) : Integrable (fun z => G (s,z)) (stdGaussian E) := by
    apply (((IsGaussian.integrable_id (μ := stdGaussian E)).norm.const_mul
      (Real.sqrt (eta s))).add (integrable_const ‖G (s,0)‖)).mono'
        (hGm s).aestronglyMeasurable
    filter_upwards with z
    have hd := hGLip s s z 0 rfl
    simp only [sub_self,norm_zero,zero_add,sub_zero] at hd
    calc
      ‖G (s,z)‖ = ‖(G (s,z)-G (s,0))+G (s,0)‖ := by rw [sub_add_cancel]
      _ ≤ ‖G (s,z)-G (s,0)‖+‖G (s,0)‖ := norm_add_le _ _
      _ ≤ Real.sqrt (eta s)*‖z‖+‖G (s,0)‖ := add_le_add hd le_rfl
      _ = _ := rfl
  refine ⟨hG,hGLip,K,hK,hKs,fun s => ⟨?_,fun a t => ?_⟩⟩
  · rw [hKs s]
    exact (integrable_map_measure (by fun_prop) (hGm s).aemeasurable).mpr (hGi s)
  · have hf : LipschitzWith (Real.toNNReal (‖a‖*Real.sqrt (eta s)))
        (fun z => inner ℝ a (G (s,z))) := by
      apply LipschitzWith.of_dist_le_mul
      intro z w
      rw [dist_eq_norm,Real.norm_eq_abs,← inner_sub_right,
        Real.coe_toNNReal _ (mul_nonneg (norm_nonneg _) (Real.sqrt_nonneg _)),dist_eq_norm]
      have hd := hGLip s s z w rfl
      simp only [sub_self,norm_zero,zero_add] at hd
      calc
        |inner ℝ a (G (s,z)-G (s,w))| ≤ ‖a‖*‖G (s,z)-G (s,w)‖ :=
          abs_real_inner_le_norm _ _
        _ ≤ ‖a‖*(Real.sqrt (eta s)*‖z-w‖) :=
          mul_le_mul_of_nonneg_left hd (norm_nonneg _)
        _ = (‖a‖*Real.sqrt (eta s))*‖z-w‖ := by ring
    have he :=
      (AutoSamplingTheory.TechnicalLemmas.Probability.GaussianLipschitzExponential.integrable_and_integrable_exp_centered_of_lipschitz
        (μ := stdGaussian E) hf).2 t
    refine ⟨?_,?_⟩
    · rw [hKs s,integral_map (hGm s).aemeasurable (by fun_prop)]
      apply (integrable_map_measure (by fun_prop) (hGm s).aemeasurable).mpr
      convert he using 1
      funext z
      rw [Function.comp_apply,inner_sub_right,integral_inner (hGi s) a]
    · have hm : (∫ v, v ∂K s) = ∫ z, G (s,z) ∂stdGaussian E := by
        rw [hKs s]
        exact integral_map (hGm s).aemeasurable (by fun_prop)
      rw [hm,hKs s,integral_map (hGm s).aemeasurable (by fun_prop)]
      calc
        _ = ∫ z, Real.exp (t * (inner ℝ a (G (s,z)) -
            ∫ v, inner ℝ a (G (s,v)) ∂stdGaussian E)) ∂stdGaussian E := by
          apply integral_congr_ae
          filter_upwards with z
          rw [inner_sub_right,integral_inner (hGi s) a]
        _ ≤ Real.exp (((Real.toNNReal (‖a‖*Real.sqrt (eta s)) : ℝ≥0) : ℝ)^2*t^2/2) :=
          AutoSamplingTheory.TechnicalLemmas.Probability.GaussianLipschitzExponential.integral_exp_centered_le_stdGaussian_of_lipschitz hf t
        _ = _ := by
          congr 1
          rw [Real.coe_toNNReal _ (mul_nonneg (norm_nonneg _) (Real.sqrt_nonneg _)),
            mul_pow,Real.sq_sqrt (hpos s).le]
          ring


end AutoSamplingTheory.ExampleCases.SmoothedPicardHMC.FullRangeProximalGaussianOracle
end
