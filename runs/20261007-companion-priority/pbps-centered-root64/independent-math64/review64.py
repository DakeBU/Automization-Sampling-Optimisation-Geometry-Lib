from pathlib import Path
import json,hashlib,subprocess,os,sys,time,re,shutil
ROOT=Path('E:/Samplinglib');BASE=ROOT/'runs/20261007-companion-priority/pbps-centered-root64';OUT=BASE/'independent-math64';ACTOR='/root/exact_science63';COMMIT='ee6bdf211d0ef8c9db63ecd199a52fa8cbbb81c4'
def sha(b):return hashlib.sha256(b).hexdigest()
def compact(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def load(p):return json.loads(Path(p).read_bytes().decode('utf-8-sig'))
def write(n,x):p=OUT/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes((json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode());return p
def rawpin(p):p=Path(p);b=p.read_bytes();return {'path':p.as_posix(),'raw_bytes':len(b),'raw_sha256':sha(b),'lf_sha256':sha(b.replace(b'\r\n',b'\n'))}
def git(*a):return subprocess.check_output(['git',*a],cwd=ROOT).decode().strip()
def diffs(a,b,p=''):
 if isinstance(a,dict) and isinstance(b,dict):
  z=[]
  for k in sorted(set(a)|set(b)):z+=diffs(a.get(k),b.get(k),p+'/'+k)
  return z
 return [] if a==b else [{'field':p,'before':a,'after':b}]
def supplement():
 s=load(BASE/'lesson-dependency64/supplement.json');original={x['path']:x for x in load(OUT/'input.manifest.json')['inputs']};rows=[]
 for i,m in enumerate(s['finite_historical_maps']):
  p=Path(m['original']['path']);q=Path(m['explicit_exact_raw_snapshot']['path']);assert sha(q.read_bytes())==m['original']['raw_sha256']==original[p.as_posix()]['raw_sha256'];assert q.read_bytes()==Path(original[p.as_posix()]['exact_RAW_snapshot']).read_bytes()
  d=diffs(load(q),load(p));rows.append({'map':m,'current':rawpin(p),'exact_structured_diff':d})
  own=OUT/'inputs'/f'supp-current-{i}.exactraw.snapshot';own.write_bytes(p.read_bytes())
 for p in [BASE/'lesson-dependency64/supplement.json']+[Path(m['explicit_exact_raw_snapshot']['path']) for m in s['finite_historical_maps']]:
  q=OUT/'inputs'/('supp-'+p.name);q.write_bytes(p.read_bytes())
 write('input.supplement.json',{'actual_pid':os.getpid(),'status':'FINITE_EXPLICIT_HISTORY_QUALIFIED_BEFORE_COMPILER','supplement':rawpin(BASE/'lesson-dependency64/supplement.json'),'qualified_maps':rows,'explanation':'Already compiled shared ingredient appended to lesson dependency list and draft publication context; no statement/formula/excerpt/Lean/header change. Original129-input freeze retained unchanged.'})
 write('observer-preflight-failure.json',{'failure':'Initial own compile preflight rejected changed original lesson/audit RAW pins before launching Lake.','Lean_launched':False,'actual_preflight_pid':'not captured by exploratory tool; not invented','resolution':'Exact root supplement supplies two finite original-to-RAW snapshots; independently equal to own frozen snapshots. Current inputs newly pinned before actual compile.','mathematical_failure':False})
 print('QUALIFIED_TWO_EXPLICIT_METADATA_MAPS',os.getpid())
def compile():
 assert git('rev-parse','HEAD')==COMMIT
 maps={m['map']['original']['path']:m for m in load(OUT/'input.supplement.json')['qualified_maps']};pre=[]
 for row in load(OUT/'input.manifest.json')['inputs']:
  p=Path(row['path']);cur=rawpin(p)
  if cur['raw_sha256']!=row['raw_sha256']:assert cur==maps[p.as_posix()]['current']
  pre.append(cur)
 pre.append(rawpin(BASE/'lesson-dependency64/supplement.json'));write('compile.before.json',{'actual_pid':os.getpid(),'inputs':pre})
 d=OUT/'focused';d.mkdir(exist_ok=True);cmd=[shutil.which('lake'),'build','Tests.ProximalBPSCenteredRootOrderInverse'];start=time.time()
 with (d/'stdout.log').open('wb') as out,(d/'stderr.log').open('wb') as err:
  proc=subprocess.Popen(cmd,cwd=ROOT,stdout=out,stderr=err);code=proc.wait()
 post=[rawpin(Path(x['path'])) for x in pre]
 write('focused/receipt.json',{'command':cmd,'cwd':ROOT.as_posix(),'actual_foreground_pid':proc.pid,'observer_pid':os.getpid(),'started_unix':start,'finished_unix':time.time(),'exit_code':code,'terminal_closed':True,'checked_BASE':COMMIT,'candidate_uncommitted':True,'pre':pre,'post':post,'pre_post_equal':pre==post,'stdout':rawpin(d/'stdout.log'),'stderr':rawpin(d/'stderr.log')})
 assert pre==post and code==0
 print(json.dumps({'status':'COMPILED_PRECOMMIT','actual_foreground_pid':proc.pid,'exit_code':code,'terminal_closed':True,'stable_RAW_LF_pins':len(pre)}));print((d/'stdout.log').read_text(encoding='utf-8',errors='replace')[-2500:])
if __name__=='__main__':{'supplement':supplement,'compile':compile}[sys.argv[1]]()
