"""Apply the immutable literal matrix-mean propositions in the real Lean kernel."""
from pathlib import Path
import json

workspace = Path(__file__).resolve().parent
seal = json.loads((workspace / 'statement-seal-v1.json').read_bytes())
old = Path('.astis/huanjian-gc-source-row-independence-20261112/SourceRowIndependenceKernelProbe.lean').read_text()
core = 'run_cmd do' + old.split('run_cmd do', 1)[1]
core = core.replace('FixedSpectrumSourceRowIndependence', 'FixedSpectrumSourceMatrixMean')
core = core.replace('actual_source_rows_independent', 'actual_source_truncated_matrix_means')
core = core.replace('actual_truncated_matrices_measurable_and_independent', 'actual_source_truncated_sum_means')
start = core.index('    let required := ')
stop = core.index('\n    unless publicParents.length', start)
bt = chr(96)
required = ('    let required := if n == target then [' + bt +
    'AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumSourceRowLaw.actual_source_row_marginal_law, ' + bt +
    'AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumTruncatedRowMoment.actual_truncated_row_second_moment] else [target, ' + bt +
    'AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumCosineGram.actual_cosine_frame_gram]')
core = core[:start] + required + core[stop:]

def literal(key):
    binders, body = seal[key]['signature'].split(' :\n', 1)
    return '∀ ' + binders + ',\n' + body

code = '''import Tests.GaussianComplexityFixedSpectrumSourceMatrixMean
open MeasureTheory ProbabilityTheory Lean
open scoped BigOperators Matrix.Norms.L2Operator
set_option autoImplicit false

'''
code += 'def ExpectedProducer : Prop := ' + literal('producer')
code += '\ndef ExpectedPrivate : Prop := ' + literal('actual_private_consumer') + '\n' + core
path = workspace / 'SourceMatrixMeanKernelProbe.lean'
with path.open('x') as out:
    out.write(code)
print(str(path))
