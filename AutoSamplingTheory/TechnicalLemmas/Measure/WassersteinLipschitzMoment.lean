import AutoSamplingTheory.TechnicalLemmas.Measure.CouplingQuadraticIntegrability
import AutoSamplingTheory.TechnicalLemmas.Measure.WassersteinSpace
import Mathlib.Tactic

/-!
# Transport of quadratic moments through Lipschitz observables

Finite quadratic Wasserstein cost transfers square-integrability of a
Lipschitz observable from the reference marginal to the transported marginal.
The proof first works with an actual coupling and then approaches the infimum
defining `wassersteinDistance`; no optimal coupling is assumed.

This is a shared measure-theoretic interface.  In particular, applying it to
phase-space coordinate projections is legitimate only for the metric used by
`wassersteinDistance`.  A paper-specific twisted metric such as the SPHMC
`M_kappa` norm still requires an explicit metric-comparison adapter.
-/

namespace AutoSamplingTheory.TechnicalLemmas.Measure.WassersteinLipschitzMoment

open MeasureTheory
open scoped ENNReal NNReal

noncomputable section

variable {E F : Type*} [NormedAddCommGroup E] [MeasurableSpace E]
  [BorelSpace E] [SecondCountableTopology E] [NormedAddCommGroup F]

omit [MeasurableSpace E] [BorelSpace E] [SecondCountableTopology E] in
private theorem lipschitz_norm_sq_bound {g : E → F} {b : ℝ≥0}
    (hg : LipschitzWith b g) (x y : E) :
    ‖g x‖ ^ 2 ≤ 2 * ‖g y‖ ^ 2 + 2 * (b : ℝ) ^ 2 * ‖x - y‖ ^ 2 := by
  have hLip : ‖g x - g y‖ ≤ (b : ℝ) * ‖x - y‖ := by
    simpa only [dist_eq_norm] using hg.dist_le_mul x y
  have htri := norm_sub_norm_le (g x) (g y)
  have hnorm : ‖g x‖ ≤ ‖g y‖ + (b : ℝ) * ‖x - y‖ := by linarith
  have hnonneg : 0 ≤ (b : ℝ) * ‖x - y‖ :=
    mul_nonneg b.coe_nonneg (norm_nonneg _)
  nlinarith [norm_nonneg (g x), norm_nonneg (g y),
    sq_nonneg (‖g y‖ - (b : ℝ) * ‖x - y‖)]

/-- An actual quadratic-cost coupling transfers the second moment of a
Lipschitz observable from its second marginal to its first marginal. -/
private theorem of_isCoupling {mu nu : Measure E} {gamma : Measure (E × E)}
    {g : E → F} {b : ℝ≥0} {s : ℝ} (hg : LipschitzWith b g)
    (hi : Integrable (fun x => ‖g x‖ ^ 2) nu)
    (hgamma : Transport.IsCoupling gamma mu nu) (hs : 0 ≤ s)
    (hcost : (∫⁻ p, WassersteinSpace.quadraticCost p ∂gamma) ≤ ENNReal.ofReal s) :
    Integrable (fun x => ‖g x‖ ^ 2) mu ∧
      (∫ x, ‖g x‖ ^ 2 ∂mu) ≤
        2 * (∫ x, ‖g x‖ ^ 2 ∂nu) + 2 * (b : ℝ) ^ 2 * s := by
  have hc : Continuous (fun x => ‖g x‖ ^ 2) := hg.continuous.norm.pow 2
  have hmp1 := CouplingQuadraticIntegrability.measurePreserving_fst_of_isCoupling hgamma
  have hmp2 := CouplingQuadraticIntegrability.measurePreserving_snd_of_isCoupling hgamma
  have hq : Integrable (fun p : E × E => ‖g p.2‖ ^ 2) gamma :=
    hmp2.integrable_comp_of_integrable hi
  have hd : Integrable (fun p : E × E => ‖p.1 - p.2‖ ^ 2) gamma := by
    have hm : AEMeasurable
        (fun p : E × E => WassersteinSpace.quadraticCost p) gamma := by
      unfold WassersteinSpace.quadraticCost
      fun_prop
    have ht := integrable_toReal_of_lintegral_ne_top hm
      (lt_of_le_of_lt hcost ENNReal.ofReal_lt_top).ne
    simpa [WassersteinSpace.quadraticCost] using ht
  have hdint : (∫ p : E × E, ‖p.1 - p.2‖ ^ 2 ∂gamma) ≤ s := by
    apply (ENNReal.ofReal_le_ofReal_iff hs).1
    rw [ofReal_integral_eq_lintegral_ofReal hd
      (Filter.Eventually.of_forall (fun p => sq_nonneg _))]
    exact hcost
  have hdom : Integrable
      (fun p : E × E =>
        2 * ‖g p.2‖ ^ 2 + 2 * (b : ℝ) ^ 2 * ‖p.1 - p.2‖ ^ 2) gamma :=
    (hq.const_mul 2).add (hd.const_mul _)
  have hp : Integrable (fun p : E × E => ‖g p.1‖ ^ 2) gamma := by
    apply hdom.mono' (hc.comp continuous_fst).aestronglyMeasurable
    filter_upwards with p
    change ‖(‖g p.1‖ ^ 2 : ℝ)‖ ≤ _
    rw [Real.norm_eq_abs, abs_of_nonneg (sq_nonneg ‖g p.1‖)]
    exact lipschitz_norm_sq_bound hg p.1 p.2
  have hmu : Integrable (fun x => ‖g x‖ ^ 2) mu := by
    rw [← hmp1.map_eq]
    exact (integrable_map_measure hc.aestronglyMeasurable measurable_fst.aemeasurable).2 hp
  have hpint : (∫ p : E × E, ‖g p.1‖ ^ 2 ∂gamma) = ∫ x, ‖g x‖ ^ 2 ∂mu := by
    rw [← hmp1.map_eq, integral_map measurable_fst.aemeasurable hc.aestronglyMeasurable]
  have hqint : (∫ p : E × E, ‖g p.2‖ ^ 2 ∂gamma) = ∫ x, ‖g x‖ ^ 2 ∂nu := by
    rw [← hmp2.map_eq, integral_map measurable_snd.aemeasurable hc.aestronglyMeasurable]
  have hm := integral_mono hp hdom (fun p => lipschitz_norm_sq_bound hg p.1 p.2)
  rw [integral_add (hq.const_mul 2) (hd.const_mul _), integral_const_mul,
    integral_const_mul, hpint, hqint] at hm
  refine ⟨hmu, hm.trans ?_⟩
  gcongr

/-- A squared `wassersteinDistance` bound transfers square-integrability and
gives the standard quadratic moment estimate for every Lipschitz observable.

The radius is written as a real number because paper applications normally
state the premise as `W₂² ≤ r²`. -/
theorem of_wassersteinDistance_sq_le {mu nu : Measure E}
    {g : E → F} {b : ℝ≥0} {r : ℝ} (hg : LipschitzWith b g)
    (hi : Integrable (fun x => ‖g x‖ ^ 2) nu)
    (hw : WassersteinSpace.wassersteinDistance mu nu ^ 2 ≤ ENNReal.ofReal (r ^ 2)) :
    Integrable (fun x => ‖g x‖ ^ 2) mu ∧
      (∫ x, ‖g x‖ ^ 2 ∂mu) ≤
        2 * (∫ x, ‖g x‖ ^ 2 ∂nu) + 2 * (b : ℝ) ^ 2 * r ^ 2 := by
  have hall (s : ℝ) (hs : r ^ 2 < s) :
      Integrable (fun x => ‖g x‖ ^ 2) mu ∧
        (∫ x, ‖g x‖ ^ 2 ∂mu) ≤
          2 * (∫ x, ‖g x‖ ^ 2 ∂nu) + 2 * (b : ℝ) ^ 2 * s := by
    have hs0 : 0 < s := (sq_nonneg r).trans_lt hs
    have hcost : Transport.transportCost
        (WassersteinSpace.quadraticCost (E := E)) mu nu < ENNReal.ofReal s := by
      rw [← WassersteinSpace.wassersteinDistance_sq]
      exact hw.trans_lt ((ENNReal.ofReal_lt_ofReal_iff hs0).2 hs)
    obtain ⟨gamma, hgamma, hgammaCost⟩ :=
      Transport.exists_isCoupling_lintegral_lt_of_transportCost_lt
        (WassersteinSpace.quadraticCost (E := E)) mu nu hcost
    exact of_isCoupling hg hi hgamma hs0.le hgammaCost.le
  refine ⟨(hall (r ^ 2 + 1) (by linarith)).1, ?_⟩
  apply le_of_forall_pos_le_add
  intro epsilon hepsilon
  have hden : 0 < 2 * (b : ℝ) ^ 2 + 1 := by positivity
  have hdelta : 0 < epsilon / (2 * (b : ℝ) ^ 2 + 1) := div_pos hepsilon hden
  have hbound := (hall (r ^ 2 + epsilon / (2 * (b : ℝ) ^ 2 + 1)) (by linarith)).2
  have heq := div_mul_cancel₀ epsilon hden.ne'
  nlinarith

end

end AutoSamplingTheory.TechnicalLemmas.Measure.WassersteinLipschitzMoment
