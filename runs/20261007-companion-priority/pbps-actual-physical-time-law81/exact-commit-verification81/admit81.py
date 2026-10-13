from pathlib import Path
import copy,datetime,hashlib,json,os,subprocess,sys
R=Path('E:/Samplinglib');os.chdir(R);sys.path[:0]=[str(R),str(R/'tools')]
from tools.astis_advance import transition_advance,_replay_advances
B=R/'runs/20261007-companion-priority/pbps-actual-physical-time-law81';O=B/'exact-commit-verification81'
C='7f815975f0ac55a211af4a4ba8c446b0d7f69a9f';ID='ASTIS-SA-20261010-PBPSIdealHalfTurnKernel'
D='AutoSamplingTheory.ExampleCases.ProximalBPS.IdealHalfTurnKernel.ideal_half_turn_returned_position_kernel'
CELL=R/'research-wiki/frontier-cells/ASTIS-SW-PBPS-ideal-half-turn-kernel.json'
M=R/'AutoSamplingTheory/ExampleCases/ProximalBPS/IdealHalfTurnKernel.lean'
A=R/'research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261010-PBPSIdealHalfTurnKernel.json'
def load(p):return json.loads(Path(p).read_text(encoding='utf-8'))
def info(p):
 p=Path(p);p=p if p.is_absolute() else R/p;b=p.read_bytes();return dict(path=p.relative_to(R).as_posix(),RAW_bytes=len(b),RAW_sha256=hashlib.sha256(b).hexdigest())
def save(n,d):
 with (O/n).open('x',encoding='utf-8',newline='\n') as f:json.dump(d,f,ensure_ascii=False,indent=2);f.write('\n')
def git(*args):return subprocess.check_output(['git',*args],cwd=R)
def states():return _replay_advances([json.loads(v) for v in (R/'runs/substantive_advances.jsonl').read_text(encoding='utf-8').splitlines() if v.strip()])
assert git('rev-parse','HEAD').decode().strip()==C
assert load(O/'checks-complete81.json')['status']=='PASS'
assert M.read_bytes()==git('show',C+':'+M.relative_to(R).as_posix())
assert info(M)['RAW_sha256']=='5b3d639fbc49e06715ae8f768d5a5c714b7844dc20c5e5a8a16cb564e823df2f'
freeze=load(O/'input-freeze81.json')
for e in freeze['exact_commit_matches']+freeze['nested_pinned_mathlib_matches']:assert info(e['path'])['RAW_sha256']==e['RAW_sha256']
toolpins=[]
for rel in ['tools/astis.py','tools/astis_advance.py','tools/astis_publication.py','tools/astis_contributor_contract.py','tools/astis_semantic_roundtrip.py','tools/astis_frontier_cells.py']:
 raw=(R/rel).read_bytes();blob=git('show',C+':'+rel);assert raw.replace(b'\r\n',b'\n')==blob.replace(b'\r\n',b'\n')
 toolpins.append(dict(**info(R/rel),git_blob_RAW_sha256=hashlib.sha256(blob).hexdigest(),exact_equal=raw==blob,newline_only_checkout_difference=raw!=blob))
save('gate-tool-commit-bindings81.json',dict(verified_commit=C,files=toolpins))
before=states();assert before[ID]['state']=='PROVED_LOCAL' and before[ID]['owner_id']=='companion_root_20261005'
lane={k:v for k,v in before.items() if v.get('state')=='STABILIZING'};assert set(lane)=={'ASTIS-SA-20261005-SPHMCImplementedPhaseKernel'}
cell=load(CELL);assert cell['status']=='proved_locally';save('cell.before-independent-admission81.json',cell)
audit=load(A);assert audit['state']=='accepted' and audit['source_review']['reviewer']=='/root/fresh_source78'
assert audit['publication_binding_sha256']=='7f5a864122254a7e0a425edf37e8d68597b161492edb419507199bb24baf29d8'
receipts=[]
for n in ['packet','focused-module','contributor','publication','publication-reviewed','semantic','frontier']:
 p=O/(n+'.receipt.json');r=load(p);assert r['exit_code']==0 and r['terminal_closed'] and r['checked_commit']==C
 for e in [r['stdout'],r['stderr']]:assert info(e['path'])==e
 receipts.append(info(p))
assert not load(O/'fake-closure-scan81.json')['hits']
math=B/'independent-math81';mr=load(math/'fresh-whole-module.receipt.json');assert mr['exit_code']==0 and mr['terminal_closed']
for e in [mr['source'],mr['probe'],mr['stdout'],mr['stderr']]:assert info(e['path'])==e
summary=load(math/'kernel-dependency-summary81.json')
v=dict(status='PASS_INDEPENDENT_EXACT_COMMIT_VERIFICATION',verifier_id='/root/exact_verify77',verified_commit=C,created_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),actual_admission_helper_PID=os.getpid(),lean_module=info(M),gate=receipts,gate_tool_bindings=info(O/'gate-tool-commit-bindings81.json'),publication_declarations=[D],publication_binding_sha256=audit['publication_binding_sha256'],semantic_roundtrip_audit='ASTIS-RT-20261010-PBPSIdealHalfTurnKernel',
 source_audit=dict(state='accepted',reviewer=audit['source_review']['reviewer'],review_result=info(B/'fresh-source81/source-review.result81.json'),review_run=info(B/'fresh-source81/source-review.run-evidence81.json'),native_manifest=info(B/'fresh-source81/source-review.run-manifest81.json'),reviewer_packet_sha256=audit['source_review']['reviewer_packet_sha256'],immutable_source_first_chronology_verified=True,coverage='65 frozen inventory items,15nodes,29edges; no unmapped items/nodes/edges; ten authored formula/BODY regions. Explicit excluded global obligations remain OPEN.',schema_adapter_acknowledgment=info(B/'fresh-source81/schema-adapter-acknowledgment81.json'),schema_adapter='All native slot source/lean/blind/assessment/relation fields preserved; original=source,reconstructed=blind,evidence preserves native assessment/provenance. Independently acknowledged additive aliases, no mathematical repair.'),
 blind_decoder=dict(identity='/root/blind_decoder81',manifest=info(B/'anonymous-decoder81/run-manifest.json'),native_decoded=info(B/'anonymous-decoder81/decoded.json'),parent_packet=info(B/'anonymous-decoder81/parent-packet.json'),source_text_visible=False,input_artifacts=['lean-statement','approved-definition-context'],native_hash_recipe_checked=True),fake_closure_scan=info(O/'fake-closure-scan81.json'),axioms=summary['axioms'],fresh_full_source_elaboration=info(math/'fresh-whole-module.receipt.json'),kernel_generated_local_proof_closure=info(math/'kernel-dependency-summary81.json'),
 evidence_reuse_reason='Own unchanged accepted complete-source elaboration plus actual theorem/_proof_1_1 kernel closure, seven real ASTIS parents and standard3axioms. Exact source/probe/inputs/toolchain/manifest/terminal logs checked by RAW and named science commit (lossless gzip archives where needed). Focused Lean rerun at this science commit. No reproof or fabricated native trajectory.',external_ASTIS_dependencies=summary['external_ASTIS_dependencies'],independent_mathematics=info(math/'decision81.json'),whole_proof=info(math/'whole-proof-mathematics81.json'),statement_definition_audit=info(math/'statement-definition-audit81.json'),exact_science_and_ten_step_freeze=info(O/'input-freeze81.json'),
 mathematical_cases=['Exact sealed full private Prop and original six assumptions;15literal definitions;11actual definitions equal80/79 and nine common equal76; zero extra public provider premises','Genuine positive Gibbs normalizer/integrability derived internally, exact normalized everywhere q_y and standardGaussian, rank0 included','Correct independently generated ((reference,momentum),Exp sample) product law and joint measurable returned-position probability kernel','Complete live-record countable good event Borel before Fubini; dummy branch excluded by explicit record=inl(L)','Actual last live infinite-wait interval, half-open endpoints, NNReal elapsed and exceptional fallback retained','Product-AE actual initialization+terminalπ arc from per-fixed-parameter commonAE80; no uniformparameterAE or correlated substitution','Derived origin pushforward dirac x product standardGaussian from actual initialization equality and genuine probability marginals'],
 lesson_review='Ten contiguous formula/prose exact BODY regions110–310. Public signature100–109 separately checked against frozen literal. No omitted BODY region.',truth_boundary=load(B/'claim.json')['truth_boundary'],open_source_routes=['Source direct Exp mean-one SLLN remains OPEN alternative to the proved sufficient indicator-SLLN parent route','Full random all-time process law and separately quantified version uniqueness are OPEN; only fixed-parameter all-time and product-input origin/π agreement are admitted','No implemented reference sampler, reference approximation, phase Markov/restart/semigroup/invariance/reversibility/hypocoercivity/main/error/cost/composition implication'],
 remaining_acceptance=['Serialized canonical shared imports/Registry/rootTests/full astis.py check','graph/site/actual visual-reader validation','Remote Lean acceptance: root reports GitHub job38057308993 failed before compilation on fixed4.33.0 Linux download SSL/TLS error35; infrastructure blocked, no compiler result','Existing sole-lane stabilization/main merge','Exposition Seal/postmerge purification/live deployment','Full paper and actual-input composition/four-paper Goal'],
 retained_verifier_diagnostics=[info(O/'preflight-range-diagnosis81.json'),info(O/'preflight-range-index-diagnosis81.json')],production_edits=False,stabilization=False,Goal_complete=False,provenance='Named commit native evidence and actual foreground terminal receipts; independent admission, no proving-worker selfverification.')
save('verified.json',v)
e={k:v[k] for k in ['verifier_id','verified_commit','source_audit','fake_closure_scan','publication_declarations','semantic_roundtrip_audit']};e['gate']=info(O/'verified.json')
transition_advance(ID,'VERIFIED',worker_id='/root/exact_verify77',evidence=e)
new=copy.deepcopy(cell);new['status']='independently_verified';new['evidence']['independent_verification']=(O/'verified.json').relative_to(R).as_posix()
CELL.write_text(json.dumps(new,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
after=states();assert after[ID]['state']=='VERIFIED'
assert {k:v for k,v in after.items() if k!=ID}=={k:v for k,v in before.items() if k!=ID}
rest=copy.deepcopy(load(CELL));rest['status']=cell['status']
if 'independent_verification' in cell.get('evidence',{}):rest['evidence']['independent_verification']=cell['evidence']['independent_verification']
else:rest['evidence'].pop('independent_verification')
assert rest==cell
save('admission81.json',dict(state='VERIFIED',cell_state='independently_verified',verified_commit=C,verifier_id='/root/exact_verify77',verified=info(O/'verified.json'),cell=info(CELL),all_other_cell_metadata_semantically_preserved=True,all_other_advances_unchanged=True,existing_stabilizing_lane_unchanged=list(lane),stabilization=False,Goal_complete=False))
print('VERIFIED',C,info(O/'verified.json')['RAW_sha256'],flush=True)
