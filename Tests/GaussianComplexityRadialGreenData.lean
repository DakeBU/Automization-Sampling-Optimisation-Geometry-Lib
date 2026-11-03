import AutoSamplingTheory.TechnicalLemmas.Analysis.Harmonic.FundamentalSolution
import AutoSamplingTheory.TechnicalLemmas.Analysis.Harmonic.PoissonKernel

open AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.RadialCalculus
open AutoSamplingTheory.TechnicalLemmas.Analysis.Harmonic.FundamentalSolution
open scoped RealInnerProductSpace

-- At the center, a quartic radial profile has zero gradient and Laplacian.
example (a : EuclideanSpace ℝ (Fin 3)) :
    gradient (fun z => (‖z - a‖ ^ 2) ^ 2) a = 0 ∧
    Laplacian.laplacian (fun z => (‖z - a‖ ^ 2) ^ 2) a = 0 := by
  have h := radial_gradient_laplacian (fun s : ℝ => s ^ 2) a a (by fun_prop)
  simpa using h

-- Zero-dimensional carrier: the canonical formula has no hidden positive-dimension guard.
example :
    Laplacian.laplacian
      (fun z : EuclideanSpace ℝ (Fin 0) => Real.exp (‖z‖ ^ 2)) 0 = 0 := by
  have h := radial_gradient_laplacian Real.exp
    (0 : EuclideanSpace ℝ (Fin 0)) 0 (by fun_prop)
  simpa using h.2

-- The actual logarithm, at the nonzero point 2e_0, has outward radial derivative 1/2.
example :
    let x : EuclideanSpace ℝ (Fin 2) := (2 : ℝ) • EuclideanSpace.single 0 1
    Real.log ‖x‖ = Real.log 2 ∧
    inner ℝ (gradient (fun z : EuclideanSpace ℝ (Fin 2) => Real.log ‖z‖) x)
      ((2 : ℝ)⁻¹ • x) = (1 / 2 : ℝ) := by
  dsimp only
  have hx : ‖((2 : ℝ) • EuclideanSpace.single 0 1 : EuclideanSpace ℝ (Fin 2))‖ = 2 := by
    simp [norm_smul]
  simpa using (fundamentalSolution_boundary_data (n := 2) (by norm_num)).2
    2 (by norm_num) _ hx

-- The actual inverse-radius potential in dimension three: value 1/2, derivative -1/4.
example :
    let x : EuclideanSpace ℝ (Fin 3) := (2 : ℝ) • EuclideanSpace.single 0 1
    ‖x‖ ^ (-1 : ℝ) = (1 / 2 : ℝ) ∧
    inner ℝ (gradient (fun z : EuclideanSpace ℝ (Fin 3) => ‖z‖ ^ (-1 : ℝ)) x)
      ((2 : ℝ)⁻¹ • x) = (-1 / 4 : ℝ) := by
  dsimp only
  have hx : ‖((2 : ℝ) • EuclideanSpace.single 0 1 : EuclideanSpace ℝ (Fin 3))‖ = 2 := by
    simp [norm_smul]
  have h := (fundamentalSolution_boundary_data (n := 3) (by norm_num)).2
    2 (by norm_num) _ hx
  norm_num [Real.rpow_neg, Real.rpow_natCast] at h ⊢
  exact h

-- Both literal source functions are harmonic on their full punctured domains.
example : InnerProductSpace.HarmonicOnNhd
    (fun x : EuclideanSpace ℝ (Fin 2) => Real.log ‖x‖) {0}ᶜ := by
  simpa using (fundamentalSolution_boundary_data (n := 2) (by norm_num)).1

example : InnerProductSpace.HarmonicOnNhd
    (fun x : EuclideanSpace ℝ (Fin 3) => ‖x‖ ^ (-1 : ℝ)) {0}ᶜ := by
  have h := (fundamentalSolution_boundary_data (n := 3) (by norm_num)).1
  norm_num at h
  exact h

#print axioms AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.RadialCalculus.radial_gradient_laplacian
#print axioms AutoSamplingTheory.TechnicalLemmas.Analysis.Harmonic.FundamentalSolution.fundamentalSolution_boundary_data
