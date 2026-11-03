import Mathlib.Analysis.InnerProductSpace.Calculus
import Mathlib.Analysis.InnerProductSpace.Laplacian
import Mathlib.Analysis.Calculus.Gradient.Basic
import Mathlib.Analysis.Calculus.ContDiff.Deriv
import Mathlib.Tactic

/-!
Local radial calculus for a scalar profile of squared distance. This is an
ASTIS canonical library specification, not an attributed theorem of HFT.
Only local C2 regularity of the scalar profile is required; the center and
dimension-zero cases are included. Source consumers discharge this regularity
internally for their actual power, logarithm, or polynomial profile.
-/

open Filter
open scoped Topology RealInnerProductSpace

namespace AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.RadialCalculus
set_option autoImplicit false
variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]

private theorem radial_fderiv (g : ℝ → ℝ) (a x : E)
    (hg : DifferentiableAt ℝ g (‖x - a‖ ^ 2)) :
    HasFDerivAt (fun z : E => g (‖z - a‖ ^ 2))
      ((2 * deriv g (‖x - a‖ ^ 2)) • innerSL ℝ (x - a)) x := by
  have hd := hg.hasDerivAt.comp_hasFDerivAt x
    (((hasFDerivAt_id x).sub_const a).norm_sq)
  convert! hd using 1
  ext y
  simp [mul_left_comm, mul_comm]

private theorem radial_second (g : ℝ → ℝ) (a x e : E)
    (hg : ContDiffAt ℝ 2 g (‖x - a‖ ^ 2)) :
    fderiv ℝ (fun z : E => fderiv ℝ (fun w : E => g (‖w - a‖ ^ 2)) z e) x e =
      4 * deriv (deriv g) (‖x - a‖ ^ 2) * (inner ℝ (x - a) e) ^ 2 +
      2 * deriv g (‖x - a‖ ^ 2) * inner ℝ e e := by
  have hs : ContinuousAt (fun z : E => ‖z - a‖ ^ 2) x := by fun_prop
  have hgerm : (fun z : E => fderiv ℝ (fun w : E => g (‖w - a‖ ^ 2)) z e) =ᶠ[𝓝 x]
      (fun z : E => (2 * deriv g (‖z - a‖ ^ 2)) * inner ℝ (z - a) e) := by
    filter_upwards [hs (hg.eventually (by norm_num))] with z hz
    change ContDiffAt ℝ 2 g (‖z - a‖ ^ 2) at hz
    rw [(radial_fderiv g a z (hz.differentiableAt (by norm_num))).fderiv]
    simp [inner_sub_left]
  have hg' : DifferentiableAt ℝ (deriv g) (‖x - a‖ ^ 2) :=
    (hg.derivWithin (m := 1) (by norm_num)).differentiableAt one_ne_zero
  have hcoef := (radial_fderiv (deriv g) a x hg').const_mul 2
  have hdot := ((hasFDerivAt_id x).sub_const a).inner ℝ (hasFDerivAt_const e x)
  have hfd := (hcoef.mul hdot).fderiv
  change fderiv ℝ (fun z : E => (2 * deriv g (‖z - a‖ ^ 2)) * inner ℝ (z - a) e) x = _ at hfd
  rw [hgerm.fderiv_eq, hfd]
  simp [smul_eq_mul, inner_sub_left]
  ring

/-- Gradient and Laplacian of a locally C2 scalar profile of squared distance
in a finite real Hilbert space, including the center and dimension zero. -/
theorem radial_gradient_laplacian
    {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E] [FiniteDimensional ℝ E]
    (g : ℝ → ℝ) (a x : E) (hg : ContDiffAt ℝ 2 g (‖x - a‖ ^ 2)) :
    gradient (fun z : E => g (‖z - a‖ ^ 2)) x =
      (2 * deriv g (‖x - a‖ ^ 2)) • (x - a) ∧
    Laplacian.laplacian (fun z : E => g (‖z - a‖ ^ 2)) x =
      4 * (‖x - a‖ ^ 2) * deriv (deriv g) (‖x - a‖ ^ 2) +
      2 * (Module.finrank ℝ E : ℝ) * deriv g (‖x - a‖ ^ 2) := by
  constructor
  · apply ext_inner_right ℝ
    intro y
    rw [inner_gradient_left,
      (radial_fderiv g a x (hg.differentiableAt (by norm_num))).fderiv]
    simp [real_inner_smul_left, inner_sub_left]
  · let f : E → ℝ := fun z => g (‖z - a‖ ^ 2)
    have hc : ContDiffAt ℝ 2 f x :=
      hg.comp x ((contDiffAt_id.sub contDiffAt_const).norm_sq ℝ)
    have hd := ((hc.fderiv_right (m := 1) (by norm_num)).differentiableAt one_ne_zero).hasFDerivAt
    have he (e : E) : fderiv ℝ (fderiv ℝ f) x e e =
        4 * deriv (deriv g) (‖x - a‖ ^ 2) * (inner ℝ (x - a) e) ^ 2 +
        2 * deriv g (‖x - a‖ ^ 2) * inner ℝ e e := by
      have hl : fderiv ℝ (fun z => fderiv ℝ f z e) x e = fderiv ℝ (fderiv ℝ f) x e e := by
        simpa using congrArg (fun T : E →L[ℝ] ℝ => T e)
          (hd.clm_apply (hasFDerivAt_const e x)).fderiv
      rw [← hl]
      exact radial_second g a x e hg
    let b := stdOrthonormalBasis ℝ E
    have ht : Laplacian.laplacian f x = ∑ i, fderiv ℝ (fderiv ℝ f) x (b i) (b i) := by
      rw [InnerProductSpace.laplacian_eq_iteratedFDeriv_stdOrthonormalBasis]
      apply Finset.sum_congr rfl
      intro i _
      rw [iteratedFDeriv_two_apply]
      rfl
    have hs : ∑ i, (inner ℝ (x - a) (b i)) ^ 2 = ‖x - a‖ ^ 2 := by
      simpa [pow_two, real_inner_comm, inner_self_eq_norm_sq] using b.sum_inner_mul_inner (x - a) (x - a)
    change Laplacian.laplacian f x = _
    rw [ht]
    simp_rw [he]
    rw [Finset.sum_add_distrib]
    simp only [← Finset.mul_sum]
    rw [hs]
    simp [b]
    ring

end AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.RadialCalculus
