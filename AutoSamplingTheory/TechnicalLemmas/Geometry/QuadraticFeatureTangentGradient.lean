import Mathlib.Analysis.InnerProductSpace.Adjoint
import Mathlib.Analysis.Calculus.FDeriv.Mul
import Mathlib.Analysis.InnerProductSpace.Calculus
import Mathlib.Tactic

open scoped InnerProductSpace Topology

namespace AutoSamplingTheory.TechnicalLemmas.Geometry.QuadraticFeatureTangentGradient

private def P {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    (w z : E) : E := z - ⟪z,w⟫_ℝ • w

private theorem P_sub {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    (w z y : E) : P w (z-y) = P w z - P w y := by
  simp only [P,inner_sub_left,sub_smul]
  abel

private theorem P_norm_le {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    (w z : E) (hw : ‖w‖ = 1) : ‖P w z‖ ≤ ‖z‖ := by
  have hsq : ‖P w z‖^2 = ‖z‖^2 - ⟪z,w⟫_ℝ^2 := by
    simp only [P,norm_sub_sq_real,inner_smul_right,norm_smul,hw,mul_one,
      Real.norm_eq_abs,sq_abs]
    ring
  nlinarith [sq_nonneg ⟪z,w⟫_ℝ,norm_nonneg (P w z),norm_nonneg z]

private theorem P_point_lip {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    (w u z : E) (hw : ‖w‖ = 1) (hu : ‖u‖ = 1) :
    ‖P w z-P u z‖ ≤ 2 * ‖z‖ * ‖w-u‖ := by
  have he : P w z-P u z = ⟪z,u⟫_ℝ • (u-w) + ⟪z,u-w⟫_ℝ • w := by
    simp only [P,inner_sub_right,smul_sub,sub_smul]
    abel
  rw [he]
  calc
    ‖⟪z,u⟫_ℝ • (u-w) + ⟪z,u-w⟫_ℝ • w‖ ≤
        ‖⟪z,u⟫_ℝ • (u-w)‖ + ‖⟪z,u-w⟫_ℝ • w‖ := norm_add_le _ _
    _ = ‖⟪z,u⟫_ℝ‖ * ‖u-w‖ + ‖⟪z,u-w⟫_ℝ‖ * ‖w‖ := by simp only [norm_smul]
    _ ≤ (‖z‖*‖u‖)*‖u-w‖ + (‖z‖*‖u-w‖)*‖w‖ := by
      gcongr <;> exact norm_inner_le_norm _ _
    _ = 2 * ‖z‖ * ‖w-u‖ := by rw [hw,hu,norm_sub_rev u w];ring

theorem quadratic_feature_potential_tangent_gradient
    {E H : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E] [CompleteSpace E]
    [NormedAddCommGroup H] [InnerProductSpace ℝ H] [CompleteSpace H]
    (F : E → H) (D : E → E →L[ℝ] H)
    (hF : ∀ w, HasFDerivAt F (D w) w)
    (M₁ M₂ : ℝ) (hM₁ : 0 ≤ M₁) (hM₂ : 0 ≤ M₂)
    (hBound : ∀ w : E, ‖w‖ ≤ 1 → ‖D w‖ ≤ M₁)
    (hLip : ∀ w u : E, ‖w‖ ≤ 1 → ‖u‖ ≤ 1 → ‖D w-D u‖ ≤ M₂*‖w-u‖) :
    let V : H → E → ℝ := fun r w => 2 * ⟪r,F w⟫_ℝ
    let G : H → E → E := fun r w =>
      (2 : ℝ) • ((D w).adjoint r - ⟪(D w).adjoint r,w⟫_ℝ • w)
    (∀ r w, HasFDerivAt (V r) ((2 : ℝ) • innerSL ℝ ((D w).adjoint r)) w) ∧
    (∀ r w, ‖w‖ = 1 →
      ⟪w,G r w⟫_ℝ = 0 ∧
      (∀ v, ⟪w,v⟫_ℝ = 0 → ⟪G r w,v⟫_ℝ = 2 * ⟪r,D w v⟫_ℝ) ∧
      ‖G r w‖ ≤ 2 * M₁ * ‖r‖) ∧
    ∀ r q w u, ‖w‖ = 1 → ‖u‖ = 1 →
      ‖G r w-G q u‖ ≤ 2 * M₁ * ‖r-q‖ +
        2 * (M₂+2*M₁) * ‖q‖ * ‖w-u‖ := by
  dsimp only
  have hAdj (w : E) (hw : ‖w‖ ≤ 1) (r : H) :
      ‖(D w).adjoint r‖ ≤ M₁ * ‖r‖ := by
    have h := (D w).adjoint.le_opNorm r
    rw [ContinuousLinearMap.adjoint.norm_map] at h
    exact h.trans (mul_le_mul_of_nonneg_right (hBound w hw) (norm_nonneg _))
  have hAdjDiff (w u : E) (hw : ‖w‖ ≤ 1) (hu : ‖u‖ ≤ 1) (q : H) :
      ‖((D w).adjoint-(D u).adjoint) q‖ ≤ (M₂*‖w-u‖)*‖q‖ := by
    have h := ((D w).adjoint-(D u).adjoint).le_opNorm q
    rw [← map_sub,ContinuousLinearMap.adjoint.norm_map] at h
    simpa only [map_sub] using h.trans (mul_le_mul_of_nonneg_right (hLip w u hw hu) (norm_nonneg _))
  have hFixed (q : H) (w u : E) (hw : ‖w‖ = 1) (hu : ‖u‖ = 1) :
      ‖P w ((D w).adjoint q) - P u ((D u).adjoint q)‖ ≤
        (M₂+2*M₁) * ‖q‖ * ‖w-u‖ := by
    have he : P w ((D w).adjoint q) - P u ((D u).adjoint q) =
        P w (((D w).adjoint-(D u).adjoint) q) +
          (P w ((D u).adjoint q) - P u ((D u).adjoint q)) := by
      rw [ContinuousLinearMap.sub_apply,P_sub]
      abel
    rw [he]
    calc
      ‖P w (((D w).adjoint-(D u).adjoint) q) +
          (P w ((D u).adjoint q) - P u ((D u).adjoint q))‖ ≤
        ‖P w (((D w).adjoint-(D u).adjoint) q)‖ +
          ‖P w ((D u).adjoint q) - P u ((D u).adjoint q)‖ := norm_add_le _ _
      _ ≤ ‖((D w).adjoint-(D u).adjoint) q‖ + 2 * ‖(D u).adjoint q‖ * ‖w-u‖ :=
        add_le_add (P_norm_le _ _ hw) (P_point_lip _ _ _ hw hu)
      _ ≤ (M₂*‖w-u‖)*‖q‖ + 2 * (M₁*‖q‖) * ‖w-u‖ := by
        gcongr
        · exact hAdjDiff w u hw.le hu.le q
        · exact hAdj u hu.le q
      _ = (M₂+2*M₁)*‖q‖*‖w-u‖ := by ring
  refine ⟨?_,?_,?_⟩
  · intro r w
    have he : (innerSL ℝ r).comp (D w) = innerSL ℝ ((D w).adjoint r) := by
      ext v
      simpa only [ContinuousLinearMap.comp_apply,innerSL_apply_apply] using
        ((D w).adjoint_inner_left v r).symm
    have h := (innerSL ℝ r).hasFDerivAt.comp w (hF w)
    rw [he] at h
    convert h.const_smul (2 : ℝ) using 1 <;>
      (first | rfl | (ext q; simp [Pi.smul_apply,smul_eq_mul,innerSL_apply_apply]))
  · intro r w hw
    refine ⟨?_,?_,?_⟩
    · simp only [inner_smul_right,inner_sub_right,inner_smul_right,real_inner_self_eq_norm_sq,hw]
      rw [real_inner_comm w ((D w).adjoint r)]
      ring
    · intro v hv
      simp only [real_inner_smul_left,inner_sub_left,real_inner_smul_left,hv,mul_zero,
        sub_zero,ContinuousLinearMap.adjoint_inner_left]
    · change ‖(2 : ℝ) • P w ((D w).adjoint r)‖ ≤ _
      rw [norm_smul,Real.norm_of_nonneg (by norm_num : (0:ℝ) ≤ 2)]
      exact (mul_le_mul_of_nonneg_left ((P_norm_le _ _ hw).trans (hAdj w hw.le r))
        (by norm_num : (0:ℝ) ≤ 2)).trans_eq (by ring)
  · intro r q w u hw hu
    change ‖(2 : ℝ) • P w ((D w).adjoint r) - (2 : ℝ) • P u ((D u).adjoint q)‖ ≤ _
    rw [← smul_sub,norm_smul,Real.norm_of_nonneg (by norm_num : (0:ℝ) ≤ 2)]
    have he : P w ((D w).adjoint r) - P u ((D u).adjoint q) =
        P w ((D w).adjoint (r-q)) +
          (P w ((D w).adjoint q) - P u ((D u).adjoint q)) := by
      rw [map_sub,P_sub]
      abel
    have hn : ‖P w ((D w).adjoint r) - P u ((D u).adjoint q)‖ ≤
        M₁*‖r-q‖ + (M₂+2*M₁)*‖q‖*‖w-u‖ := by
      rw [he]
      exact (norm_add_le _ _).trans (add_le_add
        ((P_norm_le _ _ hw).trans (hAdj w hw.le (r-q))) (hFixed q w u hw hu))
    exact (mul_le_mul_of_nonneg_left hn (by norm_num : (0:ℝ) ≤ 2)).trans_eq (by ring)

end AutoSamplingTheory.TechnicalLemmas.Geometry.QuadraticFeatureTangentGradient
