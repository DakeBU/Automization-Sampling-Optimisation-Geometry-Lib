import AutoSamplingTheory.ExampleCases.GaussianComplexity.DeterminantCancellation
import Mathlib.Analysis.SpecialFunctions.Gaussian.FourierTransform
import Mathlib.MeasureTheory.Function.LocallyIntegrable
import Mathlib.MeasureTheory.Function.SpecialFunctions.Basic

/-!
# The radialized Gaussian test integral

Zhou--Suzuki arXiv:2610.20492v1, Appendix B.2.2, Ex60 and Eq21.
This evaluates the displayed explicit iterated integral, with genuine L1
conclusions, using the existing full Haar law and actual Lemma B.6.
Identification with the original H(lambda), actual Gaussian probability laws,
conjugation/radialization, Fubini, spherical Poisson and TV are separate.
-/

open Matrix MeasureTheory Set TopologicalSpace
open AutoSamplingTheory.TechnicalLemmas.Probability.OrthogonalHaar
open AutoSamplingTheory.ExampleCases.GaussianComplexity.DeterminantFamily
open AutoSamplingTheory.ExampleCases.GaussianComplexity.DeterminantCancellation

namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.RadialIntegral

private lemma integrable_continuous_haar {n : ℕ}
    {f : Matrix.orthogonalGroup (Fin n) ℝ → ℝ} (hf : Continuous f) :
    Integrable f (orthogonalHaar n) := by
  let := (orthogonalHaar_spec n).1
  exact hf.integrable_of_hasCompactSupport (isClosed_tsupport f).isCompact

private lemma gaussian_integral {n : ℕ} {a : ℝ} (ha : 0 < a) :
    Integrable (fun x : EuclideanSpace ℝ (Fin n) => Real.exp (-a * ‖x‖ ^ 2 / 4)) volume ∧
      (∫ x : EuclideanSpace ℝ (Fin n), Real.exp (-a * ‖x‖ ^ 2 / 4)) =
        (4 * Real.pi / a) ^ ((n : ℝ) / 2) := by
  have hb : 0 < ((a / 4 : ℝ) : ℂ).re := by simpa using (show 0 < a / 4 by positivity)
  have hc := GaussianFourier.integrable_cexp_neg_mul_sq_norm_add
    (V := EuclideanSpace ℝ (Fin n)) hb 0 0
  have hi := GaussianFourier.integral_rexp_neg_mul_sq_norm
    (V := EuclideanSpace ℝ (Fin n)) (b := a / 4) (by positivity)
  have he (x : EuclideanSpace ℝ (Fin n)) :
      -(a / 4) * ‖x‖ ^ 2 = -a * ‖x‖ ^ 2 / 4 := by ring
  constructor
  · convert hc.re using 1
    funext x
    simp only [zero_mul, add_zero]
    rw [← Complex.ofReal_pow, ← Complex.ofReal_neg, ← Complex.ofReal_mul,
      ← Complex.ofReal_exp]
    change Real.exp (-a * ‖x‖ ^ 2 / 4) = Real.exp (-(a / 4) * ‖x‖ ^ 2)
    exact congrArg Real.exp (he x).symm
  · have hp : Real.pi / (a / 4) = 4 * Real.pi / a := by ring
    simpa only [he, finrank_euclideanSpace, Fintype.card_fin, hp] using hi


theorem radialized_test_integral {n : ℕ} (hn : 3 ≤ n) {κ : ℝ}
    (hκ : 4 ≤ κ) {ℓ : ℝ} (hℓ : 0 ≤ ℓ) :
    let j0 : Fin n := ⟨0, lt_of_lt_of_le (by decide : 0 < 3) hn⟩
    let U : Matrix.orthogonalGroup (Fin n) ℝ → ℝ :=
      fun O => (O : Matrix (Fin n) (Fin n) ℝ) j0 j0
    let a : Matrix.orthogonalGroup (Fin n) ℝ → ℝ :=
      fun O => κ + 1 + 4 * ℓ - (κ - 1) * U O
    let p : ℝ := (n : ℝ) / 2
    (∀ O : Matrix.orthogonalGroup (Fin n) ℝ,
      Integrable (fun x : EuclideanSpace ℝ (Fin n) => Real.exp (-a O * ‖x‖ ^ 2 / 4)) volume) ∧
    Integrable (fun O : Matrix.orthogonalGroup (Fin n) ℝ =>
      (O : Matrix (Fin n) (Fin n) ℝ).det * Real.sqrt (singleBlockPrecision κ O).det *
        (∫ x : EuclideanSpace ℝ (Fin n), Real.exp (-a O * ‖x‖ ^ 2 / 4))) (orthogonalHaar n) ∧
    Integrable (fun O : Matrix.orthogonalGroup (Fin n) ℝ =>
      ((Real.sqrt κ + 1) * U O - (Real.sqrt κ - 1)) / (a O) ^ p) (orthogonalHaar n) ∧
    (∫ O : Matrix.orthogonalGroup (Fin n) ℝ,
      (O : Matrix (Fin n) (Fin n) ℝ).det * Real.sqrt (singleBlockPrecision κ O).det *
        (∫ x : EuclideanSpace ℝ (Fin n), Real.exp (-a O * ‖x‖ ^ 2 / 4)) ∂orthogonalHaar n) /
      (2 * Real.pi) ^ p =
      ((-1 : ℝ) ^ (n - 1) * (Real.sqrt κ - 1) ^ (n - 1) / (2 : ℝ) ^ p) *
        (∫ O : Matrix.orthogonalGroup (Fin n) ℝ,
          ((Real.sqrt κ + 1) * U O - (Real.sqrt κ - 1)) / (a O) ^ p ∂orthogonalHaar n) := by
  classical
  let j0 : Fin n := ⟨0, lt_of_lt_of_le (by decide : 0 < 3) hn⟩
  let U : Matrix.orthogonalGroup (Fin n) ℝ → ℝ :=
    fun O => (O : Matrix (Fin n) (Fin n) ℝ) j0 j0
  let a : Matrix.orthogonalGroup (Fin n) ℝ → ℝ :=
    fun O => κ + 1 + 4 * ℓ - (κ - 1) * U O
  let p : ℝ := (n : ℝ) / 2
  let F : Matrix.orthogonalGroup (Fin n) ℝ → ℝ :=
    fun O => (O : Matrix (Fin n) (Fin n) ℝ).det * Real.sqrt (singleBlockPrecision κ O).det
  let N : Matrix.orthogonalGroup (Fin n) ℝ → ℝ :=
    fun O => (Real.sqrt κ + 1) * U O - (Real.sqrt κ - 1)
  let J : Matrix.orthogonalGroup (Fin n) ℝ → ℝ :=
    fun O => ∫ x : EuclideanSpace ℝ (Fin n), Real.exp (-a O * ‖x‖ ^ 2 / 4)
  let C : ℝ := (4 * Real.pi) ^ p
  let c : ℝ := (-1 : ℝ) ^ (n - 1) * (Real.sqrt κ - 1) ^ (n - 1)
  change (∀ O : Matrix.orthogonalGroup (Fin n) ℝ,
      Integrable (fun x : EuclideanSpace ℝ (Fin n) => Real.exp (-a O * ‖x‖ ^ 2 / 4)) volume) ∧
    Integrable (fun O => F O * J O) (orthogonalHaar n) ∧
    Integrable (fun O => N O / (a O) ^ p) (orthogonalHaar n) ∧
      (∫ O, F O * J O ∂orthogonalHaar n) / (2 * Real.pi) ^ p =
        (c / (2 : ℝ) ^ p) * (∫ O, N O / (a O) ^ p ∂orthogonalHaar n)
  have hUc : Continuous U := continuous_subtype_val.matrix_elem j0 j0
  have hac : Continuous a := by dsimp only [a]; fun_prop
  have ha_bound (O : Matrix.orthogonalGroup (Fin n) ℝ) : 2 + 4 * ℓ ≤ a O := by
    have hU : U O ≤ 1 := le_trans (le_abs_self _) (by
      simpa only [U, Real.norm_eq_abs] using entry_norm_bound_of_unitary O.property j0 j0)
    have hmul := mul_le_mul_of_nonneg_left hU (show 0 ≤ κ - 1 by linarith)
    dsimp only [a]
    nlinarith
  have ha_pos (O : Matrix.orthogonalGroup (Fin n) ℝ) : 0 < a O := by
    have := ha_bound O
    linarith
  have hpownz (O : Matrix.orthogonalGroup (Fin n) ℝ) : (a O) ^ p ≠ 0 :=
    (Real.rpow_pos_of_pos (ha_pos O) p).ne'
  have hpowc : Continuous (fun O => (a O) ^ p) :=
    hac.rpow_const (fun O => Or.inl (ha_pos O).ne')
  have hAc : Continuous (fun O : Matrix.orthogonalGroup (Fin n) ℝ => singleBlockPrecision κ O) := by
    unfold singleBlockPrecision
    exact continuous_const.sub
      ((continuous_subtype_val.add continuous_subtype_val.matrix_transpose).const_smul ((κ - 1) / 4))
  have hFc : Continuous F := continuous_subtype_val.matrix_det.mul
    (Real.continuous_sqrt.comp hAc.matrix_det)
  have hNc : Continuous N := (hUc.const_mul _).sub continuous_const
  have hWint : Integrable (fun O => F O / (a O) ^ p) (orthogonalHaar n) :=
    integrable_continuous_haar (hFc.div hpowc hpownz)
  have hNint : Integrable (fun O => N O / (a O) ^ p) (orthogonalHaar n) :=
    integrable_continuous_haar (hNc.div hpowc hpownz)
  have hJ (O : Matrix.orthogonalGroup (Fin n) ℝ) : J O = (4 * Real.pi / a O) ^ p :=
    (gaussian_integral (ha_pos O)).2
  have hprod (O : Matrix.orthogonalGroup (Fin n) ℝ) :
      F O * J O = C * (F O / (a O) ^ p) := by
    rw [hJ, Real.div_rpow (by positivity) (ha_pos O).le]
    dsimp only [C]
    ring
  have hOuter : Integrable (fun O => F O * J O) (orthogonalHaar n) :=
    (hWint.const_mul C).congr (Filter.Eventually.of_forall fun O => (hprod O).symm)
  refine ⟨fun O => (gaussian_integral (ha_pos O)).1, hOuter, hNint, ?_⟩
  let h : ℝ → ℝ := fun u => 1 / (max (κ + 1 + 4 * ℓ - (κ - 1) * u) 1) ^ p
  have hbase : Continuous (fun u : ℝ => max (κ + 1 + 4 * ℓ - (κ - 1) * u) 1) := by fun_prop
  have hbase_pos (u : ℝ) : 0 < max (κ + 1 + 4 * ℓ - (κ - 1) * u) 1 :=
    lt_of_lt_of_le zero_lt_one (le_max_right _ _)
  have hh : Continuous h := continuous_const.div
    (hbase.rpow_const (fun u => Or.inl (hbase_pos u).ne'))
    (fun u => (Real.rpow_pos_of_pos (hbase_pos u) p).ne')
  have hactual (O : Matrix.orthogonalGroup (Fin n) ℝ) : h (U O) = 1 / (a O) ^ p := by
    change 1 / (max (a O) 1) ^ p = 1 / (a O) ^ p
    rw [max_eq_left (by linarith [ha_bound O])]
  have hL1 : Integrable (fun O => h (U O)) (orthogonalHaar n) :=
    integrable_continuous_haar (hh.comp hUc)
  have hb := signed_sqrt_det_integral hn hκ h hh.measurable hL1
  change (∫ O, F O * h (U O) ∂orthogonalHaar n) =
    c / (2 : ℝ) ^ n * (∫ O, N O * h (U O) ∂orthogonalHaar n) at hb
  simp_rw [hactual, mul_one_div] at hb
  have hOuter_eq : (∫ O, F O * J O ∂orthogonalHaar n) =
      C * (∫ O, F O / (a O) ^ p ∂orthogonalHaar n) := by
    simp_rw [hprod]
    exact integral_const_mul _ _
  have hpi_ne : (2 * Real.pi) ^ p ≠ 0 :=
    (Real.rpow_pos_of_pos (by positivity : 0 < 2 * Real.pi) p).ne'
  have htwo_ne : (2 : ℝ) ^ p ≠ 0 := (Real.rpow_pos_of_pos (by norm_num : 0 < (2 : ℝ)) p).ne'
  have hnorm : C / (2 * Real.pi) ^ p = (2 : ℝ) ^ p := by
    dsimp only [C]
    rw [show 4 * Real.pi = (2 : ℝ) * (2 * Real.pi) by ring,
      Real.mul_rpow (by norm_num : 0 ≤ (2 : ℝ)) (by positivity)]
    exact mul_div_cancel_right₀ _ hpi_ne
  have htwos : (2 : ℝ) ^ n = (2 : ℝ) ^ p * (2 : ℝ) ^ p := by
    rw [← Real.rpow_natCast, ← Real.rpow_add (by norm_num : 0 < (2 : ℝ))]
    congr 1
    dsimp only [p]
    ring
  rw [hOuter_eq]
  calc
    C * (∫ O, F O / (a O) ^ p ∂orthogonalHaar n) / (2 * Real.pi) ^ p =
        (C / (2 * Real.pi) ^ p) * (∫ O, F O / (a O) ^ p ∂orthogonalHaar n) := by ring
    _ = (2 : ℝ) ^ p * (c / (2 : ℝ) ^ n *
        (∫ O, N O / (a O) ^ p ∂orthogonalHaar n)) := by rw [hnorm, hb]
    _ = c / (2 : ℝ) ^ p * (∫ O, N O / (a O) ^ p ∂orthogonalHaar n) := by
      rw [htwos]
      field_simp [htwo_ne]

end AutoSamplingTheory.ExampleCases.GaussianComplexity.RadialIntegral
