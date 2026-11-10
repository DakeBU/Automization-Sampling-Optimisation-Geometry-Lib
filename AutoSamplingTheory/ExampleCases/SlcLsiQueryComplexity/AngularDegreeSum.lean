/-
Copyright (c) 2026 Samplinglib contributors. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
-/
import AutoSamplingTheory.ExampleCases.SlcLsiQueryComplexity.AngularDegree
import AutoSamplingTheory.ExampleCases.SlcLsiQueryComplexity.CoefficientBlocks
import Mathlib.Probability.Distributions.Gaussian.HasGaussianLaw.Independence

/-!
# Gaussian law of a fixed-level angular degree sum

Zhou–Suzuki, arXiv:2611.05813v1 (CC BY 4.0), §4.1.1, Eq. (14)–(15).
At fixed deterministic unit directions, the literal angular polynomial has a
centered Gaussian law with variance `n * ∑ p, aᵢₚ²`. This expands an implicit
finite-sum consequence of the paper's adjacent one-block and joint laws.
No radial, adaptive, or conditional law is asserted.
-/

open MeasureTheory ProbabilityTheory
open scoped BigOperators

namespace AutoSamplingTheory.ExampleCases.SlcLsiQueryComplexity.AngularDegreeSum

open AngularDegree CoefficientBlocks

/-- The actual fixed-level degree sum under the unconditioned coefficient law.
Independence and second moments come from the existing block laws, not premises. -/
theorem angularDegreeSum_hasLaw (n : ℕ+) (h : ℕ) (i : Fin (h + 1))
    (u : Fin (h - i.val + 1) → EuclideanSpace ℝ (Fin n.val))
    (hu : ∀ j, ‖u j‖ = 1) :
    let P := {p : Fin (2 ^ (64 * (h + 1)) + 1) // Even p.val ∧ 4 ≤ p.val}
    let B := Fin (h + 1) × P
    let C := fun b : B ↦
      ((Fin b.2.val.val × (Σ j : Fin (h - b.1.val + 1),
        Fin ((2 ^ (74 * (h + 1))) ^ j.val))) → Fin n.val)
    let degree := fun p : P ↦
      (⟨p.val.val, p.property.1, p.property.2, Nat.le_of_lt_succ p.val.isLt⟩ :
        {p : ℕ // Even p ∧ 4 ≤ p ∧ p ≤ 2 ^ (64 * (h + 1))})
    let S : ℕ := ∑ j : Fin (h - i.val + 1), (2 ^ (74 * (h + 1))) ^ j.val
    let a := fun p : P ↦ 1 / ((p.val.val : ℝ) ^ 4 * (S : ℝ) ^ 2 *
      Real.sqrt ((h - i.val + 1 : ℕ) * Real.log (2 * (2 : ℝ) ^ (64 * (h + 1)) * S)))
    let F := fun (ξ : EuclideanSpace ℝ (Σ b : B, C b)) ↦ ∑ p : P,
      angularDegreeComponent n h i (degree p) u
        (WithLp.toLp 2 (fun c : C (i, p) ↦ ξ ⟨(i, p), c⟩))
    HasLaw F (gaussianReal 0 (((n.val : ℝ) * ∑ p : P, (a p) ^ 2).toNNReal))
      (stdGaussian (EuclideanSpace ℝ (Σ b : B, C b))) := by
  intro P B C degree S a F
  classical
  let Ω := EuclideanSpace ℝ (Σ b : B, C b)
  let μ : Measure Ω := stdGaussian Ω
  let ν := fun b : B ↦ stdGaussian (EuclideanSpace ℝ (C b))
  let blocks := fun (ξ : Ω) (b : B) ↦
    (WithLp.toLp 2 (fun c : C b ↦ ξ ⟨b, c⟩) : EuclideanSpace ℝ (C b))
  let atLevel : P → B := fun p ↦ (i, p)
  let component (p : P) : EuclideanSpace ℝ (C (atLevel p)) → ℝ :=
    angularDegreeComponent n h i (degree p) u
  let X (p : P) (ξ : Ω) : ℝ := component p (blocks ξ (atLevel p))
  have hJoint : HasLaw blocks (Measure.pi ν) μ := jointCoefficientBlocks_hasLaw n h
  have hBlock (b : B) : HasLaw (fun ξ ↦ blocks ξ b) (ν b) μ := by
    have hEval := measurePreserving_eval (μ := ν) b
    have h := hEval.fun_comp_hasLaw hJoint
    exact h
  have hIndep : iIndepFun (fun b ξ ↦ blocks ξ b) μ :=
    (iIndepFun_iff_hasLaw_pi_pi hBlock).2 hJoint
  have hInjective : Function.Injective atLevel := fun _ _ h ↦ congrArg Prod.snd h
  have hComponent (p : P) :
      HasLaw (component p) (gaussianReal 0 (((n.val : ℝ) * (a p) ^ 2).toNNReal))
        (ν (atLevel p)) := angularDegreeComponent_hasLaw n h i (degree p) u hu
  have hX (p : P) :
      HasLaw (X p) (gaussianReal 0 (((n.val : ℝ) * (a p) ^ 2).toNNReal)) μ :=
    (hComponent p).fun_comp (hBlock (atLevel p))
  have hXIndep : iIndepFun X μ :=
    (hIndep.precomp hInjective).comp₀ component
      (fun p ↦ (hBlock (atLevel p)).aemeasurable)
      (fun p ↦ (hBlock (atLevel p)).map_eq.symm ▸ (hComponent p).aemeasurable)
  have hGaussian (p : P) : HasGaussianLaw (X p) μ := (hX p).hasGaussianLaw
  have hSum : HasGaussianLaw F μ := hXIndep.hasGaussianLaw_fun_sum hGaussian
  have hMean : ∫ ξ, F ξ ∂μ = 0 := by
    change (∫ ξ, ∑ p : P, X p ξ ∂μ) = 0
    rw [integral_finsetSum _ (fun p _ ↦ (hGaussian p).integrable)]
    simp only [fun p ↦ (hX p).integral_eq, integral_id_gaussianReal, Finset.sum_const_zero]
  have hVar : Var[F; μ] = (n.val : ℝ) * ∑ p : P, (a p) ^ 2 := by
    have hPointwise : F = ∑ p : P, X p := by
      funext ξ
      change (∑ p : P, X p ξ) = (∑ p : P, X p) ξ
      exact (Finset.sum_apply ξ Finset.univ X).symm
    rw [hPointwise]
    rw [IndepFun.variance_sum (X := X) (s := Finset.univ)
      (fun p _ ↦ (hGaussian p).memLp_two)
      (fun p _ q _ hpq ↦ hXIndep.indepFun hpq), Finset.mul_sum]
    refine Finset.sum_congr rfl fun p _ ↦ ?_
    rw [(hX p).variance_eq, variance_id_gaussianReal]
    exact Real.coe_toNNReal _ (mul_nonneg (Nat.cast_nonneg n.val) (sq_nonneg (a p)))
  change HasLaw F (gaussianReal 0 (((n.val : ℝ) * ∑ p : P, (a p) ^ 2).toNNReal)) μ
  exact ⟨hSum.aemeasurable, by rw [hSum.map_eq_gaussianReal, hMean, hVar]⟩

end AutoSamplingTheory.ExampleCases.SlcLsiQueryComplexity.AngularDegreeSum
