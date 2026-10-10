from pathlib import Path
from datetime import datetime, timezone
import hashlib,json,os,re,subprocess,sys
ROOT=Path('E:/Samplinglib');R=ROOT/'runs/20261007-companion-priority/pbps-actual-harmonic-flow73';OLD=R/'exact-science-verification73';OWN=R/'exact-science-label-recheck73';SELF=Path(__file__)
PY='C:/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe'
SCI='d7e00a7c0e8b0f37fcc2dbe99f6b646d3a7b1de6';PARENT='63319104ccad4e81e3a2c59da23ec0009be5e17f';BASE='bc3dca8d76432f71e3abbfdbce2c3b2161ec8d19'
ID='ASTIS-SA-20261010-PBPSActualHarmonicFlow';ACTOR='/root/exact_science63';DECL='AutoSamplingTheory.ExampleCases.ProximalBPS.ActualHarmonicFlow.actual_harmonic_flow_laws'
MODULE=ROOT/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualHarmonicFlow.lean';CELL=ROOT/'research-wiki/frontier-cells/ASTIS-SW-PBPS-actual-harmonic-flow.json'
PUB=ROOT/'website/content/publications/pbps-actual-harmonic-flow.json';LESSON=ROOT/'website/content/declaration_lessons/pbps-actual-harmonic-flow.json';AUDIT=ROOT/'research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261010-PBPSActualHarmonicFlow.json';LEDGER=ROOT/'runs/substantive_advances.jsonl'
RECIPE='Replace CRLF byte pairs with LF only; preserve bare CR and every other byte.'
def now():return datetime.now(timezone.utc).isoformat()
def sha(b):return hashlib.sha256(b).hexdigest()
def canon(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def load(p):return json.loads(p.read_bytes())
def read(n):return load(OWN/n)
def write(n,x):(OWN/n).write_bytes(json.dumps(x,ensure_ascii=False,sort_keys=True,indent=2).encode()+b'\n')
def pin(p):
 b=p.read_bytes();return dict(path=p.relative_to(ROOT).as_posix(),RAW_bytes=len(b),RAW_sha256=sha(b),LF_sha256=sha(b.replace(b'\r\n',b'\n')))
def check(row):
 p=Path(row['path']);p=p if p.is_absolute() else ROOT/p;q=pin(p)
 for k,alts in [('RAW_bytes',['RAW_bytes','bytes','raw_bytes']),('RAW_sha256',['RAW_sha256','raw_sha256']),('LF_sha256',['LF_sha256','lf_sha256'])]:
  key=next((x for x in alts if x in row),None)
  if key:assert q[k]==row[key],(p,k,q[k],row[key])
 return q
def git(args):return subprocess.run(['git',*args],cwd=ROOT,capture_output=True,check=True).stdout
def state():
 sys.path[:0]=[str(ROOT),str(ROOT/'tools')];import astis_advance
 return astis_advance._replay_advances([json.loads(x) for x in LEDGER.read_bytes().splitlines() if x.strip()])[ID]
def recheck():
 for row in read('inputs.manifest.json')['inputs']:check(row)
 assert git(['rev-parse','HEAD']).decode().strip()==SCI
def differences(a,b,p=''):
 if isinstance(a,dict) and isinstance(b,dict):
  out=[]
  for k in sorted(set(a)|set(b)):
   out+=([p+'/'+k] if k not in a or k not in b else differences(a[k],b[k],p+'/'+k))
  return out
 if isinstance(a,list) and isinstance(b,list) and len(a)==len(b):
  return [z for i,(x,y) in enumerate(zip(a,b)) for z in differences(x,y,p+'/'+str(i))]
 return [] if a==b else [p]
def freeze():
 assert git(['rev-list','--parents','-n','1',SCI]).decode().split()==[SCI,PARENT]
 assert git(['rev-parse','HEAD']).decode().strip()==SCI
 paths=[MODULE,CELL,PUB,LESSON,AUDIT,ROOT/'lean-toolchain',ROOT/'lake-manifest.json']
 paths += [R/x for x in ['proved-local.json','root.failed-science73.adoption.json','root.frontier-label-overlay73.adoption.json','root.math73.adoption.json','root.source73.adoption.json','root.decoder73.adoption.json','source-review.packet.json',
 'frontier-label-overlay73/proposal.json','frontier-label-overlay73/cell.before.exactraw.json','frontier-label-overlay73/cell.proposed.exactraw.json','frontier-label-staging73/diagnosis.json',
 'independent-frontier-label-repair73/lease.final.json','independent-frontier-label-repair73/native.manifest.json','independent-frontier-label-repair73/run.json','independent-frontier-label-repair73/decision.json',
 'independent-math73/lease.final.json','independent-source73/lease.final.json','anonymous-decoder/CLOSED_LAST.json']]
 paths += [OLD/x for x in ['lease.final.json','run.json','inputs.manifest.json','complete-named-verification.payload.json','fresh-lean.result.json','source-binding-fakeclosure.audit.json','native-reuse.audit.json','whitespace.audit.json','decision.json']]
 paths += [ROOT/'tools'/x for x in ['astis.py','astis_advance.py','astis_publication.py','astis_contributor_contract.py','astis_semantic_roundtrip.py','astis_frontier_cells.py']]
 rows=[pin(p) for p in paths];assert len({x['path'] for x in rows})==len(rows)
 write('inputs.manifest.json',dict(input_count=len(rows),inputs=rows,LF_recipe=RECIPE,storage='Finite RAW/LF references; no recursive historical copies or full ledger.'))
 write('lease.open.json',dict(status='OPEN_EXACT_CHILD_SCI73_RECHECK',actual_PID=os.getpid(),actor=ACTOR,checked_commit=SCI,parent=PARENT,original_diff_base=BASE))
 b=LEDGER.read_bytes();st=state();assert st['state']=='PROVED_LOCAL' and st['owner_id']=='companion_root_20261005' and st['publication_declarations']==[DECL]
 assert not (R/'verified.json').exists()
 write('ledger.before-prefix.json',dict(path=LEDGER.relative_to(ROOT).as_posix(),RAW_bytes=len(b),RAW_sha256=sha(b),target_state=st))
 print(json.dumps(dict(status='FROZEN',actual_PID=os.getpid(),input_count=len(rows),checked_commit=SCI)))
def native_audit():
 recheck();lease=load(OLD/'lease.final.json');assert lease['status']=='CLOSED_LAST' and lease['owned_count']==102
 for row in lease['all_owned_outputs_except_only_self']:check(row)
 assert len([p for p in OLD.rglob('*') if p.is_file()])==102
 oldrun=load(OLD/'run.json');want=oldrun.pop('run_sha256');assert sha(canon(oldrun))==want==lease['whole_logical_run_sha256'];check(oldrun['complete_named_RAW_payload'])
 assert oldrun['VERIFIED'] is False and oldrun['checked_commit']==PARENT
 adopted=load(R/'root.failed-science73.adoption.json');assert adopted['native_whole_logical_run_sha256']==want;check(adopted['native_lease'])
 overlay=load(R/'root.frontier-label-overlay73.adoption.json');check(overlay['native_repair_lease']);check(overlay['before']);check(overlay['approved_after']);check(overlay['current'])
 md=load(R/'independent-frontier-label-repair73/native.manifest.json');assert len(md['owned_files'])==10
 for row in md['owned_files']:check(row)
 repair_run=load(R/'independent-frontier-label-repair73/run.json');rh=repair_run.pop('run_sha256');assert sha(canon(repair_run))==rh==overlay['native_whole_logical_run_sha256']
 assert len([p for p in (R/'independent-frontier-label-repair73').rglob('*') if p.is_file()])==12
 repair_decision=load(R/'independent-frontier-label-repair73/decision.json');assert repair_decision['decision']=='ACCEPT_EXACT_TWO_STRING_METADATA_OVERLAY_ONLY'
 before=load(R/'frontier-label-overlay73/cell.before.exactraw.json');after=load(CELL)
 expected=['/reuse_plan/searched_existing/0','/shared_floor_audit/searched/0'];assert differences(before,after)==expected
 for changes in overlay['changes']:
  ptr=changes['JSON_pointer'];a,b=ptr.split('/')[1:3];assert before[a][b][0]==changes['before'] and after[a][b][0]==changes['after']
  assert changes['after']=='Samplinglib '+changes['before'].replace('Exact','exact',1)
 assert git(['show',PARENT+':'+CELL.relative_to(ROOT).as_posix()])==(R/'frontier-label-overlay73/cell.before.exactraw.json').read_bytes()
 assert git(['show',SCI+':'+CELL.relative_to(ROOT).as_posix()])==(R/'frontier-label-overlay73/cell.proposed.exactraw.json').read_bytes()==CELL.read_bytes()
 changed=git(['diff','--name-status',PARENT,SCI]).decode().splitlines();records=[dict(status=x.split('\t')[0],path=x.split('\t')[1]) for x in changed]
 assert [x for x in records if x['status']!='A']==[dict(status='M',path=CELL.relative_to(ROOT).as_posix())]
 assert all(x['path'].startswith(R.relative_to(ROOT).as_posix()+'/') for x in records if x['status']=='A')
 core=[]
 for p in [MODULE,PUB,LESSON,AUDIT,R/'source-review.packet.json',ROOT/'lean-toolchain',ROOT/'lake-manifest.json',R/'proved-local.json',R/'root.math73.adoption.json',R/'root.source73.adoption.json',R/'root.decoder73.adoption.json']:
  name=p.relative_to(ROOT).as_posix();a=git(['show',PARENT+':'+name]);b=git(['show',SCI+':'+name]);assert a==b
  raw=p.read_bytes();assert b==raw or p.name in ['lean-toolchain','lake-manifest.json'] and b.replace(b'\r\n',b'\n')==raw.replace(b'\r\n',b'\n')
  core.append(dict(current=pin(p),Git_RAW_sha256=sha(b),Git_RAW_bytes=len(b),same_parent_child_RAW=True,current_Git_RAW_equal=b==raw,CRLF_only_LF_qualification=b!=raw))
 oldmaps=[]
 for row in load(OLD/'inputs.manifest.json')['inputs']:
  if row['path']==CELL.relative_to(ROOT).as_posix():
   assert row['RAW_sha256']==pin(R/'frontier-label-overlay73/cell.before.exactraw.json')['RAW_sha256'];oldmaps.append(dict(resolution='EXACT_REVIEWED_TWO_STRING_CELL_OVERLAY',historical=row,current=pin(CELL),before_snapshot=overlay['before'],after_snapshot=overlay['approved_after']))
  else:check(row);oldmaps.append(dict(path=row['path'],resolution='CURRENT_EXACT',RAW_sha256=row['RAW_sha256']))
 assert len(oldmaps)==49
 prior=load(OLD/'native-reuse.audit.json')
 for package in prior['packages']:
  check(package['lease'])
  if 'manifest' in package:
   check(package['manifest']);m=load(ROOT/package['manifest']['path']);entries=m.get('entries',m.get('files',m.get('owned_files')))
   for row in entries:check(row)
  else:
   dl=load(ROOT/package['lease']['path'])
   for row in dl['prior_owned_files']:check(row)
 fresh=load(OLD/'fresh-lean.result.json');assert fresh['actual_direct_Lean_PID']==36212 and fresh['terminal_EXIT']==0 and fresh['fresh_source_elaboration'] and not fresh['Lake_cache_replay'];check(fresh['module']);check(fresh['compiler']['stdout']);check(fresh['compiler']['stderr']);check(fresh['owned_olean'])
 assert fresh['module']['RAW_sha256']==pin(MODULE)['RAW_sha256']=='506c1d57b3c9133db1cfc0515dccbd8759aaec3e1dbf4a128f6a73d3aeb73c8c'
 source=load(OLD/'source-binding-fakeclosure.audit.json');assert source['source_slots']==7 and source['blocking_deltas']==0 and source['math_repairs']==0
 for row in source['finite_source_input_maps']:
  if row['resolution']=='CURRENT_EXACT':check(dict(path=row['path'],RAW_sha256=row['RAW_sha256']))
  else:
   check(row['historical'])
   if row['path']==CELL.relative_to(ROOT).as_posix():assert row['current']['RAW_sha256']==overlay['before']['RAW_sha256']
   else:check(row['current'])
 text=MODULE.read_text(encoding='utf-8');sys.path[:0]=[str(ROOT),str(ROOT/'tools')];import astis
 stripped=astis.strip_lean_comments_and_strings(text);hits=[dict(line=i+1,text=s.strip()) for i,s in enumerate(stripped.splitlines()) if astis.FORBIDDEN_REGEX.search(s)];assert not hits
 assert len(re.findall(r'^theorem ',stripped,re.M))==1 and len(re.findall(r'^private def ',stripped,re.M))==1
 write('binding-reuse-source-scan.json',dict(status='PASS_EXACT_CHILD_ONLY_METADATA_DELTA',actual_PID=os.getpid(),checked_commit=SCI,parent=PARENT,original_diff_base=BASE,child_diff_paths=records,
  only_modified_canonical=CELL.relative_to(ROOT).as_posix(),JSON_changed_pointers=expected,case_change_disclosed='Exact -> exact; not prefix bytes alone',unchanged_Git_core=core,
  original_closed102_lease=pin(OLD/'lease.final.json'),original_whole_logical_run_sha256=want,original_commit_VERIFIED=False,old49_finite_input_maps=oldmaps,
  original_source_current_maps=source['finite_source_input_maps'],cell_history_chain=[source['finite_source_input_maps'][0]] if False else [dict(stage='source_admission_before',snapshot=pin(R/'cell.before-source-admission73.exactraw.json')),dict(stage='proved_local_and_original_SCI',snapshot=overlay['before']),dict(stage='reviewed_label_child',current=pin(CELL))],
  closed_native_reuse=prior,reused_fresh_direct_Lean=fresh,source_slots=7,informational_deltas=10,blocking_source_deltas=0,math_repairs=0,exact_BODY_steps=source['exact_BODY_steps'],
  module_lines=178,public_declarations=1,private_literal_Prop_definitions=1,private_providers=0,fake_closure_hits=hits,standard3=True,new_Lean_compilation=False,reviewed_overlay_native_run_sha256=rh,
  no_aggregate_reader_full_paper_Goal_credit=True))
 print(json.dumps(dict(status='BINDING_REUSE_SOURCE_FAKECLOSURE_PASS',actual_PID=os.getpid(),child_paths=len(records),reused_Lean_PID=36212,finite_old_maps=len(oldmaps))))
def process(label,argv,accepted=(0,)):
 f=OWN/'terminals';f.mkdir(exist_ok=True);out=f/(label+'.stdout.RAW');err=f/(label+'.stderr.RAW');pre=pin(MODULE);start=now()
 with out.open('wb') as o,err.open('wb') as e:
  p=subprocess.Popen(argv,cwd=ROOT,stdout=o,stderr=e);print(json.dumps(dict(status='FOREGROUND_RUNNING',label=label,actual_PID=p.pid)),flush=True);code=p.wait()
 receipt=dict(label=label,actual_PID=p.pid,command=argv,started_utc=start,ended_utc=now(),exit_code=code,terminal_closed=True,stdout=pin(out),stderr=pin(err),module_pre=pre,module_post=pin(MODULE));write('terminals/'+label+'.receipt.json',receipt)
 assert pre==receipt['module_post'] and code in accepted,(label,code);return receipt
def gates():
 recheck();checks=[('frontier',['tools/astis_frontier_cells.py','check']),('publication',['tools/astis_publication.py','check','--base',BASE]),('contributor',['tools/astis_contributor_contract.py','check','--base',BASE]),('semantic',['tools/astis_semantic_roundtrip.py','check']),('packet',['tools/astis_publication.py','packet','--cell','ASTIS-SW-PBPS-actual-harmonic-flow'])]
 rows=[process(label,[PY,'-B','-X','utf8',*args]) for label,args in checks]
 sys.path[:0]=[str(ROOT),str(ROOT/'tools')];import astis_publication;astis_publication.check_advance([DECL],reviewed=True)
 write('gates.json',dict(status='PASS',actual_PID=os.getpid(),checked_commit=SCI,diff_base=BASE,receipts=rows,reviewed_source_gate=dict(function='astis_publication.check_advance',publication_declarations=[DECL],reviewed=True,status='PASS'),full_root_site_or_aggregate=False))
 print(json.dumps(dict(status='REQUIRED_FRESH_GATES_PASS',actual_PID=os.getpid(),actual_gates=len(rows))))
def whitespace():
 recheck();rec=process('full-RAW-whitespace',['git','-c','core.whitespace=cr-at-eol','diff','--check',BASE,SCI],accepted=(0,1,2))
 raw=(ROOT/rec['stdout']['path']).read_bytes();findings=[dict(path=m.group(1),line=int(m.group(2)),kind=m.group(3)) for m in re.finditer(r'^(.+):(\d+): (trailing whitespace|new blank line at EOF)\.',raw.decode(),re.M)]
 old=load(OLD/'whitespace.audit.json');diag=load(R/'frontier-label-staging73/diagnosis.json');oldnames={x['path'] for x in old['exact_findings']};newnames={x['path'] for x in diag['findings']};names=sorted({x['path'] for x in findings});assert findings and rec['exit_code']!=0 and set(names)<=oldnames|newnames
 rows=[]
 for name in names:
  p=ROOT/name;b=git(['show',SCI+':'+name]);assert b==p.read_bytes()
  if name in oldnames:
   previous=next(x for x in old['finite_exception_files'] if x['file']['path']==name);check(previous['file']);classification=previous['classification']
  else:
   closed=load(OLD/'lease.final.json');row=next(x for x in closed['all_owned_outputs_except_only_self'] if x['path']==name);check(row);classification='Exact immutable diagnostic RAW bound by original CLOSED102 and root finite staged diagnosis; no reformat.'
  rows.append(dict(file=pin(p),Git_RAW_equal=True,classification=classification))
 authored=process('authored-complement-whitespace',['git','-c','core.whitespace=cr-at-eol','diff','--check',BASE,SCI,'--','.',*[':(exclude)'+n for n in names]])
 child=process('child-cell-whitespace',['git','-c','core.whitespace=cr-at-eol','diff','--check',PARENT,SCI,'--',CELL.relative_to(ROOT).as_posix()])
 write('whitespace.json',dict(status='AUTHORED_PASS_RAW_NEGATIVE_RETAINED',actual_PID=os.getpid(),checked_commit=SCI,diff_base=BASE,full_RAW_PASS=False,immutable_findings=len(findings),exact_findings=findings,finite_exception_files=rows,RAW_terminal=rec,authored_complement_PASS=True,authored_terminal=authored,child_cell_PASS=True,child_cell_terminal=child,no_native_normalization=True))
 print(json.dumps(dict(status='WHITESPACE_QUALIFIED',actual_PID=os.getpid(),immutable_findings=len(findings),full_RAW_PASS=False,authored_PASS=True)))
def decision():
 recheck();assert read('gates.json')['status']=='PASS' and read('whitespace.json')['authored_complement_PASS'] and read('binding-reuse-source-scan.json')['fake_closure_hits']==[]
 before=read('ledger.before-prefix.json');assert sha(LEDGER.read_bytes())==before['RAW_sha256'] and state()['state']=='PROVED_LOCAL'
 write('decision.json',dict(schema='exact-science-label-recheck73/decision-v1',status='ACCEPTED_EXACT_CORRECTED_SCI73',accepted_exact_commit=True,checked_commit=SCI,parent=PARENT,original_diff_base=BASE,original_commit_VERIFIED=False,actor=ACTOR,actual_PID=os.getpid(),owner_id='companion_root_20261005',publication_declarations=[DECL],
  math_and_source='Unchanged exact178-line module and accepted7slot native source; fresh directLean36212 standard3 reused by exact parent/child/current RAW equality; six callers/nine laws/rank0/alphaeta1 retained.',
  delta='Exactly two search-record strings; Samplinglib label plus disclosed Exact->exact case; no premise/definition/formula/BODY/source/binding/context/packet change.',
  gates=pin(OWN/'gates.json'),source_audit=pin(OWN/'binding-reuse-source-scan.json'),fake_closure_hits=0,whitespace=pin(OWN/'whitespace.json'),
  authorized_next_action='One independent VERIFIED transition bound exclusively to new child; old SCI remains never VERIFIED.',
  remaining_boundary='Deterministic actual harmonic arcs only; bounce/rate/clock/random paths/nonexplosion/invariance/reversal/terminal kernel H K r_rho/B27 B28/main/errors/caps/cost/composition remain open.',
  aggregate=False,reader=False,main_live=False,full_Exposition_Seal=False,PURIFIED=False,whole_paper=False,Goal_complete=False))
 print(json.dumps(dict(status='ACCEPTED_EXACT_CORRECTED_SCI73',actual_PID=os.getpid(),checked_commit=SCI,transition_not_yet_called=True)))
def transition():
 recheck();d=read('decision.json');assert d['accepted_exact_commit'];before=read('ledger.before-prefix.json');old=LEDGER.read_bytes();assert len(old)==before['RAW_bytes'] and sha(old)==before['RAW_sha256'] and state()['state']=='PROVED_LOCAL';assert not (R/'verified.json').exists()
 sys.path[:0]=[str(ROOT),str(ROOT/'tools')];import astis_advance
 evidence=dict(verifier_id=ACTOR,verified_commit=SCI,publication_declarations=[DECL],gate=read('gates.json'),source_audit=pin(OWN/'binding-reuse-source-scan.json'),fake_closure_scan=dict(status='PASS',hits=0,evidence=pin(OWN/'binding-reuse-source-scan.json')),decision=pin(OWN/'decision.json'),reused_fresh_Lean=dict(actual_PID=36212,exit_code=0,standard3=True,exact_RAW=pin(MODULE)),original_failed_commit=PARENT,original_failed_commit_VERIFIED=False)
 astis_advance.transition_advance(ID,'VERIFIED',worker_id=ACTOR,modes=['independent-exact-commit-verification'],evidence=evidence)
 new=LEDGER.read_bytes();assert new.startswith(old);append=new[len(old):];events=[json.loads(x) for x in append.splitlines() if x.strip()];assert len(events)==1
 event=events[0];assert event['to_state']=='VERIFIED' and event['worker_id']==ACTOR and event['evidence']['verified_commit']==SCI and event['advance_id']==ID
 assert state()['state']=='VERIFIED';write('ledger.append.exactraw.jsonl',append.decode()) if False else (OWN/'ledger.append.exactraw.jsonl').write_bytes(append)
 record=dict(schema='exact-science-label-recheck73/verified-v1',status='VERIFIED',advance_id=ID,verifier_id=ACTOR,owner_id='companion_root_20261005',verified_commit=SCI,checked_commit=SCI,science_parent=PARENT,original_failed_commit_VERIFIED=False,actual_transition_PID=os.getpid(),transition_count=1,
  ledger_before=dict(RAW_bytes=len(old),RAW_sha256=sha(old)),ledger_after=dict(RAW_bytes=len(new),RAW_sha256=sha(new)),exact_append=pin(OWN/'ledger.append.exactraw.jsonl'),event=event,decision=pin(OWN/'decision.json'),source_audit=pin(OWN/'binding-reuse-source-scan.json'),gate=pin(OWN/'gates.json'),fake_closure_scan=dict(status='PASS',hits=0),fresh_Lean_reused_PID=36212,
  aggregate=False,reader=False,main_live=False,full_Exposition_Seal=False,PURIFIED=False,whole_paper=False,Goal_complete=False)
 write('transition.result.json',record);(R/'verified.json').write_bytes(json.dumps(record,ensure_ascii=False,sort_keys=True,indent=2).encode()+b'\n')
 print(json.dumps(dict(status='VERIFIED_APPEND_ONCE',actual_PID=os.getpid(),verified_commit=SCI,append_bytes=len(append),shared_verified=pin(R/'verified.json'))))
def transition_readback():
 recheck();r=read('transition.result.json');b=LEDGER.read_bytes();assert sha(b)==r['ledger_after']['RAW_sha256'];pre=r['ledger_before'];assert sha(b[:pre['RAW_bytes']])==pre['RAW_sha256'];assert b[pre['RAW_bytes']:]==(OWN/'ledger.append.exactraw.jsonl').read_bytes();assert state()['state']=='VERIFIED';assert load(R/'verified.json')==r
 events=[json.loads(x) for x in b[pre['RAW_bytes']:].splitlines() if x.strip()];assert len(events)==1 and events[0]['evidence']['verified_commit']==SCI
 print(json.dumps(dict(status='READONLY_VERIFIED_APPEND_CONFIRMED',actual_PID=os.getpid(),exactly_one_append=True,checked_commit=SCI)))
def allowned(exclude=()):return [pin(p) for p in sorted(OWN.rglob('*')) if p.is_file() and p.relative_to(OWN).as_posix() not in exclude]
def finalize():
 transition_readback();write('outputs.baseline.manifest.json',dict(stage='Preterminal baseline; final lease binds exact final self/terminal bytes.',files=allowned(('outputs.baseline.manifest.json','complete-named-verification.payload.json','run.json','lease.final.json'))))
 payload=dict(payload_name='COMPLETE_EXACT_CHILD_SCI73_VERIFICATION_DECISION_INPUT',decision=read('decision.json'),inputs=read('inputs.manifest.json'),binding_source_scan=read('binding-reuse-source-scan.json'),gates=read('gates.json'),whitespace=read('whitespace.json'),ledger_before=read('ledger.before-prefix.json'),transition=read('transition.result.json'),shared_verified=pin(R/'verified.json'),output_baseline=read('outputs.baseline.manifest.json'),original_obstruction_and_all_observer_negatives_preserved=pin(OLD/'lease.final.json'))
 write('complete-named-verification.payload.json',payload);run=dict(schema='exact-science-label-recheck73/run-v1',status='ACCEPTED_VERIFIED_EXACT_CHILD',checked_commit=SCI,parent=PARENT,actor=ACTOR,VERIFIED=True,decision=pin(OWN/'decision.json'),inputs_manifest=pin(OWN/'inputs.manifest.json'),complete_named_RAW_payload=pin(OWN/'complete-named-verification.payload.json'),transition=pin(OWN/'transition.result.json'),shared_verified=pin(R/'verified.json'),wholelogical_recipe='UTF8 JSON ensure_ascii=false sort_keys=true separators comma/colon; delete ONLY top-level run_sha256.',all_owned_manifest='Final CLOSED_LAST lease binds every owned output except only itself.',aggregate=False,reader=False,main_live=False,PURIFIED=False,full_Exposition_Seal=False,whole_paper=False,Goal_complete=False)
 run['run_sha256']=sha(canon(run));write('run.json',run);print(json.dumps(dict(status='FINALIZED',actual_PID=os.getpid(),whole_logical_run_sha256=run['run_sha256'],named=run['complete_named_RAW_payload'])))
def readback():
 transition_readback();run=read('run.json');h=run.pop('run_sha256');assert sha(canon(run))==h;check(run['complete_named_RAW_payload']);check(run['shared_verified']);print(json.dumps(dict(status='READBACK_PASS',actual_PID=os.getpid(),whole_logical_run_sha256=h,named_RAW_sha256=run['complete_named_RAW_payload']['RAW_sha256'])))
def close_probe():readback()
def close():
 assert not (OWN/'lease.final.json').exists();readback();assert launch('close_probe')==0;rows=allowned(('lease.final.json',));write('lease.final.json',dict(status='CLOSED_LAST',actor=ACTOR,actual_last_writer_PID=os.getpid(),closed_utc=now(),owned_count=len(rows)+1,all_owned_outputs_except_only_self=rows,closure_logical_sha256=sha(canon(rows)),whole_logical_run_sha256=read('run.json')['run_sha256'],complete_named_RAW_payload=pin(OWN/'complete-named-verification.payload.json'),final_owned_write=True,all_sessions_closed=True,postclose_owned_writes=False,VERIFIED=True,verified_commit=SCI,only_shared_writes='Exactly1 independent VERIFIED append plus r73/verified.json; no canonical/Git/aggregate/site write.'));print(json.dumps(dict(status='CLOSED_LAST',actual_PID=os.getpid(),owned_count=len(rows)+1,lease=pin(OWN/'lease.final.json'))))
def postclose():
 lease=read('lease.final.json');rows=allowned(('lease.final.json',));assert rows==lease['all_owned_outputs_except_only_self'] and sha(canon(rows))==lease['closure_logical_sha256'];readback();print(json.dumps(dict(status='READONLY_POSTCLOSE_PASS',actual_PID=os.getpid(),owned_count=len(rows)+1,total_RAW_bytes=sum(p.stat().st_size for p in OWN.rglob('*') if p.is_file()),lease=pin(OWN/'lease.final.json'),closure_logical_sha256=lease['closure_logical_sha256'],owned_writes=False)))
def launch(action):
 assert not (OWN/'lease.final.json').exists();(OWN/(action+'.executed-helper.RAW.py')).write_bytes(SELF.read_bytes());argv=[PY,'-B','-X','utf8',str(SELF),'_child',action]
 with (OWN/(action+'.stdout.log')).open('wb') as out,(OWN/(action+'.stderr.log')).open('wb') as err:
  p=subprocess.Popen(argv,cwd=ROOT,stdout=out,stderr=err);print(json.dumps(dict(status='RUNNING',actual_PID=p.pid,action=action,runner_PID=os.getpid())),flush=True);code=p.wait()
 write(action+'.receipt.json',dict(action=action,actual_PID=p.pid,runner_PID=os.getpid(),command=argv,exit_code=code,terminal_closed=True,stdout=pin(OWN/(action+'.stdout.log')),stderr=pin(OWN/(action+'.stderr.log')),executed_helper=pin(OWN/(action+'.executed-helper.RAW.py'))));print(json.dumps(dict(status='TERMINAL',actual_PID=p.pid,action=action,exit_code=code)));return code
if __name__=='__main__':
 action=sys.argv[-1]
 if sys.argv[1]=='_child':sys.exit(globals()[action]() or 0)
 elif action in ['close','postclose']:globals()[action]()
 else:sys.exit(launch(action))
