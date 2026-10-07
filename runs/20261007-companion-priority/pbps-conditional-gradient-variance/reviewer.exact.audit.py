from pathlib import Path
import json,hashlib,subprocess,sys,re,datetime,concurrent.futures
r=Path('E:/Samplinglib');prefix='runs/20261007-companion-priority/pbps-conditional-gradient-variance';run=r/prefix;commit='53f65a50263c13823aef5da7d9a3279de3514243';base='dca5e62b06d8cf2eab388dcb5e68af3bdb7dfb2b'
sha=lambda b:hashlib.sha256(b).hexdigest();lf=lambda b:b.replace(b'\r\n',b'\n').replace(b'\r',b'\n')
load=lambda p:json.loads((r/p).read_text(encoding='utf-8-sig'))
def bind(p):
 b=p.read_bytes();return {'path':p.relative_to(r).as_posix(),'bytes':len(b),'raw_sha256':sha(b),'lf_sha256':sha(lf(b))}
def put(p,j):p.write_text(json.dumps(j,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=r).decode().strip()==commit
assert load(prefix+'/reviewer.exact.focused.status.json')['exit_code']==0
fs=['math-freeze.json','proved-local.json','publication-plan.json','whole-proof-review48/receipt.json','whole-proof-review48/run.json','whole-proof-review48/input-bindings.json','whole-proof-review48/final-freeze-input-bindings.json','whole-proof-review48/compiler-evidence-audit.json','whole-proof-review48/direct-dependency-audit.json','source.0.review.json','source.1.review.json','source.review.checks.json','source.review.overlay1.checks.json','source.review.lease.json','source.1.review.lease.json','reviewer.source.lease.json','reviewer.source.1.lease.json','source.review.primary-first.lease.json','source.review.primary-first.contract.json','anonymous-decoder/run.json','anonymous-decoder/lease.json','anonymous-decoder/binding-receipt.json','publication-metadata-overlay48/repair.json']
pins=[]
def walk(j,owner,slot=''):
 if isinstance(j,dict):
  if isinstance(j.get('path'),str):
   hs={k:v for k,v in j.items() if k in ['raw_sha256','lf_sha256','sha256'] and isinstance(v,str) and re.fullmatch('[0-9a-f]{64}',v)}
   if hs:pins.append({'owner':owner,'slot':slot,'path':j['path'],'hashes':hs,'bytes':j.get('bytes',j.get('raw_bytes'))})
  for k,v in j.items():walk(v,owner,slot+'/'+k)
 elif isinstance(j,list):
  for i,v in enumerate(j):walk(v,owner,slot+'/'+str(i))
for f in fs:walk(load(prefix+'/'+f),f)
mr=load(prefix+'/whole-proof-review48/run.json')
for path,x in mr['outputs'].items():walk({'path':path,**x},'whole-proof-review48/run.json','/outputs/'+path)
snapshots={}
for p in run.rglob('*'):
 if p.is_file() and not p.name.startswith('reviewer.exact.'):
  b=p.read_bytes();snapshots.setdefault(sha(b),[]).append(p)
results=[];bypath={}
for x in pins:
 path=Path(x['path']);candidates=[path] if path.is_absolute() else [r/path,run/Path(x['owner']).parent/path]
 def match(b):return all(sha(lf(b) if 'lf' in k else b)==v for k,v in x['hashes'].items()) and (x['bytes'] is None or len(b)==x['bytes'])
 actual=next((p for p in candidates if p.is_file() and match(p.read_bytes())),None);status='PASS_STRICT_CURRENT'
 if actual is None:
  h=x['hashes'].get('raw_sha256',x['hashes'].get('sha256'));matches=[p for p in snapshots.get(h,[]) if match(p.read_bytes())];actual=matches[0] if matches else None;status='PASS_HISTORICAL_SNAPSHOT' if actual else 'UNRESOLVED'
 ap=actual.relative_to(r).as_posix() if actual and actual.is_relative_to(r) else str(actual)
 results.append({**x,'status':status,'actual_path':ap})
 if actual and actual.is_relative_to(r):bypath[ap]=actual.read_bytes()
# Byte-preserving dictionary schema and payload hashes, without rewriting any producer object.
digests=[]
def logical(path,key,ensure_ascii=False,payload=None):
 j=load(path);q=payload if payload is not None else {k:v for k,v in j.items() if k!=key};h=sha(json.dumps(q,ensure_ascii=ensure_ascii,sort_keys=True,separators=(',',':'),allow_nan=False).encode());digests.append({'path':path,'key':key,'expected':j[key],'actual':h,'status':'PASS' if h==j[key] else 'FAIL'});assert h==j[key],path
for f in ['source.0.review.json','source.1.review.json','source.review.overlay1.checks.json']:logical(prefix+'/'+f,'review_run_sha256')
for f in ['source.review.lease.json','source.1.review.lease.json','reviewer.source.lease.json','reviewer.source.1.lease.json','source.review.primary-first.lease.json']:logical(prefix+'/'+f,'lease_run_sha256')
ar=load(prefix+'/anonymous-decoder/run.json');logical(prefix+'/anonymous-decoder/run.json','decoder_run_sha256',payload=ar['execution_payload'])
assert sha((run/'whole-proof-review48/lease.json').read_bytes())==mr['closed_lease_sha256']
for name in ['packet0.json','result0.json','run.json','lease.json']:
 p=r/'.astis/decoder-48'/name
 if p.exists():assert p.read_bytes()==(run/'anonymous-decoder'/name).read_bytes();bypath[(run/'anonymous-decoder'/name).relative_to(r).as_posix()]=(run/'anonymous-decoder'/name).read_bytes()

# Mathlib API exact selected spans and whole pinned blobs.
apis=[];mc='db584cd6d46c92f209a44c0f1c829460d327499d';mathroot=r/'.lake/packages/mathlib'
for x in load(prefix+'/whole-proof-review48/api-bindings.json'):
 p=Path(x['path']);b=p.read_bytes();a,z=x['span'];fragment=b''.join(b.splitlines(keepends=True)[a-1:z]);assert sha(b)==x['whole_raw_sha256'] and sha(lf(b))==x['whole_lf_sha256'] and sha(fragment)==x['fragment_raw_sha256'] and sha(lf(fragment))==x['fragment_lf_sha256']
 bc=subprocess.check_output(['git','show',mc+':'+p.relative_to(mathroot).as_posix()],cwd=mathroot);assert lf(b)==lf(bc);apis.append({**x,'Git_blob_raw_sha256':sha(bc),'status':'PASS_PINNED_WHOLE_AND_FRAGMENT'})

# Every relevant committed current/snapshot byte has its exact Git LF representation checked.
tracked={x.split('\t',1)[1]:x.split()[2] for x in subprocess.check_output(['git','ls-tree','-r',commit],cwd=r).decode().splitlines()}
for p in subprocess.check_output(['git','diff-tree','--no-commit-id','--name-only','-r',commit],cwd=r).decode().splitlines():
 if p.startswith(prefix) or p in ['AutoSamplingTheory/ExampleCases/ProximalBPS/ConditionalGradientVariance.lean','Tests/ProximalBPSConditionalGradientVariance.lean','website/content/publications/pbps-conditional-gradient-variance.json','website/content/declaration_lessons/pbps-conditional-gradient-variance.json','research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261007-PBPSConditionalGradientVariance.json','research-wiki/frontier-cells/ASTIS-SW-PBPS-conditional-gradient-variance.json']:bypath[p]=(r/p).read_bytes()
paths=[p for p in bypath if p in tracked];batch=subprocess.run(['git','cat-file','--batch'],cwd=r,input=('\n'.join(tracked[p] for p in paths)+'\n').encode(),stdout=subprocess.PIPE,check=True).stdout;pos=0;gitrows=[]
for p in paths:
 end=batch.index(b'\n',pos);size=int(batch[pos:end].split()[2]);pos=end+1;b=batch[pos:pos+size];pos+=size+1;actual=bypath[p];gitrows.append({'path':p,'working_raw_sha256':sha(actual),'Git_blob_raw_sha256':sha(b),'LF_identical':lf(actual)==lf(b)});assert lf(actual)==lf(b),p
untracked=[p for p in bypath if p not in tracked and not p.startswith('.lake/packages/mathlib/')]
for p in untracked:
 assert p.startswith('.astis/decoder-48/'),p
 p1=Path(p).name;portable=(run/'anonymous-decoder'/p1)
 if p1=='lease.json' and bypath[p]!=portable.read_bytes():portable=run/'anonymous-decoder/initial-lease.raw.snapshot.json'
 assert bypath[p]==portable.read_bytes(),p

source0=load(prefix+'/source.0.review.json');source1=load(prefix+'/source.1.review.json');overlay=load(prefix+'/source.review.overlay1.checks.json')
assert source0['blocking'] and source0['mathematical_source_comparison']=='equivalent-after-elaboration' and len(source0['deltas'])==3
assert not source1['blocking'] and source1['verdict']=='equivalent-after-elaboration' and not source1['deltas'] and not source1['repairs'] and not source1['source_excess']
assert source1['review_run_sha256']=='2209b2a16e6d79b410b5395d23540db43e427d21286c48f71ef1a18f7c7c09bf'
assert source1['original_review_run_sha256']==source0['review_run_sha256'] and source1['overlay_review_run_sha256']==overlay['review_run_sha256']
assert overlay['no_TeX_or_newline_repair'] and overlay['production_Test_original_raw_bytes_identical']
assert overlay['exact_diff']['publication']==['/items/0/chapter_path'] and overlay['exact_diff']['lesson']==['/units/0/astis_dependencies','/units/0/mathlib_dependencies']
origsource0pins={x['path']:x for x in source0['input_artifacts']};originalbytes={}
for path in ['website/content/publications/pbps-conditional-gradient-variance.json','website/content/declaration_lessons/pbps-conditional-gradient-variance.json']:
 originalbytes[path]=snapshots[origsource0pins[path]['raw_sha256']][0].read_bytes()
def diff(a,b,p=''):
 if type(a)!=type(b):return [p]
 if isinstance(a,dict):return sum((diff(a.get(k),b.get(k),p+'/'+k) for k in sorted(set(a)|set(b))),[])
 if isinstance(a,list):
  if len(a)!=len(b):return [p]
  return sum((diff(x,y,p+'/'+str(i)) for i,(x,y) in enumerate(zip(a,b))),[])
 return [] if a==b else [p]
pubpath='website/content/publications/pbps-conditional-gradient-variance.json';lessonpath='website/content/declaration_lessons/pbps-conditional-gradient-variance.json';pubold=json.loads(originalbytes[pubpath]);pubnew=load(pubpath);lessonold=json.loads(originalbytes[lessonpath]);lessonnew=load(lessonpath)
assert diff(pubold,pubnew)==['/items/0/chapter_path']
assert lessonold['units'][0]['steps']==lessonnew['units'][0]['steps'] and lessonold['units'][0]['formula']==lessonnew['units'][0]['formula']
expected=json.loads(json.dumps(lessonold));expected['units'][0]['mathlib_dependencies']=[x.replace('InnerProductSpace.inner_gradient_left','inner_gradient_left') for x in expected['units'][0]['mathlib_dependencies']];expected['units'][0]['astis_dependencies'].append('AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.Poincare.variance_nonneg');assert expected==lessonnew
assert pubnew['items'][0]['chapter_path']=='example-cases/samplewiki/companions/proximal-bouncy-particle.html'
prod=(r/'AutoSamplingTheory/ExampleCases/ProximalBPS/ConditionalGradientVariance.lean').read_text();start=prod.index('theorem reflected_conditional_gradient_variance');header=(prod[start:prod.index(' := by',start)]+'\n').encode();assert len(header)==1356 and sha(header)=='770bb0bac75b2f2c94fc72e68c1a5a19a1d4642cd2fcf15ea71b9aa608a65e61'
compiled=(run/'reviewer.exact.focused.log').read_text();axioms=re.findall(r'depends on axioms:\s*\[([^\]]+)\]',compiled);assert len(axioms)==3 and all(set(x.replace('\n',' ').replace('\r',' ').replace(' ','').split(','))=={'propext','Classical.choice','Quot.sound'} for x in axioms)

# Bounded fresh data gates plus production/Test-only whitespace check.
sys.path.insert(0,str(r));sys.path.insert(0,str(r/'tools'));from tools import astis
cs=[['tools/astis_publication.py','packet','--cell','ASTIS-SW-PBPS-conditional-gradient-variance'],['tools/astis_publication.py','check','--base','origin/main'],['tools/astis_semantic_roundtrip.py','check'],['tools/astis_frontier_cells.py','check'],['tools/astis_contributor_contract.py','check','--base','origin/main'],['git','-c','core.whitespace=cr-at-eol','diff','--check',base,commit,'--','AutoSamplingTheory/ExampleCases/ProximalBPS/ConditionalGradientVariance.lean','Tests/ProximalBPSConditionalGradientVariance.lean']]
def check(z):
 i,c=z;cmd=c if c[0]=='git' else [sys.executable,*c];started=datetime.datetime.now(datetime.timezone.utc).isoformat();res=subprocess.run(cmd,cwd=r,stdout=subprocess.PIPE,stderr=subprocess.STDOUT);p=run/f'reviewer.exact.check.{i}.log';p.write_bytes(res.stdout);return {'command':cmd,'exit_code':res.returncode,'started_utc':started,'finished_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),**bind(p),'tail':res.stdout.decode('utf-8',errors='replace')[-450:]}
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:checks=list(pool.map(check,enumerate(cs)))
fake=astis.lean_diagnostics()
leases=[]
for name in ['compiler.lease.json','whole-proof-review48/lease.json','anonymous-decoder/lease.json','source.review.lease.json','source.1.review.lease.json','reviewer.source.lease.json','reviewer.source.1.lease.json','source.review.primary-first.lease.json']:
 j=load(prefix+'/'+name);assert j.get('status',j.get('state'))=='CLOSED';leases.append({'binding':bind(run/name),'fields':{k:v for k,v in j.items() if ('lease' in k or k in ['status','state','compiler','read','write','Python','opened_utc','closed_utc','compiler_started']) and not isinstance(v,(dict,list))}})
out={'checked_commit':commit,'pins':results,'Git_blobs':gitrows,'ignored_immutable_portable_mapping':untracked,'Mathlib_API_fragments':apis,'logical_digest_checks':digests,'wholemath_run_raw':bind(run/'whole-proof-review48/run.json'),'source0_raw':bind(run/'source.0.review.json'),'source1_raw':bind(run/'source.1.review.json'),'source_overlay_raw':bind(run/'source.review.overlay1.checks.json'),'exact_overlay_diff':{'publication':diff(pubold,pubnew),'lesson':diff(lessonold,lessonnew)},'statement_seal':{'LF_bytes':len(header),'LF_sha256':sha(header)},'compiler_status':load(prefix+'/reviewer.exact.focused.status.json'),'compiled_standard_axiom_sets':axioms,'fresh_checks':checks,'fake_closure':fake['totals'],'actual_closed_parent_leases':leases}
put(run/'reviewer.exact.bindings.json',out)
summary={'pins':len(results),'strict':sum(x['status']=='PASS_STRICT_CURRENT' for x in results),'historical':sum(x['status']=='PASS_HISTORICAL_SNAPSHOT' for x in results),'unresolved':[x for x in results if x['status']=='UNRESOLVED'],'Git_paths':len(gitrows),'Mathlib_API_fragments':len(apis),'checks':[(x['exit_code'],x['tail']) for x in checks],'fake':fake['totals']};put(run/'reviewer.exact.summary.json',summary);print(json.dumps(summary,ensure_ascii=False))
assert not summary['unresolved'];assert all(x['exit_code']==0 for x in checks);assert fake['totals']['forbidden_hits']==0
