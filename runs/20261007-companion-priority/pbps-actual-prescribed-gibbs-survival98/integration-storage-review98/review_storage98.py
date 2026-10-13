from pathlib import Path
import hashlib,json,gzip,subprocess,sys,datetime
R=Path('E:/Samplinglib');O=Path(__file__).resolve().parent;B=O.parent;V=B/'exact-commit-verification98';I=B/'integration98'
C='170e1bad1f0887512b79c4b5711ce316ade5f511';INT='1f42ab322465acf7a62e4d0e28cc045b4c22e4e4';SCI='530a58f7c036a67787956b20d2d390890ec2fec7';ORIG='9525bc0ea88a96e64ef20a53d2a92b9c8a5b966e';MAIN='f4f8d3a8ef0d4918cb30c333540a303b501ffc63';PRIOR='49fdfd309151b30f6371767dd74d698d440a8974'
PRIMARY='d81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760';sha=lambda b:hashlib.sha256(b).hexdigest()
def rel(p):return str(p).replace('\\','/').removeprefix('E:/Samplinglib/')
def load(p):return json.loads((R/rel(p)).read_bytes())
def info(p):
 p=R/rel(p);b=p.read_bytes();return dict(path=rel(p),raw_sha256=sha(b),bytes=len(b))
def save(n,x):
 p=O/n;assert not p.exists();p.write_bytes((json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode())
def git(*args):return subprocess.check_output(['git',*args],cwd=R,stderr=subprocess.PIPE)
assert git('rev-parse','HEAD').decode().strip()==C
assert git('rev-parse',C+'^1').decode().strip()==INT and git('rev-parse',C+'^2').decode().strip()==MAIN
assert git('rev-parse',INT+'^').decode().strip()==SCI and git('rev-parse',SCI+'^').decode().strip()==ORIG
main_delta=git('diff','--name-only',INT,C).decode().splitlines();assert set(main_delta)=={'README.md','docs/math-2-0-positioning.md','website/scripts/math_2_0.py'}
tree={l.split('\t',1)[1]:l.split()[2] for l in git('ls-tree','-r',C).decode().splitlines()};cache={}
def blob(p):
 p=rel(p)
 if p not in cache:cache[p]=git('cat-file','blob',tree[p])
 return cache[p]
stage=load(B/'science-staging98.json');im=load(I/'immutable-integration-RAW-archives98.json');closed=load(V/'closed-RAW-manifest98.json');freeze=load(V/'input-freeze98.json')
assert info(V/'closed-RAW-manifest98.json')['raw_sha256']=='c55a93f9ff0e8bb12b8af1153fa4b3f8260ab524b12e0b0cc9582b341288f140'
assert blob(I/'immutable-integration-RAW-archives98.json')==(I/'immutable-integration-RAW-archives98.json').read_bytes()
# Batch only bounded admitted evidence scopes; never run proof or state-transition tools.
scope=set(stage['files'])|{p for p in tree if p.startswith(rel(V)+'/')}|{x['archive'] for x in im['files']}
p=subprocess.Popen(['git','cat-file','--batch'],cwd=R,stdin=subprocess.PIPE,stdout=subprocess.PIPE)
for path in sorted(scope):
 assert path in tree,path;p.stdin.write((tree[path]+'\n').encode());p.stdin.flush();head=p.stdout.readline().split();bb=p.stdout.read(int(head[2]));assert p.stdout.read(1)==b'\n';cache[path]=bb
p.stdin.close();assert p.wait()==0
byhash={};archive_rows=[]
for path in scope:
 b=blob(path);rb=gzip.decompress(b) if path.endswith('.gz') else b
 assert sha(rb)!=PRIMARY,('full primary redistributed',path)
 byhash.setdefault(sha(rb),dict(archive=path,archive_raw_sha256=sha(b)) if path.endswith('.gz') else dict(snapshot=path))
for x in im['files']:
 ab=blob(x['archive']);rb=gzip.decompress(ab);assert sha(ab)==x['archive_raw_sha256'] and sha(rb)==x['raw_sha256'] and rb==(R/x['raw_path']).read_bytes(),x['raw_path']
 if x['public_text_raw_sha256'] is not None:assert sha(blob(x['raw_path']))==x['public_text_raw_sha256']
 archive_rows.append(x)
for x in stage['raw_archives']:
 assert sha(blob(x['archive']))==x['archive_sha256'] and sha(gzip.decompress(blob(x['archive'])))==x['raw_sha256'],x['archive']
resolved=[]
for x in closed['owned_artifacts']+[info(V/'closed-RAW-manifest98.json')]:
 assert info(x['path'])['raw_sha256']==x['raw_sha256'],('immutable verifier artifact changed',x['path'])
 assert x['raw_sha256'] in byhash,('verifier RAW not in current tree',x['path'])
 resolved.append(dict(path=x['path'],raw_sha256=x['raw_sha256'],location=byhash[x['raw_sha256']]))
def resolve(x):
 h=x['raw_sha256'];path=x['path']
 if h in byhash:return byhash[h]
 if x.get('git_commit'):
  assert subprocess.run(['git','merge-base','--is-ancestor',x['git_commit'],C],cwd=R).returncode==0
  assert sha(git('show',x['git_commit']+':'+x.get('snapshot',path)))==h;return dict(git_commit=x['git_commit'],snapshot=x.get('snapshot',path))
 if x.get('archive'):
  ab=blob(x['archive']);assert sha(gzip.decompress(ab))==h;return dict(archive=x['archive'],archive_raw_sha256=sha(ab))
 if x.get('snapshot'):
  assert sha(blob(x['snapshot']))==h;return dict(snapshot=x['snapshot'])
 assert path in tree and sha(blob(path))==h,('unpreserved science input',x);return dict(snapshot=path)
inputs=[]
for x in freeze['exact_commit_matches']:inputs.append(dict(path=x['path'],raw_sha256=x['raw_sha256'],location=resolve(x)))
for x in freeze['historical_reference_resolutions']:
 v=dict(path=rel(x['reference']['path']),raw_sha256=x['reference'].get('raw_sha256',x['reference'].get('sha256')));v.update({k:x[k] for k in ['archive','snapshot','git_commit'] if k in x});inputs.append(dict(path=v['path'],raw_sha256=v['raw_sha256'],location=resolve(v)))
for x in freeze['local_pinned_or_excluded_inputs']:assert info(x['path'])['raw_sha256']==x['raw_sha256']
collab=closed['preserved_collaborator_inputs'];assert len(collab)==21 and collab==stage['preserved_collaborator_inputs']
for x in collab:assert info(x['path'])['raw_sha256']==x['raw_sha256']
M='AutoSamplingTheory/ExampleCases/ProximalBPS/ActualPrescribedGibbsSurvival.lean';P='website/content/publications/pbps-actual-prescribed-gibbs-survival.json';A='research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261012-PBPSActualPrescribedGibbsSurvival.json';L='website/content/declaration_lessons/pbps-actual-prescribed-gibbs-survival.json';H=B.parent/'pbps-prescribed-gibbs-survival-preread98/Header98.lean'
for path in [M,P,A,L]:assert blob(path)==git('show',SCI+':'+path),(path,'science changed')
assert info(M)['raw_sha256']=='f4856a5f059ef9875e481830cbd1a6152d7bc7de690ed325a71390a791098b95'
assert info(H)['raw_sha256']=='50c6999fe069f4cf648832a804b71bb8e447b7a3aea0f0c42a836f81650c6ad0'
# Verify primary exclusion over every added/modified integration/merge blob, including compressed blobs.
delta=git('diff','--name-only','--diff-filter=ACMR',PRIOR,C).decode().splitlines()
for path in delta:
 b=blob(path);rb=gzip.decompress(b) if path.endswith('.gz') else b;assert sha(rb)!=PRIMARY,('full primary in delivery delta',path)
assert not any('/next-primary99/' in p or '/next-primary99-source-completion/' in p or '/pbps-finite-state-reversal-preread99/' in p for p in delta)
cell='research-wiki/frontier-cells/ASTIS-SW-PBPS-actual-prescribed-gibbs-survival.json';cv=json.loads(blob(cell));assert cv['status']=='independently_verified' and cv['evidence']['independent_verification']==rel(V/'verified.json')
assert info(cell)['raw_sha256']==load(V/'admission98.json')['cell']['raw_sha256']
ledger=blob('runs/substantive_advances.jsonl');events=[json.loads(l) for l in ledger.splitlines() if l.strip()];latest={}
# Read native event keys before classification; ledger format stores full advance data under record.
for e in events:
 if e.get('advance_id'):latest[e['advance_id']]=e
if not latest:
 print('EVENT_SCHEMA',list(events[-1]),flush=True)
 raise AssertionError('adapt ledger schema without mutation')
id98='ASTIS-SA-20261012-PBPSActualPrescribedGibbsSurvival';states={k:v.get('state',v.get('to_state')) for k,v in latest.items()}
assert states[id98]=='VERIFIED',latest[id98]
assert {k for k,v in states.items() if v=='STABILIZING'}=={'ASTIS-SA-20261011-PBPSActualPrescribedPathDensity'}
assert len([e for e in events if e.get('advance_id')==id98 and e.get('state',e.get('to_state'))=='VERIFIED'])==1
save('storage-review98.native.json',dict(kind='independent-bounded-integration-and-main-merge-storage-transfer',reviewer='/root/exact_verifier96',utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),decision='PASS_EXACT_STORAGE_AND_STATE_PRESERVATION',checked_commit=C,integration_commit=INT,independent_science_commit=SCI,original_science_commit=ORIG,merged_main=MAIN,main_merge_only_three_disjoint_paths=main_delta,integration_archives_verified=len(archive_rows),science_archives_verified=len(stage['raw_archives']),exact_verifier_artifact_resolutions=resolved,science_input_RAW_resolutions=inputs,all21collaborator_RAWs_preserved=True,full_primary_absent_from_delivery_delta=True,next99_excluded=True,production=info(M),Header98=info(H),production_publication_source_audit_and_lesson_unchanged_from_science=True,sole_stabilization_lane='ASTIS-SA-20261011-PBPSActualPrescribedPathDensity',SAU98_state='VERIFIED',one_VERIFIED_event=True,cell_state='independently_verified',no_shared_mutations=True,no_ledger_transition=True,no_mathematics_reaudit=True,boundary='Storage and narrow integration transfer only; root owns post-main affected build/source/site gates. No PR/push/main-merge-acceptance/purification/whole-paper credit from this receipt.'))
assert git('rev-parse','HEAD').decode().strip()==C
save('closed-RAW-storage-review98.native.json',dict(kind='closed-independent-integration-storage-review98',checked_commit=C,inputs=[info(B/'science-staging98.json'),info(I/'immutable-integration-RAW-archives98.json'),info(I/'staged-scope98.json'),info(V/'closed-RAW-manifest98.json'),info(V/'input-freeze98.json')],files=[info(p) for p in sorted(O.iterdir()) if p.is_file()],hash_algorithm='SHA256 original bytes without normalization',self_hash_intentionally_omitted=True))
for n in ['storage-review98.native.json','closed-RAW-storage-review98.native.json']:print(json.dumps(info(O/n)))
