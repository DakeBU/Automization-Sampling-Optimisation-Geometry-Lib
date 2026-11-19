import AutoSamplingTheory.TechnicalLemmas.Probability.OrthogonalHaar
import Mathlib.Analysis.InnerProductSpace.Projection.FiniteDimensional
import Mathlib.Analysis.Normed.Lp.MeasurableSpace
import Mathlib.Tactic.FunProp
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Ring

open Matrix MeasureTheory Set Metric
open scoped RealInnerProductSpace

namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarOrientedSection

set_option autoImplicit false

/-- The actual sphere admits a Borel choice of positively oriented orthogonal frames
with prescribed first column, including in dimension two. -/
theorem exists_measurable_oriented_section (n : ℕ) :
    let E := EuclideanSpace ℝ (Fin (n + 2))
    let G := Matrix.orthogonalGroup (Fin (n + 2)) ℝ
    ∃ Q : Metric.sphere (0 : E) 1 → G, Measurable Q ∧
      ∀ z : Metric.sphere (0 : E) 1,
        (Q z : Matrix (Fin (n + 2)) (Fin (n + 2)) ℝ).det = 1 ∧
        (Q z : Matrix (Fin (n + 2)) (Fin (n + 2)) ℝ) *ᵥ
          Pi.single (0 : Fin (n + 2)) (1 : ℝ) = WithLp.ofLp (z : E) := by
  classical
  let I := Fin (n + 2)
  let E := EuclideanSpace ℝ I
  let M := Matrix I I ℝ
  let G := Matrix.orthogonalGroup I ℝ
  let S := Metric.sphere (0 : E) 1
  let i : I := 0
  let j : I := ⟨1, by omega⟩
  have hij : i ≠ j := by
    intro h
    have hval := congrArg Fin.val h
    simp [i, j] at hval
  let e : E := PiLp.single 2 i (1 : ℝ)
  have he : ‖e‖ = 1 := by
    change ‖PiLp.single 2 (β := fun _ : I => ℝ) i 1‖ = 1
    rw [PiLp.norm_single]
    norm_num
  let B := EuclideanSpace.basisFun I ℝ
  let v : S → E := fun z => e - (z : E)
  let w (z : S) : E ≃ₗᵢ[ℝ] E := (ℝ ∙ v z)ᗮ.reflection
  let H (z : S) : G :=
    ⟨(w z).toMatrix B.toBasis B.toBasis, (w z).toMatrix_mem_unitaryGroup B B⟩
  -- The reflection has a Borel rank-one formula in the fixed coordinate basis.
  have hHformula (z : S) :
      (H z : M) = 1 + (-(2 : ℝ) / ‖v z‖ ^ 2) •
        Matrix.vecMulVec (WithLp.ofLp (v z)) (WithLp.ofLp (v z)) := by
    have hw (x : E) : w z x = x - (2 : ℝ) • (inner ℝ (v z) x / ‖v z‖ ^ 2) • v z := by
      change ((ℝ ∙ v z)ᗮ.reflection) x = _
      rw [Submodule.reflection_orthogonal_apply, Submodule.reflection_singleton_apply]
      simp [two_smul]
    ext a b
    change (LinearMap.toMatrix B.toBasis B.toBasis (w z).toLinearEquiv.toLinearMap) a b = _
    rw [LinearMap.toMatrix_apply]
    change (w z (B b)) a = _
    have hB : B b = PiLp.single 2 b (1 : ℝ) := EuclideanSpace.basisFun_apply I ℝ b
    have hinner : inner ℝ (v z) (B b) = WithLp.ofLp (v z) b := by
      rw [hB, EuclideanSpace.inner_single_right]
      simp
    have hIdent : (B b) a = (1 : M) a b := by
      rw [hB]
      change Pi.single (M := fun _ : I => ℝ) b 1 a = (1 : Matrix I I ℝ) a b
      rw [Matrix.one_apply]
      by_cases h : a = b <;> simp [h]
    rw [hw, hinner]
    change (B b) a - 2 * ((WithLp.ofLp (v z) b / ‖v z‖ ^ 2) *
        WithLp.ofLp (v z) a) = _
    rw [hIdent]
    simp only [Matrix.add_apply, Matrix.smul_apply, smul_eq_mul, Matrix.vecMulVec_apply]
    ring
  have hv : Measurable v := measurable_const.sub measurable_subtype_coe
  have hvEntry (a : I) : Measurable (fun z : S => WithLp.ofLp (v z) a) :=
    (PiLp.continuous_apply (p := 2) (β := fun _ : I => ℝ) a).measurable.comp hv
  have hscale : Measurable (fun z : S => -(2 : ℝ) / ‖v z‖ ^ 2) :=
    measurable_const.div (hv.norm.pow_const 2)
  have hHval : Measurable (fun z : S => fun a b : I => (H z : M) a b) := by
    apply measurable_pi_lambda
    intro a
    apply measurable_pi_lambda
    intro b
    have hEntry : (fun z : S => (H z : M) a b) =
        (fun z : S => (1 : M) a b + (-(2 : ℝ) / ‖v z‖ ^ 2) *
          (WithLp.ofLp (v z) a * WithLp.ofLp (v z) b)) := by
      funext z
      rw [hHformula]
      rfl
    rw [hEntry]
    exact measurable_const.add (hscale.mul ((hvEntry a).mul (hvEntry b)))
  have hGclosed : IsClosed (G : Set M) := isClosed_unitary
  have hEmbedding : Topology.IsClosedEmbedding (fun W : G => fun a b : I => (W : M) a b) :=
    hGclosed.isClosedEmbedding_subtypeVal
  have hH : Measurable H := hEmbedding.measurableEmbedding.measurable_comp_iff.mp hHval
  have hHdet (z : S) (hne : (z : E) ≠ e) : (H z : M).det = -1 := by
    have hvne : v z ≠ 0 := sub_ne_zero.mpr hne.symm
    change (LinearMap.toMatrix B.toBasis B.toBasis
      ((ℝ ∙ v z)ᗮ.reflection.toLinearMap)).det = _
    rw [LinearMap.det_toMatrix, Submodule.det_reflection,
      Submodule.orthogonal_orthogonal, finrank_span_singleton hvne, pow_one]
  have hHcol (z : S) : (H z : M) *ᵥ Pi.single i (1 : ℝ) = WithLp.ofLp (z : E) := by
    have hz : ‖(z : E)‖ = 1 := mem_sphere_zero_iff_norm.mp z.property
    have hwe : w z e = (z : E) := Submodule.reflection_sub (he.trans hz.symm)
    have hcoord := LinearMap.toMatrix_mulVec_repr B.toBasis B.toBasis (w z).toLinearEquiv.toLinearMap e
    change (H z : M) *ᵥ WithLp.ofLp e = WithLp.ofLp (w z e) at hcoord
    rw [hwe] at hcoord
    exact hcoord
  -- This fixed coordinate flip changes orientation while fixing the first vector.
  let D : G := ⟨Matrix.diagonal (fun a => if a = j then (-1 : ℝ) else 1), by
    apply (Matrix.mem_orthogonalGroup_iff I ℝ).2
    rw [Matrix.diagonal_transpose, Matrix.diagonal_mul_diagonal]
    have hd : (fun a : I => (if a = j then (-1 : ℝ) else 1) *
        (if a = j then (-1 : ℝ) else 1)) = fun _ => (1 : ℝ) := by
      funext a
      by_cases ha : a = j <;> simp [ha]
    rw [hd, Matrix.diagonal_one]⟩
  have hDdet : (D : M).det = -1 := by
    rw [show (D : M) = Matrix.diagonal (fun a : I => if a = j then (-1 : ℝ) else 1) from rfl,
      Matrix.det_diagonal]
    exact Fintype.prod_ite_eq' j (fun _ => (-1 : ℝ))
  have hDcol : (D : M) *ᵥ Pi.single i (1 : ℝ) = Pi.single i 1 := by
    ext a
    rw [Matrix.mulVec_single_one]
    by_cases ha : a = i <;> simp [D, ha, hij]
  let Q (z : S) : G := if (z : E) = e then 1 else H z * D
  have hAtE : MeasurableSet {z : S | (z : E) = e} :=
    (isClosed_eq continuous_subtype_val continuous_const).measurableSet
  have hQ : Measurable Q :=
    Measurable.ite hAtE measurable_const ((measurable_mul_const D).comp hH)
  refine ⟨Q, hQ, ?_⟩
  intro z
  change (Q z : M).det = 1 ∧ (Q z : M) *ᵥ Pi.single i (1 : ℝ) = WithLp.ofLp (z : E)
  by_cases hz : (z : E) = e
  · simp only [Q, if_pos hz]
    constructor
    · exact Matrix.det_one
    · change (1 : M) *ᵥ Pi.single i (1 : ℝ) = _
      rw [Matrix.one_mulVec, hz]
      rfl
  · simp only [Q, if_neg hz]
    constructor
    · change ((H z : M) * (D : M)).det = _
      rw [Matrix.det_mul, hHdet z hz, hDdet]
      norm_num
    · change ((H z : M) * (D : M)) *ᵥ Pi.single i (1 : ℝ) = _
      rw [← Matrix.mulVec_mulVec, hDcol, hHcol]

#print axioms exists_measurable_oriented_section

end AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarOrientedSection
