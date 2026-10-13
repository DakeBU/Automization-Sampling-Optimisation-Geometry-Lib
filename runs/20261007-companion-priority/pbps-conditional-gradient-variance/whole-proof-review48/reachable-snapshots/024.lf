import Mathlib.Analysis.Calculus.ContDiff.Convolution
import Mathlib.Analysis.Calculus.BumpFunction.Convolution
import Mathlib.Analysis.Calculus.MeanValue

/-!
# Actual ordinary weak zero-gradient is almost everywhere constant

Authored full-space analytic prerequisite for PBPS arXiv:2609.06905v1
Section2.2/AppendixC.1 and SPHMC arXiv:2609.06906v1 Section4.1 background.
True locally integrable rough representatives are mollified using normalized
shrinking compact kernels. Translated C1 compact weak tests kill the genuine
convolution Frechet derivative, and true mean-value constancy plus almost
everywhere convolution convergence gives one real constant. Canonical
full-space connectedness and nonzero Haar volume matter. Dimension0 is included.
No global volume integrability of nonzero constants, classical derivative of
rough input, Gibbs operator, kernel equality, Poincare or paper main is claimed.
-/
set_option autoImplicit false
noncomputable section
open MeasureTheory Filter ContinuousLinearMap
open scoped Topology Convolution ContDiff
namespace AutoSamplingTheory.TechnicalLemmas.Analysis.WeakGradientZero
variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
  [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]

private theorem convolution_derivative_zero
    (u φ : E → ℝ) (hu : LocallyIntegrable u)
    (hφ : ContDiff ℝ 1 φ) (hc : HasCompactSupport φ)
    (hweak : ∀ ψ : E → ℝ, ContDiff ℝ 1 ψ → HasCompactSupport ψ → ∀ a : E,
      Integrable (fun x => u x * fderiv ℝ ψ x a) volume ∧
      (∫ x, u x * fderiv ℝ ψ x a) = 0) (x : E) :
    HasFDerivAt (𝕜 := ℝ) (φ ⋆[lsmul ℝ ℝ (E := ℝ)] u) 0 x := by
  have hder := hc.hasFDerivAt_convolution_left (lsmul ℝ ℝ (E := ℝ)) hφ hu x
  have hzero : ((fderiv ℝ φ ⋆[(lsmul ℝ ℝ (E := ℝ)).precompL E] u) x) = 0 := by
    ext a
    let ψ := fun y : E => φ (x-y)
    have hψ : ContDiff ℝ 1 ψ := hφ.comp (contDiff_const.sub contDiff_id)
    have hψc : HasCompactSupport ψ :=
      hc.comp_homeomorph (IsometryEquiv.subLeft x).toHomeomorph
    have hψD (y : E) : fderiv ℝ ψ y a = -(fderiv ℝ φ (x-y) a) := by
      have h := (hφ.differentiable one_ne_zero (x-y)).hasFDerivAt.comp y
        ((hasFDerivAt_id y).const_sub x)
      change HasFDerivAt ψ _ y at h
      rw [h.fderiv]
      simp
    have hweak0 := (hweak ψ hψ hψc a).2
    simp_rw [hψD] at hweak0
    have hn : (∫ y, u y * fderiv ℝ φ (x-y) a) = 0 := by
      simp_rw [mul_neg,integral_neg] at hweak0
      linarith
    rw [← convolution_flip]
    change (u ⋆[(lsmul ℝ ℝ (E := ℝ)).flip.precompR E] fderiv ℝ φ) x a = 0
    rw [convolution_precompR_apply (lsmul ℝ ℝ (E := ℝ)).flip hu (hc.fderiv ℝ)
      (hφ.continuous_fderiv one_ne_zero)]
    simpa only [convolution_def,flip_apply,lsmul_apply,smul_eq_mul,mul_comm] using hn
  rwa [hzero] at hder

theorem ordinary_weak_zero_gradient_ae_constant
    (u : E → ℝ) (hu : LocallyIntegrable u)
    (hweak : ∀ ψ : E → ℝ, ContDiff ℝ 1 ψ → HasCompactSupport ψ → ∀ a : E,
      Integrable (fun x => u x * fderiv ℝ ψ x a) volume ∧
      (∫ x, u x * fderiv ℝ ψ x a) = 0) :
    ∃ c : ℝ, u =ᵐ[volume] (fun _ => c) := by
  classical
  let ρ : ℕ → ContDiffBump (0 : E) := fun n =>
    {rIn := 1/((n:ℝ)+1), rOut := 2/((n:ℝ)+1),
      rIn_pos := by positivity,
      rIn_lt_rOut := by apply div_lt_div_of_pos_right (by norm_num) (by positivity)}
  have hρ : Tendsto (fun n => (ρ n).rOut) atTop (𝓝 0) :=
    (tendsto_atTop_add_const_right atTop (1:ℝ) tendsto_natCast_atTop_atTop).const_div_atTop 2
  have hratio : ∀ n, (ρ n).rOut ≤ 2*(ρ n).rIn := by intro n; dsimp [ρ]; field_simp; norm_num
  have ht := ContDiffBump.ae_convolution_tendsto_right_of_locallyIntegrable
    (μ := (volume : Measure E)) hρ (Eventually.of_forall hratio) hu
  obtain ⟨x0,hx0⟩ := ht.exists
  refine ⟨u x0,?_⟩
  filter_upwards [ht] with x hx
  have he (n : ℕ) : ((ρ n).normed volume ⋆[lsmul ℝ ℝ] u) x =
      ((ρ n).normed volume ⋆[lsmul ℝ ℝ] u) x0 := by
    apply is_const_of_fderiv_eq_zero (𝕜 := ℝ)
    · intro y
      exact (convolution_derivative_zero u _ hu
        (contDiff_infty.mp (ρ n).contDiff_normed 1) (ρ n).hasCompactSupport_normed hweak y).differentiableAt
    · intro y
      exact (convolution_derivative_zero u _ hu
        (contDiff_infty.mp (ρ n).contDiff_normed 1) (ρ n).hasCompactSupport_normed hweak y).fderiv
  exact tendsto_nhds_unique hx ((tendsto_congr he).mpr hx0)

end AutoSamplingTheory.TechnicalLemmas.Analysis.WeakGradientZero
