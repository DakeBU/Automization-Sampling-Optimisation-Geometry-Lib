import AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Gradient
import Mathlib.Analysis.Calculus.ContDiff.FTaylorSeries
import Mathlib.Analysis.Calculus.FDeriv.CompCLM
import Mathlib.Analysis.Calculus.LineDeriv.Basic

/-!
# Line-derivative product-rule bridges

Small wrappers around Mathlib's one-dimensional derivative product rule for
line derivatives.  These leaves isolate the product-rule component needed by
finite-coordinate Langevin weighted-divergence algebra.

They do not define divergence, identify coordinate derivatives with divergence
sums, prove Hessian/Laplacian coordinate identities, prove integration by parts,
or establish stationarity, reversibility, invariant Gibbs laws, or KL/FI
dissipation.
-/

namespace AutoSamplingTheory
namespace TechnicalLemmas
namespace Analysis
namespace Calculus
namespace LineDeriv

open scoped RealInnerProductSpace

set_option backward.isDefEq.respectTransparency false in
/-- Product rule for algebra-valued line derivatives.

This is a direct wrapper around Mathlib's `HasDerivAt.mul` applied to the
one-dimensional curve `t ↦ x + t • v`.  In the Langevin tree, the real-valued
specialization supplies only the product-rule part of a coordinate calculation
such as
`∂ᵢ (rho * g) = rho * ∂ᵢ g + (∂ᵢ rho) * g`.  It does not identify `g` with a
coordinate derivative of a test function, prove the derivative of `g`, define a
divergence operator, or prove an integration-by-parts identity. -/
theorem hasLineDerivAt_mul
    {𝕜 : Type*} [NontriviallyNormedField 𝕜]
    {E : Type*} [AddCommGroup E] [Module 𝕜 E]
    {𝔸 : Type*} [NormedRing 𝔸] [NormedAlgebra 𝕜 𝔸]
    {f g : E → 𝔸} {x v : E} {f' g' : 𝔸}
    (hf : HasLineDerivAt 𝕜 f f' x v)
    (hg : HasLineDerivAt 𝕜 g g' x v) :
    HasLineDerivAt 𝕜 (fun y : E => f y * g y)
      (f' * g x + f x * g') x v := by
  unfold HasLineDerivAt at hf hg ⊢
  simpa only [Pi.mul_apply, zero_smul, add_zero] using! hf.mul hg

/-- Real-valued `rho * g` specialization of `hasLineDerivAt_mul`, in the
summand order used by finite-coordinate weighted-divergence algebra. -/
theorem hasLineDerivAt_rho_mul
    {E : Type*} [AddCommGroup E] [Module ℝ E]
    {rho g : E → ℝ} {x v : E} {rho' g' : ℝ}
    (hrho : HasLineDerivAt ℝ rho rho' x v)
    (hg : HasLineDerivAt ℝ g g' x v) :
    HasLineDerivAt ℝ (fun y : E => rho y * g y)
      (rho x * g' + rho' * g x) x v := by
  simpa [mul_comm, add_comm, add_left_comm, add_assoc] using
    hasLineDerivAt_mul (𝕜 := ℝ) (E := E) (𝔸 := ℝ)
      (f := rho) (g := g) (f' := rho') (g' := g') (x := x) (v := v)
      hrho hg

/-- Line-derivative equality form of the real-valued `rho * g` product rule.

This is the form needed by coordinate divergence displays, where a source
calculation usually names `lineDeriv ℝ (fun y => rho y * g y) x v` rather than
a `HasLineDerivAt` proof object.  It still supplies only the local product-rule
calculus component. -/
theorem lineDeriv_rho_mul_eq_of_hasLineDerivAt
    {E : Type*} [AddCommGroup E] [Module ℝ E]
    {rho g : E → ℝ} {x v : E} {rho' g' : ℝ}
    (hrho : HasLineDerivAt ℝ rho rho' x v)
    (hg : HasLineDerivAt ℝ g g' x v) :
    lineDeriv ℝ (fun y : E => rho y * g y) x v =
      rho x * g' + rho' * g x :=
  (hasLineDerivAt_rho_mul hrho hg).lineDeriv

/-- Coordinate-unit product rule for the Gibbs weight `exp (-V)`.

Given differentiability of the potential and a supplied coordinate derivative
of `g`, this computes the line derivative of
`fun y => exp (-V y) * g y` in the coordinate direction.  This removes the
Gibbs-weight derivative part of the product-rule branch, but it does not
identify `g` with a coordinate derivative of a test function, prove a Hessian
coordinate identity, define divergence, prove integration by parts, or prove
an invariant Gibbs law. -/
theorem lineDeriv_expNegPotential_mul_eq_of_differentiableAt
    {ι : Type*} [Fintype ι] [DecidableEq ι]
    {V g : EuclideanSpace ℝ ι → ℝ} {x : EuclideanSpace ℝ ι}
    {g' : ℝ} (i : ι)
    (hV : DifferentiableAt ℝ V x)
    (hg : HasLineDerivAt ℝ g g' x
      (WithLp.toLp 2 (Pi.single i (1 : ℝ)) : EuclideanSpace ℝ ι)) :
    lineDeriv ℝ
        (fun y : EuclideanSpace ℝ ι => Real.exp (-V y) * g y)
        x
        (WithLp.toLp 2 (Pi.single i (1 : ℝ)) : EuclideanSpace ℝ ι) =
      Real.exp (-V x) * g' - Real.exp (-V x) * (gradient V x) i * g x := by
  have hrho :
      HasLineDerivAt ℝ
        (fun y : EuclideanSpace ℝ ι => Real.exp (-V y))
        (-(Real.exp (-V x)) * (gradient V x) i)
        x
        (WithLp.toLp 2 (Pi.single i (1 : ℝ)) : EuclideanSpace ℝ ι) := by
    have hline :=
      _root_.AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Gradient.hasGradientAt_coordinateUnit_hasLineDerivAt
        (ι := ι)
        (f := fun y : EuclideanSpace ℝ ι => Real.exp (-V y))
        (x := x)
        (grad := -(Real.exp (-V x)) • gradient V x)
        (_root_.AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Gradient.hasGradientAt_expNegPotential_of_hasGradientAt
          (V := V) (x := x) (gradV := gradient V x) hV.hasGradientAt)
        i
    simpa using hline
  have hprod :=
    lineDeriv_rho_mul_eq_of_hasLineDerivAt
      (rho := fun y : EuclideanSpace ℝ ι => Real.exp (-V y))
      (g := g)
      (x := x)
      (v := (WithLp.toLp 2 (Pi.single i (1 : ℝ)) : EuclideanSpace ℝ ι))
      (rho' := -(Real.exp (-V x)) * (gradient V x) i)
      (g' := g')
      hrho hg
  calc
    lineDeriv ℝ
        (fun y : EuclideanSpace ℝ ι => Real.exp (-V y) * g y)
        x
        (WithLp.toLp 2 (Pi.single i (1 : ℝ)) : EuclideanSpace ℝ ι)
        = Real.exp (-V x) * g' +
            (-(Real.exp (-V x)) * (gradient V x) i) * g x := hprod
    _ = Real.exp (-V x) * g' - Real.exp (-V x) * (gradient V x) i * g x := by
      ring

/-- A supplied derivative of the first derivative gives the coordinate line
derivative of `fun y => fderiv ℝ f y v`.

This is a small Hessian-wiring leaf for the Langevin tree.  It does not assert
that the supplied second-derivative representative is Mathlib's
`fderiv ℝ (fderiv ℝ f) x` or `iteratedFDeriv ℝ 2 f x`; those identifications
are separate leaves. -/
theorem hasLineDerivAt_fderiv_apply_const_of_hasFDerivAt_fderiv
    {E : Type*} [NormedAddCommGroup E] [NormedSpace ℝ E]
    {f : E → ℝ} {x w v : E} {A : E →L[ℝ] E →L[ℝ] ℝ}
    (hf : HasFDerivAt (fun y : E => fderiv ℝ f y) A x) :
    HasLineDerivAt ℝ (fun y : E => fderiv ℝ f y v) (A w v) x w := by
  have hconst : HasFDerivAt (fun _ : E => v) (0 : E →L[ℝ] E) x :=
    hasFDerivAt_const v x
  have happly := hf.clm_apply hconst
  have hline := happly.hasLineDerivAt w
  simpa using hline

/-- Line-derivative equality form of
`hasLineDerivAt_fderiv_apply_const_of_hasFDerivAt_fderiv`. -/
theorem lineDeriv_fderiv_apply_const_eq_of_hasFDerivAt_fderiv
    {E : Type*} [NormedAddCommGroup E] [NormedSpace ℝ E]
    {f : E → ℝ} {x w v : E} {A : E →L[ℝ] E →L[ℝ] ℝ}
    (hf : HasFDerivAt (fun y : E => fderiv ℝ f y) A x) :
    lineDeriv ℝ (fun y : E => fderiv ℝ f y v) x w = A w v :=
  (hasLineDerivAt_fderiv_apply_const_of_hasFDerivAt_fderiv
    (f := f) (x := x) (w := w) (v := v) hf).lineDeriv

/-- If the total `fderiv` map is differentiable at `x`, then the line derivative
of the fixed slice `fun y => fderiv ℝ f y v` is the two-fold iterated
derivative.

This is the direct bridge from a coordinate derivative of a first derivative to
Mathlib's total `iteratedFDeriv` representative used for Hessian
diagonal/slice terms in finite-dimensional Langevin generator displays. -/
theorem lineDeriv_fderiv_apply_const_eq_iteratedFDeriv_two
    {E : Type*} [NormedAddCommGroup E] [NormedSpace ℝ E]
    {f : E → ℝ} {x w v : E}
    (hf : DifferentiableAt ℝ (fun y : E => fderiv ℝ f y) x) :
    lineDeriv ℝ (fun y : E => fderiv ℝ f y v) x w =
      iteratedFDeriv ℝ 2 f x ![w, v] := by
  have hline :=
    lineDeriv_fderiv_apply_const_eq_of_hasFDerivAt_fderiv
      (f := f) (x := x) (w := w) (v := v)
      (A := fderiv ℝ (fun y : E => fderiv ℝ f y) x)
      hf.hasFDerivAt
  calc
    lineDeriv ℝ (fun y : E => fderiv ℝ f y v) x w =
        fderiv ℝ (fun y : E => fderiv ℝ f y) x w v := hline
    _ = iteratedFDeriv ℝ 2 f x ![w, v] := by
      rw [iteratedFDeriv_two_apply]
      simp

/-- Coordinate-unit version of
`lineDeriv_fderiv_apply_const_eq_iteratedFDeriv_two` on finite Euclidean
space. -/
theorem lineDeriv_fderiv_apply_coordinate_eq_iteratedFDeriv_two
    {ι : Type*} [Fintype ι] [DecidableEq ι]
    {f : EuclideanSpace ℝ ι → ℝ} {x : EuclideanSpace ℝ ι} (i : ι)
    (hf : DifferentiableAt ℝ
      (fun y : EuclideanSpace ℝ ι => fderiv ℝ f y) x) :
    lineDeriv ℝ
        (fun y : EuclideanSpace ℝ ι =>
          fderiv ℝ f y
            (WithLp.toLp 2 (Pi.single i (1 : ℝ)) : EuclideanSpace ℝ ι))
        x
        (WithLp.toLp 2 (Pi.single i (1 : ℝ)) : EuclideanSpace ℝ ι) =
      iteratedFDeriv ℝ 2 f x
        ![(WithLp.toLp 2 (Pi.single i (1 : ℝ)) : EuclideanSpace ℝ ι),
          (WithLp.toLp 2 (Pi.single i (1 : ℝ)) : EuclideanSpace ℝ ι)] :=
  lineDeriv_fderiv_apply_const_eq_iteratedFDeriv_two
    (f := f) (x := x)
    (w := (WithLp.toLp 2 (Pi.single i (1 : ℝ)) : EuclideanSpace ℝ ι))
    (v := (WithLp.toLp 2 (Pi.single i (1 : ℝ)) : EuclideanSpace ℝ ι))
    hf

/-- Coordinate product rule for the explicit Gibbs weight multiplied by the
coordinate derivative represented as `fderiv ℝ f y eᵢ`.

Compared with `lineDeriv_expNegPotential_mul_eq_of_differentiableAt`, this
also discharges the supplied derivative of `g` when
`g y = fderiv ℝ f y eᵢ` and the total `fderiv` map of `f` is differentiable at
`x`.  It still does not replace `fderiv ℝ f y eᵢ` by `(gradient f y) i`,
define or sum divergence, prove IBP, or prove invariant Gibbs law. -/
theorem lineDeriv_expNegPotential_mul_fderiv_coordinate_eq
    {ι : Type*} [Fintype ι] [DecidableEq ι]
    {V f : EuclideanSpace ℝ ι → ℝ} {x : EuclideanSpace ℝ ι} (i : ι)
    (hV : DifferentiableAt ℝ V x)
    (hf : DifferentiableAt ℝ
      (fun y : EuclideanSpace ℝ ι => fderiv ℝ f y) x) :
    lineDeriv ℝ
        (fun y : EuclideanSpace ℝ ι =>
          Real.exp (-V y) *
            fderiv ℝ f y
              (WithLp.toLp 2 (Pi.single i (1 : ℝ)) : EuclideanSpace ℝ ι))
        x
        (WithLp.toLp 2 (Pi.single i (1 : ℝ)) : EuclideanSpace ℝ ι) =
      Real.exp (-V x) *
          iteratedFDeriv ℝ 2 f x
            ![(WithLp.toLp 2 (Pi.single i (1 : ℝ)) : EuclideanSpace ℝ ι),
              (WithLp.toLp 2 (Pi.single i (1 : ℝ)) : EuclideanSpace ℝ ι)] -
        Real.exp (-V x) * (gradient V x) i *
          fderiv ℝ f x
            (WithLp.toLp 2 (Pi.single i (1 : ℝ)) : EuclideanSpace ℝ ι) := by
  have hg :
      HasLineDerivAt ℝ
        (fun y : EuclideanSpace ℝ ι =>
          fderiv ℝ f y
            (WithLp.toLp 2 (Pi.single i (1 : ℝ)) : EuclideanSpace ℝ ι))
        (iteratedFDeriv ℝ 2 f x
          ![(WithLp.toLp 2 (Pi.single i (1 : ℝ)) : EuclideanSpace ℝ ι),
            (WithLp.toLp 2 (Pi.single i (1 : ℝ)) : EuclideanSpace ℝ ι)])
        x
        (WithLp.toLp 2 (Pi.single i (1 : ℝ)) : EuclideanSpace ℝ ι) := by
    have hraw :=
      hasLineDerivAt_fderiv_apply_const_of_hasFDerivAt_fderiv
        (f := f) (x := x)
        (w := (WithLp.toLp 2 (Pi.single i (1 : ℝ)) : EuclideanSpace ℝ ι))
        (v := (WithLp.toLp 2 (Pi.single i (1 : ℝ)) : EuclideanSpace ℝ ι))
        (A := fderiv ℝ
          (fun y : EuclideanSpace ℝ ι => fderiv ℝ f y) x)
        hf.hasFDerivAt
    let direction : EuclideanSpace ℝ ι :=
      WithLp.toLp 2 (Pi.single i (1 : ℝ))
    have hvalue :
        (fderiv ℝ (fun y : EuclideanSpace ℝ ι => fderiv ℝ f y) x)
            direction direction =
          iteratedFDeriv ℝ 2 f x ![direction, direction] := by
      rw [iteratedFDeriv_two_apply]
      simp
    rw [← hvalue]
    exact hraw
  exact lineDeriv_expNegPotential_mul_eq_of_differentiableAt
    (V := V)
    (g := fun y : EuclideanSpace ℝ ι =>
      fderiv ℝ f y
        (WithLp.toLp 2 (Pi.single i (1 : ℝ)) : EuclideanSpace ℝ ι))
    (x := x)
    (g' := iteratedFDeriv ℝ 2 f x
      ![(WithLp.toLp 2 (Pi.single i (1 : ℝ)) : EuclideanSpace ℝ ι),
        (WithLp.toLp 2 (Pi.single i (1 : ℝ)) : EuclideanSpace ℝ ι)])
    i hV hg

end LineDeriv
end Calculus
end Analysis
end TechnicalLemmas
end AutoSamplingTheory
