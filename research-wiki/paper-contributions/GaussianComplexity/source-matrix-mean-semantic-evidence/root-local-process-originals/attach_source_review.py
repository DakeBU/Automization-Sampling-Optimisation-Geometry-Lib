"""Attach exact independent source originals only after their final freeze exists."""
from pathlib import Path

old = Path('.astis/huanjian-gc-source-row-independence-20261112/attach_source_review.generated.py').read_text()
code = old.replace('source-row-independence', 'source-matrix-mean')
code = code.replace('GaussianComplexitySourceRowIndependence', 'GaussianComplexitySourceMatrixMean')
code = code.replace('ri_src_5ab9', 'mm_src_8c31').replace('row_indep_fresh_source_5ab9', 'mm_fresh_source_8c31')
code = code.replace('66e0bb9b748d68816a8443d60696656c9340222f', '5fb1440f771bdae77ad31f27b2275447fe3e89e5')
code = code.replace('51f818cce1189763710d937ce87ef07808c728984c5f93f7da4279054b037210',
                    '0d8f3df6fc7d9e27bfb4c31c24f5cd87a20fd4d35f3adc365c59e8e40eb9c226')
code = code.replace('d90576df8ae217ca7cb9ce631cdca049780f3a706510afbe2f72a71dd1c03829',
                    'c0e0e354793ad6c2901a23c28c58d1bae8a63bf682d8645ce6e555d2d96df834')
code = code.replace('private81-line actual matrix consumer', 'private158-line actual sum-integral consumer')
code = code.replace('.astis/semantic-neutral-20261112/ri_sg_78c2/raw-freeze-v1/inventory.json',
                    '.astis/semantic-neutral-20261112/mm_sg_61c4/raw-freeze-v1/atomic-inventory.json')
code = code.replace('All83 bounded atoms retain17NODE and66EXCLUDED dispositions. Distinct topology challenge checked all30nodes/33edges and472locator occurrences. Marginal-law source context remains separate canonical credit.',
                    'All79 bounded atoms retain44NODE and35EXCLUDED dispositions. Distinct topology challenge checked62nodes/94edges and463locator occurrences, including both formal roots and separate source correspondence endpoints. Canonical row/moment/frame identities retain their existing credit.')
code = code.replace('All10 bounded coordinate-product/regrouping/full-row-independence and actual-Y/measurability/image-independence ports are compiled and independently source-reviewed. Arbitrary ambient transfer, matrix-expectation adapters, centered variance/concentration and main bounds remain open.',
                    'Actual row-law and retained scalar/matrix moment applicability, actual matrix integrability, selected CLM expectation route, literal frame and actual finite integral exchange are compiled and independently source-reviewed. The entrywise OR route is unselected, not an extra requirement. Arbitrary ambient transfer, public aggregate canonicalization, centered variance/concentration and main bounds remain open.')
start = code.index("cell['proof_digestion'] = ")
stop = code.index('cell_path.write_bytes(dump(cell))', start)
code = code[:start] + '''cell['proof_digestion'] = {
    'existing_substrate': [*cell['parents'], 'MeasurePreserving.integrable_comp_of_integrable', 'integral_map',
                           'ContinuousLinearMap.integrable_comp', 'ContinuousLinearMap.integral_comp_comm',
                           'Matrix.kroneckerBilinear', 'Matrix.one_kronecker_one', 'integrable_finsetSum', 'integral_finsetSum', 'integral_smul'],
    'bookkeeping': ['Literal same-experiment row pushforward and noninjective moment transport',
                    'Fixed Gaussian-first tensor CLM and exact closed-cutoff image',
                    'Exact half-grid/frame application and paired-identity normalization',
                    'Actual finite-sum integrability and Bochner/scalar exchange'],
    'new_reusable': [],
    'new_topology': 'Same canonical row-law and truncated moment yield actual Yi integrability/means, materially consumed with the same cosine-frame node in both actual finite-sum expectation identities.',
}
cell['purification'] = {
    'status': 'pending', 'dead_code_audit': 'Strict exact probe checks2 handwritten roots and1 emitted internal helper closed/reachable with standard axioms. Independent full fresh native closure remains separate.',
    'duplicate_semantics_audit': 'One canonical existing row-law, radial moment and frame node each reused. The old private canonical-row matrix application remains immutable history without duplicate public credit.',
    'canonicalization': 'Source-specific actual original-experiment matrix means with a real two-sum Bochner expectation consumer.',
    'compressed_spine_delta': 'Exact row pushforward and retained moment -> fixed tensor CLM -> actual Yi means -> source cosine tensor sums -> actual finite-sum integrals.',
    'reader_default_view': 'Compact individual means with six source-ordered formula/Lean folds and the complete158-line private source at L17.',
}
''' + code[stop:]
code = code.replace('Attach independent Gaussian joint-row independence source and module review',
                    'Attach independent actual Gaussian matrix-mean source and reader review')
generated = Path(__file__).resolve().parent / 'attach_source_review.generated.py'
with generated.open('x') as out:
    out.write(code)
exec(compile(code, str(generated), 'exec'))
