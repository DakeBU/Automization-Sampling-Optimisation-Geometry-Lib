import GCCIntrinsicState
import GCCProjectionGeometry

noncomputable section
open Matrix MeasureTheory
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarFrames
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarConditional
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarPosterior
open AutoSamplingTheory.ExampleCases.GaussianComplexity.MeasurableFrames
namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarRevelation

attribute [local instance] matrixMeasurable matrixBorel matrixSecond

private theorem complement_projection {N : ℕ} (U : Submodule ℝ (E N)) :
    projectionMatrix Uᗮ = 1 - projectionMatrix U := by
  let M := Matrix.toEuclideanCLM (𝕜 := ℝ) (n := Fin N)
  change M.symm Uᗮ.starProjection = 1 - M.symm U.starProjection
  rw [Submodule.starProjection_orthogonal',map_sub,map_one]

private theorem projector_identifies_space {N : ℕ} {U V : Submodule ℝ (E N)}
    (he : projectionMatrix U = projectionMatrix V) : U = V := by
  let M := Matrix.toEuclideanCLM (𝕜 := ℝ) (n := Fin N)
  have h := M.symm.injective he
  change U.starProjection = V.starProjection at h
  rw [← Submodule.range_starProjection U,← Submodule.range_starProjection V,h]

private theorem complement_chart {N : ℕ} {H : Type*} [MeasurableSpace H]
    (U : H → Submodule ℝ (E N)) (hU : Measurable (fun a => projectionMatrix (U a))) :
    ∃ D : H → PublicFrame N, Measurable D ∧ ∀ a,
      (D a).1 = Module.finrank ℝ (U a) ∧
        (exposedEuclidean (D a).2.domain (D a).2.rank)ᗮ = U a := by
  have hc : Measurable (fun a => projectionMatrix (U a)ᗮ) := by
    simp only [complement_projection]
    exact measurable_const.sub hU
  obtain ⟨D,hD,he⟩ := measurable_public_chart (fun a => (U a)ᗮ) (fun _ => 1) hc (by simpa using hc)
  refine ⟨D,hD,fun a => ?_⟩
  obtain ⟨rk,ob⟩ := he a
  have hd := (U a).finrank_add_finrank_orthogonal
  rw [finrank_euclideanSpace_fin] at hd
  have fit := (D a).2.fits
  refine ⟨by omega,?_⟩
  have p := congrArg Prod.fst ob
  change (MeasurableFrames.frameObservation (D a).2.rank ((D a).2.domain,(D a).2.range)).1 =
    projectionMatrix (U a)ᗮ at p
  rw [frameObservation_projection] at p
  rw [projector_identifies_space p, Submodule.orthogonal_orthogonal]

/-- Two independently specified measurable random subspaces of the same dimension admit
jointly measurable orthogonal coordinates for their unknown directions. The common
residual dimension may vary with history. Only the two projectors are input. -/
theorem measurable_two_subspace_frames {N : ℕ} {H : Type*} [MeasurableSpace H]
    (U V : H → Submodule ℝ (E N))
    (hU : Measurable (fun a => projectionMatrix (U a)))
    (hV : Measurable (fun a => projectionMatrix (V a)))
    (dim : ∀ a, Module.finrank ℝ (U a) = Module.finrank ℝ (V a)) :
    ∃ F : H → PublicFrame N, Measurable F ∧ ∀ a,
      (F a).1 = Module.finrank ℝ (U a) ∧
      (exposedEuclidean (F a).2.domain (F a).2.rank)ᗮ = U a ∧
      (exposedEuclidean (F a).2.range (F a).2.rank)ᗮ = V a := by
  obtain ⟨D,hD,hd⟩ := complement_chart U hU
  obtain ⟨R,hR,hr⟩ := complement_chart V hV
  let join (a : H) (C : PublicFrame N) : PublicFrame N :=
    ⟨C.1,⟨C.2.rank,C.2.fits,C.2.domain,(R a).2.domain⟩⟩
  have measurable_join : Measurable (fun a => join a (D a)) := by
    apply PublicFrame.measurable_cases D hD join
    intro m hm
    exact (PublicFrame.measurable_tag m).comp (PublicFrame.measurable_blockFrame
      (PublicFrame.measurable_domain.comp hD) (PublicFrame.measurable_domain.comp hR))
  refine ⟨fun a => join a (D a),measurable_join,fun a => ⟨(hd a).1,(hd a).2,?_⟩⟩
  have eqm := (hd a).1.trans ((dim a).trans (hr a).1.symm)
  have hdf := (D a).2.fits
  have hrf := (R a).2.fits
  have eqr : (D a).2.rank = (R a).2.rank := by omega
  change (exposedEuclidean (R a).2.domain (D a).2.rank)ᗮ = V a
  rw [eqr]
  exact (hr a).2

#print axioms measurable_two_subspace_frames
end AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarRevelation
