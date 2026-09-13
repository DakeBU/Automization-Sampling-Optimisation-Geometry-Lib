import Mathlib.Analysis.Calculus.Gradient.Basic
import Mathlib.Analysis.Calculus.ContDiff.Basic
import Mathlib.Analysis.ODE.Gronwall
import Mathlib.Topology.Order.Compact

/-!
# An attained gradient-norm bound along a gradient flow

Chewi, arXiv:2605.07006v1, Section 2, Corollary 2.8. The finite normalized
bound is for positive time. Neither convexity nor a PL condition is required.
The objective and actual trajectory are supplied; no flow existence is claimed.
-/

namespace AutoSamplingTheory.TechnicalLemmas.Analysis.GradientFlowStationarity

open Set
open scoped RealInnerProductSpace

variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E] [CompleteSpace E]

/-- A minimum gradient norm is attained on the supplied time interval, and is
bounded by the square root of the initial objective gap divided by elapsed time. -/
theorem exists_min_norm_le {f : E → ℝ} {X : ℝ → E} {z : E} {T : ℝ}
    (hT : 0 < T) (hf : ContDiff ℝ 1 f) (hz : IsMinOn f univ z)
    (hX : ContinuousOn X (Icc 0 T))
    (hflow : ∀ t ∈ Ico 0 T, HasDerivWithinAt X (-gradient f (X t)) (Ici t) t) :
    ∃ s ∈ Icc 0 T, IsMinOn (fun u => ‖gradient f (X u)‖) (Icc 0 T) s ∧
      ‖gradient f (X s)‖ ≤ Real.sqrt ((f (X 0) - f z) / T) := by
  have hdf : Differentiable ℝ f := hf.differentiable (by norm_num)
  have hcg : Continuous (gradient f) :=
    (InnerProductSpace.toDual ℝ E).symm.continuous.comp (hf.continuous_fderiv (by norm_num))
  obtain ⟨s, hs, hmin⟩ := isCompact_Icc.exists_isMinOn
    (nonempty_Icc.mpr hT.le) (hcg.comp_continuousOn hX).norm
  refine ⟨s, hs, hmin, ?_⟩
  have hd (u : ℝ) (hu : u ∈ Ico 0 T) :
      HasDerivWithinAt (fun v => f (X v)) (-‖gradient f (X u)‖ ^ 2) (Ici u) u := by
    have hg : HasFDerivAt f (InnerProductSpace.toDual ℝ E (gradient f (X u))) (X u) :=
      (hdf (X u)).hasGradientAt
    simpa only [Function.comp_def, InnerProductSpace.toDual_apply_apply,
      inner_neg_right, real_inner_self_eq_norm_sq] using
      hg.comp_hasDerivWithinAt u (hflow u hu)
  have hb := le_gronwallBound_of_liminf_deriv_right_le
    (f' := fun u => -‖gradient f (X u)‖ ^ 2) (δ := f (X 0))
    (K := 0) (ε := -‖gradient f (X s)‖ ^ 2)
    (hf.continuous.comp_continuousOn hX)
    (fun u hu r hr => by simpa [slope] using (hd u hu).liminf_right_slope_le hr)
    le_rfl (fun u hu => by
      have hm := hmin (show u ∈ Icc 0 T from ⟨hu.1, hu.2.le⟩)
      have hsq := sq_le_sq₀ (norm_nonneg (gradient f (X s))) (norm_nonneg (gradient f (X u)))
      simpa using (neg_le_neg (hsq.mpr hm))) T ⟨hT.le, le_rfl⟩
  simp only [gronwallBound_K0, sub_zero] at hb
  apply (Real.le_sqrt (norm_nonneg _) (div_nonneg
    (sub_nonneg.mpr (hz (mem_univ _))) hT.le)).mpr
  apply (le_div_iff₀ hT).mpr
  have hzT : f z ≤ f (X T) := hz (mem_univ (X T))
  change f (X T) ≤ _ at hb
  nlinarith

end AutoSamplingTheory.TechnicalLemmas.Analysis.GradientFlowStationarity
