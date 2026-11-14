"""Apply both frozen literal Props in the real kernel and inspect every owned body."""
from pathlib import Path
import json

w = Path(__file__).resolve().parent
seal = json.loads((w / 'statement-seal-v1.json').read_bytes())
old = Path('.astis/huanjian-gc-source-row-law-20261112/SourceRowLawKernelProbe.lean').read_text()
core = 'run_cmd do' + old.split('run_cmd do', 1)[1]
core = core.replace('FixedSpectrumSourceRowLaw', 'FixedSpectrumSourceRowIndependence')
core = core.replace('actual_source_row_marginal_law', 'actual_source_rows_independent')
core = core.replace('actual_original_all_good_cutoff_probability',
                    'actual_truncated_matrices_measurable_and_independent')
parent = chr(96) + 'AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumSourceRowLaw.actual_source_row_marginal_law'
old_required = 'if n == target then [] else [target, ' + chr(96) + 'AutoSamplingTheory.TechnicalLemmas.Probability.StdGaussianRadialExponential.integrable_exp_norm_sq_div_three_and_integral_stdGaussian]'
assert old_required in core
core = core.replace(old_required, 'if n == target then [' + parent + '] else [target, ' + parent + ']')


def literal(key):
    binders, body = seal[key]['signature'].split(' :\n', 1)
    return '∀ ' + binders + ',\n' + body


head = '''import Tests.GaussianComplexityFixedSpectrumSourceRowIndependence
open MeasureTheory ProbabilityTheory Lean
set_option autoImplicit false

'''
code = head + 'def ExpectedProducer : Prop := ' + literal('producer')
code += '\ndef ExpectedPrivate : Prop := ' + literal('actual_private_consumer') + '\n' + core
path = w / 'SourceRowIndependenceKernelProbe.lean'
with path.open('x') as out:
    out.write(code)
print(str(path))
