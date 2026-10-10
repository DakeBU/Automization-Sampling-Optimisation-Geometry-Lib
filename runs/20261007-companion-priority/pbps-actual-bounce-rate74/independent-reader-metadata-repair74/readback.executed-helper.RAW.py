from pathlib import Path
import hashlib,json,os,re,subprocess,sys
ROOT=Path('E:/Samplinglib');R=ROOT/'runs/20261007-companion-priority/pbps-actual-bounce-rate74';OWN=R/'independent-reader-metadata-repair74';PROPOSAL=R/'reader-metadata-overlay74';SELF=Path(__file__)
PY='C:/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe';ACTOR='/root/exact_science63';RECIPE='Replace CRLF byte pairs with LF only; preserve bare CR and every other byte.'
MODULE=ROOT/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualBounceRate.lean'
def sha(b):return hashlib.sha256(b).hexdigest()
def canon(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def load(p):return json.loads(p.read_bytes())
def read(n):return load(OWN/n)
def write(n,x):(OWN/n).write_bytes(json.dumps(x,ensure_ascii=False,sort_keys=True,indent=2).encode()+b'\n')
def pin(p):
 b=p.read_bytes();return dict(path=p.relative_to(ROOT).as_posix(),RAW_bytes=len(b),RAW_sha256=sha(b),LF_sha256=sha(b.replace(b'\r\n',b'\n')))
def check(row):
 p=Path(row['path']);p=p if p.is_absolute() else ROOT/p;q=pin(p)
 for k in ['RAW_bytes','RAW_sha256','LF_sha256']:assert q[k]==row[k],(p,k)
 return q
def diff(a,b,p=''):
 if isinstance(a,dict) and isinstance(b,dict):
  return [z for k in sorted(set(a)|set(b)) for z in ([p+'/'+k] if k not in a or k not in b else diff(a[k],b[k],p+'/'+k))]
 if isinstance(a,list) and isinstance(b,list) and len(a)==len(b):return [z for i,(x,y) in enumerate(zip(a,b)) for z in diff(x,y,p+'/'+str(i))]
 return [] if a==b else [p]
def at(x,p):
 for k in p.strip('/').split('/'):x=x[int(k)] if isinstance(x,list) else x[k]
 return x
def review():
 proposal=PROPOSAL/'proposal.json';assert pin(proposal)['RAW_sha256']=='1beb82dba5d687fd6fdcb1d6d26a48f14dff79c6f2db5846a655a8f42421b38b';p=load(proposal);assert p['status']=='PROPOSED_METADATA_ONLY_NOT_APPLIED' and len(p['rows'])==2
 paths=[proposal,MODULE,R/'mathematics-freeze74.json',ROOT/'website/content/declaration_lessons/pbps-actual-bounce-rate.json',ROOT/'research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261010-PBPSActualBounceRate.json']
 for i,row in enumerate(p['rows']):paths.extend([ROOT/row['path'],PROPOSAL/(str(i)+'.before.exactraw.snapshot.json'),PROPOSAL/(str(i)+'.proposed.exactraw.json')])
 write('inputs.manifest.json',dict(input_count=len(paths),inputs=[pin(x) for x in paths],LF_recipe=RECIPE,scope='Finite exact11 RAW/LF references; no old native package or source transcript replay.'))
 write('lease.open.json',dict(status='OPEN_METADATA_TWO_STRING_REPAIR_ONLY',actual_PID=os.getpid(),actor=ACTOR,proposal_creator='companion_root_20261005',source_observer='independent_primary69'))
 write('negative.initial-read.json',dict(tool_chunk='3c8314',exit_code=1,actual_PID=None,PID_exposed=False,diagnostic='Dispatch shorthand math-freeze74.json does not exist. Exact existing mathematics-freeze74.json located via bounded file listing and pinned. Proposal read succeeded; no canonical or owned write before observer failure.'))
 module=pin(MODULE);assert module['RAW_bytes']==10565 and module['RAW_sha256']=='fcec688033797683b44f279a4d22971598926e6af3e9682ad76493d37580937c'
 freeze=load(R/'mathematics-freeze74.json');mr=next(x for x in freeze['inputs'] if x['path'].replace('\\','/').endswith('/ActualBounceRate.lean'));check(mr);assert len(MODULE.read_bytes().splitlines())==211
 sys.path[:0]=[str(ROOT),str(ROOT/'tools')];import astis
 code=astis.strip_lean_comments_and_strings(MODULE.read_text(encoding='utf-8'));decls=re.findall(r'^(private )?(def|theorem|lemma|axiom|instance|abbrev|opaque)\s+(\S+)',code,re.M)
 assert decls==[('private ','def','actual_bounce_rate_energy_statement'),('','theorem','actual_bounce_rate_energy_laws')],decls
 prefix=code.split('theorem actual_bounce_rate_energy_laws')[0];assert ': Prop :=' in prefix and 'Measurable' in prefix and 'Continuous' in prefix and 'Real.sqrt' in prefix and '∀' in prefix
 assert re.search(r':\s*actual_bounce_rate_energy_statement hα hαβ hV hH hη hβη := by',code)
 hits=[dict(line=i+1,text=x.strip()) for i,x in enumerate(code.splitlines()) if astis.FORBIDDEN_REGEX.search(x)];assert not hits
 approved=[];expected=['/purification/dead_code_audit','/items/0/purification/dead_code_audit']
 for i,row in enumerate(p['rows']):
  assert row['json_pointer']==expected[i];before=PROPOSAL/(str(i)+'.before.exactraw.snapshot.json');after=PROPOSAL/(str(i)+'.proposed.exactraw.json');current=ROOT/row['path']
  assert before.read_bytes()==current.read_bytes();assert pin(before)['RAW_bytes']==row['before_RAW_bytes'] and pin(before)['RAW_sha256']==row['before_RAW_sha256'] and pin(before)['LF_sha256']==row['before_LF_sha256']
  assert pin(after)['RAW_bytes']==row['proposed_RAW_bytes'] and pin(after)['RAW_sha256']==row['proposed_RAW_sha256']
  a,b=load(before),load(after);assert diff(a,b)==[row['json_pointer']] and at(a,row['json_pointer'])==row['old'] and at(b,row['json_pointer'])==row['new']
  assert row['old']=='Pending one actual theorem implementation.'
  assert row['new']=='One implemented public theorem uses a complete private literal Prop definition as its statement record; the private definition is not a provider or proof certificate. This audit grants no PURIFIED or full-paper credit.'
  approved.append(dict(path=row['path'],json_pointer=row['json_pointer'],before=pin(before),proposed=pin(after),current=pin(current),old=row['old'],new=row['new'],exact_one_field_only=True,current_equals_before=True))
 decision=dict(schema='independent-reader-metadata-repair74/decision-v1',status='APPROVED_EXACT_TWO_STRING_METADATA_OVERLAY_ONLY',accepted=True,actor=ACTOR,actual_PID=os.getpid(),independent_of_root_proposal_and_source_observer=True,proposal=pin(proposal),approved_rows=approved,
  module=module,module_lines=211,public_theorems=1,private_literal_Prop_definitions=1,private_providers=0,declaration_inventory=decls,fake_closure_hits=hits,private_literal_complete_statement_record=True,
  reasoning='The current whole211-line module contains one implemented public theorem asserting the value of one complete private literal Prop definition. The private definition records the proposition and contributes no proof/provider/certificate. Replacing the stale planning sentence is accurate; every other JSON value is unchanged.',
  theorem_source_BODY_callers_counts_binding_targets_unchanged=True,lesson_audit_current_pinned_unchanged=True,proposal_does_not_change_semantic_audit_or_context=True,later_unpublished_context_recomputation='Root may recompute affected context after application; that is separate from this exact two-string approval and cannot invent source acceptance.',
  applied_by_reviewer=False,no_canonical_Lean_Git_ledger_writes=True,new_theorem_or_source_review_verdict=False,Lean_compile=False,VERIFIED=False,Exposition_Seal=False,PURIFIED=False,full_paper=False,Goal_complete=False)
 write('decision.json',decision);print(json.dumps(dict(status=decision['status'],actual_PID=os.getpid(),accepted=True,input_count=len(paths),approved_rows=len(approved),no_apply=True)))
def recheck():
 for row in read('inputs.manifest.json')['inputs']:check(row)
def allowned(exclude=()):return [pin(p) for p in sorted(OWN.rglob('*')) if p.is_file() and p.relative_to(OWN).as_posix() not in exclude]
def finalize():
 recheck();write('outputs.baseline.manifest.json',dict(stage='Preterminal baseline; final lease binds self and actual closure/terminal layers.',files=allowned(('outputs.baseline.manifest.json','complete-named-decision-input.payload.json','run.json','lease.final.json'))))
 payload=dict(payload_name='COMPLETE_TWO_STRING_READER_METADATA_REPAIR74',decision=read('decision.json'),input_manifest=read('inputs.manifest.json'),observer_negative=read('negative.initial-read.json'),output_baseline=read('outputs.baseline.manifest.json'));write('complete-named-decision-input.payload.json',payload)
 run=dict(schema='independent-reader-metadata-repair74/run-v1',status='APPROVED_METADATA_ONLY_CLOSED',actor=ACTOR,accepted=True,decision=pin(OWN/'decision.json'),inputs_manifest=pin(OWN/'inputs.manifest.json'),complete_named_RAW_payload=pin(OWN/'complete-named-decision-input.payload.json'),wholelogical_recipe='UTF8 JSON ensure_ascii=false sort_keys=true separators comma/colon; remove ONLY top-level run_sha256.',final_manifest='CLOSED_LAST lease binds every owned output except itself, including self and actual terminal layers.',applied=False,theorem_source_VERIFIED_Exposition_PURIFIED_Goal_credit=False)
 run['run_sha256']=sha(canon(run));write('run.json',run);print(json.dumps(dict(status='FINALIZED',actual_PID=os.getpid(),whole_logical_run_sha256=run['run_sha256'],complete_named_RAW_payload=run['complete_named_RAW_payload'])))
def readback():
 recheck();r=read('run.json');h=r.pop('run_sha256');assert sha(canon(r))==h;check(r['complete_named_RAW_payload']);assert read('decision.json')['accepted'];print(json.dumps(dict(status='READBACK_PASS_METADATA_ONLY',actual_PID=os.getpid(),whole_logical_run_sha256=h,named_RAW_sha256=r['complete_named_RAW_payload']['RAW_sha256'])))
def close_probe():readback()
def close():
 assert not (OWN/'lease.final.json').exists();readback();assert launch('close_probe')==0;rows=allowned(('lease.final.json',));write('lease.final.json',dict(status='CLOSED_LAST',actor=ACTOR,actual_last_writer_PID=os.getpid(),owned_count=len(rows)+1,all_owned_outputs_except_only_self=rows,closure_logical_sha256=sha(canon(rows)),run_sha256=read('run.json')['run_sha256'],complete_named_RAW_payload=pin(OWN/'complete-named-decision-input.payload.json'),final_owned_write=True,all_sessions_closed=True,postclose_owned_writes=False,approved=True,applied=False,canonical_Git_ledger_writes=False));print(json.dumps(dict(status='CLOSED_LAST',actual_PID=os.getpid(),owned_count=len(rows)+1,lease=pin(OWN/'lease.final.json'))))
def postclose():
 l=read('lease.final.json');rows=allowned(('lease.final.json',));assert rows==l['all_owned_outputs_except_only_self'] and sha(canon(rows))==l['closure_logical_sha256'];readback();print(json.dumps(dict(status='READONLY_POSTCLOSE_PASS',actual_PID=os.getpid(),owned_count=len(rows)+1,total_RAW_bytes=sum(p.stat().st_size for p in OWN.rglob('*') if p.is_file()),lease=pin(OWN/'lease.final.json'),closure_logical_sha256=l['closure_logical_sha256'],owned_writes=False)))
def launch(action):
 assert not (OWN/'lease.final.json').exists();(OWN/(action+'.executed-helper.RAW.py')).write_bytes(SELF.read_bytes());argv=[PY,'-B','-X','utf8',str(SELF),'_child',action]
 with (OWN/(action+'.stdout.log')).open('wb') as o,(OWN/(action+'.stderr.log')).open('wb') as e:
  p=subprocess.Popen(argv,cwd=ROOT,stdout=o,stderr=e);print(json.dumps(dict(status='RUNNING',actual_PID=p.pid,action=action,runner_PID=os.getpid())),flush=True);code=p.wait()
 write(action+'.receipt.json',dict(action=action,actual_PID=p.pid,runner_PID=os.getpid(),command=argv,exit_code=code,terminal_closed=True,stdout=pin(OWN/(action+'.stdout.log')),stderr=pin(OWN/(action+'.stderr.log')),executed_helper=pin(OWN/(action+'.executed-helper.RAW.py'))));print(json.dumps(dict(status='TERMINAL',actual_PID=p.pid,action=action,exit_code=code)));return code
if __name__=='__main__':
 action=sys.argv[-1]
 if sys.argv[1]=='_child':sys.exit(globals()[action]() or 0)
 elif action in ['close','postclose']:globals()[action]()
 else:sys.exit(launch(action))
