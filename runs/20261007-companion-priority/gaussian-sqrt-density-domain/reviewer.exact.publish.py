from pathlib import Path
import json, hashlib, subprocess, sys, datetime
sys.path.insert(0,'tools')
import astis_advance as advance
R=Path('runs/20261007-companion-priority/gaussian-sqrt-density-domain')
C='1de412105042ebcfe147d50a3d1022fb0514faad'
A='ASTIS-SA-20261007-GaussianSqrtDensityDomain'
V='picard_commit_verifier_20261005'
def j(p):return json.loads(Path(p).read_text(encoding='utf-8'))
def sha(b):return hashlib.sha256(b).hexdigest()
def desc(p):
    b=Path(p).read_bytes()
    return {'path':str(p).replace('\\','/'),'raw_sha256':sha(b),'lf_sha256':sha(b.replace(b'\r\n',b'\n')),'bytes':len(b)}
def write(p,d):Path(p).write_bytes((json.dumps(d,ensure_ascii=False,indent=2)+'\n').encode())
assert subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()==C
checked=j(R/'reviewer.exact.checks.json');assert checked['verified_commit']==C and checked['verification_status']=='passed-scoped'
assert all(x['returncode']==0 for x in checked['gates']['results'])
state=advance.current_advances()[A];assert state['state']=='PROVED_LOCAL' and state['owner_id']!=V
targets=j(R/'proved-local.json')['lean_declarations'];assert set(targets)==set(state['publication_declarations'])
stabilizing=[a for a,x in advance.current_advances().items() if x['state']=='STABILIZING']
assert stabilizing==['ASTIS-SA-20261005-SPHMCImplementedPhaseKernel']
write(R/'reviewer.exact.advance.before.json',state)
ledger=Path('runs/substantive_advances.jsonl');before=ledger.read_bytes()
source=next(x for x in checked['checks'] if x['name']=='current_source_decoder_publication')
fake=next(x for x in checked['checks'] if x['name']=='fresh_fakeclosure')
git=next(x for x in checked['checks'] if x['name']=='current_Git_raw_LF_union')
math=next(x for x in checked['checks'] if x['name']=='whole_math_and_signature_freeze')
remaining=[
 'Only actual positive Gaussian relative density, C2/L2 sqrt/entropy/log-gradient/Dirichlet=Fisher/4 domain producers and true same-p standardized RGO for all positive measurable variable eta are certified.',
 'Gaussian LSI/T2, KL/RN/weak Sobolev representative adapters, FIRST4.6 W2, bias/fullLemma4.2/main/work/cost/composition remain OPEN.',
 'Current existing-root mandatory aggregate passes at this commit; packet32 new shared imports/Registry entry/Tests-root coverage, repository ProofSeal/site/graph integration, ExpositionSeal/postmerge purification/current remote CI/main/merge/live claims are separate pending stabilization. Registry remains475.'
]
receipt={
 'schema_version':1,'artifact_kind':'independent-exact-commit-VERIFIED',
 'verification_status':'passed-scoped','verified_commit':C,'advance_id':A,'verifier_id':V,
 'proving_owner':state['owner_id'],'lean_declarations':targets,'publication_declarations':targets,
 'owned_exact_checks':desc(R/'reviewer.exact.checks.json'),'gates':checked['gates'],
 'gate_summary':{'focused_jobs':3748,'existing_aggregate_root_jobs':9135,'existing_aggregate_Tests_jobs':9400,'publication_items':194,'semantic_audits':260,'repair_proposals':8,'frontier_cells':257,'process_memory':'PASS','contributor_affected_declarations':77,'contributor_changed_cells':73,'contributor_base':'84f0a9fc75d4babb7ceead2bfd4f98585789c857','new32_shared_imports_in_aggregate':False,'clean_build_claim':False},
 'Lean':'leanprover/lean4:v4.33.0','Mathlib':'db584cd6d46c92f209a44c0f1c829460d327499d',
 'source_audit':source,'fake_closure_scan':fake,'Git_checked_input_count':git['count'],
 'whole_mathematical_review':math,'reachable_axioms':checked['reachable_axioms'],
 'standard_axioms':['propext','Classical.choice','Quot.sound'],
 'scope':'Entire seven-private-helper generic actual Gaussian density producer, genuine true standardized RGO consumer and actual E0/L0 and eta2 y3 Tests. Same real R law/p/rho; exact quarter coefficient; no Gaussian-output/HMC substitution.',
 'independent_exact_diagnostics':{
     'signature_extraction':'Original checker substring assumed terminal newline occurs before the Lean proof delimiter. Preserved initial script/log; corrected distinct checker extracts exact declaration prefix before := by and appends sealed newline; both full sealed hashes match without source/signature edits.',
     'cell_lifecycle':'Original strict source footprint check found exactly status plus evidence.execution_boundary/proof_review/source_review on two cells, reflecting post-review PROVED_LOCAL. Typed administrative whitelist and exact current selected contexts/signatures/module bytes checked; no source or mathematical drift.',
     'initial_script':desc(R/'reviewer.exact.check.py'),'initial_log':desc(R/'reviewer.exact.check.log'),
     'second_script':desc(R/'reviewer.exact.check.attempt2.snapshot.py'),'second_log':desc(R/'reviewer.exact.check.attempt2.log'),
     'reconciled_script':desc(R/'reviewer.exact.check.reconciled.py'),'reconciled_log':desc(R/'reviewer.exact.check.reconciled.log')
 },
 'conceptual_mirror_audit':j(R/'proved-local.json')['conceptual_mirror_audit'],
 'ProofSeal':{'status':'focused-proof-accepted-scoped','repository_proof_seal_for_packet32':'pending sole serialized shared integration; existing aggregate is not new32 root coverage'},
 'remaining_boundary':remaining,'cells_modified_by_verifier':False,
 'authorization':'Own reviewer.exact.* / verified.json and sole independent VERIFIED ledger append only; no cells, source, proof, Tests, reader, shared roots, Registry, site or audits edits.',
 'sole_original_stabilization_lane':stabilizing,'read_lease':'CLOSED','compiler_lease':'CLOSED','write_lease':'CLOSED after sole transition and close receipt',
 'completed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()
}
write(R/'verified.json',receipt)
evidence={'verifier_id':V,'verified_commit':C,'gate':receipt['gate_summary'],
          'source_audit':source,'fake_closure_scan':{'reachable_modules':fake['reachable_modules'],'reachable_hits':[],'full_canonical_files':fake['full_canonical_files'],'full_hits':[],'receipt':desc(R/'reviewer.exact.checks.json')},
          'lean_declarations':targets,'publication_declarations':targets,'conceptual_mirror_audit':receipt['conceptual_mirror_audit'],'receipt':desc(R/'verified.json'),'truth_boundary':remaining}
advance.transition_advance(A,'VERIFIED',worker_id=V,modes=('independent-verification',),evidence=evidence)
after=ledger.read_bytes();assert after.startswith(before)
lines=after[len(before):].decode('utf-8').strip().splitlines();assert len(lines)==1
assert advance.current_advances()[A]['state']=='VERIFIED'
assert [a for a,x in advance.current_advances().items() if x['state']=='STABILIZING']==stabilizing
write(R/'reviewer.exact.transition.json',{'verified_commit':C,'verifier_id':V,'event':json.loads(lines[0]),'ledger_before_raw_sha256':sha(before),'ledger_after_raw_sha256':sha(after),'lines_appended':1,'cells_modified':False})
write(R/'reviewer.exact.lease.json',{'status':'CLOSED','checked_commit':C,'reviewer':V,'read_lease':'CLOSED','write_lease':'CLOSED','compiler_lease':'CLOSED','VERIFIED_transition_written':True,'receipt':desc(R/'verified.json'),'no_canonical_cells_or_math_changes':True})
print(json.dumps({'verified_commit':C,'VERIFIED':True,'receipt':desc(R/'verified.json'),'all_leases':'CLOSED','cells_modified':False},ensure_ascii=False))
