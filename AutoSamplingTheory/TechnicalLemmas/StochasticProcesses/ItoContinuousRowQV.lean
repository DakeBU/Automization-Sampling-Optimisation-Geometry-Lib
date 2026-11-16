import AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoElementaryRowQV
import AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoIntegralGridStability

/-! # Dyadic quadratic variation of completed progressive Itô rows -/

namespace AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoContinuousRowQV

open Filter MeasureTheory ProbabilityTheory
open scoped NNReal ENNReal BigOperators
open BrownianMotion ProgressiveL2 ProgressiveL2Density ProgressiveL2Truncation
  ElementaryItoIntegral ElementaryItoIsometry SampledElementaryApproximation
  EuclideanBrownianCoordinates DyadicElementaryRefinement LaggedDyadicApproximation
  LaggedDyadicConvergence ItoIntegralProcess ItoTerminalCompletion ItoIntegralIncrement
  ItoIntegralGridStability ProgressivePathEnergy ItoElementaryRowQV

/-- The quadratic variation of a completed scalar Itô row converges in
`L¹` on dyadic grids to its actual integrated square energy. -/
theorem tendsto_dyadic_ito_row_quadraticVariation_L1
    {Omega J : Type*} [MeasurableSpace Omega] [Fintype J] [DecidableEq J]
    {filtration : Filtration ℝ≥0 (inferInstance : MeasurableSpace Omega)}
    {mu : Measure Omega} [IsFiniteMeasure mu] {T : ℝ≥0}
    {B : ℝ≥0 → Omega → EuclideanSpace ℝ J}
    (hB : IsStandardBrownianMotionWithFiltration B filtration mu) (hT : 0 < T)
    (hUsual : SatisfiesUsualConditions filtration mu)
    (eta : J → ProgressiveL2Integrand filtration mu T) :
    let hcoord := (coordinateFamily hB).isBrownian
    let row := fun t omega =>
      ∑ j : J, itoIntegralProcess (eta j) hT (hcoord j) hUsual t omega
    let error := fun level omega =>
      let times := regularGridTimes (dyadicMesh T level) (2 ^ level)
      (∑ i : Fin (2 ^ level), (row (times i.succ) omega -
        row (times i.castSucc) omega)^2) -
      ∑ j : J, ∫ t, (eta j).process t omega ^ 2 ∂(TimeMeasure.upTo T)
    (∀ level, Integrable (error level) mu) ∧
      Tendsto (fun level => ∫ omega, |error level omega| ∂mu) atTop (nhds 0) := by
  intro hcoord row error
  let _ : IsProbabilityMeasure mu :=
    (hB.isStandard.2.2.1 0 1 (by norm_num) (0 : StrongDual ℝ (EuclideanSpace ℝ J))).isProbabilityMeasure
  let Inputs := J → ProgressiveL2Integrand filtration mu T
  let times (level : ℕ) := regularGridTimes (dyadicMesh T level) (2 ^ level)
  let I (f : Inputs) (t : ℝ≥0) (omega : Omega) :=
    ∑ j : J, itoIntegralProcess (f j) hT (hcoord j) hUsual t omega
  let Q (f : Inputs) (level : ℕ) (omega : Omega) :=
    ∑ i : Fin (2 ^ level), (I f (times level i.succ) omega -
      I f (times level i.castSucc) omega)^2
  let E (f : Inputs) (omega : Omega) :=
    ∑ j : J, ∫ t, (f j).process t omega ^ 2 ∂(TimeMeasure.upTo T)
  let err (f : Inputs) (level : ℕ) (omega : Omega) := Q f level omega - E f omega
  let P (f g : Inputs) (j : J) := ‖(ProgressiveL2Algebra.add (f j) (g j)).toLp‖
  let D (f g : Inputs) (j : J) := ‖(ProgressiveL2Algebra.sub (f j) (g j)).toLp‖
  let bound (f g : Inputs) :=
    (Fintype.card J : ℝ) * Real.sqrt (∑ j : J, (P f g j)^2) *
      Real.sqrt (∑ j : J, (D f g j)^2) + ∑ j : J, P f g j * D f g j
  have hmono (level : ℕ) : Monotone (times level) :=
    (regularGridTimes_strictMono (dyadicMesh_pos hT level) _).monotone
  have hlast (level : ℕ) : times level (Fin.last (2 ^ level)) = T :=
    regularDyadic_last_time T level
  have htime (level : ℕ) (i : Fin (2 ^ level + 1)) : times level i ≤ T :=
    (hmono level (Fin.le_last i)).trans_eq (hlast level)
  have hInt (f : Inputs) (level : ℕ) : Integrable (err f level) mu := by
    have hRow (i : Fin (2 ^ level)) : MemLp (fun omega =>
        I f (times level i.succ) omega - I f (times level i.castSucc) omega) 2 mu := by
      simp only [I, ← Finset.sum_sub_distrib]
      exact memLp_finsetSum Finset.univ (fun j _ =>
        (itoIntegralProcess_increment_isometry (f j) hT (hcoord j) hUsual
          (hmono level (Fin.castSucc_le_succ (i := i))) (htime level i.succ)).1)
    have hQ : Integrable (Q f level) mu :=
      integrable_finsetSum Finset.univ (fun i _ => (hRow i).integrable_sq)
    have hE : Integrable (E f) mu :=
      integrable_finsetSum Finset.univ (fun j _ => (f j).memLp.integrable_sq.integral_prod_left)
    exact hQ.sub hE
  have hCompare (f g : Inputs) (level : ℕ) :
      (∫ omega, |err f level omega| ∂mu) ≤ bound f g + ∫ omega, |err g level omega| ∂mu := by
    have hQ := itoIntegralProcess_row_grid_quadraticVariation_L1_le f g hT hcoord hUsual
      (times level) (hmono level) (hlast level).le
    have hE := progressiveL2_row_pathEnergy_L1_le f g
    let qdiff := fun omega => Q f level omega - Q g level omega
    let ediff := fun omega => E f omega - E g omega
    have hqi : Integrable qdiff mu := hQ.1
    have hei : Integrable ediff mu := hE.1
    have hgi := (hInt g level).abs
    calc
      _ ≤ ∫ omega, (|qdiff omega| + |ediff omega|) + |err g level omega| ∂mu := by
        apply integral_mono (hInt f level).abs ((hqi.abs.add hei.abs).add hgi)
        intro omega
        calc
          |err f level omega| = |(qdiff omega + -ediff omega) + err g level omega| := by
            congr 1
            dsimp only [err, qdiff, ediff]
            ring
          _ ≤ |qdiff omega| + |ediff omega| + |err g level omega| := by
            exact (abs_add_le _ _).trans (add_le_add (by simpa using abs_add_le (qdiff omega) (-ediff omega)) le_rfl)
      _ = ((∫ omega, |qdiff omega| ∂mu) + ∫ omega, |ediff omega| ∂mu) +
            ∫ omega, |err g level omega| ∂mu := by
        have hqe : Integrable (fun omega => |qdiff omega| + |ediff omega|) mu := hqi.abs.add hei.abs
        rw [integral_add hqe hgi, integral_add hqi.abs hei.abs]
      _ ≤ _ := add_le_add (add_le_add hQ.2 hE.2) le_rfl
  have hBoundLim (f : Inputs) (g : ℕ → Inputs)
      (hg : ∀ j, Tendsto (fun level => (g level j).toLp) atTop (nhds (f j).toLp)) :
      Tendsto (fun level => bound f (g level)) atTop (nhds 0) := by
    have hF (j : J) : Tendsto (fun _ : ℕ => (f j).toLp) atTop (nhds (f j).toLp) :=
      tendsto_const_nhds
    have hP (j : J) : Tendsto (fun n => P f (g n) j) atTop
        (nhds ‖(f j).toLp + (f j).toLp‖) := by
      simpa only [P, ProgressiveL2Algebra.toLp_add] using ((hF j).add (hg j)).norm
    have hD (j : J) : Tendsto (fun n => D f (g n) j) atTop (nhds 0) := by
      simpa only [D, ProgressiveL2Algebra.toLp_sub, sub_self, norm_zero]
        using ((hF j).sub (hg j)).norm
    have hPsum := tendsto_finsetSum (Finset.univ : Finset J) (fun j _ => (hP j).pow 2)
    have hDsum := tendsto_finsetSum (Finset.univ : Finset J) (fun j _ => (hD j).pow 2)
    have hProot := Real.continuous_sqrt.continuousAt.tendsto.comp hPsum
    have hDroot := Real.continuous_sqrt.continuousAt.tendsto.comp hDsum
    have hProd := tendsto_finsetSum (Finset.univ : Finset J) (fun j _ => (hP j).mul (hD j))
    simpa [bound, Function.comp_def] using ((hProot.const_mul (Fintype.card J : ℝ)).mul hDroot).add hProd
  let clip (M : ℕ) : Inputs := fun j => clipped (eta j) M
  let q (M level : ℕ) (j : J) : DyadicElementaryProcess filtration T :=
    ⟨level, laggedDyadicApprox (eta j) hT level M, laggedDyadicApprox_times _ _ _ _⟩
  let approx (M level : ℕ) : Inputs := fun j => elementaryIntegrand (q M level j) (hcoord j)
  have hApprox (M : ℕ) (j : J) :
      Tendsto (fun level => (approx M level j).toLp) atTop (nhds (clip M j).toLp) :=
    tendsto_laggedDyadicApprox_toLp_clipped (eta j) hT M
  have hMom (M level : ℕ) (j : J) (i : Fin (2 ^ (q M level j).level)) :
      (∫ omega, ((q M level j).process.coeff i omega)^4 ∂mu) ≤ (M : ℝ)^4 := by
    let c := (q M level j).process.coeff i
    have hc := (coeff_memLp (q M level j).process mu i 4).integrable_norm_pow' (p := 4)
    have hci : Integrable (fun omega => (c omega)^4) mu := by
      exact hc.congr (Eventually.of_forall fun omega => by
        simp only [Real.norm_eq_abs, ← abs_pow]
        exact abs_of_nonneg (by positivity))
    have hp (omega : Omega) : (c omega)^4 ≤ (M : ℝ)^4 := by
      have hbound : |c omega| ≤ (M : ℝ) :=
        laggedDyadicCoeff_abs_le (eta j) hT level M i omega
      simpa only [← abs_pow, abs_of_nonneg (show 0 ≤ (c omega)^4 by positivity)] using
        pow_le_pow_left₀ (abs_nonneg (c omega)) hbound 4
    calc
      _ ≤ ∫ _ : Omega, (M : ℝ)^4 ∂mu := integral_mono hci (integrable_const _) hp
      _ = _ := by simp
  have hApproxQV (M : ℕ) :
      Tendsto (fun level => ∫ omega, |err (approx M level) level omega| ∂mu) atTop (nhds 0) :=
    (tendsto_dyadic_elementary_ito_row_quadraticVariation_L1 hB hT hUsual (q M)
      (fun _ _ => rfl) ((M : ℝ)^4) (hMom M)).2
  have hClipQV (M : ℕ) :
      Tendsto (fun level => ∫ omega, |err (clip M) level omega| ∂mu) atTop (nhds 0) := by
    refine tendsto_const_nhds.squeeze ?_
      (fun _ => integral_nonneg fun _ => abs_nonneg _)
      (fun level => hCompare (clip M) (approx M level) level)
    simpa only [add_zero] using (hBoundLim (clip M) (approx M) (hApprox M)).add (hApproxQV M)
  refine ⟨hInt eta, tendsto_order.2 ⟨?_, ?_⟩⟩
  · intro x hx
    exact Eventually.of_forall (fun _ => hx.trans_le (integral_nonneg fun _ => abs_nonneg _))
  · intro epsilon heps
    have he : 0 < epsilon / 2 := by positivity
    obtain ⟨M, hM⟩ := ((tendsto_order.1
      (hBoundLim eta clip (fun j => tendsto_clipped_toLp (eta j)))).2 (epsilon / 2) he).exists
    filter_upwards [(tendsto_order.1 (hClipQV M)).2 (epsilon / 2) he] with level hlevel
    exact (hCompare eta (clip M) level).trans_lt (by linarith)

#print axioms tendsto_dyadic_ito_row_quadraticVariation_L1

end AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoContinuousRowQV
