from pathlib import Path
import json,hashlib,subprocess
W=Path(__file__).resolve().parent.relative_to(Path.cwd())
E=Path('research-wiki/paper-contributions/GaussianComplexity/source-matrix-radius-semantic-evidence')
C=Path('research-wiki/frontier-cells/ASTIS-SW-GAUSSIAN-COMPLEXITY-source-matrix-radius.json')
L=Path('runs/substantive_advances.jsonl')
sha=lambda b:hashlib.sha256(b).hexdigest()
dump=lambda o:(json.dumps(o,ensure_ascii=False,indent=2)+'\n').encode()
git=lambda *a:subprocess.check_output(['git',*a])
def create(p,b):
    p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('xb') as f:f.write(b)
head=git('rev-parse','HEAD').decode().strip();assert head=='8ec8fc501901a6c9aa90f63048f2f865aec183ab'
assert not git('diff','--cached','--name-only')
assert set(git('diff','HEAD','--name-only').decode().splitlines())=={str(C),str(L)}
append=(E/'actual-PROVED_LOCAL-append.exact.jsonl').read_bytes()
assert sha(append)=='cd0fe1d69bf33d3db43c6646d27c46135d205ff67f27c60175164fd8f99b6360'
assert L.read_bytes()==git('show',f'{head}:{L}')+append
payload=(E/'actual-PROVED_LOCAL-evidence.full.json').read_bytes()
assert sha(payload)=='e2ca572ea630b2a9df348206e21fb92f36c43954cbb6c83a02e8e8144bdd34c7'
event=json.loads(append);assert event['to_state']=='PROVED_LOCAL' and event['evidence']==json.loads(payload)
originals=E/'root-process-originals'
for p in sorted(W.rglob('*')):
    if not p.is_file() or '.private.' in p.name or p.suffix not in {'.py','.lean','.json','.txt','.md','.jsonl'}:continue
    b=p.read_bytes()
    if p.suffix=='.json':
        v=json.loads(b)
        if isinstance(v,dict):assert not set(v)&{'tracked_git_index','all_foreign_states','all_existing_tracked_fingerprints','actual_control_fingerprints'},'private guard export refused'
    create(originals/'task-files'/p.relative_to(W),b)
R=Path('.astis/huanjian-resume-20261103')
for p in sorted(R.glob('*source-matrix-radius-*.receipt.json')):
    if p.name<'20261113T011700':continue
    r=json.loads(p.read_bytes());log=Path(r['log']);assert sha(log.read_bytes())==r['log_sha256']
    for x in [p,log]:create(originals/'actual-runs'/x.name,x.read_bytes())
scope={'root_PROVED_LOCAL_API_calls':1,'root_VERIFIED_API_calls':0,'actual_append_sha256':sha(append),'full_original_payload_sha256':sha(payload),'private_control_or_index_snapshots_exported':False,'original_reader_status':'FAIL_MOBILE_TABLE_CLIPPED','conditional_CSS_proposal':'UNAPPLIED; separate candidate, not original reader acceptance','original_owner_release':False,'whole_goal':'UNFINISHED'}
create(originals/'scope.json',dump(scope))
paths=[C,L,E/'actual-PROVED_LOCAL-append.exact.jsonl',E/'actual-PROVED_LOCAL-evidence.full.json',E/'normal-PROVED_LOCAL-preservation.json',*[p for p in sorted(originals.rglob('*')) if p.is_file()]]
spec=W/'PROVED_LOCAL-carrier-paths.private.nul';create(spec,b'\0'.join(str(p).encode() for p in paths)+b'\0')
subprocess.run(['git','add','-f','--pathspec-from-file='+str(spec),'--pathspec-file-nul'],check=True)
assert set(git('diff','--cached','--name-only').decode().splitlines())==set(map(str,paths))
subprocess.run(['git','diff','--cached','--check','--',str(C),str(L)],check=True)
subprocess.run(['git','commit','--quiet','-m','Record one actual local Gaussian matrix radius proof advance'],check=True)
commit=git('rev-parse','HEAD').decode().strip()
for p in paths:assert git('show',f'{commit}:{p}')==p.read_bytes()
result={'PROVED_LOCAL_carrier_commit':commit,'exact_carried_files':len(paths),**scope}
create(W/'actual-PROVED_LOCAL-carrier-commit.json',dump(result));print(json.dumps(result))
