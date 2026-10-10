import AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Cutoff
import Mathlib.Analysis.InnerProductSpace.Laplacian

/-!
# Laplacian coordinate bridges

Small wrappers around Mathlib's finite-dimensional real inner-product-space
Laplacian API.  These leaves expose the standard orthonormal-basis second
derivative formula in ASTIS-owned names for the Langevin generator tree.

They do not prove integration by parts, boundary decay, stationarity,
reversibility, or any divergence theorem.
-/

namespace AutoSamplingTheory
namespace TechnicalLemmas
namespace Analysis
namespace Calculus
namespace Laplacian

open scoped BigOperators InnerProductSpace

/-- Mathlib's finite-dimensional standard-orthonormal-basis formula for the
Laplacian, exposed as an ASTIS calculus leaf.

For Ch.1 Langevin this is the coordinate bridge behind a supplied Laplacian
identifier `lapF = ∑ᵢ ∂ᵢᵢ f`.  It is not an integration-by-parts or invariant
measure theorem. -/
theorem laplacian_eq_sum_stdOrthonormalBasis
    {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [FiniteDimensional ℝ E] (f : E → ℝ) :
    Laplacian.laplacian f =
      fun x => ∑ i, iteratedFDeriv ℝ 2 f x
        ![(stdOrthonormalBasis ℝ E) i, (stdOrthonormalBasis ℝ E) i] :=
  InnerProductSpace.laplacian_eq_iteratedFDeriv_stdOrthonormalBasis f

/-- Handoff form of `laplacian_eq_sum_stdOrthonormalBasis` for source-defined
Laplacian functionals.

This is useful when a paper defines a weak-generator or test-function action by
the coordinate second-derivative sum and the local Lean proof needs to rewrite
that action as Mathlib's `Laplacian.laplacian`. -/
theorem laplacianFunctional_eq_of_stdOrthonormalBasis_sum
    {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [FiniteDimensional ℝ E]
    (sourceLaplacianFunctional : (E → ℝ) → ℝ)
    (sourceTest : E → ℝ) :
    sourceLaplacianFunctional (Laplacian.laplacian sourceTest) =
      sourceLaplacianFunctional
        (fun x => ∑ i, iteratedFDeriv ℝ 2 sourceTest x
          ![(stdOrthonormalBasis ℝ E) i, (stdOrthonormalBasis ℝ E) i]) := by
  rw [laplacian_eq_sum_stdOrthonormalBasis]

/-- A globally `C²` real-valued function has a continuous Mathlib Laplacian.

This packages the standard finite-dimensional route: expand the Laplacian in a
standard orthonormal basis, use continuity of the second iterated Frechet
derivative from `ContDiff`, and apply the resulting continuous multilinear map
to fixed basis directions.

It does not prove closed-box `ContDiffOn` regularity, divergence theorem,
weighted integration by parts, boundary cancellation, generator domains,
invariant laws, reversibility, or KL/FI dissipation. -/
theorem continuous_laplacian_of_contDiff_two
    {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [FiniteDimensional ℝ E]
    {f : E → ℝ} (hf : ContDiff ℝ 2 f) :
    Continuous (fun x : E => Laplacian.laplacian f x) := by
  rw [InnerProductSpace.laplacian_eq_iteratedFDeriv_stdOrthonormalBasis f]
  refine continuous_finsetSum _ ?_
  intro i _
  let v : Fin 2 → E := ![(stdOrthonormalBasis ℝ E) i, (stdOrthonormalBasis ℝ E) i]
  have h2 : Continuous (fun x : E => iteratedFDeriv ℝ 2 f x) := by
    exact (hf.iteratedFDeriv_right (m := 0) (i := 2) (by norm_num)).continuous
  exact (ContinuousMultilinearMap.apply ℝ (fun _ : Fin 2 => E) ℝ v).continuous.comp h2

/-- The Laplacian is bounded by dimension times the operator norm of the
second iterated Fréchet derivative.

The dimension factor comes only from summing the diagonal evaluations in a
standard orthonormal basis.  This is a pointwise finite-dimensional trace
bound; it assumes no compact support or integrability. -/
theorem norm_laplacian_le_finrank_mul_norm_iteratedFDeriv_two
    {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [FiniteDimensional ℝ E] (f : E → ℝ) (x : E) :
    ‖Laplacian.laplacian f x‖ ≤
      (Module.finrank ℝ E : ℝ) * ‖iteratedFDeriv ℝ 2 f x‖ := by
  rw [congrFun (InnerProductSpace.laplacian_eq_iteratedFDeriv_stdOrthonormalBasis f) x]
  calc
    ‖∑ i, iteratedFDeriv ℝ 2 f x
        ![(stdOrthonormalBasis ℝ E) i, (stdOrthonormalBasis ℝ E) i]‖ ≤
        ∑ i, ‖iteratedFDeriv ℝ 2 f x
          ![(stdOrthonormalBasis ℝ E) i, (stdOrthonormalBasis ℝ E) i]‖ :=
      norm_sum_le _ _
    _ ≤ ∑ _i : Fin (Module.finrank ℝ E), ‖iteratedFDeriv ℝ 2 f x‖ := by
      gcongr with i
      simpa using
        (iteratedFDeriv ℝ 2 f x).le_opNorm
          ![(stdOrthonormalBasis ℝ E) i, (stdOrthonormalBasis ℝ E) i]
    _ = (Module.finrank ℝ E : ℝ) * ‖iteratedFDeriv ℝ 2 f x‖ := by
      simp

/-- Positive-scale radial cutoff Laplacians have the expected `R^-2` bound,
with the finite-dimensional trace factor shown explicitly. -/
theorem radialSmoothCutoff_laplacian_bound
    {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [FiniteDimensional ℝ E] [Nontrivial E] :
    ∃ C : ℝ, 0 < C ∧ ∀ R : ℝ, 0 < R → ∀ x : E,
      ‖Laplacian.laplacian
        (Cutoff.radialSmoothCutoff R : E → ℝ) x‖ ≤
          (Module.finrank ℝ E : ℝ) * (C / R ^ 2) := by
  obtain ⟨C, hC, hbound⟩ :=
    Cutoff.radialSmoothCutoff_iteratedFDeriv_two_bound (E := E)
  refine ⟨C, hC, ?_⟩
  intro R hR x
  exact (norm_laplacian_le_finrank_mul_norm_iteratedFDeriv_two
    (Cutoff.radialSmoothCutoff R : E → ℝ) x).trans
      (mul_le_mul_of_nonneg_left (hbound R hR x) (Nat.cast_nonneg _))

end Laplacian
end Calculus
end Analysis
end TechnicalLemmas
end AutoSamplingTheory
