import os,sys,json,hashlib,datetime,subprocess,re,traceback,ast,builtins
from pathlib import Path
ROOT=Path('E:/Samplinglib');P=ROOT/'runs/20261007-companion-priority/pbps-actual-corrector-change71';O=P/'independent-math71';PRE=ROOT/'runs/20261007-companion-priority/pbps-corrector-change-preproof71';ACTOR='/root/exact_science63';CODE=ROOT/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualCorrectorChange.lean';PARENT=ROOT/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualProjectedRotation.lean';DECL='AutoSamplingTheory.ExampleCases.ProximalBPS.ActualCorrectorChange.actual_corrector_change';PY=sys.executable
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def sha(b):return hashlib.sha256(b).hexdigest()
def read(p):return json.loads(Path(p).read_bytes())
def get(n):return read(O/n)
def canon(x):return json.dumps(x,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()
def logical(d):return sha(canon({k:v for k,v in d.items() if k!='run_sha256'}))
def save(n,v):
 assert not(O/'lease.final.json').exists();p=O/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes((json.dumps(v,sort_keys=True,ensure_ascii=False,indent=2)+'\n').encode())
def pin(p):
 p=Path(p);b=p.read_bytes();lf=b.replace(b'\r\n',b'\n');return dict(path=p.as_posix(),raw_bytes=len(b),raw_sha256=sha(b),lf_bytes=len(lf),lf_sha256=sha(lf))
def checkpin(q):assert pin(q['path'])==q,('RAW/LF drift',q['path'])
def text(p):return Path(p).read_bytes().replace(b'\r\n',b'\n').decode('utf8')
def git(*args):return subprocess.check_output(['git',*args],cwd=ROOT)
def stable():
 for r in get('inputs.manifest.json')['inputs']:
  checkpin(r['original']);checkpin(r['RAW_snapshot']);checkpin(r['LF_snapshot'])
 if (O/'auxiliary.inputs.manifest.json').exists():
  for r in get('auxiliary.inputs.manifest.json')['inputs']:checkpin(r)
def freeze():
 O.mkdir(parents=True,exist_ok=True);save('lease.open.json',dict(status='OPEN',actor=ACTOR,actual_PID=os.getpid(),utc=now(),owned_scope=O.as_posix(),scope='Independent theorem mathematics only; no source final review/VERIFIED/canonical/Git/ledger writes.'))
 f=read(P/'mathematics-freeze71.json');assert f['RAW_module_sha256']==sha(CODE.read_bytes())=='f321d13c612a3702e3d42043a49fff8feb3b76bb302638a60f9dad4cb166ad1a';assert f['focused_PID']==49980 and f['focused_EXIT']==0 and f['focused_jobs']==3950 and f['axioms']==['propext','Classical.choice','Quot.sound']
 paths=[Path(r['path']) for r in f['inputs']]+[P/'mathematics-freeze71.json',P/'canonical71.frozen.exactraw.lean'];assert len(paths)==len(set(paths))==14
 rows=[]
 for i,p in enumerate(paths):
  q=pin(p)
  if i<len(f['inputs']):r=f['inputs'][i];assert q['raw_bytes']==r['RAW_bytes'] and q['raw_sha256']==r['RAW_sha256'] and q['lf_sha256']==r['LF_sha256']
  raw=O/f'inputs/{i:02}.RAW.snapshot';lf=O/f'inputs/{i:02}.LF.snapshot';raw.parent.mkdir(exist_ok=True);b=p.read_bytes();raw.write_bytes(b);lf.write_bytes(b.replace(b'\r\n',b'\n'));rows.append(dict(original=q,RAW_snapshot=pin(raw),LF_snapshot=pin(lf),root_frozen_input=i<len(f['inputs'])))
 assert CODE.read_bytes()==(P/'canonical71.frozen.exactraw.lean').read_bytes();head=git('rev-parse','HEAD').decode().strip();r=subprocess.run(['git','cat-file','-e',head+':'+CODE.relative_to(ROOT).as_posix()],cwd=ROOT,capture_output=True);save('git.baseline.json',dict(HEAD_at_freeze=head,actual_PID=os.getpid(),production_in_HEAD=r.returncode==0,theorem_only_uncommitted_bytes_not_exact_science_commit_review=True,current_parent_RAW=pin(PARENT),parent_git_blob_oid=git('rev-parse',head+':'+PARENT.relative_to(ROOT).as_posix()).decode().strip()))
 save('inputs.manifest.json',dict(status='FROZEN_BEFORE_FRESH_INDEPENDENT_COMPILER',actual_PID=os.getpid(),utc=now(),input_count=len(rows),root_frozen_count=12,additional_freeze_and_exact_module_snapshots=2,LF_recipe='Replace ONLY CRLF byte pairs with LF; preserve bare CR and every other byte; RAW authoritative.',inputs=rows,no_decoder_or_final_source_verdict_consumed=True,no_historical_package_or_ledger_copy=True));print(json.dumps(dict(status='FROZEN',actual_PID=os.getpid(),input_count=len(rows),source_RAW=sha(CODE.read_bytes()),HEAD_at_freeze=head)))
def command(label,args):
 start=now()
 with (O/(label+'.stdout.log')).open('wb') as out,(O/(label+'.stderr.log')).open('wb') as err:
  p=subprocess.Popen(args,cwd=ROOT,stdout=out,stderr=err);print(json.dumps(dict(event='FOREGROUND_START',label=label,actual_PID=p.pid)),flush=True);code=p.wait()
 r=dict(label=label,command=args,actual_foreground_PID=p.pid,actual_parent_PID=os.getpid(),started_utc=start,finished_utc=now(),exit_code=code,terminal_closed=True,stdout=pin(O/(label+'.stdout.log')),stderr=pin(O/(label+'.stderr.log')));save(label+'.receipt.json',r);return r
def compiler():
 stable();pre=[pin(CODE),pin(PARENT),pin(ROOT/'lean-toolchain'),pin(ROOT/'lake-manifest.json')];r=command('fresh-lean',['lake','env','lean',CODE.relative_to(ROOT).as_posix()]);assert r['exit_code']==0;log=text(O/'fresh-lean.stdout.log')+text(O/'fresh-lean.stderr.log');assert not re.search(r'\berror\b|sorryAx|\(deterministic\) timeout',log);xs=re.findall(re.escape(DECL)+r"' depends on axioms:\s*\[([^\]]+)\]",log);assert xs and all(set(map(str.strip,x.split(',')))=={'propext','Classical.choice','Quot.sound'} and len(x.split(','))==3 for x in xs);post=[pin(CODE),pin(PARENT),pin(ROOT/'lean-toolchain'),pin(ROOT/'lake-manifest.json')];assert pre==post;stable();save('compiler.result.json',dict(status='PASS',actual_PID=os.getpid(),receipt=r,pre_pins=pre,post_pins=post,exact_standard3=['propext','Classical.choice','Quot.sound'],axiom_output_instances=len(xs),fresh_production_Lean_elaboration=True,Lake_cache_replay=False,unchanged_dependency_oleans_reused=True,output_olean_requested=False,full_root_Tests_site_not_run=True));print(json.dumps(dict(status='PASS',actual_PID=os.getpid(),fresh_Lean_PID=r['actual_foreground_PID'])))
if __name__=='__main__':
 try:globals()[sys.argv[1]]()
 except Exception as e:
  if not(O/'lease.final.json').exists():save((sys.argv[2] if len(sys.argv)>2 else sys.argv[1])+'.failure.json',dict(actual_PID=os.getpid(),utc=now(),error=repr(e),traceback=traceback.format_exc()))
  raise
