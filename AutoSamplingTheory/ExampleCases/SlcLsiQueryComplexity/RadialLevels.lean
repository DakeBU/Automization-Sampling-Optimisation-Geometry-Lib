/-
Copyright (c) 2026 Samplinglib contributors. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
-/
import AutoSamplingTheory.ExampleCases.SlcLsiQueryComplexity.RadialLevel

open MeasureTheory ProbabilityTheory
open scoped BigOperators Classical
open AutoSamplingTheory.ExampleCases.SlcLsiQueryComplexity.AngularDegree

/-!
# Joint law of the actual radial levels at one location

Zhou–Suzuki, arXiv:2611.05813v1 (CC BY 4.0), Lemma 4.4 and the fixed-location
Gaussian calculation preceding Eq. (51). The degree-block product of the
actual coefficient vector regroups by level. Each scalar level is a
measurable function of its own group, with the previously proved marginal.
No joint-in-location, weighted-sum, or conditional claim is made here.
-/

namespace AutoSamplingTheory.ExampleCases.SlcLsiQueryComplexity.RadialLevels

open CoefficientBlocks RadialLevel

/-- The literal zero-extended radial fields at a single deterministic location
have the product of their exact one-point Gaussian laws, including Dirac factors. -/
theorem radialLevels_hasLaw (n : ℕ+) (h : ℕ)
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
    HasLaw H (Measure.pi fun i : L ↦
      gaussianReal 0 (((n.val : ℝ) * (c i) ^ 2 * ∑ p : P, (a i p) ^ 2).toNNReal))
      (stdGaussian Ω) := by
  intro L P B C E degree S a χ tail c field Ω H
  let μ : Measure Ω := stdGaussian Ω
  let ν := fun b : B ↦ stdGaussian (E b)
  let block := fun (ξ : Ω) (b : B) ↦
    (WithLp.toLp 2 (fun k : C b ↦ ξ ⟨b, k⟩) : E b)
  let e := Equiv.sigmaEquivProd L P
  let reindex := MeasurableEquiv.piCongrLeft E e
  let split := MeasurableEquiv.piCurry (fun (i : L) (p : P) ↦ E (i, p))
  let νL := fun i : L ↦ Measure.pi (fun p : P ↦ ν (i, p))
  let groups := fun (ξ : Ω) (i : L) (p : P) ↦ block ξ (i, p)
  let target := fun i : L ↦
    gaussianReal 0 (((n.val : ℝ) * (c i) ^ 2 * ∑ p : P, (a i p) ^ 2).toNNReal)
  change HasLaw H (Measure.pi target) μ
  have hBlock : HasLaw block (Measure.pi ν) μ := jointCoefficientBlocks_hasLaw n h
  have hReindex : HasLaw reindex.symm (Measure.pi fun s ↦ ν (e s)) (Measure.pi ν) :=
    ⟨reindex.symm.measurable.aemeasurable,
      ((reindex.map_apply_eq_iff_map_symm_apply_eq).mp (Measure.pi_map_piCongrLeft e ν)).symm⟩
  have hSplit : HasLaw split (Measure.pi νL) (Measure.pi fun s ↦ ν (e s)) :=
    ⟨split.measurable.aemeasurable, by
      change (Measure.pi fun s : (Σ _ : L, P) ↦ ν (s.1, s.2)).map split = Measure.pi νL
      simpa only [split, νL, Measure.infinitePi_eq_pi] using
        Measure.infinitePi_map_piCurry (fun (i : L) (p : P) ↦ ν (i, p))⟩
  have hGroup : HasLaw groups (Measure.pi νL) μ := by
    have h := hSplit.comp (hReindex.comp hBlock)
    exact h
  have hmField (i : L) : Measurable (field i) := by
    dsimp only [field, E]
    by_cases hz : ∃ j, tail i j = 0
    · simp only [if_pos hz]
      exact measurable_const
    · simp only [if_neg hz, angularDegreeComponent]
      fun_prop
  have hFactor (i : L) : (νL i).map (field i) = target i := by
    have hEval := measurePreserving_eval (μ := νL) i
    have hG := hEval.fun_comp_hasLaw hGroup
    have hLocal : HasLaw (field i) ((νL i).map (field i)) (νL i) :=
      ⟨(hmField i).aemeasurable, rfl⟩
    have hMapped : HasLaw (fun ξ ↦ H ξ i) ((νL i).map (field i)) μ :=
      hLocal.fun_comp hG
    have hMarginal : μ.map (fun ξ ↦ H ξ i) = target i := by
      have hSlots : ((∑ j : Fin (h - i.val + 1),
          (2 ^ (74 * (h + 1))) ^ j.val : ℕ) : ℝ) = S i := by
        simp only [S, Nat.cast_sum, Nat.cast_pow, Nat.cast_ofNat]
      have h := (radialLevel_hasLaw n h i (tail i)).map_eq
      dsimp only at h
      rw [hSlots] at h
      dsimp only [μ, H, field, Ω, target, E, χ, c, a, degree, B, C, L, P]
      exact h
    exact hMapped.map_eq.symm.trans hMarginal
  let : ∀ i, SigmaFinite ((νL i).map (field i)) := by
    intro i
    rw [hFactor i]
    infer_instance
  let evaluate := fun (z : (i : L) → (p : P) → E (i, p)) (i : L) ↦ field i (z i)
  have hEvaluate : HasLaw evaluate (Measure.pi target) (Measure.pi νL) := by
    refine ⟨(measurable_pi_lambda _ (fun i ↦
      (hmField i).comp (measurable_pi_apply i))).aemeasurable, ?_⟩
    rw [show (Measure.pi νL).map evaluate =
      Measure.pi (fun i ↦ (νL i).map (field i)) from
        Measure.pi_map_pi (fun i ↦ (hmField i).aemeasurable)]
    exact congrArg Measure.pi (funext hFactor)
  exact hEvaluate.comp hGroup

end AutoSamplingTheory.ExampleCases.SlcLsiQueryComplexity.RadialLevels
