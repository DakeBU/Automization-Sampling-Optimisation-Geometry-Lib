"""Form only prospective exact propositions; no proof search or target proof."""
from pathlib import Path
import json

workspace = Path(__file__).resolve().parent
common = '''    {d q : ℕ} (hq : 2 * q + 1 < d) :
  let D := EuclideanSpace ℝ (Fin d)
  let E := EuclideanSpace ℝ (Fin (q + 1))
  let Ω := Fin (q + 1) → D
  let μ : Measure Ω := Measure.pi (fun _ : Fin (q + 1) => stdGaussian D)
  let r : ℝ := ((q + 1 : ℕ) : ℝ)
  let L : ℝ := 2 * r + 3 * Real.log (1000 * (d : ℝ))
  let a : ℝ :=
    (∫ x : E, Set.indicator {y : E | ‖y‖ ^ 2 ≤ L} (fun y : E => ‖y‖ ^ 2) x
      ∂stdGaussian E) / r
  let θ : Fin d → ℝ := fun i => ((i.val : ℝ) + 1 - 1 / 2) * Real.pi / (d : ℝ)
  let t : Fin d → Fin (q + 1) → ℝ := fun i k =>
    if k.val = 0 then 1 else Real.sqrt 2 * Real.cos ((k.val : ℝ) * θ i)
  let row : Fin d → Ω → E := fun i ω =>
    WithLp.toLp 2 (fun b : Fin (q + 1) => ω b i)
  let Y : Fin d → Ω →
      Matrix (Fin (q + 1) × Fin (q + 1)) (Fin (q + 1) × Fin (q + 1)) ℝ := fun i ω =>
    if ‖row i ω‖ ^ 2 ≤ L then
      (d : ℝ)⁻¹ • Matrix.kronecker
        (Matrix.vecMulVec (WithLp.ofLp (row i ω)) (WithLp.ofLp (row i ω)))
        (Matrix.vecMulVec (t i) (t i))
    else 0
'''
producer = common + '''  (∀ i : Fin d, Integrable (Y i) μ) ∧
    ∀ i : Fin d, (∫ ω, Y i ω ∂μ) =
      (a / (d : ℝ)) • Matrix.kronecker
        (1 : Matrix (Fin (q + 1)) (Fin (q + 1)) ℝ) (Matrix.vecMulVec (t i) (t i))
'''
consumer = common + '''  Integrable (fun ω => ∑ i : Fin d, Y i ω) μ ∧
    Integrable (fun ω => ∑ i : Fin d,
      Real.cos (((2 * q + 1 : ℕ) : ℝ) * θ i) • Y i ω) μ ∧
    (∫ ω, ∑ i : Fin d, Y i ω ∂μ) =
      a • (1 : Matrix (Fin (q + 1) × Fin (q + 1)) (Fin (q + 1) × Fin (q + 1)) ℝ) ∧
    (∫ ω, ∑ i : Fin d, Real.cos (((2 * q + 1 : ℕ) : ℝ) * θ i) • Y i ω ∂μ) = 0
'''
header = '''import AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumSourceRowLaw
import AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumTruncatedRowMoment
import AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumCosineGram
import Mathlib.LinearAlgebra.Matrix.Kronecker
import Mathlib.Analysis.CStarAlgebra.Matrix

noncomputable section
open MeasureTheory ProbabilityTheory
open scoped BigOperators Matrix.Norms.L2Operator
set_option autoImplicit false

'''
text = header + 'def producerProp\n' + producer.replace(' :\n', ' : Prop :=\n', 1)
text += '\ndef consumerProp\n' + consumer.replace(' :\n', ' : Prop :=\n', 1)
text += '\n#print producerProp\n#print consumerProp\n'
for name, value in [('producer-signature.original.txt', producer),
                    ('consumer-signature.original.txt', consumer),
                    ('StatementFormation.lean', text)]:
    with (workspace / name).open('x') as out:
        out.write(value)
with (workspace / 'preseal-exposure.original.json').open('x') as out:
    out.write(json.dumps({
        'formalizer_API_pristine': False,
        'existing_context': [
            'R7 actual independent-column row experiment and matrix consumer',
            'R6 canonical actual-row marginal law',
            'Existing R16 public truncated-row second moment and its canonical one-row private matrix mean',
            'Existing cosine-frame Gram proof and the R5 weighted-frame packet',
            'Pinned complete C.2 source p1-p12 and remaining concentration context',
        ],
        'new_target_proof_search_started': False,
        'new_target_proof_files_exist': False,
        'status': 'Prospective literal Prop formation only; unsealed and unadmitted.',
        'meaning': 'No pristine API chronology is asserted; existing compiled substrate is context and will retain canonical identity.',
    }, ensure_ascii=False, indent=2) + '\n')
print('Created only prospective literal Props and explicit prior-context exposure; no theorem proof.')
