"""Bind the independently reviewed authored-background graph and full existing consumer graph."""
from pathlib import Path
import hashlib
import json

workspace = Path(__file__).resolve().parent.relative_to(Path.cwd())
sha = lambda raw: hashlib.sha256(raw).hexdigest()
originals = {}

def verify(path, digest=None, length=None, parse=True):
    path = Path(path)
    raw = path.read_bytes()
    assert not path.is_symlink()
    assert digest is None or sha(raw) == digest, str(path)
    assert length is None or len(raw) == length, str(path)
    originals[str(path)] = {'path': str(path), 'bytes': len(raw), 'sha256': sha(raw)}
    return json.loads(raw) if parse else raw

sg = Path('.astis/semantic-neutral-20261112/mp_sg_52ad')
for name, digest in [
    ('type-freeze-v1/freeze-manifest.json', '4b0bab616098bfd3af5c4cf825b9eda8ca3e5033deaf9b04a8b500b2a24b05ec'),
    ('background-graph-freeze-v1/freeze-manifest.json', '690b88567793ee26bcc04df298edcf8794e557c870f998551b73f9b363056126'),
]:
    path = sg / name
    manifest = verify(path, digest)
    for item in manifest['files']:
        verify(path.parent / item['path'], item['sha256'], item['bytes'], parse=False)
audit = verify(sg / 'type-freeze-v1/type-audit.json', '33ba7adfa422cda6da33cf7c8714f4846791cdae4d05940658ec0e72832d6122')
graph = verify(sg / 'background-graph-freeze-v1/background-source-graph.json', '46178eb3e91bade03e2d419ff44423801e1a408d9f126fa2ebfa32342e47cb47')
coverage = verify(sg / 'background-graph-freeze-v1/coverage.json', 'e4a99f31dd47a2cae21a614e45859a5d5216428b49a2081e12520e186e0db10c')
ports = verify(sg / 'background-graph-freeze-v1/internal-ports-and-source-gaps.json', '209f05c0f67342b5ee141c7795715ab37a17fc29d15b6e177b8c853fcc65941f')
assert audit['verdict'] == 'NO_GENUINE_GENERIC_CONTRACT_OR_CONSUMER_SCOPE_ISSUE_FOUND'
assert audit['EXCESS_generic_binders'] == audit['Gaussian_binder_additions'] == audit['genuine_target_issues'] == audit['genuine_source_gaps'] == []
assert graph['compiled_parents'] == graph['genuine_source_gaps'] == [] and not graph['new_shared_proof_seen']
assert coverage['inventory_counts'] == {'EXCLUDED': 37, 'NODE': 31, 'items': 68}
assert len(graph['nodes']) == 50 and len(graph['edges']) == 68 and len(graph['hyperedges']) == 1
assert len(ports['ports']) == 13 and ports['genuine_source_gaps'] == []
assert all(not p['genuine_SOURCE_GAP'] and p['compiled_parents'] == [] for p in ports['ports'])
# The background graph covers the interface, not the whole concrete Gaussian
# calculation. Carry the already separately reviewed full source consumer graph.
r9_path = Path('.astis/huanjian-gc-source-matrix-variance-20261112/reviewed-preproof-inputs.json')
r9 = verify(r9_path, 'daad00de7577d83e1d489b762bd599b864d561c14dfdd3185ae29c5eb7c85de1')
assert r9['source_type_verdict'] == r9['independent_topology_verdict'] == 'accepted'
for item in r9['independent_originals']:
    verify(item['path'], item['sha256'], item['bytes'], parse=False)
expected = json.loads((workspace / 'expected-independent-topology.json').read_bytes())
for item in expected['manifests']:
    path = Path(item['path'])
    manifest = verify(path, item['sha256'])
    for original in manifest['local_records']:
        verify(original['path'], original['sha256'], original['bytes'], parse=False)
tc = verify(expected['topology_path'], expected['topology_sha256'])
for key, value in expected['required_topology_fields'].items():
    assert tc[key] == value, key
assert expected['accepted_by_root_after_reading_full_distinct_report'] is True
record = {
    'source_type_verdict': 'accepted', 'independent_topology_verdict': 'accepted',
    'remaining_statement_or_source_topology_blockers': [],
    'unproved_internal_or_library_applicability_ports': ports['ports'],
    'formalizer_API_pristine': False,
    'statement_seal_sha256': 'a5179ed392ef8e55ab470a3a98ebd542e35301f51472e9cdd7bc168a88bafa26',
    'SG_original_verdict': audit['verdict'], 'TC_original_verdict': expected['exact_original_verdict'],
    'independent_originals': list(originals.values()), 'source_root_path': str(sg.resolve()),
    'actual_full_Gaussian_consumer_source_graph': {'readback': str(r9_path), 'sha256': sha(r9_path.read_bytes()), 'still_unproved': True},
    'boundary': 'Explicitly authored generic background/type/topology acceptance only. All13 background/application ports remain unproved; closed-convex and direct Hermitian/quadratic routes are alternatives. Planned centered consumer family stays future R9 work. The actual uncentered consumer needs its full separately reviewed R9 graph plus actual mathematical proof. No API application, compiled parent or source VERIFIED grant.',
}
path = workspace / 'reviewed-preproof-inputs.json'
with path.open('x') as out:
    json.dump(record, out, ensure_ascii=False, indent=2)
    out.write('\n')
print(json.dumps({'path': str(path), 'sha256': sha(path.read_bytes()), 'independent_originals_rehashed': len(originals), 'background_type_and_distinct_topology': 'accepted', 'unproved_background_and_application_ports': 13, 'shared_target_proof_implementation_attempts': 0}))
