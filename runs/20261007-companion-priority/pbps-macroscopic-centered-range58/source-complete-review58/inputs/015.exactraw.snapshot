import AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.GaussianMarginalPoincare
import AutoSamplingTheory.ExampleCases.ProximalBPS.RoughMeanGradient

open MeasureTheory ProbabilityTheory InnerProductSpace
open scoped RealInnerProductSpace ContDiff NNReal Topology
namespace Tests.GaussianMarginalPoincare
open AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities
open AutoSamplingTheory.ExampleCases.ProximalBPS
noncomputable section
set_option autoImplicit false
set_option maxHeartbeats 1600000

-- Actual C3 and C4 consume SAME56 T/K; domain and centering are produced.
theorem actual_same_mean_centered_contraction
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
    ∃ G : Lp ℝ 2 ν →ₗ.[ℝ] Lp E 2 ν,
      G.IsClosable ∧ G.closure.IsClosed ∧
      ∃ T : Lp ℝ 2 ν →L[ℝ] Lp ℝ 2 ν,
        ∃ K : Lp ℝ 2 ν →L[ℝ] Lp E 2 ν,
          ∀ u : Lp ℝ 2 ν,
            (T u,K u) ∈ G.closure.graph ∧
            (T u : E → ℝ) =ᵐ[ν] (fun y => ∫ x, u x ∂
              ((volume : Measure E).tilted
                (fun x => -V ((1/2 : ℝ) • (y+x)) - ‖y-x‖^2/(8*η)))) ∧
            (∫ y, (T u) y ∂ν) = ∫ x, u x ∂ν ∧
            ((∫ x, u x ∂ν)=0 →
              ((α : ℝ)/(1+(α : ℝ)*η))*‖T u‖^2 ≤ ‖K u‖^2 ∧
              ‖T u‖ ≤ ((1-(α : ℝ)*η)/(1+(α : ℝ)*η))*‖u‖) := by
  classical
  dsimp only
  let μ := (volume : Measure E).tilted (fun x => -V x)
  let J := (μ.prod (stdGaussian E)).map
    (fun p : E × E => (p.1,p.1+Real.sqrt η • p.2))
  let ν := J.snd
  let Λ := J.map (fun p : E × E => (p.2,(2 : ℝ) • p.1-p.2))
  obtain ⟨hν,G,hDense,hClose,hClosed,hGraph,hPI⟩ :=
    GaussianMarginalPoincare.actual_gaussian_marginal_centered_poincare hα hαβ hV hH hη hβη
  obtain ⟨_,G',_,_,_,hGraph',T,K,hRough⟩ :=
    RoughMeanGradient.actual_rough_mean_gradient hα hαβ hV hH hη hβη
  have hSameG : G'=G := LinearPMap.eq_of_eq_graph (by
    ext p
    rcases p with ⟨u,v⟩
    exact (hGraph' u v).trans (hGraph u v).symm)
  subst G'
  obtain ⟨hμ,hJ,_,S,hS,hSd,hSc,hSf,hSs,U,hU,hUi,hUs,M,hM,T',hAll⟩ :=
    L2MacroscopicMean.actual_macroscopic_l2_mean hα hαβ hV hH hη hβη
  letI : IsProbabilityMeasure ν := hν
  letI : IsProbabilityMeasure J := hJ
  letI : IsMarkovKernel S := hS
  letI : Λ.IsCondKernel S := hSc
  have hcompS : ν ⊗ₘ S=Λ := by
    calc
      ν ⊗ₘ S=Λ.fst ⊗ₘ S := congrArg (fun ρ => ρ ⊗ₘ S) hSf.symm
      _ = Λ := Measure.disintegrate Λ S
  have hMean (u : Lp ℝ 2 ν) : (T u : E → ℝ) =ᵐ[ν] (fun y => ∫ x, u x ∂S y) := by
    filter_upwards [(hRough u).2.2.1] with y hy
    exact hy.trans (congrArg (fun m : Measure E => ∫ x, u x ∂m) (hSd y)).symm
  have hPreserve (u : Lp ℝ 2 ν) : (∫ y, (T u) y ∂ν)=∫ x, u x ∂ν := by
    have hi : Integrable (fun p : E × E => u p.2) (ν ⊗ₘ S) := by
      rw [hcompS]
      exact ((Lp.memLp u).comp_measurePreserving
        (show MeasurePreserving (Prod.snd : E × E → E) Λ ν from ⟨measurable_snd,hSs⟩)).integrable (by norm_num)
    rw [integral_congr_ae (hMean u),← Measure.integral_compProd hi,hcompS]
    calc
      (∫ p : E × E, u p.2 ∂Λ) = ∫ x, u x ∂Λ.snd :=
        (integral_map (μ:=Λ) measurable_snd.aemeasurable (Lp.stronglyMeasurable u).aestronglyMeasurable).symm
      _ = ∫ x, u x ∂ν := by rw [hSs]
  refine ⟨G,hClose,hClosed,T,K,?_⟩
  intro u
  obtain ⟨hPair,_,hLiteral,_,hSharp,_⟩ := hRough u
  refine ⟨hPair,hLiteral,hPreserve u,?_⟩
  intro hu
  let z : G.closure.domain := ⟨T u,G.closure.mem_domain_of_mem_graph hPair⟩
  have hz : (∫ x, (z : Lp ℝ 2 ν) x ∂ν)=0 := (hPreserve u).trans hu
  have hK : G.closure z=K u := G.closure.mem_graph_snd_inj (G.closure.mem_graph z) hPair rfl
  have hC3 := hPI z hz
  change ((α : ℝ)/(1+(α : ℝ)*η))*‖T u‖^2 ≤ ‖G.closure z‖^2 at hC3
  rw [hK] at hC3
  refine ⟨hC3,?_⟩
  have hαη : (α : ℝ)*η≤1 :=
    (mul_le_mul_of_nonneg_right (show (α : ℝ)≤(β : ℝ) from hαβ) hη.le).trans hβη
  have hd : 0<1+(α : ℝ)*η := by positivity
  have hr : 0≤(1-(α : ℝ)*η)/(1+(α : ℝ)*η) := div_nonneg (sub_nonneg.mpr hαη) hd.le
  have hP : (α : ℝ)*‖T u‖^2 ≤ (1+(α : ℝ)*η)*‖K u‖^2 := by
    calc
      _ ≤ ‖K u‖^2*(1+(α : ℝ)*η) :=
        (div_le_iff₀ hd).mp (by simpa only [div_mul_eq_mul_div] using hC3)
      _ = _ := mul_comm _ _
  have hSharp' : 4*(1+(α : ℝ)*η)*η*‖K u‖^2 ≤
      (1-(α : ℝ)*η)^2*(‖u‖^2-‖T u‖^2) := by
    have hs : η*‖K u‖^2 ≤
        ((1-(α : ℝ)*η)^2*(‖u‖^2-‖T u‖^2))/(4*(1+(α : ℝ)*η)) := by
      calc
        _ ≤ (1-(α : ℝ)*η)^2/(4*(1+(α : ℝ)*η))*(‖u‖^2-‖T u‖^2) := hSharp
        _ = _ := div_mul_eq_mul_div _ _ _
    have hs' := (le_div_iff₀ (show 0<4*(1+(α : ℝ)*η) from by positivity)).mp hs
    calc
      4*(1+(α : ℝ)*η)*η*‖K u‖^2 = η*‖K u‖^2*(4*(1+(α : ℝ)*η)) := by ring
      _ ≤ _ := hs'
  have hSq : (1+(α : ℝ)*η)^2*‖T u‖^2 ≤ (1-(α : ℝ)*η)^2*‖u‖^2 := by
    nlinarith [mul_le_mul_of_nonneg_left hP (show 0≤4*η from by positivity)]
  have hSq' : ‖T u‖^2 ≤ (((1-(α : ℝ)*η)/(1+(α : ℝ)*η))*‖u‖)^2 := by
    rw [mul_pow,div_pow,div_mul_eq_mul_div]
    apply (le_div_iff₀ (sq_pos_of_pos hd)).2
    nlinarith [hSq]
  exact (sq_le_sq₀ (norm_nonneg _) (mul_nonneg hr (norm_nonneg _))).mp hSq'

#print axioms GaussianMarginalPoincare.actual_gaussian_marginal_centered_poincare
#print axioms actual_same_mean_centered_contraction
end
end Tests.GaussianMarginalPoincare
