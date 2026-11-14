"""Implement only the exact sealed source row-marginal law."""
from pathlib import Path
import json

seal = json.loads(Path('research-wiki/paper-contributions/GaussianComplexity/source-row-law-statement-seal.json').read_text())
header = """import Mathlib.Probability.Distributions.Gaussian.Multivariate
import Mathlib.MeasureTheory.Constructions.Pi

noncomputable section
open MeasureTheory ProbabilityTheory
set_option autoImplicit false

/-! Row-marginal transport for the canonical independent-column realization of
arXiv2610.20492v1 Appendix C.2 p1. Joint-row independence and transport to another
ambient experiment remain separate. -/
namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumSourceRowLaw

theorem actual_source_row_marginal_law
    """
proof = """ := by
  classical
  dsimp only
  let D := EuclideanSpace ℝ (Fin d)
  let E := EuclideanSpace ℝ (Fin (q + 1))
  let Ω := Fin (q + 1) → D
  let μ : Measure Ω := Measure.pi (fun _ : Fin (q + 1) => stdGaussian D)
  intro i
  have column_coordinates :
      Measure.map (WithLp.toLp 2 : (Fin d → ℝ) → D)
        (Measure.pi (fun _ : Fin d => gaussianReal 0 1)) = stdGaussian D :=
    map_pi_eq_stdGaussian
  have coordinate_law :
      MeasurePreserving (fun x : D => x i) (stdGaussian D) (gaussianReal 0 1) := by
    refine ⟨by fun_prop, ?_⟩
    rw [← column_coordinates, Measure.map_map (by fun_prop) (by fun_prop)]
    change Measure.map (Function.eval i)
      (Measure.pi (fun _ : Fin d => gaussianReal 0 1)) = gaussianReal 0 1
    exact (measurePreserving_eval (fun _ : Fin d => gaussianReal 0 1) i).map_eq
  have collect_coordinates :
      MeasurePreserving (fun ω : Ω => fun a : Fin (q + 1) => ω a i) μ
        (Measure.pi (fun _ : Fin (q + 1) => gaussianReal 0 1)) :=
    measurePreserving_pi (fun _ : Fin (q + 1) => stdGaussian D)
      (fun _ : Fin (q + 1) => gaussianReal 0 1) (fun _ => coordinate_law)
  have wrap_row :
      MeasurePreserving (WithLp.toLp 2 : (Fin (q + 1) → ℝ) → E)
        (Measure.pi (fun _ : Fin (q + 1) => gaussianReal 0 1)) (stdGaussian E) :=
    ⟨by fun_prop, map_pi_eq_stdGaussian⟩
  exact wrap_row.comp collect_coordinates

end AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumSourceRowLaw
"""
path = Path(seal['producer']['planned_file'])
with path.open('x') as out:
    out.write(header + seal['producer']['signature'].rstrip() + proof)
print(path)
