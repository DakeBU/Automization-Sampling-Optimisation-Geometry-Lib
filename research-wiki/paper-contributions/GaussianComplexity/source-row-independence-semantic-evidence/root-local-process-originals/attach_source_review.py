"""Attach only a separately frozen independent source report and its exact overlay."""
from pathlib import Path

old = Path('.astis/huanjian-gc-source-row-law-20261112/attach_source_review.py').read_text()
code = old.replace('source-row-law', 'source-row-independence')
code = code.replace('GaussianComplexitySourceRowLaw', 'GaussianComplexitySourceRowIndependence')
code = code.replace('rl_src_3dd4', 'ri_src_5ab9').replace('row_law_fresh_source_3dd4', 'row_indep_fresh_source_5ab9')
code = code.replace('d0654e9bbed44ab852fc44598560799949d8bd12', '66e0bb9b748d68816a8443d60696656c9340222f')
code = code.replace("assert set(git('diff', 'HEAD', '--name-only').decode().splitlines()) == {str(audit_path)}",
                    "assert not git('diff', 'HEAD', '--name-only')")
code = code.replace('57526c79133302068b87c1de935502e1ea9f64d5cb96aaa8ef7c16ee338fea40',
                    '51f818cce1189763710d937ce87ef07808c728984c5f93f7da4279054b037210')
code = code.replace('f86fb828622e7c5c6e34ae2cb49dc1a6428d94701d36d7bb81a523861d48e419',
                    'd90576df8ae217ca7cb9ce631cdca049780f3a706510afbe2f72a71dd1c03829')
code = code.replace("manifest['originals_count']", "manifest.get('entry_count', manifest.get('originals_count'))")
code = code.replace("manifest.get('entry_count', manifest.get('originals_count'))", "manifest['exact_count']")
code = code.replace("assert source.is_relative_to(phase) and destination.is_relative_to(evidence / 'source-review/ri_src_5ab9')",
                    "assert not source.is_absolute() and '..' not in source.parts and source.resolve().is_relative_to(Path.cwd())\n    assert destination.is_relative_to(evidence / 'source-review/ri_src_5ab9')\n    assert not destination.is_absolute() and '..' not in destination.parts")
code = code.replace("assert overlay['state'] == overlay['source_review']['state'] == 'accepted'",
                    "assert overlay['state'] == 'source-reviewed' and overlay['source_review']['state'] == 'accepted'")
code = code.replace("self_copy = evidence / 'source-review/ri_src_5ab9/portable-originals-manifest.json'",
                    "self_copy = Path(manifest['manifest_destination'])")
code = code.replace('private145-line same-experiment consumer', 'private81-line actual matrix consumer')
code = code.replace('Attach independent Gaussian row-law source decoding and full module review',
                    'Attach independent Gaussian joint-row independence source and module review')
code = code.replace('.astis/semantic-neutral-20261112/rl_sg_6a90/bounded_inventory.json',
                    '.astis/semantic-neutral-20261112/ri_sg_78c2/raw-freeze-v1/inventory.json')
code = code.replace('All145 bounded source atoms retain19NODE and126EXCLUDED dispositions with196 locators. Narrow row marginals do not cover source joint-row independence.',
                    'All83 bounded atoms retain17NODE and66EXCLUDED dispositions. Distinct topology challenge checked all30nodes/33edges and472locator occurrences. Marginal-law source context remains separate canonical credit.')
code = code.replace('Bounded row-measurability/pushforward, actual exponential integrability/mean transport, strict tails, finite union and measurable closed complement are compiled and source-reviewed. Joint-row independence, arbitrary extended-ambient transfer and matrix-expectation adapters remain open.',
                    'All10 bounded coordinate-product/regrouping/full-row-independence and actual-Y/measurability/image-independence ports are compiled and independently source-reviewed. Arbitrary ambient transfer, matrix-expectation adapters, centered variance/concentration and main bounds remain open.')
start = code.index("cell['proof_digestion'] = ")
stop = code.index('cell_path.write_bytes(dump(cell))', start)
code = code[:start] + r'''
cell['proof_digestion'] = {
    'existing_substrate': [*cell['parents'], 'map_pi_eq_stdGaussian', 'measurePreserving_pi',
                           'Measure.infinitePi_map_curry_symm', 'measurePreserving_piCongrLeft',
                           'Measure.infinitePi_map_curry', 'iIndepFun_iff_map_fun_eq_pi_map', 'iIndepFun.comp'],
    'bookkeeping': ['Full physical-coordinate Gaussian product identification', 'Flatten/swap/regroup of the same finite scalar array',
                    'Euclidean row wrapping and exact joint product transport', 'Actual finite-entry closed-cutoff polynomial measurability and composition'],
    'new_reusable': [],
    'new_topology': 'Existing canonical row law plus full joint coordinate regrouping yields actual row independence, materially consumed by the exact source truncated-matrix measurable images.',
}
cell['purification'] = {
    'status': 'pending', 'dead_code_audit': 'Strict focused probe checks both handwritten roots reachable, with no generated owned helper; full native transitive closure review pending.',
    'duplicate_semantics_audit': 'Reuse the same canonical row-law node and Mathlib product/independence declarations. No second marginal-law proof or public matrix wrapper.',
    'canonicalization': 'Source-specific full-row independence with actual Ex107 matrix-independence consumer.',
    'compressed_spine_delta': 'Full Gaussian coordinate product, finite regrouping and joint-law independence, then separate measurable nonlinear images.',
    'reader_default_view': 'Compact independence conclusions with six source-ordered formula/Lean folds and full81-line private source export.',
}
''' + code[stop:]
generated = Path(__file__).resolve().parent / 'attach_source_review.generated.py'
with generated.open('x') as out:
    out.write(code)
exec(compile(code, str(generated), 'exec'))
