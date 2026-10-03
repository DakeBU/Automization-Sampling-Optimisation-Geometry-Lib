import AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.BrownianQuadraticVariation
import AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.GaussianFourthMoment
import Mathlib.Probability.Moments.Variance
import Mathlib.Tactic

/-!
# Brownian quadratic variation in `L²`

This module upgrades the finite-grid mean identity for Brownian quadratic
variation to an exact mean-square identity.  For a deterministic monotone grid
`t₀ ≤ ⋯ ≤ tₙ`, the compensated error

`Q = ∑ᵢ ((B(tᵢ₊₁) - B(tᵢ))² - (tᵢ₊₁ - tᵢ))`

satisfies `E[Q²] = 2 ∑ᵢ (tᵢ₊₁ - tᵢ)²`.  The proof uses the
Gaussian fourth moment and independence of disjoint Brownian increments.  A
mesh bound is then immediate and is the reusable analytic input for dyadic
quadratic-variation convergence.
-/

namespace AutoSamplingTheory
namespace TechnicalLemmas
namespace StochasticProcesses
namespace BrownianQuadraticVariationL2

open MeasureTheory ProbabilityTheory Set
open scoped BigOperators NNReal

open BrownianMotion BrownianQuadraticVariation GaussianFourthMoment

variable {Omega : Type*} {m : MeasurableSpace Omega}
  {mu : Measure Omega} {B : ℝ≥0 → Omega → ℝ}

/-- A future Brownian increment has the centered Gaussian law with variance
equal to the elapsed time. -/
private theorem increment_hasLaw
    (hB : IsPreBrownianReal B mu)
    (s t : ℝ≥0) :
    HasLaw (fun omega => B t omega - B s omega)
      (gaussianReal 0 (nndist (t : ℝ) (s : ℝ))) mu := by
  have h := hB.hasLaw_sub t s
  convert h using 1
  · ext omega
    rfl
  · rfl

private theorem coe_nndist_eq_elapsed {s t : ℝ≥0} (hst : s ≤ t) :
    ((nndist (t : ℝ) (s : ℝ) : ℝ≥0) : ℝ) = ((t - s : ℝ≥0) : ℝ) := by
  rw [coe_nndist, Real.dist_eq, abs_of_nonneg]
  · exact (NNReal.coe_sub hst).symm
  · exact sub_nonneg.mpr (by exact_mod_cast hst)

/-- Fourth moment of one Brownian increment. -/
private theorem integral_increment_pow_four
    (hB : IsPreBrownianReal B mu)
    {s t : ℝ≥0} (hst : s ≤ t) :
    ∫ omega, (B t omega - B s omega) ^ 4 ∂mu =
      3 * (((t - s : ℝ≥0) : ℝ) ^ 2) := by
  calc
    ∫ omega, (B t omega - B s omega) ^ 4 ∂mu =
        ∫ x : ℝ, x ^ 4 ∂(gaussianReal 0 (nndist (t : ℝ) (s : ℝ))) := by
      simpa only [Function.comp_apply] using
        (increment_hasLaw hB s t).integral_comp
          (f := fun x : ℝ => x ^ 4) (by fun_prop)
    _ = 3 * (((t - s : ℝ≥0) : ℝ) ^ 2) := by
      rw [integral_pow_four_gaussianReal_zero, coe_nndist_eq_elapsed hst]

/-- Second moment of one Brownian increment, derived only from its Gaussian
law. -/
private theorem integral_increment_sq
    (hB : IsPreBrownianReal B mu)
    {s t : ℝ≥0} (hst : s ≤ t) :
    ∫ omega, (B t omega - B s omega) ^ 2 ∂mu =
      ((t - s : ℝ≥0) : ℝ) := by
  have htransport :
      ∫ omega, (B t omega - B s omega) ^ 2 ∂mu =
        ∫ x : ℝ, x ^ 2 ∂(gaussianReal 0 (nndist (t : ℝ) (s : ℝ))) := by
    simpa only [Function.comp_apply] using
      (increment_hasLaw hB s t).integral_comp
        (f := fun x : ℝ => x ^ 2) (by fun_prop)
  have hv := variance_fun_id_gaussianReal
    (μ := (0 : ℝ)) (v := nndist (t : ℝ) (s : ℝ))
  rw [variance_of_integral_eq_zero (by fun_prop)
      (integral_id_gaussianReal (μ := (0 : ℝ))
        (v := nndist (t : ℝ) (s : ℝ)))] at hv
  exact htransport.trans (by simpa [coe_nndist_eq_elapsed hst] using hv)

/-- A Brownian increment is square-integrable under the pre-Brownian
contract. -/
private theorem increment_sq_integrable
    (hB : IsPreBrownianReal B mu) (s t : ℝ≥0) :
    Integrable (fun omega => (B t omega - B s omega) ^ 2) mu := by
  have hmem : MemLp (fun omega => B t omega - B s omega) 2 mu :=
    hB.isGaussianProcess.hasGaussianLaw_fun_sub.memLp_two
  exact hmem.integrable_sq

/-- The compensated squared increment has mean zero. -/
private theorem integral_centered_increment_sq_eq_zero
    (hB : IsPreBrownianReal B mu)
    {s t : ℝ≥0} (hst : s ≤ t) :
    ∫ omega,
        ((B t omega - B s omega) ^ 2 - ((t - s : ℝ≥0) : ℝ)) ∂mu = 0 := by
  let _ : IsProbabilityMeasure mu := hB.isGaussianProcess.isProbabilityMeasure
  rw [integral_sub (increment_sq_integrable hB s t) (integrable_const _),
    integral_increment_sq hB hst, integral_const]
  simp

/-- A compensated squared Brownian increment is square-integrable. -/
private theorem centered_increment_sq_memLp_two
    (hB : IsPreBrownianReal B mu)
    (s t : ℝ≥0) :
    MemLp
      (fun omega =>
        (B t omega - B s omega) ^ 2 - ((t - s : ℝ≥0) : ℝ))
      2 mu := by
  let _ : IsProbabilityMeasure mu := hB.isGaussianProcess.isProbabilityMeasure
  let X : Omega → ℝ := fun omega => B t omega - B s omega
  let d : ℝ := ((t - s : ℝ≥0) : ℝ)
  have hX4 : Integrable (fun omega => X omega ^ 4) mu := by
    have hX : MemLp X 4 mu :=
      hB.isGaussianProcess.hasGaussianLaw_fun_sub.memLp (p := 4) (by norm_num)
    have hnorm := hX.integrable_norm_pow' (p := 4)
    exact hnorm.congr (ae_of_all mu fun omega => by
      simp only [Real.norm_eq_abs]
      rw [← abs_pow]
      exact abs_of_nonneg (by positivity))
  have hX2 : Integrable (fun omega => X omega ^ 2) mu :=
    increment_sq_integrable hB s t
  have hincmeas : AEStronglyMeasurable
      (fun omega => B t omega - B s omega) mu :=
    (hB.aemeasurable t).aestronglyMeasurable.sub
      (hB.aemeasurable s).aestronglyMeasurable
  have hmeas : AEStronglyMeasurable
      (fun omega =>
        (B t omega - B s omega) ^ 2 - ((t - s : ℝ≥0) : ℝ)) mu :=
    (hincmeas.pow 2).sub aestronglyMeasurable_const
  apply (memLp_two_iff_integrable_sq hmeas).2
  have hpoly : (fun omega => (X omega ^ 2 - d) ^ 2) =
      fun omega => X omega ^ 4 - (2 * d) * X omega ^ 2 + d ^ 2 := by
    funext omega
    ring
  rw [hpoly]
  exact (hX4.sub (hX2.const_mul _)).add (integrable_const _)

/-- Exact second moment of one compensated squared Brownian increment. -/
private theorem integral_centered_increment_sq_sq
    (hB : IsPreBrownianReal B mu)
    {s t : ℝ≥0} (hst : s ≤ t) :
    ∫ omega,
        ((B t omega - B s omega) ^ 2 - ((t - s : ℝ≥0) : ℝ)) ^ 2 ∂mu =
      2 * (((t - s : ℝ≥0) : ℝ) ^ 2) := by
  let _ : IsProbabilityMeasure mu := hB.isGaussianProcess.isProbabilityMeasure
  have h4 := integral_increment_pow_four hB hst
  have h2 := integral_increment_sq hB hst
  have h4int : Integrable (fun omega => (B t omega - B s omega) ^ 4) mu := by
    have hmem : MemLp (fun omega => B t omega - B s omega) 4 mu :=
      hB.isGaussianProcess.hasGaussianLaw_fun_sub.memLp (p := 4) (by norm_num)
    have hn := hmem.integrable_norm_pow' (p := 4)
    exact hn.congr (ae_of_all mu fun omega => by
      simp only [Real.norm_eq_abs]
      rw [← abs_pow]
      exact abs_of_nonneg (by positivity))
  have h2int := (increment_sq_integrable hB s t).const_mul
    (2 * ((t - s : ℝ≥0) : ℝ))
  have hcint : Integrable (fun _ : Omega => ((t - s : ℝ≥0) : ℝ) ^ 2) mu :=
    integrable_const _
  rw [show (fun omega =>
      ((B t omega - B s omega) ^ 2 - ((t - s : ℝ≥0) : ℝ)) ^ 2) =
      fun omega => (B t omega - B s omega) ^ 4 -
        (2 * ((t - s : ℝ≥0) : ℝ)) *
          (B t omega - B s omega) ^ 2 +
        ((t - s : ℝ≥0) : ℝ) ^ 2 by
      funext omega
      ring]
  calc
    ∫ omega, (B t omega - B s omega) ^ 4 -
          (2 * ((t - s : ℝ≥0) : ℝ)) * (B t omega - B s omega) ^ 2 +
          ((t - s : ℝ≥0) : ℝ) ^ 2 ∂mu =
        (∫ omega, (B t omega - B s omega) ^ 4 ∂mu) -
          ∫ omega, (2 * ((t - s : ℝ≥0) : ℝ)) *
            (B t omega - B s omega) ^ 2 ∂mu +
          ∫ _ : Omega, ((t - s : ℝ≥0) : ℝ) ^ 2 ∂mu := by
            let A : Omega → ℝ := fun omega => (B t omega - B s omega) ^ 4
            let C : Omega → ℝ := fun omega =>
              (2 * ((t - s : ℝ≥0) : ℝ)) * (B t omega - B s omega) ^ 2
            let K : Omega → ℝ := fun _ => ((t - s : ℝ≥0) : ℝ) ^ 2
            have hA : Integrable A mu := h4int
            have hC : Integrable C mu := h2int
            have hK : Integrable K mu := hcint
            change ∫ omega, ((A - C) + K) omega ∂mu =
              (∫ omega, A omega ∂mu) - (∫ omega, C omega ∂mu) +
                ∫ omega, K omega ∂mu
            calc
              ∫ omega, ((A - C) + K) omega ∂mu =
                  (∫ omega, (A - C) omega ∂mu) + ∫ omega, K omega ∂mu := by
                    simpa only [Pi.add_apply] using integral_add (hA.sub hC) hK
              _ = (∫ omega, A omega ∂mu) - (∫ omega, C omega ∂mu) +
                    ∫ omega, K omega ∂mu := by
                    rw [show (∫ omega, (A - C) omega ∂mu) =
                        (∫ omega, A omega ∂mu) - ∫ omega, C omega ∂mu by
                      simpa only [Pi.sub_apply] using integral_sub hA hC]
    _ = 2 * (((t - s : ℝ≥0) : ℝ) ^ 2) := by
      rw [h4, integral_const_mul, h2, integral_const]
      simp
      ring

private theorem grid_cell_le
    {n : ℕ} {times : Fin (n + 1) → ℝ≥0}
    (hmono : Monotone times) (i : Fin n) :
    times i.castSucc ≤ times i.succ :=
  hmono Fin.castSucc_lt_succ.le

/-- The compensated squared increments on a deterministic monotone grid are
jointly independent. -/
private theorem iIndepFun_centeredSquaredIncrement
    (hB : IsPreBrownianReal B mu)
    {n : ℕ} {times : Fin (n + 1) → ℝ≥0}
    (hmono : Monotone times) :
    iIndepFun (fun i : Fin n => centeredSquaredIncrement B times i) mu := by
  have hinc : iIndepFun
      (fun i : Fin n => fun omega =>
        B (times i.succ) omega - B (times i.castSucc) omega) mu :=
    hB.hasIndepIncrements n times (fun _ _ hij => hmono hij)
  have hcomp := hinc.comp
    (fun i : Fin n => fun x : ℝ => x ^ 2 -
      ((times i.succ - times i.castSucc : ℝ≥0) : ℝ))
    (fun _ => by fun_prop)
  change iIndepFun
    (fun i : Fin n => fun omega =>
      (B (times i.succ) omega - B (times i.castSucc) omega) ^ 2 -
        ((times i.succ - times i.castSucc : ℝ≥0) : ℝ)) mu
  convert hcomp using 1
  funext i omega
  rfl

/-- Exact finite-grid `L²` error identity for Brownian quadratic variation. -/
theorem integral_quadraticVariationError_sq
    (hB : IsPreBrownianReal B mu)
    {n : ℕ} {times : Fin (n + 1) → ℝ≥0}
    (hmono : Monotone times) :
    ∫ omega, (quadraticVariationError B times omega) ^ 2 ∂mu =
      2 * ∑ i : Fin n,
        (((times i.succ - times i.castSucc : ℝ≥0) : ℝ) ^ 2) := by
  let _ : IsProbabilityMeasure mu := hB.isGaussianProcess.isProbabilityMeasure
  let Y : Fin n → Omega → ℝ := fun i => centeredSquaredIncrement B times i
  have hYmem : ∀ i, MemLp (Y i) 2 mu := fun i => by
    change MemLp
      (fun omega =>
        (B (times i.succ) omega - B (times i.castSucc) omega) ^ 2 -
          ((times i.succ - times i.castSucc : ℝ≥0) : ℝ)) 2 mu
    simpa only using
      centered_increment_sq_memLp_two hB _ _
  have hYind : Set.Pairwise (↑(Finset.univ : Finset (Fin n)) : Set (Fin n))
      (fun i j => Y i ⟂ᵢ[mu] Y j) := by
    intro i _ j _ hij
    exact (iIndepFun_centeredSquaredIncrement hB hmono).indepFun hij
  have hvar := ProbabilityTheory.IndepFun.variance_sum
    (s := Finset.univ) (X := Y) (fun i _ => hYmem i) hYind
  have hsumMem : MemLp (∑ i : Fin n, Y i) 2 mu :=
    memLp_finsetSum' Finset.univ (fun i _ => hYmem i)
  have hmean : ∫ omega, (∑ i : Fin n, Y i) omega ∂mu = 0 := by
    calc
      ∫ omega, (∑ i : Fin n, Y i) omega ∂mu =
          ∫ omega, ∑ i ∈ (Finset.univ : Finset (Fin n)), Y i omega ∂mu := by
            congr 1
            funext omega
            simp only [Finset.sum_apply]
      _ = ∑ i ∈ (Finset.univ : Finset (Fin n)), ∫ omega, Y i omega ∂mu := by
        rw [integral_finsetSum]
        intro i _
        exact (hYmem i).integrable (by norm_num)
      _ = 0 := by
        apply Finset.sum_eq_zero
        intro i _
        simpa [Y, centeredSquaredIncrement] using
          integral_centered_increment_sq_eq_zero hB (grid_cell_le hmono i)
  rw [variance_of_integral_eq_zero hsumMem.aemeasurable hmean] at hvar
  change ∫ omega, (∑ i : Fin n, centeredSquaredIncrement B times i omega) ^ 2 ∂mu = _
  change ∫ omega, (∑ i : Fin n, Y i omega) ^ 2 ∂mu = _
  rw [show (∫ omega, (∑ i : Fin n, Y i omega) ^ 2 ∂mu) =
      ∑ i : Fin n, Var[Y i; mu] by
    simpa only [Finset.sum_apply] using hvar]
  rw [Finset.mul_sum]
  apply Finset.sum_congr rfl
  intro i _
  have hYiMean : ∫ omega, Y i omega ∂mu = 0 := by
    simpa [Y, centeredSquaredIncrement] using
      integral_centered_increment_sq_eq_zero hB (grid_cell_le hmono i)
  rw [variance_of_integral_eq_zero (hYmem i).aemeasurable hYiMean]
  simpa [Y, centeredSquaredIncrement] using
    integral_centered_increment_sq_sq hB (grid_cell_le hmono i)

end BrownianQuadraticVariationL2
end StochasticProcesses
end TechnicalLemmas
end AutoSamplingTheory
