from pathlib import Path
from datetime import datetime, timezone
import hashlib,json,os,re,subprocess,sys,traceback
ROOT=Path('E:/Samplinglib');R=ROOT/'runs/20261007-companion-priority/pbps-actual-hazard-clock75';OWN=R/'exact-science-verification75'
SCI='51d3a65f65b189b0afaaf91a248f8c2f58162ef2';PARENT='526a6af98cf0380032a3aed52da01c5304de3bb8'
ID='ASTIS-SA-20261010-PBPSActualHazardClock';ACTOR='/root/exact_science63';DECL='AutoSamplingTheory.ExampleCases.ProximalBPS.ActualHazardClock.actual_integrated_hazard_clock_laws'
PY='C:/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe'
MODULE=ROOT/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualHazardClock.lean';CELL=ROOT/'research-wiki/frontier-cells/ASTIS-SW-PBPS-actual-hazard-clock.json'
PUB=ROOT/'website/content/publications/pbps-actual-hazard-clock.json';LESSON=ROOT/'website/content/declaration_lessons/pbps-actual-hazard-clock.json';AUDIT=ROOT/'research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261010-PBPSActualHazardClock.json';LEDGER=ROOT/'runs/substantive_advances.jsonl'
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

def state():
 sys.path[:0]=[str(ROOT),str(ROOT/'tools')];import astis_advance
 return astis_advance._replay_advances([json.loads(x) for x in LEDGER.read_bytes().splitlines() if x.strip()])[ID]

def differences(a,b,p=''):
 if isinstance(a,dict) and isinstance(b,dict):
  return [z for k in sorted(set(a)|set(b)) for z in ([p+'/'+k] if k not in a or k not in b else differences(a[k],b[k],p+'/'+k))]
 if isinstance(a,list) and isinstance(b,list) and len(a)==len(b):return [z for i,(x,y) in enumerate(zip(a,b)) for z in differences(x,y,p+'/'+str(i))]
 return [] if a==b else [p]

def recheck():
 assert git(['rev-parse','HEAD']).decode().strip()==SCI
 for row in read('inputs.manifest.json')['inputs']:check(row)

def process(label,argv,accepted=(0,)):
 f=OWN/'terminals';f.mkdir(exist_ok=True);out=f/(label+'.stdout.RAW');err=f/(label+'.stderr.RAW');pre=pin(MODULE);start=now()
 with out.open('wb') as o,err.open('wb') as e:
  p=subprocess.Popen(argv,cwd=ROOT,stdout=o,stderr=e);print(json.dumps(dict(status='FOREGROUND_RUNNING',label=label,actual_PID=p.pid)),flush=True);code=p.wait()
 receipt=dict(label=label,actual_PID=p.pid,command=argv,started_utc=start,ended_utc=now(),exit_code=code,terminal_closed=True,stdout=pin(out),stderr=pin(err),module_pre=pre,module_post=pin(MODULE));write('terminals/'+label+'.receipt.json',receipt)
 assert pre==receipt['module_post'] and code in accepted,(label,code);return receipt

def gates():
 recheck();checks=[('frontier',['tools/astis_frontier_cells.py','check']),('publication',['tools/astis_publication.py','check','--base',PARENT]),('contributor',['tools/astis_contributor_contract.py','check','--base',PARENT]),('semantic',['tools/astis_semantic_roundtrip.py','check']),('packet',['tools/astis_publication.py','packet','--cell','ASTIS-SW-PBPS-actual-hazard-clock'])]
 rows=[process(label,[PY,'-B','-X','utf8',*args]) for label,args in checks]
 sys.path[:0]=[str(ROOT),str(ROOT/'tools')];import astis_publication;astis_publication.check_advance([DECL],reviewed=True)
 write('gates.json',dict(status='PASS',actual_PID=os.getpid(),checked_commit=SCI,diff_base=PARENT,receipts=rows,reviewed_source_gate=dict(function='astis_publication.check_advance',publication_declarations=[DECL],reviewed=True,status='PASS'),full_root_site_or_aggregate=False))
 print(json.dumps(dict(status='REQUIRED_CURRENT_GATES_PASS',actual_PID=os.getpid(),gates=len(rows))))

def transition():
 recheck();d=read('decision.json');assert d['accepted_exact_commit'];before=read('ledger.before-prefix.json');old=LEDGER.read_bytes();assert len(old)==before['RAW_bytes'] and sha(old)==before['RAW_sha256'] and state()['state']=='PROVED_LOCAL';assert not (R/'verified.json').exists()
 sys.path[:0]=[str(ROOT),str(ROOT/'tools')];import astis_advance
 evidence=dict(verifier_id=ACTOR,verified_commit=SCI,publication_declarations=[DECL],gate=pin(OWN/'gates.json'),source_audit=pin(OWN/'source-math-binding-fakeclosure.json'),fake_closure_scan=dict(status='PASS',hits=0,evidence=pin(OWN/'source-math-binding-fakeclosure.json')),decision=pin(OWN/'decision.json'),reused_fresh_Lean=dict(actual_PID=18716,exit_code=0,axioms_PID=21324,standard3=True,exact_RAW=pin(MODULE)))
 astis_advance.transition_advance(ID,'VERIFIED',worker_id=ACTOR,modes=['independent-exact-commit-verification'],evidence=evidence)
 new=LEDGER.read_bytes();assert new.startswith(old);append=new[len(old):];events=[json.loads(x) for x in append.splitlines() if x.strip()];assert len(events)==1
 event=events[0];assert event['to_state']=='VERIFIED' and event['worker_id']==ACTOR and event['evidence']['verified_commit']==SCI and event['advance_id']==ID and state()['state']=='VERIFIED'
 (OWN/'ledger.append.exactraw.jsonl').write_bytes(append)
 record=dict(schema='exact-science-verification75/verified-v1',status='VERIFIED',advance_id=ID,verifier_id=ACTOR,owner_id='companion_root_20261005',verified_commit=SCI,checked_commit=SCI,parent=PARENT,actual_transition_PID=os.getpid(),transition_count=1,
  ledger_before=dict(path=LEDGER.relative_to(ROOT).as_posix(),prefix_offset=0,RAW_bytes=len(old),RAW_sha256=sha(old)),ledger_after=dict(path=LEDGER.relative_to(ROOT).as_posix(),prefix_offset=0,RAW_bytes=len(new),RAW_sha256=sha(new)),exact_append=pin(OWN/'ledger.append.exactraw.jsonl'),before_prefix_preserved_exactly=True,event=event,
  decision=pin(OWN/'decision.json'),source_audit=pin(OWN/'source-math-binding-fakeclosure.json'),gate=pin(OWN/'gates.json'),fake_closure_scan=dict(status='PASS',hits=0),fresh_Lean_reused_PID=18716,axioms_reused_PID=21324,
  aggregate=False,current_reader=False,main_live=False,full_Exposition_Seal=False,PURIFIED=False,whole_paper=False,Goal_complete=False)
 write('transition.result.json',record);write('verified.json',record);(R/'verified.json').write_bytes(json.dumps(record,ensure_ascii=False,sort_keys=True,indent=2).encode()+b'\n')
 print(json.dumps(dict(status='VERIFIED_APPEND_ONCE',actual_PID=os.getpid(),verified_commit=SCI,append_bytes=len(append),shared_verified=pin(R/'verified.json'))))

def transition_readback():
 recheck();r=read('transition.result.json');b=LEDGER.read_bytes();assert len(b)==r['ledger_after']['RAW_bytes'] and sha(b)==r['ledger_after']['RAW_sha256'];pre=r['ledger_before'];assert sha(b[:pre['RAW_bytes']])==pre['RAW_sha256'];assert b[pre['RAW_bytes']:]==(OWN/'ledger.append.exactraw.jsonl').read_bytes();assert state()['state']=='VERIFIED';assert (R/'verified.json').read_bytes()==(OWN/'verified.json').read_bytes();assert load(R/'verified.json')==r
 events=[json.loads(x) for x in b[pre['RAW_bytes']:].splitlines() if x.strip()];assert len(events)==1 and events[0]['evidence']['verified_commit']==SCI and events[0]['worker_id']==ACTOR
 print(json.dumps(dict(status='READONLY_VERIFIED_APPEND_CONFIRMED',actual_PID=os.getpid(),exactly_one_append=True,checked_commit=SCI)))

def allowned(exclude=()):return [pin(p) for p in sorted(OWN.rglob('*')) if p.is_file() and p.relative_to(OWN).as_posix() not in exclude]

def finalize():
 transition_readback();write('outputs.baseline.manifest.json',dict(stage='Preterminal baseline; final lease binds exact final self/terminal bytes.',files=allowned(('outputs.baseline.manifest.json','complete-named-verification.payload.json','run.json','lease.final.json'))))
 payload=dict(payload_name='COMPLETE_EXACT_SCI75_VERIFICATION_DECISION_INPUT',decision=read('decision.json'),inputs=read('inputs.manifest.json'),Git_input_bindings=read('Git-inputs.json'),binding_source_scan=read('source-math-binding-fakeclosure.json'),commit_retention=read('commit-retention.json'),gates=read('gates.json'),whitespace=read('whitespace.json'),ledger_before=read('ledger.before-prefix.json'),transition=read('transition.result.json'),shared_verified=pin(R/'verified.json'),output_baseline=read('outputs.baseline.manifest.json'),all_observer_negatives=[pin(p) for p in sorted(OWN.glob('negative.*'))])
 write('complete-named-verification.payload.json',payload);run=dict(schema='exact-science-verification75/run-v1',status='ACCEPTED_VERIFIED_EXACT_SCI75',checked_commit=SCI,parent=PARENT,actor=ACTOR,VERIFIED=True,decision=pin(OWN/'decision.json'),inputs_manifest=pin(OWN/'inputs.manifest.json'),complete_named_RAW_payload=pin(OWN/'complete-named-verification.payload.json'),transition=pin(OWN/'transition.result.json'),shared_verified=pin(R/'verified.json'),wholelogical_recipe='UTF8 JSON ensure_ascii=false sort_keys=true separators comma/colon; delete ONLY top-level run_sha256.',all_owned_manifest='Final CLOSED_LAST lease binds every owned output except only itself.',aggregate=False,current_reader=False,main_live=False,PURIFIED=False,full_Exposition_Seal=False,whole_paper=False,Goal_complete=False)
 run['run_sha256']=sha(canon(run));write('run.json',run);print(json.dumps(dict(status='FINALIZED',actual_PID=os.getpid(),whole_logical_run_sha256=run['run_sha256'],named=run['complete_named_RAW_payload'])))

def readback():
 transition_readback();run=read('run.json');h=run.pop('run_sha256');assert sha(canon(run))==h;check(run['complete_named_RAW_payload']);check(run['shared_verified']);print(json.dumps(dict(status='READBACK_PASS',actual_PID=os.getpid(),whole_logical_run_sha256=h,named_RAW_sha256=run['complete_named_RAW_payload']['RAW_sha256'])))

def close_probe():readback()

def close():
 assert not (OWN/'lease.final.json').exists();readback();assert launch('close_probe')==0;rows=allowned(('lease.final.json',));write('lease.final.json',dict(status='CLOSED_LAST',actor=ACTOR,actual_last_writer_PID=os.getpid(),closed_utc=now(),owned_count=len(rows)+1,all_owned_outputs_except_only_self=rows,closure_logical_sha256=sha(canon(rows)),whole_logical_run_sha256=read('run.json')['run_sha256'],complete_named_RAW_payload=pin(OWN/'complete-named-verification.payload.json'),final_owned_write=True,all_sessions_closed=True,postclose_owned_writes=False,VERIFIED=True,verified_commit=SCI,only_shared_writes='Exactly1 independent VERIFIED append plus r75/verified.json; no canonical/Git/aggregate/site write.'));print(json.dumps(dict(status='CLOSED_LAST',actual_PID=os.getpid(),owned_count=len(rows)+1,lease=pin(OWN/'lease.final.json'))))

def postclose():
 lease=read('lease.final.json');rows=allowned(('lease.final.json',));assert rows==lease['all_owned_outputs_except_only_self'] and sha(canon(rows))==lease['closure_logical_sha256'];readback();print(json.dumps(dict(status='READONLY_POSTCLOSE_PASS',actual_PID=os.getpid(),owned_count=len(rows)+1,total_RAW_bytes=sum(p.stat().st_size for p in OWN.rglob('*') if p.is_file()),lease=pin(OWN/'lease.final.json'),closure_logical_sha256=lease['closure_logical_sha256'],owned_writes=False)))

def launch(action):
 assert not (OWN/'lease.final.json').exists();self=Path(__file__);(OWN/(action+'.executed-helper.RAW.py')).write_bytes(self.read_bytes());argv=[PY,'-B','-X','utf8',str(self),'_child',action]
 with (OWN/(action+'.stdout.log')).open('wb') as out,(OWN/(action+'.stderr.log')).open('wb') as err:
  p=subprocess.Popen(argv,cwd=ROOT,stdout=out,stderr=err);print(json.dumps(dict(status='RUNNING',actual_PID=p.pid,action=action,runner_PID=os.getpid())),flush=True);code=p.wait()
 write(action+'.receipt.json',dict(action=action,actual_PID=p.pid,runner_PID=os.getpid(),command=argv,exit_code=code,terminal_closed=True,stdout=pin(OWN/(action+'.stdout.log')),stderr=pin(OWN/(action+'.stderr.log')),executed_helper=pin(OWN/(action+'.executed-helper.RAW.py'))));print(json.dumps(dict(status='TERMINAL',actual_PID=p.pid,action=action,exit_code=code)));return code
def freeze():
 assert git(['rev-parse','HEAD']).decode().strip()==SCI
 assert git(['rev-list','--parents','-n','1',SCI]).decode().split()==[SCI,PARENT]
 names=['proved-local.json','claim.json','mathematics-freeze75.json','publication-plan.json','source-review.clean.freeze75.json','source-review.clean.packet.json','implementation-source-map75.json','root.math75.adoption.json','root.source75.adoption.json','root.decoder75.adoption.json','root.review-input-metadata75.adoption.json',
 'audit.before-decoder75.exactraw.snapshot.json','audit.before-clean-review75.exactraw.snapshot.json','audit.before-source-admission75.exactraw.json','cell.before-source-admission75.exactraw.json','publication.before-source-admission75.exactraw.json',
 'review-input-metadata-overlay75/proposal.json','review-input-metadata-overlay75/0.before.exactraw.json','review-input-metadata-overlay75/0.proposed.exactraw.json','review-input-metadata-overlay75/1.before.exactraw.json','review-input-metadata-overlay75/1.proposed.exactraw.json',
 'independent-math75/lease.final.json','independent-math75/native.manifest.json','independent-math75/run.json','independent-math75/fresh-compiler.json',
 'independent-clean-source75/CLOSED_LAST.json','independent-clean-source75/source.0.run.json','independent-clean-source75/source.0.decision.json','independent-clean-source75/source.0.input-manifest.json','independent-clean-source75/source.0.admission-fields.json','independent-clean-source75/whole-logical-payload75.json',
 'independent-clean-source75-admission-overlay/CLOSED_LAST.json','independent-clean-source75-admission-overlay/overlay.0.run.json','independent-clean-source75-admission-overlay/overlay.0.decision.json','independent-clean-source75-admission-overlay/admission-overlay75.json','independent-clean-source75-admission-overlay/whole-logical-payload75.json',
 'independent-source75/lease.final.json','independent-source75/overlay75.decision.json','independent-source75/overlay75.run.json','independent-source75/complete-named-review-decision-input-payload.json',
 'anonymous-decoder/CLOSED_LAST.json','anonymous-decoder/run.json','whitespace-diagnosis75/diagnosis.json','whitespace-diagnosis75/full-staged-immutable-negative.raw.gz','commit-proof75/receipt.json']
 paths=[MODULE,CELL,PUB,LESSON,AUDIT,ROOT/'lean-toolchain',ROOT/'lake-manifest.json',ROOT/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualHarmonicFlow.lean',ROOT/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualBounceRate.lean']+[R/n for n in names]
 paths += [ROOT/'tools'/n for n in ['astis.py','astis_advance.py','astis_publication.py','astis_contributor_contract.py','astis_semantic_roundtrip.py','astis_frontier_cells.py']]
 rows=[pin(p) for p in paths];assert len({x['path'] for x in rows})==len(rows)
 core=[]
 for p in paths:
  name=p.relative_to(ROOT).as_posix()
  if p==R/'commit-proof75/receipt.json':core.append(dict(file=pin(p),classification='POSTCOMMIT_EXTERNAL_EXECUTION_RECEIPT; causally excluded from its own SCI commit'));continue
  b=git(['show',SCI+':'+name]);raw=p.read_bytes();equal=b==raw;assert equal or b.replace(b'\r\n',b'\n')==raw.replace(b'\r\n',b'\n'),name
  core.append(dict(file=pin(p),Git_RAW_sha256=sha(b),Git_RAW_bytes=len(b),current_Git_RAW_equal=equal,CRLF_only_LF_qualification=not equal))
 write('inputs.manifest.json',dict(input_count=len(rows),inputs=rows,LF_recipe=RECIPE,storage='Finite exact RAW/LF references; no recursive history copies or full ledger.'))
 write('Git-inputs.json',dict(actual_PID=os.getpid(),checked_commit=SCI,parent=PARENT,files=core))
 write('lease.open.json',dict(status='OPEN_EXACT_SCI75',actual_PID=os.getpid(),actor=ACTOR,checked_commit=SCI,parent=PARENT))
 b=LEDGER.read_bytes();s=state();assert s['state']=='PROVED_LOCAL' and s['owner_id']=='companion_root_20261005' and s['publication_declarations']==[DECL];assert not (R/'verified.json').exists()
 write('ledger.before-prefix.json',dict(path=LEDGER.relative_to(ROOT).as_posix(),RAW_bytes=len(b),RAW_sha256=sha(b),target_state=s,storage='Full prefix remains in append-only ledger; exact byte length/hash and later byte-preserving append verified, no duplicate history.'))
 print(json.dumps(dict(status='FROZEN',actual_PID=os.getpid(),input_count=len(rows),checked_commit=SCI)))
if __name__=='__main__':
 try:
  action=sys.argv[-1]
  if sys.argv[1]=='_child':sys.exit(globals()[action]() or 0)
  elif action in ['close','postclose']:globals()[action]()
  else:sys.exit(launch(action))
 except BaseException as e:
  if not isinstance(e,SystemExit) and not (OWN/'lease.final.json').exists():write('negative.'+sys.argv[-1]+'.'+str(os.getpid())+'.json',dict(actual_PID=os.getpid(),mode=sys.argv[-1],error=repr(e),traceback=traceback.format_exc(),canonical_mutation_by_this_observer=False))
  raise

