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
  simp [RCLike.inner_apply, mul_comm]

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

private def liftReal (D : Lp ℝ 2 μ →L[ℝ] Lp ℝ 2 μ) :
    Lp ℂ 2 μ →L[ℝ] Lp ℂ 2 μ :=
  embed μ ∘L D ∘L realPart μ + Complex.I • (embed μ ∘L D ∘L imagPart μ)

private theorem liftReal_I (D : Lp ℝ 2 μ →L[ℝ] Lp ℝ 2 μ) (g : Lp ℂ 2 μ) :
    liftReal μ D (Complex.I • g) = Complex.I • liftReal μ D g := by
  change embed μ (D (realPart μ (Complex.I • g))) +
    Complex.I • embed μ (D (imagPart μ (Complex.I • g))) =
    Complex.I • (embed μ (D (realPart μ g)) + Complex.I • embed μ (D (imagPart μ g)))
  rw [real_I, imag_I, map_neg, map_neg]
  simp [smul_add, smul_smul, add_comm]

private def liftComplex (D : Lp ℝ 2 μ →L[ℝ] Lp ℝ 2 μ) :
    Lp ℂ 2 μ →L[ℂ] Lp ℂ 2 μ where
  toFun := liftReal μ D
  map_add' := (liftReal μ D).map_add
  map_smul' c g := by
    change liftReal μ D (c • g) = c • liftReal μ D g
    have hc : c • g = c.re • g + c.im • (Complex.I • g) := by
      rw [← Complex.re_add_im c, add_smul, mul_smul, Complex.coe_smul, Complex.coe_smul]
    rw [hc, map_add, map_smul, map_smul, liftReal_I]
    rw [← Complex.re_add_im c, add_smul, mul_smul, Complex.coe_smul, Complex.coe_smul]
  cont := (liftReal μ D).continuous

private theorem liftComplex_apply (D : Lp ℝ 2 μ →L[ℝ] Lp ℝ 2 μ) (g : Lp ℂ 2 μ) :
    liftComplex μ D g = embed μ (D (realPart μ g)) +
      Complex.I • embed μ (D (imagPart μ g)) := rfl

private theorem liftComplex_embed (D : Lp ℝ 2 μ →L[ℝ] Lp ℝ 2 μ) (u : Lp ℝ 2 μ) :
    liftComplex μ D (embed μ u) = embed μ (D u) := by
  simp only [liftComplex_apply, real_embed, imag_embed, map_zero, smul_zero, add_zero]

private theorem real_lift (D : Lp ℝ 2 μ →L[ℝ] Lp ℝ 2 μ) (g : Lp ℂ 2 μ) :
    realPart μ (liftComplex μ D g) = D (realPart μ g) := by
  simp only [liftComplex_apply, map_add, real_embed, real_I, imag_embed, neg_zero, add_zero]

private theorem imag_lift (D : Lp ℝ 2 μ →L[ℝ] Lp ℝ 2 μ) (g : Lp ℂ 2 μ) :
    imagPart μ (liftComplex μ D g) = D (imagPart μ g) := by
  simp only [liftComplex_apply, map_add, imag_embed, imag_I, real_embed, zero_add]

private theorem real_conjugate (g : Lp ℂ 2 μ) :
    realPart μ (conjugate μ g) = realPart μ g := by
  simp only [conjugate_parts, map_sub, real_embed, real_I, imag_embed, neg_zero, sub_zero]

private theorem imag_conjugate (g : Lp ℂ 2 μ) :
    imagPart μ (conjugate μ g) = -imagPart μ g := by
  simp only [conjugate_parts, map_sub, imag_embed, imag_I, real_embed, zero_sub]

private theorem liftComplex_conjugate (D : Lp ℝ 2 μ →L[ℝ] Lp ℝ 2 μ) (g : Lp ℂ 2 μ) :
    conjugate μ (liftComplex μ D g) = liftComplex μ D (conjugate μ g) := by
  rw [conjugate_parts, real_lift, imag_lift, liftComplex_apply, real_conjugate, imag_conjugate]
  simp only [map_neg, smul_neg, sub_eq_add_neg]

private theorem inner_lift (D : Lp ℝ 2 μ →L[ℝ] Lp ℝ 2 μ) (hD : D.IsPositive)
    (g : Lp ℂ 2 μ) :
    inner ℂ (liftComplex μ D g) g =
      ((inner ℝ (D (realPart μ g)) (realPart μ g) +
        inner ℝ (D (imagPart μ g)) (imagPart μ g) : ℝ) : ℂ) := by
  have hcross : inner ℝ (D (imagPart μ g)) (realPart μ g) =
      inner ℝ (D (realPart μ g)) (imagPart μ g) :=
    (hD.inner_left_eq_inner_right _ _).trans (real_inner_comm _ _)
  rw [liftComplex_apply]
  calc
    inner ℂ (embed μ (D (realPart μ g)) + Complex.I • embed μ (D (imagPart μ g))) g =
      inner ℂ (embed μ (D (realPart μ g)) + Complex.I • embed μ (D (imagPart μ g)))
        (embed μ (realPart μ g) + Complex.I • embed μ (imagPart μ g)) :=
      congrArg (inner ℂ (embed μ (D (realPart μ g)) + Complex.I • embed μ (D (imagPart μ g))))
        (parts μ g).symm
    _ = _ := by
      simp only [inner_add_left, inner_add_right, inner_smul_left, inner_smul_right, inner_embed]
      rw [hcross]
      simp only [map_add, Complex.conj_I]
      push_cast
      ring

private theorem liftComplex_positive (D : Lp ℝ 2 μ →L[ℝ] Lp ℝ 2 μ) (hD : D.IsPositive) :
    (liftComplex μ D).IsPositive := by
  apply ContinuousLinearMap.isPositive_iff_complex.mpr
  intro g
  rw [inner_lift μ D hD g]
  constructor
  · simp
  · simp only [Complex.ofReal_re]
    exact add_nonneg (hD.re_inner_nonneg_left (realPart μ g))
      (hD.re_inner_nonneg_left (imagPart μ g))

theorem exists_positive_complex_lift
    {Ω : Type*} [MeasurableSpace Ω] (μ : Measure Ω)
    (D : Lp ℝ 2 μ →L[ℝ] Lp ℝ 2 μ) (hD : D.IsPositive) :
    let ι : Lp ℝ 2 μ →L[ℝ] Lp ℂ 2 μ := Complex.ofRealCLM.compLpL 2 μ
    let R : Lp ℂ 2 μ →L[ℝ] Lp ℝ 2 μ := Complex.reCLM.compLpL 2 μ
    let Q : Lp ℂ 2 μ →L[ℝ] Lp ℝ 2 μ := Complex.imCLM.compLpL 2 μ
    let C : Lp ℂ 2 μ →L[ℝ] Lp ℂ 2 μ := Complex.conjCLE.toContinuousLinearMap.compLpL 2 μ
    (∀ u : Lp ℝ 2 μ, ‖ι u‖ = ‖u‖) ∧
    (∀ g : Lp ℂ 2 μ, C g = g ↔ ∃ u : Lp ℝ 2 μ, ι u = g) ∧
    ∃ Dc : Lp ℂ 2 μ →L[ℂ] Lp ℂ 2 μ,
      Dc.IsPositive ∧
      (∀ g : Lp ℂ 2 μ, Dc g = ι (D (R g)) + Complex.I • ι (D (Q g))) ∧
      (∀ u : Lp ℝ 2 μ, Dc (ι u) = ι (D u)) ∧
      (∀ g : Lp ℂ 2 μ, C (Dc g) = Dc (C g)) := by
  dsimp only
  refine ⟨norm_embed μ, fixed_range μ, liftComplex μ D, liftComplex_positive μ D hD,
    liftComplex_apply μ D, liftComplex_embed μ D, liftComplex_conjugate μ D⟩

end
end AutoSamplingTheory.TechnicalLemmas.Measure.L2RealComplexOperator
