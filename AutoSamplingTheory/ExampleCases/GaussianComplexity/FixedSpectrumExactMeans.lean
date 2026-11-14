import AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumGaussianMoments
import AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumCosineExpansion
import AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumGridAlias
import Mathlib.Analysis.SpecificLimits.Normed
import Mathlib.Tactic

/-!
# Actual exact finite-grid Gaussian means

Source: Zhou--Suzuki arXiv:2610.20492v1, Fact C.8. Internal providers
perform the signed alias reindexing, convergent geometric sums and scalar
finite-grid exchange. Only the sealed actual Gaussian Anchor receives a
public mathematical node. The private consumer derives actual mean bounds
and the normalized absolute bias. Source review and serialized publication
are separate from the local Lean proof.
-/

noncomputable section
open MeasureTheory ProbabilityTheory
open scoped BigOperators
open AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumGaussianMoments
open AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumCosineExpansion
open AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumGridAlias

namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumExactMeans


private def signedAlias (D : ℕ) (k : ℤ) : ℝ :=
  if (D : ℤ) ∣ k then (-1 : ℝ) ^ (k / (D : ℤ)) else 0

private theorem signedAlias_norm (D : ℕ) (k : ℤ) : ‖signedAlias D k‖ ≤ 1 := by
  unfold signedAlias
  split_ifs <;> simp

private theorem signedAlias_period {D : ℕ} (hD : 0 < D) (k : ℤ) :
    signedAlias D (k + D) = -signedAlias D k := by
  have hDne : (D : ℤ) ≠ 0 := by exact_mod_cast (Nat.ne_of_gt hD)
  have hdiv : (k + (D : ℤ)) / (D : ℤ) = k / (D : ℤ) + 1 := by
    simpa using Int.add_mul_ediv_right k 1 hDne
  have hdvd : ((D : ℤ) ∣ k + (D : ℤ)) ↔ (D : ℤ) ∣ k :=
    dvd_add_left (dvd_refl (D : ℤ))
  by_cases hk : (D : ℤ) ∣ k
  · simp only [signedAlias, hdvd, hk, if_true]
    rw [hdiv, zpow_add_one₀ (by norm_num : (-1 : ℝ) ≠ 0)]
    ring
  · simp [signedAlias, hdvd, hk]

private theorem summable_signedAlias (D : ℕ) {q : ℝ} (hq : ‖q‖ < 1) (c : ℤ) :
    Summable (fun j : ℕ => q ^ (j + 1) * signedAlias D (((j + 1 : ℕ) : ℤ) - c)) := by
  have hg : Summable (fun j : ℕ => ‖q‖ ^ (j + 1)) :=
    (summable_nat_add_iff 1).2 (summable_geometric_of_lt_one (norm_nonneg q) hq)
  have hbound (j : ℕ) :
      ‖q ^ (j + 1) * signedAlias D (((j + 1 : ℕ) : ℤ) - c)‖ ≤ ‖q‖ ^ (j + 1) := by
    rw [norm_mul, norm_pow]
    exact (mul_le_mul_of_nonneg_left (signedAlias_norm D _) (pow_nonneg (norm_nonneg _) _)).trans_eq (mul_one _)
  exact (Summable.of_nonneg_of_le (fun j => norm_nonneg _) hbound hg).of_norm

private theorem offset_alias_tsum {D c : ℕ} (hD : 0 < D) (hc : 1 ≤ c) (hcD : c ≤ D)
    {q : ℝ} (hq : ‖q‖ < 1) :
    (∑' j : ℕ, q ^ (j + 1) * signedAlias D (((j + 1 : ℕ) : ℤ) - (c : ℤ))) =
      q ^ c / (1 + q ^ D) := by
  classical
  let f : ℕ → ℝ := fun j => q ^ (j + 1) * signedAlias D (((j + 1 : ℕ) : ℤ) - (c : ℤ))
  let emb : ℕ → ℕ := fun a => D * a + (c - 1)
  have hDpos : (0 : ℤ) < D := by exact_mod_cast hD
  have hDne : (D : ℤ) ≠ 0 := ne_of_gt hDpos
  have hinj : Function.Injective emb := by
    intro a b h
    change D * a + (c - 1) = D * b + (c - 1) at h
    exact mul_left_cancel₀ (Nat.ne_of_gt hD) (Nat.add_right_cancel h)
  have hsupport : Function.support f ⊆ Set.range emb := by
    intro j hj
    change f j ≠ 0 at hj
    have hdiv : (D : ℤ) ∣ ((j + 1 : ℕ) : ℤ) - (c : ℤ) := by
      by_contra hn
      have ha0 : signedAlias D (((j + 1 : ℕ) : ℤ) - (c : ℤ)) = 0 := by
        simp only [signedAlias, if_neg hn]
      apply hj
      dsimp only [f]
      rw [ha0, mul_zero]
    obtain ⟨z, hz⟩ := hdiv
    have hz0 : 0 ≤ z := by
      by_contra hn
      have hzneg : z ≤ -1 := by omega
      have hm := mul_le_mul_of_nonneg_left hzneg hDpos.le
      have hcint : (c : ℤ) ≤ D := by exact_mod_cast hcD
      have hjint : (0 : ℤ) < ((j + 1 : ℕ) : ℤ) := by omega
      nlinarith
    have hcast : (((j + 1 : ℕ) : ℤ)) = (D : ℤ) * (z.toNat : ℤ) + (c : ℤ) := by
      rw [Int.toNat_of_nonneg hz0]
      linarith
    have hjnat : j + 1 = D * z.toNat + c := by exact_mod_cast hcast
    refine ⟨z.toNat, ?_⟩
    dsimp [emb]
    omega
  have hterm (a : ℕ) : f (emb a) = q ^ c * (-q ^ D) ^ a := by
    have he : emb a + 1 = D * a + c := by dsimp [emb]; omega
    have hcast : (((D * a + c : ℕ) : ℤ) - (c : ℤ)) = (D : ℤ) * (a : ℤ) := by
      push_cast
      ring
    have ha : signedAlias D ((D : ℤ) * (a : ℤ)) = (-1 : ℝ) ^ a := by
      unfold signedAlias
      rw [if_pos (dvd_mul_right _ _), Int.ediv_eq_of_eq_mul_right hDne rfl]
      simp
    dsimp only [f]
    rw [he, hcast, ha, pow_add, pow_mul, neg_pow]
    ring
  have hratio : ‖-q ^ D‖ < 1 := by
    rw [norm_neg, norm_pow]
    exact pow_lt_one₀ (norm_nonneg q) hq (Nat.ne_of_gt hD)
  have hgeom := summable_geometric_of_norm_lt_one hratio
  calc
    (∑' j : ℕ, f j) = ∑' a : ℕ, f (emb a) := (hinj.tsum_eq hsupport).symm
    _ = ∑' a : ℕ, q ^ c * (-q ^ D) ^ a := tsum_congr hterm
    _ = q ^ c * (∑' a : ℕ, (-q ^ D) ^ a) := hgeom.tsum_mul_left _
    _ = q ^ c / (1 + q ^ D) := by
      rw [tsum_geometric_of_norm_lt_one hratio, sub_neg_eq_add, div_eq_mul_inv]


private theorem inverse_grid_alias_series {d : ℕ} (hd : 2 ≤ d)
    {κ : ℝ} (hκ : 2 ≤ κ) (ℓ : ℤ) :
  let θ : Fin d → ℝ := fun i => ((i.val : ℝ) + 1 / 2) * Real.pi / (d : ℝ)
  let eigenvalue : Fin d → ℝ := fun i => (κ + 1) / 2 + (κ - 1) / 2 * Real.cos (θ i)
  let r : ℝ := (Real.sqrt κ - 1) / (Real.sqrt κ + 1)
  let a : ℤ → ℝ := signedAlias (2 * d)
  let F : ℕ → ℝ := fun j => (-r) ^ (j + 1) *
    (a (((j + 1 : ℕ) : ℤ) - ℓ) + a (((j + 1 : ℕ) : ℤ) + ℓ))
  Summable F →
  (∑ i : Fin d, Real.cos ((ℓ : ℝ) * θ i) / eigenvalue i) =
    ((d : ℝ) / Real.sqrt κ) * (a ℓ + ∑' j : ℕ, F j) := by
  classical
  let θ : Fin d → ℝ := fun i => ((i.val : ℝ) + 1 / 2) * Real.pi / (d : ℝ)
  let eigenvalue : Fin d → ℝ := fun i => (κ + 1) / 2 + (κ - 1) / 2 * Real.cos (θ i)
  let r : ℝ := (Real.sqrt κ - 1) / (Real.sqrt κ + 1)
  let a : ℤ → ℝ := signedAlias (2 * d)
  let w : Fin d → ℝ := fun i => Real.cos ((ℓ : ℝ) * θ i)
  let f : Fin d → ℕ → ℝ := fun i j =>
    (-r) ^ (j + 1) * Real.cos (((j + 1 : ℕ) : ℝ) * θ i)
  let g : Fin d → ℕ → ℝ := fun i j =>
    (-r) ^ (j + 1) * (w i * Real.cos (((j + 1 : ℕ) : ℝ) * θ i))
  let G : ℕ → ℝ := fun j => ∑ i : Fin d, g i j
  let F : ℕ → ℝ := fun j => (-r) ^ (j + 1) *
    (a (((j + 1 : ℕ) : ℤ) - ℓ) + a (((j + 1 : ℕ) : ℤ) + ℓ))
  change Summable F → (∑ i : Fin d, w i / eigenvalue i) =
    ((d : ℝ) / Real.sqrt κ) * (a ℓ + ∑' j : ℕ, F j)
  intro hF
  have heigenlower (i : Fin d) : 1 ≤ eigenvalue i := by
    dsimp [eigenvalue]
    have h := mul_nonneg (by linarith : 0 ≤ κ - 1)
      (by linarith [Real.neg_one_le_cos (θ i)] : 0 ≤ 1 + Real.cos (θ i))
    nlinarith
  have hcos (k : ℤ) : (∑ i : Fin d, Real.cos ((k : ℝ) * θ i)) = (d : ℝ) * a k := by
    simpa only [a, signedAlias, Nat.cast_mul, Nat.cast_ofNat] using
      actual_midpoint_grid_cosine_alias hd k
  obtain ⟨heq, habs, _⟩ := actual_inverse_spectrum_cosine_expansion hκ
  have hs (i : Fin d) : Summable (f i) := (habs (θ i)).of_norm
  have hmajor (i : Fin d) (j : ℕ) : ‖g i j‖ ≤ ‖f i j‖ := by
    have hw : ‖w i‖ ≤ 1 := by
      simpa only [w, Real.norm_eq_abs] using Real.abs_cos_le_one ((ℓ : ℝ) * θ i)
    calc
      ‖g i j‖ = ‖w i‖ * ‖f i j‖ := by
        rw [← norm_mul]
        congr 1
        dsimp [g, f]
        ring
      _ ≤ 1 * ‖f i j‖ := mul_le_mul_of_nonneg_right hw (norm_nonneg _)
      _ = _ := one_mul _
  have hsgnorm (i : Fin d) : Summable (fun j : ℕ => ‖g i j‖) :=
    Summable.of_nonneg_of_le (fun j => norm_nonneg _) (hmajor i) (habs (θ i))
  have hsg (i : Fin d) : Summable (g i) := (hsgnorm i).of_norm
  have hsumG : Summable G := summable_sum (fun i _ => hsg i)
  have hprod (j : ℕ) :
      2 * (∑ i : Fin d, w i * Real.cos (((j + 1 : ℕ) : ℝ) * θ i)) =
      (d : ℝ) * (a (((j + 1 : ℕ) : ℤ) - ℓ) +
        a (((j + 1 : ℕ) : ℤ) + ℓ)) := by
    have hp (i : Fin d) :
        2 * (w i * Real.cos (((j + 1 : ℕ) : ℝ) * θ i)) =
        Real.cos (((((j + 1 : ℕ) : ℤ) - ℓ : ℤ) : ℝ) * θ i) +
          Real.cos (((((j + 1 : ℕ) : ℤ) + ℓ : ℤ) : ℝ) * θ i) := by
      dsimp [w]
      push_cast
      simp only [sub_mul, add_mul, one_mul]
      have h := Real.two_mul_cos_mul_cos (((j : ℝ) + 1) * θ i) ((ℓ : ℝ) * θ i)
      simp only [add_mul, one_mul] at h
      nlinarith [h]
    calc
      _ = ∑ i : Fin d,
          (Real.cos (((((j + 1 : ℕ) : ℤ) - ℓ : ℤ) : ℝ) * θ i) +
            Real.cos (((((j + 1 : ℕ) : ℤ) + ℓ : ℤ) : ℝ) * θ i)) := by
        rw [Finset.mul_sum]
        exact Finset.sum_congr rfl (fun i _ => hp i)
      _ = _ := by rw [Finset.sum_add_distrib, hcos, hcos]; ring
  have hterm (j : ℕ) : 2 * G j = (d : ℝ) * F j := by
    dsimp [G, g, F]
    rw [← Finset.mul_sum]
    calc
      _ = (-r) ^ (j + 1) *
          (2 * ∑ i : Fin d, w i * Real.cos (((j + 1 : ℕ) : ℝ) * θ i)) := by ring
      _ = _ := by rw [hprod]; push_cast; ring
  have hseries : 2 * (∑' j : ℕ, G j) = (d : ℝ) * ∑' j : ℕ, F j := by
    rw [← hsumG.tsum_mul_left 2, ← hF.tsum_mul_left (d : ℝ)]
    exact tsum_congr hterm
  have hlin (i : Fin d) : (∑' j : ℕ, g i j) = w i * (∑' j : ℕ, f i j) := by
    calc
      _ = ∑' j : ℕ, w i * f i j := tsum_congr (fun j => by dsimp [g, f]; ring)
      _ = _ := (hs i).tsum_mul_left (w i)
  have heigen (i : Fin d) : (eigenvalue i)⁻¹ =
      (1 / Real.sqrt κ) * (1 + 2 * ∑' j : ℕ, f i j) := by
    have htwice : 2 * eigenvalue i = κ + 1 + (κ - 1) * Real.cos (θ i) := by
      dsimp [eigenvalue]
      ring
    have hrecip : (eigenvalue i)⁻¹ = 2 / (κ + 1 + (κ - 1) * Real.cos (θ i)) := by
      have hi0 : eigenvalue i ≠ 0 := ne_of_gt (lt_of_lt_of_le (by norm_num) (heigenlower i))
      rw [← htwice]
      field_simp [hi0]
    exact hrecip.trans (heq (θ i))
  have hscalar (i : Fin d) : w i / eigenvalue i =
      (1 / Real.sqrt κ) * (w i + 2 * ∑' j : ℕ, g i j) := by
    rw [div_eq_mul_inv, heigen, hlin]
    ring
  have hexchange : (∑' j : ℕ, G j) = ∑ i : Fin d, ∑' j : ℕ, g i j :=
    Summable.tsum_finsetSum (fun i _ => hsg i)
  calc
    _ = ∑ i : Fin d, (1 / Real.sqrt κ) * (w i + 2 * ∑' j : ℕ, g i j) :=
      Finset.sum_congr rfl (fun i _ => hscalar i)
    _ = (1 / Real.sqrt κ) * ((∑ i : Fin d, w i) +
        2 * (∑ i : Fin d, ∑' j : ℕ, g i j)) := by
      rw [← Finset.mul_sum, Finset.sum_add_distrib, ← Finset.mul_sum]
    _ = (1 / Real.sqrt κ) * ((∑ i : Fin d, w i) + 2 * (∑' j : ℕ, G j)) := by
      rw [hexchange]
    _ = _ := by
      have hb : (∑ i : Fin d, w i) = (d : ℝ) * a ℓ := hcos ℓ
      rw [hb, hseries]
      ring

private theorem unweighted_alias_tsum {D : ℕ} (hD : 0 < D) {q : ℝ} (hq : ‖q‖ < 1) :
    (∑' j : ℕ, q ^ (j + 1) * signedAlias D (((j + 1 : ℕ) : ℤ))) =
      -q ^ D / (1 + q ^ D) := by
  have hterm (j : ℕ) : q ^ (j + 1) * signedAlias D (((j + 1 : ℕ) : ℤ)) =
      -(q ^ (j + 1) * signedAlias D (((j + 1 : ℕ) : ℤ) - (D : ℤ))) := by
    have h := signedAlias_period hD (((j + 1 : ℕ) : ℤ) - (D : ℤ))
    rw [sub_add_cancel] at h
    rw [h]
    ring
  calc
    _ = ∑' j : ℕ, -(q ^ (j + 1) * signedAlias D (((j + 1 : ℕ) : ℤ) - (D : ℤ))) :=
      tsum_congr hterm
    _ = -(∑' j : ℕ, q ^ (j + 1) * signedAlias D (((j + 1 : ℕ) : ℤ) - (D : ℤ))) := tsum_neg
    _ = _ := by
      rw [offset_alias_tsum hD (by omega : 1 ≤ D) (le_refl D) hq]
      ring

private theorem plus_alias_tsum {D n : ℕ} (hD : 0 < D) (hnD : n < D)
    {q : ℝ} (hq : ‖q‖ < 1) :
    (∑' j : ℕ, q ^ (j + 1) * signedAlias D (((j + 1 : ℕ) : ℤ) + (n : ℤ))) =
      -q ^ (D - n) / (1 + q ^ D) := by
  have hc : 1 ≤ D - n := by omega
  have hcD : D - n ≤ D := Nat.sub_le _ _
  have hterm (j : ℕ) : q ^ (j + 1) * signedAlias D (((j + 1 : ℕ) : ℤ) + (n : ℤ)) =
      -(q ^ (j + 1) * signedAlias D (((j + 1 : ℕ) : ℤ) - ((D - n : ℕ) : ℤ))) := by
    have h := signedAlias_period hD (((j + 1 : ℕ) : ℤ) - ((D - n : ℕ) : ℤ))
    have hindex : (((j + 1 : ℕ) : ℤ) - ((D - n : ℕ) : ℤ)) + (D : ℤ) =
        ((j + 1 : ℕ) : ℤ) + (n : ℤ) := by
      rw [Nat.cast_sub hnD.le]
      ring
    rw [hindex] at h
    rw [h]
    ring
  calc
    _ = ∑' j : ℕ, -(q ^ (j + 1) * signedAlias D (((j + 1 : ℕ) : ℤ) - ((D - n : ℕ) : ℤ))) :=
      tsum_congr hterm
    _ = -(∑' j : ℕ, q ^ (j + 1) * signedAlias D (((j + 1 : ℕ) : ℤ) - ((D - n : ℕ) : ℤ))) := tsum_neg
    _ = _ := by rw [offset_alias_tsum hD hc hcD hq]; ring

private theorem weighted_alias_summable {D n : ℕ} (hn : 1 ≤ n) (hgap : 2 * n < D)
    {q : ℝ} (hq : ‖q‖ < 1) :
    Summable (fun j : ℕ => q ^ (j + 1) *
      (signedAlias D (((j + 1 : ℕ) : ℤ) - (n : ℤ)) +
        signedAlias D (((j + 1 : ℕ) : ℤ) + (n : ℤ)))) := by
  have hdisjoint (j : ℕ) : ¬ ((D : ℤ) ∣ ((j + 1 : ℕ) : ℤ) - (n : ℤ)) ∨
      ¬ ((D : ℤ) ∣ ((j + 1 : ℕ) : ℤ) + (n : ℤ)) := by
    by_contra h
    push Not at h
    have hdiv : (D : ℤ) ∣ 2 * (n : ℤ) := by
      have hh := dvd_sub h.2 h.1
      have he : ((((j + 1 : ℕ) : ℤ) + (n : ℤ)) -
          (((j + 1 : ℕ) : ℤ) - (n : ℤ))) = 2 * (n : ℤ) := by ring
      rw [he] at hh
      exact hh
    have hle := Int.le_of_dvd (by omega : (0 : ℤ) < 2 * (n : ℤ)) hdiv
    have hgapint : 2 * (n : ℤ) < (D : ℤ) := by exact_mod_cast hgap
    omega
  have hcoef (j : ℕ) :
      ‖signedAlias D (((j + 1 : ℕ) : ℤ) - (n : ℤ)) +
        signedAlias D (((j + 1 : ℕ) : ℤ) + (n : ℤ))‖ ≤ 1 := by
    rcases hdisjoint j with hm | hp
    · have hz : signedAlias D (((j + 1 : ℕ) : ℤ) - (n : ℤ)) = 0 := by
        simp only [signedAlias, if_neg hm]
      rw [hz, zero_add]
      exact signedAlias_norm _ _
    · have hz : signedAlias D (((j + 1 : ℕ) : ℤ) + (n : ℤ)) = 0 := by
        simp only [signedAlias, if_neg hp]
      rw [hz, add_zero]
      exact signedAlias_norm _ _
  have hg : Summable (fun j : ℕ => ‖q‖ ^ (j + 1)) :=
    (summable_nat_add_iff 1).2 (summable_geometric_of_lt_one (norm_nonneg q) hq)
  have hbound (j : ℕ) :
      ‖q ^ (j + 1) * (signedAlias D (((j + 1 : ℕ) : ℤ) - (n : ℤ)) +
        signedAlias D (((j + 1 : ℕ) : ℤ) + (n : ℤ)))‖ ≤ ‖q‖ ^ (j + 1) := by
    rw [norm_mul, norm_pow]
    exact (mul_le_mul_of_nonneg_left (hcoef j) (pow_nonneg (norm_nonneg _) _)).trans_eq (mul_one _)
  exact (Summable.of_nonneg_of_le (fun j => norm_nonneg _) hbound hg).of_norm

private theorem weighted_alias_tsum {D n : ℕ} (hD : 0 < D) (hn : 1 ≤ n) (hnD : n < D)
    {q : ℝ} (hq : ‖q‖ < 1) :
    (∑' j : ℕ, q ^ (j + 1) *
      (signedAlias D (((j + 1 : ℕ) : ℤ) - (n : ℤ)) +
        signedAlias D (((j + 1 : ℕ) : ℤ) + (n : ℤ)))) =
      (q ^ n - q ^ (D - n)) / (1 + q ^ D) := by
  have hm := summable_signedAlias D hq (n : ℤ)
  have hp : Summable (fun j : ℕ => q ^ (j + 1) *
      signedAlias D (((j + 1 : ℕ) : ℤ) + (n : ℤ))) := by
    simpa only [sub_neg_eq_add] using summable_signedAlias D hq (-(n : ℤ))
  calc
    _ = (∑' j : ℕ, q ^ (j + 1) * signedAlias D (((j + 1 : ℕ) : ℤ) - (n : ℤ))) +
        (∑' j : ℕ, q ^ (j + 1) * signedAlias D (((j + 1 : ℕ) : ℤ) + (n : ℤ))) := by
      rw [← hm.tsum_add hp]
      exact tsum_congr (fun j => mul_add _ _ _)
    _ = _ := by
      rw [offset_alias_tsum hD hn hnD.le hq, plus_alias_tsum hD hnD hq]
      ring


theorem actual_diagonal_gaussian_exact_means {d : ℕ} (hd : 2 ≤ d) {κ : ℝ} (hκ : 2 ≤ κ)
    (n : ℕ) (hn : 1 ≤ n) (hnd : n < d) :
  let θ : Fin d → ℝ := fun i => ((i.val : ℝ) + 1 / 2) * Real.pi / (d : ℝ)
  let eigenvalue : Fin d → ℝ := fun i => (κ + 1) / 2 + (κ - 1) / 2 * Real.cos (θ i)
  let Λ : Matrix (Fin d) (Fin d) ℝ := Matrix.diagonal eigenvalue
  let μ : Measure (EuclideanSpace ℝ (Fin d)) :=
    multivariateGaussian (0 : EuclideanSpace ℝ (Fin d)) Λ⁻¹
  let Q : EuclideanSpace ℝ (Fin d) → ℝ := fun x =>
    ∑ i : Fin d, Real.cos ((n : ℝ) * θ i) * (WithLp.ofLp x i) ^ 2
  let r : ℝ := (Real.sqrt κ - 1) / (Real.sqrt κ + 1)
  Integrable (fun x : EuclideanSpace ℝ (Fin d) => ‖x‖ ^ 2) μ ∧
  Integrable Q μ ∧
  (∫ x : EuclideanSpace ℝ (Fin d), ‖x‖ ^ 2 ∂μ) =
    ((d : ℝ) / Real.sqrt κ) * ((1 - r ^ (2 * d)) / (1 + r ^ (2 * d))) ∧
  (-1 : ℝ) ^ n * (∫ x : EuclideanSpace ℝ (Fin d), Q x ∂μ) =
    ((d : ℝ) / Real.sqrt κ) * ((r ^ n - r ^ (2 * d - n)) / (1 + r ^ (2 * d))) := by
  classical
  let θ : Fin d → ℝ := fun i => ((i.val : ℝ) + 1 / 2) * Real.pi / (d : ℝ)
  let eigenvalue : Fin d → ℝ := fun i => (κ + 1) / 2 + (κ - 1) / 2 * Real.cos (θ i)
  let Λ : Matrix (Fin d) (Fin d) ℝ := Matrix.diagonal eigenvalue
  let μ : Measure (EuclideanSpace ℝ (Fin d)) := multivariateGaussian 0 Λ⁻¹
  let Q : EuclideanSpace ℝ (Fin d) → ℝ := fun x =>
    ∑ i : Fin d, Real.cos ((n : ℝ) * θ i) * (WithLp.ofLp x i) ^ 2
  let r : ℝ := (Real.sqrt κ - 1) / (Real.sqrt κ + 1)
  let a : ℤ → ℝ := signedAlias (2 * d)
  change Integrable (fun x : EuclideanSpace ℝ (Fin d) => ‖x‖ ^ 2) μ ∧
    Integrable Q μ ∧
    (∫ x : EuclideanSpace ℝ (Fin d), ‖x‖ ^ 2 ∂μ) =
      ((d : ℝ) / Real.sqrt κ) * ((1 - r ^ (2 * d)) / (1 + r ^ (2 * d))) ∧
    (-1 : ℝ) ^ n * (∫ x : EuclideanSpace ℝ (Fin d), Q x ∂μ) =
      ((d : ℝ) / Real.sqrt κ) * ((r ^ n - r ^ (2 * d - n)) / (1 + r ^ (2 * d)))
  have hactual := actual_diagonal_gaussian_quadratic_means hd hκ n hn hnd
  change Integrable (fun x : EuclideanSpace ℝ (Fin d) => ‖x‖ ^ 2) μ ∧
    Integrable Q μ ∧
    (∫ x : EuclideanSpace ℝ (Fin d), ‖x‖ ^ 2 ∂μ) = (∑ i : Fin d, (eigenvalue i)⁻¹) ∧
    (∫ x : EuclideanSpace ℝ (Fin d), Q x ∂μ) =
      ∑ i : Fin d, Real.cos ((n : ℝ) * θ i) / eigenvalue i at hactual
  have hsqrt : 1 < Real.sqrt κ := by
    nlinarith [Real.sqrt_nonneg κ, Real.sq_sqrt (by linarith : 0 ≤ κ)]
  have hr0 : 0 < r := div_pos (by linarith) (by linarith)
  have hr1 : r < 1 := by
    dsimp [r]
    apply (div_lt_one (by linarith : 0 < Real.sqrt κ + 1)).2
    linarith
  have hq : ‖-r‖ < 1 := by simpa [Real.norm_eq_abs, abs_of_pos hr0] using hr1
  have hD : 0 < 2 * d := by omega
  have hnD : n < 2 * d := by omega
  have hqD : (-r) ^ (2 * d) = r ^ (2 * d) := by simp only [pow_mul, neg_sq]
  have hden : 1 + r ^ (2 * d) ≠ 0 := ne_of_gt (by positivity)
  have ha0 : a 0 = 1 := by simp [a, signedAlias]
  have han : a (n : ℤ) = 0 := by
    have hnot : ¬ (2 * d : ℤ) ∣ (n : ℤ) := by
      intro h
      have hle := Int.le_of_dvd (by omega : (0 : ℤ) < n) h
      have hlt : (n : ℤ) < (2 * d : ℤ) := by exact_mod_cast hnD
      omega
    simp only [a, signedAlias, Nat.cast_mul, Nat.cast_ofNat, if_neg hnot]
  have hsA : Summable (fun j : ℕ => (-r) ^ (j + 1) * a ((j + 1 : ℕ) : ℤ)) := by
    simpa only [sub_zero] using summable_signedAlias (2 * d) hq 0
  have hs0 : Summable (fun j : ℕ => (-r) ^ (j + 1) *
      (a (((j + 1 : ℕ) : ℤ) - 0) + a (((j + 1 : ℕ) : ℤ) + 0))) := by
    simpa only [sub_zero, add_zero, mul_add] using hsA.add hsA
  have ht0 : (∑' j : ℕ, (-r) ^ (j + 1) *
      (a (((j + 1 : ℕ) : ℤ) - 0) + a (((j + 1 : ℕ) : ℤ) + 0))) =
      2 * (-r ^ (2 * d) / (1 + r ^ (2 * d))) := by
    calc
      _ = ∑' j : ℕ, 2 * ((-r) ^ (j + 1) * a ((j + 1 : ℕ) : ℤ)) :=
        tsum_congr (fun j => by simp only [sub_zero, add_zero]; ring)
      _ = 2 * (∑' j : ℕ, (-r) ^ (j + 1) * a ((j + 1 : ℕ) : ℤ)) := hsA.tsum_mul_left 2
      _ = _ := by rw [unweighted_alias_tsum hD hq, hqD]
  have hgrid0 := inverse_grid_alias_series hd hκ 0 hs0
  change (∑ i : Fin d, Real.cos ((0 : ℤ) * θ i) / eigenvalue i) =
    ((d : ℝ) / Real.sqrt κ) * (a 0 + ∑' j : ℕ, (-r) ^ (j + 1) *
      (a (((j + 1 : ℕ) : ℤ) - 0) + a (((j + 1 : ℕ) : ℤ) + 0))) at hgrid0
  simp only [Int.cast_zero, zero_mul, Real.cos_zero, one_div, ha0, ht0] at hgrid0
  have hsN := weighted_alias_summable hn (by omega : 2 * n < 2 * d) hq
  have htN := weighted_alias_tsum hD hn hnD hq
  have hgridN := inverse_grid_alias_series hd hκ (n : ℤ) hsN
  change (∑ i : Fin d, Real.cos ((n : ℝ) * θ i) / eigenvalue i) =
    ((d : ℝ) / Real.sqrt κ) * (a (n : ℤ) + ∑' j : ℕ, (-r) ^ (j + 1) *
      (a (((j + 1 : ℕ) : ℤ) - (n : ℤ)) + a (((j + 1 : ℕ) : ℤ) + (n : ℤ)))) at hgridN
  rw [han, zero_add, htN, hqD] at hgridN
  have hsignsq : (-1 : ℝ) ^ n * (-1 : ℝ) ^ n = 1 := by
    rw [← mul_pow]
    norm_num
  have hparity : (-1 : ℝ) ^ (2 * d - n) = (-1 : ℝ) ^ n := by
    apply mul_left_cancel₀ (pow_ne_zero n (by norm_num : (-1 : ℝ) ≠ 0))
    rw [← pow_add, Nat.add_sub_of_le hnD.le, hsignsq]
    simp [pow_mul]
  refine ⟨hactual.1, hactual.2.1, ?_, ?_⟩
  · rw [hactual.2.2.1, hgrid0]
    field_simp [hden]
    ring
  · rw [hactual.2.2.2, hgridN, neg_pow r n, neg_pow r (2 * d - n), hparity]
    have hcancel (u : ℝ) : (-1 : ℝ) ^ n * ((-1 : ℝ) ^ n * u) = u := by
      rw [← mul_assoc, hsignsq, one_mul]
    calc
      _ = ((d : ℝ) / Real.sqrt κ) *
          (((-1 : ℝ) ^ n * ((-1 : ℝ) ^ n * (r ^ n - r ^ (2 * d - n)))) /
            (1 + r ^ (2 * d))) := by ring
      _ = _ := by rw [hcancel]

end AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumExactMeans
