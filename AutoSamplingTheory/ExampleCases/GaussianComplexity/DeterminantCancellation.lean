import AutoSamplingTheory.ExampleCases.GaussianComplexity.Normalizer
import AutoSamplingTheory.TechnicalLemmas.Probability.OrthogonalHaar
import Mathlib.LinearAlgebra.Matrix.Charpoly.Coeff
import Mathlib.MeasureTheory.Function.L1Space.Integrable
import Mathlib.MeasureTheory.Group.Integral
import Mathlib.Analysis.Normed.Group.Bounded
import Mathlib.Tactic.FunProp

/-!
# Haar principal-minor cancellation for the actual precision family

Zhou--Suzuki arXiv:2610.20492v1, Appendix B.2.1, Lemma B.6.
The statement seal retains the actual Borel/L1 hypothesis and the existing
normalized full orthogonal Haar law. Private reflection and compactness adapters
produce proof ingredients internally. This is not a Gaussian density, a
conditional sign posterior, an oracle transcript theorem or a main lower bound.
-/

open Matrix MeasureTheory Set TopologicalSpace
open AutoSamplingTheory.TechnicalLemmas.Probability.OrthogonalHaar
open AutoSamplingTheory.ExampleCases.GaussianComplexity.DeterminantFamily

namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.DeterminantCancellation

private noncomputable def rowReflection {n : ℕ} (i : Fin n) :
    Matrix.orthogonalGroup (Fin n) ℝ :=
  ⟨Matrix.diagonal (fun j => if j = i then (-1 : ℝ) else 1), by
    apply (Matrix.mem_orthogonalGroup_iff (Fin n) ℝ).2
    rw [Matrix.diagonal_transpose, Matrix.diagonal_mul_diagonal]
    have h : (fun j : Fin n => (if j = i then (-1 : ℝ) else 1) *
        (if j = i then (-1 : ℝ) else 1)) = fun _ => (1 : ℝ) := by
      funext j
      by_cases hj : j = i <;> simp [hj]
    rw [h, Matrix.diagonal_one]⟩

private lemma reflection_mul_apply {n : ℕ} (i : Fin n)
    (O : Matrix.orthogonalGroup (Fin n) ℝ) (j k : Fin n) :
    (rowReflection i * O : Matrix.orthogonalGroup (Fin n) ℝ).val j k =
      (if j = i then (-1 : ℝ) else 1) * (O : Matrix (Fin n) (Fin n) ℝ) j k := by
  change ((Matrix.diagonal (fun j : Fin n => if j = i then (-1 : ℝ) else 1)) *
    (O : Matrix (Fin n) (Fin n) ℝ)) j k = _
  simp only [Matrix.diagonal_mul]

private lemma reflection_minor_det {n : ℕ} (S : Finset (Fin n)) (i : Fin n)
    (hiS : i ∈ S) (O : Matrix.orthogonalGroup (Fin n) ℝ) :
    (((rowReflection i * O : Matrix.orthogonalGroup (Fin n) ℝ) :
      Matrix (Fin n) (Fin n) ℝ).submatrix (Subtype.val : S → Fin n)
        (Subtype.val : S → Fin n)).det =
      -((O : Matrix (Fin n) (Fin n) ℝ).submatrix
        (Subtype.val : S → Fin n) (Subtype.val : S → Fin n)).det := by
  classical
  have hm : (((rowReflection i * O : Matrix.orthogonalGroup (Fin n) ℝ) :
      Matrix (Fin n) (Fin n) ℝ).submatrix (Subtype.val : S → Fin n)
        (Subtype.val : S → Fin n)) =
      Matrix.diagonal (fun j : S => if (j : Fin n) = i then (-1 : ℝ) else 1) *
        (O : Matrix (Fin n) (Fin n) ℝ).submatrix
          (Subtype.val : S → Fin n) (Subtype.val : S → Fin n) := by
    ext j k
    simp only [Matrix.submatrix_apply, reflection_mul_apply, Matrix.diagonal_mul]
  rw [hm, Matrix.det_mul, Matrix.det_diagonal]
  have hp : (∏ j : S, if (j : Fin n) = i then (-1 : ℝ) else 1) = -1 := by
    calc
      _ = ∏ j : S, if j = (⟨i, hiS⟩ : S) then (-1 : ℝ) else 1 := by
        apply Finset.prod_congr rfl
        intro j hj
        simp only [Subtype.ext_iff]
      _ = -1 := by simp
  rw [hp, neg_one_mul]

private lemma integrable_minor_weight {n : ℕ} (S : Finset (Fin n))
    (g : Matrix.orthogonalGroup (Fin n) ℝ → ℝ) (hg : Integrable g (orthogonalHaar n)) :
    Integrable (fun O : Matrix.orthogonalGroup (Fin n) ℝ =>
      ((O : Matrix (Fin n) (Fin n) ℝ).submatrix
        (Subtype.val : S → Fin n) (Subtype.val : S → Fin n)).det * g O)
      (orthogonalHaar n) := by
  have hc : Continuous (fun O : Matrix.orthogonalGroup (Fin n) ℝ =>
      ((O : Matrix (Fin n) (Fin n) ℝ).submatrix
        (Subtype.val : S → Fin n) (Subtype.val : S → Fin n)).det) :=
    (continuous_subtype_val.matrix_submatrix _ _).matrix_det
  obtain ⟨C, hC⟩ := isCompact_univ.exists_bound_of_continuousOn hc.continuousOn
  exact hg.bdd_mul hc.measurable.aestronglyMeasurable
    (Filter.Eventually.of_forall fun O => hC O (mem_univ O))

theorem principalMinor_weighted_integral_eq_zero {n : ℕ} (hn : 3 ≤ n)
    (S : Finset (Fin n)) (i : Fin n) (hiS : i ∈ S) (hi0 : i ≠ (⟨0, lt_of_lt_of_le (by decide : 0 < 3) hn⟩ : Fin n))
    (h : ℝ → ℝ) (hh : Measurable h)
    (hL1 : Integrable (fun O : Matrix.orthogonalGroup (Fin n) ℝ => h ((O : Matrix (Fin n) (Fin n) ℝ) (⟨0, lt_of_lt_of_le (by decide : 0 < 3) hn⟩ : Fin n) (⟨0, lt_of_lt_of_le (by decide : 0 < 3) hn⟩ : Fin n))) (orthogonalHaar n)) :
    Integrable (fun O : Matrix.orthogonalGroup (Fin n) ℝ => ((O : Matrix (Fin n) (Fin n) ℝ).submatrix (Subtype.val : S → Fin n) (Subtype.val : S → Fin n)).det * h ((O : Matrix (Fin n) (Fin n) ℝ) (⟨0, lt_of_lt_of_le (by decide : 0 < 3) hn⟩ : Fin n) (⟨0, lt_of_lt_of_le (by decide : 0 < 3) hn⟩ : Fin n))) (orthogonalHaar n) ∧
      (∫ O : Matrix.orthogonalGroup (Fin n) ℝ, ((O : Matrix (Fin n) (Fin n) ℝ).submatrix (Subtype.val : S → Fin n) (Subtype.val : S → Fin n)).det * h ((O : Matrix (Fin n) (Fin n) ℝ) (⟨0, lt_of_lt_of_le (by decide : 0 < 3) hn⟩ : Fin n) (⟨0, lt_of_lt_of_le (by decide : 0 < 3) hn⟩ : Fin n)) ∂orthogonalHaar n) = 0 := by
  classical
  refine ⟨integrable_minor_weight S _ hL1, ?_⟩
  let j0 : Fin n := ⟨0, lt_of_lt_of_le (by decide : 0 < 3) hn⟩
  have hji : j0 ≠ i := Ne.symm hi0
  let F : Matrix.orthogonalGroup (Fin n) ℝ → ℝ := fun O =>
    ((O : Matrix (Fin n) (Fin n) ℝ).submatrix
      (Subtype.val : S → Fin n) (Subtype.val : S → Fin n)).det *
        h ((O : Matrix (Fin n) (Fin n) ℝ) j0 j0)
  change (∫ O, F O ∂orthogonalHaar n) = 0
  have hodd : ∀ O, F (rowReflection i * O) = -F O := by
    intro O
    dsimp only [F]
    rw [reflection_minor_det S i hiS O]
    have hu : (rowReflection i * O : Matrix.orthogonalGroup (Fin n) ℝ).val j0 j0 =
        (O : Matrix (Fin n) (Fin n) ℝ) j0 j0 := by
      simpa only [if_neg hji, one_mul] using reflection_mul_apply i O j0 j0
    rw [hu]
    ring
  have hemb : MeasurableEmbedding
      (fun O : Matrix.orthogonalGroup (Fin n) ℝ => rowReflection i * O) :=
    (MeasurableEquiv.mulLeft (rowReflection i)).measurableEmbedding
  have heq : (∫ O, F (rowReflection i * O) ∂orthogonalHaar n) =
      ∫ O, F O ∂orthogonalHaar n := by
    rw [← hemb.integral_map, orthogonalHaar_map_mul_left]
  have hz : -(∫ O, F O ∂orthogonalHaar n) = ∫ O, F O ∂orthogonalHaar n := by
    simpa only [hodd, integral_neg] using heq
  linarith


private lemma det_affine_principalMinor {n : ℕ}
    (M : Matrix (Fin n) (Fin n) ℝ) (a b : ℝ) :
    (a • M + b • (1 : Matrix (Fin n) (Fin n) ℝ)).det =
      ∑ S : Finset (Fin n), a ^ S.card * b ^ (n - S.card) *
        (M.submatrix (Subtype.val : S → Fin n) (Subtype.val : S → Fin n)).det := by
  classical
  let D := (detRowAlternating : (Fin n → ℝ) [⋀^Fin n]→ₗ[ℝ] ℝ)
  change D ((fun i => a • M i) +
    (fun i => b • (1 : Matrix (Fin n) (Fin n) ℝ) i)) = _
  rw [D.map_add_univ]
  apply Finset.sum_congr rfl
  intro S hS
  have hs : S.piecewise (fun i => a • M i)
      (fun i => b • (1 : Matrix (Fin n) (Fin n) ℝ) i) =
      fun i => (if i ∈ S then a else b) •
        S.piecewise M (1 : Matrix (Fin n) (Fin n) ℝ) i := by
    funext i j
    simp only [Finset.piecewise, Pi.smul_apply, smul_eq_mul]
    split_ifs <;> rfl
  rw [hs, D.map_smul_univ]
  have hp : (∏ i : Fin n, if i ∈ S then a else b) =
      a ^ S.card * b ^ (n - S.card) := by
    have h₁ : (Finset.univ.filter fun i : Fin n => i ∈ S) = S := by
      ext i
      simp
    have h₂ : (Finset.univ.filter fun i : Fin n => i ∉ S) = Finset.univ \ S := by
      ext i
      simp
    rw [Finset.prod_ite, h₁, h₂]
    simp only [Finset.prod_const, Finset.card_sdiff_of_subset (Finset.subset_univ S),
      Finset.card_univ, Fintype.card_fin]
  rw [hp, smul_eq_mul]
  congr 1
  exact Matrix.det_piecewise_one_eq_submatrix_det M S

private lemma affine_det_weighted_average {n : ℕ} (hn : 3 ≤ n) (a b : ℝ)
    (h : ℝ → ℝ) (hh : Measurable h)
    (hL1 : Integrable (fun O : Matrix.orthogonalGroup (Fin n) ℝ =>
      h ((O : Matrix (Fin n) (Fin n) ℝ)
        (⟨0, lt_of_lt_of_le (by decide : 0 < 3) hn⟩ : Fin n)
        (⟨0, lt_of_lt_of_le (by decide : 0 < 3) hn⟩ : Fin n))) (orthogonalHaar n)) :
    (∫ O : Matrix.orthogonalGroup (Fin n) ℝ,
      (a • (O : Matrix (Fin n) (Fin n) ℝ) + b • (1 : Matrix (Fin n) (Fin n) ℝ)).det *
        h ((O : Matrix (Fin n) (Fin n) ℝ)
          (⟨0, lt_of_lt_of_le (by decide : 0 < 3) hn⟩ : Fin n)
          (⟨0, lt_of_lt_of_le (by decide : 0 < 3) hn⟩ : Fin n)) ∂orthogonalHaar n) =
      b ^ n * (∫ O : Matrix.orthogonalGroup (Fin n) ℝ,
        h ((O : Matrix (Fin n) (Fin n) ℝ)
          (⟨0, lt_of_lt_of_le (by decide : 0 < 3) hn⟩ : Fin n)
          (⟨0, lt_of_lt_of_le (by decide : 0 < 3) hn⟩ : Fin n)) ∂orthogonalHaar n) +
      a * b ^ (n - 1) * (∫ O : Matrix.orthogonalGroup (Fin n) ℝ,
        (O : Matrix (Fin n) (Fin n) ℝ)
          (⟨0, lt_of_lt_of_le (by decide : 0 < 3) hn⟩ : Fin n)
          (⟨0, lt_of_lt_of_le (by decide : 0 < 3) hn⟩ : Fin n) *
        h ((O : Matrix (Fin n) (Fin n) ℝ)
          (⟨0, lt_of_lt_of_le (by decide : 0 < 3) hn⟩ : Fin n)
          (⟨0, lt_of_lt_of_le (by decide : 0 < 3) hn⟩ : Fin n)) ∂orthogonalHaar n) := by
  classical
  let j0 : Fin n := ⟨0, lt_of_lt_of_le (by decide : 0 < 3) hn⟩
  let g : Matrix.orthogonalGroup (Fin n) ℝ → ℝ := fun O =>
    h ((O : Matrix (Fin n) (Fin n) ℝ) j0 j0)
  let m (S : Finset (Fin n)) (O : Matrix.orthogonalGroup (Fin n) ℝ) :=
    ((O : Matrix (Fin n) (Fin n) ℝ).submatrix
      (Subtype.val : S → Fin n) (Subtype.val : S → Fin n)).det
  let c (S : Finset (Fin n)) := a ^ S.card * b ^ (n - S.card)
  have hm : ∀ S, Integrable (fun O => m S O * g O) (orthogonalHaar n) :=
    fun S => integrable_minor_weight S g hL1
  have hexp : ∀ O : Matrix.orthogonalGroup (Fin n) ℝ,
      (a • (O : Matrix (Fin n) (Fin n) ℝ) + b • (1 : Matrix (Fin n) (Fin n) ℝ)).det *
        g O = ∑ S : Finset (Fin n), c S * (m S O * g O) := by
    intro O
    rw [det_affine_principalMinor, Finset.sum_mul]
    apply Finset.sum_congr rfl
    intro S hS
    dsimp only [c, m]
    ring
  have hsum : (∫ O : Matrix.orthogonalGroup (Fin n) ℝ,
      (a • (O : Matrix (Fin n) (Fin n) ℝ) + b • (1 : Matrix (Fin n) (Fin n) ℝ)).det *
        g O ∂orthogonalHaar n) =
      ∑ S : Finset (Fin n), c S * (∫ O, m S O * g O ∂orthogonalHaar n) := by
    simp_rw [hexp]
    rw [integral_finsetSum Finset.univ (fun S hS => (hm S).const_mul (c S))]
    apply Finset.sum_congr rfl
    intro S hS
    exact integral_const_mul _ _
  let K : Finset (Finset (Fin n)) := {∅, {j0}}
  have hzero : ∀ S ∈ (Finset.univ : Finset (Finset (Fin n))), S ∉ K →
      c S * (∫ O, m S O * g O ∂orthogonalHaar n) = 0 := by
    intro S hS hSK
    have hS0 : S ≠ ∅ := by
      intro he
      apply hSK
      simp [K, he]
    have hS1 : S ≠ {j0} := by
      intro he
      apply hSK
      simp [K, he]
    have hex : ∃ i ∈ S, i ≠ j0 := by
      by_contra hnone
      push Not at hnone
      have hsub : S ⊆ {j0} := Finset.subset_singleton_iff'.2 hnone
      exact (Finset.subset_singleton_iff.mp hsub).elim hS0 hS1
    obtain ⟨i, hiS, hi0⟩ := hex
    have hz := (principalMinor_weighted_integral_eq_zero hn S i hiS hi0 h hh hL1).2
    change (∫ O, m S O * g O ∂orthogonalHaar n) = 0 at hz
    rw [hz, mul_zero]
  have hred : (∑ S : Finset (Fin n), c S *
      (∫ O, m S O * g O ∂orthogonalHaar n)) =
      c ∅ * (∫ O, m ∅ O * g O ∂orthogonalHaar n) +
        c {j0} * (∫ O, m {j0} O * g O ∂orthogonalHaar n) := by
    calc
      _ = ∑ S ∈ K, c S * (∫ O, m S O * g O ∂orthogonalHaar n) :=
        (Finset.sum_subset (Finset.subset_univ K) hzero).symm
      _ = _ := by simp [K]
  have hEmpty : ∀ O, m ∅ O = 1 := by
    intro O
    exact Matrix.det_eq_one_of_card_eq_zero (by simp)
  have hOne : ∀ O, m {j0} O = (O : Matrix (Fin n) (Fin n) ℝ) j0 j0 := by
    intro O
    exact Matrix.det_eq_elem_of_card_eq_one (by simp) (⟨j0, by simp⟩ : ({j0} : Finset (Fin n)))
  change (∫ O : Matrix.orthogonalGroup (Fin n) ℝ,
      (a • (O : Matrix (Fin n) (Fin n) ℝ) + b • (1 : Matrix (Fin n) (Fin n) ℝ)).det *
        g O ∂orthogonalHaar n) = _
  rw [hsum, hred]
  simp only [hEmpty, hOne, c, Finset.card_empty, Finset.card_singleton,
    pow_zero, pow_one, Nat.sub_zero, one_mul]
  rfl

theorem signed_sqrt_det_integral {n : ℕ} (hn : 3 ≤ n) {κ : ℝ} (hκ : 4 ≤ κ)
    (h : ℝ → ℝ) (hh : Measurable h)
    (hL1 : Integrable (fun O : Matrix.orthogonalGroup (Fin n) ℝ => h ((O : Matrix (Fin n) (Fin n) ℝ) (⟨0, lt_of_lt_of_le (by decide : 0 < 3) hn⟩ : Fin n) (⟨0, lt_of_lt_of_le (by decide : 0 < 3) hn⟩ : Fin n))) (orthogonalHaar n)) :
    (∫ O : Matrix.orthogonalGroup (Fin n) ℝ,
      (O : Matrix (Fin n) (Fin n) ℝ).det * Real.sqrt (singleBlockPrecision κ O).det *
        h ((O : Matrix (Fin n) (Fin n) ℝ) (⟨0, lt_of_lt_of_le (by decide : 0 < 3) hn⟩ : Fin n) (⟨0, lt_of_lt_of_le (by decide : 0 < 3) hn⟩ : Fin n)) ∂orthogonalHaar n) =
      ((-1 : ℝ) ^ (n - 1) * (Real.sqrt κ - 1) ^ (n - 1) / (2 : ℝ) ^ n) *
        (∫ O : Matrix.orthogonalGroup (Fin n) ℝ,
          ((Real.sqrt κ + 1) * ((O : Matrix (Fin n) (Fin n) ℝ) (⟨0, lt_of_lt_of_le (by decide : 0 < 3) hn⟩ : Fin n) (⟨0, lt_of_lt_of_le (by decide : 0 < 3) hn⟩ : Fin n)) - (Real.sqrt κ - 1)) *
            h ((O : Matrix (Fin n) (Fin n) ℝ) (⟨0, lt_of_lt_of_le (by decide : 0 < 3) hn⟩ : Fin n) (⟨0, lt_of_lt_of_le (by decide : 0 < 3) hn⟩ : Fin n)) ∂orthogonalHaar n) := by
  classical
  let j0 : Fin n := ⟨0, lt_of_lt_of_le (by decide : 0 < 3) hn⟩
  let U (O : Matrix.orthogonalGroup (Fin n) ℝ) : ℝ :=
    (O : Matrix (Fin n) (Fin n) ℝ) j0 j0
  let g : Matrix.orthogonalGroup (Fin n) ℝ → ℝ := fun O => h (U O)
  let a := Real.sqrt κ + 1
  let b := Real.sqrt κ - 1
  change (∫ O : Matrix.orthogonalGroup (Fin n) ℝ,
      (O : Matrix (Fin n) (Fin n) ℝ).det * Real.sqrt (singleBlockPrecision κ O).det *
        g O ∂orthogonalHaar n) =
    ((-1 : ℝ) ^ (n - 1) * b ^ (n - 1) / (2 : ℝ) ^ n) *
      (∫ O : Matrix.orthogonalGroup (Fin n) ℝ, (a * U O - b) * g O ∂orthogonalHaar n)
  have hnorm : ∀ O : Matrix.orthogonalGroup (Fin n) ℝ,
      (O : Matrix (Fin n) (Fin n) ℝ).det * Real.sqrt (singleBlockPrecision κ O).det =
        (1 / (2 : ℝ) ^ n) *
          (a • (O : Matrix (Fin n) (Fin n) ℝ) + (-b) • (1 : Matrix (Fin n) (Fin n) ℝ)).det := by
    intro O
    simpa only [a, b, neg_smul, sub_eq_add_neg] using singleBlockPrecision_signed_sqrt_det hn hκ O
  have hstep : (∫ O : Matrix.orthogonalGroup (Fin n) ℝ,
      (O : Matrix (Fin n) (Fin n) ℝ).det * Real.sqrt (singleBlockPrecision κ O).det *
        g O ∂orthogonalHaar n) =
      (1 / (2 : ℝ) ^ n) * (∫ O : Matrix.orthogonalGroup (Fin n) ℝ,
        (a • (O : Matrix (Fin n) (Fin n) ℝ) + (-b) • (1 : Matrix (Fin n) (Fin n) ℝ)).det *
          g O ∂orthogonalHaar n) := by
    calc
      _ = ∫ O : Matrix.orthogonalGroup (Fin n) ℝ, (1 / (2 : ℝ) ^ n) *
          ((a • (O : Matrix (Fin n) (Fin n) ℝ) + (-b) •
            (1 : Matrix (Fin n) (Fin n) ℝ)).det * g O) ∂orthogonalHaar n := by
        apply integral_congr_ae
        exact Filter.Eventually.of_forall fun O => by
          dsimp only
          rw [hnorm O]
          ring
      _ = _ := integral_const_mul _ _
  have havg := affine_det_weighted_average hn a (-b) h hh hL1
  change (∫ O : Matrix.orthogonalGroup (Fin n) ℝ,
      (a • (O : Matrix (Fin n) (Fin n) ℝ) + (-b) • (1 : Matrix (Fin n) (Fin n) ℝ)).det *
        g O ∂orthogonalHaar n) =
      (-b) ^ n * (∫ O, g O ∂orthogonalHaar n) +
        a * (-b) ^ (n - 1) * (∫ O, U O * g O ∂orthogonalHaar n) at havg
  have hUc : Continuous U := by
    dsimp only [U]
    exact (continuous_apply j0).comp ((continuous_apply j0).comp continuous_subtype_val)
  have hU : Integrable (fun O => U O * g O) (orthogonalHaar n) :=
    hL1.bdd_mul hUc.measurable.aestronglyMeasurable
      (show ∀ᵐ O : Matrix.orthogonalGroup (Fin n) ℝ ∂orthogonalHaar n, ‖U O‖ ≤ (1 : ℝ) from
        Filter.Eventually.of_forall fun O => entry_norm_bound_of_unitary O.property j0 j0)
  have hlin : (∫ O : Matrix.orthogonalGroup (Fin n) ℝ, (a * U O - b) * g O ∂orthogonalHaar n) =
      a * (∫ O, U O * g O ∂orthogonalHaar n) - b * (∫ O, g O ∂orthogonalHaar n) := by
    calc
      _ = ∫ O : Matrix.orthogonalGroup (Fin n) ℝ,
          a * (U O * g O) - b * g O ∂orthogonalHaar n := by
        apply integral_congr_ae
        exact Filter.Eventually.of_forall fun O => by ring
      _ = _ := by
        rw [integral_sub (hU.const_mul a) (hL1.const_mul b), integral_const_mul, integral_const_mul]
  rw [hstep, havg, hlin]
  have hn' : n - 1 + 1 = n := by omega
  have hp : (-b) ^ n = (-b) ^ (n - 1) * (-b) := by
    conv_lhs => rw [← hn', pow_succ]
  rw [hp]
  rw [neg_pow b (n - 1)]
  simp only [div_eq_mul_inv]
  ring


end AutoSamplingTheory.ExampleCases.GaussianComplexity.DeterminantCancellation
