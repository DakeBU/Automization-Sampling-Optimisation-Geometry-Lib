import AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoIntegralGridEnergy
import AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoIntegralProcessCongruence

/-! # Stability of squared grid increments under changes of the integrand -/

namespace AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoIntegralGridStability

open Filter MeasureTheory
open scoped NNReal BigOperators
open BrownianMotion ProgressiveL2 ElementaryItoIntegral ElementaryItoL2
  ItoIntegralProcess ItoIntegralIncrement ItoIntegralGridEnergy ItoIntegralProcessCongruence

private theorem integral_abs_sum_products_le
    {Omega I : Type*} [MeasurableSpace Omega] [Fintype I] {mu : Measure Omega}
    {u v : I → Omega → ℝ}
    (hu : ∀ i, MemLp (u i) 2 mu) (hv : ∀ i, MemLp (v i) 2 mu) :
    Integrable (fun omega => ∑ i : I, u i omega * v i omega) mu ∧
      (∫ omega, |∑ i : I, u i omega * v i omega| ∂mu) ≤
        Real.sqrt (∑ i : I, ∫ omega, (u i omega)^2 ∂mu) *
          Real.sqrt (∑ i : I, ∫ omega, (v i omega)^2 ∂mu) := by
  let A := fun i => ∫ omega, (u i omega)^2 ∂mu
  let B := fun i => ∫ omega, (v i omega)^2 ∂mu
  have hA (i) : 0 ≤ A i := integral_nonneg fun _ => sq_nonneg _
  have hB (i) : 0 ≤ B i := integral_nonneg fun _ => sq_nonneg _
  have hprod (i) : Integrable (fun omega => u i omega * v i omega) mu :=
    (hu i).integrable_mul (hv i)
  have hsum := integrable_finsetSum Finset.univ (fun i _ => hprod i)
  refine ⟨hsum, ?_⟩
  have hholder : Real.HolderConjugate 2 2 := by
    rw [Real.holderConjugate_iff]
    norm_num
  have hcell (i) : (∫ omega, |u i omega * v i omega| ∂mu) ≤
      Real.sqrt (A i) * Real.sqrt (B i) := by
    have h := integral_mul_norm_le_Lp_mul_Lq hholder
      (by simpa using hu i) (by simpa using hv i)
    simpa [A, B, Real.norm_eq_abs, abs_mul, Real.rpow_two, sq_abs, Real.sqrt_eq_rpow]
      using h
  calc
    _ ≤ ∫ omega, ∑ i : I, |u i omega * v i omega| ∂mu :=
      integral_mono hsum.abs
        (integrable_finsetSum Finset.univ (fun i _ => (hprod i).abs))
        (fun omega => Finset.abs_sum_le_sum_abs _ _)
    _ = ∑ i : I, ∫ omega, |u i omega * v i omega| ∂mu :=
      integral_finsetSum _ (fun i _ => (hprod i).abs)
    _ ≤ ∑ i : I, Real.sqrt (A i) * Real.sqrt (B i) :=
      Finset.sum_le_sum (fun i _ => hcell i)
    _ ≤ Real.sqrt (∑ i : I, A i) * Real.sqrt (∑ i : I, B i) := by
      rw [← Real.sqrt_mul (Finset.sum_nonneg fun i _ => hA i)]
      apply Real.le_sqrt_of_sq_le
      simpa only [Real.sq_sqrt (hA _), Real.sq_sqrt (hB _)]
        using Finset.sum_mul_sq_le_sq_mul_sq Finset.univ
          (fun i : I => Real.sqrt (A i)) (fun i : I => Real.sqrt (B i))

/-- The expected absolute change in the squared-increment sum of an Itô row
is controlled by product-space `L²` energies, uniformly over the time grid. -/
theorem itoIntegralProcess_row_grid_quadraticVariation_L1_le
    {Omega J : Type*} {m : MeasurableSpace Omega} [Fintype J]
    {filtration : Filtration ℝ≥0 m} {mu : Measure Omega} [IsFiniteMeasure mu]
    {T : ℝ≥0} {B : J → ℝ≥0 → Omega → ℝ}
    (eta xi : J → ProgressiveL2Integrand filtration mu T) (hT : 0 < T)
    (hB : ∀ j, IsBrownianMotionWithFiltration (B j) filtration mu)
    (hUsual : SatisfiesUsualConditions filtration mu)
    {n : ℕ} (times : Fin (n + 1) → ℝ≥0)
    (hmono : Monotone times) (hlast : times (Fin.last n) ≤ T) :
    let row := fun (f : J → ProgressiveL2Integrand filtration mu T) t omega =>
      ∑ j : J, itoIntegralProcess (f j) hT (hB j) hUsual t omega
    let qv := fun f omega => ∑ i : Fin n,
      (row f (times i.succ) omega - row f (times i.castSucc) omega)^2
    Integrable (fun omega => qv eta omega - qv xi omega) mu ∧
      (∫ omega, |qv eta omega - qv xi omega| ∂mu) ≤
        (Fintype.card J : ℝ) *
          Real.sqrt (∑ j : J, ‖(ProgressiveL2Algebra.add (eta j) (xi j)).toLp‖^2) *
          Real.sqrt (∑ j : J, ‖(ProgressiveL2Algebra.sub (eta j) (xi j)).toLp‖^2) := by
  classical
  intro row qv
  let plus := fun j => ProgressiveL2Algebra.add (eta j) (xi j)
  let minus := fun j => ProgressiveL2Algebra.sub (eta j) (xi j)
  let coordinate := fun (f : J → ProgressiveL2Integrand filtration mu T) (j : J)
      (i : Fin n) omega =>
    itoIntegralProcess (f j) hT (hB j) hUsual (times i.succ) omega -
      itoIntegralProcess (f j) hT (hB j) hUsual (times i.castSucc) omega
  let inc := fun f (i : Fin n) omega =>
    row f (times i.succ) omega - row f (times i.castSucc) omega
  have hinc (f) (i : Fin n) (omega : Omega) :
      inc f i omega = ∑ j : J, coordinate f j i omega := by
    simp only [inc, row, coordinate, Finset.sum_sub_distrib]
  have htime (i : Fin (n + 1)) : times i ≤ T :=
    (hmono (Fin.le_last _)).trans hlast
  have hcoord (f) (j : J) (i : Fin n) : MemLp (coordinate f j i) 2 mu :=
    (itoIntegralProcess_increment_isometry (f j) hT (hB j) hUsual
      (hmono (Fin.castSucc_le_succ (i := i))) (htime i.succ)).1
  have hmem (f) (i : Fin n) : MemLp (inc f i) 2 mu := by
    rw [show inc f i = (fun omega => ∑ j : J, coordinate f j i omega) from funext (hinc f i)]
    exact memLp_finsetSum Finset.univ (fun j _ => hcoord f j i)
  have hend (t : ℝ≥0) (ht : t ≤ T) : ∀ᵐ omega ∂mu,
      row plus t omega = row eta t omega + row xi t omega ∧
      row minus t omega = row eta t omega - row xi t omega := by
    have hj (j : J) : ∀ᵐ omega ∂mu,
        itoIntegralProcess (plus j) hT (hB j) hUsual t omega =
          itoIntegralProcess (eta j) hT (hB j) hUsual t omega +
            itoIntegralProcess (xi j) hT (hB j) hUsual t omega ∧
        itoIntegralProcess (minus j) hT (hB j) hUsual t omega =
          itoIntegralProcess (eta j) hT (hB j) hUsual t omega -
            itoIntegralProcess (xi j) hT (hB j) hUsual t omega := by
      have heq : (ProgressiveL2Algebra.add (minus j) (xi j)).toLp = (eta j).toLp := by
        rw [ProgressiveL2Algebra.toLp_add]
        dsimp only [minus]
        rw [ProgressiveL2Algebra.toLp_sub, sub_add_cancel]
      filter_upwards [itoIntegralProcess_add (eta j) (xi j) hT (hB j) hUsual ht,
        itoIntegralProcess_add (minus j) (xi j) hT (hB j) hUsual ht,
        itoIntegralProcess_congr_toLp_ae _ _ hT (hB j) hUsual heq ht]
        with omega hplus hsum hequal
      exact ⟨hplus, eq_sub_of_add_eq (hsum.symm.trans hequal)⟩
    filter_upwards [ae_all_iff.2 hj] with omega homega
    constructor
    · simp only [row, ← Finset.sum_add_distrib]
      exact Finset.sum_congr rfl (fun j _ => (homega j).1)
    · simp only [row, ← Finset.sum_sub_distrib]
      exact Finset.sum_congr rfl (fun j _ => (homega j).2)
  have hfactor (i : Fin n) : ∀ᵐ omega ∂mu,
      (inc eta i omega)^2 - (inc xi i omega)^2 = inc plus i omega * inc minus i omega := by
    filter_upwards [hend _ (htime i.succ), hend _ (htime i.castSucc)] with omega hr hl
    dsimp only [inc]
    rw [hr.1, hr.2, hl.1, hl.2]
    ring
  have hq : (fun omega => qv eta omega - qv xi omega) =ᵐ[mu]
      (fun omega => ∑ i : Fin n, inc plus i omega * inc minus i omega) := by
    filter_upwards [ae_all_iff.2 hfactor] with omega homega
    change (∑ i : Fin n, (inc eta i omega)^2) - (∑ i : Fin n, (inc xi i omega)^2) = _
    rw [← Finset.sum_sub_distrib]
    exact Finset.sum_congr rfl (fun i _ => homega i)
  have hcs := integral_abs_sum_products_le (hmem plus) (hmem minus)
  refine ⟨hcs.1.congr hq.symm, ?_⟩
  have henergy (f) :
      (∑ i : Fin n, ∫ omega, (inc f i omega)^2 ∂mu) ≤
        (Fintype.card J : ℝ) * ∑ j : J, ‖(f j).toLp‖^2 := by
    have hsq (i : Fin n) (omega : Omega) :
        (inc f i omega)^2 ≤ (Fintype.card J : ℝ) * ∑ j : J, (coordinate f j i omega)^2 := by
      rw [hinc]
      simpa [mul_comm] using Finset.sum_mul_sq_le_sq_mul_sq Finset.univ
        (fun j : J => coordinate f j i omega) (fun _ : J => (1 : ℝ))
    have hsingle (j : J) :
        (∑ i : Fin n, ∫ omega, (coordinate f j i omega)^2 ∂mu) ≤ ‖(f j).toLp‖^2 := by
      have hgrid := (itoIntegralProcess_grid_isometry (f j) hT (hB j) hUsual
        times hmono hlast).2
      change (∫ omega, ∑ i : Fin n, (coordinate f j i omega)^2 ∂mu) = _ at hgrid
      rw [integral_finsetSum _ (fun i _ => (hcoord f j i).integrable_sq)] at hgrid
      rw [hgrid]
      change _ ≤ ‖(f j).memLp.toLp (processFunction (f j).process)‖^2
      rw [norm_sq_toLp_eq_integral_sq]
      exact integral_mono_measure Measure.restrict_le_self (Eventually.of_forall fun _ => sq_nonneg _)
        (f j).memLp.integrable_sq
    calc
      _ ≤ ∑ i : Fin n, (Fintype.card J : ℝ) * ∑ j : J,
          ∫ omega, (coordinate f j i omega)^2 ∂mu := by
        refine Finset.sum_le_sum (fun i _ => ?_)
        rw [← integral_finsetSum _ (fun j _ => (hcoord f j i).integrable_sq), ← integral_const_mul]
        exact integral_mono (hmem f i).integrable_sq
          ((integrable_finsetSum Finset.univ (fun j _ => (hcoord f j i).integrable_sq)).const_mul _)
          (hsq i)
      _ = (Fintype.card J : ℝ) * ∑ j : J, ∑ i : Fin n,
          ∫ omega, (coordinate f j i omega)^2 ∂mu := by
        rw [← Finset.mul_sum, Finset.sum_comm]
      _ ≤ _ := mul_le_mul_of_nonneg_left (Finset.sum_le_sum (fun j _ => hsingle j)) (by positivity)
  calc
    _ = ∫ omega, |∑ i : Fin n, inc plus i omega * inc minus i omega| ∂mu :=
      integral_congr_ae (hq.mono fun _ h => congrArg abs h)
    _ ≤ _ := hcs.2
    _ ≤ _ := by
      calc
        _ ≤ Real.sqrt ((Fintype.card J : ℝ) * ∑ j : J, ‖(plus j).toLp‖^2) *
            Real.sqrt ((Fintype.card J : ℝ) * ∑ j : J, ‖(minus j).toLp‖^2) :=
          mul_le_mul (Real.sqrt_le_sqrt (henergy plus)) (Real.sqrt_le_sqrt (henergy minus))
            (Real.sqrt_nonneg _) (Real.sqrt_nonneg _)
        _ = _ := by
          rw [Real.sqrt_mul (by positivity : 0 ≤ (Fintype.card J : ℝ)),
            Real.sqrt_mul (by positivity : 0 ≤ (Fintype.card J : ℝ))]
          rw [mul_mul_mul_comm, Real.mul_self_sqrt (by positivity : 0 ≤ (Fintype.card J : ℝ)),
            mul_assoc]

#print axioms itoIntegralProcess_row_grid_quadraticVariation_L1_le

end AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoIntegralGridStability
