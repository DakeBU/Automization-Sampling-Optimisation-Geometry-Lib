from pathlib import Path
import copy,datetime,hashlib,json,os,subprocess,sys
R=Path('E:/Samplinglib');os.chdir(R);sys.path[:0]=[str(R),str(R/'tools')]
from tools.astis_advance import transition_advance,_replay_advances
B=R/'runs/20261007-companion-priority/pbps-actual-physical-time-measurability80';O=B/'exact-commit-verification80'
C='ac7cabf30e17a322ec187b7eb13e1a9d4a57695d';ID='ASTIS-SA-20261010-PBPSActualPhysicalTimeMeasurability'
D='AutoSamplingTheory.ExampleCases.ProximalBPS.ActualPhysicalTimeMeasurability.actual_physical_time_measurable_phase'
CELL=R/'research-wiki/frontier-cells/ASTIS-SW-PBPS-actual-physical-time-measurability.json'
M=R/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualPhysicalTimeMeasurability.lean'
A=R/'research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261010-PBPSActualPhysicalTimeMeasurability.json'
def load(p):return json.loads(Path(p).read_text(encoding='utf-8'))
def info(p):
 p=Path(p);p=p if p.is_absolute() else R/p;b=p.read_bytes();return dict(path=p.relative_to(R).as_posix(),RAW_bytes=len(b),RAW_sha256=hashlib.sha256(b).hexdigest())
def save(n,d):
 with (O/n).open('x',encoding='utf-8',newline='\n') as f:json.dump(d,f,ensure_ascii=False,indent=2);f.write('\n')
def git(*args):return subprocess.check_output(['git',*args],cwd=R)
def states():return _replay_advances([json.loads(v) for v in (R/'runs/substantive_advances.jsonl').read_text(encoding='utf-8').splitlines() if v.strip()])
assert git('rev-parse','HEAD').decode().strip()==C
assert load(O/'checks-complete80.json')['status']=='PASS'
assert M.read_bytes()==git('show',C+':'+M.relative_to(R).as_posix())
assert info(M)['RAW_sha256']=='bf8f66a8484fa82c46b26ac6b66a6c8484e6dd6465ac8587d7e27b2489e73a5c'
freeze=load(O/'input-freeze80.json')
for e in freeze['exact_commit_matches']+freeze['nested_pinned_mathlib_matches']:assert info(e['path'])['RAW_sha256']==e['RAW_sha256']
tools=[]
for rel in ['tools/astis.py','tools/astis_advance.py','tools/astis_publication.py','tools/astis_contributor_contract.py','tools/astis_semantic_roundtrip.py','tools/astis_frontier_cells.py']:
 raw=(R/rel).read_bytes();blob=git('show',C+':'+rel)
 assert raw.replace(b'\r\n',b'\n')==blob.replace(b'\r\n',b'\n')
 tools.append(dict(**info(R/rel),git_blob_RAW_sha256=hashlib.sha256(blob).hexdigest(),exact_equal=raw==blob,newline_only_checkout_difference=raw!=blob))
save('gate-tool-commit-bindings80.json',dict(verified_commit=C,files=tools))
before=states();assert before[ID]['state']=='PROVED_LOCAL' and before[ID]['owner_id']=='companion_root_20261005'
lane={k:v for k,v in before.items() if v.get('state')=='STABILIZING'}
assert set(lane)=={'ASTIS-SA-20261005-SPHMCImplementedPhaseKernel'}
cell=load(CELL);assert cell['status']=='proved_locally';save('cell.before-independent-admission80.json',cell)
audit=load(A);assert audit['state']=='accepted' and '/root/fresh_source78' in audit['source_review']['reviewer']
assert audit['publication_binding_sha256']=='d85b866ee0c62651a1a4cecd2db69ae8cf62f244fe547f1baee4bf00eef90eaa'
receipts=[]
for n in ['packet','focused-module','contributor','publication','publication-reviewed','semantic','frontier']:
 p=O/(n+'.receipt.json');r=load(p);assert r['exit_code']==0 and r['terminal_closed'] and r['checked_commit']==C
 for e in [r['stdout'],r['stderr']]:assert info(e['path'])==e
 receipts.append(info(p))
assert not load(O/'fake-closure-scan80.json')['hits']
math=B/'independent-math80';mr=load(math/'fresh-whole-module.receipt.json')
assert mr['exit_code']==0 and mr['terminal_closed']
for e in [mr['source'],mr['probe'],mr['stdout'],mr['stderr']]:assert info(e['path'])==e
summary=load(math/'kernel-dependency-summary80.json')
verdict=dict(status='PASS_INDEPENDENT_EXACT_COMMIT_VERIFICATION',verifier_id='/root/exact_verify77',verified_commit=C,
 created_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),actual_admission_helper_PID=os.getpid(),lean_module=info(M),
 gate=receipts,gate_tool_bindings=info(O/'gate-tool-commit-bindings80.json'),publication_declarations=[D],
 publication_binding_sha256=audit['publication_binding_sha256'],semantic_roundtrip_audit='ASTIS-RT-20261010-PBPSActualPhysicalTimeMeasurability',
 source_audit=dict(state='accepted',reviewer=audit['source_review']['reviewer'],
  review_result=info(B/'fresh-source80/source-review.result80.json'),review_run=info(B/'fresh-source80/source-review.run-evidence80.json'),
  native_manifest=info(B/'fresh-source80/source-review.run-manifest80.json'),reviewer_packet_sha256=audit['source_review']['reviewer_packet_sha256'],
  immutable_source_first_chronology_verified=True,review_scope='Bounded independent source-implicit measurable realization/init, with all41inventory/12nodes/33edges and9regions; source process/law/cost exclusions remain explicit.'),
 blind_decoder=dict(identity='/root/blind_decoder80',manifest=info(B/'anonymous-decoder80/run-manifest.json'),source_text_visible=False,source_identity_visible=False,proof_BODY_visible=False,
  metadata_overlay='Preserved v1 plus exact alias-only v2 to satisfy seven-field adoption interface; mathematical reconstruction unchanged.'),
 fake_closure_scan=info(O/'fake-closure-scan80.json'),axioms=summary['axioms'],
 fresh_full_source_elaboration=info(math/'fresh-whole-module.receipt.json'),kernel_generated_local_proof_closure=info(math/'kernel-dependency-summary80.json'),
 evidence_reuse_reason='Own unchanged accepted full exact source elaboration and kernel closure through generated match proof constant; original complete source/probe/parents/toolchain/manifest/terminal logs checked by RAW hash and named commit (lossless log archives when needed). Current focused build rerun at exact science commit; no proof redone or native trajectory fabricated.',
 external_ASTIS_dependencies=summary['external_ASTIS_dependencies'],independent_mathematics=info(math/'decision80.json'),whole_proof=info(math/'whole-proof-mathematics80.json'),statement_definition_audit=info(math/'statement-definition-audit80.json'),
 exact_science_and_nine_step_freeze=info(O/'input-freeze80.json'),
 mathematical_cases=['Sealed complete private Prop, six original analytic binders and eleven actual lets preserved; no public provider premise',
  'Correct right-associated joint parameter/time/sample pullback of measurable actual records/clocks',
  'All-input measurable half-open intervals; monotone disjointness remains valid for zero waits',
  'Stopped record clock top cannot be <=finite t, so dummy Sum projection never supplies a source phase on a covered interval',
  'Option none exactly uncovered complement and value z0; countable compatible gluing is total and jointly measurable',
  'Every covered actual live arc agrees deterministically for all samples, including last live infinite-next-wait arc',
  'Per-fixed-parameter one AE event contains all finite-time actual arc/elapsed conclusions and initialization',
  'Actual epsilon0 positivity from77 plus initialized76 strict live first increment or stopped top and73Phi0 prove AE origin; rank0/zero-hazard infinite wait included'],
 lesson_review='Nine formula/prose steps bind exact contiguous full public theorem/BODY lines93-249 with no omitted region.',
 truth_boundary=load(B/'claim.json')['truth_boundary'],
 open_source_routes=['Original direct Exp first moment/mean1 SLLN remains OPEN alternative to the proved sufficient indicator route',
  'Per-parameter AE result does not establish one event uniform over parameters or arbitrary correlated random-parameter substitution',
  'Uncovered z0 is an explicit ASTIS total representative convention; full source unique-process/Markov/law clauses remain OPEN'],
 remaining_acceptance=['canonical shared imports/Registry/root Tests/full astis.py check','graph/site/visual-reader acceptance','sole-lane serialized stabilization',
  'remote CI/main merge','Exposition Seal/postmerge purification/live validation','full paper/process/error/cost/composition and existing whole Goal'],
 production_edits=False,stabilization=False,Goal_complete=False,
 provenance='Exact named science inputs, native independent math/decoder/source manifests and real foreground terminal receipts; no fabricated native reasoning trajectory.')
save('verified.json',verdict)
e={k:verdict[k] for k in ['verifier_id','verified_commit','source_audit','fake_closure_scan','publication_declarations','semantic_roundtrip_audit']};e['gate']=info(O/'verified.json')
transition_advance(ID,'VERIFIED',worker_id='/root/exact_verify77',evidence=e)
new=copy.deepcopy(cell);new['status']='independently_verified';new['evidence']['independent_verification']=(O/'verified.json').relative_to(R).as_posix()
CELL.write_text(json.dumps(new,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
after=states();assert after[ID]['state']=='VERIFIED'
assert {k:v for k,v in after.items() if k!=ID}=={k:v for k,v in before.items() if k!=ID}
rest=copy.deepcopy(load(CELL));rest['status']=cell['status']
if 'independent_verification' in cell.get('evidence',{}):rest['evidence']['independent_verification']=cell['evidence']['independent_verification']
else:rest['evidence'].pop('independent_verification')
assert rest==cell
save('admission80.json',dict(state='VERIFIED',cell_state='independently_verified',verified_commit=C,verifier_id='/root/exact_verify77',verified=info(O/'verified.json'),cell=info(CELL),all_other_cell_metadata_semantically_preserved=True,all_other_advances_unchanged=True,existing_stabilizing_lane_unchanged=list(lane),stabilization=False,Goal_complete=False))
print('VERIFIED',C,info(O/'verified.json')['RAW_sha256'],flush=True)
