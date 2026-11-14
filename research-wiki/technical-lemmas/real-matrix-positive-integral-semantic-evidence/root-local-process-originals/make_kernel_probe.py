"""Check both immutable literal types and actual canonical calls in the Lean kernel."""
from pathlib import Path
import json

workspace = Path(__file__).resolve().parent
seal = json.loads((workspace / 'statement-seal-v1.json').read_bytes())
old = Path('.astis/huanjian-gc-source-matrix-mean-20261112/SourceMatrixMeanKernelProbe.lean').read_text()
core = 'run_cmd do' + old.split('run_cmd do', 1)[1]
core = core.replace('AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumSourceMatrixMean.actual_source_truncated_matrix_means', seal['producer']['name'])
core = core.replace('actual_source_truncated_sum_means', 'actual_source_truncated_matrix_second_moments')
start, stop = core.index('  let isOwned := '), core.index('\n  let owned := ')
is_owned = '''  let isOwned := fun (n : Name) =>
    let s := n.toString
    s.startsWith "AutoSamplingTheory.TechnicalLemmas.Probability.RealMatrixPositiveIntegral." ||
    s.startsWith "_private.AutoSamplingTheory.TechnicalLemmas.Probability.RealMatrixPositiveIntegral." ||
    s.startsWith "AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumSourceMatrixVariance." ||
    s.startsWith "_private.AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumSourceMatrixVariance."'''
core = core[:start] + is_owned + core[stop:]
start, stop = core.index('    let required := '), core.index('\n    unless publicParents.length')
bt = chr(96)
parents = [
    'AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumSourceRowLaw.actual_source_row_marginal_law',
    'AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumRadialFourthMoment.actual_radial_fourth_moment_matrix',
    'AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumWeightedFrameBound.actual_weighted_cosine_coefficient_bound',
]
required = '    let required := if n == target then [] else [target, ' + ', '.join(bt + n for n in parents) + ']'
core = core[:start] + required + core[stop:]
core = core.replace('ExpectedPrivate', 'ExpectedConsumer').replace('ActualPrivateSealedTypeCheck', 'ActualConsumerSealedTypeCheck')

def literal(key):
    binders, body = seal[key]['signature'].split(' :\n', 1)
    return '∀ ' + binders + ',\n' + body

code = '''import Tests.RealMatrixPositiveIntegral
open MeasureTheory ProbabilityTheory Lean
open scoped BigOperators Matrix.Norms.L2Operator
set_option autoImplicit false

'''
code += 'def ExpectedProducer : Prop := ' + literal('producer')
code += '\ndef ExpectedConsumer : Prop := ' + literal('actual_consumer') + '\n' + core
code += '''
-- A real empty-index instantiation: no Nonempty matrix-index hypothesis.
example {Ω : Type*} [MeasurableSpace Ω] {μ : Measure Ω} [IsProbabilityMeasure μ]
    (f : Ω → Matrix (Fin 0) (Fin 0) ℝ) (hf : Integrable f μ)
    (hpos : ∀ᵐ ω ∂μ, Matrix.PosSemidef (f ω)) :
    Matrix.PosSemidef (∫ ω, f ω ∂μ) :=
  AutoSamplingTheory.TechnicalLemmas.Probability.RealMatrixPositiveIntegral.integral_posSemidef f hf hpos

#check (AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumSourceMatrixVariance.actual_source_truncated_matrix_second_moments (d := 2) (q := 0) (by decide))
'''
path = workspace / 'SharedPositiveIntegralKernelProbe.lean'
with path.open('x') as out:
    out.write(code)
print(str(path))
