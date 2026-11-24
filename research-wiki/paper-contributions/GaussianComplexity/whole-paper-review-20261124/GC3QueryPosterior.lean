import GC3QueryGeometry
import GC3MixtureJoint

/-! Conditional law of all ambient matrices after one actual arbitrary block query. -/
noncomputable section
open Matrix MeasureTheory ProbabilityTheory
open scoped ProbabilityTheory
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarConditional
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarFrames
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarPosterior
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarProtocol
open AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumCoupling
namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.AdaptivePosterior
variable {Y : Type*} [MeasurableSpace Y] {N k n : ℕ}

private theorem kernel_profile_eq (F : Frames k N) (d : Fin k → ℕ) (e : profile F = d)
    (hd : ∀ j, 0 < d j) {b : ℝ} (hb : b = -1 ∨ b = 1) :
    ambientKernel b F = (tupleHaar d b).map (decodeAt d F) := by
  subst d
  exact ambientKernel_apply F hd hb

theorem query_joint_at {b : ℝ} (hb : b = -1 ∨ b = 1) (F : Frames (k+1) N)
    (hd : ∀ j, 0 < profile F j) (i : Fin (k+1)) (hi : profile F i = n+2) (v : Vec N) (back : Bool)
    (tag : Vec N → Y) (ht : Measurable tag) (J : Kernel Y (Ambient (k+1) N)) [IsMarkovKernel J]
    (hJ : ∀ y, J (tag y) = ambientKernel b (PublicFrame.updateRecord F (some ((i,v,back),y)))) :
    let a := fun W : Ambient (k+1) N => tag (oracleAnswer W (i,v,back))
    let μ := ambientKernel b F
    μ.map (fun W => (a W,W)) = (μ.map a) ⊗ₘ J := by
  let d := profile F
  let G := transportFrame hi (F i).2
  let u := frameUnit G back v
  let q : Query (k+1) N := (i,v,back)
  let a := fun W : Ambient (k+1) N => tag (oracleAnswer W q)
  have ha : Measurable a := ht.comp (measurable_oracleAnswer.comp (measurable_id.prodMk measurable_const))
  let μ := ambientKernel b F
  let := markov_ambientKernel (N := N) (k := k+1) hb
  let : IsProbabilityMeasure μ := inferInstanceAs (IsProbabilityMeasure (ambientKernel b F))
  let := tupleProb hd hb
  have hμ : MeasurePreserving (decodeAt d F) (tupleHaar d b) μ :=
    ⟨(measurable_decodeAt d).of_uncurry_left,(ambientKernel_apply F hd hb).symm⟩
  have he : (⟨n+2,G⟩ : PublicFrame N) = F i := tag_transport _ hi
  by_cases hc : frameComplement G back v = 0
  · let y := frameResponse G back v u
    let gen := fun p : Unit × ResidualTuple d => decodeAt d F p.2
    have hg : MeasurePreserving gen ((Measure.dirac ()).prod (tupleHaar d b)) μ :=
      hμ.comp (measurePreserving_snd (μ := Measure.dirac ()) (ν := tupleHaar d b))
    apply joint_of_generated μ J a ha (Measure.dirac ()) (tupleHaar d b) (fun _ => tag y) measurable_const gen hg
    · intro _ w
      apply congrArg tag
      change oracleAnswer (decodeAt d F w) (i,v,back) = _
      rw [query_answer,read_selected F i hi,frameAnswer_eq]
      exact frameResponse_zero G back v hc _ _
    · intro z
      rw [hJ,updateRecord_determined_eq F i G he back v hc,ambientKernel_apply F hd hb]
  · let d' := resampleDim d i n
    have hd' (j) : 0 < d' j := by
      by_cases hj : j=i
      · subst j; simp [d',resampleDim]
      · simpa only [d',resampleDim,Function.update_of_ne hj] using hd j
    let ν := tupleHaar d' b
    let σ := sphereProbability (n+2)
    let := isProbabilityMeasure_sphereProbability (n+2)
    let : IsProbabilityMeasure ν := tupleProb hd' hb
    let t := fun z : S (n+2) => tag (frameResponse G back v z)
    have ht' : Measurable t := ht.comp (measurable_frameResponse measurable_const measurable_const
      measurable_const measurable_const measurable_id)
    let rebuild := fun p : S (n+2) × ResidualTuple d' =>
      rebuildHaarTuple d i n hi (sectionQ n) back u p.1 p.2
    let gen := decodeAt d F ∘ rebuild
    have hre : MeasurePreserving rebuild (σ.prod ν) (tupleHaar d b) :=
      measurePreserving_rebuildHaarTuple d i n hi b hb (sectionQ n) (sectionQ_meas n)
        (sectionQ_col n) (sectionQ_det n) back u
    apply joint_of_generated μ J a ha σ ν t ht' gen (hμ.comp hre)
    · intro z w
      exact congrArg tag (regenerated_tuple F i hi back v z w).2
    · intro z
      change ν.map (fun w => gen (z,w)) = J (tag (frameResponse G back v z))
      rw [hJ,updateRecord_informative_eq F i G he back v hc z,
        kernel_profile_eq _ d' (profile_afterFrames F i G back v z) hd' hb]
      apply Measure.map_congr
      exact .of_forall fun w => (regenerated_tuple F i hi back v z w).1

end AutoSamplingTheory.ExampleCases.GaussianComplexity.AdaptivePosterior
