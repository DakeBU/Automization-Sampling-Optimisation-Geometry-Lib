import AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.BrownianQuadraticVariationL2

namespace AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.BrownianPredictableQuadraticVariationL2

open Filter MeasureTheory ProbabilityTheory
open scoped BigOperators NNReal
open BrownianMotion BrownianQuadraticVariation BrownianQuadraticVariationL2
  FiniteTimeGrid SampledElementaryApproximation

variable {Omega : Type*} {m : MeasurableSpace Omega}
  {mu : Measure Omega} {B : ℝ≥0 → Omega → ℝ}

private theorem centered_cell_memLp_two
    (hB : IsPreBrownianReal B mu) (s t : ℝ≥0) :
    MemLp (fun omega => (B t omega - B s omega) ^ 2 - ((t - s : ℝ≥0) : ℝ)) 2 mu := by
  let _ : IsProbabilityMeasure mu := hB.isGaussianProcess.isProbabilityMeasure
  let X (omega : Omega) := B t omega - B s omega
  have hX : MemLp X 4 mu :=
    hB.isGaussianProcess.hasGaussianLaw_fun_sub.memLp (p := 4) (by norm_num)
  have hSquare : MemLp (fun omega => X omega ^ 2) 2 mu := by
    apply (memLp_two_iff_integrable_sq (hX.aestronglyMeasurable.pow 2)).2
    refine (hX.integrable_norm_pow' (p := 4)).congr (ae_of_all mu fun omega => ?_)
    change ‖X omega‖ ^ 4 = (X omega ^ 2) ^ 2
    rw [Real.norm_eq_abs, ← abs_pow, abs_of_nonneg (by positivity : 0 ≤ X omega ^ 4)]
    ring
  exact hSquare.sub (memLp_const _)

private theorem integral_centered_cell_sq
    (hB : IsPreBrownianReal B mu) {s t : ℝ≥0} (hst : s ≤ t) :
    (∫ omega, ((B t omega - B s omega) ^ 2 - ((t - s : ℝ≥0) : ℝ)) ^ 2 ∂mu) =
      2 * (((t - s : ℝ≥0) : ℝ) ^ 2) := by
  let times : Fin 2 → ℝ≥0 := Fin.cons s (fun _ => t)
  have hMono : Monotone times := by
    intro i j hij
    fin_cases i <;> fin_cases j <;> simp [times] at hij ⊢
    exact hst
  simpa [times, quadraticVariationError, centeredSquaredIncrement] using
    integral_quadraticVariationError_sq hB hMono

private theorem regularGridTimes_monotone (delta : ℝ≥0) (n : ℕ) :
    Monotone (regularGridTimes delta n) := by
  intro i j hij
  unfold regularGridTimes
  gcongr
  exact_mod_cast hij

private theorem sum_dyadic_cellLengths_sq (T : ℝ≥0) (level : ℕ) :
    ∑ i : Fin (2 ^ level),
        (((regularGridTimes (dyadicMesh T level) (2 ^ level) i.succ -
          regularGridTimes (dyadicMesh T level) (2 ^ level) i.castSucc : ℝ≥0) : ℝ) ^ 2) =
      (T : ℝ) * ((dyadicMesh T level : ℝ≥0) : ℝ) := by
  simp_rw [dyadic_activeCell_right, add_tsub_cancel_left]
  rw [Finset.sum_const, Finset.card_fin, nsmul_eq_mul]
  simp only [dyadicMesh, NNReal.coe_div, Nat.cast_pow, Nat.cast_ofNat]
  have hpow : (2 : ℝ) ^ level ≠ 0 := by positivity
  field_simp
  norm_cast
  ac_rfl

/-- Predictable weights preserve orthogonality of compensated squared Brownian
increments. The weights need only have finite second moments. -/
theorem predictable_weighted_quadraticVariationError_L2
    {filtration : Filtration ℝ≥0 m}
    (hB : IsBrownianMotionWithFiltration B filtration mu)
    {n : ℕ} {times : Fin (n + 1) → ℝ≥0} (hmono : Monotone times)
    (weight : Fin n → Omega → ℝ)
    (hAdapted : ∀ i, StronglyMeasurable[filtration (times i.castSucc)] (weight i))
    (hWeight : ∀ i, MemLp (weight i) 2 mu) :
    let error := fun omega => ∑ i, weight i omega * centeredSquaredIncrement B times i omega
    MemLp error 2 mu ∧
      (∫ omega, (error omega)^2 ∂mu) =
        ∑ i, (∫ omega, (weight i omega)^2 ∂mu) *
          (2 * (((times i.succ - times i.castSucc : ℝ≥0) : ℝ)^2)) := by
  let _ : IsProbabilityMeasure mu := hB.isProbabilityMeasure
  let Z : Fin n → Omega → ℝ := fun i => centeredSquaredIncrement B times i
  let W : Fin n → Omega → ℝ := fun i omega => weight i omega * Z i omega
  have hPre := hB.isBrownian.toIsPreBrownianReal
  have hZ (i : Fin n) : MemLp (Z i) 2 mu :=
    centered_cell_memLp_two hPre _ _
  have hZMeas (i : Fin n) : StronglyMeasurable[filtration (times i.succ)] (Z i) := by
    have hs := (hB.stronglyAdapted (times i.castSucc)).mono
      (filtration.mono (hmono (Fin.castSucc_le_succ i)))
    exact (((hB.stronglyAdapted (times i.succ)).sub hs).pow 2).sub stronglyMeasurable_const
  have hInd (i : Fin n) (X : Omega → ℝ)
      (hX : StronglyMeasurable[filtration (times i.castSucc)] X) : IndepFun X (Z i) mu := by
    have hi := hB.indepFun_increment_of_stronglyMeasurable (hmono (Fin.castSucc_le_succ i)) hX
    exact hi.comp (φ := id)
      (ψ := fun x : ℝ => x^2 - ((times i.succ - times i.castSucc : ℝ≥0) : ℝ))
      measurable_id (by fun_prop)
  have hIndSq (i : Fin n) : IndepFun (fun omega => (weight i omega)^2)
      (fun omega => (Z i omega)^2) mu :=
    (hInd i (weight i) (hAdapted i)).comp
      (φ := fun x : ℝ => x^2) (ψ := fun x : ℝ => x^2) (by fun_prop) (by fun_prop)
  have hW (i : Fin n) : MemLp (W i) 2 mu := by
    have hMeas : AEStronglyMeasurable (W i) mu :=
      (hWeight i).aestronglyMeasurable.mul (hZ i).aestronglyMeasurable
    apply (memLp_two_iff_integrable_sq hMeas).2
    simpa only [W, mul_pow, Pi.mul_def] using
      (hIndSq i).integrable_mul (hWeight i).integrable_sq (hZ i).integrable_sq
  have hOrdered {i j : Fin n} (hij : i < j) :
      (∫ omega, W i omega * W j omega ∂mu) = 0 := by
    have hend : times i.succ ≤ times j.castSucc := hmono (Fin.le_iff_val_le_val.mpr (by
      have h : i.val < j.val := hij
      simpa using h))
    let past : Omega → ℝ := fun omega => W i omega * weight j omega
    have hpast : StronglyMeasurable[filtration (times j.castSucc)] past := by
      have hw := (hAdapted i).mono
        (filtration.mono ((hmono (Fin.castSucc_le_succ i)).trans hend))
      have hz := (hZMeas i).mono (filtration.mono hend)
      exact (hw.mul hz).mul (hAdapted j)
    have hprod := (hInd j past hpast).integral_fun_mul_eq_mul_integral
      (hpast.mono (filtration.le _)).aestronglyMeasurable (hZ j).aestronglyMeasurable
    have hmean : (∫ omega, Z j omega ∂mu) = 0 :=
      BrownianQuadraticVariation.integral_centered_increment_sq_eq_zero hB (hmono (Fin.castSucc_le_succ j))
    calc
      (∫ omega, W i omega * W j omega ∂mu) =
          ∫ omega, past omega * Z j omega ∂mu := by
        apply integral_congr_ae
        filter_upwards [] with omega
        simp only [past,W]
        ring
      _ = 0 := by rw [hprod, hmean, mul_zero]
  have hCross {i j : Fin n} (hij : i ≠ j) :
      (∫ omega, W i omega * W j omega ∂mu) = 0 := by
    rcases lt_or_gt_of_ne hij with h | h
    · exact hOrdered h
    · simpa only [mul_comm] using hOrdered h
  have hDiag (i : Fin n) : (∫ omega, (W i omega)^2 ∂mu) =
      (∫ omega, (weight i omega)^2 ∂mu) *
        (2 * (((times i.succ - times i.castSucc : ℝ≥0) : ℝ)^2)) := by
    simp only [W, mul_pow]
    rw [(hIndSq i).integral_fun_mul_eq_mul_integral
      ((hWeight i).aestronglyMeasurable.pow 2) ((hZ i).aestronglyMeasurable.pow 2)]
    rw [show (∫ omega, (Z i omega)^2 ∂mu) =
        2 * (((times i.succ - times i.castSucc : ℝ≥0) : ℝ)^2) from
      integral_centered_cell_sq hPre (hmono (Fin.castSucc_le_succ i))]
  have hPair (i j : Fin n) : Integrable (fun omega => W i omega * W j omega) mu :=
    (hW i).integrable_mul (hW j)
  intro error
  refine ⟨memLp_finsetSum Finset.univ (fun i _ => hW i), ?_⟩
  calc
    (∫ omega, (error omega)^2 ∂mu) =
        ∫ omega, ∑ i, ∑ j, W i omega * W j omega ∂mu := by
      simp only [error, W, Z, pow_two, Finset.sum_mul_sum]
    _ = ∑ i, ∑ j, ∫ omega, W i omega * W j omega ∂mu := by
      rw [integral_finsetSum]
      · apply Finset.sum_congr rfl
        intro i _
        rw [integral_finsetSum]
        intro j _
        exact hPair i j
      · intro i _
        exact integrable_finsetSum _ fun j _ => hPair i j
    _ = ∑ i, ∫ omega, (W i omega)^2 ∂mu := by
      apply Finset.sum_congr rfl
      intro i _
      rw [Finset.sum_eq_single i]
      · simp only [pow_two]
      · intro j _ hji
        exact hCross hji.symm
      · simp
    _ = _ := Finset.sum_congr rfl fun i _ => hDiag i

/-- A uniform second-moment bound on predictable dyadic weights gives
vanishing mean-square compensated quadratic-variation error. -/
theorem tendsto_integral_dyadic_predictable_weighted_quadraticVariationError_sq
    {filtration : Filtration ℝ≥0 m}
    (hB : IsBrownianMotionWithFiltration B filtration mu) (T : ℝ≥0)
    (weight : (level : ℕ) → Fin (2 ^ level) → Omega → ℝ)
    (hAdapted : ∀ level i,
      StronglyMeasurable[filtration
        (regularGridTimes (dyadicMesh T level) (2 ^ level) i.castSucc)] (weight level i))
    (hWeight : ∀ level i, MemLp (weight level i) 2 mu)
    (C : ℝ) (hC : ∀ level i, (∫ omega, (weight level i omega)^2 ∂mu) ≤ C) :
    Tendsto (fun level =>
      ∫ omega, (∑ i, weight level i omega * centeredSquaredIncrement B
        (regularGridTimes (dyadicMesh T level) (2 ^ level)) i omega)^2 ∂mu)
      atTop (nhds 0) := by
  have hUpper (level : ℕ) :
      (∫ omega, (∑ i, weight level i omega * centeredSquaredIncrement B
          (regularGridTimes (dyadicMesh T level) (2 ^ level)) i omega)^2 ∂mu) ≤
        (2 * C) * ((T : ℝ) * (dyadicMesh T level : ℝ)) := by
    let times := regularGridTimes (dyadicMesh T level) (2 ^ level)
    rw [(predictable_weighted_quadraticVariationError_L2 hB
      (regularGridTimes_monotone (dyadicMesh T level) (2 ^ level))
      (weight level) (hAdapted level) (hWeight level)).2]
    calc
      _ ≤ ∑ i : Fin (2 ^ level), C *
          (2 * (((times i.succ - times i.castSucc : ℝ≥0) : ℝ)^2)) :=
        Finset.sum_le_sum fun i _ => mul_le_mul_of_nonneg_right (hC level i) (by positivity)
      _ = ∑ i : Fin (2 ^ level), (2 * C) *
          (((times i.succ - times i.castSucc : ℝ≥0) : ℝ)^2) :=
        Finset.sum_congr rfl fun i _ => by ring
      _ = _ := by
        rw [← Finset.mul_sum, show (∑ i : Fin (2 ^ level),
          (((times i.succ - times i.castSucc : ℝ≥0) : ℝ)^2)) =
            (T : ℝ) * (dyadicMesh T level : ℝ) from sum_dyadic_cellLengths_sq T level]
  have hLimit := ((FiniteTimeGrid.dyadicMesh_tendsto_zero T).const_mul (T : ℝ)).const_mul (2 * C)
  refine tendsto_const_nhds.squeeze ?_ (fun level => integral_nonneg fun _ => sq_nonneg _) hUpper
  simpa using hLimit

end AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.BrownianPredictableQuadraticVariationL2
