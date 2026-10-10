from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,os,re,subprocess,sys,traceback
ROOT=Path('E:/Samplinglib');R=ROOT/'runs/20261007-companion-priority/pbps-actual-finite-jump-recursion76';OWN=R/'independent-math76'
PY='C:/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe';ACTOR='/root/exact_science63';BASE='54620175c56e7db191bcebe7bb010edda1744894'
MODULE=ROOT/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualFiniteJumpRecursion.lean';DECL='AutoSamplingTheory.ExampleCases.ProximalBPS.ActualFiniteJumpRecursion.actual_fixed_reference_finite_jump_recursion'
RECIPE='Replace CRLF byte pairs with LF only; preserve bare CR and all other bytes.'
def now():return datetime.now(timezone.utc).isoformat()
def sha(b):return hashlib.sha256(b).hexdigest()
def canon(d):return json.dumps(d,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def load(p):return json.loads(p.read_bytes())
def read(n):return load(OWN/n)
def write(n,d):
 p=OWN/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(json.dumps(d,ensure_ascii=False,sort_keys=True,indent=2).encode()+b'\n')
def pin(p):
 b=p.read_bytes();return dict(path=p.as_posix(),RAW_bytes=len(b),RAW_sha256=sha(b),LF_bytes=len(b.replace(b'\r\n',b'\n')),LF_sha256=sha(b.replace(b'\r\n',b'\n')))
def path(s):
 p=Path(s);return p if p.is_absolute() else ROOT/p
def check(row):
 q=pin(path(row['path']))
 for k in ['RAW_bytes','RAW_sha256','LF_bytes','LF_sha256']:
  if k in row:assert q[k]==row[k],(q,k,row[k])
 return q
def git(args):return subprocess.run(['git',*args],cwd=ROOT,capture_output=True,check=True).stdout
def recheck():
 assert git(['rev-parse','HEAD']).decode().strip()==BASE
 for row in read('inputs.manifest.json')['inputs']+read('inputs.manifest.json')['supplemental_inputs']:
  check(row['original'])
  if 'snapshot' in row:check(row['snapshot'])
def freeze():
 dispatch=load(R/'independent-math.dispatch76.json');assert len(dispatch['inputs'])==12 and dispatch['checked_parent']==BASE and git(['rev-parse','HEAD']).decode().strip()==BASE
 rows=[]
 for i,row in enumerate(dispatch['inputs']):
  check(row);p=path(row['path']);rec=dict(original=pin(p))
  if 'primary-pbps.exactraw.snapshot.html' in p.name:rec['storage']='Immutable fixed primary source reference; no duplicate whole paper; exact source regions saved separately.'
  else:
   out=OWN/'inputs'/('%02d.'%i+p.name+'.RAW');out.parent.mkdir(exist_ok=True);out.write_bytes(p.read_bytes());rec['snapshot']=pin(out)
  if p in [ROOT/'lean-toolchain',ROOT/'lake-manifest.json'] or p.parent==MODULE.parent and p!=MODULE:
   b=git(['show',BASE+':'+p.relative_to(ROOT).as_posix()]);rec['Git_parent_RAW_sha256']=sha(b);rec['Git_parent_RAW_bytes']=len(b);rec['Git_parent_RAW_equal']=b==p.read_bytes();assert rec['Git_parent_RAW_equal'] or b.replace(b'\r\n',b'\n')==p.read_bytes().replace(b'\r\n',b'\n');rec['Git_parent_CRLF_only_qualification']=not rec['Git_parent_RAW_equal']
  rows.append(rec)
 supplemental=[]
 for n in ['independent-math.dispatch76.json','mathematics-freeze76.json']:
  p=R/n;out=OWN/'inputs'/n;out.write_bytes(p.read_bytes());supplemental.append(dict(original=pin(p),snapshot=pin(out),role='Dispatch itself' if n.startswith('independent') else 'Later root control-plane freeze; only its stable source/toolchain facts used, no header/source verdict consumption.'))
 write('inputs.manifest.json',dict(dispatch_input_count=12,supplemental_input_count=2,total_input_rows=14,inputs=rows,supplemental_inputs=supplemental,checked_parent=BASE,candidate_uncommitted=True,LF_recipe=RECIPE))
 write('lease.open.json',dict(status='OPEN_WHOLE_MATHEMATICS76',actor=ACTOR,actual_PID=os.getpid(),opened_utc=now(),checked_parent=BASE,no_canonical_shared_Git_ledger_writes=True))
 print(json.dumps(dict(status='FROZEN',actual_PID=os.getpid(),dispatch_inputs=12,supplemental_inputs=2,module=pin(MODULE))))
def process(label,argv,env=None):
 pre=pin(MODULE);f=OWN/'terminals';f.mkdir(exist_ok=True);out=f/(label+'.stdout.RAW');err=f/(label+'.stderr.RAW');started=now()
 with out.open('wb') as o,err.open('wb') as e:
  p=subprocess.Popen(argv,cwd=ROOT,stdout=o,stderr=e,env=env);print(json.dumps(dict(status='FOREGROUND_RUNNING',label=label,actual_PID=p.pid)),flush=True);code=p.wait()
 rec=dict(label=label,actual_PID=p.pid,command=argv,started_utc=started,ended_utc=now(),exit_code=code,terminal_closed=True,stdout=pin(out),stderr=pin(err),module_pre=pre,module_post=pin(MODULE));write('terminals/'+label+'.receipt.json',rec);assert code==0 and rec['module_post']==pre,(label,code);return rec
def compile():
 recheck();envrec=process('fixed-Lake-environment',['lake','env',PY,'-B','-X','utf8','-c',"import os,json;print(json.dumps({k:os.environ.get(k,'') for k in ['LEAN_PATH','LEAN_SRC_PATH']}))"])
 lakeenv=json.loads(path(envrec['stdout']['path']).read_bytes());env=os.environ.copy();env.update(lakeenv);lean=ROOT/'.astis/toolchain/lean-4.33.0-windows/bin/lean.exe';version=process('fixed-Lean-version',[str(lean),'--version'],env);assert '4.33.0' in path(version['stdout']['path']).read_text()
 out=OWN/'output/ActualFiniteJumpRecursion.olean';out.parent.mkdir(exist_ok=True);rec=process('fresh-whole-canonical-module',[str(lean),'-o',str(out),str(MODULE)],env)
 driver=OWN/'inputs/ActualFiniteJumpRecursion.axiom-audit.lean';suffix='\n#print axioms '+DECL+'\n';driver.write_bytes(MODULE.read_bytes()+suffix.encode());ax=process('fresh-whole-source-standard3',[str(lean),str(driver)],env)
 text=path(ax['stdout']['path']).read_text(encoding='utf8');matches=re.findall(r'depends on axioms:\s*\[([^\]]+)\]',text,re.S);assert len(matches)==1;axioms=[x.strip() for x in matches[0].split(',')];assert set(axioms)=={'propext','Classical.choice','Quot.sound'} and len(axioms)==3
 write('fresh-compiler.json',dict(status='PASS',checked_parent=BASE,module=pin(MODULE),fresh_source_elaboration=True,Lake_build_cache_replay=False,actual_foreground_Lean_PID=rec['actual_PID'],axioms_PID=ax['actual_PID'],terminal_EXIT=0,standard_axioms=axioms,compiler_receipt=pin(OWN/'terminals/fresh-whole-canonical-module.receipt.json'),axiom_receipt=pin(OWN/'terminals/fresh-whole-source-standard3.receipt.json'),real_Lean_executable=pin(lean),version_receipt=pin(OWN/'terminals/fixed-Lean-version.receipt.json'),Lake_environment_receipt=pin(OWN/'terminals/fixed-Lake-environment.receipt.json'),fixed_environment=lakeenv,output_olean=pin(out),canonical_olean_written=False,axiom_driver=pin(driver),axiom_driver_only_suffix=suffix,axiom_driver_exact_module_prefix=True))
 recheck();print(json.dumps(dict(status='FRESH_SOURCE_AND_AXIOMS_PASS',actual_PID=os.getpid(),Lean_PID=rec['actual_PID'],axioms_PID=ax['actual_PID'],standard3=True)))
def launch(action):
 assert not (OWN/'lease.final.json').exists();p=Path(__file__);(OWN/(action+'.executed-helper.RAW.py')).write_bytes(p.read_bytes());argv=[PY,'-B','-X','utf8',str(p),'_child',action]
 with (OWN/(action+'.stdout.log')).open('wb') as o,(OWN/(action+'.stderr.log')).open('wb') as e:
  proc=subprocess.Popen(argv,cwd=ROOT,stdout=o,stderr=e);print(json.dumps(dict(status='RUNNING',action=action,actual_PID=proc.pid,runner_PID=os.getpid())),flush=True);code=proc.wait()
 write(action+'.receipt.json',dict(action=action,actual_PID=proc.pid,runner_PID=os.getpid(),command=argv,exit_code=code,terminal_closed=True,stdout=pin(OWN/(action+'.stdout.log')),stderr=pin(OWN/(action+'.stderr.log')),executed_helper=pin(OWN/(action+'.executed-helper.RAW.py'))));print(json.dumps(dict(status='TERMINAL',action=action,actual_PID=proc.pid,exit_code=code)));return code
if __name__=='__main__':
 try:
  action=sys.argv[-1]
  if sys.argv[1]=='_child':sys.exit(globals()[action]() or 0)
  elif action in ['close','postclose']:globals()[action]()
  else:sys.exit(launch(action))
 except BaseException as e:
  if not isinstance(e,SystemExit) and not (OWN/'lease.final.json').exists():write('negative.'+sys.argv[-1]+'.'+str(os.getpid())+'.json',dict(actual_PID=os.getpid(),action=sys.argv[-1],error=repr(e),traceback=traceback.format_exc(),canonical_mutation=False))
  raise
