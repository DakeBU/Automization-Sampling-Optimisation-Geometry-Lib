"""Carry original PLOCAL bytes and their actual receipt; never replay the API."""
from pathlib import Path

old = Path('.astis/huanjian-gc-source-row-law-20261112/carry_local_proof.py').read_text()
code = old.replace('source-row-law', 'source-row-independence')
code = code.replace('GaussianComplexitySourceRowLaw', 'GaussianComplexitySourceRowIndependence')
code = code.replace('huanjian_gc_20261112_source_row_law', 'huanjian_gc_20261112_source_row_independence')
code = code.replace('d0654e9bbed44ab852fc44598560799949d8bd12', '66e0bb9b748d68816a8443d60696656c9340222f')
code = code.replace('Carry original Gaussian row-law local proof event', 'Carry original Gaussian row-independence local proof event')
generated = Path(__file__).resolve().parent / 'carry_local_proof.generated.py'
with generated.open('x') as out:
    out.write(code)
exec(compile(code, str(generated), 'exec'))
