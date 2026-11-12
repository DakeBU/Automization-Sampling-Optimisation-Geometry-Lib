import Mathlib.Analysis.InnerProductSpace.Calculus
import Mathlib.Analysis.InnerProductSpace.PiL2
import Mathlib.Algebra.BigOperators.Fin
import Mathlib.Data.Fin.Rev
import AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Gradient
import AutoSamplingTheory.TechnicalLemmas.Analysis.StrongConvexGradientConverse
import Mathlib.Tactic

/-!
# A distance lower bound for gradient-span iterates

This module verifies the specific finite path quadratic in Chewi's
*Lectures on Optimization*, arXiv:2605.07006v1, Exercise 4.1. The quadratic
is fixed before the run. Only the explicit distance comparison is claimed;
this is not the objective-value lower bound or an unrestricted oracle bound.
-/

namespace AutoSamplingTheory.ExampleCases.LowerBounds.GradientSpanDistance

open AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Gradient
open AutoSamplingTheory.TechnicalLemmas.Analysis.StrongConvexGradientConverse
open Finset

private abbrev Point (d : ℕ) := EuclideanSpace ℝ (Fin d)

private def endpoints {d : ℕ} (x : Point d) : Fin (d + 2) → ℝ :=
  Fin.cons 1 (Fin.snoc x 0)

private def edge {d : ℕ} (v : Fin (d + 2) → ℝ) (i : Fin (d + 1)) : ℝ :=
  v i.castSucc - v i.succ

private noncomputable def objective {d : ℕ} (β : ℝ) (x : Point d) : ℝ :=
  (β / 8) * ((∑ i, (edge (endpoints x) i) ^ 2) - 1)

private noncomputable def affineProfile (d : ℕ) : Point d :=
  WithLp.toLp 2 (fun i : Fin d => ((d : ℝ) - (i.val : ℝ)) / ((d : ℝ) + 1))

private theorem endpoints_inner {d : ℕ} (x : Point d) (j : Fin d) :
    endpoints x j.castSucc.succ = x j := by
  simp only [endpoints, Fin.cons_succ, Fin.snoc_castSucc]

private theorem endpoints_left {d : ℕ} (x : Point d) : endpoints x 0 = 1 := rfl

private theorem endpoints_right {d : ℕ} (x : Point d) :
    endpoints x (Fin.last d).succ = 0 := by
  simp [endpoints]

private theorem objective_eq_expanded {d : ℕ} (β : ℝ) (x : Point (d + 1)) :
    objective β x =
      (β / 4) * (((x 0) ^ 2 + (∑ i : Fin d, (x i.castSucc - x i.succ) ^ 2)
          + (x (Fin.last d)) ^ 2) / 2 - x 0) := by
  have h₀ : edge (endpoints x) 0 = 1 - x 0 := by
    change endpoints x (0 : Fin (d + 2)).castSucc -
      endpoints x (0 : Fin (d + 2)).succ = _
    rw [show (0 : Fin (d + 2)).castSucc = 0 by rfl,
        show (0 : Fin (d + 2)).succ = (0 : Fin (d + 1)).castSucc.succ by rfl,
        endpoints_left, endpoints_inner]
  have hi (i : Fin d) : edge (endpoints x) i.castSucc.succ = x i.castSucc - x i.succ := by
    unfold edge
    rw [show i.castSucc.succ.castSucc = i.castSucc.castSucc.succ from Fin.ext (by simp),
        show i.castSucc.succ.succ = i.succ.castSucc.succ from Fin.ext (by simp),
        endpoints_inner, endpoints_inner]
  have hlast : edge (endpoints x) (Fin.last d).succ = x (Fin.last d) := by
    unfold edge
    rw [show (Fin.last d).succ.castSucc = (Fin.last d).castSucc.succ from Fin.ext (by simp),
        show (Fin.last d).succ.succ = (Fin.last (d + 1)).succ from Fin.ext (by simp),
        endpoints_inner, endpoints_right, sub_zero]
  rw [objective, Fin.sum_univ_succ (fun i : Fin (d + 2) => (edge (endpoints x) i) ^ 2),
    Fin.sum_univ_castSucc (fun i : Fin (d + 1) => (edge (endpoints x) i.succ) ^ 2)]
  simp only [h₀, hi, hlast]
  ring

private theorem sum_edge {d : ℕ} (v : Fin (d + 2) → ℝ) :
    ∑ i, edge v i = v 0 - v (Fin.last (d + 1)) := by
  simp only [edge, Finset.sum_sub_distrib]
  have h₁ := Fin.sum_univ_castSucc v
  have h₂ := Fin.sum_univ_succ v
  linarith only [h₁, h₂]

private theorem sum_edge_endpoints {d : ℕ} (x : Point d) :
    ∑ i, edge (endpoints x) i = 1 := by
  rw [sum_edge]
  have hlast : Fin.last (d + 1) = (Fin.last d).succ := Fin.ext (by simp)
  rw [hlast]
  simp [endpoints]

private theorem endpoints_affineProfile {d : ℕ} (i : Fin (d + 2)) :
    endpoints (affineProfile d) i = ((d : ℝ) + 1 - (i.val : ℝ)) / ((d : ℝ) + 1) := by
  have hD : (d : ℝ) + 1 ≠ 0 := by positivity
  refine Fin.cases ?_ (fun j => ?_) i
  · simp [endpoints, hD]
  · rw [endpoints, Fin.cons_succ]
    refine Fin.lastCases ?_ (fun k => ?_) j
    · simp [Fin.snoc_last, Nat.cast_succ]
    · rw [Fin.snoc_castSucc]
      change ((d : ℝ) - (k.val : ℝ)) / ((d : ℝ) + 1) =
        ((d : ℝ) + 1 - (((k.castSucc.succ).val : ℕ) : ℝ)) / ((d : ℝ) + 1)
      simp only [Fin.val_succ, Fin.val_castSucc, Nat.cast_succ]
      ring

private theorem edge_affineProfile {d : ℕ} (i : Fin (d + 1)) :
    edge (endpoints (affineProfile d)) i = 1 / ((d : ℝ) + 1) := by
  simp only [edge, endpoints_affineProfile, Fin.val_succ, Fin.val_castSucc, Nat.cast_succ]
  ring

private theorem objective_sub_affineProfile {d : ℕ} (β : ℝ) (x : Point d) :
    objective β x - objective β (affineProfile d) =
      (β / 8) * ∑ i, (edge (endpoints x) i - edge (endpoints (affineProfile d)) i) ^ 2 := by
  let c : ℝ := 1 / ((d : ℝ) + 1)
  let u : Fin (d + 1) → ℝ := edge (endpoints x)
  let v : Fin (d + 1) → ℝ := edge (endpoints (affineProfile d))
  have hsum : ∑ i, (u i - v i) = 0 := by
    rw [Finset.sum_sub_distrib]
    change (∑ i, edge (endpoints x) i) - (∑ i, edge (endpoints (affineProfile d)) i) = 0
    rw [sum_edge_endpoints, sum_edge_endpoints, sub_self]
  have hexpand : (∑ i, u i ^ 2) =
      ∑ i, (v i ^ 2 + (u i - v i) ^ 2 + (2 * c) * (u i - v i)) := by
    apply Finset.sum_congr rfl
    intro i _
    have hi : v i = c := edge_affineProfile i
    rw [hi]
    ring
  simp only [Finset.sum_add_distrib, ← Finset.mul_sum, hsum, mul_zero, add_zero] at hexpand
  change (β / 8) * ((∑ i, u i ^ 2) - 1) - (β / 8) * ((∑ i, v i ^ 2) - 1) =
    (β / 8) * ∑ i, (u i - v i) ^ 2
  rw [hexpand]
  ring

private theorem isMinOn_affineProfile {d : ℕ} {β : ℝ} (hβ : 0 ≤ β) :
    IsMinOn (objective (d := d) β) Set.univ (affineProfile d) := by
  intro x _
  change objective β (affineProfile d) ≤ objective β x
  apply sub_nonneg.mp
  rw [objective_sub_affineProfile]
  exact mul_nonneg (by positivity) (Finset.sum_nonneg fun _ _ => sq_nonneg _)

private noncomputable def paddedLin {d : ℕ} (i : Fin (d + 2)) : Point d →L[ℝ] ℝ :=
  Fin.cons (α := fun _ => Point d →L[ℝ] ℝ) 0
    (Fin.snoc (α := fun _ => Point d →L[ℝ] ℝ) (fun j : Fin d => EuclideanSpace.proj j) 0) i

private noncomputable def edgeLin {d : ℕ} (i : Fin (d + 1)) : Point d →L[ℝ] ℝ :=
  paddedLin i.castSucc - paddedLin i.succ

private theorem endpoints_add_paddedLin {d : ℕ} (x y : Point d) (i : Fin (d + 2)) :
    endpoints (x + y) i = endpoints x i + paddedLin i y := by
  refine Fin.cases ?_ (fun j => ?_) i
  · simp [endpoints, paddedLin]
  · simp only [endpoints, paddedLin, Fin.cons_succ]
    refine Fin.lastCases ?_ (fun k => ?_) j
    · simp
    · simp only [Fin.snoc_castSucc]
      rfl

private theorem hasFDerivAt_endpoints {d : ℕ} (x : Point d) (i : Fin (d + 2)) :
    HasFDerivAt (fun y => endpoints y i) (paddedLin i) x := by
  have h : HasFDerivAt (fun y => endpoints (0 : Point d) i + paddedLin i y) (paddedLin i) x := by
    exact (hasFDerivAt_const_add_iff (endpoints (0 : Point d) i)).2 (paddedLin i).hasFDerivAt
  convert h using 1
  funext y
  simpa only [zero_add] using endpoints_add_paddedLin (0 : Point d) y i

private theorem hasFDerivAt_edge {d : ℕ} (x : Point d) (i : Fin (d + 1)) :
    HasFDerivAt (fun y => edge (endpoints y) i) (edgeLin i) x :=
  (hasFDerivAt_endpoints x i.castSucc).sub (hasFDerivAt_endpoints x i.succ)

private theorem hasFDerivAt_objective {d : ℕ} (β : ℝ) (x : Point d) :
    HasFDerivAt (objective β)
      ((β / 8) • ∑ i, ((2 : ℝ) * edge (endpoints x) i) • edgeLin i) x := by
  have h (i : Fin (d + 1)) :
      HasFDerivAt (fun y => edge (endpoints y) i ^ 2)
        (((2 : ℝ) * edge (endpoints x) i) • edgeLin i) x := by
    simpa [two_nsmul, two_mul] using (hasFDerivAt_edge x i).pow 2
  have hs := HasFDerivAt.fun_sum (u := Finset.univ) fun i _ => h i
  exact (hs.sub_const (1 : ℝ)).const_mul (β / 8)

private theorem fderiv_objective_apply {d : ℕ} (β : ℝ) (x y : Point d) :
    fderiv ℝ (objective β) x y =
      (β / 4) * ∑ i, edge (endpoints x) i * edgeLin i y := by
  rw [(hasFDerivAt_objective β x).fderiv]
  simp only [smul_apply, _root_.sum_apply, smul_eq_mul]
  simp_rw [mul_assoc]
  rw [← Finset.mul_sum]
  ring

private theorem paddedLin_zero {d : ℕ} (y : Point d) :
    paddedLin (d := d) (0 : Fin (d + 1)).castSucc y = 0 := by
  change paddedLin (0 : Fin (d + 2)) y = 0
  simp [paddedLin]

private theorem paddedLin_last {d : ℕ} (y : Point d) :
    paddedLin (Fin.last d).succ y = 0 := by
  simp [paddedLin]

private theorem paddedLin_middle {d : ℕ} (y : Point d) (j : Fin d) :
    paddedLin j.castSucc.succ y = y j := by
  simp only [paddedLin, Fin.cons_succ, Fin.snoc_castSucc]
  rfl

private theorem paddedLin_middle' {d : ℕ} (y : Point d) (j : Fin d) :
    paddedLin j.succ.castSucc y = y j := by
  rw [show j.succ.castSucc = j.castSucc.succ from Fin.ext (by simp), paddedLin_middle]

private theorem sum_edgeLin_mul {d : ℕ} (a : Fin (d + 1) → ℝ) (y : Point d) :
    (∑ i, a i * edgeLin i y) =
      ∑ j : Fin d, (a j.succ - a j.castSucc) * y j := by
  simp only [edgeLin, sub_apply, mul_sub, Finset.sum_sub_distrib]
  rw [Fin.sum_univ_succ (fun i : Fin (d + 1) => a i * paddedLin i.castSucc y),
      Fin.sum_univ_castSucc (fun i : Fin (d + 1) => a i * paddedLin i.succ y)]
  simp only [paddedLin_zero, paddedLin_last, paddedLin_middle, paddedLin_middle', mul_zero,
    zero_add, add_zero, sub_mul, Finset.sum_sub_distrib]

private theorem gradient_objective_coordinate {d : ℕ} (β : ℝ) (x : Point d) (j : Fin d) :
    gradient (objective β) x j =
      (β / 4) * (edge (endpoints x) j.succ - edge (endpoints x) j.castSucc) := by
  rw [← fderiv_apply_coordinate_eq_gradient_coordinate_of_differentiableAt
    j (hasFDerivAt_objective β x).differentiableAt, fderiv_objective_apply, sum_edgeLin_mul]
  simp [mul_ite]

private theorem edge_add_dir {d : ℕ} (x y : Point d) (i : Fin (d + 1)) :
    edge (endpoints (x + y)) i = edge (endpoints x) i + edgeLin i y := by
  simp only [edge, endpoints_add_paddedLin, edgeLin, sub_apply]
  ring

private theorem edgeEnergy_le {d : ℕ} (y : Point d) :
    ∑ i, (edgeLin i y) ^ 2 ≤ 4 * ‖y‖ ^ 2 := by
  have hL : ∑ i : Fin (d + 1), (paddedLin i.castSucc y) ^ 2 = ‖y‖ ^ 2 := by
    rw [Fin.sum_univ_succ (fun i : Fin (d + 1) => (paddedLin i.castSucc y) ^ 2),
      EuclideanSpace.real_norm_sq_eq]
    simp only [paddedLin_zero, paddedLin_middle', zero_pow (by decide : (2 : ℕ) ≠ 0), zero_add]
  have hR : ∑ i : Fin (d + 1), (paddedLin i.succ y) ^ 2 = ‖y‖ ^ 2 := by
    rw [Fin.sum_univ_castSucc (fun i : Fin (d + 1) => (paddedLin i.succ y) ^ 2),
      EuclideanSpace.real_norm_sq_eq]
    simp only [paddedLin_last, paddedLin_middle, zero_pow (by decide : (2 : ℕ) ≠ 0), add_zero]
  calc
    _ ≤ ∑ i : Fin (d + 1), (2 * (paddedLin i.castSucc y) ^ 2 + 2 * (paddedLin i.succ y) ^ 2) := by
      apply Finset.sum_le_sum
      intro i _
      simp only [edgeLin, sub_apply]
      nlinarith [sq_nonneg (paddedLin i.castSucc y + paddedLin i.succ y)]
    _ = _ := by
      rw [Finset.sum_add_distrib, ← Finset.mul_sum, ← Finset.mul_sum, hL, hR]
      ring

private theorem objective_remainder {d : ℕ} (β : ℝ) (x y : Point d) :
    objective β y - objective β x - fderiv ℝ (objective β) x (y - x) =
      (β / 8) * ∑ i, (edgeLin i (y - x)) ^ 2 := by
  let a : Fin (d + 1) → ℝ := edge (endpoints x)
  let b : Fin (d + 1) → ℝ := fun i => edgeLin i (y - x)
  have hexpand : ∑ i, (edge (endpoints y) i) ^ 2 =
      ∑ i, (a i ^ 2 + 2 * (a i * b i) + b i ^ 2) := by
    apply Finset.sum_congr rfl
    intro i _
    have h : edge (endpoints y) i = a i + b i := by
      have hy : x + (y - x) = y := by abel
      simpa only [a, b, hy] using edge_add_dir x (y - x) i
    rw [h]
    ring
  rw [fderiv_objective_apply]
  change β / 8 * ((∑ i, (edge (endpoints y) i) ^ 2) - 1) -
      β / 8 * ((∑ i, a i ^ 2) - 1) - β / 4 * (∑ i, a i * b i) =
      β / 8 * ∑ i, b i ^ 2
  rw [hexpand, Finset.sum_add_distrib, Finset.sum_add_distrib, ← Finset.mul_sum]
  ring

private theorem contDiff_objective {d : ℕ} (β : ℝ) : ContDiff ℝ 1 (objective (d := d) β) := by
  refine contDiff_one_iff_hasFDerivAt.mpr ⟨_, ?_, hasFDerivAt_objective β⟩
  have h (i : Fin (d + 1)) : Continuous (fun x : Point d => edge (endpoints x) i) :=
    continuous_iff_continuousAt.mpr (fun x => (hasFDerivAt_edge x i).continuousAt)
  exact (continuous_finsetSum Finset.univ (fun i _ =>
    (continuous_const.mul (h i)).smul (continuous_const (y := edgeLin i)))).const_smul (β / 8)

private theorem convexOn_objective {d : ℕ} {β : ℝ} (hβ : 0 ≤ β) :
    ConvexOn ℝ Set.univ (objective (d := d) β) := by
  apply strongConvexOn_zero.mp
  refine strongConvexOn_of_gradient_inner_lower_bound
      convex_univ (fun x _ => (hasFDerivAt_objective β x).differentiableAt.hasGradientAt) ?_
  intro x _ y _
  rw [zero_mul, inner_sub_left,
    ← fderiv_apply_eq_inner_gradient_of_differentiableAt (hasFDerivAt_objective β y).differentiableAt,
    ← fderiv_apply_eq_inner_gradient_of_differentiableAt (hasFDerivAt_objective β x).differentiableAt]
  have hrem (x y : Point d) :
      0 ≤ objective β y - objective β x - fderiv ℝ (objective β) x (y - x) := by
    rw [objective_remainder]
    exact mul_nonneg (by positivity) (Finset.sum_nonneg fun _ _ => sq_nonneg _)
  have h := hrem y x
  rw [show x - y = -(y - x) by abel, map_neg] at h
  linarith [hrem x y]

private def prefixSubmodule (d n : ℕ) : Submodule ℝ (Point d) where
  carrier := {x | ∀ i : Fin d, n ≤ i.val → x i = 0}
  zero_mem' := by intro i _; rfl
  add_mem' := by
    intro x y hx hy i hi
    change x i + y i = 0
    rw [hx i hi, hy i hi, add_zero]
  smul_mem' := by
    intro c x hx i hi
    change c * x i = 0
    rw [hx i hi, mul_zero]

private theorem prefix_mono {d m n : ℕ} (hmn : m ≤ n) :
    prefixSubmodule d m ≤ prefixSubmodule d n := by
  intro x hx i hi
  exact hx i (hmn.trans hi)

private theorem endpoints_eq_zero_of_index {d n : ℕ} {x : Point d}
    (hx : x ∈ prefixSubmodule d n) (i : Fin (d + 2)) (hi : n + 1 ≤ i.val) :
    endpoints x i = 0 := by
  revert hi
  refine Fin.cases ?_ (fun j => ?_) i
  · simp
  · refine Fin.lastCases ?_ (fun k => ?_) j
    · simp [endpoints]
    · intro h
      simp only [endpoints, Fin.cons_succ, Fin.snoc_castSucc]
      apply hx
      simp only [Fin.val_succ, Fin.val_castSucc] at h
      omega

private theorem gradient_mem_prefix_succ {d n : ℕ} (β : ℝ) {x : Point d}
    (hx : x ∈ prefixSubmodule d n) :
    gradient (objective β) x ∈ prefixSubmodule d (n + 1) := by
  intro j hj
  have h₀ := endpoints_eq_zero_of_index hx j.castSucc.castSucc (by simpa using hj)
  have h₁ := endpoints_eq_zero_of_index hx j.castSucc.succ (by simp; omega)
  have h₃ := endpoints_eq_zero_of_index hx j.succ.succ (by simp; omega)
  change gradient (objective β) x j = 0
  rw [gradient_objective_coordinate]
  simp [edge, h₀, h₁, h₃]

private theorem mem_prefix_of_gradient_span {d : ℕ} (β : ℝ) (x : ℕ → Point d)
    (h0 : x 0 = 0)
    (hspan : ∀ n, x (n + 1) ∈ Submodule.span ℝ
      (Set.range (fun i : Fin (n + 1) => gradient (objective β) (x i.val)))) (n : ℕ) :
    x n ∈ prefixSubmodule d n := by
  induction n using Nat.strong_induction_on with
  | h n ih =>
    cases n with
    | zero => rw [h0]; exact Submodule.zero_mem _
    | succ n =>
      apply (Submodule.span_le.mpr ?_) (hspan n)
      rintro _ ⟨i, rfl⟩
      have hi := i.isLt
      exact prefix_mono (show i.val + 1 ≤ n + 1 by omega)
        (gradient_mem_prefix_succ β (ih i.val hi))

private theorem shifted_square_sum_six (d : ℕ) :
    6 * (∑ i ∈ range d, ((i : ℝ) + 1) ^ 2) =
      (d : ℝ) * ((d : ℝ) + 1) * (2 * (d : ℝ) + 1) := by
  induction d with
  | zero => simp
  | succ d ih =>
    rw [sum_range_succ, mul_add, ih]
    push_cast
    ring

private theorem shifted_square_sum_factor_eight {m d : ℕ} (hd : d ≤ 2 * m) :
    (∑ i ∈ range d, ((i : ℝ) + 1) ^ 2) ≤
      8 * (∑ i ∈ range m, ((i : ℝ) + 1) ^ 2) := by
  have h : (d : ℝ) ≤ 2 * (m : ℝ) := by exact_mod_cast hd
  have hp : (d : ℝ) * ((d : ℝ) + 1) * (2 * (d : ℝ) + 1) ≤
      (2 * (m : ℝ)) * (2 * ((m : ℝ) + 1)) * (2 * (2 * (m : ℝ) + 1)) := by
    gcongr <;> linarith
  linarith [shifted_square_sum_six d, shifted_square_sum_six m,
    show (2 * (m : ℝ)) * (2 * ((m : ℝ) + 1)) * (2 * (2 * (m : ℝ) + 1)) =
      8 * ((m : ℝ) * ((m : ℝ) + 1) * (2 * (m : ℝ) + 1)) by ring]

-- The source's zero suffix is the zero prefix after reversing coordinates.
private theorem shifted_affine_profile_distance {m d : ℕ} (hm : m ≤ d) (hd : d ≤ 2 * m)
    (x : ℕ → ℝ) (hx : ∀ i < m, x i = 0) :
    (∑ i ∈ range d, (((i : ℝ) + 1) / ((d : ℝ) + 1)) ^ 2) ≤
      8 * (∑ i ∈ range d, (x i - ((i : ℝ) + 1) / ((d : ℝ) + 1)) ^ 2) := by
  let D : ℝ := (d : ℝ) + 1
  change (∑ i ∈ range d, (((i : ℝ) + 1) / D) ^ 2) ≤
      8 * (∑ i ∈ range d, (x i - ((i : ℝ) + 1) / D) ^ 2)
  calc
    _ = (∑ i ∈ range d, ((i : ℝ) + 1) ^ 2) / D ^ 2 := by
      simp_rw [div_pow, Finset.sum_div]
    _ ≤ 8 * ((∑ i ∈ range m, ((i : ℝ) + 1) ^ 2) / D ^ 2) := by
      rw [← mul_div_assoc]
      exact div_le_div_of_nonneg_right (shifted_square_sum_factor_eight hd) (sq_nonneg D)
    _ = 8 * (∑ i ∈ range m, (((i : ℝ) + 1) / D) ^ 2) := by
      simp_rw [div_pow, Finset.sum_div]
    _ = 8 * (∑ i ∈ range m, (x i - ((i : ℝ) + 1) / D) ^ 2) := by
      congr 1
      apply sum_congr rfl
      intro i hi
      rw [hx i (mem_range.mp hi), zero_sub, neg_sq]
    _ ≤ _ := by
      apply mul_le_mul_of_nonneg_left _ (by norm_num)
      apply sum_le_sum_of_subset_of_nonneg (range_mono hm)
      intro i _ _
      exact sq_nonneg _

-- Zero-based i indexes the source's coordinate k=i+1.
private theorem affineProfile_norm_sq_le {d N : ℕ} (hd : 2 * N + 1 ≤ d)
    (x : Point d) (hx : x ∈ prefixSubmodule d N) :
    ‖affineProfile d‖ ^ 2 ≤ 8 * ‖x - affineProfile d‖ ^ 2 := by
  let m := affineProfile d
  change ‖m‖ ^ 2 ≤ 8 * ‖x - m‖ ^ 2
  let v : ℕ → ℝ := fun i => ((i : ℝ) + 1) / ((d : ℝ) + 1)
  let y : ℕ → ℝ := fun i => if h : i < d then x (Fin.rev ⟨i, h⟩) else 0
  have hy (i : ℕ) (hi : i < d - N) : y i = 0 := by
    have hi' : i < d := by omega
    rw [show y i = x (Fin.rev ⟨i, hi'⟩) from dif_pos hi']
    apply hx
    rw [Fin.val_rev]
    change N ≤ d - (i + 1)
    omega
  have hm (i : Fin d) : m i.rev = v i.val := by
    change ((d : ℝ) - (i.rev.val : ℝ)) / ((d : ℝ) + 1) = v i.val
    have he : i.rev.val + i.val + 1 = d := by
      have h := i.isLt
      rw [Fin.val_rev]
      omega
    have he' : (i.rev.val : ℝ) + (i.val : ℝ) + 1 = (d : ℝ) := by exact_mod_cast he
    dsimp [v]
    congr 1
    simp only [Fin.val_rev] at he' ⊢
    linarith
  have hsum := shifted_affine_profile_distance (m := d-N) (d := d)
    (by omega) (by omega) y hy
  change (∑ i ∈ range d, v i ^ 2) ≤ 8 * ∑ i ∈ range d, (y i - v i) ^ 2 at hsum
  rw [← Fin.sum_univ_eq_sum_range (fun i => v i ^ 2) d,
    ← Fin.sum_univ_eq_sum_range (fun i => (y i - v i) ^ 2) d] at hsum
  calc
    ‖m‖ ^ 2 = ∑ i : Fin d, (m i.rev) ^ 2 := by
      rw [EuclideanSpace.real_norm_sq_eq]
      exact (Equiv.sum_comp (Fin.revPerm : Equiv.Perm (Fin d)) (fun i => (m i) ^ 2)).symm
    _ = ∑ i : Fin d, v i.val ^ 2 := by simp_rw [hm]
    _ ≤ 8 * ∑ i : Fin d, (y i.val - v i.val) ^ 2 := hsum
    _ = 8 * ∑ i : Fin d, ((x - m) i.rev) ^ 2 := by
      congr 1
      apply sum_congr rfl
      intro i _
      rw [show y i.val = x i.rev from dif_pos i.isLt, ← hm]
      rfl
    _ = 8 * ‖x - m‖ ^ 2 := by
      rw [EuclideanSpace.real_norm_sq_eq]
      congr 1
      exact Equiv.sum_comp (Fin.revPerm : Equiv.Perm (Fin d)) (fun i => ((x - m) i) ^ 2)

private theorem distance_lower_bound_at_zero {d N : ℕ} (hd : 2 * N + 1 ≤ d) (β : ℝ)
    (x : ℕ → Point d) (h0 : x 0 = 0)
    (hspan : ∀ n, x (n + 1) ∈ Submodule.span ℝ
      (Set.range (fun i : Fin (n + 1) => gradient (objective β) (x i.val)))) :
    (1 / 8 : ℝ) * ‖x 0 - affineProfile d‖ ^ 2 ≤ ‖x N - affineProfile d‖ ^ 2 := by
  have h := affineProfile_norm_sq_le hd (x N) (mem_prefix_of_gradient_span β x h0 hspan N)
  rw [h0, zero_sub, norm_neg]
  linarith

private noncomputable def translatedObjective {d : ℕ} (β : ℝ) (x₀ x : Point d) : ℝ :=
  objective β (x - x₀)

private theorem hasFDerivAt_translatedObjective {d : ℕ} (β : ℝ) (x₀ x : Point d) :
    HasFDerivAt (translatedObjective β x₀)
      (fderiv ℝ (objective β) (x - x₀)) x := by
  have h := hasFDerivAt_objective β (x - x₀)
  rw [h.fderiv]
  change HasFDerivAt (fun y => objective β (y - x₀)) _ x
  simpa only [Function.comp_def, id_eq, ContinuousLinearMap.comp_id] using
    h.comp x ((hasFDerivAt_id x).sub_const x₀)

private theorem gradient_translatedObjective {d : ℕ} (β : ℝ) (x₀ x : Point d) :
    gradient (translatedObjective β x₀) x = gradient (objective β) (x - x₀) := by
  ext i
  have ht := hasFDerivAt_translatedObjective β x₀ x
  have ho := hasFDerivAt_objective β (x - x₀)
  change gradient (translatedObjective β x₀) x i = gradient (objective β) (x - x₀) i
  rw [← fderiv_apply_coordinate_eq_gradient_coordinate_of_differentiableAt i ht.differentiableAt,
      ← fderiv_apply_coordinate_eq_gradient_coordinate_of_differentiableAt i ho.differentiableAt,
      ht.fderiv]

private theorem translatedObjective_class {d : ℕ} {β : ℝ} (hβ : 0 ≤ β) (x₀ : Point d) :
    ConvexOn ℝ Set.univ (translatedObjective β x₀) ∧
    IsMinOn (translatedObjective β x₀) Set.univ (x₀ + affineProfile d) := by
  refine ⟨?_, ?_⟩
  · let A : Point d →ᵃ[ℝ] Point d := (AffineEquiv.constVAdd ℝ (Point d) (-x₀)).toAffineMap
    have hA (x : Point d) : A x = x - x₀ := by
      change -x₀ + x = x - x₀
      abel
    have hfun : objective β ∘ A = translatedObjective β x₀ := by
      funext x
      exact congrArg (objective β) (hA x)
    have hc := (convexOn_objective (d := d) hβ).comp_affineMap A
    rw [Set.preimage_univ, hfun] at hc
    exact hc
  · intro y _
    change objective β (x₀ + affineProfile d - x₀) ≤ objective β (y - x₀)
    rw [show x₀ + affineProfile d - x₀ = affineProfile d by abel]
    exact isMinOn_affineProfile hβ (Set.mem_univ (y - x₀))

private theorem translatedObjective_upper_model {d : ℕ} {β : ℝ} (hβ : 0 ≤ β) (x₀ x y : Point d) :
    translatedObjective β x₀ y ≤ translatedObjective β x₀ x
      + inner ℝ (gradient (translatedObjective β x₀) x) (y - x)
      + β / 2 * ‖y - x‖ ^ 2 := by
  rw [gradient_translatedObjective, ← fderiv_apply_eq_inner_gradient_of_differentiableAt
    (hasFDerivAt_objective β (x - x₀)).differentiableAt]
  change objective β (y - x₀) ≤ objective β (x - x₀) +
    fderiv ℝ (objective β) (x - x₀) (y - x) + β / 2 * ‖y - x‖ ^ 2
  have hE := mul_le_mul_of_nonneg_left (edgeEnergy_le (y - x)) (by positivity : 0 ≤ β / 8)
  have h := objective_remainder β (x - x₀) (y - x₀)
  rw [show (y - x₀) - (x - x₀) = y - x by abel] at h
  linarith

private theorem translated_distance_lower_bound {d N : ℕ} (hd : 2 * N + 1 ≤ d)
    (β : ℝ) (x₀ : Point d) (x : ℕ → Point d) (h0 : x 0 = x₀)
    (hspan : ∀ n, x (n + 1) - x₀ ∈ Submodule.span ℝ
      (Set.range (fun i : Fin (n + 1) => gradient (translatedObjective β x₀) (x i.val)))) :
    (1 / 8 : ℝ) * ‖x 0 - (x₀ + affineProfile d)‖ ^ 2 ≤
      ‖x N - (x₀ + affineProfile d)‖ ^ 2 := by
  have hs : ∀ n, x (n + 1) - x₀ ∈ Submodule.span ℝ
      (Set.range (fun i : Fin (n + 1) => gradient (objective β) (x i.val - x₀))) := by
    simpa only [gradient_translatedObjective] using hspan
  have h := distance_lower_bound_at_zero hd β (fun n => x n - x₀)
    (show x 0 - x₀ = 0 by rw [h0, sub_self]) hs
  simpa only [sub_sub] using h

/-- Chewi, *Lectures on Optimization*, Exercise 4.1: the translated path
quadratic is convex and C¹ with the prescribed quadratic upper model.
Starting at the prescribed point, every gradient-span trajectory retains at
least one eighth of the initial squared distance to the stated minimizer. -/
theorem exercise_4_1 (d N : ℕ) (_hN : 1 ≤ N) (hd : 2 * N + 1 ≤ d + 1)
    (β : ℝ) (hβ : 0 < β) (x₀ : EuclideanSpace ℝ (Fin (d + 1))) :
    let f : EuclideanSpace ℝ (Fin (d + 1)) → ℝ := fun y =>
      let v := y - x₀
      (β / 4) * (((v 0) ^ 2 + (∑ i : Fin d, (v i.castSucc - v i.succ) ^ 2)
        + (v (Fin.last d)) ^ 2) / 2 - v 0)
    let xstar : EuclideanSpace ℝ (Fin (d + 1)) :=
      x₀ + WithLp.toLp 2 (fun i : Fin (d + 1) =>
        1 - ((i.val : ℝ) + 1) / ((d : ℝ) + 2))
    ConvexOn ℝ Set.univ f ∧ ContDiff ℝ 1 f ∧ IsMinOn f Set.univ xstar ∧
      (∀ x y, f y ≤ f x + inner ℝ (gradient f x) (y - x) + β / 2 * ‖y - x‖ ^ 2) ∧
      ∀ x : ℕ → EuclideanSpace ℝ (Fin (d + 1)), x 0 = x₀ →
        (∀ n, x (n + 1) - x₀ ∈ Submodule.span ℝ
          (Set.range (fun i : Fin (n + 1) => gradient f (x i.val)))) →
        (1 / 8 : ℝ) * ‖x 0 - xstar‖ ^ 2 ≤ ‖x N - xstar‖ ^ 2 := by
  intro f xstar
  have hf : f = translatedObjective β x₀ := by
    funext y
    exact (objective_eq_expanded β (y - x₀)).symm
  have hm : xstar = x₀ + affineProfile (d + 1) := by
    change x₀ + WithLp.toLp 2 _ = x₀ + WithLp.toLp 2 _
    congr 1
    ext i
    change 1 - ((i.val : ℝ) + 1) / ((d : ℝ) + 2) =
      ((↑(d + 1) : ℝ) - (i.val : ℝ)) / ((↑(d + 1) : ℝ) + 1)
    rw [Nat.cast_succ, show (d : ℝ) + 1 + 1 = (d : ℝ) + 2 by ring]
    have hd₂ : (d : ℝ) + 2 ≠ 0 := by positivity
    field_simp [hd₂]
    ring
  rw [hf, hm]
  have hc := translatedObjective_class hβ.le x₀
  have hcd : ContDiff ℝ 1 (translatedObjective β x₀) :=
    (contDiff_objective β).comp (contDiff_id.sub contDiff_const)
  exact ⟨hc.1, hcd, hc.2, translatedObjective_upper_model hβ.le x₀,
    translated_distance_lower_bound hd β x₀⟩

end AutoSamplingTheory.ExampleCases.LowerBounds.GradientSpanDistance
