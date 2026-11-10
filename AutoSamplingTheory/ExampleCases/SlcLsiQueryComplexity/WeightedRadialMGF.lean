/-
Copyright (c) 2026 Samplinglib contributors. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
-/
import AutoSamplingTheory.ExampleCases.SlcLsiQueryComplexity.RadialLevels

open MeasureTheory ProbabilityTheory
open scoped BigOperators Classical
open AutoSamplingTheory.ExampleCases.SlcLsiQueryComplexity.AngularDegree
open scoped NNReal

/-!
# Actual fixed-location weighted Gaussian and its exponential moment

Zhou–Suzuki, arXiv:2611.05813v1 (CC BY 4.0), the variance calculation
immediately before Eq. (51) and Eq. (51) itself. This integrates only the
coefficient sample, not the location. The source weights are deterministic;
arbitrary real weights give the same isolated finite-dimensional identity.
-/

namespace AutoSamplingTheory.ExampleCases.SlcLsiQueryComplexity.WeightedRadialMGF

open RadialLevels

/-- The literal weighted field sum is centered Gaussian with the exact source
variance, and its negative exponential is integrable with the Eq. (51) mean. -/
theorem weightedRadialLevels_gaussian_mgf (n : ℕ+) (h : ℕ)
    (β : Fin (h + 1) → ℝ)
    (x : Fin (h + 1) → EuclideanSpace ℝ (Fin n.val)) :
    let L := Fin (h + 1)
    let P := {p : Fin (2 ^ (64 * (h + 1)) + 1) // Even p.val ∧ 4 ≤ p.val}
    let B := L × P
    let C := fun b : B ↦
      ((Fin b.2.val.val × (Σ j : Fin (h - b.1.val + 1),
        Fin ((2 ^ (74 * (h + 1))) ^ j.val))) → Fin n.val)
    let E := fun b : B ↦ EuclideanSpace ℝ (C b)
    let degree := fun p : P ↦
      (⟨p.val.val, p.property.1, p.property.2, Nat.le_of_lt_succ p.val.isLt⟩ :
        {p : ℕ // Even p ∧ 4 ≤ p ∧ p ≤ 2 ^ (64 * (h + 1))})
    let S := fun i : L ↦ ∑ j : Fin (h - i.val + 1), (2 ^ (74 * (h + 1))) ^ j.val
    let a := fun (i : L) (p : P) ↦ 1 / ((p.val.val : ℝ) ^ 4 * (S i : ℝ) ^ 2 *
      Real.sqrt ((h - i.val + 1 : ℕ) * Real.log (2 * (2 : ℝ) ^ (64 * (h + 1)) * S i)))
    let χ := fun r : ℝ ↦
      expNegInvGlue (r - 13 / 20) /
        (expNegInvGlue (r - 13 / 20) + expNegInvGlue (7 / 10 - r)) *
      (expNegInvGlue (1 - r) /
        (expNegInvGlue (1 - r) + expNegInvGlue (r - 19 / 20)))
    let tail := fun (i : L) (j : Fin (h - i.val + 1)) ↦ x ⟨i.val + j.val, by omega⟩
    let c := fun i : L ↦ ∏ j, χ (‖tail i j‖ / Real.sqrt n.val)
    let field := fun (i : L) (z : (p : P) → E (i, p)) ↦
      if ∃ j, tail i j = 0 then 0 else
        c i * ∑ p : P, angularDegreeComponent n h i (degree p)
          (fun j ↦ NormedSpace.normalize (tail i j)) (z p)
    let Ω := EuclideanSpace ℝ (Σ b : B, C b)
    let H := fun (ξ : Ω) (i : L) ↦ field i
      (fun p ↦ WithLp.toLp 2 (fun k : C (i, p) ↦ ξ ⟨(i, p), k⟩))
    let μ := stdGaussian Ω
    let W := fun ξ : Ω ↦ ∑ i : L, β i * H ξ i
    let V := (n.val : ℝ) * ∑ i : L, β i ^ 2 * (c i) ^ 2 * ∑ p : P, (a i p) ^ 2
    HasLaw W (gaussianReal 0 V.toNNReal) μ ∧
      Integrable (fun ξ ↦ Real.exp (-W ξ)) μ ∧
      (∫ ξ, Real.exp (-W ξ) ∂μ) = Real.exp (V / 2) := by
  intro L P B C E degree S a χ tail c field Ω H μ W V
  let v := fun i : L ↦ ∑ p : P, (a i p) ^ 2
  let σ := fun i : L ↦ (n.val : ℝ) * (c i) ^ 2 * v i
  let ν := fun i : L ↦ gaussianReal 0 (σ i).toNNReal
  let X := fun (i : L) (ξ : Ω) ↦ β i * H ξ i
  have hJoint : HasLaw H (Measure.pi ν) μ := radialLevels_hasLaw n h x
  have hMarginal (i : L) : HasLaw (fun ξ ↦ H ξ i) (ν i) μ := by
    have hEval := measurePreserving_eval (μ := ν) i
    have h := hEval.fun_comp_hasLaw hJoint
    exact h
  have hIndep : iIndepFun (fun i ξ ↦ H ξ i) μ :=
    (iIndepFun_iff_hasLaw_pi_pi hMarginal).2 hJoint
  have hXIndep : iIndepFun X μ :=
    hIndep.comp (fun i (z : ℝ) ↦ β i * z) (fun _ ↦ measurable_const.mul measurable_id)
  have hScale (i : L) :
      HasLaw (X i) (gaussianReal 0
        (NNReal.mk (β i ^ 2) (sq_nonneg (β i)) * (σ i).toNNReal)) μ := by
    simpa only [mul_zero] using gaussianReal_const_mul (hMarginal i) (β i)
  have hGauss (i : L) : HasGaussianLaw (X i) μ := (hScale i).hasGaussianLaw
  have hSum : HasGaussianLaw W μ := hXIndep.hasGaussianLaw_fun_sum hGauss
  have hMean : ∫ ξ, W ξ ∂μ = 0 := by
    change (∫ ξ, ∑ i : L, X i ξ ∂μ) = 0
    rw [integral_finsetSum _ (fun i _ ↦ (hGauss i).integrable)]
    simp only [fun i ↦ (hScale i).integral_eq, integral_id_gaussianReal, Finset.sum_const_zero]
  have hn : 0 ≤ (n.val : ℝ) := Nat.cast_nonneg _
  have hv (i : L) : 0 ≤ v i := Finset.sum_nonneg fun p _ ↦ sq_nonneg (a i p)
  have hσ (i : L) : 0 ≤ σ i := mul_nonneg (mul_nonneg hn (sq_nonneg (c i))) (hv i)
  have hVar : Var[W; μ] = V := by
    have hPointwise : W = ∑ i : L, X i := by
      funext ξ
      change (∑ i : L, X i ξ) = (∑ i : L, X i) ξ
      exact (Finset.sum_apply ξ Finset.univ X).symm
    change Var[W; μ] = (n.val : ℝ) * ∑ i : L, β i ^ 2 * (c i) ^ 2 * v i
    rw [hPointwise, IndepFun.variance_sum (X := X) (s := Finset.univ)
      (fun i _ ↦ (hGauss i).memLp_two)
      (fun i _ j _ hij ↦ hXIndep.indepFun hij), Finset.mul_sum]
    refine Finset.sum_congr rfl fun i _ ↦ ?_
    rw [(hScale i).variance_eq, variance_id_gaussianReal, NNReal.coe_mul, NNReal.coe_mk,
      Real.coe_toNNReal _ (hσ i)]
    change β i ^ 2 * ((n.val : ℝ) * (c i) ^ 2 * v i) =
      (n.val : ℝ) * (β i ^ 2 * (c i) ^ 2 * v i)
    ring
  have hW : HasLaw W (gaussianReal 0 V.toNNReal) μ :=
    ⟨hSum.aemeasurable, by rw [hSum.map_eq_gaussianReal, hMean, hVar]⟩
  have hV : 0 ≤ V := mul_nonneg hn
    (Finset.sum_nonneg fun i _ ↦
      mul_nonneg (mul_nonneg (sq_nonneg (β i)) (sq_nonneg (c i))) (hv i))
  have hMGF : mgf W μ (-1) = Real.exp (V / 2) := by
    rw [mgf_gaussianReal hW.map_eq, Real.coe_toNNReal _ hV]
    congr 1
    ring
  have hInt : Integrable (fun ξ ↦ Real.exp (-W ξ)) μ := by
    have h := (mgf_pos_iff (μ := μ) (X := W) (t := -1)).1
      (hMGF.symm ▸ Real.exp_pos _)
    simpa only [neg_one_mul] using h
  exact ⟨hW, hInt, by simpa only [mgf, neg_one_mul] using hMGF⟩

end AutoSamplingTheory.ExampleCases.SlcLsiQueryComplexity.WeightedRadialMGF
