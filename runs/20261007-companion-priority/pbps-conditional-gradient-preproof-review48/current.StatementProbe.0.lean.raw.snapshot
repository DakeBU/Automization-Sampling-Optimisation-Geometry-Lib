import AutoSamplingTheory.ExampleCases.ProximalBPS.ConditionalScore
import AutoSamplingTheory.ExampleCases.ProximalBPS.ConditionalScoreVariance
open MeasureTheory ProbabilityTheory InnerProductSpace
open scoped RealInnerProductSpace NNReal
set_option autoImplicit false
#check (∀ {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]
    {V : E → ℝ} {α β : ℝ≥0} {η : ℝ}
    (hα : 0 < (α : ℝ)) (hαβ : α ≤ β) (hV : ContDiff ℝ 2 V)
    (hH : ∀ x a : E,
      (α : ℝ) * ‖a‖^2 ≤ (fderiv ℝ (fderiv ℝ V) x a) a ∧
      (fderiv ℝ (fderiv ℝ V) x a) a ≤ (β : ℝ) * ‖a‖^2)
    (hη : 0 < η) (hβη : (β : ℝ) * η ≤ 1),
    let μ := (volume : Measure E).tilted (fun x => -V x)
    let J := Measure.map (fun p : E × E => (p.1, p.1 + Real.sqrt η • p.2))
      (μ.prod (stdGaussian E))
    ∃ R S : Kernel E E, IsMarkovKernel R ∧ IsMarkovKernel S ∧
      (J.map Prod.swap).IsCondKernel R ∧
      (∀ y, S y = (R y).map (fun x => (2 : ℝ) • x - y)) ∧
      (∀ y, S y = (volume : Measure E).tilted
        (fun u => -V ((1/2 : ℝ) • (y+u)) - ‖y-u‖^2/(8*η))) ∧
      ∀ (f : E → ℝ), ContDiff ℝ ∞ f → HasCompactSupport f →
        ∀ y, DifferentiableAt ℝ (fun z => ∫ u, f u ∂S z) y ∧
          ‖gradient (fun z => ∫ u, f u ∂S z) y‖^2 ≤
            (1/η-(α : ℝ))^2/(4*((α : ℝ)+1/η)) *
              AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.Poincare.variance
                (S y) f)
