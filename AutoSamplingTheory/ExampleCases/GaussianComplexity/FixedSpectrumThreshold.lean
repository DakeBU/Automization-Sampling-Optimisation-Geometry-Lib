import AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumModeGap
import AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumBias

/-!
# Concrete numerical threshold versus actual Gaussian bias

Zhou--Suzuki arXiv:2610.20492v1, Section4.3 numerical proof component.
For every fixed positive numeric scale C and fixed delta, one natural cutoff
works uniformly over the original condition-number and natural query range.
This auxiliary C-family does not prove the existence or concentration property
of the source absolute C in Lemma4.4 and adds no premise to a main lower bound.
Literal tau is compared with actual inverse-precision Gaussian integral bias.
The scalar envelope is8*C*d^(-delta/2)*log(d)^3. Internal logarithmic little-o
and canonical ModeGap/Bias provide every cutoff, domain and moment condition.
The half-threshold output uses the stronger actual beta-quarter estimate and
beta<=1, a sufficient local route distinct from the source early scalar cutoff.
-/

noncomputable section
open Filter Asymptotics MeasureTheory ProbabilityTheory
open scoped BigOperators
open AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumModeGap
open AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumBias
namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumThreshold

private theorem threshold_envelope {C δ κ : ℝ} (hC : 0 ≤ C)
    (hδ0 : 0 ≤ δ) (hδ1 : δ ≤ 1) (d q : ℕ)
    (hd : 1 ≤ (d : ℝ)) (hlog : 1 ≤ Real.log (d : ℝ))
    (hκcap : κ ≤ (d : ℝ) ^ (1 - δ))
    (hq : (q : ℝ) ≤ (δ / 256) * Real.sqrt κ * Real.log (d : ℝ)) :
    C * (((q : ℝ) + 1) * Real.sqrt (Real.log (d : ℝ) / (d : ℝ)) +
      (((q : ℝ) + 1) * ((q : ℝ) + 1 + Real.log (d : ℝ)) * Real.log (d : ℝ)) / (d : ℝ))
      ≤ 8 * C * (d : ℝ) ^ (-δ / 2) * (Real.log (d : ℝ)) ^ 3 := by
  let x : ℝ := d
  let L : ℝ := Real.log x
  let R : ℝ := x ^ ((1 - δ) / 2)
  let A : ℝ := (q : ℝ) + 1
  change C * (A * Real.sqrt (L / x) + A * (A + L) * L / x) ≤
    8 * C * x ^ (-δ / 2) * L ^ 3
  have hx1 : 1 ≤ x := hd
  have hx : 0 < x := by linarith
  have hL1 : 1 ≤ L := hlog
  have hL0 : 0 ≤ L := by linarith
  have hR0 : 0 ≤ R := Real.rpow_nonneg hx.le _
  have hR1 : 1 ≤ R := by
    dsimp [R]
    exact Real.one_le_rpow hx1 (by linarith)
  have hs : Real.sqrt κ ≤ R := by
    calc
      _ ≤ Real.sqrt (x ^ (1 - δ)) := Real.sqrt_le_sqrt hκcap
      _ = R := by
        rw [Real.sqrt_eq_rpow, ← Real.rpow_mul hx.le]
        congr 1
        ring
  have hqR : (q : ℝ) ≤ R * L := by
    calc
      _ ≤ (δ / 256) * Real.sqrt κ * L := hq
      _ ≤ 1 * R * L := by gcongr; linarith
      _ = R * L := by ring
  have hRL : 1 ≤ R * L := by
    calc
      1 ≤ 1 * L := by linarith
      _ ≤ R * L := mul_le_mul_of_nonneg_right hR1 hL0
  have hA : A ≤ 2 * R * L := by dsimp [A]; linarith
  have hsum : A + L ≤ 3 * R * L := by
    have hLR : L ≤ R * L := by nlinarith
    linarith
  have hsL : Real.sqrt L ≤ L := (Real.sqrt_le_iff).2 ⟨hL0, by nlinarith⟩
  have hsdiv : Real.sqrt (L / x) ≤ L / Real.sqrt x := by
    rw [Real.sqrt_div hL0]
    exact div_le_div_of_nonneg_right hsL (Real.sqrt_nonneg _)
  have hRdiv : R / Real.sqrt x = x ^ (-δ / 2) := by
    rw [Real.sqrt_eq_rpow, ← Real.rpow_sub hx]
    congr 1
    ring
  have hR2div : R ^ 2 / x = x ^ (-δ) := by
    have he : R ^ 2 = x ^ (((1 - δ) / 2) * 2) := by
      dsimp [R]
      rw [Real.rpow_mul hx.le]
      norm_num
    rw [he, ← Real.rpow_sub_one (ne_of_gt hx)]
    congr 1
    ring
  have hLpow : L ^ 2 ≤ L ^ 3 := by
    calc
      _ ≤ L ^ 2 * L := le_mul_of_one_le_right (sq_nonneg L) hL1
      _ = L ^ 3 := by ring
  have hfirst : A * Real.sqrt (L / x) ≤ 2 * x ^ (-δ / 2) * L ^ 3 := by
    calc
      _ ≤ (2 * R * L) * (L / Real.sqrt x) := by gcongr
      _ = 2 * (R / Real.sqrt x) * L ^ 2 := by ring
      _ = 2 * x ^ (-δ / 2) * L ^ 2 := by rw [hRdiv]
      _ ≤ _ := mul_le_mul_of_nonneg_left hLpow (by positivity)
  have hsecond : A * (A + L) * L / x ≤ 6 * x ^ (-δ / 2) * L ^ 3 := by
    calc
      _ ≤ (2 * R * L) * (3 * R * L) * L / x := by gcongr
      _ = 6 * (R ^ 2 / x) * L ^ 3 := by ring
      _ = 6 * x ^ (-δ) * L ^ 3 := by rw [hR2div]
      _ ≤ _ := by
        have hp : x ^ (-δ) ≤ x ^ (-δ / 2) :=
          Real.rpow_le_rpow_of_exponent_le hx1 (by linarith)
        exact mul_le_mul_of_nonneg_right (mul_le_mul_of_nonneg_left hp (by norm_num))
          (pow_nonneg hL0 3)
  calc
    _ ≤ C * (2 * x ^ (-δ / 2) * L ^ 3 + 6 * x ^ (-δ / 2) * L ^ 3) :=
      mul_le_mul_of_nonneg_left (add_le_add hfirst hsecond) hC
    _ = _ := by ring

private theorem eventual_threshold_power_small (C B : ℝ) (hC : 0 < C) (hB : 0 < B)
    {δ : ℝ} (hδ0 : 0 < δ) (hδ1 : δ < 1) :
  ∃ D : ℕ, ∀ d : ℕ, D ≤ d → ∀ κ : ℝ, 2 ≤ κ →
    κ ≤ (d : ℝ) ^ (1 - δ) → ∀ q : ℕ,
    (q : ℝ) ≤ (δ / 256) * Real.sqrt κ * Real.log (d : ℝ) →
    let τ : ℝ := C * (((q : ℝ) + 1) * Real.sqrt (Real.log (d : ℝ) / (d : ℝ)) +
      (((q : ℝ) + 1) * ((q : ℝ) + 1 + Real.log (d : ℝ)) * Real.log (d : ℝ)) / (d : ℝ))
    0 ≤ τ ∧ τ ≤ (B / 4) * (d : ℝ) ^ (-δ / 4) := by
  have hlo : (fun d : ℕ => Real.log (d : ℝ) ^ (3 : ℕ)) =o[atTop]
      (fun d : ℕ => (d : ℝ) ^ (δ / 4)) := by
    simpa only [Function.comp_def, Real.rpow_ofNat] using
      (isLittleO_log_rpow_rpow_atTop (3 : ℝ) (by linarith : 0 < δ / 4)).comp_tendsto
        tendsto_natCast_atTop_atTop
  have heps : 0 < B / (32 * C) := by positivity
  have hlogevent : ∀ᶠ d : ℕ in atTop, 1 ≤ Real.log (d : ℝ) :=
    (Real.tendsto_log_atTop.comp tendsto_natCast_atTop_atTop).eventually
      (eventually_ge_atTop 1)
  have hev : ∀ᶠ d : ℕ in atTop,
      1 ≤ d ∧ 1 ≤ Real.log (d : ℝ) ∧
      Real.log (d : ℝ) ^ (3 : ℕ) ≤ (B / (32 * C)) * (d : ℝ) ^ (δ / 4) := by
    filter_upwards [hlo.def heps, hlogevent, eventually_ge_atTop (1 : ℕ)] with d hd hl hd1
    have hl0 : 0 ≤ Real.log (d : ℝ) := by linarith
    refine ⟨hd1, hl, ?_⟩
    simpa only [Real.norm_eq_abs, abs_of_nonneg (pow_nonneg hl0 3),
      abs_of_nonneg (Real.rpow_nonneg (Nat.cast_nonneg d) _)] using hd
  rcases eventually_atTop.1 hev with ⟨D, hD⟩
  refine ⟨D, ?_⟩
  intro d hd κ hκ hκcap q hq
  rcases hD d hd with ⟨hd1, hlog, hsmall⟩
  have hd1real : (1 : ℝ) ≤ (d : ℝ) := by exact_mod_cast hd1
  have hdpos : 0 < (d : ℝ) := by linarith
  have hlog0 : 0 ≤ Real.log (d : ℝ) := by linarith
  constructor
  · positivity
  · have he := threshold_envelope hC.le hδ0.le hδ1.le d q hd1real hlog
      hκcap hq
    have hp : (d : ℝ) ^ (-δ / 2) * (d : ℝ) ^ (δ / 4) =
        (d : ℝ) ^ (-δ / 4) := by
      rw [← Real.rpow_add hdpos]
      congr 1
      ring
    have hc : 8 * C * (B / (32 * C)) = B / 4 := by
      field_simp [ne_of_gt hC]; ring
    calc
      _ ≤ 8 * C * (d : ℝ) ^ (-δ / 2) * Real.log (d : ℝ) ^ 3 := he
      _ ≤ 8 * C * (d : ℝ) ^ (-δ / 2) *
          ((B / (32 * C)) * (d : ℝ) ^ (δ / 4)) :=
        mul_le_mul_of_nonneg_left hsmall (by positivity)
      _ = (8 * C * (B / (32 * C))) *
          ((d : ℝ) ^ (-δ / 2) * (d : ℝ) ^ (δ / 4)) := by ring
      _ = _ := by rw [hc, hp]

theorem eventual_actual_gaussian_threshold_small (C : ℝ) (hC : 0 < C) {δ : ℝ} (hδ0 : 0 < δ) (hδ1 : δ < 1) :
  ∃ d₀ : ℕ, ∀ (d : ℕ), d₀ ≤ d → ∀ (κ : ℝ), 2 ≤ κ →
    κ ≤ (d : ℝ) ^ (1 - δ) → ∀ (q : ℕ),
    (q : ℝ) ≤ (δ / 256) * Real.sqrt κ * Real.log (d : ℝ) →
    let n : ℕ := 2 * q + 1
    let θ : Fin d → ℝ := fun i => ((i.val : ℝ) + 1 / 2) * Real.pi / (d : ℝ)
    let eigenvalue : Fin d → ℝ := fun i => (κ + 1) / 2 + (κ - 1) / 2 * Real.cos (θ i)
    let Λ : Matrix (Fin d) (Fin d) ℝ := Matrix.diagonal eigenvalue
    let μ : Measure (EuclideanSpace ℝ (Fin d)) :=
      multivariateGaussian (0 : EuclideanSpace ℝ (Fin d)) Λ⁻¹
    let Q : EuclideanSpace ℝ (Fin d) → ℝ := fun x =>
      ∑ i : Fin d, Real.cos ((n : ℝ) * θ i) * (WithLp.ofLp x i) ^ 2
    let τ : ℝ := C * (((q : ℝ) + 1) * Real.sqrt (Real.log (d : ℝ) / (d : ℝ)) +
      (((q : ℝ) + 1) * ((q : ℝ) + 1 + Real.log (d : ℝ)) * Real.log (d : ℝ)) / (d : ℝ))
    let M : ℝ := ∫ x : EuclideanSpace ℝ (Fin d), ‖x‖ ^ 2 ∂μ
    let b : ℝ := ∫ x : EuclideanSpace ℝ (Fin d), Q x ∂μ
    let β : ℝ := |b| / M
    0 ≤ τ ∧ τ ≤ 1 / 2 ∧ τ ≤ β / 4
 := by
  let B : ℝ := (1 - Real.exp (-4)) * Real.exp (-3)
  have he4 : Real.exp (-4) < 1 := by
    simpa only [Real.exp_zero] using Real.exp_lt_exp.mpr (by norm_num : (-4 : ℝ) < 0)
  have hBpos : 0 < B := mul_pos (by linarith) (Real.exp_pos _)
  obtain ⟨D, hD⟩ := eventual_threshold_power_small C B hC hBpos hδ0 hδ1
  obtain ⟨K, hK⟩ := eventual_source_query_mode_gap hδ0 hδ1
  refine ⟨max D K, ?_⟩
  intro d hd κ hκ hκcap q hq
  have hdD : D ≤ d := (le_max_left D K).trans hd
  have hdK : K ≤ d := (le_max_right D K).trans hd
  let n : ℕ := 2 * q + 1
  let θ : Fin d → ℝ := fun i => ((i.val : ℝ) + 1 / 2) * Real.pi / (d : ℝ)
  let eigenvalue : Fin d → ℝ := fun i => (κ + 1) / 2 + (κ - 1) / 2 * Real.cos (θ i)
  let Λ : Matrix (Fin d) (Fin d) ℝ := Matrix.diagonal eigenvalue
  let μ : Measure (EuclideanSpace ℝ (Fin d)) := multivariateGaussian 0 Λ⁻¹
  let Q : EuclideanSpace ℝ (Fin d) → ℝ := fun x =>
    ∑ i : Fin d, Real.cos ((n : ℝ) * θ i) * (WithLp.ofLp x i) ^ 2
  let τ : ℝ := C * (((q : ℝ) + 1) * Real.sqrt (Real.log (d : ℝ) / (d : ℝ)) +
      (((q : ℝ) + 1) * ((q : ℝ) + 1 + Real.log (d : ℝ)) * Real.log (d : ℝ)) / (d : ℝ))
  let M : ℝ := ∫ x : EuclideanSpace ℝ (Fin d), ‖x‖ ^ 2 ∂μ
  let b : ℝ := ∫ x : EuclideanSpace ℝ (Fin d), Q x ∂μ
  let β : ℝ := |b| / M
  change 0 ≤ τ ∧ τ ≤ 1 / 2 ∧ τ ≤ β / 4
  have hadm := hK d hdK κ hκ hκcap q hq
  change 2 ≤ d ∧ 1 ≤ n ∧ n < d ∧ Real.sqrt κ ≤ (d : ℝ) - (n : ℝ) at hadm
  rcases hadm with ⟨hd2, hn1, hnd, hgap⟩
  have ht := hD d hdD κ hκ hκcap q hq
  change 0 ≤ τ ∧ τ ≤ (B / 4) * (d : ℝ) ^ (-δ / 4) at ht
  rcases ht with ⟨hτ0, hτpoly⟩
  rcases actual_diagonal_gaussian_exponential_bias hd2 hκ n hn1 hnd hgap with
    ⟨_hMpos, _hsign, hlow, hupp⟩
  change (1 - Real.exp (-4)) * Real.exp (-3 * (n : ℝ) / Real.sqrt κ) ≤ β at hlow
  change β ≤ Real.exp (-2 * (n : ℝ) / Real.sqrt κ) at hupp
  have hdpos : 0 < (d : ℝ) := by exact_mod_cast (by omega : 0 < d)
  have hd1 : (1 : ℝ) ≤ (d : ℝ) := by exact_mod_cast (by omega : 1 ≤ d)
  have hlog0 : 0 ≤ Real.log (d : ℝ) := Real.log_nonneg hd1
  have hspos : 0 < Real.sqrt κ := Real.sqrt_pos.2 (by linarith)
  have hsone : (1 : ℝ) ≤ Real.sqrt κ := Real.le_sqrt_of_sq_le (by nlinarith)
  have hqr : (q : ℝ) / Real.sqrt κ ≤ (δ / 256) * Real.log (d : ℝ) := by
    apply (div_le_iff₀ hspos).2
    calc
      _ ≤ (δ / 256) * Real.sqrt κ * Real.log (d : ℝ) := hq
      _ = _ := by ring
  have h3s : 3 / Real.sqrt κ ≤ (3 : ℝ) := by
    apply (div_le_iff₀ hspos).2
    nlinarith
  have hncalc : 3 * (n : ℝ) / Real.sqrt κ =
      6 * ((q : ℝ) / Real.sqrt κ) + 3 / Real.sqrt κ := by
    simp only [n, Nat.cast_add, Nat.cast_mul, Nat.cast_ofNat]
    ring
  have hns : 3 * (n : ℝ) / Real.sqrt κ ≤ 3 + (δ / 4) * Real.log (d : ℝ) := by
    have hrelax : (3 * δ / 128) * Real.log (d : ℝ) ≤
        (δ / 4) * Real.log (d : ℝ) :=
      mul_le_mul_of_nonneg_right (by linarith : 3 * δ / 128 ≤ δ / 4) hlog0
    rw [hncalc]
    nlinarith [mul_le_mul_of_nonneg_left hqr (by norm_num : (0 : ℝ) ≤ 6)]
  have hexponent : -3 + Real.log (d : ℝ) * (-δ / 4) ≤
      -3 * (n : ℝ) / Real.sqrt κ := by
    calc
      _ = -(3 + (δ / 4) * Real.log (d : ℝ)) := by ring
      _ ≤ -(3 * (n : ℝ) / Real.sqrt κ) := neg_le_neg hns
      _ = _ := by ring
  have hpoly : B * (d : ℝ) ^ (-δ / 4) ≤ β := by
    calc
      _ = (1 - Real.exp (-4)) *
          (Real.exp (-3) * Real.exp (Real.log (d : ℝ) * (-δ / 4))) := by
        rw [Real.rpow_def_of_pos hdpos]
        dsimp [B]
        ring
      _ = (1 - Real.exp (-4)) * Real.exp (-3 + Real.log (d : ℝ) * (-δ / 4)) := by
        rw [Real.exp_add]
      _ ≤ (1 - Real.exp (-4)) * Real.exp (-3 * (n : ℝ) / Real.sqrt κ) :=
        mul_le_mul_of_nonneg_left (Real.exp_le_exp.mpr hexponent) (by linarith)
      _ ≤ β := hlow
  have hτβ : τ ≤ β / 4 := by
    calc
      _ ≤ (B / 4) * (d : ℝ) ^ (-δ / 4) := hτpoly
      _ = (B * (d : ℝ) ^ (-δ / 4)) / 4 := by ring
      _ ≤ _ := div_le_div_of_nonneg_right hpoly (by norm_num)
  have hβone : β ≤ 1 := by
    apply hupp.trans
    rw [← Real.exp_zero]
    apply Real.exp_le_exp.mpr
    exact div_nonpos_of_nonpos_of_nonneg
      (mul_nonpos_of_nonpos_of_nonneg (by norm_num) (Nat.cast_nonneg n)) hspos.le
  exact ⟨hτ0, by linarith, hτβ⟩

end AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumThreshold
