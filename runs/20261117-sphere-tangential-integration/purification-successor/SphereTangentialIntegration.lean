import AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence
import AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.BallFlux
import Mathlib.Geometry.Manifold.Instances.Sphere
import Mathlib.Geometry.Manifold.ContMDiff.Constructions
import Mathlib.Analysis.InnerProductSpace.Calculus
import Mathlib.Analysis.Calculus.FDeriv.Pi
import Mathlib.MeasureTheory.Constructions.HaarToSphere
import Mathlib.MeasureTheory.Integral.Pi
import Mathlib.Analysis.InnerProductSpace.Projection.Basic
import Mathlib.LinearAlgebra.Trace

/-!
# Tangential integration by parts on finite products of unit spheres

The reference measure is the probability normalization of `volume.toSphere`,
followed by the actual finite product measure. The operators use coordinate
sections and the canonical radial extension; for tangent vector fields its
ambient divergence trace is the intrinsic divergence. The extension is used
only away from zero, so its totalizing zero branch imposes no regularity there.

The proof constructs a compactly supported annular extension from intrinsic
regularity, applies the public compact-support divergence and polar-integration
producers, and cancels a strictly positive radial factor. Finite-product Fubini
and the product rule give the first theorem. Joint C² regularity gives C¹ tangent
gradients for the weighted specialization. Both dimensions may be zero.
-/

open MeasureTheory Metric Set
open scoped BigOperators Manifold ContDiff RealInnerProductSpace Topology

namespace AutoSamplingTheory.TechnicalLemmas.Geometry.SphereTangentialIntegration

abbrev SphereAmbient (n : ℕ) := EuclideanSpace ℝ (Fin (n + 1))
abbrev SpherePoint (n : ℕ) := Metric.sphere (0 : SphereAmbient n) 1
abbrev SphereConfiguration (n N : ℕ) := Fin N → SpherePoint n

noncomputable def sphereProductModel (n N : ℕ) :
    ModelWithCorners ℝ (Fin N → EuclideanSpace ℝ (Fin n))
      (ModelPi (fun _ : Fin N => EuclideanSpace ℝ (Fin n))) :=
  ModelWithCorners.pi (fun _ : Fin N => 𝓡 n)

noncomputable def sphereSurfaceMeasure (n : ℕ) : Measure (SpherePoint n) :=
  (volume : Measure (SphereAmbient n)).toSphere

noncomputable def sphereUniformMeasure (n : ℕ) : Measure (SpherePoint n) :=
  (sphereSurfaceMeasure n Set.univ)⁻¹ • sphereSurfaceMeasure n

noncomputable def sphereProductMeasure (n N : ℕ) :
    Measure (SphereConfiguration n N) :=
  Measure.pi (fun _ : Fin N => sphereUniformMeasure n)

-- The origin branch is arbitrary totalization, never an input regularity claim.
noncomputable def sphereRadialExtension {n : ℕ} {A : Type*} [Zero A]
    (f : SpherePoint n → A) (x : SphereAmbient n) : A :=
  if hx : x = 0 then 0
  else f ((homeomorphUnitSphereProd (SphereAmbient n)) ⟨x, hx⟩).1

noncomputable def sphereTangentGradient {n : ℕ}
    (f : SpherePoint n → ℝ) (x : SpherePoint n) : SphereAmbient n :=
  ((Submodule.span ℝ ({(x : SphereAmbient n)} : Set (SphereAmbient n)))ᗮ).starProjection
    (gradient (sphereRadialExtension f) (x : SphereAmbient n))

noncomputable def sphereTangentDivergence {n : ℕ}
    (V : SpherePoint n → SphereAmbient n) (x : SpherePoint n) : ℝ :=
  AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence.coordinateDivergence
    (sphereRadialExtension V) (x : SphereAmbient n)

noncomputable def sphereProductGradient {n N : ℕ}
    (f : SphereConfiguration n N → ℝ) (i : Fin N)
    (x : SphereConfiguration n N) : SphereAmbient n :=
  sphereTangentGradient (fun y => f (Function.update x i y)) (x i)

noncomputable def sphereProductDivergence {n N : ℕ}
    (V : Fin N → SphereConfiguration n N → SphereAmbient n)
    (x : SphereConfiguration n N) : ℝ :=
  ∑ i : Fin N,
    sphereTangentDivergence (fun y => V i (Function.update x i y)) (x i)


/-! Internal proof bridges under the sealed source hypotheses. -/

instance sphereSurfaceMeasure_isFinite (n : ℕ) :
    IsFiniteMeasure (sphereSurfaceMeasure n) := by
  unfold sphereSurfaceMeasure
  infer_instance

private theorem sphereSurfaceMeasure_mass_ne_zero (n : ℕ) :
    sphereSurfaceMeasure n univ ≠ 0 := by
  apply Measure.measure_univ_ne_zero.mpr
  exact Measure.toSphere_ne_zero (volume : Measure (SphereAmbient n))

instance sphereUniformMeasure_isProbability (n : ℕ) :
    IsProbabilityMeasure (sphereUniformMeasure n) where
  measure_univ := by
    rw [sphereUniformMeasure, Measure.smul_apply, smul_eq_mul]
    exact ENNReal.inv_mul_cancel (sphereSurfaceMeasure_mass_ne_zero n) (measure_ne_top _ _)

instance sphereProductMeasure_isProbability (n N : ℕ) :
    IsProbabilityMeasure (sphereProductMeasure n N) := by
  unfold sphereProductMeasure
  infer_instance

private def nonzeroDomain (n : ℕ) : TopologicalSpace.Opens (SphereAmbient n) :=
  ⟨{0}ᶜ, isClosed_singleton.isOpen_compl⟩

private theorem contMDiff_radialProjection {n : ℕ} (k : ℕ∞ω) :
    ContMDiff 𝓘(ℝ, SphereAmbient n) (𝓡 n) k
      (fun x : nonzeroDomain n => (homeomorphUnitSphereProd (SphereAmbient n) x).1) := by
  let : Fact (Module.finrank ℝ (SphereAmbient n) = n + 1) := ⟨by simp [SphereAmbient]⟩
  let U := nonzeroDomain n
  let r : U → SphereAmbient n := fun x => ‖(x : SphereAmbient n)‖⁻¹ • (x : SphereAmbient n)
  have hx (x : U) : (x : SphereAmbient n) ≠ 0 := by
    exact x.property
  have hr : ContMDiff 𝓘(ℝ, SphereAmbient n) 𝓘(ℝ, SphereAmbient n) k r := by
    intro x
    have hn : ContDiffAt ℝ k (fun y : SphereAmbient n => ‖y‖⁻¹ • y) (x : SphereAmbient n) :=
      ((contDiffAt_norm ℝ (hx x)).inv (norm_ne_zero_iff.mpr (hx x))).smul contDiffAt_id
    exact hn.contMDiffAt.comp x (contMDiff_subtype_val x)
  have hmem (x : U) : r x ∈ sphere (0 : SphereAmbient n) 1 := by
    rw [mem_sphere_zero_iff_norm]
    simp [r, norm_smul, norm_ne_zero_iff.mpr (hx x)]
  have hr' : ContMDiff 𝓘(ℝ, SphereAmbient n) (𝓡 n) k
      (Set.codRestrict r (sphere (0 : SphereAmbient n) 1) hmem) :=
    hr.codRestrict_sphere (n := n) hmem
  have heq : (fun x : U => (homeomorphUnitSphereProd (SphereAmbient n) x).1) =
      Set.codRestrict r (sphere (0 : SphereAmbient n) 1) hmem := by
    funext x
    apply Subtype.ext
    change (1 : ℝ) • ‖(x : SphereAmbient n)‖⁻¹ • (x : SphereAmbient n) = r x
    simp only [one_smul, r]
  rw [heq]
  exact hr'

/-- Intrinsic regularity gives regularity of the specified canonical radial
extension away from zero; its artificial value at zero is irrelevant. -/
private theorem contDiffAt_radialExtension {n : ℕ} {A : Type*}
    [NormedAddCommGroup A] [NormedSpace ℝ A] {k : ℕ∞ω}
    (f : SpherePoint n → A) (hf : ContMDiff (𝓡 n) 𝓘(ℝ, A) k f)
    {x : SphereAmbient n} (hx : x ≠ 0) :
    ContDiffAt ℝ k (sphereRadialExtension f) x := by
  let x' : nonzeroDomain n := ⟨x, hx⟩
  have h := hf.comp (contMDiff_radialProjection (n := n) k)
  have heq : (fun z : nonzeroDomain n => sphereRadialExtension f (z : SphereAmbient n)) =
      (fun z : nonzeroDomain n => f (homeomorphUnitSphereProd (SphereAmbient n) z).1) := by
    funext z
    have hz : (z : SphereAmbient n) ≠ 0 := z.property
    simp only [sphereRadialExtension, dif_neg hz]
    rfl
  have hlocal : ContMDiffAt 𝓘(ℝ, SphereAmbient n) 𝓘(ℝ, A) k
      (fun z : nonzeroDomain n => sphereRadialExtension f (z : SphereAmbient n)) x' := by
    rw [heq]
    exact h x'
  exact (contMDiffAt_subtype_iff.mp hlocal).contDiffAt

private theorem radialExtension_on_sphere {n : ℕ} {A : Type*} [Zero A]
    (f : SpherePoint n → A) (x : SpherePoint n) :
    sphereRadialExtension f (x : SphereAmbient n) = f x := by
  have hx : (x : SphereAmbient n) ≠ 0 := ne_zero_of_mem_unit_sphere x
  simp only [sphereRadialExtension, dif_neg hx]
  congr 1
  apply Subtype.ext
  simp [homeomorphUnitSphereProd_apply_fst_coe, norm_eq_of_mem_sphere]


private theorem tangentGradient_tangent {n : ℕ} (f : SpherePoint n → ℝ)
    (x : SpherePoint n) : inner ℝ (x : SphereAmbient n) (sphereTangentGradient f x) = 0 := by
  apply Submodule.mem_orthogonal_singleton_iff_inner_right.mp
  exact Submodule.starProjection_apply_mem _ _

private theorem tangentGradient_pairing {n : ℕ} (f : SpherePoint n → ℝ)
    (x : SpherePoint n) (v : SphereAmbient n) (hv : inner ℝ (x : SphereAmbient n) v = 0) :
    inner ℝ (sphereTangentGradient f x) v =
      fderiv ℝ (sphereRadialExtension f) (x : SphereAmbient n) v := by
  unfold sphereTangentGradient
  rw [Submodule.inner_starProjection_left_eq_right,
    Submodule.starProjection_eq_self_iff.mpr
      (Submodule.mem_orthogonal_singleton_iff_inner_right.mpr hv)]
  exact inner_gradient_left

private theorem radialExtension_smul {n : ℕ}
    (f : SpherePoint n → ℝ) (V : SpherePoint n → SphereAmbient n) :
    sphereRadialExtension (fun x => f x • V x) =
      fun y => sphereRadialExtension f y • sphereRadialExtension V y := by
  funext y
  by_cases hy : y = 0 <;> simp [sphereRadialExtension, hy]

private theorem continuous_radial_fderiv_on_sphere {n : ℕ} {A : Type*}
    [NormedAddCommGroup A] [NormedSpace ℝ A]
    (f : SpherePoint n → A) (hf : ContMDiff (𝓡 n) 𝓘(ℝ, A) 1 f) :
    Continuous (fun x : SpherePoint n => fderiv ℝ (sphereRadialExtension f) (x : SphereAmbient n)) := by
  apply continuous_iff_continuousAt.mpr
  intro x
  exact ((contDiffAt_radialExtension f hf (ne_zero_of_mem_unit_sphere x)).continuousAt_fderiv
    one_ne_zero).comp continuous_subtype_val.continuousAt

private theorem tangentDivergence_eq_fderiv_trace {n : ℕ}
    (V : SpherePoint n → SphereAmbient n)
    (hV : ContMDiff (𝓡 n) 𝓘(ℝ, SphereAmbient n) 1 V) (x : SpherePoint n) :
    sphereTangentDivergence V x = ∑ j : Fin (n + 1),
      fderiv ℝ (sphereRadialExtension V) (x : SphereAmbient n)
        (EuclideanSpace.single j (1 : ℝ)) j := by
  exact AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence.coordinateDivergence_eq_sum_fderiv_apply_of_differentiableAt
    ((contDiffAt_radialExtension V hV (ne_zero_of_mem_unit_sphere x)).differentiableAt one_ne_zero)

private theorem continuous_tangentDivergence {n : ℕ}
    (V : SpherePoint n → SphereAmbient n)
    (hV : ContMDiff (𝓡 n) 𝓘(ℝ, SphereAmbient n) 1 V) :
    Continuous (sphereTangentDivergence V) := by
  have hD := continuous_radial_fderiv_on_sphere V hV
  have heq : sphereTangentDivergence V = fun x : SpherePoint n => ∑ j : Fin (n + 1),
      fderiv ℝ (sphereRadialExtension V) (x : SphereAmbient n)
        (EuclideanSpace.single j (1 : ℝ)) j := by
    funext x
    exact tangentDivergence_eq_fderiv_trace V hV x
  rw [heq]
  apply continuous_finsetSum
  intro j _
  fun_prop

private theorem integrable_tangentDivergence {n : ℕ}
    (V : SpherePoint n → SphereAmbient n)
    (hV : ContMDiff (𝓡 n) 𝓘(ℝ, SphereAmbient n) 1 V) :
    Integrable (sphereTangentDivergence V) (sphereUniformMeasure n) := by
  have h := (continuous_tangentDivergence V hV).continuousOn.integrableOn_compact
    (μ := sphereUniformMeasure n) (K := Set.univ) isCompact_univ
  simpa only [integrableOn_univ] using h


private theorem radialExtension_pos_smul {n : ℕ} {A : Type*} [Zero A]
    (f : SpherePoint n → A) (x : SphereAmbient n) {r : ℝ} (hr : 0 < r) :
    sphereRadialExtension f (r • x) = sphereRadialExtension f x := by
  by_cases hx : x = 0
  · simp [hx]
  have hrx : r • x ≠ 0 := smul_ne_zero hr.ne' hx
  simp only [sphereRadialExtension, dif_neg hx, dif_neg hrx]
  congr 1
  apply Subtype.ext
  change (1 : ℝ) • ‖r • x‖⁻¹ • (r • x) = (1 : ℝ) • ‖x‖⁻¹ • x
  simp only [norm_smul, Real.norm_eq_abs, abs_of_pos hr, mul_inv_rev, smul_smul]
  congr 1
  field_simp


private theorem sum_dual_single_mul {n : ℕ}
    (L : SphereAmbient n →L[ℝ] ℝ) (v : SphereAmbient n) :
    (∑ j : Fin (n + 1), L (EuclideanSpace.single j (1 : ℝ)) * v j) = L v := by
  calc
    _ = ∑ j : Fin (n + 1), L (v j • EuclideanSpace.single j (1 : ℝ)) := by
      simp only [map_smul, smul_eq_mul, mul_comm]
    _ = L (∑ j : Fin (n + 1), v j • EuclideanSpace.single j (1 : ℝ)) := by
      rw [map_sum]
    _ = L v := by
      congr 1
      ext k
      simp [EuclideanSpace.single, Pi.single_apply, mul_ite]

private theorem tangentDivergence_smul {n : ℕ}
    (f : SpherePoint n → ℝ) (V : SpherePoint n → SphereAmbient n)
    (hf : ContMDiff (𝓡 n) 𝓘(ℝ, ℝ) 1 f)
    (hV : ContMDiff (𝓡 n) 𝓘(ℝ, SphereAmbient n) 1 V)
    (hTangent : ∀ x : SpherePoint n, inner ℝ (x : SphereAmbient n) (V x) = 0)
    (x : SpherePoint n) :
    sphereTangentDivergence (fun y => f y • V y) x =
      f x * sphereTangentDivergence V x + inner ℝ (sphereTangentGradient f x) (V x) := by
  have hdf := (contDiffAt_radialExtension f hf (ne_zero_of_mem_unit_sphere x)).differentiableAt one_ne_zero
  have hdV := (contDiffAt_radialExtension V hV (ne_zero_of_mem_unit_sphere x)).differentiableAt one_ne_zero
  rw [tangentGradient_pairing f x (V x) (hTangent x), tangentDivergence_eq_fderiv_trace V hV x]
  unfold sphereTangentDivergence
  rw [radialExtension_smul]
  have hmul : HasFDerivAt
      (fun y => sphereRadialExtension f y • sphereRadialExtension V y)
      (sphereRadialExtension f (x : SphereAmbient n) •
          fderiv ℝ (sphereRadialExtension V) (x : SphereAmbient n) +
        (fderiv ℝ (sphereRadialExtension f) (x : SphereAmbient n)).smulRight
          (sphereRadialExtension V (x : SphereAmbient n))) (x : SphereAmbient n) :=
    hdf.hasFDerivAt.smul hdV.hasFDerivAt
  rw [AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence.coordinateDivergence_eq_sum_fderiv_apply_of_hasFDerivAt hmul]
  simp only [add_apply, smul_apply,
    ContinuousLinearMap.smulRight_apply, PiLp.add_apply, PiLp.smul_apply, smul_eq_mul,
    radialExtension_on_sphere, Finset.sum_add_distrib, Finset.mul_sum]
  rw [sum_dual_single_mul]

private theorem radialExtension_fderiv_pos_smul {n : ℕ} {A : Type*}
    [NormedAddCommGroup A] [NormedSpace ℝ A]
    (f : SpherePoint n → A) (hf : ContMDiff (𝓡 n) 𝓘(ℝ, A) 1 f)
    (x : SphereAmbient n) (hx : x ≠ 0) {r : ℝ} (hr : 0 < r) (v : SphereAmbient n) :
    fderiv ℝ (sphereRadialExtension f) (r • x) v =
      r⁻¹ • fderiv ℝ (sphereRadialExtension f) x v := by
  have hdx := (contDiffAt_radialExtension f hf hx).differentiableAt one_ne_zero
  have hdrx := (contDiffAt_radialExtension f hf (smul_ne_zero hr.ne' hx)).differentiableAt one_ne_zero
  have hscale : HasFDerivAt (fun y : SphereAmbient n => r • y)
      (r • ContinuousLinearMap.id ℝ (SphereAmbient n)) x := by
    exact (r • ContinuousLinearMap.id ℝ (SphereAmbient n)).hasFDerivAt
  have heq : (fun y => sphereRadialExtension f (r • y)) = sphereRadialExtension f := by
    funext y
    exact radialExtension_pos_smul f y hr
  have hchain := hdrx.hasFDerivAt.comp x hscale
  change HasFDerivAt (fun y => sphereRadialExtension f (r • y)) _ x at hchain
  rw [heq] at hchain
  have hv := congrArg (fun L : SphereAmbient n →L[ℝ] A => L v)
    (hchain.unique hdx.hasFDerivAt)
  simp only [ContinuousLinearMap.comp_apply, smul_apply,
    ContinuousLinearMap.id_apply, map_smul] at hv
  rw [← hv, inv_smul_smul₀ hr.ne']


private noncomputable def annularCutoff {n : ℕ} (x : SphereAmbient n) : ℝ :=
  AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Cutoff.smoothUnitCutoff (‖x‖ ^ 2 - 4)

private theorem contDiff_annularCutoff {n : ℕ} :
    ContDiff ℝ 1 (annularCutoff : SphereAmbient n → ℝ) := by
  have h : ContDiff ℝ (⊤ : ℕ∞) (fun x : SphereAmbient n => ‖x‖ ^ 2 - 4) :=
    (contDiff_norm_sq ℝ).sub contDiff_const
  exact (AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Cutoff.smoothUnitCutoff_contDiff.comp h).of_le (by norm_num)

private theorem annularCutoff_zero_of_norm_le_one {n : ℕ} {x : SphereAmbient n}
    (hx : ‖x‖ ≤ 1) : annularCutoff x = 0 := by
  apply AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Cutoff.smoothUnitCutoff_eq_zero_of_two_le_abs
  have hn := norm_nonneg x
  rw [abs_of_nonpos (by nlinarith)]
  nlinarith

private theorem annularCutoff_zero_of_three_le_norm {n : ℕ} {x : SphereAmbient n}
    (hx : 3 ≤ ‖x‖) : annularCutoff x = 0 := by
  apply AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Cutoff.smoothUnitCutoff_eq_zero_of_two_le_abs
  rw [abs_of_nonneg (by nlinarith)]
  nlinarith

private noncomputable def annularExtension {n : ℕ}
    (V : SpherePoint n → SphereAmbient n) (x : SphereAmbient n) : SphereAmbient n :=
  annularCutoff x • sphereRadialExtension V x

private theorem contDiff_annularExtension {n : ℕ}
    (V : SpherePoint n → SphereAmbient n)
    (hV : ContMDiff (𝓡 n) 𝓘(ℝ, SphereAmbient n) 1 V) :
    ContDiff ℝ 1 (annularExtension V) := by
  apply contDiff_iff_contDiffAt.mpr
  intro x
  by_cases hx : x = 0
  · subst x
    apply (contDiffAt_const (c := (0 : SphereAmbient n))).congr_of_eventuallyEq
    filter_upwards [Metric.ball_mem_nhds (0 : SphereAmbient n) zero_lt_one] with y hy
    have hy' : ‖y‖ ≤ 1 := le_of_lt (by simpa only [mem_ball, dist_zero_right] using hy)
    simp only [annularExtension, annularCutoff_zero_of_norm_le_one hy', zero_smul]
  · exact contDiff_annularCutoff.contDiffAt.smul (contDiffAt_radialExtension V hV hx)

private theorem hasCompactSupport_annularExtension {n : ℕ}
    (V : SpherePoint n → SphereAmbient n) : HasCompactSupport (annularExtension V) := by
  apply (isCompact_closedBall (0 : SphereAmbient n) 3).of_isClosed_subset (isClosed_tsupport _)
  apply closure_minimal _ isClosed_closedBall
  intro x hx
  by_contra h
  have hx' : 3 ≤ ‖x‖ := le_of_lt (by simpa only [mem_closedBall, dist_zero_right, not_le] using h)
  exact hx (by simp [annularExtension, annularCutoff_zero_of_three_le_norm hx'])

private theorem radialExtension_tangent {n : ℕ}
    (V : SpherePoint n → SphereAmbient n)
    (hTangent : ∀ x : SpherePoint n, inner ℝ (x : SphereAmbient n) (V x) = 0)
    (x : SphereAmbient n) : inner ℝ x (sphereRadialExtension V x) = 0 := by
  by_cases hx : x = 0
  · simp [hx]
  let u : SpherePoint n := (homeomorphUnitSphereProd (SphereAmbient n) ⟨x, hx⟩).1
  have hu : (u : SphereAmbient n) = ‖x‖⁻¹ • x := by
    change (1 : ℝ) • ‖x‖⁻¹ • x = _
    simp only [one_smul]
  have h := hTangent u
  rw [hu, real_inner_smul_left] at h
  have hzero : inner ℝ x (V u) = 0 :=
    (mul_eq_zero.mp h).resolve_left (inv_ne_zero (norm_ne_zero_iff.mpr hx))
  simpa only [sphereRadialExtension, dif_neg hx, u] using hzero


private theorem fderiv_annularCutoff_tangent {n : ℕ}
    (x v : SphereAmbient n) (hv : inner ℝ x v = 0) :
    fderiv ℝ (annularCutoff : SphereAmbient n → ℝ) x v = 0 := by
  let c := AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Cutoff.smoothUnitCutoff
  have hc : Differentiable ℝ c :=
    AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Cutoff.smoothUnitCutoff_contDiff.differentiable (by simp)
  have hd : HasFDerivAt (annularCutoff : SphereAmbient n → ℝ)
      (deriv c (‖x‖ ^ 2 - 4) • (2 • innerSL ℝ x)) x :=
    (hc (‖x‖ ^ 2 - 4)).hasDerivAt.comp_hasFDerivAt x
      ((hasStrictFDerivAt_norm_sq x).hasFDerivAt.sub_const 4)
  rw [hd.fderiv]
  simp [hv]

private theorem divergence_annularExtension {n : ℕ}
    (V : SpherePoint n → SphereAmbient n)
    (hV : ContMDiff (𝓡 n) 𝓘(ℝ, SphereAmbient n) 1 V)
    (hTangent : ∀ x : SpherePoint n, inner ℝ (x : SphereAmbient n) (V x) = 0)
    (x : SphereAmbient n) (hx : x ≠ 0) :
    AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence.coordinateDivergence
      (annularExtension V) x = annularCutoff x *
      AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence.coordinateDivergence
        (sphereRadialExtension V) x := by
  have hdV := (contDiffAt_radialExtension V hV hx).differentiableAt one_ne_zero
  have hdχ := (contDiff_annularCutoff (n := n)).differentiable one_ne_zero x
  have hmul : HasFDerivAt (annularExtension V)
      (annularCutoff x • fderiv ℝ (sphereRadialExtension V) x +
        (fderiv ℝ (annularCutoff : SphereAmbient n → ℝ) x).smulRight
          (sphereRadialExtension V x)) x := hdχ.hasFDerivAt.smul hdV.hasFDerivAt
  rw [AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence.coordinateDivergence_eq_sum_fderiv_apply_of_hasFDerivAt hmul,
    AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence.coordinateDivergence_eq_sum_fderiv_apply_of_differentiableAt hdV]
  simp only [add_apply, smul_apply, ContinuousLinearMap.smulRight_apply,
    PiLp.add_apply, PiLp.smul_apply, smul_eq_mul, Finset.sum_add_distrib]
  rw [sum_dual_single_mul, fderiv_annularCutoff_tangent x _ (radialExtension_tangent V hTangent x), add_zero,
    Finset.mul_sum]

private theorem divergence_radialExtension_pos_smul {n : ℕ}
    (V : SpherePoint n → SphereAmbient n)
    (hV : ContMDiff (𝓡 n) 𝓘(ℝ, SphereAmbient n) 1 V)
    (x : SpherePoint n) {r : ℝ} (hr : 0 < r) :
    AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence.coordinateDivergence
      (sphereRadialExtension V) (r • (x : SphereAmbient n)) =
      r⁻¹ * sphereTangentDivergence V x := by
  have hx := ne_zero_of_mem_unit_sphere x
  rw [AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence.coordinateDivergence_eq_sum_fderiv_apply_of_differentiableAt
    ((contDiffAt_radialExtension V hV (smul_ne_zero hr.ne' hx)).differentiableAt one_ne_zero),
    tangentDivergence_eq_fderiv_trace V hV x]
  simp_rw [radialExtension_fderiv_pos_smul V hV _ hx hr, PiLp.smul_apply, smul_eq_mul,
    Finset.mul_sum]

private theorem divergence_annularExtension_polar {n : ℕ}
    (V : SpherePoint n → SphereAmbient n)
    (hV : ContMDiff (𝓡 n) 𝓘(ℝ, SphereAmbient n) 1 V)
    (hTangent : ∀ x : SpherePoint n, inner ℝ (x : SphereAmbient n) (V x) = 0)
    (x : SpherePoint n) {r : ℝ} (hr : 0 < r) :
    AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence.coordinateDivergence
      (annularExtension V) (r • (x : SphereAmbient n)) =
      (AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Cutoff.smoothUnitCutoff (r ^ 2 - 4) / r) *
        sphereTangentDivergence V x := by
  rw [divergence_annularExtension V hV hTangent _ (smul_ne_zero hr.ne' (ne_zero_of_mem_unit_sphere x)),
    divergence_radialExtension_pos_smul V hV x hr]
  simp [annularCutoff, norm_smul, Real.norm_eq_abs, abs_of_pos hr, norm_eq_of_mem_sphere,
    div_eq_mul_inv, mul_assoc]


private noncomputable def radialIntegrationWeight (n : ℕ) (r : ℝ) : ℝ :=
  r ^ n * (AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Cutoff.smoothUnitCutoff
    (r ^ 2 - 4) / r)

private theorem radialIntegrationWeight_zero_small (n : ℕ) {r : ℝ} (hr : |r| ≤ 1) :
    radialIntegrationWeight n r = 0 := by
  have hb := abs_le.mp hr
  have hp := mul_nonneg (sub_nonneg.mpr hb.2) (show 0 ≤ 1 + r by linarith)
  have hsq : r ^ 2 ≤ 1 := by nlinarith
  have hc : AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Cutoff.smoothUnitCutoff (r ^ 2 - 4) = 0 := by
    apply AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Cutoff.smoothUnitCutoff_eq_zero_of_two_le_abs
    rw [abs_of_nonpos (by linarith)]
    linarith
  simp [radialIntegrationWeight, hc]

private theorem radialIntegrationWeight_zero_large (n : ℕ) {r : ℝ} (hr : 3 ≤ r) :
    radialIntegrationWeight n r = 0 := by
  have hc : AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Cutoff.smoothUnitCutoff (r ^ 2 - 4) = 0 := by
    apply AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Cutoff.smoothUnitCutoff_eq_zero_of_two_le_abs
    rw [abs_of_nonneg (by nlinarith)]
    nlinarith
  simp [radialIntegrationWeight, hc]

private theorem continuous_radialIntegrationWeight (n : ℕ) :
    Continuous (radialIntegrationWeight n) := by
  apply continuous_iff_continuousAt.mpr
  intro r
  by_cases hr : r = 0
  · subst r
    apply continuousAt_const.congr_of_eventuallyEq
    filter_upwards [Metric.ball_mem_nhds (0 : ℝ) zero_lt_one] with t ht
    apply radialIntegrationWeight_zero_small
    exact le_of_lt (by simpa only [mem_ball, dist_zero_right, Real.norm_eq_abs] using ht)
  · unfold radialIntegrationWeight
    have hc : Continuous (fun t : ℝ =>
        AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Cutoff.smoothUnitCutoff (t ^ 2 - 4)) :=
      AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Cutoff.smoothUnitCutoff_contDiff.continuous.comp
        ((continuous_id.pow 2).sub continuous_const)
    exact (continuous_id.pow n).continuousAt.mul (hc.continuousAt.div continuousAt_id hr)

private noncomputable def positiveRadialIntegrationWeight (n : ℕ) (r : ℝ) : ℝ :=
  if 0 < r then radialIntegrationWeight n r else 0

private theorem continuous_positiveRadialIntegrationWeight (n : ℕ) :
    Continuous (positiveRadialIntegrationWeight n) := by
  apply (continuous_radialIntegrationWeight n).if _ continuous_const
  intro r hr
  have hr0 : r = 0 := by simpa only [show {x : ℝ | 0 < x} = Ioi 0 from rfl,
    frontier_Ioi, mem_singleton_iff] using hr
  subst r
  simp [radialIntegrationWeight]

private theorem positiveRadialIntegrationWeight_zero_small (n : ℕ) {r : ℝ} (hr : r ≤ 1) :
    positiveRadialIntegrationWeight n r = 0 := by
  by_cases h : 0 < r
  · simp only [positiveRadialIntegrationWeight, if_pos h]
    apply radialIntegrationWeight_zero_small
    rwa [abs_of_pos h]
  · simp only [positiveRadialIntegrationWeight, if_neg h]

private theorem hasCompactSupport_positiveRadialIntegrationWeight (n : ℕ) :
    HasCompactSupport (positiveRadialIntegrationWeight n) := by
  apply (isCompact_Icc : IsCompact (Icc (1 : ℝ) 3)).of_isClosed_subset (isClosed_tsupport _)
  apply closure_minimal _ isClosed_Icc
  intro r hr
  by_contra h
  have h' : r < 1 ∨ 3 < r := by simpa only [mem_Icc, not_and_or, not_le] using h
  rcases h' with h | h
  · exact hr (positiveRadialIntegrationWeight_zero_small n h.le)
  · exact hr (by simp [positiveRadialIntegrationWeight,
      radialIntegrationWeight_zero_large n h.le])

private theorem radialIntegrationWeight_integral_pos (n : ℕ) :
    0 < ∫ r in Ioi (0 : ℝ), radialIntegrationWeight n r := by
  have hnonneg : 0 ≤ positiveRadialIntegrationWeight n := by
    intro r
    change 0 ≤ positiveRadialIntegrationWeight n r
    by_cases hr : 0 < r
    · simp only [positiveRadialIntegrationWeight, if_pos hr, radialIntegrationWeight]
      exact mul_nonneg (pow_nonneg hr.le _) (div_nonneg
        (AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Cutoff.smoothUnitCutoff_mem_Icc _).1 hr.le)
    · simp only [positiveRadialIntegrationWeight, if_neg hr, le_refl]
  have htwo : positiveRadialIntegrationWeight n 2 ≠ 0 := by
    have hc : AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Cutoff.smoothUnitCutoff (2 ^ 2 - 4) = 1 :=
      AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Cutoff.smoothUnitCutoff_eq_one_of_abs_le_one (by norm_num)
    simp only [positiveRadialIntegrationWeight, show (0 : ℝ) < 2 by norm_num, if_true,
      radialIntegrationWeight, hc]
    positivity
  have h := (continuous_positiveRadialIntegrationWeight n).integral_pos_of_hasCompactSupport_nonneg_nonzero
    (μ := volume) (hasCompactSupport_positiveRadialIntegrationWeight n) hnonneg htwo
  have heq : positiveRadialIntegrationWeight n = (Ioi (0 : ℝ)).indicator (radialIntegrationWeight n) := by
    funext r
    simp only [positiveRadialIntegrationWeight, indicator_apply, mem_Ioi]
  rw [heq, integral_indicator measurableSet_Ioi] at h
  exact h


private theorem radialIntegrationWeight_polar_mass (n : ℕ) :
    (∫ r : Ioi (0 : ℝ),
      AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Cutoff.smoothUnitCutoff
        (r.1 ^ 2 - 4) / r.1 ∂Measure.volumeIoiPow n) =
      ∫ r in Ioi (0 : ℝ), radialIntegrationWeight n r := by
  simp only [Measure.volumeIoiPow, ENNReal.ofReal]
  rw [integral_withDensity_eq_integral_smul]
  · rw [integral_subtype_comap measurableSet_Ioi (fun r : ℝ =>
      Real.toNNReal (r ^ n) •
        (AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Cutoff.smoothUnitCutoff
          (r ^ 2 - 4) / r))]
    apply setIntegral_congr_fun measurableSet_Ioi
    intro r hr
    dsimp only
    rw [NNReal.smul_def, Real.coe_toNNReal _ (pow_nonneg hr.le _), smul_eq_mul]
    rfl
  · exact (measurable_subtype_coe.pow_const n).real_toNNReal


-- This specializes the existing Euclidean divergence and polar-measure producers
-- to the internally constructed annular field; it does not reprove either producer.
open AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus in
private theorem integral_tangentDivergence_surface_eq_zero {n : ℕ}
    (V : SpherePoint n → SphereAmbient n)
    (hV : ContMDiff (𝓡 n) 𝓘(ℝ, SphereAmbient n) 1 V)
    (hTangent : ∀ x : SpherePoint n, inner ℝ (x : SphereAmbient n) (V x) = 0) :
    (∫ x, sphereTangentDivergence V x ∂sphereSurfaceMeasure n) = 0 := by
  let F := annularExtension V
  let dF := Divergence.coordinateDivergence F
  have hF : ContDiff ℝ 1 F := contDiff_annularExtension V hV
  have hFc : HasCompactSupport F := hasCompactSupport_annularExtension V
  have htrace : dF = fun x => ∑ j : Fin (n + 1),
      fderiv ℝ F x (EuclideanSpace.single j (1 : ℝ)) j := by
    funext x
    exact Divergence.coordinateDivergence_eq_sum_fderiv_apply_of_differentiableAt
      (hF.differentiable one_ne_zero x)
  have hDc : Continuous dF := by
    rw [htrace]
    apply continuous_finsetSum
    intro j _
    exact (PiLp.proj (p := 2) (𝕜 := ℝ) (fun _ : Fin (n + 1) => ℝ) j).continuous.comp
      ((hF.continuous_fderiv one_ne_zero).clm_apply continuous_const)
  have hDs : HasCompactSupport dF := by
    rw [htrace]
    exact (hFc.fderiv ℝ).comp_left (g := fun L : SphereAmbient n →L[ℝ] SphereAmbient n =>
      ∑ j : Fin (n + 1), L (EuclideanSpace.single j (1 : ℝ)) j) (by simp)
  have hI : Integrable dF := hDc.integrable_of_hasCompactSupport hDs
  let e := PiLp.continuousLinearEquiv 2 ℝ (fun _ : Fin (n + 1) => ℝ)
  let G : (Fin (n + 1) → ℝ) → Fin (n + 1) → ℝ := fun x => e (F (e.symm x))
  have hzeroRaw := Divergence.integral_coordinateDivergence_wrapped_eq_zero_of_contDiff_of_hasCompactSupport
    G (e.contDiff.comp (hF.comp e.symm.contDiff))
      ((hFc.comp_homeomorph e.symm.toHomeomorph).comp_left e.map_zero)
  have hzero : (∫ x, dF x) = 0 := by
    have htransport := (PiLp.volume_preserving_toLp (Fin (n + 1))).integral_comp
      (MeasurableEquiv.measurableEmbedding (MeasurableEquiv.toLp 2 (Fin (n + 1) → ℝ))) dF
    simpa [dF, G, e] using htransport.symm.trans hzeroRaw
  let τ := sphereSurfaceMeasure n
  let q : SpherePoint n × Ioi (0 : ℝ) → ℝ := fun z => dF (z.2.1 • (z.1 : SphereAmbient n))
  have hsub : Integrable (fun x : ({0}ᶜ : Set (SphereAmbient n)) => dF x.1)
      ((volume : Measure (SphereAmbient n)).comap Subtype.val) :=
    (integrableOn_iff_comap_subtypeVal (measurableSet_singleton 0).compl).mp hI.restrict
  have hmp := (volume : Measure (SphereAmbient n)).measurePreserving_homeomorphUnitSphereProd
  have hcomp : q ∘ homeomorphUnitSphereProd (SphereAmbient n) =
      fun x : ({0}ᶜ : Set (SphereAmbient n)) => dF x.1 := by
    funext x
    change dF ((homeomorphUnitSphereProd (SphereAmbient n)).symm
      (homeomorphUnitSphereProd (SphereAmbient n) x)).1 = dF x.1
    rw [Homeomorph.symm_apply_apply]
  have hq : Integrable q (τ.prod (Measure.volumeIoiPow n)) := by
    have h := (hmp.integrable_comp_emb (Homeomorph.measurableEmbedding _)).mp (hcomp.symm ▸ hsub)
    simpa [SphereAmbient, τ, sphereSurfaceMeasure] using h
  have hqzero : (∫ z, q z ∂τ.prod (Measure.volumeIoiPow n)) = 0 := by
    have htransport := hmp.integral_comp (Homeomorph.measurableEmbedding _) q
    change (∫ x : ({0}ᶜ : Set (SphereAmbient n)),
      (q ∘ homeomorphUnitSphereProd (SphereAmbient n)) x
        ∂(volume : Measure (SphereAmbient n)).comap Subtype.val) = _ at htransport
    rw [hcomp, integral_subtype_comap (measurableSet_singleton _).compl,
      restrict_compl_singleton] at htransport
    have ht : (∫ x, dF x) = ∫ z, q z ∂τ.prod (Measure.volumeIoiPow n) := by
      simpa [SphereAmbient, τ, sphereSurfaceMeasure] using htransport
    exact ht.symm.trans hzero
  have hqval (x : SpherePoint n) (r : Ioi (0 : ℝ)) : q (x, r) =
      (Cutoff.smoothUnitCutoff (r.1 ^ 2 - 4) / r.1) * sphereTangentDivergence V x :=
    divergence_annularExtension_polar V hV hTangent x r.2
  have hfactor : (∫ z, q z ∂τ.prod (Measure.volumeIoiPow n)) =
      (∫ r in Ioi (0 : ℝ), radialIntegrationWeight n r) *
        ∫ x, sphereTangentDivergence V x ∂τ := by
    rw [integral_prod_symm q hq]
    simp_rw [hqval, integral_const_mul]
    rw [integral_mul_const, radialIntegrationWeight_polar_mass]
  have hmulzero := hfactor.symm.trans hqzero
  exact (mul_eq_zero.mp hmulzero).resolve_left (ne_of_gt (radialIntegrationWeight_integral_pos n))

private theorem integral_tangentDivergence_eq_zero {n : ℕ}
    (V : SpherePoint n → SphereAmbient n)
    (hV : ContMDiff (𝓡 n) 𝓘(ℝ, SphereAmbient n) 1 V)
    (hTangent : ∀ x : SpherePoint n, inner ℝ (x : SphereAmbient n) (V x) = 0) :
    (∫ x, sphereTangentDivergence V x ∂sphereUniformMeasure n) = 0 := by
  rw [sphereUniformMeasure, integral_smul_measure,
    integral_tangentDivergence_surface_eq_zero V hV hTangent, smul_zero]


private theorem singleSphere_integration_by_parts {n : ℕ}
    (f : SpherePoint n → ℝ) (V : SpherePoint n → SphereAmbient n)
    (hf : ContMDiff (𝓡 n) 𝓘(ℝ, ℝ) 1 f)
    (hV : ContMDiff (𝓡 n) 𝓘(ℝ, SphereAmbient n) 1 V)
    (hTangent : ∀ x : SpherePoint n, inner ℝ (x : SphereAmbient n) (V x) = 0) :
    Integrable (sphereTangentDivergence V) (sphereUniformMeasure n) ∧
    Integrable (fun x => f x * sphereTangentDivergence V x) (sphereUniformMeasure n) ∧
    Integrable (fun x => inner ℝ (sphereTangentGradient f x) (V x)) (sphereUniformMeasure n) ∧
    (∫ x, sphereTangentDivergence V x ∂sphereUniformMeasure n) = 0 ∧
    (∫ x, f x * sphereTangentDivergence V x ∂sphereUniformMeasure n) =
      -(∫ x, inner ℝ (sphereTangentGradient f x) (V x) ∂sphereUniformMeasure n) := by
  have hW : ContMDiff (𝓡 n) 𝓘(ℝ, SphereAmbient n) 1 (fun x => f x • V x) := hf.smul hV
  have hWTangent (x : SpherePoint n) : inner ℝ (x : SphereAmbient n) (f x • V x) = 0 := by
    rw [inner_smul_right, hTangent x, mul_zero]
  have hmul : Continuous (fun x => f x * sphereTangentDivergence V x) :=
    hf.continuous.mul (continuous_tangentDivergence V hV)
  have hpair : Continuous (fun x => inner ℝ (sphereTangentGradient f x) (V x)) := by
    have heq : (fun x => inner ℝ (sphereTangentGradient f x) (V x)) =
        fun x => sphereTangentDivergence (fun y => f y • V y) x - f x * sphereTangentDivergence V x := by
      funext x
      rw [tangentDivergence_smul f V hf hV hTangent x]
      ring
    rw [heq]
    exact (continuous_tangentDivergence _ hW).sub hmul
  have hImul : Integrable (fun x => f x * sphereTangentDivergence V x) (sphereUniformMeasure n) := by
    simpa only [integrableOn_univ] using hmul.continuousOn.integrableOn_compact
      (μ := sphereUniformMeasure n) (K := Set.univ) isCompact_univ
  have hIpair : Integrable (fun x => inner ℝ (sphereTangentGradient f x) (V x)) (sphereUniformMeasure n) := by
    simpa only [integrableOn_univ] using hpair.continuousOn.integrableOn_compact
      (μ := sphereUniformMeasure n) (K := Set.univ) isCompact_univ
  refine ⟨integrable_tangentDivergence V hV, hImul, hIpair,
    integral_tangentDivergence_eq_zero V hV hTangent, ?_⟩
  have hzero := integral_tangentDivergence_eq_zero (fun x => f x • V x) hW hWTangent
  simp_rw [tangentDivergence_smul f V hf hV hTangent] at hzero
  rw [integral_add hImul hIpair] at hzero
  linarith


private theorem extChartAt_sphereProduct_apply {n N : ℕ}
    (x y : SphereConfiguration n N) (i : Fin N) :
    extChartAt (sphereProductModel n N) x y i = extChartAt (𝓡 n) (x i) (y i) := rfl

private theorem contMDiff_sphereProduct {n N : ℕ}
    {E H M : Type*} [NormedAddCommGroup E] [NormedSpace ℝ E]
    [TopologicalSpace H] [TopologicalSpace M] [ChartedSpace H M]
    (I : ModelWithCorners ℝ E H) (k : ℕ∞ω) (f : M → SphereConfiguration n N)
    (hf : ∀ i, ContMDiff I (𝓡 n) k (fun x => f x i)) :
    ContMDiff I (sphereProductModel n N) k f := by
  intro x
  rw [contMDiffAt_iff]
  refine ⟨continuousAt_pi.mpr (fun i => (hf i x).continuousAt), ?_⟩
  apply contDiffWithinAt_pi.mpr
  intro i
  have h := (contMDiffAt_iff.mp (hf i x)).2
  simpa only [Function.comp_def, extChartAt_sphereProduct_apply] using h

private theorem contMDiff_sphereSection {n N : ℕ} (k : ℕ∞ω)
    (x : SphereConfiguration n N) (i : Fin N) :
    ContMDiff (𝓡 n) (sphereProductModel n N) k (fun y => Function.update x i y) := by
  apply contMDiff_sphereProduct
  intro j
  by_cases h : j = i
  · subst j
    have heq : (fun y : SpherePoint n => Function.update x i y i) = (fun y => y) := by
      funext y
      exact Function.update_self i y x
    rw [heq]
    exact contMDiff_id
  · simpa only [Function.update_of_ne h] using (contMDiff_const : ContMDiff (𝓡 n) (𝓡 n) k (fun _ : SpherePoint n => x j))


private theorem contMDiff_sphereEvaluation {n N : ℕ} (k : ℕ∞ω) (i : Fin N) :
    ContMDiff (sphereProductModel n N) (𝓡 n) k (fun x : SphereConfiguration n N => x i) := by
  intro x
  rw [contMDiffAt_iff]
  refine ⟨(continuous_apply i).continuousAt, ?_⟩
  have heq : (fun y => extChartAt (𝓡 n) (x i)
      ((extChartAt (sphereProductModel n N) x).symm y i)) =ᶠ[
        𝓝[range (sphereProductModel n N)] (extChartAt (sphereProductModel n N) x x)]
      (fun y : Fin N → EuclideanSpace ℝ (Fin n) => y i) := by
    filter_upwards [extChartAt_target_mem_nhdsWithin (I := sphereProductModel n N) x] with y hy
    simpa only [extChartAt_sphereProduct_apply] using
      congrArg (fun z : Fin N → EuclideanSpace ℝ (Fin n) => z i)
        ((extChartAt (sphereProductModel n N) x).right_inv hy)
  have hd : ContDiffWithinAt ℝ k (fun y : Fin N → EuclideanSpace ℝ (Fin n) => y i)
      (range (sphereProductModel n N)) (extChartAt (sphereProductModel n N) x x) :=
    (show (Fin N → EuclideanSpace ℝ (Fin n)) →L[ℝ] EuclideanSpace ℝ (Fin n)
      from ContinuousLinearMap.proj i).contDiff.contDiffAt.contDiffWithinAt
  exact hd.congr_of_eventuallyEq_of_mem heq ⟨_, rfl⟩

private theorem contMDiff_sphereConfiguration_coe {n N : ℕ} (k : ℕ∞ω) :
    ContMDiff (sphereProductModel n N) 𝓘(ℝ, Fin N → SphereAmbient n) k
      (fun x : SphereConfiguration n N => fun i => (x i : SphereAmbient n)) := by
  let : Fact (Module.finrank ℝ (SphereAmbient n) = n + 1) := ⟨by simp [SphereAmbient]⟩
  apply contMDiff_pi_space.mpr
  intro i
  have hcoe : ContMDiff (𝓡 n) 𝓘(ℝ, SphereAmbient n) k
      (fun x : SpherePoint n => (x : SphereAmbient n)) := contMDiff_coe_sphere
  exact hcoe.comp (contMDiff_sphereEvaluation k i)

private def configurationDomain (n N : ℕ) : TopologicalSpace.Opens (Fin N → SphereAmbient n) :=
  ⟨{z | ∀ i, z i ≠ 0}, by
    have heq : {z : Fin N → SphereAmbient n | ∀ i, z i ≠ 0} =
        ⋂ i : Fin N, (fun z : Fin N → SphereAmbient n => z i) ⁻¹' ({0}ᶜ) := by
      ext z
      simp
    rw [heq]
    exact isOpen_iInter_of_finite (fun i => isClosed_singleton.isOpen_compl.preimage (continuous_apply i))⟩

private noncomputable def configurationRadialProjection {n N : ℕ}
    (z : configurationDomain n N) : SphereConfiguration n N :=
  fun i => (homeomorphUnitSphereProd (SphereAmbient n) ⟨z.1 i, z.2 i⟩).1

private theorem contMDiff_configurationRadialProjection {n N : ℕ} (k : ℕ∞ω) :
    ContMDiff 𝓘(ℝ, Fin N → SphereAmbient n) (sphereProductModel n N) k
      (configurationRadialProjection : configurationDomain n N → SphereConfiguration n N) := by
  let : Fact (Module.finrank ℝ (SphereAmbient n) = n + 1) := ⟨by simp [SphereAmbient]⟩
  apply contMDiff_sphereProduct
  intro i
  let r : configurationDomain n N → SphereAmbient n := fun z => ‖z.1 i‖⁻¹ • z.1 i
  have hr : ContMDiff 𝓘(ℝ, Fin N → SphereAmbient n) 𝓘(ℝ, SphereAmbient n) k r := by
    intro z
    have hz : z.1 i ≠ 0 := z.2 i
    have he : ContDiffAt ℝ k (fun y : Fin N → SphereAmbient n => y i) z.1 :=
      (show (Fin N → SphereAmbient n) →L[ℝ] SphereAmbient n
        from ContinuousLinearMap.proj i).contDiff.contDiffAt
    have hn := ((he.norm ℝ hz).inv (norm_ne_zero_iff.mpr hz)).smul he
    exact hn.contMDiffAt.comp z (contMDiff_subtype_val z)
  have hmem (z : configurationDomain n N) : r z ∈ sphere (0 : SphereAmbient n) 1 := by
    rw [mem_sphere_zero_iff_norm]
    simp [r, norm_smul, norm_ne_zero_iff.mpr (z.2 i)]
  have hr' : ContMDiff 𝓘(ℝ, Fin N → SphereAmbient n) (𝓡 n) k
      (Set.codRestrict r (sphere (0 : SphereAmbient n) 1) hmem) :=
    hr.codRestrict_sphere (n := n) hmem
  have heq : (fun z : configurationDomain n N => configurationRadialProjection z i) =
      Set.codRestrict r (sphere (0 : SphereAmbient n) 1) hmem := by
    funext z
    apply Subtype.ext
    change (1 : ℝ) • ‖z.1 i‖⁻¹ • z.1 i = r z
    simp only [one_smul, r]
  rw [heq]
  exact hr'

private noncomputable def configurationRadialExtension {n N : ℕ} {A : Type*} [Zero A]
    (f : SphereConfiguration n N → A) (z : Fin N → SphereAmbient n) : A :=
  if hz : ∀ i, z i ≠ 0 then f (configurationRadialProjection ⟨z, hz⟩) else 0

private theorem contDiffAt_configurationRadialExtension {n N : ℕ} {A : Type*}
    [NormedAddCommGroup A] [NormedSpace ℝ A] {k : ℕ∞ω}
    (f : SphereConfiguration n N → A)
    (hf : ContMDiff (sphereProductModel n N) 𝓘(ℝ, A) k f)
    (z : Fin N → SphereAmbient n) (hz : ∀ i, z i ≠ 0) :
    ContDiffAt ℝ k (configurationRadialExtension f) z := by
  let z' : configurationDomain n N := ⟨z, hz⟩
  have h := hf.comp (contMDiff_configurationRadialProjection (n := n) (N := N) k)
  have heq : (fun u : configurationDomain n N => configurationRadialExtension f u.1) =
      fun u => f (configurationRadialProjection u) := by
    funext u
    have hu : ∀ i, u.1 i ≠ 0 := u.2
    rw [configurationRadialExtension, dif_pos hu]
  have hlocal : ContMDiffAt 𝓘(ℝ, Fin N → SphereAmbient n) 𝓘(ℝ, A) k
      (fun u : configurationDomain n N => configurationRadialExtension f u.1) z' := by
    rw [heq]
    exact h z'
  exact (contMDiffAt_subtype_iff.mp hlocal).contDiffAt


private theorem configurationRadialExtension_section {n N : ℕ} {A : Type*} [Zero A]
    (f : SphereConfiguration n N → A) (x : SphereConfiguration n N) (i : Fin N)
    (y : SphereAmbient n) :
    configurationRadialExtension f (Function.update (fun j => (x j : SphereAmbient n)) i y) =
      sphereRadialExtension (fun z => f (Function.update x i z)) y := by
  by_cases hy : y = 0
  · have hbad : ¬ ∀ j : Fin N,
        Function.update (fun j => (x j : SphereAmbient n)) i y j ≠ 0 := by
      intro h
      exact h i (by simp [hy])
    simp only [configurationRadialExtension, dif_neg hbad, sphereRadialExtension, dif_pos hy]
  · have hgood : ∀ j : Fin N,
        Function.update (fun j => (x j : SphereAmbient n)) i y j ≠ 0 := by
      intro j
      by_cases hj : j = i
      · subst j
        simpa only [Function.update_self] using hy
      · simpa only [Function.update_of_ne hj] using ne_zero_of_mem_unit_sphere (x j)
    simp only [configurationRadialExtension, dif_pos hgood, sphereRadialExtension, dif_neg hy]
    congr 1
    funext j
    apply Subtype.ext
    by_cases hj : j = i
    · subst j
      simp only [configurationRadialProjection, Function.update_self]
    · simp only [configurationRadialProjection, Function.update_of_ne hj]
      change (1 : ℝ) • ‖(x j : SphereAmbient n)‖⁻¹ • (x j : SphereAmbient n) = (x j : SphereAmbient n)
      simp only [one_smul, norm_eq_of_mem_sphere, inv_one]

private noncomputable def coordinateInsertion {n N : ℕ} (i : Fin N) :
    SphereAmbient n →L[ℝ] (Fin N → SphereAmbient n) :=
  ContinuousLinearMap.pi (Pi.single i (ContinuousLinearMap.id ℝ (SphereAmbient n)))

private theorem coordinateInsertion_apply {n N : ℕ} (i : Fin N) (v : SphereAmbient n) :
    coordinateInsertion i v = Pi.single i v := by
  ext j
  by_cases h : j = i <;> simp [coordinateInsertion, h]

private theorem configurationRadialExtension_section_fderiv {n N : ℕ} {A : Type*}
    [NormedAddCommGroup A] [NormedSpace ℝ A]
    (f : SphereConfiguration n N → A)
    (hf : ContMDiff (sphereProductModel n N) 𝓘(ℝ, A) 1 f)
    (x : SphereConfiguration n N) (i : Fin N) :
    fderiv ℝ (sphereRadialExtension (fun z => f (Function.update x i z))) (x i : SphereAmbient n) =
      (fderiv ℝ (configurationRadialExtension f) (fun j => (x j : SphereAmbient n))).comp
        (coordinateInsertion i) := by
  have hdf := (contDiffAt_configurationRadialExtension f hf (fun j => (x j : SphereAmbient n))
    (fun j => ne_zero_of_mem_unit_sphere (x j))).differentiableAt one_ne_zero
  have hdpoint : HasFDerivAt (configurationRadialExtension f)
      (fderiv ℝ (configurationRadialExtension f) (fun j => (x j : SphereAmbient n)))
      (Function.update (fun j => (x j : SphereAmbient n)) i (x i : SphereAmbient n)) := by
    rw [Function.update_eq_self]
    exact hdf.hasFDerivAt
  have hdinsert : HasFDerivAt (Function.update (fun j => (x j : SphereAmbient n)) i)
      (coordinateInsertion i) (x i : SphereAmbient n) :=
    hasFDerivAt_update (fun j => (x j : SphereAmbient n)) (x i : SphereAmbient n)
  have hchain := hdpoint.comp (x i : SphereAmbient n) hdinsert
  have heq : (configurationRadialExtension f ∘ Function.update (fun j => (x j : SphereAmbient n)) i) =
      sphereRadialExtension (fun z => f (Function.update x i z)) := by
    funext y
    exact configurationRadialExtension_section f x i y
  rw [heq] at hchain
  exact hchain.fderiv

private theorem continuous_configurationRadial_fderiv {n N : ℕ} {A : Type*}
    [NormedAddCommGroup A] [NormedSpace ℝ A]
    (f : SphereConfiguration n N → A)
    (hf : ContMDiff (sphereProductModel n N) 𝓘(ℝ, A) 1 f) :
    Continuous (fun x : SphereConfiguration n N =>
      fderiv ℝ (configurationRadialExtension f) (fun j => (x j : SphereAmbient n))) := by
  apply continuous_iff_continuousAt.mpr
  intro x
  have hd := (contDiffAt_configurationRadialExtension f hf (fun j => (x j : SphereAmbient n))
    (fun j => ne_zero_of_mem_unit_sphere (x j))).continuousAt_fderiv one_ne_zero
  exact hd.comp ((contMDiff_sphereConfiguration_coe (n := n) (N := N) 1).continuous.continuousAt)

private theorem configuration_divergence_coordinate_trace {n N : ℕ}
    (V : SphereConfiguration n N → SphereAmbient n)
    (hV : ContMDiff (sphereProductModel n N) 𝓘(ℝ, SphereAmbient n) 1 V)
    (x : SphereConfiguration n N) (i : Fin N) :
    sphereTangentDivergence (fun z => V (Function.update x i z)) (x i) =
      ∑ j : Fin (n + 1),
        fderiv ℝ (configurationRadialExtension V) (fun l => (x l : SphereAmbient n))
          (Pi.single i (EuclideanSpace.single j (1 : ℝ))) j := by
  have hs : ContMDiff (𝓡 n) 𝓘(ℝ, SphereAmbient n) 1
      (fun z => V (Function.update x i z)) := hV.comp (contMDiff_sphereSection 1 x i)
  rw [tangentDivergence_eq_fderiv_trace _ hs (x i), configurationRadialExtension_section_fderiv V hV x i]
  simp only [ContinuousLinearMap.comp_apply, coordinateInsertion_apply]

private theorem continuous_configuration_divergence_coordinate {n N : ℕ}
    (V : SphereConfiguration n N → SphereAmbient n)
    (hV : ContMDiff (sphereProductModel n N) 𝓘(ℝ, SphereAmbient n) 1 V)
    (i : Fin N) :
    Continuous (fun x : SphereConfiguration n N =>
      sphereTangentDivergence (fun z => V (Function.update x i z)) (x i)) := by
  have hD := continuous_configurationRadial_fderiv V hV
  have heq : (fun x : SphereConfiguration n N =>
      sphereTangentDivergence (fun z => V (Function.update x i z)) (x i)) =
      fun x => ∑ j : Fin (n + 1),
        fderiv ℝ (configurationRadialExtension V) (fun l => (x l : SphereAmbient n))
          (Pi.single i (EuclideanSpace.single j (1 : ℝ))) j := by
    funext x
    exact configuration_divergence_coordinate_trace V hV x i
  rw [heq]
  apply continuous_finsetSum
  intro j _
  exact (PiLp.proj (p := 2) (𝕜 := ℝ) (fun _ : Fin (n + 1) => ℝ) j).continuous.comp
    (hD.clm_apply continuous_const)

private theorem integral_configuration_divergence_coordinate_eq_zero {n N : ℕ}
    (V : SphereConfiguration n N → SphereAmbient n)
    (hV : ContMDiff (sphereProductModel n N) 𝓘(ℝ, SphereAmbient n) 1 V)
    (i : Fin N)
    (hTangent : ∀ x : SphereConfiguration n N, inner ℝ (x i : SphereAmbient n) (V x) = 0) :
    (∫ x, sphereTangentDivergence (fun z => V (Function.update x i z)) (x i)
      ∂sphereProductMeasure n N) = 0 := by
  cases N with
  | zero => exact Fin.elim0 i
  | succ N =>
    let σ := sphereUniformMeasure n
    let μ := Measure.pi (fun _ : Fin N => σ)
    let H : SphereConfiguration n (N + 1) → ℝ := fun x =>
      sphereTangentDivergence (fun z => V (Function.update x i z)) (x i)
    have hI : Integrable H (sphereProductMeasure n (N + 1)) := by
      simpa only [integrableOn_univ] using
        (continuous_configuration_divergence_coordinate V hV i).continuousOn.integrableOn_compact
          (μ := sphereProductMeasure n (N + 1)) (K := Set.univ) isCompact_univ
    let e := MeasurableEquiv.piFinSuccAbove (fun _ : Fin (N + 1) => SpherePoint n) i
    have hmp : MeasurePreserving e (sphereProductMeasure n (N + 1)) (σ.prod μ) :=
      measurePreserving_piFinSuccAbove (fun _ => σ) i
    let q := H ∘ e.symm
    have hq : Integrable q (σ.prod μ) :=
      (hmp.symm.integrable_comp_emb e.symm.measurableEmbedding).mpr hI
    have hqval (y : SpherePoint n) (z : Fin N → SpherePoint n) : q (y, z) =
        sphereTangentDivergence (fun w => V (i.insertNth w z)) y := by
      change sphereTangentDivergence
        (fun w => V (Function.update (i.insertNth (α := fun _ => SpherePoint n) y z) i w)) ((i.insertNth (α := fun _ => SpherePoint n) y z) i) = _
      simp only [Fin.insertNth_apply_same, Fin.update_insertNth]
    have hinner (z : Fin N → SpherePoint n) : (∫ y, q (y, z) ∂σ) = 0 := by
      let x0 : SpherePoint n := ⟨EuclideanSpace.single 0 (1 : ℝ), by simp⟩
      have hs : ContMDiff (𝓡 n) (sphereProductModel n (N + 1)) 1
          (fun y => i.insertNth (α := fun _ => SpherePoint n) y z) := by
        have h := contMDiff_sphereSection 1 (i.insertNth (α := fun _ => SpherePoint n) x0 z) i
        simpa only [Fin.update_insertNth] using h
      have hW : ContMDiff (𝓡 n) 𝓘(ℝ, SphereAmbient n) 1
          (fun y => V (i.insertNth (α := fun _ => SpherePoint n) y z)) := hV.comp hs
      have hWT (y : SpherePoint n) : inner ℝ (y : SphereAmbient n) (V (i.insertNth (α := fun _ => SpherePoint n) y z)) = 0 := by
        simpa only [Fin.insertNth_apply_same] using hTangent (i.insertNth (α := fun _ => SpherePoint n) y z)
      simp_rw [hqval]
      exact integral_tangentDivergence_eq_zero _ hW hWT
    calc
      (∫ x, H x ∂sphereProductMeasure n (N + 1)) = ∫ z, q z ∂σ.prod μ :=
        (hmp.symm.integral_comp e.symm.measurableEmbedding H).symm
      _ = ∫ z, ∫ y, q (y, z) ∂σ ∂μ := integral_prod_symm q hq
      _ = 0 := by simp only [hinner, integral_zero]

private theorem continuous_sphereProductDivergence {n N : ℕ}
    (V : Fin N → SphereConfiguration n N → SphereAmbient n)
    (hV : ∀ i, ContMDiff (sphereProductModel n N) 𝓘(ℝ, SphereAmbient n) 1 (V i)) :
    Continuous (sphereProductDivergence V) := by
  unfold sphereProductDivergence
  exact continuous_finsetSum _ (fun i _ => continuous_configuration_divergence_coordinate (V i) (hV i) i)

private theorem integral_sphereProductDivergence_eq_zero {n N : ℕ}
    (V : Fin N → SphereConfiguration n N → SphereAmbient n)
    (hV : ∀ i, ContMDiff (sphereProductModel n N) 𝓘(ℝ, SphereAmbient n) 1 (V i))
    (hTangent : ∀ (x : SphereConfiguration n N) (i : Fin N),
      inner ℝ (x i : SphereAmbient n) (V i x) = 0) :
    (∫ x, sphereProductDivergence V x ∂sphereProductMeasure n N) = 0 := by
  have hI (i : Fin N) : Integrable (fun x =>
      sphereTangentDivergence (fun z => V i (Function.update x i z)) (x i))
      (sphereProductMeasure n N) := by
    simpa only [integrableOn_univ] using
      (continuous_configuration_divergence_coordinate (V i) (hV i) i).continuousOn.integrableOn_compact
        (μ := sphereProductMeasure n N) (K := Set.univ) isCompact_univ
  unfold sphereProductDivergence
  rw [integral_finsetSum _ (fun i _ => hI i)]
  apply Finset.sum_eq_zero
  intro i _
  exact integral_configuration_divergence_coordinate_eq_zero (V i) (hV i) i (fun x => hTangent x i)

private theorem sphereProductDivergence_smul {n N : ℕ}
    (f : SphereConfiguration n N → ℝ)
    (V : Fin N → SphereConfiguration n N → SphereAmbient n)
    (hf : ContMDiff (sphereProductModel n N) 𝓘(ℝ, ℝ) 1 f)
    (hV : ∀ i, ContMDiff (sphereProductModel n N) 𝓘(ℝ, SphereAmbient n) 1 (V i))
    (hTangent : ∀ (x : SphereConfiguration n N) (i : Fin N),
      inner ℝ (x i : SphereAmbient n) (V i x) = 0)
    (x : SphereConfiguration n N) :
    sphereProductDivergence (fun i y => f y • V i y) x =
      f x * sphereProductDivergence V x +
        ∑ i : Fin N, inner ℝ (sphereProductGradient f i x) (V i x) := by
  have hcoord (i : Fin N) :
      sphereTangentDivergence (fun z => f (Function.update x i z) • V i (Function.update x i z)) (x i) =
        f x * sphereTangentDivergence (fun z => V i (Function.update x i z)) (x i) +
          inner ℝ (sphereProductGradient f i x) (V i x) := by
    have hfs : ContMDiff (𝓡 n) 𝓘(ℝ, ℝ) 1 (fun z => f (Function.update x i z)) :=
      hf.comp (contMDiff_sphereSection 1 x i)
    have hVs : ContMDiff (𝓡 n) 𝓘(ℝ, SphereAmbient n) 1 (fun z => V i (Function.update x i z)) :=
      (hV i).comp (contMDiff_sphereSection 1 x i)
    have hTs (z : SpherePoint n) : inner ℝ (z : SphereAmbient n) (V i (Function.update x i z)) = 0 := by
      simpa only [Function.update_self] using hTangent (Function.update x i z) i
    simpa only [Function.update_eq_self, sphereProductGradient] using
      tangentDivergence_smul _ _ hfs hVs hTs (x i)
  simp only [sphereProductDivergence]
  simp_rw [hcoord]
  rw [Finset.sum_add_distrib, Finset.mul_sum]

/-- Integration by parts for a C¹ function and C¹ tangent vector field on a finite
product of unit spheres, with the normalized polar product measure. -/
theorem sphere_product_tangential_integration_by_parts
    {n N : ℕ}
    (f : SphereConfiguration n N → ℝ)
    (V : Fin N → SphereConfiguration n N → SphereAmbient n)
    (hf : ContMDiff (sphereProductModel n N) 𝓘(ℝ, ℝ) 1 f)
    (hV : ∀ i, ContMDiff (sphereProductModel n N) 𝓘(ℝ, SphereAmbient n) 1 (V i))
    (hTangent : ∀ (x : SphereConfiguration n N) (i : Fin N),
      inner ℝ (x i : SphereAmbient n) (V i x) = 0) :
    Integrable (sphereProductDivergence V) (sphereProductMeasure n N) ∧
    Integrable (fun x => f x * sphereProductDivergence V x)
      (sphereProductMeasure n N) ∧
    Integrable (fun x => ∑ i : Fin N, inner ℝ (sphereProductGradient f i x) (V i x))
      (sphereProductMeasure n N) ∧
    (∫ x, sphereProductDivergence V x ∂(sphereProductMeasure n N)) = 0 ∧
    (∫ x, f x * sphereProductDivergence V x ∂(sphereProductMeasure n N)) =
      -(∫ x, ∑ i : Fin N, inner ℝ (sphereProductGradient f i x) (V i x)
        ∂(sphereProductMeasure n N)) := by
  have hW (i : Fin N) : ContMDiff (sphereProductModel n N) 𝓘(ℝ, SphereAmbient n) 1
      (fun x => f x • V i x) := hf.smul (hV i)
  have hWT (x : SphereConfiguration n N) (i : Fin N) :
      inner ℝ (x i : SphereAmbient n) (f x • V i x) = 0 := by
    rw [inner_smul_right, hTangent x i, mul_zero]
  have hmul : Continuous (fun x => f x * sphereProductDivergence V x) :=
    hf.continuous.mul (continuous_sphereProductDivergence V hV)
  have hpair : Continuous (fun x => ∑ i : Fin N,
      inner ℝ (sphereProductGradient f i x) (V i x)) := by
    have heq : (fun x => ∑ i : Fin N, inner ℝ (sphereProductGradient f i x) (V i x)) =
        fun x => sphereProductDivergence (fun i y => f y • V i y) x - f x * sphereProductDivergence V x := by
      funext x
      rw [sphereProductDivergence_smul f V hf hV hTangent x]
      ring
    rw [heq]
    exact (continuous_sphereProductDivergence _ hW).sub hmul
  have hI : Integrable (sphereProductDivergence V) (sphereProductMeasure n N) := by
    simpa only [integrableOn_univ] using
      (continuous_sphereProductDivergence V hV).continuousOn.integrableOn_compact
        (μ := sphereProductMeasure n N) (K := Set.univ) isCompact_univ
  have hImul : Integrable (fun x => f x * sphereProductDivergence V x) (sphereProductMeasure n N) := by
    simpa only [integrableOn_univ] using hmul.continuousOn.integrableOn_compact
      (μ := sphereProductMeasure n N) (K := Set.univ) isCompact_univ
  have hIpair : Integrable (fun x => ∑ i : Fin N,
      inner ℝ (sphereProductGradient f i x) (V i x)) (sphereProductMeasure n N) := by
    simpa only [integrableOn_univ] using hpair.continuousOn.integrableOn_compact
      (μ := sphereProductMeasure n N) (K := Set.univ) isCompact_univ
  refine ⟨hI, hImul, hIpair, integral_sphereProductDivergence_eq_zero V hV hTangent, ?_⟩
  have hzero := integral_sphereProductDivergence_eq_zero (fun i x => f x • V i x) hW hWT
  simp_rw [sphereProductDivergence_smul f V hf hV hTangent] at hzero
  rw [integral_add hImul hIpair] at hzero
  linarith

private theorem contMDiff_configurationRadial_fderiv {n N : ℕ}
    (g : SphereConfiguration n N → ℝ)
    (hg : ContMDiff (sphereProductModel n N) 𝓘(ℝ, ℝ) 2 g) :
    ContMDiff (sphereProductModel n N)
      𝓘(ℝ, (Fin N → SphereAmbient n) →L[ℝ] ℝ) 1
      (fun x : SphereConfiguration n N =>
        fderiv ℝ (configurationRadialExtension g) (fun j => (x j : SphereAmbient n))) := by
  intro x
  have hd : ContDiffAt ℝ 1 (fderiv ℝ (configurationRadialExtension g))
      (fun j => (x j : SphereAmbient n)) :=
    (contDiffAt_configurationRadialExtension g hg (fun j => (x j : SphereAmbient n))
      (fun j => ne_zero_of_mem_unit_sphere (x j))).fderiv_right (by norm_num)
  exact hd.contMDiffAt.comp x (contMDiff_sphereConfiguration_coe 1 x)

private theorem contMDiff_sphereProductGradient {n N : ℕ}
    (g : SphereConfiguration n N → ℝ)
    (hg : ContMDiff (sphereProductModel n N) 𝓘(ℝ, ℝ) 2 g) (i : Fin N) :
    ContMDiff (sphereProductModel n N) 𝓘(ℝ, SphereAmbient n) 1
      (fun x => sphereProductGradient g i x) := by
  let G : SphereConfiguration n N → SphereAmbient n := fun x =>
    (InnerProductSpace.toDual ℝ (SphereAmbient n)).symm
      ((fderiv ℝ (configurationRadialExtension g) (fun j => (x j : SphereAmbient n))).comp
        (coordinateInsertion i))
  have hP : ContMDiff (sphereProductModel n N) 𝓘(ℝ, SphereAmbient n →L[ℝ] ℝ) 1
      (fun x : SphereConfiguration n N => (fderiv ℝ (configurationRadialExtension g)
        (fun j => (x j : SphereAmbient n))).comp (coordinateInsertion i)) :=
    (contMDiff_configurationRadial_fderiv g hg).clm_comp contMDiff_const
  have hG : ContMDiff (sphereProductModel n N) 𝓘(ℝ, SphereAmbient n) 1 G :=
    (InnerProductSpace.toDual ℝ (SphereAmbient n)).symm.toContinuousLinearEquiv.toContinuousLinearMap.contMDiff.comp hP
  have hx : ContMDiff (sphereProductModel n N) 𝓘(ℝ, SphereAmbient n) 1
      (fun x : SphereConfiguration n N => (x i : SphereAmbient n)) :=
    contMDiff_pi_space.mp (contMDiff_sphereConfiguration_coe 1) i
  have hi : ContMDiff (sphereProductModel n N) 𝓘(ℝ, ℝ) 1
      (fun x => inner ℝ (x i : SphereAmbient n) (G x)) :=
    ((innerSL ℝ).contMDiff.comp hx).clm_apply hG
  have heq : (fun x => sphereProductGradient g i x) =
      fun x : SphereConfiguration n N => G x - inner ℝ (x i : SphereAmbient n) (G x) • (x i : SphereAmbient n) := by
    funext x
    unfold sphereProductGradient sphereTangentGradient gradient
    rw [configurationRadialExtension_section_fderiv g (hg.of_le (by norm_num)) x i,
      Submodule.starProjection_orthogonal_val, Submodule.starProjection_singleton]
    simp only [norm_eq_of_mem_sphere, one_pow, RCLike.ofReal_one, div_one]
    rfl
  rw [heq]
  exact hG.sub (hi.smul hx)

/-- The weighted-gradient specialization. C² regularity of `g` supplies the C¹
regularity of its tangent gradient; the real weight `rho` need not be positive. -/
theorem sphere_product_weighted_gradient_integration_by_parts
    {n N : ℕ}
    (f rho g : SphereConfiguration n N → ℝ)
    (hf : ContMDiff (sphereProductModel n N) 𝓘(ℝ, ℝ) 1 f)
    (hrho : ContMDiff (sphereProductModel n N) 𝓘(ℝ, ℝ) 1 rho)
    (hg : ContMDiff (sphereProductModel n N) 𝓘(ℝ, ℝ) 2 g) :
    let V : Fin N → SphereConfiguration n N → SphereAmbient n :=
      fun i x => rho x • sphereProductGradient g i x
    Integrable (sphereProductDivergence V) (sphereProductMeasure n N) ∧
    Integrable (fun x => f x * sphereProductDivergence V x)
      (sphereProductMeasure n N) ∧
    Integrable (fun x => rho x *
      ∑ i : Fin N, inner ℝ (sphereProductGradient f i x) (sphereProductGradient g i x))
      (sphereProductMeasure n N) ∧
    (∫ x, sphereProductDivergence V x ∂(sphereProductMeasure n N)) = 0 ∧
    (∫ x, f x * sphereProductDivergence V x ∂(sphereProductMeasure n N)) =
      -(∫ x, rho x *
        ∑ i : Fin N, inner ℝ (sphereProductGradient f i x) (sphereProductGradient g i x)
        ∂(sphereProductMeasure n N)) := by
  dsimp only
  have hV (i : Fin N) : ContMDiff (sphereProductModel n N) 𝓘(ℝ, SphereAmbient n) 1
      (fun x => rho x • sphereProductGradient g i x) :=
    hrho.smul (contMDiff_sphereProductGradient g hg i)
  have hT (x : SphereConfiguration n N) (i : Fin N) :
      inner ℝ (x i : SphereAmbient n) (rho x • sphereProductGradient g i x) = 0 := by
    rw [inner_smul_right]
    have ht : inner ℝ (x i : SphereAmbient n) (sphereProductGradient g i x) = 0 :=
      tangentGradient_tangent (fun y => g (Function.update x i y)) (x i)
    rw [ht, mul_zero]
  have h := sphere_product_tangential_integration_by_parts f
    (fun i x => rho x • sphereProductGradient g i x) hf hV hT
  simpa only [inner_smul_right, Finset.mul_sum] using h


/-- C¹ compatibility with the actual manifold differential through the sphere
inclusion. The derivative kills the normal direction and factors through the
actual orthogonal tangent projection. -/
private theorem radialExtension_actual_differential {n : ℕ} {A : Type*}
    [NormedAddCommGroup A] [NormedSpace ℝ A]
    (f : SpherePoint n → A) (hf : ContMDiff (𝓡 n) 𝓘(ℝ, A) 1 f)
    (x : SpherePoint n) :
    let D := fderiv ℝ (sphereRadialExtension f) (x : SphereAmbient n)
    let J := mvfderiv (𝓡 n) ((↑) : SpherePoint n → SphereAmbient n) x
    let P := (ℝ ∙ (x : SphereAmbient n))ᗮ.starProjection
    D (x : SphereAmbient n) = 0 ∧ D.comp J = mvfderiv (𝓡 n) f x ∧ D.comp P = D := by
  let : Fact (Module.finrank ℝ (SphereAmbient n) = n + 1) := ⟨by simp [SphereAmbient]⟩
  dsimp only
  let D := fderiv ℝ (sphereRadialExtension f) (x : SphereAmbient n)
  have hd := (contDiffAt_radialExtension f hf (ne_zero_of_mem_unit_sphere x)).differentiableAt one_ne_zero
  have hnormal : D (x : SphereAmbient n) = 0 := by
    let l : ℝ → SphereAmbient n := fun t => (1 + t) • (x : SphereAmbient n)
    have hl : HasDerivAt l (x : SphereAmbient n) 0 := by
      simpa [l] using (((hasDerivAt_id (0 : ℝ)).const_add 1).smul_const (x : SphereAmbient n))
    have hd' : DifferentiableAt ℝ (sphereRadialExtension f) (l 0) := by simpa [l] using hd
    have hpos : ∀ᶠ t : ℝ in 𝓝 0, 0 < 1 + t :=
      (isOpen_lt continuous_const (continuous_const.add continuous_id)).mem_nhds (by simp)
    have he : sphereRadialExtension f ∘ l =ᶠ[𝓝 0] fun _ => sphereRadialExtension f (x : SphereAmbient n) :=
      hpos.mono fun t ht => radialExtension_pos_smul f (x : SphereAmbient n) ht
    have hdv := hd'.hasFDerivAt.comp_hasDerivAt 0 hl
    have hz := (hasDerivAt_const 0 (sphereRadialExtension f (x : SphereAmbient n))).congr_of_eventuallyEq he
    simpa [l, D] using hdv.unique hz
  have he : sphereRadialExtension f ∘ ((↑) : SpherePoint n → SphereAmbient n) = f :=
    funext (radialExtension_on_sphere f)
  have hco := (contMDiff_coe_sphere (n := n) (m := 1) x).mdifferentiableAt one_ne_zero
  have hchain : D.comp (mvfderiv (𝓡 n) ((↑) : SpherePoint n → SphereAmbient n) x) =
      mvfderiv (𝓡 n) f x := by
    have hc := mfderiv_comp x hd.mdifferentiableAt hco
    rw [he, mfderiv_eq_fderiv] at hc
    exact hc.symm
  refine ⟨hnormal, hchain, ?_⟩
  ext v
  rw [ContinuousLinearMap.comp_apply, Submodule.starProjection_orthogonal_val,
    Submodule.starProjection_unit_singleton ℝ (norm_eq_of_mem_sphere x), map_sub, map_smul,
    hnormal, smul_zero, sub_zero]

/-- The projected gradient pairs with the actual sphere differential, not only
with an arbitrarily named operator. -/
private theorem tangentGradient_pairing_mvfderiv {n : ℕ}
    (f : SpherePoint n → ℝ) (hf : ContMDiff (𝓡 n) 𝓘(ℝ, ℝ) 1 f)
    (x : SpherePoint n) (u : TangentSpace (𝓡 n) x) :
    inner ℝ (sphereTangentGradient f x)
      (mvfderiv (𝓡 n) ((↑) : SpherePoint n → SphereAmbient n) x u) =
      mvfderiv (𝓡 n) f x u := by
  let : Fact (Module.finrank ℝ (SphereAmbient n) = n + 1) := ⟨by simp [SphereAmbient]⟩
  let J := mvfderiv (𝓡 n) ((↑) : SpherePoint n → SphereAmbient n) x
  have hmem : J u ∈ (ℝ ∙ (x : SphereAmbient n))ᗮ := by
    rw [← range_mvfderiv_subtypeVal (n := n) x]
    exact ⟨u, rfl⟩
  rw [tangentGradient_pairing f x (J u)
    (Submodule.mem_orthogonal_singleton_iff_inner_right.mp hmem)]
  exact congrArg (fun T : TangentSpace (𝓡 n) x →L[ℝ] ℝ => T u)
    (radialExtension_actual_differential f hf x).2.1

/-- The ambient coordinate trace equals the trace of the projected derivative
extended by zero on the normal direction. Together with the actual differential
identity above, this is the induced tangent covariant-derivative trace when the
field is tangent. For a non-tangent map it is not the divergence of its tangent
projection. -/
private theorem tangentDivergence_eq_projected_trace {n : ℕ}
    (V : SpherePoint n → SphereAmbient n)
    (hV : ContMDiff (𝓡 n) 𝓘(ℝ, SphereAmbient n) 1 V) (x : SpherePoint n) :
    let D := fderiv ℝ (sphereRadialExtension V) (x : SphereAmbient n)
    let P := (ℝ ∙ (x : SphereAmbient n))ᗮ.starProjection
    sphereTangentDivergence V x =
      ∑ j : Fin (n + 1), P (D (P (EuclideanSpace.single j (1 : ℝ)))) j := by
  intro D P
  obtain ⟨hnormal, _, hfactor⟩ := radialExtension_actual_differential V hV x
  change D (x : SphereAmbient n) = 0 at hnormal
  have hDP (v : SphereAmbient n) : D (P v) = D v :=
    congrArg (fun T : SphereAmbient n →L[ℝ] SphereAmbient n => T v) hfactor
  have hP (v : SphereAmbient n) : P v = v - inner ℝ (x : SphereAmbient n) v • (x : SphereAmbient n) := by
    simp only [P, Submodule.starProjection_orthogonal_val,
      Submodule.starProjection_unit_singleton ℝ (norm_eq_of_mem_sphere x)]
  have hzero : (∑ j : Fin (n + 1),
      inner ℝ (x : SphereAmbient n) (D (EuclideanSpace.single j (1 : ℝ))) * (x : SphereAmbient n) j) = 0 := by
    have he := sum_dual_single_mul ((innerSL ℝ (x : SphereAmbient n)).comp D) (x : SphereAmbient n)
    simpa only [ContinuousLinearMap.comp_apply, innerSL_apply_apply, hnormal, inner_zero_right] using he
  rw [tangentDivergence_eq_fderiv_trace V hV x]
  simp_rw [hDP, hP]
  simp only [PiLp.sub_apply, PiLp.smul_apply, smul_eq_mul, Finset.sum_sub_distrib]
  rw [hzero, sub_zero]


/-- Basis-independent trace on the actual induced Euclidean tangent subspace.
For tangent fields, projection of the ambient derivative along the inclusion is
the induced covariant derivative, as identified by the preceding chain rule. -/
private theorem tangentDivergence_eq_tangent_trace {n : ℕ}
    (V : SpherePoint n → SphereAmbient n)
    (hV : ContMDiff (𝓡 n) 𝓘(ℝ, SphereAmbient n) 1 V) (x : SpherePoint n) :
    let K := (ℝ ∙ (x : SphereAmbient n))ᗮ
    let D := fderiv ℝ (sphereRadialExtension V) (x : SphereAmbient n)
    sphereTangentDivergence V x =
      LinearMap.trace ℝ K (K.orthogonalProjectionOnto.toLinearMap.comp
        (D.toLinearMap.comp K.subtype)) := by
  intro K D
  have htrace : sphereTangentDivergence V x = LinearMap.trace ℝ (SphereAmbient n) D.toLinearMap := by
    rw [tangentDivergence_eq_fderiv_trace V hV x,
      LinearMap.trace_eq_matrix_trace ℝ (EuclideanSpace.basisFun (Fin (n + 1)) ℝ).toBasis]
    simp [Matrix.trace, LinearMap.toMatrix_apply, OrthonormalBasis.coe_toBasis,
      OrthonormalBasis.coe_toBasis_repr_apply, D]
  have hfactor : D.toLinearMap.comp (K.subtype.comp K.orthogonalProjectionOnto.toLinearMap) =
      D.toLinearMap := by
    apply LinearMap.ext
    intro v
    change D (K.starProjection v) = D v
    exact congrArg (fun T : SphereAmbient n →L[ℝ] SphereAmbient n => T v)
      (radialExtension_actual_differential V hV x).2.2
  calc
    sphereTangentDivergence V x = LinearMap.trace ℝ (SphereAmbient n) D.toLinearMap := htrace
    _ = LinearMap.trace ℝ (SphereAmbient n)
        (D.toLinearMap.comp (K.subtype.comp K.orthogonalProjectionOnto.toLinearMap)) :=
      congrArg (LinearMap.trace ℝ (SphereAmbient n)) hfactor.symm
    _ = LinearMap.trace ℝ K (K.orthogonalProjectionOnto.toLinearMap.comp
        (D.toLinearMap.comp K.subtype)) :=
      LinearMap.trace_comp_comm' K.orthogonalProjectionOnto.toLinearMap (D.toLinearMap.comp K.subtype)

end AutoSamplingTheory.TechnicalLemmas.Geometry.SphereTangentialIntegration
