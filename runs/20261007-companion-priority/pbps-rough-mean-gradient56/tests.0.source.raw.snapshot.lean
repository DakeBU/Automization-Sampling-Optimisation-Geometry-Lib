import AutoSamplingTheory.ExampleCases.ProximalBPS.RoughMeanGradient

open MeasureTheory ProbabilityTheory InnerProductSpace
open scoped RealInnerProductSpace ContDiff NNReal Topology
namespace Tests.ProximalBPSRoughMeanGradient
open AutoSamplingTheory.ExampleCases.ProximalBPS
noncomputable section
set_option autoImplicit false
set_option maxHeartbeats 1600000

-- Actual joint reflection block on rough differences, with the SAME T and K.
theorem actual_joint_block_rough_difference
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
    let P : Lp ℝ 2 J →L[ℝ] Lp ℝ 2 J :=
      (lpMeas ℝ ℝ (MeasurableSpace.comap Prod.snd (inferInstance : MeasurableSpace E))
        2 J).subtypeL ∘L condExpL2 ℝ ℝ measurable_snd.comap_le
    ∃ U : Lp ℝ 2 J →ₗᵢ[ℝ] Lp ℝ 2 J,
      (∀ g : Lp ℝ 2 J, (U g : E × E → ℝ) =ᵐ[J]
        g ∘ (fun p : E × E => (p.1,(2 : ℝ) • p.1-p.2))) ∧
      ∃ M : Lp ℝ 2 ν →ₗᵢ[ℝ] Lp ℝ 2 J,
        (∀ u : Lp ℝ 2 ν, (M u : E × E → ℝ) =ᵐ[J] u ∘ Prod.snd) ∧
        ∃ T : Lp ℝ 2 ν →L[ℝ] Lp ℝ 2 ν,
          ∃ K : Lp ℝ 2 ν →L[ℝ] Lp E 2 ν,
            let A := P * U.toContinuousLinearMap * P
            let B := (1-P) * U.toContinuousLinearMap * P
            ∀ u v : Lp ℝ 2 ν,
              P (M (u-v)) = M (u-v) ∧
              M (T u-T v) = A (M (u-v)) ∧
              η*‖K u-K v‖^2 ≤
                (1-(α : ℝ)*η)^2/(4*(1+(α : ℝ)*η))*‖B (M (u-v))‖^2 ∧
              4*η*‖K u-K v‖^2 ≤ ‖B (M (u-v))‖^2 := by
  dsimp only
  obtain ⟨hμ,hJ,hν,S,hS,hSd,hSc,hSf,hSs,U,hU,hUi,hUs,M,hM,T,hAll⟩ :=
    L2MacroscopicMean.actual_macroscopic_l2_mean hα hαβ hV hH hη hβη
  obtain ⟨_,G,hDense,hClose,hClosed,hGraph,T',K,hRough⟩ :=
    RoughMeanGradient.actual_rough_mean_gradient hα hαβ hV hH hη hβη
  have hSame (u : Lp ℝ 2
      (Measure.map (fun p : E × E => (p.1,p.1+Real.sqrt η • p.2))
        (((volume : Measure E).tilted (fun x => -V x)).prod (stdGaussian E))).snd) :
      T' u = T u := by
    apply Lp.ext
    obtain ⟨_,_,hMean,_,_,_⟩ := hRough u
    obtain ⟨_,_,_,hMean',_,_,_,_⟩ := hAll u
    filter_upwards [hMean,hMean'] with y hy hy'
    exact hy.trans ((congrArg (fun m : Measure E => ∫ x, u x ∂m) (hSd y)).symm.trans hy'.symm)
  refine ⟨U,hU,M,hM,T,K,?_⟩
  intro u v
  obtain ⟨hPM,hMT,_,_,_,_,_,hDef⟩ := hAll (u-v)
  obtain ⟨_,_,_,_,hSharp,hSource⟩ := hRough (u-v)
  rw [hSame] at hSharp hSource
  rw [← hDef] at hSharp hSource
  rw [map_sub] at hMT hSharp hSource
  exact ⟨hPM,hMT,hSharp,hSource⟩

-- The allowed alpha*eta=1 endpoint forces the full gradient operator to vanish.
theorem actual_sharp_endpoint_zero_gradient
    {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]
    {V : E → ℝ} {α β : ℝ≥0} {η : ℝ}
    (hα : 0 < (α : ℝ)) (hαβ : α ≤ β) (hV : ContDiff ℝ 2 V)
    (hH : ∀ x v : E,
      (α : ℝ)*‖v‖^2 ≤ (fderiv ℝ (fderiv ℝ V) x v) v ∧
      (fderiv ℝ (fderiv ℝ V) x v) v ≤ (β : ℝ)*‖v‖^2)
    (hη : 0 < η) (hβη : (β : ℝ)*η ≤ 1) (hαη : (α : ℝ)*η = 1) :
    let μ := (volume : Measure E).tilted (fun x => -V x)
    let J := (μ.prod (stdGaussian E)).map
      (fun p : E × E => (p.1,p.1+Real.sqrt η • p.2))
    let ν := J.snd
    ∃ G : Lp ℝ 2 ν →ₗ.[ℝ] Lp E 2 ν,
      G.IsClosable ∧ G.closure.IsClosed ∧
      ∃ T : Lp ℝ 2 ν →L[ℝ] Lp ℝ 2 ν,
        ∃ K : Lp ℝ 2 ν →L[ℝ] Lp E 2 ν,
          K = 0 ∧ ∀ u : Lp ℝ 2 ν,
            (T u,0) ∈ G.closure.graph ∧
            (T u : E → ℝ) =ᵐ[ν] (fun y => ∫ x, u x ∂
              ((volume : Measure E).tilted
                (fun x => -V ((1/2 : ℝ) • (y+x)) - ‖y-x‖^2/(8*η)))) := by
  dsimp only
  obtain ⟨_,G,hDense,hClose,hClosed,hGraph,T,K,hRough⟩ :=
    RoughMeanGradient.actual_rough_mean_gradient hα hαβ hV hH hη hβη
  have hZero (u) : K u = 0 := by
    obtain ⟨_,_,_,_,hs,_⟩ := hRough u
    rw [hαη] at hs
    simp only [sub_self,zero_pow (by norm_num : 2 ≠ 0),zero_div,zero_mul] at hs
    have hn : ‖K u‖^2 = 0 := by nlinarith [sq_nonneg ‖K u‖]
    exact norm_eq_zero.mp (by nlinarith [norm_nonneg (K u)])
  refine ⟨G,hClose,hClosed,T,K,?_,?_⟩
  · ext u
    exact hZero u
  · intro u
    obtain ⟨hp,_,hm,_,_,_⟩ := hRough u
    rw [hZero u] at hp
    exact ⟨hp,hm⟩

#print axioms RoughMeanGradient.actual_rough_mean_gradient
#print axioms actual_joint_block_rough_difference
#print axioms actual_sharp_endpoint_zero_gradient
end
end Tests.ProximalBPSRoughMeanGradient
