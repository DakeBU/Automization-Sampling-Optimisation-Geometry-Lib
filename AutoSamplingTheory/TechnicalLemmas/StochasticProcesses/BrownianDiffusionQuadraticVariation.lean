import AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.BrownianMixedQuadraticVariation
import Mathlib.Algebra.Order.Chebyshev

/-! # Quadratic variation of a finite predictable diffusion row -/

namespace AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.BrownianDiffusionQuadraticVariation

open Filter MeasureTheory ProbabilityTheory
open scoped NNReal ENNReal BigOperators
open BrownianMotion BrownianQuadraticVariation BrownianQuadraticVariationL2
  BrownianPredictableQuadraticVariationL2
  BrownianMixedQuadraticVariation FiniteTimeGrid SampledElementaryApproximation
  EuclideanBrownianCoordinates

/-- The compensated square of the actual diffusion-row increments converges
in mean square. The coordinate fourth moments control all product weights. -/
theorem dyadic_predictable_diffusion_row_quadraticVariation_L2
    {Omega kappa : Type*} [MeasurableSpace Omega] [Fintype kappa] [DecidableEq kappa]
    {filtration : Filtration ℝ≥0 (inferInstance : MeasurableSpace Omega)} {mu : Measure Omega}
    {B : ℝ≥0 → Omega → EuclideanSpace ℝ kappa}
    (hB : IsStandardBrownianMotionWithFiltration B filtration mu) (T : ℝ≥0)
    (coeff : (level : ℕ) → Fin (2 ^ level) → kappa → Omega → ℝ)
    (hAdapted : ∀ level i j,
      StronglyMeasurable[filtration
        (regularGridTimes (dyadicMesh T level) (2 ^ level) i.castSucc)] (coeff level i j))
    (hCoeff : ∀ level i j, MemLp (coeff level i j) 4 mu)
    (C : ℝ) (hC : ∀ level i j, (∫ omega, (coeff level i j omega)^4 ∂mu) ≤ C) :
    let error := fun level omega =>
      let times := regularGridTimes (dyadicMesh T level) (2 ^ level)
      ∑ i : Fin (2 ^ level),
        ((∑ j, coeff level i j omega *
          (B (times i.succ) omega j - B (times i.castSucc) omega j))^2 -
        (∑ j, (coeff level i j omega)^2) * ((times i.succ - times i.castSucc : ℝ≥0) : ℝ))
    (∀ level, MemLp (error level) 2 mu) ∧
      Tendsto (fun level => ∫ omega, (error level omega)^2 ∂mu) atTop (nhds 0) := by
  let _ : IsProbabilityMeasure mu :=
    (hB.isStandard.2.2.1 0 1 (by norm_num)
      (0 : StrongDual ℝ (EuclideanSpace ℝ kappa))).isProbabilityMeasure
  let times (level : ℕ) := regularGridTimes (dyadicMesh T level) (2 ^ level)
  let length (level : ℕ) (i : Fin (2^level)) : ℝ :=
    ((times level i.succ - times level i.castSucc : ℝ≥0) : ℝ)
  let inc (level : ℕ) (i : Fin (2^level)) (j : kappa) (omega : Omega) : ℝ :=
    B (times level i.succ) omega j - B (times level i.castSucc) omega j
  let weight (p : kappa × kappa) (level : ℕ) (i : Fin (2^level)) (omega : Omega) : ℝ :=
    coeff level i p.1 omega * coeff level i p.2 omega
  have hWeightAdapt (p : kappa × kappa) (level : ℕ) (i : Fin (2^level)) :
      StronglyMeasurable[filtration (times level i.castSucc)] (weight p level i) :=
    (hAdapted level i p.1).mul (hAdapted level i p.2)
  have hFourth (level : ℕ) (i : Fin (2^level)) (j : kappa) :
      Integrable (fun omega => (coeff level i j omega)^4) mu := by
    have h := (hCoeff level i j).integrable_norm_pow' (p := 4)
    exact h.congr (Eventually.of_forall fun omega => by
      simp only [Real.norm_eq_abs, ← abs_pow]
      exact abs_of_nonneg (by positivity))
  have hPoint (x y : ℝ) : (x*y)^2 ≤ (1/2)*(x^4+y^4) := by
    nlinarith [sq_nonneg (x^2-y^2)]
  have hWeight (p : kappa × kappa) (level : ℕ) (i : Fin (2^level)) :
      MemLp (weight p level i) 2 mu := by
    have hMeas : AEStronglyMeasurable (weight p level i) mu :=
      (hWeightAdapt p level i).mono (filtration.le _)|>.aestronglyMeasurable
    apply (memLp_two_iff_integrable_sq hMeas).2
    refine (((hFourth level i p.1).add (hFourth level i p.2)).const_mul (1/2 : ℝ)).mono'
      (hMeas.pow 2) (Eventually.of_forall fun omega => ?_)
    rw [Real.norm_eq_abs, abs_of_nonneg (sq_nonneg _)]
    exact hPoint _ _
  have hMoment (p : kappa × kappa) (level : ℕ) (i : Fin (2^level)) :
      (∫ omega, (weight p level i omega)^2 ∂mu) ≤ C := by
    have hJ := hFourth level i p.1
    have hK := hFourth level i p.2
    calc
      _ ≤ ∫ omega, (1/2 : ℝ) *
          ((coeff level i p.1 omega)^4 + (coeff level i p.2 omega)^4) ∂mu :=
        integral_mono (hWeight p level i).integrable_sq ((hJ.add hK).const_mul _) (fun omega => by
          exact hPoint _ _)
      _ = (1/2 : ℝ) * ((∫ omega, (coeff level i p.1 omega)^4 ∂mu) +
          (∫ omega, (coeff level i p.2 omega)^4 ∂mu)) := by
        rw [integral_const_mul]
        congr 1
        exact integral_add hJ hK
      _ ≤ C := by linarith [hC level i p.1, hC level i p.2]
  let entry (p : kappa × kappa) (level : ℕ) (omega : Omega) : ℝ :=
    ∑ i, weight p level i omega *
      (inc level i p.1 omega * inc level i p.2 omega -
        if p.1 = p.2 then length level i else 0)
  have hEntry (p : kappa × kappa) :
      (∀ level, MemLp (entry p level) 2 mu) ∧
        Tendsto (fun level => ∫ omega, (entry p level omega)^2 ∂mu) atTop (nhds 0) := by
    rcases p with ⟨j,k⟩
    by_cases hjk : j = k
    · subst k
      have hj := (coordinateFamily hB).isBrownian j
      refine ⟨fun level => ?_, ?_⟩
      · have hmono : Monotone (times level) := by
          intro a b hab
          unfold times regularGridTimes
          gcongr
          exact_mod_cast hab
        simpa only [entry,inc,length,if_pos rfl,if_true,← pow_two,centeredSquaredIncrement,coordinateFamily]
          using (predictable_weighted_quadraticVariationError_L2 hj hmono
            (weight (j,j) level) (hWeightAdapt (j,j) level) (hWeight (j,j) level)).1
      · simpa only [entry,inc,length,if_pos rfl,if_true,← pow_two,centeredSquaredIncrement,coordinateFamily]
          using tendsto_integral_dyadic_predictable_weighted_quadraticVariationError_sq hj T
            (weight (j,j)) (hWeightAdapt (j,j)) (hWeight (j,j)) C (hMoment (j,j))
    · simpa only [entry,inc,if_neg hjk,sub_zero] using
        dyadic_predictable_mixed_increment_sum_L2 hB hjk T (weight (j,k))
          (hWeightAdapt (j,k)) (hWeight (j,k)) C (hMoment (j,k))
  intro error
  have hCell (level : ℕ) (i : Fin (2^level)) (omega : Omega) :
      (∑ j, coeff level i j omega * inc level i j omega)^2 -
          (∑ j, (coeff level i j omega)^2) * length level i =
        ∑ j, ∑ k, weight (j,k) level i omega *
          (inc level i j omega * inc level i k omega - if j = k then length level i else 0) := by
    simp_rw [mul_sub, Finset.sum_sub_distrib]
    congr 1
    · simp only [pow_two, Finset.sum_mul_sum]
      apply Finset.sum_congr rfl
      intro j _
      apply Finset.sum_congr rfl
      intro k _
      simp only [weight]
      ring
    · rw [Finset.sum_mul]
      apply Finset.sum_congr rfl
      intro j _
      simp [weight, mul_ite, pow_two]
  have hError (level : ℕ) (omega : Omega) :
      error level omega = ∑ p : kappa × kappa, entry p level omega := by
    change (∑ i, ((∑ j, coeff level i j omega * inc level i j omega)^2 -
      (∑ j, (coeff level i j omega)^2) * length level i)) = _
    simp_rw [hCell]
    rw [← Finset.univ_product_univ, Finset.sum_product, Finset.sum_comm]
    apply Finset.sum_congr rfl
    intro j _
    rw [Finset.sum_comm]
  have hErrorMem (level : ℕ) : MemLp (error level) 2 mu :=
    (memLp_congr_ae (Eventually.of_forall (hError level))).2
      (memLp_finsetSum Finset.univ (fun p _ => (hEntry p).1 level))
  have hUpper (level : ℕ) :
      (∫ omega, (error level omega)^2 ∂mu) ≤
        (Fintype.card (kappa × kappa) : ℝ) *
          ∑ p : kappa × kappa, ∫ omega, (entry p level omega)^2 ∂mu := by
    have hInt (p : kappa × kappa) := ((hEntry p).1 level).integrable_sq
    have hSum := integrable_finsetSum Finset.univ (fun p _ => hInt p)
    calc
      _ ≤ ∫ omega, (Fintype.card (kappa × kappa) : ℝ) *
          ∑ p : kappa × kappa, (entry p level omega)^2 ∂mu :=
        integral_mono (hErrorMem level).integrable_sq (hSum.const_mul _) (fun omega => by
          rw [hError]
          simpa only [Finset.card_univ] using
            (sq_sum_le_card_mul_sum_sq (s := Finset.univ) (f := fun p => entry p level omega)))
      _ = _ := by
        rw [integral_const_mul, integral_finsetSum Finset.univ (fun p _ => hInt p)]
  have hLimit := (tendsto_finsetSum (Finset.univ : Finset (kappa × kappa))
    (fun p _ => (hEntry p).2)).const_mul (Fintype.card (kappa × kappa) : ℝ)
  refine ⟨hErrorMem, tendsto_const_nhds.squeeze ?_ (fun level => integral_nonneg fun _ => sq_nonneg _) hUpper⟩
  simpa using hLimit

#print axioms dyadic_predictable_diffusion_row_quadraticVariation_L2

end AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.BrownianDiffusionQuadraticVariation
