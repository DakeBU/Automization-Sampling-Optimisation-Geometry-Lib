import AutoSamplingTheory.ExampleCases.ProximalBPS.MacroscopicEnergy

namespace Tests.ProximalBPSMacroscopicEnergy
noncomputable section
set_option autoImplicit false
open MeasureTheory ProbabilityTheory InnerProductSpace
open scoped ContDiff RealInnerProductSpace NNReal
open AutoSamplingTheory.ExampleCases.ProximalBPS
set_option maxHeartbeats 800000

-- At the genuine Gaussian precision step the actual gradient energy vanishes.
-- Keep actual joint classes, squared moments and the microscopic variance norm.
theorem gaussian_precision_macroscopic_energy
    {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E] :
    let V := fun x : E => (1/2 : ℝ)*‖x‖^2
    let μ := (volume : Measure E).tilted (fun x => -V x)
    let J := Measure.map (fun p : E × E => (p.1,p.1+Real.sqrt 1 • p.2)) (μ.prod (stdGaussian E))
    let ν := J.snd
    let Λ := J.map (fun p : E × E => (p.2,(2:ℝ) • p.1-p.2))
    let P : Lp ℝ 2 J →L[ℝ] Lp ℝ 2 J :=
      (lpMeas ℝ ℝ (MeasurableSpace.comap Prod.snd (inferInstance : MeasurableSpace E))
        2 J).subtypeL ∘L condExpL2 ℝ ℝ measurable_snd.comap_le
    IsProbabilityMeasure ν ∧ ∃ S : Kernel E E, IsMarkovKernel S ∧ Λ.IsCondKernel S ∧
      ∃ U : Lp ℝ 2 J →ₗᵢ[ℝ] Lp ℝ 2 J,
        (∀ g : Lp ℝ 2 J, (U g : E × E → ℝ) =ᵐ[J]
          fun p => g (p.1,(2:ℝ) • p.1-p.2)) ∧
        let A := P * U.toContinuousLinearMap * P
        let B := (1-P) * U.toContinuousLinearMap * P
        (∀ g : Lp ℝ 2 J, P g = g → ‖B g‖^2 = ‖g‖^2-‖A g‖^2) ∧
        ∀ f : E → ℝ, ContDiff ℝ ∞ f → HasCompactSupport f →
          let Tf := fun y => ∫ u, f u ∂S y
          Differentiable ℝ Tf ∧ MemLp f 2 ν ∧ MemLp Tf 2 ν ∧
          MemLp (gradient Tf) 2 ν ∧
          Integrable (fun y =>
            AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.Poincare.variance (S y) f) ν ∧
          ∃ g : Lp ℝ 2 J,
            (g : E × E → ℝ) =ᵐ[J] (fun p => f p.2) ∧ P g = g ∧
            (A g : E × E → ℝ) =ᵐ[J] (fun p => Tf p.2) ∧
            ‖g‖^2 = (∫ y, (f y)^2 ∂ν) ∧ ‖A g‖^2 = (∫ y, (Tf y)^2 ∂ν) ∧
            (∫ y, AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.Poincare.variance
              (S y) f ∂ν) = ‖B g‖^2 ∧
            (∫ y, ‖gradient Tf y‖^2 ∂ν) = 0 := by
  dsimp only
  let V := fun x : E => (1/2 : ℝ)*‖x‖^2
  have hV : ContDiff ℝ 2 V := contDiff_const.mul (contDiff_id.norm_sq (𝕜 := ℝ))
  have hfd (x : E) : fderiv ℝ V x = innerSL ℝ x := by
    have h := ((hasFDerivAt_id x).norm_sq).const_mul (1/2 : ℝ)
    convert h.fderiv using 1 <;> first | rfl | (ext v; simp)
  have hH (x a : E) : fderiv ℝ (fderiv ℝ V) x a a = ‖a‖^2 := by
    rw [show fderiv ℝ V = innerSL ℝ from funext hfd]
    rw [(innerSL ℝ (E := E)).hasFDerivAt.fderiv]
    exact real_inner_self_eq_norm_sq a
  have result :=
    MacroscopicEnergy.actual_macroscopic_gradient_energy_blocks
      (V := V) (α := 1) (β := 1) (η := 1) (by norm_num) (by rfl) hV
      (by intro x a; simp only [hH,NNReal.coe_one,one_mul]; exact ⟨le_rfl,le_rfl⟩)
      (by norm_num) (by norm_num)
  obtain ⟨_,_,hν,R,S,hR,hS,hcond,hSR,hSd,hΛ,hfst,U,hU,hUi,hUs,hBB,hBD,hblock,hf⟩ := result
  refine ⟨hν,S,hS,hΛ,U,hU,hblock,?_⟩
  intro f hfc hfs
  obtain ⟨hd,hf2,hTf2,hg2,hvI,g,hg,hPg,hAg,hgn,hAgn,hv,hb⟩ := hf f hfc hfs
  refine ⟨hd,hf2,hTf2,hg2,hvI,g,hg,hPg,hAg,hgn,hAgn,hv,?_⟩
  norm_num at hb
  apply le_antisymm
  · simpa only [Real.sqrt_one,one_smul] using hb
  · exact integral_nonneg fun _ => sq_nonneg _

-- A nonzero, noncentered smooth compact constant is legal in rank zero.
-- Its actual L2 class has norm-square one; the microscopic block is zero.
theorem rank_zero_noncentered_constant :
    let E := EuclideanSpace ℝ (Fin 0)
    let V := fun x : E => (1/2 : ℝ)*‖x‖^2
    let μ := (volume : Measure E).tilted (fun x => -V x)
    let J := Measure.map (fun p : E × E => (p.1,p.1+Real.sqrt 1 • p.2)) (μ.prod (stdGaussian E))
    let ν := J.snd
    let P : Lp ℝ 2 J →L[ℝ] Lp ℝ 2 J :=
      (lpMeas ℝ ℝ (MeasurableSpace.comap Prod.snd (inferInstance : MeasurableSpace E))
        2 J).subtypeL ∘L condExpL2 ℝ ℝ measurable_snd.comap_le
    IsProbabilityMeasure ν ∧ ∃ S : Kernel E E, IsMarkovKernel S ∧
      ∃ U : Lp ℝ 2 J →ₗᵢ[ℝ] Lp ℝ 2 J,
        (∀ v : Lp ℝ 2 J, (U v : E × E → ℝ) =ᵐ[J]
          fun p => v (p.1,(2:ℝ) • p.1-p.2)) ∧
        let A := P * U.toContinuousLinearMap * P
        let B := (1-P) * U.toContinuousLinearMap * P
        ∃ g : Lp ℝ 2 J,
          (g : E × E → ℝ) =ᵐ[J] (fun _ => 1) ∧ P g = g ∧ A g = g ∧
          ‖g‖^2 = 1 ∧ ‖B g‖^2 = 0 ∧
          (∫ y, AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.Poincare.variance
            (S y) (fun _ => 1) ∂ν) = 0 ∧
          (∫ y, ‖gradient (fun z => ∫ u, (1 : ℝ) ∂S z) y‖^2 ∂ν) = 0 := by
  dsimp only
  let E := EuclideanSpace ℝ (Fin 0)
  let V := fun x : E => (1/2 : ℝ)*‖x‖^2
  let μ := (volume : Measure E).tilted (fun x => -V x)
  let J := Measure.map (fun p : E × E => (p.1,p.1+Real.sqrt 1 • p.2))
    (μ.prod (stdGaussian E))
  let ν := J.snd
  let P : Lp ℝ 2 J →L[ℝ] Lp ℝ 2 J :=
    (lpMeas ℝ ℝ (MeasurableSpace.comap Prod.snd (inferInstance : MeasurableSpace E))
      2 J).subtypeL ∘L condExpL2 ℝ ℝ measurable_snd.comap_le
  obtain ⟨hν,S,hS,hΛ,U,hU,hblock,hf⟩ := gaussian_precision_macroscopic_energy (E := E)
  let : IsProbabilityMeasure ν := hν
  let : IsMarkovKernel S := hS
  have hfc : HasCompactSupport (fun _ : E => (1 : ℝ)) :=
    (isClosed_tsupport _).isCompact
  obtain ⟨hd,hf2,hTf2,hgrad2,hvI,g,hg,hPg,hAg,hgn,hAgn,hv,hE⟩ :=
    hf (fun _ => 1) contDiff_const hfc
  have hTf (y : E) : (∫ u, (1 : ℝ) ∂S y) = 1 := by simp
  let A := P * U.toContinuousLinearMap * P
  have hAgEq : A g = g := by
    apply Lp.ext
    apply hAg.trans
    filter_upwards [hg] with p hp
    simp only [hTf,hp]
  have hmass : ν.real Set.univ = 1 := Measure.real_univ_eq_one
  have hgn1 : ‖g‖^2 = 1 := hgn.trans (by
    change (∫ _ : E, (1 : ℝ)^2 ∂ν) = 1
    simp only [one_pow,integral_const,hmass,one_smul])
  have hAgn1 : ‖A g‖^2 = (1 : ℝ) := hAgn.trans (by
    change (∫ y : E, (∫ u, (1 : ℝ) ∂S y)^2 ∂ν) = 1
    simp only [hTf,one_pow,integral_const,hmass,one_smul])
  have hB0 := hblock g hPg
  rw [hgn1,hAgn1,sub_self] at hB0
  refine ⟨hν,S,hS,U,hU,g,hg,hPg,hAgEq,hgn1,hB0,?_,hE⟩
  exact hv.trans hB0

#print axioms MacroscopicEnergy.actual_macroscopic_gradient_energy_blocks
#print axioms gaussian_precision_macroscopic_energy
#print axioms rank_zero_noncentered_constant
end
end Tests.ProximalBPSMacroscopicEnergy
