from pathlib import Path
import hashlib,json,subprocess,difflib,re
R=Path('E:/Samplinglib');O=Path(__file__).resolve().parent;D=O.parent
H='0ccd3eb9609e544cf4db85bbbb6438ae20966fd5';T='c168d6703d27b4554cb3013023783479917a4ae7'
sha=lambda b:hashlib.sha256(b).hexdigest()
def git(*a):return subprocess.check_output(['git',*a],cwd=R,stderr=subprocess.PIPE)
def info(p):return dict(path=p.relative_to(R).as_posix(),raw_sha256=sha(p.read_bytes()),bytes=p.stat().st_size)
def save(n,v):
 p=O/n;assert not p.exists();p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def tree(c):return {x.split('\t',1)[1]:x.split()[2] for x in git('ls-tree','-r',c).decode().splitlines()}
def norm(b):return b.replace(b'\r\n',b'\n')
assert git('rev-parse','HEAD').decode().strip()==H and git('rev-parse','MERGE_HEAD').decode().strip()==T
assert not git('ls-files','-u').strip()
BASE=git('merge-base',H,T).decode().strip();trees={c:tree(c) for c in [BASE,H,T]}
idx={x.split('\t',1)[1]:x.split()[1] for x in git('ls-files','-s').decode().splitlines()}
cache={}
def byoid(oid):
 if oid not in cache:cache[oid]=git('cat-file','blob',oid)
 return cache[oid]
def blob(c,p):return byoid(trees[c][p]) if p in trees[c] else b''
def staged(p):return byoid(idx[p])
conflicts=['AutoSamplingTheory/TechnicalLemmas/Registry.lean','Tests.lean','Tests/Basic.lean','runs/substantive_advances.jsonl','runs/substantive_discoveries.jsonl']
resolution=json.loads((D/'resolution105.json').read_bytes());assert [x['path'] for x in resolution['files']]==conflicts
rows=[];ledger_rows=[]
for i,p in enumerate(conflicts):
 bs=[blob(c,p) for c in [BASE,H,T]]
 for j,b in enumerate(bs,1):assert (D/f'normalized-merge/{i}.stage{j}.raw').read_bytes()==b
 base,ours,theirs=map(norm,bs);out=staged(p)
 assert out==(R/p).read_bytes() and sha(out)==resolution['files'][i]['raw_sha256']
 if i<3:
  snapshots=[]
  for label,b in [('ours',ours),('base',base),('theirs',theirs)]:
   q=O/f'conflict{i}.{label}.lf';q.write_bytes(b);snapshots.append(q)
  q=subprocess.run(['git','merge-file','-p',*map(str,snapshots)],cwd=R,capture_output=True)
  expected=q.stdout
  if i==2:
   assert q.returncode==1
   pattern=rb'<<<<<<<[^\n]*\nexample : TechnicalLemmas.formalizedTechnicalLemmaCount = 555 := by native_decide\n=======\nexample : TechnicalLemmas.formalizedTechnicalLemmaCount = 489 := by native_decide\n>>>>>>>[^\n]*\n'
   expected,n=re.subn(pattern,b'example : TechnicalLemmas.formalizedTechnicalLemmaCount = 556 := by native_decide\n',expected);assert n==1
  else:assert q.returncode==0
  assert out==expected
 else:
  assert theirs.startswith(base)
  assert all(op in ('equal','insert') for op,*_ in difflib.SequenceMatcher(None,base.splitlines(),ours.splitlines(),autojunk=False).get_opcodes())
  tail=theirs[len(base):];assert all(x not in ours.splitlines() for x in tail.splitlines())
  assert out==ours+tail
  ev=[json.loads(x) for x in out.splitlines()];incoming=[json.loads(x) for x in tail.splitlines()]
  assert not any(x.get('advance_id')=='ASTIS-SA-20261012-PBPSActualCountableEndpointLaw' for x in incoming)
  ledger_rows.append(dict(path=p,ours_prefix_byte_exact=True,upstream_tail_exact=True,base_subsequence_both_parents=True,appended_events=len(incoming),appended_event_ids=[x.get('advance_id',x.get('discovery_id',x.get('id'))) for x in incoming]))
  if i==3:
   states={}
   for x in ev:
    if x.get('event')=='proposal':states[x['advance_id']]=x['state']
    if x.get('event')=='transition':states[x['advance_id']]=x['to_state']
   assert states['ASTIS-SA-20261012-PBPSActualCountableEndpointLaw']=='VERIFIED'
   assert [k for k,v in states.items() if v=='STABILIZING']==['ASTIS-SA-20261011-PBPSActualPrescribedPathDensity']
 rows.append(dict(path=p,index_blob=idx[p],staged_raw_sha256=sha(out),classification='independently reconstructed conflict resolution'))
changed=git('diff','--cached','--name-only',H).decode().splitlines()
for i,p in enumerate(changed):
 if p in conflicts:continue
 base,ours,theirs=[blob(c,p) for c in [BASE,H,T]];out=staged(p)
 if norm(ours)==norm(base):assert norm(out)==norm(theirs);kind='unchanged upstream blob'
 elif norm(theirs)==norm(base):assert norm(out)==norm(ours);kind='unchanged ours blob'
 else:
  fs=[]
  for label,b in [('ours',ours),('base',base),('theirs',theirs)]:
   q=O/f'automerge{i}.{label}.lf';q.write_bytes(norm(b));fs.append(q)
  q=subprocess.run(['git','merge-file','-p',*map(str,fs)],cwd=R,capture_output=True);assert q.returncode==0 and norm(out)==q.stdout,p;kind='independently reproduced clean three-way merge'
 assert norm((R/p).read_bytes())==norm(out),p
 rows.append(dict(path=p,index_blob=idx[p],staged_raw_sha256=sha(out),classification=kind))
pre=json.loads((D/'premerge105-v2.json').read_bytes());assert pre['head']==H
for x in pre['dirty_tracked_RAW']:assert sha((R/x['path']).read_bytes())==x['raw_sha256'],x['path']
assert not set(changed)&{x['path'] for x in pre['dirty_tracked_RAW']}
for x in pre['frontier_RAW']:assert sha((R/x['path']).read_bytes())==x['raw_sha256'],x['path']
B=R/'runs/20261007-companion-priority/pbps-actual-countable-endpoint105'
closed=json.loads((B/'exact-commit-verification105/closed-RAW-manifest105.json').read_bytes());collab=closed['preserved_collaborator_inputs'];assert len(collab)==21
for x in collab:assert sha((R/x['path']).read_bytes())==x['raw_sha256']
protected=[p for p in trees[H] if p.startswith(('AutoSamplingTheory/ExampleCases/ProximalBPS/','runs/semantic-roundtrip/anonymous105/','runs/20261007-companion-priority/pbps-actual-countable-endpoint105/final-source105/','runs/20261007-companion-priority/pbps-actual-countable-endpoint105/independent-whole-math105/'))]
for p in protected:assert idx[p]==trees[H][p],p
registry=staged(conflicts[0]);assert registry.count(b'key := "geometry.sphere-gradient-characterization"')==1
assert registry.count(b'key := "geometry.curve-extension-independence"')==1
assert len(re.findall(rb'status := LemmaMemoryStatus.formalizedLocal',registry))-len(re.findall(rb'status := LemmaMemoryStatus.formalizedLocal',blob(H,conflicts[0])))==1
assert git('rev-parse','HEAD').decode().strip()==H and git('rev-parse','MERGE_HEAD').decode().strip()==T
save('review105.native.json',{'decision':'ACCEPT_BOUNDED_MERGE_RESOLUTION','reviewer':'/root/exact_verifier96','ours':H,'theirs':T,'merge_base':BASE,'merge_uncommitted':True,'reviewed_index_paths':rows,'conflicts':conflicts,'ledger_preservation':ledger_rows,'registry_count':'555 plus exactly one sphere formalized entry = 556; prior curve and PBPS imports/entries preserved.','dirty_RAW_count':len(pre['dirty_tracked_RAW']),'dirty_RAWs_all_preserved':True,'existing_frontier_RAWs_all_preserved':True,'all21collaborator_RAWs_preserved':True,'protected105_and_PBPS_index_paths_unchanged':len(protected),'sole94_stabilizing_preserved':True,'105_VERIFIED_preserved':True,'science_proof_review_repeated':False,'shared_mutations':False,'defects':[],'boundary':'Resolution/content preservation only; root compiler/aggregate gates and later exact merge-commit delivery remain separate. No PBPS main merge, purification, browser or full-paper claim.'})
inputs=[D/'premerge105-v2.json',D/'merge-result105-v4.json',D/'resolution105.json',D/'resolve_merge105.py',B/'exact-commit-verification105/closed-RAW-manifest105.json']+list((D/'normalized-merge').glob('*.raw'))
save('run105.native.json',{'reviewer':'/root/exact_verifier96','ours':H,'theirs':T,'merge_base':BASE,'inputs':[info(p) for p in inputs],'index_blobs':rows,'result':info(O/'review105.native.json'),'no_shared_writes':True})
save('closed-RAW105.native.json',{'reviewer':'/root/exact_verifier96','inputs':[info(p) for p in inputs],'outputs':[info(p) for p in sorted(O.iterdir()) if p.is_file()],'preserved_collaborator_inputs':collab,'no_shared_writes':True})
for n in ['review105.native.json','run105.native.json','closed-RAW105.native.json']:print(n,info(O/n)['raw_sha256'])
