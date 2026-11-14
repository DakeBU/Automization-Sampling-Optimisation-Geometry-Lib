"""Carry the independent original R9 normal V event/custody without replay or editing it."""
from pathlib import Path
import hashlib
import json
import subprocess
import sys
sys.dont_write_bytecode=True
sys.path.insert(0,'tools')
import astis_advance as advance
W=Path(__file__).resolve().parent.relative_to(Path.cwd())
R=Path('.astis/semantic-neutral-20261112/mv_src_6e28/r9-normal-verification/final-v1')
E=Path('research-wiki/paper-contributions/GaussianComplexity/source-matrix-variance-semantic-evidence')
D=E/'normal-verification/mv_src_6e28/r9-final-v1/originals'
C=Path('research-wiki/frontier-cells/ASTIS-SW-GAUSSIAN-COMPLEXITY-source-matrix-variance.json')
L=Path('runs/substantive_advances.jsonl')
ADV='ASTIS-SA-20261112-GaussianComplexitySourceMatrixVariance'
sha=lambda raw:hashlib.sha256(raw).hexdigest()
dump=lambda obj:(json.dumps(obj,ensure_ascii=False,indent=2)+'\n').encode()
git=lambda *args:subprocess.check_output(['git',*args])
def create(p,raw):
    p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('xb') as f:f.write(raw)
head=git('rev-parse','HEAD').decode().strip()
assert head=='02fb93c64e4222f112e57c97ced2a548235cd0f6'
assert not git('diff','--cached','--name-only')
assert set(git('diff','HEAD','--name-only').decode().splitlines())=={str(C),str(L)}
assert sha(C.read_bytes())=='69cf7e46d4d084ba82be4a5b87a42fdc99043ff59aa2881431c277387c767d3f'
assert sha((R/'normal-VERIFIED-result.final.json').read_bytes())=='b8308969ec2b6ce9581d08ee0400c8938acb3c61beb13259ff3f3ac65410c99c'
result=json.loads((R/'normal-VERIFIED-result.final.json').read_bytes())
assert result['held_metadata_HEAD']==head and result['actual_API_calls']==1 and result['actual_API_failures']==0
assert result['pre_V_count']==0 and result['post_V_count']==1 and result['owner_released'] is False
assert result['actual_postwrite_fullfrontier_schema_errors']==0
payloadraw=(R/'VERIFIED-evidence.final.full.json').read_bytes()
assert sha(payloadraw)=='ed93bceb84fc710bd40f9195127904561ac3300384acb20e8c36b7b44ca274d0'
payload=json.loads(payloadraw)
pl=json.loads((E/'actual-PROVED_LOCAL-evidence.full.json').read_bytes())
assert len(pl)==21 and all(payload[k]==v for k,v in pl.items())
append=(R/'actual-VERIFIED-append.exact.jsonl').read_bytes()
assert sha(append)=='01491915baf4a1a17b3d1fcde4d18234e98913112b71713ed7745acc3387f54b'
assert len(append.splitlines())==1
event=json.loads(append)
assert event['advance_id']==ADV and event['from_state']=='PROVED_LOCAL' and event['to_state']=='VERIFIED'
assert event['worker_id']=='/root/mv_fresh_source_6e28' and event['evidence']==payload
assert L.read_bytes()==git('show',f'{head}:{L}')+append
api=json.loads((R/'normal-API-receipt.json').read_bytes())
assert sha((R/'normal-API-receipt.json').read_bytes())=='5bc5dfe92d38d22c32ae3a082307371b82033c3350033b1187710de1e4719eb1'
assert api['exit']==0 and api['actual_API_calls']==1 and api['actual_API_failures']==0
guard=json.loads((R/'postguard-comparison.json').read_bytes())
assert guard['all_pass'] and guard['full_foreign_advances_preserved']==309
assert guard['all_foreign_regular_frontier_files_including_README_preserved']==469
assert guard['full_private_foreign_control_index_snapshots_exported'] is False
b=json.loads((W/'continuation-after-S-schema-correction.private.json').read_bytes())
states=advance._replay_advances([json.loads(x) for x in L.read_bytes().splitlines()])
assert states.pop(ADV)['state']=='VERIFIED' and states==b['all_foreign_states']
for p,h in b['all_existing_frontier_hashes'].items():assert sha(Path(p).read_bytes())==h,p
discovery=Path('runs/substantive_discoveries.jsonl').read_bytes()
cell,old=json.loads(C.read_bytes()),json.loads(git('show',f'{head}:{C}'))
assert cell['status']=='independently_verified' and cell['owner_id']==old['owner_id']
assert isinstance(cell['evidence']['independent_verification'],str) and cell['evidence']['independent_verification'].strip()
for key in ['reader_contract','truth_boundary','reuse_plan']:
    assert cell[key]==old[key],key
assert cell['evidence']['independent_native_reader']==old['evidence']['independent_native_reader']
assert cell['evidence']['conditional_reader_production_proposal']==old['evidence']['conditional_reader_production_proposal']
assert cell['evidence']['independent_native_reader']['disposition']=='NATIVE_PASS_READER_FAIL'

mp,post=R/'portable-custody-manifest.final.json',R/'late-postseal-output-index.json'
assert sha(mp.read_bytes())=='4ec0a58cef4b8e078b0c16ec9d73be0917a81eb3f1e07e59cb97236f712825be'
assert sha(post.read_bytes())=='b1d12926cea3d5d3f104f49dbe25f637fb62e8c1e9acdf46a7cd2e10d7923edb'
manifest=json.loads(mp.read_bytes());assert len(manifest['records'])==174
records=manifest['records']+json.loads(post.read_bytes())['files']
records.append({'source_path':str(post),'destination_path':str(D/post.name),'bytes':post.stat().st_size,'sha256':sha(post.read_bytes())})
plans={}
for x in records:
    p,d=Path(x['source_path']),Path(x['destination_path'])
    assert p.is_relative_to(Path('.astis')) and not p.is_absolute() and '..' not in p.parts
    assert 'private' not in p.parts and '.private.' not in p.name and d.is_relative_to(E) and '..' not in d.parts
    assert p.is_file() and not p.is_symlink() and x['bytes']<5_000_000
    raw=p.read_bytes();assert len(raw)==x['bytes'] and sha(raw)==x['sha256'],str(p)
    if d in plans:assert plans[d]==raw
    plans[d]=raw
for d,raw in plans.items():
    if d.exists():assert d.read_bytes()==raw
    else:create(d,raw)
record={'kind':'Original independent R9 normal local verification event/custody carried without replay',
    'mathematical_candidate':'e654e98642350a615c473bc8190fbc1d47fe52bd',
    'reader_author_commit':'1d0dedf3aac3c2ff72ee96566461e29e38a2eeae','held_metadata_commit':head,
    'normal_verifier':'/root/mv_fresh_source_6e28','normal_API_calls':1,'normal_API_failures':0,
    'root_VERIFIED_calls':0,'event_replayed':False,'append_sha256':sha(append),'full_original_V_payload_sha256':sha(payloadraw),
    'all21_original_PL_values_inline_unchanged':True,'API_receipt_sha256':sha((R/'normal-API-receipt.json').read_bytes()),
    'foreign_preservation':guard,'private_full_guards_exported':False,
    'byte_original_destinations_copied_or_verified':len(plans),'declared_manifest_records':174,
    'postseal_custody_corrections_preserved':True,'local_preflight_failures_preserved':5,
    'original_native_math':'PASS','original_production_reader':'FAIL',
    'proposed_CSS_candidate':'CONDITIONAL_PASS_UNAPPLIED','public_T_API_main_result_credit':False,
    'integration_publication_purification_Goal':'HOLD; no original-owner release or production repair application claimed'}
rp=E/'actual-original-independent-VERIFIED-carrier.json';create(rp,dump(record))
paths=[C,L,rp]
for p in sorted(plans):
    before=subprocess.run(['git','show',f'{head}:{p}'],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    if before.returncode or before.stdout!=p.read_bytes():paths.append(p)
spec=W/'original-normal-VERIFIED-paths.private.nul';create(spec,b'\0'.join(str(p).encode() for p in paths)+b'\0')
subprocess.run(['git','add','-f','--pathspec-from-file='+str(spec),'--pathspec-file-nul'],check=True)
assert set(git('diff','--cached','--name-only').decode().splitlines())==set(map(str,paths))
subprocess.run(['git','diff','--cached','--check','--',str(C),str(L)],check=True)
subprocess.run(['git','commit','--quiet','-m','Carry original independent actual Gaussian matrix variance verification'],check=True)
commit=git('rev-parse','HEAD').decode().strip()
for p in paths:assert git('show',f'{commit}:{p}')==p.read_bytes()
assert not git('diff','HEAD','--name-only')
assert Path('runs/substantive_discoveries.jsonl').read_bytes()==discovery
summary={k:record[k] for k in ['mathematical_candidate','reader_author_commit','held_metadata_commit','normal_API_calls','normal_API_failures','root_VERIFIED_calls','append_sha256','full_original_V_payload_sha256','byte_original_destinations_copied_or_verified','original_production_reader','proposed_CSS_candidate']}
summary.update({'VERIFIED_event_carrier_commit':commit,'changed_carried_files':len(paths)})
create(W/'actual-original-independent-VERIFIED-commit.json',dump(summary))
print(json.dumps(summary))
