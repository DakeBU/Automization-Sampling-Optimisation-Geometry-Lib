import AutoSamplingTheory.ExampleCases.GaussianComplexity.KernelAxis
import AutoSamplingTheory.ExampleCases.GaussianComplexity.RadialIntegral
import Mathlib.MeasureTheory.Integral.Prod
import Mathlib.Tactic.Positivity

/-!
# Genuine Fubini for the literal signed Gaussian mixture transform

Zhou--Suzuki arXiv:2610.20492v1, Appendix B.2.2, H definition through Eq21.
Joint Haar-times-Euclidean-volume L1 is produced internally. A finite compact
prefactor is a sufficient alternative to the sharp source Ex59 prefactor.
Actual Gaussian density/law identification and mixture/TV meanings stay separate.
-/

open Matrix MeasureTheory Set TopologicalSpace
open AutoSamplingTheory.TechnicalLemmas.Probability.OrthogonalHaar
open AutoSamplingTheory.ExampleCases.GaussianComplexity.DeterminantFamily
open AutoSamplingTheory.ExampleCases.GaussianComplexity.KernelAxis
open AutoSamplingTheory.ExampleCases.GaussianComplexity.RadialIntegral

namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.MixtureFubini

private lemma gaussian_decay_integrable {n : ℕ} :
    Integrable (fun x : EuclideanSpace ℝ (Fin n) => Real.exp (-‖x‖ ^ 2 / 2)) volume := by
  have hc := GaussianFourier.integrable_cexp_neg_mul_sq_norm_add
    (V := EuclideanSpace ℝ (Fin n))
    (b := ((1 / 2 : ℝ) : ℂ)) (by norm_num) 0 0
  convert hc.re using 1
  funext x
  simp only [zero_mul, add_zero]
  rw [← Complex.ofReal_pow, ← Complex.ofReal_neg, ← Complex.ofReal_mul,
    ← Complex.ofReal_exp]
  congr 1
  ring

private lemma joint_integrable {n : ℕ}
    (k : Matrix.orthogonalGroup (Fin n) ℝ → ℝ)
    (b : Matrix.orthogonalGroup (Fin n) ℝ × EuclideanSpace ℝ (Fin n) → ℝ)
    (hk : Continuous k) (hb : Continuous b)
    (hbound : ∀ z, b z ≤ -‖z.2‖ ^ 2 / 2) :
    Integrable (fun z => k z.1 * Real.exp (b z)) ((orthogonalHaar n).prod volume) := by
  let := (orthogonalHaar_spec n).1
  obtain ⟨C, hC⟩ := isCompact_univ.exists_bound_of_continuousOn hk.continuousOn
  have hmajor := (integrable_const C (μ := orthogonalHaar n)).mul_prod
    (gaussian_decay_integrable (n := n))
  apply hmajor.mono' ((hk.comp continuous_fst).mul (Real.continuous_exp.comp hb)).aestronglyMeasurable
  exact Filter.Eventually.of_forall fun z => by
    change ‖k z.1 * Real.exp (b z)‖ ≤ C * Real.exp (-‖z.2‖ ^ 2 / 2)
    rw [norm_mul, Real.norm_of_nonneg (Real.exp_pos (b z)).le]
    calc
      ‖k z.1‖ * Real.exp (b z) ≤ ‖k z.1‖ * Real.exp (-‖z.2‖ ^ 2 / 2) :=
        mul_le_mul_of_nonneg_left (Real.exp_le_exp.mpr (hbound z)) (norm_nonneg _)
      _ ≤ C * Real.exp (-‖z.2‖ ^ 2 / 2) :=
        mul_le_mul_of_nonneg_right (hC z.1 (mem_univ _)) (Real.exp_pos _).le

theorem literal_mixture_transform {n : ℕ} (hn : 3 ≤ n) {κ : ℝ}
    (hκ : 4 ≤ κ) {ℓ : ℝ} (hℓ : 0 ≤ ℓ) :
    let j0 : Fin n := ⟨0, lt_of_lt_of_le (by decide : 0 < 3) hn⟩
    let U : Matrix.orthogonalGroup (Fin n) ℝ → ℝ :=
      fun O => (O : Matrix (Fin n) (Fin n) ℝ) j0 j0
    let a : Matrix.orthogonalGroup (Fin n) ℝ → ℝ :=
      fun O => κ + 1 + 4 * ℓ - (κ - 1) * U O
    let p : Matrix.orthogonalGroup (Fin n) ℝ → EuclideanSpace ℝ (Fin n) → ℝ :=
      fun O x => Real.sqrt (singleBlockPrecision κ O).det /
        (2 * Real.pi) ^ ((n : ℝ) / 2) *
          Real.exp (-((WithLp.ofLp x) ⬝ᵥ
            (singleBlockPrecision κ O *ᵥ WithLp.ofLp x)) / 2)
    let f : (Matrix.orthogonalGroup (Fin n) ℝ × EuclideanSpace ℝ (Fin n)) → ℝ :=
      fun z => (z.1 : Matrix (Fin n) (Fin n) ℝ).det *
        (Real.exp (-ℓ * ‖z.2‖ ^ 2) * p z.1 z.2)
    let g : (Matrix.orthogonalGroup (Fin n) ℝ × EuclideanSpace ℝ (Fin n)) → ℝ :=
      fun z => (z.1 : Matrix (Fin n) (Fin n) ℝ).det *
        Real.sqrt (singleBlockPrecision κ z.1).det /
          (2 * Real.pi) ^ ((n : ℝ) / 2) * Real.exp (-a z.1 * ‖z.2‖ ^ 2 / 4)
    Integrable f ((orthogonalHaar n).prod volume) ∧
    Integrable g ((orthogonalHaar n).prod volume) ∧
    (∫ O : Matrix.orthogonalGroup (Fin n) ℝ,
      (O : Matrix (Fin n) (Fin n) ℝ).det *
        (∫ x : EuclideanSpace ℝ (Fin n), Real.exp (-ℓ * ‖x‖ ^ 2) * p O x)
        ∂orthogonalHaar n) =
      ((-1 : ℝ) ^ (n - 1) * (Real.sqrt κ - 1) ^ (n - 1) /
        (2 : ℝ) ^ ((n : ℝ) / 2)) *
        (∫ O : Matrix.orthogonalGroup (Fin n) ℝ,
          ((Real.sqrt κ + 1) * U O - (Real.sqrt κ - 1)) /
            (a O) ^ ((n : ℝ) / 2) ∂orthogonalHaar n) := by
  classical
  let j0 : Fin n := ⟨0, lt_of_lt_of_le (by decide : 0 < 3) hn⟩
  let U : Matrix.orthogonalGroup (Fin n) ℝ → ℝ :=
    fun O => (O : Matrix (Fin n) (Fin n) ℝ) j0 j0
  let a : Matrix.orthogonalGroup (Fin n) ℝ → ℝ :=
    fun O => κ + 1 + 4 * ℓ - (κ - 1) * U O
  let p : Matrix.orthogonalGroup (Fin n) ℝ → EuclideanSpace ℝ (Fin n) → ℝ :=
    fun O x => Real.sqrt (singleBlockPrecision κ O).det /
      (2 * Real.pi) ^ ((n : ℝ) / 2) *
        Real.exp (-((WithLp.ofLp x) ⬝ᵥ
          (singleBlockPrecision κ O *ᵥ WithLp.ofLp x)) / 2)
  let f : (Matrix.orthogonalGroup (Fin n) ℝ × EuclideanSpace ℝ (Fin n)) → ℝ :=
    fun z => (z.1 : Matrix (Fin n) (Fin n) ℝ).det *
      (Real.exp (-ℓ * ‖z.2‖ ^ 2) * p z.1 z.2)
  let g : (Matrix.orthogonalGroup (Fin n) ℝ × EuclideanSpace ℝ (Fin n)) → ℝ :=
    fun z => (z.1 : Matrix (Fin n) (Fin n) ℝ).det *
      Real.sqrt (singleBlockPrecision κ z.1).det /
        (2 * Real.pi) ^ ((n : ℝ) / 2) * Real.exp (-a z.1 * ‖z.2‖ ^ 2 / 4)
  let q (O : Matrix.orthogonalGroup (Fin n) ℝ) (x : EuclideanSpace ℝ (Fin n)) :=
    (WithLp.ofLp x) ⬝ᵥ (singleBlockPrecision κ O *ᵥ WithLp.ofLp x)
  let k (O : Matrix.orthogonalGroup (Fin n) ℝ) :=
    (O : Matrix (Fin n) (Fin n) ℝ).det * Real.sqrt (singleBlockPrecision κ O).det /
      (2 * Real.pi) ^ ((n : ℝ) / 2)
  let r (O : Matrix.orthogonalGroup (Fin n) ℝ) (x : EuclideanSpace ℝ (Fin n)) :=
    Real.sqrt (singleBlockPrecision κ O).det / (2 * Real.pi) ^ ((n : ℝ) / 2) *
      Real.exp (-(κ + 1 - (κ - 1) * U O) * ‖x‖ ^ 2 / 4)
  change Integrable f ((orthogonalHaar n).prod volume) ∧
    Integrable g ((orthogonalHaar n).prod volume) ∧ _
  let := (orthogonalHaar_spec n).1
  have hAc : Continuous (fun O : Matrix.orthogonalGroup (Fin n) ℝ => singleBlockPrecision κ O) := by
    unfold singleBlockPrecision
    exact continuous_const.sub
      ((continuous_subtype_val.add continuous_subtype_val.matrix_transpose).const_smul ((κ - 1) / 4))
  have hk : Continuous k := by dsimp only [k]; fun_prop
  have hUc : Continuous U := continuous_subtype_val.matrix_elem j0 j0
  have hac : Continuous a := by dsimp only [a]; fun_prop
  have hqc : Continuous (fun z : Matrix.orthogonalGroup (Fin n) ℝ × EuclideanSpace ℝ (Fin n) =>
      q z.1 z.2) := by dsimp only [q]; fun_prop
  have hq (O : Matrix.orthogonalGroup (Fin n) ℝ) (x : EuclideanSpace ℝ (Fin n)) :
      ‖x‖ ^ 2 ≤ q O x := by
    have h := ((singleBlockPrecision_regular hn hκ O).2 (WithLp.ofLp x)).1
    have he : (WithLp.ofLp x) ⬝ᵥ WithLp.ofLp x = ‖x‖ ^ 2 := by
      rw [EuclideanSpace.real_norm_sq_eq]
      simp only [dotProduct, pow_two]
    simpa only [he] using h
  have ha (O : Matrix.orthogonalGroup (Fin n) ℝ) : 2 ≤ a O := by
    have hu : U O ≤ 1 := le_trans (le_abs_self _) (by
      simpa only [U, Real.norm_eq_abs] using entry_norm_bound_of_unitary O.property j0 j0)
    have hm := mul_le_mul_of_nonneg_left hu (show 0 ≤ κ - 1 by linarith)
    dsimp only [a]
    linarith
  have hf : Integrable f ((orthogonalHaar n).prod volume) := by
    have hi := joint_integrable k (fun z => -ℓ * ‖z.2‖ ^ 2 + -(q z.1 z.2) / 2) hk
      (by fun_prop) (fun z => by
        have h1 := hq z.1 z.2
        have h2 := mul_nonneg hℓ (sq_nonneg ‖z.2‖)
        linarith)
    convert hi using 1
    funext z
    dsimp only [f, p, k, q]
    rw [Real.exp_add]
    ring
  have hg : Integrable g ((orthogonalHaar n).prod volume) := by
    have hi := joint_integrable k (fun z => -a z.1 * ‖z.2‖ ^ 2 / 4) hk
      (by fun_prop) (fun z => by
        have hm := mul_le_mul_of_nonneg_right (ha z.1) (sq_nonneg ‖z.2‖)
        nlinarith)
    exact hi
  refine ⟨hf, hg, ?_⟩
  have haxis (x : EuclideanSpace ℝ (Fin n)) :
      (∫ O : Matrix.orthogonalGroup (Fin n) ℝ,
        (O : Matrix (Fin n) (Fin n) ℝ).det * p O x ∂orthogonalHaar n) =
      (∫ O : Matrix.orthogonalGroup (Fin n) ℝ,
        (O : Matrix (Fin n) (Fin n) ℝ).det * r O x ∂orthogonalHaar n) :=
    (signed_kernel_radial hn hκ x).2.2
  have hgr (O : Matrix.orthogonalGroup (Fin n) ℝ) (x : EuclideanSpace ℝ (Fin n)) :
      g (O, x) = Real.exp (-ℓ * ‖x‖ ^ 2) *
        ((O : Matrix (Fin n) (Fin n) ℝ).det * r O x) := by
    dsimp only [g, r, a]
    rw [show Real.exp (-ℓ * ‖x‖ ^ 2) *
        ((O : Matrix (Fin n) (Fin n) ℝ).det *
          (Real.sqrt (singleBlockPrecision κ O).det / (2 * Real.pi) ^ ((n : ℝ) / 2) *
            Real.exp (-(κ + 1 - (κ - 1) * U O) * ‖x‖ ^ 2 / 4))) =
      ((O : Matrix (Fin n) (Fin n) ℝ).det * Real.sqrt (singleBlockPrecision κ O).det /
        (2 * Real.pi) ^ ((n : ℝ) / 2)) *
          (Real.exp (-ℓ * ‖x‖ ^ 2) * Real.exp (-(κ + 1 - (κ - 1) * U O) * ‖x‖ ^ 2 / 4)) by ring]
    rw [← Real.exp_add]
    congr 1
    congr 1
    ring
  have havg (x : EuclideanSpace ℝ (Fin n)) :
      (∫ O : Matrix.orthogonalGroup (Fin n) ℝ, f (O, x) ∂orthogonalHaar n) =
      (∫ O : Matrix.orthogonalGroup (Fin n) ℝ, g (O, x) ∂orthogonalHaar n) := by
    calc
      _ = Real.exp (-ℓ * ‖x‖ ^ 2) *
          (∫ O : Matrix.orthogonalGroup (Fin n) ℝ,
            (O : Matrix (Fin n) (Fin n) ℝ).det * p O x ∂orthogonalHaar n) := by
        rw [← integral_const_mul]
        apply integral_congr_ae
        exact Filter.Eventually.of_forall fun O => by dsimp only [f]; ring
      _ = Real.exp (-ℓ * ‖x‖ ^ 2) *
          (∫ O : Matrix.orthogonalGroup (Fin n) ℝ,
            (O : Matrix (Fin n) (Fin n) ℝ).det * r O x ∂orthogonalHaar n) := by rw [haxis]
      _ = _ := by
        rw [← integral_const_mul]
        apply integral_congr_ae
        exact Filter.Eventually.of_forall fun O => (hgr O x).symm
  have heval := (radialized_test_integral hn hκ hℓ).2.2.2
  calc
    _ = ∫ O : Matrix.orthogonalGroup (Fin n) ℝ,
        (∫ x : EuclideanSpace ℝ (Fin n), f (O, x)) ∂orthogonalHaar n := by
      apply integral_congr_ae
      exact Filter.Eventually.of_forall fun O => (integral_const_mul _ _).symm
    _ = ∫ x : EuclideanSpace ℝ (Fin n),
        (∫ O : Matrix.orthogonalGroup (Fin n) ℝ, f (O, x) ∂orthogonalHaar n) :=
      integral_integral_swap hf
    _ = ∫ x : EuclideanSpace ℝ (Fin n),
        (∫ O : Matrix.orthogonalGroup (Fin n) ℝ, g (O, x) ∂orthogonalHaar n) := by
      apply integral_congr_ae
      exact Filter.Eventually.of_forall havg
    _ = ∫ O : Matrix.orthogonalGroup (Fin n) ℝ,
        (∫ x : EuclideanSpace ℝ (Fin n), g (O, x)) ∂orthogonalHaar n :=
      (integral_integral_swap hg).symm
    _ = (∫ O : Matrix.orthogonalGroup (Fin n) ℝ,
        (O : Matrix (Fin n) (Fin n) ℝ).det * Real.sqrt (singleBlockPrecision κ O).det *
          (∫ x : EuclideanSpace ℝ (Fin n), Real.exp (-a O * ‖x‖ ^ 2 / 4))
          ∂orthogonalHaar n) / (2 * Real.pi) ^ ((n : ℝ) / 2) := by
      simp only [g, integral_const_mul]
      rw [← integral_div]
      apply integral_congr_ae
      exact Filter.Eventually.of_forall fun O => by ring
    _ = _ := heval

end AutoSamplingTheory.ExampleCases.GaussianComplexity.MixtureFubini
