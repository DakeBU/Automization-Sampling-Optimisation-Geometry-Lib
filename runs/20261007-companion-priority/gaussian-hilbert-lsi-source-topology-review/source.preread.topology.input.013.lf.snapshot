import AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.LangevinCarreDuChamp
import Mathlib.Analysis.Calculus.LineDeriv.IntegrationByParts
import Mathlib.Analysis.Calculus.FDeriv.Symmetric

/-!
# Compact-test weighted Bochner identity

Background: Kolesnikov--Milman, arXiv:1310.2526v7, Theorem 1.1 (1.3),
Euclidean compact-test localized version, proved directly. In positive
dimension an enclosing ball gives zero boundary terms; dimension zero is an
additional trivial extension. The PBPS consumer is Appendix C.1 of
arXiv:2609.06905v1, via ConditionalBochner.

Only C2 regularity of the potential is used. Haar-volume integration by parts
handles one compactly supported factor; no semigroup, spectral gap or
Poincare inequality is assumed. The sum of squared gradients of genuine
directional derivatives is the coordinate expression for the squared
Hilbert--Schmidt Hessian norm; no separate abstract norm identification is
asserted.
The weight need not be globally integrable for this compact-test identity;
normalization and probability are separate obligations of its consumer.
-/

namespace AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.WeightedBochner

open MeasureTheory InnerProductSpace
open scoped RealInnerProductSpace ContDiff

variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
  [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]

/-- Actual weighted Bochner identity, all compact-test integrability facts, and
its curvature-energy consequence. This does not establish Poincare. -/
theorem integrated_bochner_identity (W f : E → ℝ) (hW : ContDiff ℝ 2 W)
    (hf : ContDiff ℝ ∞ f) (hc : HasCompactSupport f) :
    let L := fun x => Laplacian.laplacian f x - inner ℝ (gradient W x) (gradient f x)
    let H := fun x => ∑ i, ‖gradient (fun z => fderiv ℝ f z ((stdOrthonormalBasis ℝ E) i)) x‖^2
    let C := fun x => fderiv ℝ (fderiv ℝ W) x (gradient f x) (gradient f x)
    Integrable (fun x => Real.exp (-W x) * (L x)^2) ∧
    Integrable (fun x => Real.exp (-W x) * ‖gradient f x‖^2) ∧
    Integrable (fun x => Real.exp (-W x) * H x) ∧
    Integrable (fun x => Real.exp (-W x) * C x) ∧
    (∫ x, Real.exp (-W x) * (L x)^2) =
      (∫ x, Real.exp (-W x) * H x) + ∫ x, Real.exp (-W x) * C x ∧
    ∀ m : ℝ, (∀ x v, m * ‖v‖^2 ≤ fderiv ℝ (fderiv ℝ W) x v v) →
      m * (∫ x, Real.exp (-W x) * ‖gradient f x‖^2) ≤ ∫ x, Real.exp (-W x) * (L x)^2 := by
  have weighted_directional_ibp (W g h : E → ℝ) (hW : ContDiff ℝ 1 W) (hg : ContDiff ℝ 1 g)
      (hh : ContDiff ℝ 2 h) (hc : HasCompactSupport h) (v : E) :
      (∫ x, (Real.exp (-W x) * g x) *
        fderiv ℝ (fun z => fderiv ℝ h z v) x v) =
      - ∫ x, Real.exp (-W x) *
        (fderiv ℝ g x v - g x * fderiv ℝ W x v) * fderiv ℝ h x v := by
    let F := fun x => Real.exp (-W x) * g x
    let H := fun x => fderiv ℝ h x v
    have hF : ContDiff ℝ 1 F := hW.neg.exp.mul hg
    have hH : ContDiff ℝ 1 H :=
      (hh.fderiv_right (m := 1) (by norm_num)).clm_apply contDiff_const
    have hHc : HasCompactSupport H := by
      refine HasCompactSupport.of_support_subset_isCompact hc.isCompact ?_
      intro x hx
      by_contra hnot
      exact hx (by simp [H, fderiv_of_notMem_tsupport ℝ hnot])
    have hDHc : HasCompactSupport (fun x => fderiv ℝ H x v) := by
      refine HasCompactSupport.of_support_subset_isCompact hHc.isCompact ?_
      intro x hx
      by_contra hnot
      exact hx (by simp [fderiv_of_notMem_tsupport ℝ hnot])
    have hDF : Continuous (fun x => fderiv ℝ F x v) :=
      (hF.fderiv_right (m := 0) (by norm_num)).continuous.clm_apply continuous_const
    have hDH : Continuous (fun x => fderiv ℝ H x v) :=
      (hH.fderiv_right (m := 0) (by norm_num)).continuous.clm_apply continuous_const
    have h1 : Integrable (fun x => fderiv ℝ F x v * H x) :=
      (hDF.mul hH.continuous).integrable_of_hasCompactSupport hHc.mul_left
    have h2 : Integrable (fun x => F x * fderiv ℝ H x v) :=
      (hF.continuous.mul hDH).integrable_of_hasCompactSupport hDHc.mul_left
    have h3 : Integrable (fun x => F x * H x) :=
      (hF.continuous.mul hH.continuous).integrable_of_hasCompactSupport hHc.mul_left
    have hibp := integral_mul_fderiv_eq_neg_fderiv_mul_of_integrable h1 h2 h3
      (fun x _ => hF.differentiable one_ne_zero x)
      (fun x _ => hH.differentiable one_ne_zero x)
    change (∫ x, F x * fderiv ℝ H x v) = _
    rw [hibp]
    congr 1
    apply integral_congr_ae
    filter_upwards [] with x
    have hw := (hW.differentiable one_ne_zero x).hasFDerivAt.neg.exp
    have hder := hw.mul (hg.differentiable one_ne_zero x).hasFDerivAt
    have hd : fderiv ℝ F x v = Real.exp (-W x) *
        (fderiv ℝ g x v - g x * fderiv ℝ W x v) := by
      rw [show fderiv ℝ F x = _ from hder.fderiv]
      simp only [add_apply, smul_apply,
        neg_apply, smul_eq_mul, Pi.neg_apply]
      ring
    rw [hd]

  have directional_second (h : E → ℝ) (hh : ContDiff ℝ 2 h) (x v w : E) :
      fderiv ℝ (fun z => fderiv ℝ h z w) x v =
        fderiv ℝ (fderiv ℝ h) x v w := by
    have hd := ((hh.fderiv_right (m := 1) (by norm_num)).differentiable one_ne_zero x).hasFDerivAt
    have he := hd.clm_apply (hasFDerivAt_const w x)
    simpa using congrArg (fun T : E →L[ℝ] ℝ => T v) he.fderiv

  have inner_gradient_eq_sum (f g : E → ℝ)
      (hf : Differentiable ℝ f) (hg : Differentiable ℝ g) (x : E) :
      inner ℝ (gradient f x) (gradient g x) =
        ∑ i, fderiv ℝ f x ((stdOrthonormalBasis ℝ E) i) *
          fderiv ℝ g x ((stdOrthonormalBasis ℝ E) i) := by
    simp_rw [AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Gradient.fderiv_apply_eq_inner_gradient_of_differentiableAt (hf x),
      AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Gradient.fderiv_apply_eq_inner_gradient_of_differentiableAt (hg x)]
    rw [← (stdOrthonormalBasis ℝ E).sum_inner_mul_inner (gradient f x) (gradient g x)]
    apply Finset.sum_congr rfl
    intro i _
    rw [real_inner_comm ((stdOrthonormalBasis ℝ E) i) (gradient g x)]

  have weighted_bilinear_ibp (W g h : E → ℝ) (hW : ContDiff ℝ 1 W)
      (hg : ContDiff ℝ 1 g) (hh : ContDiff ℝ 2 h) (hc : HasCompactSupport h) :
      (∫ x, Real.exp (-W x) * g x *
        (Laplacian.laplacian h x - inner ℝ (gradient W x) (gradient h x))) =
      - ∫ x, Real.exp (-W x) * inner ℝ (gradient g x) (gradient h x) := by
    let b := stdOrthonormalBasis ℝ E
    let A := fun i x => (Real.exp (-W x) * g x) *
      fderiv ℝ (fun z => fderiv ℝ h z (b i)) x (b i)
    let B := fun i x => Real.exp (-W x) *
      (fderiv ℝ g x (b i) - g x * fderiv ℝ W x (b i)) * fderiv ℝ h x (b i)
    have hA (i) : Integrable (A i) := by
      have hD : ContDiff ℝ 1 (fun z => fderiv ℝ h z (b i)) :=
        (hh.fderiv_right (m := 1) (by norm_num)).clm_apply contDiff_const
      have hC : Continuous (fun x => fderiv ℝ (fun z => fderiv ℝ h z (b i)) x (b i)) :=
        (hD.fderiv_right (m := 0) (by norm_num)).continuous.clm_apply continuous_const
      apply (((hW.neg.exp).continuous.mul hg.continuous).mul hC).integrable_of_hasCompactSupport
      refine HasCompactSupport.of_support_subset_isCompact hc.isCompact ?_
      intro x hx
      by_contra hn
      have hcD : tsupport (fun z => fderiv ℝ h z (b i)) ⊆ tsupport h := by
        apply closure_minimal _ isClosed_closure
        intro z hz
        by_contra hnz
        exact hz (by simp [fderiv_of_notMem_tsupport ℝ hnz])
      have hnD : x ∉ tsupport (fun z => fderiv ℝ h z (b i)) := fun hx => hn (hcD hx)
      exact hx (by simp [fderiv_of_notMem_tsupport ℝ hnD])
    have hB (i) : Integrable (B i) := by
      have hD (f : E → ℝ) (hf : ContDiff ℝ 1 f) : Continuous (fun x => fderiv ℝ f x (b i)) :=
        (hf.fderiv_right (m := 0) (by norm_num)).continuous.clm_apply continuous_const
      have hDh : Continuous (fun x => fderiv ℝ h x (b i)) := hD h (hh.of_le (by norm_num))
      apply ((hW.neg.exp).continuous.mul ((hD g hg).sub (hg.continuous.mul (hD W hW))) |>.mul hDh).integrable_of_hasCompactSupport
      refine HasCompactSupport.of_support_subset_isCompact hc.isCompact ?_
      intro x hx
      by_contra hn
      exact hx (by simp [fderiv_of_notMem_tsupport ℝ hn])
    have heq : (∫ x, ∑ i, A i x) = - ∫ x, ∑ i, B i x := by
      rw [integral_finsetSum _ (fun i _ => hA i), integral_finsetSum _ (fun i _ => hB i)]
      simp_rw [show ∀ i, (∫ x, A i x) = -∫ x, B i x from fun i => weighted_directional_ibp W g h hW hg hh hc (b i)]
      exact Finset.sum_neg_distrib _
    have hLap (x : E) : Laplacian.laplacian h x =
        ∑ i, fderiv ℝ (fun z => fderiv ℝ h z (b i)) x (b i) := by
      rw [InnerProductSpace.laplacian_eq_iteratedFDeriv_stdOrthonormalBasis]
      apply Finset.sum_congr rfl
      intro i _
      rw [directional_second h hh, iteratedFDeriv_two_apply]
      rfl
    have hpoint (x : E) : (∑ i, A i x) + (∑ i, B i x) =
        Real.exp (-W x) * g x *
          (Laplacian.laplacian h x - inner ℝ (gradient W x) (gradient h x)) +
        Real.exp (-W x) * inner ℝ (gradient g x) (gradient h x) := by
      rw [hLap, inner_gradient_eq_sum W h (hW.differentiable one_ne_zero) (hh.differentiable (by norm_num)),
        inner_gradient_eq_sum g h (hg.differentiable one_ne_zero) (hh.differentiable (by norm_num))]
      simp only [A, B, mul_sub, sub_mul, mul_assoc, Finset.sum_sub_distrib, ← Finset.mul_sum, b]
      ring
    -- The finite sums establish compact integrability before splitting integrals.
    have hS1 : Integrable (fun x => ∑ i, A i x) := integrable_finsetSum _ (fun i _ => hA i)
    have hS2 : Integrable (fun x => ∑ i, B i x) := integrable_finsetSum _ (fun i _ => hB i)
    let G := fun x => Real.exp (-W x) * inner ℝ (gradient g x) (gradient h x)
    have hG : Integrable G := by
      have hgD : Continuous (fun x => fderiv ℝ g x) :=
        (hg.fderiv_right (m := 0) (by norm_num)).continuous
      have hhD : Continuous (fun x => fderiv ℝ h x) :=
        (hh.fderiv_right (m := 1) (by norm_num)).continuous
      have hrep : G = fun x => Real.exp (-W x) * ∑ i, fderiv ℝ g x (b i) * fderiv ℝ h x (b i) := by
        funext x
        exact congrArg (fun t => Real.exp (-W x) * t)
          (inner_gradient_eq_sum g h (hg.differentiable one_ne_zero) (hh.differentiable (by norm_num)) x)
      rw [hrep]
      apply ((hW.neg.exp).continuous.mul (continuous_finsetSum _ fun i _ =>
        (hgD.clm_apply continuous_const).mul (hhD.clm_apply continuous_const))).integrable_of_hasCompactSupport
      refine HasCompactSupport.of_support_subset_isCompact hc.isCompact ?_
      intro x hx
      by_contra hn
      exact hx (by simp [fderiv_of_notMem_tsupport ℝ hn])
    let L := fun x => Real.exp (-W x) * g x *
        (Laplacian.laplacian h x - inner ℝ (gradient W x) (gradient h x))
    have hLG : (fun x => (∑ i, A i x) + (∑ i, B i x)) = fun x => L x + G x := funext hpoint
    have hL : Integrable L := by
      have hp := hS1.add hS2
      change Integrable (fun x => (∑ i, A i x) + (∑ i, B i x)) at hp
      rw [hLG] at hp
      convert hp.sub hG using 1
      ext x
      simp only [Pi.sub_apply, add_sub_cancel_right]
    have hz : (∫ x, L x) + (∫ x, G x) = 0 := by
      rw [← integral_add hL hG, ← hLG, integral_add hS1 hS2, heq]
      ring
    exact eq_neg_of_add_eq_zero_left hz

  let dir (f : E → ℝ) (v : E) : E → ℝ := fun x => fderiv ℝ f x v

  have dir_contDiff {n : ℕ∞ω} (f : E → ℝ) (hf : ContDiff ℝ (n+1) f) (v : E) :
      ContDiff ℝ n (dir f v) := (hf.fderiv_right le_rfl).clm_apply contDiff_const

  have dir_compact (f : E → ℝ) (hc : HasCompactSupport f) (v : E) :
      HasCompactSupport (dir f v) := by
    refine HasCompactSupport.of_support_subset_isCompact hc.isCompact ?_
    intro x hx
    by_contra hn
    exact hx (by simp [dir, fderiv_of_notMem_tsupport ℝ hn])

  have dir_comm (f : E → ℝ) (hf : ContDiff ℝ 2 f) (v w : E) :
      dir (dir f v) w = dir (dir f w) v := by
    funext x
    change fderiv ℝ (fun z => fderiv ℝ f z v) x w =
      fderiv ℝ (fun z => fderiv ℝ f z w) x v
    rw [directional_second f hf, directional_second f hf]
    exact (hf.contDiffAt.isSymmSndFDerivAt (by norm_num)).eq w v

  have laplacian_dirs (f : E → ℝ) (hf : ContDiff ℝ 2 f) :
      Laplacian.laplacian f = fun x => ∑ i,
        dir (dir f ((stdOrthonormalBasis ℝ E) i)) ((stdOrthonormalBasis ℝ E) i) x := by
    funext x
    rw [InnerProductSpace.laplacian_eq_iteratedFDeriv_stdOrthonormalBasis]
    apply Finset.sum_congr rfl
    intro i _
    change iteratedFDeriv ℝ 2 f x ![(stdOrthonormalBasis ℝ E) i, (stdOrthonormalBasis ℝ E) i] =
      fderiv ℝ (fun z => fderiv ℝ f z ((stdOrthonormalBasis ℝ E) i)) x ((stdOrthonormalBasis ℝ E) i)
    rw [directional_second f hf, iteratedFDeriv_two_apply]
    rfl

  have dir_sum {ι : Type} [Fintype ι] (f : ι → E → ℝ)
      (hf : ∀ i, Differentiable ℝ (f i)) (v : E) :
      dir (fun x => ∑ i, f i x) v = fun x => ∑ i, dir (f i) v x := by
    funext x
    dsimp [dir]
    rw [fderiv_fun_sum (fun i _ => hf i x)]
    simp

  have smooth_finite (f : E → ℝ) (hf : ContDiff ℝ ∞ f) (n : ℕ) :
      ContDiff ℝ n f := contDiff_infty.mp hf n

  have dir_mul (f g : E → ℝ) (hf : Differentiable ℝ f) (hg : Differentiable ℝ g)
      (v : E) : dir (fun x => f x * g x) v =
        fun x => dir f v x * g x + f x * dir g v x := by
    funext x
    dsimp [dir]
    change fderiv ℝ (f * g) x v = _
    rw [fderiv_mul (hf x) (hg x)]
    simp only [add_apply, smul_apply, smul_eq_mul]
    ring

  let op (W f : E → ℝ) : E → ℝ :=
    fun x => Laplacian.laplacian f x - inner ℝ (gradient W x) (gradient f x)

  have op_coords (W f : E → ℝ) (hW : ContDiff ℝ 1 W) (hf : ContDiff ℝ 2 f) :
      op W f = fun x => ∑ i,
        (dir (dir f ((stdOrthonormalBasis ℝ E) i)) ((stdOrthonormalBasis ℝ E) i) x -
          dir W ((stdOrthonormalBasis ℝ E) i) x * dir f ((stdOrthonormalBasis ℝ E) i) x) := by
    funext x
    dsimp [op]
    rw [laplacian_dirs f hf, inner_gradient_eq_sum W f (hW.differentiable one_ne_zero)
      (hf.differentiable (by norm_num))]
    exact (Finset.sum_sub_distrib _ _).symm

  have op_contDiff (W f : E → ℝ) (hW : ContDiff ℝ 2 W) (hf : ContDiff ℝ ∞ f) :
      ContDiff ℝ 1 (op W f) := by
    rw [op_coords W f (hW.of_le (by norm_num)) (smooth_finite f hf 2)]
    apply ContDiff.sum
    intro i _
    have hfd : ContDiff ℝ ∞ (dir f ((stdOrthonormalBasis ℝ E) i)) :=
      dir_contDiff f (by simpa using hf) _
    have hfdd : ContDiff ℝ ∞ (dir (dir f ((stdOrthonormalBasis ℝ E) i)) ((stdOrthonormalBasis ℝ E) i)) :=
      dir_contDiff _ (by simpa using hfd) _
    exact (smooth_finite _ hfdd 1).sub
      ((dir_contDiff W hW _).mul (smooth_finite _ hfd 1))

  have op_compact (W f : E → ℝ) (hW : ContDiff ℝ 1 W)
      (hf : ContDiff ℝ 2 f) (hc : HasCompactSupport f) : HasCompactSupport (op W f) := by
    rw [op_coords W f hW hf]
    refine HasCompactSupport.of_support_subset_isCompact hc.isCompact ?_
    intro x hx
    by_contra hn
    apply hx
    apply Finset.sum_eq_zero
    intro i _
    have hsub : tsupport (dir f ((stdOrthonormalBasis ℝ E) i)) ⊆ tsupport f := by
      apply closure_minimal _ isClosed_closure
      intro z hz
      by_contra hnz
      exact hz (by simp [dir, fderiv_of_notMem_tsupport ℝ hnz])
    have hnd : x ∉ tsupport (dir f ((stdOrthonormalBasis ℝ E) i)) := fun hx => hn (hsub hx)
    change (fderiv ℝ (dir f ((stdOrthonormalBasis ℝ E) i)) x) ((stdOrthonormalBasis ℝ E) i) -
      dir W ((stdOrthonormalBasis ℝ E) i) x * (fderiv ℝ f x) ((stdOrthonormalBasis ℝ E) i) = 0
    simp [fderiv_of_notMem_tsupport ℝ hn, fderiv_of_notMem_tsupport ℝ hnd]

  have dir_op (W f : E → ℝ) (hW : ContDiff ℝ 2 W) (hf : ContDiff ℝ ∞ f) (v : E) :
      dir (op W f) v = fun x => op W (dir f v) x -
        ∑ i, dir (dir W ((stdOrthonormalBasis ℝ E) i)) v x *
          dir f ((stdOrthonormalBasis ℝ E) i) x := by
    let b := stdOrthonormalBasis ℝ E
    have hfd (w : E) : ContDiff ℝ ∞ (dir f w) := dir_contDiff f (by simpa using hf) w
    have hfdd (w z : E) : ContDiff ℝ ∞ (dir (dir f w) z) :=
      dir_contDiff _ (by simpa using hfd w) z
    have hWd (w : E) : ContDiff ℝ 1 (dir W w) := dir_contDiff W hW w
    rw [op_coords W f (hW.of_le (by norm_num)) (smooth_finite f hf 2)]
    rw [dir_sum (fun i x => dir (dir f (b i)) (b i) x - dir W (b i) x * dir f (b i) x)
      (fun i => ((hfdd _ _).differentiable (by simp)).sub
      ((hWd _).differentiable one_ne_zero |>.mul ((hfd _).differentiable (by simp))))]
    funext x
    rw [op_coords W (dir f v) (hW.of_le (by norm_num)) (smooth_finite _ (hfd v) 2)]
    rw [← Finset.sum_sub_distrib]
    apply Finset.sum_congr rfl
    intro i _
    have hdsub : dir (fun x => dir (dir f (b i)) (b i) x - dir W (b i) x * dir f (b i) x) v x =
        dir (dir (dir f (b i)) (b i)) v x -
          dir (fun x => dir W (b i) x * dir f (b i) x) v x := by
      change fderiv ℝ (dir (dir f (b i)) (b i) - dir W (b i) * dir f (b i)) x v =
        fderiv ℝ (dir (dir f (b i)) (b i)) x v -
          fderiv ℝ (dir W (b i) * dir f (b i)) x v
      rw [fderiv_sub ((hfdd _ _).differentiable (by simp) x)
        (((hWd _).differentiable one_ne_zero).mul ((hfd _).differentiable (by simp)) x)]
      rfl
    rw [hdsub, dir_mul _ _ ((hWd _).differentiable one_ne_zero) ((hfd _).differentiable (by simp))]
    rw [dir_comm (dir f (b i)) (smooth_finite _ (hfd _) 2) (b i) v,
      dir_comm f (smooth_finite f hf 2) (b i) v]
    dsimp only [b]
    ring

  have weighted_mul_integrable (W f g : E → ℝ) (hW : Continuous W)
      (hf : Continuous f) (hg : Continuous g) (hc : HasCompactSupport g) :
      Integrable (fun x => Real.exp (-W x) * f x * g x) :=
    ((Real.continuous_exp.comp hW.neg).mul hf |>.mul hg).integrable_of_hasCompactSupport hc.mul_left

  have weighted_inner_integrable (W f g : E → ℝ) (hW : Continuous W)
      (hf : ContDiff ℝ 1 f) (hg : ContDiff ℝ 1 g) (hc : HasCompactSupport g) :
      Integrable (fun x => Real.exp (-W x) * inner ℝ (gradient f x) (gradient g x)) := by
    have hd (k : E → ℝ) (hk : ContDiff ℝ 1 k) (v : E) : Continuous (dir k v) :=
      (dir_contDiff (n := 0) k hk v).continuous
    have he : (fun x => Real.exp (-W x) * inner ℝ (gradient f x) (gradient g x)) =
        fun x => ∑ i, Real.exp (-W x) * dir f ((stdOrthonormalBasis ℝ E) i) x *
          dir g ((stdOrthonormalBasis ℝ E) i) x := by
      funext x
      rw [inner_gradient_eq_sum f g (hf.differentiable one_ne_zero) (hg.differentiable one_ne_zero)]
      simp only [Finset.mul_sum, dir, mul_assoc]
    rw [he]
    exact integrable_finsetSum _ (fun i _ => weighted_mul_integrable W _ _ hW
      (hd f hf _) (hd g hg _) (dir_compact g hc _))

  have bochner_coordinate_integrals (W f : E → ℝ) (hW : ContDiff ℝ 2 W)
      (hf : ContDiff ℝ ∞ f) (hc : HasCompactSupport f) :
      (∫ x, Real.exp (-W x) * (op W f x)^2) =
        (∑ i, ∫ x, Real.exp (-W x) *
          ‖gradient (dir f ((stdOrthonormalBasis ℝ E) i)) x‖^2) +
        ∑ i, ∫ x, Real.exp (-W x) *
          (∑ j, dir (dir W ((stdOrthonormalBasis ℝ E) j)) ((stdOrthonormalBasis ℝ E) i) x *
            dir f ((stdOrthonormalBasis ℝ E) j) x) * dir f ((stdOrthonormalBasis ℝ E) i) x := by
    let b := stdOrthonormalBasis ℝ E
    have hfd (v : E) : ContDiff ℝ ∞ (dir f v) := dir_contDiff f (by simpa using hf) v
    have hop := op_contDiff W f hW hf
    have hW1 : ContDiff ℝ 1 W := hW.of_le (by norm_num)
    have hf1 : ContDiff ℝ 1 f := smooth_finite f hf 1
    have hfd1 (v : E) : ContDiff ℝ 1 (dir f v) := smooth_finite _ (hfd v) 1
    have hWdd (v w : E) : Continuous (dir (dir W w) v) :=
      (dir_contDiff (n := 0) _ (dir_contDiff (n := 1) W hW w) v).continuous
    let T := fun i x => Real.exp (-W x) * dir (op W f) (b i) x * dir f (b i) x
    let A := fun i x => Real.exp (-W x) * dir f (b i) x * op W (dir f (b i)) x
    let K := fun i x => Real.exp (-W x) *
      (∑ j, dir (dir W (b j)) (b i) x * dir f (b j) x) * dir f (b i) x
    have hTi (i) : Integrable (T i) := weighted_mul_integrable W _ _ hW.continuous
      (dir_contDiff (n := 0) _ hop _).continuous (hfd1 _).continuous (dir_compact f hc _)
    have hAi (i) : Integrable (A i) := weighted_mul_integrable W _ _ hW.continuous
      (hfd1 _).continuous (op_contDiff W _ hW (hfd _)).continuous
      (op_compact W _ hW1 (smooth_finite _ (hfd _) 2) (dir_compact f hc _))
    have hKi (i) : Integrable (K i) := weighted_mul_integrable W _ _ hW.continuous
      (continuous_finsetSum _ fun j _ => (hWdd _ _).mul (hfd1 _).continuous)
      (hfd1 _).continuous (dir_compact f hc _)
    have hpoint (i) : T i = fun x => A i x - K i x := by
      funext x
      dsimp only [T]
      rw [dir_op W f hW hf (b i)]
      dsimp only [A, K, b]
      ring
    have hfirst : (∫ x, Real.exp (-W x) * (op W f x)^2) = -∑ i, ∫ x, T i x := by
      have hibp := weighted_bilinear_ibp W (op W f) f hW1 hop (smooth_finite f hf 2) hc
      have hlhs : (fun x => Real.exp (-W x) * op W f x *
          (Laplacian.laplacian f x - inner ℝ (gradient W x) (gradient f x))) =
          fun x => Real.exp (-W x) * (op W f x)^2 := by
        funext x
        change Real.exp (-W x) * op W f x * op W f x = _
        ring
      rw [hlhs] at hibp
      rw [hibp]
      congr 1
      rw [← integral_finsetSum _ (fun i _ => hTi i)]
      apply integral_congr_ae
      filter_upwards [] with x
      rw [inner_gradient_eq_sum (op W f) f (hop.differentiable one_ne_zero) (hf1.differentiable one_ne_zero)]
      simp only [T, dir, b, Finset.mul_sum, mul_assoc]
    have hsecond (i) : (∫ x, A i x) = -∫ x, Real.exp (-W x) * ‖gradient (dir f (b i)) x‖^2 := by
      have hibp := weighted_bilinear_ibp W (dir f (b i)) (dir f (b i)) hW1
        (hfd1 _) (smooth_finite _ (hfd _) 2) (dir_compact f hc _)
      simpa only [A, op, real_inner_self_eq_norm_sq] using hibp
    rw [hfirst]
    have heach (i) : (∫ x, T i x) =
        -(∫ x, Real.exp (-W x) * ‖gradient (dir f (b i)) x‖^2) - ∫ x, K i x := by
      rw [hpoint, integral_sub (hAi i) (hKi i), hsecond]
    simp_rw [heach]
    rw [Finset.sum_sub_distrib, Finset.sum_neg_distrib]
    dsimp only [K, b]
    ring

  have gradient_basis (f : E → ℝ) (hf : Differentiable ℝ f) (x : E) :
      gradient f x = ∑ i, dir f ((stdOrthonormalBasis ℝ E) i) x • ((stdOrthonormalBasis ℝ E) i) := by
    rw [← (stdOrthonormalBasis ℝ E).sum_repr' (gradient f x)]
    apply Finset.sum_congr rfl
    intro i _
    congr 1
    rw [real_inner_comm]
    exact (AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Gradient.fderiv_apply_eq_inner_gradient_of_differentiableAt (hf x)).symm

  have curvature_sum (W f : E → ℝ) (hW : ContDiff ℝ 2 W)
      (hf : Differentiable ℝ f) (x : E) :
      (∑ i, (∑ j, dir (dir W ((stdOrthonormalBasis ℝ E) j)) ((stdOrthonormalBasis ℝ E) i) x *
        dir f ((stdOrthonormalBasis ℝ E) j) x) * dir f ((stdOrthonormalBasis ℝ E) i) x) =
      fderiv ℝ (fderiv ℝ W) x (gradient f x) (gradient f x) := by
    have hdir (v w : E) : dir (dir W w) v x = fderiv ℝ (fderiv ℝ W) x v w :=
      directional_second W hW x v w
    simp_rw [hdir]
    rw [gradient_basis f hf x]
    simp only [map_sum, map_smul, sum_apply, smul_apply, smul_eq_mul]
    apply Finset.sum_congr rfl
    intro i _
    rw [Finset.sum_mul, Finset.mul_sum]
    apply Finset.sum_congr rfl
    intro j _
    rw [(hW.contDiffAt.isSymmSndFDerivAt (by norm_num)).eq ((stdOrthonormalBasis ℝ E) i) ((stdOrthonormalBasis ℝ E) j)]
    ring

  have curvature_component_integrable (W f : E → ℝ) (hW : ContDiff ℝ 2 W)
      (hf : ContDiff ℝ 1 f) (hc : HasCompactSupport f) (i : Fin (Module.finrank ℝ E)) :
      Integrable (fun x => Real.exp (-W x) *
        (∑ j, dir (dir W ((stdOrthonormalBasis ℝ E) j)) ((stdOrthonormalBasis ℝ E) i) x *
          dir f ((stdOrthonormalBasis ℝ E) j) x) * dir f ((stdOrthonormalBasis ℝ E) i) x) := by
    apply weighted_mul_integrable W _ _ hW.continuous
    · apply continuous_finsetSum
      intro j _
      exact ((dir_contDiff (n := 0) _ (dir_contDiff (n := 1) W hW _) _).continuous).mul
        (dir_contDiff (n := 0) f hf _).continuous
    · exact (dir_contDiff (n := 0) f hf _).continuous
    · exact dir_compact f hc _

  have curvature_integrable_and_sum (W f : E → ℝ) (hW : ContDiff ℝ 2 W)
      (hf : ContDiff ℝ 1 f) (hc : HasCompactSupport f) :
      Integrable (fun x => Real.exp (-W x) *
        fderiv ℝ (fderiv ℝ W) x (gradient f x) (gradient f x)) ∧
      (∫ x, Real.exp (-W x) * fderiv ℝ (fderiv ℝ W) x (gradient f x) (gradient f x)) =
        ∑ i, ∫ x, Real.exp (-W x) *
          (∑ j, dir (dir W ((stdOrthonormalBasis ℝ E) j)) ((stdOrthonormalBasis ℝ E) i) x *
            dir f ((stdOrthonormalBasis ℝ E) j) x) * dir f ((stdOrthonormalBasis ℝ E) i) x := by
    let K := fun i x => Real.exp (-W x) *
      (∑ j, dir (dir W ((stdOrthonormalBasis ℝ E) j)) ((stdOrthonormalBasis ℝ E) i) x *
        dir f ((stdOrthonormalBasis ℝ E) j) x) * dir f ((stdOrthonormalBasis ℝ E) i) x
    have he : (fun x => Real.exp (-W x) * fderiv ℝ (fderiv ℝ W) x (gradient f x) (gradient f x)) =
        fun x => ∑ i, K i x := by
      funext x
      rw [← curvature_sum W f hW (hf.differentiable one_ne_zero)]
      rw [Finset.mul_sum]
      apply Finset.sum_congr rfl
      intro i _
      dsimp only [K]
      ring
    rw [he]
    exact ⟨integrable_finsetSum _ (fun i _ => curvature_component_integrable W f hW hf hc i),
      integral_finsetSum _ (fun i _ => curvature_component_integrable W f hW hf hc i)⟩

  have integrated_identity (W f : E → ℝ) (hW : ContDiff ℝ 2 W)
      (hf : ContDiff ℝ ∞ f) (hc : HasCompactSupport f) :
      (∫ x, Real.exp (-W x) * (op W f x)^2) =
        (∫ x, Real.exp (-W x) * ∑ i, ‖gradient (dir f ((stdOrthonormalBasis ℝ E) i)) x‖^2) +
        ∫ x, Real.exp (-W x) * fderiv ℝ (fderiv ℝ W) x (gradient f x) (gradient f x) := by
    rw [(curvature_integrable_and_sum W f hW (smooth_finite f hf 1) hc).2,
      bochner_coordinate_integrals W f hW hf hc]
    congr 1
    have hfd (v : E) : ContDiff ℝ ∞ (dir f v) := dir_contDiff f (by simpa using hf) v
    have hI (i : Fin (Module.finrank ℝ E)) : Integrable (fun x =>
        Real.exp (-W x) * ‖gradient (dir f ((stdOrthonormalBasis ℝ E) i)) x‖^2) := by
      simpa only [real_inner_self_eq_norm_sq] using weighted_inner_integrable W
        (dir f ((stdOrthonormalBasis ℝ E) i)) (dir f ((stdOrthonormalBasis ℝ E) i)) hW.continuous
        (smooth_finite _ (hfd _) 1) (smooth_finite _ (hfd _) 1) (dir_compact f hc _)
    simp_rw [Finset.mul_sum]
    exact (integral_finsetSum _ (fun i _ => hI i)).symm

  have weighted_energy_lower_bound (W f : E → ℝ) (hW : ContDiff ℝ 2 W)
      (hf : ContDiff ℝ ∞ f) (hc : HasCompactSupport f) (m : ℝ)
      (hm : ∀ x v, m * ‖v‖^2 ≤ fderiv ℝ (fderiv ℝ W) x v v) :
      m * (∫ x, Real.exp (-W x) * ‖gradient f x‖^2) ≤
        ∫ x, Real.exp (-W x) * (op W f x)^2 := by
    have hI : Integrable (fun x => Real.exp (-W x) * ‖gradient f x‖^2) := by
      simpa only [real_inner_self_eq_norm_sq] using weighted_inner_integrable W f f hW.continuous
        (smooth_finite f hf 1) (smooth_finite f hf 1) hc
    have hC := (curvature_integrable_and_sum W f hW (smooth_finite f hf 1) hc).1
    have hbound : m * (∫ x, Real.exp (-W x) * ‖gradient f x‖^2) ≤
        ∫ x, Real.exp (-W x) * fderiv ℝ (fderiv ℝ W) x (gradient f x) (gradient f x) := by
      rw [← integral_const_mul]
      apply integral_mono (hI.const_mul m) hC
      intro x
      calc
        m * (Real.exp (-W x) * ‖gradient f x‖^2) =
          Real.exp (-W x) * (m * ‖gradient f x‖^2) := by ring
        _ ≤ _ := mul_le_mul_of_nonneg_left (hm x (gradient f x)) (Real.exp_nonneg _)
    rw [integrated_identity W f hW hf hc]
    exact hbound.trans (le_add_of_nonneg_left (integral_nonneg (fun x =>
      mul_nonneg (Real.exp_nonneg _) (Finset.sum_nonneg (fun i _ => sq_nonneg _)))))
  have hop := op_contDiff W f hW hf
  have hopc := op_compact W f (hW.of_le (by norm_num)) (smooth_finite f hf 2) hc
  have hL : Integrable (fun x => Real.exp (-W x) * (op W f x)^2) := by
    simpa only [pow_two, mul_assoc] using weighted_mul_integrable W (op W f) (op W f)
      hW.continuous hop.continuous hop.continuous hopc
  have hG : Integrable (fun x => Real.exp (-W x) * ‖gradient f x‖^2) := by
    simpa only [real_inner_self_eq_norm_sq] using weighted_inner_integrable W f f hW.continuous
      (smooth_finite f hf 1) (smooth_finite f hf 1) hc
  have hfd (v : E) : ContDiff ℝ ∞ (dir f v) := dir_contDiff f (by simpa using hf) v
  have hH : Integrable (fun x => Real.exp (-W x) *
      ∑ i, ‖gradient (dir f ((stdOrthonormalBasis ℝ E) i)) x‖^2) := by
    simp_rw [Finset.mul_sum]
    apply integrable_finsetSum
    intro i _
    simpa only [real_inner_self_eq_norm_sq] using weighted_inner_integrable W
      (dir f ((stdOrthonormalBasis ℝ E) i)) (dir f ((stdOrthonormalBasis ℝ E) i)) hW.continuous
      (smooth_finite _ (hfd _) 1) (smooth_finite _ (hfd _) 1) (dir_compact f hc _)
  exact ⟨hL,hG,hH,(curvature_integrable_and_sum W f hW (smooth_finite f hf 1) hc).1,
    integrated_identity W f hW hf hc,fun m hm => weighted_energy_lower_bound W f hW hf hc m hm⟩

end AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.WeightedBochner

