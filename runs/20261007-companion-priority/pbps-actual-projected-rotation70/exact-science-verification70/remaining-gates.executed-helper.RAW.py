import os,sys,json,hashlib,datetime,subprocess,re,traceback,copy,gzip
from pathlib import Path
ROOT=Path('E:/Samplinglib'); P=ROOT/'runs/20261007-companion-priority/pbps-actual-projected-rotation70'; O=P/'exact-science-verification70'; M=P/'independent-math70'; S=P/'independent-source70'; D=P/'anonymous-decoder'; T=P/'independent-source70-portable-admission'; PRE=ROOT/'runs/20261007-companion-priority/pbps-actual-projected-rotation-preproof70'
ACTOR='/root/exact_science63'; SCI='e44b6b1e08c8a259a1f48006d822b53efd3fecb8'; BASE='aa9dd2cf691489535aa8039850c2ee0bcdacdfb4'; SAU='ASTIS-SA-20261009-PBPSActualProjectedRotation'; DECL='AutoSamplingTheory.ExampleCases.ProximalBPS.ActualProjectedRotation.actual_projected_rotation'; MOD='AutoSamplingTheory.ExampleCases.ProximalBPS.ActualProjectedRotation'; CODE=ROOT/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualProjectedRotation.lean'; PUB=ROOT/'website/content/publications/pbps-actual-projected-rotation.json'; LESSON=ROOT/'website/content/declaration_lessons/pbps-actual-projected-rotation.json'; AUDIT=ROOT/'research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261009-PBPSActualProjectedRotation.json'; CELL=ROOT/'research-wiki/frontier-cells/ASTIS-SW-PBPS-actual-projected-rotation.json'; PY=sys.executable
sys.path.insert(0,str(ROOT));sys.path.insert(0,str(ROOT/'tools'))
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def sha(b):return hashlib.sha256(b).hexdigest()
def read(p):return json.loads(Path(p).read_bytes())
def get(n):return read(O/n)
def canon(x):return json.dumps(x,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()
def logical(d):return sha(canon({k:v for k,v in d.items() if k!='run_sha256'}))
def save(n,v):
 assert not (O/'lease.final.json').exists(); p=O/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes((json.dumps(v,sort_keys=True,ensure_ascii=False,indent=2)+'\n').encode())
def pin(p):
 p=Path(p);b=p.read_bytes();lf=b.replace(b'\r\n',b'\n');return dict(path=p.as_posix(),raw_bytes=len(b),raw_sha256=sha(b),lf_bytes=len(lf),lf_sha256=sha(lf))
def checkpin(q):assert pin(q['path'])==q,('RAW/LF drift',q['path'])
def text(p):return Path(p).read_bytes().replace(b'\r\n',b'\n').decode('utf8')
def git(*args):return subprocess.check_output(['git',*args],cwd=ROOT)
def gitpin(p):
 p=Path(p);rel=p.relative_to(ROOT).as_posix();b=git('show',SCI+':'+rel);q=pin(p);local=p.read_bytes();assert b.replace(b'\r\n',b'\n')==local.replace(b'\r\n',b'\n'),('Git LF mismatch',rel)
 return dict(path=rel,commit=SCI,Git_blob_oid=git('rev-parse',SCI+':'+rel).decode().strip(),Git_RAW_bytes=len(b),Git_RAW_sha256=sha(b),Git_LF_sha256=sha(b.replace(b'\r\n',b'\n')),current=q,qualification='EXACT_RAW_EQUAL' if b==local else 'EXPLICIT_CRLF_CHECKOUT_ONLY; exact RAW is not asserted')
def ledgerpin():
 p=ROOT/'runs/substantive_advances.jsonl';b=p.read_bytes();return dict(path=p.as_posix(),raw_bytes=len(b),raw_sha256=sha(b),line_count=len(b.splitlines()),historical_prefix_only=True)
def stable():
 assert git('rev-parse','HEAD').decode().strip()==SCI
 for r in get('inputs.manifest.json')['inputs']:
  checkpin(r['original'])
  if 'RAW_snapshot' in r:checkpin(r['RAW_snapshot']);checkpin(r['LF_snapshot'])
def freeze():
 O.mkdir(parents=True,exist_ok=True);save('lease.open.json',dict(status='OPEN',actor=ACTOR,actual_PID=os.getpid(),utc=now(),checked_commit=SCI,parent=BASE,owned_scope=O.as_posix(),allowed_shared_writes='One proper nonowner VERIFIED event and r70/verified.json ONLY after all acceptance checks.'))
 assert git('rev-parse','HEAD').decode().strip()==SCI;assert git('rev-list','--parents','-n','1',SCI).decode().split()==[SCI,BASE]
 primary=[CODE,PUB,LESSON,AUDIT,CELL,ROOT/'lean-toolchain',ROOT/'lake-manifest.json',ROOT/'AutoSamplingTheory/ExampleCases/ProximalBPS/ReflectionIntertwining.lean',ROOT/'AutoSamplingTheory/ExampleCases/ProximalBPS/GaussianReflection.lean']+[PRE/n for n in ['header0-proposed-expanded.lean','root.statement-seal70.json']]+[P/n for n in ['claim.json','proved-local.json','publication-plan.json','math-freeze.theorem-only70.json','root.math70.adoption.json','root.source70.adoption.json','root.decoder70.adoption.json','root.metadata-repair70.adoption.json','root.named-literal70.adoption.json','source-admission-finite-current-maps70.json','conceptual-mirror-audit70.json','audit.before-source-admission.exactraw.json','cell.before-proved.exactraw.json','cell.before-final-source-coverage.exactraw.json','publication.before-final-source-coverage.exactraw.json','source-review.metadata-overlay1.json','source-review.packet.1.json','whitespace-diagnosis70/diagnosis.json'] if (P/n).exists()]+[T/n for n in ['portability-only.decision.json','exact-five-field-pointer-map.json','portable-admission-fields.proposed.json']]+[ROOT/'tools'/n for n in ['astis.py','astis_publication.py','astis_contributor_contract.py','astis_semantic_roundtrip.py','astis_semantic_roundtrip_core.py','astis_frontier_cells.py','astis_advance.py','astis_harness.py']]
 native=[M/n for n in ['lease.final.json','run.json','named-review.payload.json','mathematical-review.json','inputs.manifest.json'] if (M/n).exists()]+[S/n for n in ['lease.final.json','source.0.review-run.json','source.0.decision.json','source.0.admission-fields.json','complete-exact-input-manifest.json','owned-manifest.json','complete-named-review-decision-input-payload.json']]+[T/n for n in ['lease.final.json','owned-manifest.json','complete-named-portability-review-input.json']]+[D/n for n in ['lease.json','review-run.json','native-manifest.json','complete-reconstruction-decision-input.raw.json','decoded0.json']]
 rows=[];gps=[]
 for i,p in enumerate(primary+native):
  gp=gitpin(p);gps.append(gp);r=dict(original=pin(p),Git=gp,authority='Exact SCI70 Git blob and immutable current RAW/LF authority')
  if p in primary:
   rp=O/f'inputs/{i:03}.RAW.snapshot';lp=O/f'inputs/{i:03}.LF.snapshot';rp.parent.mkdir(exist_ok=True);b=p.read_bytes();rp.write_bytes(b);lp.write_bytes(b.replace(b'\r\n',b'\n'));r.update(RAW_snapshot=pin(rp),LF_snapshot=pin(lp))
  else:r['no_duplicate_payload']='Complete CLOSED native payload pinned by exact Git reference; not recopied or recursively embedded.'
  rows.append(r)
 ext=P/'commit-science70/receipt.json';rows.append(dict(original=pin(ext),authority='External postcommit execution receipt, created after SCI70, deliberately excluded from that commit.'))
 for p in [CODE,PUB,LESSON,AUDIT,CELL]:assert next(g for g in gps if g['path']==p.relative_to(ROOT).as_posix())['qualification']=='EXACT_RAW_EQUAL'
 save('inputs.manifest.json',dict(status='FROZEN_BEFORE_FOCUSED_LAKE',actor=ACTOR,actual_PID=os.getpid(),utc=now(),checked_commit=SCI,parent=BASE,input_count=len(rows),primary_snapshots=len(primary),native_Git_references=len(native),external_postcommit_receipts=1,LF_recipe='Replace ONLY CRLF byte pairs with LF; preserve bare CR and every other byte; RAW authoritative.',inputs=rows,no_whole_ledger_history_or_native_payload_copy=True));save('Git.blobs.manifest.json',dict(checked_commit=SCI,parent=BASE,input_count=len(gps),blobs=gps));save('ledger.before.pin.json',ledgerpin())
 changed=git('diff','--name-only',BASE,SCI,'--','AutoSamplingTheory','Tests').decode().splitlines();assert changed==[CODE.relative_to(ROOT).as_posix()]
 readers=[]
 for rel in ['website/scripts/inline_lean.py','website/scripts/check_cross_domain_browser.py']:
  b=git('show',SCI+':'+rel);old=git('show',BASE+':'+rel);assert b==old;current=pin(ROOT/rel);assert current['raw_sha256']!=sha(b);readers.append(dict(path=rel,SCI_Git_RAW_bytes=len(b),SCI_Git_RAW_sha256=sha(b),unchanged_from_parent=True,current_working_pin=current,qualification='EXCLUDED from SCI70; separately reviewed working integration changes; not science Git equality.'))
 save('commit.binding.json',dict(status='PASS',checked_commit=SCI,parent=BASE,actual_PID=os.getpid(),sole_changed_Lean=changed,reader_scripts=readers,no_aggregate_Registry_Tests_site_credit=True,external_commit_receipt=pin(ext)));print(json.dumps(dict(status='FROZEN',actual_PID=os.getpid(),input_count=len(rows),Git_blobs=len(gps),snapshots=len(primary))))
def command(label,args):
 start=now()
 with (O/(label+'.stdout.log')).open('wb') as out,(O/(label+'.stderr.log')).open('wb') as err:
  p=subprocess.Popen(args,cwd=ROOT,stdout=out,stderr=err);print(json.dumps(dict(event='FOREGROUND_START',label=label,actual_PID=p.pid)),flush=True);code=p.wait()
 r=dict(label=label,command=args,actual_foreground_PID=p.pid,actual_parent_PID=os.getpid(),started_utc=start,finished_utc=now(),exit_code=code,terminal_closed=True,stdout=pin(O/(label+'.stdout.log')),stderr=pin(O/(label+'.stderr.log')));save(label+'.receipt.json',r);return r
def focused():
 stable();r=command('focused-lake',['lake','build',MOD]);assert r['exit_code']==0;log=text(O/'focused-lake.stdout.log')+text(O/'focused-lake.stderr.log');assert not re.search(r'\berror\b|sorryAx|\(deterministic\) timeout',log)
 xs=re.findall(re.escape(DECL)+r"' depends on axioms:\s*\[([^\]]+)\]",log);assert xs and all(set(map(str.strip,x.split(',')))=={'propext','Classical.choice','Quot.sound'} and len(x.split(','))==3 for x in xs);stable();save('focused.result.json',dict(status='PASS',checked_commit=SCI,receipt=r,standard3=['propext','Classical.choice','Quot.sound'],axiom_output_instances=len(xs),Lake_may_replay_cached_diagnostics=True,fresh_proof_elaboration_reused_only_through_exact_RAW_identity=dict(native_scope=M.as_posix(),actual_Lean_PID=42936,exit_code=0,artifact=pin(M/'compiler.receipt.json')),pre_post_RAW_LF_unchanged=True,full_root_Tests_site=False));print(json.dumps(dict(status='PASS',Lake_PID=r['actual_foreground_PID'])))
def gates():
 stable();rs=[]
 for label,args in [('frontier',['tools/astis_frontier_cells.py','check']),('publication',['tools/astis_publication.py','check','--base',BASE,'--ci']),('contributor',['tools/astis_contributor_contract.py','check','--base',BASE,'--ci']),('semantic',['tools/astis_semantic_roundtrip.py','check'])]:
  r=command(label,[PY,'-B','-X','utf8',*args]);rs.append(r);assert r['exit_code']==0,('REQUIRED_GATE_FAILURE',label)
 from tools import astis_publication as pub
 pub.check_advance([DECL],reviewed=True);stable();save('gates.result.json',dict(status='PASS',checked_commit=SCI,parent=BASE,actual_PID=os.getpid(),results=rs,reviewed_check_advance=dict(declarations=[DECL],reviewed=True,result='PASS',actual_PID=os.getpid()),aggregate_root_Tests_site_not_checked=True));print(json.dumps(dict(status='PASS',required_gates=5,actual_PID=os.getpid())))
def remaining_gates():
 stable();rs=[get('frontier.receipt.json')];assert rs[0]['exit_code']==1
 for label,args in [('publication',['tools/astis_publication.py','check','--base',BASE,'--ci']),('contributor',['tools/astis_contributor_contract.py','check','--base',BASE,'--ci']),('semantic',['tools/astis_semantic_roundtrip.py','check'])]:
  r=command(label,[PY,'-B','-X','utf8',*args]);rs.append(r)
 from tools import astis_publication as pub
 try:pub.check_advance([DECL],reviewed=True);reviewed=dict(result='PASS',declarations=[DECL],reviewed=True,actual_PID=os.getpid())
 except Exception as e:reviewed=dict(result='FAIL',error=repr(e),declarations=[DECL],reviewed=True,actual_PID=os.getpid())
 stable();save('gates.result.json',dict(status='REQUIRED_FRONTIER_OBSTRUCTION',checked_commit=SCI,parent=BASE,actual_PID=os.getpid(),results=rs,reviewed_check_advance=reviewed,all_required_PASS=False,no_VERIFIED=True,aggregate_root_Tests_site_not_checked=True));print(json.dumps(dict(status='REQUIRED_FRONTIER_OBSTRUCTION',other_gate_exit_codes=[r['exit_code'] for r in rs[1:]],reviewed=reviewed['result'],actual_PID=os.getpid())))
if __name__=='__main__':
 try:globals()[sys.argv[1]]()
 except Exception as e:
  if not(O/'lease.final.json').exists():save((sys.argv[2] if len(sys.argv)>2 else sys.argv[1])+'.failure.json',dict(actual_PID=os.getpid(),utc=now(),error=repr(e),traceback=traceback.format_exc()))
  raise
