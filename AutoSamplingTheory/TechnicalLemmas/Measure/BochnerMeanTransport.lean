import AutoSamplingTheory.TechnicalLemmas.Measure.Transport
import Mathlib.MeasureTheory.Integral.Bochner.Basic
import Mathlib.MeasureTheory.Function.LpSeminorm.CompareExp
import Mathlib.MeasureTheory.Function.L2Space
import Mathlib.Tactic

open MeasureTheory Filter
open scoped ENNReal Topology

namespace AutoSamplingTheory.TechnicalLemmas.Measure.BochnerMeanTransport

private theorem bounded_feature_integrable
    {U H : Type*} [MeasurableSpace U]
    [NormedAddCommGroup H] [NormedSpace ℝ H] [CompleteSpace H]
    (K : U → H) (hK : StronglyMeasurable K) (B : ℝ)
    (hBound : ∀ u, ‖K u‖ ≤ B) (μ : Measure U) [IsProbabilityMeasure μ] :
    Integrable K μ := by
  exact (integrable_const B).mono' hK.aestronglyMeasurable (ae_of_all _ hBound)

private theorem bounded_cost_lintegral
    {U : Type*} [MeasurableSpace U]
    (c : U × U → ℝ) (C : ℝ) (hC : 0 ≤ C)
    (hc0 : ∀ z, 0 ≤ c z) (hcBound : ∀ z, c z ≤ C)
    (γ : Measure (U × U)) [IsProbabilityMeasure γ] :
    (∫⁻ z, ENNReal.ofReal ((c z)^2) ∂γ) ≤ ENNReal.ofReal (C^2) := by
  calc
    (∫⁻ z, ENNReal.ofReal ((c z)^2) ∂γ) ≤ ∫⁻ _ : U × U, ENNReal.ofReal (C^2) ∂γ := by
      apply lintegral_mono
      intro z
      exact ENNReal.ofReal_le_ofReal ((sq_le_sq₀ (hc0 z) hC).2 (hcBound z))
    _ = ENNReal.ofReal (C^2) := by simp

private theorem actual_transport_cost_finite
    {U : Type*} [MeasurableSpace U]
    (c : U × U → ℝ) (C : ℝ) (hC : 0 ≤ C)
    (hc0 : ∀ z, 0 ≤ c z) (hcBound : ∀ z, c z ≤ C)
    (μ ν : Measure U) [IsProbabilityMeasure μ] [IsProbabilityMeasure ν] :
    AutoSamplingTheory.TechnicalLemmas.Measure.Transport.transportCost
      (fun z => ENNReal.ofReal ((c z)^2)) μ ν ≠ ∞ := by
  have h := AutoSamplingTheory.TechnicalLemmas.Measure.Transport.transportCost_le_lintegral_of_isCoupling
    (fun z => ENNReal.ofReal ((c z)^2)) μ ν (μ.prod ν)
    (AutoSamplingTheory.TechnicalLemmas.Measure.Transport.isCoupling_prod μ ν)
  exact ne_of_lt (lt_of_le_of_lt (h.trans (bounded_cost_lintegral c C hC hc0 hcBound _))
    ENNReal.ofReal_lt_top)


private theorem probability_square_integral_le
    {α : Type*} [MeasurableSpace α] (γ : Measure α) [IsProbabilityMeasure γ]
    (f : α → ℝ) (hf : MemLp f 2 γ) :
    (∫ x, f x ∂γ)^2 ≤ ∫ x, (f x)^2 ∂γ := by
  let m := ∫ x, f x ∂γ
  have hi : Integrable f γ := hf.integrable (by norm_num)
  have hs : Integrable (fun x => (f x)^2) γ := (memLp_two_iff_integrable_sq hf.1).1 hf
  have hm : Integrable (fun x => 2 * f x * m) γ := (hi.const_mul 2).mul_const m
  have hn : 0 ≤ ∫ x, (f x-m)^2 ∂γ := integral_nonneg fun x => sq_nonneg _
  have he : (∫ x, (f x-m)^2 ∂γ) = (∫ x, (f x)^2 ∂γ)-m^2 := by
    simp_rw [sub_sq]
    have hsub : Integrable (fun x => (f x)^2-2*f x*m) γ := hs.sub hm
    rw [integral_add hsub (integrable_const (m^2)),integral_sub hs hm]
    simp only [integral_mul_const,integral_const_mul,integral_const,probReal_univ,one_smul]
    change (∫ x, (f x)^2 ∂γ) - 2*m*m + m^2 = _
    ring
  rw [he] at hn
  change m^2 ≤ _
  linarith

private theorem actual_coupling_mean_difference
    {U H : Type*} [MeasurableSpace U]
    [NormedAddCommGroup H] [NormedSpace ℝ H] [CompleteSpace H]
    (K : U → H) (hK : StronglyMeasurable K) (B : ℝ)
    (hBound : ∀ u, ‖K u‖ ≤ B)
    (μ ν : Measure U) [IsProbabilityMeasure μ] [IsProbabilityMeasure ν]
    (γ : Measure (U × U))
    (hγ : AutoSamplingTheory.TechnicalLemmas.Measure.Transport.IsCoupling γ μ ν) :
    (∫ u, K u ∂μ) - (∫ v, K v ∂ν) = ∫ z, (K z.1-K z.2) ∂γ := by
  letI : IsProbabilityMeasure γ :=
    AutoSamplingTheory.TechnicalLemmas.Measure.Transport.isProbabilityMeasure_of_isCoupling_left hγ
  have hleft : Integrable (fun z : U × U => K z.1) γ :=
    bounded_feature_integrable _ (hK.comp_measurable measurable_fst) B
      (fun z => hBound z.1) γ
  have hright : Integrable (fun z : U × U => K z.2) γ :=
    bounded_feature_integrable _ (hK.comp_measurable measurable_snd) B
      (fun z => hBound z.2) γ
  have hfst : (∫ u, K u ∂μ) = ∫ z, K z.1 ∂γ := by
    rw [← hγ.1]
    exact integral_map_of_stronglyMeasurable measurable_fst hK
  have hsnd : (∫ v, K v ∂ν) = ∫ z, K z.2 ∂γ := by
    rw [← hγ.2]
    exact integral_map_of_stronglyMeasurable measurable_snd hK
  rw [integral_sub hleft hright,← hfst,← hsnd]


private theorem actual_coupling_squared_mean_bound
    {U H : Type*} [MeasurableSpace U]
    [NormedAddCommGroup H] [NormedSpace ℝ H] [CompleteSpace H]
    (K : U → H) (hK : StronglyMeasurable K) (B C L : ℝ)
    (hC : 0 ≤ C) (hL : 0 ≤ L) (hBound : ∀ u, ‖K u‖ ≤ B)
    (c : U × U → ℝ) (hc : Measurable c)
    (hc0 : ∀ z, 0 ≤ c z) (hcBound : ∀ z, c z ≤ C)
    (hLip : ∀ u v, ‖K u-K v‖ ≤ L*c (u,v))
    (μ ν : Measure U) [IsProbabilityMeasure μ] [IsProbabilityMeasure ν]
    (γ : Measure (U × U))
    (hγ : AutoSamplingTheory.TechnicalLemmas.Measure.Transport.IsCoupling γ μ ν) :
    ‖(∫ u, K u ∂μ)-(∫ v, K v ∂ν)‖^2 ≤ L^2 * ∫ z, (c z)^2 ∂γ := by
  letI : IsProbabilityMeasure γ :=
    AutoSamplingTheory.TechnicalLemmas.Measure.Transport.isProbabilityMeasure_of_isCoupling_left hγ
  have hcLp : MemLp c 2 γ := (memLp_const C).mono' hc.aestronglyMeasurable
    (ae_of_all _ fun z => by simpa only [Real.norm_of_nonneg (hc0 z)] using hcBound z)
  have hcInt : Integrable c γ := hcLp.integrable (by norm_num)
  have hleft : Integrable (fun z : U × U => K z.1) γ := bounded_feature_integrable _
    (hK.comp_measurable measurable_fst) B (fun z => hBound z.1) γ
  have hright : Integrable (fun z : U × U => K z.2) γ := bounded_feature_integrable _
    (hK.comp_measurable measurable_snd) B (fun z => hBound z.2) γ
  have hnorm : ‖(∫ u, K u ∂μ)-(∫ v, K v ∂ν)‖ ≤ L * ∫ z, c z ∂γ := by
    rw [actual_coupling_mean_difference K hK B hBound μ ν γ hγ]
    calc
      ‖∫ z, (K z.1-K z.2) ∂γ‖ ≤ ∫ z, ‖K z.1-K z.2‖ ∂γ := norm_integral_le_integral_norm _
      _ ≤ ∫ z, L*c z ∂γ := integral_mono (hleft.sub hright).norm
        (hcInt.const_mul L) (fun z => hLip z.1 z.2)
      _ = L * ∫ z, c z ∂γ := integral_const_mul _ _
  have hm0 : 0 ≤ ∫ z, c z ∂γ := integral_nonneg hc0
  have hs := (sq_le_sq₀ (norm_nonneg _) (mul_nonneg hL hm0)).2 hnorm
  calc
    ‖(∫ u, K u ∂μ)-(∫ v, K v ∂ν)‖^2 ≤ (L * ∫ z, c z ∂γ)^2 := hs
    _ = L^2 * (∫ z, c z ∂γ)^2 := mul_pow _ _ _
    _ ≤ L^2 * ∫ z, (c z)^2 ∂γ := mul_le_mul_of_nonneg_left
      (probability_square_integral_le γ c hcLp) (sq_nonneg _)

theorem bounded_bochner_mean_quadratic_transport_control
    {U H : Type*} [MeasurableSpace U]
    [NormedAddCommGroup H] [NormedSpace ℝ H] [CompleteSpace H]
    (K : U → H) (hK : StronglyMeasurable K)
    (B C L : ℝ) (hB : 0 ≤ B) (hC : 0 ≤ C) (hL : 0 ≤ L)
    (hBound : ∀ u, ‖K u‖ ≤ B)
    (c : U × U → ℝ) (hc : Measurable c)
    (hc0 : ∀ z, 0 ≤ c z) (hcBound : ∀ z, c z ≤ C)
    (hLip : ∀ u v, ‖K u-K v‖ ≤ L * c (u,v))
    (μ ν : Measure U) [IsProbabilityMeasure μ] [IsProbabilityMeasure ν] :
    let cost : U × U → ℝ≥0∞ := fun z => ENNReal.ofReal ((c z)^2)
    let Q := AutoSamplingTheory.TechnicalLemmas.Measure.Transport.transportCost cost μ ν
    let W := Q ^ (1 / 2 : ℝ)
    Integrable K μ ∧ Integrable K ν ∧ Q ≠ ∞ ∧
      ‖(∫ u, K u ∂μ) - (∫ v, K v ∂ν)‖ ≤ L * W.toReal ∧
      ∀ y : H, ‖(∫ u, K u ∂μ)-y‖ ≤ B+‖y‖ ∧
        ‖(∫ v, K v ∂ν)-y‖ ≤ B+‖y‖ := by
  dsimp only
  let cost : U × U → ℝ≥0∞ := fun z => ENNReal.ofReal ((c z)^2)
  let Q := AutoSamplingTheory.TechnicalLemmas.Measure.Transport.transportCost cost μ ν
  have hQ : Q ≠ ∞ := actual_transport_cost_finite c C hC hc0 hcBound μ ν
  have hμ : Integrable K μ := bounded_feature_integrable K hK B hBound μ
  have hν : Integrable K ν := bounded_feature_integrable K hK B hBound ν
  have hs (γ : Measure (U × U))
      (hγ : AutoSamplingTheory.TechnicalLemmas.Measure.Transport.IsCoupling γ μ ν) :
      ‖(∫ u, K u ∂μ)-(∫ v, K v ∂ν)‖^2 ≤ L^2 * ∫ z, (c z)^2 ∂γ :=
    actual_coupling_squared_mean_bound K hK B C L hC hL hBound c hc hc0 hcBound hLip μ ν γ hγ
  refine ⟨hμ,hν,hQ,?_,?_⟩
  · let A := ‖(∫ u, K u ∂μ)-(∫ v, K v ∂ν)‖
    change A ≤ L * (Q ^ (1 / 2 : ℝ)).toReal
    by_cases hL0 : L = 0
    · have h := hs (μ.prod ν)
        (AutoSamplingTheory.TechnicalLemmas.Measure.Transport.isCoupling_prod μ ν)
      rw [hL0] at *
      simp only [zero_mul,zero_pow (by decide : 2 ≠ 0)] at *
      change A^2 ≤ 0 at h
      nlinarith [norm_nonneg ((∫ u, K u ∂μ)-(∫ v, K v ∂ν))]
    · have hLp : 0 < L := lt_of_le_of_ne hL (Ne.symm hL0)
      have hLow : ENNReal.ofReal ((A/L)^2) ≤ Q := by
        apply le_sInf
        rintro q ⟨γ,hγ,rfl⟩
        letI : IsProbabilityMeasure γ :=
          AutoSamplingTheory.TechnicalLemmas.Measure.Transport.isProbabilityMeasure_of_isCoupling_left hγ
        have hcLp : MemLp c 2 γ := (memLp_const C).mono' hc.aestronglyMeasurable
          (ae_of_all _ fun z => by simpa only [Real.norm_of_nonneg (hc0 z)] using hcBound z)
        have hcSq : Integrable (fun z => (c z)^2) γ := (memLp_two_iff_integrable_sq hcLp.1).1 hcLp
        change ENNReal.ofReal ((A/L)^2) ≤ ∫⁻ z, ENNReal.ofReal ((c z)^2) ∂γ
        rw [← ofReal_integral_eq_lintegral_ofReal hcSq (ae_of_all _ fun z => sq_nonneg _)]
        apply ENNReal.ofReal_le_ofReal
        rw [div_pow]
        apply (div_le_iff₀ (sq_pos_of_pos hLp)).2
        simpa only [mul_comm] using hs γ hγ
      have hReal := ENNReal.toReal_mono hQ hLow
      rw [ENNReal.toReal_ofReal (sq_nonneg _)] at hReal
      have he : (Q ^ (1 / 2 : ℝ))^2 = Q := by
        rw [← ENNReal.rpow_two,← ENNReal.rpow_mul]
        norm_num
      have heReal : ((Q ^ (1 / 2 : ℝ)).toReal)^2 = Q.toReal := by
        rw [← ENNReal.toReal_pow,he]
      have hr : A/L ≤ (Q ^ (1 / 2 : ℝ)).toReal := by
        have ha : 0 ≤ A/L := div_nonneg (norm_nonneg _) hL
        have hb := ENNReal.toReal_nonneg (a := Q ^ (1 / 2 : ℝ))
        nlinarith
      calc
        A = L * (A/L) := by field_simp
        _ ≤ L * (Q ^ (1 / 2 : ℝ)).toReal := mul_le_mul_of_nonneg_left hr hL
  · have hmμ : ‖∫ u, K u ∂μ‖ ≤ B := by
      simpa only [probReal_univ,mul_one] using
        (norm_integral_le_of_norm_le_const (μ := μ) (ae_of_all _ hBound))
    have hmν : ‖∫ v, K v ∂ν‖ ≤ B := by
      simpa only [probReal_univ,mul_one] using
        (norm_integral_le_of_norm_le_const (μ := ν) (ae_of_all _ hBound))
    intro y
    exact ⟨(norm_sub_le _ _).trans (add_le_add hmμ le_rfl),
      (norm_sub_le _ _).trans (add_le_add hmν le_rfl)⟩

end AutoSamplingTheory.TechnicalLemmas.Measure.BochnerMeanTransport
