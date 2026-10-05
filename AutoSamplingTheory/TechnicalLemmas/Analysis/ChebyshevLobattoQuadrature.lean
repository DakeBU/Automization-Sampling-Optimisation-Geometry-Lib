import Mathlib.LinearAlgebra.Lagrange
import Mathlib.Topology.Algebra.Polynomial
import Mathlib.Topology.Order.Compact
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Basic
import Mathlib.Analysis.SpecialFunctions.Integrals.Basic
import Mathlib.Tactic

/-! SPHMC3.6/B1: actual source coefficients. No logarithmic Lebesgue bound,
nonnegative Clenshaw-Curtis weights or interpolation remainder is asserted. -/
noncomputable section
open Set MeasureTheory Polynomial
open scoped BigOperators

namespace AutoSamplingTheory.TechnicalLemmas.Analysis.ChebyshevLobattoQuadrature

private def nodes (J : ℕ) (h : ℝ) (i : Fin J) : ℝ :=
  h/2*(1-Real.cos ((i : ℝ)/(J-1 : ℝ)*Real.pi))

private theorem nodes_mem {J : ℕ} {h : ℝ} (hh : 0 ≤ h) (i : Fin J) :
    nodes J h i ∈ Icc 0 h := by
  dsimp [nodes]
  constructor
  · exact mul_nonneg (by positivity) (sub_nonneg.mpr (Real.cos_le_one _))
  · have hc := Real.neg_one_le_cos ((i : ℝ)/(J-1 : ℝ)*Real.pi)
    nlinarith

private theorem nodes_injective {J : ℕ} (hJ : 2 ≤ J) {h : ℝ} (hh : 0 < h) :
    Function.Injective (nodes J h) := by
  have hJr : (2 : ℝ) ≤ J := by exact_mod_cast hJ
  have hd : (0 : ℝ) < J-1 := by linarith
  have harg (i : Fin J) : (i : ℝ)/(J-1 : ℝ)*Real.pi ∈ Icc 0 Real.pi := by
    constructor
    · positivity
    · have hi' : (i : ℝ)+1 ≤ J := by
        exact_mod_cast (show (i : ℕ)+1 ≤ J from by omega)
      have hi : (i : ℝ) ≤ J-1 := by linarith
      have hr : (i : ℝ)/(J-1 : ℝ) ≤ 1 := (div_le_one hd).mpr hi
      nlinarith [Real.pi_pos]
  intro i j hij
  have he : Real.cos ((i : ℝ)/(J-1 : ℝ)*Real.pi) =
      Real.cos ((j : ℝ)/(J-1 : ℝ)*Real.pi) := by
    dsimp [nodes] at hij
    nlinarith
  have ha := Real.injOn_cos (harg i) (harg j) he
  have hd0 := ne_of_gt hd
  have hp0 := ne_of_gt Real.pi_pos
  have heq : (i : ℝ) = j := by
    apply (div_left_inj' hd0).mp
    exact (mul_left_inj' hp0).mp ha
  exact Fin.ext (by exact_mod_cast heq)

private theorem nodes_last {J : ℕ} (hJ : 2 ≤ J) (h : ℝ) :
    nodes J h ⟨J-1,by omega⟩ = h := by
  have hJr : (2 : ℝ) ≤ J := by exact_mod_cast hJ
  have hd : (J : ℝ)-1 ≠ 0 := by linarith
  simp only [nodes, Nat.cast_sub (by omega : 1 ≤ J), Nat.cast_one]
  rw [div_self hd, one_mul, Real.cos_pi]
  ring


/-- Exact source nodes and coefficient integrals, with cardinal/constant
interpolation and the sharp1/2 integrated row bound. The source logarithmic
Lebesgue estimate, momentum-weight positivity and B2 error stay independent. -/
theorem chebyshev_lobatto_coefficients {J : ℕ} (hJ : 2 ≤ J) {h : ℝ} (hh : 0 < h) :
    let t := fun i : Fin J => h/2*(1-Real.cos ((i : ℝ)/(J-1 : ℝ)*Real.pi))
    let ell := fun j : Fin J => Lagrange.basis Finset.univ t j
    let Lambda := sSup ((fun s : ℝ => ∑ j : Fin J, |(ell j).eval s|) '' Icc 0 h)
    let omega := fun i j : Fin J => ∫ s in 0..t i, (t i-s)*(ell j).eval s
    let momentumWeight := fun j : Fin J => ∫ s in 0..h, (ell j).eval s
    (∀ i, t i ∈ Icc 0 h) ∧ Function.Injective t ∧
    t ⟨J-1,by omega⟩ = h ∧
    (∀ i j, (ell i).eval (t j) = if i=j then 1 else 0) ∧
    (∀ s : ℝ, ∑ j : Fin J, (ell j).eval s = 1) ∧
    1 ≤ Lambda ∧
    (∀ i, (∑ j : Fin J, |omega i j|) ≤ (t i)^2/2*Lambda ∧
      (∑ j : Fin J, |omega i j|) ≤ h^2/2*Lambda) ∧
    (∑ j : Fin J, momentumWeight j) = h := by
  classical
  dsimp only
  let t := nodes J h
  let ell := fun j : Fin J => Lagrange.basis Finset.univ t j
  let F := fun s : ℝ => ∑ j : Fin J, |(ell j).eval s|
  let Lambda := sSup (F '' Icc 0 h)
  have ht (i : Fin J) : t i ∈ Icc 0 h := nodes_mem hh.le i
  have hinj : Function.Injective t := nodes_injective hJ hh
  have hcard (i j : Fin J) : (ell i).eval (t j) = if i=j then 1 else 0 := by
    by_cases he : i=j
    · subst j
      simpa [ell] using Lagrange.eval_basis_self (s := Finset.univ) hinj.injOn
        (Finset.mem_univ i)
    · simpa [ell,he] using Lagrange.eval_basis_of_ne (s := Finset.univ) (v := t) he
        (Finset.mem_univ j)
  have hpart (s : ℝ) : ∑ j : Fin J, (ell j).eval s = 1 := by
    have he : (∑ j : Fin J, ell j) = 1 :=
      Lagrange.sum_basis hinj.injOn ⟨⟨0,by omega⟩,Finset.mem_univ _⟩
    simpa only [Polynomial.eval_finsetSum, Polynomial.eval_one] using
      congrArg (fun p : ℝ[X] => p.eval s) he
  have hF : Continuous F := by
    apply continuous_finsetSum
    intro j _
    exact (ell j).continuous.abs
  have hbound : BddAbove (F '' Icc 0 h) := isCompact_Icc.bddAbove_image hF.continuousOn
  have hLeb (s : ℝ) (hs : s ∈ Icc 0 h) : F s ≤ Lambda :=
    le_csSup hbound (mem_image_of_mem F hs)
  have hLambda : 1 ≤ Lambda := by
    let i0 : Fin J := ⟨0,by omega⟩
    have hval : F (t i0) = 1 := by
      simp only [F,hcard]
      simp_rw [apply_ite abs,abs_one,abs_zero]
      simp
    exact hval ▸ hLeb (t i0) (ht i0)
  have hw (i : Fin J) : (∑ j : Fin J, |∫ s in 0..t i, (t i-s)*(ell j).eval s|) ≤
      (t i)^2/2*Lambda := by
    have hf (j : Fin J) : Continuous (fun s : ℝ => (t i-s)*(ell j).eval s) :=
      (continuous_const.sub continuous_id).mul (ell j).continuous
    have hfa (j : Fin J) : Continuous (fun s : ℝ => |(t i-s)*(ell j).eval s|) := (hf j).abs
    calc
      _ ≤ ∑ j : Fin J, ∫ s in 0..t i, |(t i-s)*(ell j).eval s| := by
        apply Finset.sum_le_sum
        intro j _
        simpa only [Real.norm_eq_abs] using
          intervalIntegral.norm_integral_le_integral_norm (f := fun s => (t i-s)*(ell j).eval s)
            (ht i).1
      _ = ∫ s in 0..t i, ∑ j : Fin J, |(t i-s)*(ell j).eval s| :=
        (intervalIntegral.integral_finsetSum (fun j _ => (hfa j).intervalIntegrable _ _)).symm
      _ ≤ ∫ s in 0..t i, (t i-s)*Lambda := by
        apply intervalIntegral.integral_mono_on (ht i).1
          ((continuous_finsetSum Finset.univ (fun j _ => hfa j)).intervalIntegrable _ _)
          (((continuous_const.sub continuous_id).mul continuous_const).intervalIntegrable _ _)
        intro s hs
        have hnon : 0 ≤ t i-s := sub_nonneg.mpr hs.2
        have hs' : s ∈ Icc 0 h := ⟨hs.1,hs.2.trans (ht i).2⟩
        calc
          _ = (t i-s)*F s := by
            simp only [abs_mul,abs_of_nonneg hnon,F,Finset.mul_sum]
          _ ≤ _ := mul_le_mul_of_nonneg_left (hLeb s hs') hnon
      _ = (t i)^2/2*Lambda := by
        rw [intervalIntegral.integral_mul_const,
          intervalIntegral.integral_sub (f := fun _ : ℝ => t i) (g := fun s : ℝ => s)
            (continuous_const.intervalIntegrable _ _)
            (continuous_id.intervalIntegrable _ _),intervalIntegral.integral_const,
          integral_id]
        simp only [sub_zero]
        ring
  refine ⟨ht,hinj,nodes_last hJ h,hcard,hpart,hLambda,?_,?_⟩
  · intro i
    refine ⟨hw i,(hw i).trans ?_⟩
    have hsq : (t i)^2 ≤ h^2 := sq_le_sq₀ (ht i).1 hh.le |>.mpr (ht i).2
    exact mul_le_mul_of_nonneg_right (by linarith : (t i)^2/2 ≤ h^2/2)
      (by linarith : 0 ≤ Lambda)
  · change (∑ j : Fin J, ∫ s in 0..h, (ell j).eval s) = h
    rw [← intervalIntegral.integral_finsetSum (s := Finset.univ)
      (f := fun j s => (ell j).eval s)
      (fun j _ => (ell j).continuous.intervalIntegrable 0 h)]
    simp only [hpart,intervalIntegral.integral_const]
    simp

end AutoSamplingTheory.TechnicalLemmas.Analysis.ChebyshevLobattoQuadrature
