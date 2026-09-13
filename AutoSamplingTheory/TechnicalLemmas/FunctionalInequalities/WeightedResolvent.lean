import AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.WeightedGradientDistribution
import AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.ClosedGraphResolvent

/-!
# Distributional equation for the actual closed-gradient resolvent

Euclidean analytic prerequisite toward PBPS arXiv:2609.06905v1 Appendix C.1.
Construct the weak solution using the same gradient closure, embed genuine
smooth compact tests in its domain, and remove only the normalization of the
Gibbs weight. No inverse-weighted test is assumed smooth. This is not H2
regularity, an operator core for D*D, conditional Poincare or a paper theorem.
-/

namespace AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.WeightedResolvent

open MeasureTheory InnerProductSpace
open scoped RealInnerProductSpace ContDiff Topology

/-- The genuine positive-epsilon resolvent has an ordinary weak gradient and
satisfies the weighted divergence-form equation, with all three test products
integrable for volume. The same partial operator is retained throughout. -/
theorem weak_resolvent_distributional {E : Type*}
    [NormedAddCommGroup E] [InnerProductSpace ℝ E] [FiniteDimensional ℝ E]
    [MeasurableSpace E] [BorelSpace E]
    (W : E → ℝ) (hW : ContDiff ℝ 1 W)
    (hI : Integrable (fun x => Real.exp (-W x))) :
    let μ := (volume : Measure E).tilted (fun x => -W x)
    ∀ (D : Lp ℝ 2 μ →ₗ.[ℝ] Lp E 2 μ), D.IsClosable →
      (∀ (a : Lp ℝ 2 μ) (H : Lp E 2 μ), (a,H) ∈ D.graph ↔
        ∃ φ : E → ℝ, ContDiff ℝ ∞ φ ∧ HasCompactSupport φ ∧
          a =ᵐ[μ] φ ∧ H =ᵐ[μ] gradient φ) →
      ∀ (ε : ℝ), 0 < ε → ∀ f : Lp ℝ 2 μ,
      ∃ u : D.closure.domain,
        (∀ v : D.closure.domain,
          ε * ⟪(u : Lp ℝ 2 μ), (v : Lp ℝ 2 μ)⟫ +
            ⟪D.closure u, D.closure v⟫ = ⟪f, (v : Lp ℝ 2 μ)⟫) ∧
        LocallyIntegrable (fun x => (u : Lp ℝ 2 μ) x) ∧
        LocallyIntegrable (fun x => D.closure u x) ∧
        (∀ ψ : E → ℝ, ContDiff ℝ 1 ψ → HasCompactSupport ψ → ∀ v : E,
          Integrable (fun x => ψ x * inner ℝ (D.closure u x) v) ∧
          Integrable (fun x => (u : Lp ℝ 2 μ) x * fderiv ℝ ψ x v) ∧
          (∫ x, ψ x * inner ℝ (D.closure u x) v) =
            - ∫ x, (u : Lp ℝ 2 μ) x * fderiv ℝ ψ x v) ∧
        ∀ ψ : E → ℝ, ContDiff ℝ ∞ ψ → HasCompactSupport ψ →
          Integrable (fun x => Real.exp (-W x) * ((u : Lp ℝ 2 μ) x * ψ x)) ∧
          Integrable (fun x => Real.exp (-W x) * inner ℝ (D.closure u x) (gradient ψ x)) ∧
          Integrable (fun x => Real.exp (-W x) * (f x * ψ x)) ∧
          ε * (∫ x, Real.exp (-W x) * ((u : Lp ℝ 2 μ) x * ψ x)) +
            (∫ x, Real.exp (-W x) * inner ℝ (D.closure u x) (gradient ψ x)) =
            ∫ x, Real.exp (-W x) * (f x * ψ x) := by
  let μ := (volume : Measure E).tilted (fun x => -W x)
  dsimp only
  intro D hD hgraph ε hε f
  let : IsProbabilityMeasure μ := isProbabilityMeasure_tilted hI
  obtain ⟨u,hu,_⟩ := ClosedGraphResolvent.weak_resolvent D.closure hD.closure_isClosed ε hε f
  obtain ⟨huL,hGL,hderiv⟩ := WeightedGradientDistribution.closed_gradient_distributional
    W hW hI D hD hgraph u (D.closure u) (D.closure.mem_graph u)
  refine ⟨u,hu,huL,hGL,hderiv,?_⟩
  intro ψ hψ hc
  have hgCont : Continuous (gradient ψ) :=
    (toDual ℝ E).symm.continuous.comp
      (((contDiff_infty.mp hψ 1).fderiv_right (m := 0) (by norm_num)).continuous)
  have hgComp : HasCompactSupport (gradient ψ) := by
    refine HasCompactSupport.of_support_subset_isCompact hc.isCompact ?_
    intro x hx
    by_contra hn
    exact hx (by simp [gradient, fderiv_of_notMem_tsupport ℝ hn])
  have hp : MemLp ψ 2 μ := hψ.continuous.memLp_of_hasCompactSupport hc
  have hg : MemLp (gradient ψ) 2 μ := hgCont.memLp_of_hasCompactSupport hgComp
  let p : Lp ℝ 2 μ := hp.toLp ψ
  let q : Lp E 2 μ := hg.toLp (gradient ψ)
  have hpq : (p,q) ∈ D.graph :=
    (hgraph p q).mpr ⟨ψ,hψ,hc,hp.coeFn_toLp,hg.coeFn_toLp⟩
  have hpqc : (p,q) ∈ D.closure.graph := by
    rw [← hD.graph_closure_eq_closure_graph]
    exact D.graph.le_topologicalClosure hpq
  obtain ⟨v,hv,hDv⟩ := D.closure.mem_graph_iff.mp hpqc
  have he := hu v
  rw [hv,hDv] at he
  have hpe (a : Lp ℝ 2 μ) :
      (fun x => inner ℝ (a x) (p x)) =ᵐ[μ] (fun x => a x * ψ x) := by
    filter_upwards [hp.coeFn_toLp] with x hx
    rw [show p x = ψ x from hx]
    simp [mul_comm]
  have hge :
      (fun x => inner ℝ (D.closure u x) (q x)) =ᵐ[μ]
        (fun x => inner ℝ (D.closure u x) (gradient ψ x)) := by
    filter_upwards [hg.coeFn_toLp] with x hx
    rw [show q x = gradient ψ x from hx]
  have hiu := (L2.integrable_inner (𝕜 := ℝ) (u : Lp ℝ 2 μ) p).congr (hpe u)
  have hiG := (L2.integrable_inner (𝕜 := ℝ) (D.closure u) q).congr hge
  have hif := (L2.integrable_inner (𝕜 := ℝ) f p).congr (hpe f)
  have hwu := (integrable_tilted_iff hI _).mp hiu
  have hwG := (integrable_tilted_iff hI _).mp hiG
  have hwf := (integrable_tilted_iff hI _).mp hif
  simp only [smul_eq_mul] at hwu hwG hwf
  refine ⟨hwu,hwG,hwf,?_⟩
  rw [L2.inner_def, L2.inner_def, L2.inner_def,
    integral_congr_ae (hpe u), integral_congr_ae hge,
    integral_congr_ae (hpe f)] at he
  have ht (g : E → ℝ) : (∫ x, g x ∂μ) =
      (∫ x, Real.exp (-W x))⁻¹ * ∫ x, Real.exp (-W x) * g x := by
    rw [show μ = (volume : Measure E).tilted (fun x => -W x) from rfl, integral_tilted]
    rw [← integral_const_mul]
    apply integral_congr_ae
    filter_upwards [] with x
    change (Real.exp (-W x) / (∫ z, Real.exp (-W z))) • g x = _
    simp only [smul_eq_mul, div_eq_mul_inv]
    ring
  rw [ht,ht,ht] at he
  apply mul_left_cancel₀ (inv_ne_zero (integral_exp_pos hI).ne')
  convert he using 1
  ring

end AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.WeightedResolvent
