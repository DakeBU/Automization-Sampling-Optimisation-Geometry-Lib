import AutoSamplingTheory.TechnicalLemmas.Measure.TransportGluing
import Mathlib.MeasureTheory.Integral.MeanInequalities

/-!
# L2 Minkowski core for the Wasserstein triangle inequality

For a joint law of `(X,Y,Z)`, the analytic part of the source proof is

`|X-Z| <= |X-Y| + |Y-Z|`

followed by Minkowski in `L2`.

This module intentionally stops at that joint-law statement. It does **not**
claim the Wasserstein triangle inequality: gluing transport plans and passing
from concrete joint-law costs to the transport infima are separate topology
nodes.
-/

namespace AutoSamplingTheory
namespace TechnicalLemmas
namespace Measure
namespace WassersteinTriangleCore

open MeasureTheory
open scoped ENNReal

/-- First edge length on a triple encoded as `((x,y),z)`. -/
def edgeLength12
    {E : Type*} [NormedAddCommGroup E] : ((E × E) × E) → ℝ≥0∞ :=
  fun p => ENNReal.ofReal ‖p.1.1 - p.1.2‖

/-- Second edge length on a triple encoded as `((x,y),z)`. -/
def edgeLength23
    {E : Type*} [NormedAddCommGroup E] : ((E × E) × E) → ℝ≥0∞ :=
  fun p => ENNReal.ofReal ‖p.1.2 - p.2‖

/-- Endpoint edge length on a triple encoded as `((x,y),z)`. -/
def edgeLength13
    {E : Type*} [NormedAddCommGroup E] : ((E × E) × E) → ℝ≥0∞ :=
  fun p => ENNReal.ofReal ‖p.1.1 - p.2‖

/-- The extended-nonnegative first edge length is measurable on a Borel normed
space. -/
theorem edgeLength12_measurable
    {E : Type*} [NormedAddCommGroup E] [MeasurableSpace E] [BorelSpace E]
    [SecondCountableTopology E] :
    Measurable (edgeLength12 (E := E)) := by
  have hpair : Measurable (fun p : ((E × E) × E) => (p.1.1, p.1.2)) :=
    (measurable_fst.comp measurable_fst).prodMk (measurable_snd.comp measurable_fst)
  have hdist : Measurable (fun p : ((E × E) × E) => dist p.1.1 p.1.2) :=
    measurable_dist.comp hpair
  change Measurable (fun p : ((E × E) × E) => ENNReal.ofReal ‖p.1.1 - p.1.2‖)
  simpa only [dist_eq_norm] using hdist.ennreal_ofReal

/-- Measurability of the middle-to-last edge. -/
theorem edgeLength23_measurable
    {E : Type*} [NormedAddCommGroup E] [MeasurableSpace E] [BorelSpace E]
    [SecondCountableTopology E] :
    Measurable (edgeLength23 (E := E)) := by
  have hpair : Measurable (fun p : ((E × E) × E) => (p.1.2, p.2)) :=
    (measurable_snd.comp measurable_fst).prodMk measurable_snd
  have hdist : Measurable (fun p : ((E × E) × E) => dist p.1.2 p.2) :=
    measurable_dist.comp hpair
  change Measurable (fun p : ((E × E) × E) => ENNReal.ofReal ‖p.1.2 - p.2‖)
  simpa only [dist_eq_norm] using hdist.ennreal_ofReal

/-- Measurability of the endpoint edge. -/
theorem edgeLength13_measurable
    {E : Type*} [NormedAddCommGroup E] [MeasurableSpace E] [BorelSpace E]
    [SecondCountableTopology E] :
    Measurable (edgeLength13 (E := E)) := by
  have hpair : Measurable (fun p : ((E × E) × E) => (p.1.1, p.2)) :=
    (measurable_fst.comp measurable_fst).prodMk measurable_snd
  have hdist : Measurable (fun p : ((E × E) × E) => dist p.1.1 p.2) :=
    measurable_dist.comp hpair
  change Measurable (fun p : ((E × E) × E) => ENNReal.ofReal ‖p.1.1 - p.2‖)
  simpa only [dist_eq_norm] using hdist.ennreal_ofReal

/-- Pointwise triangle inequality for the three edge lengths. -/
theorem edgeLength13_le_add
    {E : Type*} [NormedAddCommGroup E] (p : ((E × E) × E)) :
    edgeLength13 p ≤ edgeLength12 p + edgeLength23 p := by
  have hreal : ‖p.1.1 - p.2‖ ≤ ‖p.1.1 - p.1.2‖ + ‖p.1.2 - p.2‖ := by
    simpa only [dist_eq_norm] using dist_triangle p.1.1 p.1.2 p.2
  calc
    ENNReal.ofReal ‖p.1.1 - p.2‖ ≤
        ENNReal.ofReal (‖p.1.1 - p.1.2‖ + ‖p.1.2 - p.2‖) :=
      ENNReal.ofReal_le_ofReal hreal
    _ = ENNReal.ofReal ‖p.1.1 - p.1.2‖ + ENNReal.ofReal ‖p.1.2 - p.2‖ :=
      ENNReal.ofReal_add (norm_nonneg _) (norm_nonneg _)

/-- The ENNReal `L2` seminorm used by the transport proof. The exponent is a
real `rpow`, matching Mathlib's Minkowski theorem. -/
noncomputable def l2Seminorm
    {Ω : Type*} [MeasurableSpace Ω]
    (μ : Measure Ω) (f : Ω → ℝ≥0∞) : ℝ≥0∞ :=
  (∫⁻ x, f x ^ (2 : ℝ) ∂μ) ^ (1 / (2 : ℝ))

/-- Monotonicity of the ENNReal `L2` seminorm. -/
theorem l2Seminorm_mono
    {Ω : Type*} [MeasurableSpace Ω] (μ : Measure Ω)
    {f g : Ω → ℝ≥0∞} (hfg : ∀ x, f x ≤ g x) :
    l2Seminorm μ f ≤ l2Seminorm μ g := by
  unfold l2Seminorm
  gcongr with x
  exact hfg x

/-- Minkowski's inequality in the exact `p=2` form used below. -/
theorem l2Seminorm_add_le
    {Ω : Type*} [MeasurableSpace Ω] (μ : Measure Ω)
    {f g : Ω → ℝ≥0∞}
    (hf : AEMeasurable f μ) (hg : AEMeasurable g μ) :
    l2Seminorm μ (f + g) ≤ l2Seminorm μ f + l2Seminorm μ g := by
  unfold l2Seminorm
  simpa only [Pi.add_apply] using
    (ENNReal.lintegral_Lp_add_le (μ := μ) (p := (2 : ℝ)) hf hg (by norm_num))

/-- The `L2` endpoint displacement of any triple joint law is bounded by the
sum of its two adjacent `L2` displacements. -/
theorem l2_edge_triangle
    {E : Type*} [NormedAddCommGroup E] [MeasurableSpace E] [BorelSpace E]
    [SecondCountableTopology E]
    (γ : Measure ((E × E) × E)) :
    l2Seminorm γ (edgeLength13 (E := E)) ≤
      l2Seminorm γ (edgeLength12 (E := E)) +
        l2Seminorm γ (edgeLength23 (E := E)) := by
  calc
    l2Seminorm γ (edgeLength13 (E := E)) ≤
        l2Seminorm γ (edgeLength12 (E := E) + edgeLength23 (E := E)) :=
      l2Seminorm_mono γ edgeLength13_le_add
    _ ≤ l2Seminorm γ (edgeLength12 (E := E)) +
          l2Seminorm γ (edgeLength23 (E := E)) :=
      l2Seminorm_add_le γ edgeLength12_measurable.aemeasurable
        edgeLength23_measurable.aemeasurable

end WassersteinTriangleCore
end Measure
end TechnicalLemmas
end AutoSamplingTheory