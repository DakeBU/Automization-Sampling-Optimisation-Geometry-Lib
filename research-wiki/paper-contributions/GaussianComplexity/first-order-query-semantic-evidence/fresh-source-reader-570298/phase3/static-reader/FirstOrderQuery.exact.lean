import AutoSamplingTheory.ExampleCases.GaussianComplexity.BlockFamily
import Mathlib.Analysis.Calculus.Gradient.Basic
import Mathlib.Analysis.InnerProductSpace.PiL2
import Mathlib.Analysis.CStarAlgebra.Matrix
import Mathlib.Analysis.InnerProductSpace.Calculus
import Mathlib.Analysis.InnerProductSpace.Adjoint
open Matrix InnerProductSpace
open scoped BigOperators
open AutoSamplingTheory.ExampleCases.GaussianComplexity.DeterminantFamily
/-!
# Actual one-query first-order reconstruction

Zhou--Suzuki arXiv:2610.20492v1, Appendix B.1 Oracle reduction,
Ex33--Ex35. The unknown precision is the canonical actual block family.
The primitive oracle below returns exact forward or transpose products of
its hidden orthogonal blocks. Their stated affine combination reconstructs
the genuine Euclidean Frechet gradient and the actual potential value.
HasGradientAt is an output; totalized gradient fallback is never a premise.
The contiguous coordinates include the omitted zero-dimensional residual.
Finite-horizon operational2T caps, adaptive posterior/transcript/output laws,
TV-precision and expected-cost adapters and both main lower bounds are separate.
-/

namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.FirstOrderQuery
set_option autoImplicit false
theorem actual_first_order_query {d n : ℕ} (hn : 3 ≤ n) (hnd : n ≤ d)
    {κ : ℝ} (hκ : 4 ≤ κ)
    (Os : Fin (d / n) → Matrix.orthogonalGroup (Fin n) ℝ) :
    let e : ((Fin n × Fin (d / n)) ⊕ Fin (d % n)) ≃ Fin d :=
      ((Equiv.sumCongr
        ((Equiv.prodComm (Fin n) (Fin (d / n))).trans finProdFinEquiv)
        (Equiv.refl (Fin (d % n)))).trans finSumFinEquiv).trans
        (finCongr (by simpa [Nat.mul_comm] using Nat.div_add_mod d n))
    let A := blockPrecision κ Os
    let f : EuclideanSpace ℝ (Fin d) → ℝ := fun x =>
      (WithLp.ofLp x) ⬝ᵥ (A *ᵥ WithLp.ofLp x) / 2
    let query : Fin (d / n) → EuclideanSpace ℝ (Fin n) → Bool →
        EuclideanSpace ℝ (Fin n) := fun j v inverse =>
      WithLp.toLp 2 (if inverse then
        (Os j : Matrix (Fin n) (Fin n) ℝ).transpose *ᵥ WithLp.ofLp v
      else (Os j : Matrix (Fin n) (Fin n) ℝ) *ᵥ WithLp.ofLp v)
    let xb : EuclideanSpace ℝ (Fin d) → Fin (d / n) →
        EuclideanSpace ℝ (Fin n) := fun x j =>
      WithLp.toLp 2 (fun i => x (e (Sum.inl (i, j))))
    let gb : EuclideanSpace ℝ (Fin d) → Fin (d / n) →
        EuclideanSpace ℝ (Fin n) := fun x j =>
      ((κ + 1) / 2) • xb x j - ((κ - 1) / 4) •
        (query j (xb x j) false + query j (xb x j) true)
    let g : EuclideanSpace ℝ (Fin d) → EuclideanSpace ℝ (Fin d) := fun x =>
      WithLp.toLp 2 (fun a => Sum.elim
        (fun ij => gb x ij.2 ij.1)
        (fun i => x (e (Sum.inr i))) (e.symm a))
    ∀ x : EuclideanSpace ℝ (Fin d),
      HasGradientAt f (g x) x ∧
      (f x, gradient f x) = (inner ℝ x (g x) / 2, g x) := by
  classical
  dsimp only
  let e : ((Fin n × Fin (d / n)) ⊕ Fin (d % n)) ≃ Fin d :=
    ((Equiv.sumCongr
      ((Equiv.prodComm (Fin n) (Fin (d / n))).trans finProdFinEquiv)
      (Equiv.refl (Fin (d % n)))).trans finSumFinEquiv).trans
      (finCongr (by simpa [Nat.mul_comm] using Nat.div_add_mod d n))
  let A := blockPrecision κ Os
  let f : EuclideanSpace ℝ (Fin d) → ℝ := fun x =>
    (WithLp.ofLp x) ⬝ᵥ (A *ᵥ WithLp.ofLp x) / 2
  let query : Fin (d / n) → EuclideanSpace ℝ (Fin n) → Bool →
      EuclideanSpace ℝ (Fin n) := fun j v inverse =>
    WithLp.toLp 2 (if inverse then
      (Os j : Matrix (Fin n) (Fin n) ℝ).transpose *ᵥ WithLp.ofLp v
    else (Os j : Matrix (Fin n) (Fin n) ℝ) *ᵥ WithLp.ofLp v)
  let xb : EuclideanSpace ℝ (Fin d) → Fin (d / n) →
      EuclideanSpace ℝ (Fin n) := fun x j =>
    WithLp.toLp 2 (fun i => x (e (Sum.inl (i, j))))
  let gb : EuclideanSpace ℝ (Fin d) → Fin (d / n) →
      EuclideanSpace ℝ (Fin n) := fun x j =>
    ((κ + 1) / 2) • xb x j - ((κ - 1) / 4) •
      (query j (xb x j) false + query j (xb x j) true)
  let g : EuclideanSpace ℝ (Fin d) → EuclideanSpace ℝ (Fin d) := fun x =>
    WithLp.toLp 2 (fun a => Sum.elim
      (fun ij => gb x ij.2 ij.1)
      (fun i => x (e (Sum.inr i))) (e.symm a))
  let E := EuclideanSpace ℝ (Fin d)
  let H : E →L[ℝ] E := Matrix.toEuclideanCLM (𝕜 := ℝ) (n := Fin d) A
  -- The same canonical actual-family regularity node supplies symmetry.
  have hA : A.IsHermitian := (blockPrecision_regular hn hnd hκ Os).1
  have hself : IsSelfAdjoint A := hA
  have hH : H.IsSymmetric :=
    ContinuousLinearMap.isSelfAdjoint_iff_isSymmetric.mp
      (hself.map (Matrix.toEuclideanCLM (𝕜 := ℝ) (n := Fin d)))
  have hf : f = fun y : E => (1 / 2 : ℝ) * inner ℝ y (H y) := by
    funext y
    dsimp only [f]
    rw [show inner ℝ y (H y) = (WithLp.ofLp y) ⬝ᵥ (A *ᵥ WithLp.ofLp y) from
      Matrix.inner_toEuclideanCLM A y y]
    ring
  -- Differentiate the actual quadratic; no default gradient value is used.
  have hgrad (y : E) : HasGradientAt f (H y) y := by
    have hraw := ((hasFDerivAt_id y).inner ℝ H.hasFDerivAt).const_mul (1 / 2 : ℝ)
    have hlin : (1 / 2 : ℝ) •
        ((fderivInnerCLM ℝ (y, H y)).comp ((ContinuousLinearMap.id ℝ E).prod H)) =
        toDual ℝ E (H y) := by
      ext v
      change (1 / 2 : ℝ) * (inner ℝ y (H v) + inner ℝ v (H y)) = inner ℝ (H y) v
      rw [← hH.apply_clm y v, (real_inner_comm v (H y)).symm]
      ring
    apply hasGradientAt_iff_hasFDerivAt.mpr
    rw [hf, ← hlin]
    exact hraw
  let C : Matrix ((Fin n × Fin (d / n)) ⊕ Fin (d % n))
      ((Fin n × Fin (d / n)) ⊕ Fin (d % n)) ℝ :=
    Matrix.fromBlocks (Matrix.blockDiagonal (fun j => singleBlockPrecision κ (Os j)))
      0 0 (1 : Matrix (Fin (d % n)) (Fin (d % n)) ℝ)
  have hAdef : A = Matrix.reindex e e C := rfl
  intro x
  -- Ex33 is an internal actual block-action bridge, not an assumed answer.
  have hsingle (j : Fin (d / n)) : WithLp.ofLp (gb x j) =
      singleBlockPrecision κ (Os j) *ᵥ WithLp.ofLp (xb x j) := by
    simp [gb, query, singleBlockPrecision, Matrix.sub_mulVec, Matrix.smul_mulVec,
      Matrix.add_mulVec, Matrix.one_mulVec]
  -- Recombine those block actions through the literal source coordinates.
  have hG : g x = H x := by
    ext a
    change Sum.elim (fun ij => gb x ij.2 ij.1)
      (fun i => x (e (Sum.inr i))) (e.symm a) = (A *ᵥ WithLp.ofLp x) a
    rw [hAdef]
    change _ = (C.submatrix e.symm e.symm *ᵥ WithLp.ofLp x) a
    rw [Matrix.submatrix_mulVec_equiv]
    change _ = (C *ᵥ (WithLp.ofLp x ∘ e)) (e.symm a)
    generalize hz : e.symm a = z
    rcases z with ij | i
    · rcases ij with ⟨i, j⟩
      dsimp only [C]
      rw [Matrix.fromBlocks_mulVec]
      simp only [Sum.elim_inl, Matrix.zero_mulVec, add_zero]
      change (gb x j) i = (Matrix.blockDiagonal (fun j => singleBlockPrecision κ (Os j)) *ᵥ
        (fun ij => x (e (Sum.inl ij)))) (i, j)
      rw [show (gb x j) i = (singleBlockPrecision κ (Os j) *ᵥ
        (fun a => x (e (Sum.inl (a, j))))) i from congrFun (hsingle j) i]
      simp [Matrix.mulVec, dotProduct, Fintype.sum_prod_type, Matrix.blockDiagonal_apply,
        ite_mul]
    · dsimp only [C]
      rw [Matrix.fromBlocks_mulVec]
      simp only [Sum.elim_inr, Matrix.zero_mulVec, Matrix.one_mulVec,
        zero_add, Function.comp_apply]
  have hg : HasGradientAt f (g x) x := hG.symm ▸ hgrad x
  refine ⟨hg, ?_⟩
  have hval : f x = inner ℝ x (g x) / 2 := by
    rw [hG]
    exact congrArg (fun t : ℝ => t / 2) (Matrix.inner_toEuclideanCLM A x x).symm
  exact Prod.ext hval hg.gradient
end AutoSamplingTheory.ExampleCases.GaussianComplexity.FirstOrderQuery
