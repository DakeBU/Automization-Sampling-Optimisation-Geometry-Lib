import GC33Target
import AutoSamplingTheory.TechnicalLemmas.Measure.Gibbs

/-! The Gaussian target of each admissible precision is the normalized Gibbs law
of the value returned by its first-order oracle. -/
noncomputable section
open Matrix MeasureTheory ProbabilityTheory
open scoped ENNReal
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarConditional
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarPosterior
open AutoSamplingTheory.ExampleCases.GaussianComplexity.FirstOrderIndistinguishability
open AutoSamplingTheory.TechnicalLemmas.Measure.GaussianPrecisionDensity
open AutoSamplingTheory.TechnicalLemmas.Measure.Gibbs
namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.LogConcaveSubclass

/-- Lebesgue integral of the unnormalized density `exp (-V)`. -/
def gibbsMass {d : ℕ} (V : E d → ℝ) : ℝ≥0∞ :=
  ∫⁻ x, gibbsDensityENNReal V x

/-- Lebesgue Gibbs law with reciprocal partition-function normalization. -/
def gibbsLaw {d : ℕ} (V : E d → ℝ) : Measure (E d) :=
  (gibbsMass V)⁻¹ • volume.withDensity (gibbsDensityENNReal V)

theorem gibbsLaw_probability {d : ℕ} {V : E d → ℝ} (h0 : gibbsMass V ≠ 0)
    (hfin : gibbsMass V ≠ ∞) : IsProbabilityMeasure (gibbsLaw V) := by
  constructor
  change (gibbsMass V)⁻¹ * volume.withDensity (gibbsDensityENNReal V) Set.univ = 1
  rw [withDensity_apply _ MeasurableSet.univ, Measure.restrict_univ]
  exact ENNReal.inv_mul_cancel h0 hfin

private theorem precision_posDef {d : ℕ} {κ : ℝ} {A : Precision d} (hA : Admissible κ A) : A.PosDef := by
  apply Matrix.posDef_iff_dotProduct_mulVec.mpr
  refine ⟨hA.1,fun x hx => ?_⟩
  have hpos : 0 < x ⬝ᵥ x := by
    simpa only [star_trivial] using dotProduct_star_self_pos_iff.mpr hx
  simpa only [star_trivial] using hpos.trans_le (hA.2 x).1

private theorem targetLaw_eq_scaled_gibbs {d : ℕ} {A : Precision d} (hp : A.PosDef) :
    targetLaw A = ENNReal.ofReal (Real.sqrt A.det / (2*Real.pi)^((d:ℝ)/2)) •
      volume.withDensity (gibbsDensityENNReal (fun x => (precisionReply A x).1)) := by
  have hc : 0 < Real.sqrt A.det / (2*Real.pi)^((d:ℝ)/2) :=
    div_pos (Real.sqrt_pos.mpr hp.det_pos) (Real.rpow_pos_of_pos (by positivity) _)
  rw [targetLaw, multivariateGaussian_eq_withDensity_of_posDef A hp,
    ← withDensity_smul' _ _ ENNReal.ofReal_ne_top]
  congr 1
  funext x
  change ENNReal.ofReal (_ * Real.exp _) = _ * ENNReal.ofReal (Real.exp _)
  rw [ENNReal.ofReal_mul hc.le]
  congr 3
  change -(WithLp.ofLp x ⬝ᵥ A *ᵥ WithLp.ofLp x)/2 =
    -(inner ℝ x ((Matrix.toEuclideanCLM (𝕜 := ℝ) A) x)/2)
  rw [Matrix.inner_toEuclideanCLM, neg_div]

/-- The actual partition function of the quadratic potential is positive and finite
in every dimension and is the reciprocal of the Gaussian precision prefactor. -/
theorem precision_gibbs_mass {d : ℕ} {κ : ℝ} {A : Precision d} (hA : Admissible κ A) :
    let Z := gibbsMass (fun x => (precisionReply A x).1)
    0 < Z ∧ Z ≠ ∞ ∧ Z = (ENNReal.ofReal (Real.sqrt A.det / (2*Real.pi)^((d:ℝ)/2)))⁻¹ := by
  let c := ENNReal.ofReal (Real.sqrt A.det / (2*Real.pi)^((d:ℝ)/2))
  let V := fun x => (precisionReply A x).1
  have hp := precision_posDef hA
  have hc : 0 < c := ENNReal.ofReal_pos.mpr
    (div_pos (Real.sqrt_pos.mpr hp.det_pos) (Real.rpow_pos_of_pos (by positivity) _))
  have h := congrArg (fun μ : Measure (E d) => μ Set.univ) (targetLaw_eq_scaled_gibbs hp)
  change (targetLaw A) Set.univ = c * volume.withDensity (gibbsDensityENNReal V) Set.univ at h
  rw [measure_univ, withDensity_apply _ MeasurableSet.univ, Measure.restrict_univ] at h
  have he : gibbsMass V = c⁻¹ := ENNReal.eq_inv_of_mul_eq_one_left (mul_comm c _ ▸ h.symm)
  exact ⟨he ▸ ENNReal.inv_pos.mpr ENNReal.ofReal_ne_top, he ▸ ENNReal.inv_ne_top.mpr hc.ne', he⟩

/-- The Gaussian sampling target equals the normalized Gibbs law for the very
same quadratic value observed by the oracle. -/
theorem targetLaw_eq_gibbs {d : ℕ} {κ : ℝ} {A : Precision d} (hA : Admissible κ A) :
    targetLaw A = gibbsLaw (fun x => (precisionReply A x).1) := by
  rw [gibbsLaw,(precision_gibbs_mass hA).2.2, inv_inv]
  exact targetLaw_eq_scaled_gibbs (precision_posDef hA)

#print axioms targetLaw_eq_gibbs
end AutoSamplingTheory.ExampleCases.GaussianComplexity.LogConcaveSubclass
