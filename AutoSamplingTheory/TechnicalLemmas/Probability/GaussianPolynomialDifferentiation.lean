import Mathlib.Probability.Distributions.Gaussian.Multivariate
import Mathlib.MeasureTheory.Function.L2Space
import Mathlib.Probability.Distributions.Gaussian.Fernique
import Mathlib.Analysis.Calculus.MeanValue
import Mathlib.Analysis.Calculus.Deriv.Polynomial
import Mathlib.Tactic

open MeasureTheory ProbabilityTheory Filter
open scoped ENNReal InnerProductSpace Topology

namespace AutoSamplingTheory.TechnicalLemmas.Probability.GaussianPolynomialDifferentiation

private theorem polynomial_radial_envelope
    {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]
    (p : Polynomial ℝ) (R : ℝ) (hR : 0 ≤ R) (k : ℕ) :
    ∃ B : E → ℝ, MemLp B 2 (stdGaussian E) ∧ (∀ x, 0 ≤ B x) ∧
      ∀ (w : E), ‖w‖ ≤ R → ∀ x,
        ‖p.eval ⟪w,x⟫_ℝ‖ * ‖x‖^k ≤ B x := by
  classical
  letI : CompleteSpace E := FiniteDimensional.complete ℝ E
  letI : SecondCountableTopology E := inferInstance
  let μ := stdGaussian E
  have hpow (n : ℕ) : MemLp (fun x : E => ‖x‖^n) 2 μ := by
    apply (memLp_two_iff_integrable_sq (by fun_prop)).2
    have hi := (IsGaussian.memLp_id μ ((2*n : ℕ) : ℝ≥0∞)
      (ENNReal.natCast_ne_top (2*n))).integrable_norm_pow' (p := 2*n)
    convert hi using 1
    funext x
    simp only [id_eq, ← pow_mul, Nat.mul_comm n 2]
  induction p using Polynomial.induction_on' with
  | add p q hp hq =>
    obtain ⟨B,hB,hB0,hBp⟩ := hp
    obtain ⟨C,hC,hC0,hCq⟩ := hq
    refine ⟨B+C,hB.add hC,fun x => add_nonneg (hB0 x) (hC0 x),?_⟩
    intro w hw x
    calc
      ‖(p+q).eval ⟪w,x⟫_ℝ‖ * ‖x‖^k ≤
          (‖p.eval ⟪w,x⟫_ℝ‖+‖q.eval ⟪w,x⟫_ℝ‖) * ‖x‖^k := by
        rw [Polynomial.eval_add]
        exact mul_le_mul_of_nonneg_right (norm_add_le _ _) (pow_nonneg (norm_nonneg _) _)
      _ = ‖p.eval ⟪w,x⟫_ℝ‖ * ‖x‖^k + ‖q.eval ⟪w,x⟫_ℝ‖ * ‖x‖^k := by ring
      _ ≤ (B+C) x := add_le_add (hBp w hw x) (hCq w hw x)
  | monomial n a =>
    refine ⟨fun x => (‖a‖*R^n)*‖x‖^(n+k),
      (hpow (n+k)).const_mul (‖a‖*R^n),fun x => by positivity,?_⟩
    intro w hw x
    have hi : ‖⟪w,x⟫_ℝ‖ ≤ R*‖x‖ :=
      (norm_inner_le_norm (𝕜 := ℝ) w x).trans (mul_le_mul_of_nonneg_right hw (norm_nonneg _))
    simp only [Polynomial.eval_monomial,norm_mul,norm_pow]
    calc
      ‖a‖ * ‖⟪w,x⟫_ℝ‖^n * ‖x‖^k ≤ ‖a‖ * (R*‖x‖)^n * ‖x‖^k := by
        gcongr
      _ = (‖a‖*R^n)*‖x‖^(n+k) := by rw [pow_add,mul_pow];ring

private theorem ambient_feature_and_derivative_memLp
    {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]
    (p : Polynomial ℝ) :
    (∀ w : E, MemLp (fun x : E => p.eval ⟪w,x⟫_ℝ) 2 (stdGaussian E)) ∧
      ∀ w v : E, MemLp (fun x : E =>
        p.derivative.eval ⟪w,x⟫_ℝ * ⟪v,x⟫_ℝ) 2 (stdGaussian E) := by
  constructor
  · intro w
    obtain ⟨B,hB,hB0,hBound⟩ :=
      polynomial_radial_envelope (E := E) p ‖w‖ (norm_nonneg _) 0
    apply hB.mono' (by fun_prop)
    exact ae_of_all _ fun x => by simpa using hBound w le_rfl x
  · intro w v
    obtain ⟨B,hB,hB0,hBound⟩ :=
      polynomial_radial_envelope (E := E) p.derivative ‖w‖ (norm_nonneg _) 1
    apply (hB.const_mul ‖v‖).mono' (by fun_prop)
    apply ae_of_all _
    intro x
    calc
      ‖p.derivative.eval ⟪w,x⟫_ℝ * ⟪v,x⟫_ℝ‖ =
          ‖p.derivative.eval ⟪w,x⟫_ℝ‖ * ‖⟪v,x⟫_ℝ‖ := norm_mul _ _
      _ ≤ ‖p.derivative.eval ⟪w,x⟫_ℝ‖ * (‖v‖*‖x‖) :=
        mul_le_mul_of_nonneg_left (norm_inner_le_norm (𝕜 := ℝ) v x) (norm_nonneg _)
      _ = ‖v‖ * (‖p.derivative.eval ⟪w,x⟫_ℝ‖ * ‖x‖) := by ring
      _ ≤ ‖v‖ * B x := mul_le_mul_of_nonneg_left
        (by simpa using hBound w le_rfl x) (norm_nonneg _)

private theorem pointwise_ridge_hasFDerivAt
    {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    (p : Polynomial ℝ) (w x : E) :
    HasFDerivAt (fun u : E => p.eval ⟪u,x⟫_ℝ)
      (p.derivative.eval ⟪w,x⟫_ℝ • innerSL ℝ x) w := by
  have h := (p.hasDerivAt ⟪x,w⟫_ℝ).comp_hasFDerivAt w (innerSL ℝ x).hasFDerivAt
  simpa only [Function.comp_def,innerSL_apply_apply,real_inner_comm x] using h

private theorem local_increment_bounds
    {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]
    (p : Polynomial ℝ) (w : E) :
    ∃ B : E → ℝ, MemLp B 2 (stdGaussian E) ∧ (∀ x, 0 ≤ B x) ∧
      (∀ u : E, ‖u-w‖ ≤ 1 → ∀ x,
        ‖p.eval ⟪u,x⟫_ℝ - p.eval ⟪w,x⟫_ℝ‖ ≤ B x * ‖u-w‖) ∧
      ∀ (v x : E), ‖p.derivative.eval ⟪w,x⟫_ℝ * ⟪v,x⟫_ℝ‖ ≤ B x * ‖v‖ := by
  obtain ⟨B,hB,hB0,hBound⟩ := polynomial_radial_envelope
    (E := E) p.derivative (‖w‖+1) (by positivity) 1
  have hwNorm : ‖w‖ ≤ ‖w‖+1 := by linarith
  refine ⟨B,hB,hB0,?_,?_⟩
  · intro u hu x
    have huNorm : ‖u‖ ≤ ‖w‖+1 := by
      calc
        ‖u‖ = ‖(u-w)+w‖ := by rw [sub_add_cancel]
        _ ≤ ‖u-w‖+‖w‖ := norm_add_le _ _
        _ ≤ ‖w‖+1 := by linarith
    have hwMem : w ∈ Metric.closedBall (0 : E) (‖w‖+1) := by
      simpa [Metric.mem_closedBall,dist_zero_right] using hwNorm
    have huMem : u ∈ Metric.closedBall (0 : E) (‖w‖+1) := by
      simpa [Metric.mem_closedBall,dist_zero_right] using huNorm
    apply (convex_closedBall (0 : E) (‖w‖+1)).norm_image_sub_le_of_norm_hasFDerivWithin_le
      (fun z hz => (pointwise_ridge_hasFDerivAt p z x).hasFDerivWithinAt) ?_ hwMem huMem
    intro z hz
    rw [norm_smul,innerSL_apply_norm]
    have hzNorm : ‖z‖ ≤ ‖w‖+1 := by
      simpa [Metric.mem_closedBall,dist_zero_right] using hz
    simpa only [pow_one] using hBound z hzNorm x
  · intro v x
    calc
      ‖p.derivative.eval ⟪w,x⟫_ℝ * ⟪v,x⟫_ℝ‖ =
          ‖p.derivative.eval ⟪w,x⟫_ℝ‖ * ‖⟪v,x⟫_ℝ‖ := norm_mul _ _
      _ ≤ ‖p.derivative.eval ⟪w,x⟫_ℝ‖ * (‖v‖*‖x‖) :=
        mul_le_mul_of_nonneg_left (norm_inner_le_norm (𝕜 := ℝ) v x) (norm_nonneg _)
      _ = (‖p.derivative.eval ⟪w,x⟫_ℝ‖ * ‖x‖) * ‖v‖ := by ring
      _ ≤ B x * ‖v‖ := mul_le_mul_of_nonneg_right
        (by simpa only [pow_one] using hBound w hwNorm x) (norm_nonneg _)

private theorem represented_derivative_clm
    {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]
    (p : Polynomial ℝ)
    (hdf : ∀ w v : E, MemLp (fun x : E =>
      p.derivative.eval ⟪w,x⟫_ℝ * ⟪v,x⟫_ℝ) 2 (stdGaussian E)) :
    ∃ D : E → E →L[ℝ] Lp ℝ 2 (stdGaussian E),
      ∀ w v, D w v = (hdf w v).toLp
        (fun x : E => p.derivative.eval ⟪w,x⟫_ℝ * ⟪v,x⟫_ℝ) := by
  classical
  have hD (w : E) : ∃ D : E →L[ℝ] Lp ℝ 2 (stdGaussian E),
      ∀ v, D v = (hdf w v).toLp
        (fun x : E => p.derivative.eval ⟪w,x⟫_ℝ * ⟪v,x⟫_ℝ) := by
    let df := fun (v x : E) => p.derivative.eval ⟪w,x⟫_ℝ * ⟪v,x⟫_ℝ
    let L : E →ₗ[ℝ] Lp ℝ 2 (stdGaussian E) := {
      toFun := fun v => (hdf w v).toLp (df v)
      map_add' := by
        intro v u
        apply Lp.ext
        filter_upwards [(hdf w (v+u)).coeFn_toLp,
          Lp.coeFn_add ((hdf w v).toLp (df v)) ((hdf w u).toLp (df u)),
          (hdf w v).coeFn_toLp,(hdf w u).coeFn_toLp] with x hsum hadd hv hu
        simp only [Pi.add_apply] at hadd
        rw [hsum,hadd,hv,hu]
        simp [df,inner_add_left,mul_add]
      map_smul' := by
        intro c v
        apply Lp.ext
        filter_upwards [(hdf w (c • v)).coeFn_toLp,
          Lp.coeFn_smul c ((hdf w v).toLp (df v)),(hdf w v).coeFn_toLp] with x hcv hsmul hv
        simp only [Pi.smul_apply,smul_eq_mul] at hsmul
        simp only [RingHom.id_apply]
        rw [hcv,hsmul,hv]
        simp [df,real_inner_smul_left]
        ring }
    obtain ⟨B,hB,hB0,hBound⟩ :=
      polynomial_radial_envelope (E := E) p.derivative ‖w‖ (norm_nonneg _) 1
    let b := hB.toLp B
    have hnorm (v : E) : ‖L v‖ ≤ ‖v‖ * ‖b‖ := by
      apply Lp.norm_le_mul_norm_of_ae_le_mul
      filter_upwards [(hdf w v).coeFn_toLp,hB.coeFn_toLp] with x hv hBx
      change ‖(hdf w v).toLp (df v) x‖ ≤ ‖v‖ * ‖b x‖
      rw [hv]
      change ‖df v x‖ ≤ ‖v‖ * ‖hB.toLp B x‖
      rw [hBx,Real.norm_of_nonneg (hB0 x)]
      calc
        ‖df v x‖ = ‖p.derivative.eval ⟪w,x⟫_ℝ‖ * ‖⟪v,x⟫_ℝ‖ := norm_mul _ _
        _ ≤ ‖p.derivative.eval ⟪w,x⟫_ℝ‖ * (‖v‖*‖x‖) :=
          mul_le_mul_of_nonneg_left (norm_inner_le_norm (𝕜 := ℝ) v x) (norm_nonneg _)
        _ = ‖v‖ * (‖p.derivative.eval ⟪w,x⟫_ℝ‖ * ‖x‖) := by ring
        _ ≤ ‖v‖ * B x := mul_le_mul_of_nonneg_left
          (by simpa using hBound w le_rfl x) (norm_nonneg _)
    refine ⟨L.mkContinuous ‖b‖ (fun v => by simpa [mul_comm] using hnorm v),?_⟩
    intro v
    rfl
  choose D hD using hD
  exact ⟨D,hD⟩


private theorem actual_L2_hasFDerivAt
    {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]
    (p : Polynomial ℝ)
    (hf : ∀ w : E, MemLp (fun x : E => p.eval ⟪w,x⟫_ℝ) 2 (stdGaussian E))
    (hdf : ∀ w v : E, MemLp (fun x : E =>
      p.derivative.eval ⟪w,x⟫_ℝ * ⟪v,x⟫_ℝ) 2 (stdGaussian E))
    (D : E → E →L[ℝ] Lp ℝ 2 (stdGaussian E))
    (hD : ∀ w v, D w v = (hdf w v).toLp
      (fun x : E => p.derivative.eval ⟪w,x⟫_ℝ * ⟪v,x⟫_ℝ)) (w : E) :
    HasFDerivAt (fun u => (hf u).toLp (fun x : E => p.eval ⟪u,x⟫_ℝ)) (D w) w := by
  classical
  let μ := stdGaussian E
  let F := fun u : E => (hf u).toLp (fun x : E => p.eval ⟪u,x⟫_ℝ)
  let r := fun (u x : E) => p.eval ⟪u,x⟫_ℝ - p.eval ⟪w,x⟫_ℝ -
    p.derivative.eval ⟪w,x⟫_ℝ * ⟪u-w,x⟫_ℝ
  let q := fun (u x : E) => ‖u-w‖⁻¹ * ‖r u x‖
  obtain ⟨B,hB,hB0,hInc,hDir⟩ := local_increment_bounds p w
  have hR (u : E) (hu : ‖u-w‖ ≤ 1) (x : E) :
      ‖r u x‖ ≤ (2 * B x) * ‖u-w‖ := by
    exact (norm_sub_le _ _).trans ((add_le_add (hInc u hu x) (hDir (u-w) x)).trans_eq (by ring))
  have hq (u : E) (hu : ‖u-w‖ ≤ 1) (x : E) : q u x ≤ 2 * B x := by
    by_cases h : u = w
    · subst u
      simpa [q] using hB0 x
    · have hn : 0 < ‖u-w‖ := norm_pos_iff.mpr (sub_ne_zero.mpr h)
      calc
        q u x ≤ ‖u-w‖⁻¹ * ((2 * B x) * ‖u-w‖) :=
          mul_le_mul_of_nonneg_left (hR u hu x) (inv_nonneg.mpr (norm_nonneg _))
        _ = 2 * B x := by field_simp
  have hq0 (x : E) : q w x = 0 := by simp [q]
  have hqcont (x : E) : ContinuousAt (fun u : E => q u x) w := by
    rw [ContinuousAt,hq0]
    have ht := (hasFDerivAt_iff_tendsto.mp (pointwise_ridge_hasFDerivAt p w x))
    simpa only [q,r,ContinuousLinearMap.smul_apply,innerSL_apply_apply,
      smul_eq_mul,real_inner_comm x] using ht
  have hBsq : Integrable (fun x => 4 * (B x)^2) μ :=
    ((memLp_two_iff_integrable_sq hB.1).1 hB).const_mul 4
  have hc : ContinuousAt (fun u : E => ∫ x, (q u x)^2 ∂μ) w := by
    apply continuousAt_of_dominated (bound := fun x => 4 * (B x)^2)
    · exact Eventually.of_forall fun u => by dsimp [q,r]; fun_prop
    · filter_upwards [Metric.closedBall_mem_nhds w (by norm_num : (0:ℝ)<1)] with u hu
      have hu' : ‖u-w‖ ≤ 1 := by simpa [Metric.mem_closedBall,dist_eq_norm] using hu
      exact ae_of_all _ fun x => by
        rw [Real.norm_eq_abs,abs_of_nonneg (sq_nonneg _)]
        have hnon : 0 ≤ q u x := mul_nonneg (inv_nonneg.mpr (norm_nonneg _)) (norm_nonneg _)
        have h := (sq_le_sq₀ hnon (mul_nonneg (by norm_num : (0:ℝ) ≤ 2) (hB0 x))).2 (hq u hu' x)
        nlinarith
    · exact hBsq
    · exact ae_of_all _ fun x => (hqcont x).pow 2
  let R := fun u : E => F u - F w - D w (u-w)
  let G := fun u : E => ‖u-w‖⁻¹ • R u
  have hnorm (u : E) : ‖G u‖^2 = ∫ x, (q u x)^2 ∂μ := by
    rw [← real_inner_self_eq_norm_sq,L2.inner_def]
    apply integral_congr_ae
    have hd := (hdf w (u-w)).coeFn_toLp
    rw [← hD w (u-w)] at hd
    filter_upwards [Lp.coeFn_smul ‖u-w‖⁻¹ (R u),
      Lp.coeFn_sub (F u - F w) (D w (u-w)),
      Lp.coeFn_sub (F u) (F w),(hf u).coeFn_toLp,(hf w).coeFn_toLp,hd]
      with x hsm hsub hsub' hfu hfw hdx
    change inner ℝ (G u x) (G u x) = _
    have hval : G u x = ‖u-w‖⁻¹ * r u x := by
      change (‖u-w‖⁻¹ • R u) x = _
      rw [hsm]
      simp only [Pi.smul_apply,smul_eq_mul]
      change ‖u-w‖⁻¹ * (F u - F w - D w (u-w)) x = _
      rw [hsub]
      simp only [Pi.sub_apply]
      rw [hsub']
      simp only [Pi.sub_apply]
      change ‖u-w‖⁻¹ * ((hf u).toLp _ x - (hf w).toLp _ x - D w (u-w) x) = _
      rw [hfu,hfw,hdx]
    rw [hval]
    simp [q,real_inner_self_eq_norm_sq,norm_mul,Real.norm_of_nonneg (inv_nonneg.mpr (norm_nonneg (u-w))),mul_pow]
  have ht : Tendsto (fun u : E => ‖G u‖) (𝓝 w) (𝓝 0) := by
    have hsq : ContinuousAt (fun u : E => ‖G u‖^2) w := by simpa only [← hnorm] using hc
    have hz : G w = 0 := by simp [G]
    have h := (Real.continuous_sqrt.continuousAt.comp hsq).tendsto
    simpa only [Function.comp_def,Real.sqrt_sq (norm_nonneg _),hz,norm_zero,zero_pow (by decide : 2 ≠ 0),Real.sqrt_zero] using h
  apply hasFDerivAt_iff_tendsto.mpr
  simpa only [G,norm_smul,Real.norm_of_nonneg (inv_nonneg.mpr (norm_nonneg (_-w))),R,F] using ht

theorem actual_gaussian_polynomial_ridge_L2_frechet_derivative
    {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]
    (p : Polynomial ℝ) :
    let γ := ProbabilityTheory.stdGaussian E
    let f : E → E → ℝ := fun w x => p.eval ⟪w,x⟫_ℝ
    let df : E → E → E → ℝ := fun w v x => p.derivative.eval ⟪w,x⟫_ℝ * ⟪v,x⟫_ℝ
    ∃ hf : ∀ w, MemLp (f w) 2 γ,
    ∃ hdf : ∀ w v, MemLp (df w v) 2 γ,
    ∃ D : E → E →L[ℝ] Lp ℝ 2 γ,
      (∀ w v, D w v = (hdf w v).toLp (df w v)) ∧
      ∀ w, HasFDerivAt (fun u => (hf u).toLp (f u)) (D w) w := by
  dsimp only
  obtain ⟨hf,hdf⟩ := ambient_feature_and_derivative_memLp (E := E) p
  obtain ⟨D,hD⟩ := represented_derivative_clm p hdf
  exact ⟨hf,hdf,D,hD,fun w => actual_L2_hasFDerivAt p hf hdf D hD w⟩


private theorem produced_operator_bounds
    {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]
    (p : Polynomial ℝ)
    (hdf : ∀ w v : E, MemLp (fun x : E =>
      p.derivative.eval ⟪w,x⟫_ℝ * ⟪v,x⟫_ℝ) 2 (stdGaussian E))
    (D : E → E →L[ℝ] Lp ℝ 2 (stdGaussian E))
    (hD : ∀ w v, D w v = (hdf w v).toLp
      (fun x : E => p.derivative.eval ⟪w,x⟫_ℝ * ⟪v,x⟫_ℝ)) :
    ∃ M₁ M₂ : ℝ, 0 < M₁ ∧ 0 < M₂ ∧
      (∀ w : E, ‖w‖ ≤ 1 → ‖D w‖ ≤ M₁) ∧
      ∀ w u : E, ‖w‖ ≤ 1 → ‖u‖ ≤ 1 → ‖D u - D w‖ ≤ M₂ * ‖u-w‖ := by
  classical
  obtain ⟨B,hB,hB0,hBound⟩ := polynomial_radial_envelope (E := E) p.derivative 1 (by norm_num) 1
  obtain ⟨C,hC,hC0,hBound2⟩ := polynomial_radial_envelope (E := E) p.derivative.derivative 1 (by norm_num) 2
  let b := hB.toLp B
  let c := hC.toLp C
  have hnorm (w : E) (hw : ‖w‖ ≤ 1) (v : E) : ‖D w v‖ ≤ ‖v‖ * ‖b‖ := by
    apply Lp.norm_le_mul_norm_of_ae_le_mul
    rw [hD w v]
    filter_upwards [(hdf w v).coeFn_toLp,hB.coeFn_toLp] with x hv hBx
    rw [hv]
    change ‖p.derivative.eval ⟪w,x⟫_ℝ * ⟪v,x⟫_ℝ‖ ≤ ‖v‖ * ‖hB.toLp B x‖
    rw [hBx,Real.norm_of_nonneg (hB0 x),norm_mul]
    calc
      ‖p.derivative.eval ⟪w,x⟫_ℝ‖ * ‖⟪v,x⟫_ℝ‖ ≤
          ‖p.derivative.eval ⟪w,x⟫_ℝ‖ * (‖v‖*‖x‖) :=
        mul_le_mul_of_nonneg_left (norm_inner_le_norm (𝕜 := ℝ) v x) (norm_nonneg _)
      _ = ‖v‖ * (‖p.derivative.eval ⟪w,x⟫_ℝ‖ * ‖x‖) := by ring
      _ ≤ ‖v‖ * B x := mul_le_mul_of_nonneg_left
        (by simpa only [pow_one] using hBound w hw x) (norm_nonneg _)
  have hinc (w u : E) (hw : ‖w‖ ≤ 1) (hu : ‖u‖ ≤ 1) (v x : E) :
      ‖p.derivative.eval ⟪u,x⟫_ℝ * ⟪v,x⟫_ℝ -
        p.derivative.eval ⟪w,x⟫_ℝ * ⟪v,x⟫_ℝ‖ ≤ (‖v‖ * C x) * ‖u-w‖ := by
    let d := fun z : E => ⟪v,x⟫_ℝ • (p.derivative.derivative.eval ⟪z,x⟫_ℝ • innerSL ℝ x)
    have hd (z : E) : HasFDerivAt (fun q : E =>
        p.derivative.eval ⟪q,x⟫_ℝ * ⟪v,x⟫_ℝ) (d z) z := by
      convert (pointwise_ridge_hasFDerivAt p.derivative z x).const_smul ⟪v,x⟫_ℝ using 1 <;>
        (first | rfl | (ext q; simp [d,Pi.smul_apply,smul_eq_mul,mul_comm]))
    apply (convex_closedBall (0 : E) 1).norm_image_sub_le_of_norm_hasFDerivWithin_le
      (fun z _ => (hd z).hasFDerivWithinAt) ?_
      (by simpa [Metric.mem_closedBall,dist_zero_right] using hw)
      (by simpa [Metric.mem_closedBall,dist_zero_right] using hu)
    intro z hz
    have hz' : ‖z‖ ≤ 1 := by simpa [Metric.mem_closedBall,dist_zero_right] using hz
    dsimp only [d]
    rw [norm_smul,norm_smul,innerSL_apply_norm]
    calc
      ‖⟪v,x⟫_ℝ‖ * (‖p.derivative.derivative.eval ⟪z,x⟫_ℝ‖ * ‖x‖) ≤
          (‖v‖ * ‖x‖) * (‖p.derivative.derivative.eval ⟪z,x⟫_ℝ‖ * ‖x‖) :=
        mul_le_mul_of_nonneg_right (norm_inner_le_norm (𝕜 := ℝ) v x) (by positivity)
      _ = ‖v‖ * (‖p.derivative.derivative.eval ⟪z,x⟫_ℝ‖ * ‖x‖^2) := by ring
      _ ≤ ‖v‖ * C x := mul_le_mul_of_nonneg_left (hBound2 z hz' x) (norm_nonneg _)
  have hdiff (w u : E) (hw : ‖w‖ ≤ 1) (hu : ‖u‖ ≤ 1) (v : E) :
      ‖(D u-D w) v‖ ≤ (‖u-w‖*‖v‖) * ‖c‖ := by
    apply Lp.norm_le_mul_norm_of_ae_le_mul
    have hdu := (hdf u v).coeFn_toLp
    have hdw := (hdf w v).coeFn_toLp
    rw [← hD u v] at hdu
    rw [← hD w v] at hdw
    filter_upwards [Lp.coeFn_sub (D u v) (D w v),hdu,hdw,hC.coeFn_toLp]
      with x hsub hux hwx hCx
    change ‖(D u v - D w v) x‖ ≤ (‖u-w‖*‖v‖) * ‖hC.toLp C x‖
    rw [hsub]
    simp only [Pi.sub_apply]
    rw [hux,hwx,hCx,Real.norm_of_nonneg (hC0 x)]
    exact (hinc w u hw hu v x).trans_eq (by ring)
  have hOp (w : E) (hw : ‖w‖ ≤ 1) : ‖D w‖ ≤ ‖b‖ := by
    apply ContinuousLinearMap.opNorm_le_bound _ (norm_nonneg _)
    intro v
    simpa only [mul_comm] using hnorm w hw v
  have hOpDiff (w u : E) (hw : ‖w‖ ≤ 1) (hu : ‖u‖ ≤ 1) :
      ‖D u-D w‖ ≤ ‖c‖ * ‖u-w‖ := by
    apply ContinuousLinearMap.opNorm_le_bound _ (by positivity)
    intro v
    exact (hdiff w u hw hu v).trans_eq (by ring)
  refine ⟨‖b‖+1,‖c‖+1,by positivity,by positivity,?_,?_⟩
  · intro w hw
    exact (hOp w hw).trans (by linarith)
  · intro w u hw hu
    exact (hOpDiff w u hw hu).trans
      (mul_le_mul_of_nonneg_right (by linarith : ‖c‖ ≤ ‖c‖+1) (norm_nonneg _))

theorem actual_gaussian_polynomial_ridge_L2_derivative_bounds
    {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]
    (p : Polynomial ℝ) :
    let γ := ProbabilityTheory.stdGaussian E
    let f : E → E → ℝ := fun w x => p.eval ⟪w,x⟫_ℝ
    let df : E → E → E → ℝ := fun w v x => p.derivative.eval ⟪w,x⟫_ℝ * ⟪v,x⟫_ℝ
    ∃ hf : ∀ w, MemLp (f w) 2 γ,
    ∃ hdf : ∀ w v, MemLp (df w v) 2 γ,
    ∃ D : E → E →L[ℝ] Lp ℝ 2 γ,
      (∀ w v, D w v = (hdf w v).toLp (df w v)) ∧
      (∀ w, HasFDerivAt (fun u => (hf u).toLp (f u)) (D w) w) ∧
      ∃ M₁ M₂ : ℝ, 0 < M₁ ∧ 0 < M₂ ∧
        (∀ w : E, ‖w‖ ≤ 1 → ‖D w‖ ≤ M₁) ∧
        ∀ w u : E, ‖w‖ ≤ 1 → ‖u‖ ≤ 1 → ‖D u - D w‖ ≤ M₂ * ‖u-w‖ := by
  dsimp only
  obtain ⟨hf,hdf,D,hD,hDiff⟩ := actual_gaussian_polynomial_ridge_L2_frechet_derivative (E := E) p
  exact ⟨hf,hdf,D,hD,hDiff,produced_operator_bounds p hdf D hD⟩


end AutoSamplingTheory.TechnicalLemmas.Probability.GaussianPolynomialDifferentiation
