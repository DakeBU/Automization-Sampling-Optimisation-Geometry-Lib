import Mathlib.Analysis.SpecialFunctions.Trigonometric.Chebyshev.Basic
import Mathlib.Analysis.InnerProductSpace.PiL2
import Mathlib.LinearAlgebra.Matrix.ToLin
import Mathlib.Algebra.Polynomial.Degree.SmallDegree
import Mathlib.Algebra.Polynomial.Eval.SMul
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Ring

open Matrix Polynomial
open scoped BigOperators
set_option autoImplicit false

/-! The actual cosine feature matrix has exactly the source block Krylov range
(arXiv:2610.20492v1, Appendix C.2 Fact C.5). This is a pointwise identity for
arbitrary deterministic starts. No rank, independence or Gaussian certificate
is assumed. Concentration and the two main lower bounds remain separate. -/
namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumKrylovRange

theorem actual_cosine_feature_krylov_range {d q : ℕ} (κ : ℝ) (hκ : 2 ≤ κ) (hq : 2 * q + 1 < d)
    (x : EuclideanSpace ℝ (Fin d × Fin (q + 1))) :
  let θ : Fin d → ℝ := fun i => ((i.val : ℝ) + 1 / 2) * Real.pi / (d : ℝ)
  let eigenvalue : Fin d → ℝ := fun i => (κ + 1) / 2 + (κ - 1) / 2 * Real.cos (θ i)
  let Λ : Matrix (Fin d) (Fin d) ℝ := Matrix.diagonal eigenvalue
  let g : Fin (q + 1) → Fin d → ℝ := fun a i => WithLp.ofLp x (i, a)
  let t : Matrix (Fin d) (Fin (q + 1)) ℝ := fun i k =>
    if k.val = 0 then 1 else Real.sqrt 2 * Real.cos ((k.val : ℝ) * θ i)
  let B : Matrix (Fin d) (Fin (q + 1) × Fin (q + 1)) ℝ := fun i a =>
    (Real.sqrt (d : ℝ))⁻¹ * g a.1 i * t i a.2
  let K : Submodule ℝ (Fin d → ℝ) :=
    Submodule.span ℝ (Set.range (fun a : Fin (q + 1) × Fin (q + 1) =>
      (Λ ^ a.2.val).mulVec (g a.1)))
  Set.range (fun c : Fin (q + 1) × Fin (q + 1) → ℝ => B.mulVec c) =
    (K : Set (Fin d → ℝ)) := by
  classical
  dsimp only
  let θ : Fin d → ℝ := fun i => ((i.val : ℝ) + 1 / 2) * Real.pi / (d : ℝ)
  let α : ℝ := (κ + 1) / 2
  let β : ℝ := (κ - 1) / 2
  let eigenvalue : Fin d → ℝ := fun i => α + β * Real.cos (θ i)
  let Λ : Matrix (Fin d) (Fin d) ℝ := Matrix.diagonal eigenvalue
  let g : Fin (q + 1) → Fin d → ℝ := fun a i => WithLp.ofLp x (i, a)
  let t : Matrix (Fin d) (Fin (q + 1)) ℝ := fun i k =>
    if k.val = 0 then 1 else Real.sqrt 2 * Real.cos ((k.val : ℝ) * θ i)
  let s : ℝ := (Real.sqrt (d : ℝ))⁻¹
  let w : Fin (q + 1) → ℝ := fun k => if k.val = 0 then 1 else Real.sqrt 2
  let B : Matrix (Fin d) (Fin (q + 1) × Fin (q + 1)) ℝ := fun i a =>
    s * g a.1 i * t i a.2
  let K : Submodule ℝ (Fin d → ℝ) :=
    Submodule.span ℝ (Set.range (fun a : Fin (q + 1) × Fin (q + 1) =>
      (Λ ^ a.2.val).mulVec (g a.1)))
  let R : Submodule ℝ (Fin d → ℝ) := LinearMap.range B.mulVecLin
  change (R : Set (Fin d → ℝ)) = (K : Set (Fin d → ℝ))
  have hβ : β ≠ 0 := by dsimp [β]; linarith
  have hd : 0 < (d : ℝ) := by exact_mod_cast (show 0 < d by omega)
  have hs : s ≠ 0 := inv_ne_zero (Real.sqrt_ne_zero'.mpr hd)
  have hw (k : Fin (q + 1)) : w k ≠ 0 := by
    dsimp [w]
    split_ifs
    · exact one_ne_zero
    · exact Real.sqrt_ne_zero'.mpr (by norm_num)
  let z : ℝ[X] := C β⁻¹ * (X - C α)
  have hz : z.degree = 1 := by
    simp only [z, Polynomial.degree_C_mul (inv_ne_zero hβ), Polynomial.degree_X_sub_C]
  let U : Polynomial.Sequence ℝ :=
    { elems' := fun n => X ^ n
      degree_eq' := fun n => by simp }
  let Q : Polynomial.Sequence ℝ :=
    { elems' := fun n => (Polynomial.Chebyshev.T ℝ (n : ℤ)).comp z
      degree_eq' := fun n => by
        rw [Polynomial.degree_comp (by rw [hz]; norm_num)]
        simp [hz] }
  have hU : Submodule.span ℝ (U '' Set.Iio (q + 1)) = Polynomial.degreeLT ℝ (q + 1) :=
    U.span_degreeLT (fun n _ => isUnit_iff_ne_zero.mpr (Polynomial.leadingCoeff_ne_zero.mpr (U.ne_zero n)))
  have hQ : Submodule.span ℝ (Q '' Set.Iio (q + 1)) = Polynomial.degreeLT ℝ (q + 1) :=
    Q.span_degreeLT (fun n _ => isUnit_iff_ne_zero.mpr (Polynomial.leadingCoeff_ne_zero.mpr (Q.ne_zero n)))
  let F : Fin (q + 1) → ℝ[X] →ₗ[ℝ] (Fin d → ℝ) := fun a =>
    { toFun := fun p i => p.eval (eigenvalue i) * g a i
      map_add' := fun p r => by ext i; simp [add_mul]
      map_smul' := fun c p => by
        ext i
        simp only [Polynomial.eval_smul, Pi.smul_apply, RingHom.id_apply,
          smul_eq_mul, mul_assoc] }
  have hpower (a : Fin (q + 1)) (n : ℕ) :
      F a (U n) = (Λ ^ n).mulVec (g a) := by
    ext i
    simp [F, U, Λ, Matrix.diagonal_pow, Matrix.mulVec_diagonal]
  have hangle (i : Fin d) : z.eval (eigenvalue i) = Real.cos (θ i) := by
    simp only [z, Polynomial.eval_mul, Polynomial.eval_C, Polynomial.eval_sub, Polynomial.eval_X,
      eigenvalue, add_sub_cancel_left, inv_mul_cancel_left₀ hβ]
  have hcos (a : Fin (q + 1)) (n : ℕ) :
      F a (Q n) = fun i => Real.cos ((n : ℝ) * θ i) * g a i := by
    ext i
    change ((Polynomial.Chebyshev.T ℝ (n : ℤ)).comp z).eval (eigenvalue i) * g a i = _
    rw [Polynomial.eval_comp, hangle]
    simp only [Polynomial.Chebyshev.T_real_cos, Int.cast_natCast]
  have hcol (a k : Fin (q + 1)) :
      B.col (a, k) = (s * w k) • F a (Q k.val) := by
    ext i
    rw [hcos]
    change s * g a i * t i k = (s * w k) * (Real.cos ((k.val : ℝ) * θ i) * g a i)
    by_cases hk : k.val = 0
    · simp [t, w, hk, mul_comm, mul_left_comm, mul_assoc]
    · simp only [t, w, if_neg hk]
      ring
  have hpolyK (a : Fin (q + 1)) :
      Polynomial.degreeLT ℝ (q + 1) ≤ K.comap (F a) := by
    rw [← hU]
    refine Submodule.span_le.mpr ?_
    rintro _ ⟨n, hn, rfl⟩
    change F a (U n) ∈ K
    rw [hpower]
    exact Submodule.subset_span ⟨(a, ⟨n, hn⟩), rfl⟩
  have hpolyR (a : Fin (q + 1)) :
      Polynomial.degreeLT ℝ (q + 1) ≤ R.comap (F a) := by
    rw [← hQ]
    refine Submodule.span_le.mpr ?_
    rintro _ ⟨n, hn, rfl⟩
    change F a (Q n) ∈ R
    let k : Fin (q + 1) := ⟨n, hn⟩
    have hscaled : (s * w k) • F a (Q n) ∈ R := by
      rw [← hcol a k]
      change B.col (a, k) ∈ LinearMap.range B.mulVecLin
      rw [Matrix.range_mulVecLin]
      exact Submodule.subset_span ⟨(a, k), rfl⟩
    exact (R.smul_mem_iff (mul_ne_zero hs (hw k))).mp hscaled
  have hRK : R = K := by
    apply le_antisymm
    · change LinearMap.range B.mulVecLin ≤ K
      rw [Matrix.range_mulVecLin]
      refine Submodule.span_le.mpr ?_
      rintro _ ⟨⟨a, k⟩, rfl⟩
      rw [hcol]
      apply K.smul_mem
      apply hpolyK a
      rw [Polynomial.mem_degreeLT, Q.degree_eq]
      exact_mod_cast k.isLt
    · change Submodule.span ℝ _ ≤ R
      refine Submodule.span_le.mpr ?_
      rintro _ ⟨⟨a, k⟩, rfl⟩
      change (Λ ^ k.val).mulVec (g a) ∈ R
      rw [← hpower]
      apply hpolyR a
      rw [Polynomial.mem_degreeLT, U.degree_eq]
      exact_mod_cast k.isLt
  exact congrArg (fun M : Submodule ℝ (Fin d → ℝ) => (M : Set (Fin d → ℝ))) hRK

end AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumKrylovRange
