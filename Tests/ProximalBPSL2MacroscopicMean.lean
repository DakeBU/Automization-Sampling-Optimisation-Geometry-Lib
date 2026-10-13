import AutoSamplingTheory.ExampleCases.ProximalBPS.L2MacroscopicMean

open MeasureTheory ProbabilityTheory
open scoped ContDiff NNReal Topology
namespace Tests.ProximalBPSL2MacroscopicMean
open AutoSamplingTheory.ExampleCases.ProximalBPS
noncomputable section
set_option maxHeartbeats 800000

-- Actual rough L2 differences, with the SAME canonical source law and bounded operator.
theorem actual_rough_difference_variance
    {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]
    {V : E → ℝ} {α β : ℝ≥0} {η : ℝ}
    (hα : 0 < (α : ℝ)) (hαβ : α ≤ β) (hV : ContDiff ℝ 2 V)
    (hH : ∀ x v : E,
      (α : ℝ)*‖v‖^2 ≤ (fderiv ℝ (fderiv ℝ V) x v) v ∧
      (fderiv ℝ (fderiv ℝ V) x v) v ≤ (β : ℝ)*‖v‖^2)
    (hη : 0 < η) (hβη : (β : ℝ)*η ≤ 1) :
    let μ := (volume : Measure E).tilted (fun x => -V x)
    let J := (μ.prod (stdGaussian E)).map
      (fun p : E × E => (p.1,p.1+Real.sqrt η • p.2))
    let ν := J.snd
    ∃ S : Kernel E E, IsMarkovKernel S ∧
      (∀ y, S y = (volume : Measure E).tilted
        (fun x => -V ((1/2 : ℝ) • (y+x)) - ‖y-x‖^2/(8*η))) ∧
      ∃ T : Lp ℝ 2 ν →L[ℝ] Lp ℝ 2 ν,
        ∀ u v : Lp ℝ 2 ν,
          ‖T u-T v‖ ≤ ‖u-v‖ ∧
          (∫ y, AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.Poincare.variance
            (S y) ((u-v : Lp ℝ 2 ν) : E → ℝ) ∂ν) = ‖u-v‖^2-‖T u-T v‖^2 ∧
          0 ≤ (∫ y, AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.Poincare.variance
            (S y) ((u-v : Lp ℝ 2 ν) : E → ℝ) ∂ν) ∧
          (∫ y, AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.Poincare.variance
            (S y) ((u-v : Lp ℝ 2 ν) : E → ℝ) ∂ν) ≤ ‖u-v‖^2 ∧
          (T (u-v) : E → ℝ) =ᵐ[ν] (fun y => ∫ x, ((u-v : Lp ℝ 2 ν) : E → ℝ) x ∂S y) := by
  dsimp only
  obtain ⟨hμ,hJ,hν,S,hS,hSd,hSc,hSf,hSs,U,hU,hUi,hUs,M,hM,T,hMean⟩ :=
    L2MacroscopicMean.actual_macroscopic_l2_mean hα hαβ hV hH hη hβη
  refine ⟨S,hS,hSd,T,?_⟩
  intro u v
  obtain ⟨hPM,hMT,hTn,hsource,hfiber,hvarI,hvar,hDef⟩ := hMean (u-v)
  have hv := hvar.trans hDef
  rw [map_sub] at hTn hv
  refine ⟨hTn,hv,?_,?_,hsource⟩
  · rw [hvar]
    exact sq_nonneg _
  · rw [hv]
    exact sub_le_self _ (sq_nonneg _)

-- Rank zero and a noncentered constant: the actual source operator fixes1.
theorem rank_zero_actual_source_constant :
    let E := EuclideanSpace ℝ (Fin 0)
    let μ := (volume : Measure E).tilted (fun _ => -(0:ℝ))
    let J := (μ.prod (stdGaussian E)).map
      (fun p : E × E => (p.1,p.1+Real.sqrt (1:ℝ) • p.2))
    let ν := J.snd
    ∃ S : Kernel E E,
      (∀ y, S y = (volume : Measure E).tilted
        (fun x => -(0:ℝ)-‖y-x‖^2/(8*(1:ℝ)))) ∧
      ∃ hOne : MemLp (fun _ : E => (1:ℝ)) 2 ν,
        ∃ T : Lp ℝ 2 ν →L[ℝ] Lp ℝ 2 ν,
          T (hOne.toLp (fun _ => 1)) = hOne.toLp (fun _ => 1) ∧
          (∫ y, AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.Poincare.variance
            (S y) (hOne.toLp (fun _ => 1) : E → ℝ) ∂ν) = 0 := by
  let E := EuclideanSpace ℝ (Fin 0)
  let μ := (volume : Measure E).tilted (fun _ => -(0:ℝ))
  let J := (μ.prod (stdGaussian E)).map
    (fun p : E × E => (p.1,p.1+Real.sqrt (1:ℝ) • p.2))
  let ν := J.snd
  have hH (x v : E) : (1:ℝ)*‖v‖^2 ≤
      (fderiv ℝ (fderiv ℝ (fun _ : E => (0:ℝ))) x v) v ∧
      (fderiv ℝ (fderiv ℝ (fun _ : E => (0:ℝ))) x v) v ≤ (1:ℝ)*‖v‖^2 := by
    have hv : v = 0 := Subsingleton.elim _ _
    simp [hv]
  obtain ⟨hμ,hJ,hν,S,hS,hSd,hSc,hSf,hSs,U,hU,hUi,hUs,M,hM,T,hMean⟩ :=
    L2MacroscopicMean.actual_macroscopic_l2_mean
      (α := 1) (β := 1) (η := 1) (V := fun _ : E => 0)
      (by norm_num) (by norm_num) contDiff_const hH (by norm_num) (by norm_num)
  let : IsProbabilityMeasure ν := hν
  let : IsMarkovKernel S := hS
  have hOne : MemLp (fun _ : E => (1:ℝ)) 2 ν :=
    MemLp.of_bound (by fun_prop) 1 (Filter.Eventually.of_forall fun _ => by simp)
  let one := hOne.toLp (fun _ => 1)
  obtain ⟨x,hx⟩ := hOne.coeFn_toLp.exists
  have hval (y : E) : one y = 1 := by
    change hOne.toLp (fun _ => 1) y = 1
    rw [show y = x from Subsingleton.elim _ _]
    exact hx
  obtain ⟨hPM,hMT,hTn,hsource,hfiber,hvarI,hvar,hDef⟩ := hMean one
  have hfix : T one = one := by
    apply Lp.ext
    filter_upwards [hsource] with y hy
    rw [hy]
    have hm : (∫ z, one z ∂S y) = 1 := by
      rw [integral_congr_ae (Filter.Eventually.of_forall hval)]
      simp
    rw [hm,hval]
  refine ⟨S,hSd,hOne,T,hfix,?_⟩
  rw [hvar,hDef,hfix]
  ring

#print axioms L2MacroscopicMean.actual_macroscopic_l2_mean
#print axioms actual_rough_difference_variance
#print axioms rank_zero_actual_source_constant
end
end Tests.ProximalBPSL2MacroscopicMean
