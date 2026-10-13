from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,os,re,subprocess,sys,traceback
ROOT=Path('E:/Samplinglib');R=ROOT/'runs/20261007-companion-priority/pbps-actual-finite-jump-recursion76';OWN=R/'exact-science-verification76'
PARENT='54620175c56e7db191bcebe7bb010edda1744894';ACTOR='/root/exact_science63';ID='ASTIS-SA-20261010-PBPSActualFiniteJumpRecursion'
DECL='AutoSamplingTheory.ExampleCases.ProximalBPS.ActualFiniteJumpRecursion.actual_fixed_reference_finite_jump_recursion'
PY='C:/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe'
MODULE=ROOT/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualFiniteJumpRecursion.lean';LEDGER=ROOT/'runs/substantive_advances.jsonl'
EXPECTED_MODULE_RAW='1f1ebc187676e0481247bc2f58ec0bf94b2fc6f02a563b87009a0fe7bfb4910c'
RECIPE='Replace CRLF byte pairs with LF only; preserve bare CR and every other byte.'
def now():return datetime.now(timezone.utc).isoformat()

def sha(b):return hashlib.sha256(b).hexdigest()

def canon(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()

def load(p):return json.loads(p.read_bytes())

def read(n):return load(OWN/n)

def write(n,x):
 p=OWN/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(json.dumps(x,ensure_ascii=False,sort_keys=True,indent=2).encode()+b'\n')

def path(s):
 p=Path(s);return p if p.is_absolute() else ROOT/p

def pin(p):
 b=p.read_bytes();return dict(path=p.relative_to(ROOT).as_posix(),RAW_bytes=len(b),RAW_sha256=sha(b),LF_bytes=len(b.replace(b'\r\n',b'\n')),LF_sha256=sha(b.replace(b'\r\n',b'\n')))

def check(row):
 p=path(row['path']);q=pin(p)
 for k,alts in [('RAW_bytes',['RAW_bytes','bytes','raw_bytes']),('RAW_sha256',['RAW_sha256','raw_sha256']),('LF_bytes',['LF_bytes','lf_bytes']),('LF_sha256',['LF_sha256','lf_sha256'])]:
  key=next((x for x in alts if x in row),None)
  if key:assert q[k]==row[key],(p,k,q[k],row[key])
 return q

def git(args):return subprocess.run(['git',*args],cwd=ROOT,capture_output=True,check=True).stdout

def differences(a,b,p=''):
 if isinstance(a,dict) and isinstance(b,dict):
  return [z for k in sorted(set(a)|set(b)) for z in ([p+'/'+k] if k not in a or k not in b else differences(a[k],b[k],p+'/'+k))]
 if isinstance(a,list) and isinstance(b,list) and len(a)==len(b):return [z for i,(x,y) in enumerate(zip(a,b)) for z in differences(x,y,p+'/'+str(i))]
 return [] if a==b else [p]

def authorization():
 """Called only after root supplies the exact SCI76 commit and explicit permission."""
 p=OWN/'authorization76.json'
 if not p.exists():raise RuntimeError('PREPARED_ONLY: exact SCI76 and explicit root permission have not been supplied; no verification or transition allowed.')
 a=load(p);assert a['explicit_exact_commit_permission'] is True and a['authorized_by']=='/root' and re.fullmatch('[0-9a-f]{40}',a['exact_commit']) and a['parent']==PARENT
 return a

def check_exact_commit():
 a=authorization();sci=a['exact_commit'];assert git(['rev-parse','HEAD']).decode().strip()==sci
 assert git(['rev-list','--parents','-n','1',sci]).decode().split()==[sci,PARENT]
 b=MODULE.read_bytes();assert len(b)==22655 and len(b.splitlines())==412 and sha(b)==EXPECTED_MODULE_RAW
 assert git(['show',sci+':'+MODULE.relative_to(ROOT).as_posix()])==b
 return sci

def process(label,argv,accepted=(0,)):
 sci=check_exact_commit();f=OWN/'terminals';f.mkdir(exist_ok=True);out=f/(label+'.stdout.RAW');err=f/(label+'.stderr.RAW');pre=pin(MODULE);start=now()
 with out.open('wb') as o,err.open('wb') as e:
  p=subprocess.Popen(argv,cwd=ROOT,stdout=o,stderr=e);print(json.dumps(dict(status='FOREGROUND_RUNNING',label=label,actual_PID=p.pid)),flush=True);code=p.wait()
 rec=dict(label=label,actual_PID=p.pid,command=argv,checked_commit=sci,parent=PARENT,started_utc=start,ended_utc=now(),exit_code=code,terminal_closed=True,stdout=pin(out),stderr=pin(err),module_pre=pre,module_post=pin(MODULE));write('terminals/'+label+'.receipt.json',rec);assert pre==rec['module_post'] and code in accepted,(label,code);return rec

def gates():
 sci=check_exact_commit();checks=[('frontier',['tools/astis_frontier_cells.py','check']),('publication',['tools/astis_publication.py','check','--base',PARENT]),('contributor',['tools/astis_contributor_contract.py','check','--base',PARENT]),('semantic',['tools/astis_semantic_roundtrip.py','check'])]
 rows=[process(label,[PY,'-B','-X','utf8',*args]) for label,args in checks]
 sys.path[:0]=[str(ROOT),str(ROOT/'tools')];import astis_publication
 astis_publication.check_advance([DECL],reviewed=True)
 write('gates.json',dict(status='PASS',actual_PID=os.getpid(),checked_commit=sci,parent=PARENT,receipts=rows,reviewed_source_gate=dict(function='astis_publication.check_advance',publication_declarations=[DECL],reviewed=True,status='PASS'),full_aggregate_site_gate=False))

def scan():
 sci=check_exact_commit();sys.path[:0]=[str(ROOT),str(ROOT/'tools')];import astis
 text=MODULE.read_bytes().decode();stripped=astis.strip_lean_comments_and_strings(text);hits=[dict(line=i+1,text=s) for i,s in enumerate(stripped.splitlines()) if astis.FORBIDDEN_REGEX.search(s)];assert not hits
 inventory=re.findall(r'^(private )?(def|theorem|lemma|axiom|opaque)\s+([^\s:]+)',stripped,re.M);assert inventory==[('private ','def','actual_fixed_reference_finite_jump_recursion_statement'),('','theorem','actual_fixed_reference_finite_jump_recursion')]
 write('fake-closure.json',dict(status='PASS',actual_PID=os.getpid(),checked_commit=sci,module=pin(MODULE),hits=hits,inventory=inventory,private_providers=0))

def native_binding():
 check_exact_commit()
 raise RuntimeError('EXACT_SOURCE_ADMISSION_SCHEMA_REVIEW_REQUIRED: implement the bounded source/math/blind finite maps only after all final native packages are CLOSED and explicitly authorized. Preparation is not acceptance.')

def transition():
 sci=check_exact_commit();d=read('decision.json');assert d['accepted_exact_commit'] and d['checked_commit']==sci and d['all_required_current_gates_PASS'] and d['accepted_current_source_review']
 raise RuntimeError('INDEPENDENT_TRANSITION_FINAL_REVIEW_REQUIRED: single append remains disabled until actual exact-commit/native decision and owner/state/prefix audit are completed.')

def prepared_status():
 print(json.dumps(dict(status='PREPARED_ONLY_NOT_EXECUTED',actual_PID=os.getpid(),parent=PARENT,explicit_commit_authorization_present=(OWN/'authorization76.json').exists(),verification_started=False,VERIFIED=False)))

if __name__=='__main__':
 action=sys.argv[-1]
 if action=='prepared_status':prepared_status()
 else:
  authorization()
  if action not in ['gates','scan','native_binding','transition']:raise RuntimeError('Unknown or not yet admitted action')
  globals()[action]()
