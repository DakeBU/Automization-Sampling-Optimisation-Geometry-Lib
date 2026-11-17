import Mathlib.Analysis.Calculus.ContDiff.Comp
import Mathlib.Analysis.Calculus.Deriv.Pow
import Mathlib.Analysis.Calculus.MeanValue
import Mathlib.Analysis.Normed.Operator.BoundedLinearMaps
import Mathlib.Topology.MetricSpace.Thickening

namespace AutoSamplingTheory.TechnicalLemmas.Analysis.CompactTaylorRemainder

open Set Filter Metric
open scoped Topology

variable {E F : Type*} [NormedAddCommGroup E] [NormedSpace ℝ E]
  [NormedAddCommGroup F] [NormedSpace ℝ F]

/-- The residual after subtracting the first and second Taylor terms. -/
noncomputable def secondOrderRemainder (f : E → F) (x v : E) : F :=
  f (x + v) - f x - fderiv ℝ f x v - (1 / 2 : ℝ) • fderiv ℝ (fderiv ℝ f) x v v

/-- Control the second-order remainder by the Hessian oscillation along
the segment. -/
theorem norm_secondOrderRemainder_le_of_hessian_variation
    {f : E → F} {x v : E} {ε : ℝ}
    (hf : ∀ t ∈ Icc (0 : ℝ) 1, ContDiffAt ℝ 2 f (x + t • v))
    (hvar : ∀ t ∈ Icc (0 : ℝ) 1,
      ‖fderiv ℝ (fderiv ℝ f) (x + t • v) - fderiv ℝ (fderiv ℝ f) x‖ ≤ ε) :
    ‖secondOrderRemainder f x v‖ ≤ ε * ‖v‖ ^ 2 := by
  let line (t : ℝ) := x + t • v
  let H := fderiv ℝ (fderiv ℝ f)
  let a := fderiv ℝ f x v
  let b := H x v v
  let D (t : ℝ) := fderiv ℝ f (line t) v - a - t • b
  let R (t : ℝ) := f (line t) - f x - t • a - (t ^ 2 / 2) • b
  let C := ε * ‖v‖ ^ 2
  have hzero : (0 : ℝ) ∈ Icc 0 1 := left_mem_Icc.2 zero_le_one
  have hε : 0 ≤ ε := (norm_nonneg (H (line 0) - H x)).trans (hvar 0 hzero)
  have hC : 0 ≤ C := mul_nonneg hε (sq_nonneg _)
  have hline (t : ℝ) : HasDerivAt line v t := by
    simpa [line] using ((hasDerivAt_id t).smul_const v).const_add x
  have hD' (t : ℝ) (ht : t ∈ Icc (0 : ℝ) 1) :
      HasDerivAt D ((H (line t) - H x) v v) t := by
    have hh : DifferentiableAt ℝ (fderiv ℝ f) (line t) :=
      ((hf t ht).fderiv_right (m := 1) (by norm_num)).differentiableAt one_ne_zero
    have hd : HasDerivAt (fun r => fderiv ℝ f (line r)) (H (line t) v) t :=
      hh.hasFDerivAt.comp_hasDerivAt t (hline t)
    have hvalue : HasDerivAt (fun r => fderiv ℝ f (line r) v) (H (line t) v v) t :=
      (ContinuousLinearMap.apply ℝ F v).hasFDerivAt.comp_hasDerivAt t hd
    simpa only [D, b, sub_apply, id_eq, one_smul] using
      (hvalue.sub_const a).fun_sub ((hasDerivAt_id t).smul_const b)
  have hH (t : ℝ) (ht : t ∈ Icc (0 : ℝ) 1) : ‖(H (line t) - H x) v v‖ ≤ C := by
    calc
      _ ≤ ‖(H (line t) - H x) v‖ * ‖v‖ := ((H (line t) - H x) v).le_opNorm v
      _ ≤ (‖H (line t) - H x‖ * ‖v‖) * ‖v‖ :=
        mul_le_mul_of_nonneg_right ((H (line t) - H x).le_opNorm v) (norm_nonneg v)
      _ ≤ C := by
        rw [mul_assoc, ← pow_two]
        exact mul_le_mul_of_nonneg_right (hvar t ht) (sq_nonneg _)
  have hD0 : D 0 = 0 := by simp [D, line, a]
  have hD (t : ℝ) (ht : t ∈ Icc (0 : ℝ) 1) : ‖D t‖ ≤ C := by
    have h := norm_image_sub_le_of_norm_deriv_le_segment'
      (fun r hr => (hD' r hr).hasDerivWithinAt)
      (fun r hr => hH r (Ico_subset_Icc_self hr)) t ht
    rw [hD0, sub_zero, sub_zero] at h
    exact h.trans (mul_le_of_le_one_right hC ht.2)
  have hR' (t : ℝ) (ht : t ∈ Icc (0 : ℝ) 1) : HasDerivAt R (D t) t := by
    have hg : HasDerivAt (fun r => f (line r)) (fderiv ℝ f (line t) v) t :=
      ((hf t ht).differentiableAt (by norm_num)).hasFDerivAt.comp_hasDerivAt t (hline t)
    have hquad : HasDerivAt (fun r : ℝ => r ^ 2 / 2) t t := by
      have hp : HasDerivAt (fun r : ℝ => r ^ 2) (2 * t) t := by
        simpa [id] using (hasDerivAt_id t).fun_pow 2
      simpa only [show 2 * t / 2 = t by ring] using hp.div_const 2
    simpa only [R, D, id_eq, one_smul] using
      ((hg.sub_const (f x)).fun_sub ((hasDerivAt_id t).smul_const a)).fun_sub (hquad.smul_const b)
  have h := norm_image_sub_le_of_norm_deriv_le_segment_01'
    (fun t ht => (hR' t ht).hasDerivWithinAt) (fun t ht => hD t (Ico_subset_Icc_self ht))
  simpa [R, line, a, b, H, C, secondOrderRemainder] using h

/-- On a compact subset of the twice continuously differentiable locus,
one increment radius works uniformly for the second-order remainder. -/
theorem exists_uniform_secondOrderRemainder_le_on_compact
    [LocallyCompactSpace E] {f : E → F} {K : Set E} (hK : IsCompact K)
    (hf : ∀ x ∈ K, ContDiffAt ℝ 2 f x) {ε : ℝ} (hε : 0 < ε) :
    ∃ δ > 0, ∀ x ∈ K, ∀ v : E, ‖v‖ < δ →
      ‖secondOrderRemainder f x v‖ ≤ ε * ‖v‖ ^ 2 := by
  let U := {x : E | ContDiffAt ℝ 2 f x}
  have hU : IsOpen U := isOpen_iff_mem_nhds.2 fun x hx =>
    (show ContDiffAt ℝ 2 f x from hx).eventually (by norm_num)
  obtain ⟨r, hr, hUsub⟩ := hK.exists_cthickening_subset_open hU hf
  obtain ⟨s, hs, hS⟩ := hK.exists_isCompact_cthickening
  let ρ := min r s
  have hρ : 0 < ρ := lt_min hr hs
  have hT : IsCompact (cthickening ρ K) :=
    hS.of_isClosed_subset isClosed_cthickening (cthickening_mono (min_le_right r s) K)
  have hTsub : cthickening ρ K ⊆ U :=
    (cthickening_mono (min_le_left r s) K).trans hUsub
  have hH : ContinuousOn (fderiv ℝ (fderiv ℝ f)) (cthickening ρ K) := by
    intro x hx
    have h : ContDiffAt ℝ 2 f x := hTsub hx
    exact ((h.fderiv_right (m := 1) (by norm_num)).continuousAt_fderiv one_ne_zero).continuousWithinAt
  have hu : UniformContinuousOn (fderiv ℝ (fderiv ℝ f)) (cthickening ρ K) :=
    hT.uniformContinuousOn_of_continuous hH
  obtain ⟨δ, hδ, hclose⟩ :=
    (Metric.uniformContinuousOn_iff (f := fderiv ℝ (fderiv ℝ f))).1 hu ε hε
  refine ⟨min ρ δ, lt_min hρ hδ, fun x hx v hv => ?_⟩
  have hxT : x ∈ cthickening ρ K := self_subset_cthickening _ hx
  have hvρ : ‖v‖ < ρ := hv.trans_le (min_le_left _ _)
  have hvδ : ‖v‖ < δ := hv.trans_le (min_le_right _ _)
  have hdist (t : ℝ) (ht : t ∈ Icc (0 : ℝ) 1) : dist (x + t • v) x ≤ ‖v‖ := by
    rw [dist_eq_norm, add_sub_cancel_left, norm_smul, Real.norm_eq_abs, abs_of_nonneg ht.1]
    exact mul_le_of_le_one_left (norm_nonneg _) ht.2
  have hseg (t : ℝ) (ht : t ∈ Icc (0 : ℝ) 1) : x + t • v ∈ cthickening ρ K :=
    mem_cthickening_of_dist_le _ x ρ K hx ((hdist t ht).trans hvρ.le)
  apply norm_secondOrderRemainder_le_of_hessian_variation (fun t ht => hTsub (hseg t ht))
  intro t ht
  have h := hclose x hxT (x + t • v) (hseg t ht) (by rw [dist_comm]; exact (hdist t ht).trans_lt hvδ)
  change ‖-fderiv ℝ (fderiv ℝ f) x + fderiv ℝ (fderiv ℝ f) (x + t • v)‖ < ε at h
  rw [add_comm, ← sub_eq_add_neg] at h
  exact h.le

end AutoSamplingTheory.TechnicalLemmas.Analysis.CompactTaylorRemainder
