import B3PrimitiveQuery
import HaarOrientedSection
import Mathlib.Probability.Distributions.Gaussian.Multivariate

/-! Gaussianization of a fresh uniform direction in the unrevealed frame (Fact C.4). -/

noncomputable section
open Matrix MeasureTheory ProbabilityTheory
open AutoSamplingTheory.TechnicalLemmas.Probability.OrthogonalHaar
open AutoSamplingTheory.TechnicalLemmas.Probability.SphereHaar
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarConditional
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarFrames
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarPosterior

namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumCoupling

theorem map_of_fiber_laws {A B C T : Type*} [MeasurableSpace A] [MeasurableSpace B]
    [MeasurableSpace C] [MeasurableSpace T] (μ : Measure A) (ν : Measure B) (η : Measure C)
    [SFinite ν] [SFinite η] {f : A × B → T} {g : A × C → T}
    (hf : Measurable f) (hg : Measurable g)
    (h : ∀ a, ν.map (fun b => f (a,b)) = η.map (fun c => g (a,c))) :
    (μ.prod ν).map f = (μ.prod η).map g := by
  ext t ht
  rw [Measure.map_apply hf ht, Measure.map_apply hg ht, Measure.prod_apply (hf ht),
    Measure.prod_apply (hg ht)]
  apply lintegral_congr
  intro a
  have ha := congrArg (fun m : Measure T => m t) (h a)
  have hf' : Measurable (fun b => f (a,b)) := hf.comp measurable_prodMk_left
  have hg' : Measurable (fun c => g (a,c)) := hg.comp measurable_prodMk_left
  change (ν.map (fun b => f (a,b))) t = (η.map (fun c => g (a,c))) t at ha
  rw [Measure.map_apply hf' ht, Measure.map_apply hg' ht] at ha
  exact ha

/-- The orbit of every unit vector under a full Haar rotation is normalized surface measure. -/
theorem haar_rotate_fixed {m : ℕ} [NeZero m] (u : S m) :
    (orthogonalHaar m).map (fun W => rotate W u) = sphereProbability m := by
  let e := coordinatePoint (0 : Fin m)
  let w := (ℝ ∙ (e.val - u.val))ᗮ.reflection
  let b := EuclideanSpace.basisFun (Fin m) ℝ
  let Q : O m := ⟨w.toMatrix b.toBasis b.toBasis, w.toMatrix_mem_unitaryGroup b b⟩
  have hw : w e.val = u.val := Submodule.reflection_sub
    ((mem_sphere_zero_iff_norm.mp e.property).trans
      (mem_sphere_zero_iff_norm.mp u.property).symm)
  have hQ : rotate Q e = u := by
    apply Subtype.ext
    apply (WithLp.equiv 2 (Fin m → ℝ)).injective
    have hm := LinearMap.toMatrix_mulVec_repr b.toBasis b.toBasis w.toLinearEquiv.toLinearMap e.val
    exact hm.trans (congrArg WithLp.ofLp hw)
  let c := fun W : O m => rotate W e
  have hc : Measurable c := (continuous_rotate.comp (continuous_id.prodMk continuous_const)).measurable
  have hright : (orthogonalHaar m).map (fun W => W * Q) = orthogonalHaar m := by
    let := (orthogonalHaar_spec m).1
    let := (orthogonalHaar_spec m).2.1
    exact (orthogonalHaar_spec m).2.2 _
      (Measure.isProbabilityMeasure_map (measurable_mul_const Q).aemeasurable)
      (Measure.isHaarMeasure_map_mul_right (orthogonalHaar m) Q)
  have he : (fun W => rotate W u) = c ∘ (fun W => W * Q) := by
    funext W
    rw [← hQ, rotate_mul]
    rfl
  rw [he, ← Measure.map_map hc (measurable_mul_const Q), hright]
  have hv : MeasurableEmbedding (Subtype.val : S m → E m) :=
    MeasurableEmbedding.subtype_coe Metric.isClosed_sphere.measurableSet
  apply hv.map_injective
  rw [Measure.map_map hv.measurable hc, sphereProbability, Measure.map_smul]
  convert column_map_eq_normalized_surface (0 : Fin m) using 2
  funext W
  apply (WithLp.equiv 2 (Fin m → ℝ)).injective
  change WithLp.ofLp (rotate W (coordinatePoint 0)).val = fun i => W.val i 0
  rw [rotate_val]
  exact Matrix.mulVec_single_one _ _

/-- Orthogonal changes of frame preserve the entire standard Gaussian. -/
theorem stdGaussian_act {d : ℕ} (D : O d) :
    (stdGaussian (E d)).map (Matrix.toEuclideanCLM (𝕜 := ℝ) D.val) = stdGaussian (E d) := by
  let U : unitary (E d →L[ℝ] E d) :=
    ⟨_, Unitary.map_mem (Matrix.toEuclideanCLM (𝕜 := ℝ) (n := Fin d)) D.property⟩
  exact stdGaussian_map (Unitary.linearIsometryEquiv U)

/-- Keep the exposed coordinates and residual norm of a fresh Gaussian and replace the
residual direction by a fresh uniform unit vector in the latent frame. -/
def gaussianize {m r : ℕ} (D : O (m+r)) (x : E (m+r)) (z : S m) : E (m+r) :=
  WithLp.toLp 2 (encodeResponse D (exposedCoords m r (WithLp.ofLp x))
    ‖WithLp.toLp 2 (residualCoords m r (WithLp.ofLp x))‖ z)

theorem measurable_gaussianize {m r : ℕ} (D : O (m+r)) :
    Measurable (Function.uncurry (gaussianize D)) := by
  have hx := (PiLp.continuous_ofLp 2 (fun _ : Fin (m+r) => ℝ)).measurable.comp
    (measurable_fst : Measurable (Prod.fst : E (m+r) × S m → E (m+r)))
  exact (PiLp.continuous_toLp 2 (fun _ : Fin (m+r) => ℝ)).measurable.comp
    (measurable_encodeResponse measurable_const ((continuous_exposedCoords m r).measurable.comp hx)
      (((PiLp.continuous_toLp 2 (fun _ : Fin m => ℝ)).measurable.comp
        ((continuous_residualCoords m r).measurable.comp hx)).norm) measurable_snd)

set_option maxHeartbeats 1200000 in
set_option backward.isDefEq.respectTransparency false in
theorem gaussianize_law {m r : ℕ} [NeZero m] (D : O (m+r)) :
    ((stdGaussian (E (m+r))).prod (sphereProbability m)).map (Function.uncurry (gaussianize D)) =
      stdGaussian (E (m+r)) := by
  let γ := stdGaussian (E (m+r))
  let ν := orthogonalHaar m
  let : IsProbabilityMeasure ν := (orthogonalHaar_spec m).1
  let := isProbabilityMeasure_sphereProbability m
  let f (x : E (m+r)) (W : O m) : E (m+r) :=
    Matrix.toEuclideanCLM (𝕜 := ℝ) (D * prefixEmbed m r W).val x
  have hf : Measurable (Function.uncurry f) := by
    exact (PiLp.continuous_toLp 2 (fun _ : Fin (m+r) => ℝ)).measurable.comp
      ((continuous_act _).measurable.comp
        ((measurable_const.mul ((continuous_prefixEmbed m r).measurable.comp measurable_snd)).prodMk
          ((PiLp.continuous_ofLp 2 (fun _ : Fin (m+r) => ℝ)).measurable.comp measurable_fst)))
  have horbit (x : E (m+r)) : (sphereProbability m).map (gaussianize D x) = ν.map (f x) := by
    let a := exposedCoords m r (WithLp.ofLp x)
    let c := WithLp.toLp 2 (residualCoords m r (WithLp.ofLp x))
    obtain ⟨u,hu⟩ : ∃ u : S m, ‖c‖ • WithLp.ofLp u.val = WithLp.ofLp c := by
      by_cases h : c = 0
      · exact ⟨coordinatePoint 0, by simp [h]⟩
      · exact ⟨residualUnit ⟨c,h⟩, scaled_residualUnit ⟨c,h⟩⟩
    have heq : (gaussianize D x) ∘ (fun W => rotate W u) = f x := by
      funext W
      apply (WithLp.equiv 2 (Fin (m+r) → ℝ)).injective
      change act D (splitVec r a (‖c‖ • (WithLp.ofLp (rotate W u).val))) =
        act (D * prefixEmbed m r W) (WithLp.ofLp x)
      rw [rotate_val, ← Matrix.mulVec_smul, hu, act_mul]
      apply congrArg (act D)
      conv_rhs => rw [← splitVec_coords m r (WithLp.ofLp x), act_prefixEmbed]
      rfl
    have hG : Measurable (gaussianize D x) := (measurable_gaussianize D).comp measurable_prodMk_left
    have hW : Measurable (fun W : O m => rotate W u) :=
      (continuous_rotate.comp (continuous_id.prodMk continuous_const)).measurable
    rw [← haar_rotate_fixed u, Measure.map_map hG hW, heq]
  rw [map_of_fiber_laws γ (sphereProbability m) ν (measurable_gaussianize D) hf horbit]
  have hh := Measure.measurePreserving_swap (μ := ν) (ν := γ)
  rw [← hh.map_eq, Measure.map_map hf measurable_swap]
  let h : O m × E (m+r) → E (m+r) := Function.uncurry f ∘ Prod.swap
  have hs : Measurable h := Measurable.comp (g := Function.uncurry f) (f := Prod.swap) hf measurable_swap
  have he (W : O m) : γ.map (fun x => h (W,x)) = γ.map (fun x => (W,x).2) := by
    change (stdGaussian (E (m+r))).map (Matrix.toEuclideanCLM (𝕜 := ℝ)
      (D * prefixEmbed m r W).val) = (stdGaussian (E (m+r))).map id
    rw [stdGaussian_act, Measure.map_id]
  change (ν.prod γ).map h = γ
  rw [map_of_fiber_laws ν γ γ (g := Prod.snd) hs measurable_snd he, Measure.map_snd_prod,
    measure_univ, one_smul]

end AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumCoupling
