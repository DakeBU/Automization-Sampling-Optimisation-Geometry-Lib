"""Carry the independent actor's unique original V event; never execute its API script."""
from pathlib import Path
import hashlib
import json
import subprocess
import sys
sys.dont_write_bytecode=True
sys.path.insert(0,'tools')
import astis_advance as advance
W=Path(__file__).resolve().parent.relative_to(Path.cwd())
E=Path('research-wiki/technical-lemmas/real-matrix-positive-integral-semantic-evidence')
C=Path('research-wiki/frontier-cells/ASTIS-SHARED-REAL-MATRIX-POSITIVE-INTEGRAL.json')
L=Path('runs/substantive_advances.jsonl')
R=Path('.astis/semantic-neutral-20261112/mv_src_6e28/normal-verification-v2')
D=E/'normal-verification/mv_src_6e28/originals'
N=Path('.astis/semantic-neutral-20261113/psd_native_7b31/held-gates-v2')
ND=E/'native-review/psd_native_7b31/held-gates-v2'
sha=lambda raw:hashlib.sha256(raw).hexdigest()
dump=lambda obj:(json.dumps(obj,ensure_ascii=False,indent=2)+'\n').encode()
git=lambda *args:subprocess.check_output(['git',*args])
def create(p,raw):
    p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('xb') as f:f.write(raw)
def check_record(item,key='path'):
    p=Path(item[key]); raw=p.read_bytes()
    assert len(raw)==item['bytes'] and sha(raw)==item['sha256'],str(p)
    return p,raw
def copy_once(p,raw):
    if p.exists():assert p.read_bytes()==raw and not p.is_symlink(),str(p)
    else:create(p,raw)

head=git('rev-parse','HEAD').decode().strip()
assert head=='5f69ac83737e497210d8d8ad9628c45d83089458'
assert not git('diff','--cached','--name-only')
assert set(git('diff','HEAD','--name-only').decode().splitlines())=={str(C),str(L)}
expected={
    'normal-VERIFIED-result.json':'8997df84cf89d6d6f00241a6b14b58f5001afca1c7a13c8c68ee1a99dc2a818e',
    'NORMAL-VERIFIED-FROZEN.json':'87fe84fe0497ffb7103365ba574e6ef2ec0ea8c776e7e53ab9e8d6a66becbcb9',
    'portable-originals-manifest.json':'537ca70102ba7b9b3eb8f8477f064fb86e473563aca53a5a43bc426ca0f11e75',
    'postseal-output-index.json':'23e1d48237166a822842a5b9811b667318cbbb42c7f5911b63518652a6acaf6f',
    'REPORT.md':'40e653db5268b1d9b71ab8099a9ab0ad2dba721f38119e4ff78dcd5df3b7fecd'}
for n,h in expected.items():assert sha((R/n).read_bytes())==h,n
result=json.loads((R/'normal-VERIFIED-result.json').read_bytes())
assert result['heldHEAD']==head and result['mathCommit']=='9964c33c4599f85d27dc8687e8bd6fdb5c44ff49'
assert result['actual_API_calls']==1 and result['actual_API_failures']==0
assert result['pre_V_count']==0 and result['post_V_count']==1
assert result['PL_original_fields_inline_unchanged']==20
assert result['all_four_held_gates_actual_exit_zero'] and result['full_prepost_foreign_guard_passed']
assert result['private_local_only']['private_full_bytes_exported'] is False
for key in ['normal_command_receipt','full_V_payload','exact_raw_one_line_append','ownC_before','ownC_after']:
    check_record(result[key])
append=Path(result['exact_raw_one_line_append']['path']).read_bytes()
assert len(append.splitlines())==1 and sha(append)=='24cc7ea161d32a42a78e3b2e4d10a091faffe604bb1d1c419ee4b943d6d1ab78'
event=json.loads(append)
payload=json.loads(Path(result['full_V_payload']['path']).read_bytes())
assert event['advance_id']=='ASTIS-SA-20261112-RealMatrixPositiveIntegral'
assert event['worker_id']=='/root/mv_fresh_source_6e28'
assert event['from_state']=='PROVED_LOCAL' and event['to_state']=='VERIFIED'
assert event['evidence']==payload
pl=json.loads((E/'actual-PROVED_LOCAL-evidence.full.json').read_bytes())
assert len(pl)==20 and all(payload[k]==v for k,v in pl.items())
assert payload['verified_commit']==result['mathCommit'] and payload['verification_metadata_HEAD']==head
assert L.read_bytes()==git('show',f'{head}:{L}')+append
assert C.read_bytes()==Path(result['ownC_after']['path']).read_bytes()
assert git('show',f'{head}:{C}')==Path(result['ownC_before']['path']).read_bytes()
before=json.loads(git('show',f'{head}:{C}')); after=json.loads(C.read_bytes())
allowed=json.loads(json.dumps(before))
allowed['status']='independently_verified'
allowed['evidence']['independent_verification']=after['evidence']['independent_verification']
assert allowed==after and after['owner_id']=='huanjian_20261112_real_matrix_positive_integral'
states=advance._replay_advances([json.loads(x) for x in L.read_bytes().splitlines()])
assert states.pop(event['advance_id'])['state']=='VERIFIED'
b=json.loads((W/'candidate-boundary-v5.private.json').read_bytes())
assert states==b['all_foreign_states']
for p,h in b['all_existing_frontier_hashes'].items():assert sha(Path(p).read_bytes())==h,p
dg=json.loads((W/'preproof-discoveries.private.json').read_bytes())
assert sha(Path('runs/substantive_discoveries.jsonl').read_bytes())==dg['ledger_sha256']
api=json.loads((R/'normal-API-receipt.json').read_bytes())
assert api['exit']==0 and api['actual_API_calls']==1 and api['actual_API_failures']==0

carried={}
def add(dest,raw):
    assert not dest.is_absolute() and '..' not in dest.parts
    if dest in carried:assert carried[dest]==raw
    else:carried[dest]=raw
m=json.loads((R/'portable-originals-manifest.json').read_bytes())
assert m['files']==len(m['records'])==417
assert m['private_foreign_control_index_blobs_and_native_gzip_excluded'] is True
for item in m['records']:
    p,raw=check_record(item,'source_path'); dest=Path(item['destination_path'])
    assert p.is_relative_to(Path('.astis/semantic-neutral-20261112/mv_src_6e28'))
    assert dest.is_relative_to(D) and '.private.' not in p.name and not p.is_symlink()
    add(dest,raw)
post=json.loads((R/'postseal-output-index.json').read_bytes())
for item in post['files']:
    p,raw=check_record(item)
    assert p.is_relative_to(R) and '.private.' not in p.name
    add(D/'normal-verification-v2'/p.relative_to(R),raw)
add(D/'normal-verification-v2/postseal-output-index.json',(R/'postseal-output-index.json').read_bytes())
for name in ['portable-originals-manifest.json','NORMAL-VERIFIED-FROZEN.json']:
    add(D/'normal-verification-v2'/name,(R/name).read_bytes())

assert sha((N/'portable-originals-manifest.json').read_bytes())=='df9a9294cac1f1e415b9fd0289304565bb90f05e72e3bfc43dba51e007250dcc'
assert sha((N/'seal.json').read_bytes())=='d22af71fb4cd727da6903bf054a32fdac0a66300d05b624036ae1e9b8af9e964'
nm=json.loads((N/'portable-originals-manifest.json').read_bytes())
assert len(nm['entries'])==120
for item in nm['entries']:
    p,raw=check_record(item,'source'); dest=Path(item['destination'])
    assert p.resolve().is_relative_to(N.resolve()) and dest.is_relative_to(ND)
    add(dest,raw)
add(ND/'portable-originals-manifest.json',(N/'portable-originals-manifest.json').read_bytes())
for p in sorted((N/'receipts').glob('20261112T161505911537Z-freeze-v2-originals.*')):
    add(ND/'post-seal-envelope'/p.name,p.read_bytes())
for p,raw in carried.items():copy_once(p,raw)
custody={
    'kind':'ROOT exact-byte carrier of the sole independent normal V; no API replay',
    'verifier':'/root/mv_fresh_source_6e28','actual_normal_API_calls_by_independent_actor':1,
    'actual_normal_API_failures':0,'normal_V_pre_post':[0,1],'root_VERIFIED_API_calls':0,
    'mathematical_candidate':result['mathCommit'],'verification_metadata_HEAD':head,
    'exact_original_append_sha256':sha(append),'complete_V_payload_sha256':sha(Path(result['full_V_payload']['path']).read_bytes()),
    'original_PL_fields_preserved_inline':len(pl),'total_original_V_payload_fields':len(payload),
    'normal_portable_manifest_sha256':expected['portable-originals-manifest.json'],
    'normal_result_sha256':expected['normal-VERIFIED-result.json'],
    'normal_seal_sha256':expected['NORMAL-VERIFIED-FROZEN.json'],
    'postseal_output_index_sha256':expected['postseal-output-index.json'],
    'normal_verifier_scope_and_qualifications':str(D/'normal-verification-v2/REPORT.md'),
    'full_foreign_advance_states_preserved':len(states),'all_discoveries_preserved':43,
    'qualified_foreign_regular_frontiers_preserved':len(b['all_existing_frontier_hashes']),
    'independent_guard_counts_and_commitments':result['private_local_only'],
    'raw_copied_artifacts':len(carried),'V_event_replayed':False,
    'boundary':'S local independently VERIFIED only. P uncentered source/native accepted as material consumer; fullR9/T/integration/publication/purification/Goal HOLD; original stabilization owner not released.'}
custody_path=E/'actual-original-VERIFIED-root-custody.json'
create(custody_path,dump(custody))
script_copy=E/'carry-original-VERIFIED-root-script.py.txt'
create(script_copy,Path(__file__).read_bytes())
paths=[C,L,custody_path,script_copy,*carried]
assert len(paths)==len(set(paths))
spec=W/'normal-V-carrier-paths.private.nul'
create(spec,b'\0'.join(str(p).encode() for p in paths)+b'\0')
subprocess.run(['git','add','-f','--pathspec-from-file='+str(spec),'--pathspec-file-nul'],check=True)
assert set(git('diff','--cached','--name-only').decode().splitlines())==set(map(str,paths))
subprocess.run(['git','diff','--cached','--check','--',str(C),str(L),str(custody_path)],check=True)
subprocess.run(['git','commit','--quiet','-m','Carry sole independent VERIFIED event for shared real PSD integral'],check=True)
commit=git('rev-parse','HEAD').decode().strip()
for p in paths:assert git('show',f'{commit}:{p}')==p.read_bytes()
assert not git('diff','HEAD','--name-only')
record={**custody,'original_VERIFIED_carrier_commit':commit,'exact_carried_files':len(paths)}
create(W/'actual-original-VERIFIED-commit.json',dump(record))
print(json.dumps({k:record[k] for k in ['original_VERIFIED_carrier_commit','mathematical_candidate','verification_metadata_HEAD','exact_original_append_sha256','complete_V_payload_sha256','original_PL_fields_preserved_inline','total_original_V_payload_fields','raw_copied_artifacts','root_VERIFIED_API_calls']}))
