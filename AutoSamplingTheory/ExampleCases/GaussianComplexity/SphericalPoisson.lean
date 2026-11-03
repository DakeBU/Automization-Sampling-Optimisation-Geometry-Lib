import AutoSamplingTheory.TechnicalLemmas.Analysis.Harmonic.SphericalMeanValue
import AutoSamplingTheory.TechnicalLemmas.Analysis.Harmonic.PoissonKernel

/-!
Actual normalized Euclidean sphere moments for Gaussian Complexity Appendix A.1.
The source starts with n >= 2 and also contains a trailing n >= 3 clause.
The n = 2 extension is ASTIS mathematics; the paper's Eq24 application retains
n >= 3. The direct mean-value/zero-flux route is not the author's general
Poisson representation proof and does not certify that general theorem.
-/

open MeasureTheory Metric Set Filter
open scoped Topology RealInnerProductSpace

namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.SphericalPoisson

set_option autoImplicit false
noncomputable section

private theorem sphere_geometry {n : ℕ} (j : Fin n) (r : ℝ)
    (ζ : sphere (0 : EuclideanSpace ℝ (Fin n)) 1) :
    ‖(EuclideanSpace.single j (1 : ℝ))‖ = 1 ∧
    ‖r • ζ.1 - EuclideanSpace.single j (1 : ℝ)‖ ^ 2 =
      1 + r ^ 2 - 2 * r * WithLp.ofLp ζ.1 j ∧
    inner ℝ (r • ζ.1 - EuclideanSpace.single j (1 : ℝ)) ζ.1 =
      r - WithLp.ofLp ζ.1 j := by
  have hζ : ‖ζ.1‖ = 1 := mem_sphere_zero_iff_norm.mp ζ.property
  have he : ‖EuclideanSpace.single j (1 : ℝ)‖ = 1 := by simp
  have hi : inner ℝ (r • ζ.1) (EuclideanSpace.single j (1 : ℝ)) =
      r * WithLp.ofLp ζ.1 j := by
    rw [real_inner_smul_left]
    simp [EuclideanSpace.inner_single_right]
  refine ⟨he, ?_, ?_⟩
  · rw [norm_sub_sq_real, norm_smul, hζ, he, hi]
    simp only [Real.norm_eq_abs, mul_one, one_pow, sq_abs]
    ring
  · rw [inner_sub_left, real_inner_smul_left, real_inner_self_eq_norm_sq, hζ]
    simp [EuclideanSpace.inner_single_left]

private theorem pole_excluded {n : ℕ} (j : Fin n) {R : ℝ} (hR : R < 1)
    {x : EuclideanSpace ℝ (Fin n)} (hx : x ∈ closedBall 0 R) :
    x ≠ EuclideanSpace.single j (1 : ℝ) := by
  intro he
  have hn : ‖x‖ ≤ R := mem_closedBall_zero_iff.mp hx
  rw [he] at hn
  simp at hn
  linarith

private def potentialProfile (n : ℕ) (s : ℝ) : ℝ :=
  if n = 2 then (1 / 2 : ℝ) * Real.log s else s ^ (1 - (n : ℝ) / 2)

private def potential {n : ℕ} (e x : EuclideanSpace ℝ (Fin n)) : ℝ :=
  potentialProfile n (‖x - e‖ ^ 2)

private def potentialCoefficient (n : ℕ) : ℝ := if n = 2 then 1 else 2 - (n : ℝ)

private theorem potential_data {n : ℕ} (hn : 2 ≤ n)
    (e x : EuclideanSpace ℝ (Fin n)) (hx : x ≠ e) :
    ContDiffAt ℝ 2 (potential e) x ∧
    gradient (potential e) x =
      (potentialCoefficient n / (‖x - e‖ ^ 2) ^ ((n : ℝ) / 2)) • (x - e) ∧
    Laplacian.laplacian (potential e) x = 0 := by
  let S : ℝ := ‖x - e‖ ^ 2
  have hS : 0 < S := sq_pos_of_pos (norm_pos_iff.mpr (sub_ne_zero.mpr hx))
  have hg : ContDiffAt ℝ 2 (potentialProfile n) S := by
    by_cases hn2 : n = 2
    · rw [show potentialProfile n = (fun s : ℝ => (1 / 2 : ℝ) * Real.log s) by
        funext s; simp [potentialProfile, hn2]]
      exact contDiffAt_const.mul (Real.contDiffAt_log.mpr hS.ne')
    · rw [show potentialProfile n = (fun s : ℝ => s ^ (1 - (n : ℝ) / 2)) by
        funext s; simp [potentialProfile, hn2]]
      exact Real.contDiffAt_rpow_const_of_ne hS.ne'
  have hc : ContDiffAt ℝ 2 (potential e) x := by
    exact hg.comp x (((contDiffAt_id : ContDiffAt ℝ 2
      (fun y : EuclideanSpace ℝ (Fin n) => y) x).sub contDiffAt_const).norm_sq ℝ)
  have hd := TechnicalLemmas.Analysis.Calculus.RadialCalculus.radial_gradient_laplacian
    (potentialProfile n) e x hg
  by_cases hn2 : n = 2
  · subst n
    have hp : potentialProfile 2 = (fun s : ℝ => (1 / 2 : ℝ) * Real.log s) := by
      funext s
      simp [potentialProfile]
    have hf : potential e = (fun y => (1 / 2 : ℝ) * Real.log (‖y - e‖ ^ 2)) := rfl
    rw [hp] at hd
    simp only [deriv_const_mul_field', Real.deriv_log', deriv_const_mul_field,
      deriv_inv, finrank_euclideanSpace_fin] at hd
    refine ⟨hc, ?_, ?_⟩
    · rw [hf, hd.1]
      apply congrArg (fun c : ℝ => c • (x - e))
      norm_num [potentialCoefficient]
      ring
    · rw [hf, hd.2]
      change 4 * S * ((1 / 2 : ℝ) * -(S ^ 2)⁻¹) +
        2 * 2 * ((1 / 2 : ℝ) * S⁻¹) = 0
      field_simp
      ring
  · let p : ℝ := 1 - (n : ℝ) / 2
    have hp : potentialProfile n = (fun s : ℝ => s ^ p) := by
      funext s
      simp [potentialProfile, hn2, p]
    have hf : potential e = (fun y => (‖y - e‖ ^ 2) ^ p) := by
      funext y
      simp [potential, potentialProfile, hn2, p]
    rw [hp] at hd
    simp only [Real.deriv_rpow_const', deriv_const_mul_field,
      Real.deriv_rpow_const, finrank_euclideanSpace_fin] at hd
    have he : S ^ (p - 1 - 1) * S = S ^ (p - 1) := by
      rw [← Real.rpow_add_one hS.ne']
      congr 1
      ring
    refine ⟨hc, ?_, ?_⟩
    · rw [hf, hd.1]
      apply congrArg (fun c : ℝ => c • (x - e))
      change 2 * (p * S ^ (p - 1)) = potentialCoefficient n / S ^ ((n : ℝ) / 2)
      rw [show p - 1 = -((n : ℝ) / 2) by dsimp [p]; ring, Real.rpow_neg hS.le]
      simp only [potentialCoefficient, if_neg hn2, div_eq_mul_inv]
      dsimp [p]
      ring
    · rw [hf, hd.2]
      change 4 * S * (p * ((p - 1) * S ^ (p - 1 - 1))) +
        2 * (n : ℝ) * (p * S ^ (p - 1)) = 0
      calc
        _ = (2 * p * (2 * p + (n : ℝ) - 2)) * S ^ (p - 1) := by
          calc
            _ = 4 * p * (p - 1) * (S ^ (p - 1 - 1) * S) +
              2 * (n : ℝ) * p * S ^ (p - 1) := by ring
            _ = _ := by rw [he]; ring
        _ = 0 := by dsimp [p]; ring

private theorem potential_harmonic {n : ℕ} (hn : 2 ≤ n)
    (e : EuclideanSpace ℝ (Fin n)) :
    InnerProductSpace.HarmonicOnNhd (potential e) ({e}ᶜ : Set (EuclideanSpace ℝ (Fin n))) := by
  intro x hx
  have hxe : x ≠ e := by simpa using hx
  refine ⟨(potential_data hn e x hxe).1, ?_⟩
  filter_upwards [isOpen_compl_singleton.mem_nhds hx] with y hy
  exact (potential_data hn e y (by simpa using hy)).2.2

private theorem potentialCoefficient_ne_zero (n : ℕ) : potentialCoefficient n ≠ 0 := by
  by_cases h : n = 2
  · simp [potentialCoefficient, h]
  · have hcast : (2 : ℝ) ≠ (n : ℝ) := by exact_mod_cast Ne.symm h
    simpa [potentialCoefficient, h] using sub_ne_zero.mpr hcast
 
private theorem subtype_moments {n : ℕ} (hn : 2 ≤ n)
    (j : Fin n) (r : ℝ) (hr : 0 < r) (hr1 : r < 1) :
    let S := sphere (0 : EuclideanSpace ℝ (Fin n)) 1
    let τ : Measure S := (volume : Measure (EuclideanSpace ℝ (Fin n))).toSphere
    let μ : Measure S := (τ univ)⁻¹ • τ
    let K : S → ℝ := fun ζ => (1 + r ^ 2 - 2 * r * WithLp.ofLp ζ.1 j) ^ ((n : ℝ) / 2)
    Integrable (fun ζ : S => 1 / K ζ) μ ∧
    Integrable (fun ζ : S => WithLp.ofLp ζ.1 j / K ζ) μ ∧
    (∫ ζ : S, 1 / K ζ ∂μ) = 1 / (1 - r ^ 2) ∧
    (∫ ζ : S, WithLp.ofLp ζ.1 j / K ζ ∂μ) = r / (1 - r ^ 2) := by
  classical
  let : NeZero n := ⟨by omega⟩
  let E := EuclideanSpace ℝ (Fin n)
  let S := sphere (0 : E) 1
  let τ : Measure S := (volume : Measure E).toSphere
  let : NeZero τ := ⟨Measure.toSphere_ne_zero volume⟩
  let μ : Measure S := (τ univ)⁻¹ • τ
  let : IsProbabilityMeasure μ := inferInstance
  let e : E := EuclideanSpace.single j 1
  let D : S → ℝ := fun ζ => 1 + r ^ 2 - 2 * r * WithLp.ofLp ζ.1 j
  let K : S → ℝ := fun ζ => D ζ ^ ((n : ℝ) / 2)
  let g0 : S → ℝ := fun ζ => 1 / K ζ
  let g1 : S → ℝ := fun ζ => WithLp.ofLp ζ.1 j / K ζ
  change Integrable g0 μ ∧ Integrable g1 μ ∧
    (∫ ζ, g0 ζ ∂μ) = 1 / (1 - r ^ 2) ∧
    (∫ ζ, g1 ζ ∂μ) = r / (1 - r ^ 2)
  have he : ‖e‖ = 1 := by
    simpa only [norm_one] using (PiLp.norm_single 2 (fun _ : Fin n => ℝ) j (1 : ℝ))
  have hnorm (ζ : S) : ‖r • ζ.1‖ = r := by
    rw [norm_smul, mem_sphere_zero_iff_norm.mp ζ.property, Real.norm_eq_abs,
      abs_of_pos hr, mul_one]
  have hne (ζ : S) : r • ζ.1 ≠ e := by
    apply pole_excluded j hr1
    exact mem_closedBall_zero_iff.mpr (by rw [hnorm])
  have hD (ζ : S) : 0 < D ζ := by
    rw [show D ζ = ‖r • ζ.1 - e‖ ^ 2 by exact (sphere_geometry j r ζ).2.1.symm]
    exact sq_pos_of_pos (norm_pos_iff.mpr (sub_ne_zero.mpr (hne ζ)))
  have hu : Continuous (fun ζ : S => WithLp.ofLp ζ.1 j) :=
    (PiLp.proj (p := 2) (𝕜 := ℝ) (fun _ : Fin n => ℝ) j).continuous.comp
      continuous_subtype_val
  have hDc : Continuous D := continuous_const.sub (continuous_const.mul hu)
  have hKc : Continuous K := hDc.rpow_const (fun ζ => Or.inl (hD ζ).ne')
  have hKne (ζ : S) : K ζ ≠ 0 := (Real.rpow_pos_of_pos (hD ζ) _).ne'
  have hg0 : Continuous g0 := continuous_const.div hKc hKne
  have hg1 : Continuous g1 := hu.div hKc hKne
  have h0 : Integrable g0 μ := hg0.integrable_of_hasCompactSupport
    (HasCompactSupport.of_compactSpace _)
  have h1 : Integrable g1 μ := hg1.integrable_of_hasCompactSupport
    (HasCompactSupport.of_compactSpace _)
  have hden (ζ : S) : ‖r • ζ.1 - e‖ ^ n = K ζ := by
    change ‖r • ζ.1 - e‖ ^ n = D ζ ^ ((n : ℝ) / 2)
    rw [show D ζ = ‖r • ζ.1 - e‖ ^ 2 by exact (sphere_geometry j r ζ).2.1.symm]
    rw [← Real.rpow_natCast, ← Real.rpow_natCast,
      ← Real.rpow_mul (norm_nonneg _)]
    congr 1
    ring
  let P : E → ℝ := fun x => (1 - ‖x‖ ^ 2) / ‖x - e‖ ^ n
  have hP : InnerProductSpace.HarmonicOnNhd P (closedBall 0 r) :=
    (TechnicalLemmas.Analysis.Harmonic.PoissonKernel.poissonKernel_harmonicOnNhd
      hn e he).mono (fun x hx => by exact pole_excluded j hr1 hx)
  have hm := TechnicalLemmas.Analysis.Harmonic.SphericalMeanValue.harmonic_closedBall_mean_value
    hn P 0 r hr ⟨P, hP, fun _ _ => rfl⟩
  have hm' : (∫ ζ : S, P (r • ζ.1) ∂μ) = 1 := by
    change (∫ ζ : S, P (0 + r • ζ.1) ∂μ) = P 0 at hm
    have hP0 : P 0 = 1 := by simp [P, he]
    simpa only [zero_add, hP0] using hm
  have hscale : (1 - r ^ 2) * (∫ ζ : S, g0 ζ ∂μ) = 1 := by
    calc
      _ = ∫ ζ : S, (1 - r ^ 2) * g0 ζ ∂μ := (integral_const_mul _ _).symm
      _ = ∫ ζ : S, P (r • ζ.1) ∂μ := integral_congr_ae (Filter.Eventually.of_forall (fun ζ => by
        dsimp [P, g0]
        rw [hnorm, hden]
        ring))
      _ = 1 := hm'
  have hd : 0 < 1 - r ^ 2 := by nlinarith
  have hI0 : (∫ ζ : S, g0 ζ ∂μ) = 1 / (1 - r ^ 2) := by
    apply (eq_div_iff hd.ne').2
    nlinarith [hscale]
  let R : ℝ := (1 + r) / 2
  have hrR : r < R := by dsimp [R]; linarith
  have hR1 : R < 1 := by dsimp [R]; linarith
  have hR : 0 < R := lt_trans hr hrR
  have hF : InnerProductSpace.HarmonicOnNhd (potential e) (closedBall 0 R) :=
    (potential_harmonic hn e).mono (fun x hx => by exact pole_excluded j hR1 hx)
  obtain ⟨v, _, hvu, hf⟩ :=
    TechnicalLemmas.Analysis.Harmonic.SphericalFlux.harmonic_closedBall_zero_flux
      hn (potential e) 0 R hR ⟨potential e, hF, fun _ _ => rfl⟩
  have hgrad (ζ : S) : gradient v (r • ζ.1) = gradient (potential e) (r • ζ.1) := by
    have hm : r • ζ.1 ∈ ball (0 : E) R := mem_ball_zero_iff.mpr (by rw [hnorm]; exact hrR)
    have heq : v =ᶠ[𝓝 (r • ζ.1)] potential e := by
      filter_upwards [isOpen_ball.mem_nhds hm] with y hy
      exact hvu (ball_subset_closedBall hy)
    exact heq.gradient_eq
  have hτflux : (∫ ζ : S, inner ℝ (gradient (potential e) (r • ζ.1)) ζ.1 ∂τ) = 0 := by
    calc
      _ = ∫ ζ : S, inner ℝ (gradient v (0 + r • ζ.1)) ζ.1 ∂τ :=
        integral_congr_ae (Filter.Eventually.of_forall (fun ζ => by
          simpa only [zero_add] using
            congrArg (fun w : E => inner ℝ w ζ.1) (hgrad ζ).symm))
      _ = 0 := (hf r hr hrR.le).2
  have hμflux : (∫ ζ : S, inner ℝ (gradient (potential e) (r • ζ.1)) ζ.1 ∂μ) = 0 := by
    dsimp only [μ]
    rw [integral_smul_measure, hτflux, smul_zero]
  have hpair (ζ : S) :
      inner ℝ (gradient (potential e) (r • ζ.1)) ζ.1 =
        potentialCoefficient n * (r * g0 ζ - g1 ζ) := by
    rw [(potential_data hn e (r • ζ.1) (hne ζ)).2.1, real_inner_smul_left]
    rw [(sphere_geometry j r ζ).2.2, (sphere_geometry j r ζ).2.1]
    dsimp [g0, g1, K, D]
    ring
  have hz : potentialCoefficient n *
      (r * (∫ ζ : S, g0 ζ ∂μ) - (∫ ζ : S, g1 ζ ∂μ)) = 0 := by
    calc
      _ = ∫ ζ : S, potentialCoefficient n * (r * g0 ζ - g1 ζ) ∂μ := by
        rw [integral_const_mul, integral_sub (h0.const_mul r) h1, integral_const_mul]
      _ = ∫ ζ : S, inner ℝ (gradient (potential e) (r • ζ.1)) ζ.1 ∂μ :=
        integral_congr_ae (Filter.Eventually.of_forall (fun ζ => (hpair ζ).symm))
      _ = 0 := hμflux
  have hI1 : (∫ ζ : S, g1 ζ ∂μ) = r * (∫ ζ : S, g0 ζ ∂μ) :=
    (sub_eq_zero.mp ((mul_eq_zero.mp hz).resolve_left (potentialCoefficient_ne_zero n))).symm
  refine ⟨h0, h1, hI0, ?_⟩
  rw [hI1, hI0]
  ring

/-- Both actual normalized spherical Poisson values, with their L1 facts.
The n=2 case is an explicit ASTIS extension relative to the paper trailing
n>=3 clause; source consumers retain n>=3. -/
theorem spherical_poisson_moments {n : ℕ} (hn : 2 ≤ n)
    (r : ℝ) (hr : 0 < r) (hr1 : r < 1) :
    let j0 : Fin n := ⟨0, lt_of_lt_of_le (by decide : 0 < 2) hn⟩
    let τ : Measure (Metric.sphere (0 : EuclideanSpace ℝ (Fin n)) 1) :=
      (volume : Measure (EuclideanSpace ℝ (Fin n))).toSphere
    let σ : Measure (EuclideanSpace ℝ (Fin n)) :=
      (τ Set.univ)⁻¹ • τ.map (fun y => y.val)
    let K : EuclideanSpace ℝ (Fin n) → ℝ := fun y =>
      (1 + r ^ 2 - 2 * r * WithLp.ofLp y j0) ^ ((n : ℝ) / 2)
    Integrable (fun y : EuclideanSpace ℝ (Fin n) => 1 / K y) σ ∧
    Integrable (fun y : EuclideanSpace ℝ (Fin n) => WithLp.ofLp y j0 / K y) σ ∧
    (∫ y : EuclideanSpace ℝ (Fin n), 1 / K y ∂σ) = 1 / (1 - r ^ 2) ∧
    (∫ y : EuclideanSpace ℝ (Fin n), WithLp.ofLp y j0 / K y ∂σ) = r / (1 - r ^ 2) := by
  let E := EuclideanSpace ℝ (Fin n)
  let j0 : Fin n := ⟨0, lt_of_lt_of_le (by decide : 0 < 2) hn⟩
  let S := sphere (0 : E) 1
  let τ : Measure S := (volume : Measure E).toSphere
  let μ : Measure S := (τ univ)⁻¹ • τ
  let σ : Measure E := (τ univ)⁻¹ • τ.map (fun y => y.val)
  let K : E → ℝ := fun y =>
    (1 + r ^ 2 - 2 * r * WithLp.ofLp y j0) ^ ((n : ℝ) / 2)
  change Integrable (fun y : E => 1 / K y) σ ∧
    Integrable (fun y : E => WithLp.ofLp y j0 / K y) σ ∧
    (∫ y : E, 1 / K y ∂σ) = 1 / (1 - r ^ 2) ∧
    (∫ y : E, WithLp.ofLp y j0 / K y ∂σ) = r / (1 - r ^ 2)
  have hm := subtype_moments hn j0 r hr hr1
  have hσ : σ = μ.map (Subtype.val : S → E) := by
    dsimp only [σ, μ]
    rw [Measure.map_smul]
  have hemb : MeasurableEmbedding (Subtype.val : S → E) :=
    MeasurableEmbedding.subtype_coe isClosed_sphere.measurableSet
  rw [hσ]
  refine ⟨hemb.integrable_map_iff.2 hm.1, hemb.integrable_map_iff.2 hm.2.1, ?_, ?_⟩
  · rw [hemb.integral_map]
    exact hm.2.2.1
  · rw [hemb.integral_map]
    exact hm.2.2.2

end
end AutoSamplingTheory.ExampleCases.GaussianComplexity.SphericalPoisson
