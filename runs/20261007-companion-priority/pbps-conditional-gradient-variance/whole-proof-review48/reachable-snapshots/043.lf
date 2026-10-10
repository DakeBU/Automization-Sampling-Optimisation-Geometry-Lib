import AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Gradient
import Mathlib.Analysis.Calculus.LineDeriv.IntegrationByParts
import Mathlib.Analysis.InnerProductSpace.Calculus
import Mathlib.Analysis.Normed.Lp.SmoothApprox
import Mathlib.Analysis.InnerProductSpace.LinearPMap
import Mathlib.MeasureTheory.Function.L2Space
import Mathlib.MeasureTheory.Measure.Tilted

/-!
# Dense closable gradient for a normalized Gibbs measure

Directly proved Euclidean full-space Sobolev prerequisite for PBPS
arXiv:2609.06905v1 Appendix C.1. Background arXiv:1310.2526v7 section 2.5
uses weighted Sobolev completions on compact manifolds. This construction
is not that source's spectral theorem or a manifold/boundary generalization.

The actual graph consists exactly of smooth compact scalar representatives
and their genuine gradients. Weighted vector-field integration by parts
and vector-valued smooth L2 density prove single-valuedness of its closure.
Only C1 potential and actual exponential integrability are assumed; no
Poincare, coercivity, closed-generator or operator-core premise is used.
The result includes dimension zero. No claim about the operator core of D*D,
resolvent regularity, noncompact score bounds or a complete paper is made.
-/

namespace AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.WeightedGradient

open MeasureTheory InnerProductSpace
open scoped RealInnerProductSpace ContDiff Topology

variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
  [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]

theorem compact_gradient_closable (W : E → ℝ) (hW : ContDiff ℝ 1 W)
    (hI : Integrable (fun x => Real.exp (-W x))) :
    let μ := (volume : Measure E).tilted (fun x => -W x)
    ∃ D : Lp ℝ 2 μ →ₗ.[ℝ] Lp E 2 μ,
      Dense (D.domain : Set (Lp ℝ 2 μ)) ∧ D.IsClosable ∧ D.closure.IsClosed ∧
      ∀ (u : Lp ℝ 2 μ) (v : Lp E 2 μ), (u,v) ∈ D.graph ↔
        ∃ f : E → ℝ, ContDiff ℝ ∞ f ∧ HasCompactSupport f ∧
          u =ᵐ[μ] f ∧ v =ᵐ[μ] gradient f := by
  have weighted_directional (W f g : E → ℝ) (hW : ContDiff ℝ 1 W)
      (hf : ContDiff ℝ 1 f) (hg : ContDiff ℝ 1 g)
      (hgc : HasCompactSupport g) (v : E) :
      (∫ x, Real.exp (-W x) * g x * fderiv ℝ f x v) =
        - ∫ x, Real.exp (-W x) *
          (fderiv ℝ g x v - g x * fderiv ℝ W x v) * f x := by
    let F := fun x => Real.exp (-W x) * g x
    have hF : ContDiff ℝ 1 F := hW.neg.exp.mul hg
    have hFc : HasCompactSupport F := hgc.mul_left
    have hDF : Continuous (fun x => fderiv ℝ F x v) :=
      (hF.fderiv_right (m := 0) (by norm_num)).continuous.clm_apply continuous_const
    have hDf : Continuous (fun x => fderiv ℝ f x v) :=
      (hf.fderiv_right (m := 0) (by norm_num)).continuous.clm_apply continuous_const
    have hDFc : HasCompactSupport (fun x => fderiv ℝ F x v) := by
      refine HasCompactSupport.of_support_subset_isCompact hFc.isCompact ?_
      intro x hx
      by_contra hn
      exact hx (by simp [fderiv_of_notMem_tsupport ℝ hn])
    have h1 : Integrable (fun x => fderiv ℝ F x v * f x) :=
      (hDF.mul hf.continuous).integrable_of_hasCompactSupport hDFc.mul_right
    have h2 : Integrable (fun x => F x * fderiv ℝ f x v) :=
      (hF.continuous.mul hDf).integrable_of_hasCompactSupport hFc.mul_right
    have h3 : Integrable (fun x => F x * f x) :=
      (hF.continuous.mul hf.continuous).integrable_of_hasCompactSupport hFc.mul_right
    have hi := integral_mul_fderiv_eq_neg_fderiv_mul_of_integrable h1 h2 h3
      (fun x _ => hF.differentiable one_ne_zero x)
      (fun x _ => hf.differentiable one_ne_zero x)
    change (∫ x, F x * fderiv ℝ f x v) = _
    rw [hi]
    congr 1
    apply integral_congr_ae
    filter_upwards [] with x
    have hd := ((hW.differentiable one_ne_zero x).hasFDerivAt.neg.exp).mul
      (hg.differentiable one_ne_zero x).hasFDerivAt
    have he : fderiv ℝ F x v = Real.exp (-W x) *
        (fderiv ℝ g x v - g x * fderiv ℝ W x v) := by
      rw [show fderiv ℝ F x = _ from hd.fderiv]
      simp only [add_apply, smul_apply, neg_apply, smul_eq_mul, Pi.neg_apply]
      ring
    rw [he]

  have gradient_cont (f : E → ℝ) (hf : ContDiff ℝ 1 f) : Continuous (gradient f) := by
    exact (toDual ℝ E).symm.continuous.comp (hf.fderiv_right (m := 0) (by norm_num)).continuous

  have gradient_compact (f : E → ℝ) (hc : HasCompactSupport f) :
      HasCompactSupport (gradient f) := by
    refine HasCompactSupport.of_support_subset_isCompact hc.isCompact ?_
    intro x hx
    by_contra hn
    exact hx (by simp [gradient, fderiv_of_notMem_tsupport ℝ hn])

  have raw_vector_ibp (W : E → ℝ) (hW : ContDiff ℝ 1 W)
      (P : E → E) (hP : ContDiff ℝ 1 P) (hPc : HasCompactSupport P) :
      ∃ q : E → ℝ, Continuous q ∧ HasCompactSupport q ∧
        ∀ (f : E → ℝ), ContDiff ℝ 1 f →
          (∫ x, Real.exp (-W x) * inner ℝ (gradient f x) (P x)) =
            ∫ x, Real.exp (-W x) * f x * q x := by
    let b := stdOrthonormalBasis ℝ E
    let g := fun i x => inner ℝ (P x) (b i)
    have hg (i) : ContDiff ℝ 1 (g i) := hP.inner ℝ contDiff_const
    have hgc (i) : HasCompactSupport (g i) := by
      refine HasCompactSupport.of_support_subset_isCompact hPc.isCompact ?_
      intro x hx
      by_contra hn
      exact hx (by simp [g, image_eq_zero_of_notMem_tsupport hn])
    have hdg (i) : Continuous (fun x => fderiv ℝ (g i) x (b i)) :=
      ((hg i).fderiv_right (m := 0) (by norm_num)).continuous.clm_apply continuous_const
    have hdgc (i) : HasCompactSupport (fun x => fderiv ℝ (g i) x (b i)) := by
      refine HasCompactSupport.of_support_subset_isCompact (hgc i).isCompact ?_
      intro x hx
      by_contra hn
      exact hx (by simp [fderiv_of_notMem_tsupport ℝ hn])
    have hdW (i) : Continuous (fun x => fderiv ℝ W x (b i)) :=
      (hW.fderiv_right (m := 0) (by norm_num)).continuous.clm_apply continuous_const
    let Q := fun i x => -(fderiv ℝ (g i) x (b i) - g i x * fderiv ℝ W x (b i))
    have hQ (i) : Continuous (Q i) := ((hdg i).sub ((hg i).continuous.mul (hdW i))).neg
    have hQc (i) : HasCompactSupport (Q i) := ((hdgc i).sub (hgc i).mul_right).neg
    let q := fun x => ∑ i, Q i x
    refine ⟨q,continuous_finsetSum _ (fun i _ => hQ i),?_,?_⟩
    · have hfun : q = ∑ i, Q i := by funext x; simp [q]
      rw [hfun]
      exact HasCompactSupport.finset_sum (s := Finset.univ) (f := Q) fun i _ => hQc i
    intro f hf
    have hA (i) : Integrable (fun x => Real.exp (-W x) * g i x * fderiv ℝ f x (b i)) := by
      apply (((hW.neg.exp).continuous.mul (hg i).continuous).mul
        ((hf.fderiv_right (m := 0) (by norm_num)).continuous.clm_apply continuous_const)).integrable_of_hasCompactSupport
      exact (hgc i).mul_left.mul_right
    have hB (i) : Integrable (fun x => Real.exp (-W x) * f x * Q i x) :=
      (((hW.neg.exp).continuous.mul hf.continuous).mul (hQ i)).integrable_of_hasCompactSupport (hQc i).mul_left
    have hpoint (x : E) : inner ℝ (gradient f x) (P x) =
        ∑ i, g i x * fderiv ℝ f x (b i) := by
      rw [← b.sum_inner_mul_inner (gradient f x) (P x)]
      apply Finset.sum_congr rfl
      intro i _
      rw [AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Gradient.fderiv_apply_eq_inner_gradient_of_differentiableAt (hf.differentiable one_ne_zero x)]
      simp only [g, real_inner_comm (b i) (P x), mul_comm]
    simp_rw [hpoint, Finset.mul_sum]
    rw [integral_finsetSum _ (fun i _ => by simpa [mul_assoc] using hA i)]
    change _ = ∫ x, Real.exp (-W x) * f x * ∑ i, Q i x
    simp_rw [Finset.mul_sum]
    rw [integral_finsetSum _ (fun i _ => hB i)]
    apply Finset.sum_congr rfl
    intro i _
    rw [show (∫ x, Real.exp (-W x) * (g i x * fderiv ℝ f x (b i))) =
      ∫ x, Real.exp (-W x) * g i x * fderiv ℝ f x (b i) by congr 1; funext x; ring]
    rw [weighted_directional W f (g i) hW hf (hg i) (hgc i) (b i), ← integral_neg]
    apply integral_congr_ae
    filter_upwards [] with x
    dsimp only [Q]
    ring

  have tilted_vector_ibp (W : E → ℝ) (hW : ContDiff ℝ 1 W)
      (hI : Integrable (fun x => Real.exp (-W x)))
      (P : E → E) (hP : ContDiff ℝ 1 P) (hPc : HasCompactSupport P) :
      let μ := (volume : Measure E).tilted (fun x => -W x)
      ∃ q : E → ℝ, Continuous q ∧ HasCompactSupport q ∧ MemLp q 2 μ ∧
        ∀ (f : E → ℝ), ContDiff ℝ 1 f →
          (∫ x, inner ℝ (gradient f x) (P x) ∂μ) = ∫ x, f x * q x ∂μ := by
    let μ := (volume : Measure E).tilted (fun x => -W x)
    let : IsProbabilityMeasure μ := isProbabilityMeasure_tilted hI
    obtain ⟨q,hq,hqc,hi⟩ := raw_vector_ibp W hW P hP hPc
    refine ⟨q,hq,hqc,hq.memLp_of_hasCompactSupport hqc,?_⟩
    have ht (g : E → ℝ) : (∫ x, g x ∂μ) =
        (∫ x, Real.exp (-W x))⁻¹ * ∫ x, Real.exp (-W x) * g x := by
      rw [show μ = (volume : Measure E).tilted (fun x => -W x) from rfl, integral_tilted]
      rw [← integral_const_mul]
      apply integral_congr_ae
      filter_upwards [] with x
      change (Real.exp (-W x) / (∫ z, Real.exp (-W z))) • g x =
        (∫ z, Real.exp (-W z))⁻¹ * (Real.exp (-W x) * g x)
      simp only [smul_eq_mul, div_eq_mul_inv]
      ring
    intro f hf
    rw [ht,ht,hi f hf]
    congr 1
    apply integral_congr_ae
    filter_upwards [] with x
    ring

  let smoothGradientGraph (μ : Measure E) : Submodule ℝ (Lp ℝ 2 μ × Lp E 2 μ) :=
    {
      carrier := {u | ∃ f : E → ℝ, ContDiff ℝ ∞ f ∧ HasCompactSupport f ∧
        u.1 =ᵐ[μ] f ∧ u.2 =ᵐ[μ] gradient f}
      zero_mem' := by
        refine ⟨0,contDiff_const,HasCompactSupport.zero,?_,?_⟩
        · exact Lp.coeFn_zero _ _ _
        · have hz : gradient (0 : E → ℝ) = (0 : E → E) := by
            funext x
            exact gradient_fun_const x (0 : ℝ)
          change (0 : Lp E 2 μ) =ᵐ[μ] gradient (0 : E → ℝ)
          rw [hz]
          exact Lp.coeFn_zero E 2 μ
      add_mem' := by
        rintro u v ⟨f,hf,hfc,hfu,hfg⟩ ⟨g,hg,hgc,hgu,hgg⟩
        refine ⟨f+g,hf.add hg,hfc.add hgc,?_,?_⟩
        · exact (Lp.coeFn_add u.1 v.1).trans (hfu.add hgu)
        have he : gradient (f+g) = gradient f + gradient g := by
          funext x
          simp only [gradient, fderiv_add (hf.differentiable (by simp) x)
            (hg.differentiable (by simp) x), map_add, Pi.add_apply]
        rw [he]
        exact (Lp.coeFn_add u.2 v.2).trans (hfg.add hgg)
      smul_mem' := by
        rintro a u ⟨f,hf,hfc,hfu,hfg⟩
        refine ⟨a • f,contDiff_const.smul hf,hfc.smul_left,?_,?_⟩
        · exact (Lp.coeFn_smul a u.1).trans (hfu.const_smul a)
        have he : gradient (a • f) = a • gradient f := by
          funext x
          simp only [gradient, fderiv_const_smul (hf.differentiable (by simp) x),
            map_smul, Pi.smul_apply]
        rw [he]
        exact (Lp.coeFn_smul a u.2).trans (hfg.const_smul a)
    }

  have closure_unique (W : E → ℝ) (hW : ContDiff ℝ 1 W)
      (hI : Integrable (fun x => Real.exp (-W x))) :
      let μ := (volume : Measure E).tilted (fun x => -W x)
      ∀ u ∈ (smoothGradientGraph μ).topologicalClosure, u.1 = 0 → u.2 = 0 := by
    let μ := (volume : Measure E).tilted (fun x => -W x)
    let : IsProbabilityMeasure μ := isProbabilityMeasure_tilted hI
    dsimp only
    intro u hu huz
    have hd : Dense {v : Lp E 2 μ | ∃ P : E → E,
        v =ᵐ[μ] P ∧ HasCompactSupport P ∧ ContDiff ℝ ∞ P} :=
      Lp.dense_hasCompactSupport_contDiff (by norm_num)
    have horth : ∀ v ∈ {v : Lp E 2 μ | ∃ P : E → E,
        v =ᵐ[μ] P ∧ HasCompactSupport P ∧ ContDiff ℝ ∞ P}, inner ℝ u.2 v = 0 := by
      rintro v ⟨P,hv,hPc,hP⟩
      obtain ⟨q,hq,hqc,hqL,hqi⟩ := tilted_vector_ibp W hW hI P (contDiff_infty.mp hP 1) hPc
      let qv : Lp ℝ 2 μ := hqL.toLp q
      have hc : IsClosed {z : Lp ℝ 2 μ × Lp E 2 μ |
          inner ℝ z.2 v = inner ℝ z.1 qv} :=
        isClosed_eq (continuous_snd.inner continuous_const) (continuous_fst.inner continuous_const)
      have hs : (smoothGradientGraph μ : Set (Lp ℝ 2 μ × Lp E 2 μ)) ⊆
          {z | inner ℝ z.2 v = inner ℝ z.1 qv} := by
        rintro z ⟨f,hf,hfc,hfz,hfg⟩
        change inner ℝ z.2 v = inner ℝ z.1 qv
        calc
          inner ℝ z.2 v = ∫ x, inner ℝ (gradient f x) (P x) ∂μ := by
            rw [L2.inner_def]
            apply integral_congr_ae
            filter_upwards [hfg,hv] with x hx hy
            rw [hx,hy]
          _ = ∫ x, f x * q x ∂μ := hqi f (contDiff_infty.mp hf 1)
          _ = inner ℝ z.1 qv := by
            rw [L2.inner_def]
            apply integral_congr_ae
            filter_upwards [hfz,hqL.coeFn_toLp] with x hx hy
            rw [hx,show qv x = q x from hy]
            simp [mul_comm]
      have he := (closure_minimal hs hc) hu
      change inner ℝ u.2 v = inner ℝ u.1 qv at he
      simpa [huz] using he
    have hall : ∀ v : Lp E 2 μ, inner ℝ u.2 v = 0 :=
      hd.induction horth (isClosed_eq (continuous_const.inner continuous_id) continuous_const)
    exact inner_self_eq_zero.mp (hall u.2)

  let μ := (volume : Measure E).tilted (fun x => -W x)
  let : IsProbabilityMeasure μ := isProbabilityMeasure_tilted hI
  let G := smoothGradientGraph μ
  have hu : ∀ z ∈ G.topologicalClosure, z.1 = 0 → z.2 = 0 := closure_unique W hW hI
  let D := G.toLinearPMap
  have hgraph : D.graph = G :=
    G.toLinearPMap_graph_eq (fun z hz hzero => hu z (subset_closure hz) hzero)
  have hc : D.IsClosable := by
    refine ⟨G.topologicalClosure.toLinearPMap,?_⟩
    rw [hgraph]
    exact (G.topologicalClosure.toLinearPMap_graph_eq hu).symm
  have hd : Dense {u : Lp ℝ 2 μ | ∃ f : E → ℝ,
      u =ᵐ[μ] f ∧ HasCompactSupport f ∧ ContDiff ℝ ∞ f} :=
    Lp.dense_hasCompactSupport_contDiff (by norm_num)
  have hD : Dense (D.domain : Set (Lp ℝ 2 μ)) := by
    apply hd.mono
    rintro u ⟨f,huf,hfc,hf⟩
    have hgf : MemLp (gradient f) 2 μ :=
      (gradient_cont f (contDiff_infty.mp hf 1)).memLp_of_hasCompactSupport (gradient_compact f hfc)
    change u ∈ G.map (LinearMap.fst ℝ (Lp ℝ 2 μ) (Lp E 2 μ))
    exact ⟨(u,hgf.toLp (gradient f)),⟨f,hf,hfc,huf,hgf.coeFn_toLp⟩,rfl⟩
  refine ⟨D,hD,hc,hc.closure_isClosed,?_⟩
  intro u v
  rw [hgraph]
  rfl

end AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.WeightedGradient
