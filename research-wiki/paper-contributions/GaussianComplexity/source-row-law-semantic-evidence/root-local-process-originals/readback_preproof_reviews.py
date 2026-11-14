"""Rehash independent source/type/topology originals before normal intake."""
from pathlib import Path
import hashlib
import json

workspace = Path(__file__).resolve().parent
sg = Path('.astis/semantic-neutral-20261112/rl_sg_6a90')
tc = Path('.astis/semantic-neutral-20261112/rl_tc_b7e1')
sha = lambda b: hashlib.sha256(b).hexdigest()
manifests = [
    (sg / 'freeze_manifest.json', '236c0cd4dfeb3bd1c0a56ffd86e3b665b1bf333bb312c8df501cbc6848662439', 'artifacts'),
    (sg / 'typed_freeze_manifest.json', '6a4b16a67c4478692f412d47adf712ed6894503b9d209b944e3eeffb9d9b7be7', 'new_artifacts'),
    (tc / 'raw-freeze-v1.json', 'f3177059c29c68676885a0a16201ab2d1a70ecc56417e82d666873cdcfe6aef7', 'artifacts'),
    (tc / 'type-freeze-v1.json', '37b48efecfa818399c84b7a1f9e624ce7ba10b56531ddc86a673b9b3db3fa20d', 'artifacts'),
    (tc / 'topology-challenge-freeze-v1.json', '2556f68f137c87d222329ceb06b9766f24f04c75da65114f3fc83301ec26cfea', 'artifacts'),
]
originals = {}
for path, digest, key in manifests:
    raw = path.read_bytes()
    assert sha(raw) == digest, str(path)
    originals[str(path)] = {'path': str(path), 'bytes': len(raw), 'sha256': sha(raw)}
    for item in json.loads(raw)[key]:
        p = Path(item['path'])
        content = p.read_bytes()
        assert len(content) == item['bytes'] and sha(content) == item['sha256'], str(p)
        relative = p.resolve().relative_to(Path.cwd().resolve())
        originals[str(relative)] = {'path': str(relative), 'bytes': len(content), 'sha256': sha(content)}
audit = json.loads((sg / 'typed_binder_definition_audit.json').read_bytes())
assert audit['excess_binders_in_exact_visible_signatures'] == []
assert audit['root_formalizer_API_pristine'] is False
verdict_raw = (tc / 'topology-challenge-judgment-v1.json').read_bytes()
assert sha(verdict_raw) == '311a114d7e4c6ea04105da0950bcedfaf73f958499895eec397e7081f666d9c0'
verdict = json.loads(verdict_raw)
assert verdict['verdict'] == 'ACCEPTED_BOUNDED_TOPOLOGY_WITH_EXPLICIT_UNPROVED_PORTS'
assert verdict['blocking_topology_gaps'] == []
assert verdict['raw_coverage']['missing_atoms_or_bad_locators'] == []
assert not verdict['proof_or_process_permission_granted']
assert not verdict['source_verified_or_compiled_dependency_status_granted']
record = {
    'source_type_verdict': 'accepted', 'independent_topology_verdict': 'accepted',
    'remaining_mathematical_source_topology_gaps': [], 'formalizer_API_pristine': False,
    'statement_seal_sha256': 'f9476ec7454a0927d3a1068226ad635b464d9b5d631f4992421d4b3b39b70ec3',
    'SG_original_verdict': audit['scope_observation'],
    'TC_original_verdict': verdict['verdict'],
    'independent_originals': list(originals.values()),
    'mathematical_obligations': verdict['residual_unproved_ports'],
    'source_scope': 'Concrete canonical independent-column realization, actual row marginal maps and same-experiment all-good event. Arbitrary alternate ambient law/event transport and full joint-row independence remain outside the exact target.',
    'authority': 'Independent source/type/topology judgments only. Existing user authorization supports normal intake, no proof/process permission grant.',
}
raw = (json.dumps(record, ensure_ascii=False, indent=2) + '\n').encode()
with (workspace / 'reviewed-preproof-inputs.json').open('xb') as out:
    out.write(raw)
print(json.dumps({'originals_rehashed': len(originals), 'record_sha256': sha(raw),
                  'source_type': 'accepted', 'topology': 'accepted', 'required_repairs': []}))
