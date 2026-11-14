"""Normal intake only after actual sealed-type/source and distinct topology acceptance."""
from pathlib import Path

old = Path('.astis/huanjian-gc-source-row-independence-20261112/admit_reviewed_packet.generated.py').read_text()
code = old.replace('source-row-independence', 'source-matrix-mean')
code = code.replace('GaussianComplexitySourceRowIndependence', 'GaussianComplexitySourceMatrixMean')
code = code.replace('GaussianComplexityFixedSpectrumSourceRowIndependence', 'GaussianComplexityFixedSpectrumSourceMatrixMean')
code = code.replace('huanjian_gc_20261112_source_row_independence', 'huanjian_gc_20261112_source_matrix_mean')
code = code.replace('88a55849ce9e13a9a04edff6aac13ce32d4370712b1b7a422fba0d570ff0b25e',
                    'b55a1acb837288d580a667903987e5f809610626eb4848c750ff8d3a6c01149b')
code = code.replace('be03871e5c86378721ab9bde584ff06cb5ee3ed43310f70d921a98646d05441e',
                    'fe0a17ec91722e1df8de4201d6bfd9bb12db4bf2b5a65a345b247883156dbcc6')
code = code.replace('.astis/huanjian-gc-source-row-law-20261112/intake-controls.private.json',
                    '.astis/huanjian-gc-source-row-independence-20261112/intake-controls.private.json')
code = code.replace('Actual joint-row/Yi independence proof, source verification, integration and publication remain open.',
                    'Actual original-experiment matrix mean/sum proofs, source verification, integration and publication remain open.')
code = code.replace('Prove full joint independence of actual physical Gaussian rows under the literal source column-product experiment and consume it in measurability and independence of the exact Ex107 truncated matrices.',
                    'Prove integrability and exact first moments of literal Ex107 Yi under the original independent-column experiment; materially consume those results with the canonical cosine-frame identities in integrals of both actual finite sums.')
code = code.replace('Literal standard-Gaussian column-product law, actual physical coordinate rows and exact Ex107 Yi. Coordinate-basis/product-law alignment, full joint independence, actual truncated-matrix measurability and independence under the same mu are internal proof obligations. Marginals alone do not supply independence; no law/independence/measurability certificate input.',
                    'Literal original column-product law, actual physical rows and Ex107 Yi. Actual row marginal transport, scalar retained-radius well-definedness, radial moment applicability, matrix integrability, tensor mean transport, literal cosine frame and finite Bochner exchange are internal proof obligations. No law/moment/integrability/Gram/mean certificate premise; independence is separate and unnecessary for these first moments.')
generated = Path(__file__).resolve().parent / 'admit_reviewed_packet.generated.py'
with generated.open('x') as out:
    out.write(code)
exec(compile(code, str(generated), 'exec'))
