import Mathlib.Geometry.Manifold.Instances.Sphere
import Mathlib.Geometry.Manifold.Riemannian.PathELength
import Mathlib.Analysis.SpecialFunctions.Trigonometric.InverseDeriv
import Mathlib.Analysis.Calculus.ContDiff.Deriv
import Mathlib.Analysis.InnerProductSpace.Calculus
import Mathlib.MeasureTheory.Integral.IntervalIntegral.FundThmCalculus
import Mathlib.Tactic

/-!
# Induced path distance on the round unit sphere

The length infimum built from the differential of the literal sphere inclusion
equals the central angle in positive sphere dimension. The local tangent norm
does not replace the inherited chord metric. Three private implementation lemmas
support the single public distance identity.
-/

open Set MeasureTheory Filter Manifold Metric
open scoped Manifold InnerProductSpace ENNReal Topology Interval

noncomputable section

namespace AutoSamplingTheory.TechnicalLemmas.Geometry.UnitSphereInducedPathDistance

private theorem angle_le_ambient_path_integral
    {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    (x : E) (γ : ℝ → E) (hx : ‖x‖ = 1) (hstart : γ 0 = x)
    (hunit : ∀ t ∈ Icc (0 : ℝ) 1, ‖γ t‖ = 1)
    (hγ : ContDiffOn ℝ 1 γ (Icc (0 : ℝ) 1)) :
    Real.arccos ⟪x, γ 1⟫_ℝ ≤ ∫ t in (0 : ℝ)..1, ‖derivWithin γ (Icc (0 : ℝ) 1) t‖ := by
  let I := Icc (0 : ℝ) 1
  let v : ℝ → E := derivWithin γ I
  let c : ℝ → ℝ := fun t => ⟪x, γ t⟫_ℝ
  let cp : ℝ → ℝ := fun t => ⟪x, v t⟫_ℝ
  have hvc : ContinuousOn v I := hγ.continuousOn_derivWithin (uniqueDiffOn_Icc zero_lt_one) le_rfl
  have hc : ContinuousOn c I := continuousOn_const.inner hγ.continuousOn
  have hcp : ContinuousOn cp I := continuousOn_const.inner hvc
  have habs (t : ℝ) (ht : t ∈ I) : |c t| ≤ 1 := by
    simpa [c, hx, hunit t ht] using abs_real_inner_le_norm x (γ t)
  have hder (t : ℝ) (ht : t ∈ Ioo (0 : ℝ) 1) : HasDerivAt γ (v t) t := by
    have hn : I ∈ 𝓝 t := Icc_mem_nhds ht.1 ht.2
    exact ((hγ.differentiableOn one_ne_zero t (Ioo_subset_Icc_self ht)).hasDerivWithinAt).hasDerivAt hn
  have horth (t : ℝ) (ht : t ∈ Ioo (0 : ℝ) 1) : ⟪γ t, v t⟫_ℝ = 0 := by
    have heq : (fun _ : ℝ => (1 : ℝ)) =ᶠ[𝓝 t] (fun s => ‖γ s‖ ^ 2) := by
      filter_upwards [Icc_mem_nhds ht.1 ht.2] with u hu
      simp only [hunit u hu, one_pow]
    have hh := ((hder t ht).norm_sq.congr_of_eventuallyEq heq).unique (hasDerivAt_const t (1 : ℝ))
    linarith
  have hcp_bound (t : ℝ) (ht : t ∈ Ioo (0 : ℝ) 1) :
      |cp t| ≤ Real.sqrt (1 - (c t)^2) * ‖v t‖ := by
    have hu := hunit t (Ioo_subset_Icc_self ht)
    have hnorm : ‖x - c t • γ t‖ ^ 2 = 1 - (c t)^2 := by
      rw [norm_sub_sq_real, hx, norm_smul, hu, mul_one, Real.norm_eq_abs, sq_abs,
        inner_smul_right, ← show c t = ⟪x, γ t⟫_ℝ from rfl]
      ring
    have hpair : ⟪x - c t • γ t, v t⟫_ℝ = cp t := by
      simp only [inner_sub_left, real_inner_smul_left, horth t ht, mul_zero, sub_zero, cp]
    have hr : Real.sqrt (1 - (c t)^2) = ‖x - c t • γ t‖ := by
      rw [← hnorm, Real.sqrt_sq (norm_nonneg _)]
    rw [hr, ← hpair]
    exact abs_real_inner_le_norm _ _
  let L := ∫ t in (0 : ℝ)..1, ‖v t‖
  let F : ℝ → ℝ := fun a => Real.arccos (a*c 1) - Real.arccos (a*c 0)
  have hF : Continuous F := by unfold F; fun_prop
  have hFle (a : ℝ) (ha : a ∈ Ioo (0 : ℝ) 1) : F a ≤ L := by
    have ha0 : 0 < a := ha.1
    have ha1 : a < 1 := ha.2
    have hsq (t : ℝ) (ht : t ∈ I) : 0 < 1 - (a*c t)^2 := by
      have h : |a*c t| < 1 := by
        rw [abs_mul, abs_of_pos ha0]
        calc a * |c t| ≤ a * 1 := mul_le_mul_of_nonneg_left (habs t ht) ha0.le
          _ < 1 := by simpa using ha1
      rw [← sq_abs (a*c t)]
      nlinarith [mul_pos (show 0 < 1 - |a*c t| by linarith)
        (show 0 < 1 + |a*c t| by positivity)]
    let D : ℝ → ℝ := fun t => -(a*cp t) / Real.sqrt (1-(a*c t)^2)
    have hD : ContinuousOn D I := by
      refine ((continuousOn_const.mul hcp).neg).div ?_ (fun t ht => ne_of_gt (Real.sqrt_pos.2 (hsq t ht)))
      exact Real.continuous_sqrt.continuousOn.comp
        (continuousOn_const.sub ((continuousOn_const.mul hc).pow 2)) (mapsTo_univ _ _)
    have hDi : IntervalIntegrable D volume 0 1 :=
      (show ContinuousOn D (uIcc (0 : ℝ) 1) by simpa [I, uIcc_of_le zero_le_one] using hD).intervalIntegrable
    have hvi : IntervalIntegrable (fun t => ‖v t‖) volume 0 1 :=
      (show ContinuousOn (fun t => ‖v t‖) (uIcc (0 : ℝ) 1) by
        simpa [I, uIcc_of_le zero_le_one] using hvc.norm).intervalIntegrable
    have hFder (t : ℝ) (ht : t ∈ Ioo (0 : ℝ) 1) :
        HasDerivAt (fun s => Real.arccos (a*c s)) (D t) t := by
      have hc' : HasDerivAt c (cp t) t := by
        simpa only [c, cp, inner_zero_left, add_zero] using
          HasDerivAt.inner ℝ (hasDerivAt_const t x) (hder t ht)
      have hs := hsq t (Ioo_subset_Icc_self ht)
      have hm : a*c t ≠ -1 := by intro h; rw [h] at hs; norm_num at hs
      have hp : a*c t ≠ 1 := by intro h; rw [h] at hs; norm_num at hs
      convert (Real.hasDerivAt_arccos hm hp).scomp t (hc'.const_mul a) using 1 <;>
        (try rfl) <;> (simp only [D, div_eq_mul_inv]; ring)
    have hpoint (t : ℝ) (ht : t ∈ Ioo (0 : ℝ) 1) : D t ≤ ‖v t‖ := by
      have htI := Ioo_subset_Icc_self ht
      have hs := hsq t htI
      have hcs : 0 ≤ 1 - (c t)^2 := by
        rw [← sq_abs (c t)]
        nlinarith [mul_nonneg (sub_nonneg.mpr (habs t htI))
          (show 0 ≤ 1+|c t| by positivity)]
      have hA : a^2 ≤ 1 := by
        simpa only [pow_two, one_mul] using mul_le_mul ha1.le ha1.le ha0.le zero_le_one
      have hrs : a * Real.sqrt (1 - (c t)^2) ≤ Real.sqrt (1-(a*c t)^2) := by
        apply (sq_le_sq₀ (by positivity) (Real.sqrt_nonneg _)).mp
        rw [mul_pow, Real.sq_sqrt hcs, Real.sq_sqrt hs.le, mul_pow]
        linarith
      have hb : a * |cp t| ≤ Real.sqrt (1-(a*c t)^2) * ‖v t‖ := by
        calc
          a * |cp t| ≤ a * (Real.sqrt (1-(c t)^2) * ‖v t‖) :=
            mul_le_mul_of_nonneg_left (hcp_bound t ht) ha0.le
          _ = (a * Real.sqrt (1-(c t)^2)) * ‖v t‖ := (mul_assoc _ _ _).symm
          _ ≤ _ := mul_le_mul_of_nonneg_right hrs (norm_nonneg _)
      apply (div_le_iff₀ (Real.sqrt_pos.2 hs)).2
      calc
        -(a*cp t) ≤ a*|cp t| := by
          rw [← mul_neg]
          exact mul_le_mul_of_nonneg_left (neg_le_abs _) ha0.le
        _ ≤ Real.sqrt (1-(a*c t)^2) * ‖v t‖ := hb
        _ = ‖v t‖ * Real.sqrt (1-(a*c t)^2) := mul_comm _ _
    have hFTC := intervalIntegral.integral_eq_sub_of_hasDerivAt_of_le zero_le_one
      (Real.continuous_arccos.comp_continuousOn (continuousOn_const.mul hc)) hFder hDi
    have hmono := intervalIntegral.integral_mono_on_of_le_Ioo zero_le_one hDi hvi hpoint
    rw [hFTC] at hmono
    exact hmono
  have hclosed : IsClosed {a : ℝ | F a ≤ L} := isClosed_le hF continuous_const
  have hcl := closure_minimal (show Ioo (0 : ℝ) 1 ⊆ {a | F a ≤ L} from hFle) hclosed
  have hone : (1 : ℝ) ∈ closure (Ioo (0 : ℝ) 1) := by
    rw [closure_Ioo zero_ne_one]
    exact ⟨zero_le_one, le_rfl⟩
  have hh : F 1 ≤ L := hcl hone
  simpa [F, L, c, hstart, real_inner_self_eq_norm_sq, hx] using hh

private theorem unit_circle_frame
    {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [FiniteDimensional ℝ E] (n : ℕ) [Fact (Module.finrank ℝ E = n + 1)]
    (hn : 0 < n) (x y : sphere (0 : E) 1) :
    let θ := Real.arccos ⟪(x : E), (y : E)⟫_ℝ
    ∃ u : E, ‖u‖ = 1 ∧ ⟪(x : E),u⟫_ℝ = 0 ∧
      Real.cos θ • (x : E) + Real.sin θ • u = (y : E) := by
  let c := ⟪(x : E), (y : E)⟫_ℝ
  let θ := Real.arccos c
  change ∃ u : E, ‖u‖ = 1 ∧ ⟪(x : E),u⟫_ℝ = 0 ∧
    Real.cos θ • (x : E) + Real.sin θ • u = (y : E)
  have hx : ‖(x : E)‖ = 1 := by simpa only [Metric.mem_sphere, dist_zero_right] using x.property
  have hy : ‖(y : E)‖ = 1 := by simpa only [Metric.mem_sphere, dist_zero_right] using y.property
  have hc : |c| ≤ 1 := by simpa [c,hx,hy] using abs_real_inner_le_norm (x : E) (y : E)
  have hcos : Real.cos θ = c := Real.cos_arccos (abs_le.mp hc).1 (abs_le.mp hc).2
  let r : E := (y : E) - c • (x : E)
  have horth : ⟪(x : E),r⟫_ℝ = 0 := by
    simp [r, c, inner_sub_right, inner_smul_right, real_inner_self_eq_norm_sq, hx]
  have hrsq : ‖r‖^2 = 1-c^2 := by
    dsimp only [r]
    rw [norm_sub_sq_real, hy, norm_smul, hx, mul_one, Real.norm_eq_abs, sq_abs,
      inner_smul_right, real_inner_comm (x : E) (y : E)]
    change 1^2 - 2 * (c * c) + c^2 = 1-c^2
    ring
  have hsin : Real.sin θ = ‖r‖ := by
    rw [show θ = Real.arccos c from rfl, Real.sin_arccos, ← hrsq, Real.sqrt_sq (norm_nonneg _)]
  have hsum : c • (x : E) + r = (y : E) := by dsimp [r]; abel
  rw [hcos, hsin]
  by_cases hr : r = 0
  · let B := OrthonormalBasis.fromOrthogonalSpanSingleton (𝕜 := ℝ) n
      (ne_zero_of_mem_unit_sphere x)
    let i : Fin n := ⟨0,hn⟩
    refine ⟨(B i : E), ?_, ?_, ?_⟩
    · exact B.orthonormal.norm_eq_one i
    · exact Submodule.mem_orthogonal_singleton_iff_inner_right.mp (B i).property
    · simpa [hr] using hsum
  · have hrnorm : ‖r‖ ≠ 0 := norm_ne_zero_iff.mpr hr
    refine ⟨‖r‖⁻¹ • r, ?_, ?_, ?_⟩
    · rw [norm_smul, Real.norm_eq_abs, abs_inv, abs_of_nonneg (norm_nonneg _),
        inv_mul_cancel₀ hrnorm]
    · rw [inner_smul_right, horth, mul_zero]
    · rw [smul_smul, mul_inv_cancel₀ hrnorm, one_smul]
      exact hsum

private theorem derivative_of_ambient_sphere_curve
    {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [FiniteDimensional ℝ E] (n : ℕ) [Fact (Module.finrank ℝ E = n + 1)]
    (γ : ℝ → sphere (0 : E) 1) (t : ℝ)
    (hγ : MDifferentiableAt 𝓘(ℝ, ℝ) (𝓡 n) γ t) :
    mvfderiv (𝓡 n) ((↑) : sphere (0 : E) 1 → E) (γ t)
        (mfderiv 𝓘(ℝ, ℝ) (𝓡 n) γ t 1) = deriv (fun t => (γ t : E)) t := by
  let inc : sphere (0 : E) 1 → E := Subtype.val
  have hcoe : MDifferentiableAt (𝓡 n) 𝓘(ℝ, E) inc (γ t) :=
    (contMDiff_coe_sphere (n := n) (m := 1) (γ t)).mdifferentiableAt one_ne_zero
  change mvfderiv (𝓡 n) inc (γ t) (mfderiv 𝓘(ℝ, ℝ) (𝓡 n) γ t 1) = deriv (inc ∘ γ) t
  calc
    _ = mvfderiv 𝓘(ℝ, ℝ) (inc ∘ γ) t 1 := by
      simp only [mvfderiv, mfderiv_comp t hcoe hγ, ContinuousLinearMap.comp_apply]
      rfl
    _ = _ := by
      simp only [mvfderiv, mfderiv_eq_fderiv, ContinuousLinearMap.comp_apply,
        fderiv_apply_one_eq_deriv]
      rfl

theorem unit_sphere_induced_riemannianEDist_eq_arccos
    {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [FiniteDimensional ℝ E] (n : ℕ) [Fact (Module.finrank ℝ E = n + 1)]
    (hn : 0 < n) (x y : Metric.sphere (0 : E) 1) :
  letI : ∀ z : Metric.sphere (0 : E) 1, ENorm (TangentSpace (𝓡 n) z) :=
    fun z => ⟨fun v =>
      ‖mvfderiv (𝓡 n) ((↑) : Metric.sphere (0 : E) 1 → E) z v‖ₑ⟩
  Manifold.riemannianEDist (𝓡 n) x y =
    ENNReal.ofReal (Real.arccos ⟪(x : E), (y : E)⟫_ℝ) := by
  classical
  let S := sphere (0 : E) 1
  let inc : S → E := Subtype.val
  let EN : ∀ z : S, ENorm (TangentSpace (𝓡 n) z) := fun z =>
    ⟨fun v => ‖mvfderiv (𝓡 n) inc z v‖ₑ⟩
  letI := EN
  change riemannianEDist (𝓡 n) x y = ENNReal.ofReal (Real.arccos ⟪(x : E),(y : E)⟫_ℝ)
  letI : ∀ z : S, ENormSMulClass ℝ (TangentSpace (𝓡 n) z) := fun z =>
    ⟨fun r v => by
      change ‖mvfderiv (𝓡 n) inc z (r • v)‖ₑ = ‖r‖ₑ * ‖mvfderiv (𝓡 n) inc z v‖ₑ
      rw [map_smul,enorm_smul]⟩
  apply le_antisymm
  · let θ := Real.arccos ⟪(x : E),(y : E)⟫_ℝ
    obtain ⟨u,hu,horth,hy⟩ := unit_circle_frame n hn x y
    have hx : ‖(x : E)‖ = 1 := by simpa only [Metric.mem_sphere, dist_zero_right] using x.property
    have hnorm (a b : ℝ) : ‖a • (x : E) + b • u‖ ^ 2 = a^2 + b^2 := by
      rw [norm_add_sq_real, norm_smul, norm_smul, hx, hu, mul_one, mul_one,
        Real.norm_eq_abs, Real.norm_eq_abs, sq_abs, sq_abs,
        real_inner_smul_left, inner_smul_right, horth]
      ring
    let f : ℝ → E := fun t => Real.cos t • (x : E) + Real.sin t • u
    have hfunit (t : ℝ) : f t ∈ S := by
      change f t ∈ Metric.sphere (0 : E) 1
      rw [Metric.mem_sphere, dist_zero_right]
      have hsq : ‖f t‖^2 = 1 := by
        rw [show f t = Real.cos t • (x : E) + Real.sin t • u from rfl, hnorm]
        linarith [Real.sin_sq_add_cos_sq t]
      nlinarith [norm_nonneg (f t)]
    let γ : ℝ → S := Set.codRestrict f S hfunit
    have hf : ContDiff ℝ 1 f := by unfold f; fun_prop
    have hγ : ContMDiff 𝓘(ℝ, ℝ) (𝓡 n) 1 γ := hf.contMDiff.codRestrict_sphere hfunit
    have h0 : γ 0 = x := by apply Subtype.ext; simp [γ, f]
    have h1 : γ θ = y := by apply Subtype.ext; exact hy
    have hθ : 0 ≤ θ := Real.arccos_nonneg _
    have hspeed (t : ℝ) : ‖mfderiv 𝓘(ℝ, ℝ) (𝓡 n) γ t 1‖ₑ = 1 := by
      change ‖mvfderiv (𝓡 n) inc (γ t) (mfderiv 𝓘(ℝ, ℝ) (𝓡 n) γ t 1)‖ₑ = 1
      rw [derivative_of_ambient_sphere_curve n γ t (hγ.mdifferentiableAt one_ne_zero)]
      change ‖deriv f t‖ₑ = 1
      have hd : HasDerivAt f ((-Real.sin t) • (x : E) + Real.cos t • u) t :=
        ((Real.hasDerivAt_cos t).smul_const (x : E)).add
          ((Real.hasDerivAt_sin t).smul_const u)
      have hs : ‖deriv f t‖ = 1 := by
        rw [hd.deriv]
        have hsq := hnorm (-Real.sin t) (Real.cos t)
        nlinarith [Real.sin_sq_add_cos_sq t, norm_nonneg ((-Real.sin t) • (x : E) + Real.cos t • u)]
      rw [← ofReal_norm, hs, ENNReal.ofReal_one]
    calc
      riemannianEDist (𝓡 n) x y ≤ pathELength (𝓡 n) γ 0 θ :=
        riemannianEDist_le_pathELength hγ.contMDiffOn h0 h1 hθ
      _ = ENNReal.ofReal θ := by
        rw [pathELength_eq_lintegral_mfderiv_Ioo]
        simp only [hspeed, lintegral_const, one_mul, Measure.restrict_apply_univ, Real.volume_Ioo, sub_zero]
  · by_contra! hlt
    obtain ⟨γ,h0,h1,hγ,hL⟩ := exists_lt_of_riemannianEDist_lt hlt
    let I := Icc (0 : ℝ) 1
    let f : ℝ → E := inc ∘ γ
    let v : ℝ → E := derivWithin f I
    have hfM : ContMDiffOn 𝓘(ℝ, ℝ) 𝓘(ℝ, E) 1 f I :=
      contMDiff_coe_sphere.comp_contMDiffOn hγ
    have hf : ContDiffOn ℝ 1 f I := contMDiffOn_iff_contDiffOn.mp hfM
    have hx : ‖(x : E)‖ = 1 := by simpa only [Metric.mem_sphere, dist_zero_right] using x.property
    have hstart : f 0 = (x : E) := congrArg inc h0
    have hunit (t : ℝ) (_ht : t ∈ I) : ‖f t‖ = 1 := by
      change ‖(γ t : E)‖ = 1
      simpa only [Metric.mem_sphere, dist_zero_right] using (γ t).property
    have hangle := angle_le_ambient_path_integral (x : E) f hx hstart hunit hf
    have hfinish : f 1 = (y : E) := congrArg inc h1
    rw [hfinish] at hangle
    have hv : ContinuousOn v I := hf.continuousOn_derivWithin (uniqueDiffOn_Icc zero_lt_one) le_rfl
    have hvi : IntervalIntegrable (fun t => ‖v t‖) volume 0 1 :=
      (show ContinuousOn (fun t => ‖v t‖) (uIcc (0 : ℝ) 1) by
        simpa [I, uIcc_of_le zero_le_one] using hv.norm).intervalIntegrable
    have he : pathELength (𝓡 n) γ 0 1 = ENNReal.ofReal (∫ t in (0 : ℝ)..1, ‖v t‖) := by
      rw [pathELength_eq_lintegral_mfderiv_Ioo, intervalIntegral.integral_of_le zero_le_one,
        ofReal_integral_eq_lintegral_ofReal hvi.1 (Eventually.of_forall (fun _ => norm_nonneg _)),
        ← restrict_Ioo_eq_restrict_Ioc]
      apply setLIntegral_congr_fun measurableSet_Ioo
      intro t ht
      have hnt := Icc_mem_nhds ht.1 ht.2
      have hγt := (hγ t (Ioo_subset_Icc_self ht)).mdifferentiableWithinAt one_ne_zero
      have hγa := hγt.mdifferentiableAt hnt
      change ‖mvfderiv (𝓡 n) inc (γ t) (mfderiv 𝓘(ℝ, ℝ) (𝓡 n) γ t 1)‖ₑ =
        ENNReal.ofReal ‖v t‖
      rw [derivative_of_ambient_sphere_curve n γ t hγa, ofReal_norm]
      rw [show v t = deriv f t from derivWithin_of_mem_nhds hnt]
      rfl
    have hle : ENNReal.ofReal (Real.arccos ⟪(x : E),(y : E)⟫_ℝ) ≤
        pathELength (𝓡 n) γ 0 1 := by
      rw [he]
      exact ENNReal.ofReal_le_ofReal hangle
    exact (not_lt_of_ge hle) hL

end AutoSamplingTheory.TechnicalLemmas.Geometry.UnitSphereInducedPathDistance
