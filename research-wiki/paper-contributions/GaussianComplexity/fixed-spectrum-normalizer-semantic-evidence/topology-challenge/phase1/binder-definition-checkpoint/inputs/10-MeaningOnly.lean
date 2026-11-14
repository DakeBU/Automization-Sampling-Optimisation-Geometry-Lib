import Mathlib.Probability.Distributions.Gaussian.Multivariate

open MeasureTheory

-- Only necessary standard carrier/measure meaning, no target proof or API.
variable (d : ℕ)
#synth MeasureSpace (EuclideanSpace ℝ (Fin d))
#synth MeasurableSpace (EuclideanSpace ℝ (Fin d))
#print WithLp.ofLp
