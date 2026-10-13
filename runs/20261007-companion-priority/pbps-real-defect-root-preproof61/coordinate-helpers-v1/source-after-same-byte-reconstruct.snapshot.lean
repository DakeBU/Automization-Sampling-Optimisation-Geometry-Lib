import AutoSamplingTheory.TechnicalLemmas.Measure.L2RealComplexOperator
import Mathlib.Analysis.InnerProductSpace.StarOrder
import Mathlib.Analysis.CStarAlgebra.ContinuousFunctionalCalculus.Instances
import Mathlib.Analysis.SpecialFunctions.ContinuousFunctionalCalculus.Rpow.Basic

open MeasureTheory
open scoped ENNReal ComplexConjugate

namespace AutoSamplingTheory.TechnicalLemmas.Measure.L2RealSquareRoot
noncomputable section
set_option autoImplicit false
set_option maxHeartbeats 1000000

variable {Ω : Type*} [MeasurableSpace Ω] (μ : Measure Ω)

private abbrev embed : Lp ℝ 2 μ →L[ℝ] Lp ℂ 2 μ := Complex.ofRealCLM.compLpL 2 μ
private abbrev realPart : Lp ℂ 2 μ →L[ℝ] Lp ℝ 2 μ := Complex.reCLM.compLpL 2 μ
private abbrev conjugate : Lp ℂ 2 μ →L[ℝ] Lp ℂ 2 μ :=
  Complex.conjCLE.toContinuousLinearMap.compLpL 2 μ

private theorem real_embed (u : Lp ℝ 2 μ) : realPart μ (embed μ u) = u := by
  apply Lp.ext
  filter_upwards [Complex.reCLM.coeFn_compLpL (embed μ u),
    Complex.ofRealCLM.coeFn_compLpL u] with x hr he
  change (realPart μ (embed μ u)) x = u x
  rw [hr, he]
  simp

private theorem inner_embed (u v : Lp ℝ 2 μ) :
    inner ℂ (embed μ u) (embed μ v) = (inner ℝ u v : ℂ) := by
  rw [L2.inner_def, L2.inner_def, ← integral_complex_ofReal]
  apply integral_congr_ae
  filter_upwards [Complex.ofRealCLM.coeFn_compLpL u,
    Complex.ofRealCLM.coeFn_compLpL v] with x hu hv
  rw [hu, hv]
  simp [RCLike.inner_apply, mul_comm]

private theorem conjugate_involutive (g : Lp ℂ 2 μ) :
    conjugate μ (conjugate μ g) = g := by
  apply Lp.ext
  filter_upwards [Complex.conjCLE.toContinuousLinearMap.coeFn_compLpL (conjugate μ g),
    Complex.conjCLE.toContinuousLinearMap.coeFn_compLpL g] with x h1 h2
  rw [h1, h2]
  simp

private theorem conjugate_smul (c : ℂ) (g : Lp ℂ 2 μ) :
    conjugate μ (c • g) = conj c • conjugate μ g := by
  apply Lp.ext
  filter_upwards [Complex.conjCLE.toContinuousLinearMap.coeFn_compLpL (c • g),
    Complex.conjCLE.toContinuousLinearMap.coeFn_compLpL g,
    Lp.coeFn_smul c g, Lp.coeFn_smul (conj c) (conjugate μ g)] with x h1 h2 hs ht
  rw [h1, ht, Pi.smul_apply, h2, hs, Pi.smul_apply]
  simp [smul_eq_mul]

private theorem inner_conjugate (g h : Lp ℂ 2 μ) :
    inner ℂ (conjugate μ g) (conjugate μ h) = conj (inner ℂ g h) := by
  rw [L2.inner_def, L2.inner_def]
  rw [← Complex.conjCLE.integral_comp_comm]
  apply integral_congr_ae
  filter_upwards [Complex.conjCLE.toContinuousLinearMap.coeFn_compLpL g,
    Complex.conjCLE.toContinuousLinearMap.coeFn_compLpL h] with x hg hh
  rw [hg, hh]
  simp [RCLike.inner_apply]

private def conjugateOperator (A : Lp ℂ 2 μ →L[ℂ] Lp ℂ 2 μ) :
    Lp ℂ 2 μ →L[ℂ] Lp ℂ 2 μ where
  toFun g := conjugate μ (A (conjugate μ g))
  map_add' g h := by simp only [map_add]
  map_smul' c g := by
    change conjugate μ (A (conjugate μ (c • g))) = c • conjugate μ (A (conjugate μ g))
    rw [conjugate_smul, map_smul, conjugate_smul, Complex.conj_conj]
  cont := (conjugate μ).continuous.comp (A.continuous.comp (conjugate μ).continuous)

end
end AutoSamplingTheory.TechnicalLemmas.Measure.L2RealSquareRoot
