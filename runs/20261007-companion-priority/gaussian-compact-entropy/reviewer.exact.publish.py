from pathlib import Path
import json,hashlib,subprocess,sys,datetime,re
sys.path.insert(0,'tools')
import astis_advance as advance,astis_publication as pub
R=Path('runs/20261007-companion-priority/gaussian-compact-entropy');C='421496a5de7355830c0b4904ea10f33722ed3602';V='picard_commit_verifier_20261005'
def j(p):return json.loads(Path(p).read_text(encoding='utf-8'))
def sha(b):return hashlib.sha256(b).hexdigest()
def d(p):
 b=Path(p).read_bytes();return {'path':Path(p).as_posix(),'raw_sha256':sha(b),'lf_sha256':sha(b.replace(b'\r\n',b'\n')),'bytes':len(b)}
def put(p,x):
 assert not p.exists(),p
 p.write_bytes((json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode());return d(p)
assert subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()==C
check=j(R/'reviewer.exact.bindings.json');assert check['status']=='passed-scoped-exact-admission-ready' and check['checked_commit']==C
for row in check['exact_currentGit_inputs']:assert d(row['path'])['raw_sha256']==row['raw_sha256']
for row in check['fresh_gates']['results']:assert row['returncode']==0 and d(row['path'])['raw_sha256']==row['raw_sha256']
source=j(R/'source.0.review.json');packet=j(R/'source.0.reviewer-packet.json');dec=j(R/'anonymous-decoder/run.json')
assert pub.digest(packet['candidate_publication_context'])==source['review_context_sha256']
assert sha(packet['source']['original_text'].encode())==source['source_sha256']==packet['source']['text_sha256']
assert sha(packet['lean']['statement'].encode())==source['statement_sha256']==packet['lean']['statement_sha256']
assert source['source_excess']==0 and source['EXCESS']==[]
for row in dec['output_artifacts']:
 p=R/'anonymous-decoder'/Path(row['path']).name
 assert d(p)['raw_sha256']==row['raw_sha256'] and d(p)['lf_sha256']==row['lf_sha256']
initial=R/'anonymous-decoder/initial-lease.raw.snapshot.json';lease=j(R/'anonymous-decoder/lease.json')
assert d(initial)['raw_sha256']==lease['initial_lease_raw_sha256'] and d(initial)['lf_sha256']==lease['initial_lease_lf_sha256']
A=j(R/'claim.json')['advance_id'];local=j(R/'proved-local.json');decls=j(R/'publication-plan.json')['mathematical_declarations'];assert decls==local['lean_declarations']==local['publication_declarations']
states=advance.current_advances();assert states[A]['state']=='PROVED_LOCAL' and states[A]['owner_id']!=V
stabilizing=[k for k,v in states.items() if v['state']=='STABILIZING'];assert stabilizing==['ASTIS-SA-20261005-SPHMCImplementedPhaseKernel']
pub.check_advance(decls,reviewed=True)
snapshots=[]
for p in ['research-wiki/frontier-cells/ASTIS-SW-SPHMC-gaussian-compact-entropy.json','research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261007-GaussianCompactEntropy.json']:
 target=R/('reviewer.exact.before.'+Path(p).name+'.raw.snapshot');assert not target.exists();target.write_bytes(Path(p).read_bytes());snapshots.append(d(target))
diagnosis={'status':'CLOSED-verifier-script-repairs-only','checked_commit':C,'attempts':[{'script':d(R/'reviewer.exact.check.py'),'log':d(R/'reviewer.exact.check.log'),'typed_issue':'Verifier omitted the anticipated four cell claimed-to-proved_locally administrative paths. Canonical status and source88 snapshot were reconciled without changing source/math.'},{'script':d(R/'reviewer.exact.check.retry1.py'),'log':d(R/'reviewer.exact.check.retry1.log'),'typed_issue':'Verifier compared acyclic decoder basis reconstruction with final result including its additional decoder_run_sha256. Exact shared payload unchanged; singleton appended run-hash verified independently.'},{'script':d(R/'reviewer.exact.check.retry2.py'),'log':d(R/'reviewer.exact.check.retry2.log'),'status':'passed-scoped'}],'canonical_mutations':False,'repeated_same_route':False,'new_mathematical_credit':False}
diagnostic=put(R/'reviewer.exact.script-reconciliation.json',diagnosis)
scope_log=(R/'reviewer.exact.contributor.log').read_text(encoding='utf-8');m=re.search(r'affected declarations=(\d+); changed cells=(\d+)',scope_log);assert m
gate={'status':'PASS','checked_commit':C,'fresh_focused_jobs':3162,'fresh_aggregate_jobs':check['aggregate_jobs'],'metadata_counts':{'publication':199,'semantic_audits':265,'repair_proposals':8,'frontier_cells':262,'contributor_affected_declarations':int(m[1]),'contributor_changed_cells':int(m[2])},'contributor_base':subprocess.check_output(['git','rev-parse','origin/main'],text=True).strip(),'foreground_serialized_commands':check['fresh_gates'],'source_publication_reviewed_true':True,'root_scope':'Previous integrated34/35 shared roots and Registry479; focused actual36 production/Test independently exercised. No36 shared import/Registry/repository ProofSeal credit.'}
source_evidence={'audit_id':'ASTIS-RT-20261007-GaussianCompactEntropy','state':'accepted','reviewed':True,'source_receipt':d(R/'source.0.review.json'),'source_packet':d(R/'source.0.reviewer-packet.json'),'source_review_run_sha256':check['source_review_run_sha256'],'publication_binding_sha256':check['source_binding_sha256'],'source_review_context_sha256':source['review_context_sha256'],'decoder_run_sha256':check['decoder_run_sha256'],'decoder_packet_sha256':check['decoder_packet_sha256'],'source_actor':source['reviewer'],'decoder_actor':dec['actor'],'seven_slots':list(source['semantic_slots']),'source_inputs':88,'source_excess':0,'administrative_reconciliation':check['source_admin_reconciliation'],'historical_OPEN_manifests':'Immutable snapshots remain historical; active decoder/source/wholemath leases independently checked CLOSED.'}
receipt={'schema_version':4,'verification_status':'passed-scoped','verified_commit':C,'checked_working_head':C,'verifier_id':V,'role':'independent_verifier','advance_id':A,'proving_owner':states[A]['owner_id'],'lean_declarations':decls,'publication_declarations':decls,'result_kind':local['result_kind'],'gate':gate,'source_audit':source_evidence,'fake_closure_scan':check['fake_closure_scan'],'named_standard_axioms':check['named_standard_axioms'],'exact_raw_LF_Git_evidence':d(R/'reviewer.exact.bindings.json'),'exact_Git_input_count':352,'whole_mathematical_review_reused':check['whole_math_review'],'whole_math_run_sha256':check['whole_math_run_sha256'],'wholemath_binding_count':36,'original_freeze_count':22,'parent_API_regions':check['parent_API_regions'],'proof_scope':{'private_providers':3,'authored_core':'Actual same Bool-count signed sqrt-normalized sums, three Gaussian/allN-count L1 domains and successor mass/logenergy/derivative-square/homogeneous entropy limits. Compact C2 only; zero mass and N0 included.','same_actual_ASTIS_parent':'AutoSamplingTheory.TechnicalLemmas.Probability.BalancedRademacherCLT.balanced_count_sum_tendsto_gaussian','independent_stress_reused':'Exact immutable nonzero-N0 probe x*smoothUnitCutoff x yields derivative-square integral1, demonstrating N0 energy need not vanish. First failed API experiment retained and excluded.','current_Test_linter_warnings':'Two unnecessarySimpa warnings retained; no additional axiom or mathematical gap.'},'statement_seal':{'bytes':1581,'raw_LF_sha256':'d0adc2bfa9a83b8389706c10b31d10c64b5f7b6dba8c7454cd370a738ac7100e'},'source_topology_scope':'Prior independently reviewed 65-node/163-edge/2OR/114-region/1195-line authored compact-core topology reused unchanged; full source/paper not discharged.','conceptual_mirror_audit':local['conceptual_mirror_audit'],'remaining_boundary':check['remaining_boundary'],'repository_ProofSeal':'pending serialized36 shared integration; exact local mathematical/source VERIFIED only','before_raw_snapshots':snapshots,'verifier_script_diagnostics':diagnostic,'leases':{'read':'CLOSED','write':'CLOSED','compiler':'CLOSED','Python':'CLOSED'},'completed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
saved=put(R/'verified.json',receipt)
evidence={'gate':gate,'verifier_id':V,'verified_commit':C,'source_audit':source_evidence,'fake_closure_scan':check['fake_closure_scan'],'lean_declarations':decls,'publication_declarations':decls,'conceptual_mirror_audit':local['conceptual_mirror_audit'],'verification_receipt':saved,'remaining_boundary':check['remaining_boundary'],'independent_verifier_role':True}
advance.transition_advance(A,'VERIFIED',worker_id=V,evidence=evidence)
assert advance.current_advances()[A]['state']=='VERIFIED'
assert [k for k,v in advance.current_advances().items() if v['state']=='STABILIZING']==stabilizing
done=put(R/'reviewer.exact.transition.json',{'status':'CLOSED','advance_id':A,'verified_commit':C,'transition':'PROVED_LOCAL -> VERIFIED','verifier_id':V,'verification_receipt':saved,'cell_projection_left_to_root':True,'canonical_mutations':False,'sole_STABILIZING_preserved':stabilizing,'leases':{'read':'CLOSED','write':'CLOSED','compiler':'CLOSED','Python':'CLOSED'}})
leasepath=R/'reviewer.exact.lease.json';before=R/'reviewer.exact.lease.open.raw.snapshot.json';assert not before.exists();before.write_bytes(leasepath.read_bytes())
leasepath.write_bytes((json.dumps({'status':'CLOSED','verifier_id':V,'verified_commit':C,'read':'CLOSED','write':'CLOSED','compiler':'CLOSED','Python':'CLOSED','initial_manifest':d(before),'transition_receipt':done},ensure_ascii=False,indent=2)+'\n').encode())
print(json.dumps({'status':'VERIFIED','verified_commit':C,'receipt':saved,'all_leases':'CLOSED','canonical_cells_mutated':False},ensure_ascii=False))
