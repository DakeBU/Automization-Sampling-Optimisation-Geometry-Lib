import Mathlib.Analysis.Calculus.ContDiff.Comp
import Mathlib.Analysis.Calculus.ContDiff.Operations
import Mathlib.Analysis.Normed.Module.FiniteDimension
import Mathlib.MeasureTheory.Function.Holder
import Mathlib.Probability.Distributions.Gaussian.Multivariate
import Mathlib.Tactic

open MeasureTheory ProbabilityTheory
open scoped ENNReal InnerProductSpace ContDiff

namespace AutoSamplingTheory.TechnicalLemmas.Probability.GaussianPolynomialRidgeSmooth

open scoped BigOperators

variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
  [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]

private theorem smooth_power_ridge (n : ℕ) (q : ℝ≥0∞) [Fact (1 ≤ q)] (hqtop : q ≠ ⊤) :
    ∃ F : E → Lp ℝ q (stdGaussian E), ContDiff ℝ (∞ : ℕ∞ω) F ∧
      ∀ w, (F w : E → ℝ) =ᵐ[stdGaussian E] fun x => ⟪w, x⟫_ℝ ^ n := by
  let μ := stdGaussian E
  induction n generalizing q with
  | zero =>
    have h : MemLp (fun _ : E => (1 : ℝ)) q μ := memLp_const _
    exact ⟨fun _ => h.toLp _, contDiff_const, fun w => by
      simpa only [pow_zero] using h.coeFn_toLp⟩
  | succ n ih =>
    have hq' : 1 ≤ 2 * q := (Fact.out : 1 ≤ q).trans (by rw [two_mul]; exact le_add_of_nonneg_right bot_le)
    have hq'top : 2 * q ≠ ⊤ := ENNReal.mul_ne_top (by norm_num) hqtop
    have : Fact (1 ≤ 2 * q) := ⟨hq'⟩
    have : ENNReal.HolderTriple (2 * q) (2 * q) q := ⟨by
      rw [ENNReal.mul_inv (.inl (by norm_num : (2 : ℝ≥0∞) ≠ 0))
        (.inl (by norm_num : (2 : ℝ≥0∞) ≠ ⊤)), ← add_mul, ← two_mul,
        ENNReal.mul_inv_cancel (by norm_num : (2 : ℝ≥0∞) ≠ 0) (by norm_num), one_mul]⟩
    obtain ⟨F, hF, hFa⟩ := ih (2 * q) hq'top
    have hlin (w : E) : MemLp (fun x : E => ⟪w, x⟫_ℝ) (2 * q) μ :=
      IsGaussian.memLp_dual μ (innerSL ℝ w) (2 * q) hq'top
    let L : E →ₗ[ℝ] Lp ℝ (2 * q) μ :=
      { toFun := fun w => (hlin w).toLp _
        map_add' := by
          intro u v
          apply Lp.ext
          filter_upwards [(hlin (u + v)).coeFn_toLp, (hlin u).coeFn_toLp,
            (hlin v).coeFn_toLp, Lp.coeFn_add ((hlin u).toLp _) ((hlin v).toLp _)]
            with x huv hu hv hsum
          rw [huv, hsum, Pi.add_apply, hu, hv, inner_add_left]
        map_smul' := by
          intro c w
          apply Lp.ext
          filter_upwards [(hlin (c • w)).coeFn_toLp, (hlin w).coeFn_toLp,
            Lp.coeFn_smul c ((hlin w).toLp _)] with x hcw hw hsmul
          rw [RingHom.id_apply, hcw, hsmul, Pi.smul_apply, hw, real_inner_smul_left, smul_eq_mul] }
    let B := ContinuousLinearMap.mul ℝ ℝ
    let M := B.holderL μ (2 * q) (2 * q) q
    refine ⟨fun w => M (F w) (L w), ?_, ?_⟩
    · exact (M.contDiff.comp hF).clm_apply L.toContinuousLinearMap.contDiff
    · intro w
      change ⇑(B.holder q (F w) ((hlin w).toLp _)) =ᵐ[μ] _
      filter_upwards [B.coeFn_holder (r := q) (F w) ((hlin w).toLp _), hFa w, (hlin w).coeFn_toLp]
        with x hmul hf hl
      rw [hmul, hf, hl, pow_succ]
      rfl

theorem standard_gaussian_polynomial_ridge_L2_smooth
    {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]
    (p : Polynomial ℝ) :
    ∃ h : ∀ w : E, MemLp (fun x : E => p.eval ⟪w, x⟫_ℝ) 2 (stdGaussian E),
      ContDiff ℝ (∞ : ℕ∞ω) (fun w : E => (h w).toLp (fun x : E => p.eval ⟪w, x⟫_ℝ)) := by
  have representation :
      ∃ F : E → Lp ℝ 2 (stdGaussian E), ContDiff ℝ (∞ : ℕ∞ω) F ∧
        ∀ w, (F w : E → ℝ) =ᵐ[stdGaussian E] fun x => p.eval ⟪w, x⟫_ℝ := by
    induction p using Polynomial.induction_on' with
    | add p r hp hr =>
      obtain ⟨F, hF, hFa⟩ := hp
      obtain ⟨G, hG, hGa⟩ := hr
      refine ⟨fun w => F w + G w, hF.add hG, fun w => ?_⟩
      filter_upwards [Lp.coeFn_add (F w) (G w), hFa w, hGa w] with x hsum hf hg
      simp only [hsum, Pi.add_apply, hf, hg, Polynomial.eval_add]
    | monomial n c =>
      obtain ⟨F, hF, hFa⟩ := smooth_power_ridge (E := E) n 2 (by norm_num)
      refine ⟨fun w => c • F w, hF.const_smul c, fun w => ?_⟩
      filter_upwards [Lp.coeFn_smul c (F w), hFa w] with x hsmul hf
      simp only [hsmul, Pi.smul_apply, smul_eq_mul, hf, Polynomial.eval_monomial]
  obtain ⟨F, hF, hFa⟩ := representation
  let h : ∀ w : E, MemLp (fun x : E => p.eval ⟪w, x⟫_ℝ) 2 (stdGaussian E) :=
    fun w => (memLp_congr_ae (hFa w)).1 (Lp.memLp (F w))
  refine ⟨h, ?_⟩
  convert hF using 1
  funext w
  exact Lp.ext ((h w).coeFn_toLp.trans (hFa w).symm)

#print axioms standard_gaussian_polynomial_ridge_L2_smooth

end AutoSamplingTheory.TechnicalLemmas.Probability.GaussianPolynomialRidgeSmooth
