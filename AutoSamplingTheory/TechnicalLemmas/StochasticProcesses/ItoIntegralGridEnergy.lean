import AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoIntegralIncrement

/-! # Finite-grid energy of the completed Itô process -/

namespace AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoIntegralGridEnergy

open MeasureTheory Set
open scoped NNReal BigOperators
open BrownianMotion ProgressiveL2 ElementaryItoIntegral ItoIntegralProcess ItoIntegralIncrement

private theorem sum_setIntegral_grid_cells
    {Omega : Type*} [MeasurableSpace Omega] {nu : Measure (Omega × ℝ≥0)}
    {f : Omega × ℝ≥0 → ℝ} (hf : Integrable f nu)
    {n : ℕ} (times : Fin (n + 1) → ℝ≥0) (hmono : Monotone times) :
    (∑ i : Fin n, ∫ z in Prod.snd ⁻¹' Ico (times i.castSucc) (times i.succ), f z ∂nu) =
      ∫ z in Prod.snd ⁻¹' Ico (times 0) (times (Fin.last n)), f z ∂nu := by
  induction n with
  | zero => simp
  | succ n ih =>
    rw [Fin.sum_univ_castSucc]
    have hp := ih (times ∘ Fin.castSucc) (hmono.comp (fun _ _ hij => Fin.castSucc_le_castSucc_iff.2 hij))
    simp only [Function.comp_apply, Fin.castSucc_zero, Fin.castSucc_succ] at hp
    rw [hp]
    let a := times 0
    let b := times (Fin.last n).castSucc
    let c := times (Fin.last (n + 1))
    have hab : a ≤ b := hmono (Fin.zero_le _)
    have hbc : b ≤ c := hmono (Fin.le_last _)
    change (∫ z in Prod.snd ⁻¹' Ico a b, f z ∂nu) +
      (∫ z in Prod.snd ⁻¹' Ico b c, f z ∂nu) =
        ∫ z in Prod.snd ⁻¹' Ico a c, f z ∂nu
    rw [← Ico_union_Ico_eq_Ico hab hbc, Set.preimage_union]
    symm
    apply setIntegral_union _ (measurable_snd measurableSet_Ico) hf.integrableOn hf.integrableOn
    exact (Set.disjoint_left.mpr fun _ hx hy => (not_lt_of_ge hy.1) hx.2)

/-- Add the cellwise Itô energies over a deterministic grid, with its half-open
span on the probability–time side. -/
theorem itoIntegralProcess_grid_isometry
    {Omega : Type*} {m : MeasurableSpace Omega}
    {filtration : Filtration ℝ≥0 m} {mu : Measure Omega} [IsFiniteMeasure mu]
    {T : ℝ≥0} {B : ℝ≥0 → Omega → ℝ}
    (eta : ProgressiveL2Integrand filtration mu T) (hT : 0 < T)
    (hB : IsBrownianMotionWithFiltration B filtration mu)
    (hUsual : SatisfiesUsualConditions filtration mu)
    {n : ℕ} (times : Fin (n + 1) → ℝ≥0)
    (hmono : Monotone times) (hlast : times (Fin.last n) ≤ T) :
    let squares := fun omega => ∑ i : Fin n,
      (itoIntegralProcess eta hT hB hUsual (times i.succ) omega -
        itoIntegralProcess eta hT hB hUsual (times i.castSucc) omega)^2
    Integrable squares mu ∧
      (∫ omega, squares omega ∂mu) =
        ∫ z in Prod.snd ⁻¹' Set.Ico (times 0) (times (Fin.last n)),
          (processFunction eta.process z)^2 ∂(processTimeMeasure mu T) := by
  intro squares
  let inc := fun (i : Fin n) omega =>
    itoIntegralProcess eta hT hB hUsual (times i.succ) omega -
      itoIntegralProcess eta hT hB hUsual (times i.castSucc) omega
  have hc (i : Fin n) :=
    itoIntegralProcess_increment_isometry eta hT hB hUsual
      (hmono (Fin.castSucc_le_succ (i := i))) ((hmono (Fin.le_last _)).trans hlast)
  have hi (i : Fin n) : Integrable (fun omega => (inc i omega)^2) mu :=
    (hc i).1.integrable_sq
  refine ⟨integrable_finsetSum Finset.univ (fun i _ => hi i), ?_⟩
  change (∫ omega, ∑ i : Fin n, (inc i omega)^2 ∂mu) = _
  rw [integral_finsetSum _ (fun i _ => hi i)]
  calc
    _ = ∑ i : Fin n, ∫ z in Prod.snd ⁻¹' Ico (times i.castSucc) (times i.succ),
          (processFunction eta.process z)^2 ∂(processTimeMeasure mu T) :=
      Finset.sum_congr rfl (fun i _ => (hc i).2)
    _ = _ := sum_setIntegral_grid_cells eta.memLp.integrable_sq times hmono

#print axioms itoIntegralProcess_grid_isometry

end AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoIntegralGridEnergy
