import AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.CountableConvergenceInMeasure
import AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.DyadicWeightedLimits
import AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoDyadicPrefixCrossQV

namespace AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoDyadicWeightedCovariation

open Filter MeasureTheory Set
open scoped BigOperators NNReal Topology
open BrownianMotion ProgressiveL2 ElementaryItoIntegral SampledElementaryApproximation
  DyadicElementaryRefinement EuclideanBrownianCoordinates ItoIntegralProcess ItoDyadicPrefixQV
  ItoDyadicPrefixCrossQV CountableConvergenceInMeasure DyadicWeightedLimits
open AutoSamplingTheory.TechnicalLemmas.Analysis.PrefixIntegral

/-- Continuous left-endpoint weights against the covariation of two actual
completed Itô rows converge to the weighted integral of the diffusion inner product. -/
theorem tendstoInMeasure_dyadic_weighted_covariation_of_ito_rows
    {Ω J : Type*} [MeasurableSpace Ω] [Fintype J] [DecidableEq J]
    {filtration : Filtration ℝ≥0 (inferInstance : MeasurableSpace Ω)}
    {μ : Measure Ω} [IsFiniteMeasure μ] {T : ℝ≥0}
    {B : ℝ≥0 → Ω → EuclideanSpace ℝ J}
    (hB : IsStandardBrownianMotionWithFiltration B filtration μ) (hT : 0 < T)
    (hUsual : SatisfiesUsualConditions filtration μ)
    (η ξ : J → ProgressiveL2Integrand filtration μ T)
    (A C W : ℝ≥0 → Ω → ℝ)
    (hAmeas : ∀ t ≤ T, AEStronglyMeasurable (A t) μ)
    (hCmeas : ∀ t ≤ T, AEStronglyMeasurable (C t) μ)
    (hWmeas : ∀ t ≤ T, AEStronglyMeasurable (W t) μ)
    (hA : ∀ᵐ ω ∂μ, ContinuousOn (fun t => A t ω) (Icc 0 T) ∧
      BoundedVariationOn (fun t => A t ω) (Icc 0 T))
    (hC : ∀ᵐ ω ∂μ, ContinuousOn (fun t => C t ω) (Icc 0 T) ∧
      BoundedVariationOn (fun t => C t ω) (Icc 0 T))
    (hW : ∀ᵐ ω ∂μ, ContinuousOn (fun t => W t ω) (Icc 0 T)) :
    let X := fun t ω => A t ω + ∑ j : J,
      itoIntegralProcess (η j) hT ((coordinateFamily hB).isBrownian j) hUsual t ω
    let Y := fun t ω => C t ω + ∑ j : J,
      itoIntegralProcess (ξ j) hT ((coordinateFamily hB).isBrownian j) hUsual t ω
    TendstoInMeasure μ (fun n ω =>
      let t := regularGridTimes (dyadicMesh T n) (2 ^ n)
      ∑ i : Fin (2 ^ n), W (t i.castSucc) ω *
        ((X (t i.succ) ω - X (t i.castSucc) ω) * (Y (t i.succ) ω - Y (t i.castSucc) ω)))
      atTop (fun ω => ∫ s, W s ω *
        (∑ j : J, (η j).process s ω * (ξ j).process s ω) ∂(TimeMeasure.upTo T)) := by
  intro X Y
  let t (n : ℕ) := regularGridTimes (dyadicMesh T n) (2 ^ n)
  let Δ (F : ℝ≥0 → Ω → ℝ) (n : ℕ) (i : Fin (2 ^ n)) (ω : Ω) :=
    F (t n i.succ) ω - F (t n i.castSucc) ω
  let z (ω : Ω) (n : ℕ) (i : Fin (2 ^ n)) := Δ X n i ω * Δ Y n i ω
  let b (ω : Ω) (s : ℝ≥0) := ∑ j : J, (η j).process s ω * (ξ j).process s ω
  let S (n : ℕ) (ω : Ω) := ∑ i : Fin (2 ^ n), W (t n i.castSucc) ω * z ω n i
  let P (m : ℕ) (k : Fin (2 ^ m + 1)) (n : ℕ) (ω : Ω) :=
    ∑ i : Fin (2 ^ n), if t n i.succ ≤ t m k then z ω n i else 0
  let Q (F : ℝ≥0 → Ω → ℝ) (n : ℕ) (ω : Ω) :=
    ∑ i : Fin (2 ^ n), if t n i.succ ≤ t 0 (Fin.last (2 ^ (0 : ℕ))) then Δ F n i ω ^ 2 else 0
  let E (r : J → ProgressiveL2Integrand filtration μ T) (ω : Ω) :=
    ∑ j : J, ∫ s in Iic (t 0 (Fin.last (2 ^ (0 : ℕ)))), (r j).process s ω ^ 2 ∂(TimeMeasure.upTo T)
  have ht (n : ℕ) (i : Fin (2 ^ n + 1)) : t n i ≤ T :=
    ((regularGridTimes_strictMono (dyadicMesh_pos hT n) _).monotone (Fin.le_last i)).trans_eq
      (regularDyadic_last_time T n)
  have hProduct : ∀ᵐ ω ∂μ, ∀ j : J,
      Integrable (fun s => (η j).process s ω * (ξ j).process s ω) (TimeMeasure.upTo T) :=
    ae_all_iff.2 fun j => ((η j).memLp.integrable_mul (ξ j).memLp).prod_right_ae
  have hPrefix (m : ℕ) (k : Fin (2 ^ m + 1)) :
      TendstoInMeasure μ (P m k) atTop (fun ω => prefixIntegral (b ω) T (t m k)) := by
    apply TendstoInMeasure.congr_right ?_
      (tendstoInMeasure_dyadic_prefix_mul_increments_of_ito_rows
        hB hT hUsual η ξ A C hAmeas hCmeas hA hC m k)
    filter_upwards [hProduct] with ω hω
    have hRestrict (j : J) : Integrable (fun s => (η j).process s ω * (ξ j).process s ω)
        ((TimeMeasure.upTo T).restrict (Iio (t m k))) := (hω j).integrableOn
    rw [prefixIntegral_eq_setIntegral, min_eq_left (ht m k)]
    change (∑ j : J, ∫ s in Iic (t m k),
      (η j).process s ω * (ξ j).process s ω ∂(TimeMeasure.upTo T)) =
      ∫ s in Iio (t m k), ∑ j : J, (η j).process s ω * (ξ j).process s ω ∂(TimeMeasure.upTo T)
    rw [integral_finsetSum _ (fun j _ => hRestrict j)]
    exact Finset.sum_congr rfl fun _ _ => setIntegral_congr_set (Iio_ae_eq_Iic' (by simp)).symm
  have hQX : TendstoInMeasure μ (Q X) atTop (E η) :=
    tendstoInMeasure_dyadic_prefix_sq_increments_of_ito_row hB hT hUsual η A hAmeas hA 0 (Fin.last _)
  have hQY : TendstoInMeasure μ (Q Y) atTop (E ξ) :=
    tendstoInMeasure_dyadic_prefix_sq_increments_of_ito_row hB hT hUsual ξ C hCmeas hC 0 (Fin.last _)
  have hI (r : J → ProgressiveL2Integrand filtration μ T) (s : ℝ≥0) :
      AEStronglyMeasurable (fun ω => ∑ j : J,
        itoIntegralProcess (r j) hT ((coordinateFamily hB).isBrownian j) hUsual s ω) μ :=
    (Finset.aestronglyMeasurable_sum Finset.univ fun j _ =>
      (((itoIntegralProcess_stronglyAdapted (r j) hT
        ((coordinateFamily hB).isBrownian j) hUsual) s).mono
          (filtration.le s)).aestronglyMeasurable).congr
      (Eventually.of_forall fun ω => by simp only [Finset.sum_apply])
  have hSm (n : ℕ) : AEStronglyMeasurable (S n) μ := by
    have hXm (s : ℝ≥0) (hs : s ≤ T) : AEStronglyMeasurable (X s) μ :=
      (hAmeas s hs).add (hI η s)
    have hYm (s : ℝ≥0) (hs : s ≤ T) : AEStronglyMeasurable (Y s) μ :=
      (hCmeas s hs).add (hI ξ s)
    have hCell (i : Fin (2 ^ n)) :
        AEStronglyMeasurable (fun ω => W (t n i.castSucc) ω * z ω n i) μ :=
      (hWmeas _ (ht n i.castSucc)).mul
        (((hXm _ (ht n i.succ)).sub (hXm _ (ht n i.castSucc))).mul
          ((hYm _ (ht n i.succ)).sub (hYm _ (ht n i.castSucc))))
    exact (Finset.aestronglyMeasurable_sum Finset.univ fun i _ => hCell i).congr
      (Eventually.of_forall fun ω => by simp only [S, Finset.sum_apply])
  let K := (Σ m : ℕ, Fin (2 ^ m + 1)) ⊕ Bool
  let F : K → ℕ → Ω → ℝ :=
    Sum.elim (fun k => P k.1 k.2) (fun side => if side then Q Y else Q X)
  let G : K → Ω → ℝ :=
    Sum.elim (fun k ω => prefixIntegral (b ω) T (t k.1 k.2))
      (fun side => if side then E ξ else E η)
  have hF : ∀ k, TendstoInMeasure μ (F k) atTop (G k) := by
    rintro (k | side)
    · exact hPrefix k.1 k.2
    · cases side
      · exact hQX
      · exact hQY
  change TendstoInMeasure μ S atTop (fun ω => ∫ s, W s ω * b ω s ∂(TimeMeasure.upTo T))
  refine (exists_seq_tendstoInMeasure_atTop_iff hSm).2 ?_
  intro u hu
  have hFamily (k : K) : TendstoInMeasure μ (F k ∘ u) atTop (G k) :=
    (hF k).comp hu.tendsto_atTop
  obtain ⟨v, hv, hPath⟩ := exists_seq_tendsto_ae_of_countable hFamily
  refine ⟨v, hv, ?_⟩
  filter_upwards [hPath, hProduct, hW] with ω hω hp hw
  let σ := u ∘ v
  have hσ : Tendsto σ atTop atTop := (hu.comp hv).tendsto_atTop
  have hEnergy : Tendsto (fun n => (Q X (σ n) ω + Q Y (σ n) ω) / 2) atTop
      (𝓝 ((E η ω + E ξ ω) / 2)) :=
    ((hω (.inr false)).add (hω (.inr true))).div_const 2
  obtain ⟨M, hM⟩ := hEnergy.bddAbove_range
  have hVar (n : ℕ) : ∑ i : Fin (2 ^ σ n), |z ω (σ n) i| ≤ M := by
    calc
      _ ≤ ∑ i : Fin (2 ^ σ n), (Δ X (σ n) i ω ^ 2 + Δ Y (σ n) i ω ^ 2) / 2 := by
        apply Finset.sum_le_sum
        intro i _
        dsimp only [z]
        rw [abs_mul]
        have h := sq_nonneg (|Δ X (σ n) i ω| - |Δ Y (σ n) i ω|)
        nlinarith only [h, sq_abs (Δ X (σ n) i ω), sq_abs (Δ Y (σ n) i ω)]
      _ = (Q X (σ n) ω + Q Y (σ n) ω) / 2 := by
        rw [← Finset.sum_div, Finset.sum_add_distrib]
        simp only [Q, show t 0 (Fin.last (2 ^ (0 : ℕ))) = T from regularDyadic_last_time T 0,
          if_pos (ht _ _)]
      _ ≤ M := hM (mem_range_self n)
  have hb : Integrable (b ω) (TimeMeasure.upTo T) := integrable_finsetSum _ (fun j _ => hp j)
  exact tendsto_dyadic_weighted_sums_of_prefix_limits hT (fun s => W s ω) (b ω) hw hb
    (z ω) σ hσ ⟨M, hVar⟩ (fun m k => hω (.inl ⟨m, k⟩))

end AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoDyadicWeightedCovariation
