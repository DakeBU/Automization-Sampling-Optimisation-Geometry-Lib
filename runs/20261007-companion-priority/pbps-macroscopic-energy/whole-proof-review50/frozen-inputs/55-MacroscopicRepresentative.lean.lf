import AutoSamplingTheory.ExampleCases.ProximalBPS.ConditionalScore
import AutoSamplingTheory.ExampleCases.ProximalBPS.ReflectionL2
import Mathlib.Probability.Kernel.Composition.MeasureCompProd
import Mathlib.Probability.Kernel.MeasurableIntegral

/-!
# The actual compressed reflection has a differentiable representative

Source: arXiv:2609.06905v1 Appendix C.1, connecting the conditional expectation
to the macroscopic compression from Appendix B.1. This identifies actual joint
disintegration, L2 classes and the classical smooth-test derivative. It does
not supply a conditional Poincare inequality or a general Sobolev extension.
-/

open MeasureTheory ProbabilityTheory
open scoped ContDiff

namespace AutoSamplingTheory.ExampleCases.ProximalBPS.MacroscopicRepresentative

universe u

/-- The actual reflected pair has conditional kernel S, and the actual
compressed reflection PUP of each smooth compactly supported macroscopic test
has the S-expectation as an L2 representative with the score covariance
derivative. All conditional and representative identities use one compatible
kernel; no equality between independently existential witnesses is assumed. -/
theorem macroscopic_reflection_smooth_representative {E : Type u} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]
    {V : E → ℝ} {α β : NNReal} {η : ℝ}
    (hα : 0 < (α : ℝ)) (hV : ContDiff ℝ 2 V)
    (hH : ∀ x v : E,
      (α : ℝ)*‖v‖^2 ≤ (fderiv ℝ (fderiv ℝ V) x v) v ∧
      (fderiv ℝ (fderiv ℝ V) x v) v ≤ (β : ℝ)*‖v‖^2) (hη : 0 < η) :
    let μ := (volume : Measure E).tilted (fun x => -V x)
    let J := Measure.map (fun p : E × E => (p.1,p.1+Real.sqrt η • p.2))
      (μ.prod (stdGaussian E))
    let Λ := J.map (fun p : E × E => (p.2,(2:ℝ) • p.1-p.2))
    let P : Lp ℝ 2 J →L[ℝ] Lp ℝ 2 J :=
      (lpMeas ℝ ℝ (MeasurableSpace.comap Prod.snd (inferInstance : MeasurableSpace E)) 2 J).subtypeL
        ∘L condExpL2 ℝ ℝ measurable_snd.comap_le
    let s := fun y u : E => -(1/2:ℝ) • fderiv ℝ V ((1/2:ℝ) • (y+u)) -
      (1/(4*η)) • innerSL ℝ (y-u)
    ∃ S : Kernel E E, IsMarkovKernel S ∧ Λ.IsCondKernel S ∧ Λ.fst = J.snd ∧
      ∃ U : Lp ℝ 2 J →ₗᵢ[ℝ] Lp ℝ 2 J,
        (∀ g : Lp ℝ 2 J, (U g : E × E → ℝ) =ᵐ[J]
          (fun p => g (p.1,(2:ℝ) • p.1-p.2))) ∧
        Function.Involutive U ∧ IsSelfAdjoint U.toContinuousLinearMap ∧
        ∀ (f : E → ℝ), ContDiff ℝ ∞ f → HasCompactSupport f →
          ∃ g : Lp ℝ 2 J,
            (g : E × E → ℝ) =ᵐ[J] (fun p => f p.2) ∧ P g = g ∧
            ((P * U.toContinuousLinearMap * P) g : E × E → ℝ) =ᵐ[J]
              (fun p => ∫ u, f u ∂S p.2) ∧
            MemLp (fun y => ∫ u, f u ∂S y) 2 J.snd ∧
            ∀ y, Integrable (s y) (S y) ∧ Integrable (fun u => f u • s y u) (S y) ∧
              HasFDerivAt (fun z => ∫ u, f u ∂S z)
              ((∫ u, f u • s y u ∂S y) -
                (∫ u, f u ∂S y) • (∫ u, s y u ∂S y)) y := by
  have reflected_disintegration {E : Type u} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
      [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]
      (ρ : Measure (E × E)) [IsFiniteMeasure ρ]
      (R S : Kernel E E) [IsMarkovKernel R] [IsMarkovKernel S]
      [ρ.IsCondKernel R]
      (hS : ∀ y, S y = (R y).map (fun x => (2:ℝ) • x-y)) :
      let G := fun p : E × E => (p.1,(2:ℝ) • p.2-p.1)
      (ρ.map G).fst = ρ.fst ∧ (ρ.map G).IsCondKernel S := by
    let G := fun p : E × E => (p.1,(2:ℝ) • p.2-p.1)
    have hG : Measurable G := by fun_prop
    have hfst : (ρ.map G).fst = ρ.fst := by
      exact Measure.fst_map_prodMk (by fun_prop)
    have hmap : ρ.fst ⊗ₘ S = (ρ.fst ⊗ₘ R).map G := by
      ext t ht
      rw [Measure.compProd_apply ht, Measure.map_apply hG ht,
        Measure.compProd_apply (hG ht)]
      apply lintegral_congr_ae
      filter_upwards with y
      rw [hS y, Measure.map_apply (by fun_prop) (measurable_prodMk_left ht)]
      rfl
    refine ⟨hfst,⟨?_⟩⟩
    rw [hfst,hmap,Measure.disintegrate ρ R]



  have macroscopic_class {E : Type u} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
      [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]
      (J : Measure (E × E)) [IsProbabilityMeasure J]
      (f : E → ℝ) (hf : Continuous f) {M : ℝ} (hMf : ∀ u, ‖f u‖ ≤ M) :
      let P : Lp ℝ 2 J →L[ℝ] Lp ℝ 2 J :=
        (lpMeas ℝ ℝ (MeasurableSpace.comap Prod.snd (inferInstance : MeasurableSpace E)) 2 J).subtypeL
          ∘L condExpL2 ℝ ℝ measurable_snd.comap_le
      ∃ g : Lp ℝ 2 J, (g : E × E → ℝ) =ᵐ[J] (fun p => f p.2) ∧ P g = g := by
    let mY : MeasurableSpace (E × E) := MeasurableSpace.comap Prod.snd (inferInstance : MeasurableSpace E)
    let _ : MeasurableSpace (E × E) := Prod.instMeasurableSpace
    have hm : mY ≤ Prod.instMeasurableSpace := measurable_snd.comap_le
    let : Fact (mY ≤ Prod.instMeasurableSpace) := ⟨hm⟩
    have hLp : MemLp (fun p : E × E => f p.2) 2 J :=
      MemLp.of_bound (hf.comp continuous_snd).aestronglyMeasurable M
        (Filter.Eventually.of_forall fun p => hMf p.2)
    let g := hLp.toLp (fun p : E × E => f p.2)
    have hg : (g : E × E → ℝ) =ᵐ[J] (fun p => f p.2) := hLp.coeFn_toLp
    have hSnd : Measurable[mY] (Prod.snd : E × E → E) := measurable_iff_comap_le.mpr le_rfl
    have hgm : AEStronglyMeasurable[mY] (g : E × E → ℝ) J :=
      (hf.stronglyMeasurable.comp_measurable hSnd).aestronglyMeasurable.congr hg.symm
    refine ⟨g,hg,?_⟩
    change (lpMeas ℝ ℝ mY 2 J).starProjection g = g
    exact Submodule.starProjection_eq_self_iff.mpr (mem_lpMeas_iff_aestronglyMeasurable.mpr hgm)



  have projection_kernel {E : Type u} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
      [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]
      (J : Measure (E × E)) [IsProbabilityMeasure J]
      (R : Kernel E E) [IsMarkovKernel R] [(J.map Prod.swap).IsCondKernel R]
      (v : Lp ℝ 2 J) :
      let P : Lp ℝ 2 J →L[ℝ] Lp ℝ 2 J :=
        (lpMeas ℝ ℝ (MeasurableSpace.comap Prod.snd (inferInstance : MeasurableSpace E)) 2 J).subtypeL
          ∘L condExpL2 ℝ ℝ measurable_snd.comap_le
      (P v : E × E → ℝ) =ᵐ[J] (fun p => ∫ x, v (x,p.2) ∂R p.2) := by
    have hvI := (Lp.memLp v).integrable (by norm_num)
    have hswap : Integrable (fun p : E × E => v p.swap) (J.map Prod.swap) := by
      apply (integrable_map_equiv (MeasurableEquiv.prodComm : E × E ≃ᵐ E × E) _).2
      exact hvI
    have h := condExp_prod_ae_eq_integral_condDistrib'
      (μ := J) (X := Prod.snd) (Y := Prod.fst)
      (f := fun p : E × E => v p.swap) measurable_snd measurable_fst.aemeasurable hswap
    have heq : R =ᵐ[(J.map Prod.swap).fst] (J.map Prod.swap).condKernel :=
      eq_condKernel_of_measure_eq_compProd R (Measure.disintegrate _ _).symm
    rw [Measure.fst_map_swap] at heq
    have heq' : ∀ᵐ p ∂J, R p.2 = (J.map Prod.swap).condKernel p.2 :=
      ae_of_ae_map measurable_snd.aemeasurable heq
    have hP := (Lp.memLp v).condExpL2_ae_eq_condExp (𝕜 := ℝ) measurable_snd.comap_le
    rw [Lp.toLp_coeFn] at hP
    apply hP.trans
    filter_upwards [h,heq'] with p hp he
    rw [he]
    simp only [condDistrib] at hp
    exact hp

  have fiber_ae {E : Type u} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
      [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]
      (J : Measure (E × E)) [IsProbabilityMeasure J]
      (R : Kernel E E) [IsMarkovKernel R] [(J.map Prod.swap).IsCondKernel R]
      {a b : E × E → ℝ} (hab : a =ᵐ[J] b) :
      ∀ᵐ y ∂J.snd, (fun x => a (x,y)) =ᵐ[R y] (fun x => b (x,y)) := by
    have hswap : (fun p : E × E => a p.swap) =ᵐ[J.map Prod.swap] (fun p => b p.swap) := by
      apply (MeasurableEquiv.prodComm.measurableEmbedding.ae_map_iff).2
      change ∀ᵐ p ∂J, a p.swap.swap = b p.swap.swap
      simp only [Prod.swap_swap]
      exact hab
    rw [← Measure.disintegrate (J.map Prod.swap) R] at hswap
    have h := Measure.ae_ae_of_ae_compProd hswap
    rw [Measure.fst_map_swap] at h
    exact h



  have expectation_memLp {E : Type u} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
      [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]
      (ν : Measure E) [IsFiniteMeasure ν] (S : Kernel E E) [IsMarkovKernel S]
      (f : E → ℝ) (hf : Continuous f) {M : ℝ} (hMf : ∀ u, ‖f u‖ ≤ M) :
      MemLp (fun y => ∫ u, f u ∂S y) 2 ν := by
    refine MemLp.of_bound hf.stronglyMeasurable.integral_kernel.aestronglyMeasurable M ?_
    filter_upwards with y
    simpa using (norm_integral_le_of_norm_le_const (μ := S y)
      (Filter.Eventually.of_forall hMf))

  have expectation_map {E : Type u} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
      [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]
      (R S : Kernel E E) (hS : ∀ y, S y = (R y).map (fun x => (2:ℝ) • x-y))
      (f : E → ℝ) (hf : Continuous f) (y : E) :
      ∫ u, f u ∂S y = ∫ x, f ((2:ℝ) • x-y) ∂R y := by
    rw [hS y, integral_map (by fun_prop) hf.aestronglyMeasurable]


  have compressed_representative {E : Type u}
      [NormedAddCommGroup E] [InnerProductSpace ℝ E]
      [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]
      (J : Measure (E × E)) [IsProbabilityMeasure J]
      (R S : Kernel E E) [IsMarkovKernel R] [IsMarkovKernel S]
      [(J.map Prod.swap).IsCondKernel R]
      (hS : ∀ y, S y = (R y).map (fun x => (2:ℝ) • x-y))
      (U : Lp ℝ 2 J →ₗᵢ[ℝ] Lp ℝ 2 J)
      (hF : MeasurePreserving (fun p : E × E => (p.1,(2:ℝ) • p.1-p.2)) J J)
      (hU : ∀ g : Lp ℝ 2 J, (U g : E × E → ℝ) =ᵐ[J]
        (fun p => g (p.1,(2:ℝ) • p.1-p.2)))
      (f : E → ℝ) (hf : Continuous f) (g : Lp ℝ 2 J)
      (hg : (g : E × E → ℝ) =ᵐ[J] (fun p => f p.2)) :
      let P : Lp ℝ 2 J →L[ℝ] Lp ℝ 2 J :=
        (lpMeas ℝ ℝ (MeasurableSpace.comap Prod.snd (inferInstance : MeasurableSpace E)) 2 J).subtypeL
          ∘L condExpL2 ℝ ℝ measurable_snd.comap_le
      (P (U g) : E × E → ℝ) =ᵐ[J] (fun p => ∫ u, f u ∂S p.2) := by
    have hUg : (U g : E × E → ℝ) =ᵐ[J] (fun p => f ((2:ℝ) • p.1-p.2)) :=
      (hU g).trans (hF.quasiMeasurePreserving.ae_eq hg)
    have hs := fiber_ae J R hUg
    have hs' : ∀ᵐ p ∂J, (fun x => (U g) (x,p.2)) =ᵐ[R p.2]
        (fun x => f ((2:ℝ) • x-p.2)) :=
      ae_of_ae_map measurable_snd.aemeasurable hs
    apply (projection_kernel J R (U g)).trans
    filter_upwards [hs'] with p hp
    calc
      (∫ x, (U g) (x,p.2) ∂R p.2) = ∫ x, f ((2:ℝ) • x-p.2) ∂R p.2 :=
        integral_congr_ae hp
      _ = ∫ u, f u ∂S p.2 := (expectation_map R S hS f hf p.2).symm
  let μ := (volume : Measure E).tilted (fun x => -V x)
  let J := Measure.map (fun p : E × E => (p.1,p.1+Real.sqrt η • p.2))
    (μ.prod (stdGaussian E))
  let Λ := J.map (fun p : E × E => (p.2,(2:ℝ) • p.1-p.2))
  have density := AutoSamplingTheory.ExampleCases.ProximalBPS.GibbsAugmentation.normalized_augmentation_density
    hα hV (fun x v => (hH x v).1) hη
  have hi : Integrable (fun x => Real.exp (-V x)) (volume : Measure E) := by
    by_contra hn
    exact (ne_of_gt density.1) (integral_undef hn)
  have : IsProbabilityMeasure μ := isProbabilityMeasure_tilted hi
  have : IsProbabilityMeasure J := Measure.isProbabilityMeasure_map (by fun_prop)
  obtain ⟨R,S,hR,hS,hcond,hSR,hSν,hder⟩ :=
    AutoSamplingTheory.ExampleCases.ProximalBPS.ConditionalScore.reflected_conditional_covariance hα hV hH hη
  let _ : IsMarkovKernel R := hR
  let _ : IsMarkovKernel S := hS
  let _ : (J.map Prod.swap).IsCondKernel R := hcond
  have hΛ : (J.map Prod.swap).map (fun p : E × E => (p.1,(2:ℝ) • p.2-p.1)) = Λ := by
    rw [Measure.map_map (by fun_prop) (by fun_prop)]
    rfl
  obtain ⟨hfst,hΛcond⟩ := reflected_disintegration (J.map Prod.swap) R S hSR
  rw [hΛ,Measure.fst_map_swap] at hfst
  rw [hΛ] at hΛcond
  obtain ⟨R₀,hR₀,hRf₀,U,hU,hUi,hUs,hrest⟩ :=
    AutoSamplingTheory.ExampleCases.ProximalBPS.ReflectionL2.actual_reflection_block_identities μ hη
  have hF : MeasurePreserving (fun p : E × E => (p.1,(2:ℝ) • p.1-p.2)) J J :=
    ⟨by fun_prop,
      (AutoSamplingTheory.ExampleCases.ProximalBPS.GaussianReflection.reflection_preserves_augmentation μ η hη).2⟩
  dsimp only
  refine ⟨S,hS,hΛcond,hfst,U,hU,hUi,hUs,?_⟩
  intro f hf hfc
  obtain ⟨M,hM⟩ := hf.continuous.norm.bddAbove_range_of_hasCompactSupport hfc.norm
  have hMf (u : E) : ‖f u‖ ≤ M := hM (Set.mem_range_self u)
  obtain ⟨g,hg,hPg⟩ := macroscopic_class J f hf.continuous hMf
  refine ⟨g,hg,hPg,?_,expectation_memLp J.snd S f hf.continuous hMf,?_⟩
  · change ((lpMeas ℝ ℝ (MeasurableSpace.comap Prod.snd (inferInstance : MeasurableSpace E)) 2 J).subtypeL
      ∘L condExpL2 ℝ ℝ measurable_snd.comap_le) (U
        (((lpMeas ℝ ℝ (MeasurableSpace.comap Prod.snd (inferInstance : MeasurableSpace E)) 2 J).subtypeL
          ∘L condExpL2 ℝ ℝ measurable_snd.comap_le) g)) =ᵐ[J] _
    rw [hPg]
    exact compressed_representative J R S hSR U hF hU f hf.continuous g hg
  · intro y
    exact hder f hf hfc y


end AutoSamplingTheory.ExampleCases.ProximalBPS.MacroscopicRepresentative
