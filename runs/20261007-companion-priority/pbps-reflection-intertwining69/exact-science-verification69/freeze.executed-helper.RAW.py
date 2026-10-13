import os,sys,json,hashlib,datetime,subprocess,re,traceback,copy
from pathlib import Path
ROOT=Path('E:/Samplinglib');P=ROOT/'runs/20261007-companion-priority/pbps-reflection-intertwining69';O=P/'exact-science-verification69';M=P/'independent-math69';S=P/'independent-source69';D=P/'anonymous-decoder';PRE=ROOT/'runs/20261007-companion-priority/pbps-reflection-rotation-preproof69';ACTOR='/root/exact_science63';SCI='2d286c283a6fb5dfc13180204bb0da54531a5c67';BASE='663c12a46996d03eb8c1a31a1f63bfa20bffc653';SAU='ASTIS-SA-20261009-PBPSActualReflectionIntertwining';DECL='AutoSamplingTheory.ExampleCases.ProximalBPS.ReflectionIntertwining.actual_reflection_intertwining';CODE=ROOT/'AutoSamplingTheory/ExampleCases/ProximalBPS/ReflectionIntertwining.lean';PUB=ROOT/'website/content/publications/pbps-actual-reflection-intertwining.json';LESSON=ROOT/'website/content/declaration_lessons/pbps-actual-reflection-intertwining.json';AUDIT=ROOT/'research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261009-PBPSActualReflectionIntertwining.json';CELL=ROOT/'research-wiki/frontier-cells/ASTIS-SW-PBPS-actual-reflection-intertwining.json';PY=sys.executable
sys.path.insert(0,str(ROOT));sys.path.insert(0,str(ROOT/'tools'))
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def sha(b):return hashlib.sha256(b).hexdigest()
def read(p):return json.loads(Path(p).read_bytes())
def get(n):return read(O/n)
def save(n,v):
 assert not(O/'lease.final.json').exists();p=O/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes((json.dumps(v,ensure_ascii=False,sort_keys=True,indent=2)+'\n').encode())
def pin(p):
 p=Path(p);b=p.read_bytes();lf=b.replace(b'\r\n',b'\n');return dict(path=p.as_posix(),raw_bytes=len(b),raw_sha256=sha(b),lf_bytes=len(lf),lf_sha256=sha(lf))
def checkpin(q):assert pin(q['path'])==q,('RAW/LF drift',q['path'])
def text(p):return Path(p).read_bytes().replace(b'\r\n',b'\n').decode('utf-8')
def logical(d):return sha(json.dumps({k:v for k,v in d.items() if k!='run_sha256'},sort_keys=True,ensure_ascii=False,separators=(',',':')).encode())
def git(*args):return subprocess.check_output(['git',*args],cwd=ROOT)
def gitpin(p):
 p=Path(p);rel=p.relative_to(ROOT).as_posix();b=git('show',SCI+':'+rel);q=pin(p);assert b.replace(b'\r\n',b'\n')==p.read_bytes().replace(b'\r\n',b'\n'),('Git mismatch',rel)
 return dict(path=rel,commit=SCI,Git_blob_oid=git('rev-parse',SCI+':'+rel).decode().strip(),Git_RAW_bytes=len(b),Git_RAW_sha256=sha(b),Git_LF_sha256=sha(b.replace(b'\r\n',b'\n')),current=q,qualification='EXACT_RAW_EQUAL' if b==p.read_bytes() else 'ONLY_CRLF_CHECKOUT_DIFFERENCE_EXPLICIT; no RAW equality claim')
def ledgerpin():
 p=ROOT/'runs/substantive_advances.jsonl';b=p.read_bytes();return dict(path=p.as_posix(),raw_bytes=len(b),raw_sha256=sha(b),line_count=len(b.splitlines()),historical_prefix_only=True)
def stable():
 assert git('rev-parse','HEAD').decode().strip()==SCI
 for r in get('inputs.manifest.json')['inputs']:
  checkpin(r['original'])
  if 'RAW_snapshot' in r:checkpin(r['RAW_snapshot']);checkpin(r['LF_snapshot'])
def freeze():
 O.mkdir(parents=True,exist_ok=True);save('lease.open.json',dict(status='OPEN',actor=ACTOR,actual_PID=os.getpid(),utc=now(),checked_commit=SCI,parent=BASE,owned_scope=O.as_posix(),only_allowed_shared_writes='ONE proper nonowner VERIFIED event and r69/verified.json after acceptance.'))
 assert git('rev-parse','HEAD').decode().strip()==SCI;assert git('rev-list','--parents','-n','1',SCI).decode().split()==[SCI,BASE]
 primary=[CODE,ROOT/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualRootCommutation.lean',ROOT/'AutoSamplingTheory/ExampleCases/ProximalBPS/ReflectionL2.lean',PUB,LESSON,AUDIT,CELL,ROOT/'lean-toolchain',ROOT/'lake-manifest.json']+[PRE/n for n in ['header0-expanded.lean','header0-public.lean','statement0.definition.lean','root.statement-seal69.json']]+[P/n for n in ['proved-local.json','publication-plan.json','math-freeze.theorem-only69.json','publication-freeze69.json','root.math69.adoption.json','root.source69.adoption.json','root.decoder69.adoption.json','source.0.reviewer-packet.json','source-admission-finite-current-maps69.json','reader-api-overlay69/application.json','reader-api-overlay69/lesson.before.exactraw.json','reader-api-overlay69/audit.before.exactraw.json','audit.0.before-decoder.exactraw.snapshot.json','audit.before-source-admission.exactraw.json','cell.before-proved.exactraw.json','frozen-cell69.json','conceptual-mirror-audit69.json','whitespace-diagnosis69/diagnosis.json']]+[ROOT/'tools'/n for n in ['astis.py','astis_publication.py','astis_contributor_contract.py','astis_semantic_roundtrip.py','astis_frontier_cells.py','astis_advance.py','astis_harness.py']]
 native=[M/n for n in ['lease.final.json','run.json','named-mathematical-review.payload.json','mathematical-review.json','inputs.manifest.json']]+[S/n for n in ['lease.final.json','review-run.json','complete-named-review-decision-input-payload.json','source.0.decision.json','current-input-manifest.json','owned-manifest.json','reader-api-metadata-overlay.proposal.json','reader-api-metadata-overlay.decision.json','six-BODY-formula-and-code-review.json','finite-current-source-review-coverage.json','whole-module446-line-coverage.json']]+[D/n for n in ['lease.json','review-run.json','manifest.json','anonymous_reconstruction_69.json','terminal-receipts.json']]
 rows=[];gps=[]
 for i,p in enumerate(primary+native):
  gp=gitpin(p);gps.append(gp);r=dict(original=pin(p),authority='Exact immutable checked Git blob; complete original RAW recoverable at named Git object',Git=gp)
  if p in primary:
   rp=O/f'inputs/{i:03}.RAW.snapshot';lp=O/f'inputs/{i:03}.LF.snapshot';rp.parent.mkdir(exist_ok=True);b=p.read_bytes();rp.write_bytes(b);lp.write_bytes(b.replace(b'\r\n',b'\n'));r.update(RAW_snapshot=pin(rp),LF_snapshot=pin(lp))
  else:r['no_duplicate_native_payload_copy']='Native immutable artifact is pinned in Git and original CLOSED scope; avoid recursively duplicating prior reviews.'
  rows.append(r)
 ext=P/'commit-science69/receipt.json';rows.append(dict(original=pin(ext),authority='EXTERNAL_POSTCOMMIT_EXECUTION_RECEIPT; causally created after commit, explicitly excluded, never claimed as same-commit Git content'))
 assert all(q['qualification']=='EXACT_RAW_EQUAL' for q in gps if q['path'] in [CODE.relative_to(ROOT).as_posix(),PUB.relative_to(ROOT).as_posix(),LESSON.relative_to(ROOT).as_posix(),AUDIT.relative_to(ROOT).as_posix(),CELL.relative_to(ROOT).as_posix()]);save('inputs.manifest.json',dict(status='FROZEN_BEFORE_FRESH_COMPILER',actual_PID=os.getpid(),utc=now(),checked_commit=SCI,parent=BASE,input_count=len(rows),primary_snapshots=len(primary),native_Git_references=len(native),external_postcommit_receipts=1,LF_recipe='Replace ONLY CRLF bytes with LF; preserve bare CR/encoding/all else; exact RAW authoritative.',inputs=rows,no_whole_ledger_or_history_copy=True));save('Git.blobs.manifest.json',dict(checked_commit=SCI,parent=BASE,input_count=len(gps),blobs=gps));save('ledger.before.pin.json',ledgerpin());save('commit.binding.json',dict(status='PASS',checked_commit=SCI,parent=BASE,actual_PID=os.getpid(),sole_new_Lean_module=[p for p in git('diff','--name-only',BASE,SCI,'--','AutoSamplingTheory','Tests').decode().splitlines() if p.endswith('.lean')],new_aggregate_or_Registry_credit=False,root_commit_receipt_external=pin(ext)));assert get('commit.binding.json')['sole_new_Lean_module']==[CODE.relative_to(ROOT).as_posix()];print(json.dumps(dict(status='FROZEN',actual_PID=os.getpid(),inputs=len(rows),Git_blobs=len(gps))))
def command(label,args):
 start=now()
 with (O/(label+'.stdout.log')).open('wb') as out,(O/(label+'.stderr.log')).open('wb') as err:p=subprocess.Popen(args,cwd=ROOT,stdout=out,stderr=err);print(json.dumps(dict(event='FOREGROUND_START',label=label,actual_PID=p.pid)),flush=True);code=p.wait()
 r=dict(label=label,command=args,actual_foreground_PID=p.pid,actual_parent_PID=os.getpid(),started_utc=start,finished_utc=now(),exit_code=code,terminal_closed=True,stdout=pin(O/(label+'.stdout.log')),stderr=pin(O/(label+'.stderr.log')));save(label+'.receipt.json',r);return r
def compile():
 stable();r=command('focused',['lake','env','lean',CODE.relative_to(ROOT).as_posix()]);assert r['exit_code']==0;log=text(O/'focused.stdout.log')+text(O/'focused.stderr.log');assert not re.search(r'\berror\b|sorryAx|\(deterministic\) timeout',log);xs=re.findall(re.escape(DECL)+r"' depends on axioms:\s*\[([^\]]+)\]",log);assert xs and all(set(map(str.strip,x.split(',')))=={'propext','Classical.choice','Quot.sound'} and len(x.split(','))==3 for x in xs);stable();save('focused.result.json',dict(status='PASS',checked_commit=SCI,receipt=r,exact_standard3=['propext','Classical.choice','Quot.sound'],fresh_Lean_source_compiler=True,unchanged_import_oleans_reused=True,olean_output_requested=False,pre_post_RAW_LF_unchanged=True,axiom_output_instances=len(xs),full_root_or_tests_build=False));print(json.dumps(dict(status='PASS',actual_PID=os.getpid(),fresh_Lean_PID=r['actual_foreground_PID'])))
def gates():
 stable();rs=[]
 for label,args in [('frontier',['tools/astis_frontier_cells.py','check']),('publication',['tools/astis_publication.py','check','--base',BASE,'--ci']),('contributor',['tools/astis_contributor_contract.py','check','--base',BASE,'--ci']),('semantic',['tools/astis_semantic_roundtrip.py','check'])]:
  r=command(label,[PY,'-B','-X','utf8',*args]);rs.append(r);assert r['exit_code']==0,('required gate failure',label)
 from tools import astis_publication as pub
 pub.check_advance([DECL],reviewed=True);stable();save('gates.result.json',dict(status='PASS',checked_commit=SCI,parent=BASE,actual_PID=os.getpid(),results=rs,reviewed_check_advance=dict(declarations=[DECL],reviewed=True,result='PASS',actual_PID=os.getpid()),aggregate_root_Tests_site_not_checked=True));print(json.dumps(dict(status='PASS',actual_PID=os.getpid(),required_gates=5)))
if __name__=='__main__':
 try:globals()[sys.argv[1]]()
 except Exception as e:
  if not(O/'lease.final.json').exists():save((sys.argv[2] if len(sys.argv)>2 else sys.argv[1])+'.failure.json',dict(actual_PID=os.getpid(),utc=now(),error=repr(e),traceback=traceback.format_exc()))
  raise
