import B3HistoryUpdate
import Mathlib.Probability.Kernel.MeasurableLIntegral

/-! Iterating a disintegration while retaining the same hidden random object. -/
noncomputable section
open MeasureTheory ProbabilityTheory
open scoped ProbabilityTheory
namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.AdaptivePosterior

variable {H X Z : Type*} [MeasurableSpace H] [MeasurableSpace X] [MeasurableSpace Z]

theorem joint_update (ρ : Measure H) [SFinite ρ] (K : Kernel H X) [IsMarkovKernel K]
    (next : H × X → H) (hm : Measurable next)
    (localLaw : ∀ h, (K h).map (fun x => (next (h,x), x)) =
      ((K h).map (fun x => next (h,x))) ⊗ₘ K) :
    (ρ ⊗ₘ K).map (fun p => (next p, p.2)) = ((ρ ⊗ₘ K).map next) ⊗ₘ K := by
  ext s hs
  rw [Measure.map_apply (hm.prodMk measurable_snd) hs,
    Measure.compProd_apply ((hm.prodMk measurable_snd) hs), Measure.compProd_apply hs,
    lintegral_map (Kernel.measurable_kernel_prodMk_left hs) hm,
    Measure.lintegral_compProd (show Measurable (fun p : H × X => K (next p) (Prod.mk (next p) ⁻¹' s)) from
      (Kernel.measurable_kernel_prodMk_left hs).comp hm)]
  apply lintegral_congr
  intro h
  have e := congrArg (fun ν : Measure (H × X) => ν s) (localLaw h)
  have hn : Measurable (fun x => next (h,x)) := hm.comp measurable_prodMk_left
  change ((K h).map (fun x => (next (h,x),x))) s = _ at e
  rw [Measure.map_apply (show Measurable (fun x => (next (h,x),x)) from hn.prodMk measurable_id) hs,
    Measure.compProd_apply hs, lintegral_map (Kernel.measurable_kernel_prodMk_left hs) hn] at e
  exact e

/-- A deterministic simulation can always retain its original oracle across all public steps. -/
def repeatState (next : H × X → H) (h : H) : ℕ → X → H
  | 0, _ => h
  | n+1, x => next (repeatState next h n x, x)

theorem measurable_repeatState (next : H × X → H) (hm : Measurable next) (h : H) (n : ℕ) :
    Measurable (repeatState next h n) := by
  induction n with
  | zero => exact measurable_const
  | succ n ih => exact hm.comp (ih.prodMk measurable_id)

theorem repeat_joint (K : Kernel H X) [IsMarkovKernel K]
    (next : H × X → H) (hm : Measurable next)
    (localLaw : ∀ h, (K h).map (fun x => (next (h,x),x)) =
      ((K h).map (fun x => next (h,x))) ⊗ₘ K) (h : H) (n : ℕ) :
    (K h).map (fun x => (repeatState next h n x, x)) =
      ((K h).map (repeatState next h n)) ⊗ₘ K := by
  induction n with
  | zero =>
    simp only [repeatState, Measure.map_const, measure_univ, one_smul]
    ext s hs
    rw [Measure.compProd_apply hs, Measure.map_apply measurable_prodMk_left hs,
      lintegral_dirac' _ (Kernel.measurable_kernel_prodMk_left hs)]
  | succ n ih =>
    let pair (x : X) := (repeatState next h n x, x)
    have hp : Measurable pair := (measurable_repeatState _ hm _ _).prodMk measurable_id
    have hr := joint_update ((K h).map (repeatState next h n)) K next hm localLaw
    rw [← ih, Measure.map_map (hm.prodMk measurable_snd) hp, Measure.map_map hm hp] at hr
    exact hr

/-- Forgetting a deterministic part of a public state preserves any posterior kernel
that already depends only on the retained public record. -/
theorem project_joint (ρ : Measure H) [SFinite ρ] (r : H → Z) (hr : Measurable r)
    (K : Kernel H X) [IsMarkovKernel K] (J : Kernel Z X) [IsMarkovKernel J]
    (hK : ∀ h, K h = J (r h)) :
    (ρ ⊗ₘ K).map (Prod.map r id) = (ρ.map r) ⊗ₘ J := by
  ext s hs
  rw [Measure.map_apply (hr.prodMap measurable_id) hs,
    Measure.compProd_apply ((hr.prodMap measurable_id) hs), Measure.compProd_apply hs,
    lintegral_map (Kernel.measurable_kernel_prodMk_left hs) hr]
  apply lintegral_congr
  intro h
  rw [hK]
  rfl

end AutoSamplingTheory.ExampleCases.GaussianComplexity.AdaptivePosterior
