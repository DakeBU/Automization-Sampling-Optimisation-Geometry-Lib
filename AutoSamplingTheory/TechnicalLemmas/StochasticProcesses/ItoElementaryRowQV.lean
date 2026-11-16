import AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.BrownianDiffusionQuadraticVariation
import AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoIntegralElementaryIncrement
import AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ProgressivePathEnergy

/-! # Dyadic quadratic variation of actual elementary Itô rows -/

namespace AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoElementaryRowQV

open Filter MeasureTheory ProbabilityTheory
open scoped NNReal ENNReal BigOperators
open BrownianMotion ProgressiveL2 ProgressiveL2Density ElementaryItoIntegral ElementaryItoIsometry
  SampledElementaryApproximation EuclideanBrownianCoordinates DyadicElementaryRefinement
  ItoIntegralProcess ItoTerminalCompletion ItoIntegralElementaryIncrement
  BrownianDiffusionQuadraticVariation ProgressivePathEnergy

variable {Omega : Type*} [MeasurableSpace Omega]
  {filtration : Filtration ℝ≥0 (inferInstance : MeasurableSpace Omega)} {T : ℝ≥0}

private def cell (q : DyadicElementaryProcess filtration T)
    {level : ℕ} (h : q.level = level) (i : Fin (2 ^ level)) : Fin (2 ^ q.level) :=
  Fin.cast (congrArg (fun n : ℕ => 2 ^ n) h.symm) i

private theorem grid_endpoints (q : DyadicElementaryProcess filtration T)
    {level : ℕ} (h : q.level = level) (i : Fin (2 ^ level)) :
    q.process.times (cell q h i).castSucc =
      regularGridTimes (dyadicMesh T level) (2 ^ level) i.castSucc ∧
    q.process.times (cell q h i).succ =
      regularGridTimes (dyadicMesh T level) (2 ^ level) i.succ := by
  subst level
  simp [cell, q.times_eq]

private theorem elementary_grid_compensator (q : DyadicElementaryProcess filtration T)
    {level : ℕ} (h : q.level = level) (omega : Omega) :
    let times := regularGridTimes (dyadicMesh T level) (2 ^ level)
    (∫ t, (q.process.value t omega)^2 ∂(TimeMeasure.upTo T)) =
      ∑ i : Fin (2 ^ level), (q.process.coeff (cell q h i) omega)^2 *
        ((times i.succ - times i.castSucc : ℝ≥0) : ℝ) := by
  subst level
  have htime (k : Fin (2 ^ q.level + 1)) : q.process.times k ≤ T := by
    have hlast : q.process.times (Fin.last (2 ^ q.level)) = T := by
      rw [q.times_eq, regularDyadic_last_time]
    exact (q.process.times_strictMono.monotone (Fin.le_last k)).trans_eq hlast
  simp only [elementary_integral_value_sq, min_eq_left (htime _), cell, Fin.cast_eq_self]
  rw [q.times_eq]

/-- The Brownian grid calculation applies to the increments of the completed
elementary integrals and to their actual pathwise time energies. -/
theorem tendsto_dyadic_elementary_ito_row_quadraticVariation_L1
    {Omega J : Type*} [MeasurableSpace Omega] [Fintype J] [DecidableEq J]
    {filtration : Filtration ℝ≥0 (inferInstance : MeasurableSpace Omega)}
    {mu : Measure Omega} [IsFiniteMeasure mu] {T : ℝ≥0}
    {B : ℝ≥0 → Omega → EuclideanSpace ℝ J}
    (hB : IsStandardBrownianMotionWithFiltration B filtration mu) (hT : 0 < T)
    (hUsual : SatisfiesUsualConditions filtration mu)
    (q : ℕ → J → DyadicElementaryProcess filtration T)
    (hlevel : ∀ level j, (q level j).level = level)
    (C : ℝ) (hC : ∀ level j i, (∫ omega, ((q level j).process.coeff i omega)^4 ∂mu) ≤ C) :
    let hcoord := (coordinateFamily hB).isBrownian
    let eta := fun level j => elementaryIntegrand (q level j) (hcoord j)
    let row := fun level t omega =>
      ∑ j : J, itoIntegralProcess (eta level j) hT (hcoord j) hUsual t omega
    let error := fun level omega =>
      let times := regularGridTimes (dyadicMesh T level) (2 ^ level)
      (∑ i : Fin (2 ^ level), (row level (times i.succ) omega -
        row level (times i.castSucc) omega)^2) -
      ∑ j : J, ∫ t, (eta level j).process t omega ^ 2 ∂(TimeMeasure.upTo T)
    (∀ level, MemLp (error level) 2 mu) ∧
      Tendsto (fun level => ∫ omega, |error level omega| ∂mu) atTop (nhds 0) := by
  intro hcoord eta row error
  let _ : IsProbabilityMeasure mu :=
    (hB.isStandard.2.2.1 0 1 (by norm_num) (0 : StrongDual ℝ (EuclideanSpace ℝ J))).isProbabilityMeasure
  let times (level : ℕ) := regularGridTimes (dyadicMesh T level) (2 ^ level)
  let coeff (level : ℕ) (i : Fin (2 ^ level)) (j : J) :=
    (q level j).process.coeff (cell (q level j) (hlevel level j) i)
  have hadapted (level : ℕ) (i : Fin (2 ^ level)) (j : J) :
      StronglyMeasurable[filtration (times level i.castSucc)] (coeff level i j) := by
    have hEq : (q level j).process.times (cell (q level j) (hlevel level j) i).castSucc =
        times level i.castSucc := (grid_endpoints (q level j) (hlevel level j) i).1
    exact Eq.mp (congrArg (fun t : ℝ≥0 => StronglyMeasurable[filtration t] (coeff level i j)) hEq)
      ((q level j).process.coeff_stronglyMeasurable (cell (q level j) (hlevel level j) i))
  have hcoeff (level : ℕ) (i : Fin (2 ^ level)) (j : J) :
      MemLp (coeff level i j) 4 mu := coeff_memLp (q level j).process mu _ 4
  have hmoment (level : ℕ) (i : Fin (2 ^ level)) (j : J) :
      (∫ omega, (coeff level i j omega)^4 ∂mu) ≤ C := hC level j _
  let discrete := fun level omega =>
    ∑ i : Fin (2 ^ level),
      ((∑ j : J, coeff level i j omega *
        (B (times level i.succ) omega j - B (times level i.castSucc) omega j))^2 -
      (∑ j : J, (coeff level i j omega)^2) *
        ((times level i.succ - times level i.castSucc : ℝ≥0) : ℝ))
  have hDis : (∀ level, MemLp (discrete level) 2 mu) ∧
      Tendsto (fun level => ∫ omega, (discrete level omega)^2 ∂mu) atTop (nhds 0) :=
    dyadic_predictable_diffusion_row_quadraticVariation_L2 hB T coeff hadapted hcoeff C hmoment
  have hInc (level : ℕ) (i : Fin (2 ^ level)) (j : J) :
      ∀ᵐ omega ∂mu,
        itoIntegralProcess (eta level j) hT (hcoord j) hUsual (times level i.succ) omega -
          itoIntegralProcess (eta level j) hT (hcoord j) hUsual (times level i.castSucc) omega =
          coeff level i j omega *
            (B (times level i.succ) omega j - B (times level i.castSucc) omega j) := by
    have h := itoIntegralProcess_elementary_grid_increment_ae
      (q level j) hT (hcoord j) hUsual (cell (q level j) (hlevel level j) i)
    dsimp only at h
    rw [(grid_endpoints (q level j) (hlevel level j) i).1,
      (grid_endpoints (q level j) (hlevel level j) i).2] at h
    exact h
  have hEnergy (level : ℕ) (omega : Omega) :
      (∑ j : J, ∫ t, (eta level j).process t omega ^ 2 ∂(TimeMeasure.upTo T)) =
        ∑ i : Fin (2 ^ level), (∑ j : J, (coeff level i j omega)^2) *
          ((times level i.succ - times level i.castSucc : ℝ≥0) : ℝ) := by
    change (∑ j : J, ∫ t, ((q level j).process.value t omega)^2 ∂(TimeMeasure.upTo T)) = _
    simp_rw [elementary_grid_compensator (q level _) (hlevel level _)]
    rw [Finset.sum_comm]
    exact Finset.sum_congr rfl (fun i _ => (Finset.sum_mul ..).symm)
  have hEq (level : ℕ) : error level =ᵐ[mu] discrete level := by
    filter_upwards [ae_all_iff.2 fun i => ae_all_iff.2 (hInc level i)] with omega hpoint
    change (∑ i : Fin (2 ^ level), (row level (times level i.succ) omega -
      row level (times level i.castSucc) omega)^2) -
      (∑ j : J, ∫ t, (eta level j).process t omega ^ 2 ∂(TimeMeasure.upTo T)) = _
    rw [hEnergy]
    simp only [discrete, Finset.sum_sub_distrib]
    congr 1
    apply Finset.sum_congr rfl
    intro i _
    congr 1
    dsimp only [row]
    rw [← Finset.sum_sub_distrib]
    exact Finset.sum_congr rfl (fun j _ => hpoint i j)
  have hmem (level : ℕ) : MemLp (error level) 2 mu :=
    (memLp_congr_ae (hEq level)).2 (hDis.1 level)
  have hSqLim : Tendsto (fun level => ∫ omega, (error level omega)^2 ∂mu) atTop (nhds 0) := by
    have hEqIntegral (level : ℕ) :
        (∫ omega, (error level omega)^2 ∂mu) = ∫ omega, (discrete level omega)^2 ∂mu :=
      integral_congr_ae ((hEq level).mono fun _ h => congrArg (· ^ (2 : ℕ)) h)
    exact (tendsto_congr' (Eventually.of_forall hEqIntegral)).2 hDis.2
  have hUpper (level : ℕ) :
      (∫ omega, |error level omega| ∂mu) ≤ Real.sqrt (∫ omega, (error level omega)^2 ∂mu) := by
    have hholder : Real.HolderConjugate 2 2 := by
      rw [Real.holderConjugate_iff]
      norm_num
    have h := integral_mul_norm_le_Lp_mul_Lq hholder (μ := mu)
      (f := error level) (g := fun _ : Omega => (1 : ℝ))
      (by simpa using hmem level) (memLp_const 1)
    simpa [Real.norm_eq_abs, Real.rpow_two, sq_abs, Real.sqrt_eq_rpow] using h
  have hRoot : Tendsto (fun level => Real.sqrt (∫ omega, (error level omega)^2 ∂mu))
      atTop (nhds 0) := by
    simpa only [Function.comp_def, Real.sqrt_zero] using
      Real.continuous_sqrt.continuousAt.tendsto.comp hSqLim
  exact ⟨hmem, tendsto_const_nhds.squeeze hRoot (fun _ => integral_nonneg fun _ => abs_nonneg _) hUpper⟩

#print axioms tendsto_dyadic_elementary_ito_row_quadraticVariation_L1

end AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoElementaryRowQV
