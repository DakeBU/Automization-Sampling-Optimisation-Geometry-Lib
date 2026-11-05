import AutoSamplingTheory.ExampleCases.GaussianComplexity.MixtureDensities
import Mathlib.MeasureTheory.Function.L2Space
import Lean.Util.FoldConsts

open Matrix MeasureTheory
open scoped ENNReal
open AutoSamplingTheory.TechnicalLemmas.Probability.OrthogonalHaar
open AutoSamplingTheory.ExampleCases.GaussianComplexity.DeterminantFamily
open AutoSamplingTheory.ExampleCases.GaussianComplexity.MixtureDensities
set_option autoImplicit false

-- The actual density representatives supply the source's basic affinity range.
example {n : ℕ} (hn : 3 ≤ n) {κ : ℝ} (hκ : 4 ≤ κ) :
    let μ := orthogonalHaar n
    let νpos := (2 : ℝ≥0∞) • μ.restrict
      {O : Matrix.orthogonalGroup (Fin n) ℝ | (O : Matrix (Fin n) (Fin n) ℝ).det = 1}
    let νneg := (2 : ℝ≥0∞) • μ.restrict
      {O : Matrix.orthogonalGroup (Fin n) ℝ | (O : Matrix (Fin n) (Fin n) ℝ).det = -1}
    let γ : Matrix.orthogonalGroup (Fin n) ℝ → Measure (EuclideanSpace ℝ (Fin n)) :=
      fun O => ProbabilityTheory.multivariateGaussian (0 : EuclideanSpace ℝ (Fin n))
        (singleBlockPrecision κ O)⁻¹
    let p : Matrix.orthogonalGroup (Fin n) ℝ → EuclideanSpace ℝ (Fin n) → ℝ :=
      fun O x => Real.sqrt (singleBlockPrecision κ O).det /
        (2 * Real.pi) ^ ((n : ℝ) / 2) *
        Real.exp (-((WithLp.ofLp x) ⬝ᵥ
          (singleBlockPrecision κ O *ᵥ WithLp.ofLp x)) / 2)
    let qpos : EuclideanSpace ℝ (Fin n) → ℝ := fun x => ∫ O, p O x ∂νpos
    let qneg : EuclideanSpace ℝ (Fin n) → ℝ := fun x => ∫ O, p O x ∂νneg
    let a : ℝ := ∫ x, Real.sqrt (qpos x * qneg x)
    Integrable (fun x => Real.sqrt (qpos x * qneg x)) volume ∧ 0 ≤ a ∧ a ≤ 1 ∧
    νpos.bind γ = volume.withDensity (fun x => ENNReal.ofReal (qpos x)) ∧
    νneg.bind γ = volume.withDensity (fun x => ENNReal.ofReal (qneg x)) := by
  dsimp only
  have hd := actual_mixture_densities hn hκ
  dsimp only at hd
  have hbasic (f g : EuclideanSpace ℝ (Fin n) → ℝ)
      (hf0 : ∀ x, 0 ≤ f x) (hg0 : ∀ x, 0 ≤ g x)
      (hfm : Measurable f) (hgm : Measurable g)
      (hfi : Integrable f volume) (hgi : Integrable g volume)
      (hf1 : (∫ x, f x) = 1) (hg1 : (∫ x, g x) = 1) :
      Integrable (fun x => Real.sqrt (f x * g x)) volume ∧
        0 ≤ (∫ x, Real.sqrt (f x * g x)) ∧
        (∫ x, Real.sqrt (f x * g x)) ≤ 1 := by
    have hfsq : Integrable (fun x => (Real.sqrt (f x)) ^ 2) volume :=
      hfi.congr (Filter.Eventually.of_forall (fun x => (Real.sq_sqrt (hf0 x)).symm))
    have hgsq : Integrable (fun x => (Real.sqrt (g x)) ^ 2) volume :=
      hgi.congr (Filter.Eventually.of_forall (fun x => (Real.sq_sqrt (hg0 x)).symm))
    have hF : MemLp (fun x => Real.sqrt (f x)) 2 volume :=
      (memLp_two_iff_integrable_sq (by fun_prop)).2 hfsq
    have hG : MemLp (fun x => Real.sqrt (g x)) 2 volume :=
      (memLp_two_iff_integrable_sq (by fun_prop)).2 hgsq
    have hmul : Integrable (fun x => Real.sqrt (f x) * Real.sqrt (g x)) volume :=
      hF.integrable_mul hG
    have hc := integral_mul_le_Lp_mul_Lq_of_nonneg
      (p := 2) (q := 2) (Real.holderConjugate_iff.mpr (by norm_num))
      (Filter.Eventually.of_forall (fun x => Real.sqrt_nonneg (f x)))
      (Filter.Eventually.of_forall (fun x => Real.sqrt_nonneg (g x)))
      (by simpa using hF) (by simpa using hG)
    simp_rw [Real.rpow_two] at hc
    have hfs : (fun x => (Real.sqrt (f x)) ^ 2) = f :=
      funext (fun x => Real.sq_sqrt (hf0 x))
    have hgs : (fun x => (Real.sqrt (g x)) ^ 2) = g :=
      funext (fun x => Real.sq_sqrt (hg0 x))
    rw [hfs, hgs, hf1, hg1] at hc
    norm_num at hc
    have heq : (fun x => Real.sqrt (f x * g x)) =
        (fun x => Real.sqrt (f x) * Real.sqrt (g x)) :=
      funext (fun x => Real.sqrt_mul (hf0 x) (g x))
    refine ⟨heq.symm ▸ hmul, integral_nonneg (fun x => Real.sqrt_nonneg _), ?_⟩
    rw [heq]
    exact hc
  have ha := hbasic _ _ (fun x => (hd.1 x).1) (fun x => (hd.1 x).2)
    hd.2.1 hd.2.2.1 hd.2.2.2.1 hd.2.2.2.2.1
    hd.2.2.2.2.2.1 hd.2.2.2.2.2.2.1
  exact ⟨ha.1, ha.2.1, ha.2.2, hd.2.2.2.2.2.2.2.1, hd.2.2.2.2.2.2.2.2⟩

#print axioms actual_mixture_densities
open Lean in
run_cmd do
  let env ← getEnv
  let some info := env.find? `AutoSamplingTheory.ExampleCases.GaussianComplexity.MixtureDensities.actual_mixture_densities | throwError "Target missing"
  let some body := info.value? (allowOpaque := true) | throwError "Body missing"
  let parents := body.getUsedConstants.filter fun n =>
    n.toString.startsWith "AutoSamplingTheory" ||
    n.toString.contains "lintegral_lintegral_swap" ||
    n.toString.contains "integrableOn_compact" ||
    n.toString.contains "ofReal_integral_eq_lintegral_ofReal" ||
    n.toString.contains "integral_prod_left"
  logInfo m!"ACTUAL COMPILED PARENTS {parents}"
