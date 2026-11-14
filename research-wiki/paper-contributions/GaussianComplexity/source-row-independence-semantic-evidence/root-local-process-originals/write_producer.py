"""Implement only the unchanged sealed joint-row independence proposition."""
from pathlib import Path
import json

w = Path(__file__).resolve().parent
seal = json.loads((w / 'statement-seal-v1.json').read_bytes())
p = Path(seal['producer']['planned_file'])
head = '''import AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumSourceRowLaw
import Mathlib.Probability.Independence.Basic
import Mathlib.Probability.ProductMeasure

noncomputable section
open MeasureTheory ProbabilityTheory
open AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumSourceRowLaw
set_option autoImplicit false

namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumSourceRowIndependence

theorem actual_source_rows_independent
    '''
proof = r''' := by
  classical
  dsimp only
  let Q := Fin (q + 1)
  let I := Fin d
  let D := EuclideanSpace ℝ I
  let E := EuclideanSpace ℝ Q
  let Ω := Q → D
  let μ : Measure Ω := Measure.pi (fun _ : Q => stdGaussian D)
  let row : I → Ω → E := fun i ω => WithLp.toLp 2 (fun a : Q => ω a i)
  let σ : Measure ℝ := gaussianReal 0 1
  let ν : Measure (Q → I → ℝ) :=
    Measure.pi (fun _ : Q => Measure.pi (fun _ : I => σ))
  let ρ : Measure (I → Q → ℝ) :=
    Measure.pi (fun _ : I => Measure.pi (fun _ : Q => σ))
  change iIndepFun row μ
  have row_law := actual_source_row_marginal_law (d := d) (q := q) hq
  change ∀ i : I, MeasurePreserving (row i) μ (stdGaussian E) at row_law

  -- The full physical-coordinate product law, not merely scalar marginals.
  have column_product :
      Measure.map (WithLp.toLp 2 : (I → ℝ) → D)
        (Measure.pi (fun _ : I => σ)) = stdGaussian D :=
    map_pi_eq_stdGaussian
  have unwrap_column :
      MeasurePreserving (fun x : D => fun i : I => x i)
        (stdGaussian D) (Measure.pi (fun _ : I => σ)) := by
    have hm : Measurable (fun x : D => fun i : I => x i) := by
      dsimp [D]
      fun_prop
    refine ⟨hm, ?_⟩
    rw [← column_product, Measure.map_map hm (by fun_prop)]
    change Measure.map id (Measure.pi (fun _ : I => σ)) = _
    exact Measure.map_id
  have unwrap_columns :
      MeasurePreserving (fun ω : Ω => fun a : Q => fun i : I => ω a i) μ ν :=
    measurePreserving_pi (fun _ : Q => stdGaussian D)
      (fun _ : Q => Measure.pi (fun _ : I => σ)) (fun _ => unwrap_column)

  -- Flatten, permute the two finite indices, and regroup the same scalar array.
  have flatten :
      MeasurePreserving (MeasurableEquiv.curry Q I ℝ).symm ν
        (Measure.pi (fun _ : Q × I => σ)) := by
    refine ⟨(MeasurableEquiv.curry Q I ℝ).symm.measurable, ?_⟩
    simpa only [Measure.infinitePi_eq_pi] using
      (Measure.infinitePi_map_curry_symm (fun (_ : Q) (_ : I) => σ))
  have swap :=
    measurePreserving_piCongrLeft (α := fun _ : I × Q => ℝ)
      (fun _ : I × Q => σ) (Equiv.prodComm Q I)
  have regroup :
      MeasurePreserving (MeasurableEquiv.curry I Q ℝ)
        (Measure.pi (fun _ : I × Q => σ)) ρ := by
    refine ⟨(MeasurableEquiv.curry I Q ℝ).measurable, ?_⟩
    simpa only [Measure.infinitePi_eq_pi] using
      (Measure.infinitePi_map_curry (fun (_ : I) (_ : Q) => σ))
  have transpose :
      MeasurePreserving (fun x : Q → I → ℝ => fun i : I => fun a : Q => x a i) ν ρ :=
    regroup.comp (swap.comp flatten)
  have wrap_rows :
      MeasurePreserving (fun x : I → Q → ℝ => fun i : I => WithLp.toLp 2 (x i))
        ρ (Measure.pi (fun _ : I => stdGaussian E)) :=
    measurePreserving_pi (fun _ : I => Measure.pi (fun _ : Q => σ))
      (fun _ : I => stdGaussian E) (fun _ => ⟨by fun_prop, map_pi_eq_stdGaussian⟩)
  have actual_joint :
      MeasurePreserving (fun ω : Ω => fun i : I => row i ω) μ
        (Measure.pi (fun _ : I => stdGaussian E)) :=
    wrap_rows.comp (transpose.comp unwrap_columns)

  -- Exact joint product law implies full finite-family independence.
  apply (iIndepFun_iff_map_fun_eq_pi_map (fun i => (row_law i).aemeasurable)).2
  calc
    μ.map (fun ω i => row i ω) = Measure.pi (fun _ : I => stdGaussian E) :=
      actual_joint.map_eq
    _ = Measure.pi (fun i : I => μ.map (row i)) := by
      congr 1
      funext i
      exact (row_law i).map_eq.symm

end AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumSourceRowIndependence
'''
with p.open('x') as out:
    out.write(head + seal['producer']['signature'].rstrip() + proof)
