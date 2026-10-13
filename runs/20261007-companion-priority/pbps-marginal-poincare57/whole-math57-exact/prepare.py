import pathlib,json,hashlib,os,datetime,subprocess
R=pathlib.Path('E:/Samplinglib');B=R/'runs/20261007-companion-priority/pbps-marginal-poincare57';O=B/'whole-math57-exact';M=B/'whole-math57'
def sha(b):return hashlib.sha256(b).hexdigest()
def logical(d):return sha(json.dumps(d,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode('utf-8'))
def load(p):return json.loads(p.read_text(encoding='utf-8'))
def pin(p):
 b=p.read_bytes();lf=b.replace(b'\r\n',b'\n');return dict(path=p.relative_to(R).as_posix(),bytes=len(b),lf_bytes=len(lf),raw_sha256=sha(b),lf_sha256=sha(lf))
def dump(n,d):(O/n).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def selfcheck(p,k):
 d=load(p);h=logical({a:v for a,v in d.items() if a!=k});assert d[k]==h;return dict(input=pin(p),self_field=k,logical_sha256=h)
def matches(e,p):
 a=pin(p);return all(a[k]==e[k] for k in ['bytes','raw_sha256','lf_sha256'])
for n in ['plan.json','preparation.readback.json','preparation.lease.json','protocol.api.snapshot.json']:
 assert not (O/n).exists(),n
heads=subprocess.check_output(['git','rev-parse','HEAD'],cwd=R,text=True,encoding='utf-8').strip()
checks=[selfcheck(M/'receipt.json','receipt_sha256'),selfcheck(M/'run.json','run_sha256'),selfcheck(M/'lease.json','lease_sha256')]
run=load(M/'run.json');receipt=load(M/'receipt.json');lease=load(M/'lease.json')
assert logical(run['review_binding_payload'])==run['review_binding_payload_sha256']==receipt['review_binding_payload_sha256']
assert lease['status']=='CLOSED' and all(lease[k]=='CLOSED' for k in ['read','write','Python','compiler'])
assert lease['actual_compiler_PID']==54196 and lease['actual_compiler_exit_code']==0
assert matches(lease['run'],M/'run.json') and matches(lease['receipt'],M/'receipt.json')
assert matches(lease['readback'],M/'readback.json')
assert load(M/'readback.json')['status']=='PASS'
assert len(receipt['fake_closure_scan'])==10 and all(not x['authored_fake_closure_hits'] for x in receipt['fake_closure_scan'])
for n,k in [('AutoSamplingTheory/TechnicalLemmas/FunctionalInequalities/GaussianMarginalPoincare.lean','production'),('Tests/GaussianMarginalPoincare.lean','Tests')]:
 assert matches(run['review_binding_payload'][k],R/n)
api=[]
for n,a,b in [('tools/astis_advance.py',441,452),('tools/astis_advance.py',523,605),('tools/astis_publication.py',387,399),('tools/astis_frontier_cells.py',83,84),('tools/astis_frontier_cells.py',373,378)]:
 p=R/n;lines=p.read_text(encoding='utf-8').splitlines();selected=('\n'.join(lines[a-1:b])+'\n').encode('utf-8')
 api.append(dict(whole=pin(p),first_line=a,last_line=b,selected_lf_bytes=len(selected),selected_lf_sha256=sha(selected),selected_utf8=selected.decode('utf-8')))
dump('protocol.api.snapshot.json',dict(status='READ_ONLY_API_INSPECTION',snapshots=api,commands_or_imported_gates_executed=False,source_review_verdict_read=False,lookup_observation='Guessed research-wiki/frontier-cells/schema.json path absent; actual tools/astis_frontier_cells.py _nonempty explicitly requires string. No schema inference used.'))
inputs=[pin(M/n) for n in ['receipt.json','run.json','lease.json','readback.json','outputs.final.json','mathematical-reasons.json','checks.json','input.manifest.json']]+[pin(R/'tools'/n) for n in ['astis_advance.py','astis_publication.py','astis_frontier_cells.py']]+[pin(O/'prepare.py')]
plan=dict(schema_version=1,artifact_kind='bounded-preparation-only-exact-science57-plan',actor='/root/whole_math52',future_independent_verifier_id='whole_math52_exact57',advance_id='ASTIS-SA-20261008-GaussianMarginalPoincare',frontier_cell='ASTIS-SHARED-gaussian-marginal-poincare',status='PREPARED_AWAIT_ROOT_CLOSED_SOURCE_ADMISSION_AND_EXACT_SCIENCE_COMMIT',scientific_commit=None,observed_head=heads,observed_head_is_not_science_verification=True,
 no_current_verdict=True,no_VERIFIED_transition=True,no_compiler_or_gate_started=True,source_or_decoder_final_verdict_read=False,
 immutable_complete_math57_reuse=dict(native_self_checks=checks,actual_CLOSED_compiler_PID=54196,actual_exit_code=0,raw_LF_originals=602,distinct_inputs=611,fake_scan_rows=10,complete_run_minus_run_sha256=run['run_sha256'],named_review_binding_payload_sha256=run['review_binding_payload_sha256'],payload_key='review_binding_payload',payload_digest_key='review_binding_payload_sha256',terminal_lease_self_key='lease_sha256',originals_unchanged=True),
 protocol=pin(O/'protocol.api.snapshot.json'),inputs=inputs,
 trigger='Root sends actual scientific commit after CLOSED independently accepted source review and adoption. Until then no source-verdict read, compiler, gate, admission or canonical mutation.',
 exact_stage_sequence=[
 'Bind actual HEAD/scientific commit, branch and actual explicit owned Git tree entries with raw/LF and byte counts; production/Test LF and exact1244 signature must agree with original sealed/current compiled bytes. Do not assume entry counts or source-native schemas from56.',
 'Reuse unchanged complete math57 reasons. Verify native complete-object receipt/run/lease self keys, separately named payload, CLOSED compiler/readback/output manifests and ten fake scan rows. Recheck602 originals plus611 prior distinct inputs exactly. Any lawful audit/cell administration changes require exact BEFORE raw/LF snapshot mappings at entire original row equality, never path-only fallback or silent skips.',
 'Only after trigger read actual CLOSED source57 review, decoder, separately reviewed overlays, source-adoption mapping and canonical accepted audit. Validate their actual native schemas, complete-object self recipes, named payloads, original raw/LF input/output pins, source chronology/body exposure and repaired/negative artifacts. Do not infer identity blindness or acceptance merely from root prose.',
 'Acquire exclusive exact-stage compiler lease. Remove inherited ELAN_TOOLCHAIN; confirm repo Lean4.33.0 and pinned Mathlibdb584. Set LEAN_NUM_THREADS=2 and PYTHONUTF8=1, use bundled Python -B, no forced rebuild. Invoke lake build Tests.GaussianMarginalPoincare exactly once, bind actual PID/log/status/source and distinguish replay from fresh elaboration. Require EXIT0, CLOSED compiler and actual main/Test standard3.',
 'Run actual reviewed publication check_advance([exact declaration], reviewed=True), appropriate pub--baseorigin/main, semantic/frontier/contributor focused gates and fake-closure scan. Bind every command/status/log. Full serialized shared/root/Registry/site gates belong to subsequent root integration; do not manufacture those now.',
 'Before transition bind all actual science entries and current allowed mutable cell/audit/ledger bytes with exact before snapshots. Require current57 PROVED_LOCAL, source accepted, proving owner distinct from verifier, and original PhaseKernel sole STABILIZING.',
 'If and only if all actual gates pass, call tools.astis_advance.transition_advance(advance_id, VERIFIED, worker_id=whole_math52_exact57, evidence=...) with verifier_id equal worker_id, verified_commit actual science SHA, gate/source_audit/fake_closure_scan and unchanged publication target set. Update only corresponding cell to independently_verified; evidence.independent_verification must be a STRING path, with structured details separately. Preserve all learning/publication/remaining-boundary contracts.',
 'Author exact native receipt/run/verified evidence with checked_commit, distinct named payload and complete-run self digest. Read back every original/Git/input/output/self/payload/transition binding before actual CLOSED-last compiler/Python/read/write lease and synchronous finalizer EXIT0. No commit/push/shared-import/Registry/site/stabilization/PURIFIED mutation.'
 ],
 future_native_output_schema=dict(receipt_self='receipt_sha256',run_self='run_sha256',named_component='verifier_binding_payload',named_component_digest='verifier_binding_payload_sha256',lease_self='lease_sha256',raw_and_LF='Actual raw bytes/length and CRLF-pairs-only LF bytes/length; complete self excludes ONLY exact named top-level self field; selected component digest never replaces whole-run digest'),
 residual_boundary='Genuine compact-gradient closure centered PI and SAME56 C3/C4 only. Separate weighted weakH1/fullB13, Gamma positive root/gap/inverse, macro-range, halfturn, dynamics/main/errors/cost/composition/full-reader/live/PURIFIED OPEN.',preparation_PID=os.getpid())
plan['plan_sha256']=logical(plan);dump('plan.json',plan);selfcheck(O/'plan.json','plan_sha256')
for e in inputs:assert matches(e,R/e['path'])
outputs=[pin(O/n) for n in ['prepare.py','protocol.api.snapshot.json','plan.json']]
dump('preparation.readback.json',dict(status='PASS_PREPARATION_ONLY',outputs=outputs,actual_native_math_self_checks=3,actual_component_payload_check=True,actual_terminal_CLOSED_math_lease=True,ten_fake_scan_rows_checked=True,scientific_commit_supplied=False,compiler='NOT_STARTED',source_verdict_read=False,actual_PID=os.getpid()))
for e in outputs:assert matches(e,R/e['path'])
lp=dict(schema_version=1,artifact_kind='preparation-only-resource-lease',status='CLOSED',read='CLOSED',write='CLOSED',Python='CLOSED',compiler='NOT_STARTED_CLOSED',actual_PID=os.getpid(),actual_foreground_exit_code=0,exit_evidence='Actual synchronous enclosing tools.exec_command EXIT0 follows last filesystem write; no compiler, imported gate or detached subprocess was started.',closed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),outputs=outputs+[pin(O/'preparation.readback.json')],plan=pin(O/'plan.json'),closure_order='LAST owned filesystem write; all readbacks beforehand. No acceptance or VERIFIED admission.')
lp['lease_sha256']=logical(lp);lb=(json.dumps(lp,ensure_ascii=False,indent=2)+'\n').encode('utf-8')
out=dict(status=plan['status'],observed_head=heads,plan=lp['plan'],plan_sha256=plan['plan_sha256'],preparation_lease_raw_sha256=sha(lb),preparation_lease_sha256=lp['lease_sha256'],compiler='NOT_STARTED_CLOSED',actual_PID=os.getpid())
(O/'preparation.lease.json').write_bytes(lb)
print(json.dumps(out,ensure_ascii=False))
