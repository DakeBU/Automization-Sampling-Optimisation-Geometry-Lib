import AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.RadialCalculus
import Mathlib.Analysis.InnerProductSpace.Harmonic.Basic
import Mathlib.Analysis.SpecialFunctions.Pow.Deriv
import Mathlib.Analysis.SpecialFunctions.Log.Deriv

/-!
The literal power/log Green test functions used in HFT, second edition,
printed pages 2 and 5 (PDF pages 10 and 13). The source omits these calculus
computations. The all-positive-radius boundary formula below is an explicit
ASTIS expansion. No distributional normalization, geometric annulus normal,
Green identity, zero flux or mean-value theorem is claimed here.
-/

open Filter
open scoped Topology RealInnerProductSpace
namespace AutoSamplingTheory.TechnicalLemmas.Analysis.Harmonic.FundamentalSolution
set_option autoImplicit false
open AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.RadialCalculus
variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
  [FiniteDimensional ℝ E]

omit [InnerProductSpace ℝ E] [FiniteDimensional ℝ E] in
private theorem power_sq_profile (q : ℝ) :
    (fun z : E => ‖z‖ ^ q) = (fun z : E => (‖z‖ ^ 2) ^ (q / 2)) := by
  funext z
  rw [← Real.rpow_natCast, ← Real.rpow_mul (norm_nonneg _)]
  congr 1
  ring

private theorem power_data (q : ℝ) (x : E) (hx : x ≠ 0) :
    ContDiffAt ℝ 2 (fun z : E => ‖z‖ ^ q) x ∧
    gradient (fun z : E => ‖z‖ ^ q) x = (q * ‖x‖ ^ (q - 2)) • x ∧
    Laplacian.laplacian (fun z : E => ‖z‖ ^ q) x =
      q * (q + (Module.finrank ℝ E : ℝ) - 2) * ‖x‖ ^ (q - 2) := by
  have hn : ‖x‖ ≠ 0 := norm_ne_zero_iff.mpr hx
  have hS : ‖x‖ ^ 2 ≠ 0 := pow_ne_zero 2 hn
  let p : ℝ := q / 2
  have hc : ContDiffAt ℝ 2 (fun s : ℝ => s ^ p) (‖x‖ ^ 2) :=
    Real.contDiffAt_rpow_const_of_ne hS
  have hb := radial_gradient_laplacian (fun s : ℝ => s ^ p) (0 : E) x (by simpa using hc)
  simp only [sub_zero, Real.deriv_rpow_const', deriv_const_mul_field,
    Real.deriv_rpow_const] at hb
  have hp : (‖x‖ ^ 2) ^ (p - 1) = ‖x‖ ^ (q - 2) := by
    rw [← Real.rpow_natCast, ← Real.rpow_mul (norm_nonneg _)]
    congr 1
    dsimp [p]
    ring
  have he : (‖x‖ ^ 2) ^ (p - 2) * (‖x‖ ^ 2) = (‖x‖ ^ 2) ^ (p - 1) := by
    rw [← Real.rpow_add_one hS]
    congr 1
    ring
  refine ⟨(contDiffAt_id.norm ℝ hx).rpow_const_of_ne hn, ?_, ?_⟩
  · rw [power_sq_profile q]
    convert hb.1 using 1
    rw [hp]
    congr 1
    dsimp [p]
    ring
  · rw [power_sq_profile q]
    calc
      _ = 4 * (‖x‖ ^ 2) * (p * ((p - 1) * (‖x‖ ^ 2) ^ (p - 1 - 1))) +
          2 * (Module.finrank ℝ E : ℝ) * (p * (‖x‖ ^ 2) ^ (p - 1)) := hb.2
      _ = (2 * p * (2 * p + (Module.finrank ℝ E : ℝ) - 2)) *
          (‖x‖ ^ 2) ^ (p - 1) := by
        rw [show p - 1 - 1 = p - 2 by ring]
        calc
          _ = 4 * p * (p - 1) * ((‖x‖ ^ 2) ^ (p - 2) * (‖x‖ ^ 2)) +
              2 * (Module.finrank ℝ E : ℝ) * p * (‖x‖ ^ 2) ^ (p - 1) := by ring
          _ = _ := by rw [he]; ring
      _ = _ := by rw [hp]; dsimp [p]; ring

omit [InnerProductSpace ℝ E] [FiniteDimensional ℝ E] in
private theorem log_sq_profile :
    (fun z : E => Real.log ‖z‖) = (fun z : E => (1 / 2 : ℝ) * Real.log (‖z‖ ^ 2)) := by
  funext z
  rw [Real.log_pow]
  ring

private theorem log_data (x : E) (hx : x ≠ 0) :
    ContDiffAt ℝ 2 (fun z : E => Real.log ‖z‖) x ∧
    gradient (fun z : E => Real.log ‖z‖) x = (‖x‖ ^ 2)⁻¹ • x ∧
    Laplacian.laplacian (fun z : E => Real.log ‖z‖) x =
      ((Module.finrank ℝ E : ℝ) - 2) * (‖x‖ ^ 2)⁻¹ := by
  have hn : ‖x‖ ≠ 0 := norm_ne_zero_iff.mpr hx
  have hS : ‖x‖ ^ 2 ≠ 0 := pow_ne_zero 2 hn
  have hc : ContDiffAt ℝ 2 (fun s : ℝ => (1 / 2 : ℝ) * Real.log s) (‖x‖ ^ 2) :=
    contDiffAt_const.mul (Real.contDiffAt_log.mpr hS)
  have hb := radial_gradient_laplacian (fun s : ℝ => (1 / 2 : ℝ) * Real.log s)
    (0 : E) x (by simpa using hc)
  simp only [sub_zero, deriv_const_mul_field', Real.deriv_log', deriv_const_mul_field,
    deriv_inv] at hb
  refine ⟨(contDiffAt_id.norm ℝ hx).log hn, ?_, ?_⟩
  · rw [log_sq_profile]
    convert hb.1 using 1
    congr 1
    ring
  · rw [log_sq_profile, hb.2]
    field_simp [hS]
    ring

/-- HFT's power/log test functions are harmonic away from the origin, with
their literal values and outward radial derivative on every positive sphere.
The all-radius bundle expands computations omitted by the source. -/
theorem fundamentalSolution_boundary_data {n : ℕ} (hn : 2 ≤ n) :
    let F : EuclideanSpace ℝ (Fin n) → ℝ := fun x =>
      if n = 2 then Real.log ‖x‖ else ‖x‖ ^ ((2 : ℝ) - (n : ℝ))
    InnerProductSpace.HarmonicOnNhd F ({0}ᶜ : Set (EuclideanSpace ℝ (Fin n))) ∧
    ∀ R : ℝ, 0 < R → ∀ x : EuclideanSpace ℝ (Fin n), ‖x‖ = R →
      F x = (if n = 2 then Real.log R else R ^ ((2 : ℝ) - (n : ℝ))) ∧
      inner ℝ (gradient F x) (R⁻¹ • x) =
        (if n = 2 then R⁻¹ else ((2 : ℝ) - (n : ℝ)) * R ^ ((1 : ℝ) - (n : ℝ))) := by
  dsimp only
  rcases eq_or_lt_of_le hn with hdim | hdim
  · have hdim : n = 2 := hdim.symm
    simp only [hdim, ↓reduceIte]
    constructor
    · intro x hx
      have hne : x ≠ 0 := by simpa using hx
      refine ⟨(log_data x hne).1, ?_⟩
      filter_upwards [eventually_ne_nhds hne] with z hz
      simpa [hdim] using (log_data z hz).2.2
    · intro R hR x hx
      have hne : x ≠ 0 := norm_ne_zero_iff.mp (by rw [hx]; exact hR.ne')
      refine ⟨by rw [hx], ?_⟩
      rw [(log_data x hne).2.1]
      simp only [real_inner_smul_left, inner_smul_right, real_inner_self_eq_norm_sq, hx]
      field_simp
  · have hdim : n ≠ 2 := ne_of_gt hdim
    simp only [hdim, ↓reduceIte]
    constructor
    · intro x hx
      have hne : x ≠ 0 := by simpa using hx
      refine ⟨(power_data ((2 : ℝ) - (n : ℝ)) x hne).1, ?_⟩
      filter_upwards [eventually_ne_nhds hne] with z hz
      simp [(power_data ((2 : ℝ) - (n : ℝ)) z hz).2.2]
    · intro R hR x hx
      have hne : x ≠ 0 := norm_ne_zero_iff.mp (by rw [hx]; exact hR.ne')
      refine ⟨by rw [hx], ?_⟩
      rw [(power_data ((2 : ℝ) - (n : ℝ)) x hne).2.1]
      simp only [real_inner_smul_left, inner_smul_right, real_inner_self_eq_norm_sq, hx]
      have he : R ^ ((2 : ℝ) - (n : ℝ) - 2) * R = R ^ ((1 : ℝ) - (n : ℝ)) := by
        rw [← Real.rpow_add_one hR.ne']
        congr 1
        ring
      calc
        _ = ((2 : ℝ) - (n : ℝ)) * (R ^ ((2 : ℝ) - (n : ℝ) - 2) * R) := by
          field_simp
        _ = _ := by rw [he]
end AutoSamplingTheory.TechnicalLemmas.Analysis.Harmonic.FundamentalSolution
