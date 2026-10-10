import AutoSamplingTheory.TechnicalLemmas.Analysis.HessianStrongConvexity
import Mathlib.Analysis.Calculus.FDeriv.Symmetric
import Mathlib.Analysis.Calculus.Gradient.Basic
import Mathlib.Analysis.Calculus.MeanValue
import Mathlib.Analysis.InnerProductSpace.Rayleigh

/-!
# Curvature and smoothness of an actual quadratic regularization

The quadratic potential shifts the genuine Hessian by a scalar multiple of
the inner product. The lower bound supplies strong convexity; symmetry, Riesz
representation and the Rayleigh norm formula turn the upper bound into actual
gradient Lipschitz continuity. No Hessian field or operator norm is assumed.

Source consumers: SPHMC arXiv:2609.06906v1 Lemma 6.4's curvature/smoothness
clause, and the PBPS arXiv:2609.06905v1 potential in (2.9). This theorem does
not identify conditional laws or prove the subsequent covariance/sampler claims.
-/

namespace AutoSamplingTheory.TechnicalLemmas.Analysis.QuadraticRegularization

open InnerProductSpace
open scoped NNReal

set_option backward.isDefEq.respectTransparency false in
/-- A nonnegative quadratic regularization shifts the strong-convexity and
actual gradient-Lipschitz constants by its precision, including zero precision.
All derivatives are genuine because the input potential is everywhere C². -/
theorem strongConvexOn_and_lipschitzWith_gradient_add_quadratic
    {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E] [CompleteSpace E]
    {U : E → ℝ} {m L r : ℝ≥0}
    (hU : ContDiff ℝ 2 U)
    (hH : ∀ x v : E,
      (m : ℝ) * ‖v‖ ^ 2 ≤ (fderiv ℝ (fderiv ℝ U) x v) v ∧
      (fderiv ℝ (fderiv ℝ U) x v) v ≤ (L : ℝ) * ‖v‖ ^ 2)
    (u : E) :
    let W := fun x => U x + (r : ℝ) / 2 * ‖x - u‖ ^ 2
    StrongConvexOn Set.univ ((m + r : ℝ≥0) : ℝ) W ∧
      LipschitzWith (L + r) (gradient W) := by
  let W := fun x => U x + (r : ℝ) / 2 * ‖x - u‖ ^ 2
  have hUd : Differentiable ℝ U := hU.differentiable (by norm_num)
  have hUdd : Differentiable ℝ (fderiv ℝ U) :=
    (hU.fderiv_right (m := 1) (by norm_num)).differentiable_one
  have hn : ContDiff ℝ 2 (fun x : E => ‖x - u‖ ^ 2) :=
    (contDiff_id.sub contDiff_const).norm_sq (𝕜 := ℝ)
  have hW : ContDiff ℝ 2 W := hU.add (contDiff_const.mul hn)
  have hq (x : E) : HasFDerivAt (fun z => (r : ℝ) / 2 * ‖z - u‖ ^ 2)
      ((r : ℝ) • innerSL ℝ (x - u)) x := by
    convert (((hasFDerivAt_id x).sub_const u).norm_sq).const_mul ((r : ℝ) / 2)
      using 1 <;> first | rfl | (ext v; simp; ring)
  have hWfd (x : E) : fderiv ℝ W x =
      fderiv ℝ U x + (r : ℝ) • innerSL ℝ (x - u) :=
    ((hUd x).hasFDerivAt.add (hq x)).fderiv
  let J : E →L[ℝ] (E →L[ℝ] ℝ) :=
    { toFun := fun v => innerSL ℝ v
      map_add' := by intros; ext; simp
      map_smul' := by intros; ext; simp
      cont := (innerSL ℝ (E := E)).continuous }
  have hWdd (x : E) : HasFDerivAt (fderiv ℝ W)
      (fderiv ℝ (fderiv ℝ U) x + (r : ℝ) • J) x := by
    rw [show fderiv ℝ W = (fun z => fderiv ℝ U z +
      (r : ℝ) • innerSL ℝ (z - u)) from funext hWfd]
    convert (hUdd x).hasFDerivAt.add
      ((J.hasFDerivAt.comp x ((hasFDerivAt_id x).sub_const u)).const_smul
        (r : ℝ)) using 1 <;> rfl
  have hbounds (x v : E) :
      ((m + r : ℝ≥0) : ℝ) * ‖v‖ ^ 2 ≤ (fderiv ℝ (fderiv ℝ W) x v) v ∧
      (fderiv ℝ (fderiv ℝ W) x v) v ≤ ((L + r : ℝ≥0) : ℝ) * ‖v‖ ^ 2 := by
    rw [(hWdd x).fderiv]
    change ((m : ℝ) + r) * ‖v‖ ^ 2 ≤
        (fderiv ℝ (fderiv ℝ U) x v) v + (r : ℝ) * inner ℝ v v ∧
      (fderiv ℝ (fderiv ℝ U) x v) v + (r : ℝ) * inner ℝ v v ≤
        ((L : ℝ) + r) * ‖v‖ ^ 2
    rw [real_inner_self_eq_norm_sq]
    constructor <;> nlinarith [(hH x v).1, (hH x v).2]
  refine ⟨HessianStrongConvexity.strongConvexOn_univ_of_fderiv2_lower hW
    (fun x v => (hbounds x v).1), ?_⟩
  let R : (E →L[ℝ] ℝ) →L[ℝ] E :=
    { toFun := (toDual ℝ E).symm
      map_add' := (toDual ℝ E).symm.map_add
      map_smul' := by intros; simp
      cont := (toDual ℝ E).symm.continuous }
  let T (x : E) : E →L[ℝ] E := R.comp (fderiv ℝ (fderiv ℝ W) x)
  have hTd (x : E) : HasFDerivAt (gradient W) (T x) x := by
    exact R.hasFDerivAt.comp x
      (((hW.fderiv_right (m := 1) (by norm_num)).differentiable_one x).hasFDerivAt)
  have hinner (x v w : E) : inner ℝ (T x v) w =
      (fderiv ℝ (fderiv ℝ W) x v) w := by
    exact toDual_symm_apply
  have hsym (x : E) : (T x).IsSymmetric := by
    intro v w
    change inner ℝ (T x v) w = inner ℝ v (T x w)
    calc
      _ = (fderiv ℝ (fderiv ℝ W) x v) w := hinner x v w
      _ = (fderiv ℝ (fderiv ℝ W) x w) v :=
        hW.contDiffAt.isSymmSndFDerivAt (by norm_num) v w
      _ = inner ℝ (T x w) v := (hinner x w v).symm
      _ = inner ℝ v (T x w) := real_inner_comm _ _
  have hnorm (x : E) : ‖T x‖ ≤ ((L + r : ℝ≥0) : ℝ) := by
    rw [(T x).norm_eq_iSup_rayleighQuotient (hsym x)]
    apply ciSup_le
    intro v
    change |inner ℝ (T x v) v / ‖v‖ ^ 2| ≤ ((L + r : ℝ≥0) : ℝ)
    rw [hinner]
    have hnonneg : 0 ≤ (fderiv ℝ (fderiv ℝ W) x v) v :=
      (mul_nonneg (NNReal.coe_nonneg _) (sq_nonneg _)).trans (hbounds x v).1
    rw [abs_of_nonneg (div_nonneg hnonneg (sq_nonneg _))]
    by_cases hv : v = 0
    · simp [hv]
      positivity
    · exact (div_le_iff₀ (sq_pos_of_pos (norm_pos_iff.mpr hv))).2 (hbounds x v).2
  apply lipschitzWith_of_nnnorm_fderiv_le (fun x => (hTd x).differentiableAt)
  intro x
  rw [(hTd x).fderiv]
  exact hnorm x

end AutoSamplingTheory.TechnicalLemmas.Analysis.QuadraticRegularization
