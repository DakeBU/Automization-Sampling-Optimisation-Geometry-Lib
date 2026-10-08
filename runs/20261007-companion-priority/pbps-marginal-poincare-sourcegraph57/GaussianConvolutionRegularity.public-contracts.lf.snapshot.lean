import Mathlib.Analysis.InnerProductSpace.Calculus
import Mathlib.Analysis.Calculus.ParametricIntegral
import Mathlib.Analysis.SpecialFunctions.ExpDeriv
import Mathlib.Analysis.SpecialFunctions.Log.Deriv
import Mathlib.MeasureTheory.Measure.Tilted
import Mathlib.MeasureTheory.Function.L2Space
import Mathlib.Probability.Moments.CovarianceBilin
import Mathlib.Tactic
import AutoSamplingTheory.ExampleCases.ProximalBPS.GaussianAugmentation
open MeasureTheory ProbabilityTheory Filter Set
open scoped Topology InnerProductSpace
namespace AutoSamplingTheory.TechnicalLemmas.Measure.GaussianConvolutionRegularity
noncomputable section
set_option backward.isDefEq.respectTransparency false
variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
variable [MeasurableSpace E] [BorelSpace E] [FiniteDimensional ℝ E]

theorem gaussian_convolution_potential_c2 (μ : Measure E) [IsProbabilityMeasure μ]
    {η : ℝ} (hη : 0 < η) :
    let C := ((Real.sqrt (2*Real.pi*η))⁻¹)^Module.finrank ℝ E
    let Z := fun y : E => ∫ x, Real.exp (-‖y-x‖^2/(2*η)) ∂μ
    (μ.prod (stdGaussian E)).map (fun p => p.1+Real.sqrt η • p.2) =
      (volume : Measure E).withDensity (fun y => ENNReal.ofReal (C*Z y)) ∧
    (∀ y, 0 < C*Z y) ∧ ContDiff ℝ 2 Z ∧
      ContDiff ℝ 2 (fun y => -Real.log (C*Z y)) 
theorem gaussian_convolution_derivatives (μ : Measure E) [IsProbabilityMeasure μ] {η C : ℝ} (hη : 0 < η)
    (hC : 0 < C) :
    let R := fun y : E => μ.tilted (fun x => -‖x-y‖^2/(2*η))
    let U := fun y : E => -Real.log (C*∫ x, Real.exp (-‖y-x‖^2/(2*η)) ∂μ)
    (∀ y, IsProbabilityMeasure (R y) ∧ MemLp (fun x : E => x) 2 (R y)) ∧
    (∀ y v, fderiv ℝ U y v = inner ℝ (y-∫ x, x ∂(R y)) v/η) ∧
    ∀ y v w, fderiv ℝ (fderiv ℝ U) y v w =
      inner ℝ v w/η - covarianceBilin (R y) v w/η^2 