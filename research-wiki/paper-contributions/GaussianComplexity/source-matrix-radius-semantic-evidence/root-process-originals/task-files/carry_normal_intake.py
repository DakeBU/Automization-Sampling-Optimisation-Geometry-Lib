"""Freeze the actual one-time radius intake and its real source/receipt originals."""
from pathlib import Path
import hashlib
import json
import subprocess
W=Path(__file__).resolve().parent.relative_to(Path.cwd())
E=Path('research-wiki/paper-contributions/GaussianComplexity/source-matrix-radius-semantic-evidence')
SP=Path('research-wiki/paper-contributions/GaussianComplexity/source-matrix-radius-statement-seal.json')
C=Path('research-wiki/frontier-cells/ASTIS-SW-GAUSSIAN-COMPLEXITY-source-matrix-radius.json')
L=Path('runs/substantive_advances.jsonl')
sha=lambda raw:hashlib.sha256(raw).hexdigest()
dump=lambda obj:(json.dumps(obj,ensure_ascii=False,indent=2)+'\n').encode()
git=lambda *args:subprocess.check_output(['git',*args])
def create(p,raw):
    p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('xb') as f:f.write(raw)
head=git('rev-parse','HEAD').decode().strip()
assert head=='505879e768e94f446bddd790d9330bf43ca2ea76'
assert not git('diff','--cached','--name-only')
assert set(git('diff','HEAD','--name-only').decode().splitlines())=={str(L)}
append=(E/'normal-EXPLORING-append.exact.jsonl').read_bytes()
assert sha(append)=='791117a0325f05a8d48451eb834062da3b1c763b6924f861877de5c8a834cfb4'
assert L.read_bytes()==git('show',f'{head}:{L}')+append
events=[json.loads(x) for x in append.splitlines()]
assert len(events)==3 and [x.get('state',x.get('to_state')) for x in events]==['PROPOSED','CLAIMED','EXPLORING']
sourcefiles=['start_radius_sau.attempt1.original.py','complete_radius_intake_after_schema_correction.py',
    'reserved-cell.schema-attempt1.original.json','intake-schema-attempt1-diagnosis.json',
    'normal-intake-attempted.once.json','reviewed-preproof-inputs.json']
for n in sourcefiles:create(E/'intake-originals'/n,(W/n).read_bytes())
for stem,exitcode in [
    ('20261113T002736521664Z-source-matrix-radius-normal-source-admitted-intake',1),
    ('20261113T003045452370Z-source-matrix-radius-normal-intake-after-project-label-correction',0),
    ('20261113T002339246901Z-source-matrix-radius-actual-environment-before-intake',0)]:
    rp=Path('.astis/huanjian-resume-20261103')/(stem+'.receipt.json')
    r=json.loads(rp.read_bytes());log=Path(r['log'])
    assert r['exit_code']==exitcode and sha(log.read_bytes())==r['log_sha256']
    for p in [rp,log]:create(E/'intake-originals/actual-runs'/p.name,p.read_bytes())
summary=json.loads((E/'normal-intake-preservation.json').read_bytes())
qualification={'historical_and_control_artifact_count':summary['actual_control_files_preserved'],
    'scope':'All files captured from runs (including historical artifacts) plus named .astis global control/queue/runtime roots. This is not a count of literal queues.',
    'all_existing_tracked_artifacts_count':summary['all_existing_tracked_bytes_modes_index_preserved_except_exact_ledger_append'],
    'full_foreign_states_and_index_snapshots_private':True,'initial_schema_failure_before_any_API':True,
    'actual_intake_API_calls':3,'target_formal_proof_calls':0,'root_VERIFIED_calls':0}
create(E/'intake-originals/control-scope-qualification.json',dump(qualification))
paths=[SP,C,L,*[p for p in sorted(E.rglob('*')) if p.is_file()]]
assert all('.private.' not in p.name for p in paths)
spec=W/'normal-intake-paths.private.nul';create(spec,b'\0'.join(str(p).encode() for p in paths)+b'\0')
subprocess.run(['git','add','-f','--pathspec-from-file='+str(spec),'--pathspec-file-nul'],check=True)
assert set(git('diff','--cached','--name-only').decode().splitlines())==set(map(str,paths))
subprocess.run(['git','diff','--cached','--check','--',str(C),str(SP),str(L)],check=True)
subprocess.run(['git','commit','--quiet','-m','Admit exact original Gaussian summand radius source packet'],check=True)
commit=git('rev-parse','HEAD').decode().strip()
for p in paths:assert git('show',f'{commit}:{p}')==p.read_bytes()
assert not git('diff','HEAD','--name-only')
result={**summary,'intake_carrier_commit':commit,'byte_exact_public_files':len(paths),'control_count_qualification':qualification['scope']}
create(W/'actual-normal-intake-commit.json',dump(result))
print(json.dumps(result))
