/-
Copyright (c) 2026 Samplinglib contributors. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
-/
import Mathlib.Probability.Distributions.Gaussian.Multivariate
import Mathlib.Probability.HasLaw
import Mathlib.Probability.ProductMeasure
import Mathlib.Data.PNat.Basic

open MeasureTheory ProbabilityTheory

noncomputable section

/-!
# Joint Gaussian law of the ordered coefficient blocks

Zhou–Suzuki, arXiv:2611.05813v1 (CC BY 4.0), §4.1.1 after Eq. (15).
The entrywise inverse of the direct-sum collection sends the actual
unconditioned standard Gaussian to the product of the block laws.
The target dependent function type is used as a measurable product, not
as a claim that its default norm is the direct-sum norm.
-/

namespace AutoSamplingTheory.ExampleCases.SlcLsiQueryComplexity.CoefficientBlocks

/-- Regroup the flat ordered coordinates without changing any coefficient.
The product law supplies the standard Gaussian marginals and mutual independence.
The isolated identity does not require the paper's large-dimension choice of
level depth and makes no claim after conditioning on admissibility. -/
theorem jointCoefficientBlocks_hasLaw (n : ℕ+) (h : ℕ) :
    let B := Fin (h + 1) × {p : Fin (2 ^ (64 * (h + 1)) + 1) // Even p.val ∧ 4 ≤ p.val}
    let C := fun b : B ↦
      ((Fin b.2.val.val × (Σ j : Fin (h - b.1.val + 1),
        Fin ((2 ^ (74 * (h + 1))) ^ j.val))) → Fin n.val)
    let blocks := fun (ξ : EuclideanSpace ℝ (Σ b : B, C b)) (b : B) ↦
      (WithLp.toLp 2 (fun c : C b ↦ ξ ⟨b, c⟩) : EuclideanSpace ℝ (C b))
    HasLaw blocks (Measure.pi fun b : B ↦ stdGaussian (EuclideanSpace ℝ (C b)))
      (stdGaussian (EuclideanSpace ℝ (Σ b : B, C b))) := by
  intro B C blocks
  classical
  let flat : Measure ((Σ b : B, C b) → ℝ) :=
    Measure.pi fun _ ↦ gaussianReal 0 1
  let grouped : Measure (∀ b : B, C b → ℝ) :=
    Measure.pi fun b ↦ Measure.pi fun _ : C b ↦ gaussianReal 0 1
  let split := MeasurableEquiv.piCurry (fun (b : B) (_ : C b) ↦ ℝ)
  let wrap (x : ∀ b : B, C b → ℝ) (b : B) : EuclideanSpace ℝ (C b) :=
    WithLp.toLp 2 (x b)
  have hmBlocks : Measurable blocks := by
    dsimp [blocks]
    fun_prop
  have hmWrap : Measurable wrap := by
    dsimp [wrap]
    fun_prop
  have hSplit : flat.map split = grouped := by
    simpa only [flat, grouped, split, Measure.infinitePi_eq_pi] using
      Measure.infinitePi_map_piCurry (fun (b : B) (_ : C b) ↦ gaussianReal 0 1)
  have hFactor (b : B) :
      (Measure.pi (fun _ : C b ↦ gaussianReal 0 1)).map
        (WithLp.toLp 2 : (C b → ℝ) → EuclideanSpace ℝ (C b)) =
      stdGaussian (EuclideanSpace ℝ (C b)) :=
    map_pi_eq_stdGaussian
  let : ∀ b : B, SigmaFinite ((Measure.pi (fun _ : C b ↦ gaussianReal 0 1)).map
      (WithLp.toLp 2 : (C b → ℝ) → EuclideanSpace ℝ (C b))) := by
    intro b
    rw [hFactor b]
    infer_instance
  have hWrap : grouped.map wrap =
      Measure.pi fun b : B ↦ stdGaussian (EuclideanSpace ℝ (C b)) := by
    rw [show grouped.map wrap = Measure.pi (fun b : B ↦
      (Measure.pi (fun _ : C b ↦ gaussianReal 0 1)).map
        (WithLp.toLp 2 : (C b → ℝ) → EuclideanSpace ℝ (C b))) from
      Measure.pi_map_pi (fun b ↦ (by fun_prop : Measurable
        (WithLp.toLp 2 : (C b → ℝ) → EuclideanSpace ℝ (C b))).aemeasurable)]
    exact congrArg Measure.pi (funext hFactor)
  have hFlat : flat.map (WithLp.toLp 2) =
      stdGaussian (EuclideanSpace ℝ (Σ b : B, C b)) :=
    map_pi_eq_stdGaussian
  have hCompose : blocks ∘ (WithLp.toLp 2) = wrap ∘ split := rfl
  refine ⟨hmBlocks.aemeasurable, ?_⟩
  rw [← hFlat, Measure.map_map hmBlocks (by fun_prop), hCompose,
    ← Measure.map_map hmWrap split.measurable, hSplit, hWrap]

end AutoSamplingTheory.ExampleCases.SlcLsiQueryComplexity.CoefficientBlocks
