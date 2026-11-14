import AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumThreshold
import AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumSignalStrength
import AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumVariances

/-!
Private NON-ANCHOR genuine concrete-threshold application. One enlarged
C,delta cutoff yields the actual shifted diagonal-Gaussian bad-event bound.
No concentration validity of C, rotated law/detector, algorithm, oracle/TV/cost
or main lower bound is asserted. The two quadratics share the same sample.
The variance proof integrates the centered pointwise Young inequality; it
uses canonical actual L2/moment bounds and does not copy the earlier private
contrast provider or invoke independence between Q and norm squared.
-/

noncomputable section
open MeasureTheory ProbabilityTheory
open scoped BigOperators
open AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumThreshold
open AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumSignalStrength
open AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumModeGap
open AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumBias
open AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumVariances

set_option maxHeartbeats 800000 in
private theorem actual_gaussian_source_query_shifted_event_le_tenth (C : ℝ) (hC : 0 < C) {δ : ℝ} (hδ0 : 0 < δ) (hδ1 : δ < 1) :
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
    (μ {x | (-1 : ℝ) ^ n * Q x - 2 * τ * ‖x‖ ^ 2 ≤ 0}).toReal ≤ (1 : ℝ) / 10
 := by
  let B : ℝ := (1 - Real.exp (-4)) * Real.exp (-3)
  have he4 : Real.exp (-4) < 1 := by
    simpa only [Real.exp_zero] using Real.exp_lt_exp.mpr (by norm_num : (-4 : ℝ) < 0)
  have hBpos : 0 < B := mul_pos (by linarith) (Real.exp_pos _)
  obtain ⟨J, hJ⟩ := exists_nat_ge (640 / B ^ 2)
  obtain ⟨T, hT⟩ := eventual_actual_gaussian_threshold_small C hC hδ0 hδ1
  obtain ⟨S, hS⟩ := eventual_actual_gaussian_signal_strength hδ0 hδ1
  obtain ⟨K, hK⟩ := eventual_source_query_mode_gap hδ0 hδ1
  refine ⟨max T (max S (max K (J ^ 2))), ?_⟩
  intro d hd κ hκ hκcap q hq
  have hdT : T ≤ d := (le_max_left T (max S (max K (J ^ 2)))).trans hd
  have hdSKJ : max S (max K (J ^ 2)) ≤ d :=
    (le_max_right T (max S (max K (J ^ 2)))).trans hd
  have hdS : S ≤ d := (le_max_left S (max K (J ^ 2))).trans hdSKJ
  have hdKJ : max K (J ^ 2) ≤ d := (le_max_right S (max K (J ^ 2))).trans hdSKJ
  have hdK : K ≤ d := (le_max_left K (J ^ 2)).trans hdKJ
  have hdJ : J ^ 2 ≤ d := (le_max_right K (J ^ 2)).trans hdKJ
  let n : ℕ := 2 * q + 1
  let θ : Fin d → ℝ := fun i => ((i.val : ℝ) + 1 / 2) * Real.pi / (d : ℝ)
  let eigenvalue : Fin d → ℝ := fun i => (κ + 1) / 2 + (κ - 1) / 2 * Real.cos (θ i)
  let Λ : Matrix (Fin d) (Fin d) ℝ := Matrix.diagonal eigenvalue
  let μ : Measure (EuclideanSpace ℝ (Fin d)) := multivariateGaussian 0 Λ⁻¹
  let Q : EuclideanSpace ℝ (Fin d) → ℝ := fun x =>
    ∑ i : Fin d, Real.cos ((n : ℝ) * θ i) * (WithLp.ofLp x i) ^ 2
  let τ : ℝ := C * (((q : ℝ) + 1) * Real.sqrt (Real.log (d : ℝ) / (d : ℝ)) +
      (((q : ℝ) + 1) * ((q : ℝ) + 1 + Real.log (d : ℝ)) * Real.log (d : ℝ)) / (d : ℝ))
  let N : EuclideanSpace ℝ (Fin d) → ℝ := fun x => ‖x‖ ^ 2
  let M : ℝ := ∫ x : EuclideanSpace ℝ (Fin d), ‖x‖ ^ 2 ∂μ
  let b : ℝ := ∫ x : EuclideanSpace ℝ (Fin d), Q x ∂μ
  let β : ℝ := |b| / M
  let X : EuclideanSpace ℝ (Fin d) → ℝ := fun x => (-1 : ℝ) ^ n * Q x
  let Z : EuclideanSpace ℝ (Fin d) → ℝ := fun x => X x - 2 * τ * N x
  let m : ℝ := (-1 : ℝ) ^ n * b
  let zmean : ℝ := m - 2 * τ * M
  change (μ {x | Z x ≤ 0}).toReal ≤ (1 : ℝ) / 10
  have hadm := hK d hdK κ hκ hκcap q hq
  change 2 ≤ d ∧ 1 ≤ n ∧ n < d ∧ Real.sqrt κ ≤ (d : ℝ) - (n : ℝ) at hadm
  rcases hadm with ⟨hd2, hn1, hnd, hgap⟩
  have ht := hT d hdT κ hκ hκcap q hq
  change 0 ≤ τ ∧ τ ≤ 1 / 2 ∧ τ ≤ β / 4 at ht
  rcases ht with ⟨hτ0, hτhalf, hτβ⟩
  have hs := hS d hdS κ hκ hκcap q hq
  change 0 < M ∧ 0 < β ∧ (d : ℝ) / (2 * Real.sqrt κ) ≤ M ∧
    (d : ℝ) ^ ((1 + δ) / 2) / 2 ≤ M ∧
    (B ^ 2 / 2) * Real.sqrt (d : ℝ) ≤ M * β ^ 2 at hs
  rcases hs with ⟨hMpos, hβpos, _hMlower, _hMpower, hproduct⟩
  have hJsq : (J : ℝ) ^ 2 ≤ (d : ℝ) := by exact_mod_cast hdJ
  have hJsqrt : (J : ℝ) ≤ Real.sqrt (d : ℝ) := Real.le_sqrt_of_sq_le hJsq
  have hthreshold : (320 : ℝ) ≤ (B ^ 2 / 2) * Real.sqrt (d : ℝ) := by
    have ht := mul_le_mul_of_nonneg_left (hJ.trans hJsqrt) (by positivity : 0 ≤ B ^ 2 / 2)
    have heq : (B ^ 2 / 2) * (640 / B ^ 2) = (320 : ℝ) := by
      field_simp [ne_of_gt hBpos]; ring
    rw [heq] at ht
    exact ht
  have hsignal : (320 : ℝ) ≤ M * β ^ 2 := hthreshold.trans hproduct
  rcases actual_diagonal_gaussian_exponential_bias hd2 hκ n hn1 hnd hgap with
    ⟨_hMposBias, hmpos, _hlow, _hupp⟩
  change 0 < m at hmpos
  rcases actual_diagonal_gaussian_quadratic_variances hd2 hκ n hn1 hnd with
    ⟨hN, hQ, _hNexact, _hQexact, hNbound, hQbound, _hMupper⟩
  change MemLp N 2 μ at hN
  change MemLp Q 2 μ at hQ
  change Var[N; μ] ≤ 2 * M at hNbound
  change Var[Q; μ] ≤ 2 * M at hQbound
  have hX : MemLp X 2 μ := hQ.const_mul _
  have hZLp : MemLp Z 2 μ := hX.sub (hN.const_mul (2 * τ))
  have hZmeas : Measurable Z := by
    have hcoord (i : Fin d) : Measurable (fun x : EuclideanSpace ℝ (Fin d) =>
        WithLp.ofLp x i) := (EuclideanSpace.proj i).continuous.measurable
    change Measurable (fun x : EuclideanSpace ℝ (Fin d) =>
      (-1 : ℝ) ^ n * (∑ i : Fin d, Real.cos ((n : ℝ) * θ i) *
        (WithLp.ofLp x i) ^ 2) - 2 * τ * ‖x‖ ^ 2)
    exact ((Finset.measurable_sum _ (fun i _ =>
      (hcoord i).pow_const 2 |>.const_mul _)).const_mul _).sub
        ((measurable_norm.pow_const 2).const_mul (2 * τ))
  have hZ : MemLp Z 2 μ := ⟨hZmeas.aestronglyMeasurable, hZLp.2⟩
  have hmeanX : (∫ x, X x ∂μ) = m := by exact integral_const_mul _ _
  have hmeanZ : (∫ x, Z x ∂μ) = zmean := by
    calc
      _ = (∫ x, X x ∂μ) - ∫ x, (2 * τ) * N x ∂μ :=
        integral_sub (hX.integrable (by norm_num))
          ((hN.const_mul (2 * τ)).integrable (by norm_num))
      _ = _ := by rw [hmeanX, integral_const_mul]
  have habs : |b| = m := by
    calc
      |b| = |(-1 : ℝ) ^ n * b| := by rw [abs_mul, abs_neg_one_pow, one_mul]
      _ = _ := abs_of_pos hmpos
  have hmeanRatio : m = β * M := by
    dsimp [β]
    rw [habs]
    exact (div_mul_cancel₀ m (ne_of_gt hMpos)).symm
  have hmeansq : m ^ 2 = (M * β ^ 2) * M := by rw [hmeanRatio]; ring
  have hmeanlower : m / 2 ≤ zmean := by
    have ht := mul_le_mul_of_nonneg_right hτβ hMpos.le
    dsimp [zmean]
    rw [hmeanRatio]
    nlinarith
  have hzpos : 0 < zmean := by linarith
  have hsign : ((-1 : ℝ) ^ n) ^ 2 = 1 := by
    rw [← pow_mul, Nat.mul_comm, pow_mul]
    norm_num
  have hXbound : Var[X; μ] ≤ 2 * M := by
    change Var[fun x => (-1 : ℝ) ^ n * Q x; μ] ≤ _
    rw [variance_const_mul, hsign, one_mul]
    exact hQbound
  have hcenter (x : EuclideanSpace ℝ (Fin d)) :
      Z x - (∫ y, Z y ∂μ) =
        (X x - (∫ y, X y ∂μ)) - 2 * τ * (N x - (∫ y, N y ∂μ)) := by
    rw [hmeanZ, hmeanX]
    change (X x - 2 * τ * N x) - (m - 2 * τ * M) =
      (X x - m) - 2 * τ * (N x - M)
    ring
  have hIZ := (hZ.sub (memLp_const (∫ x, Z x ∂μ))).integrable_sq
  have hI1 := ((hX.sub (memLp_const (∫ x, X x ∂μ))).integrable_sq).const_mul (2 : ℝ)
  have hI2 := ((hN.sub (memLp_const (∫ x, N x ∂μ))).integrable_sq).const_mul (8 * τ ^ 2)
  change Integrable (fun x => (Z x - (∫ y, Z y ∂μ)) ^ 2) μ at hIZ
  change Integrable (fun x => 2 * (X x - (∫ y, X y ∂μ)) ^ 2) μ at hI1
  change Integrable (fun x => (8 * τ ^ 2) * (N x - (∫ y, N y ∂μ)) ^ 2) μ at hI2
  have hVYoung : Var[Z; μ] ≤ 2 * Var[X; μ] + 8 * τ ^ 2 * Var[N; μ] := by
    calc
      _ = ∫ x, (Z x - (∫ y, Z y ∂μ)) ^ 2 ∂μ := variance_eq_integral hZ.aemeasurable
      _ ≤ ∫ x, (2 * (X x - (∫ y, X y ∂μ)) ^ 2 +
          (8 * τ ^ 2) * (N x - (∫ y, N y ∂μ)) ^ 2) ∂μ := by
        apply integral_mono_ae hIZ (hI1.add hI2)
        exact Filter.Eventually.of_forall fun x => by
          change (Z x - (∫ y, Z y ∂μ)) ^ 2 ≤
            2 * (X x - (∫ y, X y ∂μ)) ^ 2 +
              (8 * τ ^ 2) * (N x - (∫ y, N y ∂μ)) ^ 2
          rw [hcenter x]
          nlinarith only [sq_nonneg ((X x - (∫ y, X y ∂μ)) +
            2 * τ * (N x - (∫ y, N y ∂μ)))]
      _ = 2 * (∫ x, (X x - (∫ y, X y ∂μ)) ^ 2 ∂μ) +
          (8 * τ ^ 2) * (∫ x, (N x - (∫ y, N y ∂μ)) ^ 2 ∂μ) := by
        calc
          _ = (∫ x, 2 * (X x - (∫ y, X y ∂μ)) ^ 2 ∂μ) +
              (∫ x, (8 * τ ^ 2) * (N x - (∫ y, N y ∂μ)) ^ 2 ∂μ) :=
            integral_add hI1 hI2
          _ = _ := congrArg₂ (fun a b : ℝ => a + b)
            (integral_const_mul 2 (fun x => (X x - (∫ y, X y ∂μ)) ^ 2))
            (integral_const_mul (8 * τ ^ 2) (fun x => (N x - (∫ y, N y ∂μ)) ^ 2))
      _ = _ := congrArg₂ (fun a b : ℝ => 2 * a + (8 * τ ^ 2) * b)
        (variance_eq_integral hX.aemeasurable).symm
        (variance_eq_integral hN.aemeasurable).symm
  have hτsq : τ ^ 2 ≤ (1 : ℝ) / 4 := by nlinarith only [hτ0, hτhalf]
  have hV : Var[Z; μ] ≤ 8 * M := by
    calc
      _ ≤ 2 * Var[X; μ] + 8 * τ ^ 2 * Var[N; μ] := hVYoung
      _ ≤ 2 * (2 * M) + 8 * τ ^ 2 * (2 * M) :=
        add_le_add (mul_le_mul_of_nonneg_left hXbound (by norm_num))
          (mul_le_mul_of_nonneg_left hNbound (by positivity))
      _ ≤ _ := by nlinarith only [mul_le_mul_of_nonneg_right hτsq hMpos.le]
  have hlarge : 80 * M ≤ zmean ^ 2 := by
    have hsM := mul_le_mul_of_nonneg_right hsignal hMpos.le
    have hsq := pow_le_pow_left₀ (by positivity : 0 ≤ m / 2) hmeanlower 2
    rw [← hmeansq] at hsM
    nlinarith only [hsM, hsq]
  have hsub : {x | Z x ≤ 0} ⊆ {x | zmean ≤ |Z x - (∫ y, Z y ∂μ)|} := by
    intro x hx
    change Z x ≤ 0 at hx
    change zmean ≤ |Z x - (∫ y, Z y ∂μ)|
    rw [hmeanZ, abs_of_nonpos (by linarith : Z x - zmean ≤ 0)]
    linarith
  have hc := meas_ge_le_variance_div_sq hZ hzpos
  have hm : μ {x | Z x ≤ 0} ≤ ENNReal.ofReal (Var[Z; μ] / zmean ^ 2) :=
    (measure_mono hsub).trans (by simpa only [hmeanZ] using hc)
  have hprob : (μ {x | Z x ≤ 0}).toReal ≤ Var[Z; μ] / zmean ^ 2 := by
    calc
      _ ≤ (ENNReal.ofReal (Var[Z; μ] / zmean ^ 2)).toReal :=
        ENNReal.toReal_mono ENNReal.ofReal_ne_top hm
      _ = _ := ENNReal.toReal_ofReal (div_nonneg (variance_nonneg _ _) (sq_nonneg _))
  calc
    _ ≤ Var[Z; μ] / zmean ^ 2 := hprob
    _ ≤ 8 * M / zmean ^ 2 := div_le_div_of_nonneg_right hV (sq_nonneg zmean)
    _ ≤ (1 : ℝ) / 10 := by
      apply (div_le_iff₀ (sq_pos_of_pos hzpos)).2
      nlinarith
