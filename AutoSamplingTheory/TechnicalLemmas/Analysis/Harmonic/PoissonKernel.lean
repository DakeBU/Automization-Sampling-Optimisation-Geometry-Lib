import AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.LaplacianProduct
import AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.RadialCalculus
import Mathlib.Analysis.InnerProductSpace.Calculus
import Mathlib.Analysis.InnerProductSpace.Harmonic.Basic
import Mathlib.Analysis.SpecialFunctions.Pow.Deriv

/-!
# The actual spherical Poisson kernel away from its unit pole

HFT, second edition, Proposition 1.18 (printed page 13 / PDF page 21),
with the source standing dimension n > 1. The kernel is the literal quotient
from Eq. 1.15, with the pole fixed and the first argument varying over its
entire complement. Factor regularity and every derivative/cancellation are
proved internally using the canonical local Laplacian product rule.

The source leaves this computation to the reader. No surface integral,
mean-value formula, Gaussian Eq. 24, TV separation or oracle bound is claimed.
-/

open Filter
open scoped RealInnerProductSpace Topology
namespace AutoSamplingTheory.TechnicalLemmas.Analysis.Harmonic.PoissonKernel
set_option autoImplicit false
variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
omit [InnerProductSpace ℝ E] in
private theorem inv_norm_pow_eq_rpow (z a : E) (n : ℕ) :
    (‖z - a‖ ^ n)⁻¹ = (‖z - a‖ ^ 2) ^ (-(n : ℝ) / 2) := by
  calc
    (‖z - a‖ ^ n)⁻¹ = ‖z - a‖ ^ (-(n : ℝ)) := by
      rw [Real.rpow_neg (norm_nonneg _), Real.rpow_natCast]
    _ = (‖z - a‖ ^ 2) ^ (-(n : ℝ) / 2) := by
      rw [← Real.rpow_natCast, ← Real.rpow_mul (norm_nonneg _)]
      congr 1
      ring_nf
private theorem numerator_calculus [FiniteDimensional ℝ E] (x : E) :
    gradient (fun z : E => (1 : ℝ) - ‖z‖ ^ 2) x = (-2 : ℝ) • x ∧
    Laplacian.laplacian (fun z : E => (1 : ℝ) - ‖z‖ ^ 2) x = (-2 : ℝ) * (Module.finrank ℝ E : ℝ) := by
  have h := AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.RadialCalculus.radial_gradient_laplacian
    (fun s : ℝ => (1 : ℝ) - s) (0 : E) x (by fun_prop)
  simpa [mul_comm, mul_left_comm] using h
private theorem poisson_laplace_zero {n : ℕ} {ζ x : EuclideanSpace ℝ (Fin n)}
    (hζ : ‖ζ‖ = 1) (hx : x ≠ ζ) :
    Laplacian.laplacian (fun z : EuclideanSpace ℝ (Fin n) =>
      ((1 : ℝ) - ‖z‖ ^ 2) / ‖z - ζ‖ ^ n) x = 0 := by
  let p : ℝ := -(n : ℝ) / 2
  let u : EuclideanSpace ℝ (Fin n) → ℝ := fun z => 1 - ‖z‖ ^ 2
  let v : EuclideanSpace ℝ (Fin n) → ℝ := fun z => (‖z - ζ‖ ^ 2) ^ p
  have hn : ‖x - ζ‖ ^ 2 ≠ 0 := pow_ne_zero 2 (norm_ne_zero_iff.mpr (sub_ne_zero.mpr hx))
  have hu : ContDiffAt ℝ 2 u x := contDiffAt_const.sub (contDiffAt_id.norm_sq ℝ)
  have hv : ContDiffAt ℝ 2 v x :=
    ((contDiffAt_id.sub contDiffAt_const).norm_sq ℝ).rpow_const_of_ne hn
  have hfun : (fun z : EuclideanSpace ℝ (Fin n) => ((1 : ℝ) - ‖z‖ ^ 2) / ‖z - ζ‖ ^ n) =
      fun z => u z * v z := by
    funext z
    simp only [div_eq_mul_inv, u, v, p, inv_norm_pow_eq_rpow]
  have he (q : ℝ) : (‖x - ζ‖ ^ 2) ^ q = (‖x - ζ‖ ^ 2) ^ (q - 1) * (‖x - ζ‖ ^ 2) := by
    calc
      _ = (‖x - ζ‖ ^ 2) ^ ((q - 1) + 1) := by congr 1; ring_nf
      _ = _ := Real.rpow_add_one hn (q - 1)
  have hr := AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.RadialCalculus.radial_gradient_laplacian
    (fun s : ℝ => s ^ p) ζ x (Real.contDiffAt_rpow_const_of_ne hn)
  simp only [Real.deriv_rpow_const', deriv_const_mul_field, Real.deriv_rpow_const] at hr
  have hgrad : gradient v x = (2 * p * (‖x - ζ‖ ^ 2) ^ (p - 1)) • (x - ζ) := by
    simpa [mul_assoc] using hr.1
  have hlv : Laplacian.laplacian v x = 2 * (n : ℝ) * (‖x - ζ‖ ^ 2) ^ (p - 1) := by
    change Laplacian.laplacian (fun z => (‖z - ζ‖ ^ 2) ^ p) x = _
    rw [hr.2]
    simp only [finrank_euclideanSpace_fin]
    have hpow : (‖x - ζ‖ ^ 2) ^ (p - 1 - 1) * (‖x - ζ‖ ^ 2) =
        (‖x - ζ‖ ^ 2) ^ (p - 1) := by
      rw [← Real.rpow_add_one hn]
      congr 1
      ring
    calc
      _ = 4 * p * (p - 1) * ((‖x - ζ‖ ^ 2) ^ (p - 1 - 1) * (‖x - ζ‖ ^ 2)) +
          2 * (n : ℝ) * p * (‖x - ζ‖ ^ 2) ^ (p - 1) := by ring
      _ = _ := by rw [hpow]; dsimp [p]; ring
  have hcancel : 1 - ‖x‖ ^ 2 + 2 * inner ℝ x (x - ζ) - ‖x - ζ‖ ^ 2 = 0 := by
    rw [norm_sub_sq_real]
    simp only [inner_sub_right, real_inner_self_eq_norm_sq, hζ]
    ring_nf
  rw [hfun, AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.LaplacianProduct.laplacian_mul hu hv]
  rw [hlv, hgrad, (numerator_calculus x).1, (numerator_calculus x).2]
  simp only [finrank_euclideanSpace_fin, real_inner_smul_left, inner_smul_right]
  dsimp only [u, v]
  rw [he p]
  calc
    _ = (2 * (n : ℝ) * (‖x - ζ‖ ^ 2) ^ (p - 1)) *
        (1 - ‖x‖ ^ 2 + 2 * inner ℝ x (x - ζ) - ‖x - ζ‖ ^ 2) := by dsimp [p]; ring_nf
    _ = 0 := by rw [hcancel]; ring_nf
/-- HFT Proposition 1.18: the literal unit-pole Poisson kernel is harmonic
in a neighborhood of every point of the pole complement. -/
theorem poissonKernel_harmonicOnNhd {n : ℕ} (hn : 2 ≤ n)
    (ζ : EuclideanSpace ℝ (Fin n)) (hζ : ‖ζ‖ = 1) :
    InnerProductSpace.HarmonicOnNhd
      (fun x : EuclideanSpace ℝ (Fin n) => (1 - ‖x‖ ^ 2) / ‖x - ζ‖ ^ n)
      ({ζ}ᶜ : Set (EuclideanSpace ℝ (Fin n))) := by
  clear hn
  intro x hx
  have hne : x ≠ ζ := by simpa using hx
  constructor
  · have hu : ContDiffAt ℝ 2 (fun z : EuclideanSpace ℝ (Fin n) => (1 : ℝ) - ‖z‖ ^ 2) x :=
      contDiffAt_const.sub (contDiffAt_id.norm_sq ℝ)
    have hv : ContDiffAt ℝ 2 (fun z : EuclideanSpace ℝ (Fin n) => ‖z - ζ‖ ^ n) x :=
      ((contDiffAt_id.sub contDiffAt_const).norm ℝ (sub_ne_zero.mpr hne)).pow n
    exact hu.div hv (pow_ne_zero n (norm_ne_zero_iff.mpr (sub_ne_zero.mpr hne)))
  · filter_upwards [eventually_ne_nhds hne] with z hz
    exact poisson_laplace_zero hζ hz
end AutoSamplingTheory.TechnicalLemmas.Analysis.Harmonic.PoissonKernel
