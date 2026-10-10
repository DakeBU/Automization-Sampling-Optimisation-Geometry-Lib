from pathlib import Path
import copy,datetime,hashlib,json,os,subprocess,sys
R=Path('E:/Samplinglib');os.chdir(R);sys.path[:0]=[str(R),str(R/'tools')]
from tools.astis_advance import transition_advance,_replay_advances
B=R/'runs/20261007-companion-priority/pbps-actual-small-time-continuity82';O=B/'exact-commit-verification82';G=O/'successor-8e182aeb'
C='8e182aeb384e5b9edb922c02fc14ceeca6f9b090';ID='ASTIS-SA-20261010-PBPSActualSmallTimeContinuity'
D='AutoSamplingTheory.ExampleCases.ProximalBPS.ActualSmallTimeContinuity.actual_small_time_stochastic_continuity'
CELL=R/'research-wiki/frontier-cells/ASTIS-SW-PBPS-actual-small-time-continuity.json'
M=R/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualSmallTimeContinuity.lean'
A=R/'research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261010-PBPSActualSmallTimeContinuity.json'
def load(p):return json.loads(Path(p).read_text(encoding='utf8'))
def info(p):
 p=Path(p);p=p if p.is_absolute() else R/p;b=p.read_bytes();return dict(path=p.relative_to(R).as_posix(),RAW_bytes=len(b),RAW_sha256=hashlib.sha256(b).hexdigest())
def save(n,d):
 with (O/n).open('x',encoding='utf8',newline='\n') as f:json.dump(d,f,ensure_ascii=False,indent=2);f.write('\n')
def git(*a):return subprocess.check_output(['git',*a],cwd=R)
def states():return _replay_advances([json.loads(v) for v in (R/'runs/substantive_advances.jsonl').read_text(encoding='utf8').splitlines() if v.strip()])
assert git('rev-parse','HEAD').decode().strip()==C
assert load(G/'checks-complete82.json')['status']=='PASS'
assert M.read_bytes()==git('show',C+':'+M.relative_to(R).as_posix())
assert info(M)['RAW_sha256']=='f2bbb2a495ff6af2f2d1d73f77c498ccf16406bb0b07d20b8437631afb1a7bde'
freeze=load(G/'input-freeze82.json')
for e in freeze['exact_commit_matches']+freeze['nested_pinned_mathlib_matches']+freeze['local_fixed_primary']:assert info(e['path'])['RAW_sha256']==e['RAW_sha256']
preserved=load(O/'collaborator-modified-RAW.before82.json')
for e in preserved:assert info(e['path'])==e
before=states();assert before[ID]['state']=='PROVED_LOCAL' and before[ID]['owner_id']=='companion_root_20261005'
lane={k:v for k,v in before.items() if v.get('state')=='STABILIZING'};assert set(lane)=={'ASTIS-SA-20261005-SPHMCImplementedPhaseKernel'}
cell=load(CELL);assert cell['status']=='proved_locally' and cell['graph_contribution']['lean_view']=='new-node';save('cell.before-independent-admission82.json',cell)
audit=load(A);assert audit['state']=='accepted' and audit['source_review']['reviewer']=='/root/fresh_source78'
assert audit['publication_binding_sha256']=='996913629e7bce2e7fb674454986bb49386ac51b3eb9a0f2856b265aa3bff8b7'
receipts=[]
for n in ['packet','focused-module','contributor','publication','publication-reviewed','semantic','frontier']:
 p=G/(n+'.receipt.json');r=load(p);assert r['exit_code']==0 and r['terminal_closed'] and r['checked_commit']==C
 for e in [r['stdout'],r['stderr']]:assert info(e['path'])==e
 receipts.append(info(p))
assert not load(G/'fake-closure-scan82.json')['hits']
math=B/'independent-math82';mr=load(math/'fresh-whole-module.receipt.json');assert mr['exit_code']==0 and mr['terminal_closed']
for e in [mr['source'],mr['probe'],mr['stdout'],mr['stderr']]:assert info(e['path'])==e
summary=load(math/'kernel-dependency-summary82.json')
v=dict(status='PASS_INDEPENDENT_EXACT_COMMIT_VERIFICATION',verifier_id='/root/exact_verify77',verified_commit=C,
 created_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),actual_admission_helper_PID=os.getpid(),
 lean_module=info(M),gate=receipts,publication_declarations=[D],publication_binding_sha256=audit['publication_binding_sha256'],
 semantic_roundtrip_audit='ASTIS-RT-20261010-PBPSActualSmallTimeContinuity',
 source_audit=dict(state='accepted',reviewer=audit['source_review']['reviewer'],review_result=info(B/'fresh-source82/source-review.result82.json'),review_run=info(B/'fresh-source82/source-review.run-evidence82.json'),native_manifest=info(B/'fresh-source82/source-review.run-manifest82.json'),reviewer_packet_sha256=audit['source_review']['reviewer_packet_sha256'],immutable_source_first_chronology_verified=True,canonical_semantic_slots_exact_native=True,coverage='36 frozen inventory items,13nodes,20edges; zero unmapped. G82-05 live first record/stopped alternative title acknowledged; E82-14 cap route optional. Nine exact authored BODY/formula regions. Full source Ex22 L2 continuation and other global obligations remain OPEN.'),
 blind_decoder=dict(identity='root-blind-decoder82',manifest=info(B/'anonymous-decoder82/RAW-manifest.json'),native_run=info(B/'anonymous-decoder82/decoder-run.json'),native_decoded=info(B/'anonymous-decoder82/decoder-result.json'),packet=info(B/'anonymous.decoder82.json'),source_text_visible=False,hash_recipe='SHA256 of exact decoder-run.json bytes, not canonical-flat edge81 recipe. Native copied output bytes verified against original .astis/decoder82 manifest basenames.'),
 fake_closure_scan=info(G/'fake-closure-scan82.json'),axioms=summary['axioms'],
 fresh_full_source_elaboration=info(math/'fresh-whole-module.receipt.json'),
 kernel_generated_and_transitive_ASTIS_proof_closure=info(math/'kernel-dependency-summary82.json'),
 evidence_reuse_reason='Own unchanged accepted complete-source elaboration, two local target proof constants, exact four ASTIS parents and full imported ASTIS closure29constants/32edges; only standard3axioms. Module/probe/closed inputs/native terminal logs checked against named science commit (lossless gzip where required); primary57 remains local fixed RAW honestly pinned. Focused Lean rerun on current successor. No reproof/private trajectory fabrication.',
 external_ASTIS_dependencies=summary['external_ASTIS_dependencies'],
 independent_mathematics=info(math/'decision82.json'),whole_proof=info(math/'whole-proof-mathematics82.json'),
 statement_definition_audit=info(math/'statement-definition-audit82.json'),
 exposition_body_audit=info(math/'exposition-body-audit82.json'),exact_science_freeze=info(G/'input-freeze82.json'),
 mathematical_cases=['Sealed complete private Prop, original six binders/eleven actual definitions/four old Z clauses unchanged; no new public provider premises',
 'Actual P coordinate0 law transported through exact clamped inverse hazard; no abstract substitute exponential source',
 'Every raw first live record, finite/top/zero wait, strict no-event half-open interval; stopped branch carries no phase and infinity retains live arc',
 'Defect subset first-event complement, not equality; finite real probability and measurable complement justify bound',
 'Positive real threshold closed norm tail; continuous Phi and Lambda at zero, ordinary nonpunctured NNReal neighborhood squeeze',
 'Rank0, zero rate/cap/energy and exceptional raw inputs retained without positivity or division premises; fixed-parameter AE initialization/alltime realization inherited'],
 retained_diagnostics=[info(O/'contributor-negative-diagnosis82.json'),info(O/'contributor.receipt.json'),info(G/'successor-delta82.json'),info(math/'initial-hash-negative82.json')],
 rejected_original_commit='396c13491e5a9bdf0abcd5d7fb00c1fb8ef97fcc',
 metadata_successor='Only cell graph lean_view theorem-edge -> new-node; SAU result_kind remains theorem-edge. Source/statement/BODY/native reviews/publication binding unchanged.',
 documentation_successor='Original frozen a5d0303... -> current f2bbb2a... exact one-line docstring only; same complete private Prop and BODY bytes/linecount; step4 formula survival only, defect-probability bound step6.',
 truth_boundary=load(B/'claim.json')['truth_boundary'],
 open_source_routes=['Source direct Exp mean-one SLLN remains distinct OPEN alternative to inherited sufficient indicator-SLLN route',
 'Full Ex22 L2 strong continuity/invariance/Jensen/density continuation and Markov/restart/semigroup remain OPEN',
 'No uniform-parameter nullset/limit, arbitrary correlated random-parameter substitution, global process, hypocoercivity, implementation, cost/main/composition claim'],
 remaining_acceptance=['Serialized shared imports/Registry/rootTests/full astis.py check','Graph/site/actual visual-reader validation','Sole existing stabilization lane/main merge','Exposition Seal/postmerge purification/live deployment','Full paper/actual-input composition/four-paper Goal'],
 collaborator_modified_tracked_RAW_count=len(preserved),all_collaborator_modified_tracked_RAWs_preserved=True,
 production_edits=False,stabilization=False,Goal_complete=False,
 provenance='Named exact science commit, independent native math/blind/source reviews, foreground terminal gate receipts and independent verifier admission. Root proving owner did not self-verify.')
save('verified.json',v)
e={k:v[k] for k in ['verifier_id','verified_commit','source_audit','fake_closure_scan','publication_declarations','semantic_roundtrip_audit']};e['gate']=info(O/'verified.json')
transition_advance(ID,'VERIFIED',worker_id='/root/exact_verify77',evidence=e)
new=copy.deepcopy(cell);new['status']='independently_verified';new['evidence']['independent_verification']=(O/'verified.json').relative_to(R).as_posix()
CELL.write_text(json.dumps(new,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
after=states();assert after[ID]['state']=='VERIFIED'
assert {k:v for k,v in after.items() if k!=ID}=={k:v for k,v in before.items() if k!=ID}
rest=copy.deepcopy(load(CELL));rest['status']=cell['status']
if 'independent_verification' in cell.get('evidence',{}):rest['evidence']['independent_verification']=cell['evidence']['independent_verification']
else:rest['evidence'].pop('independent_verification')
assert rest==cell
for e in preserved:assert info(e['path'])==e
save('admission82.json',dict(state='VERIFIED',cell_state='independently_verified',verified_commit=C,verifier_id='/root/exact_verify77',verified=info(O/'verified.json'),cell=info(CELL),all_other_cell_metadata_semantically_preserved=True,all_other_advances_unchanged=True,existing_stabilizing_lane_unchanged=list(lane),all_collaborator_modified_tracked_RAWs_preserved=True,stabilization=False,Goal_complete=False))
print('VERIFIED',C,info(O/'verified.json')['RAW_sha256'],flush=True)
