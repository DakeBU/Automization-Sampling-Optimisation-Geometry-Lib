"""Normal intake only after the actual independent sealed-type/topology readback."""
from pathlib import Path

code = Path('.astis/huanjian-gc-source-matrix-mean-20261112/admit_reviewed_packet.generated.py').read_text()
code = code.replace('source-matrix-mean', 'source-matrix-variance')
code = code.replace('GaussianComplexitySourceMatrixMean', 'GaussianComplexitySourceMatrixVariance')
code = code.replace('GaussianComplexityFixedSpectrumSourceMatrixMean', 'GaussianComplexityFixedSpectrumSourceMatrixVariance')
code = code.replace('huanjian_gc_20261112_source_matrix_mean', 'huanjian_gc_20261112_source_matrix_variance')
code = code.replace('b55a1acb837288d580a667903987e5f809610626eb4848c750ff8d3a6c01149b', '5f905cafe6035238cebdedd4f841e87b703e741b4c8aa204471d89e4c07e8a14')
code = code.replace('fe0a17ec91722e1df8de4201d6bfd9bb12db4bf2b5a65a345b247883156dbcc6', '14b1975d5ebc7ff8f368d6364df573e1a537d7c0c5f252827e2c8d031387b769')
code = code.replace('.astis/huanjian-gc-source-row-independence-20261112/intake-controls.private.json', '.astis/huanjian-gc-source-matrix-mean-20261112/intake-controls.private.json')
code = code.replace('Actual original-experiment matrix mean/sum proofs, source verification, integration and publication remain open.', 'Actual original-experiment squared-moment and centered-variance proofs, source verification, integration and publication remain open.')
code = code.replace('Prove integrability and exact first moments of literal Ex107 Yi under the original independent-column experiment; materially consume those results with the canonical cosine-frame identities in integrals of both actual finite sums.', 'Prove squared integrability and the uncentered PSD bound for literal Ex107 Yi under the original independent-column experiment; materially consume those results in squared integrability and genuine L2 operator-norm bounds for both actual centered and cosine-weighted centered variance sums.')
code = code.replace('Literal original column-product law, actual physical rows and Ex107 Yi. Actual row marginal transport, scalar retained-radius well-definedness, radial moment applicability, matrix integrability, tensor mean transport, literal cosine frame and finite Bochner exchange are internal proof obligations. No law/moment/integrability/Gram/mean certificate premise; independence is separate and unnecessary for these first moments.', 'Literal original product-Gaussian physical rows and closed-cutoff Ex107 Yi, with actual mean and Z on that same mu. Row-law and radial-fourth applicability, squared integrability, tensor/rank-one algebra, PSD integral and weighted-frame assembly, actual first integrability, noncommutative centering, Hermitian/PSD and true operator-norm conversion are internal proof obligations. No law/moment/mean/Gram/variance/PSD/norm certificate premise; q0 retained. Joint independence and Bernstein p15 are outside this packet.')
generated = Path(__file__).resolve().parent / 'admit_reviewed_packet.generated.py'
with generated.open('x') as out:
    out.write(code)
exec(compile(code, str(generated), 'exec'))
