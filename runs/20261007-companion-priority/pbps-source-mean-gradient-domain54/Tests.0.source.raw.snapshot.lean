import AutoSamplingTheory.ExampleCases.ProximalBPS.SourceMeanGradientDomain
import Tests.ProximalBPSReflectedMeanRegularity

namespace Tests.ProximalBPSSourceMeanGradientDomain
noncomputable section
set_option autoImplicit false
open MeasureTheory ProbabilityTheory InnerProductSpace
open scoped ContDiff NNReal RealInnerProductSpace
open AutoSamplingTheory.ExampleCases.ProximalBPS

-- The actual macroscopic Ag representative and the new closed-gradient pair
-- refer to the SAME literal source mean and the SAME Gaussian augmentation.
theorem actual_macroscopic_mean_closed_gradient
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
    let F := fun p : E × E => (p.1,(2:ℝ) • p.1-p.2)
    let P : Lp ℝ 2 J →L[ℝ] Lp ℝ 2 J :=
      (lpMeas ℝ ℝ (MeasurableSpace.comap Prod.snd (inferInstance : MeasurableSpace E))
        2 J).subtypeL ∘L condExpL2 ℝ ℝ measurable_snd.comap_le
    let S := fun y : E => (volume : Measure E).tilted
      (fun u => -V ((1/2:ℝ) • (y+u)) - ‖y-u‖^2/(8*η))
    ∃ U : Lp ℝ 2 J →ₗᵢ[ℝ] Lp ℝ 2 J,
      (∀ g : Lp ℝ 2 J, (U g : E × E → ℝ) =ᵐ[J] g ∘ F) ∧
      ∃ G : Lp ℝ 2 ν →ₗ.[ℝ] Lp E 2 ν, G.closure.IsClosed ∧
        ∀ f : E → ℝ, ContDiff ℝ ∞ f → HasCompactSupport f →
          let Tf := fun y : E => ∫ u, f u ∂S y
          ∃ hTf : MemLp Tf 2 ν, ∃ hGrad : MemLp (gradient Tf) 2 ν,
            ∃ g : Lp ℝ 2 J,
              (g : E × E → ℝ) =ᵐ[J] (fun p => f p.2) ∧ P g = g ∧
              ((P*U.toContinuousLinearMap*P) g : E × E → ℝ) =ᵐ[J]
                (fun p => Tf p.2) ∧
              (hTf.toLp Tf,hGrad.toLp (gradient Tf)) ∈ G.closure.graph := by
  obtain ⟨hμ,hJ,hν,R,S₀,hR,hS,hcond,hSR,hSd,hΛcond,hfst,
    U,hU,hUi,hUs,hBB,hBD,hblock,henergy⟩ :=
    MacroscopicEnergy.actual_macroscopic_gradient_energy_blocks hα hαβ hV hH hη hβη
  obtain ⟨_,G,hDense,hClosable,hClosed,hGraph,hDomain⟩ :=
    SourceMeanGradientDomain.literal_source_mean_in_closed_gradient hα hαβ hV hH hη hβη
  refine ⟨U,hU,G,hClosed,?_⟩
  intro f hf hc
  obtain ⟨hTf,hGrad,hPair⟩ := hDomain f hf hc
  obtain ⟨_,_,_,_,_,g,hg,hPg,hAg,_⟩ := henergy f hf hc
  refine ⟨hTf,hGrad,g,hg,hPg,?_,hPair⟩
  apply hAg.trans
  filter_upwards with p
  exact congrArg (fun m : Measure E => ∫ u, f u ∂m) (hSd p.2)

-- Noncentered constant1 survives the actual source mean in dimension zero.
-- The canonical input is constant1 and its graph output is the zero gradient.
theorem rank_zero_noncentered_source_mean_graph :
    let E := EuclideanSpace ℝ (Fin 0)
    let μ := (volume : Measure E).tilted (fun _ => -(0:ℝ))
    let J := (μ.prod (stdGaussian E)).map
      (fun p : E × E => (p.1,p.1+Real.sqrt (1:ℝ) • p.2))
    let ν := J.snd
    let S := fun y : E => (volume : Measure E).tilted
      (fun u => -(0:ℝ)-‖y-u‖^2/(8*(1:ℝ)))
    ∃ G : Lp ℝ 2 ν →ₗ.[ℝ] Lp E 2 ν,
      ∃ hOne : MemLp (fun _ : E => (1:ℝ)) 2 ν,
        ∃ hZero : MemLp (fun _ : E => (0:E)) 2 ν,
          (hOne.toLp (fun _ => 1),hZero.toLp (fun _ => 0)) ∈ G.closure.graph ∧
          (∀ y, (∫ _u, (1:ℝ) ∂S y) = 1) ∧
          gradient (fun y : E => ∫ _u, (1:ℝ) ∂S y) = (fun _ => 0) := by
  let E := EuclideanSpace ℝ (Fin 0)
  have hH (x v : E) : (1:ℝ)*‖v‖^2 ≤
      (fderiv ℝ (fderiv ℝ (fun _ : E => (0:ℝ))) x v) v ∧
      (fderiv ℝ (fderiv ℝ (fun _ : E => (0:ℝ))) x v) v ≤ (1:ℝ)*‖v‖^2 := by
    have hv : v = 0 := Subsingleton.elim _ _
    simp [hv]
  obtain ⟨_,G,hDense,hClosable,hClosed,hGraph,hDomain⟩ :=
    SourceMeanGradientDomain.literal_source_mean_in_closed_gradient
      (α := 1) (β := 1) (η := 1) (V := fun _ : E => 0)
      (by norm_num) (by norm_num) contDiff_const hH (by norm_num) (by norm_num)
  have hc : HasCompactSupport (fun _ : E => (1:ℝ)) := (isClosed_tsupport _).isCompact
  obtain ⟨hp,hq,hPair⟩ := hDomain (fun _ => 1) contDiff_const hc
  have hmean := ProximalBPSReflectedMeanRegularity.rank_zero_source_noncentered_mean
  have he := funext hmean.2.1
  have hge : gradient (fun y : E => ∫ _u, (1:ℝ) ∂
      (volume : Measure E).tilted (fun u => -(0:ℝ)-‖y-u‖^2/(8*(1:ℝ)))) =
      (fun _ : E => 0) := by
    rw [he]
    exact gradient_fun_const' 1
  have hOne : MemLp (fun _ : E => (1:ℝ)) 2 _ := by simpa only [he] using hp
  have hZero : MemLp (fun _ : E => (0:E)) 2 _ := by simpa only [hge] using hq
  refine ⟨G,hOne,hZero,?_,hmean.2.1,hge⟩
  simpa only [he,hge,gradient_fun_const'] using hPair

#print axioms SourceMeanGradientDomain.literal_source_mean_in_closed_gradient
#print axioms actual_macroscopic_mean_closed_gradient
#print axioms rank_zero_noncentered_source_mean_graph

end
end Tests.ProximalBPSSourceMeanGradientDomain
