import AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.BakryEmeryGradientContraction

namespace AutoSamplingTheory.Tests.BakryEmeryGradientContraction

open AutoSamplingTheory.TechnicalLemmas.StochasticProcesses
open AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.CarreDuChamp

variable {X : Type*}

def zeroGenerator : (X → ℝ) →ₗ[ℝ] (X → ℝ) := 0

def identityEvolution (_u : ℝ) : (X → ℝ) →ₗ[ℝ] (X → ℝ) :=
  LinearMap.id

example {alpha : ℝ} (halpha : 0 < alpha) (orbit : ℝ → X → ℝ)
    (x : X) {s t : ℝ} (hst : s ≤ t) :
    identityEvolution (X := X) s
        (carreDuChamp zeroGenerator (orbit s) (orbit s)) x ≤
      identityEvolution (X := X) t
          (carreDuChamp zeroGenerator (orbit t) (orbit t)) x *
        Real.exp (-(2 * alpha) * (t - s)) := by
  have hBE : SatisfiesBakryEmery (zeroGenerator (X := X)) alpha := by
    refine ⟨halpha, ?_⟩
    intro f y
    simp [zeroGenerator, carreDuChamp, iteratedCarreDuChamp]
  apply backwardInterpolation_contraction_of_bakryEmery
    (zeroGenerator (X := X)) hBE (identityEvolution (X := X)) orbit x
  · intro u f g hfg z
    exact hfg z
  · simpa [identityEvolution, zeroGenerator, carreDuChamp] using
      (continuous_const : Continuous (fun _ : ℝ => (0 : ℝ)))
  · intro u
    simpa [identityEvolution, zeroGenerator, carreDuChamp] using
      (hasDerivWithinAt_const (x := u) (c := (0 : ℝ)) (s := Set.Ici u))
  · exact hst

end AutoSamplingTheory.Tests.BakryEmeryGradientContraction
