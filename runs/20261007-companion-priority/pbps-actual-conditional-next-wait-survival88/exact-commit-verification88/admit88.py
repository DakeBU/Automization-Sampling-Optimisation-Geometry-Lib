from pathlib import Path
import copy,datetime,hashlib,json,os,subprocess,sys
R=Path('E:/Samplinglib');O=Path(__file__).parent;B=O.parent
sys.path[:0]=[str(R),str(R/'tools')]
from tools.astis_advance import transition_advance,current_advances
C='456e13f9561abcf01a285133e91b3951bf2ed892'
ID='ASTIS-SA-20261011-PBPSActualConditionalNextWaitSurvival'
CELL=R/'research-wiki/frontier-cells/ASTIS-SW-PBPS-actual-conditional-next-wait-survival.json'
M=R/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualConditionalNextWaitSurvival.lean'
A=R/'research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261011-PBPSActualConditionalNextWaitSurvival.json'
D='AutoSamplingTheory.ExampleCases.ProximalBPS.ActualConditionalNextWaitSurvival.actual_conditional_next_wait_survival'
ME='/root/exact_verify77'
def path(p):
 p=Path(p);return p if p.is_absolute() else R/p
def load(p):return json.loads(path(p).read_bytes())
def sha(b):return hashlib.sha256(b).hexdigest()
def info(p):
 p=path(p);b=p.read_bytes();return dict(path=p.relative_to(R).as_posix(),raw_sha256=sha(b),bytes=len(b))
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def save(n,d):
 with (O/n).open('x',encoding='utf8',newline='\n') as f:json.dump(d,f,ensure_ascii=False,indent=2);f.write('\n')
def git(*args):return subprocess.check_output(['git',*args],cwd=R)
assert git('rev-parse','HEAD').decode().strip()==C
assert load(O/'checks-complete88.json')['status']=='PASS'
assert info(M)['raw_sha256']=='2f509ce49343d349f7a9fb21d2f7b1697c1a6de942353f6cd8ff16d522911569'
assert M.read_bytes()==git('show',C+':'+M.relative_to(R).as_posix())
freeze=load(O/'input-freeze88.json')
for group in ['exact_commit_matches','nested_mathlib_matches','local_fixed_primary_and_excluded_extracts','preexisting_collaborator_inputs']:
 for e in freeze[group]:assert info(e['path'])['raw_sha256']==e['raw_sha256']
preserved=load(O/'collaborator-preservation88.json')['RAWs'];assert len(preserved)==21
for e in preserved:assert info(e['path'])==e
before=current_advances();assert before[ID]['state']=='PROVED_LOCAL'
assert before[ID]['owner_id']=='companion_root_20261005'
lane={k:v for k,v in before.items() if v['state']=='STABILIZING'}
assert set(lane)=={'ASTIS-SA-20261005-SPHMCImplementedPhaseKernel'}
cell=load(CELL);assert cell['status']=='proved_locally' and cell['graph_contribution']['lean_view']=='new-node'
save('cell.before-independent-admission88.json',cell)
ledger=R/'runs/substantive_advances.jsonl';ledger_before=ledger.read_bytes()
save('ledger.before-admission88.json',info(ledger))
other_cells={p.relative_to(R).as_posix():sha(p.read_bytes()) for p in CELL.parent.glob('*.json') if p!=CELL}
save('other-cells.before-admission88.json',other_cells)
receipts=[]
for n in ['packet','focused-module','current-kernel','contributor','publication','publication-reviewed','semantic','frontier']:
 p=O/(n+'.receipt.json');d=load(p)
 assert d['exit_code']==0 and d['terminal_closed'] and d['checked_commit']==C
 for k in ['stdout','stderr']:assert info(d[k]['path'])==d[k]
 receipts.append(info(p))
audit=load(A);source=B/'independent-source88';native=load(source/'source-review88.decision.native.json')
math=B/'independent-math88';kernel=load(math/'kernel-dependency-summary88.json');dec=B/'anonymous-decoder'
assert audit['state']=='accepted' and audit['source_review']['reviewer']=='/root/fresh_source87'
assert audit['publication_binding_sha256']=='01f6aaf74fd89229d665d649fbe18d0769a8253b9c2e717d56772bb9678344bb'
assert not load(O/'fake-closure-scan88.json')['hits'] and not native['blocking_deltas'] and not native['repairs']
assert len(audit['semantic_slots'])==7 and native['accepted_truth_boundary']['target_source_node']=='S87-I4'
v=dict(status='PASS_INDEPENDENT_EXACT_COMMIT_VERIFICATION',verifier_id=ME,verified_commit=C,created_utc=now(),actual_admission_helper_PID=os.getpid(),lean_module=info(M),gate=receipts,publication_declarations=[D],publication_binding_sha256=audit['publication_binding_sha256'],semantic_roundtrip_audit='ASTIS-RT-20261011-PBPSActualConditionalNextWaitSurvival',
 source_audit=dict(state='accepted',reviewer='/root/fresh_source87',review_result=info(source/'source-review88.decision.native.json'),review_run=info(source/'source-review88.run.native.json'),native_manifest=info(source/'closed-raw-manifest.source-review88.native.json'),reviewer_packet_sha256=audit['source_review']['reviewer_packet_sha256'],immutable_source_first_chronology_verified=True,canonical_seven_semantic_slots_exact_native=True,distinct_topology_review=info(R/'runs/20261007-companion-priority/pbps-conditional-next-wait-preread88/header-math88/topology-review88.json'),topology_creator_not_self_approving=True,coverage='Local9nodes/10AND edges; all13 actual definitions/six analytic conditions/five complete contiguous formula/BODY regions. Only S87-I4 conditional history-dependent survival accepted; I5/fullG11/fullA7 remainOPEN.',accepted_truth_boundary=native['accepted_truth_boundary']),
 blind_decoder=dict(identity='/root/blind_decoder88',manifest=info(dec/'closed-RAW-manifest.json'),native_run=info(dec/'decoder.run.json'),native_result=info(dec/'reconstructed-theorem.json'),packet=info(B/'anonymous.decoder88.json'),source_text_visible=False,source_identity_visible=False,hash_recipe='Actual88 closed-RAW-manifest input RAW hash and canonical COMPLETE packet hash; declared canonical packet excluding top-level packet_sha256 checked separately. Exact native statement/text/run hashes checked. Native output immutable, not adapted from87 schema.',notation_resolution=info(source/'decoder-wording-clarification88.native.json'),interpretation='The fixed deterministic Borel function d may give random d(H_n); no future-input/external-random-function duration is admitted. Source reviewer explicitly accepted notation resolution, native wording retained.'),
 fake_closure_scan=info(O/'fake-closure-scan88.json'),standard_axioms=['propext','Classical.choice','Quot.sound'],fresh_current_focused_build=info(O/'focused-module.receipt.json'),fresh_current_public_kernel=info(O/'current-kernel.receipt.json'),reused_complete_source_elaboration=info(math/'fresh-whole-source-kernel.receipt.json'),independent_mathematics=info(math/'decision88.json'),independent_mathematics_closed_manifest=info(math/'closed-RAW-manifest88.json'),independent_complete_exposition=info(math/'whole-exposition-review88.json'),kernel_generated_and_transitive_ASTIS_proof_closure=info(math/'kernel-dependency-summary88.json'),kernel_source_binding=info(math/'transitive-kernel-source-binding88.json'),actual_public_producer_dependencies=kernel['immediate_public_theorem_parents'],private_immediate_dependencies=[n for n in kernel['immediate_ASTIS_dependencies'] if n.startswith('_private.')],owned_proof_constant_count=10,immediate_ASTIS_dependency_count=12,transitive_ASTIS_constant_count=58,transitive_ASTIS_edge_count=84,
 generic_reuse_boundary='Generic sum-product measurable equivalence, strict Borel comparison, map_apply, ofReal_measureReal, product section integral and restricted indicator lintegral are pinned Mathlib. The new ASTIS result consumes actual87/75/77 internally for history-dependent conditional survival; no parent/provider premise.',
 evidence_reuse_reason='Exact committed module2f509 and sealed private Prop are byte-identical to independently audited whole source/probe. Complete standard3axiom type+value private/generated closure transfers unchanged. Fresh focused/current public kernel and current source/publication-reviewed/semantic/frontier/contributor gates passed on named science.',lossless_native_archive_audit=info(O/'lossless-archives88.audit.json'),exact_science_freeze=info(O/'input-freeze88.json'),
 mathematical_cases=['Same13 actual literal definitions/six analytic binders; d/A are admissible deterministic Borel tests, not analytic/provider hypotheses.','waitObs dead-zero is proof-only; strict u>=0 comparison false afterstop. Joint Borel event established before product integration.','Fixed-history fiber exact pointwise identity for all histories, then actual history/tail product sections; no random-parameter AE substitution or event normalization.','Null A, n0, rank0, flat/zero hazard, zero normals, zero/clipped exceptional inputs and live infinite waits retain exact public semantics; deterministic eventdepth only.'],
 truth_boundary=load(B/'claim.json')['truth_boundary'],remaining_acceptance=['Serialized shared imports/Registry/rootTests/full aggregate and existing sole stabilization lane','Reader/graph/site/browser/visual acceptance; current source DOM content check gives no browser/layout credit','Main merge, ExpositionSeal/postmerge purification/live deployment','I5 conditional finite-wait density/ordered-time iteration/final-factor/fullA7/fullG11 pathlaw','Physical-time residual memorylessness/random stopping/restart/Markov/CK/reversal/invariance/Jensen/allL2','Implementation/error/cost/main/actual-input composition/fullpaper/four-paperGoal'],
 all21collaborator_RAWs_preserved=True,production_edits=False,stabilization=False,PURIFIED=False,Goal_complete=False,provenance='Independent named-science-commit verifier distinct from proving owner, blind decoder and final source reviewer. No self-source review or canonical graph mutation; native review inputs and archives exact.')
save('verified.json',v)
e={k:v[k] for k in ['verifier_id','verified_commit','source_audit','fake_closure_scan','publication_declarations','semantic_roundtrip_audit']}
e['gate']=info(O/'verified.json')
transition_advance(ID,'VERIFIED',worker_id=ME,evidence=e)
new=copy.deepcopy(cell);new['status']='independently_verified'
new['evidence']['independent_verification']=(O/'verified.json').relative_to(R).as_posix()
CELL.write_text(json.dumps(new,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
after=current_advances();assert after[ID]['state']=='VERIFIED'
assert {k:v for k,v in after.items() if k!=ID}=={k:v for k,v in before.items() if k!=ID}
ledger_after=ledger.read_bytes();assert ledger_after.startswith(ledger_before)
assert len(ledger_after[len(ledger_before):].splitlines())==1
rest=copy.deepcopy(load(CELL));rest['status']=cell['status']
if 'independent_verification' in cell.get('evidence',{}):rest['evidence']['independent_verification']=cell['evidence']['independent_verification']
else:rest['evidence'].pop('independent_verification')
assert rest==cell
assert {p.relative_to(R).as_posix():sha(p.read_bytes()) for p in CELL.parent.glob('*.json') if p!=CELL}==other_cells
for x in preserved:assert info(x['path'])==x
save('admission88.json',dict(state='VERIFIED',cell_state='independently_verified',verified_commit=C,verifier_id=ME,verified=info(O/'verified.json'),cell=info(CELL),ledger=info(ledger),exactly_one_append_only_event=True,independent_verification_is_string=True,all_other_cell_metadata_semantically_preserved=True,all_other_cell_RAWs_preserved=True,all_other_advances_unchanged=True,existing_stabilizing_lane_unchanged=[dict(id=k,owner=v['owner_id']) for k,v in lane.items()],all21collaborator_RAWs_preserved=True,stabilization=False,Goal_complete=False))
env=dict(os.environ,PYTHONUTF8='1',PYTHONIOENCODING='utf8')
args=[sys.executable,'-X','utf8','tools/astis_frontier_cells.py','check'];start=now()
with (O/'post-admission-frontier.stdout.log').open('xb') as out,(O/'post-admission-frontier.stderr.log').open('xb') as err:
 child=subprocess.Popen(args,cwd=R,env=env,stdout=out,stderr=err);print('post-admission-frontier foreground PID',child.pid,flush=True);code=child.wait()
save('post-admission-frontier.receipt.json',dict(command=args,actual_foreground_PID=child.pid,exit_code=code,terminal_closed=True,checked_science_commit=C,started_utc=start,finished_utc=now(),stdout=info(O/'post-admission-frontier.stdout.log'),stderr=info(O/'post-admission-frontier.stderr.log')))
assert code==0
for x in preserved:assert info(x['path'])==x
save('run-manifest88.json',dict(status='CLOSED_INDEPENDENT_EXACT_SCIENCE_ADMISSION',verified_commit=C,verifier_id=ME,verified=info(O/'verified.json'),admission=info(O/'admission88.json'),gate_receipts=receipts+[info(O/'post-admission-frontier.receipt.json')],science_input_freeze=info(O/'input-freeze88.json'),archive_audit=info(O/'lossless-archives88.audit.json'),postscience_cell_and_ledger_only=True,production_or_shared_integration_edits=False,all21collaborator_RAWs_preserved=True,native_reasoning_trajectory_claimed=False))
owned=[info(p) for p in sorted(O.iterdir()) if p.is_file()]
save('closed-RAW-manifest88.json',dict(status='CLOSED_RAW_NONCIRCULAR',verified_commit=C,verifier_id=ME,checked_science_inputs=freeze['exact_commit_matches'],nested_pinned_mathlib=freeze['nested_mathlib_matches'],local_fixed_primary_and_excluded_extracts=freeze['local_fixed_primary_and_excluded_extracts'],preexisting_collaborator_inputs=freeze['preexisting_collaborator_inputs'],owned_artifacts=owned,self_hash_intentionally_omitted=True,admission_cell_and_ledger_are_explicit_postscience_changes=True,science_input_cell_ledger_hashes_bind_named_git_commit_not_postadmission_worktree=True,native_review_inputs_unchanged=True,all21collaborator_RAWs_preserved=True))
for i in owned:assert info(i['path'])==i
assert git('rev-parse','HEAD').decode().strip()==C
print(json.dumps(dict(status='VERIFIED_NATIVE_CLOSED',verified_commit=C,verified=info(O/'verified.json'),manifest=info(O/'closed-RAW-manifest88.json'),admission=info(O/'admission88.json'),post_admission_frontier=info(O/'post-admission-frontier.receipt.json')),indent=2),flush=True)
