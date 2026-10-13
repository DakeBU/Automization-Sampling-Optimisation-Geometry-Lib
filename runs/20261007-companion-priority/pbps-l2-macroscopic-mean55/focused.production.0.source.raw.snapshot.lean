import AutoSamplingTheory.ExampleCases.ProximalBPS.MacroscopicEnergy
import AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.GaussianMarginalGradient

open MeasureTheory ProbabilityTheory
open scoped ContDiff NNReal Topology
namespace AutoSamplingTheory.ExampleCases.ProximalBPS.L2MacroscopicMean
set_option maxHeartbeats 800000

theorem actual_macroscopic_l2_mean
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
    let Λ := J.map (fun p : E × E => (p.2,(2 : ℝ) • p.1-p.2))
    let F := fun p : E × E => (p.1,(2 : ℝ) • p.1-p.2)
    let P : Lp ℝ 2 J →L[ℝ] Lp ℝ 2 J :=
      (lpMeas ℝ ℝ (MeasurableSpace.comap Prod.snd (inferInstance : MeasurableSpace E))
        2 J).subtypeL ∘L condExpL2 ℝ ℝ measurable_snd.comap_le
    IsProbabilityMeasure μ ∧ IsProbabilityMeasure J ∧ IsProbabilityMeasure ν ∧
    ∃ S : Kernel E E, IsMarkovKernel S ∧
      (∀ y, S y = (volume : Measure E).tilted
        (fun x => -V ((1/2 : ℝ) • (y+x)) - ‖y-x‖^2/(8*η))) ∧
      Λ.IsCondKernel S ∧ Λ.fst = ν ∧ Λ.snd = ν ∧
      ∃ U : Lp ℝ 2 J →ₗᵢ[ℝ] Lp ℝ 2 J,
        (∀ g : Lp ℝ 2 J, (U g : E × E → ℝ) =ᵐ[J] g ∘ F) ∧
        Function.Involutive U ∧ IsSelfAdjoint U.toContinuousLinearMap ∧
        ∃ M : Lp ℝ 2 ν →ₗᵢ[ℝ] Lp ℝ 2 J,
          (∀ u : Lp ℝ 2 ν, (M u : E × E → ℝ) =ᵐ[J] u ∘ Prod.snd) ∧
          ∃ T : Lp ℝ 2 ν →L[ℝ] Lp ℝ 2 ν,
            let A := P * U.toContinuousLinearMap * P
            let B := (1-P) * U.toContinuousLinearMap * P
            ∀ u : Lp ℝ 2 ν,
              P (M u) = M u ∧ M (T u) = A (M u) ∧ ‖T u‖ ≤ ‖u‖ ∧
              (T u : E → ℝ) =ᵐ[ν] (fun y => ∫ x, u x ∂S y) ∧
              (∀ᵐ y ∂ν, Integrable (u : E → ℝ) (S y) ∧
                Integrable (fun x => (u x)^2) (S y)) ∧
              Integrable (fun y =>
                AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.Poincare.variance
                  (S y) (u : E → ℝ)) ν ∧
              (∫ y, AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.Poincare.variance
                (S y) (u : E → ℝ) ∂ν) = ‖B (M u)‖^2 ∧
              ‖B (M u)‖^2 = ‖u‖^2-‖T u‖^2 := by
  dsimp only
  let μ := (volume : Measure E).tilted (fun x => -V x)
  let J := (μ.prod (stdGaussian E)).map
    (fun p : E × E => (p.1,p.1+Real.sqrt η • p.2))
  let ν := J.snd
  let Λ := J.map (fun p : E × E => (p.2,(2 : ℝ) • p.1-p.2))
  let F := fun p : E × E => (p.1,(2 : ℝ) • p.1-p.2)
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
  let Ar := (A.comp M.toContinuousLinearMap).codRestrict M.toLinearMap.range hAM
  let T : Lp ℝ 2 ν →L[ℝ] Lp ℝ 2 ν :=
    M.equivRange.symm.toContinuousLinearEquiv.toContinuousLinearMap.comp Ar
  have hMT (u : Lp ℝ 2 ν) : M (T u) = A (M u) := by
    have he := M.equivRange.apply_symm_apply (Ar u)
    exact congrArg Subtype.val he
  have hPn (v : Lp ℝ 2 J) : ‖P v‖ ≤ ‖v‖ :=
    norm_condExpL2_coe_le measurable_snd.comap_le v
  have hTn (u : Lp ℝ 2 ν) : ‖T u‖ ≤ ‖u‖ := by
    calc
      ‖T u‖ = ‖M (T u)‖ := (M.norm_map _).symm
      _ = ‖A (M u)‖ := by rw [hMT]
      _ = ‖P (U (M u))‖ := by
        change ‖P (U (P (M u)))‖ = ‖P (U (M u))‖
        rw [hPM]
      _ ≤ ‖U (M u)‖ := hPn _
      _ = ‖u‖ := by rw [U.norm_map,M.norm_map]

  let : IsMarkovKernel R := hR
  let : IsMarkovKernel S := hS
  let : (J.map Prod.swap).IsCondKernel R := hRc
  let : Λ.IsCondKernel S := hSc
  obtain ⟨hFi,hFmap⟩ := GaussianReflection.reflection_preserves_augmentation μ η hη
  have hFm : Measurable F := by fun_prop
  have hFp : MeasurePreserving F J J := ⟨hFm,hFmap⟩
  have hΛsnd : Λ.snd = ν := by
    calc
      Λ.snd = (J.map F).snd := by
        dsimp only [Λ,Measure.snd]
        rw [Measure.map_map measurable_snd (by fun_prop),Measure.map_map measurable_snd hFm]
        rfl
      _ = ν := by rw [hFmap]
  have hstation : S ∘ₘ ν = ν := by
    rw [← Measure.snd_compProd,← hSf,Measure.disintegrate Λ S,hΛsnd]
  obtain ⟨R₀,hR₀,hR₀d,hR₀c⟩ :=
    AutoSamplingTheory.TechnicalLemmas.Probability.GaussianConditionalKernel.exists_tilted_isCondKernel μ hη
  let : IsMarkovKernel R₀ := hR₀
  let : (J.map Prod.swap).IsCondKernel R₀ := hR₀c
  obtain ⟨R₁,hR₁,hR₁d,U₁,hU₁,hUi₁,hUs₁,hPk,hAlgebra₁⟩ :=
    ReflectionL2.actual_reflection_block_identities μ hη
  have hR₁₀ : R₁ = R₀ := by
    ext y s hs
    rw [hR₁d y,hR₀d y]
  have hR₀R : R₀ =ᵐ[ν] R := by
    have h₀ := eq_condKernel_of_measure_eq_compProd R₀ (Measure.disintegrate (J.map Prod.swap) R₀).symm
    have hr := eq_condKernel_of_measure_eq_compProd R (Measure.disintegrate (J.map Prod.swap) R).symm
    simpa only [Measure.fst_map_swap] using h₀.trans hr.symm
  have hR₁R : R₁ =ᵐ[ν] R := by rw [hR₁₀]; exact hR₀R
  have hSource (u : Lp ℝ 2 ν) :
      (T u : E → ℝ) =ᵐ[ν] (fun y => ∫ x, u x ∂S y) := by
    have huS : Integrable (u : E → ℝ) (S ∘ₘ ν) := by
      rw [hstation]
      exact (Lp.memLp u).integrable (by norm_num)
    have hfiberS := Measure.ae_integrable_of_integrable_comp huS
    have hUM : (U (M u) : E × E → ℝ) =ᵐ[J]
        (fun p => u ((2 : ℝ) • p.1-p.2)) :=
      (hU (M u)).trans (hFp.quasiMeasurePreserving.ae_eq (hM u))
    have hswap : (fun p : E × E => (U (M u)) (p.2,p.1)) =ᵐ[J.map Prod.swap]
        (fun p => u ((2 : ℝ) • p.2-p.1)) := by
      rw [← (MeasurableEquiv.prodComm : E × E ≃ᵐ E × E).map_ae]
      simpa only [Filter.eventually_map] using hUM
    have hswap' : (fun p : E × E => (U (M u)) (p.2,p.1)) =ᵐ[ν ⊗ₘ R]
        (fun p => u ((2 : ℝ) • p.2-p.1)) := by
      rw [← Measure.fst_map_swap (μ := J),Measure.disintegrate (J.map Prod.swap) R]
      exact hswap
    have hfiberR := Measure.ae_ae_of_ae_compProd hswap'
    have hSourceJ : (fun p : E × E => (T u) p.2) =ᵐ[J]
        (fun p => ∫ x, u x ∂S p.2) := by
      have hMTae : (M (T u) : E × E → ℝ) =ᵐ[J]
          (fun p => ∫ x, (U (M u)) (x,p.2) ∂R₁ p.2) := by
        rw [hMT]
        change (P (U (P (M u))) : E × E → ℝ) =ᵐ[J] _
        rw [hPM]
        exact hPk (U (M u))
      have hkJ := ae_of_ae_map measurable_snd.aemeasurable hR₁R
      have hfJ := ae_of_ae_map measurable_snd.aemeasurable hfiberR
      have hfiJ := ae_of_ae_map measurable_snd.aemeasurable hfiberS
      filter_upwards [(hM (T u)).symm.trans hMTae,hkJ,hfJ,hfiJ] with p hmean hk hf hfi
      rw [hmean,hk,integral_congr_ae hf,hSr p.2]
      exact (integral_map (by fun_prop) (by simpa only [hSr p.2] using hfi.aestronglyMeasurable)).symm
    exact (ae_map_iff measurable_snd.aemeasurable
      (measurableSet_eq_fun (T u).stronglyMeasurable.measurable
        (u.stronglyMeasurable.integral_kernel.measurable))).mpr hSourceJ
  let B := (1-P) * U.toContinuousLinearMap * P
  refine ⟨hμ,hJ,hν,S,hS,hSd,hSc,hSf,hΛsnd,U,hU,hUi,hUs,M,hM,T,?_⟩
  intro u
  have huS : Integrable (u : E → ℝ) (S ∘ₘ ν) := by
    rw [hstation]
    exact (Lp.memLp u).integrable (by norm_num)
  have huSqS : Integrable (fun x => (u x)^2) (S ∘ₘ ν) := by
    rw [hstation]
    exact (Lp.memLp u).integrable_sq
  have hfS := Measure.ae_integrable_of_integrable_comp huS
  have hfSqS := Measure.ae_integrable_of_integrable_comp huSqS
  have hfs : ∀ᵐ y ∂ν, Integrable (u : E → ℝ) (S y) ∧
      Integrable (fun x => (u x)^2) (S y) := hfS.and hfSqS
  have hmean := hSource u
  let m := fun y => ∫ x, u x ∂S y
  have hmLp : MemLp m 2 ν := (Lp.memLp (T u)).congr hmean
  have hsqI : Integrable (fun y => ∫ x, (u x)^2 ∂S y) ν := by
    have hi := Measure.integrable_integral_norm_of_integrable_comp huSqS
    simpa only [Real.norm_eq_abs,abs_pow,sq_abs] using hi
  have hvarEq : (fun y => AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.Poincare.variance
      (S y) (u : E → ℝ)) =ᵐ[ν] (fun y => (∫ x, (u x)^2 ∂S y)-(m y)^2) := by
    filter_upwards [hfSqS] with y hy
    have hLpY := (memLp_two_iff_integrable_sq u.stronglyMeasurable.aestronglyMeasurable).mpr hy
    dsimp only [AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.Poincare.variance,m]
    rw [← variance_eq_integral hLpY.aemeasurable,variance_eq_sub hLpY]
    rfl
  have hvarI : Integrable (fun y =>
      AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.Poincare.variance (S y) (u : E → ℝ)) ν :=
    (hsqI.sub hmLp.integrable_sq).congr hvarEq.symm
  have hsecond : (∫ y, ∫ x, (u x)^2 ∂S y ∂ν) = ∫ x, (u x)^2 ∂ν := by
    have hj : Integrable (fun p : E × E => (u p.2)^2) (ν ⊗ₘ S) := by
      rw [← hSf,Measure.disintegrate Λ S]
      apply ((Lp.memLp u).comp_measurePreserving
        (show MeasurePreserving (Prod.snd : E × E → E) Λ ν from ⟨measurable_snd,hΛsnd⟩)).integrable_sq
    rw [← Measure.integral_compProd hj,← hSf,Measure.disintegrate Λ S]
    exact (integral_map measurable_snd.aemeasurable
      (by simpa only [← Measure.snd, hΛsnd] using (Lp.memLp u).integrable_sq.aestronglyMeasurable)).symm
  have hn (v : Lp ℝ 2 ν) : ‖v‖^2 = ∫ y, (v y)^2 ∂ν := by
    calc
      ‖v‖^2 = inner ℝ v v := (real_inner_self_eq_norm_sq v).symm
      _ = ∫ y, (v y)^2 ∂ν := by rw [L2.inner_def]; simp only [real_inner_self_eq_norm_sq,Real.norm_eq_abs,sq_abs]
  have hDef : ‖B (M u)‖^2 = ‖u‖^2-‖T u‖^2 := by
    calc
      ‖B (M u)‖^2 = ‖M u‖^2-‖A (M u)‖^2 := hdef _ (hPM u)
      _ = ‖u‖^2-‖T u‖^2 := by rw [M.norm_map,← hMT,M.norm_map]
  have hvarDef : (∫ y,
      AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.Poincare.variance (S y) (u : E → ℝ) ∂ν) =
      ‖B (M u)‖^2 := by
    rw [integral_congr_ae hvarEq,integral_sub hsqI hmLp.integrable_sq,hsecond,hDef,hn u,hn (T u)]
    congr 1
    exact (integral_congr_ae (hmean.fun_pow 2)).symm
  exact ⟨hPM u,hMT u,hTn u,hmean,hfs,hvarI,hvarDef,hDef⟩

end AutoSamplingTheory.ExampleCases.ProximalBPS.L2MacroscopicMean
