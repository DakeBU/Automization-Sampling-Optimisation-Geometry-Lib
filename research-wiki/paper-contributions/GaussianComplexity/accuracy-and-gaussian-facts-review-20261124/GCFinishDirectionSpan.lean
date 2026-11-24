import GCFinishDirection

noncomputable section
open MeasureTheory ProbabilityTheory
open scoped RealInnerProductSpace
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarConditional
namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumCoupling

private theorem ae_projection_ne_zero {d : ℕ} (K : Submodule ℝ (E d)) (hK : Module.finrank ℝ K < d) :
    ∀ᵐ x ∂stdGaussian (E d), Kᗮ.orthogonalProjectionOnto x ≠ 0 := by
  let m := Module.finrank ℝ Kᗮ
  have hm := K.finrank_add_finrank_orthogonal
  rw [finrank_euclideanSpace_fin] at hm
  have : NeZero m := ⟨by dsimp [m]; omega⟩
  let w : Kᗮ := (stdOrthonormalBasis ℝ Kᗮ) (0 : Fin m)
  have hw : ‖w‖ = 1 := (stdOrthonormalBasis ℝ Kᗮ).norm_eq_one _
  let L := innerSL ℝ (w : E d)
  have hL : ‖L‖ = 1 := (innerSL_apply_norm ℝ (w : E d)).trans hw
  have hmap : (stdGaussian (E d)).map L = gaussianReal 0 1 := by
    rw [IsGaussian.map_eq_gaussianReal L,integral_strongDual_stdGaussian,variance_dual_stdGaussian,hL]
    norm_num
  have hpres : MeasurePreserving L (stdGaussian (E d)) (gaussianReal 0 1) := ⟨L.continuous.measurable,hmap⟩
  let := nullSingletonClass_gaussianReal (μ := (0 : ℝ)) (v := 1) one_ne_zero
  have hne : ∀ᵐ t ∂gaussianReal 0 1, t ≠ 0 := by simp [ae_iff]
  filter_upwards [hpres.quasiMeasurePreserving.ae hne] with x hx
  intro h
  apply hx
  change inner ℝ (w : E d) x = 0
  rw [← Kᗮ.inner_orthogonalProjectionOnto_eq_of_mem_left w x, h, inner_zero_right]

/-- Both conclusions of Fact C.4 on an arbitrary probability space with the given laws. -/
theorem gaussianize_uniform_complement {d : ℕ} (K : Submodule ℝ (E d)) (hK : Module.finrank ℝ K < d)
    {Ω : Type*} [MeasurableSpace Ω] (μ : Measure Ω) [IsProbabilityMeasure μ] (Z v : Ω → E d)
    (hZ : MeasurePreserving Z μ (stdGaussian (E d))) (hv : MeasurePreserving v μ (complementSphere K))
    (hi : IndepFun Z v μ) :
    let g := fun ω => K.starProjection (Z ω) + ‖Kᗮ.orthogonalProjectionOnto (Z ω)‖ • v ω
    MeasurePreserving g μ (stdGaussian (E d)) ∧
    ∀ᵐ ω ∂μ, v ω ∈ K ⊔ Submodule.span ℝ {g ω} := by
  let F (p : E d × E d) := K.starProjection p.1 + ‖Kᗮ.orthogonalProjectionOnto p.1‖ • p.2
  have hF : Continuous F := (K.starProjection.continuous.comp continuous_fst).add
    ((Kᗮ.orthogonalProjectionOnto.continuous.comp continuous_fst).norm.smul continuous_snd)
  have hpair : MeasurePreserving (fun ω => (Z ω,v ω)) μ ((stdGaussian (E d)).prod (complementSphere K)) := by
    refine ⟨hZ.measurable.prodMk hv.measurable, ?_⟩
    rw [hi.map_prod_eq_prod_map_map hZ.measurable.aemeasurable hv.measurable.aemeasurable, hZ.map_eq, hv.map_eq]
  refine ⟨(show MeasurePreserving F _ _ from ⟨hF.measurable,subspace_gaussianize_map K hK⟩).comp hpair, ?_⟩
  filter_upwards [hZ.quasiMeasurePreserving.ae (ae_projection_ne_zero K hK)] with ω hω
  let U := K ⊔ Submodule.span ℝ {F (Z ω,v ω)}
  let a := ‖Kᗮ.orthogonalProjectionOnto (Z ω)‖
  have ha : a ≠ 0 := norm_ne_zero_iff.mpr hω
  have h1 : F (Z ω,v ω) ∈ U := (show Submodule.span ℝ {F (Z ω,v ω)} ≤ U from le_sup_right) (Submodule.subset_span (Set.mem_singleton _))
  have h2 : K.starProjection (Z ω) ∈ U := (show K ≤ U from le_sup_left) (K.orthogonalProjectionOnto (Z ω)).property
  have h3 : a • v ω ∈ U := by simpa [F,a] using U.sub_mem h1 h2
  simpa only [← mul_smul, inv_mul_cancel₀ ha,one_smul] using U.smul_mem a⁻¹ h3

#print axioms gaussianize_uniform_complement
end AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumCoupling
