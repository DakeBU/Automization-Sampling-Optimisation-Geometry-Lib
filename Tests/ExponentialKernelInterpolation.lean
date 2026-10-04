import AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.ExponentialKernelInterpolation

open Set
open AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities

example {H H' : ℝ → ℝ} {rate source t energy : ℝ}
    (hrate : 0 < rate) (ht : 0 ≤ t)
    (hH : ∀ s ∈ Icc (0 : ℝ) t, HasDerivAt H (H' s) s)
    (hzero : H 0 = 0)
    (hderiv : ∀ s ∈ Ioo (0 : ℝ) t,
      H' s ≤ source * Real.exp (-rate * (t - s)) * energy) :
    H t ≤ (source / rate) * (1 - Real.exp (-rate * t)) * energy :=
  endpoint_le_of_deriv_le_exponential_kernel
    hrate ht hH hzero hderiv
