from pathlib import Path
import json, hashlib, sys, subprocess, datetime

sys.path.insert(0,'tools')
import astis_advance as advance
R=Path('runs/20261007-companion-priority/smoothed-score-posterior')
C='f91b82a2920b40299e57ccb821583a91e0a3e188'
A='ASTIS-SA-20261007-SmoothedScorePosterior'
V='picard_commit_verifier_20261005'
def j(p):return json.loads(Path(p).read_text(encoding='utf-8'))
def sha(b):return hashlib.sha256(b).hexdigest()
def dump(p,x):Path(p).write_bytes((json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode())
def descriptor(p):
    b=Path(p).read_bytes()
    return {'path':str(p).replace('\\','/'),'raw_sha256':sha(b),'lf_sha256':sha(b.replace(b'\r\n',b'\n')),'bytes':len(b)}
assert subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()==C
checked=j(R/'reviewer.exact.retry.checks.json')
assert checked['verified_commit']==C and checked['verification_status']=='passed-scoped'
assert all(x['returncode']==0 for x in checked['gates']['results'])
states=advance.current_advances();item=states[A]
assert item['state']=='PROVED_LOCAL' and item['owner_id']!=V
stabilizing_before=[x for x,s in states.items() if s['state']=='STABILIZING']
assert stabilizing_before==['ASTIS-SA-20261005-SPHMCImplementedPhaseKernel'],stabilizing_before
targets=j(R/'proved-local.json')['lean_declarations']
assert set(targets)==set(item['publication_declarations'])
dump(R/'reviewer.exact.retry.advance.before.json',item)
ledger=Path('runs/substantive_advances.jsonl');ledger_before=ledger.read_bytes()
source=next(x for x in checked['checks'] if x['name']=='current_source_admission')
fake=next(x for x in checked['checks'] if x['name']=='reachable_fakeclosure')
focus=next(x for x in checked['checks'] if x['name']=='focused_evidence_reuse')
receipt={
 'schema_version':1,'artifact_kind':'independent-exact-commit-VERIFIED',
 'verification_status':'passed-scoped','verified_commit':C,'verifier_id':V,
 'advance_id':A,'proving_worker':item['owner_id'],
 'lean_declarations':targets,'publication_declarations':targets,
 'checked_inputs':descriptor(R/'reviewer.exact.retry.checks.json'),
 'gate':checked['gates'],
 'gate_summary':{'mandatory_foreground_astis_check':'PASS','root_jobs':9133,'Tests_jobs':9396,
                 'focused_jobs':3751,'focused_evidence':'Previous independent focused invocation and complete mathematical review reused only after exact unchanged four mathematical file raw/LF and parent proof byte checks; replay is not clean rebuild.',
                 'publication_items':192,'semantic_audits':258,'semantic_repair_proposals':8,
                 'frontier_cells':255,'contributor_declarations':75,'contributor_cells':71,
                 'contributor_base':'84f0a9fc75d4babb7ceead2bfd4f98585789c857'},
 'proof_scope':'Actual generic Gibbs gradient mean zero (no alpha<=beta, including E0) and genuine unnormalized smoothed potential score/posterior identity, with the same produced p/r/rho standardized chain for every eta>0.',
 'source_audit':source,'fake_closure_scan':fake,
 'reachable_axioms':focus['printed_axioms'],'standard_axioms':['propext','Classical.choice','Quot.sound'],
 'Lean':'leanprover/lean4:v4.33.0','Mathlib':'db584cd6d46c92f209a44c0f1c829460d327499d',
 'exact_git_input_count':1076,'original_mathematical_freeze_inputs':13,'actual_mathematical_parent_inputs':10,
 'whole_mathematical_review':descriptor(R/'whole-math-review.json'),
 'independent_math_reuse':'Complete separate whole-math proof review + current raw/LF freeze, actual Test endpoints, selected source contracts, compiler evidence and 39 reachable ASTIS/Test file fake scan. No duplicate proof credit.',
 'source_repair_overlay':descriptor(R/'source.repair.overlay-review.json'),
 'source_reconciliation':'Old BLOCKED source receipts and original verifier rejection preserved. Repaired seven-slot source reviews and current bindings accepted. This retry independently verifies exactly two canonical reuse-list metadata fields against unchanged independently source-reviewed lesson IDs; selected publication/source/decoder/whole-module contexts stay identical.',
 'conceptual_mirror_audit':j(R/'proved-local.json')['conceptual_mirror_audit'],
 'ProofSeal':{'status':'focused-proof-accepted-scoped','repository_scope':'Current existing repository ASTIS gate passes; new packet31 root imports/Registry/shared integration and repository ProofSeal await the sole root stabilization lane. No integration badge inferred from current aggregate.'},
 'remaining_boundary':[
     'Only generic meanzero, actual score/posterior identity and same p/r/rho chain at all eta>0. No Gaussian-output law/HMC substitution.',
     'FIRST4.6 W2, LSI/T2, bias, fullLemma4.2, algorithm/work/cost, main results of both papers and composition remain OPEN.',
     'Serialized packet31 shared imports/Registry/source correspondence/site/graph integration, repository ProofSeal, ExpositionSeal, rendered QA, current remote CI and merge remain separate. No PURIFIED/full-paper completion claim.'
 ],
 'canonical_cells_modified_by_verifier':False,
 'authorization':'Only own retry/verified receipts and one independent VERIFIED ledger append; no cell, production, Test, lesson, publication, audit, shared-root or site edits.',
 'original_stabilization_owner_preserved':stabilizing_before,
 'read_lease':'CLOSED','compiler_lease':'CLOSED','write_lease':'CLOSED after this sole transition and lease receipt',
 'verified_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()
}
dump(R/'verified.json',receipt)
evidence={
 'verifier_id':V,'verified_commit':C,'gate':receipt['gate_summary'],
 'source_audit':{'audits':source['reviews'],'current_reviewed_publication_admission':True,
                 'reviewer':'phase_source_reviewer_20261005','decoder':'/root/blind_statement_decoder_31',
                 'repair_and_metadata_reconciliation':descriptor(R/'reviewer.exact.retry.checks.json')},
 'fake_closure_scan':{'files':fake['files'],'hits':[],'receipt':descriptor(R/'reviewer.exact.retry.checks.json')},
 'lean_declarations':targets,'publication_declarations':targets,
 'conceptual_mirror_audit':receipt['conceptual_mirror_audit'],
 'receipt':descriptor(R/'verified.json'),'truth_boundary':receipt['remaining_boundary']
}
advance.transition_advance(A,'VERIFIED',worker_id=V,modes=('independent-verification',),evidence=evidence)
after=ledger.read_bytes();assert after.startswith(ledger_before)
new=after[len(ledger_before):].decode('utf-8').strip().splitlines();assert len(new)==1,len(new)
assert advance.current_advances()[A]['state']=='VERIFIED'
assert [x for x,s in advance.current_advances().items() if s['state']=='STABILIZING']==stabilizing_before
dump(R/'reviewer.exact.retry.transition.json',{'verified_commit':C,'verifier_id':V,'advance_id':A,'event':json.loads(new[0]),'ledger_before_raw_sha256':sha(ledger_before),'ledger_after_raw_sha256':sha(after),'appended_lines':1,'cells_modified':False})
dump(R/'reviewer.exact.retry.lease.json',{'status':'CLOSED','checked_commit':C,'reviewer':V,'read_lease':'CLOSED','write_lease':'CLOSED','compiler_lease':'CLOSED','VERIFIED_transition_written':True,'receipt':descriptor(R/'verified.json'),'original_failed_receipts_immutable':True,'no_cells_or_canonical_inputs_changed':True})
print(json.dumps({'verified_commit':C,'VERIFIED':True,'receipt':descriptor(R/'verified.json'),'read_write_compiler_leases':'CLOSED','cells_unchanged':True},ensure_ascii=False))
