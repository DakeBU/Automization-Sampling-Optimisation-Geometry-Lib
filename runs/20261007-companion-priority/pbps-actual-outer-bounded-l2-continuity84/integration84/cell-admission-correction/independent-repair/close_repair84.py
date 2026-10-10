from pathlib import Path
import datetime,hashlib,json,os,re,subprocess,sys
R=Path('E:/Samplinglib');B=R/'runs/20261007-companion-priority/pbps-actual-outer-bounded-l2-continuity84';O=Path(__file__).parent;C='5186f92607df617c4e4a8a90d0c5e6b5fc611090';S=B/'integration84/cell-admission-correction/graph-scope'
def info(p):
 p=Path(p);p=p if p.is_absolute() else R/p;b=p.read_bytes();return dict(path=p.relative_to(R).as_posix(),RAW_sha256=hashlib.sha256(b).hexdigest(),RAW_bytes=len(b))
def load(p):return json.loads(Path(p).read_bytes())
def save(n,d):
 with (O/n).open('x',encoding='utf8',newline='\n') as f:json.dump(d,f,ensure_ascii=False,indent=2);f.write('\n')
def norm(b):return b.replace(b'\r\n',b'\n')
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=R).decode().strip()==C
prior=load(O/'bounded-repair-evidence.json');scope=load(S/'scope-correction.json');cell=R/'research-wiki/frontier-cells/ASTIS-SW-PBPS-actual-outer-bounded-l2-continuity.json';old=load(O/'current-cell.before-graph-scope-clarification.snapshot.json');cur=load(cell)
assert info(S/'cell.before.json')['RAW_sha256']==info(O/'current-cell.before-graph-scope-clarification.snapshot.json')['RAW_sha256']=='d2fefdde6795303e706cfe687e2806dcc39304558a1ff6bf1f0cba0d49d0d493'
assert (S/'note.before.json').read_bytes()==(O/'integration.corrected.notes.before-graph-clarification.snapshot.json').read_bytes()
assert cur['status']=='independently_verified' and cur['evidence']==old['evidence'];v=cur['graph_contribution']['visual_review'];assert 'incomplete name-scanned reference signals' in v and 'not elaborated theorem dependencies' in v and 'four actual producer parents are certified separately' in v
rest=json.loads(json.dumps(cur));rest['graph_contribution']['visual_review']=old['graph_contribution']['visual_review'];assert rest==old
note=load(B/'integration.corrected.notes.json');assert 'not elaborated proof dependencies' in note['graph_delta'] and 'four actual producer parents' in note['graph_delta'] and 'incomplete scanner signals' in note['graph_delta']
assert note['kernel_dependency_evidence']['RAW_sha256']==info(B/'independent-math84/kernel-dependency-summary84.json')['RAW_sha256']=='0234233d39e8c5f2101d80d5c43961522f70d700f100af3aea375e3cba22b04a'
assert scope['after']['cell']['RAW_sha256']==info(cell)['RAW_sha256'] and scope['after']['note']['RAW_sha256']==info(B/'integration.corrected.notes.json')['RAW_sha256']
checks=[]
for label in ['refresh-reference-graph','correct84-graph','publication','frontier','semantic','site-check']:
 p=S/(label+'.receipt.json');q=load(p);assert q['exit_code']==0 and q['terminal_closed']
 for stream in ['stdout','stderr']:assert info(q[stream]['path'])['RAW_sha256']==q[stream]['RAW_sha256']
 if label=='correct84-graph':assert q['command'][-1]=='ASTIS-SW-PBPS-actual-outer-bounded-l2-continuity'
 checks.append(info(p))
for e in prior['source_theorem_publication_tests_toolchain_ledger_unchanged']:assert info(e['path'])['RAW_sha256']==e['RAW_sha256']
for e in prior['exact_two_one_token_helper_corrections']+[prior['handoff_pointer_only']]:assert info(e['path'])==e
for e in prior['original_retained_receipts']+prior['new_correction_receipts']:assert info(e['receipt']['path'] if 'receipt' in e else e['path'])['RAW_sha256']==(e['receipt']['RAW_sha256'] if 'receipt' in e else e['RAW_sha256'])
assert info(B/'integration.notes.json')['RAW_sha256']==note['prior_integration_note']['RAW_sha256']
sys.path[:0]=[str(R/'tools'),str(R/'website/scripts')];import astis_site,publication_reader
src=astis_site.source_digest();assert src==prior['source_digest']==note['lean_source_digest']==load(R/'.astis/site-lean-gate.json')['source_digest']
graph=load(R/'_site/data/underlying-lean-graph.json');gd=publication_reader.graph_input_digest();assert gd==graph['publication_inputs_sha256']==note['publication_inputs_sha256']
assert info(R/'_site/data/underlying-lean-graph.json')['RAW_sha256']==note['current_graph']['RAW_sha256']==scope['after']['graph']['RAW_sha256']
assert graph['reference_contract']=='Name-scanned references are incomplete signals, not elaborated proof dependencies.'
target='decl:AutoSamplingTheory.ExampleCases.ProximalBPS.ActualOuterBoundedL2Continuity.actual_outer_bounded_l2_continuity';edges=[e for e in graph['edges'] if e.get('target')==target];kernel=load(B/'independent-math84/kernel-dependency-summary84.json');expected=set(kernel['external_ASTIS_dependencies']);actual={e['source'][5:] for e in edges if e['source'].startswith('decl:')}
assert len(expected)==4 and len(expected-actual)==2 and actual-expected=={'AutoSamplingTheory.TechnicalLemmas.Geometry.LogConcavity.LogConcaveOn.prod'}
page=R/'_site/example-cases/samplewiki/companions/proximal-bouncy-particle.html';assert info(page)==prior['page'] and info(page)['RAW_sha256']==load(B/'integration84/offline-reader.json')['page_RAW_sha256']
for p,h in load(R/'runs/20261007-companion-priority/pbps-outer-bounded-l2-preread84/pre-fetch84.workspace-RAW.json')['tracked_modified'].items():assert info(p)['RAW_sha256']==h
from astis_advance import current_advances
states=current_advances();assert states['ASTIS-SA-20261011-PBPSActualOuterBoundedL2Continuity']['state']=='VERIFIED';assert {k for k,v in states.items() if v['state']=='STABILIZING'}=={'ASTIS-SA-20261005-SPHMCImplementedPhaseKernel'}
freeze=[cell,B/'integration.corrected.notes.json',B/'integration.notes.json',S/'scope-correction.json',S/'cell.before.json',S/'note.before.json',B/'commit_integration84.py',B/'run_gates84.py',B/'fix_integration_admission84.py',B/'scope_graph_evidence84.py',R/'docs/companion-papers-handoff.md',R/'website/scripts/underlying_lean_graph.py',R/'website/scripts/publication_reader.py',R/'tools/astis_site.py',R/'.astis/site-lean-gate.json',R/'_site/data/underlying-lean-graph.json',page,B/'independent-math84/kernel-dependency-summary84.json',B/'exact-commit-verification84/verified.json',B/'integration84/final-admin.json',B/'integration84/offline-reader.json',B/'integration84/cell.before-final-admin84.snapshot.json',R/'runs/20261007-companion-priority/pbps-outer-bounded-l2-preread84/pre-fetch84.workspace-RAW.json']
freeze.extend([B/'commit_admission_correction84.py', B/'push_and_pr84_corrected.py'])
for e in prior['source_theorem_publication_tests_toolchain_ledger_unchanged']:freeze.append(R/e['path'])
for e in prior['original_retained_receipts']:
 p=R/e['receipt']['path'];freeze.append(p)
 for stream in ['stdout','stderr']:
  q=Path(load(p)[stream]['path']);freeze.append(q if q.is_absolute() else R/q)
for directory in [B/'integration84/cell-admission-correction',S]:
 for p in directory.glob('*'):
  if p.is_file():freeze.append(p)
frozen={info(p)['path']:info(p) for p in freeze}
decision=dict(status='ACCEPTED_BOUNDED_CONTROL_PLANE_RESTORE_WITH_EXPLICIT_GRAPH_LIMITATION',reviewer_id='/root/exact_verify77',created_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),checked_published_integration_commit=C,checked_science_commit='dd3a23011b91569acbcd591ccd7b06301147d339',proposed_cell=info(cell),corrected_note=info(B/'integration.corrected.notes.json'),exact_cell_omission_confirmed=True,remote_cell_status='proved_locally',restored_status='independently_verified',restoration_reuses_already_completed_independent_verified_admission=True,one_token_cell_staging_path_and_graph_target_corrections_only=True,handoff_pointer_only=True,graph_scope_followup='Only visual_review wording changed after initial restore; exact source/test/publication/statement/BODY/HTML and ledger untouched. Current generated reference graph refreshed for new cell metadata digest; correct84 graph/publication/frontier/semantic/site checks terminal PASS.',kernel_parent_count=4,kernel_evidence=info(B/'independent-math84/kernel-dependency-summary84.json'),current_graph_evidence='Incomplete name-scanned reference signals and contribution coverage only. Actual83 and UnitExp appear; GibbsAugmentation and GaussianConditionalKernel signals are absent and LogConcaveOn.prod is a scanner false positive. Four elaborated dependency edges are NOT certified in this generated graph.',four_actual_edges_in_site_certified=False,retained_mismatch=info(O/'graph-evidence-mismatch.diagnosis.json'),gate_reuse='Native aggregate root9195/Tests9495/check and original sitebuild used unchanged Lean/source/publication/eight-step HTML. Current Lean source digest matches original native aggregate certificate; current reference graph digest matches refreshed cell metadata. No Lean/source reproof rerun.',fresh_metadata_graph_site_receipts=checks,prior_bounded_review=info(O/'bounded-repair-evidence.json'),root_jobs=9195,test_jobs=9495,Registry_count=533,all21collaborator_RAWs_preserved=True,no_new_math_or_source_promotion=True,no_new_VERIFIED_event=True,sole_existing_stabilization_lane_unchanged=True,production_shared_or_state_edits_by_reviewer=False,remaining=['Root must stage exact84 cell, exact helper corrections and honest correction notes/evidence, then commit/push normal.','Actual page/interactive visual acceptance, ExpositionSeal, main merge/PURIFIED/live/fullpaper/composition/Goal remain open.','General all-L2/invariance/Jensen-contraction/density/path-law/restart/Markov claims remain separate.'])
decision['verdict']='ACCEPT_BOUNDED_CONTROL_PLANE_RESTORE_WITH_EXPLICIT_GRAPH_LIMITATION'
decision['planned_commit_helper']=info(B/'commit_admission_correction84.py')
decision['planned_push_existing_PR_helper']=info(B/'push_and_pr84_corrected.py')
decision['helper_review']='Read-only inspection: initially empty index, explicit bounded owned paths plus correction evidence and lossless log archives, all21 collaborator RAW preservation, no production/shared Lean/ledger staging; ordinary non-force push and existing PR315 update. Not executed by reviewer; actual corrective commit/push remains root obligation.'
save('decision.json',decision)
save('closed-RAW-manifest.json',dict(status='CLOSED_RAW_NONCIRCULAR',reviewer_id='/root/exact_verify77',checked_integration_commit=C,frozen_current_inputs=list(frozen.values()),owned_artifacts=[info(p) for p in sorted(O.iterdir()) if p.is_file()],self_hash_intentionally_omitted=True,historical_original_generated_graph_RAW_recorded_not_claimed_current=True,original_wrong_target_receipts_and_prior_wording_preserved=True,no_source_or_math_reproof=True,no_state_mutation_by_reviewer=True))
for e in frozen.values():assert info(R/e['path'])==e
for name in ['decision.json','closed-RAW-manifest.json']:print(json.dumps(info(O/name)))
