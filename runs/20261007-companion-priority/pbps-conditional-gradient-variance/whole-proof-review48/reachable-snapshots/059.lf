import AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence
import AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Gradient
import AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Laplacian
import AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.LineDeriv
import AutoSamplingTheory.TechnicalLemmas.Geometry.EuclideanSpaceCoordinates
import Mathlib.Analysis.InnerProductSpace.Basic
import Mathlib.Analysis.SpecialFunctions.ExpDeriv
import Mathlib.Analysis.Calculus.Deriv.Mul
import Mathlib.Algebra.BigOperators.Fin
import Mathlib.Tactic.Ring

/-!
# Langevin generator pointwise algebra

These leaves record the one-dimensional Gibbs-weight product-rule identity
behind the overdamped Langevin generator convention
`L f = f'' - V' * f'`.

They also record the finite-dimensional weighted-divergence algebra step that
comes after product-rule and chain-rule identities have already been supplied:
`div (rho ∇f) = rho * (lap f - <∇V, ∇f>)` when `∇rho = -rho ∇V`.
The coordinate-sum leaves additionally aggregate supplied coordinate product
rules into the same divergence-form expression.

They do not prove stationarity, reversibility, integration by parts, boundary
decay, Fokker--Planck regularity, generator domains, or normalization of a
Gibbs measure.
-/

namespace AutoSamplingTheory
namespace TechnicalLemmas
namespace StochasticProcesses
namespace Langevin

open scoped RealInnerProductSpace BigOperators ENNReal
open MeasureTheory Filter

/-- Pointwise product-rule identity for the one-dimensional Gibbs weight
`exp (-V)`.  In source notation this is the local calculation
`(exp (-V) f')' = exp (-V) * (f'' - V' * f')`.

This is only an ordinary derivative statement in one dimension. -/
theorem hasDerivAt_gibbsWeight_mul_testDeriv_eq_langevinGenerator_1d
    {f V : ℝ → ℝ} {x f' f'' V' : ℝ}
    (hV : HasDerivAt V V' x)
    (hf : HasDerivAt f f' x)
    (hf' : HasDerivAt (deriv f) f'' x) :
    HasDerivAt (fun y : ℝ => Real.exp (-V y) * deriv f y)
      (Real.exp (-V x) * (f'' - V' * f')) x := by
  have hnegV : HasDerivAt (fun y : ℝ => -V y) (-V') x := hV.neg
  have hexp : HasDerivAt (fun y : ℝ => Real.exp (-V y))
      ((-V') * Real.exp (-V x)) x := by
    simpa [mul_comm] using hnegV.exp
  have hmul := hexp.mul hf'
  simpa only [Pi.mul_apply] using! hmul.congr_deriv (by
    rw [hf.deriv]
    ring)

/-- Derivative-form version of
`hasDerivAt_gibbsWeight_mul_testDeriv_eq_langevinGenerator_1d`. -/
theorem deriv_gibbsWeight_mul_testDeriv_eq_langevinGenerator_1d
    {f V : ℝ → ℝ} {x f' f'' V' : ℝ}
    (hV : HasDerivAt V V' x)
    (hf : HasDerivAt f f' x)
    (hf' : HasDerivAt (deriv f) f'' x) :
    deriv (fun y : ℝ => Real.exp (-V y) * deriv f y) x =
      Real.exp (-V x) * (f'' - V' * f') :=
  (hasDerivAt_gibbsWeight_mul_testDeriv_eq_langevinGenerator_1d hV hf hf').deriv

/-- Algebraic multidimensional handoff behind the weighted-divergence form of
the overdamped Langevin generator.

The hypotheses are intentionally supplied product-rule and chain-rule outputs:
`hdiv` stands for
`div (rho ∇f) = rho * lapF + <∇rho, ∇f>`, and `hgrad` stands for
`∇rho = -rho ∇V`.  The theorem performs only the final scalar/inner-product
algebra. -/
theorem weightedDivergence_gibbsWeight_langevinGenerator_algebra
    {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    {rho lapF divWeighted : ℝ} {gradRho gradV gradF : E}
    (hdiv : divWeighted = rho * lapF + inner ℝ gradRho gradF)
    (hgrad : gradRho = (-rho) • gradV) :
    divWeighted = rho * (lapF - inner ℝ gradV gradF) := by
  calc
    divWeighted = rho * lapF + inner ℝ gradRho gradF := hdiv
    _ = rho * lapF + inner ℝ ((-rho) • gradV) gradF := by rw [hgrad]
    _ = rho * lapF + (-rho) * inner ℝ gradV gradF := by
      simp [real_inner_smul_left]
    _ = rho * (lapF - inner ℝ gradV gradF) := by ring

/-- Source-facing specialization of
`weightedDivergence_gibbsWeight_langevinGenerator_algebra` with the Gibbs weight
`rho = exp (-Vx)`.  This is still only algebra after the product-rule and
chain-rule facts have been supplied. -/
theorem expNeg_weightedDivergence_langevinGenerator_algebra
    {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    {Vx lapF divWeighted : ℝ} {gradRho gradV gradF : E}
    (hdiv :
      divWeighted =
        Real.exp (-Vx) * lapF + inner ℝ gradRho gradF)
    (hgrad : gradRho = (-(Real.exp (-Vx))) • gradV) :
    divWeighted =
      Real.exp (-Vx) * (lapF - inner ℝ gradV gradF) :=
  weightedDivergence_gibbsWeight_langevinGenerator_algebra hdiv hgrad

/-- Finite-coordinate aggregation of supplied product-rule and chain-rule
identities for the weighted-divergence form of the Langevin generator.

Here `divCoord i` represents the already-supplied coordinate derivative
`∂ᵢ (rho * ∂ᵢ f)`, `hessDiag i` represents `∂ᵢᵢ f`, and `gradRho`,
`gradV`, `gradF` are coordinate representatives.  This theorem only sums those
coordinate algebra facts and factors the scalar `rho`; it does not define or
prove partial derivatives, gradients, divergence, or the Laplacian. -/
theorem finiteCoord_weightedDivergence_langevinGenerator_algebra
    {ι : Type*} [Fintype ι]
    {rho : ℝ} {divCoord hessDiag gradRho gradV gradF : ι → ℝ}
    (hdiv : ∀ i, divCoord i = rho * hessDiag i + gradRho i * gradF i)
    (hgrad : ∀ i, gradRho i = -rho * gradV i) :
    (∑ i, divCoord i) =
      rho * ((∑ i, hessDiag i) - ∑ i, gradV i * gradF i) := by
  have hsumHess : (∑ i, rho * hessDiag i) = rho * ∑ i, hessDiag i := by
    rw [Finset.mul_sum]
  have hsumDrift : (∑ i, (-rho * gradV i) * gradF i) =
      -rho * ∑ i, gradV i * gradF i := by
    calc
      (∑ i, (-rho * gradV i) * gradF i) =
          ∑ i, -rho * (gradV i * gradF i) := by
        exact Finset.sum_congr rfl (fun i _ => by ring)
      _ = -rho * ∑ i, gradV i * gradF i := by
        rw [Finset.mul_sum]
  calc
    (∑ i, divCoord i) =
        ∑ i, (rho * hessDiag i + gradRho i * gradF i) := by
      exact Finset.sum_congr rfl (fun i _ => hdiv i)
    _ = ∑ i, (rho * hessDiag i + (-rho * gradV i) * gradF i) := by
      exact Finset.sum_congr rfl (fun i _ => by rw [hgrad i])
    _ = rho * ((∑ i, hessDiag i) - ∑ i, gradV i * gradF i) := by
      rw [Finset.sum_add_distrib, hsumHess, hsumDrift]
      ring

/-- Named finite-coordinate wrapper for
`finiteCoord_weightedDivergence_langevinGenerator_algebra`.

The hypotheses `hlap` and `hinner` are supplied identifications of the
coordinate sums with a named Laplacian scalar and a named gradient inner-product
scalar.  The theorem does not prove those identifications. -/
theorem finiteCoord_named_weightedDivergence_langevinGenerator_algebra
    {ι : Type*} [Fintype ι]
    {rho lapF divWeighted innerGradVGradF : ℝ}
    {divCoord hessDiag gradRho gradV gradF : ι → ℝ}
    (hdivWeighted : divWeighted = ∑ i, divCoord i)
    (hdiv : ∀ i, divCoord i = rho * hessDiag i + gradRho i * gradF i)
    (hgrad : ∀ i, gradRho i = -rho * gradV i)
    (hlap : lapF = ∑ i, hessDiag i)
    (hinner : innerGradVGradF = ∑ i, gradV i * gradF i) :
    divWeighted = rho * (lapF - innerGradVGradF) := by
  calc
    divWeighted = ∑ i, divCoord i := hdivWeighted
    _ = rho * ((∑ i, hessDiag i) - ∑ i, gradV i * gradF i) :=
      finiteCoord_weightedDivergence_langevinGenerator_algebra hdiv hgrad
    _ = rho * (lapF - innerGradVGradF) := by rw [hlap, hinner]

/-- Finite-coordinate Langevin divergence-form handoff using the Mathlib
`EuclideanSpace` inner-product notation for the coordinate gradients.

The coordinate product rule, Gibbs-weight chain rule, and Laplacian-coordinate
identification are still supplied as hypotheses.  This theorem only combines
the finite-coordinate algebra with the reusable Euclidean coordinate
inner-product bridge. -/
theorem finiteCoord_toLpInner_weightedDivergence_langevinGenerator_algebra
    {ι : Type*} [Fintype ι]
    {rho lapF divWeighted : ℝ}
    {divCoord hessDiag gradRho gradV gradF : ι → ℝ}
    (hdivWeighted : divWeighted = ∑ i, divCoord i)
    (hdiv : ∀ i, divCoord i = rho * hessDiag i + gradRho i * gradF i)
    (hgrad : ∀ i, gradRho i = -rho * gradV i)
    (hlap : lapF = ∑ i, hessDiag i) :
    divWeighted =
      rho * (lapF - inner ℝ (WithLp.toLp 2 gradV : EuclideanSpace ℝ ι)
        (WithLp.toLp 2 gradF : EuclideanSpace ℝ ι)) := by
  have hinner :
      inner ℝ (WithLp.toLp 2 gradV : EuclideanSpace ℝ ι)
        (WithLp.toLp 2 gradF : EuclideanSpace ℝ ι) =
        ∑ i, gradV i * gradF i :=
    _root_.AutoSamplingTheory.TechnicalLemmas.Geometry.EuclideanSpaceCoordinates.euclideanSpace_inner_toLp_toLp_eq_sum_mul
      gradV gradF
  calc
    divWeighted = ∑ i, divCoord i := hdivWeighted
    _ = rho * ((∑ i, hessDiag i) - ∑ i, gradV i * gradF i) :=
      finiteCoord_weightedDivergence_langevinGenerator_algebra hdiv hgrad
    _ = rho * (lapF - inner ℝ (WithLp.toLp 2 gradV : EuclideanSpace ℝ ι)
        (WithLp.toLp 2 gradF : EuclideanSpace ℝ ι)) := by rw [hlap, hinner]

/-- Finite-coordinate Langevin divergence-form handoff using direct
`EuclideanSpace` inner-product notation for supplied coordinate gradients.

The coordinate product rule, Gibbs-weight chain rule, and Laplacian-coordinate
identification are still supplied as hypotheses.  This theorem only combines
the finite-coordinate algebra with the reusable Euclidean coordinate
inner-product bridge. -/
theorem finiteCoord_euclideanInner_weightedDivergence_langevinGenerator_algebra
    {ι : Type*} [Fintype ι]
    {rho lapF divWeighted : ℝ}
    {divCoord hessDiag gradRho : ι → ℝ}
    {gradV gradF : EuclideanSpace ℝ ι}
    (hdivWeighted : divWeighted = ∑ i, divCoord i)
    (hdiv : ∀ i, divCoord i = rho * hessDiag i + gradRho i * gradF i)
    (hgrad : ∀ i, gradRho i = -rho * gradV i)
    (hlap : lapF = ∑ i, hessDiag i) :
    divWeighted = rho * (lapF - inner ℝ gradV gradF) := by
  have hinner :
      inner ℝ gradV gradF = ∑ i, gradV i * gradF i :=
    _root_.AutoSamplingTheory.TechnicalLemmas.Geometry.EuclideanSpaceCoordinates.euclideanSpace_inner_eq_sum_mul
      gradV gradF
  exact finiteCoord_named_weightedDivergence_langevinGenerator_algebra
    hdivWeighted hdiv hgrad hlap hinner

/-- Pointwise finite-dimensional Euclidean display of the formal Langevin
differential expression.

This rewrites Mathlib's `Laplacian.laplacian f x - inner ℝ (gradient V x)
(gradient f x)` into a finite coordinate-basis second-derivative sum minus the
coordinate inner-product sum.  It is only a pointwise display identity using
Mathlib's total `gradient` and `Laplacian.laplacian` definitions.  It does not
prove divergence identities, product rules, IBP, stationarity, reversibility,
or any invariant Gibbs law. -/
theorem finiteEuclidean_langevinGenerator_basisDisplay
    {ι : Type*} [Fintype ι]
    (V f : EuclideanSpace ℝ ι → ℝ) (x : EuclideanSpace ℝ ι) :
    Laplacian.laplacian f x - inner ℝ (gradient V x) (gradient f x) =
      (∑ i, iteratedFDeriv ℝ 2 f x
        ![(EuclideanSpace.basisFun ι ℝ) i, (EuclideanSpace.basisFun ι ℝ) i]) -
        ∑ i, (gradient V x) i * (gradient f x) i := by
  have hlap_fun :
      Laplacian.laplacian f =
        fun x => ∑ i, iteratedFDeriv ℝ 2 f x
          ![(EuclideanSpace.basisFun ι ℝ) i, (EuclideanSpace.basisFun ι ℝ) i] :=
    InnerProductSpace.laplacian_eq_iteratedFDeriv_orthonormalBasis f
      (EuclideanSpace.basisFun ι ℝ)
  have hlap :
      Laplacian.laplacian f x =
        ∑ i, iteratedFDeriv ℝ 2 f x
          ![(EuclideanSpace.basisFun ι ℝ) i, (EuclideanSpace.basisFun ι ℝ) i] :=
    congrFun hlap_fun x
  have hinner :
      inner ℝ (gradient V x) (gradient f x) =
        ∑ i, (gradient V x) i * (gradient f x) i :=
    _root_.AutoSamplingTheory.TechnicalLemmas.Geometry.EuclideanSpaceCoordinates.euclideanSpace_inner_eq_sum_mul
      (gradient V x) (gradient f x)
  rw [hlap, hinner]

/-- Explicit coordinate-unit version of
`finiteEuclidean_langevinGenerator_basisDisplay`.

The additional `[DecidableEq ι]` instance is only used to unfold Mathlib's
`EuclideanSpace.basisFun` into `EuclideanSpace.single i 1`. -/
theorem finiteEuclidean_langevinGenerator_coordinateDisplay
    {ι : Type*} [Fintype ι] [DecidableEq ι]
    (V f : EuclideanSpace ℝ ι → ℝ) (x : EuclideanSpace ℝ ι) :
    Laplacian.laplacian f x - inner ℝ (gradient V x) (gradient f x) =
      (∑ i, iteratedFDeriv ℝ 2 f x
        ![(EuclideanSpace.single i (1 : ℝ)), (EuclideanSpace.single i (1 : ℝ))]) -
        ∑ i, (gradient V x) i * (gradient f x) i := by
  simpa [EuclideanSpace.basisFun_apply] using
    finiteEuclidean_langevinGenerator_basisDisplay V f x

/-- Supplied-hypothesis finite-coordinate handoff from weighted-divergence
algebra to the Mathlib pointwise expression `Δ f - <∇V, ∇f>`.

The hypotheses still provide the coordinate product-rule output, the
Gibbs-weight chain-rule output, and the coordinate divergence sum.  This theorem
only replaces the coordinate second-derivative and gradient-product sums by
Mathlib's `Laplacian.laplacian` and `gradient` display. -/
theorem finiteEuclidean_weightedDivergence_langevinGenerator_basisHandoff
    {ι : Type*} [Fintype ι]
    {rho divWeighted : ℝ}
    {V f : EuclideanSpace ℝ ι → ℝ} {x : EuclideanSpace ℝ ι}
    {divCoord gradRho : ι → ℝ}
    (hdivWeighted : divWeighted = ∑ i, divCoord i)
    (hdiv : ∀ i,
      divCoord i =
        rho * iteratedFDeriv ℝ 2 f x
          ![(EuclideanSpace.basisFun ι ℝ) i, (EuclideanSpace.basisFun ι ℝ) i] +
        gradRho i * (gradient f x) i)
    (hgrad : ∀ i, gradRho i = -rho * (gradient V x) i) :
    divWeighted =
      rho * (Laplacian.laplacian f x -
        inner ℝ (gradient V x) (gradient f x)) := by
  have hcoord :
      (∑ i, divCoord i) =
        rho *
          ((∑ i, iteratedFDeriv ℝ 2 f x
            ![(EuclideanSpace.basisFun ι ℝ) i, (EuclideanSpace.basisFun ι ℝ) i]) -
            ∑ i, (gradient V x) i * (gradient f x) i) :=
    finiteCoord_weightedDivergence_langevinGenerator_algebra
      (rho := rho)
      (divCoord := divCoord)
      (hessDiag := fun i =>
        iteratedFDeriv ℝ 2 f x
          ![(EuclideanSpace.basisFun ι ℝ) i, (EuclideanSpace.basisFun ι ℝ) i])
      (gradRho := gradRho)
      (gradV := fun i => (gradient V x) i)
      (gradF := fun i => (gradient f x) i)
      hdiv hgrad
  have hdisplay := finiteEuclidean_langevinGenerator_basisDisplay V f x
  calc
    divWeighted = ∑ i, divCoord i := hdivWeighted
    _ = rho *
        ((∑ i, iteratedFDeriv ℝ 2 f x
          ![(EuclideanSpace.basisFun ι ℝ) i, (EuclideanSpace.basisFun ι ℝ) i]) -
          ∑ i, (gradient V x) i * (gradient f x) i) := hcoord
    _ = rho * (Laplacian.laplacian f x -
        inner ℝ (gradient V x) (gradient f x)) := by rw [← hdisplay]

/-- Explicit coordinate-unit version of
`finiteEuclidean_weightedDivergence_langevinGenerator_basisHandoff`.

This is still a supplied-hypothesis algebra/display handoff.  The theorem does
not prove the coordinate product rule, divergence theorem, integration by
parts, stationarity, reversibility, or any semigroup-generator statement. -/
theorem finiteEuclidean_weightedDivergence_langevinGenerator_coordinateHandoff
    {ι : Type*} [Fintype ι] [DecidableEq ι]
    {rho divWeighted : ℝ}
    {V f : EuclideanSpace ℝ ι → ℝ} {x : EuclideanSpace ℝ ι}
    {divCoord gradRho : ι → ℝ}
    (hdivWeighted : divWeighted = ∑ i, divCoord i)
    (hdiv : ∀ i,
      divCoord i =
        rho * iteratedFDeriv ℝ 2 f x
          ![(EuclideanSpace.single i (1 : ℝ)), (EuclideanSpace.single i (1 : ℝ))] +
        gradRho i * (gradient f x) i)
    (hgrad : ∀ i, gradRho i = -rho * (gradient V x) i) :
    divWeighted =
      rho * (Laplacian.laplacian f x -
        inner ℝ (gradient V x) (gradient f x)) := by
  have hcoord :
      (∑ i, divCoord i) =
        rho *
          ((∑ i, iteratedFDeriv ℝ 2 f x
            ![(EuclideanSpace.single i (1 : ℝ)), (EuclideanSpace.single i (1 : ℝ))]) -
            ∑ i, (gradient V x) i * (gradient f x) i) :=
    finiteCoord_weightedDivergence_langevinGenerator_algebra
      (rho := rho)
      (divCoord := divCoord)
      (hessDiag := fun i =>
        iteratedFDeriv ℝ 2 f x
          ![(EuclideanSpace.single i (1 : ℝ)), (EuclideanSpace.single i (1 : ℝ))])
      (gradRho := gradRho)
      (gradV := fun i => (gradient V x) i)
      (gradF := fun i => (gradient f x) i)
      hdiv hgrad
  have hdisplay := finiteEuclidean_langevinGenerator_coordinateDisplay V f x
  calc
    divWeighted = ∑ i, divCoord i := hdivWeighted
    _ = rho *
        ((∑ i, iteratedFDeriv ℝ 2 f x
          ![(EuclideanSpace.single i (1 : ℝ)), (EuclideanSpace.single i (1 : ℝ))]) -
          ∑ i, (gradient V x) i * (gradient f x) i) := hcoord
    _ = rho * (Laplacian.laplacian f x -
        inner ℝ (gradient V x) (gradient f x)) := by rw [← hdisplay]

/-- Basis-coordinate handoff with the Gibbs-weight chain rule discharged by
Mathlib's gradient API.

The coordinate product-rule output and divergence-sum identity remain supplied
as hypotheses.  The only removed hypothesis compared with
`finiteEuclidean_weightedDivergence_langevinGenerator_basisHandoff` is the
coordinate Gibbs-weight gradient identity
`∇ exp(-V) = -exp(-V) ∇V`, obtained here from `DifferentiableAt ℝ V x`.

This does not prove the coordinate product rule, divergence theorem,
integration by parts, no-boundary term, semigroup/Ito generator result,
stationarity, reversibility, invariant Gibbs law, or KL/FI dissipation. -/
theorem finiteEuclidean_expNeg_weightedDivergence_langevinGenerator_basisHandoff
    {ι : Type*} [Fintype ι]
    {divWeighted : ℝ}
    {V f : EuclideanSpace ℝ ι → ℝ} {x : EuclideanSpace ℝ ι}
    {divCoord : ι → ℝ}
    (hV : DifferentiableAt ℝ V x)
    (hdivWeighted : divWeighted = ∑ i, divCoord i)
    (hdiv : ∀ i,
      divCoord i =
        Real.exp (-V x) * iteratedFDeriv ℝ 2 f x
          ![(EuclideanSpace.basisFun ι ℝ) i, (EuclideanSpace.basisFun ι ℝ) i] +
        (gradient (fun y : EuclideanSpace ℝ ι => Real.exp (-V y)) x) i *
          (gradient f x) i) :
    divWeighted =
      Real.exp (-V x) * (Laplacian.laplacian f x -
        inner ℝ (gradient V x) (gradient f x)) := by
  exact finiteEuclidean_weightedDivergence_langevinGenerator_basisHandoff
    (rho := Real.exp (-V x))
    (divWeighted := divWeighted)
    (V := V) (f := f) (x := x)
    (divCoord := divCoord)
    (gradRho := fun i =>
      (gradient (fun y : EuclideanSpace ℝ ι => Real.exp (-V y)) x) i)
    hdivWeighted hdiv
    (fun i =>
      _root_.AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Gradient.gradient_expNegPotential_coordinate_eq_of_differentiableAt
        (V := V) (x := x) hV i)

/-- Coordinate-unit version of
`finiteEuclidean_expNeg_weightedDivergence_langevinGenerator_basisHandoff`.

This removes only the Gibbs-weight chain-rule hypothesis from the explicit
coordinate-unit display.  Divergence, coordinate product-rule, IBP, generator
domains, stationarity, reversibility, invariant Gibbs law, and KL/FI
dissipation remain separate red branches. -/
theorem finiteEuclidean_expNeg_weightedDivergence_langevinGenerator_coordinateHandoff
    {ι : Type*} [Fintype ι] [DecidableEq ι]
    {divWeighted : ℝ}
    {V f : EuclideanSpace ℝ ι → ℝ} {x : EuclideanSpace ℝ ι}
    {divCoord : ι → ℝ}
    (hV : DifferentiableAt ℝ V x)
    (hdivWeighted : divWeighted = ∑ i, divCoord i)
    (hdiv : ∀ i,
      divCoord i =
        Real.exp (-V x) * iteratedFDeriv ℝ 2 f x
          ![(EuclideanSpace.single i (1 : ℝ)), (EuclideanSpace.single i (1 : ℝ))] +
        (gradient (fun y : EuclideanSpace ℝ ι => Real.exp (-V y)) x) i *
          (gradient f x) i) :
    divWeighted =
      Real.exp (-V x) * (Laplacian.laplacian f x -
        inner ℝ (gradient V x) (gradient f x)) := by
  exact finiteEuclidean_weightedDivergence_langevinGenerator_coordinateHandoff
    (rho := Real.exp (-V x))
    (divWeighted := divWeighted)
    (V := V) (f := f) (x := x)
    (divCoord := divCoord)
    (gradRho := fun i =>
      (gradient (fun y : EuclideanSpace ℝ ι => Real.exp (-V y)) x) i)
    hdivWeighted hdiv
    (fun i =>
      _root_.AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Gradient.gradient_expNegPotential_coordinate_eq_of_differentiableAt
        (V := V) (x := x) hV i)

/-- Coordinate-line-derivative sum display for the explicit Gibbs-weighted
first-derivative field.

This theorem aggregates the compiled pointwise leaf
`lineDeriv_expNegPotential_mul_fderiv_coordinate_eq` across all finite
coordinates and then calls the existing Euclidean Langevin display handoff.
It removes the supplied coordinate product-rule/Hessian-diagonal hypothesis
from `finiteEuclidean_expNeg_weightedDivergence_langevinGenerator_coordinateHandoff`
for the specific field
`x ↦ exp (-V x) * fderiv ℝ f x eᵢ`.

The hypothesis `hgradF` is intentionally still supplied: it is the pointwise
identification of the `fderiv` coordinate slice with Mathlib's `gradient`
coordinate.  This theorem does not define a divergence operator, assert that
the displayed sum is the divergence of a vector field, prove integration by
parts, establish a semigroup-generator/domain theorem, or prove stationarity,
reversibility, invariant Gibbs law, or KL/FI dissipation. -/
theorem finiteEuclidean_expNeg_lineDeriv_fderiv_coordinateSum_langevinGenerator_display
    {ι : Type*} [Fintype ι] [DecidableEq ι]
    {V f : EuclideanSpace ℝ ι → ℝ} {x : EuclideanSpace ℝ ι}
    (hV : DifferentiableAt ℝ V x)
    (hf : DifferentiableAt ℝ
      (fun y : EuclideanSpace ℝ ι => fderiv ℝ f y) x)
    (hgradF : ∀ i,
      fderiv ℝ f x (EuclideanSpace.single i (1 : ℝ)) = (gradient f x) i) :
    (∑ i, lineDeriv ℝ
        (fun y : EuclideanSpace ℝ ι =>
          Real.exp (-V y) * fderiv ℝ f y (EuclideanSpace.single i (1 : ℝ)))
        x (EuclideanSpace.single i (1 : ℝ))) =
      Real.exp (-V x) * (Laplacian.laplacian f x -
        inner ℝ (gradient V x) (gradient f x)) := by
  have hcoordLineDeriv : ∀ i,
      lineDeriv ℝ
        (fun y : EuclideanSpace ℝ ι =>
          Real.exp (-V y) * fderiv ℝ f y (EuclideanSpace.single i (1 : ℝ)))
        x (EuclideanSpace.single i (1 : ℝ)) =
        Real.exp (-V x) * iteratedFDeriv ℝ 2 f x
          ![(EuclideanSpace.single i (1 : ℝ)), (EuclideanSpace.single i (1 : ℝ))] +
        (gradient (fun y : EuclideanSpace ℝ ι => Real.exp (-V y)) x) i *
          (gradient f x) i := by
    intro i
    have hline :=
      _root_.AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.LineDeriv.lineDeriv_expNegPotential_mul_fderiv_coordinate_eq
        (V := V) (f := f) (x := x) i hV hf
    have hgradRho :=
      _root_.AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Gradient.gradient_expNegPotential_coordinate_eq_of_differentiableAt
        (V := V) (x := x) hV i
    calc
      lineDeriv ℝ
          (fun y : EuclideanSpace ℝ ι =>
            Real.exp (-V y) * fderiv ℝ f y (EuclideanSpace.single i (1 : ℝ)))
          x (EuclideanSpace.single i (1 : ℝ)) =
        Real.exp (-V x) * iteratedFDeriv ℝ 2 f x
          ![(EuclideanSpace.single i (1 : ℝ)), (EuclideanSpace.single i (1 : ℝ))] -
        Real.exp (-V x) * (gradient V x) i *
          fderiv ℝ f x (EuclideanSpace.single i (1 : ℝ)) := by
        simpa only [EuclideanSpace.single, PiLp.single] using hline
      _ = Real.exp (-V x) * iteratedFDeriv ℝ 2 f x
          ![(EuclideanSpace.single i (1 : ℝ)), (EuclideanSpace.single i (1 : ℝ))] +
        (gradient (fun y : EuclideanSpace ℝ ι => Real.exp (-V y)) x) i *
          (gradient f x) i := by
        rw [hgradF i, hgradRho]
        ring
  exact finiteEuclidean_expNeg_weightedDivergence_langevinGenerator_coordinateHandoff
    (V := V) (f := f) (x := x)
    (divCoord := fun i => lineDeriv ℝ
        (fun y : EuclideanSpace ℝ ι =>
          Real.exp (-V y) * fderiv ℝ f y (EuclideanSpace.single i (1 : ℝ)))
        x (EuclideanSpace.single i (1 : ℝ)))
    hV rfl hcoordLineDeriv

/-- Coordinate-line-derivative sum display with the local gradient-coordinate
bridge discharged.

Compared with
`finiteEuclidean_expNeg_lineDeriv_fderiv_coordinateSum_langevinGenerator_display`,
this theorem removes the supplied hypothesis
`fderiv ℝ f x eᵢ = (gradient f x) i` using the pointwise
`fderiv`/`gradient` coordinate bridge from `DifferentiableAt ℝ f x`.

It is still only a pointwise finite-coordinate sum display.  It does not define
a divergence operator, assert that the sum is a divergence, prove integration
by parts, establish generator domains, or prove invariant Gibbs law,
reversibility, or KL/FI dissipation. -/
theorem finiteEuclidean_expNeg_lineDeriv_fderiv_coordinateSum_langevinGenerator_display_of_differentiableAt
    {ι : Type*} [Fintype ι] [DecidableEq ι]
    {V f : EuclideanSpace ℝ ι → ℝ} {x : EuclideanSpace ℝ ι}
    (hV : DifferentiableAt ℝ V x)
    (hfderiv : DifferentiableAt ℝ
      (fun y : EuclideanSpace ℝ ι => fderiv ℝ f y) x)
    (hf : DifferentiableAt ℝ f x) :
    (∑ i, lineDeriv ℝ
        (fun y : EuclideanSpace ℝ ι =>
          Real.exp (-V y) * fderiv ℝ f y (EuclideanSpace.single i (1 : ℝ)))
        x (EuclideanSpace.single i (1 : ℝ))) =
      Real.exp (-V x) * (Laplacian.laplacian f x -
        inner ℝ (gradient V x) (gradient f x)) :=
  finiteEuclidean_expNeg_lineDeriv_fderiv_coordinateSum_langevinGenerator_display
    (V := V) (f := f) (x := x) hV hfderiv
    (fun i =>
      _root_.AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Gradient.fderiv_apply_coordinate_eq_gradient_coordinate_of_differentiableAt
        (f := f) (x := x) i hf)

/-- Named coordinate-divergence version of the finite Euclidean Gibbs-weighted
first-derivative display.

The vector field is the coordinate representative
`y ↦ exp (-V y) * fderiv ℝ f y eᵢ`.  The theorem only rewrites the compiled
coordinate-sum display through the local pointwise `coordinateDivergence`
definition.  It does not identify this with any integration theorem, prove
weighted integration by parts, establish generator domains, or prove invariant
Gibbs law, reversibility, or KL/FI dissipation. -/
theorem coordinateDivergence_expNeg_fderivCoordinateField_langevinGenerator_display_of_differentiableAt
    {ι : Type*} [Fintype ι] [DecidableEq ι]
    {V f : EuclideanSpace ℝ ι → ℝ} {x : EuclideanSpace ℝ ι}
    (hV : DifferentiableAt ℝ V x)
    (hfderiv : DifferentiableAt ℝ
      (fun y : EuclideanSpace ℝ ι => fderiv ℝ f y) x)
    (hf : DifferentiableAt ℝ f x) :
    _root_.AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence.coordinateDivergence
      (fun y : EuclideanSpace ℝ ι =>
        (WithLp.toLp 2 (fun i =>
          Real.exp (-V y) * fderiv ℝ f y (EuclideanSpace.single i (1 : ℝ))) :
          EuclideanSpace ℝ ι)) x =
      Real.exp (-V x) * (Laplacian.laplacian f x -
        inner ℝ (gradient V x) (gradient f x)) := by
  dsimp [
    _root_.AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence.coordinateDivergence]
  simpa using
    finiteEuclidean_expNeg_lineDeriv_fderiv_coordinateSum_langevinGenerator_display_of_differentiableAt
      (V := V) (f := f) (x := x) hV hfderiv hf

/-- Trace-summand display for the explicit Pi-space vector field
`x ↦ exp (-V x) * fderiv f x eᵢ`.

This is the pointwise bridge from Mathlib's finite-box divergence-theorem trace
integrand to the Langevin display
`exp (-V) * (Δ f - <∇V, ∇f>)`.  It uses the supplied Frechet derivative of the
explicit Pi-space vector field, plus pointwise differentiability assumptions
needed by the compiled coordinate-divergence display.

It does not prove that the supplied derivative exists on a box, prove
continuity or integrability, invoke a divergence theorem, cancel boundary
terms, establish weighted integration by parts, define a generator domain, or
prove invariant/reversible Gibbs laws. -/
theorem trace_expNeg_fderivCoordinateField_langevinGenerator_display_of_hasFDerivAt
    {n : ℕ}
    {V f : EuclideanSpace ℝ (Fin (n + 1)) → ℝ}
    {x : Fin (n + 1) → ℝ}
    {F' : (Fin (n + 1) → ℝ) →L[ℝ] (Fin (n + 1) → ℝ)}
    (hF : HasFDerivAt
      (fun z : Fin (n + 1) → ℝ => fun i =>
        Real.exp (-V (WithLp.toLp 2 z : EuclideanSpace ℝ (Fin (n + 1)))) *
          fderiv ℝ f (WithLp.toLp 2 z : EuclideanSpace ℝ (Fin (n + 1)))
            (EuclideanSpace.single i (1 : ℝ))) F' x)
    (hV : DifferentiableAt ℝ V
      (WithLp.toLp 2 x : EuclideanSpace ℝ (Fin (n + 1))))
    (hfderiv : DifferentiableAt ℝ
      (fun y : EuclideanSpace ℝ (Fin (n + 1)) => fderiv ℝ f y)
      (WithLp.toLp 2 x : EuclideanSpace ℝ (Fin (n + 1))))
    (hf : DifferentiableAt ℝ f
      (WithLp.toLp 2 x : EuclideanSpace ℝ (Fin (n + 1)))) :
    (∑ i, F' (Pi.single i (1 : ℝ)) i) =
      Real.exp (-V (WithLp.toLp 2 x : EuclideanSpace ℝ (Fin (n + 1)))) *
        (Laplacian.laplacian f
            (WithLp.toLp 2 x : EuclideanSpace ℝ (Fin (n + 1))) -
          inner ℝ
            (gradient V (WithLp.toLp 2 x : EuclideanSpace ℝ (Fin (n + 1))))
            (gradient f (WithLp.toLp 2 x : EuclideanSpace ℝ (Fin (n + 1))))) := by
  have htrace :=
    _root_.AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence.coordinateDivergence_wrapped_toPi_trace_of_hasFDerivAt
      (ι := Fin (n + 1)) hF
  have hdisplay :=
    coordinateDivergence_expNeg_fderivCoordinateField_langevinGenerator_display_of_differentiableAt
      (V := V) (f := f)
      (x := (WithLp.toLp 2 x : EuclideanSpace ℝ (Fin (n + 1)))) hV hfderiv hf
  rw [← htrace]
  simpa using hdisplay

/-- Continuity of the scalar Langevin display on a finite Pi-box from
component continuity.

The hypotheses keep the analytic regularity inputs explicit: continuity of the
potential, the Mathlib Laplacian display, and the two gradient fields after the
`WithLp.toLp 2` coordinate bridge.  The theorem only assembles these component
facts into continuity of
`exp (-V) * (Δ f - <∇V, ∇f>)`.

It does not prove that the components are continuous from a `ContDiff` or
test-function class, does not prove differentiability of the explicit vector
field, and does not prove trace integrability, IBP, boundary cancellation,
generator domains, invariant laws, reversibility, or KL/FI dissipation. -/
theorem continuousOn_expNeg_langevinGenerator_rhs_of_components
    {n : ℕ}
    {a b : Fin (n + 1) → ℝ}
    {V f : EuclideanSpace ℝ (Fin (n + 1)) → ℝ}
    (hV : ContinuousOn
      (fun x : Fin (n + 1) → ℝ =>
        V (WithLp.toLp 2 x : EuclideanSpace ℝ (Fin (n + 1))))
      (Set.Icc a b))
    (hlap : ContinuousOn
      (fun x : Fin (n + 1) → ℝ =>
        Laplacian.laplacian f (WithLp.toLp 2 x : EuclideanSpace ℝ (Fin (n + 1))))
      (Set.Icc a b))
    (hgradV : ContinuousOn
      (fun x : Fin (n + 1) → ℝ =>
        gradient V (WithLp.toLp 2 x : EuclideanSpace ℝ (Fin (n + 1))))
      (Set.Icc a b))
    (hgradf : ContinuousOn
      (fun x : Fin (n + 1) → ℝ =>
        gradient f (WithLp.toLp 2 x : EuclideanSpace ℝ (Fin (n + 1))))
      (Set.Icc a b)) :
    ContinuousOn
      (fun x : Fin (n + 1) → ℝ =>
        Real.exp (-V (WithLp.toLp 2 x : EuclideanSpace ℝ (Fin (n + 1)))) *
          (Laplacian.laplacian f
              (WithLp.toLp 2 x : EuclideanSpace ℝ (Fin (n + 1))) -
            inner ℝ
              (gradient V (WithLp.toLp 2 x : EuclideanSpace ℝ (Fin (n + 1))))
              (gradient f (WithLp.toLp 2 x : EuclideanSpace ℝ (Fin (n + 1)))))) 
      (Set.Icc a b) := by
  exact hV.neg.rexp.mul (hlap.sub (hgradV.inner hgradf))

/-- Continuity of the scalar Langevin display on a finite Pi-box from global
`C¹/C²` test-function regularity.

The assumptions are deliberately global total-derivative hypotheses:
`V` is `C¹` and `f` is `C²` on the finite-dimensional Euclidean space.  The
theorem only derives the four component `ContinuousOn` inputs needed by
`continuousOn_expNeg_langevinGenerator_rhs_of_components` and then assembles
the scalar display
`exp (-V) * (Δ f - <∇V, ∇f>)`.

It does not prove a closed-box `ContDiffOn` variant, differentiability of the
explicit Pi-space trace field, trace integrability, weighted IBP, boundary
cancellation, generator domains, invariant laws, reversibility, or KL/FI
dissipation. -/
theorem continuousOn_expNeg_langevinGenerator_rhs_of_contDiff
    {n : ℕ}
    {a b : Fin (n + 1) → ℝ}
    {V f : EuclideanSpace ℝ (Fin (n + 1)) → ℝ}
    (hV : ContDiff ℝ 1 V)
    (hf : ContDiff ℝ 2 f) :
    ContinuousOn
      (fun x : Fin (n + 1) → ℝ =>
        Real.exp (-V (WithLp.toLp 2 x : EuclideanSpace ℝ (Fin (n + 1)))) *
          (Laplacian.laplacian f
              (WithLp.toLp 2 x : EuclideanSpace ℝ (Fin (n + 1))) -
            inner ℝ
              (gradient V (WithLp.toLp 2 x : EuclideanSpace ℝ (Fin (n + 1))))
              (gradient f (WithLp.toLp 2 x : EuclideanSpace ℝ (Fin (n + 1))))))
      (Set.Icc a b) := by
  have hV_cont : ContinuousOn
      (fun x : Fin (n + 1) → ℝ =>
        V (WithLp.toLp 2 x : EuclideanSpace ℝ (Fin (n + 1))))
      (Set.Icc a b) :=
    (hV.continuous.comp (PiLp.continuous_toLp 2 _)).continuousOn
  have hlap_cont : ContinuousOn
      (fun x : Fin (n + 1) → ℝ =>
        Laplacian.laplacian f (WithLp.toLp 2 x : EuclideanSpace ℝ (Fin (n + 1))))
      (Set.Icc a b) :=
    ((_root_.AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Laplacian.continuous_laplacian_of_contDiff_two hf).comp
      (PiLp.continuous_toLp 2 _)).continuousOn
  have hgradV_cont : ContinuousOn
      (fun x : Fin (n + 1) → ℝ =>
        gradient V (WithLp.toLp 2 x : EuclideanSpace ℝ (Fin (n + 1))))
      (Set.Icc a b) :=
    ((_root_.AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Gradient.continuous_gradient_of_contDiff_one hV).comp
      (PiLp.continuous_toLp 2 _)).continuousOn
  have hgradf_cont : ContinuousOn
      (fun x : Fin (n + 1) → ℝ =>
        gradient f (WithLp.toLp 2 x : EuclideanSpace ℝ (Fin (n + 1))))
      (Set.Icc a b) :=
    ((_root_.AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Gradient.continuous_gradient_of_contDiff_one
        (hf.of_le (by norm_num))).comp
      (PiLp.continuous_toLp 2 _)).continuousOn
  exact continuousOn_expNeg_langevinGenerator_rhs_of_components
    hV_cont hlap_cont hgradV_cont hgradf_cont

/-- The explicit Pi-space vector field
`z ↦ (i ↦ exp (-V (toLp z)) * fderiv f (toLp z) eᵢ)` is differentiable when
the potential is differentiable and the total first-derivative map of `f` is
differentiable at the transported point.

The derivative representative is intentionally chosen to be Mathlib's own
`fderiv`; this avoids claiming a closed-form Jacobian for the product/chain
rule.  This is the smallest field-differentiability leaf needed by the finite
box trace integrability handoff. -/
theorem hasFDerivAt_expNeg_fderivCoordinateField_of_differentiableAt
    {n : ℕ}
    {V f : EuclideanSpace ℝ (Fin (n + 1)) → ℝ}
    {x : Fin (n + 1) → ℝ}
    (hV : DifferentiableAt ℝ V
      (WithLp.toLp 2 x : EuclideanSpace ℝ (Fin (n + 1))))
    (hfderiv : DifferentiableAt ℝ
      (fun y : EuclideanSpace ℝ (Fin (n + 1)) => fderiv ℝ f y)
      (WithLp.toLp 2 x : EuclideanSpace ℝ (Fin (n + 1)))) :
    HasFDerivAt
      (fun z : Fin (n + 1) → ℝ => fun i =>
        Real.exp (-V (WithLp.toLp 2 z : EuclideanSpace ℝ (Fin (n + 1)))) *
          fderiv ℝ f (WithLp.toLp 2 z : EuclideanSpace ℝ (Fin (n + 1)))
            (EuclideanSpace.single i (1 : ℝ)))
      (fderiv ℝ
        (fun z : Fin (n + 1) → ℝ => fun i =>
          Real.exp (-V (WithLp.toLp 2 z : EuclideanSpace ℝ (Fin (n + 1)))) *
            fderiv ℝ f (WithLp.toLp 2 z : EuclideanSpace ℝ (Fin (n + 1)))
              (EuclideanSpace.single i (1 : ℝ))) x) x := by
  exact DifferentiableAt.hasFDerivAt <| differentiableAt_pi.2 fun i => by
    have htoLp : DifferentiableAt ℝ
        (fun z : Fin (n + 1) → ℝ =>
          (WithLp.toLp 2 z : EuclideanSpace ℝ (Fin (n + 1)))) x :=
      (PiLp.hasFDerivAt_toLp (𝕜 := ℝ) (E := fun _ : Fin (n + 1) => ℝ) 2 x).differentiableAt
    have hVcomp : DifferentiableAt ℝ
        (fun z : Fin (n + 1) → ℝ =>
          V (WithLp.toLp 2 z : EuclideanSpace ℝ (Fin (n + 1)))) x :=
      hV.comp x htoLp
    have hexp : DifferentiableAt ℝ
        (fun z : Fin (n + 1) → ℝ =>
          Real.exp (-V (WithLp.toLp 2 z : EuclideanSpace ℝ (Fin (n + 1))))) x :=
      hVcomp.neg.exp
    have hfderivComp : DifferentiableAt ℝ
        (fun z : Fin (n + 1) → ℝ =>
          fderiv ℝ f (WithLp.toLp 2 z : EuclideanSpace ℝ (Fin (n + 1)))) x :=
      hfderiv.comp x htoLp
    have hslice : DifferentiableAt ℝ
        (fun z : Fin (n + 1) → ℝ =>
          fderiv ℝ f (WithLp.toLp 2 z : EuclideanSpace ℝ (Fin (n + 1)))
            (EuclideanSpace.single i (1 : ℝ))) x :=
      hfderivComp.clm_apply (differentiableAt_const (EuclideanSpace.single i (1 : ℝ)))
    exact hexp.mul hslice

/-- Global `C¹/C²` version of
`hasFDerivAt_expNeg_fderivCoordinateField_of_differentiableAt`. -/
theorem hasFDerivAt_expNeg_fderivCoordinateField_of_contDiff
    {n : ℕ}
    {V f : EuclideanSpace ℝ (Fin (n + 1)) → ℝ}
    {x : Fin (n + 1) → ℝ}
    (hV : ContDiff ℝ 1 V)
    (hf : ContDiff ℝ 2 f) :
    HasFDerivAt
      (fun z : Fin (n + 1) → ℝ => fun i =>
        Real.exp (-V (WithLp.toLp 2 z : EuclideanSpace ℝ (Fin (n + 1)))) *
          fderiv ℝ f (WithLp.toLp 2 z : EuclideanSpace ℝ (Fin (n + 1)))
            (EuclideanSpace.single i (1 : ℝ)))
      (fderiv ℝ
        (fun z : Fin (n + 1) → ℝ => fun i =>
          Real.exp (-V (WithLp.toLp 2 z : EuclideanSpace ℝ (Fin (n + 1)))) *
            fderiv ℝ f (WithLp.toLp 2 z : EuclideanSpace ℝ (Fin (n + 1)))
              (EuclideanSpace.single i (1 : ℝ))) x) x := by
  exact hasFDerivAt_expNeg_fderivCoordinateField_of_differentiableAt
    (V := V) (f := f) (x := x)
    (hV.differentiable one_ne_zero _)
    ((hf.fderiv_right (m := 1) (by norm_num)).differentiable one_ne_zero _)

/-- Finite-box trace integrability for the explicit Gibbs-weighted Langevin
trace display, assuming the displayed scalar RHS is continuous on the box.

This closes the integrability handoff only under explicit regularity data:
the Pi-space vector field has the supplied derivative on the closed box, the
pointwise differentiability hypotheses needed by the Langevin display hold on
the closed box, and the scalar display
`exp (-V) * (Δ f - <∇V, ∇f>)` is continuous on that box.

The theorem does not prove those regularity hypotheses, does not prove
whole-space integrability, does not cancel finite-box face terms, and does not
prove weighted IBP, invariant law, reversibility, stationarity, or KL/FI
dissipation. -/
theorem integrableOn_trace_expNeg_fderivCoordinateField_of_continuousOn
    {n : ℕ}
    (a b : Fin (n + 1) → ℝ)
    (V f : EuclideanSpace ℝ (Fin (n + 1)) → ℝ)
    (F' : (Fin (n + 1) → ℝ) →
      (Fin (n + 1) → ℝ) →L[ℝ] (Fin (n + 1) → ℝ))
    (hF : ∀ x ∈ Set.Icc a b,
      HasFDerivAt
        (fun z : Fin (n + 1) → ℝ => fun i =>
          Real.exp (-V (WithLp.toLp 2 z : EuclideanSpace ℝ (Fin (n + 1)))) *
            fderiv ℝ f (WithLp.toLp 2 z : EuclideanSpace ℝ (Fin (n + 1)))
              (EuclideanSpace.single i (1 : ℝ))) (F' x) x)
    (hV : ∀ x ∈ Set.Icc a b,
      DifferentiableAt ℝ V
        (WithLp.toLp 2 x : EuclideanSpace ℝ (Fin (n + 1))))
    (hfderiv : ∀ x ∈ Set.Icc a b,
      DifferentiableAt ℝ
        (fun y : EuclideanSpace ℝ (Fin (n + 1)) => fderiv ℝ f y)
        (WithLp.toLp 2 x : EuclideanSpace ℝ (Fin (n + 1))))
    (hf : ∀ x ∈ Set.Icc a b,
      DifferentiableAt ℝ f
        (WithLp.toLp 2 x : EuclideanSpace ℝ (Fin (n + 1))))
    (hcont : ContinuousOn
      (fun x : Fin (n + 1) → ℝ =>
        Real.exp (-V (WithLp.toLp 2 x : EuclideanSpace ℝ (Fin (n + 1)))) *
          (Laplacian.laplacian f
              (WithLp.toLp 2 x : EuclideanSpace ℝ (Fin (n + 1))) -
            inner ℝ
              (gradient V (WithLp.toLp 2 x : EuclideanSpace ℝ (Fin (n + 1))))
              (gradient f (WithLp.toLp 2 x : EuclideanSpace ℝ (Fin (n + 1))))))
      (Set.Icc a b)) :
    IntegrableOn (fun x => ∑ i, F' x (Pi.single i (1 : ℝ)) i)
      (Set.Icc a b) volume := by
  have h_exp : IntegrableOn
      (fun x : Fin (n + 1) → ℝ =>
        Real.exp (-V (WithLp.toLp 2 x : EuclideanSpace ℝ (Fin (n + 1)))) *
          (Laplacian.laplacian f
              (WithLp.toLp 2 x : EuclideanSpace ℝ (Fin (n + 1))) -
            inner ℝ
              (gradient V (WithLp.toLp 2 x : EuclideanSpace ℝ (Fin (n + 1))))
              (gradient f (WithLp.toLp 2 x : EuclideanSpace ℝ (Fin (n + 1))))))
      (Set.Icc a b) volume :=
    hcont.integrableOn_compact isCompact_Icc
  refine (integrableOn_congr_fun ?_ measurableSet_Icc).mp h_exp
  intro x hx
  exact (trace_expNeg_fderivCoordinateField_langevinGenerator_display_of_hasFDerivAt
    (V := V) (f := f) (x := x) (F' := F' x)
    (hF x hx) (hV x hx) (hfderiv x hx) (hf x hx)).symm

/-- Finite-box trace integrability for the explicit Gibbs-weighted Langevin
trace display from component continuity.

This is a convenience wrapper around
`integrableOn_trace_expNeg_fderivCoordinateField_of_continuousOn`.  It replaces
the single scalar `ContinuousOn` hypothesis by separate continuity hypotheses
for `V`, `Laplacian.laplacian f`, `gradient V`, and `gradient f`, all after the
`WithLp.toLp 2` coordinate bridge.

It still assumes the explicit Pi-space vector field has the supplied Frechet
derivative on the closed box and that the pointwise differentiability
hypotheses needed by the trace/display equality hold there.  It does not derive
those assumptions from a concrete test-function class, does not cancel face
terms, and does not prove weighted IBP, generator domains, invariant laws,
reversibility, stationarity, or KL/FI dissipation. -/
theorem integrableOn_trace_expNeg_fderivCoordinateField_of_component_continuousOn
    {n : ℕ}
    (a b : Fin (n + 1) → ℝ)
    (V f : EuclideanSpace ℝ (Fin (n + 1)) → ℝ)
    (F' : (Fin (n + 1) → ℝ) →
      (Fin (n + 1) → ℝ) →L[ℝ] (Fin (n + 1) → ℝ))
    (hF : ∀ x ∈ Set.Icc a b,
      HasFDerivAt
        (fun z : Fin (n + 1) → ℝ => fun i =>
          Real.exp (-V (WithLp.toLp 2 z : EuclideanSpace ℝ (Fin (n + 1)))) *
            fderiv ℝ f (WithLp.toLp 2 z : EuclideanSpace ℝ (Fin (n + 1)))
              (EuclideanSpace.single i (1 : ℝ))) (F' x) x)
    (hV : ∀ x ∈ Set.Icc a b,
      DifferentiableAt ℝ V
        (WithLp.toLp 2 x : EuclideanSpace ℝ (Fin (n + 1))))
    (hfderiv : ∀ x ∈ Set.Icc a b,
      DifferentiableAt ℝ
        (fun y : EuclideanSpace ℝ (Fin (n + 1)) => fderiv ℝ f y)
        (WithLp.toLp 2 x : EuclideanSpace ℝ (Fin (n + 1))))
    (hf : ∀ x ∈ Set.Icc a b,
      DifferentiableAt ℝ f
        (WithLp.toLp 2 x : EuclideanSpace ℝ (Fin (n + 1))))
    (hV_cont : ContinuousOn
      (fun x : Fin (n + 1) → ℝ =>
        V (WithLp.toLp 2 x : EuclideanSpace ℝ (Fin (n + 1))))
      (Set.Icc a b))
    (hlap_cont : ContinuousOn
      (fun x : Fin (n + 1) → ℝ =>
        Laplacian.laplacian f (WithLp.toLp 2 x : EuclideanSpace ℝ (Fin (n + 1))))
      (Set.Icc a b))
    (hgradV_cont : ContinuousOn
      (fun x : Fin (n + 1) → ℝ =>
        gradient V (WithLp.toLp 2 x : EuclideanSpace ℝ (Fin (n + 1))))
      (Set.Icc a b))
    (hgradf_cont : ContinuousOn
      (fun x : Fin (n + 1) → ℝ =>
        gradient f (WithLp.toLp 2 x : EuclideanSpace ℝ (Fin (n + 1))))
      (Set.Icc a b)) :
    IntegrableOn (fun x => ∑ i, F' x (Pi.single i (1 : ℝ)) i)
      (Set.Icc a b) volume := by
  have hcont := continuousOn_expNeg_langevinGenerator_rhs_of_components
    (a := a) (b := b) (V := V) (f := f)
    hV_cont hlap_cont hgradV_cont hgradf_cont
  exact integrableOn_trace_expNeg_fderivCoordinateField_of_continuousOn
    a b V f F' hF hV hfderiv hf hcont

/-- Finite-box trace integrability for the explicit Gibbs-weighted Langevin
trace display from global `C¹/C²` regularity, still assuming the explicit
Pi-space trace field has the supplied Frechet derivative on the box.

Compared with
`integrableOn_trace_expNeg_fderivCoordinateField_of_component_continuousOn`,
this wrapper derives the component continuity and pointwise differentiability
hypotheses from `ContDiff ℝ 1 V` and `ContDiff ℝ 2 f`.  The remaining
nontrivial regularity input is the explicit Pi-space field derivative `hF`.

It does not prove that field derivative, whole-space integrability, weighted
IBP, boundary cancellation, generator domains, invariant laws, reversibility,
or KL/FI dissipation. -/
theorem integrableOn_trace_expNeg_fderivCoordinateField_of_contDiff
    {n : ℕ}
    (a b : Fin (n + 1) → ℝ)
    (V f : EuclideanSpace ℝ (Fin (n + 1)) → ℝ)
    (F' : (Fin (n + 1) → ℝ) →
      (Fin (n + 1) → ℝ) →L[ℝ] (Fin (n + 1) → ℝ))
    (hF : ∀ x ∈ Set.Icc a b,
      HasFDerivAt
        (fun z : Fin (n + 1) → ℝ => fun i =>
          Real.exp (-V (WithLp.toLp 2 z : EuclideanSpace ℝ (Fin (n + 1)))) *
            fderiv ℝ f (WithLp.toLp 2 z : EuclideanSpace ℝ (Fin (n + 1)))
              (EuclideanSpace.single i (1 : ℝ))) (F' x) x)
    (hV : ContDiff ℝ 1 V)
    (hf : ContDiff ℝ 2 f) :
    IntegrableOn (fun x => ∑ i, F' x (Pi.single i (1 : ℝ)) i)
      (Set.Icc a b) volume := by
  have hVdiff : ∀ x ∈ Set.Icc a b,
      DifferentiableAt ℝ V
        (WithLp.toLp 2 x : EuclideanSpace ℝ (Fin (n + 1))) := by
    intro x _
    exact hV.differentiable one_ne_zero _
  have hfderiv : ∀ x ∈ Set.Icc a b,
      DifferentiableAt ℝ
        (fun y : EuclideanSpace ℝ (Fin (n + 1)) => fderiv ℝ f y)
        (WithLp.toLp 2 x : EuclideanSpace ℝ (Fin (n + 1))) := by
    intro x _
    exact (hf.fderiv_right (m := 1) (by norm_num)).differentiable one_ne_zero _
  have hfdiff : ∀ x ∈ Set.Icc a b,
      DifferentiableAt ℝ f
        (WithLp.toLp 2 x : EuclideanSpace ℝ (Fin (n + 1))) := by
    intro x _
    exact hf.differentiable (by norm_num) _
  have hcont := continuousOn_expNeg_langevinGenerator_rhs_of_contDiff
    (a := a) (b := b) (V := V) (f := f) hV hf
  exact integrableOn_trace_expNeg_fderivCoordinateField_of_continuousOn
    a b V f F' hF hVdiff hfderiv hfdiff hcont

/-- Finite-box trace integrability for the explicit Gibbs-weighted Langevin
field under global `C¹/C²` regularity, with the field derivative chosen as
Mathlib's `fderiv`.

This removes the remaining supplied `hF` input from
`integrableOn_trace_expNeg_fderivCoordinateField_of_contDiff`, but only for the
canonical derivative representative.  It is still a finite-box regularity
handoff, not weighted integration by parts, boundary cancellation, a generator
domain theorem, an invariant law, reversibility, or KL/FI dissipation. -/
theorem integrableOn_trace_expNeg_fderivCoordinateField_of_contDiff_fderiv
    {n : ℕ}
    (a b : Fin (n + 1) → ℝ)
    (V f : EuclideanSpace ℝ (Fin (n + 1)) → ℝ)
    (hV : ContDiff ℝ 1 V)
    (hf : ContDiff ℝ 2 f) :
    IntegrableOn
      (fun x : Fin (n + 1) → ℝ =>
        ∑ i,
          (fderiv ℝ
            (fun z : Fin (n + 1) → ℝ => fun i =>
              Real.exp (-V (WithLp.toLp 2 z : EuclideanSpace ℝ (Fin (n + 1)))) *
                fderiv ℝ f (WithLp.toLp 2 z : EuclideanSpace ℝ (Fin (n + 1)))
                  (EuclideanSpace.single i (1 : ℝ))) x)
            (Pi.single i (1 : ℝ)) i)
      (Set.Icc a b) volume := by
  let F : (Fin (n + 1) → ℝ) → Fin (n + 1) → ℝ :=
    fun z => fun i =>
      Real.exp (-V (WithLp.toLp 2 z : EuclideanSpace ℝ (Fin (n + 1)))) *
        fderiv ℝ f (WithLp.toLp 2 z : EuclideanSpace ℝ (Fin (n + 1)))
          (EuclideanSpace.single i (1 : ℝ))
  have hF : ∀ x ∈ Set.Icc a b, HasFDerivAt F (fderiv ℝ F x) x := by
    intro x _
    simpa [F] using
      hasFDerivAt_expNeg_fderivCoordinateField_of_contDiff
        (V := V) (f := f) (x := x) hV hf
  simpa [F] using
    integrableOn_trace_expNeg_fderivCoordinateField_of_contDiff
      a b V f (fun x => fderiv ℝ F x) hF hV hf

/-- Whole-space integrability of the concrete Gibbs-weighted Langevin
generator display for a compactly supported `C²` test function.

The compact support belongs to the test function, not to the Gibbs weight.
Outside `tsupport f`, local equality with the zero function forces both
`gradient f` and `Laplacian.laplacian f` to vanish.  Thus the full display
`exp (-V) * (Δ f - <∇V, ∇f>)` is continuous and compactly supported even when
`gradient V` is unbounded and the unnormalized Gibbs mass has not been shown
finite.

This is the concrete main-term integrability input for the cutoff route.  It
does not prove the cutoff limit itself, weighted integration by parts,
generator-domain semantics, stationarity, an invariant law, reversibility, or
KL/FI dissipation. -/
theorem integrable_expNeg_langevinGenerator_rhs_of_contDiff_of_hasCompactSupport
    {n : ℕ}
    {V f : EuclideanSpace ℝ (Fin (n + 1)) → ℝ}
    (hV : ContDiff ℝ 1 V)
    (hf : ContDiff ℝ 2 f)
    (hf_support : HasCompactSupport f) :
    Integrable
      (fun y : EuclideanSpace ℝ (Fin (n + 1)) =>
        Real.exp (-V y) *
          (Laplacian.laplacian f y - inner ℝ (gradient V y) (gradient f y)))
      volume := by
  have hcontinuous : Continuous
      (fun y : EuclideanSpace ℝ (Fin (n + 1)) =>
        Real.exp (-V y) *
          (Laplacian.laplacian f y - inner ℝ (gradient V y) (gradient f y))) := by
    exact hV.continuous.neg.rexp.mul
      ((_root_.AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Laplacian.continuous_laplacian_of_contDiff_two
          hf).sub
        ((_root_.AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Gradient.continuous_gradient_of_contDiff_one
            hV).inner
          (_root_.AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Gradient.continuous_gradient_of_contDiff_one
            (hf.of_le (by norm_num)))))
  have hsupport : HasCompactSupport
      (fun y : EuclideanSpace ℝ (Fin (n + 1)) =>
        Real.exp (-V y) *
          (Laplacian.laplacian f y - inner ℝ (gradient V y) (gradient f y))) := by
    refine HasCompactSupport.of_support_subset_isCompact hf_support ?_
    intro y hy
    by_contra hy_mem
    have hzero : f =ᶠ[nhds y] (0 : EuclideanSpace ℝ (Fin (n + 1)) → ℝ) := by
      rwa [← notMem_tsupport_iff_eventuallyEq]
    have hgrad : gradient f y = 0 := by
      rw [gradient, hzero.fderiv_eq]
      simp
    have hlap : Laplacian.laplacian f y = 0 := by
      have hzero_lap := InnerProductSpace.laplacian_congr_nhds hzero
      have hzero_lap_y := mem_of_mem_nhds hzero_lap
      calc
        Laplacian.laplacian f y =
            Laplacian.laplacian
              (0 : EuclideanSpace ℝ (Fin (n + 1)) → ℝ) y := hzero_lap_y
        _ = 0 := by
          change Laplacian.laplacian
            (fun _ : EuclideanSpace ℝ (Fin (n + 1)) => (0 : ℝ)) y = 0
          rw [InnerProductSpace.laplacian_const]
          rfl
    exact hy (by simp [hlap, hgrad])
  exact hcontinuous.integrable_of_hasCompactSupport hsupport

/-- Raw finite-coordinate form of
`integrable_expNeg_langevinGenerator_rhs_of_contDiff_of_hasCompactSupport`.

This transports the Euclidean-space result through Mathlib's
volume-preserving `WithLp.toLp 2` equivalence.  Its conclusion is in the exact
shape consumed by the radial-cutoff dominated-convergence theorem.  It does
not itself take a cutoff limit or prove weighted integration by parts,
generator-domain semantics, stationarity, or invariance. -/
theorem integrable_expNeg_langevinGenerator_rhs_comp_toLp_of_contDiff_of_hasCompactSupport
    {n : ℕ}
    {V f : EuclideanSpace ℝ (Fin (n + 1)) → ℝ}
    (hV : ContDiff ℝ 1 V)
    (hf : ContDiff ℝ 2 f)
    (hf_support : HasCompactSupport f) :
    Integrable
      (fun x : Fin (n + 1) → ℝ =>
        Real.exp (-V (WithLp.toLp 2 x : EuclideanSpace ℝ (Fin (n + 1)))) *
          (Laplacian.laplacian f
              (WithLp.toLp 2 x : EuclideanSpace ℝ (Fin (n + 1))) -
            inner ℝ
              (gradient V (WithLp.toLp 2 x : EuclideanSpace ℝ (Fin (n + 1))))
              (gradient f (WithLp.toLp 2 x : EuclideanSpace ℝ (Fin (n + 1))))))
      volume := by
  have hintegrable :=
    integrable_expNeg_langevinGenerator_rhs_of_contDiff_of_hasCompactSupport
      (V := V) (f := f) hV hf hf_support
  rw [← (PiLp.volume_preserving_toLp (Fin (n + 1))).integrable_comp_emb
    (MeasurableEquiv.toLp 2 _).measurableEmbedding] at hintegrable
  simpa [Function.comp_def] using hintegrable

/-- Whole-space integrability of the unnormalized Gibbs weight in raw
finite-Pi coordinates.

The hypothesis is the finite `ℝ≥0∞` Gibbs mass on Euclidean space.  Continuity
supplies measurability, and Mathlib's volume-preserving `WithLp.toLp 2`
equivalence transports integrability to the coordinate representation used by
the cutoff lemmas.  No test function, generator, tail limit, IBP, or invariant
law is asserted here. -/
theorem integrable_expNeg_comp_toLp_of_lintegral_expNeg_ne_top
    {n : ℕ}
    {V : EuclideanSpace ℝ (Fin (n + 1)) → ℝ}
    (hV : Continuous V)
    (hZ : (∫⁻ y : EuclideanSpace ℝ (Fin (n + 1)),
      ENNReal.ofReal (Real.exp (-V y)) ∂volume) ≠ ∞) :
    Integrable
      (fun x : Fin (n + 1) → ℝ =>
        Real.exp (-V (WithLp.toLp 2 x : EuclideanSpace ℝ (Fin (n + 1)))))
      volume := by
  have hweight_euclidean :
      Integrable (fun y : EuclideanSpace ℝ (Fin (n + 1)) =>
        Real.exp (-V y)) volume := by
    exact
      (lintegral_ofReal_ne_top_iff_integrable
        hV.neg.rexp.aestronglyMeasurable
        (Filter.Eventually.of_forall fun y => Real.exp_nonneg (-V y))).1 hZ
  rw [← (PiLp.volume_preserving_toLp (Fin (n + 1))).integrable_comp_emb
    (MeasurableEquiv.toLp 2 _).measurableEmbedding] at hweight_euclidean
  simpa [Function.comp_def] using hweight_euclidean

/-- The unnormalized Gibbs mass outside expanding Euclidean balls tends to
zero, in the raw finite-Pi coordinates used by the radial cutoff route.

This combines finite Gibbs mass with the generic `L¹` tail theorem.  It is a
Gibbs-tail convergence certificate only: it does not identify a cutoff-field
divergence, prove weighted integration by parts, supply generator/semigroup
domains, or establish stationarity or invariance. -/
theorem tendsto_setIntegral_expNeg_norm_ge_comp_toLp_of_lintegral_expNeg_ne_top
    {n : ℕ}
    {V : EuclideanSpace ℝ (Fin (n + 1)) → ℝ}
    (hV : Continuous V)
    (hZ : (∫⁻ y : EuclideanSpace ℝ (Fin (n + 1)),
      ENNReal.ofReal (Real.exp (-V y)) ∂volume) ≠ ∞) :
    Tendsto
      (fun R : ℝ => ∫ x in
        {x : Fin (n + 1) → ℝ |
          R ≤ ‖(WithLp.toLp 2 x : EuclideanSpace ℝ (Fin (n + 1)))‖},
        Real.exp (-V (WithLp.toLp 2 x : EuclideanSpace ℝ (Fin (n + 1))))
          ∂volume)
      atTop (nhds 0) := by
  have htail :=
    _root_.AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence.tendsto_setIntegral_norm_norm_ge_comp_toLp
      (integrable_expNeg_comp_toLp_of_lintegral_expNeg_ne_top hV hZ)
  simpa [Real.norm_eq_abs, abs_of_pos (Real.exp_pos _)] using htail

/-- Whole-space Gibbs-weighted Langevin integration by parts for a compactly
supported `C²` test function:
`∫ exp (-V) * (Δ f - ⟪∇V, ∇f⟫) = 0`.

The proof builds the raw finite-Pi vector field `exp (-V) * Df`, proves that
it is `C¹` and compactly supported, applies the reusable whole-space
coordinate-divergence theorem, identifies its trace with the Langevin
generator display pointwise, and transports volume back to Euclidean space.
No finite Gibbs-mass assumption is needed because the test function is
compactly supported.

This is the analytic core identity used by a later generator-domain and
semigroup-to-invariance bridge.  It does not itself construct a closed
generator, a Markov semigroup, or an invariant probability measure. -/
theorem integral_expNeg_langevinGenerator_rhs_eq_zero_of_contDiff_of_hasCompactSupport
    {n : ℕ}
    {V f : EuclideanSpace ℝ (Fin (n + 1)) → ℝ}
    (hV : ContDiff ℝ 1 V)
    (hf : ContDiff ℝ 2 f)
    (hf_support : HasCompactSupport f) :
    ∫ y : EuclideanSpace ℝ (Fin (n + 1)),
        Real.exp (-V y) *
          (Laplacian.laplacian f y - inner ℝ (gradient V y) (gradient f y)) = 0 := by
  let e : EuclideanSpace ℝ (Fin (n + 1)) ≃L[ℝ] (Fin (n + 1) → ℝ) :=
    PiLp.continuousLinearEquiv 2 ℝ (fun _ : Fin (n + 1) => ℝ)
  let F : (Fin (n + 1) → ℝ) → Fin (n + 1) → ℝ :=
    fun z => fun i =>
      Real.exp (-V (e.symm z)) *
        fderiv ℝ f (e.symm z) (EuclideanSpace.single i (1 : ℝ))
  have hF : ContDiff ℝ 1 F := by
    apply contDiff_pi.2
    intro i
    exact (hV.comp e.symm.contDiff).neg.exp.mul
      (((hf.fderiv_right (m := 1) (by norm_num)).comp e.symm.contDiff).clm_apply
        contDiff_const)
  have hF_support : HasCompactSupport F := by
    refine HasCompactSupport.of_support_subset_isCompact
      (hf_support.isCompact.image e.continuous) ?_
    intro x hx
    have hxe : e.symm x ∈ tsupport f := by
      by_contra hxe
      have hzero : fderiv ℝ f (e.symm x) = 0 :=
        fderiv_of_notMem_tsupport ℝ hxe
      exact hx (by
        funext i
        simp [F, hzero])
    exact ⟨e.symm x, hxe, e.apply_symm_apply x⟩
  have hdiv :=
    _root_.AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence.integral_coordinateDivergence_wrapped_eq_zero_of_contDiff_of_hasCompactSupport
      F hF hF_support
  have hraw :
      ∫ x : Fin (n + 1) → ℝ,
          Real.exp (-V (e.symm x)) *
            (Laplacian.laplacian f (e.symm x) -
              inner ℝ (gradient V (e.symm x)) (gradient f (e.symm x))) = 0 := by
    calc
      ∫ x : Fin (n + 1) → ℝ,
          Real.exp (-V (e.symm x)) *
            (Laplacian.laplacian f (e.symm x) -
              inner ℝ (gradient V (e.symm x)) (gradient f (e.symm x))) =
          ∫ x : Fin (n + 1) → ℝ,
            _root_.AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence.coordinateDivergence
              (fun y : EuclideanSpace ℝ (Fin (n + 1)) =>
                (WithLp.toLp 2 (F (WithLp.ofLp y)) :
                  EuclideanSpace ℝ (Fin (n + 1))))
              (WithLp.toLp 2 x : EuclideanSpace ℝ (Fin (n + 1))) := by
        apply integral_congr_ae
        exact Filter.Eventually.of_forall fun x => by
          have htrace :=
            trace_expNeg_fderivCoordinateField_langevinGenerator_display_of_hasFDerivAt
              (V := V) (f := f) (x := x) (F' := fderiv ℝ F x)
              (by simpa [F, e] using (hF.differentiable one_ne_zero x).hasFDerivAt)
              (hV.differentiable one_ne_zero _)
              ((hf.fderiv_right (m := 1) (by norm_num)).differentiable one_ne_zero _)
              (hf.differentiable (by norm_num) _)
          have hwrapped :=
            _root_.AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence.coordinateDivergence_wrapped_toPi_trace_of_hasFDerivAt
              (ι := Fin (n + 1)) (hF.differentiable one_ne_zero x).hasFDerivAt
          change
            Real.exp (-V (e.symm x)) *
                (Laplacian.laplacian f (e.symm x) -
                  inner ℝ (gradient V (e.symm x)) (gradient f (e.symm x))) =
              _root_.AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence.coordinateDivergence
                (fun y : EuclideanSpace ℝ (Fin (n + 1)) =>
                  (WithLp.toLp 2 (F (WithLp.ofLp y)) :
                    EuclideanSpace ℝ (Fin (n + 1))))
                (WithLp.toLp 2 x : EuclideanSpace ℝ (Fin (n + 1)))
          calc
            _ = ∑ i, fderiv ℝ F x (Pi.single i (1 : ℝ)) i := by
              simpa [e] using htrace.symm
            _ = _ := hwrapped.symm
      _ = 0 := by simpa [F, e] using hdiv
  rw [← (PiLp.volume_preserving_toLp (Fin (n + 1))).integral_comp
    (MeasurableEquiv.toLp 2 _).measurableEmbedding]
  simpa [e] using hraw

/-- Whole-space integrability of the Gibbs-weighted coordinate derivative
field from finiteness of the unnormalized Gibbs mass and a uniform operator
norm bound on the test-function derivative.

This theorem proves only source-field integrability.  It does not prove a
cutoff main-term limit, weighted integration by parts, stationarity, or an
invariant Gibbs law. -/
theorem integrable_expNeg_fderivCoordinateField_of_lintegral_expNeg_ne_top_of_fderiv_norm_le
    {n : ℕ}
    {V f : EuclideanSpace ℝ (Fin (n + 1)) → ℝ} {C : ℝ}
    (hV : Continuous V)
    (hf : ContDiff ℝ 1 f)
    (hZ : (∫⁻ y : EuclideanSpace ℝ (Fin (n + 1)),
      ENNReal.ofReal (Real.exp (-V y)) ∂volume) ≠ ∞)
    (hf_bound : ∀ y, ‖fderiv ℝ f y‖ ≤ C) :
    Integrable
      (fun x : Fin (n + 1) → ℝ => fun i =>
        Real.exp (-V (WithLp.toLp 2 x : EuclideanSpace ℝ (Fin (n + 1)))) *
          fderiv ℝ f (WithLp.toLp 2 x : EuclideanSpace ℝ (Fin (n + 1)))
            (EuclideanSpace.single i (1 : ℝ))) volume := by
  have hweight :=
    integrable_expNeg_comp_toLp_of_lintegral_expNeg_ne_top hV hZ
  let D : (Fin (n + 1) → ℝ) → (Fin (n + 1) → ℝ) :=
    fun x i =>
      fderiv ℝ f (WithLp.toLp 2 x : EuclideanSpace ℝ (Fin (n + 1)))
        (EuclideanSpace.single i (1 : ℝ))
  have hD_continuous : Continuous D := by
    refine continuous_pi fun i => ?_
    exact
      ((hf.continuous_fderiv one_ne_zero).comp
        (PiLp.continuous_toLp 2 _)).clm_apply continuous_const
  have hC : 0 ≤ C := by
    exact (norm_nonneg (fderiv ℝ f 0)).trans (hf_bound 0)
  have hD_bound : ∀ x, ‖D x‖ ≤ C := by
    intro x
    refine (pi_norm_le_iff_of_nonneg hC).2 fun i => ?_
    calc
      ‖D x i‖ ≤
          ‖fderiv ℝ f
            (WithLp.toLp 2 x : EuclideanSpace ℝ (Fin (n + 1)))‖ *
            ‖EuclideanSpace.single i (1 : ℝ)‖ :=
        ContinuousLinearMap.le_opNorm _ _
      _ = ‖fderiv ℝ f
            (WithLp.toLp 2 x : EuclideanSpace ℝ (Fin (n + 1)))‖ := by
        rw [(EuclideanSpace.orthonormal_single (𝕜 := ℝ)).1 i]
        simp
      _ ≤ C := hf_bound _
  have hproduct := hweight.smul_bdd C hD_continuous.aestronglyMeasurable
    (Filter.Eventually.of_forall hD_bound)
  simpa [D, Pi.smul_apply, smul_eq_mul] using! hproduct

end Langevin
end StochasticProcesses
end TechnicalLemmas
end AutoSamplingTheory
