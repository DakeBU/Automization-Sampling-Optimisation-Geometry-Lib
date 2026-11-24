import GCCRevelationLaw
import GCCAmbientState
import GCCLastCoordinate
import GCCResidualSphere
import GCCLiftInverse

/-! Both clauses of Fact C.1 for the actual ambient vector. Coordinates of an isometry
between the random spaces may be supplied by any measurable orthonormal frames. -/
noncomputable section
set_option maxHeartbeats 900000
set_option backward.isDefEq.respectTransparency false
open Matrix MeasureTheory ProbabilityTheory
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarConditional
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarFrames
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarPosterior
open AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumCoupling
open AutoSamplingTheory.TechnicalLemmas.Probability.ParameterizedPushforward
open AutoSamplingTheory.TechnicalLemmas.Probability.OrthogonalHaar
namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarRevelation

def directionLift {N m : ℕ} (F : BlockFrame N m) (b : Bool) (z : S m) : Vec N :=
  residualLift (queryFrame b F.domain F.range) F.rank F.fits z

private theorem response_on_lift {N m : ℕ} (F : BlockFrame N m) (b : Bool) (W : O m) (u : S m) :
    response b (F.realize W) (directionLift F b u) =
      directionLift F (!b) (rotate (if b then W⁻¹ else W) u) := by
  rcases F with ⟨r,e,D,R⟩
  subst N
  cases b
  · exact (normalized_responses D R W 0 1 u).1
  · exact (normalized_responses D R W 0 1 u).2

/-- F and G are the unexposed domain and range subspaces. Revealing an image
or a preimage of a history-measurable ambient unit vector gives the uniform
sphere law in the opposite subspace. Given that observed ambient answer, the
remaining isometry in its new orthonormal frames is Haar. -/
theorem actual_unit_revelation {N m : ℕ} {Ω H : Type*} [MeasurableSpace Ω] [MeasurableSpace H]
    (μ : Measure Ω) [IsFiniteMeasure μ] (h : Ω → H) (F : H → BlockFrame N (m+1)) (W : Ω → O (m+1))
    (hD : Measurable (fun a => (F a).domain)) (hR : Measurable (fun a => (F a).range))
    (hW : LawGiven μ h W (orthogonalHaar (m+1))) (b : Bool) (x : H → E N) (hx : Measurable x)
    (hu : ∀ᵐ a ∂μ.map h, ‖x a‖ = 1 ∧ x a ∈
      (exposedEuclidean (queryFrame b (F a).domain (F a).range) (F a).rank)ᗮ) :
    let y (ω : Ω) := WithLp.toLp 2 (response b ((F (h ω)).realize (W ω)) (x (h ω)).ofLp)
    let small (ω : Ω) := (reveal b (frameUnit (F (h ω)) b (x (h ω)).ofLp) (W ω)).2
    (∀ᵐ a ∂μ.map h, condDistrib y h μ a =
      complementSphere (exposedEuclidean (queryFrame (!b) (F a).domain (F a).range) (F a).rank)) ∧
    LawGiven μ (fun ω => (h ω,y ω)) small (orthogonalHaar m) := by
  let u (a : H) := frameUnit (F a) b (x a).ofLp
  have hm : Measurable u := measurable_frameUnit hD hR measurable_const
    ((PiLp.continuous_ofLp 2 _).measurable.comp hx)
  let z (ω : Ω) := (reveal b (u (h ω)) (W ω)).1
  let v (ω : Ω) := (reveal b (u (h ω)) (W ω)).2
  have hj := conditional_haar_revelation hW b u hm
  have hz : LawGiven μ h z (sphereProbability (m+1)) := hj.1
  have hv : LawGiven μ (fun ω => (h ω,z ω)) v (orthogonalHaar m) := hj.2
  let lift (a : H) (t : S (m+1)) := WithLp.toLp 2 (directionLift (F a) (!b) t)
  have hlift : Measurable (Function.uncurry lift) := by
    let F' : H → BlockFrame N (m+1) := fun a => ⟨(F a).rank,(F a).fits,
      queryFrame (!b) (F a).domain (F a).range,1⟩
    have hd : Measurable (fun p : H × S (m+1) => (F' p.1).domain) :=
      (measurable_queryFrame measurable_const hD hR).comp measurable_fst
    exact (PiLp.continuous_toLp 2 _).measurable.comp
      (measurable_residualLift (F := fun p => F' p.1) hd measurable_snd)
  have hLift : Measurable (fun p : H × S (m+1) => lift p.1 p.2) := hlift
  let y (ω : Ω) := WithLp.toLp 2 (response b ((F (h ω)).realize (W ω)) (x (h ω)).ofLp)
  have hh : Measurable h := measurable_fst.comp hz.measurable
  have hA : Measurable (fun ω => (F (h ω)).realize (W ω)) :=
    measurable_realize_family (F := fun ω => F (h ω)) (hD.comp hh) (hR.comp hh) (measurable_snd.comp hW.measurable)
  have hX : Measurable (fun ω => (x (h ω)).ofLp) := (PiLp.continuous_ofLp 2 _).measurable.comp (hx.comp hh)
  let inputs (ω : Ω) : O N × Vec N := ((F (h ω)).realize (W ω),(x (h ω)).ofLp)
  have hI : Measurable inputs := hA.prodMk hX
  have hraw : Measurable ((fun p : O N × Vec N => response b p.1 p.2) ∘ inputs) :=
    (measurable_response b).comp hI
  have hy : Measurable y := (PiLp.continuous_toLp 2 _).measurable.comp hraw
  have he : y =ᵐ[μ] (fun ω => lift (h ω) (z ω)) := by
    filter_upwards [ae_of_ae_map hh.aemeasurable hu] with ω hw
    have ex := residualLift_frameUnit_eq (F (h ω)) b (x (h ω)).ofLp hw.1 hw.2
    have ey := response_on_lift (F (h ω)) b (W ω) (u (h ω))
    change directionLift (F (h ω)) b (u (h ω)) = _ at ex
    rw [ex] at ey
    exact congrArg (WithLp.toLp 2) (ey.trans
      (congrArg (directionLift (F (h ω)) (!b)) (reveal_direction b (u (h ω)) (W ω)).symm))
  let := isProbabilityMeasure_sphereProbability (m+1)
  let := (orthogonalHaar_spec m).1
  have hl (a : H) : (sphereProbability (m+1)).map (lift a) =
      complementSphere (exposedEuclidean (queryFrame (!b) (F a).domain (F a).range) (F a).rank) :=
    (measurePreserving_residualLift _ _ (F a).fits).map_eq
  let lifted (ω : Ω) := lift (h ω) (z ω)
  have stm : Measurable lifted := hlift.comp hz.measurable
  have joint : μ.map (fun ω => (h ω,lifted ω)) = ((μ.map h).prod (sphereProbability (m+1))).map
      (fun p : H × S (m+1) => (p.1,lift p.1 p.2)) := by
    rw [← hz.map_eq, Measure.map_map (measurable_fst.prodMk hLift) hz.measurable]; rfl
  let := isMarkovKernel_kernel (sphereProbability (m+1)) lift hlift
  have hdistr := condDistrib_ae_eq_of_measure_eq_compProd h stm.aemeasurable
    (joint.trans (map_prod_eq_compProd _ _ lift hlift))
  constructor
  · change ∀ᵐ a ∂μ.map h, condDistrib y h μ a = _
    rw [condDistrib_congr he Filter.EventuallyEq.rfl]
    filter_upwards [hdistr] with a ha
    exact ha.trans ((kernel_apply _ _ hLift a).trans (hl a))
  · change LawGiven μ (fun ω => (h ω,y ω)) v (orthogonalHaar m)
    have hvm : Measurable v := (measurable_snd : Measurable (Prod.snd : (H × S (m+1)) × O m → O m)).comp hv.measurable
    have hs := hv.map_history (measurable_fst.prodMk hLift)
    exact hs.congr_ae (hh.prodMk hy) hvm
      (he.mono (fun ω heω => Prod.ext rfl heω.symm)) Filter.EventuallyEq.rfl

#print axioms actual_unit_revelation
end AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarRevelation
