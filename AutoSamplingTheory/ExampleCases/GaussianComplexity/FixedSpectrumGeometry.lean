import AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumFirstOrder
import AutoSamplingTheory.TechnicalLemmas.Analysis.StrongConvexGradientConverse
import Mathlib.Analysis.Calculus.ContDiff.Operations
import Mathlib.Analysis.InnerProductSpace.Rayleigh

open Matrix InnerProductSpace
open scoped ContDiff
set_option autoImplicit false

/-!
# Actual fixed-spectrum potential geometry

Zhou--Suzuki arXiv:2610.20492v1, Eq.(11) and Appendix C.4.
The literal potential is globally smooth, with genuine constant Euclidean
Hessian, source strong-convexity/smoothness constants and unique minimizer0.

The implementation reuses the canonical actual precision bounds and actual
first-order identity. Strong convexity uses the existing quantitative-gradient
converse; the source author's Hessian route remains separately represented in
the source proof graph. The operator-norm estimate is a Euclidean Rayleigh
quotient bound, not an entrywise matrix norm. This declaration does not prove
an adaptive algorithm, query cap, TV/precision/cost transport or main lower bound.
-/

namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumGeometry

theorem actual_potential_geometry {d : ℕ} (hd : 2 ≤ d)
    {κ : ℝ} (hκ : 2 ≤ κ)
    (O : Matrix.orthogonalGroup (Fin d) ℝ) :
  let θ : Fin d → ℝ := fun i => ((i.val : ℝ) + 1 / 2) * Real.pi / (d : ℝ)
  let A : Matrix (Fin d) (Fin d) ℝ :=
    (O : Matrix (Fin d) (Fin d) ℝ) *
      Matrix.diagonal (fun i => (κ + 1) / 2 + (κ - 1) / 2 * Real.cos (θ i)) *
      (O : Matrix (Fin d) (Fin d) ℝ).transpose
  let f : EuclideanSpace ℝ (Fin d) → ℝ := fun x =>
    (WithLp.ofLp x) ⬝ᵥ (A *ᵥ WithLp.ofLp x) / 2
  ContDiff ℝ ∞ f ∧
    (∀ x : EuclideanSpace ℝ (Fin d),
      HasFDerivAt (gradient f) (Matrix.toEuclideanCLM (𝕜 := ℝ) (n := Fin d) A) x) ∧
    StrongConvexOn (Set.univ : Set (EuclideanSpace ℝ (Fin d))) 1 f ∧
    (∀ x y : EuclideanSpace ℝ (Fin d),
      ‖gradient f x - gradient f y‖ ≤ κ * ‖x - y‖) ∧
    f 0 = 0 ∧
    (∀ x : EuclideanSpace ℝ (Fin d), IsMinOn f Set.univ x ↔ x = 0) := by
  classical
  dsimp only
  let θ : Fin d → ℝ := fun i => ((i.val : ℝ) + 1 / 2) * Real.pi / (d : ℝ)
  let A : Matrix (Fin d) (Fin d) ℝ :=
    (O : Matrix (Fin d) (Fin d) ℝ) *
      Matrix.diagonal (fun i => (κ + 1) / 2 + (κ - 1) / 2 * Real.cos (θ i)) *
      (O : Matrix (Fin d) (Fin d) ℝ).transpose
  let E := EuclideanSpace ℝ (Fin d)
  let f : E → ℝ := fun x => (WithLp.ofLp x) ⬝ᵥ (A *ᵥ WithLp.ofLp x) / 2
  let H : E →L[ℝ] E := Matrix.toEuclideanCLM (𝕜 := ℝ) (n := Fin d) A
  have hA : A.PosDef ∧ (A - 1).PosSemidef ∧
      (κ • (1 : Matrix (Fin d) (Fin d) ℝ) - A).PosSemidef :=
    FixedSpectrumAdmissibility.actual_precision_admissible hd hκ O
  have hself : IsSelfAdjoint A := hA.1.1
  have hH : H.IsSymmetric :=
    ContinuousLinearMap.isSelfAdjoint_iff_isSymmetric.mp
      (hself.map (Matrix.toEuclideanCLM (𝕜 := ℝ) (n := Fin d)))
  have hf : f = fun y : E => (1 / 2 : ℝ) * inner ℝ y (H y) := by
    funext y
    dsimp only [f]
    rw [show inner ℝ y (H y) = (WithLp.ofLp y) ⬝ᵥ (A *ᵥ WithLp.ofLp y) from
      Matrix.inner_toEuclideanCLM A y y]
    ring
  have hgrad (x : E) : HasGradientAt f (H x) x :=
    (FixedSpectrumFirstOrder.actual_first_order_query hd hκ O x).1
  have hg : gradient f = fun x : E => H x := funext fun x => (hgrad x).gradient
  have hcinfty : ContDiff ℝ ∞ f := by
    rw [hf]
    have hi : ContDiff ℝ ∞ (fun y : E => inner ℝ y (H y)) :=
      contDiff_id.inner ℝ H.contDiff
    exact (contDiff_const : ContDiff ℝ ∞ (fun _ : E => (1 / 2 : ℝ))).mul hi
  have hhessian (x : E) : HasFDerivAt (gradient f) H x := by
    rw [hg]
    exact H.hasFDerivAt
  have hquad (M : Matrix (Fin d) (Fin d) ℝ) (hM : M.PosSemidef) (x : E) :
      0 ≤ inner ℝ x (Matrix.toEuclideanCLM (𝕜 := ℝ) (n := Fin d) M x) := by
    rw [Matrix.inner_toEuclideanCLM]
    simpa only [star_trivial] using hM.dotProduct_mulVec_nonneg (WithLp.ofLp x)
  have hlower (x : E) : ‖x‖ ^ 2 ≤ inner ℝ x (H x) := by
    have h := hquad (A - 1) hA.2.1 x
    rw [map_sub, map_one] at h
    simp only [_root_.sub_apply, one_apply_eq_self,
      inner_sub_right, real_inner_self_eq_norm_sq] at h
    change 0 ≤ inner ℝ x (H x) - ‖x‖ ^ 2 at h
    linarith
  have hupper (x : E) : inner ℝ x (H x) ≤ κ * ‖x‖ ^ 2 := by
    have h := hquad (κ • (1 : Matrix (Fin d) (Fin d) ℝ) - A) hA.2.2 x
    rw [map_sub, map_smul, map_one] at h
    simp only [_root_.sub_apply, _root_.smul_apply,
      one_apply_eq_self, inner_sub_right, inner_smul_right,
      real_inner_self_eq_norm_sq] at h
    change 0 ≤ κ * ‖x‖ ^ 2 - inner ℝ x (H x) at h
    linarith
  have hκ0 : 0 ≤ κ := le_trans (by norm_num) hκ
  have hnorm : ‖H‖ ≤ κ := by
    rw [H.norm_eq_iSup_rayleighQuotient hH]
    apply ciSup_le
    intro x
    change |inner ℝ (H x) x / ‖x‖ ^ 2| ≤ κ
    rw [real_inner_comm x (H x)]
    have hnonneg : 0 ≤ inner ℝ x (H x) := le_trans (sq_nonneg _) (hlower x)
    rw [abs_of_nonneg (div_nonneg hnonneg (sq_nonneg _))]
    by_cases hx : x = 0
    · simpa [hx] using hκ0
    · exact (div_le_iff₀ (sq_pos_of_pos (norm_pos_iff.mpr hx))).2 (hupper x)
  have hstrong : StrongConvexOn (Set.univ : Set E) 1 f := by
    apply AutoSamplingTheory.TechnicalLemmas.Analysis.StrongConvexGradientConverse.strongConvexOn_of_gradient_inner_lower_bound
      convex_univ (fun x _ => hgrad x)
    intro x _ y _
    simp only [one_mul]
    change ‖y - x‖ ^ 2 ≤ inner ℝ (H y - H x) (y - x)
    rw [← H.map_sub, real_inner_comm]
    exact hlower (y - x)
  have hsmooth (x y : E) : ‖gradient f x - gradient f y‖ ≤ κ * ‖x - y‖ := by
    rw [hg, ← H.map_sub]
    exact (H.le_opNorm (x - y)).trans
      (mul_le_mul_of_nonneg_right hnorm (norm_nonneg _))
  have hzero : f 0 = 0 := by simp [f]
  have hnonneg (x : E) : 0 ≤ f x := by
    rw [hf]
    nlinarith [hlower x, sq_nonneg ‖x‖]
  have hpositive (x : E) (hx : x ≠ 0) : 0 < f x := by
    rw [hf]
    nlinarith [hlower x, sq_pos_of_pos (norm_pos_iff.mpr hx)]
  refine ⟨hcinfty, hhessian, hstrong, hsmooth, hzero, ?_⟩
  intro x
  constructor
  · intro hmin
    by_contra hx
    have hle : f x ≤ f 0 := (isMinOn_iff.mp hmin) 0 (Set.mem_univ _)
    rw [hzero] at hle
    exact (not_le_of_gt (hpositive x hx)) hle
  · rintro rfl
    apply isMinOn_iff.mpr
    intro y _
    change f 0 ≤ f y
    rw [hzero]
    exact hnonneg y

end AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumGeometry
