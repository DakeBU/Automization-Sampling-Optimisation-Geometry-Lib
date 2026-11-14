"""Carry the original local proof append and receipt without replay."""
from pathlib import Path

old = Path('.astis/huanjian-gc-source-row-independence-20261112/carry_local_proof.generated.py').read_text()
code = old.replace('source-row-independence', 'source-matrix-mean')
code = code.replace('GaussianComplexitySourceRowIndependence', 'GaussianComplexitySourceMatrixMean')
code = code.replace('huanjian_gc_20261112_source_row_independence', 'huanjian_gc_20261112_source_matrix_mean')
code = code.replace('66e0bb9b748d68816a8443d60696656c9340222f', '5fb1440f771bdae77ad31f27b2275447fe3e89e5')
code = code.replace('Carry original Gaussian row-independence local proof event', 'Carry original actual Gaussian matrix-mean local proof event')
generated = Path(__file__).resolve().parent / 'carry_local_proof.generated.py'
with generated.open('x') as out:
    out.write(code)
exec(compile(code, str(generated), 'exec'))
