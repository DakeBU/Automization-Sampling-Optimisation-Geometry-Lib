import Mathlib.Analysis.Convex.SpecificFunctions.Basic
import Mathlib.Analysis.SpecialFunctions.Trigonometric.DerivHyp
import Mathlib.Tactic

/-!
# Query budget in the hidden determinant lower bound

Zhou–Suzuki, arXiv:2610.20492v1, Section 3.3, equations (9) and (10).
Use the separation upper bound at n = 2T+1 when this block fits. The scalar
proof keeps the integer quotient k = d/n and the paper's exponential and
logarithmic constants.
-/

namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.FirstOrderIndistinguishability

/-- Convert the gap estimate (8) and the accuracy upper bound into (9).
The tangent bound for the exponential at zero gives the logarithmic estimate
without an integral. -/
private theorem separation_exponent {a ε : ℝ} (ha : 0 ≤ a) (he : ε ≤ 1/16)
    (h : 1 - Real.exp (-a) ≤ 2*ε) : a ≤ 4*ε := by
  have h₁ : 1 - 2*ε ≤ Real.exp (-a) := by linarith
  have h₂ := mul_le_mul_of_nonneg_right h₁ (Real.exp_nonneg a)
  rw [Real.exp_neg, inv_mul_cancel₀ (Real.exp_ne_zero _)] at h₂
  have h₃ := mul_le_mul_of_nonneg_left (Real.add_one_le_exp a)
    (show 0 ≤ 1-2*ε by linarith)
  nlinarith [mul_nonneg ha (show 0 ≤ 1/2-2*ε by linarith)]

private theorem floor_twice {d n : ℕ} (hn : 0 < n) (hnd : n ≤ d) :
    (d : ℝ) ≤ 2*(n:ℝ)*((d/n:ℕ):ℝ) := by
  have hk : 0 < d/n := Nat.div_pos hnd hn
  have hnle : n ≤ n*(d/n) := Nat.le_mul_of_pos_right _ hk
  have hmod := Nat.mod_lt d hn
  have hdiv := Nat.div_add_mod d n
  exact_mod_cast (show d ≤ 2*n*(d/n) by nlinarith)

/-- The exponential form of the bound on T in (10) implies the logarithm in
the theorem. The constants use sinh t ≥ t and the concavity of log. -/
private theorem budget_log {D t s ε : ℝ} (hD : 0 ≤ D) (ht : 0 ≤ t) (hs : 0 < s)
    (he : 0 < ε) (h : D ≤ 192*ε*t*Real.exp (30*t/s)) :
    s * Real.log (1 + D/(s*ε)) ≤ 192*t := by
  let z := 30*t/s
  let u := D/(s*ε)
  have hz : 0 ≤ z := by dsimp [z]; positivity
  have hu : 0 ≤ u := by dsimp [u]; positivity
  have hscale : (5/16:ℝ)*u ≤ 2*Real.exp z*z := by
    calc
      _ = (5/(16*s*ε))*D := by dsimp [u]; ring
      _ ≤ (5/(16*s*ε))*(192*ε*t*Real.exp z) :=
        mul_le_mul_of_nonneg_left h (by positivity)
      _ = _ := by dsimp [z]; field_simp; ring
  have hdouble : Real.exp (2*z) - 1 = 2*Real.exp z*Real.sinh z := by
    rw [show 2*z = z+z by ring, Real.exp_add, Real.sinh_eq, Real.exp_neg]
    field_simp
  have hlog : Real.log (1 + (5/16:ℝ)*u) ≤ 2*z := by
    apply (Real.log_le_iff_le_exp (by positivity)).mpr
    have hss : z ≤ Real.sinh z := Real.self_le_sinh_iff.mpr hz
    linarith only [hdouble, hscale, mul_le_mul_of_nonneg_left hss (show 0 ≤ 2*Real.exp z by positivity)]
  have hc := strictConcaveOn_log_Ioi.concaveOn.2
    (show (1:ℝ) ∈ Set.Ioi 0 by norm_num) (show 1+u ∈ Set.Ioi (0:ℝ) by
      exact add_pos_of_pos_of_nonneg zero_lt_one hu)
    (show 0 ≤ (11/16:ℝ) by norm_num) (show 0 ≤ (5/16:ℝ) by norm_num)
    (show (11/16:ℝ)+5/16=1 by norm_num)
  simp only [smul_eq_mul, Real.log_one, mul_zero, zero_add] at hc
  rw [show (11/16:ℝ)*1+(5/16)*(1+u)=1+(5/16)*u by ring] at hc
  calc
    _ = ((16/5:ℝ)*s)*((5/16:ℝ)*Real.log (1+u)) := by dsimp [u]; ring
    _ ≤ ((16/5:ℝ)*s)*(2*z) := mul_le_mul_of_nonneg_left (hc.trans hlog) (by positivity)
    _ = _ := by dsimp [z]; field_simp; ring

/-- The quantitative implication in Theorem 3.1, including the alternative in
which the proposed block is too large for the ambient dimension. -/
theorem query_budget_of_separation {d T : ℕ} {κ ε : ℝ} (hT : 1 ≤ T)
    (hκ : 4 ≤ κ) (hε : 0 < ε) (hsmall : ε ≤ 1/16)
    (hsep : 2*T+1 ≤ d →
      1 - Real.exp (-(((d/(2*T+1):ℕ):ℝ)/8) *
        Real.exp (-(10*((2*T+1:ℕ):ℝ))/Real.sqrt κ)) ≤ 2*ε) :
    (1/256:ℝ) * min (d:ℝ) (Real.sqrt κ * Real.log (1+(d:ℝ)/(Real.sqrt κ*ε))) ≤ (T:ℝ) := by
  let n := 2*T+1
  let s := Real.sqrt κ
  have hs : 0 < s := Real.sqrt_pos.mpr (by linarith)
  have ht : (0 : ℝ) ≤ T := by positivity
  by_cases hnd : n ≤ d
  · let k := d/n
    have hn : 0 < n := by dsimp [n]; omega
    have hnt : (n:ℝ) ≤ 3*(T:ℝ) := by exact_mod_cast (show n ≤ 3*T by dsimp [n]; omega)
    have hgap : 1 - Real.exp ( -((k:ℝ)/8) * Real.exp (-(10*(n:ℝ))/s)) ≤ 2*ε := hsep hnd
    have hneg : -((k:ℝ)/8) * Real.exp (-(10*(n:ℝ))/s) =
        -(((k:ℝ)/8) * Real.exp (-(10*(n:ℝ))/s)) := by ring
    rw [hneg] at hgap
    have ha := separation_exponent (a := ((k:ℝ)/8)*Real.exp (-(10*(n:ℝ))/s))
      (by positivity) hsmall hgap
    have hratio : (k:ℝ)/Real.exp (10*(n:ℝ)/s) ≤ 32*ε := by
      rw [neg_div, Real.exp_neg] at ha
      rw [div_eq_mul_inv]
      linarith
    have hk := (div_le_iff₀ (Real.exp_pos _)).mp hratio
    have hg : Real.exp (10*(n:ℝ)/s) ≤ Real.exp (30*(T:ℝ)/s) := by
      apply Real.exp_le_exp.mpr
      exact div_le_div_of_nonneg_right (by linarith) hs.le
    have he : (d:ℝ) ≤ 192*ε*(T:ℝ)*Real.exp (30*(T:ℝ)/s) := by
      calc
        _ ≤ 2*(n:ℝ)*(k:ℝ) := floor_twice hn hnd
        _ ≤ 2*(n:ℝ)*(32*ε*Real.exp (10*(n:ℝ)/s)) :=
          mul_le_mul_of_nonneg_left hk (by positivity)
        _ = (64*ε) * ((n:ℝ)*Real.exp (10*(n:ℝ)/s)) := by ring
        _ ≤ (64*ε) * ((3*(T:ℝ))*Real.exp (30*(T:ℝ)/s)) := by
          apply mul_le_mul_of_nonneg_left _ (by positivity)
          exact mul_le_mul hnt hg (Real.exp_nonneg _) (by positivity)
        _ = _ := by ring
    have hlog := budget_log (D := (d:ℝ)) (by positivity) ht hs hε he
    have hmin := min_le_right (d:ℝ) (s * Real.log (1+(d:ℝ)/(s*ε)))
    change (1/256:ℝ)*min (d:ℝ) (s * Real.log (1+(d:ℝ)/(s*ε))) ≤ _
    linarith
  · have hdim : d ≤ 2*T := by dsimp [n] at hnd; omega
    have hdim' : (d:ℝ) ≤ 2*(T:ℝ) := by exact_mod_cast hdim
    have hmin := min_le_left (d:ℝ) (Real.sqrt κ * Real.log (1+(d:ℝ)/(Real.sqrt κ*ε)))
    linarith

#print axioms query_budget_of_separation

end AutoSamplingTheory.ExampleCases.GaussianComplexity.FirstOrderIndistinguishability
