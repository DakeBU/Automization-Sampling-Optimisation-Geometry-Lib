from pathlib import Path
import json, hashlib, sys, subprocess, datetime
sys.path.insert(0,'tools')
import astis_advance as advance, astis_publication as pub
R=Path('runs/20261007-companion-priority/balanced-rademacher-clt')
R34=Path('runs/20261007-companion-priority/bernoulli-function-lsi')
C='4d9e71a6b835b54453a5cfd2d132f9a51f66f69c';C34='6d5df34cdb124e28022f16f566ff549145eb7e65';V='picard_commit_verifier_20261005'
def j(p):return json.loads(Path(p).read_text(encoding='utf-8'))
def sha(b):return hashlib.sha256(b).hexdigest()
def d(p):
 b=Path(p).read_bytes();return {'path':Path(p).as_posix(),'raw_sha256':sha(b),'lf_sha256':sha(b.replace(b'\r\n',b'\n')),'bytes':len(b)}
def put(p,obj):
 assert not p.exists(),p
 p.write_bytes((json.dumps(obj,ensure_ascii=False,indent=2)+'\n').encode());return d(p)
assert subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()==C
check=j(R/'reviewer.exact.bindings.json');assert check['status']=='passed-scoped-exact-admission-ready' and check['checked_working_head']==C
assert d(R/'reviewer.exact.bindings.json')['raw_sha256']=='965db59cb8d18fb6adfa784222ecc2c1b101124a1deff89afa684a97099364b5'
for row in check['exact_currentGit_inputs']:assert d(row['path'])['raw_sha256']==row['raw_sha256']
for row in check['fresh_gates']['results']:assert row['returncode']==0 and d(row['path'])['raw_sha256']==row['raw_sha256']
before=advance.current_advances();stabilizing=[k for k,v in before.items() if v['state']=='STABILIZING'];assert stabilizing==['ASTIS-SA-20261005-SPHMCImplementedPhaseKernel']
transition_rows=[]
for run,commit,number in [(R34,C34,'34'),(R,C,'35')]:
 claim=j(run/'claim.json');plan=j(run/'publication-plan.json');A=claim['advance_id'];decls=plan['mathematical_declarations'];local=j(run/'proved-local.json')
 assert set(decls)==set(local['lean_declarations'])==set(local['publication_declarations'])
 assert before[A]['state']=='PROVED_LOCAL' and before[A]['owner_id']!=V
 pub.check_advance(decls,reviewed=True)
 source=[x for x in check['current3_source_bindings'] if x['declaration'] in decls]
 assert len(source)==len(decls) and all(x['reviewed'] for x in source)
 reused34={'prior_ready':d(R34/'reviewer.exact.overlay2.ready.json'),'original_failed_admission':d(R34/'reviewer.exact.failed-admission.json'),'scope':'Original a83 proof/source/focused/direct six-standard-axiom checks and repaired6d5 proof retained. All468 committed ready inputs independently rechecked unchanged against actual4d9. Earlier unreviewed35 live-global failure is historical; real current whole-workspace gates now passed.'}
 actual35={'whole_math_review':d(R/'whole-proof-review/math.review.json'),'whole_math_run_sha256':check['35_math_run_sha256'],'frozen14_all_unchanged':True,'mathematical_inputs_checked':35,'private_providers':14,'actual_parent_API_regions':check['35_parent_API_regions_checked'],'source_inputs_checked':77,'exact_source_admin_diff':check['35_exact_admin_reconciliation'],'evidence_list_string_overlay':check['35_evidence_representation_overlay'],'blind_decoder_run_sha256':check['35_sourceblind_decoder_run_sha256'],'topology_review':check['35_independent_topology'],'topology_coverage':check['35_topology_scope'],'exact573byte_sealed_signature_sha256':'271595fa838cf28466cf90591d2c6aaa1024b42a1af73d85eee25cfc32e04777'}
 gates={'status':'PASS','checked_working_head':C,'mandatory_astis':d(R/'reviewer.exact.aggregate.log'),'aggregate_jobs':{'root':9138,'Tests':9406},'focused35':d(R/'reviewer.exact.focused.log'),'direct35':d(R/'reviewer.exact.direct-axioms.log'),'metadata':check['fresh_gates'],'publication_items':198,'semantic_audits':264,'repair_proposals':8,'frontier_cells':261,'contributor_affected_declarations':81,'contributor_changed_cells':77,'contributor_base':'84f0a9fc75d4babb7ceead2bfd4f98585789c857','old34_focused_reused_by_unchanged_hashes':number=='34','source_binding_reviewed_true':True,'root_imports_scope':'Aggregate still uses prior33 root/Test imports and Registry476. New34/35 declarations are independently exercised by focused Tests; shared integration is not asserted.'}
 remaining=check['remaining_boundary']
 receipt={'schema_version':4,'verification_status':'passed-scoped','verified_commit':commit,'checked_working_head':C,'advance_id':A,'verifier_id':V,'role':'independent_verifier','proving_owner':before[A]['owner_id'],'lean_declarations':decls,'publication_declarations':decls,'result_kind':local['result_kind'],'gate':gates,'source_audit':source,'fake_closure_scan':check['fake_closure_scan'],'named_standard_axioms':check['named_axioms'],'complete_independent_raw_LF_Git_evidence':d(R/'reviewer.exact.bindings.json'),'exact_combined_Git_input_count':check['exact_currentGit_input_count'],'proof_scope':reused34 if number=='34' else actual35,'conceptual_mirror_audit':local['conceptual_mirror_audit'],'remaining_boundary':remaining,'repository_ProofSeal':'pending serialized shared integration; this is exact local mathematical/source VERIFIED admission only','leases':{'read':'CLOSED','write':'CLOSED','compiler':'CLOSED','Python':'CLOSED'},'completed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
 saved=put(run/'verified.json',receipt)
 evidence={'gate':gates,'verifier_id':V,'verified_commit':commit,'checked_working_head':C,'source_audit':source,'fake_closure_scan':check['fake_closure_scan'],'lean_declarations':decls,'publication_declarations':decls,'conceptual_mirror_audit':local['conceptual_mirror_audit'],'verification_receipt':saved,'remaining_boundary':remaining,'independent_verifier_role':True}
 advance.transition_advance(A,'VERIFIED',worker_id=V,evidence=evidence)
 assert advance.current_advances()[A]['state']=='VERIFIED'
 transition_rows.append({'advance_id':A,'verified_commit':commit,'checked_working_head':C,'verifier_id':V,'receipt':saved,'transition':'PROVED_LOCAL -> VERIFIED','cells_mutated':False})
assert [k for k,v in advance.current_advances().items() if v['state']=='STABILIZING']==stabilizing
done=put(R/'reviewer.exact.transitions.json',{'status':'CLOSED','independent_transitions':transition_rows,'sole_STABILIZING_preserved':stabilizing,'canonical_cell_projection_left_to_root':True,'production_shared_site_registry_mutations':False,'leases':{'read':'CLOSED','write':'CLOSED','compiler':'CLOSED','Python':'CLOSED'}})
for path,commit in [(R/'reviewer.exact.lease.json',C),(R34/'reviewer.exact.final.lease.json',C34)]:
 obj={'status':'CLOSED','verifier_id':V,'verified_commit':commit,'checked_working_head':C,'read':'CLOSED','write':'CLOSED','compiler':'CLOSED','Python':'CLOSED','actual_transitions':done,'completed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
 if path.exists():path.write_bytes((json.dumps(obj,ensure_ascii=False,indent=2)+'\n').encode())
 else:put(path,obj)
print(json.dumps({'transitions':transition_rows,'all_leases':'CLOSED','sole_STABILIZING_preserved':stabilizing},ensure_ascii=False))
