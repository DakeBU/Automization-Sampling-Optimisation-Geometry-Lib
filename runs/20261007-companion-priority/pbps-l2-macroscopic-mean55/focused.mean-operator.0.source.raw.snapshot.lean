import AutoSamplingTheory.ExampleCases.ProximalBPS.MacroscopicEnergy
import AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.GaussianMarginalGradient

open MeasureTheory ProbabilityTheory
open scoped ContDiff NNReal Topology
namespace AutoSamplingTheory.ExampleCases.ProximalBPS.L2MacroscopicMean
set_option maxHeartbeats 800000

private theorem pullback_stage
    {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]
    {V : E → ℝ} {α β : ℝ≥0} {η : ℝ}
    (hα : 0 < (α : ℝ)) (hαβ : α ≤ β) (hV : ContDiff ℝ 2 V)
    (hH : ∀ x v : E, (α : ℝ)*‖v‖^2 ≤ (fderiv ℝ (fderiv ℝ V) x v) v ∧
      (fderiv ℝ (fderiv ℝ V) x v) v ≤ (β : ℝ)*‖v‖^2)
    (hη : 0 < η) (hβη : (β : ℝ)*η ≤ 1) :
    let μ := (volume : Measure E).tilted (fun x => -V x)
    let J := (μ.prod (stdGaussian E)).map
      (fun p : E × E => (p.1,p.1+Real.sqrt η • p.2))
    let ν := J.snd
    let F := fun p : E × E => (p.1,(2 : ℝ) • p.1-p.2)
    let P : Lp ℝ 2 J →L[ℝ] Lp ℝ 2 J :=
      (lpMeas ℝ ℝ (MeasurableSpace.comap Prod.snd (inferInstance : MeasurableSpace E))
        2 J).subtypeL ∘L condExpL2 ℝ ℝ measurable_snd.comap_le
    ∃ U : Lp ℝ 2 J →ₗᵢ[ℝ] Lp ℝ 2 J,
      (∀ g : Lp ℝ 2 J, (U g : E × E → ℝ) =ᵐ[J] g ∘ F) ∧
      ∃ M : Lp ℝ 2 ν →ₗᵢ[ℝ] Lp ℝ 2 J,
        (∀ u : Lp ℝ 2 ν, (M u : E × E → ℝ) =ᵐ[J] u ∘ Prod.snd) ∧
        ∀ u, P (M u) = M u ∧
          (P * U.toContinuousLinearMap * P) (M u) ∈ M.toLinearMap.range := by
  dsimp only
  let μ := (volume : Measure E).tilted (fun x => -V x)
  let J := (μ.prod (stdGaussian E)).map
    (fun p : E × E => (p.1,p.1+Real.sqrt η • p.2))
  let ν := J.snd
  let P : Lp ℝ 2 J →L[ℝ] Lp ℝ 2 J :=
    (lpMeas ℝ ℝ (MeasurableSpace.comap Prod.snd (inferInstance : MeasurableSpace E))
      2 J).subtypeL ∘L condExpL2 ℝ ℝ measurable_snd.comap_le
  obtain ⟨hμ,hJ,hν,R,S,hR,hS,hRc,hSr,hSd,hSc,hSf,U,hU,hUi,hUs,hops⟩ :=
    MacroscopicEnergy.actual_macroscopic_gradient_energy_blocks hα hαβ hV hH hη hβη
  let : IsProbabilityMeasure μ := hμ
  let : IsProbabilityMeasure J := hJ
  let : IsProbabilityMeasure ν := hν
  obtain ⟨hBA,hBD,hdef,hcompact⟩ := hops
  let A := P * U.toContinuousLinearMap * P
  have hp : MeasurePreserving (Prod.snd : E × E → E) J ν := ⟨measurable_snd,rfl⟩
  let M : Lp ℝ 2 ν →ₗᵢ[ℝ] Lp ℝ 2 J := Lp.compMeasurePreservingₗᵢ ℝ Prod.snd hp
  have hM (u : Lp ℝ 2 ν) : (M u : E × E → ℝ) =ᵐ[J] u ∘ Prod.snd :=
    Lp.coeFn_compMeasurePreserving u hp
  obtain ⟨D,hDense,hClose,hClosed,hGraph⟩ :=
    AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.GaussianMarginalGradient.gaussian_marginal_gradient_closable μ hη
  have hCore (u : Lp ℝ 2 ν) (hu : u ∈ D.domain) :
      P (M u) = M u ∧ A (M u) ∈ M.toLinearMap.range := by
    obtain ⟨f,hf,hfc,huf,hdf⟩ := (hGraph u (D ⟨u,hu⟩)).mp (D.mem_graph ⟨u,hu⟩)
    obtain ⟨hTd,hfLp,hTfLp,hgrad,hvar,g,hg,hPg,hAg,hn,hAn,hvb,hEnergy⟩ := hcompact f hf hfc
    have hufJ : (fun p : E × E => u p.2) =ᵐ[J] (fun p => f p.2) :=
      ae_of_ae_map measurable_snd.aemeasurable huf
    have hMg : M u = g := Lp.ext ((hM u).trans (hufJ.trans hg.symm))
    refine ⟨by rw [hMg]; exact hPg, ?_⟩
    let v := hTfLp.toLp (fun y => ∫ x, f x ∂S y)
    have hvJ : (fun p : E × E => v p.2) =ᵐ[J]
        (fun p => ∫ x, f x ∂S p.2) :=
      ae_of_ae_map measurable_snd.aemeasurable hTfLp.coeFn_toLp
    have hAv : A (M u) = M v := by
      rw [hMg]
      exact Lp.ext (hAg.trans ((hM v).trans hvJ).symm)
    exact ⟨v,hAv.symm⟩
  have hPM (u : Lp ℝ 2 ν) : P (M u) = M u := by
    exact hDense.induction (P := fun v => P (M v) = M v)
      (fun v hv => (hCore v hv).1)
      (isClosed_eq (P.continuous.comp M.continuous) M.continuous) u
  have hAM (u : Lp ℝ 2 ν) : A (M u) ∈ M.toLinearMap.range := by
    exact hDense.induction (P := fun v => A (M v) ∈ M.toLinearMap.range)
      (fun v hv => (hCore v hv).2)
      (M.isometry.isClosedEmbedding.isClosed_range.preimage (A.continuous.comp M.continuous)) u
  exact ⟨U,hU,M,hM,fun u => ⟨hPM u,hAM u⟩⟩

#print axioms pullback_stage
#check ContinuousLinearMap.codRestrict
#check LinearIsometry.equivRange
end AutoSamplingTheory.ExampleCases.ProximalBPS.L2MacroscopicMean
