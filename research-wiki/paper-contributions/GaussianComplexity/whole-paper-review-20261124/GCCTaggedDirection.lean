import GCCTaggedLocal
import GCCIntrinsicPreimage
noncomputable section
open Matrix MeasureTheory ProbabilityTheory
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarFrames
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarConditional
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarPosterior
open AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumCoupling
namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarRevelation

variable {Ω H : Type*} [MeasurableSpace Ω] [MeasurableSpace H]
  {N m : ℕ} {μ : Measure Ω} [IsFiniteMeasure μ] {h : Ω → H} {A : Ω → O N}

def direction (G : PublicFrame N) (A : O N) (v : Vec N) : E N :=
  WithLp.toLp 2 (normalizedPreimage G.2 A v)

def sphereOf (G : PublicFrame N) := complementSphere (exposedEuclidean G.2.domain G.2.rank)

def residualSize (G : PublicFrame N) (v : Vec N) : ℝ := ‖frameComplement G.2 true v‖

theorem measurable_residualSize {G : H → PublicFrame N} (hG : Measurable G)
    {v : H → Vec N} (hv : Measurable v) : Measurable (fun a => residualSize (G a) (v a)) := by
  apply PublicFrame.measurable_cases G hG (fun a F => residualSize F (v a))
  intro m hm
  let F := fun a => atRank m hm (G a)
  have hD : Measurable (fun a => (F a).domain) := PublicFrame.measurable_domain.comp hG
  have hR : Measurable (fun a => (F a).range) := PublicFrame.measurable_range.comp hG
  exact (measurable_frameComplement hD hR (measurable_const (a := true)) hv).norm

theorem measurable_direction {G : H → PublicFrame N} (hG : Measurable G)
    {a : H → O N} (ha : Measurable a) {v : H → Vec N} (hv : Measurable v) :
    Measurable (fun h => direction (G h) (a h) (v h)) := by
  apply PublicFrame.measurable_cases G hG (fun h F => direction F (a h) (v h))
  intro m hm
  let F := fun h => atRank m hm (G h)
  change Measurable (fun h => WithLp.toLp 2 (normalizedPreimage (F h) (a h) (v h)))
  have hD : Measurable (fun h => (F h).domain) := PublicFrame.measurable_domain.comp hG
  have hR : Measurable (fun h => (F h).range) := PublicFrame.measurable_range.comp hG
  let c := fun h => frameComplement (F h) true (v h)
  have hc : Measurable c := measurable_frameComplement hD hR measurable_const hv
  cases m with
  | zero =>
    have e (h) : c h = 0 := by apply WithLp.ofLp_injective; exact funext fun i => i.elim0
    have hz : (fun h => WithLp.toLp 2 (normalizedPreimage (F h) (a h) (v h))) = fun _ => (0 : E N) := by
      funext j
      have ej : frameComplement (F j) true (v j) = 0 := e j
      simp [normalizedPreimage,ej]
    rw [hz]; exact measurable_const
  | succ m =>
    let z : S (m+1) := coordinatePoint 0
    let k := fun h => knownPreimage (F h) (v h)
    have eqk : k = fun h => frameResponse (F h) true (v h) z - ‖c h‖ • residualLift (F h).domain (F h).rank (F h).fits z := by
      funext h; rw [frameResponse_preimage,add_sub_cancel_right]
    have hk : Measurable k := eqk ▸
      ((measurable_frameResponse hD hR (measurable_const (a := true)) hv (measurable_const (a := z))).sub
      (hc.norm.smul (measurable_residualLift hD (measurable_const (a := z)))))
    apply (PiLp.continuous_toLp 2 _).measurable.comp
    exact hc.norm.inv.smul (((measurable_response (N := N) true).comp (ha.prodMk hv)).sub hk)

theorem HaarState.uniform_of_nonzero {F : H → BlockFrame N m} {W : Ω → O m}
    (st : HaarState μ h A F W) {v : H → Vec N} (hv : Measurable v)
    (hn : ∀ᵐ ω ∂μ, frameComplement (F (h ω)) true (v (h ω)) ≠ 0) :
    ∀ᵐ a ∂μ.map h, condDistrib (fun ω => direction ⟨m,F (h ω)⟩ (A ω) (v (h ω))) h μ a =
      complementSphere (exposedEuclidean (F a).domain (F a).rank) := by
  cases m with
  | zero =>
    have hh : Measurable h := measurable_fst.comp st.law.measurable
    have hf : ∀ᵐ ω ∂μ, False := hn.mono (fun ω ne => ne (by apply WithLp.ofLp_injective; exact funext fun i => i.elim0))
    have emp : ∀ᵐ _ ∂μ.map h, False := (ae_map_iff hh.aemeasurable (p := fun _ => False) MeasurableSet.empty).mpr hf
    exact emp.mono (fun _ no => no.elim)
  | succ m => exact st.preimage_uniform_complement hv hn

set_option maxHeartbeats 900000 in
/-- The ambient normalized unknown part is conditionally uniform on the
orthogonal complement, on precisely the informative histories. Ranks and
zero/nonzero outcomes may both vary with the original arbitrary history. -/
theorem TaggedState.preimage_uniform_complement {G : H → PublicFrame N} (st : TaggedState μ h A G)
    {v : H → Vec N} (hv : Measurable v) :
    ∀ᵐ a ∂μ.map h, residualSize (G a) (v a) ≠ 0 →
      condDistrib (fun ω => direction (G (h ω)) (A ω) (v (h ω))) h μ a =
        complementSphere (exposedEuclidean (G a).2.domain (G a).2.rank) := by
  let Y := fun ω => direction (G (h ω)) (A ω) (v (h ω))
  have hY : Measurable Y := measurable_direction (st.frame.comp st.history) st.ambient (hv.comp st.history)
  let s := fun i : Fin (N+1) => {a | (G a).1 = i.val ∧ residualSize (G a) (v a) ≠ 0}
  have hs (i : Fin (N+1)) : MeasurableSet (s i) :=
    ((PublicFrame.measurable_profile.comp st.frame) (measurableSet_singleton i.val)).inter
      ((measurable_residualSize st.frame hv) (measurableSet_singleton (0:ℝ)).compl)
  have each (i : Fin (N+1)) : ∀ᵐ a ∂μ.map h, a ∈ s i →
      condDistrib Y h μ a = complementSphere (exposedEuclidean (G a).2.domain (G a).2.rank) := by
    apply (ae_restrict_iff' (hs i)).mp
    let μr := μ.restrict (h ⁻¹' s i)
    have hlaw : condDistrib Y h μr =ᵐ[(μ.map h).restrict (s i)] condDistrib Y h μ :=
      condDistrib_restrict_history st.history hY (hs i)
    have hm : μr.map h = (μ.map h).restrict (s i) := (Measure.restrict_map st.history (hs i)).symm
    have hi : i.val ≤ N := by omega
    let F := fun a => atRank i.val hi (G a)
    let tag := fun a => (⟨i.val,F a⟩ : PublicFrame N)
    have ht : Measurable tag := (PublicFrame.measurable_tag i.val).comp (measurable_atRank st.frame hi)
    have eqv {a} (ha : a ∈ s i) : tag a = G a := tag_atRank hi ha.1
    have hmem : ∀ᵐ a ∂μr.map h, a ∈ s i := hm ▸ ae_restrict_mem (hs i)
    have htold : G =ᵐ[μr.map h] tag := hmem.mono (fun a ha => (eqv ha).symm)
    have localState := ((st.restrict_history (hs i)).congr_frame ht htold).fixed
    let Yf := fun ω => direction (tag (h ω)) (A ω) (v (h ω))
    have he : Y =ᵐ[μr] Yf := by
      filter_upwards [ae_restrict_mem (μ := μ) (st.history (hs i))] with ω hw
      exact congrArg (fun T => direction T (A ω) (v (h ω))) (eqv hw).symm
    have nonzero : ∀ᵐ ω ∂μr, frameComplement (F (h ω)) true (v (h ω)) ≠ 0 := by
      filter_upwards [ae_restrict_mem (μ := μ) (st.history (hs i))] with ω hw
      have e : residualSize (tag (h ω)) (v (h ω)) ≠ 0 := (eqv hw).symm ▸ hw.2
      exact norm_ne_zero_iff.mp e
    have e : ∀ᵐ a ∂μr.map h, condDistrib Yf h μr a =
        complementSphere (exposedEuclidean (F a).domain (F a).rank) :=
      localState.uniform_of_nonzero hv nonzero
    have eqcond : condDistrib Y h μr = condDistrib Yf h μr := condDistrib_congr he Filter.EventuallyEq.rfl
    rw [← hm] at hlaw ⊢
    filter_upwards [e,hlaw,hmem] with a ea el ha
    have es : sphereOf (tag a) = sphereOf (G a) := congrArg sphereOf (eqv ha)
    have ea' : condDistrib Yf h μr a = sphereOf (tag a) := ea
    calc
      condDistrib Y h μ a = condDistrib Y h μr a := el.symm
      _ = condDistrib Yf h μr a := congrArg (fun K : Kernel H (E N) => K a) eqcond
      _ = sphereOf (tag a) := ea'
      _ = sphereOf (G a) := es
  filter_upwards [ae_all_iff.mpr each] with a ha
  intro hz
  have e := (G a).2.fits
  exact ha ⟨(G a).1,by omega⟩ ⟨rfl,hz⟩

#print axioms TaggedState.preimage_uniform_complement
end AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarRevelation
