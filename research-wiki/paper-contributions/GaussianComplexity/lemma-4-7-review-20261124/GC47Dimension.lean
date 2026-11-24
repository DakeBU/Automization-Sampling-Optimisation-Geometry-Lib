import GC47MinorPolynomial
import GC47Rank
import GC47GaussianZero

/-! Lemma 4.7 of Zhou and Suzuki: almost-sure dimension of the block Krylov space. -/
noncomputable section
open MeasureTheory ProbabilityTheory
open AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumSaturation
namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumKrylov

/-- A fixed maximal minor is a nonzero polynomial in the independent Gaussian
coordinates. This holds on either side of the point where the span fills the ambient space. -/
theorem dimension_of_gaussian_krylov {d q : ℕ} {κ : ℝ} (hκ : κ ≠ 1) :
    ∀ᵐ g ∂gaussianStarts d q, Module.finrank ℝ (krylov d q κ g) = min d ((q+1)^2) := by
  let node := gridNode d κ
  have h := ae_eval_gaussian_starts (minorPolynomial q node)
    (minorPolynomial_ne_zero q node (gridNode_injective d hκ))
  filter_upwards [h] with g hg
  apply finrank_krylov_of_minor g (minorRow d q) (minorColumn d q)
  change minorDet node g ≠ 0
  rwa [← eval_minorPolynomial node g]

/-- Source statement on any probability space carrying independent standard Gaussian starts. -/
theorem dimension_of_independent_gaussian_starts {d q : ℕ} {κ : ℝ} (hκ : κ ≠ 1)
    {Ω : Type*} [MeasurableSpace Ω] (μ : Measure Ω) (g : Fin (q+1) → Ω → Space d)
    (hg : ∀ a, MeasurePreserving (g a) μ (stdGaussian (Space d))) (hi : iIndepFun g μ) :
    ∀ᵐ ω ∂μ, Module.finrank ℝ (krylov d q κ (fun a => g a ω)) = min d ((q+1)^2) := by
  have hp : MeasurePreserving (fun ω a => g a ω) μ (gaussianStarts d q) := by
    refine ⟨measurable_pi_lambda _ (fun a => (hg a).measurable), ?_⟩
    rw [hi.map_fun_eq_pi_map (fun a => (hg a).measurable.aemeasurable)]
    simp_rw [fun a => (hg a).map_eq]
    rfl
  exact hp.quasiMeasurePreserving.ae (dimension_of_gaussian_krylov hκ)

/-- Once the number of generators reaches d, the random span is the entire space. -/
theorem gaussian_krylov_eq_top {d q : ℕ} {κ : ℝ} (hκ : κ ≠ 1) (hd : d ≤ (q+1)^2) :
    ∀ᵐ g ∂gaussianStarts d q, krylov d q κ g = ⊤ := by
  filter_upwards [dimension_of_gaussian_krylov (d := d) (q := q) hκ] with g hg
  apply Submodule.eq_top_of_finrank_eq
  simpa [min_eq_left hd] using hg

#print axioms dimension_of_gaussian_krylov
#print axioms dimension_of_independent_gaussian_starts
#print axioms gaussian_krylov_eq_top
end AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumKrylov
