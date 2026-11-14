"""Carry the exact completed PL append once, using a small explicit allowlist."""
from pathlib import Path
import json,hashlib,subprocess
W=Path(__file__).resolve().parent.relative_to(Path.cwd())
E=Path('research-wiki/paper-contributions/GaussianComplexity/source-gram-realization-semantic-evidence')
C=Path('research-wiki/frontier-cells/ASTIS-SW-GAUSSIAN-COMPLEXITY-source-gram-realization.json')
L=Path('runs/substantive_advances.jsonl')
sha=lambda b:hashlib.sha256(b).hexdigest()
dump=lambda o:(json.dumps(o,ensure_ascii=False,indent=2)+'\n').encode()
git=lambda *a:subprocess.check_output(['git',*a])
def create(p,b):
 p.parent.mkdir(parents=True,exist_ok=True)
 with p.open('xb') as f:f.write(b)
cfg=json.loads((W/'PL-carrier-inputs.json').read_bytes())
head=git('rev-parse','HEAD').decode().strip()
assert head==cfg['parent_HEAD']
assert not git('diff','--cached','--name-only')
assert set(git('diff','HEAD','--name-only').decode().splitlines())=={str(C),str(L)}
append=(E/'actual-PROVED_LOCAL-append.exact.jsonl').read_bytes()
payload=(E/'actual-PROVED_LOCAL-evidence.full.json').read_bytes()
assert sha(append)==cfg['append_sha256'] and sha(payload)==cfg['payload_sha256']
assert L.read_bytes()==git('show',f'{head}:{L}')+append
event=json.loads(append)
assert event['advance_id']=='ASTIS-SA-20261113-GaussianComplexitySourceGramRealization'
assert event['to_state']=='PROVED_LOCAL' and event['evidence']==json.loads(payload)
originals=E/'root-PL-originals'
owned_names=['record_gram_proved_local.py','preservation_guard.py','normal-PL-inputs.json',
 'normal-PROVED_LOCAL-attempted.once.json','original-owner-current-after-C2.json',
 'carry_gram_proved_local.py','PL-carrier-inputs.json']
for name in owned_names:
 p=W/name;b=p.read_bytes()
 if p.suffix=='.json':
  o=json.loads(b)
  assert not set(o)&{'tracked_git_index','all_foreign_states','all_existing_tracked_fingerprints','actual_control_fingerprints'}
 create(originals/'task-files'/name,b)
receipt=Path(cfg['actual_PL_receipt']);r=json.loads(receipt.read_bytes())
log=Path(r['log']);assert r['exit_code']==0 and sha(log.read_bytes())==r['log_sha256']
for p in [receipt,log]:create(originals/'actual-runs'/p.name,p.read_bytes())
scope={'root_PROVED_LOCAL_API_calls':1,'root_VERIFIED_API_calls':0,
 'actual_append_sha256':sha(append),'full_original_payload_sha256':sha(payload),
 'explicit_task_originals_count':len(owned_names),'private_maps_exported':False,
 'production_shared_CSS_changed':False,'original_owner_release':False,
 'integration_publication_purification':'HELD','whole_goal':'UNFINISHED'}
create(originals/'scope.json',dump(scope))
paths=[C,L,E/'actual-PROVED_LOCAL-append.exact.jsonl',E/'actual-PROVED_LOCAL-evidence.full.json',
 E/'normal-PROVED_LOCAL-preservation.json',*[p for p in sorted(originals.rglob('*')) if p.is_file()]]
spec=W/'PROVED_LOCAL-carrier-paths.private.nul'
create(spec,b'\0'.join(str(p).encode() for p in paths)+b'\0')
subprocess.run(['git','add','-f','--pathspec-from-file='+str(spec),'--pathspec-file-nul'],check=True)
assert set(git('diff','--cached','--name-only').decode().splitlines())==set(map(str,paths))
subprocess.run(['git','diff','--cached','--check','--',str(C),str(L)],check=True)
subprocess.run(['git','commit','--quiet','-m','Record one local Gaussian source Gram realization proof advance'],check=True)
commit=git('rev-parse','HEAD').decode().strip()
for p in paths:assert git('show',f'{commit}:{p}')==p.read_bytes()
out={'PROVED_LOCAL_carrier_commit':commit,'exact_carried_files':len(paths),**scope}
create(W/'actual-PROVED_LOCAL-carrier-commit.json',dump(out))
print(json.dumps(out))
