import AutoSamplingTheory.TechnicalLemmas.InformationTheory.ProductEntropy
import AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.GaussianCompactLogSobolev
import Mathlib.MeasureTheory.Integral.Pi
import Mathlib.Analysis.Calculus.ContDiff.Operations
import Mathlib.Analysis.Calculus.FDeriv.Const
import Mathlib.Analysis.Calculus.Deriv.Pi
import Mathlib.Analysis.Calculus.Deriv.Comp
import Mathlib.Topology.Algebra.Module.Equiv

/-! Compact finite-product Gaussian log-Sobolev background. Coordinate energy
is the sum of squared directional derivatives; the default Pi operator norm
is a different quantity. Hilbert transport and noncompact extension are separate.
The compact Pi result keeps Hilbert transport, noncompact extension and paper
main results as separate boundaries. -/

open MeasureTheory ProbabilityTheory
open scoped Topology BigOperators

namespace AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.GaussianCompactProductLogSobolev

private theorem compact_domains
    (n : ℕ) (f : (Fin n → ℝ) → ℝ)
    (hf : ContDiff ℝ 2 f) (hs : HasCompactSupport f) :
    let γ : Measure (Fin n → ℝ) := Measure.pi (fun _ : Fin n => gaussianReal 0 1)
    let D : Fin n → (Fin n → ℝ) → ℝ := fun i x => fderiv ℝ f x (Pi.single i 1)
    Integrable (fun x => (f x)^2) γ ∧
    Integrable (fun x => (f x)^2 * Real.log ((f x)^2)) γ ∧
    (∀ i, Integrable (fun x => (D i x)^2) γ) ∧
    Integrable (fun x => ∑ i, (D i x)^2) γ := by
  dsimp only
  have hA : Continuous (fun x => (f x)^2) := hf.continuous.pow 2
  have sA : HasCompactSupport (fun x => (f x)^2) := by
    simpa only [Function.comp_def] using hs.comp_left (g := fun t : ℝ => t^2) (by simp)
  have hB : Continuous (fun x => (f x)^2 * Real.log ((f x)^2)) :=
    Real.continuous_mul_log.comp hA
  have sB : HasCompactSupport (fun x => (f x)^2 * Real.log ((f x)^2)) := by
    simpa only [Function.comp_def] using
      sA.comp_left (g := fun t : ℝ => t * Real.log t) (by simp)
  have iD : ∀ i : Fin n, Integrable (fun x => (fderiv ℝ f x (Pi.single i 1))^2)
      (Measure.pi (fun _ : Fin n => gaussianReal 0 1)) := by
    intro i
    have hc : Continuous (fun x => fderiv ℝ f x (Pi.single i 1)) :=
      (hf.continuous_fderiv (by norm_num)).clm_apply continuous_const
    have sc : HasCompactSupport (fun x => (fderiv ℝ f x (Pi.single i 1))^2) := by
      simpa only [Function.comp_def] using
        (hs.fderiv_apply ℝ (Pi.single i 1)).comp_left (g := fun t : ℝ => t^2) (by simp)
    exact (hc.pow 2).integrable_of_hasCompactSupport sc
  exact ⟨hA.integrable_of_hasCompactSupport sA,
    hB.integrable_of_hasCompactSupport sB, iD,
    integrable_finsetSum _ (fun i _ => iD i)⟩

private theorem original_slices
    (n : ℕ) (f : (Fin (n+1) → ℝ) → ℝ)
    (hf : ContDiff ℝ 2 f) (hs : HasCompactSupport f) :
    (∀ y : Fin n → ℝ,
      ContDiff ℝ 2 (fun a : ℝ => f (Fin.cons a y)) ∧
      HasCompactSupport (fun a : ℝ => f (Fin.cons a y))) ∧
    (∀ a : ℝ,
      ContDiff ℝ 2 (fun y : Fin n → ℝ => f (Fin.cons a y)) ∧
      HasCompactSupport (fun y : Fin n → ℝ => f (Fin.cons a y))) := by
  let e := Fin.consEquivL ℝ (fun _ : Fin (n+1) => ℝ)
  have he : ContDiff ℝ 2 e := e.toContinuousLinearMap.contDiff
  constructor
  · intro y
    have hc : ContDiff ℝ 2 (fun a : ℝ => f (e (a, y))) :=
      hf.comp (he.comp (contDiff_prodMk_left y))
    have hd : Topology.IsClosedEmbedding (fun a : ℝ => e (a, y)) :=
      e.toHomeomorph.isClosedEmbedding.comp
        ⟨isEmbedding_prodMkLeft y, by
          simpa only [Set.image_univ] using
            (isClosedMap_prodMk_right y) (Set.univ : Set ℝ) isClosed_univ⟩
    exact ⟨hc, hs.comp_isClosedEmbedding hd⟩
  · intro a
    have hc : ContDiff ℝ 2 (fun y : Fin n → ℝ => f (e (a, y))) :=
      hf.comp (he.comp (contDiff_prodMk_right a))
    have hd : Topology.IsClosedEmbedding (fun y : Fin n → ℝ => e (a, y)) :=
      e.toHomeomorph.isClosedEmbedding.comp
        ⟨isEmbedding_prodMkRight a, by
          simpa only [Set.image_univ] using
            (isClosedMap_prodMk_left a) (Set.univ : Set (Fin n → ℝ)) isClosed_univ⟩
    exact ⟨hc, hs.comp_isClosedEmbedding hd⟩

private theorem split_law (n : ℕ) :
    MeasurePreserving (fun z : ℝ × (Fin n → ℝ) => Fin.cons z.1 z.2)
      ((gaussianReal 0 1).prod (Measure.pi (fun _ : Fin n => gaussianReal 0 1)))
      (Measure.pi (fun _ : Fin (n+1) => gaussianReal 0 1)) := by
  have h := (measurePreserving_piFinSuccAbove
    (fun _ : Fin (n+1) => gaussianReal 0 1) 0).symm
  simpa only [MeasurableEquiv.piFinSuccAbove_symm_apply, Fin.insertNthEquiv,
    Equiv.coe_fn_mk, Fin.insertNth_zero, cast_eq] using h

private theorem empty_entropy (f : (Fin 0 → ℝ) → ℝ) :
    (∫ x, (f x)^2 * Real.log ((f x)^2)
      ∂Measure.pi (fun _ : Fin 0 => gaussianReal 0 1)) -
      (∫ x, (f x)^2 ∂Measure.pi (fun _ : Fin 0 => gaussianReal 0 1)) *
        Real.log (∫ x, (f x)^2 ∂Measure.pi (fun _ : Fin 0 => gaussianReal 0 1)) ≤
    2 * ∫ x, (∑ i : Fin 0, (fderiv ℝ f x (Pi.single i 1))^2)
      ∂Measure.pi (fun _ : Fin 0 => gaussianReal 0 1) := by
  let c := f 0
  have hconst : f = fun _ => c := by
    funext x
    congr 1
    exact Subsingleton.elim x 0
  rw [hconst]
  simp

private theorem coordinate_derivatives
    (n : ℕ) (f : (Fin (n+1) → ℝ) → ℝ)
    (hf : ContDiff ℝ 2 f) (hs : HasCompactSupport f)
    (a : ℝ) (y : Fin n → ℝ) :
    deriv (fun t : ℝ => f (Fin.cons t y)) a =
      fderiv ℝ f (Fin.cons a y) (Pi.single 0 1) ∧
    (∀ i : Fin n,
      fderiv ℝ (fun z : Fin n → ℝ => f (Fin.cons a z)) y (Pi.single i 1) =
      fderiv ℝ f (Fin.cons a y) (Pi.single i.succ 1)) := by
  constructor
  · have h := ((hf.differentiable (by norm_num))
      (Function.update (Fin.cons 0 y) 0 a)).hasFDerivAt.comp_hasDerivAt a
        (hasDerivAt_update (Fin.cons 0 y) 0 a)
    simpa only [Function.comp_def, Fin.update_cons_zero] using h.deriv
  · intro i
    have ht := (original_slices n f hf hs).2 a |>.1
    have h1 := ((ht.differentiable (by norm_num))
      (Function.update y i (y i))).hasFDerivAt.comp_hasDerivAt
      (y i) (hasDerivAt_update y i (y i))
    have h2 := ((hf.differentiable (by norm_num))
      (Function.update (Fin.cons a y) i.succ (y i))).hasFDerivAt.comp_hasDerivAt
      (y i) (hasDerivAt_update (Fin.cons a y) i.succ (y i))
    have heq : (fun t : ℝ => f (Fin.cons a (Function.update y i t))) =
        (fun t : ℝ => f (Function.update (Fin.cons a y) i.succ t)) := by
      funext t
      rw [Fin.cons_update]
    have hd1 := h1.deriv
    have hd2 := h2.deriv
    have hup : Function.update (Fin.cons a y : Fin (n+1) → ℝ) i.succ (y i) =
        (Fin.cons a y : Fin (n+1) → ℝ) :=
      Function.update_eq_self i.succ (Fin.cons a y : Fin (n+1) → ℝ)
    simp only [Function.comp_def, Function.update_eq_self] at hd1
    simp only [Function.comp_def, hup] at hd2
    rw [heq] at hd1
    exact hd1.symm.trans hd2

private theorem split_square_class
    (n : ℕ) (f : (Fin (n+1) → ℝ) → ℝ)
    (hf : ContDiff ℝ 2 f) (hs : HasCompactSupport f) :
    let F : ℝ × (Fin n → ℝ) → ℝ := fun z => (f (Fin.cons z.1 z.2))^2
    Measurable F ∧ (∀ z, 0 ≤ F z) ∧ (∃ C : ℝ, ∀ z, F z ≤ C) := by
  dsimp only
  let e := Fin.consEquivL ℝ (fun _ : Fin (n+1) => ℝ)
  have hc : Continuous (fun z : ℝ × (Fin n → ℝ) => (f (e z))^2) :=
    (hf.continuous.comp e.continuous).pow 2
  obtain ⟨D, hD⟩ := hs.exists_bound_of_continuous hf.continuous
  let K := max D 0
  refine ⟨hc.measurable, fun z => sq_nonneg _, K^2, ?_⟩
  intro z
  have hb : |f (Fin.cons z.1 z.2)| ≤ K := by
    simpa only [Real.norm_eq_abs] using (hD (Fin.cons z.1 z.2)).trans (le_max_left D 0)
  have h := abs_le.mp hb
  nlinarith [mul_nonneg (sub_nonneg.mpr h.2) (sub_nonneg.mpr h.1)]

private theorem split_entropy_bound
    (n : ℕ) (f : (Fin (n+1) → ℝ) → ℝ)
    (hf : ContDiff ℝ 2 f) (hs : HasCompactSupport f) :
    let μ : Measure ℝ := gaussianReal 0 1
    let ν : Measure (Fin n → ℝ) := Measure.pi (fun _ : Fin n => gaussianReal 0 1)
    let F : ℝ × (Fin n → ℝ) → ℝ := fun z => (f (Fin.cons z.1 z.2))^2
    let Φ : ℝ → ℝ := fun t => t * Real.log t
    let U : ℝ → ℝ := fun a =>
      (∫ y, Φ (F (a,y)) ∂ν) - Φ (∫ y, F (a,y) ∂ν)
    let V : (Fin n → ℝ) → ℝ := fun y =>
      (∫ a, Φ (F (a,y)) ∂μ) - Φ (∫ a, F (a,y) ∂μ)
    Integrable U μ ∧ Integrable V ν ∧
    (∫ z, Φ (F z) ∂μ.prod ν) - Φ (∫ z, F z ∂μ.prod ν) ≤
      (∫ a, U a ∂μ) + (∫ y, V y ∂ν) := by
  dsimp only
  let μ : Measure ℝ := gaussianReal 0 1
  let ν : Measure (Fin n → ℝ) := Measure.pi (fun _ : Fin n => gaussianReal 0 1)
  let F : ℝ × (Fin n → ℝ) → ℝ := fun z => (f (Fin.cons z.1 z.2))^2
  let Φ : ℝ → ℝ := fun t => t * Real.log t
  rcases split_square_class n f hf hs with ⟨hF, hF0, hFb⟩
  rcases AutoSamplingTheory.TechnicalLemmas.InformationTheory.ProductEntropy.bounded_product_entropy_subadditivity
      μ ν F hF hF0 hFb with ⟨_, iΦ, _, _, _, _, iA, iB, hEnt⟩
  have iU : Integrable (fun a =>
      (∫ y, Φ (F (a,y)) ∂ν) - Φ (∫ y, F (a,y) ∂ν)) μ :=
    iΦ.integral_prod_left.sub iA
  have iV : Integrable (fun y =>
      (∫ a, Φ (F (a,y)) ∂μ) - Φ (∫ a, F (a,y) ∂μ)) ν :=
    iΦ.integral_prod_right.sub iB
  refine ⟨iU, iV, ?_⟩
  have hU : (∫ a, ((∫ y, Φ (F (a,y)) ∂ν) - Φ (∫ y, F (a,y) ∂ν)) ∂μ) =
      (∫ z, Φ (F z) ∂μ.prod ν) - (∫ a, Φ (∫ y, F (a,y) ∂ν) ∂μ) := by
    rw [integral_sub iΦ.integral_prod_left iA, ← integral_prod _ iΦ]
  have hV : (∫ y, ((∫ a, Φ (F (a,y)) ∂μ) - Φ (∫ a, F (a,y) ∂μ)) ∂ν) =
      (∫ z, Φ (F z) ∂μ.prod ν) - (∫ y, Φ (∫ a, F (a,y) ∂μ) ∂ν) := by
    rw [integral_sub iΦ.integral_prod_right iB, ← integral_prod_symm _ iΦ]
  change (∫ z, Φ (F z) ∂μ.prod ν) - Φ (∫ z, F z ∂μ.prod ν) ≤
    (∫ a, ((∫ y, Φ (F (a,y)) ∂ν) - Φ (∫ y, F (a,y) ∂ν)) ∂μ) +
    (∫ y, ((∫ a, Φ (F (a,y)) ∂μ) - Φ (∫ a, F (a,y) ∂μ)) ∂ν)
  rw [hU, hV]
  linarith

private theorem finite_lsi
    (n : ℕ) (f : (Fin n → ℝ) → ℝ)
    (hf : ContDiff ℝ 2 f) (hs : HasCompactSupport f) :
    (∫ x, (f x)^2 * Real.log ((f x)^2)
      ∂Measure.pi (fun _ : Fin n => gaussianReal 0 1)) -
      (∫ x, (f x)^2 ∂Measure.pi (fun _ : Fin n => gaussianReal 0 1)) *
        Real.log (∫ x, (f x)^2 ∂Measure.pi (fun _ : Fin n => gaussianReal 0 1)) ≤
    2 * ∫ x, (∑ i : Fin n, (fderiv ℝ f x (Pi.single i 1))^2)
      ∂Measure.pi (fun _ : Fin n => gaussianReal 0 1) := by
  induction n with
  | zero => exact empty_entropy f
  | succ n ih =>
    let μ : Measure ℝ := gaussianReal 0 1
    let ν : Measure (Fin n → ℝ) := Measure.pi (fun _ : Fin n => gaussianReal 0 1)
    let τ : Measure (Fin (n+1) → ℝ) := Measure.pi (fun _ : Fin (n+1) => gaussianReal 0 1)
    let H : ℝ × (Fin n → ℝ) → ℝ := fun z =>
      (fderiv ℝ f (Fin.cons z.1 z.2) (Pi.single 0 1))^2
    let T : ℝ × (Fin n → ℝ) → ℝ := fun z =>
      ∑ i : Fin n, (fderiv ℝ f (Fin.cons z.1 z.2) (Pi.single i.succ 1))^2
    let U : ℝ → ℝ := fun a =>
      (∫ y, (f (Fin.cons a y))^2 * Real.log ((f (Fin.cons a y))^2) ∂ν) -
        (∫ y, (f (Fin.cons a y))^2 ∂ν) * Real.log (∫ y, (f (Fin.cons a y))^2 ∂ν)
    let V : (Fin n → ℝ) → ℝ := fun y =>
      (∫ a, (f (Fin.cons a y))^2 * Real.log ((f (Fin.cons a y))^2) ∂μ) -
        (∫ a, (f (Fin.cons a y))^2 ∂μ) * Real.log (∫ a, (f (Fin.cons a y))^2 ∂μ)
    rcases compact_domains (n+1) f hf hs with ⟨_, _, iD, _⟩
    have it : Integrable (fun x => ∑ i : Fin n,
        (fderiv ℝ f x (Pi.single i.succ 1))^2) τ :=
      integrable_finsetSum _ (fun i _ => iD i.succ)
    have pH : Integrable H (μ.prod ν) :=
      (split_law n).integrable_comp_of_integrable (iD 0)
    have pT : Integrable T (μ.prod ν) :=
      (split_law n).integrable_comp_of_integrable it
    rcases split_entropy_bound n f hf hs with ⟨iU, iV, hChain⟩
    have iU' : Integrable U μ := iU
    have iV' : Integrable V ν := iV
    have hUbd : ∀ a, U a ≤ 2 * ∫ y, T (a,y) ∂ν := by
      intro a
      let g : (Fin n → ℝ) → ℝ := fun y => f (Fin.cons a y)
      have hg := (original_slices n f hf hs).2 a
      have hi := ih g hg.1 hg.2
      have heq : (fun y : Fin n → ℝ => ∑ i : Fin n,
          (fderiv ℝ g y (Pi.single i 1))^2) = (fun y => T (a,y)) := by
        funext y
        apply Finset.sum_congr rfl
        intro i _
        rw [(coordinate_derivatives n f hf hs a y).2 i]
      rw [heq] at hi
      exact hi
    have hVbd : ∀ y, V y ≤ 2 * ∫ a, H (a,y) ∂μ := by
      intro y
      have hg := (original_slices n f hf hs).1 y
      have hi := GaussianCompactLogSobolev.compact_gaussian_logSobolev
        (fun a : ℝ => f (Fin.cons a y)) hg.1 hg.2
      have heq : (fun a : ℝ => (deriv (fun t : ℝ => f (Fin.cons t y)) a)^2) =
          (fun a => H (a,y)) := by
        funext a
        rw [(coordinate_derivatives n f hf hs a y).1]
      rw [heq] at hi
      exact hi
    have hUi := integral_mono iU' (pT.integral_prod_left.const_mul 2) hUbd
    have hVi := integral_mono iV' (pH.integral_prod_right.const_mul 2) hVbd
    rw [integral_const_mul, ← integral_prod _ pT] at hUi
    rw [integral_const_mul, ← integral_prod_symm _ pH] at hVi
    have emb : MeasurableEmbedding (fun z : ℝ × (Fin n → ℝ) =>
        (Fin.cons z.1 z.2 : Fin (n+1) → ℝ)) :=
      (Fin.consEquivL ℝ (fun _ : Fin (n+1) => ℝ)).toHomeomorph.measurableEmbedding
    have hM : (∫ z : ℝ × (Fin n → ℝ), (f (Fin.cons z.1 z.2))^2 ∂μ.prod ν) =
        (∫ x, (f x)^2 ∂τ) :=
      (split_law n).integral_comp emb (fun x => (f x)^2)
    have hJ : (∫ z : ℝ × (Fin n → ℝ),
        (f (Fin.cons z.1 z.2))^2 * Real.log ((f (Fin.cons z.1 z.2))^2) ∂μ.prod ν) =
        (∫ x, (f x)^2 * Real.log ((f x)^2) ∂τ) :=
      (split_law n).integral_comp emb (fun x => (f x)^2 * Real.log ((f x)^2))
    change (∫ z : ℝ × (Fin n → ℝ),
      (f (Fin.cons z.1 z.2))^2 * Real.log ((f (Fin.cons z.1 z.2))^2) ∂μ.prod ν) -
      (∫ z : ℝ × (Fin n → ℝ), (f (Fin.cons z.1 z.2))^2 ∂μ.prod ν) *
        Real.log (∫ z : ℝ × (Fin n → ℝ), (f (Fin.cons z.1 z.2))^2 ∂μ.prod ν) ≤
      (∫ a, U a ∂μ) + (∫ y, V y ∂ν) at hChain
    rw [hJ, hM] at hChain
    have hH : (∫ z, H z ∂μ.prod ν) =
        (∫ x, (fderiv ℝ f x (Pi.single 0 1))^2 ∂τ) :=
      (split_law n).integral_comp emb (fun x => (fderiv ℝ f x (Pi.single 0 1))^2)
    have hT : (∫ z, T z ∂μ.prod ν) =
        (∫ x, (∑ i : Fin n, (fderiv ℝ f x (Pi.single i.succ 1))^2) ∂τ) :=
      (split_law n).integral_comp emb
        (fun x => ∑ i : Fin n, (fderiv ℝ f x (Pi.single i.succ 1))^2)
    have hE : (∫ x, (∑ i : Fin (n+1), (fderiv ℝ f x (Pi.single i 1))^2) ∂τ) =
        (∫ z, H z ∂μ.prod ν) + (∫ z, T z ∂μ.prod ν) := by
      rw [hH, hT, ← integral_add (iD 0) it]
      apply integral_congr_ae
      exact Filter.Eventually.of_forall fun x => Fin.sum_univ_succ _
    change (∫ x, (f x)^2 * Real.log ((f x)^2) ∂τ) -
      (∫ x, (f x)^2 ∂τ) * Real.log (∫ x, (f x)^2 ∂τ) ≤
      2 * ∫ x, (∑ i : Fin (n+1), (fderiv ℝ f x (Pi.single i 1))^2) ∂τ
    rw [hE]
    linarith

/-- Actual compact finite-product Gaussian LSI, including signed observers,
zero mass and dimension0. Domains, slices and coordinate energy are internal. -/
theorem compact_gaussian_pi_logSobolev
    (n : ℕ) (f : (Fin n → ℝ) → ℝ)
    (hf : ContDiff ℝ 2 f) (hs : HasCompactSupport f) :
    let γ : Measure (Fin n → ℝ) := Measure.pi (fun _ : Fin n => gaussianReal 0 1)
    let D : Fin n → (Fin n → ℝ) → ℝ := fun i x => fderiv ℝ f x (Pi.single i 1)
    Integrable (fun x => (f x)^2) γ ∧
    Integrable (fun x => (f x)^2 * Real.log ((f x)^2)) γ ∧
    (∀ i, Integrable (fun x => (D i x)^2) γ) ∧
    Integrable (fun x => ∑ i, (D i x)^2) γ ∧
    (∫ x, (f x)^2 * Real.log ((f x)^2) ∂γ) -
      (∫ x, (f x)^2 ∂γ) * Real.log (∫ x, (f x)^2 ∂γ) ≤
    2 * ∫ x, ∑ i, (D i x)^2 ∂γ := by
  dsimp only
  rcases compact_domains n f hf hs with ⟨iA, iB, iD, iE⟩
  exact ⟨iA, iB, iD, iE, finite_lsi n f hf hs⟩

end AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.GaussianCompactProductLogSobolev
