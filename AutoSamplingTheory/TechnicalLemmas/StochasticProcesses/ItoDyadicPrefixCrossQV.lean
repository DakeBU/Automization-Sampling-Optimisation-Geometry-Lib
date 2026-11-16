import AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoDyadicPrefixQV

namespace AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoDyadicPrefixCrossQV

open Filter MeasureTheory Set
open scoped BigOperators NNReal ENNReal Topology
open BrownianMotion ProgressiveL2 ElementaryItoIntegral SampledElementaryApproximation
  DyadicElementaryRefinement EuclideanBrownianCoordinates ItoIntegralProcess ItoDyadicPrefixQV

private theorem boundedVariationOn_add {f g : ℝ≥0 → ℝ} {S : Set ℝ≥0}
    (hf : BoundedVariationOn f S) (hg : BoundedVariationOn g S) :
    BoundedVariationOn (fun t => f t + g t) S := by
  have hfinite : eVariationOn f S + eVariationOn g S ≠ ∞ :=
    ENNReal.add_ne_top.2 ⟨hf, hg⟩
  apply ne_top_of_le_ne_top hfinite
  rw [eVariationOn]
  refine iSup_le ?_
  rintro ⟨n, u, hu, hS⟩
  calc
    _ ≤ ∑ i ∈ Finset.range n,
        (edist (f (u (i + 1))) (f (u i)) + edist (g (u (i + 1))) (g (u i))) :=
      Finset.sum_le_sum (fun i _ => edist_add_add_le _ _ _ _)
    _ ≤ eVariationOn f S + eVariationOn g S := by
      rw [Finset.sum_add_distrib]
      exact add_le_add (eVariationOn.sum_le hu hS) (eVariationOn.sum_le hu hS)

/-- Mixed quadratic variation of two completed Itô rows up to a fixed dyadic time. -/
theorem tendstoInMeasure_dyadic_prefix_mul_increments_of_ito_rows
    {Ω J : Type*} [MeasurableSpace Ω] [Fintype J] [DecidableEq J]
    {filtration : Filtration ℝ≥0 (inferInstance : MeasurableSpace Ω)}
    {μ : Measure Ω} [IsFiniteMeasure μ] {T : ℝ≥0}
    {B : ℝ≥0 → Ω → EuclideanSpace ℝ J}
    (hB : IsStandardBrownianMotionWithFiltration B filtration μ) (hT : 0 < T)
    (hUsual : SatisfiesUsualConditions filtration μ)
    (η ξ : J → ProgressiveL2Integrand filtration μ T)
    (A C : ℝ≥0 → Ω → ℝ)
    (hAmeas : ∀ t ≤ T, AEStronglyMeasurable (A t) μ)
    (hCmeas : ∀ t ≤ T, AEStronglyMeasurable (C t) μ)
    (hA : ∀ᵐ ω ∂μ, ContinuousOn (fun t => A t ω) (Icc 0 T) ∧
      BoundedVariationOn (fun t => A t ω) (Icc 0 T))
    (hC : ∀ᵐ ω ∂μ, ContinuousOn (fun t => C t ω) (Icc 0 T) ∧
      BoundedVariationOn (fun t => C t ω) (Icc 0 T))
    (m : ℕ) (k : Fin (2 ^ m + 1)) :
    let τ := regularGridTimes (dyadicMesh T m) (2 ^ m) k
    let X := fun t ω => A t ω + ∑ j : J,
      itoIntegralProcess (η j) hT ((coordinateFamily hB).isBrownian j) hUsual t ω
    let Y := fun t ω => C t ω + ∑ j : J,
      itoIntegralProcess (ξ j) hT ((coordinateFamily hB).isBrownian j) hUsual t ω
    TendstoInMeasure μ (fun n ω =>
      let t := regularGridTimes (dyadicMesh T n) (2 ^ n)
      ∑ i : Fin (2 ^ n), if t i.succ ≤ τ then
        (X (t i.succ) ω - X (t i.castSucc) ω) *
          (Y (t i.succ) ω - Y (t i.castSucc) ω) else 0) atTop
      (fun ω => ∑ j : J, ∫ s in Iic τ, (η j).process s ω * (ξ j).process s ω ∂(TimeMeasure.upTo T)) := by
  intro τ X Y
  let t (n : ℕ) := regularGridTimes (dyadicMesh T n) (2 ^ n)
  let I (r : J → ProgressiveL2Integrand filtration μ T) (j : J) :=
    itoIntegralProcess (r j) hT ((coordinateFamily hB).isBrownian j) hUsual
  let plus (j : J) := ProgressiveL2Algebra.add (η j) (ξ j)
  let D (s : ℝ≥0) (ω : Ω) := A s ω + C s ω
  let Z (s : ℝ≥0) (ω : Ω) := D s ω + ∑ j : J, I plus j s ω
  let Δ (F : ℝ≥0 → Ω → ℝ) (n : ℕ) (i : Fin (2 ^ n)) (ω : Ω) :=
    F (t n i.succ) ω - F (t n i.castSucc) ω
  let Q (F : ℝ≥0 → Ω → ℝ) (n : ℕ) (ω : Ω) :=
    ∑ i : Fin (2 ^ n), if t n i.succ ≤ τ then (Δ F n i ω) ^ 2 else 0
  let E (r : J → ProgressiveL2Integrand filtration μ T) (ω : Ω) :=
    ∑ j : J, ∫ s in Iic τ, (r j).process s ω ^ 2 ∂(TimeMeasure.upTo T)
  have hDmeas (s : ℝ≥0) (hs : s ≤ T) : AEStronglyMeasurable (D s) μ :=
    (hAmeas s hs).add (hCmeas s hs)
  have hD : ∀ᵐ ω ∂μ, ContinuousOn (fun s => D s ω) (Icc 0 T) ∧
      BoundedVariationOn (fun s => D s ω) (Icc 0 T) := by
    filter_upwards [hA, hC] with ω ha hc
    exact ⟨ha.1.add hc.1, boundedVariationOn_add ha.2 hc.2⟩
  have hX : TendstoInMeasure μ (Q X) atTop (E η) :=
    tendstoInMeasure_dyadic_prefix_sq_increments_of_ito_row hB hT hUsual η A hAmeas hA m k
  have hY : TendstoInMeasure μ (Q Y) atTop (E ξ) :=
    tendstoInMeasure_dyadic_prefix_sq_increments_of_ito_row hB hT hUsual ξ C hCmeas hC m k
  have hZ : TendstoInMeasure μ (Q Z) atTop (E plus) :=
    tendstoInMeasure_dyadic_prefix_sq_increments_of_ito_row hB hT hUsual plus D hDmeas hD m k
  have ht (n : ℕ) (i : Fin (2 ^ n + 1)) : t n i ≤ T :=
    ((regularGridTimes_strictMono (dyadicMesh_pos hT n) _).monotone (Fin.le_last i)).trans_eq
      (regularDyadic_last_time T n)
  have hSum (s : ℝ≥0) (hs : s ≤ T) : ∀ᵐ ω ∂μ, Z s ω = X s ω + Y s ω := by
    have hCoordinate : ∀ᵐ ω ∂μ, ∀ j : J, I plus j s ω = I η j s ω + I ξ j s ω := by
      rw [ae_all_iff]
      intro j
      exact itoIntegralProcess_add (η j) (ξ j) hT ((coordinateFamily hB).isBrownian j) hUsual hs
    filter_upwards [hCoordinate] with ω hω
    change A s ω + C s ω + (∑ j : J, I plus j s ω) =
      (A s ω + ∑ j : J, I η j s ω) + (C s ω + ∑ j : J, I ξ j s ω)
    simp only [hω, Finset.sum_add_distrib]
    ring
  let P (n : ℕ) (ω : Ω) :=
    ∑ i : Fin (2 ^ n), if t n i.succ ≤ τ then Δ X n i ω * Δ Y n i ω else 0
  have hPolar (n : ℕ) : ∀ᵐ ω ∂μ,
      (Q Z n ω - Q X n ω - Q Y n ω) / 2 = P n ω := by
    have hGrid : ∀ᵐ ω ∂μ, ∀ i, Z (t n i) ω = X (t n i) ω + Y (t n i) ω :=
      ae_all_iff.2 (fun i => hSum _ (ht n i))
    filter_upwards [hGrid] with ω hω
    change ((∑ i : Fin (2 ^ n), if t n i.succ ≤ τ then Δ Z n i ω ^ 2 else 0) -
      (∑ i : Fin (2 ^ n), if t n i.succ ≤ τ then Δ X n i ω ^ 2 else 0) -
      (∑ i : Fin (2 ^ n), if t n i.succ ≤ τ then Δ Y n i ω ^ 2 else 0)) / 2 = P n ω
    rw [← Finset.sum_sub_distrib, ← Finset.sum_sub_distrib, Finset.sum_div]
    apply Finset.sum_congr rfl
    intro i _
    dsimp only [Δ]
    by_cases hi : t n i.succ ≤ τ
    · simp only [if_pos hi, hω]
      ring
    · simp [hi]
  have hI (r : J → ProgressiveL2Integrand filtration μ T) (s : ℝ≥0) :
      AEStronglyMeasurable (fun ω => ∑ j : J, I r j s ω) μ :=
    (Finset.aestronglyMeasurable_sum Finset.univ fun j _ =>
      (((itoIntegralProcess_stronglyAdapted (r j) hT
        ((coordinateFamily hB).isBrownian j) hUsual) s).mono
          (filtration.le s)).aestronglyMeasurable).congr
      (Eventually.of_forall fun ω => by simp only [Finset.sum_apply, I])
  have hPm (n : ℕ) : AEStronglyMeasurable (P n) μ := by
    have hXm (s : ℝ≥0) (hs : s ≤ T) : AEStronglyMeasurable (X s) μ :=
      (hAmeas s hs).add (hI η s)
    have hYm (s : ℝ≥0) (hs : s ≤ T) : AEStronglyMeasurable (Y s) μ :=
      (hCmeas s hs).add (hI ξ s)
    have hCell (i : Fin (2 ^ n)) : AEStronglyMeasurable
        (fun ω => if t n i.succ ≤ τ then Δ X n i ω * Δ Y n i ω else 0) μ := by
      by_cases hi : t n i.succ ≤ τ
      · simp only [if_pos hi]
        exact ((hXm _ (ht n i.succ)).sub (hXm _ (ht n i.castSucc))).mul
          ((hYm _ (ht n i.succ)).sub (hYm _ (ht n i.castSucc)))
      · simpa only [if_neg hi] using
          (aestronglyMeasurable_const : AEStronglyMeasurable (fun _ : Ω => (0 : ℝ)) μ)
    exact (Finset.aestronglyMeasurable_sum Finset.univ fun i _ => hCell i).congr
      (Eventually.of_forall fun ω => by simp only [P, Finset.sum_apply])
  let M (ω : Ω) := ∑ j : J, ∫ s in Iic τ,
    (η j).process s ω * (ξ j).process s ω ∂(TimeMeasure.upTo T)
  have hEnergy : ∀ᵐ ω ∂μ, (E plus ω - E η ω - E ξ ω) / 2 = M ω := by
    have hCell (j : J) : ∀ᵐ ω ∂μ,
        ((∫ s in Iic τ, (plus j).process s ω ^ 2 ∂(TimeMeasure.upTo T)) -
          (∫ s in Iic τ, (η j).process s ω ^ 2 ∂(TimeMeasure.upTo T)) -
          (∫ s in Iic τ, (ξ j).process s ω ^ 2 ∂(TimeMeasure.upTo T))) / 2 =
        ∫ s in Iic τ, (η j).process s ω * (ξ j).process s ω ∂(TimeMeasure.upTo T) := by
      filter_upwards [(plus j).memLp.integrable_sq.prod_right_ae,
        (η j).memLp.integrable_sq.prod_right_ae, (ξ j).memLp.integrable_sq.prod_right_ae]
        with ω hp he hx
      let ν := (TimeMeasure.upTo T).restrict (Iic τ)
      have hp' : Integrable (fun s => (plus j).process s ω ^ 2) ν := hp.integrableOn
      have he' : Integrable (fun s => (η j).process s ω ^ 2) ν := he.integrableOn
      have hx' : Integrable (fun s => (ξ j).process s ω ^ 2) ν := hx.integrableOn
      have hsub : Integrable (fun s => (plus j).process s ω ^ 2 - (η j).process s ω ^ 2) ν :=
        hp'.sub he'
      change ((∫ s, (plus j).process s ω ^ 2 ∂ν) -
        (∫ s, (η j).process s ω ^ 2 ∂ν) - (∫ s, (ξ j).process s ω ^ 2 ∂ν)) / 2 = _
      rw [← integral_sub hp' he', ← integral_sub hsub hx', div_eq_mul_inv, mul_comm,
        ← integral_const_mul]
      apply integral_congr_ae
      exact Eventually.of_forall fun s => by
        change (2 : ℝ)⁻¹ * (((η j).process s ω + (ξ j).process s ω) ^ 2 -
          (η j).process s ω ^ 2 - (ξ j).process s ω ^ 2) =
          (η j).process s ω * (ξ j).process s ω
        ring
    filter_upwards [ae_all_iff.2 hCell] with ω hω
    simp only [E, M, ← Finset.sum_sub_distrib, Finset.sum_div, hω]
  change TendstoInMeasure μ P atTop M
  refine (exists_seq_tendstoInMeasure_atTop_iff hPm).2 ?_
  intro n hn
  obtain ⟨a, ha, hza⟩ := (hZ.comp hn.tendsto_atTop).exists_seq_tendsto_ae
  obtain ⟨b, hb, hxb⟩ := (hX.comp (hn.comp ha).tendsto_atTop).exists_seq_tendsto_ae
  obtain ⟨c, hc, hyc⟩ := (hY.comp ((hn.comp ha).comp hb).tendsto_atTop).exists_seq_tendsto_ae
  refine ⟨a ∘ b ∘ c, ha.comp (hb.comp hc), ?_⟩
  filter_upwards [hza, hxb, hyc, hEnergy, ae_all_iff.2 hPolar] with ω hz hx hy he hq
  have hz' := hz.comp (hb.comp hc).tendsto_atTop
  have hx' := hx.comp hc.tendsto_atTop
  have hLimit := ((hz'.sub hx').sub hy).div_const 2
  simpa only [Function.comp_apply, he, hq] using hLimit

end AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoDyadicPrefixCrossQV
