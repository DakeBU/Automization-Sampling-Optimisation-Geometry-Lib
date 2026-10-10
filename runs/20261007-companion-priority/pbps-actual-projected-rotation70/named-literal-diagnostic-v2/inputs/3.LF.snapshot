import Mathlib.Probability.Distributions.Gaussian.Multivariate
import Mathlib.MeasureTheory.Measure.Prod
import Mathlib.Tactic.Abel
import Mathlib.Tactic.FunProp

/-!
# Reflection of the generative Gaussian augmentation

This is the generative-law proof component of Proposition 2.1(iii) in Chen,
Chewi, Lu and Zhang, arXiv:2609.06905v1, Section 2.2, equations (2.7) and (2.14):
<https://arxiv.org/html/2609.06905v1#S2.SS2>.

The law below is defined by independent `X ~ μ`, `Z ~ stdGaussian E` and
`Y = X + sqrt η • Z`. Identifying it with the normalized density (2.6) is a
separate obligation. The symmetry component needs no potential, curvature or
upper step-size bound; this generality is explicit, not a claim to have proved
those source assumptions or the invariance of any PBPS process.
-/

open MeasureTheory ProbabilityTheory

namespace AutoSamplingTheory.ExampleCases.ProximalBPS.GaussianReflection

variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
  [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]

/-- Reflecting the auxiliary point through the position is involutive and
preserves the generative Gaussian augmentation. All maps used in the
pushforward calculation are proved measurable. The positive-scale hypothesis
retains the paper's sampling regime; the reflection algebra itself is
scale-independent. Intended consumers are the auxiliary update in Section 3.1
and, after a separate `L²` adapter, the reflection operator in Appendix B. -/
theorem reflection_preserves_augmentation (μ : Measure E) [IsProbabilityMeasure μ]
    (η : ℝ) (_hη : 0 < η) :
    Function.Involutive (fun p : E × E => (p.1, (2 : ℝ) • p.1 - p.2)) ∧
      Measure.map (fun p : E × E => (p.1, (2 : ℝ) • p.1 - p.2))
        (Measure.map (fun p : E × E => (p.1, p.1 + Real.sqrt η • p.2))
          (μ.prod (stdGaussian E))) =
        Measure.map (fun p : E × E => (p.1, p.1 + Real.sqrt η • p.2))
          (μ.prod (stdGaussian E)) := by
  let Φ : E × E → E × E := fun p => (p.1, p.1 + Real.sqrt η • p.2)
  let R : E × E → E × E := fun p => (p.1, (2 : ℝ) • p.1 - p.2)
  let S : E × E → E × E := Prod.map id (fun z => -z)
  have hΦ : Measurable Φ := by fun_prop
  have hR : Measurable R := by fun_prop
  have hS : Measurable S := by fun_prop
  have hneg : Measure.map (fun z : E => -z) (stdGaussian E) = stdGaussian E := by
    simpa using (stdGaussian_map (LinearIsometryEquiv.neg ℝ (E := E)))
  have hprod : Measure.map S (μ.prod (stdGaussian E)) = μ.prod (stdGaussian E) := by
    dsimp [S]
    rw [← Measure.map_prod_map μ (stdGaussian E) measurable_id (by fun_prop),
      hneg, Measure.map_id]
  have hcomp : R ∘ Φ = Φ ∘ S := by
    funext p
    apply Prod.ext
    · rfl
    · dsimp [R, Φ, S]
      simp only [smul_neg, two_smul]
      abel
  constructor
  · intro p
    apply Prod.ext
    · rfl
    · exact sub_sub_cancel ((2 : ℝ) • p.1) p.2
  · change Measure.map R (Measure.map Φ (μ.prod (stdGaussian E))) =
      Measure.map Φ (μ.prod (stdGaussian E))
    rw [Measure.map_map hR hΦ, hcomp, ← Measure.map_map hΦ hS, hprod]

end AutoSamplingTheory.ExampleCases.ProximalBPS.GaussianReflection
