theorem actual_rough_mean_gradient
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
    let S := fun y : E => (volume : Measure E).tilted
      (fun x => -V ((1/2 : ℝ) • (y+x)) - ‖y-x‖^2/(8*η))
    IsProbabilityMeasure ν ∧
      ∃ G : Lp ℝ 2 ν →ₗ.[ℝ] Lp E 2 ν,
        Dense (G.domain : Set (Lp ℝ 2 ν)) ∧ G.IsClosable ∧ G.closure.IsClosed ∧
        (∀ (u : Lp ℝ 2 ν) (v : Lp E 2 ν), (u,v) ∈ G.graph ↔
          ∃ φ : E → ℝ, ContDiff ℝ ∞ φ ∧ HasCompactSupport φ ∧
            u =ᵐ[ν] φ ∧ v =ᵐ[ν] gradient φ) ∧
        ∃ T : Lp ℝ 2 ν →L[ℝ] Lp ℝ 2 ν,
          ∃ K : Lp ℝ 2 ν →L[ℝ] Lp E 2 ν,
            ∀ u : Lp ℝ 2 ν,
              (T u,K u) ∈ G.closure.graph ∧ ‖T u‖ ≤ ‖u‖ ∧
              (T u : E → ℝ) =ᵐ[ν] (fun y => ∫ x, u x ∂S y) ∧
              (∀ᵐ y ∂ν, Integrable (u : E → ℝ) (S y) ∧
                Integrable (fun x => (u x)^2) (S y)) ∧
              η*‖K u‖^2 ≤
                (1-(α : ℝ)*η)^2/(4*(1+(α : ℝ)*η)) * (‖u‖^2-‖T u‖^2) ∧
              4*η*‖K u‖^2 ≤ ‖u‖^2-‖T u‖^2 := by
  classical
  dsimp only
  let μ := (volume : Measure E).tilted (fun x => -V x)
  let J := (μ.prod (stdGaussian E)).map
    (fun p : E × E => (p.1,p.1+Real.sqrt η • p.2))
  let ν := J.snd
  let S := fun y : E => (volume : Measure E).tilted
    (fun x => -V ((1/2 : ℝ) • (y+x)) - ‖y-x‖^2/(8*η))
  let c := (1-(α : ℝ)*η)^2/(4*(1+(α : ℝ)*η))
  obtain ⟨hμ,hJ,hν,S₀,hS₀,hSd,hSc,hSf,hSs,U,hU,hUi,hUs,M,hM,T,hAll⟩ :=
    L2MacroscopicMean.actual_macroscopic_l2_mean hα hαβ hV hH hη hβη
  let : IsProbabilityMeasure μ := hμ
  let : IsProbabilityMeasure J := hJ
  let : IsProbabilityMeasure ν := hν
  let : IsMarkovKernel S₀ := hS₀
  let Λ := J.map (fun p : E × E => (p.2,(2 : ℝ) • p.1-p.2))
  let : Λ.IsCondKernel S₀ := hSc
  have hstation : S₀ ∘ₘ ν = ν := by
    rw [← Measure.snd_compProd]
    have hc : ν ⊗ₘ S₀ = Λ := by
      have hfirst : Λ.fst = ν := hSf
      rw [← hfirst]
      exact Measure.disintegrate Λ S₀
    rw [hc]
    exact hSs
  obtain ⟨_,G,hDense,hClose,hClosed,hGraph,hMean⟩ :=
    SourceMeanGradientDomain.literal_source_mean_in_closed_gradient hα hαβ hV hH hη hβη
  obtain ⟨_,_,_,R₁,S₁,hR₁,hS₁,hRc₁,hSr₁,hSd₁,hSc₁,hSf₁,
    U₁,hU₁,hUi₁,hUs₁,hBB₁,hBD₁,hBlock₁,hEnergy⟩ :=
    MacroscopicEnergy.actual_macroscopic_gradient_energy_blocks hα hαβ hV hH hη hβη
  have hn (u : Lp ℝ 2 ν) : ‖u‖^2 = ∫ y, (u y)^2 ∂ν := by
    rw [← real_inner_self_eq_norm_sq, L2.inner_def]
    simp only [real_inner_self_eq_norm_sq,Real.norm_eq_abs,sq_abs]
  have hnE (v : Lp E 2 ν) : ‖v‖^2 = ∫ y, ‖v y‖^2 ∂ν := by
    rw [← real_inner_self_eq_norm_sq,L2.inner_def]
    simp only [real_inner_self_eq_norm_sq]
  have hFiberEq (u : Lp ℝ 2 ν) (f : E → ℝ) (hf : u =ᵐ[ν] f) :
      ∀ᵐ y ∂ν, (u : E → ℝ) =ᵐ[S₀ y] f := by
    have hcomp : (u : E → ℝ) =ᵐ[S₀ ∘ₘ ν] f := by rw [hstation]; exact hf
    exact Measure.ae_ae_of_ae_comp hcomp
  have hCore (u : G.domain) :
      ∃ v : Lp E 2 ν, (T u,v) ∈ G.closure.graph ∧
        η*‖v‖^2 ≤ c*(‖(u : Lp ℝ 2 ν)‖^2-‖T u‖^2) := by
    obtain ⟨f,hf,hfc,huf,_⟩ := (hGraph u (G u)).mp (G.mem_graph u)
    let Tf := fun y : E => ∫ x, f x ∂S y
    obtain ⟨hTf,hGrad,hPair⟩ := hMean f hf hfc
    obtain ⟨_,_,hTn,hSource,hFib,_,_,_⟩ := hAll u
    have hTu : T u = hTf.toLp Tf := by
      apply Lp.ext
      filter_upwards [hSource,hFiberEq u f huf,hTf.coeFn_toLp] with y hy heq ht
      exact hy.trans ((integral_congr_ae heq).trans
        ((congrArg (fun m : Measure E => ∫ x, f x ∂m) (hSd y)).trans ht.symm))
    obtain ⟨_,_,_,_,_,g,hg,hPg,hAg,hgn,hAgn,hvb,hSharp⟩ := hEnergy f hf hfc
    have hSame : (fun y : E => ∫ x, f x ∂S₁ y) = Tf := by
      funext y
      exact congrArg (fun m : Measure E => ∫ x, f x ∂m) (hSd₁ y)
    have hUn : ‖(u : Lp ℝ 2 ν)‖^2 = ∫ y, (f y)^2 ∂ν := by
      rw [hn]
      exact integral_congr_ae (Filter.EventuallyEq.fun_comp huf (fun t : ℝ => t^2))
    have hTn' : ‖T u‖^2 = ∫ y, (Tf y)^2 ∂ν := by
      rw [hTu,hn]
      exact integral_congr_ae (Filter.EventuallyEq.fun_comp hTf.coeFn_toLp (fun t : ℝ => t^2))
    have hGradn : ‖hGrad.toLp (gradient Tf)‖^2 = ∫ y, ‖gradient Tf y‖^2 ∂ν := by
      rw [hnE]
      exact integral_congr_ae (Filter.EventuallyEq.fun_comp hGrad.coeFn_toLp (fun t : E => ‖t‖^2))
    have hDef := hBlock₁ g hPg
    rw [hDef,hgn,hAgn] at hSharp
    rw [hSame] at hSharp
    refine ⟨hGrad.toLp (gradient Tf),?_,?_⟩
    · rw [hTu]
      exact hPair
    · rw [hGradn,hUn,hTn']
      exact hSharp
  have hDom (u : G.domain) : T u ∈ G.closure.domain :=
    G.closure.mem_domain_of_mem_graph (hCore u).choose_spec.1
  let q : G.domain →ₗ[ℝ] G.closure.domain :=
    (T.toLinearMap.comp G.domain.subtype).codRestrict G.closure.domain hDom
  let D : G.domain →ₗ[ℝ] Lp E 2 ν := G.closure.toFun.comp q
  have hDpair (u : G.domain) : (T u,D u) ∈ G.closure.graph :=
    G.closure.mem_graph (q u)
  have hDsharp (u : G.domain) :
      η*‖D u‖^2 ≤ c*(‖(u : Lp ℝ 2 ν)‖^2-‖T u‖^2) := by
    obtain ⟨v,hv,hvSharp⟩ := hCore u
    have hDv : D u = v := G.closure.mem_graph_snd_inj (hDpair u) hv rfl
    rw [hDv]
    exact hvSharp
  have hc : 0 ≤ c := div_nonneg (sq_nonneg _) (by positivity)
  have hNormBound (u : G.domain) : ‖D u‖ ≤ Real.sqrt (c/η)*‖(u : Lp ℝ 2 ν)‖ := by
    have hSq : ‖D u‖^2 ≤ (c/η)*‖(u : Lp ℝ 2 ν)‖^2 := by
      calc
        ‖D u‖^2 ≤ (c*‖(u : Lp ℝ 2 ν)‖^2)/η := (le_div_iff₀ hη).mpr (by
          have he := hDsharp u
          have he' := mul_nonneg hc (sq_nonneg ‖T u‖)
          nlinarith)
        _ = (c/η)*‖(u : Lp ℝ 2 ν)‖^2 := by ring
    apply (sq_le_sq₀ (norm_nonneg _) (mul_nonneg (Real.sqrt_nonneg _) (norm_nonneg _))).mp
    rw [mul_pow,Real.sq_sqrt (div_nonneg hc hη.le)]
    exact hSq
  have hRange : DenseRange (G.domain.subtype : G.domain →ₗ[ℝ] Lp ℝ 2 ν) := by
    change Dense (Set.range (Subtype.val : G.domain → Lp ℝ 2 ν))
    have hr : Set.range (Subtype.val : G.domain → Lp ℝ 2 ν) =
        (G.domain : Set (Lp ℝ 2 ν)) := by
      ext x
      constructor
      · rintro ⟨v,rfl⟩
        exact v.property
      · intro hx
        exact ⟨⟨x,hx⟩,rfl⟩
    rw [hr]
    exact hDense
  let K : Lp ℝ 2 ν →L[ℝ] Lp E 2 ν := D.extendOfNorm G.domain.subtype
  have hKcore (u : G.domain) : K u = D u :=
    LinearMap.extendOfNorm_eq hRange ⟨Real.sqrt (c/η),hNormBound⟩ u
  have hPairAll (u : Lp ℝ 2 ν) : (T u,K u) ∈ G.closure.graph := by
    exact hDense.induction (P := fun v => (T v,K v) ∈ G.closure.graph)
      (fun v hv => by rw [hKcore ⟨v,hv⟩]; exact hDpair ⟨v,hv⟩)
      (hClosed.preimage (T.continuous.prodMk K.continuous)) u
  have hSharpAll (u : Lp ℝ 2 ν) :
      η*‖K u‖^2 ≤ c*(‖u‖^2-‖T u‖^2) := by
    exact hDense.induction (P := fun v => η*‖K v‖^2 ≤ c*(‖v‖^2-‖T v‖^2))
      (fun v hv => by rw [hKcore ⟨v,hv⟩]; exact hDsharp ⟨v,hv⟩)
      (isClosed_le (by fun_prop) (by fun_prop)) u
  have haη : 0 ≤ (α : ℝ)*η := mul_nonneg hα.le hη.le
  have haη1 : (α : ℝ)*η ≤ 1 := le_trans
    (mul_le_mul_of_nonneg_right (show (α : ℝ) ≤ (β : ℝ) from by exact_mod_cast hαβ) hη.le) hβη
  have hcCap : c ≤ 1/4 := by
    dsimp only [c]
    apply (div_le_iff₀ (by positivity : 0 < 4*(1+(α : ℝ)*η))).mpr
    nlinarith [mul_nonneg haη (show 0 ≤ 1-(α : ℝ)*η by linarith)]
  refine ⟨hν,G,hDense,hClose,hClosed,hGraph,T,K,?_⟩
  intro u
  obtain ⟨_,_,hTn,hSource,hFib,_,_,_⟩ := hAll u
  have hNonneg : 0 ≤ ‖u‖^2-‖T u‖^2 := by
    have hs := (sq_le_sq₀ (norm_nonneg (T u)) (norm_nonneg u)).mpr hTn
    linarith
  refine ⟨hPairAll u,hTn,?_,?_,hSharpAll u,?_⟩
  · filter_upwards [hSource] with y hy
    exact hy.trans (congrArg (fun m : Measure E => ∫ x, u x ∂m) (hSd y))
  · filter_upwards [hFib] with y hy
    simpa only [hSd y] using hy
  · have hSharp := hSharpAll u
    have hCap := mul_le_mul_of_nonneg_right hcCap hNonneg
    nlinarith

end
end AutoSamplingTheory.ExampleCases.ProximalBPS.RoughMeanGradient
