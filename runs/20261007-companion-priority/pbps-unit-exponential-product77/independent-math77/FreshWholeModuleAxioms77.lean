import Mathlib.Probability.Distributions.Exponential
import Mathlib.Probability.Independence.InfinitePi
import Mathlib.Probability.StrongLaw

open MeasureTheory ProbabilityTheory Filter
open scoped Topology BigOperators NNReal

namespace AutoSamplingTheory.TechnicalLemmas.Probability.UnitExponentialProduct

set_option autoImplicit false

/-- Concrete countable Exp(1) input proposition.
Source: Chen--Chewi--Lu--Zhang, arXiv:2609.06905v1 Appendix A.1 Ex9.
The later consumer combines these actual thresholds with the compiled finite
PBPS recursion. No event-time, process, invariance or cost claim is made here.
-/
private def unit_exponential_product_statement : Prop :=
  let P : Measure (ℕ → ℝ) := Measure.infinitePi (fun _ : ℕ => expMeasure (1 : ℝ))
  let X : ℕ → (ℕ → ℝ) → ℝ := fun k ω => ω k
  let ε : ℕ → (ℕ → ℝ) → ℝ≥0 := fun k ω => Real.toNNReal (X k ω)
  IsProbabilityMeasure P ∧
  (∀ k : ℕ, Measurable (X k) ∧ Measurable (ε k) ∧
    Measure.map (X k) P = expMeasure (1 : ℝ)) ∧
  iIndepFun X P ∧
  (∀ᵐ ω ∂P, ∀ k : ℕ, 0 < X k ω ∧ (ε k ω : ℝ) = X k ω) ∧
  (∀ᵐ ω ∂P, Tendsto (fun n : ℕ => ∑ k ∈ Finset.range n, (ε k ω : ℝ))
    atTop atTop)

/-- The actual unit-exponential product realizes the countable source clocks.
The divergence proof uses an ASTIS sufficient alternative: the bounded iid
indicators of coordinates above one, their positive mean, and the strong law.
It does not assert an Exp(1) first-moment calculation or event-time convergence.
-/
theorem unit_exponential_product_laws : unit_exponential_product_statement := by
  classical
  let P : Measure (ℕ → ℝ) := Measure.infinitePi (fun _ : ℕ => expMeasure (1 : ℝ))
  let X : ℕ → (ℕ → ℝ) → ℝ := fun k ω => ω k
  let ε : ℕ → (ℕ → ℝ) → ℝ≥0 := fun k ω => Real.toNNReal (X k ω)
  change IsProbabilityMeasure P ∧
    (∀ k : ℕ, Measurable (X k) ∧ Measurable (ε k) ∧
      Measure.map (X k) P = expMeasure (1 : ℝ)) ∧
    iIndepFun X P ∧
    (∀ᵐ ω ∂P, ∀ k : ℕ, 0 < X k ω ∧ (ε k ω : ℝ) = X k ω) ∧
    (∀ᵐ ω ∂P, Tendsto (fun n : ℕ => ∑ k ∈ Finset.range n, (ε k ω : ℝ))
      atTop atTop)
  -- The factor probability theorem activates the actual infinite-product APIs.
  let : IsProbabilityMeasure (expMeasure (1 : ℝ)) :=
    isProbabilityMeasure_expMeasure zero_lt_one
  have hP : IsProbabilityMeasure P := inferInstance
  let : IsProbabilityMeasure P := hP
  have hX (k : ℕ) : Measurable (X k) := measurable_pi_apply k
  have hε (k : ℕ) : Measurable (ε k) := measurable_real_toNNReal.comp (hX k)
  have hmap (k : ℕ) : Measure.map (X k) P = expMeasure (1 : ℝ) :=
    Measure.infinitePi_map_eval (fun _ : ℕ => expMeasure (1 : ℝ)) k
  have hindep : iIndepFun X P :=
    iIndepFun_infinitePi (X := fun _ : ℕ => (id : ℝ → ℝ))
      (fun _ => measurable_id)
  -- CDF(0)=0 gives strict positivity; countability gives a single good event.
  have hnull : expMeasure (1 : ℝ) (Set.Iic 0) = 0 := by
    apply (measureReal_eq_zero_iff (μ := expMeasure (1 : ℝ)) (s := Set.Iic 0)).mp
    rw [← cdf_eq_real, cdf_expMeasure_eq zero_lt_one]
    norm_num
  have hpos : ∀ᵐ x ∂expMeasure (1 : ℝ), 0 < x := by
    rw [ae_iff]
    simp only [not_lt]
    change expMeasure (1 : ℝ) (Set.Iic 0) = 0
    exact hnull
  have hpos_all : ∀ᵐ ω ∂P, ∀ k : ℕ, 0 < X k ω := by
    rw [ae_all_iff]
    intro k
    apply ae_of_ae_map (hX k).aemeasurable
    simpa only [hmap] using hpos
  have hgood : ∀ᵐ ω ∂P, ∀ k : ℕ, 0 < X k ω ∧ (ε k ω : ℝ) = X k ω := by
    filter_upwards [hpos_all] with ω hω
    exact fun k => ⟨hω k, Real.coe_toNNReal _ (hω k).le⟩
  -- ASTIS OR-route: a bounded indicator has a computable strictly positive mean.
  let b : ℝ → ℝ := (Set.Ioi (1 : ℝ)).indicator (fun _ => 1)
  have hb : Measurable b := measurable_const.indicator measurableSet_Ioi
  let B : ℕ → (ℕ → ℝ) → ℝ := fun k ω => b (X k ω)
  have hB0 : Integrable (B 0) P := by
    exact (integrable_const (1 : ℝ)).indicator
      (measurableSet_Ioi.preimage (hX 0))
  have hBindep : iIndepFun B P := hindep.comp (fun _ => b) (fun _ => hb)
  have hident (k : ℕ) : IdentDistrib (B k) (B 0) P P := by
    have hx : IdentDistrib (X k) (X 0) P P :=
      ⟨(hX k).aemeasurable, (hX 0).aemeasurable, (hmap k).trans (hmap 0).symm⟩
    exact hx.comp hb
  have htail : (expMeasure (1 : ℝ)).real (Set.Ioi (1 : ℝ)) = Real.exp (-1) := by
    rw [← Set.compl_Iic, measureReal_compl measurableSet_Iic, probReal_univ,
      ← cdf_eq_real, cdf_expMeasure_eq zero_lt_one]
    norm_num
  have hmean : (∫ ω, B 0 ω ∂P) = Real.exp (-1) := by
    calc
      (∫ ω, B 0 ω ∂P) = ∫ x, b x ∂Measure.map (X 0) P :=
        (integral_map (hX 0).aemeasurable hb.aestronglyMeasurable).symm
      _ = ∫ x, b x ∂expMeasure (1 : ℝ) := by rw [hmap]
      _ = (expMeasure (1 : ℝ)).real (Set.Ioi (1 : ℝ)) :=
        integral_indicator_one measurableSet_Ioi
      _ = Real.exp (-1) := htail
  have hslln : ∀ᵐ ω ∂P, Tendsto
      (fun n : ℕ => (∑ k ∈ Finset.range n, B k ω) / (n : ℝ))
      atTop (𝓝 (Real.exp (-1))) := by
    simpa only [hmean] using
      strong_law_ae_real B hB0 (fun _ _ hij => hBindep.indepFun hij) hident
  -- Positive limiting average forces unbounded sums; each indicator is below ε.
  have hdiv : ∀ᵐ ω ∂P, Tendsto
      (fun n : ℕ => ∑ k ∈ Finset.range n, (ε k ω : ℝ)) atTop atTop := by
    filter_upwards [hslln] with ω hω
    have hmul := hω.pos_mul_atTop (Real.exp_pos (-1))
      (tendsto_natCast_atTop_atTop (R := ℝ))
    have hsum : Tendsto (fun n : ℕ => ∑ k ∈ Finset.range n, B k ω) atTop atTop := by
      apply hmul.congr'
      exact Filter.Eventually.of_forall fun n => by
        by_cases hn : n = 0
        · subst n
          simp
        · exact div_mul_cancel₀ _ (Nat.cast_ne_zero.mpr hn)
    apply tendsto_atTop_mono _ hsum
    intro n
    apply Finset.sum_le_sum
    intro k _
    by_cases hk : 1 < X k ω
    · have hraw := Real.le_coe_toNNReal (X k ω)
      simpa [B, b, Set.indicator_of_mem, hk, ε] using hk.le.trans hraw
    · simp [B, b, hk]
  exact ⟨hP, fun k => ⟨hX k, hε k, hmap k⟩, hindep, hgood, hdiv⟩

end AutoSamplingTheory.TechnicalLemmas.Probability.UnitExponentialProduct

/- Independent fresh whole-module elaboration and axiom inspection; no new proof. -/
#print axioms AutoSamplingTheory.TechnicalLemmas.Probability.UnitExponentialProduct.unit_exponential_product_laws
#check AutoSamplingTheory.TechnicalLemmas.Probability.UnitExponentialProduct.unit_exponential_product_laws
