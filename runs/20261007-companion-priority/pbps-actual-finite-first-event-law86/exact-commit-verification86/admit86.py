from pathlib import Path
import copy,datetime,hashlib,json,os,subprocess,sys
R=Path('E:/Samplinglib');O=Path(__file__).parent;B=O.parent;sys.path[:0]=[str(R),str(R/'tools')]
from tools.astis_advance import transition_advance,current_advances
C='0bb3cd64ba1235114feaeed99ba22e675b23db76';ID='ASTIS-SA-20261011-PBPSActualFiniteFirstEventLaw'
D='AutoSamplingTheory.ExampleCases.ProximalBPS.ActualFiniteFirstEventLaw.actual_finite_first_event_law'
CELL=R/'research-wiki/frontier-cells/ASTIS-SW-PBPS-actual-finite-first-event-law.json'
M=R/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualFiniteFirstEventLaw.lean'
A=R/'research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261011-PBPSActualFiniteFirstEventLaw.json'
def path(p):
 p=Path(p);return p if p.is_absolute() else R/p
def load(p):return json.loads(path(p).read_bytes())
def info(p):
 p=path(p);b=p.read_bytes();return dict(path=p.relative_to(R).as_posix(),raw_sha256=hashlib.sha256(b).hexdigest(),bytes=len(b))
def save(n,v):
 with (O/n).open('x',encoding='utf8',newline='\n') as f:json.dump(v,f,ensure_ascii=False,indent=2);f.write('\n')
def git(*a):return subprocess.check_output(['git',*a],cwd=R)
assert git('rev-parse','HEAD').decode().strip()==C and load(O/'checks-complete86.json')['status']=='PASS'
assert info(M)['raw_sha256']=='d6667ccbb917d6463e96b2082a5a26089950889fd20af4859052cd7a9a1db776' and M.read_bytes()==git('show',C+':'+M.relative_to(R).as_posix())
freeze=load(O/'input-freeze86.json')
for group in ['exact_commit_matches','nested_mathlib_matches','local_fixed_primary_and_excluded_extracts','local_compiled_artifacts','preexisting_collaborator_inputs']:
 for e in freeze[group]:assert info(e['path'])['raw_sha256']==e['raw_sha256']
preserved=load(O/'collaborator-preservation86.json')['RAWs'];assert len(preserved)==21
for e in preserved:assert info(e['path'])==e
before=current_advances();assert before[ID]['state']=='PROVED_LOCAL' and before[ID]['owner_id']=='companion_root_20261005'
lane={k:v for k,v in before.items() if v['state']=='STABILIZING'};assert set(lane)=={'ASTIS-SA-20261005-SPHMCImplementedPhaseKernel'}
cell=load(CELL);assert cell['status']=='proved_locally' and cell['graph_contribution']['lean_view']=='new-node'
save('cell.before-independent-admission86.json',cell)
ledger=R/'runs/substantive_advances.jsonl';ledger_before=ledger.read_bytes();save('ledger.before-admission86.json',info(ledger))
audit=load(A);assert audit['state']=='accepted' and audit['source_review']['reviewer']=='independent-primary-source-reviewer86' and audit['publication_binding_sha256']=='30871a16346f70e877abadba35385e969b265af174bfeb19b8914658e0a0ffdd'
receipts=[]
for n in ['packet','focused-module','current-kernel','contributor','publication','publication-reviewed','semantic','frontier']:
 p=O/(n+'.receipt.json');r=load(p);assert r['exit_code']==0 and r['terminal_closed'] and r['checked_commit']==C
 for s in ['stdout','stderr']:assert info(r[s]['path'])==r[s]
 receipts.append(info(p))
assert not load(O/'fake-closure-scan86.json')['hits']
math=B/'independent-math86';summary=load(math/'kernel-dependency-summary86.json')
assert summary['standard_axioms_only'] and summary['exact_four_public_parents'] and len(summary['actual_public_producer_parents'])==4 and len(summary['private_spec_dependencies'])==12
assert [summary[k] for k in ['owned_count','transitive_count','edge_count']]==[19,39,44]
source=B/'independent-source86';dec=B/'anonymous-decoder86'
v=dict(status='PASS_INDEPENDENT_EXACT_COMMIT_VERIFICATION',verifier_id='/root/exact_verify77',verified_commit=C,created_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),actual_admission_helper_PID=os.getpid(),lean_module=info(M),gate=receipts,publication_declarations=[D],publication_binding_sha256=audit['publication_binding_sha256'],semantic_roundtrip_audit='ASTIS-RT-20261011-PBPSActualFiniteFirstEventLaw',source_audit=dict(state='accepted',reviewer='independent-primary-source-reviewer86',review_result=info(source/'source-review86.eof-rebound.final.decision.json'),review_run=info(source/'source-review86.eof-rebound.final.run.json'),native_manifest=info(source/'source-review86.eof-rebound.final.native-RAW-manifest.json'),reviewer_packet_sha256=audit['source_review']['reviewer_packet_sha256'],immutable_source_first_chronology_verified=True,canonical_semantic_slots_exact_native=True,coverage='47inventory/72atomic anchors/38nodes/76relations=73dependencies+3excluded associations. Original heuristic route EXCLUDED; selected CDF/FTC versus alternative hazard transport remains OR with AND ingredients. Final Gaussian G38 explicitly AND-consumes fixed-time probability/positivity/T1=1 through distinctly reviewed fifth edge; all global source conclusions OPEN. Full source statement six analytic binders/14literal definitions and eleven exact helper/publicBODY/formula regions accepted.'),blind_decoder=dict(identity=load(dec/'decoder-run.json')['decoder'],manifest=info(dec/'RAW-manifest.json'),native_run=info(dec/'decoder-run.json'),native_result=info(dec/'decoder-result.json'),packet=info(dec/'anonymous.packet.json'),source_text_visible=False,packet_byte_identical_across_EOF_rebinding=True,hash_recipe='Actual86 native decoder-run RAW49061692..., canonical anonymous packeteaeaa318..., all2inputs/3outputs rehashed and original .astis copies equal published copies. No85 hash substitutions or invented trajectory.'),fake_closure_scan=info(O/'fake-closure-scan86.json'),standard_axioms=['propext','Classical.choice','Quot.sound'],fresh_current_public_kernel=info(O/'current-kernel.receipt.json'),fresh_current_focused_build=info(O/'focused-module.receipt.json'),reused_full_source_elaboration=info(math/'fresh-whole-module.receipt.json'),fresh_exact_EOF_proposed_full_source=info(B/'eof-math-review86/fresh-proposed-source.receipt.json'),kernel_generated_and_transitive_ASTIS_proof_closure=info(math/'kernel-dependency-summary86.json'),actual_public_producer_dependencies=summary['actual_public_producer_parents'],private_immediate_dependencies=summary['private_spec_dependencies'],owned_proof_constant_count=19,transitive_ASTIS_constant_count=39,transitive_ASTIS_edge_count=44,independent_mathematics=info(math/'decision86.json'),independent_EOF_transfer=info(B/'eof-math-review86/decision86.json'),exact_science_freeze=info(O/'input-freeze86.json'),evidence_reuse_reason='Own full-source six standard-axiom blocks and complete private/generated kernel closure are unchanged over exact one final LF deletion; fresh complete proposed source already accepted at exact current d666 RAW. Current named science source and eleven source regions match; fresh focused build/current public kernel and all current contracts rerun. Historical module and lesson descriptors resolve explicitly to immutable before snapshots without mutating original native records.',mathematical_cases=['Original six analytic binders and fourteen literal actual definitions; exact sealed private Prop preserved; no density/FTC/integrability/normalizer/provider hypothesis added.','Actual infinite Exp1 product coordinate0 feeds stopped U; positive finite A={0<U<=T} excludes infinity and real-default0 before finite projection.','Finite CDF equality derives density law; true Borel postbounce mark supplies marked pushforward; finite mass1-exp(-LambdaT)<=1 is not renormalized.','Three bounded-Borel L1 outputs and exact weighted integral_map/withDensity identity, including T0/M0/rank0/zero-normal/flat-hazard/infinite-wait/nullzero thresholds.'],historical_nonmathematical_stage_log=info(O/'stage-log-history86.json'),postscience_helper_observation=info(O/'postscience-helper-observation86.json'),truth_boundary=load(B/'claim.json')['truth_boundary'],remaining_acceptance=['Serialized imports/Registry/rootTests/full astis.py check','Renderer application, graph/site/visual-reader acceptance','Existing sole stabilization lane/main merge','ExpositionSeal/postmerge purification/live deployment','Unused-tail conditional/path A7/residual-survival/reversal/invariance/AE-safe Jensen/allL2/density/restart/Markov/CK/semigroup','Implementation/error/unboundedcost/actual-input composition/fullpaper/four-paperGoal'],all21collaborator_RAWs_preserved=True,production_edits=False,stabilization=False,Goal_complete=False,provenance='Independent named science admission; proof owner did not self-verify; native math/blind/source reused only after exact RAW/archive checks.')
save('verified.json',v)
e={k:v[k] for k in ['verifier_id','verified_commit','source_audit','fake_closure_scan','publication_declarations','semantic_roundtrip_audit']};e['gate']=info(O/'verified.json')
transition_advance(ID,'VERIFIED',worker_id='/root/exact_verify77',evidence=e)
new=copy.deepcopy(cell);new['status']='independently_verified';new['evidence']['independent_verification']=(O/'verified.json').relative_to(R).as_posix();CELL.write_text(json.dumps(new,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
after=current_advances();assert after[ID]['state']=='VERIFIED' and {k:v for k,v in after.items() if k!=ID}=={k:v for k,v in before.items() if k!=ID}
ledger_after=ledger.read_bytes();assert ledger_after.startswith(ledger_before) and len(ledger_after[len(ledger_before):].splitlines())==1
rest=copy.deepcopy(load(CELL));rest['status']=cell['status']
if 'independent_verification' in cell.get('evidence',{}):rest['evidence']['independent_verification']=cell['evidence']['independent_verification']
else:rest['evidence'].pop('independent_verification')
assert rest==cell
for e in preserved:assert info(e['path'])==e
save('admission86.json',dict(state='VERIFIED',cell_state='independently_verified',verified_commit=C,verifier_id='/root/exact_verify77',verified=info(O/'verified.json'),cell=info(CELL),ledger=info(ledger),exactly_one_append_only_event=True,all_other_cell_metadata_semantically_preserved=True,all_other_advances_unchanged=True,existing_stabilizing_lane_unchanged=list(lane),all21collaborator_RAWs_preserved=True,stabilization=False,Goal_complete=False))
env=dict(os.environ,PYTHONUTF8='1',PYTHONIOENCODING='utf8');args=[sys.executable,'-X','utf8','tools/astis_frontier_cells.py','check'];start=datetime.datetime.now(datetime.timezone.utc).isoformat()
with (O/'post-admission-frontier.stdout.log').open('xb') as out,(O/'post-admission-frontier.stderr.log').open('xb') as err:
 child=subprocess.Popen(args,cwd=R,env=env,stdout=out,stderr=err);print('post-admission-frontier foreground PID',child.pid,flush=True);code=child.wait()
save('post-admission-frontier.receipt.json',dict(command=args,actual_foreground_PID=child.pid,exit_code=code,terminal_closed=True,checked_science_commit=C,started_utc=start,finished_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),stdout=info(O/'post-admission-frontier.stdout.log'),stderr=info(O/'post-admission-frontier.stderr.log')));assert code==0
for e in preserved:assert info(e['path'])==e
save('closed-RAW-manifest86.json',dict(status='CLOSED_RAW_NONCIRCULAR',verified_commit=C,verifier_id='/root/exact_verify77',checked_science_inputs=freeze['exact_commit_matches'],nested_pinned_mathlib=freeze['nested_mathlib_matches'],local_fixed_primary_and_excluded_extracts=freeze['local_fixed_primary_and_excluded_extracts'],local_compiled_artifacts=freeze['local_compiled_artifacts'],preexisting_collaborator_inputs=freeze['preexisting_collaborator_inputs'],historical_descriptors_resolved_without_native_mutation=freeze['historical_descriptors_resolved_without_native_mutation'],owned_artifacts=[info(p) for p in sorted(O.iterdir()) if p.is_file()],self_hash_intentionally_omitted=True,admission_cell_and_ledger_are_explicit_postscience_changes=True,science_input_cell_ledger_hashes_bind_named_git_commit_not_postadmission_worktree=True,native_review_inputs_unchanged=True,all21collaborator_RAWs_preserved=True))
print('VERIFIED CLOSED',C,info(O/'verified.json')['raw_sha256'],info(O/'closed-RAW-manifest86.json')['raw_sha256'],info(O/'post-admission-frontier.receipt.json')['raw_sha256'],flush=True)
