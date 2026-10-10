import Mathlib.MeasureTheory.Measure.Tilted
import Mathlib.MeasureTheory.Measure.Haar.NormedSpace
import Mathlib.MeasureTheory.Group.Integral
import Mathlib.Tactic

/-! A literal affine change of variables for normalized Lebesgue tilts.
The true Jacobian cancels between the partition and set numerator. This is
an identity of Mathlib tilted measures, not a probability assertion: applications
must produce actual finite positive partitions separately. Dimension zero is
allowed. The scaling-only private route in NormalizedReferenceCall was searched;
this canonical leaf adds arbitrary translations and nonzero real scales. -/

namespace AutoSamplingTheory.TechnicalLemmas.Measure.AffineGibbs
open MeasureTheory Set
noncomputable section
variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
  [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]

/-- Actual affine pushforward, with its inverse potential and Jacobian canceled.
No regularity, integrability, probability or moment certificate is assumed. -/
theorem map_affine_gibbs (F : E → ℝ) (p : E) {s : ℝ} (hs : s ≠ 0) :
    Measure.map (fun x : E => p+s • x)
      ((volume : Measure E).tilted (fun x => -F x)) =
      volume.tilted (fun x => -F (s⁻¹ • (x-p))) 