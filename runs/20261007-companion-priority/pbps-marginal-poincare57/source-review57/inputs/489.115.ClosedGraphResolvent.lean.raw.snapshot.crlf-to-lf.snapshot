import Mathlib.Analysis.InnerProductSpace.Projection.Basic
import Mathlib.Analysis.InnerProductSpace.ProdL2
import Mathlib.Topology.Algebra.Module.LinearPMap

/-!
# Epsilon weak resolvent from a closed graph

An abstract Hilbert-space prerequisite for the full-space weighted Poisson route
used toward PBPS arXiv:2609.06905v1 Appendix C.1. The Poisson/Sobolev background
in Kolesnikov-Milman arXiv:1310.2526v7 sections 2.4-2.5 concerns compact
manifolds; this result asserts only a directly constructed weak equation.
It proves no classical elliptic regularity, generator core or Poincare bound.
The operator may be unbounded and its domain need not be dense.
-/

namespace AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.ClosedGraphResolvent

open scoped RealInnerProductSpace

/-- Orthogonal projection onto the scaled closed graph constructs the unique
weak solution. Norms of domain elements below are their ambient H norms;
the explicit bounds depend on epsilon and do not persist uniformly as it
approaches zero. -/
theorem weak_resolvent {H K : Type*}
    [NormedAddCommGroup H] [InnerProductSpace ℝ H] [CompleteSpace H]
    [NormedAddCommGroup K] [InnerProductSpace ℝ K] [CompleteSpace K]
    (A : H →ₗ.[ℝ] K) (hA : A.IsClosed) (ε : ℝ) (hε : 0 < ε) (f : H) :
    ∃ u : A.domain,
      (∀ v : A.domain, ε * ⟪(u : H), (v : H)⟫ + ⟪A u, A v⟫ = ⟪f, (v : H)⟫) ∧
      ε * ‖(u : H)‖^2 + ‖A u‖^2 = ⟪f, (u : H)⟫ ∧
      ‖(u : H)‖ ≤ ε⁻¹ * ‖f‖ ∧
      ε * ‖(u : H)‖^2 + ‖A u‖^2 ≤ ε⁻¹ * ‖f‖^2 ∧
      ∀ w : A.domain,
        (∀ v : A.domain, ε * ⟪(w : H), (v : H)⟫ + ⟪A w, A v⟫ = ⟪f, (v : H)⟫) → w = u := by
  have hex : ∃ u : A.domain, ∀ v : A.domain,
      ε * ⟪(u : H), (v : H)⟫ + ⟪A u, A v⟫ = ⟪f, (v : H)⟫ := by
    let s := Real.sqrt ε
    have hs : 0 < s := Real.sqrt_pos.2 hε
    have hs0 : s ≠ 0 := ne_of_gt hs
    have hss : s * s = ε := Real.mul_self_sqrt hε.le
    let T : WithLp 2 (H × K) →L[ℝ] H × K :=
      (s⁻¹ • (WithLp.fstL 2 ℝ H K)).prod (WithLp.sndL 2 ℝ H K)
    let G : Submodule ℝ (WithLp 2 (H × K)) := A.graph.comap T.toLinearMap
    have hG : IsClosed (G : Set (WithLp 2 (H × K))) := hA.preimage T.continuous
    let : CompleteSpace G := hG.completeSpace_coe
    let z : WithLp 2 (H × K) := WithLp.toLp 2 (s⁻¹ • f, 0)
    let p := G.starProjection z
    have hp : T p ∈ A.graph := G.starProjection_apply_mem z
    obtain ⟨u,hu,hAu⟩ := A.mem_graph_iff.mp hp
    have hu' : s • (u : H) = p.fst := by
      rw [hu]
      change s • (s⁻¹ • p.fst) = p.fst
      simp [smul_smul, hs0]
    refine ⟨u, ?_⟩
    intro v
    let w : WithLp 2 (H × K) := WithLp.toLp 2 (s • (v : H), A v)
    have hw : w ∈ G := by
      change T w ∈ A.graph
      apply A.mem_graph_iff.mpr
      refine ⟨v, ?_, ?_⟩
      · change (v : H) = s⁻¹ • (s • (v : H))
        simp [smul_smul, hs0]
      · rfl
    have ho := G.starProjection_inner_eq_zero z w hw
    change ⟪s⁻¹ • f - p.fst, s • (v : H)⟫ + ⟪(0 : K) - p.snd, A v⟫ = 0 at ho
    have hAu' : A u = p.snd := hAu
    rw [← hu', ← hAu'] at ho
    simp only [inner_sub_left, real_inner_smul_left, real_inner_smul_right, zero_sub,
      inner_neg_left] at ho
    simp only [← mul_assoc, mul_inv_cancel₀ hs0, hss, one_mul] at ho
    linarith
  obtain ⟨u,hu⟩ := hex
  have he : ε * ‖(u : H)‖^2 + ‖A u‖^2 = ⟪f, (u : H)⟫ := by
    simpa only [real_inner_self_eq_norm_sq] using hu u
  have hn : ε * ‖(u : H)‖ ≤ ‖f‖ := by
    have hcs := real_inner_le_norm f (u : H)
    by_cases hz : ‖(u : H)‖ = 0
    · simp [hz]
    · have hp : 0 < ‖(u : H)‖ := lt_of_le_of_ne (norm_nonneg _) (Ne.symm hz)
      nlinarith [sq_nonneg ‖A u‖]
  have hb : ‖(u : H)‖ ≤ ε⁻¹ * ‖f‖ := by
    have hn' : ‖(u : H)‖ ≤ ‖f‖ / ε := (le_div_iff₀ hε).2 (by simpa [mul_comm] using hn)
    simpa [div_eq_mul_inv, mul_comm] using hn'
  have heb : ε * ‖(u : H)‖^2 + ‖A u‖^2 ≤ ε⁻¹ * ‖f‖^2 := by
    rw [he]
    calc
      ⟪f, (u : H)⟫ ≤ ‖f‖ * ‖(u : H)‖ := real_inner_le_norm _ _
      _ ≤ ‖f‖ * (ε⁻¹ * ‖f‖) := mul_le_mul_of_nonneg_left hb (norm_nonneg _)
      _ = _ := by ring
  refine ⟨u,hu,he,hb,heb,?_⟩
  intro w hw
  let d : A.domain := w-u
  have hd : ε * ⟪(d : H), (d : H)⟫ + ⟪A d, A d⟫ = 0 := by
    have heq := sub_eq_zero.mpr ((hw d).trans (hu d).symm)
    have hAd : A d = A w - A u := A.toFun.map_sub w u
    rw [hAd, inner_sub_left]
    change ε * ⟪(w : H) - (u : H), (d : H)⟫ + _ = 0
    rw [inner_sub_left]
    rw [hAd] at heq
    nlinarith
  rw [real_inner_self_eq_norm_sq, real_inner_self_eq_norm_sq] at hd
  have hz : ‖(d : H)‖ = 0 := by
    by_contra hz
    have hp : 0 < ‖(d : H)‖ := lt_of_le_of_ne (norm_nonneg _) (Ne.symm hz)
    have hpos := mul_pos hε (sq_pos_of_pos hp)
    nlinarith [sq_nonneg ‖A d‖]
  apply Subtype.ext
  exact sub_eq_zero.mp (norm_eq_zero.mp hz)

end AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.ClosedGraphResolvent
