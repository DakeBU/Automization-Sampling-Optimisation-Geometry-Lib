import AutoSamplingTheory.TechnicalLemmas.Probability.SphereHaar
import AutoSamplingTheory.ExampleCases.GaussianComplexity.DeterminantComponents
import Mathlib.MeasureTheory.Measure.WithDensity
import Mathlib.Tactic.FunProp

open Matrix MeasureTheory Metric Set
open scoped ENNReal
open AutoSamplingTheory.TechnicalLemmas.Probability.OrthogonalHaar
open AutoSamplingTheory.TechnicalLemmas.Probability.SphereHaar
open AutoSamplingTheory.ExampleCases.GaussianComplexity.DeterminantComponents

namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarConditional

set_option autoImplicit false

abbrev O (n : ℕ) := Matrix.orthogonalGroup (Fin n) ℝ
abbrev E (n : ℕ) := EuclideanSpace ℝ (Fin n)
abbrev S (n : ℕ) := Metric.sphere (0 : E n) 1

noncomputable def sphereProbability (n : ℕ) : Measure (S n) :=
  let τ : Measure (S n) := (volume : Measure (E n)).toSphere
  (τ univ)⁻¹ • τ

theorem isProbabilityMeasure_sphereProbability (n : ℕ) [NeZero n] :
    IsProbabilityMeasure (sphereProbability n) := by
  let τ : Measure (S n) := (volume : Measure (E n)).toSphere
  let : NeZero τ := ⟨Measure.toSphere_ne_zero volume⟩
  change IsProbabilityMeasure ((τ univ)⁻¹ • τ)
  infer_instance

def detFiber (n : ℕ) (b : ℝ) : Set (O n) :=
  {W | (W : Matrix (Fin n) (Fin n) ℝ).det = b}

theorem measurableSet_detFiber (n : ℕ) (b : ℝ) : MeasurableSet (detFiber n b) :=
  (isClosed_eq (show Continuous (fun W : O n =>
    (W : Matrix (Fin n) (Fin n) ℝ).det) by fun_prop) continuous_const).measurableSet

noncomputable def componentHaar (n : ℕ) (b : ℝ) : Measure (O n) :=
  (2 : ℝ≥0∞) • (orthogonalHaar n).restrict (detFiber n b)

theorem isProbabilityMeasure_componentHaar {n : ℕ} (hn : 0 < n) {b : ℝ}
    (hb : b = -1 ∨ b = 1) : IsProbabilityMeasure (componentHaar n b) := by
  rcases hb with rfl | rfl
  · exact (component_probabilities hn).2.2.2
  · exact (component_probabilities hn).2.2.1

/-- Apply an orthogonal matrix to an actual point on the unit sphere. -/
noncomputable def rotate {n : ℕ} (R : O n) (z : S n) : S n :=
  let T := Matrix.toEuclideanCLM (𝕜 := ℝ) (n := Fin n)
  let A : unitary (E n →L[ℝ] E n) := ⟨T R.val, Unitary.map_mem T R.property⟩
  ⟨T R.val z.val, (mem_sphere_zero_iff_norm.mpr
    ((Unitary.linearIsometryEquiv A).norm_map z.val |>.trans
      (mem_sphere_zero_iff_norm.mp z.property)))⟩

theorem rotate_val {n : ℕ} (R : O n) (z : S n) :
    WithLp.ofLp (rotate R z).val = R.val *ᵥ WithLp.ofLp z.val := rfl

theorem continuous_rotate {n : ℕ} : Continuous (fun p : O n × S n => rotate p.1 p.2) := by
  apply Continuous.subtype_mk
  change Continuous (fun p : O n × S n => WithLp.toLp 2
    (fun i => ∑ k : Fin n, p.1.val i k * WithLp.ofLp p.2.val k))
  apply (PiLp.continuous_toLp 2 (fun _ : Fin n => ℝ)).comp
  apply continuous_pi
  intro i
  apply continuous_finsetSum
  intro k _
  exact ((continuous_subtype_val.comp continuous_fst).matrix_elem i k).mul
    ((continuous_apply k).comp ((PiLp.continuous_ofLp 2 (fun _ : Fin n => ℝ)).comp
      (continuous_subtype_val.comp continuous_snd)))

theorem rotate_mul {n : ℕ} (A B : O n) (z : S n) :
    rotate A (rotate B z) = rotate (A * B) z := by
  apply Subtype.ext
  apply (WithLp.equiv 2 (Fin n → ℝ)).injective
  change WithLp.ofLp (rotate A (rotate B z)).val =
    WithLp.ofLp (rotate (A * B) z).val
  rw [rotate_val, rotate_val, rotate_val, Matrix.mulVec_mulVec]
  rfl

def coordinatePoint {n : ℕ} (j : Fin n) : S n :=
  ⟨PiLp.single 2 j (1 : ℝ), by
    rw [mem_sphere_zero_iff_norm, PiLp.norm_single]
    norm_num⟩

theorem measurePreserving_rotate {n : ℕ} (j : Fin n) (R : O n) :
    MeasurePreserving (rotate R) (sphereProbability n) (sphereProbability n) := by
  let c : O n → S n := fun W => rotate W (coordinatePoint j)
  have hc : Measurable c := (continuous_rotate.comp
    (continuous_id.prodMk continuous_const)).measurable
  have hR : Measurable (rotate R) := (continuous_rotate.comp
    (continuous_const.prodMk continuous_id)).measurable
  have hval : MeasurableEmbedding (Subtype.val : S n → E n) :=
    MeasurableEmbedding.subtype_coe isClosed_sphere.measurableSet
  have hcol : (orthogonalHaar n).map c = sphereProbability n := by
    apply hval.map_injective
    rw [Measure.map_map hval.measurable hc, sphereProbability, Measure.map_smul]
    convert column_map_eq_normalized_surface j using 2
    funext W
    apply (WithLp.equiv 2 (Fin n → ℝ)).injective
    change WithLp.ofLp (rotate W (coordinatePoint j)).val = fun i => W.val i j
    rw [rotate_val]
    exact Matrix.mulVec_single_one _ _
  refine ⟨hR, ?_⟩
  rw [← hcol, Measure.map_map hR hc]
  have he : (rotate R) ∘ c = c ∘ (fun W => R * W) := by
    funext W
    exact rotate_mul R W (coordinatePoint j)
  rw [he, ← Measure.map_map hc (measurable_const_mul R), orthogonalHaar_map_mul_left]

/-- Product transport by a normalized base law and skew left Haar translations. -/
theorem map_prod_eq_haar_of_skew {m k : ℕ} {Z : Type*} [MeasurableSpace Z]
    (σ : Measure Z) [IsProbabilityMeasure σ]
    (F : Z × O k → O m) (hF : Measurable F)
    (g : O m → Z → Z) (hg : ∀ R, MeasurePreserving (g R) σ σ)
    (c : O m → Z → O k) (hc : ∀ R, Measurable (c R))
    (equivariance : ∀ R z v, F (g R z, c R z * v) = R * F (z,v)) :
    (σ.prod (orthogonalHaar k)).map F = orthogonalHaar m := by
  let ν := (σ.prod (orthogonalHaar k)).map F
  let := (orthogonalHaar_spec k).1
  let := (orthogonalHaar_spec m).1
  let := (orthogonalHaar_spec m).2.1
  let : IsProbabilityMeasure ν := Measure.isProbabilityMeasure_map hF.aemeasurable
  let : ν.IsMulLeftInvariant := ⟨fun R => by
    let t : Z × O k → Z × O k := fun p => (g R p.1, c R p.1 * p.2)
    have ht : MeasurePreserving t (σ.prod (orthogonalHaar k))
        (σ.prod (orthogonalHaar k)) := (hg R).skew_product
      (((hc R).comp measurable_fst).mul measurable_snd)
      (Filter.Eventually.of_forall fun z => orthogonalHaar_map_mul_left k (c R z))
    change Measure.map (fun W => R * W) ((σ.prod (orthogonalHaar k)).map F) = _
    rw [Measure.map_map (measurable_const_mul R) hF]
    have hcomp : (fun W => R * W) ∘ F = F ∘ t := by
      funext p
      exact (equivariance R p.1 p.2).symm
    rw [hcomp, ← Measure.map_map hF ht.measurable, ht.map_eq]⟩
  have hscale := Measure.isMulInvariant_eq_smul_of_compactSpace ν (orthogonalHaar m)
  have hfactor : Measure.haarScalarFactor ν (orthogonalHaar m) = 1 := by
    have h := congrArg (fun μ : Measure (O m) => μ univ) hscale
    simpa only [measure_univ, Measure.smul_apply, ENNReal.smul_def, smul_eq_mul,
      mul_one, ENNReal.coe_eq_one] using h.symm
  change ν = orthogonalHaar m
  rw [hscale, hfactor, one_smul]

/-- Restrict an assembled full Haar law using the exact determinant of its residual block. -/
theorem map_prod_component {m k : ℕ} {b : ℝ} {Z : Type*} [MeasurableSpace Z]
    (σ : Measure Z) [IsProbabilityMeasure σ]
    (F : Z × O k → O m) (hF : Measurable F)
    (hmap : (σ.prod (orthogonalHaar k)).map F = orthogonalHaar m)
    (hdet : ∀ p, F p ∈ detFiber m b ↔ p.2 ∈ detFiber k b) :
    (σ.prod (componentHaar k b)).map F = componentHaar m b := by
  let := (orthogonalHaar_spec k).1
  have hpre : F ⁻¹' detFiber m b = univ ×ˢ detFiber k b := by
    ext p
    simpa using hdet p
  have hrestrict :
      ((σ.prod (orthogonalHaar k)).restrict (univ ×ˢ detFiber k b)).map F =
        (orthogonalHaar m).restrict (detFiber m b) := by
    rw [← hpre, ← Measure.restrict_map hF (measurableSet_detFiber m b), hmap]
  have hprod :
      σ.prod ((orthogonalHaar k).restrict (detFiber k b)) =
        (σ.prod (orthogonalHaar k)).restrict (univ ×ˢ detFiber k b) := by
    simpa only [Measure.restrict_univ] using
      (Measure.prod_restrict (μ := σ) (ν := orthogonalHaar k) univ (detFiber k b))
  rw [componentHaar, componentHaar, Measure.prod_smul_right, Measure.map_smul,
    hprod, hrestrict]

theorem det_inv {n : ℕ} (W : O n) : W⁻¹.val.det = W.val.det := by
  have inv_eq : (W⁻¹ : O n).val = W.val.transpose := by
    ext i j
    rfl
  rw [inv_eq, Matrix.det_transpose]

/-- Inversion of orthogonal matrices preserves both normalized determinant components. -/
theorem componentHaar_map_inv (n : ℕ) (b : ℝ) :
    (componentHaar n b).map Inv.inv = componentHaar n b := by
  let μ := orthogonalHaar n
  let := (orthogonalHaar_spec n).1
  let := (orthogonalHaar_spec n).2.1
  let : μ.IsMulRightInvariant := ⟨fun W =>
    (orthogonalHaar_spec n).2.2 _
      (Measure.isProbabilityMeasure_map (measurable_mul_const W).aemeasurable)
      (Measure.isHaarMeasure_map_mul_right μ W)⟩
  let : IsProbabilityMeasure μ.inv :=
    Measure.isProbabilityMeasure_map (show Measurable (Inv.inv : O n → O n) from
      measurable_inv).aemeasurable
  have hscale := Measure.isMulInvariant_eq_smul_of_compactSpace μ.inv μ
  have hfactor : Measure.haarScalarFactor μ.inv μ = 1 := by
    have h := congrArg (fun ν : Measure (O n) => ν univ) hscale
    simpa only [measure_univ, Measure.smul_apply, ENNReal.smul_def, smul_eq_mul,
      mul_one, ENNReal.coe_eq_one] using h.symm
  have hinv : μ.map (Inv.inv : O n → O n) = μ := by
    change μ.inv = μ
    rw [hscale, hfactor, one_smul]
  have hpre : Inv.inv ⁻¹' detFiber n b = detFiber n b := by
    ext W
    change (W⁻¹ : O n).val.det = b ↔ W.val.det = b
    rw [det_inv]
  have hrestriction :
      (μ.map (Inv.inv : O n → O n)).restrict (detFiber n b) =
        (μ.restrict (detFiber n b)).map Inv.inv := by
    rw [Measure.restrict_map measurable_inv (measurableSet_detFiber n b), hpre]
  change ((2 : ℝ≥0∞) • μ.restrict (detFiber n b)).map Inv.inv = _
  rw [Measure.map_smul, ← hrestriction, hinv]
  rfl

end AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarConditional
