import AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.GaussianCompactProductLogSobolev
import AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Gradient
import Mathlib.Probability.Distributions.Gaussian.Multivariate
import Mathlib.Topology.Algebra.Module.FiniteDimension

/-! Compact Gaussian function LSI on the actual finite-dimensional Hilbert law.
The canonical basis transports the measure and Parseval transports the energy.
The noncompact square-root-density extension and Gaussian T2 remain separate. -/

open MeasureTheory ProbabilityTheory
open scoped BigOperators RealInnerProductSpace

namespace AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.GaussianCompactHilbertLogSobolev

private theorem pullback_energy
    {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [CompleteSpace E] {n : ℕ} (b : OrthonormalBasis (Fin n) ℝ E)
    (f : E → ℝ) (hf : ContDiff ℝ 2 f) (x : Fin n → ℝ) :
    let T := b.toBasis.equivFunL.symm
    ∑ i, (fderiv ℝ (f ∘ T) x (Pi.single i 1))^2 =
      ‖gradient f (T x)‖^2 := by
  dsimp only
  let T := b.toBasis.equivFunL.symm
  have hsingle (i : Fin n) : T (Pi.single i 1) = b i := by
    change b.toBasis.equivFun.symm (Pi.single i 1) = b i
    rw [b.toBasis.equivFun_symm_apply]
    simp
  have hD (i : Fin n) : fderiv ℝ (f ∘ T) x (Pi.single i 1) =
      inner ℝ (gradient f (T x)) (b i) := by
    change (fderiv ℝ (f ∘ T.toContinuousLinearMap) x) (Pi.single i 1) = _
    rw [fderiv_comp x (hf.differentiable (by norm_num)).differentiableAt
      T.toContinuousLinearMap.differentiableAt]
    rw [ContinuousLinearMap.comp_apply, T.toContinuousLinearMap.fderiv]
    change fderiv ℝ f (T x) (T (Pi.single i 1)) = _
    rw [hsingle]
    exact (inner_gradient_left).symm
  change ∑ i, (fderiv ℝ (f ∘ T) x (Pi.single i 1))^2 = ‖gradient f (T x)‖^2
  simp_rw [hD]
  exact b.sum_sq_inner_left (gradient f (T x))

/-- Actual compact finite-Hilbert Gaussian LSI with its three true L1 domains.
Signed functions, zero mass and dimension zero are included. -/
theorem compact_stdGaussian_logSobolev
    {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [CompleteSpace E] [FiniteDimensional ℝ E]
    [MeasurableSpace E] [BorelSpace E]
    (f : E → ℝ) (hf : ContDiff ℝ 2 f) (hs : HasCompactSupport f) :
    let γ : Measure E := ProbabilityTheory.stdGaussian E
    Integrable (fun x => (f x)^2) γ ∧
    Integrable (fun x => (f x)^2 * Real.log ((f x)^2)) γ ∧
    Integrable (fun x => ‖gradient f x‖^2) γ ∧
    (∫ x, (f x)^2 * Real.log ((f x)^2) ∂γ) -
      (∫ x, (f x)^2 ∂γ) * Real.log (∫ x, (f x)^2 ∂γ) ≤
      2 * ∫ x, ‖gradient f x‖^2 ∂γ := by
  dsimp only
  let n := Module.finrank ℝ E
  let b := stdOrthonormalBasis ℝ E
  let T := b.toBasis.equivFunL.symm
  let μ : Measure (Fin n → ℝ) := Measure.pi (fun _ : Fin n => gaussianReal 0 1)
  have hγ : stdGaussian E = μ.map T := by
    unfold stdGaussian
    congr 1
    funext x
    exact (b.toBasis.equivFun_symm_apply x).symm
  have hg : ContDiff ℝ 2 (f ∘ T) :=
    hf.comp_continuousLinearMap (g := T.toContinuousLinearMap)
  have hgs : HasCompactSupport (f ∘ T) := hs.comp_homeomorph T.toHomeomorph
  obtain ⟨hm, hp, _, he, hLSI⟩ :=
    GaussianCompactProductLogSobolev.compact_gaussian_pi_logSobolev n (f ∘ T) hg hgs
  have henergy : ∀ x, (∑ i : Fin n, (fderiv ℝ (f ∘ T) x (Pi.single i 1))^2) =
      ‖gradient f (T x)‖^2 := pullback_energy b f hf
  have cm : Continuous (fun x => (f x)^2) := hf.continuous.pow 2
  have cp : Continuous (fun x => (f x)^2 * Real.log ((f x)^2)) := Real.Continuous.mul_log cm
  have ce : Continuous (fun x => ‖gradient f x‖^2) :=
    (Analysis.Calculus.Gradient.continuous_gradient_of_contDiff_one
      (hf.of_le (by norm_num))).norm.pow 2
  have hTm := T.continuous.measurable.aemeasurable (μ := μ)
  have im : Integrable (fun x => (f x)^2) (stdGaussian E) := by
    rw [hγ]
    exact (integrable_map_measure cm.aestronglyMeasurable hTm).2 hm
  have ip : Integrable (fun x => (f x)^2 * Real.log ((f x)^2)) (stdGaussian E) := by
    rw [hγ]
    exact (integrable_map_measure cp.aestronglyMeasurable hTm).2 hp
  have ie : Integrable (fun x => ‖gradient f x‖^2) (stdGaussian E) := by
    rw [hγ]
    apply (integrable_map_measure ce.aestronglyMeasurable hTm).2
    change Integrable (fun x : Fin n → ℝ => ‖gradient f (T x)‖^2) μ
    simpa only [henergy] using he
  refine ⟨im, ip, ie, ?_⟩
  rw [hγ, integral_map hTm cp.aestronglyMeasurable,
    integral_map hTm cm.aestronglyMeasurable,
    integral_map hTm ce.aestronglyMeasurable]
  simpa only [Function.comp_apply, henergy] using hLSI

end AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.GaussianCompactHilbertLogSobolev
