import AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.GaussianMarginalGradient
import AutoSamplingTheory.ExampleCases.ProximalBPS.MacroscopicEnergy

namespace Tests.ProximalBPSGaussianMarginalGradient
noncomputable section
set_option autoImplicit false
set_option maxHeartbeats 800000
open MeasureTheory ProbabilityTheory InnerProductSpace
open scoped ContDiff RealInnerProductSpace NNReal
open AutoSamplingTheory.ExampleCases.ProximalBPS
open AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities

-- Use the SAME actual PBPS mu/J/nu, with probability produced by the actual
-- macroscopic-energy theorem. Exercise real L2 representatives in the graph.
theorem actual_pbps_compact_gradient_graph
    {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]
    {V : E → ℝ} {α β : ℝ≥0} {η : ℝ}
    (hα : 0 < (α : ℝ)) (hαβ : α ≤ β) (hV : ContDiff ℝ 2 V)
    (hH : ∀ x a : E,
      (α : ℝ) * ‖a‖^2 ≤ (fderiv ℝ (fderiv ℝ V) x a) a ∧
      (fderiv ℝ (fderiv ℝ V) x a) a ≤ (β : ℝ) * ‖a‖^2)
    (hη : 0 < η) (hβη : (β : ℝ) * η ≤ 1) :
    let μ := (volume : Measure E).tilted (fun x => -V x)
    let J := (μ.prod (stdGaussian E)).map
      (fun p : E × E => (p.1,p.1+Real.sqrt η • p.2))
    let ν := J.snd
    IsProbabilityMeasure ν ∧
      ∃ D : Lp ℝ 2 ν →ₗ.[ℝ] Lp E 2 ν,
        Dense (D.domain : Set (Lp ℝ 2 ν)) ∧ D.IsClosable ∧ D.closure.IsClosed ∧
        ∀ f : E → ℝ, ContDiff ℝ ∞ f → HasCompactSupport f →
          ∃ (u : Lp ℝ 2 ν) (v : Lp E 2 ν),
            u =ᵐ[ν] f ∧ v =ᵐ[ν] gradient f ∧ (u,v) ∈ D.graph := by
  let μ := (volume : Measure E).tilted (fun x => -V x)
  let J := (μ.prod (stdGaussian E)).map
    (fun p : E × E => (p.1,p.1+Real.sqrt η • p.2))
  let ν := J.snd
  have hactual := MacroscopicEnergy.actual_macroscopic_gradient_energy_blocks
    hα hαβ hV hH hη hβη
  letI : IsProbabilityMeasure μ := hactual.1
  have hν : IsProbabilityMeasure ν := hactual.2.2.1
  letI := hν
  obtain ⟨D,hDense,hCl,hClosed,hgraph⟩ :=
    GaussianMarginalGradient.gaussian_marginal_gradient_closable μ hη
  refine ⟨hν,D,hDense,hCl,hClosed,?_⟩
  intro f hf hfc
  have hf2 : MemLp f 2 ν := hf.continuous.memLp_of_hasCompactSupport hfc
  have hgc : HasCompactSupport (gradient f) := by
    refine HasCompactSupport.of_support_subset_isCompact hfc.isCompact ?_
    intro x hx
    by_contra hn
    exact hx (by simp [gradient,fderiv_of_notMem_tsupport ℝ hn])
  have hgrad :=
    AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Gradient.continuous_gradient_of_contDiff_one
      (contDiff_infty.mp hf 1)
  have hg2 : MemLp (gradient f) 2 ν := hgrad.memLp_of_hasCompactSupport hgc
  refine ⟨hf2.toLp f,hg2.toLp (gradient f),hf2.coeFn_toLp,hg2.coeFn_toLp,?_⟩
  exact (hgraph _ _).mpr ⟨f,hf,hfc,hf2.coeFn_toLp,hg2.coeFn_toLp⟩

-- In rank zero the NONCENTERED constant1 is genuinely compact and has mean1.
-- Its actual scalar class and the zero vector class belong to the SAME D.graph.
theorem rank_zero_noncentered_graph :
    let E := EuclideanSpace ℝ (Fin 0)
    let V := fun x : E => (1/2 : ℝ)*‖x‖^2
    let μ := (volume : Measure E).tilted (fun x => -V x)
    let J := (μ.prod (stdGaussian E)).map
      (fun p : E × E => (p.1,p.1+Real.sqrt 1 • p.2))
    let ν := J.snd
    ∃ D : Lp ℝ 2 ν →ₗ.[ℝ] Lp E 2 ν,
      Dense (D.domain : Set (Lp ℝ 2 ν)) ∧ D.IsClosable ∧ D.closure.IsClosed ∧
      ∃ u : Lp ℝ 2 ν,
        u =ᵐ[ν] (fun _ => (1 : ℝ)) ∧ (∫ y, u y ∂ν) = 1 ∧
          (u,(0 : Lp E 2 ν)) ∈ D.graph := by
  let E := EuclideanSpace ℝ (Fin 0)
  let V := fun x : E => (1/2 : ℝ)*‖x‖^2
  have hV : ContDiff ℝ 2 V := contDiff_const.mul (contDiff_id.norm_sq (𝕜 := ℝ))
  have hfd (x : E) : fderiv ℝ V x = innerSL ℝ x := by
    have h := ((hasFDerivAt_id x).norm_sq).const_mul (1/2 : ℝ)
    convert h.fderiv using 1 <;> first | rfl | (ext v; simp)
  have hH (x a : E) : fderiv ℝ (fderiv ℝ V) x a a = ‖a‖^2 := by
    rw [show fderiv ℝ V = innerSL ℝ from funext hfd]
    rw [(innerSL ℝ (E := E)).hasFDerivAt.fderiv]
    exact real_inner_self_eq_norm_sq a
  let μ := (volume : Measure E).tilted (fun x => -V x)
  let J := (μ.prod (stdGaussian E)).map
    (fun p : E × E => (p.1,p.1+Real.sqrt 1 • p.2))
  let ν := J.snd
  obtain ⟨hν,D,hDense,hCl,hClosed,hf⟩ :=
    actual_pbps_compact_gradient_graph (V := V) (α := 1) (β := 1) (η := 1)
      (by norm_num) (by rfl) hV
      (by intro x a; simp only [hH,NNReal.coe_one,one_mul]; exact ⟨le_rfl,le_rfl⟩)
      (by norm_num) (by norm_num)
  letI : IsProbabilityMeasure ν := hν
  have hfc : HasCompactSupport (fun _ : E => (1 : ℝ)) :=
    (isClosed_tsupport _).isCompact
  obtain ⟨u,v,hu,hv,hgraph⟩ := hf (fun _ => 1) contDiff_const hfc
  have hv0 : v = 0 := by
    apply Lp.ext
    filter_upwards [hv] with x hx
    simpa [gradient] using hx
  have hmean : (∫ y, u y ∂ν) = 1 := by
    calc
      (∫ y, u y ∂ν) = ∫ _ : E, (1 : ℝ) ∂ν := integral_congr_ae hu
      _ = 1 := by
        simp only [integral_const,Measure.real,measure_univ,ENNReal.toReal_one,one_smul]
  refine ⟨D,hDense,hCl,hClosed,u,hu,hmean,?_⟩
  simpa only [hv0] using hgraph

#print axioms GaussianMarginalGradient.gaussian_marginal_gradient_closable
#print axioms actual_pbps_compact_gradient_graph
#print axioms rank_zero_noncentered_graph
end
end Tests.ProximalBPSGaussianMarginalGradient
