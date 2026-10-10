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
def native_binding():
 recheck();packages=[]
 # Mathematical native package: canonical complete run minus only its explicit self-hash.
 ma=load(R/'root.math75.adoption.json');ml=load(R/'independent-math75/lease.final.json');check(ma['native_lease']);check(ml['manifest']);mm=load(path(ml['manifest']['path']))
 assert ml['status']=='CLOSED_LAST' and len(mm['entries'])==mm['entry_count']==44 and sha(canon(mm['entries']))==mm['logical_entries_sha256']
 for row in mm['entries']:check(row)
 mr=load(R/'independent-math75/run.json');mh=mr.pop('run_sha256');assert sha(canon(mr))==mh==ma['native_whole_logical_run_sha256'];check(ma['native_complete_named']);assert len(all_files(R/'independent-math75'))==46
 for row in mr['input_manifest']['inputs']:check(row['original']);check(row['snapshot'])
 for row in load(R/'mathematics-freeze75.json')['inputs']:check(row)
 fresh=load(R/'independent-math75/fresh-compiler.json');assert fresh['fresh_source_elaboration'] and not fresh['Lake_build_cache_replay'] and fresh['actual_foreground_Lean_PID']==18716 and fresh['axiom_audit_PID']==21324 and fresh['terminal_EXIT']==0
 for k in ['compiler_receipt','axiom_audit_receipt','output_olean','real_Lean_executable','version_output','axiom_audit_driver']:check(fresh[k])
 comp=load(path(fresh['compiler_receipt']['path']));ax=load(path(fresh['axiom_audit_receipt']['path']));assert comp['terminal_EXIT']==ax['terminal_EXIT']==0
 for rec in [comp,ax]:check(rec['stdout']);check(rec['stderr'])
 b=MODULE.read_bytes();assert len(b)==21771 and len(b.splitlines())==396 and sha(b)=='fd93d01583eec206285573c1f1631b94739f95471c50e1ff940e66080238e23d'
 assert path(fresh['axiom_audit_driver']['path']).read_bytes()==b+fresh['axiom_driver_only_suffix'].encode()
 axtext=path(ax['stdout']['path']).read_text(encoding='utf-8');m=re.search(r'depends on axioms:\s*\[([^\]]+)\]',axtext,re.S);assert m and [x.strip() for x in m.group(1).split(',')]==['propext','Classical.choice','Quot.sound']==fresh['standard_axioms']
 packages.append(dict(package='math75',owned_count=46,lease=pin(R/'independent-math75/lease.final.json'),run_sha256=mh,complete_named_RAW=ma['native_complete_named'],all_manifest_rows_checked=44,fresh_compiler_reused=True))
 # Fresh source generation1 + distinct administrative generation: retain every named RAW byte.
 sa=load(R/'root.source75.adoption.json');source=R/'independent-clean-source75';admin=R/'independent-clean-source75-admission-overlay'
 for base,lease_name,run_name,selfkey,count in [(source,'CLOSED_LAST.json','source.0.run.json','review_run_sha256',52),(admin,'CLOSED_LAST.json','overlay.0.run.json','administrative_run_sha256',19)]:
  le=load(base/lease_name);assert le['status']=='CLOSED_LAST' and len(le['complete_owned_prior_manifest'])==count-1 and len(all_files(base))==count
  for row in le['complete_owned_prior_manifest']:check(row)
  run=load(base/run_name);rh=run.pop(selfkey);assert sha(canon(run))==rh
  whole=load(base/'whole-logical-payload75.json');wh=whole.pop('whole_logical_payload_sha256');assert sha(canon(whole))==wh==le['whole_logical_payload_sha256']
  for row in whole['complete_named_RAW_payloads']:
   check(row);assert row['RAW_utf8'].encode()==path(row['path']).read_bytes()
  assert len(whole['complete_named_RAW_payloads'])==(5 if base==source else 10)
  packages.append(dict(package=base.name,owned_count=count,lease=pin(base/lease_name),native_run_hash_field=selfkey,native_run_sha256=rh,whole_complete_named_payload=pin(base/'whole-logical-payload75.json'),whole_complete_named_logical_sha256=wh,named_RAW_count=len(whole['complete_named_RAW_payloads'])))
 check(sa['native_lease']);check(sa['administrative_overlay_lease']);check(sa['native_whole_five_payload']);check(sa['administrative_overlay_complete_payload'])
 sr=load(source/'source.0.run.json');assert sr['review_run_sha256']==sa['native_whole_logical_run_sha256']=='db373b9bcc61a10d1ea3a42d51f16e8d5f3e34b4b8d6031e02f71b7e435887c5'
 sourcefirst=load(source/'source-only.freeze75.json');assert all(sourcefirst[k] is False for k in ['candidate_or_current_Lean_read','canonical_packet_or_publication_metadata_read','old_verdict_decision_admission_repair_read'])
 # Exposed sibling is retention/three-field-overlay authority ONLY, never source acceptance.
 oa=load(R/'root.review-input-metadata75.adoption.json');old=R/'independent-source75';ol=load(old/'lease.final.json');check(oa['native_lease']);assert ol['source_admission_ready'] is False and ol['source_status']=='SUPPLEMENTAL_SOURCE_REVIEW_NOT_ANTI_ANCHORED' and len(all_files(old))==82
 for row in ol['files']:check(row)
 ol2=dict(ol);lh=ol2.pop('lease_sha256');assert sha(canon(ol2))==lh
 op=load(old/'complete-named-review-decision-input-payload.json');oph=op.pop('whole_logical_run_sha256');assert sha(canon(op))==oph==ol['whole_logical_run_sha256']
 for row in op['named_complete_RAW_payloads'].values():check(row['RAW']);assert row['complete_RAW_UTF8'].encode()==path(row['RAW']['path']).read_bytes()
 oru=load(old/'overlay75.run.json');oh=oru.pop('run_sha256');assert sha(canon(oru))==oh
 od=load(old/'overlay75.decision.json');check(oa['native_overlay_decision']);assert od['status']=='ACCEPTED_EXACT_THREE_FIELD_METADATA_OVERLAY_ONLY' and od['field_count']==3 and not od['source_admission_granted'] and not od['mathematical_repair'] and not od['source_repair']
 packages.append(dict(package='exposed-source75-OVERLAY-RETENTION-ONLY',owned_count=82,lease=pin(old/'lease.final.json'),whole_complete_payload_sha256=oph,source_admission_ready=False,admitted_source_verdict=False,overlay_sha256=oh))
 proposal=load(R/'review-input-metadata-overlay75/proposal.json');overlay_maps=[]
 for row in proposal['rows']:
  check(row['before']);check(row['proposed']);a=load(path(row['before']['path']));z=json.loads(json.dumps(a))
  for change in row['changes']:
   keys=change['json_pointer'].split('/')[1:];obj=z
   for key in keys[:-1]:obj=obj[int(key)] if isinstance(obj,list) else obj[key]
   key=keys[-1];assert (obj[int(key)] if isinstance(obj,list) else obj[key])==change['old']
   if isinstance(obj,list):obj[int(key)]=change['new']
   else:obj[key]=change['new']
  assert z==load(path(row['proposed']['path']))
  before=R/('cell.before-source-admission75.exactraw.json' if row['path']==CELL.relative_to(ROOT).as_posix() else 'publication.before-source-admission75.exactraw.json');assert before.read_bytes()==path(row['proposed']['path']).read_bytes()
  overlay_maps.append(dict(path=row['path'],before=check(row['before']),approved_after=check(row['proposed']),source_admission_before=pin(before),current=pin(path(row['path'])),exact_changed_pointers=[c['json_pointer'] for c in row['changes']]))
 assert sum(len(x['exact_changed_pointers']) for x in overlay_maps)==3
 # Native blind archive: original custom hash rule, not a rewritten new run convention.
 da=load(R/'root.decoder75.adoption.json');check(da['native_lease']);check(da['native_complete_payload']);dl=load(R/'anonymous-decoder/CLOSED_LAST.json');assert dl['status']=='CLOSED' and dl['closed_exit_receipt']['exit_code']==0
 for row in dl['bound_prior_owned_files']:
  check(row);assert path(row['path']).read_bytes()==(R/'anonymous-decoder'/row['file']).read_bytes()
 check(dl['sole_input_receipt']);assert path(dl['sole_input_receipt']['path']).read_bytes()==(R/'anonymous-decoder/parent-packet.json').read_bytes()
 dr=load(R/'anonymous-decoder/run.json');dp=dict(dr['logical_run_payload']);dp.pop('decoder_run_sha256');assert canon(dp)==dr['canonical_logical_run_utf8'].encode() and sha(canon(dp))==dr['decoder_run_sha256']==da['native_whole_logical_run_sha256']
 native=load(R/'anonymous-decoder/reconstruction.json');adapter=load(R/'anonymous-decoder/decoded.root-adapter.json');assert adapter['native_complete_reconstruction']==native and adapter['native_complete_run']==dr and native['scopes']==native['scopes_senses']
 assert len(all_files(path(dl['owned_output_directory'])))==4
 packages.append(dict(package='strictblind75',owned_count=4,lease=pin(R/'anonymous-decoder/CLOSED_LAST.json'),native_custom_preimage_rule='logical_run_payload minus only decoder_run_sha256',native_run_sha256=dr['decoder_run_sha256'],scope_alias_only=True))
 # Exact three admission maps; all other clean inputs remain current RAW.
 ci=load(source/'source.0.input-manifest.json');admit=load(admin/'admission-overlay75.json');audit=load(AUDIT);before_a=load(R/'audit.before-source-admission75.exactraw.json');expected=dict(before_a);expected.update(admit['audit_fields']);assert expected==audit
 cell=load(CELL);pub=load(PUB);bc=load(R/'cell.before-source-admission75.exactraw.json');bp=load(R/'publication.before-source-admission75.exactraw.json')
 assert cell['source_proof_coverage']==admit['cell_source_proof_coverage'] and pub['items'][0]['source_proof_coverage']==admit['publication_source_proof_coverage']
 allowedc=['conceptual_mirror_audit','evidence','source_proof_coverage','status'];assert all(x.split('/')[1] in allowedc for x in differences(bc,cell));assert all(x.startswith('/items/0/source_proof_coverage/') for x in differences(bp,pub))
 assert cell['status']=='proved_locally' and cell['conceptual_mirror_audit']['status']=='none-found'
 maps={AUDIT.relative_to(ROOT).as_posix():R/'audit.before-source-admission75.exactraw.json',CELL.relative_to(ROOT).as_posix():R/'cell.before-source-admission75.exactraw.json',PUB.relative_to(ROOT).as_posix():R/'publication.before-source-admission75.exactraw.json'}
 finite=[]
 for row in ci['clean_finite_inputs']:
  check(dict(row,path=row['snapshot']))
  if row['path'] in maps:
   hist=maps[row['path']];assert path(row['snapshot']).read_bytes()==hist.read_bytes();finite.append(dict(path=row['path'],resolution='EXACT_INDEPENDENT_ADMIN_ADMISSION_PLUS_PROVED_LOCAL',historical=pin(hist),current=pin(path(row['path'])),changed_pointers=differences(load(hist),load(path(row['path'])))))
  else:check(row);finite.append(dict(path=row['path'],resolution='CURRENT_EXACT',RAW_sha256=row['RAW_sha256']))
 for row in ci['source_only_inputs']['inputs']+ci['generic_API_inputs']:check(row)
 draft=load(R/'audit.before-decoder75.exactraw.snapshot.json');blindbefore=load(R/'audit.before-clean-review75.exactraw.snapshot.json');assert differences(draft,blindbefore)==['/reconstruction','/state'] and blindbefore==before_a
 # Match complete actual statement/helpers/source packets and literal BODY spans.
 packet=load(R/'source-review.clean.packet.json');sd=load(source/'source.0.decision.json');review=load(source/'source.0.review.json');assert sd['accepted'] and sd['verdict']=='equivalent-after-elaboration' and sd['blocking_deltas']==[] and sd['repairs']==[]
 assert set(review['semantic_slots'])=={'objects','domains','quantifiers','assumptions','conclusion','scopes','constant_dependencies'}
 assert audit['semantic_slots']==review['semantic_slots'] and audit['deltas']==review['deltas']==[] and audit['source_review']['reviewer']=='/root/independent_clean_source75'
 assert audit['source_review']['review_run_sha256']==sr['review_run_sha256'] and audit['source_review']['independent_from_formalizer'] and audit['source_review']['independent_from_decoder']
 assert packet['packet_sha256']==sd['reviewer_packet_sha256']==audit['source_review']['reviewer_packet_sha256']
 assert packet['publication_binding_sha256']==sd['publication_binding_sha256']==audit['publication_binding_sha256']=='014e4bebc1b357d5f9a3ea7917903fd700273223963f8dd11932231b227273f3' and packet['candidate_publication_context']==audit['publication_context']
 assert native['reconstructed_theorem_text']==audit['reconstruction']['text']==packet['blind_reconstruction']['text']
 text=b.decode();private=text[text.index('private def actual_integrated_hazard_clock_statement'):text.index('set_option maxHeartbeats')];args,body=private.split(' : Prop :=',1)
 expanded='theorem actual_integrated_hazard_clock_laws'+packet['lean']['statement']+'\n';assert expanded.encode()==(R/'expanded75.frozen.header.lean').read_bytes()
 reconstructed=args.replace('private def actual_integrated_hazard_clock_statement','theorem actual_integrated_hazard_clock_laws',1)+' :'+body;assert reconstructed.split()==expanded.split()
 public=text[text.index('theorem actual_integrated_hazard_clock_laws'):text.index(':= by',text.index('theorem actual_integrated_hazard_clock_laws'))];publicargs=public[:public.index(' :\n    actual_integrated_hazard_clock_statement')];assert publicargs.split()==args.replace('private def actual_integrated_hazard_clock_statement','theorem actual_integrated_hazard_clock_laws',1).split()
 assert 'actual_integrated_hazard_clock_statement hα hαβ hV hH hη hβη' in public
 unit=load(LESSON)['units'][0];assert unit['declaration']==DECL and len(unit['steps'])==9;steps=[];lines=b.splitlines(keepends=True)
 for i,step in enumerate(unit['steps']):
  reg=step['lean_source_region'];span=b''.join(lines[reg['start_line']-1:reg['end_line']]);assert reg['source_raw_sha256']==sha(b) and span==step['lean'].encode() and sha(span)==reg['exact_code_raw_sha256']
  assert reg['start_line']>=136;steps.append(dict(index=i+1,formula=step['formula'],region=reg,literal_BODY_match=True))
 sys.path[:0]=[str(ROOT),str(ROOT/'tools')];import astis
 stripped=astis.strip_lean_comments_and_strings(text);hits=[dict(line=i+1,text=s.strip()) for i,s in enumerate(stripped.splitlines()) if astis.FORBIDDEN_REGEX.search(s)];assert not hits
 inventory=re.findall(r'^(private )?(def|theorem|lemma|axiom|opaque)\s+([^\s:]+)',stripped,re.M);assert inventory==[('private ','def','actual_integrated_hazard_clock_statement'),('private ','theorem','actual_hazard_primitive_laws'),('','theorem','actual_integrated_hazard_clock_laws')]
 assert text.count('ActualHarmonicFlow.actual_harmonic_flow_laws')>=1 and text.count('ActualBounceRate.actual_bounce_rate_energy_laws')>=1
 for field in [cell['shared_floor_audit']['searched'],cell['reuse_plan']['searched_existing']]:assert any('Samplinglib' in x for x in field) and any('Mathlib' in x for x in field)
 write('source-math-binding-fakeclosure.json',dict(status='PASS',actual_PID=os.getpid(),checked_commit=SCI,parent=PARENT,packages=packages,native_owned_count=203,math_inputs_current=14,math_freeze_current_inputs=8,clean_source17_finite_maps=finite,three_field_metadata_overlay_maps=overlay_maps,source_other_exact_input_counts=dict(source_only_inputs=len(ci['source_only_inputs']['inputs']),generic_API_inputs=len(ci['generic_API_inputs'])),draft_to_blind_exact_state_map=dict(before=pin(R/'audit.before-decoder75.exactraw.snapshot.json'),after=pin(R/'audit.before-clean-review75.exactraw.snapshot.json'),changed_pointers=['/reconstruction','/state']),
  module=pin(MODULE),module_lines=396,source_callers=6,literal_let_definitions=['c','Φ','rate','H','C','Λ','τ','W'],conclusion_groups=10,exact_BODY_steps=steps,private_literal_full_expansion_matches_sealed_v2=True,private_primitive_is_proved_internal_ingredient=True,private_providers=0,source_slots=7,source_blocking_deltas=0,mathematical_repairs=0,source_run_sha256=sr['review_run_sha256'],source_native_decision=pin(source/'source.0.decision.json'),publication_binding_sha256=audit['publication_binding_sha256'],packet_sha256=packet['packet_sha256'],fake_closure_hits=hits,declaration_inventory=inventory,fresh_Lean_reused=fresh,new_Lean_compilation=False,
  original_six_callers_and_degeneracies='Original finite real Hilbert/Borel C2 and two Hessians,0<alpha<=beta,eta>0,betaeta<=1. Rank0/alphaeta1/e0/zero energy/zero cap/infinite clock remain legal; no nonexplosion/finite-clock/onto/regularity/provider premise.',
  boundary='One actual harmonic-segment integrated hazard, joint Borel continuous-time first clock and Exp(1) pushforward strict survival only; iid recursion/global path/SLLN/nonexplosion/Markov/invariance/terminal kernel/main/cost/composition/reader/PURIFIED/full-paper/Goal remain open.',documentation_debt=sd['nonblocking_observations']))
 print(json.dumps(dict(status='NATIVE_SOURCE_MATH_BINDING_SCAN_PASS',actual_PID=os.getpid(),native_owned_count=203,source_slots=7,exact_BODY_steps=9,reused_direct_Lean_PID=18716,axioms_PID=21324)))
def all_files(p):return [x for x in p.rglob('*') if x.is_file()]
if __name__=='__main__':
 try:
  action=sys.argv[-1]
  if sys.argv[1]=='_child':sys.exit(globals()[action]() or 0)
  elif action in ['close','postclose']:globals()[action]()
  else:sys.exit(launch(action))
 except BaseException as e:
  if not isinstance(e,SystemExit) and not (OWN/'lease.final.json').exists():write('negative.'+sys.argv[-1]+'.'+str(os.getpid())+'.json',dict(actual_PID=os.getpid(),mode=sys.argv[-1],error=repr(e),traceback=traceback.format_exc(),canonical_mutation_by_this_observer=False))
  raise

