"""Rehash independent frozen originals before a single normal mathematical intake."""
from pathlib import Path
import hashlib
import json

workspace = Path(__file__).resolve().parent.relative_to(Path.cwd())
sha = lambda b: hashlib.sha256(b).hexdigest()
originals = {}

def verify(path, digest=None, length=None, parse=True):
    path = Path(path)
    raw = path.read_bytes()
    assert not path.is_symlink()
    assert digest is None or sha(raw) == digest, str(path)
    assert length is None or len(raw) == length, str(path)
    originals[str(path)] = {'path': str(path), 'bytes': len(raw), 'sha256': sha(raw)}
    return json.loads(raw) if parse else raw

sg = Path('.astis/semantic-neutral-20261112/mm_sg_61c4')
for name, digest in [
    ('raw-freeze-v1/freeze-manifest.json', '4daf44e6a41b758d624abc58eaa9ac78101c7d43e309fe5554fcac3dd40d2ac7'),
    ('type-freeze-v1/freeze-manifest.json', 'fb51437ebd9e6d36241e4c84637a2d1e168f11c75818edef785c7b4a9a2c474c'),
    ('source-graph-freeze-v1/freeze-manifest.json', 'c22ea07651b9d402eaf97a0c8be5d29bc3530031e0d29a9a401300fa7ef6d7d6'),
]:
    path = sg / name
    manifest = verify(path, digest)
    for item in manifest['files']:
        verify(path.parent / item['path'], item['sha256'], item['bytes'], parse=False)
audit = verify(sg / 'type-freeze-v1/type-audit.json', '57478b54ec7f5bd2ecc7b5ef0fa4761d271eda6cbfde1c6f2075b54002f1ae90')
graph = verify(sg / 'source-graph-freeze-v1/source-proof-graph.json', '72cbce5939c8ac2b27ab9dc6d0b347e8b8f5311cc161d78727cc08e0ae9915b4')
coverage = verify(sg / 'source-graph-freeze-v1/post-seal-coverage.json', '508560a2f8c69f42e6482fab0c89f12b1f935700feb25e989a61e7f05667b8b8')
ports = verify(sg / 'source-graph-freeze-v1/internal-ports-and-source-gaps.json', '70a8b803ed6d8b99cdd836dc57450075b0982e15e12326f31d6c276f13705d16')
verify(sg / 'source-graph-freeze-v1/chronology-qualification.json', '2c8964caeed7abd102fd068b2d95eda8bc69723014cded26de77aaa5d49630e3')
assert audit['verdict'] == 'NO_GENUINE_TYPE_BINDER_DEFINITION_OR_SOURCE_SCOPE_ISSUE_FOUND'
assert audit['EXCESS_public_binders'] == audit['genuine_target_issues'] == audit['genuine_SOURCE_GAPs'] == []
assert graph['compiled_parents'] == graph['genuine_source_gaps'] == []
assert not graph['implementation_seen'] and not graph['new_target_compiled']
assert coverage['counts'] == {'EXCLUDED': 35, 'NODE': 44, 'atoms': 79}
assert len(graph['nodes']) == 62 and len(graph['edges']) == 94
assert len(ports['ports']) == 13 and ports['genuine_source_gaps'] == []
assert all(p['status'] == 'OPEN_INTERNAL_PROOF_APPLICABILITY' and not p['SOURCE_GAP'] for p in ports['ports'])
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
    'statement_seal_sha256': 'b55a1acb837288d580a667903987e5f809610626eb4848c750ff8d3a6c01149b',
    'SG_original_verdict': audit['verdict'],
    'TC_original_verdict': expected['exact_original_verdict'],
    'independent_originals': list(originals.values()),
    'source_root_path': str(sg.resolve()),
    'boundary': 'Independent source/type/coverage/topology acceptance only. All13 internal/applicability ports remain unproved; CLM and entrywise routes are alternatives, so the unselected route need not be proved. No actual new compiled proof parent or source VERIFIED grant.',
}
path = workspace / 'reviewed-preproof-inputs.json'
with path.open('x') as out:
    json.dump(record, out, ensure_ascii=False, indent=2)
    out.write('\n')
print(json.dumps({'path': str(path), 'sha256': sha(path.read_bytes()),
                  'independent_originals_rehashed': len(originals),
                  'source_type_and_distinct_topology': 'accepted', 'unproved_internal_ports': 13,
                  'target_proof_implementation_attempts': 0}))
