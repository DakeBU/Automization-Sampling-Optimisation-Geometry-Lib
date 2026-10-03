import AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.BakryEmeryInterpolation

namespace AutoSamplingTheory.Tests.BakryEmeryInterpolation

open Set
open AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.SemigroupDecay

example {rate s t : ℝ} (hst : s ≤ t) :
    (0 : ℝ) ≤ 0 * Real.exp (-rate * (t - s)) := by
  apply backward_interpolation_contraction_of_growth
    (interpolation := fun _ : ℝ => 0)
    (interpolation' := fun _ : ℝ => 0)
  · exact continuous_const
  · intro u
    simpa using
      (hasDerivWithinAt_const
        (x := u) (s := Ici u) (c := (0 : ℝ)))
  · intro u
    simp
  · exact hst

end AutoSamplingTheory.Tests.BakryEmeryInterpolation
