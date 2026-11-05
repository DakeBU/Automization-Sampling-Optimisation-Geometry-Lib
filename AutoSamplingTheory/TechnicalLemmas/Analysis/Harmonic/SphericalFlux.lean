import AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.BallFlux
import Mathlib.Analysis.InnerProductSpace.Harmonic.Basic

/-!
Real closed-ball specialization of the zero-flux fact used in HFT1.4.
The one actual harmonic extension is retained at every positive subradius.
The differentiated function is that extension; the original total function is
arbitrary off the closed ball. The boundary law is literal volume.toSphere.
-/

open MeasureTheory Metric Set Filter
open scoped Topology RealInnerProductSpace

namespace AutoSamplingTheory.TechnicalLemmas.Analysis.Harmonic.SphericalFlux

set_option autoImplicit false
noncomputable section

private theorem gradient_c1 {n : ℕ} (v : EuclideanSpace ℝ (Fin n) → ℝ)
    (x : EuclideanSpace ℝ (Fin n)) (hv : ContDiffAt ℝ 2 v x) :
    ContDiffAt ℝ 1 (gradient v) x := by
  unfold gradient
  let L := (InnerProductSpace.toDual ℝ (EuclideanSpace ℝ (Fin n))).symm.toContinuousLinearEquiv
  exact L.contDiff.contDiffAt.comp x (hv.fderiv_right (m := 1) (by norm_num))

private theorem divergence_gradient {n : ℕ} (v : EuclideanSpace ℝ (Fin n) → ℝ)
    (x : EuclideanSpace ℝ (Fin n)) (hv : ContDiffAt ℝ 2 v x) :
    Calculus.Divergence.coordinateDivergence (gradient v) x = Laplacian.laplacian v x := by
  have hgd := ((gradient_c1 v x hv).differentiableAt one_ne_zero).hasFDerivAt
  have hfd := ((hv.fderiv_right (m := 1) (by norm_num)).differentiableAt one_ne_zero).hasFDerivAt
  rw [Calculus.Divergence.coordinateDivergence_eq_sum_fderiv_apply_of_hasFDerivAt hgd,
    InnerProductSpace.laplacian_eq_iteratedFDeriv_orthonormalBasis v
      (EuclideanSpace.basisFun (Fin n) ℝ)]
  apply Finset.sum_congr rfl
  intro i _
  let e := EuclideanSpace.single i (1 : ℝ)
  let π : EuclideanSpace ℝ (Fin n) →L[ℝ] ℝ :=
    PiLp.proj (p := 2) (𝕜 := ℝ) (fun _ : Fin n => ℝ) i
  have hcomp : (fun y => (gradient v y) i) = fun y => fderiv ℝ v y e := by
    funext y
    change (gradient v y) i = fderiv ℝ v y (EuclideanSpace.single i (1 : ℝ))
    rw [← inner_gradient_left, EuclideanSpace.inner_single_right]
    simp
  have hl : fderiv ℝ (fun y => (gradient v y) i) x e =
      (fderiv ℝ (gradient v) x e) i := by
    simpa [π, Function.comp_def] using congrArg (fun L : EuclideanSpace ℝ (Fin n) →L[ℝ] ℝ => L e)
      (π.hasFDerivAt.comp x hgd).fderiv
  have hr : fderiv ℝ (fun y => fderiv ℝ v y e) x e = fderiv ℝ (fderiv ℝ v) x e e := by
    simpa using congrArg (fun L : EuclideanSpace ℝ (Fin n) →L[ℝ] ℝ => L e)
      (hfd.clm_apply (hasFDerivAt_const e x)).fderiv
  simp only [EuclideanSpace.basisFun_apply, iteratedFDeriv_two_apply]
  change (fderiv ℝ (gradient v) x e) i = fderiv ℝ (fderiv ℝ v) x e e
  rw [← hl, hcomp, hr]

-- The source standing dimension and parent-radius hypotheses are retained
-- literally even though the internal all-subradii argument is more general.
set_option linter.unusedVariables false in
/-- One source harmonic extension has integrable zero radial gradient flux at
all positive internal radii, including the parent boundary. -/
theorem harmonic_closedBall_zero_flux {n : ℕ} (hn : 2 ≤ n)
    (u : EuclideanSpace ℝ (Fin n) → ℝ)
    (a : EuclideanSpace ℝ (Fin n)) (R : ℝ) (hR : 0 < R)
    (hu : ∃ v : EuclideanSpace ℝ (Fin n) → ℝ,
      InnerProductSpace.HarmonicOnNhd v (Metric.closedBall a R) ∧
      Set.EqOn v u (Metric.closedBall a R)) :
    let τ : MeasureTheory.Measure (Metric.sphere (0 : EuclideanSpace ℝ (Fin n)) 1) :=
      (MeasureTheory.volume : MeasureTheory.Measure (EuclideanSpace ℝ (Fin n))).toSphere
    ∃ v : EuclideanSpace ℝ (Fin n) → ℝ,
      InnerProductSpace.HarmonicOnNhd v (Metric.closedBall a R) ∧
      Set.EqOn v u (Metric.closedBall a R) ∧
      ∀ r : ℝ, 0 < r → r ≤ R →
        MeasureTheory.Integrable (fun ζ : Metric.sphere (0 : EuclideanSpace ℝ (Fin n)) 1 =>
          inner ℝ (gradient v (a + r • ζ.1)) ζ.1) τ ∧
        (∫ ζ : Metric.sphere (0 : EuclideanSpace ℝ (Fin n)) 1,
          inner ℝ (gradient v (a + r • ζ.1)) ζ.1 ∂τ) = 0 := by
  dsimp only
  obtain ⟨v, hv, hvu⟩ := hu
  refine ⟨v, hv, hvu, ?_⟩
  intro r hr hrR
  have hvsub : InnerProductSpace.HarmonicOnNhd v (closedBall a r) :=
    hv.mono (closedBall_subset_closedBall hrR)
  obtain ⟨_, hL1, hflux⟩ := Calculus.BallFlux.ball_flux_eq_integral_divergence
    (gradient v) a r hr (fun x hx => gradient_c1 v x (hvsub x hx).1)
  refine ⟨hL1, ?_⟩
  have hvol : (∫ x in ball a r, Calculus.Divergence.coordinateDivergence (gradient v) x) = 0 := by
    apply setIntegral_eq_zero_of_forall_eq_zero
    intro x hx
    have hh := hvsub x (ball_subset_closedBall hx)
    rw [divergence_gradient v x hh.1]
    exact hh.2.eq_of_nhds
  rw [hvol] at hflux
  exact (mul_eq_zero.mp hflux.symm).resolve_left (pow_ne_zero _ hr.ne')

end
end AutoSamplingTheory.TechnicalLemmas.Analysis.Harmonic.SphericalFlux
