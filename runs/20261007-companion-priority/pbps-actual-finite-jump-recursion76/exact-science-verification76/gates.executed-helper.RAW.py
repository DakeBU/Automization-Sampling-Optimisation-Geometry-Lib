from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,os,re,subprocess,sys,traceback,gzip
ROOT=Path('E:/Samplinglib');R=ROOT/'runs/20261007-companion-priority/pbps-actual-finite-jump-recursion76';OWN=R/'exact-science-verification76'
PRE=ROOT/'runs/20261007-companion-priority/pbps-recursive-preproof76';SOURCE=PRE/'fresh-compiled-source76'
SCI='e1f1d85d34426954829a97a46b563ea8e1dab8f1';PARENT='54620175c56e7db191bcebe7bb010edda1744894';ACTOR='/root/exact_science63';ID='ASTIS-SA-20261010-PBPSActualFiniteJumpRecursion'
DECL='AutoSamplingTheory.ExampleCases.ProximalBPS.ActualFiniteJumpRecursion.actual_fixed_reference_finite_jump_recursion'
PY='C:/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe'
MODULE=ROOT/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualFiniteJumpRecursion.lean';CELL=ROOT/'research-wiki/frontier-cells/ASTIS-SW-PBPS-actual-finite-jump-recursion.json'
PUB=ROOT/'website/content/publications/pbps-actual-finite-jump-recursion.json';LESSON=ROOT/'website/content/declaration_lessons/pbps-actual-finite-jump-recursion.json';AUDIT=ROOT/'research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261010-PBPSActualFiniteJumpRecursion.json';LEDGER=ROOT/'runs/substantive_advances.jsonl'
EXPECTED='1f1ebc187676e0481247bc2f58ec0bf94b2fc6f02a563b87009a0fe7bfb4910c'
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

def process(label,argv,accepted=(0,)):
 f=OWN/'terminals';f.mkdir(exist_ok=True);out=f/(label+'.stdout.RAW');err=f/(label+'.stderr.RAW');pre=pin(MODULE);start=now()
 with out.open('wb') as o,err.open('wb') as e:
  p=subprocess.Popen(argv,cwd=ROOT,stdout=o,stderr=e);print(json.dumps(dict(status='FOREGROUND_RUNNING',label=label,actual_PID=p.pid)),flush=True);code=p.wait()
 receipt=dict(label=label,actual_PID=p.pid,command=argv,started_utc=start,ended_utc=now(),exit_code=code,terminal_closed=True,stdout=pin(out),stderr=pin(err),module_pre=pre,module_post=pin(MODULE));write('terminals/'+label+'.receipt.json',receipt)
 assert pre==receipt['module_post'] and code in accepted,(label,code);return receipt

def transition():
 recheck();d=read('decision.json');assert d['accepted_exact_commit'];before=read('ledger.before-prefix.json');old=LEDGER.read_bytes();assert len(old)==before['RAW_bytes'] and sha(old)==before['RAW_sha256'] and state()['state']=='PROVED_LOCAL';assert not (R/'verified.json').exists()
 sys.path[:0]=[str(ROOT),str(ROOT/'tools')];import astis_advance
 evidence=dict(verifier_id=ACTOR,verified_commit=SCI,publication_declarations=[DECL],gate=pin(OWN/'gates.json'),source_audit=pin(OWN/'source-math-binding-fakeclosure.json'),fake_closure_scan=dict(status='PASS',hits=0,evidence=pin(OWN/'source-math-binding-fakeclosure.json')),decision=pin(OWN/'decision.json'),reused_fresh_Lean=dict(actual_PID=28496,exit_code=0,axioms_PID=29336,standard3=True,exact_RAW=pin(MODULE)))
 astis_advance.transition_advance(ID,'VERIFIED',worker_id=ACTOR,modes=['independent-exact-commit-verification'],evidence=evidence)
 new=LEDGER.read_bytes();assert new.startswith(old);append=new[len(old):];events=[json.loads(x) for x in append.splitlines() if x.strip()];assert len(events)==1
 event=events[0];assert event['to_state']=='VERIFIED' and event['worker_id']==ACTOR and event['evidence']['verified_commit']==SCI and event['advance_id']==ID and state()['state']=='VERIFIED'
 (OWN/'ledger.append.exactraw.jsonl').write_bytes(append)
 record=dict(schema='exact-science-verification76/verified-v1',status='VERIFIED',advance_id=ID,verifier_id=ACTOR,owner_id='companion_root_20261005',verified_commit=SCI,checked_commit=SCI,parent=PARENT,actual_transition_PID=os.getpid(),transition_count=1,
  ledger_before=dict(path=LEDGER.relative_to(ROOT).as_posix(),prefix_offset=0,RAW_bytes=len(old),RAW_sha256=sha(old)),ledger_after=dict(path=LEDGER.relative_to(ROOT).as_posix(),prefix_offset=0,RAW_bytes=len(new),RAW_sha256=sha(new)),exact_append=pin(OWN/'ledger.append.exactraw.jsonl'),before_prefix_preserved_exactly=True,event=event,
  decision=pin(OWN/'decision.json'),source_audit=pin(OWN/'source-math-binding-fakeclosure.json'),gate=pin(OWN/'gates.json'),fake_closure_scan=dict(status='PASS',hits=0),fresh_Lean_reused_PID=28496,axioms_reused_PID=29336,
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
 payload=dict(payload_name='COMPLETE_EXACT_SCI76_VERIFICATION_DECISION_INPUT',decision=read('decision.json'),inputs=read('inputs.manifest.json'),Git_input_bindings=read('Git-inputs.json'),binding_source_scan=read('source-math-binding-fakeclosure.json'),commit_retention=read('commit-retention.json'),gates=read('gates.json'),whitespace=read('whitespace.json'),ledger_before=read('ledger.before-prefix.json'),transition=read('transition.result.json'),shared_verified=pin(R/'verified.json'),output_baseline=read('outputs.baseline.manifest.json'),all_observer_negatives=[pin(p) for p in sorted(OWN.glob('negative.*'))])
 write('complete-named-verification.payload.json',payload);run=dict(schema='exact-science-verification76/run-v1',status='ACCEPTED_VERIFIED_EXACT_SCI76',checked_commit=SCI,parent=PARENT,actor=ACTOR,VERIFIED=True,decision=pin(OWN/'decision.json'),inputs_manifest=pin(OWN/'inputs.manifest.json'),complete_named_RAW_payload=pin(OWN/'complete-named-verification.payload.json'),transition=pin(OWN/'transition.result.json'),shared_verified=pin(R/'verified.json'),wholelogical_recipe='UTF8 JSON ensure_ascii=false sort_keys=true separators comma/colon; delete ONLY top-level run_sha256.',all_owned_manifest='Final CLOSED_LAST lease binds every owned output except only itself.',aggregate=False,current_reader=False,main_live=False,PURIFIED=False,full_Exposition_Seal=False,whole_paper=False,Goal_complete=False)
 run['run_sha256']=sha(canon(run));write('run.json',run);print(json.dumps(dict(status='FINALIZED',actual_PID=os.getpid(),whole_logical_run_sha256=run['run_sha256'],named=run['complete_named_RAW_payload'])))

def readback():
 transition_readback();run=read('run.json');h=run.pop('run_sha256');assert sha(canon(run))==h;check(run['complete_named_RAW_payload']);check(run['shared_verified']);print(json.dumps(dict(status='READBACK_PASS',actual_PID=os.getpid(),whole_logical_run_sha256=h,named_RAW_sha256=run['complete_named_RAW_payload']['RAW_sha256'])))

def close_probe():readback()

def close():
 assert not (OWN/'lease.final.json').exists();readback();assert launch('close_probe')==0;rows=allowned(('lease.final.json',));write('lease.final.json',dict(status='CLOSED_LAST',actor=ACTOR,actual_last_writer_PID=os.getpid(),closed_utc=now(),owned_count=len(rows)+1,all_owned_outputs_except_only_self=rows,closure_logical_sha256=sha(canon(rows)),whole_logical_run_sha256=read('run.json')['run_sha256'],complete_named_RAW_payload=pin(OWN/'complete-named-verification.payload.json'),final_owned_write=True,all_sessions_closed=True,postclose_owned_writes=False,VERIFIED=True,verified_commit=SCI,only_shared_writes='Exactly1 independent VERIFIED append plus r76/verified.json; no canonical/Git/aggregate/site write.'));print(json.dumps(dict(status='CLOSED_LAST',actual_PID=os.getpid(),owned_count=len(rows)+1,lease=pin(OWN/'lease.final.json'))))

def postclose():
 lease=read('lease.final.json');rows=allowned(('lease.final.json',));assert rows==lease['all_owned_outputs_except_only_self'] and sha(canon(rows))==lease['closure_logical_sha256'];readback();print(json.dumps(dict(status='READONLY_POSTCLOSE_PASS',actual_PID=os.getpid(),owned_count=len(rows)+1,total_RAW_bytes=sum(p.stat().st_size for p in OWN.rglob('*') if p.is_file()),lease=pin(OWN/'lease.final.json'),closure_logical_sha256=lease['closure_logical_sha256'],owned_writes=False)))

def launch(action):
 assert not (OWN/'lease.final.json').exists();self=Path(__file__);(OWN/(action+'.executed-helper.RAW.py')).write_bytes(self.read_bytes());argv=[PY,'-B','-X','utf8',str(self),'_child',action]
 with (OWN/(action+'.stdout.log')).open('wb') as out,(OWN/(action+'.stderr.log')).open('wb') as err:
  p=subprocess.Popen(argv,cwd=ROOT,stdout=out,stderr=err);print(json.dumps(dict(status='RUNNING',actual_PID=p.pid,action=action,runner_PID=os.getpid())),flush=True);code=p.wait()
 write(action+'.receipt.json',dict(action=action,actual_PID=p.pid,runner_PID=os.getpid(),command=argv,exit_code=code,terminal_closed=True,stdout=pin(OWN/(action+'.stdout.log')),stderr=pin(OWN/(action+'.stderr.log')),executed_helper=pin(OWN/(action+'.executed-helper.RAW.py'))));print(json.dumps(dict(status='TERMINAL',actual_PID=p.pid,action=action,exit_code=code)));return code

def all_files(p):return [x for x in p.rglob('*') if x.is_file()]

def recheck():
 assert git(['rev-parse','HEAD']).decode().strip()==SCI
 assert git(['rev-list','--parents','-n','1',SCI]).decode().split()==[SCI,PARENT]
 for row in read('inputs.manifest.json')['inputs']:check(row)

def freeze():
 assert git(['rev-parse','HEAD']).decode().strip()==SCI
 assert git(['rev-list','--parents','-n','1',SCI]).decode().split()==[SCI,PARENT]
 a=read('authorization76.json');assert a['exact_commit']==SCI and a['explicit_exact_commit_permission']
 names=['proved-local.json','claim.json','mathematics-freeze76.json','publication-plan.json','expanded76.frozen.header.lean','neutral-expanded-binders76.json','source-review.clean.packet.json','root.math76.adoption.json','root.source76.adoption.json','root.decoder76.adoption.json','audit.before-decoder76.exactraw.snapshot.json','audit.before-source-admission76.exactraw.json','cell.before-source-admission76.exactraw.json','publication.before-source-admission76.exactraw.json','independent-math76/lease.final.json','independent-math76/run.json','independent-math76/inputs.manifest.json','independent-math76/analysis.inputs.manifest.json','independent-math76/fresh-compiler.json','independent-math76/complete-named-mathematical-review.payload.json','anonymous-decoder/CLOSED_LAST.json','anonymous-decoder/run.json','anonymous-decoder/decoded.root-adapter.json','whitespace-diagnosis76/diagnosis.json','whitespace-diagnosis76/full-staged-immutable-negative.raw.gz','commit-science76/receipt.json']
 snames=['CLOSED_LAST.json','review-logical-run76.json','review-logical-run76.raw.json','compiled-source-review76.json','compiled-source-coverage76.json','compiled-source-topology76.json','canonical-cell-source-proof-coverage76.json','canonical-publication-source-proof-coverage76.json','source-only.freeze76.json','candidate-intake76.json']
 paths=[MODULE,CELL,PUB,LESSON,AUDIT,ROOT/'lean-toolchain',ROOT/'lake-manifest.json',ROOT/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualHarmonicFlow.lean',ROOT/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualBounceRate.lean',ROOT/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualHazardClock.lean',PRE/'header76.v3.proposed.lean',PRE/'root.statement-seal76.json']+[R/n for n in names]+[SOURCE/n for n in snames]
 paths += [ROOT/'tools'/n for n in ['astis.py','astis_advance.py','astis_publication.py','astis_contributor_contract.py','astis_semantic_roundtrip.py','astis_frontier_cells.py']]
 rows=[pin(p) for p in paths];assert len({x['path'] for x in rows})==len(rows)
 core=[]
 for p in paths:
  name=p.relative_to(ROOT).as_posix()
  if p==R/'commit-science76/receipt.json':core.append(dict(file=pin(p),classification='POSTCOMMIT_EXTERNAL_EXECUTION_RECEIPT; causally excluded from own SCI'));continue
  b=git(['show',SCI+':'+name]);raw=p.read_bytes();equal=b==raw;assert equal or b.replace(b'\r\n',b'\n')==raw.replace(b'\r\n',b'\n'),name
  core.append(dict(file=pin(p),Git_RAW_sha256=sha(b),Git_RAW_bytes=len(b),current_Git_RAW_equal=equal,CRLF_only_LF_qualification=not equal))
 assert sha(MODULE.read_bytes())==EXPECTED and len(MODULE.read_bytes().splitlines())==412
 write('inputs.manifest.json',dict(input_count=len(rows),inputs=rows,LF_recipe=RECIPE,storage='Finite exact RAW/LF references; no recursive history copies or full ledger. Existing closed native bytes checked in place.'))
 write('Git-inputs.json',dict(actual_PID=os.getpid(),checked_commit=SCI,parent=PARENT,files=core))
 write('lease.open.json',dict(status='OPEN_EXACT_SCI76',actual_PID=os.getpid(),actor=ACTOR,checked_commit=SCI,parent=PARENT))
 b=LEDGER.read_bytes();s=state();assert s['state']=='PROVED_LOCAL' and s['owner_id']=='companion_root_20261005' and s['publication_declarations']==[DECL];assert not (R/'verified.json').exists()
 write('ledger.before-prefix.json',dict(path=LEDGER.relative_to(ROOT).as_posix(),RAW_bytes=len(b),RAW_sha256=sha(b),target_state=s,storage='Exact complete prefix hash/length, retained in original append-only ledger; later verify unchanged prefix plus one exact append.'))
 print(json.dumps(dict(status='FROZEN',actual_PID=os.getpid(),input_count=len(rows),checked_commit=SCI)))

def gates():
 recheck();checks=[('frontier',['tools/astis_frontier_cells.py','check']),('publication',['tools/astis_publication.py','check','--base',PARENT]),('contributor',['tools/astis_contributor_contract.py','check','--base',PARENT]),('semantic',['tools/astis_semantic_roundtrip.py','check']),('packet',['tools/astis_publication.py','packet','--cell','ASTIS-SW-PBPS-actual-finite-jump-recursion'])]
 rows=[process(label,[PY,'-B','-X','utf8',*args]) for label,args in checks]
 sys.path[:0]=[str(ROOT),str(ROOT/'tools')];import astis_publication;astis_publication.check_advance([DECL],reviewed=True)
 write('gates.json',dict(status='PASS',actual_PID=os.getpid(),checked_commit=SCI,diff_base=PARENT,receipts=rows,reviewed_source_gate=dict(function='astis_publication.check_advance',publication_declarations=[DECL],reviewed=True,status='PASS'),new_Lean_compilation=False,fresh_Lean_reused_PID=28496,axioms_reused_PID=29336,full_root_site_or_aggregate=False))
 print(json.dumps(dict(status='REQUIRED_CURRENT_GATES_PASS',actual_PID=os.getpid(),gates=len(rows))))

def native_binding():
 recheck();packages=[];ma=load(R/'root.math76.adoption.json');M=R/'independent-math76';ml=load(M/'lease.final.json');check(ma['native_lease']);assert ml['status']=='CLOSED_LAST' and ml['owned_count']==82
 mrows=ml['all_owned_outputs_except_only_self'];assert len(mrows)==81
 for row in mrows:check(row)
 assert {path(q['path']).resolve() for q in mrows}=={p.resolve() for p in all_files(M) if p.name!='lease.final.json'}
 mr=load(M/'run.json');mh=mr.pop('run_sha256');assert sha(canon(mr))==mh==ma['native_whole_logical_run_sha256'];check(ma['native_complete_named']);check(mr['complete_named_RAW_payload']);assert len(all_files(M))==82
 mi=load(M/'inputs.manifest.json');assert mi['total_input_rows']==14
 for row in mi['inputs']+mi['supplemental_inputs']:
  check(row['original'])
  if 'snapshot' in row:check(row['snapshot'])
 ai=load(M/'analysis.inputs.manifest.json')
 for row in ai['API_inputs']:check(row['original']);check(row['fragment'])
 check(ai['expanded_header_input'])
 fresh=load(M/'fresh-compiler.json');assert fresh['fresh_source_elaboration'] and not fresh['Lake_build_cache_replay'] and fresh['actual_foreground_Lean_PID']==28496 and fresh['axioms_PID']==29336 and fresh['terminal_EXIT']==0 and fresh['module']['RAW_sha256']==EXPECTED
 for k in ['compiler_receipt','axiom_receipt','output_olean','real_Lean_executable','version_receipt','Lake_environment_receipt','axiom_driver']:check(fresh[k])
 comp=load(path(fresh['compiler_receipt']['path']));ax=load(path(fresh['axiom_receipt']['path']));assert comp['exit_code']==ax['exit_code']==0 and comp['actual_PID']==28496 and ax['actual_PID']==29336
 for rec in [comp,ax]:check(rec['stdout']);check(rec['stderr'])
 b=MODULE.read_bytes();assert len(b)==22655 and len(b.splitlines())==412 and sha(b)==EXPECTED and path(fresh['axiom_driver']['path']).read_bytes()==b+fresh['axiom_driver_only_suffix'].encode()
 axtext=path(ax['stdout']['path']).read_text(encoding='utf-8');m=re.search(r'depends on axioms:\s*\[([^\]]+)\]',axtext,re.S);assert m and [x.strip() for x in m.group(1).split(',')]==['propext','Classical.choice','Quot.sound']==fresh['standard_axioms']
 packages.append(dict(package='independent-whole-math76',owned_count=82,lease=pin(M/'lease.final.json'),native_whole_logical_run_sha256=mh,complete_named_RAW=ma['native_complete_named'],fresh_direct_Lean_reused_PID=28496,axioms_reused_PID=29336,new_Lean_compilation=False,all14_math_inputs_current=True))
 sa=load(R/'root.source76.adoption.json');sl=load(SOURCE/'CLOSED_LAST.json');check(sa['native_lease']);check(sa['native_named_payload']);check(sa['native_report']);assert sl['state']=='CLOSED_LAST' and sl['file_count_before_marker']==120 and len(sl['files'])==120
 for row in sl['files']:
  q=pin(SOURCE/row['path']);assert q['RAW_bytes']==row['RAW_bytes'] and q['RAW_sha256']==row['RAW_sha256'] and q['LF_bytes']==row['CRLF_to_LF_only_bytes'] and q['LF_sha256']==row['CRLF_to_LF_only_sha256']
 assert {q['path'] for q in sl['files']}=={p.relative_to(SOURCE).as_posix() for p in all_files(SOURCE) if p.name!='CLOSED_LAST.json'} and len(all_files(SOURCE))==121
 sr=load(SOURCE/'review-logical-run76.raw.json');raw=(SOURCE/'review-logical-run76.raw.json').read_bytes();assert raw==(SOURCE/'review-logical-run76.json').read_bytes() and sha(raw)==sa['native_whole_logical_run_sha256']==sl['review_run_sha256'] and 'run_sha256' not in sr and 'review_run_sha256' not in sr
 report=load(SOURCE/'compiled-source-review76.json');assert report['state']=='accepted' and report['verdict']=='equivalent-after-elaboration' and report['source_or_publication_mathematical_repair_required'] is False
 assert sr['candidate_access_authorized_after_source_freeze'] and sr['prior_verdicts_or_other_reviewer_outcomes_seen'] is False and sr['canonical_audit_cell_publication_contents_seen'] is False and sr['hash_only_pins_used_as_content'] is False
 sourcefirst=load(SOURCE/'source-only.freeze76.json');assert sourcefirst['anti_anchoring']['source_first_extraction'] and all(v is False for k,v in sourcefirst['anti_anchoring'].items() if k!='source_first_extraction')
 cov=load(SOURCE/'compiled-source-coverage76.json');assert cov['counts']==dict(blocks=131,node=44,excluded=87,subclaims=9,external_citations=12) and len(cov['inventory'])==131 and sum(x['disposition']=='NODE' for x in cov['inventory'])==44 and sum(x['disposition']=='EXCLUDED' for x in cov['inventory'])==87
 assert len(cov['open_optional_subclaims'])==1 and cov['open_optional_subclaims'][0]['compiled76_projection']['status']=='OPEN_OPTIONAL_NOT_CLAIMED'
 assert sha((SOURCE/'compiled-source-coverage76.json').read_bytes())==sr['source_coverage_artifact_sha256'] and sha((SOURCE/'compiled-source-topology76.json').read_bytes())==sr['source_topology_artifact_sha256']
 readable=[]
 for row in sr['readable_input_manifest']:
  current=check(row);copy=SOURCE/row['own_raw_copy'];assert copy.read_bytes()==path(row['path']).read_bytes();readable.append(dict(original=current,native_snapshot=pin(copy),current_exact_RAW=True))
 audit=load(AUDIT);cell=load(CELL);pub=load(PUB);before_a=load(R/'audit.before-source-admission76.exactraw.json');before_c=load(R/'cell.before-source-admission76.exactraw.json');before_p=load(R/'publication.before-source-admission76.exactraw.json')
 expected=json.loads(json.dumps(before_a));nf=report['audit_fields']
 for k in ['state','semantic_slots','verdict','repairs']:expected[k]=nf[k]
 converted=[]
 for delta in nf['deltas']:
  assert delta['kind']=='explicit-elaboration' and delta['blocking'] is False
  z=dict(delta);z.update(severity='informational',description=delta['classification']+': '+delta['source']+' '+delta['lean']);converted.append(z)
 expected['deltas']=converted
 nsr=dict(report['source_review']);assert 'run_artifact' not in nsr;nsr['run_artifact']=(SOURCE/'review-logical-run76.json').relative_to(ROOT).as_posix();assert path(nsr['run_artifact']).read_bytes()==raw
 expected['source_review']=nsr;assert expected==audit,'canonical audit must equal exact native projection plus only4delta schema fields and run locator'
 assert set(nf['semantic_slots'])=={'objects','domains','quantifiers','assumptions','conclusion','scopes','constant_dependencies'} and len(nf['deltas'])==4 and nf['repairs']==[]
 cp=load(SOURCE/'canonical-cell-source-proof-coverage76.json')['source_proof_coverage'];pp=load(SOURCE/'canonical-publication-source-proof-coverage76.json')['source_proof_coverage'];assert cell['source_proof_coverage']==cp and pub['items'][0]['source_proof_coverage']==pp
 dc=differences(before_c,cell);dp=differences(before_p,pub);assert all(x.split('/')[1] in ['source_proof_coverage','conceptual_mirror_audit','evidence','status'] for x in dc) and all(x.startswith('/items/0/source_proof_coverage/') for x in dp)
 assert cell['status']=='proved_locally' and cell['conceptual_mirror_audit']['status']=='none-found'
 maps={AUDIT.relative_to(ROOT).as_posix():R/'audit.before-source-admission76.exactraw.json',CELL.relative_to(ROOT).as_posix():R/'cell.before-source-admission76.exactraw.json',PUB.relative_to(ROOT).as_posix():R/'publication.before-source-admission76.exactraw.json'}
 finite=[]
 for row in sr['hash_only_manifest']:
  key=path(row['path']).relative_to(ROOT).as_posix();hist=maps[key];check(dict(row,path=hist.as_posix()));finite.append(dict(current=pin(path(row['path'])),historical=pin(hist),classification='Source reviewer hash-only input; exact pre-admission historical snapshot, never content-read source evidence',changed_pointers=differences(load(hist),load(path(row['path'])))))
 draft=load(R/'audit.before-decoder76.exactraw.snapshot.json');assert differences(draft,before_a)==['/reconstruction','/state']
 packages.append(dict(package='fresh-anti-anchored-source76',owned_count=121,lease=pin(SOURCE/'CLOSED_LAST.json'),native_report=pin(SOURCE/'compiled-source-review76.json'),native_whole_run_RAW_sha256=sha(raw),native_hash_recipe='Complete immutable RAW UTF8 JSON bytes; no run/self hash field and no deletion/reserialization.',complete_named_RAW=pin(SOURCE/'review-logical-run76.raw.json'),source_slots=7,source_inventory=cov['counts'],explicit_nonblocking_deltas=4,blocking_deltas=0,mathematical_repairs=0,run_locator_addition_only=True))
 da=load(R/'root.decoder76.adoption.json');check(da['native_lease']);check(da['native_complete_payload']);dl=load(R/'anonymous-decoder/CLOSED_LAST.json');assert dl['status']=='CLOSED' and dl['closed_exit_receipt']['exit_code']==0 and dl['closed_exit_receipt']['actual_PID']==44928
 original_dir=path(dl['bound_prior_owned_files'][0]['path']).parent
 for row in dl['bound_prior_owned_files']:
  check(row);assert path(row['path']).read_bytes()==(R/'anonymous-decoder'/Path(row['path']).name).read_bytes()
 assert len(all_files(original_dir))==4 and path(da['native_lease']['path']).read_bytes()==(R/'anonymous-decoder/CLOSED_LAST.json').read_bytes()
 check(dl['sole_input_receipt']);assert path(dl['sole_input_receipt']['path']).read_bytes()==(R/'anonymous-decoder/parent-packet.json').read_bytes()
 dr=load(R/'anonymous-decoder/run.json');preimage=dict(dr['logical_run_payload']);preimage.pop('decoder_run_sha256');assert canon(preimage)==dr['canonical_logical_run_utf8'].encode() and sha(canon(preimage))==dr['decoder_run_sha256']==da['native_whole_logical_run_sha256']
 native=load(R/'anonymous-decoder/reconstruction.json');adapter=load(R/'anonymous-decoder/decoded.root-adapter.json');assert adapter['native_complete_reconstruction']==native and adapter['native_complete_run']==dr and native['scopes']==native['scopes_senses']
 packet=load(R/'source-review.clean.packet.json');assert native['reconstructed_theorem_text']==audit['reconstruction']['text']==packet['blind_reconstruction']['text']
 assert packet['packet_sha256']==report['packet_sha256']==sr['packet_sha256']==audit['source_review']['reviewer_packet_sha256']
 assert packet['publication_binding_sha256']==audit['publication_binding_sha256']==report['publication_binding_sha256']=='ef7ddf32173166e15704713b04a186c1ae19f324f9d555083a416ed5af930c11' and packet['candidate_publication_context']==audit['publication_context']
 packages.append(dict(package='strict-source-blind-decoder76',owned_count=4,root_archive_count=len(all_files(R/'anonymous-decoder')),native_lease=pin(path(da['native_lease']['path'])),native_run_sha256=dr['decoder_run_sha256'],native_custom_preimage='Canonical logical_run_payload minus only decoder_run_sha256',source_visible=False,proof_visible=False,scope_alias_only=True))
 text=b.decode();private=text[text.index('private def actual_fixed_reference_finite_jump_recursion_statement'):text.index('/--',text.index('private def actual_fixed_reference_finite_jump_recursion_statement'))] if '/--' in text[text.index('private def actual_fixed_reference_finite_jump_recursion_statement'):] else ''
 # Exact declared definition ends immediately before the public theorem; comments/options may follow.
 pstart=text.index('private def actual_fixed_reference_finite_jump_recursion_statement');tstart=text.index('theorem actual_fixed_reference_finite_jump_recursion',pstart);header=(R/'expanded76.frozen.header.lean').read_text(encoding='utf-8');dpart=text[pstart:tstart];args,result=dpart.split(' : Prop :=',1);result=result[:result.index('/--')] if '/--' in result else result
 # The declaration doc-comment occurs between definition and public theorem. Strip comments and command options explicitly below.
 sys.path[:0]=[str(ROOT),str(ROOT/'tools')];import astis
 clean=astis.strip_lean_comments_and_strings(dpart);args,result=clean.split(' : Prop :=',1);result=re.split(r'\nset_option ',result)[0]
 reconstructed=args.replace('private def actual_fixed_reference_finite_jump_recursion_statement','theorem actual_fixed_reference_finite_jump_recursion',1)+' :'+result
 assert reconstructed.split()==header.split(),'full private literal must expand to exact sealed header'
 expanded='theorem actual_fixed_reference_finite_jump_recursion'+packet['lean']['statement']+'\n';assert expanded.encode()==(R/'expanded76.frozen.header.lean').read_bytes()
 public=text[tstart:text.index(':= by',tstart)];publicargs=public[:public.index(' :\n    actual_fixed_reference_finite_jump_recursion_statement')];assert publicargs.split()==args.replace('private def actual_fixed_reference_finite_jump_recursion_statement','theorem actual_fixed_reference_finite_jump_recursion',1).split() and 'actual_fixed_reference_finite_jump_recursion_statement hα hαβ hV hH hη hβη' in public
 unit=load(LESSON)['units'][0];assert unit['declaration']==DECL and len(unit['steps'])==10;steps=[];lines=b.splitlines(keepends=True)
 for i,step in enumerate(unit['steps']):
  reg=step['lean_source_region'];span=b''.join(lines[reg['start_line']-1:reg['end_line']]);assert reg['source_raw_sha256']==sha(b) and span==step['lean'].encode() and sha(span)==reg['exact_code_raw_sha256'] and reg['start_line']>=193
  steps.append(dict(index=i+1,formula=step['formula'],region=reg,literal_BODY_match=True))
 stripped=astis.strip_lean_comments_and_strings(text);hits=[dict(line=i+1,text=s.strip()) for i,s in enumerate(stripped.splitlines()) if astis.FORBIDDEN_REGEX.search(s)];assert not hits
 inventory=re.findall(r'^(private )?(def|theorem|lemma|axiom|opaque)\s+([^\s:]+)',stripped,re.M);assert inventory==[('private ','def','actual_fixed_reference_finite_jump_recursion_statement'),('','theorem','actual_fixed_reference_finite_jump_recursion')]
 for name in ['ActualHarmonicFlow.actual_harmonic_flow_laws','ActualBounceRate.actual_bounce_rate_energy_laws','ActualHazardClock.actual_integrated_hazard_clock_laws']:assert name in text
 for field in [cell['shared_floor_audit']['searched'],cell['reuse_plan']['searched_existing']]:assert any('Samplinglib' in x for x in field) and any('Mathlib' in x for x in field)
 write('source-math-binding-fakeclosure.json',dict(status='PASS',actual_PID=os.getpid(),checked_commit=SCI,parent=PARENT,packages=packages,native_owned_count=207,math_inputs_current=14,source_readable15_inputs_current=readable,source_hash_only3_exact_historical_maps=finite,draft_to_blind_exact_map=dict(before=pin(R/'audit.before-decoder76.exactraw.snapshot.json'),after=pin(R/'audit.before-source-admission76.exactraw.json'),changed_pointers=['/reconstruction','/state']),canonical_admission_differences=dict(audit=differences(before_a,audit),cell=dc,publication=dp),native_schema_adapter=dict(retained_native_delta_count=4,added_only_top_delta_fields=['severity','description'],severity='informational',description_recipe='classification + colon + source + space + lean',source_review_addition_only=dict(run_artifact=nsr['run_artifact'],resolves_complete_exact_native_RAW=True),native_verdict_unchanged=True),module=pin(MODULE),module_lines=412,source_callers=6,literal_let_definitions=['c','Φ','S','rate','H','C','Λ','τ','next','record','eventTime'],conclusion_groups=10,exact_BODY_steps=steps,private_literal_full_expansion_matches_sealed=True,private_providers=0,source_slots=7,source_blocking_deltas=0,mathematical_repairs=0,source_run_sha256=sha(raw),publication_binding_sha256=audit['publication_binding_sha256'],packet_sha256=packet['packet_sha256'],fake_closure_hits=hits,declaration_inventory=inventory,fresh_Lean_reused=fresh,new_Lean_compilation=False,source_stale_coordinate_notes_retained=sr['provenance_notes'],boundary='Deterministic fixed-reference finite/stopped actual A.2 recursion only. Arbitrary nonnegative thresholds, no phase at infinity; iid/nonaccumulation/global process/Markov/invariance/terminal sampler/main/error/cost/composition/aggregate/reader/PURIFIED/whole-paper/Goal remain open.'))
 print(json.dumps(dict(status='NATIVE_SOURCE_MATH_BINDING_SCAN_PASS',actual_PID=os.getpid(),native_owned_count=207,source_slots=7,exact_BODY_steps=10,reused_direct_Lean_PID=28496,axioms_PID=29336)))


def whitespace():
 recheck();rec=process('full-RAW-whitespace',['git','-c','core.whitespace=cr-at-eol','diff','--check',PARENT,SCI],accepted=(0,1,2));raw=path(rec['stdout']['path']).read_bytes()
 parse=lambda z:[dict(path=m.group(1),line=int(m.group(2)),kind=m.group(3)) for m in re.finditer(r'^(.+):(\d+): (trailing whitespace|new blank line at EOF)\.',z.decode(),re.M)]
 findings=parse(raw);diag=load(R/'whitespace-diagnosis76/diagnosis.json');assert findings==diag['findings'] and len(findings)==459 and rec['exit_code']!=0 and not diag['full_staged_whitespace_PASS']
 stored=gzip.decompress((R/'whitespace-diagnosis76/full-staged-immutable-negative.raw.gz').read_bytes());assert sha(stored)==diag['negative_RAW_sha256'] and parse(stored)==findings
 rows=[]
 for row in diag['immutable_raw_paths']:
  check(row);p=path(row['path']);assert git(['show',SCI+':'+row['path']])==p.read_bytes();rows.append(dict(file=pin(p),Git_RAW_equal=True,classification='Immutable exact source or successful/failed native terminal; preserve every RAW byte.'))
 names=sorted({x['path'] for x in findings});assert len(names)==len(rows)==14
 authored=process('authored-complement-whitespace',['git','-c','core.whitespace=cr-at-eol','diff','--check',PARENT,SCI,'--','.',*[':(exclude)'+n for n in names]])
 write('whitespace.json',dict(status='AUTHORED_PASS_RAW_NEGATIVE_RETAINED',actual_PID=os.getpid(),checked_commit=SCI,parent=PARENT,policy='core.whitespace=cr-at-eol',full_RAW_PASS=False,immutable_findings=459,exact_findings=findings,finite_exception_files=rows,RAW_terminal=rec,root_original_negative=dict(storage=pin(R/'whitespace-diagnosis76/full-staged-immutable-negative.raw.gz'),decompressed_RAW_bytes=len(stored),decompressed_RAW_sha256=sha(stored),fresh_RAW_exact_equal=stored==raw,exact_all_findings_equal=True),authored_complement_PASS=True,authored_terminal=authored,no_native_normalization=True))
 print(json.dumps(dict(status='WHITESPACE_QUALIFIED',actual_PID=os.getpid(),immutable_findings=459,exception_files=14,full_RAW_PASS=False,authored_PASS=True)))

def commit_retention():
 recheck();bound=[]
 for folder in [R/'independent-math76',SOURCE,R/'anonymous-decoder']:
  for p in sorted(all_files(folder)):
   name=p.relative_to(ROOT).as_posix();b=git(['show',SCI+':'+name]);assert b==p.read_bytes(),name;bound.append(dict(path=name,Git_RAW_bytes=len(b),Git_RAW_sha256=sha(b),current_Git_RAW_equal=True))
 assert len(bound)==209
 changes=git(['diff','--name-status',PARENT,SCI]).decode().splitlines();nonruns=[x for x in changes if not x.split('\t')[-1].startswith('runs/')]
 assert nonruns==['A\t'+p.relative_to(ROOT).as_posix() for p in [MODULE,CELL,AUDIT,LESSON,PUB]],nonruns
 for p in ['AutoSamplingTheory.lean','AutoSamplingTheory/TechnicalLemmas/Registry.lean','Tests.lean']:assert git(['rev-parse',PARENT+':'+p])==git(['rev-parse',SCI+':'+p])
 write('commit-retention.json',dict(status='PASS',actual_PID=os.getpid(),checked_commit=SCI,parent=PARENT,diff_paths=len(changes),exact_nonruns_delta=nonruns,closed_native_Git_RAW_files=len(bound),closed_native_Git_RAW_bindings=bound,original_blind4_exact_to_root_archive6=True,no_aggregate_import_Registry_root_tests_delta=True))
 print(json.dumps(dict(status='COMMIT_RETENTION_PASS',actual_PID=os.getpid(),diff_paths=len(changes),closed_native_Git_RAW_files=len(bound))))

def decision():
 recheck();assert read('gates.json')['status']=='PASS' and read('whitespace.json')['authored_complement_PASS'] and read('source-math-binding-fakeclosure.json')['fake_closure_hits']==[] and read('commit-retention.json')['status']=='PASS'
 before=read('ledger.before-prefix.json');assert sha(LEDGER.read_bytes())==before['RAW_sha256'] and state()['state']=='PROVED_LOCAL'
 write('decision.json',dict(schema='exact-science-verification76/decision-v1',status='ACCEPTED_EXACT_SCI76',accepted_exact_commit=True,checked_commit=SCI,parent=PARENT,actor=ACTOR,actual_PID=os.getpid(),owner_id='companion_root_20261005',publication_declarations=[DECL],module=pin(MODULE),math_and_source='Exact412-line source, same6callers/11literal definitions/10conclusion groups/10literal BODY steps. Closed independent math82/fresh anti-source121/strictblind4 retained and exact Git RAW checked. Independent fresh directLean28496/axioms29336 standard3 reused by exact module/toolchain/manifest pins; no new compilation claimed. Four native explicit-elaboration deltas remain visible with informational schema additions; native source_review is copied plus only exact run_artifact locator.',all_required_current_gates_PASS=True,accepted_current_source_review=True,gates=pin(OWN/'gates.json'),source_audit=pin(OWN/'source-math-binding-fakeclosure.json'),fake_closure_hits=0,whitespace=pin(OWN/'whitespace.json'),commit_retention=pin(OWN/'commit-retention.json'),observer_negatives=[pin(p) for p in sorted(OWN.glob('negative.*'))],authorized_next_action='Exactly one nonowner VERIFIED transition for exact SCI76 only.',remaining_boundary='Only actual fixed-reference deterministic finite/stopped jump recursion and Borel/energy/cap/waiting laws. No iid realization/SLLN/nonaccumulation/all-time process/Markov/invariance/terminal kernel/main/error/expected-query cost/actual-input composition.',aggregate=False,current_reader=False,main_live=False,full_Exposition_Seal=False,PURIFIED=False,whole_paper=False,Goal_complete=False))
 print(json.dumps(dict(status='ACCEPTED_EXACT_SCI76',actual_PID=os.getpid(),transition_not_yet_called=True)))

if __name__=='__main__':
 try:
  action=sys.argv[-1]
  if sys.argv[1]=='_child':sys.exit(globals()[action]() or 0)
  elif action in ['close','postclose']:globals()[action]()
  else:sys.exit(launch(action))
 except BaseException as e:
  if not isinstance(e,SystemExit) and not (OWN/'lease.final.json').exists():write('negative.'+sys.argv[-1]+'.'+str(os.getpid())+'.json',dict(actual_PID=os.getpid(),mode=sys.argv[-1],error=repr(e),traceback=traceback.format_exc(),canonical_mutation_by_this_observer=False))
  raise
