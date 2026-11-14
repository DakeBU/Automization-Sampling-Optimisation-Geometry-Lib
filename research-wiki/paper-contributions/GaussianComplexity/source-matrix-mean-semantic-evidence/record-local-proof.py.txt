"""Append one local proof event only after exact independent source acceptance."""
from pathlib import Path

old = Path('.astis/huanjian-gc-source-row-independence-20261112/record_local_proof.generated.py').read_text()
code = old.replace('source-row-independence', 'source-matrix-mean')
code = code.replace('GaussianComplexitySourceRowIndependence', 'GaussianComplexitySourceMatrixMean')
code = code.replace('huanjian_gc_20261112_source_row_independence', 'huanjian_gc_20261112_source_matrix_mean')
code = code.replace('66e0bb9b748d68816a8443d60696656c9340222f', '5fb1440f771bdae77ad31f27b2275447fe3e89e5')
code = code.replace("'generated_reachable_internal': 0", "'generated_reachable_internal': 1")
code = code.replace('Both owned declarations are closed and reachable with standard axioms only; no generated owned helper.',
                    'Two handwritten roots and one emitted internal helper are all closed and reachable with standard axioms only.')
code = code.replace("'consumer_initial_build_failures': 0", "'consumer_initial_build_failures': 2")
code = code.replace('No actual target implementation or strict-probe failure. Preseal formation history and failed exploratory unqualified API lookup are retained separately.',
                    'Actual consumer proof-local Matrix annotation and implicit Finset.smul_sum argument failures diagnosed; final v3 and the unchanged strict probe passed. Producer passed first attempt; exact sealed types unchanged.')
code = code.replace("cell['learning_contract']['failure_class'] = 'API_BLOCKED'",
                    "cell['learning_contract']['failure_class'] = 'IMPLEMENTATION_FAILED'")
code = code.replace('Preseal formation and exploratory namespace lookup diagnoses retained. Both unchanged sealed actual targets compiled on their first implementation attempt; the unchanged strict kernel probe passed. No discarded mathematical fragment.',
                    'Control-plane reservation label and exploratory API lookup failures retained. Producer compiled first attempt; two consumer elaboration/API errors fixed without changing the exact statement or mathematical route. Final v3 and original strict kernel probe passed. All failed source versions/streams retained; no discarded mathematical fragment.')
generated = Path(__file__).resolve().parent / 'record_local_proof.generated.py'
with generated.open('x') as out:
    out.write(code)
exec(compile(code, str(generated), 'exec'))
