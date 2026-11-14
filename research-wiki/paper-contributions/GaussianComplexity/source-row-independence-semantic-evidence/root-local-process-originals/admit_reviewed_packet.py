"""Prepare the normal source-backed intake; execution requires independent readback."""
from pathlib import Path

old = Path('.astis/huanjian-gc-source-row-law-20261112/admit_reviewed_packet.py').read_text()
code = old.replace('source-row-law', 'source-row-independence')
code = code.replace('GaussianComplexitySourceRowLaw', 'GaussianComplexitySourceRowIndependence')
code = code.replace('GaussianComplexityFixedSpectrumSourceRowLaw', 'GaussianComplexityFixedSpectrumSourceRowIndependence')
code = code.replace('huanjian_gc_20261112_source_row_law', 'huanjian_gc_20261112_source_row_independence')
code = code.replace('f9476ec7454a0927d3a1068226ad635b464d9b5d631f4992421d4b3b39b70ec3',
                    '88a55849ce9e13a9a04edff6aac13ce32d4370712b1b7a422fba0d570ff0b25e')
code = code.replace('f6f0aa6b71a13c7fbcfa545fceab890c12252bfd5530051d18a0af0baa13bbe8',
                    'be03871e5c86378721ab9bde584ff06cb5ee3ed43310f70d921a98646d05441e')
code = code.replace('remaining_mathematical_source_topology_gaps', 'remaining_statement_or_source_topology_blockers')
code = code.replace('.astis/huanjian-gc-weighted-cosine-frame-20261112/intake-controls.private.json',
                    '.astis/huanjian-gc-source-row-law-20261112/intake-controls.private.json')
code = code.replace('Source/type/topology acceptance only. New mathematical proof, original-family law transport, source verification, integration and publication remain open.',
                    'Independent source/type/topology acceptance only; explicit internal/applicability ports remain unproved. Actual joint-row/Yi independence proof, source verification, integration and publication remain open.')
code = code.replace('Prove actual row marginal-law transport from the source column-product experiment and consume it with the canonical exponential moment in the original global good cutoff event.',
                    'Prove full joint independence of actual physical Gaussian rows under the literal source column-product experiment and consume it in measurability and independence of the exact Ex107 truncated matrices.')
code = code.replace('Literal standard-Gaussian independent-column product law, coordinate row maps, closed cutoff and global good event. Row measurability/pushforward, exponential moment applicability/transport, strict tails, finite union and measurable complement arithmetic are internal proof obligations.',
                    'Literal standard-Gaussian column-product law, actual physical coordinate rows and exact Ex107 Yi. Coordinate-basis/product-law alignment, full joint independence, actual truncated-matrix measurability and independence under the same mu are internal proof obligations. Marginals alone do not supply independence; no law/independence/measurability certificate input.')
generated = Path(__file__).resolve().parent / 'admit_reviewed_packet.generated.py'
with generated.open('x') as out:
    out.write(code)
exec(compile(code, str(generated), 'exec'))
