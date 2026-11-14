from pathlib import Path
import datetime
import hashlib
import json

ROOT = Path('/Users/zhouhuanjian/ASTIS-GC')
OWN = ROOT / '.astis/semantic-neutral-20261112/ri_tc_24a6'
DEST = OWN / 'conceptual-v1'
INPUT = ROOT / '.astis/huanjian-gc-source-row-independence-20261112/bounded-conceptual-mirror-input.json'

def sha(b):
    return hashlib.sha256(b).hexdigest()

def digest(p):
    b = p.read_bytes()
    return {'path':str(p.relative_to(ROOT)), 'bytes':len(b), 'sha256':sha(b)}

def write(name, value):
    (DEST/name).write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n')

assert digest(INPUT)['sha256'] == '230ed47231d7bfc83122dd8c06d529fd62bb6df8c3be77e0e896c9c425da67e7'
packet = json.loads(INPUT.read_text())
expected = {
    'ASTIS-DISC-20261007-GaussianSymmetryPushforwardRepaired':
        ('merged', 'family:gaussian-law-symmetry', 'transport:gaussian-symmetry-pushforward'),
    'ASTIS-DISC-20261111-GaussianRadialWeightedMatrixSymmetry':
        ('validated', 'family:orthogonal-invariance', 'transport:gaussian-radial-weighted-matrix-symmetry'),
}
assert len(packet['existing']) == 2
existing = []
for item in packet['existing']:
    status, family, bridge = expected[item['discovery_id']]
    assert (item['status'], item['metadata']['family_id'], item['metadata']['bridge_id']) == (status, family, bridge)
    existing.append({
        'discovery_id':item['discovery_id'], 'status_as_supplied':status,
        'family_id':family, 'bridge_id':bridge,
        'embedded_record_canonical_json_sha256':sha(json.dumps(item,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()),
        'digest_note':'Binds the exact embedded record via canonical JSON, not an independently fetched registry revision.',
        'identity_and_status_preserved':True, 'revalidation_performed':False,
        'metadata_or_status_update_requested_or_made':False,
    })

preserved = {
    'raw-freeze.json':'dc5f3b9278a7fe8d3eac246c794f0832ca157f4d9cf3b9c52443c28444e70ee9',
    'type-freeze.json':'8d363393f9486f01bb526747d6142c8843823917f74b70a664a537988f69147a',
    'graph-freeze-v1.json':'4e855074ab1cfd1a684415909c4595d941452b0cf8b35a986fbafeff6d10767b',
}
for name, val in preserved.items():
    assert digest(OWN/name)['sha256'] == val
manifest = {
    'input':digest(INPUT),
    'assignment':digest(DEST/'assignment.txt'),
    'source_scope':packet['source_scope'],
    'existing_embedded_records':existing,
    'prior_own_freezes_preserved_by_byte_hash':[digest(OWN/name) for name in preserved],
    'no_global_inventory_or_additional_record_fetch':True,
}
write('input-manifest.json', manifest)
judgment = {
    'version':1, 'actor':'/root/row_indep_topology_24a6',
    'audit_kind':'bounded-new-conceptual-correspondence-only',
    'status':'none-found',
    'scope':'Genuinely NEW source-backed correspondence in canonical row joint independence and actual separate Ex107 truncated-matrix images.',
    'global_novelty_or_inventory_claim':False,
    'new_candidates':[],
    'canonical_reuse_findings':[
        {'mechanism':'Physical scalar-coordinate product law plus independent columns and finite regrouping.',
         'source':['arXiv:2610.20492v1#A3.SS2.p1'],
         'classification':'ordinary canonical product/map/independence reuse',
         'failure_boundary':'Permutation/exchangeability or law invariance alone does not imply full independence; stdOrthonormalBasis to physical-coordinate applicability still needs internal discharge.'},
        {'mechanism':'Separate i-dependent measurable images of the already independent actual rows.',
         'source':['arXiv:2610.20492v1#A3.SS2.p12.1','arXiv:2610.20492v1#A3.Ex107'],
         'classification':'ordinary canonical independence-image reuse',
         'failure_boundary':'Requires actual row independence and separate measurable row maps under the same mu; does not require injectivity or imply iid matrices.'}
    ],
    'existing_records_preserved':existing,
    'distinction_from_existing':{
        'gaussian_law_symmetry':'A law-preserving symmetry transported through an intertwining actual map concludes invariance; it supplies no product factorization by itself.',
        'radial_weighted_matrix_symmetry':'Signs/permutations/trace identify weighted matrix moments under their own integrability conditions; those identities neither establish nor are needed as premises for the selected full independence.'
    },
    'discovery_creation_requested':packet['discovery_creation_requested'],
    'proof_or_Mathlib_applicability_verified':False,
    'compiled_edges_accepted':[],
    'source_VERIFIED_or_proof_process_permission_grant':False,
    'ledger_graph_UI_implementation_mutation':False,
}
write('judgment.json', judgment)
local_names = ['assignment.txt','judgment.md','exposure.json','freeze.py','input-manifest.json','judgment.json']
freeze = {
    'kind':'independent-bounded-new-conceptual-correspondence-freeze',
    'version':1, 'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'actor':'/root/row_indep_topology_24a6', 'finding':'none-found',
    'new_candidates':0, 'existing_records_preserved_without_revalidation':existing,
    'input':digest(INPUT), 'local_records':[digest(DEST/name) for name in local_names],
    'prior_raw_type_topology_freezes_preserved':[digest(OWN/name) for name in preserved],
    'truth_boundary':'Bounded NEW-correspondence judgment only; no mathematical proof, API applicability, compiled edge, source VERIFIED status, ledger/graph/UI/implementation mutation or proof/process permission grant.',
}
write('freeze.json', freeze)
records = [digest(DEST/name) for name in local_names] + [digest(DEST/'freeze.json')]
(DEST/'SHA256SUMS').write_text(''.join(f"{a['sha256']}  {Path(a['path']).name}\n" for a in records))
print(json.dumps({'freeze':digest(DEST/'freeze.json'),'judgment':digest(DEST/'judgment.json'),
                  'input_manifest':digest(DEST/'input-manifest.json'),'finding':'none-found',
                  'existing_statuses':{x['discovery_id']:x['status_as_supplied'] for x in existing},
                  'prior_freezes_preserved':True},indent=2))
