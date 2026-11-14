"""Actually rehash independent originals after reading the separate complete judgments."""
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

sg = Path('.astis/semantic-neutral-20261112/mv_sg_42f6')
for name, digest in [
    ('raw-freeze-v1/freeze-manifest.json', 'fc43d029ffd38278845eefd77f397929647ee9c3594b693f8540433675a9516d'),
    ('raw-freeze-v2/freeze-manifest.json', 'e7e6ca17db84515ecfc8af6ff48f019a297a057c3e185e5e0ccb1cab590aa05f'),
    ('type-freeze-v1/freeze-manifest.json', '40d25d926a291fba12bbe7b77e79b35c658882f2b075414bb265562d8796e377'),
    ('source-graph-freeze-v1/freeze-manifest.json', '7ffb2efb54166fe004c4369751daa953fc07bfcf772bbad159baaf92e9aace8b'),
]:
    path = sg / name
    manifest = verify(path, digest)
    for item in manifest['files']:
        verify(path.parent / item['path'], item['sha256'], item['bytes'], parse=False)
audit = verify(sg / 'type-freeze-v1/type-audit.json', 'fe0f281b09a49220b0896db169e3eaa4717fabee5d1d86317a686579a3e1ae4e')
graph = verify(sg / 'source-graph-freeze-v1/source-proof-graph.json', '83d87c553a977e0010ed376a7590d3430b73959600108b041c9c1bfb66271f09')
coverage = verify(sg / 'source-graph-freeze-v1/post-seal-coverage.json', 'a5f9b7e5bf7c7661d4d7ad12f832f2af5f3f18e9bf89463c476ef9f5ddabae09')
ports = verify(sg / 'source-graph-freeze-v1/internal-ports-and-source-gaps.json', '96e839165132fd33b5ae7364c3c834e61a22da9b49c968fb3b0017da673fb80d')
assert audit['verdict'] == 'NO_GENUINE_TYPE_BINDER_DEFINITION_OR_SOURCE_SCOPE_ISSUE_FOUND'
assert audit['EXCESS_public_binders'] == audit['genuine_target_issues'] == audit['genuine_SOURCE_GAPs'] == []
assert graph['compiled_parents'] == graph['genuine_source_gaps'] == []
assert not graph['implementation_seen'] and not graph['actual_new_target_compiled']
assert coverage['counts'] == {'EXCLUDED': 55, 'NODE': 50, 'atoms': 105}
assert coverage['p15_all_excluded'] and len(coverage['units']) == 67
assert len(graph['nodes']) == 80 and len(graph['edges']) == 129 and len(graph['hyperedges']) == 2
assert len(ports['ports']) == 23 and ports['genuine_source_gaps'] == []
assert all(p['status'] == 'OPEN_UNPROVED_INTERNAL_APPLICABILITY' and not p['genuine_SOURCE_GAP'] for p in ports['ports'])
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
    'statement_seal_sha256': '5f905cafe6035238cebdedd4f841e87b703e741b4c8aa204471d89e4c07e8a14',
    'SG_original_verdict': audit['verdict'], 'TC_original_verdict': expected['exact_original_verdict'],
    'independent_originals': list(originals.values()), 'source_root_path': str(sg.resolve()),
    'boundary': 'Independent source/type/coverage/topology acceptance only. All23 internal/applicability ports remain unproved; tensor transport and actual-Y integrability have two separate OR alternatives, not four compulsory proof routes or public certificates. No new compiled proof parent or source VERIFIED grant.',
}
path = workspace / 'reviewed-preproof-inputs.json'
with path.open('x') as out:
    json.dump(record, out, ensure_ascii=False, indent=2)
    out.write('\n')
print(json.dumps({'path': str(path), 'sha256': sha(path.read_bytes()), 'independent_originals_rehashed': len(originals), 'source_type_and_distinct_topology': 'accepted', 'unproved_internal_ports': 23, 'target_proof_implementation_attempts': 0}))
