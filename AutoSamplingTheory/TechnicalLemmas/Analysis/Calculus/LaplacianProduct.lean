import Mathlib.Analysis.InnerProductSpace.Laplacian
import Mathlib.Analysis.Calculus.Gradient.Basic
import Mathlib.Analysis.InnerProductSpace.PiL2
import Mathlib.Analysis.Calculus.FDeriv.Mul
import Mathlib.Tactic

/-!
The real Laplacian product rule with only local C2 regularity.
This canonical node localizes the former private global-C2 calculus in
CompactPoissonSmoothGraph. It is also applicable to the actual Poisson kernel
away from its pole. HFT second edition Eq1.19 is the source calculus identity;
local germs and arbitrary finite real Hilbert spaces are explicit generalizations.
No harmonicity, mean-value property or surface integral is asserted here.
-/

open Filter
open scoped Topology

namespace AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.LaplacianProduct
set_option autoImplicit false

private theorem directional_second
    {E : Type*} [NormedAddCommGroup E] [NormedSpace ℝ E]
    {f : E → ℝ} {x : E} (hf : ContDiffAt ℝ 2 f x) (v : E) :
    fderiv ℝ (fun z => fderiv ℝ f z v) x v =
      fderiv ℝ (fderiv ℝ f) x v v := by
  have hd := ((hf.fderiv_right (m := 1) (by norm_num)).differentiableAt
    one_ne_zero).hasFDerivAt
  simpa using congrArg (fun T : E →L[ℝ] ℝ => T v)
    (hd.clm_apply (hasFDerivAt_const v x)).fderiv

private theorem second_product
    {E : Type*} [NormedAddCommGroup E] [NormedSpace ℝ E]
    {f g : E → ℝ} {x : E}
    (hf : ContDiffAt ℝ 2 f x) (hg : ContDiffAt ℝ 2 g x) (v : E) :
    fderiv ℝ (fderiv ℝ (fun z => f z * g z)) x v v =
      f x * fderiv ℝ (fderiv ℝ g) x v v +
      2 * (fderiv ℝ f x v * fderiv ℝ g x v) +
      g x * fderiv ℝ (fderiv ℝ f) x v v := by
  have hf1 : ContDiffAt ℝ 1 f x := hf.of_le (by norm_num)
  have hg1 : ContDiffAt ℝ 1 g x := hg.of_le (by norm_num)
  have hfd : ContDiffAt ℝ 1 (fun z => fderiv ℝ f z v) x :=
    (hf.fderiv_right (m := 1) (by norm_num)).clm_apply contDiffAt_const
  have hgd : ContDiffAt ℝ 1 (fun z => fderiv ℝ g z v) x :=
    (hg.fderiv_right (m := 1) (by norm_num)).clm_apply contDiffAt_const
  have he : (fun z => fderiv ℝ (fun w => f w * g w) z v) =ᶠ[𝓝 x]
      fun z => f z * fderiv ℝ g z v + g z * fderiv ℝ f z v := by
    filter_upwards [hf.eventually (by norm_num), hg.eventually (by norm_num)]
      with z hfz hgz
    have hd := (hfz.differentiableAt (by norm_num)).hasFDerivAt.mul
      (hgz.differentiableAt (by norm_num)).hasFDerivAt
    rw [show fderiv ℝ (fun w => f w * g w) z = _ from hd.fderiv]
    simp only [add_apply, smul_apply, smul_eq_mul]
  rw [← directional_second (hf.mul hg) v, he.fderiv_eq]
  have hd := ((hf1.differentiableAt one_ne_zero).hasFDerivAt.mul
    (hgd.differentiableAt one_ne_zero).hasFDerivAt).add
    ((hg1.differentiableAt one_ne_zero).hasFDerivAt.mul
      (hfd.differentiableAt one_ne_zero).hasFDerivAt)
  rw [show fderiv ℝ (fun z => f z * fderiv ℝ g z v +
    g z * fderiv ℝ f z v) x = _ from hd.fderiv]
  simp only [add_apply, smul_apply, smul_eq_mul]
  rw [directional_second hg v, directional_second hf v]
  ring

/-- The pointwise scalar Laplacian product rule in every finite real Hilbert
space, including dimension zero. Only local C2 regularity at this point is used. -/
theorem laplacian_mul
    {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [FiniteDimensional ℝ E] {f g : E → ℝ} {x : E}
    (hf : ContDiffAt ℝ 2 f x) (hg : ContDiffAt ℝ 2 g x) :
    Laplacian.laplacian (fun z => f z * g z) x =
      f x * Laplacian.laplacian g x +
      2 * inner ℝ (gradient f x) (gradient g x) +
      g x * Laplacian.laplacian f x := by
  have ht (h : E → ℝ) : Laplacian.laplacian h x =
      ∑ i, fderiv ℝ (fderiv ℝ h) x
        ((stdOrthonormalBasis ℝ E) i) ((stdOrthonormalBasis ℝ E) i) := by
    rw [InnerProductSpace.laplacian_eq_iteratedFDeriv_stdOrthonormalBasis]
    apply Finset.sum_congr rfl
    intro i _
    rw [iteratedFDeriv_two_apply]
    rfl
  have hi : inner ℝ (gradient f x) (gradient g x) =
      ∑ i, fderiv ℝ f x ((stdOrthonormalBasis ℝ E) i) *
        fderiv ℝ g x ((stdOrthonormalBasis ℝ E) i) := by
    rw [← (stdOrthonormalBasis ℝ E).sum_inner_mul_inner (gradient f x) (gradient g x)]
    simp only [inner_gradient_left, inner_gradient_right, conj_trivial]
  rw [ht, ht, ht, hi]
  simp_rw [second_product hf hg]
  simp only [Finset.sum_add_distrib, ← Finset.mul_sum]

end AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.LaplacianProduct
