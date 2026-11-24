import GC43FrameMeasurable
noncomputable section
open Matrix MeasureTheory
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarFrames
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarConditional
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarPosterior
open AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumCoupling
namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarRevelation

/-- Embed a unit vector in residual coordinates into its ambient complement. -/
def residualLift {N m : ℕ} (D : O N) (r : ℕ) (e : m+r=N) (z : S m) : Vec N :=
  castVec e (encodeResponse (castOrthogonal e.symm D) (0 : Vec r) 1 z)

theorem measurable_residualLift {H : Type*} [MeasurableSpace H] {N m : ℕ}
    {F : H → BlockFrame N m} {z : H → S m}
    (hD : Measurable fun h => (F h).domain) (hz : Measurable z) :
    Measurable (fun h => residualLift (F h).domain (F h).rank (F h).fits (z h)) := by
  apply measurable_frameFamily F (fun a f => residualLift f.domain f.rank f.fits (z a))
  intro r e; subst N
  exact measurable_encodeResponse (m := m) (r := r) hD
    (measurable_const (a := (0 : Vec r))) (measurable_const (a := (1 : ℝ))) hz

end AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarRevelation
