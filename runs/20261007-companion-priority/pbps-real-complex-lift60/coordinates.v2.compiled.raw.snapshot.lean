import Mathlib.MeasureTheory.Function.L2Space
import Mathlib.MeasureTheory.Integral.Bochner.ContinuousLinearMap
import Mathlib.Analysis.Complex.Basic
import Mathlib.Analysis.InnerProductSpace.Positive

open MeasureTheory
open scoped ENNReal ComplexConjugate

namespace AutoSamplingTheory.TechnicalLemmas.Measure.L2RealComplexOperator
noncomputable section
set_option autoImplicit false
set_option maxHeartbeats 1000000

variable {Ω : Type*} [MeasurableSpace Ω] (μ : Measure Ω)

private abbrev embed : Lp ℝ 2 μ →L[ℝ] Lp ℂ 2 μ := Complex.ofRealCLM.compLpL 2 μ
private abbrev realPart : Lp ℂ 2 μ →L[ℝ] Lp ℝ 2 μ := Complex.reCLM.compLpL 2 μ
private abbrev imagPart : Lp ℂ 2 μ →L[ℝ] Lp ℝ 2 μ := Complex.imCLM.compLpL 2 μ
private abbrev conjugate : Lp ℂ 2 μ →L[ℝ] Lp ℂ 2 μ :=
  Complex.conjCLE.toContinuousLinearMap.compLpL 2 μ

private theorem real_embed (u : Lp ℝ 2 μ) : realPart μ (embed μ u) = u := by
  apply Lp.ext
  filter_upwards [Complex.reCLM.coeFn_compLpL (embed μ u),
    Complex.ofRealCLM.coeFn_compLpL u] with x hr he
  change (realPart μ (embed μ u)) x = u x
  rw [hr, he]
  simp

private theorem imag_embed (u : Lp ℝ 2 μ) : imagPart μ (embed μ u) = 0 := by
  apply Lp.ext
  filter_upwards [Complex.imCLM.coeFn_compLpL (embed μ u),
    Complex.ofRealCLM.coeFn_compLpL u, Lp.coeFn_zero ℝ 2 μ] with x hi he hz
  change (imagPart μ (embed μ u)) x = (0 : Lp ℝ 2 μ) x
  rw [hi, he, hz]
  simp

private theorem parts (g : Lp ℂ 2 μ) :
    embed μ (realPart μ g) + Complex.I • embed μ (imagPart μ g) = g := by
  apply Lp.ext
  filter_upwards [Complex.ofRealCLM.coeFn_compLpL (realPart μ g),
    Complex.ofRealCLM.coeFn_compLpL (imagPart μ g),
    Complex.reCLM.coeFn_compLpL g, Complex.imCLM.coeFn_compLpL g,
    Lp.coeFn_add (embed μ (realPart μ g)) (Complex.I • embed μ (imagPart μ g)),
    Lp.coeFn_smul Complex.I (embed μ (imagPart μ g))] with x her hei hr hi ha hs
  rw [ha, Pi.add_apply, hs, Pi.smul_apply, her, hei, hr, hi]
  simpa [smul_eq_mul, mul_comm] using Complex.re_add_im (g x)

private theorem real_I (g : Lp ℂ 2 μ) :
    realPart μ (Complex.I • g) = -imagPart μ g := by
  apply Lp.ext
  filter_upwards [Complex.reCLM.coeFn_compLpL (Complex.I • g),
    Complex.imCLM.coeFn_compLpL g, Lp.coeFn_smul Complex.I g,
    Lp.coeFn_neg (imagPart μ g)] with x hr hi hs hn
  rw [hr, hn, Pi.neg_apply, hi, hs, Pi.smul_apply]
  simp [smul_eq_mul]

private theorem imag_I (g : Lp ℂ 2 μ) :
    imagPart μ (Complex.I • g) = realPart μ g := by
  apply Lp.ext
  filter_upwards [Complex.imCLM.coeFn_compLpL (Complex.I • g),
    Complex.reCLM.coeFn_compLpL g, Lp.coeFn_smul Complex.I g] with x hi hr hs
  rw [hi, hr, hs]
  simp [smul_eq_mul]

private theorem inner_embed (u v : Lp ℝ 2 μ) :
    inner ℂ (embed μ u) (embed μ v) = (inner ℝ u v : ℂ) := by
  rw [L2.inner_def, L2.inner_def, ← integral_complex_ofReal]
  apply integral_congr_ae
  filter_upwards [Complex.ofRealCLM.coeFn_compLpL u,
    Complex.ofRealCLM.coeFn_compLpL v] with x hu hv
  rw [hu, hv]
  simp [RCLike.inner_apply, Real.inner_apply, mul_comm]

private theorem norm_embed (u : Lp ℝ 2 μ) : ‖embed μ u‖ = ‖u‖ := by
  have hsq : ‖embed μ u‖ ^ 2 = ‖u‖ ^ 2 := by
    rw [← inner_self_eq_norm_sq (𝕜 := ℂ) (embed μ u)]
    change (inner ℂ (embed μ u) (embed μ u)).re = ‖u‖ ^ 2
    rw [inner_embed, Complex.ofReal_re, real_inner_self_eq_norm_sq]
  nlinarith [norm_nonneg (embed μ u), norm_nonneg u]

private theorem conjugate_embed (u : Lp ℝ 2 μ) :
    conjugate μ (embed μ u) = embed μ u := by
  apply Lp.ext
  filter_upwards [Complex.conjCLE.toContinuousLinearMap.coeFn_compLpL (embed μ u),
    Complex.ofRealCLM.coeFn_compLpL u] with x hc he
  rw [hc, he]
  simp

private theorem conjugate_parts (g : Lp ℂ 2 μ) :
    conjugate μ g = embed μ (realPart μ g) - Complex.I • embed μ (imagPart μ g) := by
  apply Lp.ext
  filter_upwards [Complex.conjCLE.toContinuousLinearMap.coeFn_compLpL g,
    Complex.ofRealCLM.coeFn_compLpL (realPart μ g),
    Complex.ofRealCLM.coeFn_compLpL (imagPart μ g),
    Complex.reCLM.coeFn_compLpL g, Complex.imCLM.coeFn_compLpL g,
    Lp.coeFn_sub (embed μ (realPart μ g)) (Complex.I • embed μ (imagPart μ g)),
    Lp.coeFn_smul Complex.I (embed μ (imagPart μ g))] with x hc her hei hr hi hsub hs
  rw [hc, hsub, Pi.sub_apply, hs, Pi.smul_apply, her, hei, hr, hi]
  apply Complex.ext <;> simp [smul_eq_mul]

private theorem fixed_range (g : Lp ℂ 2 μ) :
    conjugate μ g = g ↔ ∃ u : Lp ℝ 2 μ, embed μ u = g := by
  constructor
  · intro h
    refine ⟨realPart μ g, ?_⟩
    apply Lp.ext
    filter_upwards [Complex.conjCLE.toContinuousLinearMap.coeFn_compLpL g,
      Complex.ofRealCLM.coeFn_compLpL (realPart μ g),
      Complex.reCLM.coeFn_compLpL g] with x hc he hr
    have hz : conj (g x) = g x := by simpa [h] using hc.symm
    have him : (g x).im = 0 := by
      have hi := congrArg Complex.im hz
      simp only [Complex.conj_im] at hi
      linarith
    rw [he, hr]
    apply Complex.ext <;> simp [him]
  · rintro ⟨u, rfl⟩
    exact conjugate_embed μ u

end
end AutoSamplingTheory.TechnicalLemmas.Measure.L2RealComplexOperator
