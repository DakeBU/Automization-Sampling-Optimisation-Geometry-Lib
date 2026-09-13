import AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.WeightedGradient

/-!
# Weighted test identity on the actual gradient graph closure

Direct full-space analytic prerequisite to PBPS arXiv:2609.06905v1 Appendix C.1.
The same partial gradient operator used by the conditional weak resolvent is
retained. No classical derivatives of arbitrary L2 representatives are asserted.
This is not unweighted distributional regularity, an operator core of D*D,
Poincare, or the compact-manifold spectral theory in arXiv:1310.2526v7 section 2.5.
-/

namespace AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.WeightedGradientWeak

open MeasureTheory InnerProductSpace
open scoped RealInnerProductSpace ContDiff Topology

variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
  [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]

-- Adapt the inaccessible local helper in WeightedGradient, keeping its C1 scope.
private theorem compact_directional_ibp (W f φ : E → ℝ)
    (hW : ContDiff ℝ 1 W) (hf : ContDiff ℝ 1 f) (hφ : ContDiff ℝ 1 φ)
    (hc : HasCompactSupport φ) (v : E) :
    (∫ x, Real.exp (-W x) * φ x * fderiv ℝ f x v) =
      - ∫ x, Real.exp (-W x) *
        (fderiv ℝ φ x v - φ x * fderiv ℝ W x v) * f x := by
  let F := fun x => Real.exp (-W x) * φ x
  have hF : ContDiff ℝ 1 F := hW.neg.exp.mul hφ
  have hFc : HasCompactSupport F := hc.mul_left
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
    (hφ.differentiable one_ne_zero x).hasFDerivAt
  have he : fderiv ℝ F x v = Real.exp (-W x) *
      (fderiv ℝ φ x v - φ x * fderiv ℝ W x v) := by
    rw [show fderiv ℝ F x = _ from hd.fderiv]
    simp only [add_apply, smul_apply, neg_apply, smul_eq_mul, Pi.neg_apply]
    ring
  rw [he]

/-- Every member of the same closed gradient graph satisfies weighted compact
test integration by parts, with both integrands genuinely integrable. The exact
original graph is the already constructed smooth core, not an assumed IBP law. -/
theorem closed_gradient_weighted_ibp (W : E → ℝ) (hW : ContDiff ℝ 1 W)
    (hI : Integrable (fun x => Real.exp (-W x))) :
    let μ := (volume : Measure E).tilted (fun x => -W x)
    ∀ (D : Lp ℝ 2 μ →ₗ.[ℝ] Lp E 2 μ), D.IsClosable →
      (∀ (u : Lp ℝ 2 μ) (G : Lp E 2 μ), (u,G) ∈ D.graph ↔
        ∃ f : E → ℝ, ContDiff ℝ ∞ f ∧ HasCompactSupport f ∧
          u =ᵐ[μ] f ∧ G =ᵐ[μ] gradient f) →
      ∀ (u : Lp ℝ 2 μ) (G : Lp E 2 μ), (u,G) ∈ D.closure.graph →
      ∀ (φ : E → ℝ), ContDiff ℝ 1 φ → HasCompactSupport φ → ∀ v : E,
        Integrable (fun x => φ x * inner ℝ (G x) v) μ ∧
        Integrable (fun x => u x * (fderiv ℝ φ x v - φ x * fderiv ℝ W x v)) μ ∧
        (∫ x, φ x * inner ℝ (G x) v ∂μ) =
          - ∫ x, u x * (fderiv ℝ φ x v - φ x * fderiv ℝ W x v) ∂μ := by
  let μ := (volume : Measure E).tilted (fun x => -W x)
  let : IsProbabilityMeasure μ := isProbabilityMeasure_tilted hI
  dsimp only
  intro D hD hgraph u G hu φ hφ hc v
  let P := fun x => φ x • v
  let q := fun x => fderiv ℝ φ x v - φ x * fderiv ℝ W x v
  have hP : Continuous P := hφ.continuous.smul continuous_const
  have hPc : HasCompactSupport P := hc.smul_right
  have hdφ : Continuous (fun x => fderiv ℝ φ x v) :=
    (hφ.fderiv_right (m := 0) (by norm_num)).continuous.clm_apply continuous_const
  have hdW : Continuous (fun x => fderiv ℝ W x v) :=
    (hW.fderiv_right (m := 0) (by norm_num)).continuous.clm_apply continuous_const
  have hdc : HasCompactSupport (fun x => fderiv ℝ φ x v) := by
    refine HasCompactSupport.of_support_subset_isCompact hc.isCompact ?_
    intro x hx
    by_contra hn
    exact hx (by simp [fderiv_of_notMem_tsupport ℝ hn])
  have hq : Continuous q := hdφ.sub (hφ.continuous.mul hdW)
  have hqc : HasCompactSupport q := hdc.sub hc.mul_right
  have hPL : MemLp P 2 μ := hP.memLp_of_hasCompactSupport hPc
  have hqL : MemLp q 2 μ := hq.memLp_of_hasCompactSupport hqc
  let pv : Lp E 2 μ := hPL.toLp P
  let qv : Lp ℝ 2 μ := hqL.toLp q
  have hPe (H : Lp E 2 μ) :
      (fun x => inner ℝ (H x) (pv x)) =ᵐ[μ] (fun x => φ x * inner ℝ (H x) v) := by
    filter_upwards [hPL.coeFn_toLp] with x hx
    rw [show pv x = P x from hx]
    simp [P, inner_smul_right]
  have hqe (a : Lp ℝ 2 μ) :
      (fun x => inner ℝ (a x) (qv x)) =ᵐ[μ] (fun x => a x * q x) := by
    filter_upwards [hqL.coeFn_toLp] with x hx
    rw [show qv x = q x from hx]
    simp [mul_comm]
  refine ⟨(L2.integrable_inner (𝕜 := ℝ) G pv).congr (hPe G),
    (L2.integrable_inner (𝕜 := ℝ) u qv).congr (hqe u), ?_⟩
  have ht (g : E → ℝ) : (∫ x, g x ∂μ) =
      (∫ x, Real.exp (-W x))⁻¹ * ∫ x, Real.exp (-W x) * g x := by
    rw [show μ = (volume : Measure E).tilted (fun x => -W x) from rfl, integral_tilted]
    rw [← integral_const_mul]
    apply integral_congr_ae
    filter_upwards [] with x
    change (Real.exp (-W x) / (∫ z, Real.exp (-W z))) • g x = _
    simp only [smul_eq_mul, div_eq_mul_inv]
    ring
  have hclosed : IsClosed {z : Lp ℝ 2 μ × Lp E 2 μ |
      inner ℝ z.2 pv = -inner ℝ z.1 qv} :=
    isClosed_eq (continuous_snd.inner continuous_const)
      (continuous_fst.inner continuous_const).neg
  have hsub : (D.graph : Set (Lp ℝ 2 μ × Lp E 2 μ)) ⊆
      {z | inner ℝ z.2 pv = -inner ℝ z.1 qv} := by
    rintro ⟨a,H⟩ hz
    obtain ⟨f,hf,hfc,ha,hH⟩ := (hgraph a H).mp hz
    change inner ℝ H pv = -inner ℝ a qv
    rw [L2.inner_def, L2.inner_def, integral_congr_ae (hPe H), integral_congr_ae (hqe a)]
    have hff := contDiff_infty.mp hf 1
    have hleft : (∫ x, φ x * inner ℝ (H x) v ∂μ) =
        ∫ x, φ x * fderiv ℝ f x v ∂μ := by
      apply integral_congr_ae
      filter_upwards [hH] with x hx
      rw [hx, AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Gradient.fderiv_apply_eq_inner_gradient_of_differentiableAt
        (hff.differentiable one_ne_zero x)]
    have hright : (∫ x, a x * q x ∂μ) = ∫ x, f x * q x ∂μ :=
      integral_congr_ae (ha.mul (Filter.EventuallyEq.refl _ _))
    rw [hleft, hright, ht, ht]
    have hi := compact_directional_ibp W f φ hW hff hφ hc v
    simp_rw [← mul_assoc] at ⊢
    rw [hi]
    simp only [mul_neg]
    congr 1
    congr 1
    apply integral_congr_ae
    filter_upwards [] with x
    dsimp [q]
    ring
  have hmem : (u,G) ∈ D.graph.topologicalClosure := by
    rwa [hD.graph_closure_eq_closure_graph]
  have he := (closure_minimal hsub hclosed) hmem
  change inner ℝ G pv = -inner ℝ u qv at he
  rw [L2.inner_def, L2.inner_def, integral_congr_ae (hPe G), integral_congr_ae (hqe u)] at he
  exact he

end AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.WeightedGradientWeak
