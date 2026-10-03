import AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.SemigroupDecay

/-!
# Forced energy-dissipation decay

This file extends the scalar semigroup-decay interface by allowing a constant
forcing term.  The result is the exact nonzero-forcing specialization of
Mathlib's one-sided Grönwall comparison: an energy satisfying
`E' ≤ -r E + b` approaches the floor `b / r` with exponential rate `r`.

Concrete semigroup construction, generator differentiation and curvature
estimates remain separate inputs.
-/

namespace AutoSamplingTheory
namespace TechnicalLemmas
namespace FunctionalInequalities
namespace SemigroupDecay

open Filter Set
open scoped Topology

noncomputable section

/-- A forced coercive inequality gives an exponentially weighted interpolation
between the initial energy and the forcing floor.

The hypothesis
`rate * energy ≤ scale * dissipation + forcing`, together with
`energy' = -scale * dissipation`, is exactly the scalar differential
inequality `energy' ≤ -rate * energy + forcing`.  This form is useful when a
semigroup curvature estimate contains an additive error or when a dissipative
flow is driven by a bounded source. -/
theorem forced_exponential_decay_of_scaled_dissipation_from
    {scale rate forcing : ℝ} (hrate : 0 < rate)
    (curve : DissipationCurve scale)
    (hcoercive : ∀ u : ℝ,
      rate * curve.energy u ≤ scale * curve.dissipation u + forcing)
    {s t : ℝ} (hst : s ≤ t) :
    curve.energy t ≤
      curve.energy s * Real.exp (-rate * (t - s)) +
        (forcing / rate) * (1 - Real.exp (-rate * (t - s))) := by
  have hbound : ∀ x ∈ Ico s t,
      -scale * curve.dissipation x ≤
        (-rate) * curve.energy x + forcing := by
    intro x _hx
    have hneg := neg_le_neg (hcoercive x)
    linarith
  have hgronwall :=
    le_gronwallBound_of_liminf_deriv_right_le
      (f := curve.energy)
      (f' := fun x => -scale * curve.dissipation x)
      (δ := curve.energy s)
      (K := -rate)
      (ε := forcing)
      (a := s)
      (b := t)
      curve.energy_continuous.continuousOn
      (fun x _hx r hr => by
        simpa [slope] using
          (curve.energy_hasDerivWithinAt x).liminf_right_slope_le hr)
      le_rfl
      hbound
      t
      ⟨hst, le_rfl⟩
  rw [gronwallBound] at hgronwall
  simp only [if_neg (neg_ne_zero.mpr hrate.ne')] at hgronwall
  calc
    curve.energy t ≤
        curve.energy s * Real.exp (-rate * (t - s)) +
          forcing / -rate *
            (Real.exp (-rate * (t - s)) - 1) := hgronwall
    _ = curve.energy s * Real.exp (-rate * (t - s)) +
          (forcing / rate) *
            (1 - Real.exp (-rate * (t - s))) := by
      field_simp [hrate.ne']
      ring

end

end SemigroupDecay
end FunctionalInequalities
end TechnicalLemmas
end AutoSamplingTheory
