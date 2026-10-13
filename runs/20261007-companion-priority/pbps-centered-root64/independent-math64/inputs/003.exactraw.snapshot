import AutoSamplingTheory.ExampleCases.ProximalBPS.ConditionalScoreDomain
import AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.WeightedBochner

/-!
# Bochner energy of the actual reflected conditional Gibbs law

This is an analytic prerequisite to PBPS v1 Appendix C.1's conditional
Poincare step. The actual Markov kernels and curvature come from the same
ConditionalScoreDomain construction. Global normalization is recovered from
that genuine probability law, not inferred from compact-test integrability.
The inherited beta eta <= 1 restriction belongs to that parent interface;
the Bochner identity itself does not require an upper curvature bound.
Weighted closure/core and the noncompact extension remain separate.
-/

namespace AutoSamplingTheory.ExampleCases.ProximalBPS.ConditionalBochner

open MeasureTheory ProbabilityTheory InnerProductSpace
open AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities
open scoped ContDiff NNReal RealInnerProductSpace

/-- Actual conditional normalized Bochner identity and curvature-energy bound.
The displayed Hessian square term uses genuine directional derivatives in
an orthonormal basis, not an assumed operator or a spectral-gap premise. -/
theorem conditional_bochner_energy {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]
    {V : E → ℝ} {α β : NNReal} {η : ℝ}
    (hα : 0 < (α:ℝ)) (hαβ : α ≤ β) (hV : ContDiff ℝ 2 V)
    (hH : ∀ x v : E, (α:ℝ)*‖v‖^2 ≤ (fderiv ℝ (fderiv ℝ V) x v) v ∧
      (fderiv ℝ (fderiv ℝ V) x v) v ≤ (β:ℝ)*‖v‖^2)
    (hη : 0 < η) (hβη : (β:ℝ)*η ≤ 1) :
    let μ := (volume : Measure E).tilted (fun x => -V x)
    let J := Measure.map (fun p : E × E => (p.1,p.1+Real.sqrt η • p.2)) (μ.prod (stdGaussian E))
    let W := fun y u : E => V ((1/2:ℝ) • (y+u)) + ‖u-y‖^2/(8*η)
    ∃ R S : Kernel E E, IsMarkovKernel R ∧ IsMarkovKernel S ∧
      (J.map Prod.swap).IsCondKernel R ∧
      (∀ y, S y = (R y).map (fun x => (2:ℝ) • x-y)) ∧
      ∀ y, S y = (volume : Measure E).tilted (fun u => -W y u) ∧
        ContDiff ℝ 2 (W y) ∧ Integrable (fun u => Real.exp (-W y u)) ∧
        0 < (∫ u, Real.exp (-W y u)) ∧
        ∀ f : E → ℝ, ContDiff ℝ ∞ f → HasCompactSupport f →
          let L := fun u => Laplacian.laplacian f u - inner ℝ (gradient (W y) u) (gradient f u)
          let H := fun u => ∑ i, ‖gradient (fun z => fderiv ℝ f z ((stdOrthonormalBasis ℝ E) i)) u‖^2
          let C := fun u => fderiv ℝ (fderiv ℝ (W y)) u (gradient f u) (gradient f u)
          Integrable (fun u => (L u)^2) (S y) ∧
          Integrable (fun u => ‖gradient f u‖^2) (S y) ∧
          Integrable H (S y) ∧ Integrable C (S y) ∧
          (∫ u, (L u)^2 ∂S y) = (∫ u, H u ∂S y) + ∫ u, C u ∂S y ∧
          (((α:ℝ)+1/η)/4) * (∫ u, ‖gradient f u‖^2 ∂S y) ≤ ∫ u, (L u)^2 ∂S y := by
  obtain ⟨R,S,hR,hS,hcond,hSR,hfiber⟩ :=
    ConditionalScoreDomain.conditional_curvature_and_score_domain hα hαβ hV hH hη hβη
  let _ : IsMarkovKernel S := hS
  dsimp only
  refine ⟨R,S,hR,hS,hcond,hSR,?_⟩
  intro y
  let W := fun u : E => V ((1/2:ℝ) • (y+u)) + ‖u-y‖^2/(8*η)
  obtain ⟨hSy,hWC,_,_,hcurv,_,_⟩ := hfiber y
  change S y = (volume : Measure E).tilted (fun u => -W u) at hSy
  have hweight : Integrable (fun u => Real.exp (-W u)) := by
    by_contra hn
    have hz : S y = 0 := hSy.trans (tilted_of_not_integrable hn)
    have hu := measure_univ (μ := S y)
    rw [hz] at hu
    norm_num at hu
  have hZ : 0 < ∫ u, Real.exp (-W u) := integral_exp_pos hweight
  refine ⟨hSy,hWC,hweight,hZ,?_⟩
  intro f hf hc
  obtain ⟨hL,hG,hHess,hC,hidentity,hbound⟩ :=
    WeightedBochner.integrated_bochner_identity W f hWC hf hc
  have hI (g : E → ℝ) (hg : Integrable (fun u => Real.exp (-W u)*g u)) :
      Integrable g (S y) := by
    rw [hSy]
    exact (integrable_tilted_iff hweight g).mpr (by simpa only [smul_eq_mul] using hg)
  have htilt (g : E → ℝ) : (∫ u, g u ∂S y) =
      (∫ u, Real.exp (-W u))⁻¹ * (∫ u, Real.exp (-W u)*g u) := by
    rw [hSy, integral_tilted]
    rw [← integral_const_mul]
    apply integral_congr_ae
    filter_upwards [] with u
    change (Real.exp (-W u) / (∫ z, Real.exp (-W z))) • g u =
      (∫ z, Real.exp (-W z))⁻¹ * (Real.exp (-W u) * g u)
    simp only [smul_eq_mul, div_eq_mul_inv]
    ring
  refine ⟨hI _ hL,hI _ hG,hI _ hHess,hI _ hC,?_,?_⟩
  · rw [htilt,htilt,htilt,hidentity,mul_add]
  · rw [htilt,htilt]
    calc
      _ = (∫ u, Real.exp (-W u))⁻¹ *
          ((((α:ℝ)+1/η)/4) * (∫ u, Real.exp (-W u)*‖gradient f u‖^2)) := by ring
      _ ≤ _ := mul_le_mul_of_nonneg_left (hbound _ hcurv) (inv_nonneg.mpr hZ.le)

end AutoSamplingTheory.ExampleCases.ProximalBPS.ConditionalBochner
