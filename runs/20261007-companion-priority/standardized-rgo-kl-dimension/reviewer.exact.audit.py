from pathlib import Path
import json,hashlib,subprocess,datetime,sys,re,concurrent.futures
r=Path(r'E:/Samplinglib');run=r/'runs/20261007-companion-priority/standardized-rgo-kl-dimension';prefix=run.relative_to(r).as_posix();commit='76373366787499ebbc9e778fe568d0332233aef0';base='96565a16061f57f2c3e46b93680055b8a93dd44f';sha=lambda b:hashlib.sha256(b).hexdigest();lf=lambda b:b.replace(b'\r\n',b'\n').replace(b'\r',b'\n');load=lambda p:json.loads((r/p).read_text(encoding='utf-8-sig'))
sys.path.insert(0,str(r));sys.path.insert(0,str(r/'tools'));from tools import astis
fs=['math-freeze.json','proved-local.json','publication-plan.json','whole-proof-review45/reviewer.math.review.json','whole-proof-review45/reviewer.math.run.json','whole-proof-review45/reviewer.math.inputs.initial.json','whole-proof-review45/reviewer.math.inputs.final.json','whole-proof-review45/reviewer.math.additional-inputs.json','whole-proof-review45/reviewer.math.checks.json','whole-proof-review45/reachability.analysis.json','source.0.review.json','source.review.inputs.json','source.review.checks.json','source.review.lease.json','source.review.primary-first.contract.json','source.review.primary-first.lease.json','anonymous-decoder/run.json','anonymous-decoder/lease.json','anonymous-decoder/binding-receipt.json','anonymous-decoder/result0.json']
pins=[]
def walk(j,owner,slot=''):
 if isinstance(j,dict):
  if isinstance(j.get('path'),str):
   hs={k:v for k,v in j.items() if 'sha256' in k.lower() and isinstance(v,str) and re.fullmatch('[0-9a-f]{64}',v)}
   if hs:pins.append({'owner':owner,'slot':slot,'path':j['path'],'hashes':hs,'bytes':j.get('bytes')})
  for k,v in j.items():walk(v,owner,slot+'/'+k)
 elif isinstance(j,list):
  for i,v in enumerate(j):walk(v,owner,slot+'/'+str(i))
for f in fs:
 p=run/f
 if p.exists():walk(load(prefix+'/'+f),f)
# Map dictionary-keyed outputs and root-relative input manifest digest pairs with same raw byte contracts.
mr=load(prefix+'/whole-proof-review45/reviewer.math.run.json');ar=load(prefix+'/anonymous-decoder/run.json')
for owner,j in [('whole-proof-review45/reviewer.math.run.json',mr),('anonymous-decoder/run.json',ar)]:
 for k in ['outputs','output_artifacts']:
  rows=j.get(k,{})
  if isinstance(rows,dict):
   for p,item in rows.items():
    if isinstance(item,dict) and any('sha256' in z.lower() for z in item):walk({'path':p,**item},owner,'/'+k+'/'+p)
results=[];bypath={};snapshots={}
for p in run.rglob('*'):
 if p.is_file() and not p.name.startswith('reviewer.exact.'):
  b=p.read_bytes();snapshots.setdefault(sha(b),[]).append(p)
for x in pins:
 pp=Path(x['path']);candidates=[pp] if pp.is_absolute() else [r/pp,run/Path(x['owner']).parent/pp]
 p=next((p for p in candidates if p.exists()),None)
 def match(data):return all(sha(lf(data) if 'lf' in k.lower() else data)==v for k,v in x['hashes'].items()) and (x['bytes'] is None or len(data)==x['bytes'])
 if p and match(p.read_bytes()):status='PASS_STRICT_CURRENT';actual=p
 else:
  rawhash=next((v for k,v in x['hashes'].items() if 'raw' in k.lower()),None);matches=[p for p in snapshots.get(rawhash,[]) if match(p.read_bytes())];actual=matches[0] if matches else None;status='PASS_HISTORICAL_SNAPSHOT' if matches else 'UNRESOLVED'
 result={**x,'status':status,'actual_path':actual.relative_to(r).as_posix() if actual and actual.is_relative_to(r) else str(actual)};results.append(result)
 if actual and actual.is_relative_to(r):bypath[actual.relative_to(r).as_posix()]=actual.read_bytes()
# Wholemath relative19 outputs may be list already handled by walk; all manifest/hash bindings exact.
tracked=set(subprocess.check_output(['git','ls-tree','-r','--name-only',commit],cwd=r).decode().splitlines());git=[];mp=[];mathroot=r/'.lake/packages/mathlib';mathcommit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=mathroot).decode().strip();assert mathcommit=='db584cd6d46c92f209a44c0f1c829460d327499d'
newpaths=subprocess.check_output(['git','diff-tree','--no-commit-id','--name-only','-r',commit],cwd=r).decode().splitlines()
for p in newpaths:bypath.setdefault(p,(r/p).read_bytes())
for p,b in bypath.items():
 if p in tracked:
  bc=subprocess.check_output(['git','show',commit+':'+p],cwd=r);git.append({'path':p,'git_blob_raw_sha256':sha(bc),'git_blob_lf_sha256':sha(lf(bc)),'working_raw_sha256':sha(b),'raw_identical':bc==b,'lf_identical':lf(bc)==lf(b),'status':'PASS' if lf(bc)==lf(b) else 'FAIL'})
 elif p.startswith('.lake/packages/mathlib/'):
  rp=p.split('.lake/packages/mathlib/',1)[1];bc=subprocess.check_output(['git','show',mathcommit+':'+rp],cwd=mathroot);mp.append({'path':p,'Mathlib_commit':mathcommit,'blob_raw_sha256':sha(bc),'working_raw_sha256':sha(b),'lf_identical':lf(bc)==lf(b)})
 else:git.append({'path':p,'status':'NOT_IN_COMMIT'})
def hashcheck(path,key,payload=None):
 j=load(path);payload=payload if payload is not None else {k:v for k,v in j.items() if k!=key};matching=[]
 for ascii in [True,False]:
  for sort in [True,False]:
   h=sha(json.dumps(payload,ensure_ascii=ascii,sort_keys=sort,separators=(',',':'),allow_nan=False).encode())
   if h==j[key]:matching.append({'ensure_ascii':ascii,'sort_keys':sort,'compact':True,'no_newline':True})
 return {'path':path,'key':key,'sha256':j[key],'serializations':matching,'status':'PASS' if matching else 'UNRESOLVED'}
dig=[hashcheck(prefix+'/whole-proof-review45/reviewer.math.run.json','run_hash'),hashcheck(prefix+'/source.0.review.json','review_run_sha256'),hashcheck(prefix+'/source.review.lease.json','lease_run_sha256'),hashcheck(prefix+'/anonymous-decoder/run.json','decoder_run_sha256',ar['execution_payload'])]
# Additional plain named digests across review/manifests.
review=load(prefix+'/whole-proof-review45/reviewer.math.review.json');named=[]
for p,k in [('whole-proof-review45/reviewer.math.inputs.initial.json','initial_raw_sha256'),('whole-proof-review45/reviewer.math.inputs.final.json','final_raw_sha256'),('whole-proof-review45/reviewer.math.additional-inputs.json','additional_raw_sha256')]:
 expected=review['input_bindings'][k];actual=sha((run/p).read_bytes());assert expected==actual;named.append({'path':prefix+'/'+p,'expected':expected,'actual':actual,'status':'PASS'})
header=(r/'AutoSamplingTheory/ExampleCases/SmoothedPicardHMC/StandardizedRGOKLDimension.lean').read_text();start=header.index('theorem standardized_rgo_unique_prox_and_kl_le_dimension');h=(header[start:header.index(' := by',start)]+'\n').encode();assert len(h)==1357 and sha(h)=='6b54ac62b436aeb4032aafb15b12c26a5661450013151633e01da02dd08b163d'
# Fresh metadata only, scoped CR-aware diff only; no giant historical diagnostic replay.
owned=['AutoSamplingTheory/ExampleCases/SmoothedPicardHMC/StandardizedRGOKLDimension.lean','Tests/StandardizedRGOKLDimension.lean','research-wiki/frontier-cells/ASTIS-SW-SPHMC-standardized-rgo-kl-dimension.json','research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261007-StandardizedRGOKLDimension.json','website/content/declaration_lessons/standardized-rgo-kl-dimension.json','website/content/publications/standardized-rgo-kl-dimension.json']
cs=[['tools/astis_publication.py','packet','--cell','ASTIS-SW-SPHMC-standardized-rgo-kl-dimension'],['tools/astis_publication.py','check','--base','origin/main'],['tools/astis_semantic_roundtrip.py','check'],['tools/astis_frontier_cells.py','check'],['tools/astis_contributor_contract.py','check','--base','origin/main'],['git','-c','core.whitespace=cr-at-eol','diff','--check',base,commit,'--']+owned]
def check(z):
 i,c=z;cmd=c if c[0]=='git' else [sys.executable]+c;start=datetime.datetime.now(datetime.timezone.utc).isoformat();res=subprocess.run(cmd,cwd=r,stdout=subprocess.PIPE,stderr=subprocess.STDOUT);p=run/f'reviewer.exact.check.{i}.log';p.write_bytes(res.stdout);return {'command':cmd,'exit_code':res.returncode,'started_utc':start,'finished_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'log':p.relative_to(r).as_posix(),'raw_sha256':sha(res.stdout),'tail':res.stdout.decode('utf8',errors='replace')[-500:]}
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as ex:checks=list(ex.map(check,enumerate(cs)))
fake=astis.lean_diagnostics();out={'checked_commit':commit,'pins':results,'Git_blobs':git,'Mathlib_pins':mp,'digest_checks':dig,'wholemath_named_manifests':named,'statement_seal':{'bytes':len(h),'LF_sha256':sha(h)},'checks':checks,'fake_closure':{'files':fake['totals']['files'],'hits':fake['totals']['forbidden_hits']},'compiler':'NOT_STARTED_CLOSED'};(run/'reviewer.exact.bindings.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print('PINCOUNTS',len(results),'STRICT',sum(x['status']=='PASS_STRICT_CURRENT' for x in results),'HISTORICAL',sum(x['status']=='PASS_HISTORICAL_SNAPSHOT' for x in results),'GIT',len(git),'MATHLIB',len(mp),'FAKE',out['fake_closure'])
for x in results:
 if x['status']!='PASS_STRICT_CURRENT':print(json.dumps(x,ensure_ascii=False))
for x in git:
 if x['status']!='PASS':print('GIT',x)
print('DIGESTS',json.dumps(dig));print('CHECKS',json.dumps(checks,ensure_ascii=False))
