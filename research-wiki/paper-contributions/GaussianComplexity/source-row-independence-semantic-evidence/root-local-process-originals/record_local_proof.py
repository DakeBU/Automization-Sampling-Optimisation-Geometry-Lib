"""Append one normal local proof event after accepted exact independent source review."""
from pathlib import Path

old = Path('.astis/huanjian-gc-source-row-law-20261112/record_local_proof.py').read_text()
code = old.replace('source-row-law', 'source-row-independence')
code = code.replace('GaussianComplexitySourceRowLaw', 'GaussianComplexitySourceRowIndependence')
code = code.replace('huanjian_gc_20261112_source_row_law', 'huanjian_gc_20261112_source_row_independence')
code = code.replace('d0654e9bbed44ab852fc44598560799949d8bd12', '66e0bb9b748d68816a8443d60696656c9340222f')
code = code.replace("all(item['identity_unchanged'] for item in cell['conceptual_mirror_audit']['existing_validated_mirrors'])",
                    "all(item['identity_and_status_preserved'] for item in cell['conceptual_mirror_audit']['existing_validated_mirrors'])")
code = code.replace("'generated_reachable_internal': 2", "'generated_reachable_internal': 0")
code = code.replace('All four owned declarations are closed and reachable with standard axioms only.',
                    'Both owned declarations are closed and reachable with standard axioms only; no generated owned helper.')
code = code.replace("'producer_initial_failures': 1, 'consumer_initial_build_failures': 1,",
                    "'producer_initial_failures': 0, 'consumer_initial_build_failures': 0,")
code = code.replace("'initial_strict_kernel_failure': 'Unreachable generated not_le simp cache; diagnostic retained.',",
                    "'initial_strict_kernel_failure': None,")
code = code.replace("'recovery': 'Remove redundant explicit not_le, unchanged sealed signatures and strict probe; independent v2 code review retained.',",
                    "'recovery': 'No actual target implementation or strict-probe failure. Preseal formation history and failed exploratory unqualified API lookup are retained separately.',")
code = code.replace('Recorded implementation failures diagnosed; unchanged sealed types compiled with the original strict kernel probe. All original failed sources/diagnostics preserved.',
                    'Preseal formation and exploratory namespace lookup diagnoses retained. Both unchanged sealed actual targets compiled on their first implementation attempt; the unchanged strict kernel probe passed. No discarded mathematical fragment.')
code = code.replace("cell['learning_contract']['failure_class'] = 'IMPLEMENTATION_FAILED'",
                    "cell['learning_contract']['failure_class'] = 'API_BLOCKED'")
generated = Path(__file__).resolve().parent / 'record_local_proof.generated.py'
with generated.open('x') as out:
    out.write(code)
exec(compile(code, str(generated), 'exec'))
