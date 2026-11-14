"""Read back distinct frozen source/type/topology evidence before normal intake."""
from pathlib import Path
import hashlib
import json

workspace = Path(__file__).resolve().parent.relative_to(Path.cwd())
sha = lambda raw: hashlib.sha256(raw).hexdigest()
originals = {}


def verify(path, expected=None, length=None):
    path = Path(path)
    raw = path.read_bytes()
    assert not path.is_symlink()
    if expected is not None:
        assert sha(raw) == expected, str(path)
    if length is not None:
        assert len(raw) == length, str(path)
    originals[str(path)] = {'path': str(path), 'bytes': len(raw), 'sha256': sha(raw)}
    return json.loads(raw)


sg_raw_path = Path('.astis/semantic-neutral-20261112/ri_sg_78c2/raw-freeze-v1/frozen-manifest.json')
sg_type_path = Path('.astis/semantic-neutral-20261112/ri_sg_78c2/type-phase-v1/freeze-manifest.json')
for path, digest in [
    (sg_raw_path, '2bdc92ca14e919b33ec81f8480e8782bf0fe16e94fca4442e2f1e15ad040b351'),
    (sg_type_path, 'cd82a466624449344f6371ea5012afcc8ddc57ae68260403ac306271a9b5ee7f'),
]:
    manifest = verify(path, digest)
    for entry in manifest['files']:
        verify(path.parent / entry['path'], entry['sha256'], entry['bytes']) if entry['path'].endswith('.json') else None
        raw_path = path.parent / entry['path']
        raw = raw_path.read_bytes()
        assert len(raw) == entry['bytes'] and sha(raw) == entry['sha256']
        originals[str(raw_path)] = {'path': str(raw_path), 'bytes': len(raw), 'sha256': sha(raw)}
for name, digest in [
    ('raw-freeze.json', 'dc5f3b9278a7fe8d3eac246c794f0832ca157f4d9cf3b9c52443c28444e70ee9'),
    ('type-freeze.json', '8d363393f9486f01bb526747d6142c8843823917f74b70a664a537988f69147a'),
    ('graph-freeze-v1.json', '4e855074ab1cfd1a684415909c4595d941452b0cf8b35a986fbafeff6d10767b'),
]:
    path = Path('.astis/semantic-neutral-20261112/ri_tc_24a6') / name
    manifest = verify(path, digest)
    for entry in manifest['local_records']:
        raw_path = Path(entry['path'])
        raw = raw_path.read_bytes()
        assert not raw_path.is_symlink() and len(raw) == entry['bytes'] and sha(raw) == entry['sha256']
        originals[str(raw_path)] = {'path': str(raw_path), 'bytes': len(raw), 'sha256': sha(raw)}
sg_audit = verify(sg_type_path.parent / 'type-audit.json',
                  'b1ea8b9740aecac67a45f3c9f101197553fa8dcacc3ba825b5285dad2dfc37cb')
tc_type = verify('.astis/semantic-neutral-20261112/ri_tc_24a6/type-freeze.json')
tc_graph = verify('.astis/semantic-neutral-20261112/ri_tc_24a6/graph-freeze-v1.json')
ports = verify(sg_type_path.parent / 'internal-bridge-and-applicability-ports.json',
               '81ce2bf272b44dd42e208cf842a10cf39dcb1229bd0c5ea2a5570c1057ceb61a')
assert sg_audit['verdict'] == 'NO_GENUINE_TARGET_MEANING_OR_BINDER_ISSUE_FOUND'
assert sg_audit['EXCESS'] == []
assert tc_type['type_source_meaning_finding'].startswith('No type/source meaning issue found')
assert tc_graph['finding'] == 'ACCEPT_BOUNDED_SOURCE_COVERAGE_AND_UNPROVED_SOURCE_TOPOLOGY'
assert tc_graph['genuine_statement_or_source_coverage_blockers'] == []
assert len(ports['ports']) == tc_graph['expected_unproved_internal_ports'] == 10
assert all(p['status'] == 'OPEN_UNPROVED_INTERNAL_PORT' for p in ports['ports'])
record = {
    'source_type_verdict': 'accepted', 'independent_topology_verdict': 'accepted',
    'remaining_statement_or_source_topology_blockers': [],
    'unproved_internal_or_library_applicability_ports': ports['ports'],
    'formalizer_API_pristine': False,
    'statement_seal_sha256': '88a55849ce9e13a9a04edff6aac13ce32d4370712b1b7a422fba0d570ff0b25e',
    'SG_original_verdict': sg_audit['verdict'],
    'TC_original_verdict': tc_graph['finding'],
    'independent_originals': list(originals.values()),
    'boundary': 'Source/type/topology acceptance only; all10 internal proof/applicability ports remain unproved, with no actual parent/call or source VERIFICATION grant.',
}
path = workspace / 'reviewed-preproof-inputs.json'
with path.open('x') as out:
    json.dump(record, out, ensure_ascii=False, indent=2)
    out.write('\n')
print(json.dumps({'path': str(path), 'sha256': sha(path.read_bytes()),
                  'independent_originals_rehashed': len(originals),
                  'source_type_and_distinct_topology': 'accepted',
                  'unproved_internal_ports': len(ports['ports']), 'target_proof_implementation_attempts': 0}))
