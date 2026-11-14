"""Admit the single shared bridge only after its independent background topology review."""
from pathlib import Path

code = Path('.astis/huanjian-gc-source-matrix-mean-20261112/admit_reviewed_packet.generated.py').read_text()
code = code.replace('source-matrix-mean', 'real-matrix-positive-integral')
code = code.replace('huanjian-gc-real-matrix-positive-integral', 'huanjian-real-matrix-positive-integral')
code = code.replace('GaussianComplexityFixedSpectrumSourceMatrixMean', 'RealMatrixPositiveIntegral')
code = code.replace('GaussianComplexitySourceMatrixMean', 'RealMatrixPositiveIntegral')
code = code.replace('huanjian_gc_20261112_source_matrix_mean', 'huanjian_20261112_real_matrix_positive_integral')
code = code.replace("paper = Path('research-wiki/paper-contributions/GaussianComplexity')", "paper = Path('research-wiki/technical-lemmas')")
code = code.replace('ASTIS-SW-GAUSSIAN-COMPLEXITY-real-matrix-positive-integral', 'ASTIS-SHARED-REAL-MATRIX-POSITIVE-INTEGRAL')
code = code.replace('b55a1acb837288d580a667903987e5f809610626eb4848c750ff8d3a6c01149b', 'a5179ed392ef8e55ab470a3a98ebd542e35301f51472e9cdd7bc168a88bafa26')
code = code.replace('fe0a17ec91722e1df8de4201d6bfd9bb12db4bf2b5a65a345b247883156dbcc6', '72901ad14e2a05263f01dd130e53530fc3ee37979d2ea67a316e0218f34a37c9')
code = code.replace("('producer', 'actual_private_consumer')", "('producer', 'actual_consumer')")
code = code.replace("assert not git('diff', 'HEAD', '--name-only') and not git('diff', '--cached', '--name-only')", "assert git('diff', 'HEAD', '--name-only').decode().splitlines() == baseline['preexisting_tracked_diff_names']\nassert not git('diff', '--cached', '--name-only')")
code = code.replace('.astis/huanjian-gc-source-row-independence-20261112/intake-controls.private.json', '.astis/huanjian-gc-source-matrix-variance-20261112/intake-controls.private.json')
code = code.replace('Actual original-experiment matrix mean/sum proofs, source verification, integration and publication remain open.', 'The shared arbitrary-f positivity proof and actual unchanged Gaussian squared-moment consumer remain unproved. No generic hypothesis may be added to the source target; normal source verification, integration and publication remain open.')
code = code.replace('Prove integrability and exact first moments of literal Ex107 Yi under the original independent-column experiment; materially consume those results with the canonical cosine-frame identities in integrals of both actual finite sums.', 'Prove one shared finite-real-matrix integral positivity interface with internally proved cone applicability, and materially consume it in the unchanged actual original-experiment Gaussian squared-moment PSD bound. Preserve full source signatures and prior active R9 intake without replay.')
code = code.replace('Literal original column-product law, actual physical rows and Ex107 Yi. Actual row marginal transport, scalar retained-radius well-definedness, radial moment applicability, matrix integrability, tensor mean transport, literal cosine frame and finite Bochner exchange are internal proof obligations. No law/moment/integrability/Gram/mean certificate premise; independence is separate and unnecessary for these first moments.', 'Explicit ASTIS-authored arbitrary-f probability/integrability/AE-full-PSD contract, with empty finite indices allowed and actual L2Operator Bochner integral. Closed/convex PSD cone and integral applicability are internal. Its actual Gaussian source consumer is the unchanged sealed R9 uncentered target; it must prove each generic application premise internally. This is not a printed general primary-paper theorem or a source repair.')
generated = Path(__file__).resolve().parent / 'admit_reviewed_packet.generated.py'
with generated.open('x') as out:
    out.write(code)
exec(compile(code, str(generated), 'exec'))
