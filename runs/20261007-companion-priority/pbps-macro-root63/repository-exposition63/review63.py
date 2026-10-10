from pathlib import Path
import json,hashlib,os,sys,subprocess,time,gzip,re
ROOT=Path('E:/Samplinglib');BASE=ROOT/'runs/20261007-companion-priority/pbps-macro-root63';OUT=BASE/'repository-exposition63'
COMMIT='ee6bdf211d0ef8c9db63ecd199a52fa8cbbb81c4';SCI='4d02622332d02d0bd6c977d3cee48fd535ebf203';ACTOR='/root/exact_science63';PY='C:/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe'
CELL='research-wiki/frontier-cells/ASTIS-SW-PBPS-unique-macroscopic-defect-root.json'
DECL='AutoSamplingTheory.ExampleCases.ProximalBPS.MacroscopicDefectRoot.actual_unique_positive_macroscopic_defect_root'
MAIN='AutoSamplingTheory/ExampleCases/ProximalBPS/MacroscopicDefectRoot.lean';TEST='Tests/ProximalBPSMacroscopicDefectRoot.lean'
def sha(b):return hashlib.sha256(b).hexdigest()
def compact(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def load(p):return json.loads(Path(p).read_bytes().decode('utf-8-sig'))
def write(name,x):
 p=OUT/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes((json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode());return p
def rawpin(p):
 p=Path(p);b=p.read_bytes();lf=b.replace(b'\r\n',b'\n');return {'path':p.as_posix(),'raw_bytes':len(b),'raw_sha256':sha(b),'lf_bytes':len(lf),'lf_sha256':sha(lf)}
def git(*args):return subprocess.check_output(['git',*args],cwd=ROOT,stderr=subprocess.DEVNULL).decode().strip()
def abspath(s):
 p=Path(s);return p if p.is_absolute() else ROOT/p
def strings(x):
 if isinstance(x,str):yield x
 elif isinstance(x,list):
  for v in x:yield from strings(v)
 elif isinstance(x,dict):
  for v in x.values():yield from strings(v)
def freeze():
 assert git('rev-parse','HEAD')==COMMIT and git('rev-parse',COMMIT+'^')==SCI
 OUT.mkdir(parents=True,exist_ok=True);write('lease.json',{'status':'OPEN','actor':ACTOR,'exact_checked_commit':COMMIT,'opened_utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),'actual_pid':os.getpid(),'only_owned_prefix':OUT.as_posix(),'shared_or_Git_or_ledger_writes_authorized':False})
 names=['integration.notes.json','visual.inspection.json','root.exact-verification63.adoption.json','exact-step-code63.manifest.json','installation63.json']
 paths={BASE/p for p in names};paths|={ROOT/p for p in [MAIN,TEST,CELL,'AutoSamplingTheory.lean','Tests.lean','AutoSamplingTheory/TechnicalLemmas/Registry.lean','website/content/declaration_lessons/pbps-unique-positive-macroscopic-defect-root.json','website/content/publications/pbps-unique-positive-macroscopic-defect-root.json','research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261009-PBPSUniquePositiveMacroscopicDefectRoot.json','lean-toolchain','lake-manifest.json']}
 for p in (BASE/'integration63').rglob('*'):
  if p.is_file() and not any(v.startswith(('commit-integration','push-integration')) for v in p.relative_to(BASE/'integration63').parts):paths.add(p)
 for name in names:
  for s in strings(load(BASE/name)):
   if '\n' in s or len(s)>500 or ':' in s.replace('\\','/')[3:]:continue
   p=abspath(s)
   if p.is_file() and p.stat().st_size<20000000 and OUT not in p.parents:paths.add(p)
 # Pin the closed science capsule, rather than replaying its raw proof transcripts.
 for name in ['lease.json','native.receipt.json','transition.result.json','bindings.result.json','focused.result.json','run.json','named-verification.payload.json','input.manifest.json']:
  paths.add(BASE/'exact-science-verification'/name)
 # Bounded generated reader surfaces referenced by the visual capsule.
 vis=load(BASE/'visual.inspection.json')
 for p in [ROOT/'_site'/'library/proximal-bps.html',ROOT/'_site'/'lean-branches.json']:
  if p.is_file():paths.add(p)
 rows=[]
 for i,p in enumerate(sorted(paths)):
  row=rawpin(p)
  if row['raw_bytes']<20000000:
   q=OUT/'inputs'/f'{i:04}.exactraw.snapshot';q.parent.mkdir(exist_ok=True);q.write_bytes(p.read_bytes());row['exact_raw_snapshot']=q.as_posix()
  else:row['storage']='large input retained in place; hash pinned before review'
  rows.append(row)
 write('input.manifest.json',{'exact_checked_commit':COMMIT,'science_parent':SCI,'git_tree':git('rev-parse',COMMIT+'^{tree}'),'initial_git_status':git('status','--porcelain'),'read_before_any_independent_gate':True,'input_artifacts':rows,'excluded_uncommitted64':'All64 scratch, newcell and working ledger tail excluded from mathematical/repository credit','actual_pid':os.getpid()})
 print(json.dumps({'status':'FROZEN_BOUNDED_REPOSITORY_INPUTS','files':len(rows),'actual_pid':os.getpid()}))
def scalar():
 n=load(BASE/'integration.notes.json');print('notes',{k:v for k,v in n.items() if k not in ['checks']})
 for c in n['checks']:
  r=load(abspath(c['receipt']['path']));print('receipt',c['label'],{k:v for k,v in r.items() if not isinstance(v,(dict,list))})
 v=load(BASE/'visual.inspection.json');print('visual_keys',list(v.keys()));print('visual_scalar',{k:v for k,v in v.items() if not isinstance(v,(dict,list))});print('visual_lists',[(k,len(val)) for k,val in v.items() if isinstance(val,list)])
 for name in ['root.exact-verification63.adoption.json','integration63/owned-before.json','integration63/newline-preservation.json']:
  x=load(BASE/name);print(name,{k:v for k,v in x.items() if not isinstance(v,(dict,list))})
 print('integration_prod_changed',[p for p in git('diff','--name-only',SCI,COMMIT).splitlines() if not p.startswith('runs/')])
if __name__=='__main__':{'freeze':freeze,'scalar':scalar}[sys.argv[1]]()
