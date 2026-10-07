import AutoSamplingTheory.TechnicalLemmas.Probability.BalancedRademacherCLT
import Mathlib.Analysis.Calculus.ContDiff.Deriv
import Mathlib.Analysis.Calculus.Deriv.Support
import Mathlib.Topology.ContinuousMap.BoundedCompactlySupported
import Mathlib.MeasureTheory.Function.LocallyIntegrable
import Mathlib.Analysis.SpecialFunctions.Log.NegMulLog

/-! Actual normalized Boolean-count observer limits for the compact Gaussian
entropy core. This does not assert the separate full coordinate-flip energy
limit, Gaussian LSI, or the noncompact SPHMC density extension. -/

open MeasureTheory ProbabilityTheory Filter
open scoped Topology BigOperators ENNReal

namespace AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.GaussianCompactEntropy

private noncomputable def countLaw (n : ℕ) : Measure (Fin n → Bool) :=
  (Fintype.card (Fin n → Bool) : ℝ≥0∞)⁻¹ • Measure.count

private noncomputable def normalizedSum (n : ℕ) (ε : Fin n → Bool) : ℝ :=
  (Real.sqrt (n : ℝ))⁻¹ * ∑ j : Fin n, if ε j then (1 : ℝ) else -1

private theorem compact_observer (g : ℝ → ℝ) (hg : Continuous g)
    (hs : HasCompactSupport g) :
    Integrable g (gaussianReal 0 1) ∧
    (∀ n : ℕ, Integrable (fun ε => g (normalizedSum n ε)) (countLaw n)) ∧
    Tendsto (fun n : ℕ => ∫ ε, g (normalizedSum (n+1) ε) ∂countLaw (n+1))
      atTop (𝓝 (∫ x, g x ∂gaussianReal 0 1)) := by
  rcases AutoSamplingTheory.TechnicalLemmas.Probability.BalancedRademacherCLT.balanced_count_sum_tendsto_gaussian
    with ⟨laws, hlaws, _, hlim⟩
  have hmap (n : ℕ) : (laws n : Measure ℝ) = (countLaw n).map (normalizedSum n) :=
    hlaws n
  have hmeas (n : ℕ) : Measurable (normalizedSum n) := measurable_of_finite _
  have hi (n : ℕ) : Integrable g (laws n : Measure ℝ) :=
    hg.integrable_of_hasCompactSupport hs
  have hic (n : ℕ) : Integrable (fun ε => g (normalizedSum n ε)) (countLaw n) := by
    have hm : Integrable g ((countLaw n).map (normalizedSum n)) := by
      rw [← hmap n]
      exact hi n
    exact hm.comp_measurable (hmeas n)
  have hI (n : ℕ) : (∫ x, g x ∂(laws n : Measure ℝ)) =
      ∫ ε, g (normalizedSum n ε) ∂countLaw n := by
    rw [hmap n]
    exact integral_map_of_stronglyMeasurable (hmeas n) hg.stronglyMeasurable
  have ht := ProbabilityMeasure.tendsto_iff_forall_integral_tendsto.mp hlim
    (ofCompactSupport g hg hs)
  change Tendsto (fun n : ℕ => ∫ x, g x ∂(laws (n+1) : Measure ℝ))
    atTop (𝓝 (∫ x, g x ∂gaussianReal 0 1)) at ht
  exact ⟨hg.integrable_of_hasCompactSupport hs, hic, ht.congr (fun n => hI (n+1))⟩

/-- Compact C2 core: actual Gaussian and every finite-count L1 domain,
and successor mass/log-entropy/derivative-observer and homogeneous entropy limits.
Zero mass is included; the full flip energy and noncompact extension are separate. -/
theorem compact_count_gaussian_entropy_limits
    (f : ℝ → ℝ) (hf : ContDiff ℝ 2 f) (hs : HasCompactSupport f) :
    let μ : (n : ℕ) → Measure (Fin n → Bool) := fun n =>
      (Fintype.card (Fin n → Bool) : ℝ≥0∞)⁻¹ • Measure.count
    let S : (n : ℕ) → (Fin n → Bool) → ℝ := fun n ε =>
      (Real.sqrt (n : ℝ))⁻¹ * ∑ j : Fin n, if ε j then (1 : ℝ) else -1
    let γ : Measure ℝ := gaussianReal 0 1
    Integrable (fun x => (f x)^2) γ ∧
    Integrable (fun x => (f x)^2 * Real.log ((f x)^2)) γ ∧
    Integrable (fun x => (deriv f x)^2) γ ∧
    (∀ n : ℕ,
      Integrable (fun ε => (f (S n ε))^2) (μ n) ∧
      Integrable (fun ε => (f (S n ε))^2 * Real.log ((f (S n ε))^2)) (μ n) ∧
      Integrable (fun ε => (deriv f (S n ε))^2) (μ n)) ∧
    Tendsto (fun n : ℕ => ∫ ε, (f (S (n+1) ε))^2 ∂μ (n+1)) atTop
      (𝓝 (∫ x, (f x)^2 ∂γ)) ∧
    Tendsto (fun n : ℕ => ∫ ε,
      (f (S (n+1) ε))^2 * Real.log ((f (S (n+1) ε))^2) ∂μ (n+1)) atTop
      (𝓝 (∫ x, (f x)^2 * Real.log ((f x)^2) ∂γ)) ∧
    Tendsto (fun n : ℕ => ∫ ε, (deriv f (S (n+1) ε))^2 ∂μ (n+1)) atTop
      (𝓝 (∫ x, (deriv f x)^2 ∂γ)) ∧
    Tendsto (fun n : ℕ =>
      (∫ ε, (f (S (n+1) ε))^2 * Real.log ((f (S (n+1) ε))^2) ∂μ (n+1)) -
      (∫ ε, (f (S (n+1) ε))^2 ∂μ (n+1)) *
        Real.log (∫ ε, (f (S (n+1) ε))^2 ∂μ (n+1))) atTop
      (𝓝 ((∫ x, (f x)^2 * Real.log ((f x)^2) ∂γ) -
        (∫ x, (f x)^2 ∂γ) * Real.log (∫ x, (f x)^2 ∂γ))) := by
  have hA : Continuous (fun x => (f x)^2) := hf.continuous.pow 2
  have sA : HasCompactSupport (fun x => (f x)^2) := by
    simpa only [Function.comp_def] using hs.comp_left (g := fun t : ℝ => t^2) (by simp)
  have hB : Continuous (fun x => (f x)^2 * Real.log ((f x)^2)) :=
    Real.continuous_mul_log.comp hA
  have sB : HasCompactSupport (fun x => (f x)^2 * Real.log ((f x)^2)) := by
    simpa only [Function.comp_def] using
      sA.comp_left (g := fun t : ℝ => t * Real.log t) (by simp)
  have hC : Continuous (fun x => (deriv f x)^2) :=
    (hf.continuous_deriv (by norm_num)).pow 2
  have sC : HasCompactSupport (fun x => (deriv f x)^2) := by
    simpa only [Function.comp_def] using
      hs.deriv.comp_left (g := fun t : ℝ => t^2) (by simp)
  rcases compact_observer (fun x => (f x)^2) hA sA with ⟨iA, jA, tA⟩
  rcases compact_observer (fun x => (f x)^2 * Real.log ((f x)^2)) hB sB
    with ⟨iB, jB, tB⟩
  rcases compact_observer (fun x => (deriv f x)^2) hC sC with ⟨iC, jC, tC⟩
  have tE := tB.sub ((Real.continuous_mul_log.continuousAt.tendsto).comp tA)
  exact ⟨iA, iB, iC, fun n => ⟨jA n, jB n, jC n⟩, tA, tB, tC, tE⟩

end AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.GaussianCompactEntropy

