from pathlib import Path
import copy,datetime,hashlib,json,os,subprocess,sys
R=Path('E:/Samplinglib');os.chdir(R);sys.path[:0]=[str(R),str(R/'tools')]
from tools.astis_advance import transition_advance,_replay_advances
B=R/'runs/20261007-companion-priority/pbps-actual-bounded-test-continuity83';O=B/'exact-commit-verification83'
C='43b698b4d8dbdb7c881ff41b9c26ca8f0135c781';ID='ASTIS-SA-20261010-PBPSActualBoundedTestContinuity'
D='AutoSamplingTheory.ExampleCases.ProximalBPS.ActualBoundedTestContinuity.actual_bounded_test_expectation_continuity'
CELL=R/'research-wiki/frontier-cells/ASTIS-SW-PBPS-actual-bounded-test-continuity.json'
M=R/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualBoundedTestContinuity.lean'
A=R/'research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261010-PBPSActualBoundedTestContinuity.json'
def load(p):return json.loads(Path(p).read_text(encoding='utf8'))
def info(p):
 p=Path(p);p=p if p.is_absolute() else R/p;b=p.read_bytes();return dict(path=p.relative_to(R).as_posix(),RAW_bytes=len(b),RAW_sha256=hashlib.sha256(b).hexdigest())
def save(n,d):
 with (O/n).open('x',encoding='utf8',newline='\n') as f:json.dump(d,f,ensure_ascii=False,indent=2);f.write('\n')
def git(*a):return subprocess.check_output(['git',*a],cwd=R)
def states():return _replay_advances([json.loads(v) for v in (R/'runs/substantive_advances.jsonl').read_text(encoding='utf8').splitlines() if v.strip()])
assert git('rev-parse','HEAD').decode().strip()==C
assert load(O/'checks-complete83.json')['status']=='PASS'
assert M.read_bytes()==git('show',C+':'+M.relative_to(R).as_posix())
assert info(M)['RAW_sha256']=='0a88a2071df983f791899b01b0de40f52241b06ba452eea3751e471396adec6b'
freeze=load(O/'input-freeze83.correct-cell.json')
for e in freeze['exact_commit_matches']+freeze['nested_pinned_mathlib_matches']+freeze['local_fixed_primary']:assert info(e['path'])['RAW_sha256']==e['RAW_sha256']
preserved=load(O/'collaborator-modified-RAW.before83.json')
baseline=load(R/'runs/20261007-companion-priority/pbps-bounded-test-preread83/post-fetch83.workspace-RAW.corrected.json')['tracked_modified']
assert len(preserved)==21 and {e['path']:e['RAW_sha256'] for e in preserved}==baseline
for e in preserved:assert info(e['path'])==e
before=states();assert before[ID]['state']=='PROVED_LOCAL' and before[ID]['owner_id']=='companion_root_20261005'
lane={k:v for k,v in before.items() if v.get('state')=='STABILIZING'};assert set(lane)=={'ASTIS-SA-20261005-SPHMCImplementedPhaseKernel'}
cell=load(CELL);assert cell['status']=='proved_locally' and cell['graph_contribution']['lean_view']=='new-node';save('cell.before-independent-admission83.json',cell)
audit=load(A);assert audit['state']=='accepted' and audit['source_review']['reviewer']=='/root/fresh_source78'
assert audit['publication_binding_sha256']=='d9e38c7530c2c337b7e95a866a299ba3110c9f1c64db4e4d2e049f0b90fcf04c'
receipts=[]
for n in ['packet-correct-cell','focused-module','contributor','publication','publication-reviewed','semantic','frontier']:
 p=O/(n+'.receipt.json');r=load(p);assert r['exit_code']==0 and r['terminal_closed'] and r['checked_commit']==C
 for e in [r['stdout'],r['stderr']]:assert info(e['path'])==e
 receipts.append(info(p))
assert not load(O/'fake-closure-scan83.json')['hits']
math=B/'independent-math83';mr=load(math/'fresh-whole-module.receipt.json');assert mr['exit_code']==0 and mr['terminal_closed']
for e in [mr['source'],mr['probe'],mr['stdout'],mr['stderr']]:assert info(e['path'])==e
summary=load(math/'kernel-dependency-summary83.json');assert summary['expected_four_parent_frontier_exact']
assert set(summary['axioms'])=={'propext','Classical.choice','Quot.sound'}
v=dict(status='PASS_INDEPENDENT_EXACT_COMMIT_VERIFICATION',verifier_id='/root/exact_verify77',verified_commit=C,
 created_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),actual_admission_helper_PID=os.getpid(),
 lean_module=info(M),gate=receipts,publication_declarations=[D],publication_binding_sha256=audit['publication_binding_sha256'],
 semantic_roundtrip_audit='ASTIS-RT-20261010-PBPSActualBoundedTestContinuity',
 source_audit=dict(state='accepted',reviewer='/root/fresh_source78',review_result=info(B/'independent-source83/source-review.result83.json'),review_run=info(B/'independent-source83/source-review.run-evidence83.json'),native_manifest=info(B/'independent-source83/source-review.run-manifest83.json'),reviewer_packet_sha256=audit['source_review']['reviewer_packet_sha256'],immutable_source_first_chronology_verified=True,canonical_semantic_slots_exact_native=True,coverage='30 inventory items,17 nodes,30 relation rows=29 dependencies+1 excluded boundary association; zero unmapped. Separately reviewed AND-inside-optional-OR topology overlay retained. Eight exact contiguous formula/BODY regions121-230. Full outer L2/global obligations OPEN.'),
 blind_decoder=dict(identity='root-blind-decoder83',manifest=info(B/'anonymous-decoder83/RAW-manifest.json'),native_run=info(B/'anonymous-decoder83/decoder-run.json'),native_decoded=info(B/'anonymous-decoder83/decoder-result.json'),packet=info(B/'anonymous-decoder83/packet.json'),source_text_visible=False,hash_recipe='Exact native decoder-run.json RAW SHA; local .astis/decoder83/packet.json identical committed packet.json/anonymous.decoder83.json, exact output basenames copied unchanged.'),
 fake_closure_scan=info(O/'fake-closure-scan83.json'),axioms=summary['axioms'],
 fresh_full_source_elaboration=info(math/'fresh-whole-module.receipt.json'),kernel_generated_and_transitive_ASTIS_proof_closure=info(math/'kernel-dependency-summary83.json'),
 evidence_reuse_reason='Own unchanged accepted full source elaboration; two local proof constants, four actual ASTIS parents, imported closure31 constants/37edges. All native closed inputs and logs bound to named science commit or exact lossless gzip; fixed primary57 local RAW honestly pinned, not claimed committed. Current focused Lean rerun. No reproof or fabricated trajectory.',
 external_ASTIS_dependencies=summary['external_ASTIS_dependencies'],independent_mathematics=info(math/'decision83.json'),whole_proof=info(math/'whole-proof-mathematics83.json'),statement_definition_audit=info(math/'statement-definition-audit83.json'),exposition_body_audit=info(math/'exposition-body-audit83.json'),exact_science_freeze=info(O/'input-freeze83.correct-cell.json'),
 mathematical_cases=['Sealed full private Prop, six source binders, eleven literal actual definitions; retained82 clauses and single Z before all tests; no public provider premises',
 'Actual test measurability and integrability from global absolute bound under internally proved actual product probability',
 'Pointwise2M measurable defect indicator; integral subtraction/constant normalization and finite real event measure; inclusion bound, not event equality',
 'Actual flow and hazard continuity/zero laws; nonpunctured NNReal zero expectation squeeze; no AS-DCT from probability convergence',
 'M0/rank0/zero raw thresholds/top wait/stopped/fallback/fixed-parameter AE boundaries retained'],
 retained_diagnostics=[info(p) for p in sorted(O.glob('*diagnosis*.json'))]+[info(p) for p in sorted(O.glob('*negative*.json'))],
 wrong_packet_diagnostic=info(O/'packet.receipt.json'),correct_packet=info(O/'packet-correct-cell.receipt.json'),
 truth_boundary=load(B/'claim.json')['truth_boundary'],
 open_source_routes=['Source compactly supported C_c consumer extended explicitly to bounded continuous real C_b; quantitative2M attributed ASTIS elaboration',
 'Outer-state L2 DCT/invariance/Jensen contraction/density/operator laws/global Markov-restart-semigroup remainOPEN',
 'No uniformparameter AE/limit or arbitrary correlated randomparameter substitution; no unbounded moments/cost/main/composition claim'],
 remaining_acceptance=['Serialized shared imports/Registry/rootTests/full astis.py check','Graph/site/visual-reader validation','Existing sole stabilization/main merge','Exposition Seal/postmerge purification/live deployment','Full paper/actual-input composition/four-paper Goal'],
 collaborator_modified_tracked_RAW_count=21,all_collaborator_modified_tracked_RAWs_preserved=True,production_edits=False,stabilization=False,Goal_complete=False,
 provenance='Independent exact science verification with native math/blind/source reviews and foreground terminal receipts. Proving owner did not self-verify.')
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
save('admission83.json',dict(state='VERIFIED',cell_state='independently_verified',verified_commit=C,verifier_id='/root/exact_verify77',verified=info(O/'verified.json'),cell=info(CELL),all_other_cell_metadata_semantically_preserved=True,all_other_advances_unchanged=True,existing_stabilizing_lane_unchanged=list(lane),all_collaborator_modified_tracked_RAWs_preserved=True,stabilization=False,Goal_complete=False))
env=dict(os.environ,PYTHONUTF8='1',PYTHONIOENCODING='utf8');args=[sys.executable,'-X','utf8','tools/astis_frontier_cells.py','check'];start=datetime.datetime.now(datetime.timezone.utc).isoformat()
with (O/'post-admission-frontier.stdout.log').open('xb') as out,(O/'post-admission-frontier.stderr.log').open('xb') as err:
 child=subprocess.Popen(args,cwd=R,env=env,stdout=out,stderr=err);code=child.wait()
save('post-admission-frontier.receipt.json',dict(command_argv=args,actual_foreground_PID=child.pid,exit_code=code,terminal_closed=True,checked_science_commit=C,start_utc=start,end_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),stdout=info(O/'post-admission-frontier.stdout.log'),stderr=info(O/'post-admission-frontier.stderr.log')))
assert code==0
save('closed-RAW-manifest83.json',dict(status='CLOSED',verified_commit=C,verifier_id='/root/exact_verify77',checked_science_inputs=freeze['exact_commit_matches'],local_fixed_primary=freeze['local_fixed_primary'],owned_artifacts=[info(p) for p in sorted(O.iterdir()) if p.is_file()],self_hash_omitted=True,admission_cell_and_ledger_are_explicit_postscience_changes=True,native_review_inputs_unchanged=True))
print('VERIFIED CLOSED',C,info(O/'verified.json')['RAW_sha256'],info(O/'closed-RAW-manifest83.json')['RAW_sha256'],flush=True)
