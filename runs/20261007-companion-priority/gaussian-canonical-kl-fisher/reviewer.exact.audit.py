from pathlib import Path
import json, subprocess, hashlib, datetime, re, sys, concurrent.futures
root=Path(r'E:/Samplinglib'); run=root/'runs/20261007-companion-priority/gaussian-canonical-kl-fisher'; prefix=run.relative_to(root).as_posix(); commit='19b569ae0fe37c97da0f98b4d1f4933ebabc7052'; py=sys.executable
sha=lambda b:hashlib.sha256(b).hexdigest()
lf=lambda b:b.replace(b'\r\n',b'\n').replace(b'\r',b'\n')
load=lambda p:json.loads((root/p).read_text(encoding='utf-8-sig'))
def write(p,j):(run/p).write_text(json.dumps(j,indent=2,ensure_ascii=False)+'\n',encoding='utf8')
files=['math-freeze.json','proved-local.json','publication-plan.json','whole-proof-review43/reviewer.math.review.json','whole-proof-review43/reviewer.math.run.json','whole-proof-review43/reviewer.math.checks.json','whole-proof-review43/reviewer.math.inputs.json','whole-proof-review43/reviewer.math.freeze-inputs.json','whole-proof-review43/reachability.analysis.json','source.1.review.json','source.review.repair1.lease.json','source.review.repair1.overlay-review.json','source.review.primary-first.contract.json','source.review.lease.json','source.review.checks.json','anonymous-decoder/run.json','anonymous-decoder/lease.json','anonymous-decoder/binding-receipt.json','anonymous-decoder/result0.json','exposition-provenance-overlay/repair.json']
pins=[]
def walk(j,owner,slot=''):
 if isinstance(j,dict):
  if isinstance(j.get('path'),str):
   hs={k:v for k,v in j.items() if 'sha256' in k.lower() and isinstance(v,str) and re.fullmatch('[0-9a-f]{64}',v)}
   if hs:pins.append({'owner':owner,'slot':slot,'path':j['path'],'expected':hs,'bytes':j.get('bytes')})
  for k,v in j.items():walk(v,owner,slot+'/'+k)
 elif isinstance(j,list):
  for i,v in enumerate(j):walk(v,owner,slot+'/'+str(i))
for f in files:walk(load(prefix+'/'+f),f)
results=[]; bypath={}
for pin in pins:
 p=Path(pin['path']); p=p if p.is_absolute() else root/p
 if not p.exists(): results.append({**pin,'status':'MISSING'}); continue
 b=p.read_bytes(); hashes={'raw':sha(b),'lf':sha(lf(b))}
 mismatch=[]
 for k,v in pin['expected'].items():
  norm='lf' if 'lf' in k.lower() else 'raw'
  if v!=hashes[norm]: mismatch.append(k)
 if pin['bytes'] is not None and pin['bytes']!=len(b):mismatch.append('bytes')
 result={**pin,'actual':hashes,'actual_bytes':len(b),'status':'PASS' if not mismatch else 'MISMATCH','mismatches':mismatch}; results.append(result)
 if p.is_relative_to(root):bypath[p.relative_to(root).as_posix()]=b
tracked=subprocess.check_output(['git','ls-tree','-r','--name-only',commit],cwd=root).decode().splitlines(); tracked=set(tracked)
gitresults=[]
for p,b in bypath.items():
 if p not in tracked:
  gitresults.append({'path':p,'status':'NOT_IN_COMMIT'}); continue
 blob=subprocess.check_output(['git','show',commit+':'+p],cwd=root)
 gitresults.append({'path':p,'blob_oid':subprocess.check_output(['git','rev-parse',commit+':'+p],cwd=root).decode().strip(),'git_raw_sha256':sha(blob),'git_lf_sha256':sha(lf(blob)),'working_raw_sha256':sha(b),'working_lf_sha256':sha(lf(b)),'raw_identical':b==blob,'lf_identical':lf(b)==lf(blob),'status':'PASS' if lf(b)==lf(blob) else 'FAIL'})
# Also check every committed file introduced by exact proof commit (metadata evidence plus mathematical production).
newpaths=subprocess.check_output(['git','diff-tree','--no-commit-id','--name-only','-r',commit],cwd=root).decode().splitlines()
for p in newpaths:
 if p in bypath:continue
 b=(root/p).read_bytes(); blob=subprocess.check_output(['git','show',commit+':'+p],cwd=root)
 gitresults.append({'path':p,'git_raw_sha256':sha(blob),'git_lf_sha256':sha(lf(blob)),'working_raw_sha256':sha(b),'working_lf_sha256':sha(lf(b)),'raw_identical':b==blob,'lf_identical':lf(b)==lf(blob),'status':'PASS' if lf(b)==lf(blob) else 'FAIL'})
write('reviewer.exact.bindings.json',{'commit':commit,'pins':results,'git_blobs':gitresults})
print('PINS',len(results),'PASS',sum(x['status']=='PASS' for x in results),'GIT',len(gitresults),'FAIL',sum(x['status']!='PASS' for x in gitresults))
for x in results:
 if x['status']!='PASS': print(json.dumps(x,ensure_ascii=False))
# Run independent metadata gates; no compiler or site generation.
commands=[['tools/astis_publication.py','packet','--cell','ASTIS-SW-SPHMC-standardized-rgo-kl-fisher'],['tools/astis_publication.py','check','--base','origin/main'],['tools/astis_semantic_roundtrip.py','check'],['tools/astis_frontier_cells.py','check'],['tools/astis_contributor_contract.py','check','--base','origin/main'],['git','diff','--check','origin/main']]
def check(i,c):
 start=datetime.datetime.now(datetime.timezone.utc).isoformat(); cmd=c if c[0]=='git' else [py]+c
 r=subprocess.run(cmd,cwd=root,stdout=subprocess.PIPE,stderr=subprocess.STDOUT); (run/f'reviewer.exact.check.{i}.log').write_bytes(r.stdout)
 return {'command':cmd,'exit_code':r.returncode,'started_utc':start,'finished_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'log':prefix+f'/reviewer.exact.check.{i}.log','raw_sha256':sha(r.stdout),'tail':r.stdout.decode('utf8',errors='replace')[-1500:]}
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as ex:checks=list(ex.map(lambda z:check(*z),enumerate(commands)))
write('reviewer.exact.checks.json',checks)
for c in checks:print(json.dumps(c,ensure_ascii=False))
