import AutoSamplingTheory.TechnicalLemmas.Geometry.EuclideanSpaceCoordinates
import Mathlib.Analysis.Calculus.Gradient.Basic
import Mathlib.Analysis.Calculus.LineDeriv.Basic
import Mathlib.Analysis.SpecialFunctions.ExpDeriv

/-!
# Gradient coordinate bridges

Small finite-dimensional bridges from Mathlib's gradient API to coordinate
directional derivatives.  These leaves provide the calculus side of the
coordinate representatives used by the Langevin generator algebra.

They do not prove divergence identities, weighted product rules, integration by
parts, boundary decay, stationarity, reversibility, or invariant Gibbs laws.
-/

namespace AutoSamplingTheory
namespace TechnicalLemmas
namespace Analysis
namespace Calculus
namespace Gradient

open scoped BigOperators RealInnerProductSpace

/-- Chain rule for the Gibbs weight `exp (-V)` in Mathlib's gradient API.

This is the pointwise gradient identity behind the Langevin supplied hypothesis
`∇rho = -rho • ∇V` when `rho x = exp (-V x)`.  It does not prove any weighted
divergence, product-rule, integration-by-parts, stationarity, or invariant-law
statement. -/
theorem hasGradientAt_expNegPotential_of_hasGradientAt
    {F : Type*} [NormedAddCommGroup F] [InnerProductSpace ℝ F] [CompleteSpace F]
    {V : F → ℝ} {x gradV : F}
    (hV : HasGradientAt V gradV x) :
    HasGradientAt
      (fun y : F => Real.exp (-V y))
      (-(Real.exp (-V x)) • gradV)
      x := by
  rw [hasGradientAt_iff_hasFDerivAt]
  have hmap :
      Real.exp (-V x) • -(InnerProductSpace.toDual ℝ F gradV) =
        InnerProductSpace.toDual ℝ F (-(Real.exp (-V x)) • gradV) := by
    apply ContinuousLinearMap.ext
    intro y
    simp [InnerProductSpace.toDual_apply_apply]
  rw [← hmap]
  exact hV.hasFDerivAt.neg.exp

/-- Mathlib-gradient form of the Gibbs weight chain rule from a supplied
potential gradient.

This is the same local chain rule as
`hasGradientAt_expNegPotential_of_hasGradientAt`, followed by Mathlib's
uniqueness theorem `HasGradientAt.gradient`. -/
theorem gradient_expNegPotential_eq_of_hasGradientAt
    {F : Type*} [NormedAddCommGroup F] [InnerProductSpace ℝ F] [CompleteSpace F]
    {V : F → ℝ} {x gradV : F}
    (hV : HasGradientAt V gradV x) :
    gradient (fun y : F => Real.exp (-V y)) x =
      -(Real.exp (-V x)) • gradV := by
  exact (hasGradientAt_expNegPotential_of_hasGradientAt hV).gradient

/-- Coordinate form of
`gradient_expNegPotential_eq_of_hasGradientAt` on finite Euclidean space. -/
theorem gradient_expNegPotential_coordinate_eq_of_hasGradientAt
    {ι : Type*} [Fintype ι]
    {V : EuclideanSpace ℝ ι → ℝ} {x gradV : EuclideanSpace ℝ ι}
    (hV : HasGradientAt V gradV x) (i : ι) :
    (gradient (fun y : EuclideanSpace ℝ ι => Real.exp (-V y)) x) i =
      -Real.exp (-V x) * gradV i := by
  have hgrad := gradient_expNegPotential_eq_of_hasGradientAt hV
  calc
    (gradient (fun y : EuclideanSpace ℝ ι => Real.exp (-V y)) x) i =
        (-(Real.exp (-V x)) • gradV) i := by rw [hgrad]
    _ = -Real.exp (-V x) * gradV i := by simp

/-- Pointwise Mathlib-gradient form of the Gibbs weight chain rule.

If `V` is differentiable at `x`, then Mathlib's total `gradient` of
`fun y => exp (-V y)` agrees with the expected vector
`-exp (-V x) • gradient V x`.  This is still only a pointwise calculus leaf; it
does not prove weighted divergence, product-rule, integration-by-parts,
stationarity, or invariant-law statements. -/
theorem gradient_expNegPotential_eq_of_differentiableAt
    {F : Type*} [NormedAddCommGroup F] [InnerProductSpace ℝ F] [CompleteSpace F]
    {V : F → ℝ} {x : F}
    (hV : DifferentiableAt ℝ V x) :
    gradient (fun y : F => Real.exp (-V y)) x =
      -(Real.exp (-V x)) • gradient V x := by
  exact gradient_expNegPotential_eq_of_hasGradientAt hV.hasGradientAt

/-- Coordinate form of
`gradient_expNegPotential_eq_of_differentiableAt` on finite Euclidean space.

This is the narrow reusable leaf that supplies the Gibbs-weight chain-rule
coordinate equality used by the Langevin algebra handoffs. -/
theorem gradient_expNegPotential_coordinate_eq_of_differentiableAt
    {ι : Type*} [Fintype ι]
    {V : EuclideanSpace ℝ ι → ℝ} {x : EuclideanSpace ℝ ι}
    (hV : DifferentiableAt ℝ V x) (i : ι) :
    (gradient (fun y : EuclideanSpace ℝ ι => Real.exp (-V y)) x) i =
      -Real.exp (-V x) * (gradient V x) i := by
  exact gradient_expNegPotential_coordinate_eq_of_hasGradientAt hV.hasGradientAt i

/-- A globally `C¹` real-valued function has a continuous Mathlib gradient.

This is the reusable regularity handoff from a test-function class to the
component-continuity hypothesis used in the Langevin finite-box trace leaves.
It uses Mathlib's total `gradient = (toDual ℝ F).symm ∘ fderiv ℝ f`.

It does not prove any `ContDiffOn` closed-box statement, Hessian regularity,
divergence theorem, weighted integration by parts, boundary cancellation,
generator domains, invariant laws, reversibility, or KL/FI dissipation. -/
theorem continuous_gradient_of_contDiff_one
    {F : Type*} [NormedAddCommGroup F] [InnerProductSpace ℝ F] [CompleteSpace F]
    {f : F → ℝ} (hf : ContDiff ℝ 1 f) :
    Continuous (fun x : F => gradient f x) := by
  exact ((InnerProductSpace.toDual ℝ F).symm.continuous.comp
    (hf.continuous_fderiv one_ne_zero))

/-- Apply the Frechet derivative to a vector when a gradient representative is
supplied.

This is the basic bridge from Mathlib's `fderiv` to the inner-product
gradient convention.  It is pointwise only: it does not choose coordinates,
define divergence, prove integration by parts, or assert any global
regularity. -/
theorem fderiv_apply_eq_inner_of_hasGradientAt
    {F : Type*} [NormedAddCommGroup F] [InnerProductSpace ℝ F] [CompleteSpace F]
    {f : F → ℝ} {x grad v : F}
    (hf : HasGradientAt f grad x) :
    fderiv ℝ f x v = inner ℝ grad v := by
  have hfd : fderiv ℝ f x = InnerProductSpace.toDual ℝ F grad :=
    hf.differentiableAt.hasFDerivAt.unique hf.hasFDerivAt
  calc
    fderiv ℝ f x v = InnerProductSpace.toDual ℝ F grad v := by rw [hfd]
    _ = inner ℝ grad v := by rw [InnerProductSpace.toDual_apply_apply]

/-- Apply the Frechet derivative to a vector and rewrite the result using
Mathlib's total `gradient`.

This is the pointwise `fderiv`/`gradient` bridge used before finite-coordinate
Langevin displays. -/
theorem fderiv_apply_eq_inner_gradient_of_differentiableAt
    {F : Type*} [NormedAddCommGroup F] [InnerProductSpace ℝ F] [CompleteSpace F]
    {f : F → ℝ} {x v : F}
    (hf : DifferentiableAt ℝ f x) :
    fderiv ℝ f x v = inner ℝ (gradient f x) v :=
  fderiv_apply_eq_inner_of_hasGradientAt hf.hasGradientAt

/-- Euclidean coordinate form of the pointwise `fderiv`/`gradient` bridge.

For the coordinate unit `eᵢ`, applying `fderiv ℝ f x` is the corresponding
coordinate of Mathlib's `gradient f x`.  This removes only the local
gradient-coordinate replacement used by finite-dimensional Langevin displays;
divergence, Laplacian identities, integration by parts, generator domains, and
invariant-law statements remain separate obligations. -/
theorem fderiv_apply_coordinate_eq_gradient_coordinate_of_differentiableAt
    {ι : Type*} [Fintype ι] [DecidableEq ι]
    {f : EuclideanSpace ℝ ι → ℝ} {x : EuclideanSpace ℝ ι} (i : ι)
    (hf : DifferentiableAt ℝ f x) :
    fderiv ℝ f x (EuclideanSpace.single i (1 : ℝ)) = (gradient f x) i := by
  have hinner :
      inner ℝ (gradient f x) (EuclideanSpace.single i (1 : ℝ)) =
        (gradient f x) i := by
    simpa [EuclideanSpace.basisFun_apply] using
      (EuclideanSpace.inner_basisFun_real (ι := ι) (x := gradient f x) i)
  calc
    fderiv ℝ f x (EuclideanSpace.single i (1 : ℝ)) =
        inner ℝ (gradient f x) (EuclideanSpace.single i (1 : ℝ)) :=
      fderiv_apply_eq_inner_gradient_of_differentiableAt hf
    _ = (gradient f x) i := hinner

/-- A supplied Mathlib gradient gives the line derivative in a coordinate unit
direction, with value equal to that coordinate of the gradient.

This is a pointwise Euclidean coordinate bridge.  It does not define divergence,
the Laplacian, or any integration-by-parts identity. -/
theorem hasGradientAt_coordinateUnit_hasLineDerivAt
    {ι : Type*} [Fintype ι] [DecidableEq ι]
    {f : EuclideanSpace ℝ ι → ℝ}
    {x grad : EuclideanSpace ℝ ι}
    (hf : HasGradientAt f grad x) (i : ι) :
    HasLineDerivAt ℝ f (grad i) x
      (WithLp.toLp 2 (Pi.single i (1 : ℝ)) : EuclideanSpace ℝ ι) := by
  let direction : EuclideanSpace ℝ ι := WithLp.toLp 2 (Pi.single i (1 : ℝ))
  have hvalue : (InnerProductSpace.toDual ℝ _ grad) direction = grad i := by
    rw [InnerProductSpace.toDual_apply_apply]
    rw [
      _root_.AutoSamplingTheory.TechnicalLemmas.Geometry.EuclideanSpaceCoordinates.euclideanSpace_inner_eq_sum_mul]
    rw [Finset.sum_eq_single i]
    · simp [direction]
    · intro j _ hj
      simp [direction, Pi.single_eq_of_ne hj]
    · intro hi
      exact False.elim (hi (Finset.mem_univ i))
  rw [← hvalue]
  exact hf.hasFDerivAt.hasLineDerivAt direction

end Gradient
end Calculus
end Analysis
end TechnicalLemmas
end AutoSamplingTheory
