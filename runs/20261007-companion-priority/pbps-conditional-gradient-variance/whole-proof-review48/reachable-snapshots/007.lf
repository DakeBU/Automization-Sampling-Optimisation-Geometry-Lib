import AutoSamplingTheory.ExampleCases.ProximalBPS.ConditionalScore
import Mathlib.Analysis.Calculus.FDeriv.Symmetric
import Mathlib.Analysis.InnerProductSpace.Rayleigh
import AutoSamplingTheory.TechnicalLemmas.Analysis.QuadraticRegularization
import AutoSamplingTheory.TechnicalLemmas.Analysis.Integrability
import Mathlib.MeasureTheory.Measure.Tilted
import Mathlib.MeasureTheory.Function.L2Space
import AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.Poincare
open MeasureTheory ProbabilityTheory InnerProductSpace
open AutoSamplingTheory.TechnicalLemmas.Analysis
open scoped ContDiff NNReal



/-!
# Actual conditional curvature and noncompact directional scores

Source: arXiv:2609.06905v1 Appendix C.1, the conditional Hessian and score
bounds preceding the conditional Poincare step. This derives the actual
noncompact test domain, not the curvature-to-Poincare inequality itself.
The explicit alpha <= beta hypothesis is retained even in dimension zero.
-/

namespace AutoSamplingTheory.ExampleCases.ProximalBPS.ConditionalScoreDomain
universe u

/-- The actual reflected conditional law has the source curvature and sharp
score derivative bound, with directional scores in L2 and the stated finite
variance/gradient-energy domain. No Poincare inequality is assumed or proved. -/
theorem conditional_curvature_and_score_domain {E : Type u} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]
    {V : E → ℝ} {α β : NNReal} {η : ℝ}
    (hα : 0 < (α:ℝ)) (hαβ : α ≤ β) (hV : ContDiff ℝ 2 V)
    (hH : ∀ x v : E, (α:ℝ)*‖v‖^2 ≤ (fderiv ℝ (fderiv ℝ V) x v) v ∧
      (fderiv ℝ (fderiv ℝ V) x v) v ≤ (β:ℝ)*‖v‖^2)
    (hη : 0 < η) (hβη : (β:ℝ)*η ≤ 1) :
    let μ := (volume : Measure E).tilted (fun x => -V x)
    let J := Measure.map (fun p : E × E => (p.1,p.1+Real.sqrt η • p.2)) (μ.prod (stdGaussian E))
    let W := fun y u : E => V ((1/2:ℝ) • (y+u)) + ‖u-y‖^2/(8*η)
    let s := fun y u : E => -(1/2:ℝ) • fderiv ℝ V ((1/2:ℝ) • (y+u)) - (1/(4*η)) • innerSL ℝ (y-u)
    ∃ R S : Kernel E E, IsMarkovKernel R ∧ IsMarkovKernel S ∧
      (J.map Prod.swap).IsCondKernel R ∧
      (∀ y, S y = (R y).map (fun x => (2:ℝ) • x-y)) ∧
      ∀ y, S y = (volume : Measure E).tilted (fun u => -W y u) ∧
        ContDiff ℝ 2 (W y) ∧ ContDiff ℝ 1 (s y) ∧
        (∀ u v w,
          (fderiv ℝ (fderiv ℝ (W y)) u v) w =
            (1/4:ℝ)*(fderiv ℝ (fderiv ℝ V) ((1/2:ℝ) • (y+u)) v) w + (1/(4*η))*inner ℝ v w ∧
          (fderiv ℝ (s y) u v) w = (1/(4*η))*inner ℝ v w -
            (1/4:ℝ)*(fderiv ℝ (fderiv ℝ V) ((1/2:ℝ) • (y+u)) v) w) ∧
        (∀ u v, (((α:ℝ)+1/η)/4)*‖v‖^2 ≤ (fderiv ℝ (fderiv ℝ (W y)) u v) v) ∧
        (∀ u, ‖fderiv ℝ (s y) u‖ ≤ (1/η-(α:ℝ))/4) ∧
        ∀ a : E, ContDiff ℝ 1 (fun u => s y u a) ∧
          MemLp (fun u => s y u a) 2 (S y) ∧
          AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.Poincare.Admissible (S y) (fun u => s y u a) ∧
          ∀ u, ‖gradient (fun z => s y z a) u‖ ≤ ((1/η-(α:ℝ))/4)*‖a‖ := by
  have conditional_derivatives {E : Type u} [NormedAddCommGroup E] [InnerProductSpace ℝ E] [CompleteSpace E]
      {V : E → ℝ} (hV : ContDiff ℝ 2 V) (η : ℝ) (y : E) :
      let W := fun u : E => V ((1/2:ℝ) • (y+u)) + ‖u-y‖^2/(8*η)
      let s := fun u : E => -(1/2:ℝ) • fderiv ℝ V ((1/2:ℝ) • (y+u)) -
        (1/(4*η)) • innerSL ℝ (y-u)
      ContDiff ℝ 2 W ∧ ContDiff ℝ 1 s ∧
        ∀ u v w : E,
          (fderiv ℝ (fderiv ℝ W) u v) w =
            (1/4:ℝ) * (fderiv ℝ (fderiv ℝ V) ((1/2:ℝ) • (y+u)) v) w +
              (1/(4*η)) * inner ℝ v w ∧
          (fderiv ℝ s u v) w =
            (1/(4*η)) * inner ℝ v w -
              (1/4:ℝ) * (fderiv ℝ (fderiv ℝ V) ((1/2:ℝ) • (y+u)) v) w := by
    let mid := fun u : E => (1/2:ℝ) • (y+u)
    let W := fun u : E => V (mid u) + ‖u-y‖^2/(8*η)
    let s := fun u : E => -(1/2:ℝ) • fderiv ℝ V (mid u) -
        (1/(4*η)) • innerSL ℝ (y-u)
    let J : E →L[ℝ] (E →L[ℝ] ℝ) :=
      { toFun := fun v => innerSL ℝ v
        map_add' := by intros; ext; simp
        map_smul' := by intros; ext; simp
        cont := (innerSL ℝ (E := E)).continuous }
    have hmid (u : E) : HasFDerivAt mid ((1/2:ℝ) • ContinuousLinearMap.id ℝ E) u := by
      convert ((hasFDerivAt_const (𝕜 := ℝ) y u).add (hasFDerivAt_id u)).const_smul (1/2:ℝ) using 1 <;> simp [mid] <;> rfl
    have hVd := hV.differentiable (by norm_num)
    have hVdd := (hV.fderiv_right (m := 1) (by norm_num)).differentiable_one
    have hmidC : ContDiff ℝ 2 mid := by fun_prop
    have hWC : ContDiff ℝ 2 W := hV.comp hmidC |>.add (((contDiff_id.sub contDiff_const).norm_sq (𝕜 := ℝ)).div_const _)
    have hsC : ContDiff ℝ 1 s := by
      apply ContDiff.sub
      · exact ((hV.fderiv_right (m := 1) (by norm_num)).comp (hmidC.of_le (by norm_num))).const_smul _
      · exact (J.contDiff.comp (contDiff_const.sub contDiff_id)).const_smul _
    have hWfd (u : E) : fderiv ℝ W u =
        (1/2:ℝ) • fderiv ℝ V (mid u) + (1/(4*η)) • J (u-y) := by
      have hv := (hVd (mid u)).hasFDerivAt.comp u (hmid u)
      have hq := (((hasFDerivAt_id u).sub_const y).norm_sq).const_mul (1/(8*η))
      have hw : HasFDerivAt W ((1/2:ℝ) • fderiv ℝ V (mid u) + (1/(4*η)) • J (u-y)) u := by
        convert hv.add hq using 1 <;> first | rfl | (ext v; simp [W,J,Function.comp_def]; ring)
      exact hw.fderiv
    have hWdd (u : E) : HasFDerivAt (fderiv ℝ W)
        ((1/4:ℝ) • fderiv ℝ (fderiv ℝ V) (mid u) + (1/(4*η)) • J) u := by
      rw [show fderiv ℝ W = _ from funext hWfd]
      convert (((hVdd (mid u)).hasFDerivAt.comp u (hmid u)).const_smul (1/2:ℝ)).add
        ((J.hasFDerivAt.comp u ((hasFDerivAt_id u).sub_const y)).const_smul (1/(4*η))) using 1 <;>
        first | rfl | (ext v w; simp; ring)
    have hsD (u : E) : HasFDerivAt s
        ((1/(4*η)) • J - (1/4:ℝ) • fderiv ℝ (fderiv ℝ V) (mid u)) u := by
      convert (((hVdd (mid u)).hasFDerivAt.comp u (hmid u)).const_smul (-(1/2:ℝ))).sub
        ((J.hasFDerivAt.comp u ((hasFDerivAt_const (𝕜 := ℝ) y u).sub (hasFDerivAt_id u))).const_smul (1/(4*η))) using 1 <;>
        first | rfl | (ext v w; simp; ring)
    refine ⟨hWC,hsC,?_⟩
    intro u v w
    rw [(hWdd u).fderiv,(hsD u).fderiv]
    constructor <;> rfl

  have sharp_score_norm {E : Type u} [NormedAddCommGroup E] [InnerProductSpace ℝ E] [CompleteSpace E]
      {V : E → ℝ} (hV : ContDiff ℝ 2 V) {α β η : ℝ}
      (hαβ : α ≤ β) (hη : 0 < η) (hβη : β*η ≤ 1)
      (hH : ∀ x v : E, α*‖v‖^2 ≤ (fderiv ℝ (fderiv ℝ V) x v) v ∧
        (fderiv ℝ (fderiv ℝ V) x v) v ≤ β*‖v‖^2)
      (x : E) (D : E →L[ℝ] (E →L[ℝ] ℝ))
      (hD : ∀ v w, D v w = (1/(4*η))*inner ℝ v w -
        (1/4:ℝ)*(fderiv ℝ (fderiv ℝ V) x v) w) :
      ‖D‖ ≤ (1/η-α)/4 := by
    let R : (E →L[ℝ] ℝ) →L[ℝ] E :=
      { toFun := (toDual ℝ E).symm
        map_add' := (toDual ℝ E).symm.map_add
        map_smul' := by intros; simp
        cont := (toDual ℝ E).symm.continuous }
    let T := R.comp D
    have hinner (v w : E) : inner ℝ (T v) w = D v w := toDual_symm_apply
    have hsym : T.IsSymmetric := by
      intro v w
      change inner ℝ (T v) w = inner ℝ v (T w)
      calc
        _ = D v w := hinner v w
        _ = D w v := by
          rw [hD,hD,hV.contDiffAt.isSymmSndFDerivAt (by norm_num) v w,real_inner_comm w v]
        _ = inner ℝ (T w) v := (hinner w v).symm
        _ = inner ℝ v (T w) := real_inner_comm _ _
    have hβ : β ≤ 1/η := (le_div_iff₀ hη).2 hβη
    have hc : 0 ≤ (1/η-α)/4 := div_nonneg (sub_nonneg.mpr (hαβ.trans hβ)) (by norm_num)
    have hdiag (v : E) : D v v = ((1/η)*‖v‖^2-(fderiv ℝ (fderiv ℝ V) x v) v)/4 := by
      rw [hD,real_inner_self_eq_norm_sq]
      ring
    have hbounds (v : E) : 0 ≤ D v v ∧ D v v ≤ ((1/η-α)/4)*‖v‖^2 := by
      rw [hdiag]
      have hh := hH x v
      have hb := mul_le_mul_of_nonneg_right hβ (sq_nonneg ‖v‖)
      constructor <;> nlinarith
    have hnormT : ‖T‖ ≤ (1/η-α)/4 := by
      rw [T.norm_eq_iSup_rayleighQuotient hsym]
      apply ciSup_le
      intro v
      change |inner ℝ (T v) v / ‖v‖^2| ≤ (1/η-α)/4
      rw [hinner,abs_of_nonneg (div_nonneg (hbounds v).1 (sq_nonneg _))]
      by_cases hv : v=0
      · simpa [hv] using hc
      · exact (div_le_iff₀ (sq_pos_of_pos (norm_pos_iff.mpr hv))).2 (hbounds v).2
    apply D.opNorm_le_bound hc
    intro v
    calc
      ‖D v‖ = ‖T v‖ := ((toDual ℝ E).symm.norm_map (D v)).symm
      _ ≤ ‖T‖ * ‖v‖ := T.le_opNorm v
      _ ≤ ((1/η-α)/4)*‖v‖ := mul_le_mul_of_nonneg_right hnormT (norm_nonneg _)

  have absorb_quadratic {a r : ℝ} (ha : 0 < a) :
      r^2 * Real.exp (-a*r^2) ≤ (2/a)*Real.exp (-(a/2)*r^2) := by
    have hx : (a/2)*r^2 ≤ Real.exp ((a/2)*r^2) := by
      linarith [Real.add_one_le_exp ((a/2)*r^2)]
    have hm := mul_le_mul_of_nonneg_right hx (Real.exp_nonneg (-a*r^2))
    have he : Real.exp ((a/2)*r^2)*Real.exp (-a*r^2) = Real.exp (-(a/2)*r^2) := by
      rw [← Real.exp_add]
      congr 1
      ring
    rw [he] at hm
    calc
      r^2 * Real.exp (-a*r^2) ≤ Real.exp (-(a/2)*r^2)/(a/2) :=
        (le_div_iff₀ (by positivity : 0 < a/2)).2 (by nlinarith [hm])
      _ = (2/a)*Real.exp (-(a/2)*r^2) := by ring

  have weighted_linear_memLp {E : Type u} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
      [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]
      (w q : E → ℝ) (hw : Continuous w) (hq : Continuous q)
      {a C A B : ℝ} (ha : 0 < a) (hC : 0 ≤ C) (hA : 0 ≤ A) (hB : 0 ≤ B)
      (hweight : ∀ u, Real.exp (w u) ≤ C*Real.exp (-a*‖u‖^2))
      (hgrowth : ∀ u, ‖q u‖ ≤ A+B*‖u‖) :
      Integrable (fun u => Real.exp (w u)) (volume : Measure E) ∧
        MemLp q 2 ((volume : Measure E).tilted w) := by
    have hwi : Integrable (fun u => Real.exp (w u)) (volume : Measure E) := by
      apply ((AutoSamplingTheory.TechnicalLemmas.Analysis.Integrability.integrable_exp_neg_mul_norm_sq
        (E := E) ha).const_mul C).mono' hw.rexp.aestronglyMeasurable
      filter_upwards with u
      simpa only [Real.norm_eq_abs,abs_of_pos (Real.exp_pos _)] using hweight u
    refine ⟨hwi,?_⟩
    apply (memLp_two_iff_integrable_sq hq.aestronglyMeasurable).2
    apply (integrable_tilted_iff hwi (fun u => q u ^ 2)).2
    have hdom := (AutoSamplingTheory.TechnicalLemmas.Analysis.Integrability.integrable_exp_neg_mul_norm_sq
        (E := E) (show 0 < a/2 by positivity)).const_mul (C*(2*A^2+4*B^2/a))
    apply hdom.mono' (hw.rexp.smul (hq.pow 2)).aestronglyMeasurable
    filter_upwards with u
    change ‖Real.exp (w u)*(q u)^2‖ ≤ C*(2*A^2+4*B^2/a)*Real.exp (-(a/2)*‖u‖^2)
    simp only [smul_eq_mul,Real.norm_eq_abs,abs_of_nonneg (mul_nonneg (Real.exp_nonneg _) (sq_nonneg _))]
    have hs : (q u)^2 ≤ 2*A^2+2*B^2*‖u‖^2 := by
      have hh := (sq_le_sq₀ (norm_nonneg (q u)) (by positivity)).2 (hgrowth u)
      rw [Real.norm_eq_abs,sq_abs] at hh
      nlinarith [sq_nonneg (A-B*‖u‖)]
    have he : Real.exp (-a*‖u‖^2) ≤ Real.exp (-(a/2)*‖u‖^2) := by
      apply Real.exp_le_exp.mpr
      nlinarith [mul_nonneg ha.le (sq_nonneg ‖u‖)]
    calc
      Real.exp (w u)*(q u)^2 ≤ (C*Real.exp (-a*‖u‖^2))*(2*A^2+2*B^2*‖u‖^2) :=
        mul_le_mul (hweight u) hs (sq_nonneg _) (mul_nonneg hC (Real.exp_nonneg _))
      _ = C*(2*A^2*Real.exp (-a*‖u‖^2)+2*B^2*(‖u‖^2*Real.exp (-a*‖u‖^2))) := by ring
      _ ≤ C*(2*A^2*Real.exp (-(a/2)*‖u‖^2)+2*B^2*((2/a)*Real.exp (-(a/2)*‖u‖^2))) := by
        apply mul_le_mul_of_nonneg_left _ hC
        exact add_le_add (mul_le_mul_of_nonneg_left he (by positivity))
          (mul_le_mul_of_nonneg_left (absorb_quadratic (r := ‖u‖) ha) (by positivity))
      _ = C*(2*A^2+4*B^2/a)*Real.exp (-(a/2)*‖u‖^2) := by ring

  have admissible_of_memLp_gradient_bound {E : Type u} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
      [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]
      (μ : Measure E) [IsFiniteMeasure μ] (q : E → ℝ)
      (hq : ContDiff ℝ 1 q) (hLp : MemLp q 2 μ)
      {M : ℝ} (hM : ∀ u, ‖gradient q u‖ ≤ M) :
      AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.Poincare.Admissible μ q := by
    have hgc : Continuous (gradient q) :=
      (toDual ℝ E).symm.continuous.comp (hq.continuous_fderiv (by norm_num))
    have hgLp : MemLp (gradient q) 2 μ :=
      MemLp.of_bound hgc.aestronglyMeasurable M (Filter.Eventually.of_forall hM)
    refine ⟨hLp.integrable (by norm_num),?_,?_⟩
    · exact (hLp.sub (memLp_const _)).integrable_sq
    · exact (memLp_two_iff_integrable_sq_norm hgc.aestronglyMeasurable).1 hgLp

  have directional_score {E : Type u} [NormedAddCommGroup E] [InnerProductSpace ℝ E] [CompleteSpace E]
      (s : E → (E →L[ℝ] ℝ)) (hs : ContDiff ℝ 1 s) {c : ℝ} (hc : 0 ≤ c)
      (hD : ∀ u, ‖fderiv ℝ s u‖ ≤ c) (a : E) :
      ContDiff ℝ 1 (fun u => s u a) ∧ ∀ u,
        ‖gradient (fun z => s z a) u‖ ≤ c*‖a‖ := by
    let ev := ContinuousLinearMap.apply' ℝ (RingHom.id ℝ) a
    have hq : ContDiff ℝ 1 (fun u => s u a) := ev.contDiff.comp hs
    refine ⟨hq,?_⟩
    intro u
    have hqD : HasFDerivAt (fun z => s z a) (ev.comp (fderiv ℝ s u)) u :=
      ev.hasFDerivAt.comp u ((hs.differentiable (by norm_num)) u).hasFDerivAt
    have hdn : ‖fderiv ℝ (fun z => s z a) u‖ ≤ c*‖a‖ := by
      rw [hqD.fderiv]
      apply ContinuousLinearMap.opNorm_le_bound _ (mul_nonneg hc (norm_nonneg _))
      intro v
      change ‖(fderiv ℝ s u v) a‖ ≤ (c*‖a‖)*‖v‖
      calc
        ‖(fderiv ℝ s u v) a‖ ≤ ‖fderiv ℝ s u v‖*‖a‖ := (fderiv ℝ s u v).le_opNorm a
        _ ≤ (‖fderiv ℝ s u‖*‖v‖)*‖a‖ := mul_le_mul_of_nonneg_right ((fderiv ℝ s u).le_opNorm v) (norm_nonneg _)
        _ ≤ (c*‖v‖)*‖a‖ := mul_le_mul_of_nonneg_right (mul_le_mul_of_nonneg_right (hD u) (norm_nonneg _)) (norm_nonneg _)
        _ = (c*‖a‖)*‖v‖ := by ring
    rw [← toDual_gradient,(toDual ℝ E).norm_map] at hdn
    exact hdn

  have potential_controls {E : Type u} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
      [FiniteDimensional ℝ E] {V : E → ℝ} {α β : ℝ≥0}
      (hα : 0 < (α : ℝ)) (hV : ContDiff ℝ 2 V)
      (hH : ∀ x v : E,
        (α : ℝ)*‖v‖^2 ≤ (fderiv ℝ (fderiv ℝ V) x v) v ∧
        (fderiv ℝ (fderiv ℝ V) x v) v ≤ (β : ℝ)*‖v‖^2) :
      (∀ x, V 0 - (α : ℝ)⁻¹/2*‖gradient V 0‖^2 ≤ V x) ∧
      (∀ x, ‖fderiv ℝ V x‖ ≤ ‖gradient V 0‖ + (β : ℝ)*‖x‖) := by
    have hd : Differentiable ℝ V := hV.differentiable (by norm_num)
    have hreg := QuadraticRegularization.strongConvexOn_and_lipschitzWith_gradient_add_quadratic
      hV hH (r := 0) (0 : E)
    simp only [NNReal.coe_zero, zero_div, zero_mul, add_zero] at hreg
    constructor
    · intro x
      have hfirst := StrongConvexFirstOrder.firstOrder_lower_bound_of_strongConvexOn hreg.1
          (fun z _ => (hd z).hasGradientAt) (x := 0) (y := x)
          (Set.mem_univ _) (Set.mem_univ _)
      simp only [sub_zero] at hfirst
      have hinner := (abs_le.mp (abs_real_inner_le_norm (gradient V 0) x)).1
      have hyoung := two_mul_le_add_mul_sq (a := ‖x‖) (b := ‖gradient V 0‖) hα
      nlinarith
    · intro x
      rw [← toDual_gradient]
      rw [(toDual ℝ E).norm_map]
      calc
        ‖gradient V x‖ ≤ ‖gradient V x - gradient V 0‖ + ‖gradient V 0‖ :=
          norm_le_norm_sub_add _ _
        _ ≤ (β : ℝ)*‖x‖ + ‖gradient V 0‖ := by
          apply add_le_add _ (le_refl _)
          simpa using hreg.2.norm_sub_le x 0
        _ = _ := add_comm _ _

  have weight_envelope {E : Type u} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
      (V : E → ℝ) {m η R : ℝ} (hV : ∀ x, m ≤ V x) (hη : 0 < η)
      (y u : E) (hy : ‖y‖ ≤ R) :
      Real.exp (-V ((1/2:ℝ) • (y+u)) - ‖y-u‖^2/(8*η)) ≤
        Real.exp (-m+R^2/(8*η)) * Real.exp (-(1/(16*η))*‖u‖^2) := by
    have hR : 0 ≤ R := (norm_nonneg y).trans hy
    have htri : ‖u‖ ≤ ‖y-u‖ + R := by
      have h := norm_le_norm_sub_add u y
      rw [norm_sub_rev u y] at h
      linarith
    have hsq : ‖u‖^2 ≤ 2*‖y-u‖^2 + 2*R^2 := by
      have ht := (sq_le_sq₀ (norm_nonneg u) (by positivity)).mpr htri
      nlinarith [sq_nonneg (‖y-u‖-R)]
    have hq := div_le_div_of_nonneg_right hsq (by positivity : 0 ≤ 16*η)
    have hdiv : ‖u‖^2/(16*η) ≤ ‖y-u‖^2/(8*η) + R^2/(8*η) := by
      have heq : (2*‖y-u‖^2+2*R^2)/(16*η) = ‖y-u‖^2/(8*η)+R^2/(8*η) := by
        field_simp
        ring
      rw [heq] at hq
      exact hq
    rw [← Real.exp_add]
    apply Real.exp_le_exp.mpr
    have hv := hV ((1/2:ℝ) • (y+u))
    simp only [div_eq_mul_inv, one_mul] at hdiv ⊢
    nlinarith

  have score_envelope {E : Type u} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
      [CompleteSpace E] (V : E → ℝ) {G β η R : ℝ}
      (hG : ∀ x, ‖fderiv ℝ V x‖ ≤ G+β*‖x‖) (hβ : 0 ≤ β) (hη : 0 < η)
      (y u : E) (hy : ‖y‖ ≤ R) :
      ‖-(1/2:ℝ) • fderiv ℝ V ((1/2:ℝ) • (y+u)) -
        (1/(4*η)) • innerSL ℝ (y-u)‖ ≤
        G/2 + ((β+η⁻¹)/4)*R + ((β+η⁻¹)/4)*‖u‖ := by
    have hmid : ‖(1/2:ℝ) • (y+u)‖ ≤ (R+‖u‖)/2 := by
      rw [norm_smul, Real.norm_eq_abs]
      norm_num
      have h := norm_add_le y u
      linarith
    have hfd : ‖fderiv ℝ V ((1/2:ℝ) • (y+u))‖ ≤ G+β*((R+‖u‖)/2) :=
      (hG _).trans (add_le_add (le_refl _) (mul_le_mul_of_nonneg_left hmid hβ))
    have hdiff : ‖y-u‖ ≤ R+‖u‖ := (norm_sub_le _ _).trans (add_le_add hy (le_refl _))
    calc
      _ ≤ ‖-(1/2:ℝ) • fderiv ℝ V ((1/2:ℝ) • (y+u))‖ +
          ‖(1/(4*η)) • innerSL ℝ (y-u)‖ := norm_sub_le _ _
      _ = (1/2:ℝ)*‖fderiv ℝ V ((1/2:ℝ) • (y+u))‖ + (1/(4*η))*‖y-u‖ := by
        simp only [norm_smul, Real.norm_eq_abs, innerSL_apply_norm]
        rw [abs_of_pos (by positivity : 0 < 1/(4*η))]
        norm_num
      _ ≤ (1/2:ℝ)*(G+β*((R+‖u‖)/2)) + (1/(4*η))*(R+‖u‖) := by
        gcongr
      _ = _ := by simp only [div_eq_mul_inv, mul_inv_rev]; ring
  let W := fun y u : E => V ((1/2:ℝ) • (y+u)) + ‖u-y‖^2/(8*η)
  let s := fun y u : E => -(1/2:ℝ) • fderiv ℝ V ((1/2:ℝ) • (y+u)) - (1/(4*η)) • innerSL ℝ (y-u)
  obtain ⟨R,S,hR,hS,hcond,hSR,hSν,hder⟩ :=
    AutoSamplingTheory.ExampleCases.ProximalBPS.ConditionalScore.reflected_conditional_covariance hα hV hH hη
  let _ : IsMarkovKernel S := hS
  obtain ⟨hmin,hgrad⟩ := potential_controls hα hV hH
  have hαβr : (α:ℝ) ≤ β := hαβ
  have hβInv : (β:ℝ) ≤ 1/η := (le_div_iff₀ hη).2 hβη
  have hc : 0 ≤ (1/η-(α:ℝ))/4 := div_nonneg (sub_nonneg.mpr (hαβr.trans hβInv)) (by norm_num)
  dsimp only
  refine ⟨R,S,hR,hS,hcond,hSR,?_⟩
  intro y
  have hSy : S y = (volume : Measure E).tilted (fun u => -W y u) := by
    rw [hSν y]
    congr 1
    funext u
    dsimp [W]
    rw [norm_sub_rev u y]
    ring
  obtain ⟨hWC,hsC,hcalc⟩ := conditional_derivatives hV η y
  have hDn (u : E) : ‖fderiv ℝ (s y) u‖ ≤ (1/η-(α:ℝ))/4 :=
    sharp_score_norm hV hαβr hη hβη hH ((1/2:ℝ) • (y+u)) (fderiv ℝ (s y) u)
      (fun v w => (hcalc u v w).2)
  refine ⟨hSy,hWC,hsC,hcalc,?_,hDn,?_⟩
  · intro u v
    rw [(hcalc u v v).1,real_inner_self_eq_norm_sq]
    have hco : 1/(4*η) = (1/η)/4 := by ring
    rw [hco]
    nlinarith [(hH ((1/2:ℝ) • (y+u)) v).1]
  · intro a
    obtain ⟨hqC,hqG⟩ := directional_score (s y) hsC hc hDn a
    let b := ((β:ℝ)+η⁻¹)/4
    let A := ‖gradient V 0‖/2+b*‖y‖
    let m := V 0 - (α:ℝ)⁻¹/2*‖gradient V 0‖^2
    have hb : 0 ≤ b := by dsimp [b]; positivity
    have hA : 0 ≤ A := by dsimp [A]; positivity
    have hqgrowth (u : E) : ‖s y u a‖ ≤ (A*‖a‖)+(b*‖a‖)*‖u‖ := by
      have hsg := score_envelope V hgrad (NNReal.coe_nonneg β) hη y u (le_refl ‖y‖)
      calc
        ‖s y u a‖ ≤ ‖s y u‖*‖a‖ := (s y u).le_opNorm a
        _ ≤ (A+b*‖u‖)*‖a‖ := mul_le_mul_of_nonneg_right hsg (norm_nonneg _)
        _ = _ := by ring
    have hweight (u : E) : Real.exp (-W y u) ≤
        Real.exp (-m+‖y‖^2/(8*η))*Real.exp (-(1/(16*η))*‖u‖^2) := by
      have hw := weight_envelope V hmin hη y u (le_refl ‖y‖)
      convert hw using 1
      dsimp [W]
      rw [norm_sub_rev u y]
      congr 1
      ring
    have hLp : MemLp (fun u => s y u a) 2 (S y) := by
      rw [hSy]
      exact (weighted_linear_memLp (fun u => -W y u) (fun u => s y u a)
        hWC.continuous.neg hqC.continuous (by positivity) (Real.exp_nonneg _)
        (mul_nonneg hA (norm_nonneg _)) (mul_nonneg hb (norm_nonneg _)) hweight hqgrowth).2
    exact ⟨hqC,hLp,admissible_of_memLp_gradient_bound (S y) (fun u => s y u a) hqC hLp hqG,hqG⟩

end AutoSamplingTheory.ExampleCases.ProximalBPS.ConditionalScoreDomain
