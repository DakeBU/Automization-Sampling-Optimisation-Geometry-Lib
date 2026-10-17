import AutoSamplingTheory.TechnicalLemmas.Probability.OrthogonalHaar
import Mathlib.MeasureTheory.Constructions.HaarToSphere
import Mathlib.MeasureTheory.Measure.Haar.InnerProductSpace
import Mathlib.Analysis.InnerProductSpace.Projection.Reflection
import Mathlib.MeasureTheory.Integral.Prod
open Matrix MeasureTheory
open AutoSamplingTheory.TechnicalLemmas.Probability.OrthogonalHaar
namespace AutoSamplingTheory.TechnicalLemmas.Probability.SphereHaar
set_option autoImplicit false
/-!
Canonical actual full-orthogonal Haar column law on Euclidean space.
The surface measure is derived from actual Euclidean volume by the cone
construction and finite nonzero normalization. No invariant-law identity,
conditional law or Poisson evaluation is assumed.
-/
open Set Metric
open scoped Pointwise ENNReal
theorem column_map_eq_normalized_surface {n : ℕ} (j : Fin n) :
    let τ : Measure (Metric.sphere (0 : EuclideanSpace ℝ (Fin n)) 1) :=
      (volume : Measure (EuclideanSpace ℝ (Fin n))).toSphere
    let σ : Measure (EuclideanSpace ℝ (Fin n)) :=
      (τ Set.univ)⁻¹ • τ.map (fun y => y.val)
    (orthogonalHaar n).map
      (fun O : Matrix.orthogonalGroup (Fin n) ℝ => WithLp.toLp 2 (fun i => (O : Matrix (Fin n) (Fin n) ℝ) i j)) = σ := by
  classical
  let : NeZero n := ⟨by have := j.isLt; omega⟩
  let E := EuclideanSpace ℝ (Fin n)
  let G := Matrix.orthogonalGroup (Fin n) ℝ
  let S := Metric.sphere (0 : E) 1
  let τ : Measure S := (volume : Measure E).toSphere
  let σ : Measure E := (τ univ)⁻¹ • τ.map Subtype.val
  let c : G → E := fun O => WithLp.toLp 2 (fun i => (O : Matrix (Fin n) (Fin n) ℝ) i j)
  let T : G → E →L[ℝ] E := fun O =>
    Matrix.toEuclideanCLM (𝕜 := ℝ) (n := Fin n) (O : Matrix (Fin n) (Fin n) ℝ)
  let μ := orthogonalHaar n
  let ν : Measure E := μ.map c
  have hc : Continuous c :=
    (PiLp.continuous_toLp 2 (fun _ : Fin n => ℝ)).comp
      (continuous_pi (fun i => continuous_subtype_val.matrix_elem i j))
  let := (orthogonalHaar_spec n).1
  let : NeZero τ := ⟨Measure.toSphere_ne_zero volume⟩
  let ρ : Measure S := (τ univ)⁻¹ • τ
  have hρ : IsProbabilityMeasure ρ := inferInstance
  have hσ : σ = ρ.map Subtype.val := by rw [Measure.map_smul]
  let := hρ
  have hσprob : IsProbabilityMeasure σ := by
    rw [hσ]
    exact Measure.isProbabilityMeasure_map measurable_subtype_coe.aemeasurable
  let := hσprob
  have hσsphere : ∀ᵐ y ∂σ, ‖y‖ = 1 := by
    rw [hσ]
    apply (ae_map_iff measurable_subtype_coe.aemeasurable
      (isClosed_eq continuous_norm continuous_const).measurableSet).2
    exact Filter.Eventually.of_forall (fun y => mem_sphere_zero_iff_norm.mp y.property)
  have hσiso (Q : E ≃ₗᵢ[ℝ] E) : σ.map Q = σ := by
    classical
    let E := EuclideanSpace ℝ (Fin n)
    let S := Metric.sphere (0 : E) 1
    let τ : Measure S := (volume : Measure E).toSphere
    let q : S → S := fun y => ⟨Q y, by
      change Q (y : E) ∈ Metric.sphere (0 : E) 1
      rw [mem_sphere_zero_iff_norm, Q.norm_map]
      exact mem_sphere_zero_iff_norm.mp y.property⟩
    have hq : Measurable q := (Q.continuous.comp continuous_subtype_val).subtype_mk _ |>.measurable
    have hτ : τ.map q = τ := by
      ext t ht
      rw [Measure.map_apply hq ht]
      change (volume : Measure E).toSphere (q ⁻¹' t) = (volume : Measure E).toSphere t
      rw [Measure.toSphere_apply' _ (ht.preimage hq), Measure.toSphere_apply' _ ht]
      congr 1
      have hc : Ioo (0 : ℝ) 1 • (Subtype.val '' (q ⁻¹' t)) =
          Q ⁻¹' (Ioo (0 : ℝ) 1 • (Subtype.val '' t)) := by
        ext x
        constructor
        · rintro ⟨a, ha, z, ⟨y, hy, rfl⟩, rfl⟩
          exact ⟨a, ha, Q y, ⟨q y, hy, rfl⟩, (Q.map_smul a y).symm⟩
        · rintro ⟨a, ha, z, ⟨y, hy, rfl⟩, hxy⟩
          let w : S := ⟨Q.symm y, by
            change Q.symm (y : E) ∈ Metric.sphere (0 : E) 1
            rw [mem_sphere_zero_iff_norm, Q.symm.norm_map]
            exact mem_sphere_zero_iff_norm.mp y.property⟩
          have hw : q w = y := by apply Subtype.ext; exact Q.apply_symm_apply y
          refine ⟨a, ha, Q.symm y, ⟨w, ?_, rfl⟩, ?_⟩
          · change q w ∈ t
            rw [hw]
            exact hy
          · apply Q.injective
            simpa using hxy
      rw [hc]
      exact Q.measurePreserving.measure_preimage_emb Q.toHomeomorph.measurableEmbedding _
    change ((τ univ)⁻¹ • τ.map Subtype.val).map Q = (τ univ)⁻¹ • τ.map Subtype.val
    rw [Measure.map_smul, Measure.map_map Q.continuous.measurable measurable_subtype_coe]
    have he : (Q : E → E) ∘ Subtype.val = Subtype.val ∘ q := rfl
    rw [he, ← Measure.map_map measurable_subtype_coe hq, hτ]
  have hσinv (O : G) : σ.map (T O) = σ := by
    let u : unitary (E →L[ℝ] E) :=
      ⟨T O, Unitary.map_mem (Matrix.toEuclideanCLM (𝕜 := ℝ) (n := Fin n)) O.property⟩
    exact hσiso (Unitary.linearIsometryEquiv u)
  have horbit : ∀ y : E, ‖y‖ = 1 → μ.map (fun O : G => T O y) = ν := by
    classical
    let E := EuclideanSpace ℝ (Fin n)
    let G := Matrix.orthogonalGroup (Fin n) ℝ
    let j0 : Fin n := j
    let c : G → E := fun O => WithLp.toLp 2 (fun i => (O : Matrix (Fin n) (Fin n) ℝ) i j0)
    let T : G → E →L[ℝ] E := fun O =>
      Matrix.toEuclideanCLM (𝕜 := ℝ) (n := Fin n) (O : Matrix (Fin n) (Fin n) ℝ)
    let e0 : E := PiLp.single 2 j0 (1 : ℝ)
    have hc : Continuous c :=
      (PiLp.continuous_toLp 2 (fun _ : Fin n => ℝ)).comp
        (continuous_pi (fun i => continuous_subtype_val.matrix_elem i j0))
    have he (O : G) : T O e0 = c O := by
      apply (WithLp.equiv 2 (Fin n → ℝ)).injective
      change (O : Matrix (Fin n) (Fin n) ℝ) *ᵥ Pi.single j0 1 = fun i =>
        (O : Matrix (Fin n) (Fin n) ℝ) i j0
      rw [Matrix.mulVec_single_one]
      rfl
    have hr (Q : G) : (orthogonalHaar n).map (fun O => O * Q) = orthogonalHaar n := by
      let := (orthogonalHaar_spec n).1
      let := (orthogonalHaar_spec n).2.1
      exact (orthogonalHaar_spec n).2.2 _
        (Measure.isProbabilityMeasure_map (measurable_mul_const Q).aemeasurable)
        (Measure.isHaarMeasure_map_mul_right (orthogonalHaar n) Q)
    change ∀ y : E, ‖y‖ = 1 → (orthogonalHaar n).map (fun O : G => T O y) = (orthogonalHaar n).map c
    intro y hy
    let w : E ≃ₗᵢ[ℝ] E := (ℝ ∙ (e0 - y))ᗮ.reflection
    let b := EuclideanSpace.basisFun (Fin n) ℝ
    let Q : G := ⟨w.toMatrix b.toBasis b.toBasis, w.toMatrix_mem_unitaryGroup b b⟩
    have hw : w e0 = y := Submodule.reflection_sub (by
      change ‖(PiLp.single 2 j0 (1 : ℝ) : E)‖ = ‖y‖
      rw [PiLp.norm_single]
      simpa using hy.symm)
    have hQ : T Q e0 = y := by
      apply (WithLp.equiv 2 (Fin n → ℝ)).injective
      have hm := LinearMap.toMatrix_mulVec_repr b.toBasis b.toBasis w.toLinearEquiv.toLinearMap e0
      change (Q : Matrix (Fin n) (Fin n) ℝ) *ᵥ WithLp.ofLp e0 = WithLp.ofLp (w e0) at hm
      exact hm.trans (congrArg WithLp.ofLp hw)
    have hm (O : G) : T O y = c (O * Q) := by
      rw [← hQ, ← he]
      change (Matrix.toEuclideanCLM (𝕜 := ℝ) (n := Fin n) (O : Matrix (Fin n) (Fin n) ℝ))
        ((Matrix.toEuclideanCLM (𝕜 := ℝ) (n := Fin n) (Q : Matrix (Fin n) (Fin n) ℝ)) e0) =
        (Matrix.toEuclideanCLM (𝕜 := ℝ) (n := Fin n)
          ((O : Matrix (Fin n) (Fin n) ℝ) * (Q : Matrix (Fin n) (Fin n) ℝ))) e0
      rw [map_mul]
      rfl
    change (orthogonalHaar n).map (fun O => T O y) = (orthogonalHaar n).map c
    calc
      _ = (orthogonalHaar n).map (c ∘ fun O => O * Q) := by congr 1; funext O; exact hm O
      _ = ((orthogonalHaar n).map (fun O => O * Q)).map c :=
        (Measure.map_map hc.measurable (measurable_mul_const Q)).symm
      _ = _ := by rw [hr]
  have hact : Continuous (fun p : G × E => T p.1 p.2) := by
    change Continuous (fun p : G × E => WithLp.toLp 2
      (fun i => ∑ k : Fin n, (p.1 : Matrix (Fin n) (Fin n) ℝ) i k * WithLp.ofLp p.2 k))
    apply (PiLp.continuous_toLp 2 (fun _ : Fin n => ℝ)).comp
    apply continuous_pi
    intro i
    apply continuous_finsetSum
    intro k _
    exact ((continuous_subtype_val.comp continuous_fst).matrix_elem i k).mul
      ((continuous_apply k).comp
        ((PiLp.continuous_ofLp 2 (fun _ : Fin n => ℝ)).comp continuous_snd))
  change ν = σ
  ext t ht
  let g : E → ℝ≥0∞ := t.indicator (fun _ => 1)
  have hg : Measurable g := measurable_const.indicator ht
  have hgint (η : Measure E) : (∫⁻ x, g x ∂η) = η t := by
    simp [g, lintegral_indicator ht]
  have hleft (O : G) : (∫⁻ y, g (T O y) ∂σ) = σ t := by
    rw [← lintegral_map hg (T O).continuous.measurable, hσinv, hgint]
  have hright : ∀ᵐ y ∂σ, (∫⁻ O : G, g (T O y) ∂μ) = ν t := by
    filter_upwards [hσsphere] with y hy
    have hymeas : Measurable (fun O : G => T O y) :=
      (hact.comp (continuous_id.prodMk (continuous_const (y := y)))).measurable
    rw [← lintegral_map hg hymeas, horbit y hy, hgint]
  calc
    ν t = ∫⁻ y : E, ∫⁻ O : G, g (T O y) ∂μ ∂σ := by
      rw [lintegral_congr_ae hright]
      simp
    _ = ∫⁻ O : G, ∫⁻ y : E, g (T O y) ∂σ ∂μ :=
      (lintegral_lintegral_swap (μ := μ) (ν := σ)
        (f := fun O : G => fun y : E => g (T O y))
        (hg.comp hact.measurable).aemeasurable).symm
    _ = σ t := by
      simp_rw [hleft]
      rw [lintegral_const, (orthogonalHaar_spec n).1.measure_univ, mul_one]

end AutoSamplingTheory.TechnicalLemmas.Probability.SphereHaar
