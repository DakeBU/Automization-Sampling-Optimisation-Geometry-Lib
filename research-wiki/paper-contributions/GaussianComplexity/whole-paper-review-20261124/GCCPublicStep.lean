import GCCStateEndpoints
open MeasureTheory ProbabilityTheory
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarFrames
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarConditional
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarPosterior
open AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumCoupling
noncomputable section
namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarRevelation
open Classical in
/-- Update the public frame using precisely the new actual image or preimage.
Zero residual leaves it unchanged. An informative last unit direction fully
determines the matrix. -/
def nextPublic {N : ℕ} (F : PublicFrame N) (b : Bool) (x y : Vec N) : PublicFrame N :=
  match F with
  | ⟨0,D⟩ => ⟨0,D⟩
  | ⟨1,D⟩ => if frameComplement D b x = 0 then ⟨1,D⟩ else
      ⟨0,fullFrame (D.realize (lastDecode (frameUnit D b x) (frameUnit D (!b) y)))⟩
  | ⟨n+2,D⟩ => if frameComplement D b x = 0 then ⟨n+2,D⟩ else
      ⟨n+1,frameAfter D (sectionQ n) b x (frameUnit D (!b) y)⟩

theorem measurable_nextPublic {H : Type*} [MeasurableSpace H] {N : ℕ} {F : H → PublicFrame N}
    (hF : Measurable F) (b : Bool) {x y : H → Vec N} (hx : Measurable x) (hy : Measurable y) :
    Measurable (fun a => nextPublic (F a) b (x a) (y a)) := by
  classical
  apply PublicFrame.measurable_cases F hF (fun a G => nextPublic G b (x a) (y a))
  intro m hm
  let D : H → BlockFrame N m := fun a => ⟨N-m,by omega,(F a).2.domain,(F a).2.range⟩
  have hD : Measurable (fun a => (D a).domain) := PublicFrame.measurable_domain.comp hF
  have hR : Measurable (fun a => (D a).range) := PublicFrame.measurable_range.comp hF
  have old := (PublicFrame.measurable_tag m).comp (PublicFrame.measurable_blockFrame hD hR)
  change Measurable (fun a => nextPublic ⟨m,D a⟩ b (x a) (y a))
  cases m with
  | zero => exact old
  | succ n =>
    have hc := measurable_frameComplement hD hR (measurable_const (a := b)) hx
    have hs := hc (measurableSet_singleton 0)
    have hu := measurable_frameUnit hD hR (measurable_const (a := b)) hx
    have hz := measurable_frameUnit hD hR (measurable_const (a := !b)) hy
    cases n with
    | zero =>
      apply Measurable.ite hs old
      apply (PublicFrame.measurable_tag 0).comp
      refine PublicFrame.measurable_blockFrame ?_ ?_
      · exact measurable_const
      exact measurable_realize_family hD hR (measurable_lastDecode.comp (hu.prodMk hz))
    | succ n =>
      apply Measurable.ite hs old
      apply (PublicFrame.measurable_tag (n+1)).comp
      have e := measurable_frameAfter (sectionQ n) (sectionQ_meas n) hD hR (measurable_const (a := b)) hx hz
      exact PublicFrame.measurable_blockFrame e.1 e.2

end AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarRevelation
