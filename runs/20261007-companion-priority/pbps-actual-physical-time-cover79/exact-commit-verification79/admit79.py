"""Independent child admission only; preserve sole existing stabilization lane."""
from pathlib import Path
import copy,datetime,hashlib,json,os,subprocess,sys
R=Path('E:/Samplinglib');os.chdir(R);sys.path[:0]=[str(R),str(R/'tools')]
from tools.astis_advance import transition_advance,_replay_advances
B=R/'runs/20261007-companion-priority/pbps-actual-physical-time-cover79';O=B/'exact-commit-verification79'
C='56e4b7e101a1016e03df2971018b1f018f03e6c1';ID='ASTIS-SA-20261010-PBPSActualPhysicalTimeCover'
D='AutoSamplingTheory.ExampleCases.ProximalBPS.ActualPhysicalTimeCover.actual_fixed_reference_physical_time_cover'
CELL=R/'research-wiki/frontier-cells/ASTIS-SW-PBPS-actual-physical-time-cover.json'
M=R/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualPhysicalTimeCover.lean'
def load(p):return json.loads(Path(p).read_text(encoding='utf-8'))
def info(p):
 p=Path(p);b=p.read_bytes();return dict(path=str(p),RAW_bytes=len(b),RAW_sha256=hashlib.sha256(b).hexdigest())
def save(n,v):
 p=O/n;assert not p.exists();p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def states():return _replay_advances([json.loads(x) for x in (R/'runs/substantive_advances.jsonl').read_text(encoding='utf-8').splitlines() if x.strip()])
assert subprocess.check_output(['git','rev-parse','HEAD']).decode().strip()==C
assert load(O/'checks-complete79.json')['status']=='PASS'
assert M.read_bytes()==subprocess.check_output(['git','show',C+':'+M.relative_to(R).as_posix()])
assert info(M)['RAW_sha256']=='2f329dd32047f46adb81b65f51b9de56305021a944f7b8cdf62ae25665839c86'
tool_matches=[]
for rel in ['tools/astis.py','tools/astis_advance.py','tools/astis_publication.py','tools/astis_contributor_contract.py','tools/astis_semantic_roundtrip.py','tools/astis_frontier_cells.py']:
 raw=(R/rel).read_bytes();blob=subprocess.check_output(['git','show',C+':'+rel])
 assert raw.replace(b'\r\n',b'\n')==blob.replace(b'\r\n',b'\n')
 tool_matches.append(dict(**info(R/rel),git_blob_RAW_sha256=hashlib.sha256(blob).hexdigest(),exact_equal=raw==blob,newline_only_checkout_difference=raw!=blob))
save('gate-tool-commit-bindings79.json',dict(verified_commit=C,files=tool_matches))
before=states();assert before[ID]['state']=='PROVED_LOCAL' and before[ID]['owner_id']=='companion_root_20261005'
lane={k:v for k,v in before.items() if v.get('state')=='STABILIZING'};assert set(lane)=={'ASTIS-SA-20261005-SPHMCImplementedPhaseKernel'}
cell=load(CELL);assert cell['status']=='proved_locally';save('cell.before-independent-admission79.json',cell)
audit=load(R/'research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261010-PBPSActualPhysicalTimeCover.json')
assert audit['state']=='accepted' and audit['source_review']['reviewer']=='/root/fresh_source78'
assert audit['publication_binding_sha256']=='2d83e2bd8857f34d06176947dfbf85594073e988ca487c738714e5f7368ccb4c'
receipts=[]
for n in ['packet','focused-module','contributor','publication','semantic','frontier']:
 p=O/(n+'.receipt.json');r=load(p);assert r['exit_code']==0 and r['terminal_closed'] and r['checked_commit']==C
 for e in [r['stdout'],r['stderr']]:assert info(e['path'])['RAW_sha256']==e['RAW_sha256']
 receipts.append(info(p))
assert not load(O/'fake-closure-scan79.json')['hits']
for rpath in ['fresh-whole-module-attempt2.receipt.json','kernel-local-proof-closure-attempt2.receipt.json']:
 r=load(B/'independent-math79'/rpath);assert r['exit_code']==0 and r['terminal_closed']
 for e in r['inputs']+[r['stdout'],r['stderr']]:assert info(e['path'])['RAW_sha256']==e['RAW_sha256']
verdict=dict(status='PASS_INDEPENDENT_EXACT_COMMIT_VERIFICATION',verifier_id='/root/exact_verify77',verified_commit=C,
 created_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),actual_admission_helper_PID=os.getpid(),lean_module=info(M),gate=receipts,
 gate_tool_bindings=info(O/'gate-tool-commit-bindings79.json'),publication_declarations=[D],
 publication_binding_sha256=audit['publication_binding_sha256'],semantic_roundtrip_audit='ASTIS-RT-20261010-PBPSActualPhysicalTimeCover',
 source_audit=dict(state='accepted',reviewer='/root/fresh_source78',
  review_result=info(B/'fresh-source79/source-review.result79.json'),review_run=info(B/'fresh-source79/source-review.run-evidence79.json'),
  native_manifest=info(B/'fresh-source79/source-review.run-manifest79.json'),reviewer_packet_sha256='a04fb9a861cac2368722a69b9c899fd43f4884e1d075ffe5beae9c300fc10455',
  immutable_source_first_chronology_verified=True),
 blind_decoder=dict(identity='/root/blind_decoder79',manifest=info(B/'anonymous-decoder79/run-manifest.json'),source_seen=False,identity_seen=False,proof_BODY_seen=False),
 fake_closure_scan=info(O/'fake-closure-scan79.json'),axioms=['propext','Classical.choice','Quot.sound'],
 fresh_full_source_elaboration=info(B/'independent-math79/fresh-whole-module-attempt2.receipt.json'),
 kernel_generated_local_proof_closure=info(B/'independent-math79/kernel-local-proof-closure-attempt2.receipt.json'),
 evidence_reuse_reason='Own unchanged accepted complete-source elaboration/standard-three axioms and kernel closure through local generated omega/simp proofs; every frozen scientific input, probe and terminal log remains hash-exact and commit-bound. Focused module build rerun at current exact commit; no proof redone.',
 external_ASTIS_dependencies=load(B/'independent-math79/fresh-compiler-dependency-summary79.json')['direct_ASTIS_dependencies'],
 independent_mathematics=info(B/'independent-math79/decision79.json'),whole_proof=info(B/'independent-math79/whole-proof-mathematics79.json'),
 statement_definition_audit=info(B/'independent-math79/statement-definition-audit79.json'),
 exact_science_and_nine_step_freeze=info(O/'input-freeze79.json'),
 mathematical_cases=['all original six source binders, complete private Prop and eleven actual definitions preserved; no providers',
 'single AE actual78 event supports all finite horizons for each fixed deterministic parameter triple',
 'least crossing k>0 and predecessor k-1 yield actual half-open coverage',
 'monotonicity gives interval uniqueness even with zero waits/empty intervals',
 'finite covering time excludes stopped record and supplies unique actual live record',
 'next infinite wait leaves last live arc and every finite elapsed time admissible',
 'finite wait uses same actual tau and guarded next-record time, with a.time<=t validating NNReal subtraction',
 'rank0/cap0, endpoints and exceptional nonpositive samples preserved within AE bounded claim'],
 lesson_review='Nine source-ordered formulas/prose and exact contiguous full public BODY lines81-210 independently inspected. No omitted BODY region or global interpolation claim.',
 truth_boundary=load(B/'claim.json')['truth_boundary'],
 open_source_routes=['Explicit index0/initial-state identity requires support/positive-wait and Phi0 interpolation adapters beyond this interval theorem',
 'Selected measurable index, interpolated global phase path and path/process uniqueness/regularity remain OPEN',
 'Upstream original direct Exp first-moment/mean1 SLLN remains OPEN alternative to proved sufficient indicator route'],
 remaining_acceptance=['canonical shared imports/Registry/root Tests and full astis.py check','graph/site generation/check and visual reader admission','existing sole-lane serialized stabilization',
 'main merge and remote CI','live validation','Exposition Seal/postmerge purification','full PBPS/SPHMC main/process/cost/composition and existing four-paper Goal'],
 purification_notes=['Explicit UnitExponentialProduct import has no direct kernel BODY dependency; optional minimal-import cleanup remains'],
 production_edits=False,stabilization=False,Goal_complete=False,
 provenance='Exact named input hashes, real foreground terminal receipts and independent native math/decoder/source evidence; no fabricated native reasoning trajectory. Native Python bytecode output is explicitly local administrative data, not a Git mathematical certificate.')
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
save('admission79.json',dict(state='VERIFIED',cell_state='independently_verified',verified_commit=C,verifier_id='/root/exact_verify77',verified=info(O/'verified.json'),
 cell=info(CELL),all_other_cell_metadata_semantically_preserved=True,all_other_advance_records_unchanged=True,existing_stabilization_lane_unchanged=list(lane),stabilization=False,Goal_complete=False))
print('VERIFIED',C,info(O/'verified.json')['RAW_sha256'])
