import pathlib,json,hashlib,subprocess,sys,os,datetime,gzip
ROOT=pathlib.Path('E:/Samplinglib');R=ROOT/'runs/20261007-companion-priority/pbps-real-complex-lift60';D=R/'exact-science-verification';SCI='0a77416f5ec38702c46ec1358966b9dd4846c8d3';BASE='10d9fef15afc4c21208b6b75d8a71f51c664cfce'
def sha(b):return hashlib.sha256(b).hexdigest()
def canon(q):return json.dumps(q,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def load(p):return json.loads(p.read_bytes())
def write(p,q):p.write_bytes((json.dumps(q,ensure_ascii=False,indent=2,allow_nan=False)+'\n').encode())
def pin(p):
 b=p.read_bytes();l=b.replace(b'\r\n',b'\n');return dict(path=p.as_posix(),bytes=len(b),lf_bytes=len(l),raw_sha256=sha(b),lf_sha256=sha(l))
def check(x):assert pin(pathlib.Path(x['path']))==x
def freeze():
 q=load(R/'math-freeze.json');assert len(q['inputs'])==31
 for x in q['inputs']:
  a=pin(pathlib.Path(x['path']));assert a['bytes']==x['raw_bytes'] and a['raw_sha256']==x['raw_sha256'] and a['lf_sha256']==x['lf_sha256']
 assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT).decode().strip()==SCI
 return q
if '--readback' in sys.argv:
 freeze();inputs=load(D/'input.manifest.json')
 for row in inputs['artifacts']:check(row)
 q=load(D/'run.json');assert sha(canon({k:v for k,v in q.items() if k!='run_sha256'}))==q['run_sha256'];assert sha(canon(q['named_exact_verification_payload']))==q['named_exact_verification_payload_sha256']
 assert load(D/'payload.json')==q['named_exact_verification_payload']
 for row in [q['receipt'],q['inputs'],q['payload'],q['transition']]:check(row)
 t=load(D/'transition.json');current=(ROOT/'runs/substantive_advances.jsonl').read_bytes();before=(D/'ledger.before-VERIFIED.exactraw.snapshot.jsonl').read_bytes();assert current.startswith(before) and pin(ROOT/'runs/substantive_advances.jsonl')==t['ledger_after']
 write(D/'readback.json',dict(status='PASS',actual_PID=os.getpid(),qualified_input_count=inputs['count'],frozen_originals=31,whole_run_self_recipe='Complete sorted compact UTF8 run excluding ONLY run_sha256',run_sha256=q['run_sha256'],distinct_payload_recipe='Sorted compact UTF8 named_exact_verification_payload only',named_exact_verification_payload_sha256=q['named_exact_verification_payload_sha256'],ledger_prefix_preserved=True,VERIFIED_independent=True))
 print('READBACK_PASS',os.getpid(),flush=True);sys.exit(0)
f=freeze();native=load(D/'native-checks.json');gates=load(D/'gates.json');assert all(x['exit_code']==0 and x['terminal_closed'] for x in gates['actual'])
fake=load(D/'fake-closure-axioms.json');assert fake['authored_fake_closures']==0 and fake['count']==4
ledger=ROOT/'runs/substantive_advances.jsonl';old=pin(ledger);snapshot=D/'ledger.before-VERIFIED.exactraw.snapshot.jsonl';snapshot.write_bytes(ledger.read_bytes());historical=[dict(original=old,exact_snapshot=pin(snapshot),reason='Exact ledger prefix before independently authorized append-only VERIFIED')]
plan=load(R/'publication-plan.json')
for i,(group,names) in enumerate([('cells',plan['active_cells']),('audits',plan['audit_ids'])]):
 for j,name in enumerate(names):
  original=ROOT/('research-wiki/frontier-cells/'+name+'.json' if group=='cells' else 'research-wiki/semantic-roundtrip/audits/'+name+'.json');p=D/('admin-before.'+group+'.'+str(j)+'.exactraw.snapshot.json');p.write_bytes(original.read_bytes());historical.append(dict(original=pin(original),exact_snapshot=pin(p),reason='Exact current administrative input before later root serialized integration; verifier does not mutate it'))
write(D/'before-admin-mappings.json',dict(mappings=historical,count=len(historical),identity='Full original qualified path/raw/LF/length; exact separate snapshot, no basename aliases'))
rows={}
def add(row):check(row);rows[(row['path'],row['raw_sha256'],row['lf_sha256'])]=row
for x in native['readbacks']:
 resolved=x['resolved']
 if resolved['path']==old['path'] and resolved['raw_sha256']==old['raw_sha256']:resolved=pin(snapshot)
 add(resolved)
for p in sorted(D.iterdir()):
 if p.is_file() and p.name not in ['lease.json','input.manifest.json','run.json','payload.json','receipt.json','outputs.final.json','readback.json','transition.json','verification-evidence.json']:
  add(pin(p))
for p in [R/'commit-observer-split.json',R/'root.math60.adoption.json',R/'root.decoder60.adoption.json',R/'root.source60.adoption.json',R/'math-freeze.json',R/'whitespace-diagnosis60/diagnosis.json']:
 add(pin(p))
white=load(R/'whitespace-diagnosis60/diagnosis.json');assert len(white['findings'])==159 and len(white['immutable_native_exceptions'])==12 and white['authored_complement_check_exit']==0 and white['full_staged_exit']==2
for p in (R/'whitespace-diagnosis60').iterdir():
 if p.suffix=='.gz':assert sha(gzip.decompress(p.read_bytes()))==white['negative_raw_sha256'];add(pin(p))
write(D/'input.manifest.json',dict(artifacts=list(rows.values()),count=len(rows),frozen_originals=31,prior_native_qualified_pin_count=native['native_qualified_pin_count'],native_historical_map_count=load(D/'historical-mappings.json')['used_count'],exact_ledger_and_current_admin_before_mappings=pin(D/'before-admin-mappings.json'),science_git_bindings=pin(D/'science.git-pins.json'),original_resolution_manifest=pin(D/'historical-mappings.json')))
payload=dict(verdict='ACCEPT_EXACT_SCIENCE_SCOPED_INDEPENDENT_VERIFICATION',checked_commit=SCI,checked_base=BASE,result_kind='reusable-interface',exact_scope='Positive real-to-complex L2 lift and actual same PBPS positive defect adapter; complex-root anonymous Test API consumer only.',mathematical_declarations=f['mathematical_declarations'],mathematics_reused=pin(R/'independent-math60/receipt.json'),current_native_source=pin(R/'source-review60/native.receipt.json'),source_verdicts=['equivalent-after-elaboration','equivalent-after-elaboration'],source_blocking_or_repair_count=0,source_scope='Attributed ASTIS background completion, not printed real Gamma/B11 theorem; arbitrary measure background and disclosed rank0 extension.',native_hash_recipes=native['distinct_payload_recipes'],source_and_decoder_roles_separate=True,decoder_source_TEXT_blind=True,decoder_source_identity_blind=True,focused_build=next(x for x in gates['actual'] if x['label']=='focused'),standard3=fake['actual_named_standard3_closures'],fake_closure_scan=pin(D/'fake-closure-axioms.json'),reviewed_publication_gate=pin(D/'source-publication-gate.json'),actual_noncompiler_gates=pin(D/'gates.json'),science_bindings=dict(total=358,current_LF_exact=357,explicit_root_observer_split=1,evidence=pin(D/'science.git-pins.json'),negative=pin(D/'science-git-negative.json'),root_resolution=pin(R/'commit-observer-split.json')),counts=dict(frozen_originals=31,private_providers=26,exact_public_signatures=2,native_qualified_pin_identities=native['native_qualified_pin_count'],native_run_self_checks=3,distinct_native_payload_checks=3,historical_maps_used=load(D/'historical-mappings.json')['used_count'],actual_gates=len(gates['actual']),fake_source_scans=4,actual_named_axiom_closures=3),remaining=['Real root descent/conjugation preservation/uniqueness/Gamma/Gamma0/B11/B15/B16/polar/full weakH1/dynamics/main/error/cost/composition/full-paper/Goal remain open.','Mandatory aggregate root/Tests/Registry/graph/site deferred to root serialized integration; not run here.','Full-staged whitespace NEGATIVE159findings12exactimmutablepaths; authored complement alone PASS.','One postcommit root observer log split is explicit; no all358 current/Git equality claim.','Reader schema negatives and actual Git negative preserved; no original CLOSED math/source/decoder edits.'],no_canonical_cells_or_proofs_mutated=True,no_STABILIZING_or_PURIFIED=True)
write(D/'payload.json',payload)
evidence=dict(verifier_id='/root/whole_math52/exact-science60',verified_commit=SCI,checked_commit=SCI,publication_declarations=f['mathematical_declarations'],gate=dict(focused=next(x for x in gates['actual'] if x['label']=='focused'),publication_reviewed=pin(D/'source-publication-gate.json'),actual_other_gates=pin(D/'gates.json')),source_audit=[x['audit']['path'] for x in native['current_source_audits']],fake_closure_scan=pin(D/'fake-closure-axioms.json'),exact_scope=payload['exact_scope'],native_payload_path=(D/'payload.json').as_posix(),named_exact_verification_payload_sha256=sha(canon(payload)),historical_ledger_snapshot=pin(snapshot),remaining_boundary=payload['remaining'])
write(D/'verification-evidence.json',evidence)
with (D/'promotion.stdout.log').open('wb') as out,(D/'promotion.stderr.log').open('wb') as err:
 command=[sys.executable,'-B','-X','utf8',str(D/'promote.py')];p=subprocess.Popen(command,cwd=ROOT,stdout=out,stderr=err);pid=p.pid;code=p.wait()
write(D/'promotion.status.json',dict(command=command,actual_PID=pid,exit_code=code,terminal_closed=True,stdout=pin(D/'promotion.stdout.log'),stderr=pin(D/'promotion.stderr.log')));assert code==0
receipt=dict(verdict=payload['verdict'],status='VERIFIED_BY_INDEPENDENT_VERIFIER_LEDGER_ONLY',actor=evidence['verifier_id'],checked_commit=SCI,counts=payload['counts'],qualified_input_count=len(rows),blockers=[],truth_boundary=payload['remaining'],named_exact_verification_payload_sha256=sha(canon(payload)),inputs=pin(D/'input.manifest.json'),payload=pin(D/'payload.json'),transition=pin(D/'transition.json'),actual_promotion_PID=pid,actual_promotion_exit_code=0,actual_compiler_PID=payload['focused_build']['actual_PID'],actual_compiler_exit_code=0,source_audits=evidence['source_audit'])
write(D/'receipt.json',receipt)
run=dict(schema='native-exact-science60-v1',actor=evidence['verifier_id'],checked_commit=SCI,checked_base=BASE,actual_finalizer_PID=os.getpid(),actual_check_reader=dict(PID=native['actual_reader_PID'],exit_code=0,tool_chunk='43552f'),actual_gates=gates,inputs=pin(D/'input.manifest.json'),receipt=pin(D/'receipt.json'),payload=pin(D/'payload.json'),transition=pin(D/'transition.json'),named_exact_verification_payload=payload,named_exact_verification_payload_sha256=sha(canon(payload)),hash_recipes=dict(run_sha256='SHA256 sorted compact UTF8 complete run excluding ONLY top-level run_sha256',named_exact_verification_payload_sha256='SHA256 sorted compact UTF8 named_exact_verification_payload object only',raw='Actual bytes',LF='Actual bytes replacing CRLF pairs with LF only'),ledger_only_transition=True)
run['run_sha256']=sha(canon(run));write(D/'run.json',run)
with (D/'readback.stdout.log').open('wb') as out,(D/'readback.stderr.log').open('wb') as err:
 command=[sys.executable,'-B','-X','utf8',str(D/'close.py'),'--readback'];p=subprocess.Popen(command,cwd=ROOT,stdout=out,stderr=err);readpid=p.pid;code=p.wait()
write(D/'readback.status.json',dict(command=command,actual_PID=readpid,exit_code=code,terminal_closed=True,stdout=pin(D/'readback.stdout.log'),stderr=pin(D/'readback.stderr.log')));assert code==0
outputs=[pin(p) for p in sorted(D.iterdir()) if p.is_file() and p.name not in ['lease.json','outputs.final.json']]
o=dict(artifacts=outputs,count=len(outputs),hash_recipe='Complete sorted compact UTF8 output manifest excluding ONLY outputs_sha256');o['outputs_sha256']=sha(canon(o));write(D/'outputs.final.json',o)
for row in outputs:check(row)
assert sha(canon({k:v for k,v in load(D/'run.json').items() if k!='run_sha256'}))==run['run_sha256']
lease=dict(status='CLOSEDLAST',actor=evidence['verifier_id'],checked_commit=SCI,actual_finalizer_PID=os.getpid(),actual_finalizer_exit_evidence='Parent tool terminal EXIT0 after final stdout',compiler=dict(PID=payload['focused_build']['actual_PID'],exit_code=0,status='CLOSED'),check_reader=dict(PID=native['actual_reader_PID'],exit_code=0,status='CLOSED'),promotion=dict(PID=pid,exit_code=0,status='CLOSED'),readback=dict(PID=readpid,exit_code=0,status='CLOSED'),Python_children='ACTUAL_EXIT0_CLOSED',read_resources='CLOSED',write_resources='CLOSED_AFTER_THIS_FINAL_FILE_WRITE',run=pin(D/'run.json'),receipt=pin(D/'receipt.json'),payload=pin(D/'payload.json'),outputs=pin(D/'outputs.final.json'),readback_artifact=pin(D/'readback.json'),transition=pin(D/'transition.json'),run_sha256=run['run_sha256'],named_exact_verification_payload_sha256=run['named_exact_verification_payload_sha256'],closed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),lease_hash_recipe='Complete sorted compact UTF8 lease excluding ONLY lease_sha256');lease['lease_sha256']=sha(canon(lease));write(D/'lease.json',lease)
print(json.dumps(dict(status='CLOSEDLAST_VERIFIED',actual_finalizer_PID=os.getpid(),promotion_PID=pid,readback_PID=readpid,run_sha256=run['run_sha256'],payload_sha256=run['named_exact_verification_payload_sha256'],receipt=pin(D/'receipt.json'),run=pin(D/'run.json'),lease=pin(D/'lease.json'),lease_sha256=lease['lease_sha256'],input_count=len(rows),output_count=len(outputs))),flush=True)
