from pathlib import Path
import datetime
import hashlib
import json

ROOT = Path('/Users/zhouhuanjian/ASTIS-GC')
OWN = ROOT/'.astis/semantic-neutral-20261112/mm_tc_7f32'
DEST = OWN/'conceptual-v1'
INPUT = ROOT/'.astis/huanjian-gc-source-matrix-mean-20261112/bounded-conceptual-mirror-input.json'

def sha(b):
    return hashlib.sha256(b).hexdigest()

def digest(path):
    b = path.read_bytes()
    return {'path':str(path.relative_to(ROOT)), 'bytes':len(b), 'sha256':sha(b)}

def canonical(obj):
    return json.dumps(obj,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()

def write(name,obj):
    (DEST/name).write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n')

assert digest(INPUT)['sha256'] == '104e4b92122186356b52f47cc3f29e0ffa5fb8f6fb246a81ba252d61eb8542f6'
p = json.loads(INPUT.read_text())
expected = {
    'ASTIS-DISC-20261007-GaussianSymmetryPushforwardRepaired':
        ('merged','family:gaussian-law-symmetry','transport:gaussian-symmetry-pushforward'),
    'ASTIS-DISC-20261111-GaussianRadialWeightedMatrixSymmetry':
        ('validated','family:orthogonal-invariance','transport:gaussian-radial-weighted-matrix-symmetry'),
}
assert len(p['existing']) == 2
preserved_records = []
for item in p['existing']:
    status,family,bridge = expected[item['discovery_id']]
    assert (item['status'],item['metadata']['family_id'],item['metadata']['bridge_id']) == (status,family,bridge)
    preserved_records.append({
        'discovery_id':item['discovery_id'], 'status':status,
        'family_id':family, 'bridge_id':bridge,
        'identity_and_status_preserved':True,
        'historical_scope_and_metadata_preserved':True,
        'revalidation_performed':False, 'status_or_metadata_updated':False,
        'original_embedded_record_canonical_json_sha256':sha(canonical(item)),
        'digest_scope':'Exact embedded input record, not an independently fetched historical registry revision.',
    })
write('existing-records-preserved.json',{
    'existing':p['existing'],
    'preservation_note':'Original embedded metadata/statements/statuses copied without field edits, including historical candidate/compiled wording. No historical or new theorem revalidation.',
})
copied = json.loads((DEST/'existing-records-preserved.json').read_text())['existing']
assert copied == p['existing']
assert all(sha(canonical(a)) == sha(canonical(b)) for a,b in zip(copied,p['existing']))

types = p['current_exact_sealed_types']
assert sha(types['producer']['signature'].encode()) == types['producer']['signature_sha256'] == '099bcbe9d6cc440754282873a7f1e1001584c3566fc771a70bf9f1a3846b85fe'
assert sha(types['actual_private_consumer']['signature'].encode()) == types['actual_private_consumer']['signature_sha256'] == '00c0b050a632e03d9b169acdb6632ae85a9ec43cc2b5e8aa26b7b6152a711b7e'
prior_expected = {
    'raw-freeze.json':'30a7d626b681fb59c522969a9be91797d1ca794f5e0433ea6941dfc7064c3fa8',
    'type-v1/freeze.json':'4602bbe4a97d053a1e9cf788f0247fee5a6965d33e0cfdb40928767f995c43e7',
    'topology-v1/freeze.json':'a43b65e9fe4c7cec392c0a1b4e7338e250b5f5a73a6042c16dce255179f3fa6e',
}
for name,val in prior_expected.items():
    assert digest(OWN/name)['sha256'] == val
prior_local = []
for rel in ['SHA256SUMS','type-v1/SHA256SUMS','topology-v1/SHA256SUMS']:
    manifest = OWN/rel
    for line in manifest.read_text().splitlines():
        val,name = line.split('  ',1)
        assert digest(manifest.parent/name)['sha256'] == val
        prior_local.append(digest(manifest.parent/name))
    prior_local.append(digest(manifest))

input_manifest = {
    'input':digest(INPUT),'assignment':digest(DEST/'assignment.txt'),
    'input_scope':p['scope'],'source_scope':p['source_scope'],
    'embedded_exact_producer_signature_sha256_recomputed':types['producer']['signature_sha256'],
    'embedded_exact_consumer_signature_sha256_recomputed':types['actual_private_consumer']['signature_sha256'],
    'existing_records_preserved_without_revalidation':preserved_records,
    'prior_existing_packet_reference_as_supplied_not_opened':p['prior_existing_record_packet'],
    'prior_own_raw_type_topology_records_preserved_by_byte_hash':prior_local,
    'SG_files_not_reopened_or_written_this_phase':True,
    'source_graph_private_review_implementation_API_or_global_inventory_fetches':[],
}
write('input-manifest.json',input_manifest)
judgment = {
    'version':1,'actor':'/root/row_indep_topology_24a6',
    'audit_kind':'bounded_NEW_source_backed_conceptual_correspondence_only',
    'finding':'none-found','new_candidates':[],
    'bounded_scope':p['scope'],'source_scope':p['source_scope'],
    'global_novelty_or_inventory_claim':False,
    'existing_records_preserved_without_revalidation':preserved_records,
    'reasoning':[
        'The Ex108 radial-moment mechanism is already inside the preserved existing radial weighted-matrix correspondence; matching the same canonical moment to the actual row is canonical law/integral transport.',
        'Fixed tensor/scalar CLM or finite-entry expectation transport and exact cosine-frame plus finite-sum integral linearity are ordinary canonical reuse, not a distinct new cross-source pair.',
        'No additional source-backed hypothesis/key-identity/conclusion map was identified beyond existing correspondence reuse and these exact applications.',
    ],
    'canonical_reuse_and_failure_boundaries':[
        {'reuse':'Actual row-law and canonical moment transport',
         'boundary':'Requires the exact actual-row pushforward law, integrability and matching r,L,a under the same mu; no arbitrary ambient/surrogate transfer or joint independence premise.'},
        {'reuse':'Existing radial weighted-matrix mechanism',
         'boundary':'Radial weight/law sign-permutation symmetries and weight-specific integrability are essential. Current truncated first moments do not imply unbounded radial fourth moments, Ex113 variance, concentration or main bounds.'},
        {'reuse':'Fixed tensor CLM or finite-entry integral transport',
         'boundary':'Linearity is in the already formed truncated row-matrix with deterministic factors; it does not commute expectation with the original nonlinear row outer-product/cutoff map.'},
        {'reuse':'Exact cosine-frame identities',
         'boundary':'Midpoint grid, constant-feature normalization, n=2q+1, standing range and q=0 conventions must match; arbitrary grids/weights/normalizations are not covered.'},
        {'reuse':'Finite actual-sum expectation linearity',
         'boundary':'Requires actual integrability and deterministic cosine scalar matching; zero mean provides no variance/concentration/cost result and Bochner totalization is not a proof.'},
        {'reuse':'Existing Gaussian symmetry pushforward correspondence',
         'boundary':'Its actual law-preserving and intertwining reflection/rotation hypotheses/conclusions remain distinct. This delta provides no new such pair or new implication to matrix moments or frame sums.'}
    ],
    'historical_candidate_wording_note':'Original wording remains historical metadata under supplied merged/validated identities. No prior compiled claim or current proof-call/application is recertified here.',
    'exact_API_calls_or_compiled_edges_verified':False,
    'discovery_creation_requested':p['discovery_creation_requested'],
    'Discovery_created_or_validated':False,
    'shared_metadata_C_L_Git_ledger_global_graph_written':False,
    'root_V_integration_or_permission_grant':False,
}
write('judgment.json',judgment)
local_names = ['assignment.txt','judgment.md','exposure.json','freeze.py',
               'existing-records-preserved.json','input-manifest.json','judgment.json']
freeze = {
    'version':1,'kind':'independent-bounded-NEW-conceptual-correspondence-freeze',
    'actor':'/root/row_indep_topology_24a6','created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'finding':'none-found','new_candidates':[],
    'existing_records_preserved_without_revalidation':preserved_records,
    'input':digest(INPUT),'local_records':[digest(DEST/name) for name in local_names],
    'preserved_prior_own_freezes':[digest(OWN/name) for name in prior_expected],
    'prior_raw_type_topology_artifacts_preserved':True,
    'SG_files_opened_or_written_this_phase':False,
    'proof_API_implementation_or_other_review_read_this_phase':False,
    'compiled_edge_source_VERIFIED_root_V_integration_or_permission_grant':False,
    'truth_boundary':'Bounded NEW-correspondence judgment only, preserving supplied existing identities/statuses/historical metadata without revalidation. No Discovery, proof implication, current API call certification or shared state mutation.',
}
write('freeze.json',freeze)
records = [digest(DEST/name) for name in local_names]+[digest(DEST/'freeze.json')]
(DEST/'SHA256SUMS').write_text(''.join(f"{a['sha256']}  {Path(a['path']).name}\n" for a in records))
print(json.dumps({'freeze':digest(DEST/'freeze.json'),'judgment_json':digest(DEST/'judgment.json'),
                  'judgment_md':digest(DEST/'judgment.md'),'input_manifest':digest(DEST/'input-manifest.json'),
                  'exposure':digest(DEST/'exposure.json'),'finding':'none-found','new_candidates':[],
                  'existing_records_preserved_without_revalidation':preserved_records,
                  'old_own_records_preserved':len(prior_local)},indent=2))
