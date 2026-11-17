import AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ElementaryItoL2
import AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ProgressiveL2Algebra

/-! # Pathwise square energy of progressive and elementary integrands -/

namespace AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ProgressivePathEnergy

open Filter MeasureTheory Set
open scoped NNReal ENNReal BigOperators
open ProgressiveL2 ElementaryItoIntegral ElementaryItoIsometry ElementaryItoL2

private theorem scalar_pathEnergy_L1_le
    {Omega : Type*} {m : MeasurableSpace Omega}
    {filtration : Filtration ℝ≥0 m} {mu : Measure Omega} [IsFiniteMeasure mu] {T : ℝ≥0}
    (eta xi : ProgressiveL2Integrand filtration mu T) :
    let diff := fun omega =>
      (∫ t, eta.process t omega ^ 2 ∂(TimeMeasure.upTo T)) -
        ∫ t, xi.process t omega ^ 2 ∂(TimeMeasure.upTo T)
    Integrable diff mu ∧
      (∫ omega, |diff omega| ∂mu) ≤
        ‖(ProgressiveL2Algebra.add eta xi).toLp‖ * ‖(ProgressiveL2Algebra.sub eta xi).toLp‖ := by
  intro diff
  let nu := TimeMeasure.upTo T
  let plus := ProgressiveL2Algebra.add eta xi
  let minus := ProgressiveL2Algebra.sub eta xi
  let u := processFunction plus.process
  let v := processFunction minus.process
  let f : Omega × ℝ≥0 → ℝ := fun z => u z * v z
  have hEta := eta.memLp.integrable_sq
  have hXi := xi.memLp.integrable_sq
  have hprod : Integrable f (mu.prod nu) := plus.memLp.integrable_mul minus.memLp
  have hEq : diff =ᵐ[mu] fun omega => ∫ t, f (omega, t) ∂nu := by
    filter_upwards [hEta.prod_right_ae, hXi.prod_right_ae] with omega he hx
    change (∫ t, eta.process t omega ^ 2 ∂nu) -
      (∫ t, xi.process t omega ^ 2 ∂nu) = _
    change Integrable (fun t => eta.process t omega ^ 2) nu at he
    change Integrable (fun t => xi.process t omega ^ 2) nu at hx
    rw [← integral_sub he hx]
    apply integral_congr_ae
    filter_upwards [] with t
    change eta.process t omega ^ 2 - xi.process t omega ^ 2 =
      (eta.process t omega + xi.process t omega) * (eta.process t omega - xi.process t omega)
    ring
  have hi := hprod.integral_prod_left.congr hEq.symm
  refine ⟨hi, ?_⟩
  have hholder : Real.HolderConjugate 2 2 := by
    rw [Real.holderConjugate_iff]
    norm_num
  have hcs := integral_mul_norm_le_Lp_mul_Lq hholder
    (f := u) (g := v) (by simpa using plus.memLp) (by simpa using minus.memLp)
  have hnormPlus : (∫ z, (u z)^2 ∂(mu.prod nu)) = ‖plus.toLp‖^2 :=
    (norm_sq_toLp_eq_integral_sq plus.memLp).symm
  have hnormMinus : (∫ z, (v z)^2 ∂(mu.prod nu)) = ‖minus.toLp‖^2 :=
    (norm_sq_toLp_eq_integral_sq minus.memLp).symm
  calc
    _ = ∫ omega, |∫ t, f (omega, t) ∂nu| ∂mu :=
      integral_congr_ae (hEq.mono fun _ h => congrArg abs h)
    _ ≤ ∫ omega, ∫ t, |f (omega, t)| ∂nu ∂mu := by
      apply integral_mono hprod.integral_prod_left.abs hprod.abs.integral_prod_left
      intro omega
      simpa only [Real.norm_eq_abs] using
        norm_integral_le_integral_norm (fun t => f (omega, t)) (μ := nu)
    _ = ∫ z, |f z| ∂(mu.prod nu) := (integral_prod _ hprod.abs).symm
    _ ≤ ‖plus.toLp‖ * ‖minus.toLp‖ := by
      have hbound : (∫ z, |f z| ∂(mu.prod nu)) ≤
          Real.sqrt (∫ z, (u z)^2 ∂(mu.prod nu)) *
            Real.sqrt (∫ z, (v z)^2 ∂(mu.prod nu)) := by
        simpa [f, nu, processTimeMeasure, Real.norm_eq_abs, abs_mul, Real.rpow_two, sq_abs, Real.sqrt_eq_rpow] using hcs
      rwa [hnormPlus, hnormMinus, Real.sqrt_sq (norm_nonneg _), Real.sqrt_sq (norm_nonneg _)] at hbound

/-- The pathwise time energies of a finite row vary continuously in the
product-space `L²` inputs. -/
theorem progressiveL2_row_pathEnergy_L1_le
    {Omega J : Type*} {m : MeasurableSpace Omega} [Fintype J]
    {filtration : Filtration ℝ≥0 m} {mu : Measure Omega} [IsFiniteMeasure mu] {T : ℝ≥0}
    (eta xi : J → ProgressiveL2Integrand filtration mu T) :
    let energy := fun (f : J → ProgressiveL2Integrand filtration mu T) omega =>
      ∑ j : J, ∫ t, (f j).process t omega ^ 2 ∂(TimeMeasure.upTo T)
    Integrable (fun omega => energy eta omega - energy xi omega) mu ∧
      (∫ omega, |energy eta omega - energy xi omega| ∂mu) ≤
        ∑ j : J, ‖(ProgressiveL2Algebra.add (eta j) (xi j)).toLp‖ *
          ‖(ProgressiveL2Algebra.sub (eta j) (xi j)).toLp‖ := by
  intro energy
  let diff := fun j omega =>
    (∫ t, (eta j).process t omega ^ 2 ∂(TimeMeasure.upTo T)) -
      ∫ t, (xi j).process t omega ^ 2 ∂(TimeMeasure.upTo T)
  have hi (j : J) : Integrable (diff j) mu := (scalar_pathEnergy_L1_le (eta j) (xi j)).1
  have heq (omega : Omega) : energy eta omega - energy xi omega = ∑ j : J, diff j omega :=
    (Finset.sum_sub_distrib ..).symm
  have hsum := integrable_finsetSum Finset.univ (fun j _ => hi j)
  refine ⟨hsum.congr (Eventually.of_forall fun omega => (heq omega).symm), ?_⟩
  simp_rw [heq]
  calc
    _ ≤ ∫ omega, ∑ j : J, |diff j omega| ∂mu :=
      integral_mono hsum.abs
        (integrable_finsetSum Finset.univ (fun j _ => (hi j).abs))
        (fun omega => Finset.abs_sum_le_sum_abs _ _)
    _ = ∑ j : J, ∫ omega, |diff j omega| ∂mu :=
      integral_finsetSum _ (fun j _ => (hi j).abs)
    _ ≤ _ := Finset.sum_le_sum (fun j _ => (scalar_pathEnergy_L1_le (eta j) (xi j)).2)

/-- The real time integral of an elementary square is its exact sum of
squared coefficients times clipped cell lengths. -/
theorem elementary_integral_value_sq
    {Omega : Type*} {m : MeasurableSpace Omega}
    {filtration : Filtration ℝ≥0 m} {n : ℕ}
    (q : ElementaryAdaptedProcess filtration n) (T : ℝ≥0) (omega : Omega) :
    (∫ t, (q.value t omega)^2 ∂(TimeMeasure.upTo T)) =
      ∑ i : Fin n, (q.coeff i omega)^2 *
        ((min (q.times i.succ) T - min (q.times i.castSucc) T : ℝ≥0) : ℝ) := by
  have hm : Measurable (fun t => q.value t omega) := by
    unfold ElementaryAdaptedProcess.value
    exact Finset.measurable_sum _ fun _ _ =>
      Measurable.ite measurableSet_Ioc measurable_const measurable_const
  rw [integral_eq_lintegral_of_nonneg_ae (Eventually.of_forall fun _ => sq_nonneg _)
    (hm.pow_const 2).aestronglyMeasurable, lintegral_value_sq, ENNReal.toReal_sum]
  · apply Finset.sum_congr rfl
    intro i _
    rw [ENNReal.toReal_mul, ENNReal.toReal_ofReal (sq_nonneg _)]
    rfl
  · intro i _
    exact ENNReal.mul_ne_top ENNReal.ofReal_ne_top ENNReal.coe_ne_top

#print axioms progressiveL2_row_pathEnergy_L1_le
#print axioms elementary_integral_value_sq

end AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ProgressivePathEnergy
