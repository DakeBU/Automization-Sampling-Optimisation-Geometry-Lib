"""Only form prospective actual second-moment and variance propositions."""
from pathlib import Path
import json

workspace = Path(__file__).resolve().parent
previous = Path('.astis/huanjian-gc-source-matrix-mean-20261112/producer-signature.original.txt').read_text()
common = previous.split('  (∀ i : Fin d, Integrable (Y i) μ)', 1)[0]
scalar_a = '''  let a : ℝ :=
    (∫ x : E, Set.indicator {y : E | ‖y‖ ^ 2 ≤ L} (fun y : E => ‖y‖ ^ 2) x
      ∂stdGaussian E) / r
'''
assert common.count(scalar_a) == 1
common = common.replace(scalar_a, '')
matrix = 'Matrix (Fin (q + 1) × Fin (q + 1)) (Fin (q + 1) × Fin (q + 1)) ℝ'
producer = common + '''  let C : ℝ := 2 * r * (r + 2) / (d : ℝ)
  (∀ i : Fin d, Integrable (fun ω => Y i ω * Y i ω) μ) ∧
    Matrix.PosSemidef
      (C • (1 : ''' + matrix + ''') -
        ∑ i : Fin d, ∫ ω, Y i ω * Y i ω ∂μ)
'''
consumer = common + '''  let mean : Fin d → ''' + matrix + ''' :=
    fun i => ∫ ω, Y i ω ∂μ
  let Z : Fin d → Ω → ''' + matrix + ''' :=
    fun i ω => Y i ω - mean i
  let w : Fin d → ℝ := fun i => Real.cos (((2 * q + 1 : ℕ) : ℝ) * θ i)
  let C : ℝ := 2 * r * (r + 2) / (d : ℝ)
  (∀ i : Fin d, Integrable (fun ω => Z i ω * Z i ω) μ) ∧
    (∀ i : Fin d, Integrable (fun ω => (w i • Z i ω) * (w i • Z i ω)) μ) ∧
    ‖∑ i : Fin d, ∫ ω, Z i ω * Z i ω ∂μ‖ ≤ C ∧
    ‖∑ i : Fin d, ∫ ω, (w i • Z i ω) * (w i • Z i ω) ∂μ‖ ≤ C
'''
header = '''import AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumWeightedFrameBound
import AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumRadialFourthMoment
import AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumSourceRowLaw
import AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumSourceMatrixMean
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
        'known_context': [
            'Prior R4 full radial-fourth matrix moment and R5 weighted-frame/old private canonical-row squared-moment aggregate code and proof APIs are known.',
            'Prior R6 actual-row law, R7 independence and current R8 actual first-moment/sum code, proof APIs and kernel results are known.',
            'Pinned C.2 source first moments, squared moments, centered identity and cosine weighting have already been read in the wider task.',
            'Source/consumer selection distinguishes PSD domination from the actual variance operator norm; required positivity/integrability/Bochner and norm bridges must remain internal, not new target premises.',
        ],
        'source_locator_correction': 'Initial raw-reading assignment called the centered variance passage p15. Actual pinned source places Z definition in p13 and Ex113/114 plus centered/cos² variance comparisons in p14; p15 is Bernstein and remains outside this prospective packet.',
        'new_target_library_API_retrieval_or_implementation_started': False,
        'new_target_proof_files_exist': False,
        'status': 'Unsealed/unadmitted prospective literal formation only. No theorem proof or pristine chronology claimed.',
    }, ensure_ascii=False, indent=2) + '\n')
print('Created only exact prospective propositions and honest known-context exposure.')
