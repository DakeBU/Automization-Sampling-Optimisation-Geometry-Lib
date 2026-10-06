import pathlib,json,sys,hashlib,subprocess,datetime
sys.path.insert(0,'tools')
import astis_advance as adv
R=pathlib.Path('runs/20261006-companion-priority/smoothed-hessian-lower')
C='d8f540f5b4409387b839f7ccfb50fd3297af4c70';V='picard_commit_verifier_20261005'
def J(p):return json.loads(pathlib.Path(p).read_text(encoding='utf8'))
def F(p):
 p=pathlib.Path(p);b=p.read_bytes()
 return {'path':p.as_posix(),'raw_sha256':hashlib.sha256(b).hexdigest(),'lf_sha256':hashlib.sha256(b.replace(b'\r\n',b'\n').replace(b'\r',b'\n')).hexdigest(),'bytes':len(b)}
def W(p,x):
 pathlib.Path(p).write_bytes((json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode('utf8'))
assert subprocess.check_output(['git','rev-parse','HEAD']).decode().strip()==C
e=J(R/'exact-admission-reconciliation.json');m=J(R/'math-review.json');pl=J(R/'proved-local.json');c=J(R/'claim.json')
assert e['status']=='passed-scoped' and e['verified_candidate_commit']==C
assert e['stable_count']==54 and e['current_source_input_union_count']==56 and e['committed_raw_run_artifact_count']==283
assert e['source_scan_count']==59 and e['fake_closure_hits']==[]
assert pl['lean_declarations']==pl['publication_declarations']==c['declarations']
state=adv.current_advances();assert state[c['advance_id']]['state']=='PROVED_LOCAL'
lane=[k for k,z in state.items()if z['state']=='STABILIZING']
assert lane==['ASTIS-SA-20261005-SPHMCImplementedPhaseKernel']
cells=[]
for cid in c['cells']:
 p=pathlib.Path('research-wiki/frontier-cells')/(cid+'.json')
 z=J(p);assert z['status']=='proved_locally'
 s=R/(cid+'.exact-before-verified.raw.snapshot.json');assert not s.exists()
 s.write_bytes(p.read_bytes());cells.append((p,z,s))
gate={'scope':'Independent exact focused Lean/source admission; repository ProofSeal and shared integration remain pending.',
 'focused':{'command':'ELAN_TOOLCHAIN=leanprover/lean4:v4.33.0 LEAN_NUM_THREADS=2 lake build Tests.SmoothedHessianBounds','result':'PASS3877; cached dependencies; all6 actual axiom prints standard3 only','check':e['checks'][0]},
 'prior_fresh_direct':m['fresh_direct_elaboration'],'reuse_condition':'Both complete production modules/Test, invoked stable parent/pinned Mathlib and original raw logs remain exactly unchanged; successful actual sharp-quadratic stress retained.',
 'publication':{'result':'PASS185 source items; --base origin/main','check':e['checks'][1]},
 'semantic':{'result':'PASS245 audits/8 repairs','check':e['checks'][2]},
 'frontier':{'result':'PASS248cells','check':e['checks'][3]},
 'contributor':{'result':'PASS affected68 declarations/64changed cells; terminal affected-metadata-only classifier is retained honestly, independently checked actual code/consumer and source gates supply Lean proof evidence','check':e['checks'][4]},
 'reviewed_publication_admission':{'reviewed':True,'declarations':c['declarations'],'result':'PASS independently invoked, then schema4 transition revalidates same exact set'}}
out={'schema_version':1,'kind':'independent-exact-commit-verification','advance_id':c['advance_id'],'cell_ids':c['cells'],
 'verification_status':'passed-scoped','verified_commit':C,'verifier_id':V,'worker_id':V,'role':'independent_verifier',
 'independent_from_formalizer':True,'formalizer':'companion_root_20261005',
 'lean_declarations':pl['lean_declarations'],'publication_declarations':pl['publication_declarations'],'lean_files':pl['lean_files'],
 'gate':gate,'source_audit':e['accepted_source_bindings'],
 'fake_closure_scan':{'method':'fresh canonical astis.strip_lean_comments_and_strings / FORBIDDEN_REGEX over actual import-reachable ASTIS/Test modules','file_count':59,'hits':[],'original_full_inventory':F(R/'independent-fake-closure-scan.json'),'exact_rescan':F(R/'exact-admission-reconciliation.json')},
 'standard_axioms':e['standard_axioms'],'conceptual_mirror_audit':pl['conceptual_mirror_audit'],
 'pinned_toolchain':e['toolchain'],'pinned_mathlib':e['mathlib'],
 'math_review':F(R/'math-review.json'),'exact_admission_reconciliation':F(R/'exact-admission-reconciliation.json'),
 'immutable_evidence':{'stable_math_inputs':54,'context_snapshots':4,'current_source_input_union':56,'committed_raw_run_artifacts':283,'Git_canonical_inputs':len(e['git_canonical_inputs']),'parent_modules':12,'pinned_Mathlib_API_files':12,
 'two_before_verified_cell_snapshots':[F(s)for p,z,s in cells],'original_freeze':F(R/'math-freeze.json'),
 'independent_math_metadata_reconciliation':F(R/'independent-math-metadata-reconciliation.json'),
 'source_provenance_lifecycle_reconciliation':F(R/'source.provenance-lifecycle-reconciliation.json'),
 'exact_validator_script':F(R/'independent-exact-admission.py'),'exact_validator_log':F(R/'independent-exact-admission.attempt2.log'),
 'validator_adapter_diagnostic':F(R/'independent-exact-admission.attempt1.diagnostic.txt'),
 'raw_LF_Git_note':'Canonical working-tree CRLF distinguished from Git LF; all283 immutable committed run artifacts match Git exact raw bytes, no JSON reserialization or log normalization.'},
 'mathematical_scope':{'complete_new_modules':[57,148],'public_declarations':2,'private_declarations':0,'all_local_helpers_read':True,'focused_Test_lines':113,'reader_steps':[6,7],
 'genuine_canonical_variance':True,'genuine_actual_R_y_prob_vector_L2_partitions':True,'true_U_equals_V_eta_plus_logZ':True,
 'source_beta1_alpha_kappainv_eta_cap':True,'Hessian_constants':['1/(kappa+eta)','1/(1+eta)'],'true_global_gradient_Lipschitz_constant':1,
 'independent_sharp_quadratic_stress':'lam1/2 kappa2 eta1 constant7: genuine posterior covariance2/3, direction2=8/3, exact source Hessian1/3; standard3 only.',
 'nonquadratic_Test':'eta1/2 bounds2/5..2/3; eta1 bounds1/3..1/2; genuine finite-dimension0 constant7 probability/posteriorL2/covariance0.',
 'no_moment_covariance_PI_normalizer_certificate_premise_on_source_anchor':True,'no_duplicated_old_parent_completion_credit':True},
 'statement_seals':e['signature_seals'],'source_topology':e['source_topology'],
 'coverage':{'source_graph_inventory':184,'source_nodes':14,'source_use_edges':15,'source_gaps_retained':5,
 'reviewed_graph_path':'runs/20261006-companion-priority/smoothed-hessian-lower/preproof/source-proof-graph.revised.json',
 'discharged_here':'Scoped analytic Lemma4.1 sufficient PI-to-isotropic-linear-covariance route and actual internally produced calculus/normalization/moments/Hessian-to-Lip interfaces.',
 'not_discharged':'Full anisotropic Brascamp-Lieb, full cited textbook reverse-Cramer-Rao proof, higher smoothness, sampler/main/cost/composition.',
 'not_a_website_expansion_or_full_section_completion':True},
 'proof_seal_scope':{'focused_exact_proof_and_source_admission':'accepted-scoped','repository_ProofSeal':'pending serialized actual aggregate/root Tests check and fixed integration commit','purification_ExpositionSeal':'separate pending admission'},
 'reviewer_exposure':{'whole_math_review_performed_by_this_actor_before_decoder_source_verdicts':True,'preproof_primary_first_topology_performed_by_this_actor':True,
 'exact_phase_reads_distinct_source_and_decoder_receipts_for_admission':True,'historical_total_blindness_claim':False,'future_proof_prototypes_or_source_preread_content_read':False},
 'out_of_scope':{'untracked_future_preread':e['excluded_untracked_future_artifact'],'packet24_commit_admin':e['out_of_packet25_commit_changes']},
 'remaining_boundary':e['remaining_boundary'],'compiler_sessions_closed':True,'compiler_lease':'CLOSED',
 'write_lease':'CLOSED after this isolated independent transition/cell publication; root sole stabilization owner remains unchanged.',
 'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
vp=R/'verified.json';assert not vp.exists();W(vp,out)
ev={'verifier_id':V,'role':'independent_verifier','verification_status':'passed-scoped','verified_commit':C,
 'gate':gate,'source_audit':e['accepted_source_bindings'],'fake_closure_scan':out['fake_closure_scan'],
 'lean_declarations':pl['lean_declarations'],'publication_declarations':pl['publication_declarations'],
 'conceptual_mirror_audit':pl['conceptual_mirror_audit'],'truth_boundary':pl['truth_boundary'],
 'receipt':F(vp),'proof_seal_scope':out['proof_seal_scope']}
adv.transition_advance(c['advance_id'],'VERIFIED',worker_id=V,modes=['independent-exact-verification'],evidence=ev)
for p,z,s in cells:
 z['status']='independently_verified'
 z.setdefault('evidence',{})['independent_verification']=vp.as_posix()
 z['evidence']['independent_verification_details']={'verification_status':'passed-scoped','verifier_id':V,'verified_commit':C,'receipt':F(vp),
  'source_audit_ids':[x['audit_id']for x in e['accepted_source_bindings']],'focused':'PASS3877','reachable_fake_closure_files':59,
  'source_admission':'accepted equivalent-after-elaboration both whole modules; raw/LF/Git snapshots verified',
  'repository_ProofSeal':'pending root serial integration','no_main_completion_claim':True}
 W(p,z)
assert adv.current_advances()[c['advance_id']]['state']=='VERIFIED'
assert lane==[k for k,z in adv.current_advances().items()if z['state']=='STABILIZING']
r=subprocess.run([sys.executable,'tools/astis_frontier_cells.py','check'],stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
log=R/'independent-post-verified-frontier.log';log.write_bytes(r.stdout);assert r.returncode==0,r.stdout.decode()
W(R/'independent-verification-closed.json',{'verified_commit':C,'advance_id':c['advance_id'],'state':'VERIFIED','verifier_id':V,'verified_receipt':F(vp),
 'two_cells':[{'path':p.as_posix(),'status':J(p)['status'],'independent_verification_type':type(J(p)['evidence']['independent_verification']).__name__}for p,z,s in cells],
 'post_frontier':F(log),'exit_code':0,'sole_stabilization_owner_unchanged':lane,'compiler_sessions':'CLOSED','write_lease':'CLOSED',
 'completed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()})
print(json.dumps({'verified_commit':C,'state':'VERIFIED','receipt':F(vp),'cells':c['cells'],'compiler_lease':'CLOSED','write_lease':'CLOSED','post_frontier':r.stdout.decode().strip()},ensure_ascii=False,indent=2))
