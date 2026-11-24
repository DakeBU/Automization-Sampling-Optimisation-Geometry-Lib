import GC43Gaussian
import Mathlib.Analysis.InnerProductSpace.ProdL2

/-! Fact C.4 for every proper subspace of Euclidean space. -/
noncomputable section
open MeasureTheory ProbabilityTheory Matrix
open scoped RealInnerProductSpace
open AutoSamplingTheory.TechnicalLemmas.Probability.OrthogonalHaar
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarConditional
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarFrames
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarPosterior

namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumCoupling

variable {d : ℕ}

/-- Uniform unit direction in the orthogonal complement, as a measure on ambient vectors.
An orthonormal coordinate isometry transports normalized surface measure. -/
def complementSphere (K : Submodule ℝ (E d)) : Measure (E d) :=
  let b := (stdOrthonormalBasis ℝ Kᗮ).repr
  (sphereProbability (Module.finrank ℝ Kᗮ)).map (fun u => Kᗮ.subtypeL (b.symm u.val))

private def orthogonalAction {m : ℕ} (W : O m) : E m ≃ₗᵢ[ℝ] E m :=
  Unitary.linearIsometryEquiv
    (⟨Matrix.toEuclideanCLM (𝕜 := ℝ) W.val,
      Unitary.map_mem (Matrix.toEuclideanCLM (𝕜 := ℝ) (n := Fin m)) W.property⟩ :
      unitary (E m →L[ℝ] E m))

private theorem continuous_orthogonalAction (m : ℕ) :
    Continuous (fun p : O m × E m => orthogonalAction p.1 p.2) := by
  change Continuous (fun p : O m × E m => WithLp.toLp 2
    (act p.1 (WithLp.ofLp p.2)))
  exact (PiLp.continuous_toLp 2 _).comp ((continuous_act _).comp
    (continuous_fst.prodMk ((PiLp.continuous_ofLp 2 _).comp continuous_snd)))

set_option maxHeartbeats 1000000 in
set_option backward.isDefEq.respectTransparency false in
/-- Keeping the projection and replacing the complementary direction with an independent
uniform direction preserves the full Gaussian law. -/
theorem subspace_gaussianize_map (K : Submodule ℝ (E d)) (hK : Module.finrank ℝ K < d) :
    ((stdGaussian (E d)).prod (complementSphere K)).map
      (fun p => K.starProjection p.1 + ‖Kᗮ.orthogonalProjectionOnto p.1‖ • p.2) =
      stdGaussian (E d) := by
  let m := Module.finrank ℝ Kᗮ
  have hm := K.finrank_add_finrank_orthogonal
  rw [finrank_euclideanSpace_fin] at hm
  have : NeZero m := ⟨by dsimp [m]; omega⟩
  let b := (stdOrthonormalBasis ℝ Kᗮ).repr
  let c (x : E d) := b (Kᗮ.orthogonalProjectionOnto x)
  let j (y : E m) := Kᗮ.subtypeL (b.symm y)
  let F (p : E d × E d) := K.starProjection p.1 + ‖Kᗮ.orthogonalProjectionOnto p.1‖ • p.2
  let G (p : E d × O m) := K.starProjection p.1 + j (orthogonalAction p.2 (c p.1))
  have hc : Continuous c := b.continuous.comp Kᗮ.orthogonalProjectionOnto.continuous
  have hj : Continuous j := Kᗮ.subtypeL.continuous.comp b.symm.continuous
  have hF : Continuous F := by
    unfold F
    fun_prop
  have hG : Continuous G := by
    let f (p : E d × O m) : O m × E m := (p.2, c p.1)
    have hf : Continuous f := by
      unfold f
      exact continuous_snd.prodMk (hc.comp continuous_fst)
    have hr : Continuous ((fun p : O m × E m => orthogonalAction p.1 p.2) ∘ f) :=
      Continuous.comp (continuous_orthogonalAction m) hf
    have hout := Continuous.comp hj hr
    have hleft : Continuous (fun p : E d × O m => K.starProjection p.1) := by fun_prop
    exact Continuous.add hleft hout
  let ν := orthogonalHaar m
  let γ := stdGaussian (E d)
  let : IsProbabilityMeasure ν := (orthogonalHaar_spec m).1
  let := isProbabilityMeasure_sphereProbability m
  let u (z : S m) := j z.val
  have hu : Measurable u := (hj.comp continuous_subtype_val).measurable
  have huLaw : (sphereProbability m).map u = complementSphere K := rfl
  have : IsProbabilityMeasure (complementSphere K) := by
    rw [← huLaw]
    exact Measure.isProbabilityMeasure_map (μ := sphereProbability m) hu.aemeasurable
  have hfiber (x : E d) : (complementSphere K).map (fun v => F (x,v)) =
      ν.map (fun W => G (x,W)) := by
    obtain ⟨z,hz⟩ : ∃ z : S m, ‖c x‖ • z.val = c x := by
      by_cases hx : c x = 0
      · exact ⟨coordinatePoint 0, by simp [hx]⟩
      · refine ⟨residualUnit ⟨c x,hx⟩, ?_⟩
        exact (WithLp.equiv 2 (Fin m → ℝ)).injective (scaled_residualUnit ⟨c x,hx⟩)
    have hrot : Measurable (fun W : O m => rotate W z) :=
      (continuous_rotate.comp (continuous_id.prodMk continuous_const)).measurable
    have hFx : Measurable (fun v => F (x,v)) := hF.measurable.comp measurable_prodMk_left
    rw [← huLaw, Measure.map_map hFx hu, ← haar_rotate_fixed z, Measure.map_map (hFx.comp hu) hrot]
    congr 1
    funext W
    change K.starProjection x + ‖Kᗮ.orthogonalProjectionOnto x‖ •
      Kᗮ.subtypeL (b.symm (orthogonalAction W z.val)) = _
    rw [show ‖Kᗮ.orthogonalProjectionOnto x‖ = ‖c x‖ from (b.norm_map _).symm,
      ← map_smul, ← map_smul, ← map_smul, hz]
  change (γ.prod (complementSphere K)).map F = γ
  rw [map_of_fiber_laws γ (complementSphere K) ν hF.measurable hG.measurable hfiber]
  have hswap := Measure.measurePreserving_swap (μ := ν) (ν := γ)
  rw [← hswap.map_eq, Measure.map_map hG.measurable measurable_swap]
  have hfiber' (W : O m) : γ.map (fun x => (G ∘ Prod.swap) (W,x)) = γ.map (fun x => (W,x).2) := by
    let U := b.trans ((orthogonalAction W).trans b.symm)
    let A := K.orthogonalDecomposition.trans (((LinearIsometryEquiv.refl ℝ K).withLpProdCongr 2 U).trans
      K.orthogonalDecomposition.symm)
    have hA (x : E d) : A x = G (x,W) := by
      simp only [A, LinearIsometryEquiv.trans_apply, Submodule.orthogonalDecomposition_apply,
        LinearIsometryEquiv.withLpProdCongr_apply, Submodule.orthogonalDecomposition_symm_apply]
      rfl
    rw [show (fun x => (G ∘ Prod.swap) (W,x)) = A from funext (fun x => (hA x).symm),
      stdGaussian_map]
    exact Measure.map_id.symm
  rw [map_of_fiber_laws ν γ γ (g := Prod.snd) (hG.measurable.comp measurable_swap) measurable_snd hfiber',
    Measure.map_snd_prod, measure_univ, one_smul]

end AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumCoupling
