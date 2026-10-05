import Mathlib.Analysis.InnerProductSpace.Basic
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Sinc
import Mathlib.Tactic

/-!
# Explicit geodesics on the unit sphere

This module gives the ambient formula for the exponential map of the unit
sphere in a real inner-product space.  It proves smoothness, exact derivatives
through order four, uniform derivative bounds, and exact preservation of the
unit norm for tangent increments.  The results are independent of any
statistical model and can be reused in Riemannian optimization and geometric
numerical analysis.
-/

namespace AutoSamplingTheory.TechnicalLemmas.Geometry.UnitSphere

open scoped InnerProductSpace

noncomputable section

variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
/-- The unit-sphere exponential-map formula written in the ambient inner
product space. Real.sinc supplies the continuous value at zero. -/
noncomputable def unitSphereExp (w z : E) : E :=
  Real.cos ‖z‖ • w + Real.sinc ‖z‖ • z

/-- Signed geodesic parameterization through `w` with initial velocity `z`.
Unlike `unitSphereExp w (t • z)`, this formula is smooth across negative values of
`t`; on nonnegative times the two parameterizations agree. -/
noncomputable def unitSphereGeodesic (w z : E) (t : ℝ) : E :=
  if ‖z‖ = 0 then w
  else Real.cos (t * ‖z‖) • w +
    (Real.sin (t * ‖z‖) / ‖z‖) • z

/-- For fixed base point and velocity, the signed sphere geodesic is smooth
to every finite order. -/
theorem unitSphereGeodesic_contDiff (w z : E) (n : WithTop ℕ∞) :
    ContDiff ℝ n (unitSphereGeodesic w z) := by
  by_cases hz : ‖z‖ = 0
  · have hgeo : unitSphereGeodesic w z = fun _ : ℝ => w := by
      funext t
      simp [unitSphereGeodesic, hz]
    rw [hgeo]
    fun_prop
  · unfold unitSphereGeodesic
    simp only [hz, ↓reduceIte]
    fun_prop

/-- The sphere exponential map is continuous in its tangent increment. -/
theorem unitSphereExp_continuous (w : E) : Continuous (unitSphereExp w) := by
  unfold unitSphereExp
  fun_prop

private theorem unitSphereGeodesic_zero (w z : E) :
    unitSphereGeodesic w z 0 = w := by
  by_cases hz : ‖z‖ = 0
  · simp [unitSphereGeodesic, hz]
  · simp [unitSphereGeodesic, hz]

/-- On forward time, the smooth signed geodesic is exactly the sphere
exponential map evaluated at the scaled tangent vector. -/
theorem unitSphereExp_smul_eq_unitSphereGeodesic
    (w z : E) {t : ℝ} (ht : 0 ≤ t) :
    unitSphereExp w (t • z) = unitSphereGeodesic w z t := by
  by_cases hz : z = 0
  · subst z
    simp [unitSphereExp, unitSphereGeodesic]
  by_cases ht0 : t = 0
  · subst t
    simp [unitSphereExp, unitSphereGeodesic]
  have hr : ‖z‖ ≠ 0 := norm_ne_zero_iff.mpr hz
  have htne : t ≠ 0 := ht0
  have hnorm : ‖t • z‖ = t * ‖z‖ := by
    rw [norm_smul, Real.norm_eq_abs, abs_of_nonneg ht]
  rw [unitSphereExp, unitSphereGeodesic, if_neg hr, hnorm,
    Real.sinc_of_ne_zero (mul_ne_zero htne hr)]
  congr 1
  rw [smul_smul]
  congr 1
  field_simp [htne, hr]

/-- First derivative of the signed sphere geodesic. -/
private theorem unitSphereGeodesic_hasDerivAt
    (w : E) {z : E} (hz : z ≠ 0) (t : ℝ) :
    HasDerivAt (unitSphereGeodesic w z)
      ((-(‖z‖ * Real.sin (t * ‖z‖))) • w +
        Real.cos (t * ‖z‖) • z) t := by
  have hr : ‖z‖ ≠ 0 := norm_ne_zero_iff.mpr hz
  have hgeo : unitSphereGeodesic w z = fun s : ℝ =>
      Real.cos (s * ‖z‖) • w +
        (Real.sin (s * ‖z‖) / ‖z‖) • z := by
    funext s
    simp [unitSphereGeodesic, hr]
  rw [hgeo]
  have harg : HasDerivAt (fun s : ℝ => s * ‖z‖) ‖z‖ t := by
    simpa using (hasDerivAt_id t).mul_const ‖z‖
  have hcos :
      HasDerivAt (fun s : ℝ => Real.cos (s * ‖z‖))
        (-(‖z‖ * Real.sin (t * ‖z‖))) t := by
    have h := (Real.hasDerivAt_cos (t * ‖z‖)).comp t harg
    exact h.congr_deriv (by ring)
  have hsin :
      HasDerivAt (fun s : ℝ => Real.sin (s * ‖z‖) / ‖z‖)
        (Real.cos (t * ‖z‖)) t := by
    have h :=
      ((Real.hasDerivAt_sin (t * ‖z‖)).comp t harg).div_const ‖z‖
    exact h.congr_deriv (by field_simp [hr])
  exact (hcos.smul_const w).add (hsin.smul_const z)

/-- At the base point, the sphere geodesic has initial velocity `z`. -/
private theorem unitSphereGeodesic_hasDerivAt_zero (w z : E) :
    HasDerivAt (unitSphereGeodesic w z) z 0 := by
  by_cases hz : z = 0
  · subst z
    have hgeo : unitSphereGeodesic w (0 : E) = fun _ : ℝ => w := by
      funext s
      simp [unitSphereGeodesic]
    rw [hgeo]
    exact hasDerivAt_const (x := (0 : ℝ)) w
  · simpa using unitSphereGeodesic_hasDerivAt w hz 0

/-- Second derivative of the signed sphere geodesic. -/
private theorem unitSphereGeodesic_velocity_hasDerivAt
    (w z : E) (t : ℝ) :
    HasDerivAt
      (fun s : ℝ =>
        (-(‖z‖ * Real.sin (s * ‖z‖))) • w +
          Real.cos (s * ‖z‖) • z)
      ((-(‖z‖ ^ (2 : ℕ) * Real.cos (t * ‖z‖))) • w +
        (-(‖z‖ * Real.sin (t * ‖z‖))) • z) t := by
  have harg : HasDerivAt (fun s : ℝ => s * ‖z‖) ‖z‖ t := by
    simpa using (hasDerivAt_id t).mul_const ‖z‖
  have hfirst :
      HasDerivAt
        (fun s : ℝ => -(‖z‖ * Real.sin (s * ‖z‖)))
        (-(‖z‖ ^ (2 : ℕ) * Real.cos (t * ‖z‖))) t := by
    have h :=
      (((Real.hasDerivAt_sin (t * ‖z‖)).comp t harg).const_mul ‖z‖).neg
    exact h.congr_deriv (by ring)
  have hsecond :
      HasDerivAt (fun s : ℝ => Real.cos (s * ‖z‖))
        (-(‖z‖ * Real.sin (t * ‖z‖))) t := by
    have h := (Real.hasDerivAt_cos (t * ‖z‖)).comp t harg
    exact h.congr_deriv (by ring)
  exact (hfirst.smul_const w).add (hsecond.smul_const z)

/-- Third derivative of the signed sphere geodesic. -/
private theorem unitSphereGeodesic_acceleration_hasDerivAt
    (w z : E) (t : ℝ) :
    HasDerivAt
      (fun s : ℝ =>
        (- (‖z‖ ^ (2 : ℕ) * Real.cos (s * ‖z‖))) • w +
          (- (‖z‖ * Real.sin (s * ‖z‖))) • z)
      ((‖z‖ ^ (3 : ℕ) * Real.sin (t * ‖z‖)) • w +
        (- (‖z‖ ^ (2 : ℕ) * Real.cos (t * ‖z‖))) • z) t := by
  have harg : HasDerivAt (fun s : ℝ => s * ‖z‖) ‖z‖ t := by
    simpa using (hasDerivAt_id t).mul_const ‖z‖
  have hfirst : HasDerivAt
      (fun s : ℝ => -(‖z‖ ^ (2 : ℕ) * Real.cos (s * ‖z‖)))
      (‖z‖ ^ (3 : ℕ) * Real.sin (t * ‖z‖)) t := by
    have h := (((Real.hasDerivAt_cos (t * ‖z‖)).comp t harg).const_mul
      (‖z‖ ^ (2 : ℕ))).neg
    exact h.congr_deriv (by ring)
  have hsecond : HasDerivAt
      (fun s : ℝ => -(‖z‖ * Real.sin (s * ‖z‖)))
      (- (‖z‖ ^ (2 : ℕ) * Real.cos (t * ‖z‖))) t := by
    have h := (((Real.hasDerivAt_sin (t * ‖z‖)).comp t harg).const_mul
      ‖z‖).neg
    exact h.congr_deriv (by ring)
  exact (hfirst.smul_const w).add (hsecond.smul_const z)

/-- Fourth derivative of the signed sphere geodesic. -/
private theorem unitSphereGeodesic_jerk_hasDerivAt
    (w z : E) (t : ℝ) :
    HasDerivAt
      (fun s : ℝ =>
        (‖z‖ ^ (3 : ℕ) * Real.sin (s * ‖z‖)) • w +
          (- (‖z‖ ^ (2 : ℕ) * Real.cos (s * ‖z‖))) • z)
      ((‖z‖ ^ (4 : ℕ) * Real.cos (t * ‖z‖)) • w +
        (‖z‖ ^ (3 : ℕ) * Real.sin (t * ‖z‖)) • z) t := by
  have harg : HasDerivAt (fun s : ℝ => s * ‖z‖) ‖z‖ t := by
    simpa using (hasDerivAt_id t).mul_const ‖z‖
  have hfirst : HasDerivAt
      (fun s : ℝ => ‖z‖ ^ (3 : ℕ) * Real.sin (s * ‖z‖))
      (‖z‖ ^ (4 : ℕ) * Real.cos (t * ‖z‖)) t := by
    have h := ((Real.hasDerivAt_sin (t * ‖z‖)).comp t harg).const_mul
      (‖z‖ ^ (3 : ℕ))
    exact h.congr_deriv (by ring)
  have hsecond : HasDerivAt
      (fun s : ℝ => -(‖z‖ ^ (2 : ℕ) * Real.cos (s * ‖z‖)))
      (‖z‖ ^ (3 : ℕ) * Real.sin (t * ‖z‖)) t := by
    have h := (((Real.hasDerivAt_cos (t * ‖z‖)).comp t harg).const_mul
      (‖z‖ ^ (2 : ℕ))).neg
    exact h.congr_deriv (by ring)
  exact (hfirst.smul_const w).add (hsecond.smul_const z)

/-- Uniform fourth-derivative envelope along a unit-sphere geodesic. -/
private theorem unitSphereGeodesic_fourth_derivative_norm_le
    {w z : E} (hw : ‖w‖ = 1) (t : ℝ) :
    ‖(‖z‖ ^ (4 : ℕ) * Real.cos (t * ‖z‖)) • w +
        (‖z‖ ^ (3 : ℕ) * Real.sin (t * ‖z‖)) • z‖ ≤
      2 * ‖z‖ ^ (4 : ℕ) := by
  calc
    _ ≤ ‖(‖z‖ ^ (4 : ℕ) * Real.cos (t * ‖z‖)) • w‖ +
        ‖(‖z‖ ^ (3 : ℕ) * Real.sin (t * ‖z‖)) • z‖ :=
      norm_add_le _ _
    _ ≤ ‖z‖ ^ 4 + ‖z‖ ^ 4 := by
      rw [norm_smul, norm_smul, hw, mul_one, Real.norm_eq_abs,
        Real.norm_eq_abs]
      apply add_le_add
      · rw [abs_mul, abs_of_nonneg (by positivity : 0 ≤ ‖z‖ ^ 4)]
        exact mul_le_of_le_one_right (by positivity)
          (Real.abs_cos_le_one _)
      · rw [abs_mul, abs_of_nonneg (by positivity : 0 ≤ ‖z‖ ^ 3)]
        have h := mul_le_mul_of_nonneg_left
          (Real.abs_sin_le_one (t * ‖z‖))
          (by positivity : 0 ≤ ‖z‖ ^ 3)
        nlinarith [norm_nonneg z]
    _ = 2 * ‖z‖ ^ 4 := by ring

/-- Uniform first-derivative envelope along a unit-sphere geodesic. -/
private theorem unitSphereGeodesic_first_derivative_norm_le
    {w z : E} (hw : ‖w‖ = 1) (t : ℝ) :
    ‖(-(‖z‖ * Real.sin (t * ‖z‖))) • w +
        Real.cos (t * ‖z‖) • z‖ ≤ 2 * ‖z‖ := by
  calc
    _ ≤ ‖(-(‖z‖ * Real.sin (t * ‖z‖))) • w‖ +
        ‖Real.cos (t * ‖z‖) • z‖ := norm_add_le _ _
    _ ≤ ‖z‖ + ‖z‖ := by
      rw [norm_smul, norm_smul, hw, mul_one, Real.norm_eq_abs,
        Real.norm_eq_abs, abs_neg]
      apply add_le_add
      · rw [abs_mul, abs_of_nonneg (norm_nonneg z)]
        exact mul_le_of_le_one_right (norm_nonneg z)
          (Real.abs_sin_le_one _)
      · exact mul_le_of_le_one_left (norm_nonneg z)
          (Real.abs_cos_le_one _)
    _ = 2 * ‖z‖ := by ring

/-- Uniform third-derivative envelope along a unit-sphere geodesic. -/
private theorem unitSphereGeodesic_third_derivative_norm_le
    {w z : E} (hw : ‖w‖ = 1) (t : ℝ) :
    ‖(‖z‖ ^ (3 : ℕ) * Real.sin (t * ‖z‖)) • w +
        (-(‖z‖ ^ (2 : ℕ) * Real.cos (t * ‖z‖))) • z‖ ≤
      2 * ‖z‖ ^ (3 : ℕ) := by
  calc
    _ ≤ ‖(‖z‖ ^ (3 : ℕ) * Real.sin (t * ‖z‖)) • w‖ +
        ‖(-(‖z‖ ^ (2 : ℕ) * Real.cos (t * ‖z‖))) • z‖ :=
      norm_add_le _ _
    _ ≤ ‖z‖ ^ 3 + ‖z‖ ^ 3 := by
      rw [norm_smul, norm_smul, hw, mul_one, Real.norm_eq_abs,
        Real.norm_eq_abs, abs_neg]
      apply add_le_add
      · rw [abs_mul, abs_of_nonneg (by positivity : 0 ≤ ‖z‖ ^ 3)]
        exact mul_le_of_le_one_right (by positivity)
          (Real.abs_sin_le_one _)
      · rw [abs_mul, abs_of_nonneg (by positivity : 0 ≤ ‖z‖ ^ 2)]
        have h := mul_le_mul_of_nonneg_left
          (Real.abs_cos_le_one (t * ‖z‖))
          (by positivity : 0 ≤ ‖z‖ ^ 2)
        nlinarith [norm_nonneg z]
    _ = 2 * ‖z‖ ^ 3 := by ring

/-- Uniform second-derivative envelope along a unit-sphere geodesic. -/
private theorem unitSphereGeodesic_second_derivative_norm_le
    {w z : E} (hw : ‖w‖ = 1) (t : ℝ) :
    ‖(-(‖z‖ ^ (2 : ℕ) * Real.cos (t * ‖z‖))) • w +
        (-(‖z‖ * Real.sin (t * ‖z‖))) • z‖ ≤
      2 * ‖z‖ ^ (2 : ℕ) := by
  calc
    ‖(-(‖z‖ ^ (2 : ℕ) * Real.cos (t * ‖z‖))) • w +
        (-(‖z‖ * Real.sin (t * ‖z‖))) • z‖ ≤
      ‖(-(‖z‖ ^ (2 : ℕ) * Real.cos (t * ‖z‖))) • w‖ +
        ‖(-(‖z‖ * Real.sin (t * ‖z‖))) • z‖ := norm_add_le _ _
    _ ≤ ‖z‖ ^ (2 : ℕ) + ‖z‖ ^ (2 : ℕ) := by
      rw [norm_smul, norm_smul, hw, mul_one, Real.norm_eq_abs,
        Real.norm_eq_abs, abs_neg, abs_neg]
      apply add_le_add
      · rw [abs_mul, abs_of_nonneg (sq_nonneg ‖z‖)]
        simpa using mul_le_mul_of_nonneg_left
          (Real.abs_cos_le_one (t * ‖z‖)) (sq_nonneg ‖z‖)
      · rw [abs_mul, abs_of_nonneg (norm_nonneg z)]
        have hsin := mul_le_mul_of_nonneg_left
          (Real.abs_sin_le_one (t * ‖z‖)) (norm_nonneg z)
        nlinarith [norm_nonneg z]
    _ = 2 * ‖z‖ ^ (2 : ℕ) := by ring

/-- The first four derivatives of the signed unit-sphere geodesic, together
with uniform norm bounds for a unit base point.  The explicit nonzero-velocity
hypothesis is needed only for the displayed closed form of the geodesic; the
zero-velocity curve is constant. -/
theorem unitSphereGeodesic_derivatives_and_bounds
    {w z : E} (hw : ‖w‖ = 1) (hz : z ≠ 0) (t : ℝ) :
    (HasDerivAt (unitSphereGeodesic w z)
        ((-(‖z‖ * Real.sin (t * ‖z‖))) • w +
          Real.cos (t * ‖z‖) • z) t ∧
      HasDerivAt
        (fun s : ℝ =>
          (-(‖z‖ * Real.sin (s * ‖z‖))) • w +
            Real.cos (s * ‖z‖) • z)
        ((-(‖z‖ ^ (2 : ℕ) * Real.cos (t * ‖z‖))) • w +
          (-(‖z‖ * Real.sin (t * ‖z‖))) • z) t ∧
      HasDerivAt
        (fun s : ℝ =>
          (-(‖z‖ ^ (2 : ℕ) * Real.cos (s * ‖z‖))) • w +
            (-(‖z‖ * Real.sin (s * ‖z‖))) • z)
        ((‖z‖ ^ (3 : ℕ) * Real.sin (t * ‖z‖)) • w +
          (-(‖z‖ ^ (2 : ℕ) * Real.cos (t * ‖z‖))) • z) t ∧
      HasDerivAt
        (fun s : ℝ =>
          (‖z‖ ^ (3 : ℕ) * Real.sin (s * ‖z‖)) • w +
            (-(‖z‖ ^ (2 : ℕ) * Real.cos (s * ‖z‖))) • z)
        ((‖z‖ ^ (4 : ℕ) * Real.cos (t * ‖z‖)) • w +
          (‖z‖ ^ (3 : ℕ) * Real.sin (t * ‖z‖)) • z) t) ∧
    (‖(-(‖z‖ * Real.sin (t * ‖z‖))) • w +
          Real.cos (t * ‖z‖) • z‖ ≤ 2 * ‖z‖ ∧
      ‖(-(‖z‖ ^ (2 : ℕ) * Real.cos (t * ‖z‖))) • w +
          (-(‖z‖ * Real.sin (t * ‖z‖))) • z‖ ≤
        2 * ‖z‖ ^ (2 : ℕ) ∧
      ‖(‖z‖ ^ (3 : ℕ) * Real.sin (t * ‖z‖)) • w +
          (-(‖z‖ ^ (2 : ℕ) * Real.cos (t * ‖z‖))) • z‖ ≤
        2 * ‖z‖ ^ (3 : ℕ) ∧
      ‖(‖z‖ ^ (4 : ℕ) * Real.cos (t * ‖z‖)) • w +
          (‖z‖ ^ (3 : ℕ) * Real.sin (t * ‖z‖)) • z‖ ≤
        2 * ‖z‖ ^ (4 : ℕ)) := by
  constructor
  · exact ⟨unitSphereGeodesic_hasDerivAt w hz t,
      unitSphereGeodesic_velocity_hasDerivAt w z t,
      unitSphereGeodesic_acceleration_hasDerivAt w z t,
      unitSphereGeodesic_jerk_hasDerivAt w z t⟩
  · exact ⟨unitSphereGeodesic_first_derivative_norm_le hw t,
      unitSphereGeodesic_second_derivative_norm_le hw t,
      unitSphereGeodesic_third_derivative_norm_le hw t,
      unitSphereGeodesic_fourth_derivative_norm_le hw t⟩
/-- A tangent exponential-map step preserves unit norm exactly. -/
theorem unitSphereExp_norm_eq_one
    {w z : E}
    (hw : ‖w‖ = 1)
    (htan : ⟪w, z⟫_ℝ = 0) :
    ‖unitSphereExp w z‖ = 1 := by
  by_cases hz : z = 0
  · subst z
    simp [unitSphereExp, hw]
  · have hr : ‖z‖ ≠ 0 := norm_ne_zero_iff.mpr hz
    have hcross :
        ⟪Real.cos ‖z‖ • w, Real.sinc ‖z‖ • z⟫_ℝ = 0 := by
      simp [real_inner_smul_left, real_inner_smul_right, htan]
    have hpyth :
        ‖unitSphereExp w z‖ ^ (2 : ℕ) =
          ‖Real.cos ‖z‖ • w‖ ^ (2 : ℕ) +
          ‖Real.sinc ‖z‖ • z‖ ^ (2 : ℕ) := by
      rw [unitSphereExp, norm_add_sq_real, hcross]
      ring
    have hfirst :
        ‖Real.cos ‖z‖ • w‖ ^ (2 : ℕ) =
          Real.cos ‖z‖ ^ (2 : ℕ) := by
      simp [norm_smul, hw, sq_abs]
    have hsinc :
        Real.sinc ‖z‖ = Real.sin ‖z‖ / ‖z‖ :=
      Real.sinc_of_ne_zero hr
    have hsecond :
        ‖Real.sinc ‖z‖ • z‖ ^ (2 : ℕ) =
          Real.sin ‖z‖ ^ (2 : ℕ) := by
      rw [norm_smul, Real.norm_eq_abs, hsinc]
      have hrpos : 0 < ‖z‖ := norm_pos_iff.mpr hz
      rw [abs_div, abs_of_pos hrpos]
      rw [div_mul_cancel₀ _ hr]
      exact sq_abs (Real.sin ‖z‖)
    have hsq : ‖unitSphereExp w z‖ ^ (2 : ℕ) = 1 := by
      rw [hpyth, hfirst, hsecond]
      nlinarith [Real.sin_sq_add_cos_sq ‖z‖]
    have hnonneg : 0 ≤ ‖unitSphereExp w z‖ := norm_nonneg _
    nlinarith


end

end AutoSamplingTheory.TechnicalLemmas.Geometry.UnitSphere
