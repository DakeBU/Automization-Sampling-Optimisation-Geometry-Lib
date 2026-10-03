import AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.BakryEmeryCalculus

namespace AutoSamplingTheory.Tests.BakryEmeryCalculus

open AutoSamplingTheory.TechnicalLemmas.StochasticProcesses
open AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.CarreDuChamp

variable {X : Type*}

def zeroGenerator : (X → ℝ) →ₗ[ℝ] (X → ℝ) := 0

theorem zeroGenerator_satisfiesBakryEmery {alpha : ℝ} (halpha : 0 < alpha) :
    SatisfiesBakryEmery (zeroGenerator (X := X)) alpha := by
  refine ⟨halpha, ?_⟩
  intro f x
  simp [zeroGenerator, carreDuChamp, iteratedCarreDuChamp]

example {alpha : ℝ} (halpha : 0 < alpha) (f : X → ℝ) (x : X) :
    2 * alpha * carreDuChamp (zeroGenerator (X := X)) f f x ≤
      zeroGenerator (X := X)
          (carreDuChamp (zeroGenerator (X := X)) f f) x -
        2 * carreDuChamp (zeroGenerator (X := X)) f
          (zeroGenerator (X := X) f) x :=
  interpolationDerivative_lower_bound_of_expandedBakryEmery
    (zeroGenerator (X := X)) halpha (by
      intro g y
      simpa only [iteratedCarreDuChamp] using
        (zeroGenerator_satisfiesBakryEmery halpha).2 g y) f x

end AutoSamplingTheory.Tests.BakryEmeryCalculus
