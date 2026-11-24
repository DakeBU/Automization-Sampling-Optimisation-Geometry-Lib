import GCCPreimage
import GCCResidualSphere

noncomputable section
open Matrix MeasureTheory ProbabilityTheory
open scoped ProbabilityTheory
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarFrames
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarConditional
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarPosterior
open AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumCoupling
namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarRevelation

variable {Ω H : Type*} [MeasurableSpace Ω] [MeasurableSpace H] {N m : ℕ}
  {μ : Measure Ω} [IsFiniteMeasure μ] {h : Ω → H} {A : Ω → O N}

/-- Equation (27) in ambient Euclidean coordinates. Given the original history,
the normalized unknown part of the actual preimage is uniform on the unit sphere of
the orthogonal complement of the original exposed domain. -/
theorem HaarState.preimage_uniform_complement {F : H → BlockFrame N (m+1)} {W : Ω → O (m+1)}
    (state : HaarState μ h A F W) {x : H → Vec N} (hx : Measurable x)
    (hc : ∀ᵐ ω ∂μ, frameComplement (F (h ω)) true (x (h ω)) ≠ 0) :
    ∀ᵐ a ∂μ.map h, condDistrib (fun ω => WithLp.toLp 2
      (normalizedPreimage (F (h ω)) (A ω) (x (h ω)))) h μ a =
        complementSphere (exposedEuclidean (F a).domain (F a).rank) := by
  let Y := fun ω => normalizedPreimage (F (h ω)) (A ω) (x (h ω))
  let c := fun a => frameComplement (F a) true (x a)
  let k := fun a => knownPreimage (F a) (x a)
  let z : S (m+1) := coordinatePoint 0
  have hC : Measurable c := measurable_frameComplement state.domain state.range measurable_const hx
  have hK : Measurable k := by
    have e : k = fun a => frameResponse (F a) true (x a) z - ‖c a‖ •
        residualLift (F a).domain (F a).rank (F a).fits z := by
      funext a; rw [frameResponse_preimage]; exact (add_sub_cancel_right _ _).symm
    rw [e]
    exact (measurable_frameResponse state.domain state.range measurable_const hx measurable_const).sub
      (hC.norm.smul (measurable_residualLift state.domain measurable_const))
  have hh := measurable_fst.comp state.law.measurable
  have hY : Measurable Y := (hC.norm.inv.comp hh).smul
    (((measurable_response true).comp (state.ambient.prodMk (hx.comp hh))).sub (hK.comp hh))
  have hl := (PiLp.continuous_toLp 2 (fun _ : Fin N => ℝ)).measurable
  have hpush := condDistrib_comp (mβ := inferInstance) (μ := μ) h hY.aemeasurable hl
  filter_upwards [hpush,state.preimage_uniform hx hc] with a hp he
  change condDistrib (WithLp.toLp 2 ∘ Y) h μ a = _
  have hL : Measurable (residualLift (F a).domain (F a).rank (F a).fits) :=
    measurable_residualLift (F := fun _ : S (m+1) => F a) measurable_const measurable_id
  rw [hp,Kernel.map_apply _ hl,show condDistrib Y h μ a = _ from he,
    Measure.map_map hl hL]
  exact (measurePreserving_residualLift (F a).domain (F a).rank (F a).fits).map_eq

#print axioms HaarState.preimage_uniform_complement
end AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarRevelation
