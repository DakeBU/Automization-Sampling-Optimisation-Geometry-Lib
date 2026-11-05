import AutoSamplingTheory.TechnicalLemmas.Analysis.Harmonic.SphericalFlux
import AutoSamplingTheory.TechnicalLemmas.Probability.SphereHaar
import Mathlib.Analysis.Calculus.ParametricIntegral
import Mathlib.Analysis.Calculus.Deriv.MeanValue

/-!
Closed-ball spherical mean value with an actual harmonic extension. The direct
radial-mean proof consumes the canonical all-subradius zero-flux theorem.
The normalized law is the existing literal volume.toSphere law.
-/

open MeasureTheory Metric Set Filter Matrix
open scoped Topology RealInnerProductSpace

namespace AutoSamplingTheory.TechnicalLemmas.Analysis.Harmonic.SphericalMeanValue

set_option autoImplicit false
noncomputable section

private def sphereRotation {n : ℕ} (Q : Matrix.orthogonalGroup (Fin n) ℝ)
    (ζ : sphere (0 : EuclideanSpace ℝ (Fin n)) 1) :
    sphere (0 : EuclideanSpace ℝ (Fin n)) 1 :=
  ⟨Matrix.toEuclideanCLM (𝕜 := ℝ) (n := Fin n)
      (Q : Matrix (Fin n) (Fin n) ℝ) ζ.1, by
    let u : unitary (EuclideanSpace ℝ (Fin n) →L[ℝ] EuclideanSpace ℝ (Fin n)) :=
      ⟨_, Unitary.map_mem (Matrix.toEuclideanCLM (𝕜 := ℝ) (n := Fin n)) Q.property⟩
    apply mem_sphere_zero_iff_norm.mpr
    change ‖(Unitary.linearIsometryEquiv u) ζ.1‖ = 1
    rw [(Unitary.linearIsometryEquiv u).norm_map]
    exact mem_sphere_zero_iff_norm.mp ζ.property⟩

private theorem normalized_sphere_law {n : ℕ} (hn : 2 ≤ n) :
    let τ := (volume : Measure (EuclideanSpace ℝ (Fin n))).toSphere
    let μ := (τ univ)⁻¹ • τ
    IsProbabilityMeasure μ ∧
      ∀ Q : Matrix.orthogonalGroup (Fin n) ℝ, μ.map (sphereRotation Q) = μ := by
  classical
  let E := EuclideanSpace ℝ (Fin n)
  let S := sphere (0 : E) 1
  let G := Matrix.orthogonalGroup (Fin n) ℝ
  let τ : Measure S := (volume : Measure E).toSphere
  let μ : Measure S := (τ univ)⁻¹ • τ
  let j : Fin n := ⟨0, by omega⟩
  let c : G → E := fun O => WithLp.toLp 2
    (fun i => (O : Matrix (Fin n) (Fin n) ℝ) i j)
  let T : G → E →L[ℝ] E := fun O => Matrix.toEuclideanCLM
    (𝕜 := ℝ) (n := Fin n) (O : Matrix (Fin n) (Fin n) ℝ)
  let ν := Probability.OrthogonalHaar.orthogonalHaar n
  have hc : Continuous c :=
    (PiLp.continuous_toLp 2 (fun _ : Fin n => ℝ)).comp
      (continuous_pi (fun i => continuous_subtype_val.matrix_elem i j))
  have hcolumn : ν.map c = μ.map Subtype.val := by
    rw [Measure.map_smul]
    exact Probability.SphereHaar.column_map_eq_normalized_surface j
  let : IsProbabilityMeasure ν := (Probability.OrthogonalHaar.orthogonalHaar_spec n).1
  have hp : IsProbabilityMeasure (μ.map Subtype.val) := by
    rw [← hcolumn]
    exact Measure.isProbabilityMeasure_map hc.measurable.aemeasurable
  let := hp
  have hμ : IsProbabilityMeasure μ := Measure.isProbabilityMeasure_of_map Subtype.val
  refine ⟨hμ, ?_⟩
  intro Q
  let e0 : E := PiLp.single 2 j (1 : ℝ)
  have he (O : G) : T O e0 = c O := by
    apply (WithLp.equiv 2 (Fin n → ℝ)).injective
    change (O : Matrix (Fin n) (Fin n) ℝ) *ᵥ Pi.single j 1 =
      fun i => (O : Matrix (Fin n) (Fin n) ℝ) i j
    rw [Matrix.mulVec_single_one]
    rfl
  have hm (O : G) : T Q (c O) = c (Q * O) := by
    rw [← he O, ← he (Q * O)]
    change (Matrix.toEuclideanCLM (𝕜 := ℝ) (n := Fin n)
      (Q : Matrix (Fin n) (Fin n) ℝ))
        ((Matrix.toEuclideanCLM (𝕜 := ℝ) (n := Fin n)
          (O : Matrix (Fin n) (Fin n) ℝ)) e0) =
      (Matrix.toEuclideanCLM (𝕜 := ℝ) (n := Fin n)
        ((Q : Matrix (Fin n) (Fin n) ℝ) * (O : Matrix (Fin n) (Fin n) ℝ))) e0
    rw [map_mul]
    rfl
  have hrot : (μ.map Subtype.val).map (T Q) = μ.map Subtype.val := by
    rw [← hcolumn, Measure.map_map (T Q).continuous.measurable hc.measurable]
    have hcomp : (T Q) ∘ c = c ∘ (fun O : G => Q * O) := funext hm
    rw [hcomp, ← Measure.map_map hc.measurable (measurable_const_mul Q)]
    rw [Probability.OrthogonalHaar.orthogonalHaar_map_mul_left]
  have hq : Measurable (sphereRotation Q) :=
    ((T Q).continuous.comp continuous_subtype_val).subtype_mk _ |>.measurable
  apply (MeasurableEmbedding.subtype_coe
    (isClosed_sphere : IsClosed (sphere (0 : E) 1)).measurableSet).map_injective
  rw [Measure.map_map measurable_subtype_coe hq]
  change μ.map ((T Q) ∘ Subtype.val) = μ.map Subtype.val
  rw [← Measure.map_map (T Q).continuous.measurable measurable_subtype_coe]
  exact hrot

private theorem affine_sphere_mem {n : ℕ} (a : EuclideanSpace ℝ (Fin n))
    {R t : ℝ} (ht : t ∈ Icc 0 R)
    (ζ : sphere (0 : EuclideanSpace ℝ (Fin n)) 1) : a + t • ζ.1 ∈ closedBall a R := by
  have hζ := mem_sphere_zero_iff_norm.mp ζ.property
  simpa only [mem_closedBall, dist_eq_norm, add_sub_cancel_left, norm_smul,
    Real.norm_eq_abs, abs_of_nonneg ht.1, hζ, mul_one] using ht.2

private theorem sphere_section_continuous {n : ℕ}
    (v : EuclideanSpace ℝ (Fin n) → ℝ) (a : EuclideanSpace ℝ (Fin n))
    {R t : ℝ} (hv : InnerProductSpace.HarmonicOnNhd v (closedBall a R))
    (ht : t ∈ Icc 0 R) :
    Continuous (fun ζ : sphere (0 : EuclideanSpace ℝ (Fin n)) 1 => v (a + t • ζ.1)) := by
  apply continuous_iff_continuousAt.mpr
  intro ζ
  have hmap : ContinuousAt (fun η : sphere (0 : EuclideanSpace ℝ (Fin n)) 1 =>
      a + t • η.1) ζ := by fun_prop
  exact ContinuousAt.comp (f := fun η : sphere (0 : EuclideanSpace ℝ (Fin n)) 1 =>
      a + t • η.1) (x := ζ) (hv _ (affine_sphere_mem a ht ζ)).1.continuousAt hmap

private theorem spherical_mean_continuous {n : ℕ}
    (v : EuclideanSpace ℝ (Fin n) → ℝ) (a : EuclideanSpace ℝ (Fin n)) (R : ℝ)
    (hv : InnerProductSpace.HarmonicOnNhd v (closedBall a R))
    (μ : Measure (sphere (0 : EuclideanSpace ℝ (Fin n)) 1)) [IsFiniteMeasure μ] :
    ContinuousOn (fun t : ℝ => ∫ ζ, v (a + t • ζ.1) ∂μ) (Icc 0 R) := by
  rw [continuousOn_iff_continuous_domRestrict]
  change Continuous (fun t : Icc (0 : ℝ) R => ∫ ζ, v (a + t.1 • ζ.1) ∂μ)
  have hc : Continuous (Function.uncurry (fun (t : Icc (0 : ℝ) R)
      (ζ : sphere (0 : EuclideanSpace ℝ (Fin n)) 1) => v (a + t.1 • ζ.1))) := by
    apply continuous_iff_continuousAt.mpr
    intro p
    have hmap : ContinuousAt (fun q : Icc (0 : ℝ) R ×
        sphere (0 : EuclideanSpace ℝ (Fin n)) 1 => a + q.1.1 • q.2.1) p := by fun_prop
    exact ContinuousAt.comp (f := fun q : Icc (0 : ℝ) R ×
        sphere (0 : EuclideanSpace ℝ (Fin n)) 1 => a + q.1.1 • q.2.1) (x := p)
      (hv _ (affine_sphere_mem a p.1.property p.2)).1.continuousAt hmap
  simpa using continuous_parametric_integral_of_continuous (μ := μ) hc isCompact_univ

private theorem spherical_mean_hasDerivAt {n : ℕ}
    (v : EuclideanSpace ℝ (Fin n) → ℝ) (a : EuclideanSpace ℝ (Fin n)) (R : ℝ)
    (hv : InnerProductSpace.HarmonicOnNhd v (closedBall a R))
    (μ : Measure (sphere (0 : EuclideanSpace ℝ (Fin n)) 1)) [IsFiniteMeasure μ]
    {t : ℝ} (ht : t ∈ Ioo 0 R) :
    HasDerivAt (fun s : ℝ => ∫ ζ, v (a + s • ζ.1) ∂μ)
      (∫ ζ, inner ℝ (gradient v (a + t • ζ.1)) ζ.1 ∂μ) t := by
  let E := EuclideanSpace ℝ (Fin n)
  let S := sphere (0 : E) 1
  have hdc : ContinuousOn (fderiv ℝ v) (closedBall a R) := by
    intro x hx
    exact ((hv x hx).1.continuousAt_fderiv (by norm_num)).continuousWithinAt
  obtain ⟨C, hC⟩ := (isCompact_closedBall a R).exists_bound_of_continuousOn hdc
  have hFc (s : ℝ) (hs : s ∈ Icc 0 R) :
      Continuous (fun ζ : S => fderiv ℝ v (a + s • ζ.1) ζ.1) := by
    apply continuous_iff_continuousAt.mpr
    intro ζ
    have hmap : ContinuousAt (fun η : S => a + s • η.1) ζ := by fun_prop
    have hcomp := ContinuousAt.comp (f := fun η : S => a + s • η.1) (x := ζ)
      ((hv _ (affine_sphere_mem a hs ζ)).1.continuousAt_fderiv (by norm_num)) hmap
    exact hcomp.clm_apply continuous_subtype_val.continuousAt
  have hmeas : ∀ᶠ s in 𝓝 t, AEStronglyMeasurable
      (fun ζ : S => v (a + s • ζ.1)) μ := by
    filter_upwards [isOpen_Ioo.mem_nhds ht] with s hs
    exact (sphere_section_continuous v a hv (Ioo_subset_Icc_self hs)).aestronglyMeasurable
  have hint : Integrable (fun ζ : S => v (a + t • ζ.1)) μ :=
    (sphere_section_continuous v a hv (Ioo_subset_Icc_self ht)).integrable_of_hasCompactSupport
      (HasCompactSupport.of_compactSpace _)
  have hbound : ∀ᵐ ζ : S ∂μ, ∀ s ∈ Ioo 0 R,
      ‖fderiv ℝ v (a + s • ζ.1) ζ.1‖ ≤ C := by
    filter_upwards with ζ
    intro s hs
    calc
      _ ≤ ‖fderiv ℝ v (a + s • ζ.1)‖ * ‖ζ.1‖ :=
        (fderiv ℝ v (a + s • ζ.1)).le_opNorm _
      _ = ‖fderiv ℝ v (a + s • ζ.1)‖ := by
        rw [mem_sphere_zero_iff_norm.mp ζ.property, mul_one]
      _ ≤ C := hC _ (affine_sphere_mem a (Ioo_subset_Icc_self hs) ζ)
  have hdiff : ∀ᵐ ζ : S ∂μ, ∀ s ∈ Ioo 0 R,
      HasDerivAt (fun s : ℝ => v (a + s • ζ.1))
        (fderiv ℝ v (a + s • ζ.1) ζ.1) s := by
    filter_upwards with ζ
    intro s hs
    have harg : HasDerivAt (fun r : ℝ => a + r • ζ.1) ζ.1 s := by
      simpa using ((hasDerivAt_id s).smul_const ζ.1).const_add a
    exact HasFDerivAt.comp_hasDerivAt (f := fun r : ℝ => a + r • ζ.1) (x := s)
      ((hv _ (affine_sphere_mem a (Ioo_subset_Icc_self hs) ζ)).1.differentiableAt
        (by norm_num)).hasFDerivAt harg
  have hi := hasDerivAt_integral_of_dominated_loc_of_deriv_le
    (μ := μ) (F := fun s (ζ : S) => v (a + s • ζ.1))
    (F' := fun s (ζ : S) => fderiv ℝ v (a + s • ζ.1) ζ.1)
    (bound := fun _ : S => C) (isOpen_Ioo.mem_nhds ht) hmeas hint
    (hFc t (Ioo_subset_Icc_self ht)).aestronglyMeasurable hbound (integrable_const C) hdiff
  simpa only [← inner_gradient_left] using hi.2

/-- Real closed-ball spherical mean value. Off-ball values of the original
function are unrestricted; all derivatives use one actual harmonic extension. -/
theorem harmonic_closedBall_mean_value {n : ℕ} (hn : 2 ≤ n)
    (u : EuclideanSpace ℝ (Fin n) → ℝ)
    (a : EuclideanSpace ℝ (Fin n)) (r : ℝ) (hr : 0 < r)
    (hu : ∃ v : EuclideanSpace ℝ (Fin n) → ℝ,
      InnerProductSpace.HarmonicOnNhd v (Metric.closedBall a r) ∧
      Set.EqOn v u (Metric.closedBall a r)) :
    let τ : MeasureTheory.Measure (Metric.sphere (0 : EuclideanSpace ℝ (Fin n)) 1) :=
      (MeasureTheory.volume : MeasureTheory.Measure (EuclideanSpace ℝ (Fin n))).toSphere
    (∫ ζ : Metric.sphere (0 : EuclideanSpace ℝ (Fin n)) 1,
      u (a + r • (ζ : EuclideanSpace ℝ (Fin n))) ∂((τ Set.univ)⁻¹ • τ)) = u a := by
  let E := EuclideanSpace ℝ (Fin n)
  let S := sphere (0 : E) 1
  let τ : Measure S := (volume : Measure E).toSphere
  let μ : Measure S := (τ univ)⁻¹ • τ
  have hlaw := normalized_sphere_law hn
  let : IsProbabilityMeasure μ := hlaw.1
  change (∫ ζ : S, u (a + r • ζ.1) ∂μ) = u a
  obtain ⟨v, hv, hvu, hflux⟩ :=
    SphericalFlux.harmonic_closedBall_zero_flux hn u a r hr hu
  let M : ℝ → ℝ := fun t => ∫ ζ : S, v (a + t • ζ.1) ∂μ
  have hM : ContinuousOn M (Icc 0 r) := spherical_mean_continuous v a r hv μ
  have hd (t : ℝ) (ht : t ∈ Ioo 0 r) : HasDerivAt M 0 t := by
    have hzero : (∫ ζ : S, inner ℝ (gradient v (a + t • ζ.1)) ζ.1 ∂μ) = 0 := by
      dsimp only [μ]
      rw [integral_smul_measure, (hflux t ht.1 ht.2.le).2, smul_zero]
    have hstep : HasDerivAt M
        (∫ ζ : S, inner ℝ (gradient v (a + t • ζ.1)) ζ.1 ∂μ) t :=
      spherical_mean_hasDerivAt v a r hv μ ht
    rw [hzero] at hstep
    exact hstep
  obtain ⟨c, hc, hslope⟩ := exists_hasDerivAt_eq_slope M (fun _ => 0) hr hM hd
  have hconstant : M r = M 0 := by
    have hz : (M r - M 0) / r = 0 := by simpa using hslope.symm
    exact sub_eq_zero.mp (((div_eq_zero_iff).mp hz).resolve_right hr.ne')
  have hcenter : M 0 = v a := by simp [M]
  have hsample : (fun ζ : S => v (a + r • ζ.1)) =ᵐ[μ]
      (fun ζ : S => u (a + r • ζ.1)) := by
    filter_upwards with ζ
    exact hvu (affine_sphere_mem a ⟨hr.le, le_rfl⟩ ζ)
  have hvint : Integrable (fun ζ : S => v (a + r • ζ.1)) μ :=
    (sphere_section_continuous v a hv ⟨hr.le, le_rfl⟩).integrable_of_hasCompactSupport
      (HasCompactSupport.of_compactSpace _)
  have huint : Integrable (fun ζ : S => u (a + r • ζ.1)) μ := hvint.congr hsample
  calc
    _ = ∫ ζ : S, v (a + r • ζ.1) ∂μ := integral_congr_ae hsample.symm
    _ = M 0 := hconstant
    _ = v a := hcenter
    _ = u a := hvu (mem_closedBall_self hr.le)

end
end AutoSamplingTheory.TechnicalLemmas.Analysis.Harmonic.SphericalMeanValue
