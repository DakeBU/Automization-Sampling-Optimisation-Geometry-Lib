import pathlib,json,hashlib,subprocess,os,sys,datetime
ROOT=pathlib.Path('E:/Samplinglib');os.chdir(ROOT);sys.path.insert(0,str(ROOT))
R=ROOT/'runs/20261007-companion-priority/pbps-centered-defect59';D=R/'exact-science-verification'
COMMIT='2d6cd0167adc4fae1d8d166068a2eda51cd3c3ad';SAU='ASTIS-SA-20261008-PBPSCenteredDefectOperator';ACTOR='/root/whole_math52/exact-science59'
def sha(b):return hashlib.sha256(b).hexdigest()
def canon(q):return json.dumps(q,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def load(p):return json.loads(pathlib.Path(p).read_bytes())
def write(p,q):pathlib.Path(p).write_bytes((json.dumps(q,ensure_ascii=False,indent=2,allow_nan=False)+'\n').encode())
def pin(p):
 p=pathlib.Path(p);b=p.read_bytes();l=b.replace(b'\r\n',b'\n');return dict(path=p.as_posix(),bytes=len(b),lf_bytes=len(l),raw_sha256=sha(b),lf_sha256=sha(l))
def check(row):assert pin(row['path'])==row,row['path']
git=load(D/'git-science-inputs.json'); native=load(D/'native-checks.json'); math=load(D/'math-inputs.json');gates=load(D/'gates.json');freeze=load(R/'math-freeze.json')
assert subprocess.check_output(['git','rev-parse','HEAD']).decode().strip()==COMMIT
for row in git['entries']:check(row['working'])
for row in math['inputs']:check(row)
for row in native['native_object_inputs']:check(row)
for row in native['pin_checks']:check(row['resolved'])
for row in gates['actual_foreground_gates']:
 assert row['actual_exit_code']==0 and row['closed'];check(row['stdout']);check(row['stderr'])
ledger=ROOT/'runs/substantive_advances.jsonl';before=(D/'ledger.before.exactraw.snapshot').read_bytes();assert ledger.read_bytes()==before
from tools import astis_advance as advance, astis_publication as pub
states=advance.current_advances();state=states[SAU];assert state['state']=='PROVED_LOCAL' and state['owner_id']!=ACTOR
stab=[k for k,v in states.items() if v.get('state')=='STABILIZING'];assert stab==['ASTIS-SA-20261005-SPHMCImplementedPhaseKernel']
pub.check_advance(freeze['mathematical_declarations'],reviewed=True)
auditnames=['ASTIS-RT-20261008-PBPSCenteredSelfadjointDefect','ASTIS-RT-20261008-PBPSCenteredDefectInverse']
slugs=['pbps-centered-selfadjoint-defect','pbps-centered-defect-inverse'];auditrows=[];adminmaps=[]
for i,(auditid,slug,decl) in enumerate(zip(auditnames,slugs,freeze['mathematical_declarations'])):
 p=ROOT/f'research-wiki/semantic-roundtrip/audits/{auditid}.json';q=load(p);nativeq=load(R/f'source-review59/source.{i}.review.json')
 item=next(x for x in pub.load() if any(b['declaration']==decl for b in x['bindings']))
 b=next(x for x in item['bindings'] if x['declaration']==decl)
 binding=pub.binding_digest(item,b)
 assert q['publication_binding_sha256']==nativeq['publication_binding_sha256']==binding
 assert q['source_review']['state']=='accepted' and q['source_review']['review_run_sha256']==nativeq['review_run_sha256']
 assert q['source_review']['reviewer']==nativeq['reviewer'] and q['source_review']['run_artifact']==f'runs/20261007-companion-priority/pbps-centered-defect59/source-review59/source.{i}.review.json'
 auditrows.append(dict(current_audit=pin(p),native_source_review=pin(R/f'source-review59/source.{i}.review.json'),actual_publication_binding_sha256=binding,slots=7,blocking_deltas=0,repairs=0))
 cell=ROOT/f'research-wiki/frontier-cells/ASTIS-SW-PBPS-centered-{["selfadjoint-defect","defect-inverse"][i]}.json'
 for j,t in enumerate([p,cell]):
  snap=D/f'admin-before.{i}.{j}.{sha(t.as_posix().encode())[:16]}.exactraw.snapshot';snap.write_bytes(t.read_bytes())
  adminmaps.append(dict(original=pin(t),exact_snapshot=pin(snap),reason='Read-only exact current science snapshot; any later serialized administrative update must match this precise row'))
helperpaths=['tools/astis_advance.py','tools/astis_publication.py','tools/astis_semantic_roundtrip.py','tools/astis_semantic_roundtrip_core.py','tools/astis_frontier_cells.py','tools/astis_contributor_contract.py']
write(D/'current-audit-and-admin-bindings.json',dict(source_audits=auditrows,before_admin_mappings=adminmaps,ledger_before=dict(original=pin(ledger),exact_snapshot=pin(D/'ledger.before.exactraw.snapshot')),helper_inputs=[pin(ROOT/x) for x in helperpaths],sole_STABILIZING=stab))
payload=dict(actor=ACTOR,result_kind='integration-node',checked_commit=COMMIT,scope='Independent exact-science verification of actual_centered_selfadjoint_defect and actual_centered_defect_coercive_and_unit',declarations=freeze['mathematical_declarations'],science_entries=git['entry_count'],strict_frozen_math_inputs=27,native_qualified_unique_identities=native['qualified_unique_pin_count'],native_whole_self_checks=4,native_distinct_payload_checks=2,anonymous_packet_self_checks=2,historical_audit_mapping_count=2,current_admin_snapshot_count=4,actual_gates=gates['actual_foreground_gates'],source_audits=auditrows,fake_closure_scan=pin(D/'headers-and-fake-scan.json'),axiom_closures=load(D/'axiom-closures.json')['closures'],reused_complete_mathematics=dict(run_sha256=native['math_run_sha256'],payload_sha256=native['math_payload_sha256'],current_entire_body_same_frozen_bytes=True),mathematical_reasons=[
 'Actual55 probability, stationary reflected disintegration, U and snd isometry M produce SAME T internally. Selfadjointness follows true inner transport and conditional projection, not an added operator certificate.',
 'Probability L2 implies L1; actual S disintegration and both nu marginals prove mean preservation. Canonical q is the AE-one L2Expectation class. Selfadjointness plus mean pairing fixes q, and H0 is the entire complete closed kernel of inner(q), not a selected core.',
 'T0 is the actual restriction to that invariant kernel. I-T squared and I-T0 squared have their true actions and exact quadratic norm defects; contraction proves positivity. Full-space defect kills q and is not claimed invertible.',
 'The real Test identifies SAME U through AE action, transports mean through actual M and nu=J.snd, and applies actual58 contraction to PM=M. Norm isometry gives exact rho for T0; delta=1-rho squared is positive under original cap and includes alpha eta=1.',
 'CompleteSpace of the continuous functional kernel and fixed Mathlib coercivity prove IsUnit of the centered squared defect on the same entire domain. No finite-dimensional L2, Nontrivial, caller PI, domain, centering, probability or inverse premise. Rank0 remains valid.'
 ],decoder_disclosure=dict(source_text_visible=False,source_identity_visible=False,native_decoder_run_has_whole_self_field=False,actual_raw_bound=True),preserved_negative_boundary='All536 committed entries, including failed syntax/type/body diagnostics and source/topology overlays, are raw/LF bound. Failed-only elaboration sorryAx is not admitted proof credit; early diagnostic-input controls do not prove the two final targets.',unrun_integration_controls=gates['deferred'],remaining=['Gamma positive root/Loewner inverse/polar construction','Full weakH1 and hypocoercivity','Dynamics/main/errors/cost/composition','Full paper/reader purification/live/Goal'],blockers=[])
payloadhash=sha(canon(payload));write(D/'exact-verification.payload.json',payload)
write(D/'before-transition.json',dict(status='ALL_EXACT_SCIENCE_GATES_PASS',checked_commit=COMMIT,actual_author_pid=os.getpid(),named_exact_verification_payload_sha256=payloadhash,payload=pin(D/'exact-verification.payload.json'),ledger_before=pin(D/'ledger.before.exactraw.snapshot'),source_audits=auditrows))
evidence=dict(verifier_id=ACTOR,verified_commit=COMMIT,checked_commit=COMMIT,gate=dict(focused=pin(D/'focused.status.json'),reviewed_publication=pin(D/'publication.reviewed.status.json'),changed_module_inventory=pin(D/'publication.changed-module.status.json'),semantic=pin(D/'semantic.status.json'),frontier=pin(D/'frontier.status.json'),contributor=pin(D/'contributor.status.json'),full_aggregate='DEFERRED_TO_SERIALIZED_ROOT_INTEGRATION'),source_audit=auditrows,fake_closure_scan=pin(D/'headers-and-fake-scan.json'),publication_declarations=freeze['mathematical_declarations'],exact_scope=payload['scope'],remaining_truth_boundary=payload['remaining'],native_verifier_payload=pin(D/'exact-verification.payload.json'),named_exact_verification_payload_sha256=payloadhash,receipt_path=(D/'receipt.json').as_posix(),root_not_verifier=True,cells_mutated_by_verifier=False)
advance.transition_advance(SAU,'VERIFIED',worker_id=ACTOR,modes=['independent-exact-science-verification'],evidence=evidence)
after=ledger.read_bytes();assert after.startswith(before)
delta=after[len(before):];rows=[json.loads(x) for x in delta.splitlines() if x.strip()];assert len(rows)==1
assert rows[0]['event']=='transition' and rows[0]['worker_id']==ACTOR and rows[0]['to_state']=='VERIFIED'
(D/'ledger.after.exactraw.snapshot').write_bytes(after)
write(D/'transition.json',dict(actual_author_pid=os.getpid(),actual_transition=rows[0],append_only=True,appended_records=1,before=pin(D/'ledger.before.exactraw.snapshot'),after=pin(D/'ledger.after.exactraw.snapshot'),current_ledger=pin(ledger),before_original_to_exact_snapshot_mapping=dict(original=git['ledger_before'],exact_snapshot=pin(D/'ledger.before.exactraw.snapshot'))))
post=advance.current_advances();assert post[SAU]['state']=='VERIFIED'
assert [k for k,v in post.items() if v.get('state')=='STABILIZING']==stab
for x in adminmaps:check(x['original'])
write(D/'promotion.author.status.json',dict(status='INDEPENDENT_VERIFIED_LEDGER_APPEND_COMPLETE',actual_Python_pid=os.getpid(),checked_commit=COMMIT,transition=pin(D/'transition.json'),cells_and_audits_unchanged=True))
print(json.dumps(dict(status='INDEPENDENT_VERIFIED_LEDGER_APPEND_COMPLETE',actual_Python_pid=os.getpid(),checked_commit=COMMIT,payload_sha256=payloadhash,append_records=1)),flush=True)
