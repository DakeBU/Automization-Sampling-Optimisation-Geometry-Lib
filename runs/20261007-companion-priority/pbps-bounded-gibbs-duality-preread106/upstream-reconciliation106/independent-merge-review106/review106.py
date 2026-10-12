from pathlib import Path
import json, hashlib, subprocess, datetime
R=Path('E:/Samplinglib'); D=Path(__file__).parent; U=D.parent
C='8b25d43e477db682be0227f14ce8140859567fc1'; T='26dce3a7442577b8bdfbfb20e8b77f681c052528'
V=R/'runs/20261007-companion-priority/pbps-actual-bounded-gibbs-duality106/exact-commit-verification106'
def git(*args): return subprocess.check_output(['git',*args],cwd=R)
def blob(ref,p):
 q=subprocess.run(['git','show',ref+':'+p],cwd=R,capture_output=True)
 return q.stdout if q.returncode==0 else None
def sha(b): return hashlib.sha256(b).hexdigest()
def info(p):
 b=p.read_bytes();return dict(path=p.relative_to(R).as_posix(),raw_sha256=sha(b),bytes=len(b))
def norm(b):return (b or b'').replace(b'\r\n',b'\n')
def save(n,o):
 p=D/n;assert not p.exists();p.write_text(json.dumps(o,indent=2)+'\n',encoding='utf8',newline='\n');return info(p)
assert git('rev-parse','HEAD').decode().strip()==C
assert git('rev-parse','MERGE_HEAD').decode().strip()==T
B=git('merge-base',C,T).decode().strip()
assert not git('ls-files','-u').strip()
paths=git('diff','--cached','--name-only').decode().splitlines(); assert len(paths)==43
incoming=git('diff','--name-only',B,T).decode().splitlines();assert set(paths)==set(incoming)
conflicts=json.loads((U/'conflict-paths106.json').read_bytes());assert len(conflicts)==4
rows=[];ledger_results=[]
for p in paths:
 base,ours,theirs,index=[blob(ref,p) for ref in [B,C,T,'']]
 assert index is not None
 if p in ['runs/substantive_advances.jsonl','runs/substantive_discoveries.jsonl']:
  old=ours.splitlines(); incoming_lines=theirs.splitlines(); baseline=base.splitlines()
  def subseq(a,b):
   it=iter(b);return all(any(x==y for y in it) for x in a)
  assert subseq(baseline,old) and subseq(baseline,incoming_lines)
  extras=[x for x in incoming_lines if x not in set(old)]
  assert index.splitlines()==old+extras, p
  assert index.startswith(ours),('exact ledger prefix',p)
  assert [json.loads(x) for x in index.splitlines()]==[json.loads(x) for x in old+extras]
  suffix=index[len(ours):]; assert suffix.splitlines()==extras
  if p.endswith('advances.jsonl'):
   stages=U/'normalized-merge';assert (stages/'3.stage2.raw').read_bytes()==ours
   assert (stages/'3.stage1.raw').read_bytes()==base and (stages/'3.stage3.raw').read_bytes()==theirs
   es=[json.loads(x) for x in index.splitlines()]
   states={}
   for e in es:
    if 'to_state' in e:states[e['advance_id']]=e['to_state']
   assert states['ASTIS-SA-20261012-PBPSActualBoundedGibbsDuality']=='VERIFIED'
   assert [k for k,v in states.items() if v=='STABILIZING']==['ASTIS-SA-20261011-PBPSActualPrescribedPathDensity']
  ledger_results.append(dict(path=p,old_events=len(old),upstream_new_events=len(extras),merged_events=len(index.splitlines()),exact_ours_RAW_prefix=True,both_histories_preserved=True,tail_sha256=sha(suffix)))
  mechanism='exact ours RAW prefix plus only upstream new events'
 elif p=='Tests/Basic.lean':
  assert norm(index)==norm(ours).replace(b'formalizedTechnicalLemmaCount = 557',b'formalizedTechnicalLemmaCount = 559')
  mechanism='only count 557 to 559; two new registry entries'
 elif norm(ours)==norm(base):
  assert norm(index)==norm(theirs),p
  mechanism='upstream exact content; EOL presentation allowed'
 else:
  temp=D/'reconstruction';temp.mkdir(exist_ok=True)
  for label,data in [('ours',ours),('base',base),('theirs',theirs)]: (temp/label).write_bytes(norm(data))
  q=subprocess.run(['git','merge-file','-p',str(temp/'ours'),str(temp/'base'),str(temp/'theirs')],cwd=R,capture_output=True)
  assert q.returncode==0,(p,q.stderr)
  assert q.stdout==norm(index),p
  mechanism='independent LF-normalized three-way reconstruction'
 rows.append(dict(path=p,index_blob=git('rev-parse',':'+p).decode().strip(),raw_sha256=sha(index),bytes=len(index),ours_raw_sha256=sha(ours) if ours else None,theirs_raw_sha256=sha(theirs) if theirs else None,mechanism=mechanism))
reg=norm(blob('',conflicts[0]));oldreg=norm(blob(C,conflicts[0]));assert reg.count(b'key :=')==oldreg.count(b'key :=')+2
assert reg.count(b'key := "geometry.sphere-rayleigh-gradient"')==1 and reg.count(b'key := "geometry.sphere-rayleigh-critical-eigenvectors"')==1
for i,p in enumerate(conflicts[:3]):
 for s,ref in [(1,B),(2,C),(3,T)]:assert (U/'normalized-merge'/f'{i}.stage{s}.raw').read_bytes()==blob(ref,p)
pre=json.loads((U/'premerge106.json').read_bytes());assert pre['head']==C
dirty=[]
for row in pre['dirty_tracked_RAW']:
 assert sha((R/row['path']).read_bytes())==row['raw_sha256'],('dirty RAW',row['path'])
 dirty.append(row)
assert not set(x['path'] for x in dirty)&set(paths)
frontier=[]
for row in pre['frontier_RAW']:
 if row['path'] not in paths:assert sha((R/row['path']).read_bytes())==row['raw_sha256'],('frontier RAW',row['path'])
 frontier.append(row)
manifest=json.loads((V/'closed-RAW-manifest106.json').read_bytes());collab=manifest['preserved_collaborator_inputs'];assert len(collab)==21
for row in collab:assert sha((R/row['path']).read_bytes())==row['raw_sha256'],('collaborator RAW',row['path'])
protected=git('ls-tree','-r','--name-only',C,'AutoSamplingTheory/ExampleCases/ProximalBPS','runs/20261007-companion-priority/pbps-actual-bounded-gibbs-duality106','runs/20261007-companion-priority/pbps-bounded-gibbs-duality-preread106','runs/semantic-roundtrip/anonymous106','website/content/declaration_lessons/pbps-actual-bounded-gibbs-duality.json','website/content/publications/pbps-actual-bounded-gibbs-duality.json','research-wiki/frontier-cells/ASTIS-SW-PBPS-actual-bounded-gibbs-duality.json','research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261012-PBPSActualBoundedGibbsDuality.json').decode().splitlines()
for p in protected:assert blob('',p)==blob(C,p),('protected index',p)
assert sha((R/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualBoundedGibbsDuality.lean').read_bytes())=='4fad17d78149b7a4a784170309e9de3f70941ef533f90228b0405dee5fc2707d'
inputs=[info(p) for p in [U/'premerge106.json',U/'resolution106.json',U/'merge-result106.json',U/'conflict-paths106.json',V/'closed-RAW-manifest106.json']]
decision=save('decision106.native.json',dict(status='ACCEPT_BOUNDED_MERGE_RESOLUTION',reviewer='/root/exact_verifier96',checked_ours=C,checked_theirs=T,merge_base=B,staged_paths=43,conflicts=4,registry_delta='557 + 2 = 559',checks=dict(exact_incoming_scope=True,independent_threeway_reconstruction=True,all91_premerge_dirty_RAW_preserved=len(dirty)==91,all21_collaborator_RAW_preserved=True,unrelated_frontier_RAW_preserved=True,protected_committed_paths_unchanged=len(protected),production106_RAW_unchanged=True,sole94_STABILIZING_preserved=True,SAU106_VERIFIED_preserved=True),ledger_results=ledger_results,scope='Read-only merge resolution audit. No new math audit, no PBPS main-merge or purification credit. Root owns Tests and commit.',inputs=inputs))
record=save('run106.native.json',dict(status='PASS',utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),decision=decision,staged_blobs=rows,protected_paths=protected,preserved_dirty_inputs=dirty,preserved_collaborator_inputs=collab,inputs=inputs))
closed=save('closed-RAW106.native.json',dict(status='CLOSED',parents=[C,T],inputs=inputs,outputs=[decision,record,info(Path(__file__))],preserved_collaborator_inputs=collab))
print(json.dumps(dict(decision=decision,run=record,closed=closed)))
