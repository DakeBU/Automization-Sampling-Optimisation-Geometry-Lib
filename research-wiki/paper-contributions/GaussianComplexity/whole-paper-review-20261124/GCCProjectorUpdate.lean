import GCCIntrinsicSupport
import GCCProjectionGeometry
import GCCSpanAll

noncomputable section
open Matrix MeasureTheory
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarConditional
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarFrames
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarPosterior
open AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumCoupling
open AutoSamplingTheory.ExampleCases.GaussianComplexity.MeasurableFrames
namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarRevelation

attribute [local instance] matrixMeasurable matrixBorel matrixSecond

/-- Joining a history-measurable subspace to the line of a history-measurable vector
preserves projector measurability on every history, including the zero vector. -/
theorem measurable_projection_sup_line {H : Type*} [MeasurableSpace H] {N : ℕ}
    (V : H → Submodule ℝ (E N)) (hV : Measurable (fun a => projectionMatrix (V a)))
    (x : H → E N) (hx : Measurable x) :
    Measurable (fun a => projectionMatrix (V a ⊔ ℝ ∙ (x a))) := by
  obtain ⟨F,hF,hobs⟩ := measurable_public_chart V (fun _ => 1) hV (by simpa using hV)
  let raw (a : H) := (x a).ofLp
  let G (a : H) := nextPublic (F a) false (raw a) (raw a)
  have hr : Measurable raw := (PiLp.continuous_ofLp 2 _).measurable.comp hx
  have hG : Measurable G := measurable_nextPublic hF false hr hr
  have hm := measurable_fst.comp ((measurable_observationOf N).comp hG)
  convert hm using 1
  funext a
  let old := (F a).2
  have eo := (hobs a).2
  have part : (1 : O N) ∈ Set.range old.realize := by
    rw [range_realize_eq_compatible]
    change (1 : O N).val * (observationOf old).1 = (observationOf old).2
    rw [show observationOf old = _ from eo]
  obtain ⟨w,ew⟩ := part
  have ha : response false (old.realize w) (raw a) = raw a := by
    rw [ew]; exact Matrix.one_mulVec _
  have en := nextPublic_exposed_eq (F a) w false (raw a)
  change exposedSpace (nextPublic (F a) false (raw a) (response false (old.realize w) (raw a))).2.domain
    (nextPublic (F a) false (raw a) (response false (old.realize w) (raw a))).2.rank =
    exposedSpace old.domain old.rank ⊔ ℝ ∙ (raw a) at en
  rw [ha] at en
  let g := (WithLp.linearEquiv 2 ℝ (Vec N)).symm
  have h (D : O N) (r : ℕ) : (exposedSpace D r).map g.toLinearMap = exposedEuclidean D r :=
    Submodule.map_equiv_eq_comap_symm g _
  have hg : exposedEuclidean (G a).2.domain (G a).2.rank =
      exposedEuclidean old.domain old.rank ⊔ ℝ ∙ (x a) := by
    rw [← h,show exposedSpace (G a).2.domain (G a).2.rank = _ from en,Submodule.map_sup,h,
      Submodule.map_span,Set.image_singleton]
    rfl
  have ep := congrArg Prod.fst eo
  change (MeasurableFrames.frameObservation old.rank (old.domain,old.range)).1 = projectionMatrix (V a) at ep
  rw [frameObservation_projection] at ep
  let M := Matrix.toEuclideanCLM (𝕜 := ℝ) (n := Fin N)
  have e : (exposedEuclidean old.domain old.rank).starProjection = (V a).starProjection := M.symm.injective ep
  have eV : exposedEuclidean old.domain old.rank = V a := by
    rw [← Submodule.range_starProjection (exposedEuclidean old.domain old.rank),
      ← Submodule.range_starProjection (V a),e]
  change projectionMatrix (V a ⊔ ℝ ∙ x a) =
    (MeasurableFrames.frameObservation (G a).2.rank ((G a).2.domain,(G a).2.range)).1
  rw [frameObservation_projection,hg,eV]

#print axioms measurable_projection_sup_line
end AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarRevelation
