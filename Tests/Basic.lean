import AutoSamplingTheory
import AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence

open scoped ENNReal RealInnerProductSpace BigOperators

open AutoSamplingTheory
open MeasureTheory Filter Topology

example : literatureCount = 4 := rfl

example : automationTaskCount = 2 := rfl

example : threeLayerAgentContracts.length = 4 := rfl

example : SALD.saldExcludedFiles = ["sald_version_2.tex"] := rfl

example : SALD.firstFaithfulLabels.length = 10 := rfl

example : SALD.saldGronwallCandidateContract.status = ProofStatus.obligation := rfl

example : SALD.saldGronwallCandidateContract.mathlibRoute.length = 9 := rfl

example : SALD.saldLsiKlFiDensityTestContract.status = ProofStatus.obligation := rfl

example : SALD.saldLsiKlFiDensityTestContract.dependencies.length = 17 := rfl

example : SALD.cycle42DvVariationMiddleObligation.status = ProofStatus.obligation := rfl

example : SALD.cycle42DvVariationLowerObligation.status = ProofStatus.obligation := rfl

example : SALD.cycle43LsiKlFiUpperPacket.status = ProofStatus.obligation := rfl

example : SALD.cycle43LsiKlFiUpperObligation.status = ProofStatus.obligation := rfl

example : SALD.cycle43LsiKlFiMiddleObligation.status = ProofStatus.obligation := rfl

example : SALD.cycle43LsiKlFiLowerObligation.status = ProofStatus.obligation := rfl

example : SALD.saldStatusForLabel "lem:dv_variation" = ProofStatus.sourceCited := rfl

example : RMFLD.exploratorySeedLabels.length = 5 := rfl

example : openProblemCount = 1 := rfl

example : forbiddenProofPatterns.length = 5 := rfl

example : TechnicalLemmas.formalizedTechnicalLemmaCount = 430 := by native_decide

example (x : ℝ) :
    TechnicalLemmas.Analysis.Calculus.Cutoff.smoothUnitCutoff x =
      Real.smoothTransition (2 - |x|) :=
  TechnicalLemmas.Analysis.Calculus.Cutoff.smoothUnitCutoff_eq_smoothTransition x

example : ContDiff ℝ (⊤ : ℕ∞)
    TechnicalLemmas.Analysis.Calculus.Cutoff.smoothUnitCutoff :=
  TechnicalLemmas.Analysis.Calculus.Cutoff.smoothUnitCutoff_contDiff

example {x : ℝ} (hx : |x| ≤ 1) :
    TechnicalLemmas.Analysis.Calculus.Cutoff.smoothUnitCutoff x = 1 :=
  TechnicalLemmas.Analysis.Calculus.Cutoff.smoothUnitCutoff_eq_one_of_abs_le_one hx

example {x : ℝ} (hx : 2 ≤ |x|) :
    TechnicalLemmas.Analysis.Calculus.Cutoff.smoothUnitCutoff x = 0 :=
  TechnicalLemmas.Analysis.Calculus.Cutoff.smoothUnitCutoff_eq_zero_of_two_le_abs hx

example (x : ℝ) :
    TechnicalLemmas.Analysis.Calculus.Cutoff.smoothUnitCutoff x ∈ Set.Icc (0 : ℝ) 1 :=
  TechnicalLemmas.Analysis.Calculus.Cutoff.smoothUnitCutoff_mem_Icc x

example : ∃ C : ℝ, 0 < C ∧ ∀ x : ℝ,
    ‖deriv TechnicalLemmas.Analysis.Calculus.Cutoff.smoothUnitCutoff x‖ ≤ C :=
  TechnicalLemmas.Analysis.Calculus.Cutoff.smoothUnitCutoff_deriv_bounded

example : Continuous
    (deriv (deriv TechnicalLemmas.Analysis.Calculus.Cutoff.smoothUnitCutoff)) :=
  TechnicalLemmas.Analysis.Calculus.Cutoff.smoothUnitCutoff_secondDeriv_continuous

example : HasCompactSupport
    (deriv (deriv TechnicalLemmas.Analysis.Calculus.Cutoff.smoothUnitCutoff)) :=
  TechnicalLemmas.Analysis.Calculus.Cutoff.smoothUnitCutoff_secondDeriv_hasCompactSupport

example : ∃ C : ℝ, 0 < C ∧ ∀ x : ℝ,
    ‖deriv (deriv TechnicalLemmas.Analysis.Calculus.Cutoff.smoothUnitCutoff) x‖ ≤ C :=
  TechnicalLemmas.Analysis.Calculus.Cutoff.smoothUnitCutoff_secondDeriv_bounded

example {E : Type*} [NormedAddCommGroup E] {R : ℝ} (hR : 0 < R) {x : E}
    (hx : ‖x‖ ≤ R) :
    TechnicalLemmas.Analysis.Calculus.Cutoff.radialSmoothCutoff R x = 1 :=
  TechnicalLemmas.Analysis.Calculus.Cutoff.radialSmoothCutoff_eq_one_of_norm_le hR hx

example {E : Type*} [NormedAddCommGroup E] {R : ℝ} (hR : 0 < R) {x : E}
    (hx : 2 * R ≤ ‖x‖) :
    TechnicalLemmas.Analysis.Calculus.Cutoff.radialSmoothCutoff R x = 0 :=
  TechnicalLemmas.Analysis.Calculus.Cutoff.radialSmoothCutoff_eq_zero_of_two_mul_le_norm hR hx

example {E : Type*} [NormedAddCommGroup E] [NormedSpace ℝ E]
    {R : ℝ} (hR : 0 < R) (x : E) :
    ‖fderiv ℝ (fun y : E => ‖y‖ / R) x‖ ≤ 1 / R :=
  TechnicalLemmas.Analysis.Calculus.Cutoff.fderiv_norm_div_bound hR x

example {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    {R : ℝ} (hR : 0 < R) :
    ContDiff ℝ (⊤ : ℕ∞)
      (TechnicalLemmas.Analysis.Calculus.Cutoff.radialSmoothCutoff R : E → ℝ) :=
  TechnicalLemmas.Analysis.Calculus.Cutoff.radialSmoothCutoff_contDiff hR

example {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E] :
    ∃ C : ℝ, 0 < C ∧ ∀ R : ℝ, 0 < R → ∀ x : E,
      ‖fderiv ℝ
          (TechnicalLemmas.Analysis.Calculus.Cutoff.radialSmoothCutoff R : E → ℝ) x‖
        ≤ C / R :=
  TechnicalLemmas.Analysis.Calculus.Cutoff.radialSmoothCutoff_fderiv_bound

example {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [FiniteDimensional ℝ E] [Nontrivial E] :
    ∃ C : ℝ, 0 < C ∧ ∀ R : ℝ, 0 < R → ∀ x : E,
      ‖iteratedFDeriv ℝ 2
        (TechnicalLemmas.Analysis.Calculus.Cutoff.radialSmoothCutoff R : E → ℝ) x‖ ≤
          C / R ^ 2 :=
  TechnicalLemmas.Analysis.Calculus.Cutoff.radialSmoothCutoff_iteratedFDeriv_two_bound

example {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [FiniteDimensional ℝ E] (f : E → ℝ) (x : E) :
    ‖Laplacian.laplacian f x‖ ≤
      (Module.finrank ℝ E : ℝ) * ‖iteratedFDeriv ℝ 2 f x‖ :=
  TechnicalLemmas.Analysis.Calculus.Laplacian.norm_laplacian_le_finrank_mul_norm_iteratedFDeriv_two
    f x

example {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [FiniteDimensional ℝ E] [Nontrivial E] :
    ∃ C : ℝ, 0 < C ∧ ∀ R : ℝ, 0 < R → ∀ x : E,
      ‖Laplacian.laplacian
        (TechnicalLemmas.Analysis.Calculus.Cutoff.radialSmoothCutoff R : E → ℝ) x‖ ≤
          (Module.finrank ℝ E : ℝ) * (C / R ^ 2) :=
  TechnicalLemmas.Analysis.Calculus.Laplacian.radialSmoothCutoff_laplacian_bound

example {E : Type*} [NormedAddCommGroup E] [NormedSpace ℝ E]
    {R : ℝ} (hR : 0 < R) {x : E} (hx : 2 * R ≤ ‖x‖) :
    fderiv ℝ
        (TechnicalLemmas.Analysis.Calculus.Cutoff.radialSmoothCutoff R : E → ℝ) x = 0 :=
  TechnicalLemmas.Analysis.Calculus.Cutoff.radialSmoothCutoff_fderiv_eq_zero_of_two_mul_le_norm
    hR hx

example {E : Type*} [NormedAddCommGroup E] {R : ℝ} (hR : 0 < R) :
    tsupport (TechnicalLemmas.Analysis.Calculus.Cutoff.radialSmoothCutoff R : E → ℝ) ⊆
      Metric.closedBall 0 (2 * R) :=
  TechnicalLemmas.Analysis.Calculus.Cutoff.radialSmoothCutoff_tsupport_subset_closedBall hR

example {E : Type*} [NormedAddCommGroup E] [NormedSpace ℝ E]
    [FiniteDimensional ℝ E] {R : ℝ} (hR : 0 < R) :
    HasCompactSupport
      (TechnicalLemmas.Analysis.Calculus.Cutoff.radialSmoothCutoff R : E → ℝ) :=
  TechnicalLemmas.Analysis.Calculus.Cutoff.radialSmoothCutoff_hasCompactSupport hR

example {E : Type*} [NormedAddCommGroup E] (x : E) :
    Filter.Tendsto
      (fun R : ℝ => TechnicalLemmas.Analysis.Calculus.Cutoff.radialSmoothCutoff R x)
      Filter.atTop (nhds 1) :=
  TechnicalLemmas.Analysis.Calculus.Cutoff.radialSmoothCutoff_tendsto_one x

example {E : Type*} [NormedAddCommGroup E] [NormedSpace ℝ E]
    [FiniteDimensional ℝ E] {K U : Set E}
    (hK : IsCompact K) (hU : IsOpen U) (hKU : K ⊆ U) :
    ∃ χ : E → ℝ,
      Function.support χ ⊆ U ∧ tsupport χ ⊆ U ∧ HasCompactSupport χ ∧
        ContDiff ℝ (⊤ : ℕ∞) χ ∧ Set.range χ ⊆ Set.Icc 0 1 ∧
          Set.EqOn χ 1 K :=
  TechnicalLemmas.Analysis.Calculus.Cutoff.exists_contDiff_eq_one_tsupport_subset
    hK hU hKU

example {n : ℕ} {a b A B : Fin (n + 1) → ℝ}
    (hab : a ≤ b) (hA : ∀ i, A i < a i) (hB : ∀ i, b i < B i) :
    ∃ χ : (Fin (n + 1) → ℝ) → ℝ,
      Function.support χ ⊆ Set.univ.pi (fun i => Set.Ioo (A i) (B i)) ∧
      tsupport χ ⊆ Set.univ.pi (fun i => Set.Ioo (A i) (B i)) ∧
      HasCompactSupport χ ∧ ContDiff ℝ (⊤ : ℕ∞) χ ∧
      Set.range χ ⊆ Set.Icc 0 1 ∧ Set.EqOn χ 1 (Set.Icc a b) :=
  TechnicalLemmas.Analysis.Calculus.Divergence.exists_contDiff_cutoff_eq_one_on_Icc_tsupport_subset_outer_univ_pi_Ioo
    hab hA hB

example {n : ℕ} {Ω : Type*} [MeasurableSpace Ω]
    {μs : Fin n → MeasureTheory.Measure Ω}
    [∀ i, MeasureTheory.IsProbabilityMeasure (μs i)] (i : Fin n) :
    MeasureTheory.Measure.map (fun p : Ω × (Fin n → Ω) => Function.update p.2 i p.1)
      ((μs i).prod (MeasureTheory.Measure.pi μs)) =
        MeasureTheory.Measure.pi μs :=
  TechnicalLemmas.Measure.Product.map_update_prod_pi (μs := μs) i

example {n : ℕ} {Ω : Type*} [MeasurableSpace Ω]
    {μs : Fin n → MeasureTheory.Measure Ω}
    [∀ i, MeasureTheory.IsProbabilityMeasure (μs i)] (i : Fin n) :
    MeasureTheory.MeasurePreserving
      (fun p : Ω × (Fin n → Ω) => Function.update p.2 i p.1)
      ((μs i).prod (MeasureTheory.Measure.pi μs))
      (MeasureTheory.Measure.pi μs) :=
  TechnicalLemmas.Measure.Product.measurePreserving_update_prod_pi (μs := μs) i

example {n : ℕ} {Ω : Type*} [MeasurableSpace Ω]
    {μs : Fin n → MeasureTheory.Measure Ω}
    [∀ i, MeasureTheory.IsProbabilityMeasure (μs i)]
    (i : Fin n) {f : (Fin n → Ω) → ℝ}
    (hf : MeasureTheory.Integrable f (MeasureTheory.Measure.pi μs)) :
    ∫ y, ∫ x, f (Function.update x i y) ∂(MeasureTheory.Measure.pi μs) ∂(μs i) =
      ∫ z, f z ∂(MeasureTheory.Measure.pi μs) :=
  TechnicalLemmas.Measure.Product.integral_update_prod_pi_eq_integral
    (μs := μs) i hf

example {n : ℕ} {Ω : Type*} [MeasurableSpace Ω]
    {μs : Fin n → MeasureTheory.Measure Ω}
    [∀ i, MeasureTheory.IsProbabilityMeasure (μs i)]
    (i : Fin n) {f : (Fin n → Ω) → ℝ}
    (hf : MeasureTheory.Integrable f (MeasureTheory.Measure.pi μs)) :
    ∀ᵐ x ∂MeasureTheory.Measure.pi μs,
      MeasureTheory.Integrable (fun y => f (Function.update x i y)) (μs i) :=
  TechnicalLemmas.Measure.Product.integrable_update_slice_ae
    (μs := μs) i hf

example {ι : Type*} [Fintype ι] (u v : ι → ℝ) :
    inner ℝ (WithLp.toLp 2 u : EuclideanSpace ℝ ι)
        (WithLp.toLp 2 v : EuclideanSpace ℝ ι) =
      ∑ i, u i * v i :=
  TechnicalLemmas.Geometry.EuclideanSpaceCoordinates.euclideanSpace_inner_toLp_toLp_eq_sum_mul
    u v

example {ι : Type*} [Fintype ι] (u v : EuclideanSpace ℝ ι) :
    inner ℝ u v = ∑ i, u i * v i :=
  TechnicalLemmas.Geometry.EuclideanSpaceCoordinates.euclideanSpace_inner_eq_sum_mul
    u v

example {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [FiniteDimensional ℝ E] (f : E → ℝ) :
    Laplacian.laplacian f =
      fun x => ∑ i, iteratedFDeriv ℝ 2 f x
        ![(stdOrthonormalBasis ℝ E) i, (stdOrthonormalBasis ℝ E) i] :=
  TechnicalLemmas.Analysis.Calculus.Laplacian.laplacian_eq_sum_stdOrthonormalBasis
    f

example {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [FiniteDimensional ℝ E]
    (sourceLaplacianFunctional : (E → ℝ) → ℝ)
    (sourceTest : E → ℝ) :
    sourceLaplacianFunctional (Laplacian.laplacian sourceTest) =
      sourceLaplacianFunctional
        (fun x => ∑ i, iteratedFDeriv ℝ 2 sourceTest x
          ![(stdOrthonormalBasis ℝ E) i, (stdOrthonormalBasis ℝ E) i]) :=
  TechnicalLemmas.Analysis.Calculus.Laplacian.laplacianFunctional_eq_of_stdOrthonormalBasis_sum
    sourceLaplacianFunctional sourceTest

example {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [FiniteDimensional ℝ E]
    {f : E → ℝ} (hf : ContDiff ℝ 2 f) :
    Continuous (fun x : E => Laplacian.laplacian f x) :=
  TechnicalLemmas.Analysis.Calculus.Laplacian.continuous_laplacian_of_contDiff_two
    hf

example {ι : Type*} [Fintype ι] [DecidableEq ι]
    (F : EuclideanSpace ℝ ι → EuclideanSpace ℝ ι)
    (x : EuclideanSpace ℝ ι) :
    TechnicalLemmas.Analysis.Calculus.Divergence.coordinateDivergence F x =
      ∑ i, lineDeriv ℝ (fun y : EuclideanSpace ℝ ι => F y i) x
        (EuclideanSpace.single i (1 : ℝ)) :=
  TechnicalLemmas.Analysis.Calculus.Divergence.coordinateDivergence_eq_sum_lineDeriv
    F x

example {ι : Type*} [Fintype ι] [DecidableEq ι]
    {F : EuclideanSpace ℝ ι → EuclideanSpace ℝ ι}
    {F' : EuclideanSpace ℝ ι →L[ℝ] EuclideanSpace ℝ ι}
    {x : EuclideanSpace ℝ ι}
    (hF : HasFDerivAt F F' x) :
    TechnicalLemmas.Analysis.Calculus.Divergence.coordinateDivergence F x =
      ∑ i, F' (EuclideanSpace.single i (1 : ℝ)) i :=
  TechnicalLemmas.Analysis.Calculus.Divergence.coordinateDivergence_eq_sum_fderiv_apply_of_hasFDerivAt
    hF

example {ι : Type*} [Fintype ι] [DecidableEq ι]
    {F : EuclideanSpace ℝ ι → EuclideanSpace ℝ ι}
    {x : EuclideanSpace ℝ ι}
    (hF : DifferentiableAt ℝ F x) :
    TechnicalLemmas.Analysis.Calculus.Divergence.coordinateDivergence F x =
      ∑ i, fderiv ℝ F x (EuclideanSpace.single i (1 : ℝ)) i :=
  TechnicalLemmas.Analysis.Calculus.Divergence.coordinateDivergence_eq_sum_fderiv_apply_of_differentiableAt
    hF

example {ι : Type*} [Fintype ι] [DecidableEq ι] (i : ι) :
    (PiLp.continuousLinearEquiv 2 ℝ (fun _ : ι => ℝ))
      (EuclideanSpace.single i (1 : ℝ)) = Pi.single i (1 : ℝ) :=
  TechnicalLemmas.Analysis.Calculus.Divergence.continuousLinearEquiv_apply_euclideanSpace_single
    i

example {n : ℕ} {R : ℝ} (hR : 0 < R) (x : Fin (n + 1) → ℝ) :
    HasFDerivAt
      (fun z => TechnicalLemmas.Analysis.Calculus.Cutoff.radialSmoothCutoff R
        (WithLp.toLp 2 z : EuclideanSpace ℝ (Fin (n + 1))))
      ((fderiv ℝ
          (TechnicalLemmas.Analysis.Calculus.Cutoff.radialSmoothCutoff R :
            EuclideanSpace ℝ (Fin (n + 1)) → ℝ)
          (WithLp.toLp 2 x)).comp
        (PiLp.continuousLinearEquiv
          2 ℝ (fun _ : Fin (n + 1) => ℝ)).symm.toContinuousLinearMap)
      x :=
  TechnicalLemmas.Analysis.Calculus.Divergence.hasFDerivAt_radialSmoothCutoff_comp_toLp
    hR x

example {n : ℕ} {μ : Measure (Fin (n + 1) → ℝ)}
    {G : (Fin (n + 1) → ℝ) → Fin (n + 1) → ℝ}
    (hG : Integrable G μ) :
    Tendsto
      (fun R : ℝ =>
        ∫ x, ‖fderiv ℝ
          (fun z => TechnicalLemmas.Analysis.Calculus.Cutoff.radialSmoothCutoff R
            (WithLp.toLp 2 z : EuclideanSpace ℝ (Fin (n + 1))))
          x (G x)‖ ∂μ)
      atTop (𝓝 0) :=
  TechnicalLemmas.Analysis.Calculus.Divergence.tendsto_integral_norm_fderiv_radialSmoothCutoff_comp_toLp_apply
    hG

example {n : ℕ} {F : Type*} [NormedAddCommGroup F] [NormedSpace ℝ F]
    {μ : Measure (Fin (n + 1) → ℝ)}
    {H : (Fin (n + 1) → ℝ) → F}
    (hH : Integrable H μ) :
    Tendsto
      (fun R : ℝ =>
        ∫ x,
          TechnicalLemmas.Analysis.Calculus.Cutoff.radialSmoothCutoff R
            (WithLp.toLp 2 x : EuclideanSpace ℝ (Fin (n + 1))) • H x ∂μ)
      atTop (𝓝 (∫ x, H x ∂μ)) :=
  TechnicalLemmas.Analysis.Calculus.Divergence.tendsto_integral_radialSmoothCutoff_comp_toLp_smul
    hH

example {n : ℕ} {F : Type*} [NormedAddCommGroup F] [NormedSpace ℝ F]
    {μ : Measure (Fin (n + 1) → ℝ)}
    {H : (Fin (n + 1) → ℝ) → F}
    (hH : Integrable H μ) :
    Tendsto
      (fun R : ℝ => ∫ x in
        {x : Fin (n + 1) → ℝ |
          R ≤ ‖(WithLp.toLp 2 x : EuclideanSpace ℝ (Fin (n + 1)))‖},
        ‖H x‖ ∂μ)
      atTop (𝓝 0) :=
  TechnicalLemmas.Analysis.Calculus.Divergence.tendsto_setIntegral_norm_norm_ge_comp_toLp
    hH

example {ι : Type*} [Fintype ι] [DecidableEq ι]
    (χ' : (ι → ℝ) →L[ℝ] ℝ) (G : ι → ℝ) :
    ∑ i, ((χ'.smulRight G) (Pi.single i (1 : ℝ))) i = χ' G :=
  TechnicalLemmas.Analysis.Calculus.Divergence.sum_smulRight_apply_pi_single_eq_apply
    χ' G

example {ι : Type*} [Fintype ι] [DecidableEq ι]
    {F : (ι → ℝ) → ι → ℝ}
    {F' : (ι → ℝ) →L[ℝ] (ι → ℝ)}
    {x : ι → ℝ}
    (hF : HasFDerivAt F F' x) :
    TechnicalLemmas.Analysis.Calculus.Divergence.coordinateDivergence
        (fun y : EuclideanSpace ℝ ι =>
          (WithLp.toLp 2 (F (WithLp.ofLp y)) : EuclideanSpace ℝ ι))
        (WithLp.toLp 2 x : EuclideanSpace ℝ ι) =
      ∑ i, F' (Pi.single i (1 : ℝ)) i :=
  TechnicalLemmas.Analysis.Calculus.Divergence.coordinateDivergence_wrapped_toPi_trace_of_hasFDerivAt
    hF

example {n : ℕ} {β : Type*}
    {a b : Fin (n + 1) → ℝ}
    {f g : (Fin (n + 1) → ℝ) → β}
    {s : Set (Fin (n + 1) → ℝ)}
    (hs : s.Countable)
    (hfg : ∀ x ∈ (Set.univ.pi fun i => Set.Ioo (a i) (b i)) \ s, f x = g x) :
    f =ᵐ[MeasureTheory.volume.restrict (Set.Icc a b)] g :=
  TechnicalLemmas.Analysis.Calculus.Divergence.eventuallyEq_restrict_Icc_of_eqOn_univ_pi_Ioo_diff_countable
    hs hfg

example {n : ℕ}
    (a b : Fin (n + 1) → ℝ)
    (F : (Fin (n + 1) → ℝ) → Fin (n + 1) → ℝ)
    (F' : (Fin (n + 1) → ℝ) →
      (Fin (n + 1) → ℝ) →L[ℝ] (Fin (n + 1) → ℝ))
    (hF_ae : ∀ᵐ x ∂MeasureTheory.volume.restrict (Set.Icc a b),
      HasFDerivAt F (F' x) x) :
      (fun x => TechnicalLemmas.Analysis.Calculus.Divergence.coordinateDivergence
        (fun y : EuclideanSpace ℝ (Fin (n + 1)) =>
          (WithLp.toLp 2 (F (WithLp.ofLp y)) :
            EuclideanSpace ℝ (Fin (n + 1))))
        (WithLp.toLp 2 x : EuclideanSpace ℝ (Fin (n + 1))))
      =ᵐ[MeasureTheory.volume.restrict (Set.Icc a b)]
      fun x => ∑ i, F' x (Pi.single i (1 : ℝ)) i :=
  TechnicalLemmas.Analysis.Calculus.Divergence.coordinateDivergence_wrapped_toPi_trace_ae_of_ae_hasFDerivAt
    a b F F' hF_ae

example {n : ℕ}
    (a b : Fin (n + 1) → ℝ)
    (F : (Fin (n + 1) → ℝ) → Fin (n + 1) → ℝ)
    (F' : (Fin (n + 1) → ℝ) →
      (Fin (n + 1) → ℝ) →L[ℝ] (Fin (n + 1) → ℝ))
    (s : Set (Fin (n + 1) → ℝ)) (hs : s.Countable)
    (Hd : ∀ x ∈ (Set.univ.pi fun i => Set.Ioo (a i) (b i)) \ s,
      HasFDerivAt F (F' x) x) :
      (fun x => TechnicalLemmas.Analysis.Calculus.Divergence.coordinateDivergence
        (fun y : EuclideanSpace ℝ (Fin (n + 1)) =>
          (WithLp.toLp 2 (F (WithLp.ofLp y)) :
            EuclideanSpace ℝ (Fin (n + 1))))
        (WithLp.toLp 2 x : EuclideanSpace ℝ (Fin (n + 1))))
      =ᵐ[MeasureTheory.volume.restrict (Set.Icc a b)]
      fun x => ∑ i, F' x (Pi.single i (1 : ℝ)) i :=
  TechnicalLemmas.Analysis.Calculus.Divergence.coordinateDivergence_wrapped_toPi_trace_ae_of_hasFDerivAt_off_countable
    a b F F' s hs Hd

example {n : ℕ}
    (a b : Fin (n + 1) → ℝ)
    (F : (Fin (n + 1) → ℝ) → Fin (n + 1) → ℝ)
    (F' : (Fin (n + 1) → ℝ) →
      (Fin (n + 1) → ℝ) →L[ℝ] (Fin (n + 1) → ℝ))
    (s : Set (Fin (n + 1) → ℝ)) (hs : s.Countable)
    (Hd : ∀ x ∈ (Set.univ.pi fun i => Set.Ioo (a i) (b i)) \ s,
      HasFDerivAt F (F' x) x)
    (Hi_trace : MeasureTheory.IntegrableOn
      (fun x => ∑ i, F' x (Pi.single i (1 : ℝ)) i)
      (Set.Icc a b) MeasureTheory.volume) :
    MeasureTheory.IntegrableOn
      (fun x => TechnicalLemmas.Analysis.Calculus.Divergence.coordinateDivergence
        (fun y : EuclideanSpace ℝ (Fin (n + 1)) =>
          (WithLp.toLp 2 (F (WithLp.ofLp y)) :
            EuclideanSpace ℝ (Fin (n + 1))))
        (WithLp.toLp 2 x : EuclideanSpace ℝ (Fin (n + 1))))
      (Set.Icc a b) MeasureTheory.volume :=
  TechnicalLemmas.Analysis.Calculus.Divergence.integrableOn_coordinateDivergence_wrapped_of_integrableOn_trace_of_hasFDerivAt_off_countable
    a b F F' s hs Hd Hi_trace

example {n : ℕ}
    (a b : Fin (n + 1) → ℝ) (hle : a ≤ b)
    (F : (Fin (n + 1) → ℝ) → Fin (n + 1) → ℝ)
    (F' : (Fin (n + 1) → ℝ) →
      (Fin (n + 1) → ℝ) →L[ℝ] (Fin (n + 1) → ℝ))
    (s : Set (Fin (n + 1) → ℝ)) (hs : s.Countable)
    (Hc : ContinuousOn F (Set.Icc a b))
    (Hd : ∀ x ∈ (Set.univ.pi fun i => Set.Ioo (a i) (b i)) \ s,
      HasFDerivAt F (F' x) x)
    (Hi_trace : MeasureTheory.IntegrableOn
      (fun x => ∑ i, F' x (Pi.single i (1 : ℝ)) i)
      (Set.Icc a b) MeasureTheory.volume) :
    ∫ x in Set.Icc a b, TechnicalLemmas.Analysis.Calculus.Divergence.coordinateDivergence
        (fun y : EuclideanSpace ℝ (Fin (n + 1)) =>
          (WithLp.toLp 2 (F (WithLp.ofLp y)) :
            EuclideanSpace ℝ (Fin (n + 1))))
        (WithLp.toLp 2 x : EuclideanSpace ℝ (Fin (n + 1))) =
      ∑ i : Fin (n + 1),
        ((∫ x in Set.Icc (a ∘ i.succAbove) (b ∘ i.succAbove),
            F (i.insertNth (b i) x) i) -
          ∫ x in Set.Icc (a ∘ i.succAbove) (b ∘ i.succAbove),
            F (i.insertNth (a i) x) i) :=
  TechnicalLemmas.Analysis.Calculus.Divergence.integral_coordinateDivergence_toPi_box_of_integrableOn_trace_of_hasFDerivAt_off_countable
    a b hle F F' s hs Hc Hd Hi_trace

example {n : ℕ}
    (a b : Fin (n + 1) → ℝ) (hle : a ≤ b)
    (F : (Fin (n + 1) → ℝ) → Fin (n + 1) → ℝ)
    (F' : (Fin (n + 1) → ℝ) →
      (Fin (n + 1) → ℝ) →L[ℝ] (Fin (n + 1) → ℝ))
    (s : Set (Fin (n + 1) → ℝ)) (hs : s.Countable)
    (Hc : ContinuousOn F (Set.Icc a b))
    (Hd : ∀ x ∈ (Set.univ.pi fun i => Set.Ioo (a i) (b i)) \ s,
      HasFDerivAt F (F' x) x)
    (Hi_trace : MeasureTheory.IntegrableOn
      (fun x => ∑ i, F' x (Pi.single i (1 : ℝ)) i)
      (Set.Icc a b) MeasureTheory.volume)
    (hfaces :
      ∑ i : Fin (n + 1),
        ((∫ x in Set.Icc (a ∘ i.succAbove) (b ∘ i.succAbove),
            F (i.insertNth (b i) x) i) -
          ∫ x in Set.Icc (a ∘ i.succAbove) (b ∘ i.succAbove),
            F (i.insertNth (a i) x) i) = 0) :
    ∫ x in Set.Icc a b, TechnicalLemmas.Analysis.Calculus.Divergence.coordinateDivergence
        (fun y : EuclideanSpace ℝ (Fin (n + 1)) =>
          (WithLp.toLp 2 (F (WithLp.ofLp y)) :
            EuclideanSpace ℝ (Fin (n + 1))))
        (WithLp.toLp 2 x : EuclideanSpace ℝ (Fin (n + 1))) = 0 :=
  TechnicalLemmas.Analysis.Calculus.Divergence.integral_coordinateDivergence_toPi_box_eq_zero_of_integrableOn_trace_of_hasFDerivAt_off_countable
    a b hle F F' s hs Hc Hd Hi_trace hfaces

example {n : ℕ}
    (a b : Fin (n + 1) → ℝ)
    (F : (Fin (n + 1) → ℝ) → Fin (n + 1) → ℝ)
    (hupper : ∀ (i : Fin (n + 1)) (x : Fin n → ℝ),
      F (i.insertNth (b i) x) i = 0)
    (hlower : ∀ (i : Fin (n + 1)) (x : Fin n → ℝ),
      F (i.insertNth (a i) x) i = 0) :
    ∑ i : Fin (n + 1),
        ((∫ x in Set.Icc (a ∘ i.succAbove) (b ∘ i.succAbove),
            F (i.insertNth (b i) x) i) -
          ∫ x in Set.Icc (a ∘ i.succAbove) (b ∘ i.succAbove),
            F (i.insertNth (a i) x) i) = 0 :=
  TechnicalLemmas.Analysis.Calculus.Divergence.signedFaceTermSum_eq_zero_of_boundary_component_eq_zero
    a b F hupper hlower

example {n : ℕ}
    (a b : Fin (n + 1) → ℝ)
    (F : (Fin (n + 1) → ℝ) → Fin (n + 1) → ℝ)
    (hupper : ∀ (i : Fin (n + 1)) (x : Fin (n + 1) → ℝ),
      F (Function.update x i (b i)) i = 0)
    (hlower : ∀ (i : Fin (n + 1)) (x : Fin (n + 1) → ℝ),
      F (Function.update x i (a i)) i = 0) :
    ∑ i : Fin (n + 1),
        ((∫ x in Set.Icc (a ∘ i.succAbove) (b ∘ i.succAbove),
            F (i.insertNth (b i) x) i) -
          ∫ x in Set.Icc (a ∘ i.succAbove) (b ∘ i.succAbove),
            F (i.insertNth (a i) x) i) = 0 :=
  TechnicalLemmas.Analysis.Calculus.Divergence.signedFaceTermSum_eq_zero_of_update_boundary_component_eq_zero
    a b F hupper hlower

example {n : ℕ}
    (a b : Fin (n + 1) → ℝ)
    (F : (Fin (n + 1) → ℝ) → Fin (n + 1) → ℝ)
    (hoff : ∀ x ∉ (Set.univ.pi fun i => Set.Ioo (a i) (b i)), F x = 0) :
    (∀ (i : Fin (n + 1)) (x : Fin (n + 1) → ℝ),
        F (Function.update x i (b i)) i = 0) ∧
      (∀ (i : Fin (n + 1)) (x : Fin (n + 1) → ℝ),
        F (Function.update x i (a i)) i = 0) :=
  TechnicalLemmas.Analysis.Calculus.Divergence.update_boundary_component_eq_zero_of_eq_zero_off_univ_pi_Ioo
    a b F hoff

example {n : ℕ}
    (a b : Fin (n + 1) → ℝ)
    (F : (Fin (n + 1) → ℝ) → Fin (n + 1) → ℝ)
    (hoff : ∀ x ∉ (Set.univ.pi fun i => Set.Ioo (a i) (b i)), F x = 0) :
    ∑ i : Fin (n + 1),
        ((∫ x in Set.Icc (a ∘ i.succAbove) (b ∘ i.succAbove),
            F (i.insertNth (b i) x) i) -
          ∫ x in Set.Icc (a ∘ i.succAbove) (b ∘ i.succAbove),
            F (i.insertNth (a i) x) i) = 0 :=
  TechnicalLemmas.Analysis.Calculus.Divergence.signedFaceTermSum_eq_zero_of_eq_zero_off_univ_pi_Ioo
    a b F hoff

example {n : ℕ}
    (a b : Fin (n + 1) → ℝ) (hle : a ≤ b)
    (F : (Fin (n + 1) → ℝ) → Fin (n + 1) → ℝ)
    (F' : (Fin (n + 1) → ℝ) →
      (Fin (n + 1) → ℝ) →L[ℝ] (Fin (n + 1) → ℝ))
    (s : Set (Fin (n + 1) → ℝ)) (hs : s.Countable)
    (Hc : ContinuousOn F (Set.Icc a b))
    (Hd : ∀ x ∈ (Set.univ.pi fun i => Set.Ioo (a i) (b i)) \ s,
      HasFDerivAt F (F' x) x)
    (Hi_trace : MeasureTheory.IntegrableOn
      (fun x => ∑ i, F' x (Pi.single i (1 : ℝ)) i)
      (Set.Icc a b) MeasureTheory.volume)
    (hupper : ∀ (i : Fin (n + 1)) (x : Fin n → ℝ),
      F (i.insertNth (b i) x) i = 0)
    (hlower : ∀ (i : Fin (n + 1)) (x : Fin n → ℝ),
      F (i.insertNth (a i) x) i = 0) :
    ∫ x in Set.Icc a b, TechnicalLemmas.Analysis.Calculus.Divergence.coordinateDivergence
        (fun y : EuclideanSpace ℝ (Fin (n + 1)) =>
          (WithLp.toLp 2 (F (WithLp.ofLp y)) :
            EuclideanSpace ℝ (Fin (n + 1))))
        (WithLp.toLp 2 x : EuclideanSpace ℝ (Fin (n + 1))) = 0 :=
  TechnicalLemmas.Analysis.Calculus.Divergence.integral_coordinateDivergence_toPi_box_eq_zero_of_boundary_component_eq_zero
    a b hle F F' s hs Hc Hd Hi_trace hupper hlower

example {n : ℕ}
    (a b : Fin (n + 1) → ℝ) (hle : a ≤ b)
    (F : (Fin (n + 1) → ℝ) → Fin (n + 1) → ℝ)
    (F' : (Fin (n + 1) → ℝ) →
      (Fin (n + 1) → ℝ) →L[ℝ] (Fin (n + 1) → ℝ))
    (s : Set (Fin (n + 1) → ℝ)) (hs : s.Countable)
    (Hc : ContinuousOn F (Set.Icc a b))
    (Hd : ∀ x ∈ (Set.univ.pi fun i => Set.Ioo (a i) (b i)) \ s,
      HasFDerivAt F (F' x) x)
    (Hi_trace : MeasureTheory.IntegrableOn
      (fun x => ∑ i, F' x (Pi.single i (1 : ℝ)) i)
      (Set.Icc a b) MeasureTheory.volume)
    (hupper : ∀ (i : Fin (n + 1)) (x : Fin (n + 1) → ℝ),
      F (Function.update x i (b i)) i = 0)
    (hlower : ∀ (i : Fin (n + 1)) (x : Fin (n + 1) → ℝ),
      F (Function.update x i (a i)) i = 0) :
    ∫ x in Set.Icc a b, TechnicalLemmas.Analysis.Calculus.Divergence.coordinateDivergence
        (fun y : EuclideanSpace ℝ (Fin (n + 1)) =>
          (WithLp.toLp 2 (F (WithLp.ofLp y)) :
            EuclideanSpace ℝ (Fin (n + 1))))
        (WithLp.toLp 2 x : EuclideanSpace ℝ (Fin (n + 1))) = 0 :=
  TechnicalLemmas.Analysis.Calculus.Divergence.integral_coordinateDivergence_toPi_box_eq_zero_of_update_boundary_component_eq_zero
    a b hle F F' s hs Hc Hd Hi_trace hupper hlower

example {n : ℕ}
    (a b : Fin (n + 1) → ℝ) (hle : a ≤ b)
    (F : (Fin (n + 1) → ℝ) → Fin (n + 1) → ℝ)
    (F' : (Fin (n + 1) → ℝ) →
      (Fin (n + 1) → ℝ) →L[ℝ] (Fin (n + 1) → ℝ))
    (s : Set (Fin (n + 1) → ℝ)) (hs : s.Countable)
    (Hc : ContinuousOn F (Set.Icc a b))
    (Hd : ∀ x ∈ (Set.univ.pi fun i => Set.Ioo (a i) (b i)) \ s,
      HasFDerivAt F (F' x) x)
    (Hi_trace : MeasureTheory.IntegrableOn
      (fun x => ∑ i, F' x (Pi.single i (1 : ℝ)) i)
      (Set.Icc a b) MeasureTheory.volume)
    (hoff : ∀ x ∉ (Set.univ.pi fun i => Set.Ioo (a i) (b i)), F x = 0) :
    ∫ x in Set.Icc a b, TechnicalLemmas.Analysis.Calculus.Divergence.coordinateDivergence
        (fun y : EuclideanSpace ℝ (Fin (n + 1)) =>
          (WithLp.toLp 2 (F (WithLp.ofLp y)) :
            EuclideanSpace ℝ (Fin (n + 1))))
        (WithLp.toLp 2 x : EuclideanSpace ℝ (Fin (n + 1))) = 0 :=
  TechnicalLemmas.Analysis.Calculus.Divergence.integral_coordinateDivergence_toPi_box_eq_zero_of_eq_zero_off_univ_pi_Ioo
    a b hle F F' s hs Hc Hd Hi_trace hoff

example {n : ℕ}
    (a b : Fin (n + 1) → ℝ)
    (F : (Fin (n + 1) → ℝ) → Fin (n + 1) → ℝ)
    (hsupp : Function.support F ⊆ (Set.univ.pi fun i => Set.Ioo (a i) (b i))) :
    ∀ x ∉ (Set.univ.pi fun i => Set.Ioo (a i) (b i)), F x = 0 :=
  TechnicalLemmas.Analysis.Calculus.Divergence.eq_zero_off_univ_pi_Ioo_of_support_subset_univ_pi_Ioo
    a b F hsupp

example {n : ℕ} {a b x : Fin (n + 1) → ℝ}
    (hx : x ∈ Set.univ.pi fun i => Set.Ioo (a i) (b i)) :
    ∃ χ : (Fin (n + 1) → ℝ) → ℝ,
      tsupport χ ⊆ Set.univ.pi (fun i => Set.Ioo (a i) (b i)) ∧
      HasCompactSupport χ ∧
      ContDiff ℝ (⊤ : ℕ∞) χ ∧
      Set.range χ ⊆ Set.Icc 0 1 ∧
      χ x = 1 :=
  TechnicalLemmas.Analysis.Calculus.Divergence.exists_contDiff_cutoff_tsupport_subset_univ_pi_Ioo
    hx

example {n : ℕ} {a b : Fin (n + 1) → ℝ}
    {χ : (Fin (n + 1) → ℝ) → ℝ}
    (hχ : tsupport χ ⊆ Set.univ.pi (fun i => Set.Ioo (a i) (b i))) :
    Function.support χ ⊆ Set.univ.pi (fun i => Set.Ioo (a i) (b i)) :=
  TechnicalLemmas.Analysis.Calculus.Divergence.support_subset_univ_pi_Ioo_of_tsupport_subset_univ_pi_Ioo
    hχ

example {n : ℕ} {a b x : Fin (n + 1) → ℝ}
    (hx : x ∈ Set.univ.pi fun i => Set.Ioo (a i) (b i)) :
    ∃ χ : (Fin (n + 1) → ℝ) → ℝ,
      Function.support χ ⊆ Set.univ.pi (fun i => Set.Ioo (a i) (b i)) ∧
      tsupport χ ⊆ Set.univ.pi (fun i => Set.Ioo (a i) (b i)) ∧
      HasCompactSupport χ ∧
      ContDiff ℝ (⊤ : ℕ∞) χ ∧
      Set.range χ ⊆ Set.Icc 0 1 ∧
      χ x = 1 :=
  TechnicalLemmas.Analysis.Calculus.Divergence.exists_contDiff_cutoff_support_subset_univ_pi_Ioo
    hx

example {n : ℕ} (a b : Fin (n + 1) → ℝ) :
    ∃ χ : (Fin (n + 1) → ℝ) → ℝ,
      Function.support χ = Set.univ.pi (fun i => Set.Ioo (a i) (b i)) ∧
      ContDiff ℝ (⊤ : ℕ∞) χ ∧
      Set.range χ ⊆ Set.Icc 0 1 :=
  TechnicalLemmas.Analysis.Calculus.Divergence.exists_contDiff_support_eq_univ_pi_Ioo
    a b

example {n : ℕ} {a b : Fin (n + 1) → ℝ}
    {χ : (Fin (n + 1) → ℝ) → ℝ}
    (hχsupp : Function.support χ = Set.univ.pi (fun i => Set.Ioo (a i) (b i)))
    (hχrange : Set.range χ ⊆ Set.Icc 0 1)
    {x : Fin (n + 1) → ℝ}
    (hx : x ∈ Set.univ.pi (fun i => Set.Ioo (a i) (b i))) :
    0 < χ x :=
  TechnicalLemmas.Analysis.Calculus.Divergence.positive_on_univ_pi_Ioo_of_support_eq_univ_pi_Ioo
    hχsupp hχrange hx

example {n : ℕ} {a b A B : Fin (n + 1) → ℝ}
    (hA : ∀ i, A i < a i)
    (hB : ∀ i, b i < B i) :
    Set.Icc a b ⊆ Set.univ.pi (fun i => Set.Ioo (A i) (B i)) :=
  TechnicalLemmas.Analysis.Calculus.Divergence.Icc_subset_univ_pi_Ioo_of_strict_bounds
    hA hB

example {n : ℕ} {a b A B x : Fin (n + 1) → ℝ}
    (hA : ∀ i, A i < a i)
    (hB : ∀ i, b i < B i)
    (hx : x ∈ Set.Icc a b) :
    ∃ χ : (Fin (n + 1) → ℝ) → ℝ,
      Function.support χ ⊆ Set.univ.pi (fun i => Set.Ioo (A i) (B i)) ∧
      tsupport χ ⊆ Set.univ.pi (fun i => Set.Ioo (A i) (B i)) ∧
      HasCompactSupport χ ∧
      ContDiff ℝ (⊤ : ℕ∞) χ ∧
      Set.range χ ⊆ Set.Icc 0 1 ∧
      χ x = 1 :=
  TechnicalLemmas.Analysis.Calculus.Divergence.exists_contDiff_cutoff_support_subset_outer_univ_pi_Ioo_of_mem_Icc
    hA hB hx

example {n : ℕ}
    (a b : Fin (n + 1) → ℝ)
    (F : (Fin (n + 1) → ℝ) → Fin (n + 1) → ℝ)
    (hsupp : Function.support F ⊆ (Set.univ.pi fun i => Set.Ioo (a i) (b i))) :
    ∑ i : Fin (n + 1),
        ((∫ x in Set.Icc (a ∘ i.succAbove) (b ∘ i.succAbove),
            F (i.insertNth (b i) x) i) -
          ∫ x in Set.Icc (a ∘ i.succAbove) (b ∘ i.succAbove),
            F (i.insertNth (a i) x) i) = 0 :=
  TechnicalLemmas.Analysis.Calculus.Divergence.signedFaceTermSum_eq_zero_of_support_subset_univ_pi_Ioo
    a b F hsupp

example {n : ℕ}
    (a b : Fin (n + 1) → ℝ) (hle : a ≤ b)
    (F : (Fin (n + 1) → ℝ) → Fin (n + 1) → ℝ)
    (F' : (Fin (n + 1) → ℝ) →
      (Fin (n + 1) → ℝ) →L[ℝ] (Fin (n + 1) → ℝ))
    (s : Set (Fin (n + 1) → ℝ)) (hs : s.Countable)
    (Hc : ContinuousOn F (Set.Icc a b))
    (Hd : ∀ x ∈ (Set.univ.pi fun i => Set.Ioo (a i) (b i)) \ s,
      HasFDerivAt F (F' x) x)
    (Hi_trace : MeasureTheory.IntegrableOn
      (fun x => ∑ i, F' x (Pi.single i (1 : ℝ)) i)
      (Set.Icc a b) MeasureTheory.volume)
    (hsupp : Function.support F ⊆ (Set.univ.pi fun i => Set.Ioo (a i) (b i))) :
    ∫ x in Set.Icc a b, TechnicalLemmas.Analysis.Calculus.Divergence.coordinateDivergence
        (fun y : EuclideanSpace ℝ (Fin (n + 1)) =>
          (WithLp.toLp 2 (F (WithLp.ofLp y)) :
            EuclideanSpace ℝ (Fin (n + 1))))
        (WithLp.toLp 2 x : EuclideanSpace ℝ (Fin (n + 1))) = 0 :=
  TechnicalLemmas.Analysis.Calculus.Divergence.integral_coordinateDivergence_toPi_box_eq_zero_of_support_subset_univ_pi_Ioo
    a b hle F F' s hs Hc Hd Hi_trace hsupp

example {n : ℕ}
    (a b : Fin (n + 1) → ℝ)
    (χ : (Fin (n + 1) → ℝ) → ℝ)
    (G : (Fin (n + 1) → ℝ) → Fin (n + 1) → ℝ)
    (hχ : ∀ x ∉ (Set.univ.pi fun i => Set.Ioo (a i) (b i)), χ x = 0) :
    Function.support (fun x => χ x • G x) ⊆
      (Set.univ.pi fun i => Set.Ioo (a i) (b i)) :=
  TechnicalLemmas.Analysis.Calculus.Divergence.support_smul_subset_univ_pi_Ioo_of_eq_zero_off_univ_pi_Ioo
    a b χ G hχ

example {n : ℕ}
    (a b : Fin (n + 1) → ℝ)
    (χ : (Fin (n + 1) → ℝ) → ℝ)
    (G : (Fin (n + 1) → ℝ) → Fin (n + 1) → ℝ)
    (hχsupp : Function.support χ ⊆
      (Set.univ.pi fun i => Set.Ioo (a i) (b i))) :
    Function.support (fun x => χ x • G x) ⊆
      (Set.univ.pi fun i => Set.Ioo (a i) (b i)) :=
  TechnicalLemmas.Analysis.Calculus.Divergence.support_smul_subset_univ_pi_Ioo_of_scalar_support_subset_univ_pi_Ioo
    a b χ G hχsupp

example {n : ℕ}
    (a b : Fin (n + 1) → ℝ)
    (χ : (Fin (n + 1) → ℝ) → ℝ)
    (G : (Fin (n + 1) → ℝ) → Fin (n + 1) → ℝ)
    (hχtsupp : tsupport χ ⊆
      Set.univ.pi (fun i => Set.Ioo (a i) (b i))) :
    Function.support (fun x => χ x • G x) ⊆
      (Set.univ.pi fun i => Set.Ioo (a i) (b i)) :=
  TechnicalLemmas.Analysis.Calculus.Divergence.support_smul_subset_univ_pi_Ioo_of_scalar_tsupport_subset_univ_pi_Ioo
    a b χ G hχtsupp

example {n : ℕ}
    (a b : Fin (n + 1) → ℝ)
    (χ : (Fin (n + 1) → ℝ) → ℝ)
    (G : (Fin (n + 1) → ℝ) → Fin (n + 1) → ℝ)
    (hχ : ContinuousOn χ (Set.Icc a b))
    (hG : ContinuousOn G (Set.Icc a b)) :
    ContinuousOn (fun x => χ x • G x) (Set.Icc a b) :=
  TechnicalLemmas.Analysis.Calculus.Divergence.continuousOn_smul_vectorField_of_continuousOn
    a b χ G hχ hG

example {n : ℕ}
    (χ : (Fin (n + 1) → ℝ) → ℝ)
    (χ' : (Fin (n + 1) → ℝ) →L[ℝ] ℝ)
    (G : (Fin (n + 1) → ℝ) → Fin (n + 1) → ℝ)
    (G' : (Fin (n + 1) → ℝ) →L[ℝ] (Fin (n + 1) → ℝ))
    (x : Fin (n + 1) → ℝ)
    (hχ : HasFDerivAt χ χ' x)
    (hG : HasFDerivAt G G' x) :
    HasFDerivAt (fun y => χ y • G y)
      (χ x • G' + χ'.smulRight (G x)) x :=
  TechnicalLemmas.Analysis.Calculus.Divergence.hasFDerivAt_smul_vectorField_of_hasFDerivAt
    χ χ' G G' x hχ hG

example {n : ℕ}
    (a b : Fin (n + 1) → ℝ)
    (χ : (Fin (n + 1) → ℝ) → ℝ)
    (χ' : (Fin (n + 1) → ℝ) → (Fin (n + 1) → ℝ) →L[ℝ] ℝ)
    (G : (Fin (n + 1) → ℝ) → Fin (n + 1) → ℝ)
    (G' : (Fin (n + 1) → ℝ) →
      (Fin (n + 1) → ℝ) →L[ℝ] (Fin (n + 1) → ℝ))
    (s : Set (Fin (n + 1) → ℝ))
    (hχ : ∀ x ∈ (Set.univ.pi fun i => Set.Ioo (a i) (b i)) \ s,
      HasFDerivAt χ (χ' x) x)
    (hG : ∀ x ∈ (Set.univ.pi fun i => Set.Ioo (a i) (b i)) \ s,
      HasFDerivAt G (G' x) x) :
    ∀ x ∈ (Set.univ.pi fun i => Set.Ioo (a i) (b i)) \ s,
      HasFDerivAt (fun y => χ y • G y)
        (χ x • G' x + (χ' x).smulRight (G x)) x :=
  TechnicalLemmas.Analysis.Calculus.Divergence.hasFDerivAt_smul_vectorField_off_countable
    a b χ χ' G G' s hχ hG

example {n : ℕ}
    (a b : Fin (n + 1) → ℝ)
    (χ : (Fin (n + 1) → ℝ) → ℝ)
    (G : (Fin (n + 1) → ℝ) → Fin (n + 1) → ℝ)
    (hχ : ∀ x ∉ (Set.univ.pi fun i => Set.Ioo (a i) (b i)), χ x = 0) :
    ∑ i : Fin (n + 1),
        ((∫ x in Set.Icc (a ∘ i.succAbove) (b ∘ i.succAbove),
            (χ (i.insertNth (b i) x) • G (i.insertNth (b i) x)) i) -
          ∫ x in Set.Icc (a ∘ i.succAbove) (b ∘ i.succAbove),
            (χ (i.insertNth (a i) x) • G (i.insertNth (a i) x)) i) = 0 :=
  TechnicalLemmas.Analysis.Calculus.Divergence.signedFaceTermSum_smul_eq_zero_of_cutoff_eq_zero_off_univ_pi_Ioo
    a b χ G hχ

example {n : ℕ}
    (a b : Fin (n + 1) → ℝ)
    (χ : (Fin (n + 1) → ℝ) → ℝ)
    (G : (Fin (n + 1) → ℝ) → Fin (n + 1) → ℝ)
    (hχsupp : Function.support χ ⊆
      (Set.univ.pi fun i => Set.Ioo (a i) (b i))) :
    ∑ i : Fin (n + 1),
        ((∫ x in Set.Icc (a ∘ i.succAbove) (b ∘ i.succAbove),
            (χ (i.insertNth (b i) x) • G (i.insertNth (b i) x)) i) -
          ∫ x in Set.Icc (a ∘ i.succAbove) (b ∘ i.succAbove),
            (χ (i.insertNth (a i) x) • G (i.insertNth (a i) x)) i) = 0 :=
  TechnicalLemmas.Analysis.Calculus.Divergence.signedFaceTermSum_smul_eq_zero_of_scalar_support_subset_univ_pi_Ioo
    a b χ G hχsupp

example {n : ℕ}
    (a b : Fin (n + 1) → ℝ)
    (χ : (Fin (n + 1) → ℝ) → ℝ)
    (G : (Fin (n + 1) → ℝ) → Fin (n + 1) → ℝ)
    (hχtsupp : tsupport χ ⊆
      Set.univ.pi (fun i => Set.Ioo (a i) (b i))) :
    ∑ i : Fin (n + 1),
        ((∫ x in Set.Icc (a ∘ i.succAbove) (b ∘ i.succAbove),
            (χ (i.insertNth (b i) x) • G (i.insertNth (b i) x)) i) -
          ∫ x in Set.Icc (a ∘ i.succAbove) (b ∘ i.succAbove),
            (χ (i.insertNth (a i) x) • G (i.insertNth (a i) x)) i) = 0 :=
  TechnicalLemmas.Analysis.Calculus.Divergence.signedFaceTermSum_smul_eq_zero_of_scalar_tsupport_subset_univ_pi_Ioo
    a b χ G hχtsupp

example {n : ℕ}
    (a b : Fin (n + 1) → ℝ) (hle : a ≤ b)
    (χ : (Fin (n + 1) → ℝ) → ℝ)
    (G : (Fin (n + 1) → ℝ) → Fin (n + 1) → ℝ)
    (F' : (Fin (n + 1) → ℝ) →
      (Fin (n + 1) → ℝ) →L[ℝ] (Fin (n + 1) → ℝ))
    (s : Set (Fin (n + 1) → ℝ)) (hs : s.Countable)
    (Hc : ContinuousOn (fun x => χ x • G x) (Set.Icc a b))
    (Hd : ∀ x ∈ (Set.univ.pi fun i => Set.Ioo (a i) (b i)) \ s,
      HasFDerivAt (fun x => χ x • G x) (F' x) x)
    (Hi_trace : MeasureTheory.IntegrableOn
      (fun x => ∑ i, F' x (Pi.single i (1 : ℝ)) i)
      (Set.Icc a b) MeasureTheory.volume)
    (hχ : ∀ x ∉ (Set.univ.pi fun i => Set.Ioo (a i) (b i)), χ x = 0) :
    ∫ x in Set.Icc a b, TechnicalLemmas.Analysis.Calculus.Divergence.coordinateDivergence
        (fun y : EuclideanSpace ℝ (Fin (n + 1)) =>
          (WithLp.toLp 2 ((χ (WithLp.ofLp y)) • G (WithLp.ofLp y)) :
            EuclideanSpace ℝ (Fin (n + 1))))
        (WithLp.toLp 2 x : EuclideanSpace ℝ (Fin (n + 1))) = 0 :=
  TechnicalLemmas.Analysis.Calculus.Divergence.integral_coordinateDivergence_toPi_box_eq_zero_of_cutoff_eq_zero_off_univ_pi_Ioo
    a b hle χ G F' s hs Hc Hd Hi_trace hχ

example {n : ℕ}
    (a b : Fin (n + 1) → ℝ) (hle : a ≤ b)
    (χ : (Fin (n + 1) → ℝ) → ℝ)
    (G : (Fin (n + 1) → ℝ) → Fin (n + 1) → ℝ)
    (F' : (Fin (n + 1) → ℝ) →
      (Fin (n + 1) → ℝ) →L[ℝ] (Fin (n + 1) → ℝ))
    (s : Set (Fin (n + 1) → ℝ)) (hs : s.Countable)
    (Hc : ContinuousOn (fun x => χ x • G x) (Set.Icc a b))
    (Hd : ∀ x ∈ (Set.univ.pi fun i => Set.Ioo (a i) (b i)) \ s,
      HasFDerivAt (fun x => χ x • G x) (F' x) x)
    (Hi_trace : MeasureTheory.IntegrableOn
      (fun x => ∑ i, F' x (Pi.single i (1 : ℝ)) i)
      (Set.Icc a b) MeasureTheory.volume)
    (hχsupp : Function.support χ ⊆
      (Set.univ.pi fun i => Set.Ioo (a i) (b i))) :
    ∫ x in Set.Icc a b, TechnicalLemmas.Analysis.Calculus.Divergence.coordinateDivergence
        (fun y : EuclideanSpace ℝ (Fin (n + 1)) =>
          (WithLp.toLp 2 ((χ (WithLp.ofLp y)) • G (WithLp.ofLp y)) :
            EuclideanSpace ℝ (Fin (n + 1))))
        (WithLp.toLp 2 x : EuclideanSpace ℝ (Fin (n + 1))) = 0 :=
  TechnicalLemmas.Analysis.Calculus.Divergence.integral_coordinateDivergence_toPi_box_eq_zero_of_scalar_support_subset_univ_pi_Ioo
    a b hle χ G F' s hs Hc Hd Hi_trace hχsupp

example {n : ℕ}
    (a b : Fin (n + 1) → ℝ) (hle : a ≤ b)
    (χ : (Fin (n + 1) → ℝ) → ℝ)
    (G : (Fin (n + 1) → ℝ) → Fin (n + 1) → ℝ)
    (F' : (Fin (n + 1) → ℝ) →
      (Fin (n + 1) → ℝ) →L[ℝ] (Fin (n + 1) → ℝ))
    (s : Set (Fin (n + 1) → ℝ)) (hs : s.Countable)
    (Hc : ContinuousOn (fun x => χ x • G x) (Set.Icc a b))
    (Hd : ∀ x ∈ (Set.univ.pi fun i => Set.Ioo (a i) (b i)) \ s,
      HasFDerivAt (fun x => χ x • G x) (F' x) x)
    (Hi_trace : MeasureTheory.IntegrableOn
      (fun x => ∑ i, F' x (Pi.single i (1 : ℝ)) i)
      (Set.Icc a b) MeasureTheory.volume)
    (hχtsupp : tsupport χ ⊆
      Set.univ.pi (fun i => Set.Ioo (a i) (b i))) :
    ∫ x in Set.Icc a b, TechnicalLemmas.Analysis.Calculus.Divergence.coordinateDivergence
        (fun y : EuclideanSpace ℝ (Fin (n + 1)) =>
          (WithLp.toLp 2 ((χ (WithLp.ofLp y)) • G (WithLp.ofLp y)) :
            EuclideanSpace ℝ (Fin (n + 1))))
        (WithLp.toLp 2 x : EuclideanSpace ℝ (Fin (n + 1))) = 0 :=
  TechnicalLemmas.Analysis.Calculus.Divergence.integral_coordinateDivergence_toPi_box_eq_zero_of_scalar_tsupport_subset_univ_pi_Ioo
    a b hle χ G F' s hs Hc Hd Hi_trace hχtsupp

example {n : ℕ}
    (a b : Fin (n + 1) → ℝ) (hle : a ≤ b)
    (χ : (Fin (n + 1) → ℝ) → ℝ)
    (χ' : (Fin (n + 1) → ℝ) → (Fin (n + 1) → ℝ) →L[ℝ] ℝ)
    (G : (Fin (n + 1) → ℝ) → Fin (n + 1) → ℝ)
    (G' : (Fin (n + 1) → ℝ) →
      (Fin (n + 1) → ℝ) →L[ℝ] (Fin (n + 1) → ℝ))
    (s : Set (Fin (n + 1) → ℝ)) (hs : s.Countable)
    (hχc : ContinuousOn χ (Set.Icc a b))
    (hGc : ContinuousOn G (Set.Icc a b))
    (hχd : ∀ x ∈ (Set.univ.pi fun i => Set.Ioo (a i) (b i)) \ s,
      HasFDerivAt χ (χ' x) x)
    (hGd : ∀ x ∈ (Set.univ.pi fun i => Set.Ioo (a i) (b i)) \ s,
      HasFDerivAt G (G' x) x)
    (Hi_trace : MeasureTheory.IntegrableOn
      (fun x => ∑ i, ((χ x • G' x + (χ' x).smulRight (G x))
        (Pi.single i (1 : ℝ))) i)
      (Set.Icc a b) MeasureTheory.volume)
    (hχzero : ∀ x ∉ (Set.univ.pi fun i => Set.Ioo (a i) (b i)), χ x = 0) :
    ∫ x in Set.Icc a b, TechnicalLemmas.Analysis.Calculus.Divergence.coordinateDivergence
        (fun y : EuclideanSpace ℝ (Fin (n + 1)) =>
          (WithLp.toLp 2 ((χ (WithLp.ofLp y)) • G (WithLp.ofLp y)) :
            EuclideanSpace ℝ (Fin (n + 1))))
        (WithLp.toLp 2 x : EuclideanSpace ℝ (Fin (n + 1))) = 0 :=
  TechnicalLemmas.Analysis.Calculus.Divergence.integral_coordinateDivergence_toPi_box_eq_zero_of_cutoff_eq_zero_off_univ_pi_Ioo_of_regularity
    a b hle χ χ' G G' s hs hχc hGc hχd hGd Hi_trace hχzero

example {n : ℕ}
    (a b : Fin (n + 1) → ℝ) (hle : a ≤ b)
    (χ : (Fin (n + 1) → ℝ) → ℝ)
    (χ' : (Fin (n + 1) → ℝ) → (Fin (n + 1) → ℝ) →L[ℝ] ℝ)
    (G : (Fin (n + 1) → ℝ) → Fin (n + 1) → ℝ)
    (G' : (Fin (n + 1) → ℝ) →
      (Fin (n + 1) → ℝ) →L[ℝ] (Fin (n + 1) → ℝ))
    (s : Set (Fin (n + 1) → ℝ)) (hs : s.Countable)
    (hχc : ContinuousOn χ (Set.Icc a b))
    (hGc : ContinuousOn G (Set.Icc a b))
    (hχd : ∀ x ∈ (Set.univ.pi fun i => Set.Ioo (a i) (b i)) \ s,
      HasFDerivAt χ (χ' x) x)
    (hGd : ∀ x ∈ (Set.univ.pi fun i => Set.Ioo (a i) (b i)) \ s,
      HasFDerivAt G (G' x) x)
    (Hi_trace : MeasureTheory.IntegrableOn
      (fun x => ∑ i, ((χ x • G' x + (χ' x).smulRight (G x))
        (Pi.single i (1 : ℝ))) i)
      (Set.Icc a b) MeasureTheory.volume)
    (hχsupp : Function.support χ ⊆
      (Set.univ.pi fun i => Set.Ioo (a i) (b i))) :
    ∫ x in Set.Icc a b, TechnicalLemmas.Analysis.Calculus.Divergence.coordinateDivergence
        (fun y : EuclideanSpace ℝ (Fin (n + 1)) =>
          (WithLp.toLp 2 ((χ (WithLp.ofLp y)) • G (WithLp.ofLp y)) :
            EuclideanSpace ℝ (Fin (n + 1))))
        (WithLp.toLp 2 x : EuclideanSpace ℝ (Fin (n + 1))) = 0 :=
  TechnicalLemmas.Analysis.Calculus.Divergence.integral_coordinateDivergence_toPi_box_eq_zero_of_scalar_support_subset_univ_pi_Ioo_of_regularity
    a b hle χ χ' G G' s hs hχc hGc hχd hGd Hi_trace hχsupp

example {n : ℕ}
    (a b : Fin (n + 1) → ℝ) (hle : a ≤ b)
    (χ : (Fin (n + 1) → ℝ) → ℝ)
    (χ' : (Fin (n + 1) → ℝ) → (Fin (n + 1) → ℝ) →L[ℝ] ℝ)
    (G : (Fin (n + 1) → ℝ) → Fin (n + 1) → ℝ)
    (s : Set (Fin (n + 1) → ℝ)) (hs : s.Countable)
    (hχc : ContinuousOn χ (Set.Icc a b))
    (hGc : ContinuousOn G (Set.Icc a b))
    (hχd : ∀ x ∈ (Set.univ.pi fun i => Set.Ioo (a i) (b i)) \ s,
      HasFDerivAt χ (χ' x) x)
    (hGd : ∀ x ∈ (Set.univ.pi fun i => Set.Ioo (a i) (b i)) \ s,
      DifferentiableAt ℝ G x)
    (Hi_trace : MeasureTheory.IntegrableOn
      (fun x => ∑ i, ((χ x • fderiv ℝ G x + (χ' x).smulRight (G x))
        (Pi.single i (1 : ℝ))) i)
      (Set.Icc a b) MeasureTheory.volume)
    (hχsupp : Function.support χ ⊆
      (Set.univ.pi fun i => Set.Ioo (a i) (b i))) :
    ∫ x in Set.Icc a b, TechnicalLemmas.Analysis.Calculus.Divergence.coordinateDivergence
        (fun y : EuclideanSpace ℝ (Fin (n + 1)) =>
          (WithLp.toLp 2 ((χ (WithLp.ofLp y)) • G (WithLp.ofLp y)) :
            EuclideanSpace ℝ (Fin (n + 1))))
        (WithLp.toLp 2 x : EuclideanSpace ℝ (Fin (n + 1))) = 0 :=
  TechnicalLemmas.Analysis.Calculus.Divergence.integral_coordinateDivergence_toPi_box_eq_zero_of_scalar_support_subset_univ_pi_Ioo_of_fderiv
    a b hle χ χ' G s hs hχc hGc hχd hGd Hi_trace hχsupp

example {n : ℕ}
    (a b : Fin (n + 1) → ℝ)
    (χ : (Fin (n + 1) → ℝ) → ℝ)
    (χ' : (Fin (n + 1) → ℝ) → (Fin (n + 1) → ℝ) →L[ℝ] ℝ)
    (G : (Fin (n + 1) → ℝ) → Fin (n + 1) → ℝ)
    (G' : (Fin (n + 1) → ℝ) →
      (Fin (n + 1) → ℝ) →L[ℝ] (Fin (n + 1) → ℝ))
    (htrace : ContinuousOn
      (fun x => ∑ i, ((χ x • G' x + (χ' x).smulRight (G x))
        (Pi.single i (1 : ℝ))) i)
      (Set.Icc a b)) :
    MeasureTheory.IntegrableOn
      (fun x => ∑ i, ((χ x • G' x + (χ' x).smulRight (G x))
        (Pi.single i (1 : ℝ))) i)
      (Set.Icc a b) MeasureTheory.volume :=
  TechnicalLemmas.Analysis.Calculus.Divergence.integrableOn_smul_vectorField_trace_of_continuousOn
    a b χ χ' G G' htrace

example {n : ℕ}
    (a b : Fin (n + 1) → ℝ) (hle : a ≤ b)
    (χ : (Fin (n + 1) → ℝ) → ℝ)
    (χ' : (Fin (n + 1) → ℝ) → (Fin (n + 1) → ℝ) →L[ℝ] ℝ)
    (G : (Fin (n + 1) → ℝ) → Fin (n + 1) → ℝ)
    (G' : (Fin (n + 1) → ℝ) →
      (Fin (n + 1) → ℝ) →L[ℝ] (Fin (n + 1) → ℝ))
    (s : Set (Fin (n + 1) → ℝ)) (hs : s.Countable)
    (hχc : ContinuousOn χ (Set.Icc a b))
    (hGc : ContinuousOn G (Set.Icc a b))
    (hχd : ∀ x ∈ (Set.univ.pi fun i => Set.Ioo (a i) (b i)) \ s,
      HasFDerivAt χ (χ' x) x)
    (hGd : ∀ x ∈ (Set.univ.pi fun i => Set.Ioo (a i) (b i)) \ s,
      HasFDerivAt G (G' x) x)
    (htrace : ContinuousOn
      (fun x => ∑ i, ((χ x • G' x + (χ' x).smulRight (G x))
        (Pi.single i (1 : ℝ))) i)
      (Set.Icc a b))
    (hχzero : ∀ x ∉ (Set.univ.pi fun i => Set.Ioo (a i) (b i)), χ x = 0) :
    ∫ x in Set.Icc a b, TechnicalLemmas.Analysis.Calculus.Divergence.coordinateDivergence
        (fun y : EuclideanSpace ℝ (Fin (n + 1)) =>
          (WithLp.toLp 2 ((χ (WithLp.ofLp y)) • G (WithLp.ofLp y)) :
            EuclideanSpace ℝ (Fin (n + 1))))
        (WithLp.toLp 2 x : EuclideanSpace ℝ (Fin (n + 1))) = 0 :=
  TechnicalLemmas.Analysis.Calculus.Divergence.integral_coordinateDivergence_toPi_box_eq_zero_of_cutoff_eq_zero_off_univ_pi_Ioo_of_trace_continuous
    a b hle χ χ' G G' s hs hχc hGc hχd hGd htrace hχzero

example {n : ℕ}
    (a b : Fin (n + 1) → ℝ) (hle : a ≤ b)
    (χ : (Fin (n + 1) → ℝ) → ℝ)
    (χ' : (Fin (n + 1) → ℝ) → (Fin (n + 1) → ℝ) →L[ℝ] ℝ)
    (G : (Fin (n + 1) → ℝ) → Fin (n + 1) → ℝ)
    (G' : (Fin (n + 1) → ℝ) →
      (Fin (n + 1) → ℝ) →L[ℝ] (Fin (n + 1) → ℝ))
    (s : Set (Fin (n + 1) → ℝ)) (hs : s.Countable)
    (hχc : ContinuousOn χ (Set.Icc a b))
    (hGc : ContinuousOn G (Set.Icc a b))
    (hχd : ∀ x ∈ (Set.univ.pi fun i => Set.Ioo (a i) (b i)) \ s,
      HasFDerivAt χ (χ' x) x)
    (hGd : ∀ x ∈ (Set.univ.pi fun i => Set.Ioo (a i) (b i)) \ s,
      HasFDerivAt G (G' x) x)
    (htrace : ContinuousOn
      (fun x => ∑ i, ((χ x • G' x + (χ' x).smulRight (G x))
        (Pi.single i (1 : ℝ))) i)
      (Set.Icc a b))
    (hχsupp : Function.support χ ⊆
      (Set.univ.pi fun i => Set.Ioo (a i) (b i))) :
    ∫ x in Set.Icc a b, TechnicalLemmas.Analysis.Calculus.Divergence.coordinateDivergence
        (fun y : EuclideanSpace ℝ (Fin (n + 1)) =>
          (WithLp.toLp 2 ((χ (WithLp.ofLp y)) • G (WithLp.ofLp y)) :
            EuclideanSpace ℝ (Fin (n + 1))))
        (WithLp.toLp 2 x : EuclideanSpace ℝ (Fin (n + 1))) = 0 :=
  TechnicalLemmas.Analysis.Calculus.Divergence.integral_coordinateDivergence_toPi_box_eq_zero_of_scalar_support_subset_univ_pi_Ioo_of_trace_continuous
    a b hle χ χ' G G' s hs hχc hGc hχd hGd htrace hχsupp

example {n : ℕ}
    (a b : Fin (n + 1) → ℝ)
    (χ : (Fin (n + 1) → ℝ) → ℝ)
    (χ' : (Fin (n + 1) → ℝ) → (Fin (n + 1) → ℝ) →L[ℝ] ℝ)
    (G : (Fin (n + 1) → ℝ) → Fin (n + 1) → ℝ)
    (G' : (Fin (n + 1) → ℝ) →
      (Fin (n + 1) → ℝ) →L[ℝ] (Fin (n + 1) → ℝ))
    (hχ : ContinuousOn χ (Set.Icc a b))
    (hG : ∀ i, ContinuousOn (fun x => G x i) (Set.Icc a b))
    (hχ' : ∀ i, ContinuousOn
      (fun x => χ' x (Pi.single i (1 : ℝ))) (Set.Icc a b))
    (hG' : ∀ i, ContinuousOn
      (fun x => (G' x (Pi.single i (1 : ℝ))) i) (Set.Icc a b)) :
    ContinuousOn
      (fun x => ∑ i, ((χ x • G' x + (χ' x).smulRight (G x))
        (Pi.single i (1 : ℝ))) i)
      (Set.Icc a b) :=
  TechnicalLemmas.Analysis.Calculus.Divergence.continuousOn_smul_vectorField_trace_of_component_continuousOn
    a b χ χ' G G' hχ hG hχ' hG'

example {n : ℕ}
    (a b : Fin (n + 1) → ℝ)
    (χ : (Fin (n + 1) → ℝ) → ℝ)
    (χ' : (Fin (n + 1) → ℝ) → (Fin (n + 1) → ℝ) →L[ℝ] ℝ)
    (G : (Fin (n + 1) → ℝ) → Fin (n + 1) → ℝ)
    (G' : (Fin (n + 1) → ℝ) →
      (Fin (n + 1) → ℝ) →L[ℝ] (Fin (n + 1) → ℝ))
    (hχc : ContinuousOn χ (Set.Icc a b))
    (hχ'c : ContinuousOn χ' (Set.Icc a b))
    (hGc : ContinuousOn G (Set.Icc a b))
    (hG'c : ContinuousOn G' (Set.Icc a b)) :
    ContinuousOn
      (fun x => ∑ i, ((χ x • G' x + (χ' x).smulRight (G x))
        (Pi.single i (1 : ℝ))) i)
      (Set.Icc a b) :=
  TechnicalLemmas.Analysis.Calculus.Divergence.continuousOn_smul_vectorField_trace_of_components
    a b χ χ' G G' hχc hχ'c hGc hG'c

example {n : ℕ}
    (a b : Fin (n + 1) → ℝ) (hle : a ≤ b)
    (χ : (Fin (n + 1) → ℝ) → ℝ)
    (χ' : (Fin (n + 1) → ℝ) → (Fin (n + 1) → ℝ) →L[ℝ] ℝ)
    (G : (Fin (n + 1) → ℝ) → Fin (n + 1) → ℝ)
    (G' : (Fin (n + 1) → ℝ) →
      (Fin (n + 1) → ℝ) →L[ℝ] (Fin (n + 1) → ℝ))
    (s : Set (Fin (n + 1) → ℝ)) (hs : s.Countable)
    (hχc : ContinuousOn χ (Set.Icc a b))
    (hGc : ContinuousOn G (Set.Icc a b))
    (hχ'c : ∀ i, ContinuousOn
      (fun x => χ' x (Pi.single i (1 : ℝ))) (Set.Icc a b))
    (hG'c : ∀ i, ContinuousOn
      (fun x => (G' x (Pi.single i (1 : ℝ))) i) (Set.Icc a b))
    (hχd : ∀ x ∈ (Set.univ.pi fun i => Set.Ioo (a i) (b i)) \ s,
      HasFDerivAt χ (χ' x) x)
    (hGd : ∀ x ∈ (Set.univ.pi fun i => Set.Ioo (a i) (b i)) \ s,
      HasFDerivAt G (G' x) x)
    (hχzero : ∀ x ∉ (Set.univ.pi fun i => Set.Ioo (a i) (b i)), χ x = 0) :
    ∫ x in Set.Icc a b, TechnicalLemmas.Analysis.Calculus.Divergence.coordinateDivergence
        (fun y : EuclideanSpace ℝ (Fin (n + 1)) =>
          (WithLp.toLp 2 ((χ (WithLp.ofLp y)) • G (WithLp.ofLp y)) :
            EuclideanSpace ℝ (Fin (n + 1))))
        (WithLp.toLp 2 x : EuclideanSpace ℝ (Fin (n + 1))) = 0 :=
  TechnicalLemmas.Analysis.Calculus.Divergence.integral_coordinateDivergence_toPi_box_eq_zero_of_cutoff_eq_zero_off_univ_pi_Ioo_of_component_continuous
    a b hle χ χ' G G' s hs hχc hGc hχ'c hG'c hχd hGd hχzero

example {n : ℕ}
    (a b : Fin (n + 1) → ℝ) (hle : a ≤ b)
    (χ : (Fin (n + 1) → ℝ) → ℝ)
    (χ' : (Fin (n + 1) → ℝ) → (Fin (n + 1) → ℝ) →L[ℝ] ℝ)
    (G : (Fin (n + 1) → ℝ) → Fin (n + 1) → ℝ)
    (G' : (Fin (n + 1) → ℝ) →
      (Fin (n + 1) → ℝ) →L[ℝ] (Fin (n + 1) → ℝ))
    (s : Set (Fin (n + 1) → ℝ)) (hs : s.Countable)
    (hχc : ContinuousOn χ (Set.Icc a b))
    (hGc : ContinuousOn G (Set.Icc a b))
    (hχ'c : ∀ i, ContinuousOn
      (fun x => χ' x (Pi.single i (1 : ℝ))) (Set.Icc a b))
    (hG'c : ∀ i, ContinuousOn
      (fun x => (G' x (Pi.single i (1 : ℝ))) i) (Set.Icc a b))
    (hχd : ∀ x ∈ (Set.univ.pi fun i => Set.Ioo (a i) (b i)) \ s,
      HasFDerivAt χ (χ' x) x)
    (hGd : ∀ x ∈ (Set.univ.pi fun i => Set.Ioo (a i) (b i)) \ s,
      HasFDerivAt G (G' x) x)
    (hχsupp : Function.support χ ⊆
      (Set.univ.pi fun i => Set.Ioo (a i) (b i))) :
    ∫ x in Set.Icc a b, TechnicalLemmas.Analysis.Calculus.Divergence.coordinateDivergence
        (fun y : EuclideanSpace ℝ (Fin (n + 1)) =>
          (WithLp.toLp 2 ((χ (WithLp.ofLp y)) • G (WithLp.ofLp y)) :
            EuclideanSpace ℝ (Fin (n + 1))))
        (WithLp.toLp 2 x : EuclideanSpace ℝ (Fin (n + 1))) = 0 :=
  TechnicalLemmas.Analysis.Calculus.Divergence.integral_coordinateDivergence_toPi_box_eq_zero_of_scalar_support_subset_univ_pi_Ioo_of_component_continuous
    a b hle χ χ' G G' s hs hχc hGc hχ'c hG'c hχd hGd hχsupp

example {n : ℕ}
    (a b : Fin (n + 1) → ℝ) (hle : a ≤ b)
    (F : (Fin (n + 1) → ℝ) → Fin (n + 1) → ℝ)
    (F' : (Fin (n + 1) → ℝ) →
      (Fin (n + 1) → ℝ) →L[ℝ] (Fin (n + 1) → ℝ))
    (s : Set (Fin (n + 1) → ℝ)) (hs : s.Countable)
    (Hc : ContinuousOn F (Set.Icc a b))
    (Hd : ∀ x ∈ (Set.univ.pi fun i => Set.Ioo (a i) (b i)) \ s,
      HasFDerivAt F (F' x) x)
    (hdiv_ae :
      (fun x => TechnicalLemmas.Analysis.Calculus.Divergence.coordinateDivergence
        (fun y : EuclideanSpace ℝ (Fin (n + 1)) =>
          (WithLp.toLp 2 (F (WithLp.ofLp y)) :
            EuclideanSpace ℝ (Fin (n + 1))))
        (WithLp.toLp 2 x : EuclideanSpace ℝ (Fin (n + 1))))
      =ᵐ[MeasureTheory.volume.restrict (Set.Icc a b)]
      fun x => ∑ i, F' x (Pi.single i (1 : ℝ)) i)
    (Hi : MeasureTheory.IntegrableOn
      (fun x => TechnicalLemmas.Analysis.Calculus.Divergence.coordinateDivergence
        (fun y : EuclideanSpace ℝ (Fin (n + 1)) =>
          (WithLp.toLp 2 (F (WithLp.ofLp y)) :
            EuclideanSpace ℝ (Fin (n + 1))))
        (WithLp.toLp 2 x : EuclideanSpace ℝ (Fin (n + 1))))
      (Set.Icc a b) MeasureTheory.volume) :
    ∫ x in Set.Icc a b, TechnicalLemmas.Analysis.Calculus.Divergence.coordinateDivergence
        (fun y : EuclideanSpace ℝ (Fin (n + 1)) =>
          (WithLp.toLp 2 (F (WithLp.ofLp y)) :
            EuclideanSpace ℝ (Fin (n + 1))))
        (WithLp.toLp 2 x : EuclideanSpace ℝ (Fin (n + 1))) =
      ∑ i : Fin (n + 1),
        ((∫ x in Set.Icc (a ∘ i.succAbove) (b ∘ i.succAbove),
            F (i.insertNth (b i) x) i) -
          ∫ x in Set.Icc (a ∘ i.succAbove) (b ∘ i.succAbove),
            F (i.insertNth (a i) x) i) :=
  TechnicalLemmas.Analysis.Calculus.Divergence.integral_coordinateDivergence_toPi_box_of_hasFDerivAt_off_countable
    a b hle F F' s hs Hc Hd hdiv_ae Hi

example {F : Type*} [NormedAddCommGroup F] [InnerProductSpace ℝ F] [CompleteSpace F]
    {V : F → ℝ} {x gradV : F}
    (hV : HasGradientAt V gradV x) :
    HasGradientAt
      (fun y : F => Real.exp (-V y))
      (-(Real.exp (-V x)) • gradV)
      x :=
  TechnicalLemmas.Analysis.Calculus.Gradient.hasGradientAt_expNegPotential_of_hasGradientAt
    hV

example {F : Type*} [NormedAddCommGroup F] [InnerProductSpace ℝ F] [CompleteSpace F]
    {V : F → ℝ} {x gradV : F}
    (hV : HasGradientAt V gradV x) :
    gradient (fun y : F => Real.exp (-V y)) x =
      -(Real.exp (-V x)) • gradV :=
  TechnicalLemmas.Analysis.Calculus.Gradient.gradient_expNegPotential_eq_of_hasGradientAt
    hV

example {ι : Type*} [Fintype ι]
    {V : EuclideanSpace ℝ ι → ℝ} {x gradV : EuclideanSpace ℝ ι}
    (hV : HasGradientAt V gradV x) (i : ι) :
    (gradient (fun y : EuclideanSpace ℝ ι => Real.exp (-V y)) x) i =
      -Real.exp (-V x) * gradV i :=
  TechnicalLemmas.Analysis.Calculus.Gradient.gradient_expNegPotential_coordinate_eq_of_hasGradientAt
    hV i

example {F : Type*} [NormedAddCommGroup F] [InnerProductSpace ℝ F] [CompleteSpace F]
    {V : F → ℝ} {x : F}
    (hV : DifferentiableAt ℝ V x) :
    gradient (fun y : F => Real.exp (-V y)) x =
      -(Real.exp (-V x)) • gradient V x :=
  TechnicalLemmas.Analysis.Calculus.Gradient.gradient_expNegPotential_eq_of_differentiableAt
    hV

example {ι : Type*} [Fintype ι]
    {V : EuclideanSpace ℝ ι → ℝ} {x : EuclideanSpace ℝ ι}
    (hV : DifferentiableAt ℝ V x) (i : ι) :
    (gradient (fun y : EuclideanSpace ℝ ι => Real.exp (-V y)) x) i =
      -Real.exp (-V x) * (gradient V x) i :=
  TechnicalLemmas.Analysis.Calculus.Gradient.gradient_expNegPotential_coordinate_eq_of_differentiableAt
    hV i

example {F : Type*} [NormedAddCommGroup F] [InnerProductSpace ℝ F] [CompleteSpace F]
    {f : F → ℝ} (hf : ContDiff ℝ 1 f) :
    Continuous (fun x : F => gradient f x) :=
  TechnicalLemmas.Analysis.Calculus.Gradient.continuous_gradient_of_contDiff_one
    hf

example {ι : Type*} [Fintype ι] [DecidableEq ι]
    {f : EuclideanSpace ℝ ι → ℝ}
    {x grad : EuclideanSpace ℝ ι}
    (hf : HasGradientAt f grad x) (i : ι) :
    HasLineDerivAt ℝ f (grad i) x
      (WithLp.toLp 2 (Pi.single i (1 : ℝ)) : EuclideanSpace ℝ ι) :=
  TechnicalLemmas.Analysis.Calculus.Gradient.hasGradientAt_coordinateUnit_hasLineDerivAt
    hf i

example {F : Type*} [NormedAddCommGroup F] [InnerProductSpace ℝ F] [CompleteSpace F]
    {f : F → ℝ} {x grad v : F}
    (hf : HasGradientAt f grad x) :
    fderiv ℝ f x v = inner ℝ grad v :=
  TechnicalLemmas.Analysis.Calculus.Gradient.fderiv_apply_eq_inner_of_hasGradientAt
    hf

example {F : Type*} [NormedAddCommGroup F] [InnerProductSpace ℝ F] [CompleteSpace F]
    {f : F → ℝ} {x v : F}
    (hf : DifferentiableAt ℝ f x) :
    fderiv ℝ f x v = inner ℝ (gradient f x) v :=
  TechnicalLemmas.Analysis.Calculus.Gradient.fderiv_apply_eq_inner_gradient_of_differentiableAt
    hf

example {ι : Type*} [Fintype ι] [DecidableEq ι]
    {f : EuclideanSpace ℝ ι → ℝ} {x : EuclideanSpace ℝ ι} (i : ι)
    (hf : DifferentiableAt ℝ f x) :
    fderiv ℝ f x (EuclideanSpace.single i (1 : ℝ)) = (gradient f x) i :=
  TechnicalLemmas.Analysis.Calculus.Gradient.fderiv_apply_coordinate_eq_gradient_coordinate_of_differentiableAt
    i hf

example {𝕜 : Type*} [NontriviallyNormedField 𝕜]
    {E : Type*} [AddCommGroup E] [Module 𝕜 E]
    {𝔸 : Type*} [NormedRing 𝔸] [NormedAlgebra 𝕜 𝔸]
    {f g : E → 𝔸} {x v : E} {f' g' : 𝔸}
    (hf : HasLineDerivAt 𝕜 f f' x v)
    (hg : HasLineDerivAt 𝕜 g g' x v) :
    HasLineDerivAt 𝕜 (fun y : E => f y * g y)
      (f' * g x + f x * g') x v :=
  TechnicalLemmas.Analysis.Calculus.LineDeriv.hasLineDerivAt_mul
    hf hg

example {E : Type*} [AddCommGroup E] [Module ℝ E]
    {rho g : E → ℝ} {x v : E} {rho' g' : ℝ}
    (hrho : HasLineDerivAt ℝ rho rho' x v)
    (hg : HasLineDerivAt ℝ g g' x v) :
    HasLineDerivAt ℝ (fun y : E => rho y * g y)
      (rho x * g' + rho' * g x) x v :=
  TechnicalLemmas.Analysis.Calculus.LineDeriv.hasLineDerivAt_rho_mul
    hrho hg

example {E : Type*} [AddCommGroup E] [Module ℝ E]
    {rho g : E → ℝ} {x v : E} {rho' g' : ℝ}
    (hrho : HasLineDerivAt ℝ rho rho' x v)
    (hg : HasLineDerivAt ℝ g g' x v) :
    lineDeriv ℝ (fun y : E => rho y * g y) x v =
      rho x * g' + rho' * g x :=
  TechnicalLemmas.Analysis.Calculus.LineDeriv.lineDeriv_rho_mul_eq_of_hasLineDerivAt
    hrho hg

example {ι : Type*} [Fintype ι] [DecidableEq ι]
    {V g : EuclideanSpace ℝ ι → ℝ} {x : EuclideanSpace ℝ ι}
    {g' : ℝ} (i : ι)
    (hV : DifferentiableAt ℝ V x)
    (hg : HasLineDerivAt ℝ g g' x
      (WithLp.toLp 2 (Pi.single i (1 : ℝ)) : EuclideanSpace ℝ ι)) :
    lineDeriv ℝ
        (fun y : EuclideanSpace ℝ ι => Real.exp (-V y) * g y)
        x
        (WithLp.toLp 2 (Pi.single i (1 : ℝ)) : EuclideanSpace ℝ ι) =
      Real.exp (-V x) * g' - Real.exp (-V x) * (gradient V x) i * g x :=
  TechnicalLemmas.Analysis.Calculus.LineDeriv.lineDeriv_expNegPotential_mul_eq_of_differentiableAt
    i hV hg

example {E : Type*} [NormedAddCommGroup E] [NormedSpace ℝ E]
    {f : E → ℝ} {x w v : E} {A : E →L[ℝ] E →L[ℝ] ℝ}
    (hf : HasFDerivAt (fun y : E => fderiv ℝ f y) A x) :
    HasLineDerivAt ℝ (fun y : E => fderiv ℝ f y v) (A w v) x w :=
  TechnicalLemmas.Analysis.Calculus.LineDeriv.hasLineDerivAt_fderiv_apply_const_of_hasFDerivAt_fderiv
    hf

example {E : Type*} [NormedAddCommGroup E] [NormedSpace ℝ E]
    {f : E → ℝ} {x w v : E} {A : E →L[ℝ] E →L[ℝ] ℝ}
    (hf : HasFDerivAt (fun y : E => fderiv ℝ f y) A x) :
    lineDeriv ℝ (fun y : E => fderiv ℝ f y v) x w = A w v :=
  TechnicalLemmas.Analysis.Calculus.LineDeriv.lineDeriv_fderiv_apply_const_eq_of_hasFDerivAt_fderiv
    hf

example {E : Type*} [NormedAddCommGroup E] [NormedSpace ℝ E]
    {f : E → ℝ} {x w v : E}
    (hf : DifferentiableAt ℝ (fun y : E => fderiv ℝ f y) x) :
    lineDeriv ℝ (fun y : E => fderiv ℝ f y v) x w =
      iteratedFDeriv ℝ 2 f x ![w, v] :=
  TechnicalLemmas.Analysis.Calculus.LineDeriv.lineDeriv_fderiv_apply_const_eq_iteratedFDeriv_two
    hf

example {ι : Type*} [Fintype ι] [DecidableEq ι]
    {f : EuclideanSpace ℝ ι → ℝ} {x : EuclideanSpace ℝ ι} (i : ι)
    (hf : DifferentiableAt ℝ
      (fun y : EuclideanSpace ℝ ι => fderiv ℝ f y) x) :
    lineDeriv ℝ
        (fun y : EuclideanSpace ℝ ι =>
          fderiv ℝ f y
            (WithLp.toLp 2 (Pi.single i (1 : ℝ)) : EuclideanSpace ℝ ι))
        x
        (WithLp.toLp 2 (Pi.single i (1 : ℝ)) : EuclideanSpace ℝ ι) =
      iteratedFDeriv ℝ 2 f x
        ![(WithLp.toLp 2 (Pi.single i (1 : ℝ)) : EuclideanSpace ℝ ι),
          (WithLp.toLp 2 (Pi.single i (1 : ℝ)) : EuclideanSpace ℝ ι)] :=
  TechnicalLemmas.Analysis.Calculus.LineDeriv.lineDeriv_fderiv_apply_coordinate_eq_iteratedFDeriv_two
    i hf

example {ι : Type*} [Fintype ι] [DecidableEq ι]
    {V f : EuclideanSpace ℝ ι → ℝ} {x : EuclideanSpace ℝ ι} (i : ι)
    (hV : DifferentiableAt ℝ V x)
    (hf : DifferentiableAt ℝ
      (fun y : EuclideanSpace ℝ ι => fderiv ℝ f y) x) :
    lineDeriv ℝ
        (fun y : EuclideanSpace ℝ ι =>
          Real.exp (-V y) *
            fderiv ℝ f y
              (WithLp.toLp 2 (Pi.single i (1 : ℝ)) : EuclideanSpace ℝ ι))
        x
        (WithLp.toLp 2 (Pi.single i (1 : ℝ)) : EuclideanSpace ℝ ι) =
      Real.exp (-V x) *
          iteratedFDeriv ℝ 2 f x
            ![(WithLp.toLp 2 (Pi.single i (1 : ℝ)) : EuclideanSpace ℝ ι),
              (WithLp.toLp 2 (Pi.single i (1 : ℝ)) : EuclideanSpace ℝ ι)] -
        Real.exp (-V x) * (gradient V x) i *
          fderiv ℝ f x
            (WithLp.toLp 2 (Pi.single i (1 : ℝ)) : EuclideanSpace ℝ ι) :=
  TechnicalLemmas.Analysis.Calculus.LineDeriv.lineDeriv_expNegPotential_mul_fderiv_coordinate_eq
    i hV hf

example :
    MeasureTheory.Integrable
      (fun x : ℝ => Real.exp (-(2 : ℝ) * ‖x‖ ^ 2))
      MeasureTheory.volume :=
  TechnicalLemmas.Analysis.Integrability.integrable_exp_neg_mul_norm_sq
    (E := ℝ) (a := 2) (by norm_num)

example :
    ∫⁻ x : ℝ, ENNReal.ofReal (Real.exp (-(2 : ℝ) * ‖x‖ ^ 2))
        ∂(MeasureTheory.volume : MeasureTheory.Measure ℝ) =
      ENNReal.ofReal ((Real.pi / (2 : ℝ)) ^ ((Module.finrank ℝ ℝ : ℝ) / 2)) :=
  TechnicalLemmas.Analysis.Integrability.lintegral_exp_neg_mul_norm_sq_eq
    (E := ℝ) (a := 2) (by norm_num)

example :
    MeasureTheory.Integrable
      (fun x : ℝ => Real.exp (-((2 : ℝ) * ‖x - 3‖ ^ 2 + 1)))
      MeasureTheory.volume :=
  TechnicalLemmas.Analysis.Integrability.integrable_exp_neg_add_mul_norm_sub_sq
    (E := ℝ) (a := 2) (b := 1) (3 : ℝ) (by norm_num)

example :
    MeasureTheory.Integrable
      (fun x : ℝ => Real.exp (-((2 : ℝ) * |x| + 1)))
      MeasureTheory.volume :=
  TechnicalLemmas.Analysis.Integrability.integrable_exp_neg_add_mul_abs
    (a := 2) (b := 1) (by norm_num)

example :
    ∫ x : ℝ, Real.exp (-((2 : ℝ) * |x| + 1)) ∂MeasureTheory.volume =
      2 * Real.exp (-(1 : ℝ)) / 2 :=
  TechnicalLemmas.Analysis.Integrability.integral_exp_neg_add_mul_abs_eq
    (a := 2) (b := 1) (by norm_num)

example :
    ∫⁻ x : ℝ, ENNReal.ofReal (Real.exp (-((2 : ℝ) * ‖x - 3‖ ^ 2 + 1)))
        ∂(MeasureTheory.volume : MeasureTheory.Measure ℝ) =
      ENNReal.ofReal (Real.exp (-(1 : ℝ)) *
        (Real.pi / (2 : ℝ)) ^ ((Module.finrank ℝ ℝ : ℝ) / 2)) :=
  TechnicalLemmas.Analysis.Integrability.lintegral_exp_neg_add_mul_norm_sub_sq_eq
    (E := ℝ) (a := 2) (b := 1) (3 : ℝ) (by norm_num)

example :
    ∫⁻ x : ℝ, ENNReal.ofReal (Real.exp (-((2 : ℝ) * |x| + 1)))
        ∂(MeasureTheory.volume : MeasureTheory.Measure ℝ) ≠ ∞ :=
  TechnicalLemmas.Analysis.Integrability.lintegral_exp_neg_add_mul_abs_ne_top
    (a := 2) (b := 1) (by norm_num)

example :
    ∫⁻ x : ℝ, ENNReal.ofReal (Real.exp (-((2 : ℝ) * |x| + 1)))
        ∂(MeasureTheory.volume : MeasureTheory.Measure ℝ) =
      ENNReal.ofReal (2 * Real.exp (-(1 : ℝ)) / 2) :=
  TechnicalLemmas.Analysis.Integrability.lintegral_exp_neg_add_mul_abs_eq
    (a := 2) (b := 1) (by norm_num)

example :
    MeasureTheory.IsProbabilityMeasure
      ((MeasureTheory.volume : MeasureTheory.Measure ℝ).withDensity fun x =>
        (ENNReal.ofReal
          (Real.exp (-(0 : ℝ)) *
            (Real.pi / (1 : ℝ)) ^ ((Module.finrank ℝ ℝ : ℝ) / 2)))⁻¹ *
          ENNReal.ofReal (Real.exp (-((1 : ℝ) * ‖x‖ ^ 2 + 0)))) :=
  TechnicalLemmas.Analysis.Integrability.isProbabilityMeasure_withDensity_exp_neg_add_mul_norm_sq
    (E := ℝ) (a := 1) (b := 0) (by norm_num)

example :
    MeasureTheory.IsProbabilityMeasure
      ((MeasureTheory.volume : MeasureTheory.Measure ℝ).withDensity fun x =>
        (ENNReal.ofReal
          (Real.exp (-(0 : ℝ)) *
            (Real.pi / (1 : ℝ)) ^ ((Module.finrank ℝ ℝ : ℝ) / 2)))⁻¹ *
          ENNReal.ofReal (Real.exp (-((1 : ℝ) * ‖x - 3‖ ^ 2 + 0)))) :=
  TechnicalLemmas.Analysis.Integrability.isProbabilityMeasure_withDensity_exp_neg_add_mul_norm_sub_sq
    (E := ℝ) (a := 1) (b := 0) (3 : ℝ) (by norm_num)

example :
    MeasureTheory.IsProbabilityMeasure
      ((MeasureTheory.volume : MeasureTheory.Measure ℝ).withDensity fun x =>
        (ENNReal.ofReal (2 * Real.exp (-(0 : ℝ)) / 1))⁻¹ *
          ENNReal.ofReal (Real.exp (-((1 : ℝ) * |x| + 0)))) :=
  TechnicalLemmas.Analysis.Integrability.isProbabilityMeasure_withDensity_exp_neg_add_mul_abs
    (a := 1) (b := 0) (by norm_num)

example :
    ∫⁻ x : ℝ, TechnicalLemmas.Measure.Gibbs.gibbsDensityENNReal
      (fun z : ℝ => ‖z‖ ^ 2) x ∂(MeasureTheory.volume : MeasureTheory.Measure ℝ) ≠ ∞ :=
  TechnicalLemmas.Analysis.Integrability.lintegral_gibbsDensityENNReal_ne_top_of_ae_quadratic_lower_bound
    (E := ℝ) (V := fun z : ℝ => ‖z‖ ^ 2) (a := 1) (b := 0)
    (by norm_num)
    (by simp)

example :
    ∫⁻ x : ℝ, TechnicalLemmas.Measure.Gibbs.gibbsDensityENNReal
      (fun z : ℝ => ‖z - 3‖ ^ 2) x ∂(MeasureTheory.volume : MeasureTheory.Measure ℝ) ≠ ∞ :=
  TechnicalLemmas.Analysis.Integrability.lintegral_gibbsDensityENNReal_ne_top_of_ae_centered_quadratic_lower_bound
    (E := ℝ) (V := fun z : ℝ => ‖z - 3‖ ^ 2) (a := 1) (b := 0)
    (3 : ℝ)
    (by norm_num)
    (by simp)

example :
    ∫⁻ x : ℝ, TechnicalLemmas.Measure.Gibbs.gibbsDensityENNReal
      (fun z : ℝ => |z|) x ∂(MeasureTheory.volume : MeasureTheory.Measure ℝ) ≠ ∞ :=
  TechnicalLemmas.Analysis.Integrability.lintegral_gibbsDensityENNReal_ne_top_of_ae_abs_linear_lower_bound
    (V := fun z : ℝ => |z|) (a := 1) (b := 0)
    (by norm_num)
    (by simp)

example :
    TechnicalLemmas.Geometry.LogConcavity.LogConcaveOn (Set.univ : Set ℝ)
      (fun x : ℝ =>
        ((ENNReal.ofReal (2 : ℝ))⁻¹ *
          TechnicalLemmas.Measure.Gibbs.gibbsDensityENNReal (fun z : ℝ => |z|) x).toReal) :=
  TechnicalLemmas.Measure.GibbsLogConcavity.logConcaveOn_normalized_gibbsDensityENNReal_toReal_of_convexOn
    (TechnicalLemmas.Geometry.LogConcavity.convexOn_univ_abs)
    (by norm_num)
    (by simp)

example :
    TechnicalLemmas.Geometry.LogConcavity.LogConcaveOn (Set.univ : Set ℝ)
      (fun x : ℝ =>
        ((∫⁻ y, TechnicalLemmas.Measure.Gibbs.gibbsDensityENNReal
          (fun z : ℝ => |z|) y ∂(MeasureTheory.volume : MeasureTheory.Measure ℝ))⁻¹ *
          TechnicalLemmas.Measure.Gibbs.gibbsDensityENNReal (fun z : ℝ => |z|) x).toReal) :=
  TechnicalLemmas.Measure.GibbsLogConcavity.logConcaveOn_lintegral_normalized_gibbsDensityENNReal_toReal_of_convexOn
    (MeasureTheory.volume : MeasureTheory.Measure ℝ)
    (TechnicalLemmas.Geometry.LogConcavity.convexOn_univ_abs)
    (TechnicalLemmas.Measure.Gibbs.lintegral_gibbsDensityENNReal_ne_zero
      (MeasureTheory.volume : MeasureTheory.Measure ℝ) (by fun_prop))
    (TechnicalLemmas.Analysis.Integrability.lintegral_gibbsDensityENNReal_ne_top_of_ae_abs_linear_lower_bound
      (V := fun z : ℝ => |z|) (a := 1) (b := 0) (by norm_num) (by simp))

example :
    TechnicalLemmas.Geometry.LogConcavity.LogConcaveOn (Set.univ : Set ℝ)
      (fun x : ℝ =>
        ((ENNReal.ofReal (2 * Real.exp (-(0 : ℝ)) / 1))⁻¹ *
          TechnicalLemmas.Measure.Gibbs.gibbsDensityENNReal
            (fun y : ℝ => (1 : ℝ) * |y| + 0) x).toReal) :=
  TechnicalLemmas.Measure.GibbsLogConcavity.logConcaveOn_normalized_laplace_gibbsDensityENNReal_toReal
    (a := 1) (b := 0) (by norm_num)

example :
    MeasureTheory.IsProbabilityMeasure
      ((MeasureTheory.volume : MeasureTheory.Measure ℝ).withDensity fun x =>
        (∫⁻ y, TechnicalLemmas.Measure.Gibbs.gibbsDensityENNReal
          (fun z : ℝ => ‖z‖ ^ 2) y ∂(MeasureTheory.volume : MeasureTheory.Measure ℝ))⁻¹ *
          TechnicalLemmas.Measure.Gibbs.gibbsDensityENNReal
            (fun z : ℝ => ‖z‖ ^ 2) x) :=
  TechnicalLemmas.Analysis.Integrability.isProbabilityMeasure_withDensity_normalized_gibbs_of_ae_quadratic_lower_bound
    (E := ℝ) (V := fun z : ℝ => ‖z‖ ^ 2) (a := 1) (b := 0)
    (by fun_prop)
    (by norm_num)
    (by simp)

example :
    MeasureTheory.IsProbabilityMeasure
      ((MeasureTheory.volume : MeasureTheory.Measure ℝ).withDensity fun x =>
        (∫⁻ y, TechnicalLemmas.Measure.Gibbs.gibbsDensityENNReal
          (fun z : ℝ => ‖z - 3‖ ^ 2) y ∂(MeasureTheory.volume : MeasureTheory.Measure ℝ))⁻¹ *
          TechnicalLemmas.Measure.Gibbs.gibbsDensityENNReal
            (fun z : ℝ => ‖z - 3‖ ^ 2) x) :=
  TechnicalLemmas.Analysis.Integrability.isProbabilityMeasure_withDensity_normalized_gibbs_of_ae_centered_quadratic_lower_bound
    (E := ℝ) (V := fun z : ℝ => ‖z - 3‖ ^ 2) (a := 1) (b := 0)
    (3 : ℝ)
    (by fun_prop)
    (by norm_num)
    (by simp)

example :
    MeasureTheory.IsProbabilityMeasure
      ((MeasureTheory.volume : MeasureTheory.Measure ℝ).withDensity fun x =>
        (∫⁻ y, TechnicalLemmas.Measure.Gibbs.gibbsDensityENNReal
          (fun z : ℝ => |z|) y ∂(MeasureTheory.volume : MeasureTheory.Measure ℝ))⁻¹ *
          TechnicalLemmas.Measure.Gibbs.gibbsDensityENNReal
            (fun z : ℝ => |z|) x) :=
  TechnicalLemmas.Analysis.Integrability.isProbabilityMeasure_withDensity_normalized_gibbs_of_ae_abs_linear_lower_bound
    (V := fun z : ℝ => |z|) (a := 1) (b := 0)
    (by fun_prop)
    (by norm_num)
    (by simp)

example (g : ℝ → ℝ) :
    ∫ x, g x ∂(MeasureTheory.volume : MeasureTheory.Measure ℝ).withDensity
        (fun x =>
          (ENNReal.ofReal (2 : ℝ))⁻¹ *
            TechnicalLemmas.Measure.Gibbs.gibbsDensityENNReal (fun z : ℝ => |z|) x) =
      ∫ x, ((ENNReal.ofReal (2 : ℝ)).toReal⁻¹ * Real.exp (-|x|)) • g x
        ∂(MeasureTheory.volume : MeasureTheory.Measure ℝ) :=
  TechnicalLemmas.Measure.GibbsIntegral.integral_withDensity_inv_mul_gibbsDensityENNReal_eq_integral_inv_mul_exp_smul
    (MeasureTheory.volume : MeasureTheory.Measure ℝ)
    (V := fun z : ℝ => |z|)
    (by fun_prop)
    (by norm_num)
    g

example {V : ℝ → ℝ}
    (hV : AEMeasurable V (MeasureTheory.volume : MeasureTheory.Measure ℝ))
    {Z : ℝ≥0∞} (hZ0 : Z ≠ 0) (g : ℝ → ℝ) :
    ∫ x, g x ∂(MeasureTheory.volume : MeasureTheory.Measure ℝ).withDensity
        (fun x => Z⁻¹ * TechnicalLemmas.Measure.Gibbs.gibbsDensityENNReal V x) =
      ∫ x, (Z.toReal⁻¹ * Real.exp (-V x)) • g x
        ∂(MeasureTheory.volume : MeasureTheory.Measure ℝ) :=
  TechnicalLemmas.Measure.GibbsIntegral.integral_withDensity_inv_mul_gibbsDensityENNReal_eq_integral_inv_mul_exp_smul
    (MeasureTheory.volume : MeasureTheory.Measure ℝ) hV hZ0 g

example {V : ℝ → ℝ}
    (hV : AEMeasurable V (MeasureTheory.volume : MeasureTheory.Measure ℝ))
    (hZ0 :
      ∫⁻ y, TechnicalLemmas.Measure.Gibbs.gibbsDensityENNReal V y
        ∂(MeasureTheory.volume : MeasureTheory.Measure ℝ) ≠ 0)
    (g : ℝ → ℝ) :
    ∫ x, g x ∂(MeasureTheory.volume : MeasureTheory.Measure ℝ).withDensity
        (fun x =>
          (∫⁻ y, TechnicalLemmas.Measure.Gibbs.gibbsDensityENNReal V y
            ∂(MeasureTheory.volume : MeasureTheory.Measure ℝ))⁻¹ *
            TechnicalLemmas.Measure.Gibbs.gibbsDensityENNReal V x) =
      ∫ x,
        ((∫⁻ y, TechnicalLemmas.Measure.Gibbs.gibbsDensityENNReal V y
          ∂(MeasureTheory.volume : MeasureTheory.Measure ℝ)).toReal⁻¹ *
          Real.exp (-V x)) • g x
        ∂(MeasureTheory.volume : MeasureTheory.Measure ℝ) :=
  TechnicalLemmas.Measure.GibbsIntegral.integral_withDensity_lintegral_inv_mul_gibbsDensityENNReal_eq_integral_lintegral_inv_mul_exp_smul
    (MeasureTheory.volume : MeasureTheory.Measure ℝ) hV hZ0 g

example {V : ℝ → ℝ}
    (hV : AEMeasurable V (MeasureTheory.volume : MeasureTheory.Measure ℝ))
    (g : ℝ → ℝ) :
    ∫ x, g x ∂(MeasureTheory.volume : MeasureTheory.Measure ℝ).withDensity
        (fun x =>
          (∫⁻ y, TechnicalLemmas.Measure.Gibbs.gibbsDensityENNReal V y
            ∂(MeasureTheory.volume : MeasureTheory.Measure ℝ))⁻¹ *
            TechnicalLemmas.Measure.Gibbs.gibbsDensityENNReal V x) =
      ∫ x,
        ((∫⁻ y, TechnicalLemmas.Measure.Gibbs.gibbsDensityENNReal V y
          ∂(MeasureTheory.volume : MeasureTheory.Measure ℝ)).toReal⁻¹ *
          Real.exp (-V x)) • g x
        ∂(MeasureTheory.volume : MeasureTheory.Measure ℝ) :=
  TechnicalLemmas.Measure.GibbsIntegral.integral_withDensity_lintegral_inv_mul_gibbsDensityENNReal_eq_integral_lintegral_inv_mul_exp_smul_of_neZero
    (MeasureTheory.volume : MeasureTheory.Measure ℝ) hV g

example {V : ℝ → ℝ} {k : ℝ}
    (hstrong : StrongConvexOn (Set.univ : Set ℝ) k V)
    (x₀ : ℝ) (hx₀ : IsMinOn V (Set.univ : Set ℝ) x₀) :
    ∀ x : ℝ, V x₀ + (k / 4) * ‖x - x₀‖ ^ 2 ≤ V x :=
  TechnicalLemmas.Geometry.StrongConvexity.centered_quadratic_lower_bound_of_strongConvexOn_minimizer
    hstrong x₀ hx₀

example {V : ℝ → ℝ} {k : ℝ}
    (hstrong : StrongConvexOn (Set.univ : Set ℝ) k V) (hk : 0 ≤ k) :
    ConvexOn ℝ (Set.univ : Set ℝ) V :=
  TechnicalLemmas.Geometry.StrongConvexity.convexOn_of_strongConvexOn_nonneg
    hstrong hk

example {V : ℝ → ℝ} {k : ℝ}
    (hstrong : StrongConvexOn (Set.univ : Set ℝ) k V) (hk : 0 ≤ k) :
    TechnicalLemmas.Geometry.LogConcavity.LogConcaveOn
      (Set.univ : Set ℝ) (fun x : ℝ => Real.exp (-V x)) :=
  TechnicalLemmas.Geometry.StrongConvexity.logConcaveOn_exp_neg_of_strongConvexOn
    hstrong hk

example {V : ℝ → ℝ} {k c : ℝ}
    (hstrong : StrongConvexOn (Set.univ : Set ℝ) k V) (hk : 0 ≤ k) (hc : 0 < c) :
    TechnicalLemmas.Geometry.LogConcavity.LogConcaveOn
      (Set.univ : Set ℝ) (fun x : ℝ => c * Real.exp (-V x)) :=
  TechnicalLemmas.Geometry.StrongConvexity.logConcaveOn_const_mul_exp_neg_of_strongConvexOn
    hstrong hk hc

example {V : ℝ → ℝ} {k : ℝ} {Z : ℝ≥0∞}
    (hstrong : StrongConvexOn (Set.univ : Set ℝ) k V) (hk : 0 ≤ k)
    (hZ0 : Z ≠ 0) (hZtop : Z ≠ ∞) :
    TechnicalLemmas.Geometry.LogConcavity.LogConcaveOn (Set.univ : Set ℝ)
      (fun x : ℝ => (Z⁻¹ * TechnicalLemmas.Measure.Gibbs.gibbsDensityENNReal V x).toReal) :=
  TechnicalLemmas.Measure.GibbsLogConcavity.logConcaveOn_normalized_gibbsDensityENNReal_toReal_of_strongConvexOn
    hstrong hk hZ0 hZtop

example {V : ℝ → ℝ} {k : ℝ}
    (hstrong : StrongConvexOn (Set.univ : Set ℝ) k V) (hk : 0 ≤ k)
    (hZ0 :
      ∫⁻ y, TechnicalLemmas.Measure.Gibbs.gibbsDensityENNReal V y
        ∂(MeasureTheory.volume : MeasureTheory.Measure ℝ) ≠ 0)
    (hZtop :
      ∫⁻ y, TechnicalLemmas.Measure.Gibbs.gibbsDensityENNReal V y
        ∂(MeasureTheory.volume : MeasureTheory.Measure ℝ) ≠ ∞) :
    TechnicalLemmas.Geometry.LogConcavity.LogConcaveOn (Set.univ : Set ℝ)
      (fun x : ℝ =>
        ((∫⁻ y, TechnicalLemmas.Measure.Gibbs.gibbsDensityENNReal V y
          ∂(MeasureTheory.volume : MeasureTheory.Measure ℝ))⁻¹ *
          TechnicalLemmas.Measure.Gibbs.gibbsDensityENNReal V x).toReal) :=
  TechnicalLemmas.Measure.GibbsLogConcavity.logConcaveOn_lintegral_normalized_gibbsDensityENNReal_toReal_of_strongConvexOn
    (MeasureTheory.volume : MeasureTheory.Measure ℝ) hstrong hk hZ0 hZtop

example {V : ℝ → ℝ} {k : ℝ} (hk : 0 < k) (x₀ : ℝ)
    (hstrong : StrongConvexOn (Set.univ : Set ℝ) k V)
    (hx₀ : IsMinOn V (Set.univ : Set ℝ) x₀) :
    ∫⁻ x : ℝ, TechnicalLemmas.Measure.Gibbs.gibbsDensityENNReal V x
        ∂(MeasureTheory.volume : MeasureTheory.Measure ℝ) ≠ ∞ :=
  TechnicalLemmas.Analysis.Integrability.lintegral_gibbsDensityENNReal_ne_top_of_strongConvexOn_minimizer
    (E := ℝ) hk x₀ hstrong hx₀

example {V : ℝ → ℝ} {k : ℝ}
    (hV : AEMeasurable V
      (MeasureTheory.volume : MeasureTheory.Measure ℝ))
    (hk : 0 < k) (x₀ : ℝ)
    (hstrong : StrongConvexOn (Set.univ : Set ℝ) k V)
    (hx₀ : IsMinOn V (Set.univ : Set ℝ) x₀) :
    MeasureTheory.IsProbabilityMeasure
      ((MeasureTheory.volume : MeasureTheory.Measure ℝ).withDensity fun x =>
        (∫⁻ y, TechnicalLemmas.Measure.Gibbs.gibbsDensityENNReal V y
          ∂(MeasureTheory.volume : MeasureTheory.Measure ℝ))⁻¹ *
          TechnicalLemmas.Measure.Gibbs.gibbsDensityENNReal V x) :=
  TechnicalLemmas.Analysis.Integrability.isProbabilityMeasure_withDensity_normalized_gibbs_of_strongConvexOn_minimizer
    (E := ℝ) hV hk x₀ hstrong hx₀

example {V : ℝ → ℝ} {k : ℝ}
    (hV : AEMeasurable V
      (MeasureTheory.volume : MeasureTheory.Measure ℝ))
    (hk : 0 < k) (x₀ : ℝ)
    (hstrong : StrongConvexOn (Set.univ : Set ℝ) k V)
    (hx₀ : IsMinOn V (Set.univ : Set ℝ) x₀) :
    TechnicalLemmas.Geometry.LogConcavity.LogConcaveOn (Set.univ : Set ℝ)
      (fun x : ℝ =>
        ((∫⁻ y, TechnicalLemmas.Measure.Gibbs.gibbsDensityENNReal V y
          ∂(MeasureTheory.volume : MeasureTheory.Measure ℝ))⁻¹ *
          TechnicalLemmas.Measure.Gibbs.gibbsDensityENNReal V x).toReal) :=
  TechnicalLemmas.Measure.GibbsLogConcavity.logConcaveOn_lintegral_normalized_gibbsDensityENNReal_toReal_of_strongConvexOn_minimizer
    (E := ℝ) hV hk x₀ hstrong hx₀

example :
    TechnicalLemmas.Geometry.LogConcavity.LogConcaveOn
      (Set.Ioi (0 : ℝ)) (fun x : ℝ => x) :=
  TechnicalLemmas.Geometry.LogConcavity.logConcaveOn_id_Ioi

example : ConvexOn ℝ (Set.Ioi (0 : ℝ)) (fun x : ℝ => -Real.log x) :=
  TechnicalLemmas.Geometry.LogConcavity.logConcaveOn_id_Ioi.convexOn_neg_log

example : Convex ℝ {x : ℝ | x ∈ Set.Ioi (0 : ℝ) ∧ -Real.log x ≤ 1} :=
  TechnicalLemmas.Geometry.LogConcavity.logConcaveOn_id_Ioi.convex_sublevel_neg_log 1

example : Convex ℝ {x : ℝ | x ∈ Set.Ioi (0 : ℝ) ∧ (1 : ℝ) ≤ x} :=
  TechnicalLemmas.Geometry.LogConcavity.logConcaveOn_id_Ioi.convex_superlevel 1

example : QuasiconcaveOn ℝ (Set.Ioi (0 : ℝ)) (fun x : ℝ => x) :=
  TechnicalLemmas.Geometry.LogConcavity.logConcaveOn_id_Ioi.quasiconcaveOn

example :
    TechnicalLemmas.Geometry.LogConcavity.LogConcaveOn
      {x : ℝ | x ∈ Set.Ioi (0 : ℝ) ∧ (1 : ℝ) ≤ x} (fun x : ℝ => x) :=
  TechnicalLemmas.Geometry.LogConcavity.logConcaveOn_id_Ioi.restrict_superlevel 1

example :
    TechnicalLemmas.Geometry.LogConcavity.LogConcaveOn
      ((LinearMap.id : ℝ →ₗ[ℝ] ℝ) ⁻¹' Set.Ioi (0 : ℝ))
      (fun x : ℝ => ((LinearMap.id : ℝ →ₗ[ℝ] ℝ) x)) :=
  TechnicalLemmas.Geometry.LogConcavity.logConcaveOn_id_Ioi.comp_linearMap
    (LinearMap.id : ℝ →ₗ[ℝ] ℝ)

example :
    TechnicalLemmas.Geometry.LogConcavity.LogConcaveOn
      ((AffineMap.id ℝ ℝ) ⁻¹' Set.Ioi (0 : ℝ))
      (fun x : ℝ => (AffineMap.id ℝ ℝ) x) :=
  TechnicalLemmas.Geometry.LogConcavity.logConcaveOn_id_Ioi.comp_affineMap
    (AffineMap.id ℝ ℝ)

example :
    TechnicalLemmas.Geometry.LogConcavity.LogConcaveOn
      (Set.univ : Set ℝ) (fun x : ℝ => 2 * Real.exp (-x)) :=
  TechnicalLemmas.Geometry.LogConcavity.logConcaveOn_const_mul_exp_neg_of_convexOn
    (convexOn_id convex_univ) (by norm_num)

example : ConvexOn ℝ (Set.univ : Set ℝ) (fun x : ℝ => |x|) :=
  TechnicalLemmas.Geometry.LogConcavity.convexOn_univ_abs

example : ConvexOn ℝ (Set.univ : Set ℝ) (fun x : ℝ => (2 : ℝ) * |x| + 3) :=
  TechnicalLemmas.Geometry.LogConcavity.convexOn_univ_const_mul_abs_add
    (a := 2) (b := 3) (by norm_num)

example :
    TechnicalLemmas.Geometry.LogConcavity.LogConcaveOn
      (Set.univ : Set ℝ)
      (fun x : ℝ => Real.exp (-((2 : ℝ) * |x| + 3))) :=
  TechnicalLemmas.Geometry.LogConcavity.logConcaveOn_exp_neg_abs_linear
    (a := 2) (b := 3) (by norm_num)

example :
    TechnicalLemmas.Geometry.LogConcavity.LogConcaveOn
      (Set.univ : Set ℝ)
      (fun x : ℝ => (2 : ℝ) * Real.exp (-((1 : ℝ) * |x| + 0))) :=
  TechnicalLemmas.Geometry.LogConcavity.logConcaveOn_const_mul_exp_neg_abs_linear
    (a := 1) (b := 0) (c := 2) (by norm_num) (by norm_num)

example :
    TechnicalLemmas.Geometry.LogConcavity.LogConcaveOn
      (Set.univ : Set ℝ)
      (fun x : ℝ =>
        (2 * Real.exp (-(0 : ℝ)) / 1)⁻¹ *
          Real.exp (-((1 : ℝ) * |x| + 0))) :=
  TechnicalLemmas.Geometry.LogConcavity.logConcaveOn_explicit_abs_linear_normalized_density
    (a := 1) (b := 0) (by norm_num)

example :
    TechnicalLemmas.Geometry.LogConcavity.LogConcaveOn
      (Set.Ioi (0 : ℝ)) (fun x : ℝ => x * x) :=
  TechnicalLemmas.Geometry.LogConcavity.logConcaveOn_id_Ioi.mul
    TechnicalLemmas.Geometry.LogConcavity.logConcaveOn_id_Ioi

example :
    TechnicalLemmas.Geometry.LogConcavity.LogConcaveOn
      (Set.Ioi (0 : ℝ)) (fun x : ℝ => x ^ ((1 : ℝ) / 2)) :=
  TechnicalLemmas.Geometry.LogConcavity.logConcaveOn_id_Ioi.rpow (by norm_num)

example :
    TechnicalLemmas.Geometry.LogConcavity.LogConcaveOn
      ((Set.Ioi (0 : ℝ)) ×ˢ (Set.Ioi (0 : ℝ))) (fun x : ℝ × ℝ => x.1 * x.2) :=
  TechnicalLemmas.Geometry.LogConcavity.logConcaveOn_id_Ioi.prod
    TechnicalLemmas.Geometry.LogConcavity.logConcaveOn_id_Ioi

example : ConvexOn ℝ (Set.univ : Set ℝ) (fun x : ℝ => ‖x‖ ^ 2) :=
  TechnicalLemmas.Geometry.LogConcavity.convexOn_univ_norm_sq

example : ConvexOn ℝ (Set.univ : Set ℝ) (fun x : ℝ => (2 : ℝ) * ‖x‖ ^ 2 + 3) :=
  TechnicalLemmas.Geometry.LogConcavity.convexOn_univ_const_mul_norm_sq_add
    (E := ℝ) (a := 2) (b := 3) (by norm_num)

example :
    TechnicalLemmas.Geometry.LogConcavity.LogConcaveOn
      (Set.univ : Set ℝ)
      (fun x : ℝ => Real.exp (-((1 : ℝ) * ‖x‖ ^ 2 + 0))) :=
  TechnicalLemmas.Geometry.LogConcavity.logConcaveOn_exp_neg_quadratic_norm
    (E := ℝ) (a := 1) (b := 0) (by norm_num)

example :
    TechnicalLemmas.Geometry.LogConcavity.LogConcaveOn
      (Set.univ : Set ℝ)
      (fun x : ℝ =>
        (Real.exp (-(0 : ℝ)) *
            (Real.pi / (1 : ℝ)) ^ ((Module.finrank ℝ ℝ : ℝ) / 2))⁻¹ *
          Real.exp (-((1 : ℝ) * ‖x‖ ^ 2 + 0))) :=
  TechnicalLemmas.Geometry.LogConcavity.logConcaveOn_explicit_quadratic_normalized_density
    (E := ℝ) (a := 1) (b := 0) (by norm_num)

example : ConvexOn ℝ (Set.univ : Set ℝ) (fun x : ℝ => (2 : ℝ) * ‖x - 3‖ ^ 2 + 1) :=
  TechnicalLemmas.Geometry.LogConcavity.convexOn_univ_const_mul_norm_sub_sq_add
    (E := ℝ) (a := 2) (b := 1) (3 : ℝ) (by norm_num)

example :
    TechnicalLemmas.Geometry.LogConcavity.LogConcaveOn
      (Set.univ : Set ℝ)
      (fun x : ℝ => Real.exp (-((1 : ℝ) * ‖x - 3‖ ^ 2 + 0))) :=
  TechnicalLemmas.Geometry.LogConcavity.logConcaveOn_exp_neg_shifted_quadratic_norm
    (E := ℝ) (a := 1) (b := 0) (3 : ℝ) (by norm_num)

example :
    TechnicalLemmas.Geometry.LogConcavity.LogConcaveOn
      (Set.univ : Set ℝ)
      (fun x : ℝ =>
        (Real.exp (-(0 : ℝ)) *
            (Real.pi / (1 : ℝ)) ^ ((Module.finrank ℝ ℝ : ℝ) / 2))⁻¹ *
          Real.exp (-((1 : ℝ) * ‖x - 3‖ ^ 2 + 0))) :=
  TechnicalLemmas.Geometry.LogConcavity.logConcaveOn_explicit_shifted_quadratic_normalized_density
    (E := ℝ) (a := 1) (b := 0) (3 : ℝ) (by norm_num)

example : ConvexOn ℝ (Set.univ : Set (ℝ × ℝ))
    (fun z : ℝ × ℝ => (2 : ℝ) * ‖z.1 - z.2‖ ^ 2 + 1) :=
  TechnicalLemmas.Geometry.LogConcavity.convexOn_univ_const_mul_norm_fst_sub_snd_sq_add
    (E := ℝ) (a := 2) (b := 1) (by norm_num)

example :
    TechnicalLemmas.Geometry.LogConcavity.LogConcaveOn
      (Set.univ : Set (ℝ × ℝ))
      (fun z : ℝ × ℝ => Real.exp (-((1 : ℝ) * ‖z.1 - z.2‖ ^ 2 + 0))) :=
  TechnicalLemmas.Geometry.LogConcavity.logConcaveOn_exp_neg_pair_sub_quadratic_norm
    (E := ℝ) (a := 1) (b := 0) (by norm_num)

example :
    TechnicalLemmas.Geometry.LogConcavity.LogConcaveOn
      (Set.univ : Set (ℝ × ℝ))
      (fun z : ℝ × ℝ =>
        (Real.exp (-(0 : ℝ)) *
            (Real.pi / (1 : ℝ)) ^ ((Module.finrank ℝ ℝ : ℝ) / 2))⁻¹ *
          Real.exp (-((1 : ℝ) * ‖z.1 - z.2‖ ^ 2 + 0))) :=
  TechnicalLemmas.Geometry.LogConcavity.logConcaveOn_explicit_pair_sub_quadratic_kernel
    (E := ℝ) (a := 1) (b := 0) (by norm_num)

example :
    MeasureTheory.IsProbabilityMeasure
      ((MeasureTheory.Measure.dirac (0 : ℝ)).withDensity (fun _ : ℝ => (1 : ℝ≥0∞))) :=
  TechnicalLemmas.Measure.RadonNikodym.isProbabilityMeasure_withDensity_of_lintegral_eq_one
    (MeasureTheory.Measure.dirac (0 : ℝ)) (fun _ : ℝ => (1 : ℝ≥0∞)) (by simp)

example :
    MeasureTheory.IsProbabilityMeasure
      ((MeasureTheory.Measure.dirac (0 : ℝ)).withDensity fun x : ℝ =>
        ENNReal.ofReal (Real.exp ((fun _ : ℝ => 0) x))) :=
  TechnicalLemmas.Measure.RadonNikodym.isProbabilityMeasure_withDensity_ofReal_exp_of_integral_eq_one
    (MeasureTheory.Measure.dirac (0 : ℝ)) (U := fun _ : ℝ => 0)
    (by simp)
    (by simp)

example :
    MeasureTheory.IsProbabilityMeasure
      ((MeasureTheory.Measure.dirac (0 : ℝ)).withDensity
        fun x : ℝ =>
          (∫⁻ y, (if y = y then (1 : ℝ≥0∞) else 1) ∂(MeasureTheory.Measure.dirac (0 : ℝ)))⁻¹ *
            (if x = x then (1 : ℝ≥0∞) else 1)) :=
  TechnicalLemmas.Measure.RadonNikodym.isProbabilityMeasure_withDensity_normalized_lintegral
    (MeasureTheory.Measure.dirac (0 : ℝ)) (fun x : ℝ => if x = x then (1 : ℝ≥0∞) else 1)
    (by simp) (by simp)

example :
    AEMeasurable
      (TechnicalLemmas.Measure.Gibbs.gibbsDensityENNReal (fun x : ℝ => x))
      (MeasureTheory.Measure.dirac (0 : ℝ)) :=
  TechnicalLemmas.Measure.Gibbs.aemeasurable_gibbsDensityENNReal
    (MeasureTheory.Measure.dirac (0 : ℝ)) measurable_id.aemeasurable

example :
    MeasureTheory.IsProbabilityMeasure
      ((MeasureTheory.Measure.dirac (0 : ℝ)).withDensity
        fun x : ℝ =>
          (∫⁻ y, TechnicalLemmas.Measure.Gibbs.gibbsDensityENNReal
            (fun z : ℝ => z) y ∂(MeasureTheory.Measure.dirac (0 : ℝ)))⁻¹ *
            TechnicalLemmas.Measure.Gibbs.gibbsDensityENNReal (fun z : ℝ => z) x) :=
  TechnicalLemmas.Measure.Gibbs.isProbabilityMeasure_withDensity_normalized_gibbs
    (MeasureTheory.Measure.dirac (0 : ℝ)) (fun x : ℝ => x)
    (by simp [TechnicalLemmas.Measure.Gibbs.gibbsDensityENNReal])
    (by simp [TechnicalLemmas.Measure.Gibbs.gibbsDensityENNReal])

example :
    ∫⁻ x, TechnicalLemmas.Measure.Gibbs.gibbsDensityENNReal
      (fun z : ℝ => z) x ∂(MeasureTheory.Measure.dirac (0 : ℝ)) ≠ 0 :=
  TechnicalLemmas.Measure.Gibbs.lintegral_gibbsDensityENNReal_ne_zero
    (MeasureTheory.Measure.dirac (0 : ℝ)) measurable_id.aemeasurable

example :
    ∫⁻ x, TechnicalLemmas.Measure.Gibbs.gibbsDensityENNReal
      (fun z : ℝ => z) x ∂(MeasureTheory.Measure.dirac (0 : ℝ)) ≠ ∞ :=
  TechnicalLemmas.Measure.Gibbs.lintegral_gibbsDensityENNReal_ne_top_of_ae_le
    (MeasureTheory.Measure.dirac (0 : ℝ)) (fun z : ℝ => z)
    (fun _ : ℝ => (1 : ℝ≥0∞))
    (by simp [TechnicalLemmas.Measure.Gibbs.gibbsDensityENNReal])
    (by simp)

example :
    TechnicalLemmas.Measure.Gibbs.gibbsDensityENNReal
        (fun _ : ℝ => 1) (0 : ℝ) ≤
      TechnicalLemmas.Measure.Gibbs.gibbsDensityENNReal
        (fun _ : ℝ => 0) (0 : ℝ) :=
  TechnicalLemmas.Measure.Gibbs.gibbsDensityENNReal_le_of_potential_ge
    (by norm_num)

example :
    ∫⁻ x, TechnicalLemmas.Measure.Gibbs.gibbsDensityENNReal
      (fun z : ℝ => z) x ∂(MeasureTheory.Measure.dirac (0 : ℝ)) ≠ ∞ :=
  TechnicalLemmas.Measure.Gibbs.lintegral_gibbsDensityENNReal_ne_top_of_ae_potential_ge
    (MeasureTheory.Measure.dirac (0 : ℝ)) (W := fun z : ℝ => z)
    (by simp)
    (by simp [TechnicalLemmas.Measure.Gibbs.gibbsDensityENNReal])

example :
    ∫⁻ x, TechnicalLemmas.Measure.Gibbs.gibbsDensityENNReal
      (fun z : ℝ => z) x ∂(MeasureTheory.Measure.dirac (0 : ℝ)) ≠ ∞ :=
  TechnicalLemmas.Measure.Gibbs.lintegral_gibbsDensityENNReal_ne_top_of_ae_ge_const
    (MeasureTheory.Measure.dirac (0 : ℝ)) (c := 0)
    (by simp)

example :
    MeasureTheory.IsProbabilityMeasure
      ((MeasureTheory.Measure.dirac (0 : ℝ)).withDensity
        fun x : ℝ =>
          (∫⁻ y, TechnicalLemmas.Measure.Gibbs.gibbsDensityENNReal
            (fun z : ℝ => z) y ∂(MeasureTheory.Measure.dirac (0 : ℝ)))⁻¹ *
            TechnicalLemmas.Measure.Gibbs.gibbsDensityENNReal (fun z : ℝ => z) x) :=
  TechnicalLemmas.Measure.Gibbs.isProbabilityMeasure_withDensity_normalized_gibbs_of_ae_le
    (MeasureTheory.Measure.dirac (0 : ℝ)) (fun _ : ℝ => (1 : ℝ≥0∞))
    measurable_id.aemeasurable
    (by simp [TechnicalLemmas.Measure.Gibbs.gibbsDensityENNReal])
    (by simp)

example :
    MeasureTheory.IsProbabilityMeasure
      ((MeasureTheory.Measure.dirac (0 : ℝ)).withDensity
        fun x : ℝ =>
          (∫⁻ y, TechnicalLemmas.Measure.Gibbs.gibbsDensityENNReal
            (fun z : ℝ => z) y ∂(MeasureTheory.Measure.dirac (0 : ℝ)))⁻¹ *
            TechnicalLemmas.Measure.Gibbs.gibbsDensityENNReal (fun z : ℝ => z) x) :=
  TechnicalLemmas.Measure.Gibbs.isProbabilityMeasure_withDensity_normalized_gibbs_of_ae_potential_ge
    (MeasureTheory.Measure.dirac (0 : ℝ)) (W := fun z : ℝ => z)
    measurable_id.aemeasurable
    (by simp)
    (by simp [TechnicalLemmas.Measure.Gibbs.gibbsDensityENNReal])

example :
    MeasureTheory.IsProbabilityMeasure
      ((MeasureTheory.Measure.dirac (0 : ℝ)).withDensity
        fun x : ℝ =>
          (∫⁻ y, TechnicalLemmas.Measure.Gibbs.gibbsDensityENNReal
            (fun z : ℝ => z) y ∂(MeasureTheory.Measure.dirac (0 : ℝ)))⁻¹ *
            TechnicalLemmas.Measure.Gibbs.gibbsDensityENNReal (fun z : ℝ => z) x) :=
  TechnicalLemmas.Measure.Gibbs.isProbabilityMeasure_withDensity_normalized_gibbs_of_ae_ge_const
    (MeasureTheory.Measure.dirac (0 : ℝ)) (c := 0)
    measurable_id.aemeasurable
    (by simp)

example :
    ((MeasureTheory.Measure.dirac (0 : ℝ)).withDensity
        (fun _ : ℝ => (1 : ℝ≥0∞))).map (MeasurableEquiv.refl ℝ) =
      ((MeasureTheory.Measure.dirac (0 : ℝ)).map (MeasurableEquiv.refl ℝ)).withDensity
        (fun _ : ℝ => (1 : ℝ≥0∞)) :=
  TechnicalLemmas.Measure.RadonNikodym.measurableEquiv_map_withDensity
    (MeasurableEquiv.refl ℝ) (MeasureTheory.Measure.dirac (0 : ℝ)) measurable_const

example :
    ∫ x : ℝ, x ∂(ProbabilityTheory.gaussianReal 0 (1 : NNReal)) = 0 :=
  TechnicalLemmas.Gaussian.integral_id_gaussianReal_zero 1

example :
    (ProbabilityTheory.gaussianReal 0 (1 : NNReal)).withDensity
        (fun x : ℝ => ENNReal.ofReal (Real.exp ((2 : ℝ) * x - (2 : ℝ) ^ 2 / 2))) =
      ProbabilityTheory.gaussianReal 2 (1 : NNReal) :=
  TechnicalLemmas.ProbabilityDistributions.Gaussian.gaussianReal_withDensity_exp_shift 2

example :
    ∫ x : ℝ, Real.exp ((3 : ℝ) * x)
        ∂(ProbabilityTheory.gaussianReal 0 (1 : NNReal)) =
      Real.exp ((3 : ℝ) ^ 2 / 2) :=
  TechnicalLemmas.ProbabilityDistributions.Gaussian.integral_exp_mul_gaussianReal_zero_one 3

example :
    MeasureTheory.Integrable
      (fun w : Fin 2 → ℝ => ∑ i : Fin 2, (2 : ℝ) * w i)
      (TechnicalLemmas.ProbabilityDistributions.Gaussian.stdGaussianPi 2) :=
  TechnicalLemmas.ProbabilityDistributions.Gaussian.integrable_linearForm_stdGaussianPi
    (n := 2) (fun _ => 2)

example :
    ∫ w : Fin 2 → ℝ, (∑ i : Fin 2, (2 : ℝ) * w i)
        ∂(TechnicalLemmas.ProbabilityDistributions.Gaussian.stdGaussianPi 2) = 0 :=
  TechnicalLemmas.ProbabilityDistributions.Gaussian.integral_linearForm_stdGaussianPi
    (n := 2) (fun _ => 2)

example :
    ∫ w : Fin 2 → ℝ,
        Real.exp ((∑ i : Fin 2, (1 : ℝ) * w i) - (∑ _ : Fin 2, (1 : ℝ) ^ 2) / 2)
          ∂(TechnicalLemmas.ProbabilityDistributions.Gaussian.stdGaussianPi 2) = 1 :=
  TechnicalLemmas.ProbabilityDistributions.Gaussian.integral_exp_centered_linearForm_stdGaussianPi
    (n := 2) (fun _ => 1)

example :
    (TechnicalLemmas.ProbabilityDistributions.Gaussian.stdGaussianPi 2).withDensity
        (fun y : Fin 2 → ℝ =>
          ENNReal.ofReal
            (Real.exp ((∑ i : Fin 2, (1 : ℝ) * y i) -
              (∑ _ : Fin 2, (1 : ℝ) ^ 2) / 2))) =
      MeasureTheory.Measure.pi
        (fun _ : Fin 2 => ProbabilityTheory.gaussianReal 1 (1 : NNReal)) :=
  TechnicalLemmas.ProbabilityDistributions.Gaussian.stdGaussianPi_withDensity_exp_shift
    (n := 2) (fun _ => 1)

example :
    ∫ _ : Fin 2 → ℝ, (1 : ℝ)
        ∂MeasureTheory.Measure.pi
          (fun _ : Fin 2 => ProbabilityTheory.gaussianReal 1 (1 : NNReal)) =
      ∫ X : Fin 2 → ℝ,
        Real.exp ((∑ i : Fin 2, (1 : ℝ) * X i) -
          (∑ _ : Fin 2, (1 : ℝ) ^ 2) / 2) * (1 : ℝ)
          ∂(TechnicalLemmas.ProbabilityDistributions.Gaussian.stdGaussianPi 2) :=
  TechnicalLemmas.ProbabilityDistributions.Gaussian.stdGaussianPi_shift_integral
    (n := 2) (fun _ => 1) (fun _ => 1)

example :
    ∫ _ : EuclideanSpace ℝ (Fin 2), (1 : ℝ)
        ∂(MeasureTheory.Measure.pi
          (fun _ : Fin 2 => ProbabilityTheory.gaussianReal 1 (1 : NNReal))).map
            (WithLp.toLp 2) =
      ∫ X : Fin 2 → ℝ,
        Real.exp ((∑ i : Fin 2, (1 : ℝ) * X i) -
          (∑ _ : Fin 2, (1 : ℝ) ^ 2) / 2) * (1 : ℝ)
          ∂(TechnicalLemmas.ProbabilityDistributions.Gaussian.stdGaussianPi 2) :=
  TechnicalLemmas.ProbabilityDistributions.Gaussian.stdGaussianPi_shift_integral_map_toLp
    (n := 2) (fun _ => 1) (f := fun _ => (1 : ℝ)) measurable_const

example :
    ∫ _ : EuclideanSpace ℝ (Fin 2), (1 : ℝ)
        ∂(MeasureTheory.Measure.pi
          (fun _ : Fin 2 => ProbabilityTheory.gaussianReal 1 (1 : NNReal))).map
            (WithLp.toLp 2) =
      ∫ Z : EuclideanSpace ℝ (Fin 2),
        Real.exp (inner ℝ (WithLp.toLp 2 (fun _ : Fin 2 => (1 : ℝ))
            : EuclideanSpace ℝ (Fin 2)) Z -
          ‖(WithLp.toLp 2 (fun _ : Fin 2 => (1 : ℝ))
            : EuclideanSpace ℝ (Fin 2))‖ ^ 2 / 2) * (1 : ℝ)
          ∂(ProbabilityTheory.stdGaussian (EuclideanSpace ℝ (Fin 2))) :=
  TechnicalLemmas.ProbabilityDistributions.Gaussian.stdGaussian_shift_integral_map_toLp
    (ι := Fin 2) (fun _ => 1) (f := fun _ => (1 : ℝ)) measurable_const

example :
    ∫ _ : EuclideanSpace ℝ (Fin 2), (1 : ℝ)
        ∂(TechnicalLemmas.StochasticProcesses.Girsanov.finiteShiftedGaussianPathMeasure
          (fun _ : Fin 2 => (1 : ℝ))) =
      ∫ Z : EuclideanSpace ℝ (Fin 2),
        TechnicalLemmas.StochasticProcesses.Girsanov.finiteGaussianGirsanovWeight
          (fun _ : Fin 2 => (1 : ℝ)) Z * (1 : ℝ)
          ∂(ProbabilityTheory.stdGaussian (EuclideanSpace ℝ (Fin 2))) :=
  TechnicalLemmas.StochasticProcesses.Girsanov.finiteGaussianGirsanovCylinderIntegral
    (ι := Fin 2) (fun _ => 1) (F := fun _ => (1 : ℝ)) measurable_const

example :
    ∫ Z : EuclideanSpace ℝ (Fin 2),
        TechnicalLemmas.StochasticProcesses.Girsanov.finiteGaussianGirsanovWeight
          (fun _ : Fin 2 => (1 : ℝ)) Z
          ∂(ProbabilityTheory.stdGaussian (EuclideanSpace ℝ (Fin 2))) = 1 :=
  TechnicalLemmas.StochasticProcesses.Girsanov.integral_finiteGaussianGirsanovWeight_eq_one
    (ι := Fin 2) (fun _ => 1)

example :
    TechnicalLemmas.StochasticProcesses.Girsanov.finiteShiftedGaussianPathMeasure
        (fun _ : Fin 2 => (1 : ℝ)) =
      (ProbabilityTheory.stdGaussian (EuclideanSpace ℝ (Fin 2))).withDensity
        (fun Z =>
          ENNReal.ofReal
            (TechnicalLemmas.StochasticProcesses.Girsanov.finiteGaussianGirsanovWeight
              (fun _ : Fin 2 => (1 : ℝ)) Z)) :=
  TechnicalLemmas.StochasticProcesses.Girsanov.finiteGaussianGirsanovCylinderMeasure_eq_withDensity
    (ι := Fin 2) (fun _ => 1)

example :
    @TechnicalLemmas.Probability.LawMap.lawMapIntegral =
      @lawMapIntegral := rfl

example :
    @TechnicalLemmas.Probability.ConditionalKernel.condDistribIntegralNamedLawIntegral =
      @condDistribIntegralNamedLawIntegral := rfl

example :
    @TechnicalLemmas.InformationTheory.DonskerVaradhan.dvVariationalScaledTestEnergyBound =
      @dvVariationalScaledTestEnergyBound := rfl

example :
    @TechnicalLemmas.InformationTheory.KLDensity.klPointwiseDerivSimplify =
      @TechnicalLemmas.InformationTheory.KLDensity.klPointwiseDerivSimplify := rfl

example :
    @TechnicalLemmas.InformationTheory.KLDensity.klDerivativeRemoveMassTerm =
      @TechnicalLemmas.InformationTheory.KLDensity.klDerivativeRemoveMassTerm := rfl

example :
    0 < TechnicalLemmas.InformationTheory.Renyi.renyiIntegrand
      ((1 : ℝ) / 2) 2 3 :=
  TechnicalLemmas.InformationTheory.Renyi.renyiIntegrand_pos
    (by norm_num) (by norm_num)

example :
    Measurable fun x : ℝ =>
      TechnicalLemmas.InformationTheory.Renyi.renyiIntegrand
        ((1 : ℝ) / 2) x x :=
  TechnicalLemmas.InformationTheory.Renyi.measurable_renyiIntegrand
    (by norm_num) (by norm_num) measurable_id measurable_id

example :
    ∫⁻ x, TechnicalLemmas.InformationTheory.Renyi.renyiIntegrandENNReal
      ((1 : ℝ) / 2) (fun _ : ℝ => 1) (fun _ : ℝ => 1) x
        ∂(MeasureTheory.Measure.dirac (0 : ℝ)) ≠ ∞ :=
  TechnicalLemmas.InformationTheory.Renyi.lintegral_renyiIntegrandENNReal_ne_top_of_ae_le
    (MeasureTheory.Measure.dirac (0 : ℝ)) ((1 : ℝ) / 2)
    (fun _ : ℝ => 1) (fun _ : ℝ => 1) (fun _ : ℝ => (1 : ℝ≥0∞))
    (by simp [TechnicalLemmas.InformationTheory.Renyi.renyiIntegrandENNReal,
      TechnicalLemmas.InformationTheory.Renyi.renyiIntegrand])
    (by simp)

example :
    HasDerivAt
      (fun s : ℝ =>
        TechnicalLemmas.InformationTheory.Renyi.renyiIntegrand
          ((1 : ℝ) / 2) ((fun _ : ℝ => 2) s) ((fun _ : ℝ => 3) s))
      0 0 := by
  simpa using
    TechnicalLemmas.InformationTheory.Renyi.hasDerivAt_renyiIntegrand
      (a := ((1 : ℝ) / 2)) (p := fun _ : ℝ => 2) (q := fun _ : ℝ => 3)
      (t := 0) (pdot := 0) (qdot := 0)
      (hasDerivAt_const (0 : ℝ) (2 : ℝ))
      (hasDerivAt_const (0 : ℝ) (3 : ℝ))
      (by norm_num) (by norm_num)

example :
    @TechnicalLemmas.StochasticProcesses.WeakGenerator.weakGeneratorFromSampleDerivative =
      @TechnicalLemmas.StochasticProcesses.WeakGenerator.weakGeneratorFromSampleDerivative := rfl

example :
    @TechnicalLemmas.StochasticProcesses.FokkerPlanckAlgebra.fpRewriteScalarAlgebra =
      @TechnicalLemmas.StochasticProcesses.FokkerPlanckAlgebra.fpRewriteScalarAlgebra := rfl

example :
    @TechnicalLemmas.StochasticProcesses.FokkerPlanckAlgebra.fisherIbpAlgebra =
      @TechnicalLemmas.StochasticProcesses.FokkerPlanckAlgebra.fisherIbpAlgebra := rfl

example {f V : ℝ → ℝ} {x f' f'' V' : ℝ}
    (hV : HasDerivAt V V' x)
    (hf : HasDerivAt f f' x)
    (hf' : HasDerivAt (deriv f) f'' x) :
    HasDerivAt (fun y : ℝ => Real.exp (-V y) * deriv f y)
      (Real.exp (-V x) * (f'' - V' * f')) x :=
  TechnicalLemmas.StochasticProcesses.Langevin.hasDerivAt_gibbsWeight_mul_testDeriv_eq_langevinGenerator_1d
    hV hf hf'

example {f V : ℝ → ℝ} {x f' f'' V' : ℝ}
    (hV : HasDerivAt V V' x)
    (hf : HasDerivAt f f' x)
    (hf' : HasDerivAt (deriv f) f'' x) :
    deriv (fun y : ℝ => Real.exp (-V y) * deriv f y) x =
      Real.exp (-V x) * (f'' - V' * f') :=
  TechnicalLemmas.StochasticProcesses.Langevin.deriv_gibbsWeight_mul_testDeriv_eq_langevinGenerator_1d
    hV hf hf'

example {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    {rho lapF divWeighted : ℝ} {gradRho gradV gradF : E}
    (hdiv : divWeighted = rho * lapF + inner ℝ gradRho gradF)
    (hgrad : gradRho = (-rho) • gradV) :
    divWeighted = rho * (lapF - inner ℝ gradV gradF) :=
  TechnicalLemmas.StochasticProcesses.Langevin.weightedDivergence_gibbsWeight_langevinGenerator_algebra
    hdiv hgrad

example {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    {Vx lapF divWeighted : ℝ} {gradRho gradV gradF : E}
    (hdiv :
      divWeighted =
        Real.exp (-Vx) * lapF + inner ℝ gradRho gradF)
    (hgrad : gradRho = (-(Real.exp (-Vx))) • gradV) :
    divWeighted =
      Real.exp (-Vx) * (lapF - inner ℝ gradV gradF) :=
  TechnicalLemmas.StochasticProcesses.Langevin.expNeg_weightedDivergence_langevinGenerator_algebra
    hdiv hgrad

example {ι : Type*} [Fintype ι]
    {rho : ℝ} {divCoord hessDiag gradRho gradV gradF : ι → ℝ}
    (hdiv : ∀ i, divCoord i = rho * hessDiag i + gradRho i * gradF i)
    (hgrad : ∀ i, gradRho i = -rho * gradV i) :
    (∑ i, divCoord i) =
      rho * ((∑ i, hessDiag i) - ∑ i, gradV i * gradF i) :=
  TechnicalLemmas.StochasticProcesses.Langevin.finiteCoord_weightedDivergence_langevinGenerator_algebra
    hdiv hgrad

example {ι : Type*} [Fintype ι]
    {rho lapF divWeighted innerGradVGradF : ℝ}
    {divCoord hessDiag gradRho gradV gradF : ι → ℝ}
    (hdivWeighted : divWeighted = ∑ i, divCoord i)
    (hdiv : ∀ i, divCoord i = rho * hessDiag i + gradRho i * gradF i)
    (hgrad : ∀ i, gradRho i = -rho * gradV i)
    (hlap : lapF = ∑ i, hessDiag i)
    (hinner : innerGradVGradF = ∑ i, gradV i * gradF i) :
    divWeighted = rho * (lapF - innerGradVGradF) :=
  TechnicalLemmas.StochasticProcesses.Langevin.finiteCoord_named_weightedDivergence_langevinGenerator_algebra
    hdivWeighted hdiv hgrad hlap hinner

example {ι : Type*} [Fintype ι]
    {rho lapF divWeighted : ℝ}
    {divCoord hessDiag gradRho gradV gradF : ι → ℝ}
    (hdivWeighted : divWeighted = ∑ i, divCoord i)
    (hdiv : ∀ i, divCoord i = rho * hessDiag i + gradRho i * gradF i)
    (hgrad : ∀ i, gradRho i = -rho * gradV i)
    (hlap : lapF = ∑ i, hessDiag i) :
    divWeighted =
      rho * (lapF - inner ℝ (WithLp.toLp 2 gradV : EuclideanSpace ℝ ι)
        (WithLp.toLp 2 gradF : EuclideanSpace ℝ ι)) :=
  TechnicalLemmas.StochasticProcesses.Langevin.finiteCoord_toLpInner_weightedDivergence_langevinGenerator_algebra
    hdivWeighted hdiv hgrad hlap

example {ι : Type*} [Fintype ι]
    {rho lapF divWeighted : ℝ}
    {divCoord hessDiag gradRho : ι → ℝ}
    {gradV gradF : EuclideanSpace ℝ ι}
    (hdivWeighted : divWeighted = ∑ i, divCoord i)
    (hdiv : ∀ i, divCoord i = rho * hessDiag i + gradRho i * gradF i)
    (hgrad : ∀ i, gradRho i = -rho * gradV i)
    (hlap : lapF = ∑ i, hessDiag i) :
    divWeighted = rho * (lapF - inner ℝ gradV gradF) :=
  TechnicalLemmas.StochasticProcesses.Langevin.finiteCoord_euclideanInner_weightedDivergence_langevinGenerator_algebra
    hdivWeighted hdiv hgrad hlap

example {ι : Type*} [Fintype ι]
    (V f : EuclideanSpace ℝ ι → ℝ) (x : EuclideanSpace ℝ ι) :
    Laplacian.laplacian f x - inner ℝ (gradient V x) (gradient f x) =
      (∑ i, iteratedFDeriv ℝ 2 f x
        ![(EuclideanSpace.basisFun ι ℝ) i, (EuclideanSpace.basisFun ι ℝ) i]) -
        ∑ i, (gradient V x) i * (gradient f x) i :=
  TechnicalLemmas.StochasticProcesses.Langevin.finiteEuclidean_langevinGenerator_basisDisplay
    V f x

example {ι : Type*} [Fintype ι] [DecidableEq ι]
    (V f : EuclideanSpace ℝ ι → ℝ) (x : EuclideanSpace ℝ ι) :
    Laplacian.laplacian f x - inner ℝ (gradient V x) (gradient f x) =
      (∑ i, iteratedFDeriv ℝ 2 f x
        ![(EuclideanSpace.single i (1 : ℝ)), (EuclideanSpace.single i (1 : ℝ))]) -
        ∑ i, (gradient V x) i * (gradient f x) i :=
  TechnicalLemmas.StochasticProcesses.Langevin.finiteEuclidean_langevinGenerator_coordinateDisplay
    V f x

example {ι : Type*} [Fintype ι]
    {rho divWeighted : ℝ}
    {V f : EuclideanSpace ℝ ι → ℝ} {x : EuclideanSpace ℝ ι}
    {divCoord gradRho : ι → ℝ}
    (hdivWeighted : divWeighted = ∑ i, divCoord i)
    (hdiv : ∀ i,
      divCoord i =
        rho * iteratedFDeriv ℝ 2 f x
          ![(EuclideanSpace.basisFun ι ℝ) i, (EuclideanSpace.basisFun ι ℝ) i] +
        gradRho i * (gradient f x) i)
    (hgrad : ∀ i, gradRho i = -rho * (gradient V x) i) :
    divWeighted =
      rho * (Laplacian.laplacian f x -
        inner ℝ (gradient V x) (gradient f x)) :=
  TechnicalLemmas.StochasticProcesses.Langevin.finiteEuclidean_weightedDivergence_langevinGenerator_basisHandoff
    hdivWeighted hdiv hgrad

example {ι : Type*} [Fintype ι] [DecidableEq ι]
    {rho divWeighted : ℝ}
    {V f : EuclideanSpace ℝ ι → ℝ} {x : EuclideanSpace ℝ ι}
    {divCoord gradRho : ι → ℝ}
    (hdivWeighted : divWeighted = ∑ i, divCoord i)
    (hdiv : ∀ i,
      divCoord i =
        rho * iteratedFDeriv ℝ 2 f x
          ![(EuclideanSpace.single i (1 : ℝ)), (EuclideanSpace.single i (1 : ℝ))] +
        gradRho i * (gradient f x) i)
    (hgrad : ∀ i, gradRho i = -rho * (gradient V x) i) :
    divWeighted =
      rho * (Laplacian.laplacian f x -
        inner ℝ (gradient V x) (gradient f x)) :=
  TechnicalLemmas.StochasticProcesses.Langevin.finiteEuclidean_weightedDivergence_langevinGenerator_coordinateHandoff
    hdivWeighted hdiv hgrad

example {ι : Type*} [Fintype ι]
    {divWeighted : ℝ}
    {V f : EuclideanSpace ℝ ι → ℝ} {x : EuclideanSpace ℝ ι}
    {divCoord : ι → ℝ}
    (hV : DifferentiableAt ℝ V x)
    (hdivWeighted : divWeighted = ∑ i, divCoord i)
    (hdiv : ∀ i,
      divCoord i =
        Real.exp (-V x) * iteratedFDeriv ℝ 2 f x
          ![(EuclideanSpace.basisFun ι ℝ) i, (EuclideanSpace.basisFun ι ℝ) i] +
        (gradient (fun y : EuclideanSpace ℝ ι => Real.exp (-V y)) x) i *
          (gradient f x) i) :
    divWeighted =
      Real.exp (-V x) * (Laplacian.laplacian f x -
        inner ℝ (gradient V x) (gradient f x)) :=
  TechnicalLemmas.StochasticProcesses.Langevin.finiteEuclidean_expNeg_weightedDivergence_langevinGenerator_basisHandoff
    hV hdivWeighted hdiv

example {ι : Type*} [Fintype ι] [DecidableEq ι]
    {divWeighted : ℝ}
    {V f : EuclideanSpace ℝ ι → ℝ} {x : EuclideanSpace ℝ ι}
    {divCoord : ι → ℝ}
    (hV : DifferentiableAt ℝ V x)
    (hdivWeighted : divWeighted = ∑ i, divCoord i)
    (hdiv : ∀ i,
      divCoord i =
        Real.exp (-V x) * iteratedFDeriv ℝ 2 f x
          ![(EuclideanSpace.single i (1 : ℝ)), (EuclideanSpace.single i (1 : ℝ))] +
        (gradient (fun y : EuclideanSpace ℝ ι => Real.exp (-V y)) x) i *
          (gradient f x) i) :
    divWeighted =
      Real.exp (-V x) * (Laplacian.laplacian f x -
        inner ℝ (gradient V x) (gradient f x)) :=
  TechnicalLemmas.StochasticProcesses.Langevin.finiteEuclidean_expNeg_weightedDivergence_langevinGenerator_coordinateHandoff
    hV hdivWeighted hdiv

example {ι : Type*} [Fintype ι] [DecidableEq ι]
    {V f : EuclideanSpace ℝ ι → ℝ} {x : EuclideanSpace ℝ ι}
    (hV : DifferentiableAt ℝ V x)
    (hf : DifferentiableAt ℝ
      (fun y : EuclideanSpace ℝ ι => fderiv ℝ f y) x)
    (hgradF : ∀ i,
      fderiv ℝ f x (EuclideanSpace.single i (1 : ℝ)) = (gradient f x) i) :
    (∑ i, lineDeriv ℝ
        (fun y : EuclideanSpace ℝ ι =>
          Real.exp (-V y) * fderiv ℝ f y (EuclideanSpace.single i (1 : ℝ)))
        x (EuclideanSpace.single i (1 : ℝ))) =
      Real.exp (-V x) * (Laplacian.laplacian f x -
        inner ℝ (gradient V x) (gradient f x)) :=
  TechnicalLemmas.StochasticProcesses.Langevin.finiteEuclidean_expNeg_lineDeriv_fderiv_coordinateSum_langevinGenerator_display
    hV hf hgradF

example {ι : Type*} [Fintype ι] [DecidableEq ι]
    {V f : EuclideanSpace ℝ ι → ℝ} {x : EuclideanSpace ℝ ι}
    (hV : DifferentiableAt ℝ V x)
    (hfderiv : DifferentiableAt ℝ
      (fun y : EuclideanSpace ℝ ι => fderiv ℝ f y) x)
    (hf : DifferentiableAt ℝ f x) :
    (∑ i, lineDeriv ℝ
        (fun y : EuclideanSpace ℝ ι =>
          Real.exp (-V y) * fderiv ℝ f y (EuclideanSpace.single i (1 : ℝ)))
        x (EuclideanSpace.single i (1 : ℝ))) =
      Real.exp (-V x) * (Laplacian.laplacian f x -
        inner ℝ (gradient V x) (gradient f x)) :=
  TechnicalLemmas.StochasticProcesses.Langevin.finiteEuclidean_expNeg_lineDeriv_fderiv_coordinateSum_langevinGenerator_display_of_differentiableAt
    hV hfderiv hf

example {ι : Type*} [Fintype ι] [DecidableEq ι]
    {V f : EuclideanSpace ℝ ι → ℝ} {x : EuclideanSpace ℝ ι}
    (hV : DifferentiableAt ℝ V x)
    (hfderiv : DifferentiableAt ℝ
      (fun y : EuclideanSpace ℝ ι => fderiv ℝ f y) x)
    (hf : DifferentiableAt ℝ f x) :
    TechnicalLemmas.Analysis.Calculus.Divergence.coordinateDivergence
      (fun y : EuclideanSpace ℝ ι =>
        (WithLp.toLp 2 (fun i =>
          Real.exp (-V y) * fderiv ℝ f y (EuclideanSpace.single i (1 : ℝ))) :
          EuclideanSpace ℝ ι)) x =
      Real.exp (-V x) * (Laplacian.laplacian f x -
        inner ℝ (gradient V x) (gradient f x)) :=
  TechnicalLemmas.StochasticProcesses.Langevin.coordinateDivergence_expNeg_fderivCoordinateField_langevinGenerator_display_of_differentiableAt
    hV hfderiv hf

example {n : ℕ}
    {V f : EuclideanSpace ℝ (Fin (n + 1)) → ℝ}
    {x : Fin (n + 1) → ℝ}
    {F' : (Fin (n + 1) → ℝ) →L[ℝ] (Fin (n + 1) → ℝ)}
    (hF : HasFDerivAt
      (fun z : Fin (n + 1) → ℝ => fun i =>
        Real.exp (-V (WithLp.toLp 2 z : EuclideanSpace ℝ (Fin (n + 1)))) *
          fderiv ℝ f (WithLp.toLp 2 z : EuclideanSpace ℝ (Fin (n + 1)))
            (EuclideanSpace.single i (1 : ℝ))) F' x)
    (hV : DifferentiableAt ℝ V
      (WithLp.toLp 2 x : EuclideanSpace ℝ (Fin (n + 1))))
    (hfderiv : DifferentiableAt ℝ
      (fun y : EuclideanSpace ℝ (Fin (n + 1)) => fderiv ℝ f y)
      (WithLp.toLp 2 x : EuclideanSpace ℝ (Fin (n + 1))))
    (hf : DifferentiableAt ℝ f
      (WithLp.toLp 2 x : EuclideanSpace ℝ (Fin (n + 1)))) :
    (∑ i, F' (Pi.single i (1 : ℝ)) i) =
      Real.exp (-V (WithLp.toLp 2 x : EuclideanSpace ℝ (Fin (n + 1)))) *
        (Laplacian.laplacian f
            (WithLp.toLp 2 x : EuclideanSpace ℝ (Fin (n + 1))) -
          inner ℝ
            (gradient V (WithLp.toLp 2 x : EuclideanSpace ℝ (Fin (n + 1))))
            (gradient f (WithLp.toLp 2 x : EuclideanSpace ℝ (Fin (n + 1))))) :=
  TechnicalLemmas.StochasticProcesses.Langevin.trace_expNeg_fderivCoordinateField_langevinGenerator_display_of_hasFDerivAt
    hF hV hfderiv hf

example {n : ℕ}
    {V f : EuclideanSpace ℝ (Fin (n + 1)) → ℝ}
    {x : Fin (n + 1) → ℝ}
    (hV : ContDiff ℝ 1 V)
    (hf : ContDiff ℝ 2 f) :
    HasFDerivAt
      (fun z : Fin (n + 1) → ℝ => fun i =>
        Real.exp (-V (WithLp.toLp 2 z : EuclideanSpace ℝ (Fin (n + 1)))) *
          fderiv ℝ f (WithLp.toLp 2 z : EuclideanSpace ℝ (Fin (n + 1)))
            (EuclideanSpace.single i (1 : ℝ)))
      (fderiv ℝ
        (fun z : Fin (n + 1) → ℝ => fun i =>
          Real.exp (-V (WithLp.toLp 2 z : EuclideanSpace ℝ (Fin (n + 1)))) *
            fderiv ℝ f (WithLp.toLp 2 z : EuclideanSpace ℝ (Fin (n + 1)))
              (EuclideanSpace.single i (1 : ℝ))) x) x :=
  TechnicalLemmas.StochasticProcesses.Langevin.hasFDerivAt_expNeg_fderivCoordinateField_of_contDiff
    hV hf

example {n : ℕ}
    (a b : Fin (n + 1) → ℝ)
    (V f : EuclideanSpace ℝ (Fin (n + 1)) → ℝ)
    (F' : (Fin (n + 1) → ℝ) →
      (Fin (n + 1) → ℝ) →L[ℝ] (Fin (n + 1) → ℝ))
    (hF : ∀ x ∈ Set.Icc a b,
      HasFDerivAt
        (fun z : Fin (n + 1) → ℝ => fun i =>
          Real.exp (-V (WithLp.toLp 2 z : EuclideanSpace ℝ (Fin (n + 1)))) *
            fderiv ℝ f (WithLp.toLp 2 z : EuclideanSpace ℝ (Fin (n + 1)))
              (EuclideanSpace.single i (1 : ℝ))) (F' x) x)
    (hV : ∀ x ∈ Set.Icc a b,
      DifferentiableAt ℝ V
        (WithLp.toLp 2 x : EuclideanSpace ℝ (Fin (n + 1))))
    (hfderiv : ∀ x ∈ Set.Icc a b,
      DifferentiableAt ℝ
        (fun y : EuclideanSpace ℝ (Fin (n + 1)) => fderiv ℝ f y)
        (WithLp.toLp 2 x : EuclideanSpace ℝ (Fin (n + 1))))
    (hf : ∀ x ∈ Set.Icc a b,
      DifferentiableAt ℝ f
        (WithLp.toLp 2 x : EuclideanSpace ℝ (Fin (n + 1))))
    (hcont : ContinuousOn
      (fun x : Fin (n + 1) → ℝ =>
        Real.exp (-V (WithLp.toLp 2 x : EuclideanSpace ℝ (Fin (n + 1)))) *
          (Laplacian.laplacian f
              (WithLp.toLp 2 x : EuclideanSpace ℝ (Fin (n + 1))) -
            inner ℝ
              (gradient V (WithLp.toLp 2 x : EuclideanSpace ℝ (Fin (n + 1))))
              (gradient f (WithLp.toLp 2 x : EuclideanSpace ℝ (Fin (n + 1))))))
      (Set.Icc a b)) :
    MeasureTheory.IntegrableOn (fun x => ∑ i, F' x (Pi.single i (1 : ℝ)) i)
      (Set.Icc a b) MeasureTheory.volume :=
  TechnicalLemmas.StochasticProcesses.Langevin.integrableOn_trace_expNeg_fderivCoordinateField_of_continuousOn
    a b V f F' hF hV hfderiv hf hcont

example {n : ℕ} {a b : Fin (n + 1) → ℝ}
    {V f : EuclideanSpace ℝ (Fin (n + 1)) → ℝ}
    (hV : ContinuousOn
      (fun x : Fin (n + 1) → ℝ =>
        V (WithLp.toLp 2 x : EuclideanSpace ℝ (Fin (n + 1))))
      (Set.Icc a b))
    (hlap : ContinuousOn
      (fun x : Fin (n + 1) → ℝ =>
        Laplacian.laplacian f (WithLp.toLp 2 x : EuclideanSpace ℝ (Fin (n + 1))))
      (Set.Icc a b))
    (hgradV : ContinuousOn
      (fun x : Fin (n + 1) → ℝ =>
        gradient V (WithLp.toLp 2 x : EuclideanSpace ℝ (Fin (n + 1))))
      (Set.Icc a b))
    (hgradf : ContinuousOn
      (fun x : Fin (n + 1) → ℝ =>
        gradient f (WithLp.toLp 2 x : EuclideanSpace ℝ (Fin (n + 1))))
      (Set.Icc a b)) :
    ContinuousOn
      (fun x : Fin (n + 1) → ℝ =>
        Real.exp (-V (WithLp.toLp 2 x : EuclideanSpace ℝ (Fin (n + 1)))) *
          (Laplacian.laplacian f
              (WithLp.toLp 2 x : EuclideanSpace ℝ (Fin (n + 1))) -
            inner ℝ
              (gradient V (WithLp.toLp 2 x : EuclideanSpace ℝ (Fin (n + 1))))
              (gradient f (WithLp.toLp 2 x : EuclideanSpace ℝ (Fin (n + 1))))))
      (Set.Icc a b) :=
  TechnicalLemmas.StochasticProcesses.Langevin.continuousOn_expNeg_langevinGenerator_rhs_of_components
    hV hlap hgradV hgradf

example {n : ℕ} {a b : Fin (n + 1) → ℝ}
    {V f : EuclideanSpace ℝ (Fin (n + 1)) → ℝ}
    (hV : ContDiff ℝ 1 V)
    (hf : ContDiff ℝ 2 f) :
    ContinuousOn
      (fun x : Fin (n + 1) → ℝ =>
        Real.exp (-V (WithLp.toLp 2 x : EuclideanSpace ℝ (Fin (n + 1)))) *
          (Laplacian.laplacian f
              (WithLp.toLp 2 x : EuclideanSpace ℝ (Fin (n + 1))) -
            inner ℝ
              (gradient V (WithLp.toLp 2 x : EuclideanSpace ℝ (Fin (n + 1))))
              (gradient f (WithLp.toLp 2 x : EuclideanSpace ℝ (Fin (n + 1))))))
      (Set.Icc a b) :=
  TechnicalLemmas.StochasticProcesses.Langevin.continuousOn_expNeg_langevinGenerator_rhs_of_contDiff
    hV hf

example {n : ℕ}
    (a b : Fin (n + 1) → ℝ)
    (V f : EuclideanSpace ℝ (Fin (n + 1)) → ℝ)
    (F' : (Fin (n + 1) → ℝ) →
      (Fin (n + 1) → ℝ) →L[ℝ] (Fin (n + 1) → ℝ))
    (hF : ∀ x ∈ Set.Icc a b,
      HasFDerivAt
        (fun z : Fin (n + 1) → ℝ => fun i =>
          Real.exp (-V (WithLp.toLp 2 z : EuclideanSpace ℝ (Fin (n + 1)))) *
            fderiv ℝ f (WithLp.toLp 2 z : EuclideanSpace ℝ (Fin (n + 1)))
              (EuclideanSpace.single i (1 : ℝ))) (F' x) x)
    (hV : ∀ x ∈ Set.Icc a b,
      DifferentiableAt ℝ V
        (WithLp.toLp 2 x : EuclideanSpace ℝ (Fin (n + 1))))
    (hfderiv : ∀ x ∈ Set.Icc a b,
      DifferentiableAt ℝ
        (fun y : EuclideanSpace ℝ (Fin (n + 1)) => fderiv ℝ f y)
        (WithLp.toLp 2 x : EuclideanSpace ℝ (Fin (n + 1))))
    (hf : ∀ x ∈ Set.Icc a b,
      DifferentiableAt ℝ f
        (WithLp.toLp 2 x : EuclideanSpace ℝ (Fin (n + 1))))
    (hV_cont : ContinuousOn
      (fun x : Fin (n + 1) → ℝ =>
        V (WithLp.toLp 2 x : EuclideanSpace ℝ (Fin (n + 1))))
      (Set.Icc a b))
    (hlap_cont : ContinuousOn
      (fun x : Fin (n + 1) → ℝ =>
        Laplacian.laplacian f (WithLp.toLp 2 x : EuclideanSpace ℝ (Fin (n + 1))))
      (Set.Icc a b))
    (hgradV_cont : ContinuousOn
      (fun x : Fin (n + 1) → ℝ =>
        gradient V (WithLp.toLp 2 x : EuclideanSpace ℝ (Fin (n + 1))))
      (Set.Icc a b))
    (hgradf_cont : ContinuousOn
      (fun x : Fin (n + 1) → ℝ =>
        gradient f (WithLp.toLp 2 x : EuclideanSpace ℝ (Fin (n + 1))))
      (Set.Icc a b)) :
    MeasureTheory.IntegrableOn (fun x => ∑ i, F' x (Pi.single i (1 : ℝ)) i)
      (Set.Icc a b) MeasureTheory.volume :=
  TechnicalLemmas.StochasticProcesses.Langevin.integrableOn_trace_expNeg_fderivCoordinateField_of_component_continuousOn
    a b V f F' hF hV hfderiv hf hV_cont hlap_cont hgradV_cont hgradf_cont

example {n : ℕ}
    (a b : Fin (n + 1) → ℝ)
    (V f : EuclideanSpace ℝ (Fin (n + 1)) → ℝ)
    (F' : (Fin (n + 1) → ℝ) →
      (Fin (n + 1) → ℝ) →L[ℝ] (Fin (n + 1) → ℝ))
    (hF : ∀ x ∈ Set.Icc a b,
      HasFDerivAt
        (fun z : Fin (n + 1) → ℝ => fun i =>
          Real.exp (-V (WithLp.toLp 2 z : EuclideanSpace ℝ (Fin (n + 1)))) *
            fderiv ℝ f (WithLp.toLp 2 z : EuclideanSpace ℝ (Fin (n + 1)))
              (EuclideanSpace.single i (1 : ℝ))) (F' x) x)
    (hV : ContDiff ℝ 1 V)
    (hf : ContDiff ℝ 2 f) :
    MeasureTheory.IntegrableOn (fun x => ∑ i, F' x (Pi.single i (1 : ℝ)) i)
      (Set.Icc a b) MeasureTheory.volume :=
  TechnicalLemmas.StochasticProcesses.Langevin.integrableOn_trace_expNeg_fderivCoordinateField_of_contDiff
    a b V f F' hF hV hf

example {n : ℕ}
    (a b : Fin (n + 1) → ℝ)
    (V f : EuclideanSpace ℝ (Fin (n + 1)) → ℝ)
    (hV : ContDiff ℝ 1 V)
    (hf : ContDiff ℝ 2 f) :
    MeasureTheory.IntegrableOn
      (fun x : Fin (n + 1) → ℝ =>
        ∑ i,
          (fderiv ℝ
            (fun z : Fin (n + 1) → ℝ => fun i =>
              Real.exp (-V (WithLp.toLp 2 z : EuclideanSpace ℝ (Fin (n + 1)))) *
                fderiv ℝ f (WithLp.toLp 2 z : EuclideanSpace ℝ (Fin (n + 1)))
                  (EuclideanSpace.single i (1 : ℝ))) x)
            (Pi.single i (1 : ℝ)) i)
      (Set.Icc a b) MeasureTheory.volume :=
  TechnicalLemmas.StochasticProcesses.Langevin.integrableOn_trace_expNeg_fderivCoordinateField_of_contDiff_fderiv
    a b V f hV hf

example {n : ℕ}
    {V f : EuclideanSpace ℝ (Fin (n + 1)) → ℝ} {C : ℝ}
    (hV : Continuous V)
    (hf : ContDiff ℝ 1 f)
    (hZ : (∫⁻ y : EuclideanSpace ℝ (Fin (n + 1)),
      ENNReal.ofReal (Real.exp (-V y)) ∂MeasureTheory.volume) ≠ ∞)
    (hf_bound : ∀ y, ‖fderiv ℝ f y‖ ≤ C) :
    MeasureTheory.Integrable
      (fun x : Fin (n + 1) → ℝ => fun i =>
        Real.exp (-V (WithLp.toLp 2 x : EuclideanSpace ℝ (Fin (n + 1)))) *
          fderiv ℝ f (WithLp.toLp 2 x : EuclideanSpace ℝ (Fin (n + 1)))
            (EuclideanSpace.single i (1 : ℝ))) MeasureTheory.volume :=
  TechnicalLemmas.StochasticProcesses.Langevin.integrable_expNeg_fderivCoordinateField_of_lintegral_expNeg_ne_top_of_fderiv_norm_le
    hV hf hZ hf_bound

example {n : ℕ}
    {V f : EuclideanSpace ℝ (Fin (n + 1)) → ℝ}
    (hV : ContDiff ℝ 1 V)
    (hf : ContDiff ℝ 2 f)
    (hf_support : HasCompactSupport f) :
    MeasureTheory.Integrable
      (fun y : EuclideanSpace ℝ (Fin (n + 1)) =>
        Real.exp (-V y) *
          (Laplacian.laplacian f y - inner ℝ (gradient V y) (gradient f y)))
      MeasureTheory.volume :=
  TechnicalLemmas.StochasticProcesses.Langevin.integrable_expNeg_langevinGenerator_rhs_of_contDiff_of_hasCompactSupport
    hV hf hf_support

example {n : ℕ}
    {V f : EuclideanSpace ℝ (Fin (n + 1)) → ℝ}
    (hV : ContDiff ℝ 1 V)
    (hf : ContDiff ℝ 2 f)
    (hf_support : HasCompactSupport f) :
    MeasureTheory.Integrable
      (fun x : Fin (n + 1) → ℝ =>
        Real.exp (-V (WithLp.toLp 2 x : EuclideanSpace ℝ (Fin (n + 1)))) *
          (Laplacian.laplacian f
              (WithLp.toLp 2 x : EuclideanSpace ℝ (Fin (n + 1))) -
            inner ℝ
              (gradient V (WithLp.toLp 2 x : EuclideanSpace ℝ (Fin (n + 1))))
              (gradient f (WithLp.toLp 2 x : EuclideanSpace ℝ (Fin (n + 1))))))
      MeasureTheory.volume :=
  TechnicalLemmas.StochasticProcesses.Langevin.integrable_expNeg_langevinGenerator_rhs_comp_toLp_of_contDiff_of_hasCompactSupport
    hV hf hf_support

example {n : ℕ}
    {V : EuclideanSpace ℝ (Fin (n + 1)) → ℝ}
    (hV : Continuous V)
    (hZ : (∫⁻ y : EuclideanSpace ℝ (Fin (n + 1)),
      ENNReal.ofReal (Real.exp (-V y)) ∂MeasureTheory.volume) ≠ ∞) :
    MeasureTheory.Integrable
      (fun x : Fin (n + 1) → ℝ =>
        Real.exp (-V (WithLp.toLp 2 x : EuclideanSpace ℝ (Fin (n + 1)))))
      MeasureTheory.volume :=
  TechnicalLemmas.StochasticProcesses.Langevin.integrable_expNeg_comp_toLp_of_lintegral_expNeg_ne_top
    hV hZ

example {n : ℕ}
    {V : EuclideanSpace ℝ (Fin (n + 1)) → ℝ}
    (hV : Continuous V)
    (hZ : (∫⁻ y : EuclideanSpace ℝ (Fin (n + 1)),
      ENNReal.ofReal (Real.exp (-V y)) ∂MeasureTheory.volume) ≠ ∞) :
    Tendsto
      (fun R : ℝ => ∫ x in
        {x : Fin (n + 1) → ℝ |
          R ≤ ‖(WithLp.toLp 2 x : EuclideanSpace ℝ (Fin (n + 1)))‖},
        Real.exp (-V (WithLp.toLp 2 x : EuclideanSpace ℝ (Fin (n + 1))))
          ∂MeasureTheory.volume)
      atTop (𝓝 0) :=
  TechnicalLemmas.StochasticProcesses.Langevin.tendsto_setIntegral_expNeg_norm_ge_comp_toLp_of_lintegral_expNeg_ne_top
    hV hZ

example {n : ℕ}
    (F : (Fin (n + 1) → ℝ) → Fin (n + 1) → ℝ)
    (hF : ContDiff ℝ 1 F)
    (hF_support : HasCompactSupport F) :
    ∫ x : Fin (n + 1) → ℝ,
        TechnicalLemmas.Analysis.Calculus.Divergence.coordinateDivergence
          (fun y : EuclideanSpace ℝ (Fin (n + 1)) =>
            (WithLp.toLp 2 (F (WithLp.ofLp y)) :
              EuclideanSpace ℝ (Fin (n + 1))))
          (WithLp.toLp 2 x : EuclideanSpace ℝ (Fin (n + 1))) = 0 :=
  TechnicalLemmas.Analysis.Calculus.Divergence.integral_coordinateDivergence_wrapped_eq_zero_of_contDiff_of_hasCompactSupport
    F hF hF_support

example {n : ℕ}
    {V f : EuclideanSpace ℝ (Fin (n + 1)) → ℝ}
    (hV : ContDiff ℝ 1 V)
    (hf : ContDiff ℝ 2 f)
    (hf_support : HasCompactSupport f) :
    ∫ y : EuclideanSpace ℝ (Fin (n + 1)),
        Real.exp (-V y) *
          (Laplacian.laplacian f y - inner ℝ (gradient V y) (gradient f y)) = 0 :=
  TechnicalLemmas.StochasticProcesses.Langevin.integral_expNeg_langevinGenerator_rhs_eq_zero_of_contDiff_of_hasCompactSupport
    hV hf hf_support

example {n : ℕ} {f : EuclideanSpace ℝ (Fin (n + 1)) → ℝ} :
    TechnicalLemmas.StochasticProcesses.LangevinGenerator.CompactlySupportedC2 f ↔
      ContDiff ℝ 2 f ∧ HasCompactSupport f :=
  Iff.rfl

example {n : ℕ} (V f : EuclideanSpace ℝ (Fin (n + 1)) → ℝ) (x) :
    TechnicalLemmas.StochasticProcesses.LangevinGenerator.operator V f x =
      Laplacian.laplacian f x - inner ℝ (gradient V x) (gradient f x) :=
  rfl

example {n : ℕ}
    {V : EuclideanSpace ℝ (Fin (n + 1)) → ℝ}
    {A : (EuclideanSpace ℝ (Fin (n + 1)) → ℝ) →
      EuclideanSpace ℝ (Fin (n + 1)) → ℝ}
    {D : Set (EuclideanSpace ℝ (Fin (n + 1)) → ℝ)}
    (hcore : TechnicalLemmas.StochasticProcesses.LangevinGenerator.CoreContract V A D)
    {f : EuclideanSpace ℝ (Fin (n + 1)) → ℝ}
    (hf : TechnicalLemmas.StochasticProcesses.LangevinGenerator.CompactlySupportedC2 f) :
    f ∈ D :=
  hcore.core_mem_domain f hf

example {n : ℕ}
    {V f : EuclideanSpace ℝ (Fin (n + 1)) → ℝ}
    (hV : ContDiff ℝ 1 V)
    (hf : TechnicalLemmas.StochasticProcesses.LangevinGenerator.CompactlySupportedC2 f) :
    ∫ x, TechnicalLemmas.StochasticProcesses.LangevinGenerator.operator V f x
        ∂MeasureTheory.volume.withDensity
          (fun x =>
            (∫⁻ y, TechnicalLemmas.Measure.Gibbs.gibbsDensityENNReal V y
              ∂MeasureTheory.volume)⁻¹ *
              TechnicalLemmas.Measure.Gibbs.gibbsDensityENNReal V x) = 0 :=
  TechnicalLemmas.StochasticProcesses.LangevinGenerator.integral_operator_normalizedGibbs_eq_zero_on_compactlySupportedC2
    hV hf

example {E : Type*} [MeasurableSpace E]
    {P : ℝ → (E → ℝ) → E → ℝ}
    {A : (E → ℝ) → E → ℝ}
    {D : Set (E → ℝ)} {μ : MeasureTheory.Measure E}
    (hP : TechnicalLemmas.StochasticProcesses.WeakGenerator.IntegratedSemigroupGeneratorContract
      P A D μ)
    (hA : ∀ f ∈ D, ∫ x, A f x ∂μ = 0) :
    TechnicalLemmas.StochasticProcesses.WeakGenerator.IsInvariantOn P μ D :=
  TechnicalLemmas.StochasticProcesses.WeakGenerator.isInvariantOn_of_integral_generator_eq_zero
    hP hA

example {n : ℕ}
    {V : EuclideanSpace ℝ (Fin (n + 1)) → ℝ}
    {P : ℝ →
      (EuclideanSpace ℝ (Fin (n + 1)) → ℝ) →
        EuclideanSpace ℝ (Fin (n + 1)) → ℝ}
    {A :
      (EuclideanSpace ℝ (Fin (n + 1)) → ℝ) →
        EuclideanSpace ℝ (Fin (n + 1)) → ℝ}
    (hV : ContDiff ℝ 1 V)
    (hcore : TechnicalLemmas.StochasticProcesses.LangevinGenerator.CoreContract
      V A (Set.ofPred TechnicalLemmas.StochasticProcesses.LangevinGenerator.CompactlySupportedC2))
    (hsemigroup :
      TechnicalLemmas.StochasticProcesses.WeakGenerator.IntegratedSemigroupGeneratorContract
        P A
        (Set.ofPred TechnicalLemmas.StochasticProcesses.LangevinGenerator.CompactlySupportedC2)
        (MeasureTheory.volume.withDensity
          (fun x =>
            (∫⁻ y, TechnicalLemmas.Measure.Gibbs.gibbsDensityENNReal V y
              ∂MeasureTheory.volume)⁻¹ *
              TechnicalLemmas.Measure.Gibbs.gibbsDensityENNReal V x))) :
    TechnicalLemmas.StochasticProcesses.WeakGenerator.IsInvariantOn P
      (MeasureTheory.volume.withDensity
        (fun x =>
          (∫⁻ y, TechnicalLemmas.Measure.Gibbs.gibbsDensityENNReal V y
            ∂MeasureTheory.volume)⁻¹ *
            TechnicalLemmas.Measure.Gibbs.gibbsDensityENNReal V x))
      (Set.ofPred TechnicalLemmas.StochasticProcesses.LangevinGenerator.CompactlySupportedC2) :=
  TechnicalLemmas.StochasticProcesses.LangevinGenerator.isInvariantOn_normalizedGibbs_on_compactlySupportedC2
    hV hcore hsemigroup

example :
    @TechnicalLemmas.FunctionalInequalities.LogSobolev.lsiKlFiSqrtDensityFisherChainIntegralHandoffScalar =
      @lsiKlFiSqrtDensityFisherChainIntegralHandoffScalar := rfl

example {E : Type*} [MeasurableSpace E] [NormedAddCommGroup E]
    [InnerProductSpace ℝ E] [CompleteSpace E] (μ : Measure E) (f : E → ℝ) :
    TechnicalLemmas.FunctionalInequalities.Poincare.dirichletEnergy μ f =
      ∫ x, ‖gradient f x‖ ^ 2 ∂μ := rfl

example {E : Type*} [MeasurableSpace E] [NormedAddCommGroup E]
    [InnerProductSpace ℝ E] [CompleteSpace E]
    {μ : Measure E} {tests : Set (E → ℝ)} {C D : ℝ}
    (hC : TechnicalLemmas.FunctionalInequalities.Poincare.Satisfies μ tests C)
    (hCD : C ≤ D) :
    TechnicalLemmas.FunctionalInequalities.Poincare.Satisfies μ tests D :=
  TechnicalLemmas.FunctionalInequalities.Poincare.mono_constant hC hCD

example {E : Type*} [MeasurableSpace E] [NormedAddCommGroup E]
    [InnerProductSpace ℝ E] [CompleteSpace E]
    {μ : Measure E} {small large : Set (E → ℝ)} {C : ℝ}
    (hC : TechnicalLemmas.FunctionalInequalities.Poincare.Satisfies μ large C)
    (hsub : small ⊆ large) :
    TechnicalLemmas.FunctionalInequalities.Poincare.Satisfies μ small C :=
  TechnicalLemmas.FunctionalInequalities.Poincare.mono_tests hC hsub

example :
    @TechnicalLemmas.ProbabilityDistributions.Gaussian.integral_id_gaussianReal_zero =
      @TechnicalLemmas.Gaussian.integral_id_gaussianReal_zero := rfl

example :
    @TechnicalLemmas.Analysis.Calculus.Taylor.iteratedFDerivTwoOpNormOfFDerivFDerivOpNorm =
      @TechnicalLemmas.Taylor.iteratedFDerivTwoOpNormOfFDerivFDerivOpNorm := rfl

example {α β : Type*} [MeasurableSpace α] [MeasurableSpace β]
    (μ : Measure α) (ν : Measure β) [IsProbabilityMeasure μ] [IsProbabilityMeasure ν] :
    TechnicalLemmas.Measure.Transport.IsCoupling (μ.prod ν) μ ν :=
  TechnicalLemmas.Measure.Transport.isCoupling_prod μ ν

example {α β : Type*} [MeasurableSpace α] [MeasurableSpace β]
    {γ : Measure (α × β)} {μ : Measure α} {ν : Measure β}
    [IsProbabilityMeasure μ]
    (hγ : TechnicalLemmas.Measure.Transport.IsCoupling γ μ ν) :
    IsProbabilityMeasure γ :=
  TechnicalLemmas.Measure.Transport.isProbabilityMeasure_of_isCoupling_left hγ
