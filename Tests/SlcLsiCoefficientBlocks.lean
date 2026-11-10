/-
Copyright (c) 2026 Samplinglib contributors. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
-/
import AutoSamplingTheory.ExampleCases.SlcLsiQueryComplexity.CoefficientBlocks

open MeasureTheory ProbabilityTheory
open AutoSamplingTheory.ExampleCases.SlcLsiQueryComplexity.CoefficientBlocks

-- Derive every source-block marginal and mutual independence from the actual law.
example (n : ℕ+) (h : ℕ) :
    let B := Fin (h + 1) × {p : Fin (2 ^ (64 * (h + 1)) + 1) // Even p.val ∧ 4 ≤ p.val}
    let C := fun b : B ↦
      ((Fin b.2.val.val × (Σ j : Fin (h - b.1.val + 1),
        Fin ((2 ^ (74 * (h + 1))) ^ j.val))) → Fin n.val)
    let blocks := fun (ξ : EuclideanSpace ℝ (Σ b : B, C b)) (b : B) ↦
      (WithLp.toLp 2 (fun c : C b ↦ ξ ⟨b, c⟩) : EuclideanSpace ℝ (C b))
    let μ := stdGaussian (EuclideanSpace ℝ (Σ b : B, C b))
    (∀ b : B, HasLaw (fun ξ ↦ blocks ξ b) (stdGaussian (EuclideanSpace ℝ (C b))) μ) ∧
      iIndepFun (fun b ξ ↦ blocks ξ b) μ := by
  intro B C blocks μ
  classical
  have hJoint :
      HasLaw blocks (Measure.pi fun b : B ↦ stdGaussian (EuclideanSpace ℝ (C b))) μ :=
    jointCoefficientBlocks_hasLaw n h
  have hMarginal (b : B) :
      HasLaw (fun ξ ↦ blocks ξ b) (stdGaussian (EuclideanSpace ℝ (C b))) μ := by
    have hEval := measurePreserving_eval (μ := fun j : B ↦ stdGaussian (EuclideanSpace ℝ (C j))) b
    have h := hEval.fun_comp_hasLaw hJoint
    exact h
  refine ⟨hMarginal, (iIndepFun_iff_map_fun_eq_pi_map (μ := μ)
    (f := fun b ξ ↦ blocks ξ b) (fun b ↦ (hMarginal b).aemeasurable)).2 ?_⟩
  rw [hJoint.map_eq]
  exact congrArg Measure.pi (funext fun b ↦ (hMarginal b).map_eq.symm)

#print axioms jointCoefficientBlocks_hasLaw
#check @jointCoefficientBlocks_hasLaw
