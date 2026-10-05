import AutoSamplingTheory.TechnicalLemmas.Analysis.FinitePowerSeries

open scoped BigOperators

open AutoSamplingTheory.TechnicalLemmas.Analysis.FinitePowerSeries

example (a : ℕ → ℝ) (u : ℝ) :
    iteratedDeriv 4 (finitePowerSeries {0, 2, 4} a) u =
      finitePowerSeriesDerivative 4 {0, 2, 4} a u :=
  iteratedDeriv_finitePowerSeries 4 {0, 2, 4} a u

example (a : ℕ → ℝ) {u : ℝ} (hu : |u| ≤ 1) :
    |iteratedDeriv 4 (finitePowerSeries {0, 2, 4} a) u| ≤
      finitePowerSeriesDerivativeMass 4 {0, 2, 4} a :=
  abs_iteratedDeriv_finitePowerSeries_le_mass 4 {0, 2, 4} a hu

example {k1 k2 k3 k4 u1 u2 u3 u4 A1 A2 A3 A4 : ℝ}
    (hk1 : |k1| ≤ A1) (hk2 : |k2| ≤ A2)
    (hk3 : |k3| ≤ A3) (hk4 : |k4| ≤ A4) :
    |k4 * u1 ^ (4 : ℕ) + 6 * k3 * u1 ^ (2 : ℕ) * u2 +
        3 * k2 * u2 ^ (2 : ℕ) + 4 * k2 * u1 * u3 + k1 * u4| ≤
      A4 * |u1| ^ (4 : ℕ) + 6 * A3 * |u1| ^ (2 : ℕ) * |u2| +
        3 * A2 * |u2| ^ (2 : ℕ) + 4 * A2 * |u1| * |u3| + A1 * |u4| :=
  fourthOrderCompositionExpression_abs_le hk1 hk2 hk3 hk4
