"""Record explicit user resume without replaying proof/ledger events."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,subprocess
W=Path(__file__).resolve().parent.relative_to(Path.cwd())
E=Path('research-wiki/paper-contributions/GaussianComplexity/source-matrix-radius-semantic-evidence')
C=Path('research-wiki/frontier-cells/ASTIS-SW-GAUSSIAN-COMPLEXITY-source-matrix-radius.json')
A=Path('research-wiki/semantic-roundtrip/audits/huanjian-gaussian-source-matrix-radius.json')
L=Path('runs/substantive_advances.jsonl')
sha=lambda b:hashlib.sha256(b).hexdigest()
dump=lambda o:(json.dumps(o,ensure_ascii=False,indent=2)+'\n').encode()
git=lambda *a:subprocess.check_output(['git',*a])
def create(p,b):
    p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('xb') as f:f.write(b)
head=git('rev-parse','HEAD').decode().strip();assert head=='49206ff8355cff54423c7758d0a7bdc8ad137252'
assert not git('diff','HEAD','--name-only') and not git('diff','--cached','--name-only')
ledger=L.read_bytes();audit=json.loads(A.read_bytes())
assert audit['publication_binding_sha256']=='7081c71690e9b29aa32cd09b9e093358d2660a231066384243784fa4654c64fa'
assert audit['source_review']['state']=='accepted'
assert sha((E/'actual-PROVED_LOCAL-evidence.full.json').read_bytes())=='e2ca572ea630b2a9df348206e21fb92f36c43954cbb6c83a02e8e8144bdd34c7'
assert len(json.loads((E/'actual-PROVED_LOCAL-evidence.full.json').read_bytes()))==25
env=json.loads((W/'actual-environment-at-resume.json').read_bytes())
owner=json.loads((W/'original-owner-at-resume.json').read_bytes())
dest=E/'resume-20261113/originals'
for n in ['verify_environment.py','observe_original_owner.py','actual-environment-at-resume.json','original-owner-at-resume.json','hold_resume_candidate.py']:create(dest/n,(W/n).read_bytes())
runs=Path('.astis/huanjian-resume-20261103')
for p in sorted(runs.glob('*radius-resume-*.receipt.json')):
    r=json.loads(p.read_bytes());log=Path(r['log']);assert r['exit_code']==0 and sha(log.read_bytes())==r['log_sha256']
    for f in [p,log]:create(dest/'actual-runs'/f.name,f.read_bytes())
record={'recorded_utc':datetime.now(timezone.utc).isoformat(),'user_instruction':'好我们继续做gaussian的','prior_pause_commit':head,'action':'Resume same unfinished Goal; finish R10 independent acceptance before next SAU.','mathematics_changed':False,'proof_source_and_decoder_evidence_reused_only_if_hash_unchanged':True,'current_state':'PROVED_LOCAL;normalV0','base_for_final_metadata_gates':'50097800f60ad4a95cab1e47be200b629ce5e7a6','environment':{'file':str(dest/'actual-environment-at-resume.json'),'sha256':sha((W/'actual-environment-at-resume.json').read_bytes()),'actual_packages':len(env['packages'])},'original_owner':{'file':str(dest/'original-owner-at-resume.json'),'sha256':sha((W/'original-owner-at-resume.json').read_bytes()),'released':False,'exact_main':owner['refs'][0]['commit']},'upload_failure':'Original HTTP408 remains recorded; no unchanged upload retry or main/shared integration.','normal_ledger_calls':0,'normal_VERIFIED_calls_by_ROOT':0,'remaining':'Native conditional visual review; final held-commit4metadata gates; independent full private guards and exactly-once verification. OriginalreaderFAIL and unappliedCSS remain separate from local math V.'}
create(E/'resume-20261113/resume.json',dump(record))
cell=json.loads(C.read_bytes());assert cell['status']=='proved_locally'
cell['paused_by_user']['active']=False
cell['paused_by_user']['resumed_by_user']=True
cell['resumed_by_user']={'instruction':'好我们继续做gaussian的','evidence':str(E/'resume-20261113/resume.json'),'current_normal_state':'PROVED_LOCAL','normal_ledger_calls':0}
C.write_bytes(dump(cell));assert L.read_bytes()==ledger
paths=[C,*[p for p in sorted((E/'resume-20261113').rglob('*')) if p.is_file()]]
spec=W/'held-paths.private.nul';create(spec,b'\0'.join(str(p).encode() for p in paths)+b'\0')
subprocess.run(['git','add','-f','--pathspec-from-file='+str(spec),'--pathspec-file-nul'],check=True)
assert set(git('diff','--cached','--name-only').decode().splitlines())==set(map(str,paths))
subprocess.run(['git','diff','--cached','--check'],check=True)
subprocess.run(['git','commit','--quiet','-m','Resume Gaussian radius acceptance with unchanged proof and source seals'],check=True)
commit=git('rev-parse','HEAD').decode().strip()
for p in paths:assert git('show',f'{commit}:{p}')==p.read_bytes()
result={'held_commit':commit,'base':'50097800f60ad4a95cab1e47be200b629ce5e7a6','exact_owned_metadata_files':len(paths),'math_changed':False,'ledger_changed':False,'ROOT_normalV_calls':0}
create(W/'actual-held-resume-commit.json',dump(result));print(json.dumps(result))
