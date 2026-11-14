from datetime import datetime,timezone
from pathlib import Path
import copy,json,sys
sys.dont_write_bytecode=True
from transition_common import *

assert git('rev-parse','HEAD').decode().strip()==HEAD
assert sha(AUDIT.read_bytes())==AUDIT_BEFORE
assert tracked_changes()==[]
old=readjson(AUDIT)
review=readjson(BASE/'phase3/independent_source_semantic_verdict.json')
runraw=(BASE/'phase3/review_run.json').read_bytes()
assert sha(runraw)=='c7524efc49a5193ba912807ecd56c4b2669a65a7b3f04e7af7079ccb10c289e1'
assert sha((BASE/'phase3/freeze_manifest.json').read_bytes())=='46fee361f6798fb8577c75479a563de2d30dbb2241059af624a29b3fbc4227a7'
pub3=PUBLIC/'fresh-source-reader-4e8f6a/phase3'
assert sha((pub3/'review_run.json').read_bytes())==sha(runraw)
assert sha((pub3/'freeze_manifest.json').read_bytes())==sha((BASE/'phase3/freeze_manifest.json').read_bytes())
public3=pub3.relative_to(ROOT).as_posix()
proposal=copy.deepcopy(old)
proposal['state']='accepted'
proposal['semantic_slots']=copy.deepcopy(review['semantic_slots'])
proposal['verdict']=review['verdict']
proposal['deltas']=[
 {'slot':'assumptions','severity':'informational','description':review['deltas'][0]['detail'],'evidence':public3+'/independent_source_semantic_verdict.json; frozen Phase3 explicit-elaboration review.'},
 {'slot':'scopes','severity':'informational','description':review['deltas'][1]['detail'],'evidence':public3+'/independent_source_semantic_verdict.json; full source/cost/TV/reader-runtime boundary remains separate.'}
]
proposal['source_review']={
 'state':'accepted','reviewer':ACTOR,'independent_from_formalizer':True,'independent_from_decoder':True,
 'reviewer_packet_sha256':'9f6bb17d32f9661f999fb0de7aa20c2ea15d2971ef78c9e30165d0bca0b80524',
 'reviewer_packet_raw_sha256':'0510cc019b9bcdb0b389b097a88108f3c7d0732d342174e27274dd43428f5168',
 'review_run_sha256':sha(runraw),'run_artifact':public3+'/review_run.json',
 'evidence':'Independent frozen Phase3 source/module/fresh-Lean/kernel/anonymous/both-determinant-sign/fake-closure/owned-STATIC-reader review at '+HEAD+'. Actual producer has one direct ASTIS parent; actual private Test has two; standard three axioms. Runtime/pixels/current canonical rootGate/site/Chrome acceptance is deferred. Actual scaffolding and preview transport failures plus root-interruption clarification remain preserved.',
 'checked_candidate_commit':HEAD,'publication_binding_sha256':old['publication_binding_sha256'],
 'scope':'Selected local first-order producer and actual same-O forward private consumer; STATIC source-review reader only.',
 'phase1_manifest_sha256':'cf4dd57dc05d19cb3ca6938032a7730d402aba6220a200ae4a3afe2aca721fac',
 'phase2_manifest_sha256':'85a0e1542ce93bd0f65203f136fbe8879f2f9be1713f0c05861ab3885af5971c',
 'phase3_manifest_sha256':'46fee361f6798fb8577c75479a563de2d30dbb2241059af624a29b3fbc4227a7',
 'fresh_compile_receipt':public3+'/fresh_compile_receipt.json',
 'kernel_application_receipt':public3+'/kernel_application_receipt.json',
 'fake_closure_receipt':public3+'/focused_fake_closure_receipt.json',
 'static_reader_receipt':public3+'/static_reader_review.json',
 'runtime_pixel_site_acceptance':False
}
proposal['successor_provenance']={
 'predecessor_canonical_audit_sha256':AUDIT_BEFORE,
 'predecessor_state':'blind-reconstructed','checked_candidate_commit':HEAD,
 'prepared_utc':datetime.now(timezone.utc).isoformat(),
 'prepared_by':ACTOR,'proof_owner':OWNER,
 'chronology':'Candidate '+HEAD+' contains the blind-reconstructed predecessor, not this accepted audit. Independent Phase1/2/3 reviews were subsequently frozen. This exact successor is preparation only until separately authorized canonical copy and one normal PROVED_LOCAL→VERIFIED event; that future event supplies actual transition time. No retroactive claim that checked commit contained accepted source review.',
 'normal_VERIFIED_API_already_run':False
}
for key in ['id','source','lean','reconstruction','repairs','publication_binding_sha256','publication_context']:
 assert proposal[key]==old[key],key
writejson(PREP/'proposed-accepted-audit.json',proposal)
(PREP/'canonical-blind-audit.before.json').write_bytes(AUDIT.read_bytes())
current=state();assert len(current)==285
own=current[ADVANCE];assert own['state']=='PROVED_LOCAL' and own['owner_id']==OWNER
assert own['publication_declarations']==[DECL]
assert ACTOR!=OWNER and ACTOR!=old['reconstruction']['decoder']
protected={}
for phase in ['phase1','phase2','phase3']:
 for p in (BASE/phase).rglob('*'):
  if p.is_file():protected[p.relative_to(ROOT).as_posix()]=sha(p.read_bytes())
publicroot=PUBLIC/'fresh-source-reader-4e8f6a'
for p in publicroot.rglob('*'):
 if p.is_file():protected[p.relative_to(ROOT).as_posix()]=sha(p.read_bytes())
extra=[
 BASE/'phase2-selective-input.json',
 PUBLIC/'full-anti-anchored-reviewer-packet.json',PUBLIC/'full-review-input-pins.json',
 ROOT/old['reconstruction']['run_artifact'],ROOT/old['reconstruction']['ambient_exposure_record'],
 ROOT/'research-wiki/semantic-roundtrip/registry.json'
]
for p in extra:
 assert p.is_file(),p
 protected[p.relative_to(ROOT).as_posix()]=sha(p.read_bytes())
frontiers=frontier_hashes();assert len(frontiers)==444,len(frontiers)
ledger_before=LEDGER.read_bytes();assert ledger_before.endswith(b'\n')
(PREP/'substantive_advances.before.jsonl').write_bytes(ledger_before)
baseline={
 'created_utc':datetime.now(timezone.utc).isoformat(),'checked_candidate_commit':HEAD,
 'actor':ACTOR,'proof_owner':OWNER,'own_advance_id':ADVANCE,
 'own_state':own,'sau_count':285,'foreign_sau_count':284,
 'foreign_sau_state_sha256':foreign_state_digest(current),
 'frontier_count':444,'frontier_hashes':frontiers,
 'discovery_sha256':sha(DISCOVERY.read_bytes()),
 'git_index_entries_sha256':sha(git('ls-files','-s','-z')),
 'git_tracked_diff_before':[],
 'tracked_source_config_README_models_policy':'All tracked paths protected by immutable HEAD+unchanged index+actual git diff; only own canonical audit and advance ledger may differ after apply. No need to hash 125k checkout/dependency paths.',
 'canonical_audit_before_sha256':AUDIT_BEFORE,
 'advance_ledger_before_sha256':sha(ledger_before),
 'advance_ledger_before_bytes':len(ledger_before),
 'advance_ledger_before_lines':len(ledger_before.splitlines()),
 'foreign_audits_and_protocol_sha256':foreign_audit_digest(rt.load_registry()),
 'frozen_review_and_provenance_files':protected,
 'allowed_tracked_mutation_paths':[AUDIT.relative_to(ROOT).as_posix(),LEDGER.relative_to(ROOT).as_posix()]
}
writejson(PREP/'preservation-baseline.json',baseline)
evidence={
 'verifier_id':ACTOR,'verified_commit':HEAD,'publication_declarations':[DECL],
 'gate':{'kind':'independent-source-module-freshLean-kernel-static-reader','review_manifest':public3+'/freeze_manifest.json','review_manifest_sha256':'46fee361f6798fb8577c75479a563de2d30dbb2241059af624a29b3fbc4227a7','fresh_compile_receipt':public3+'/fresh_compile_receipt.json','fresh_compile_receipt_sha256':sha((pub3/'fresh_compile_receipt.json').read_bytes()),'kernel_receipt':public3+'/kernel_application_receipt.json','kernel_receipt_sha256':sha((pub3/'kernel_application_receipt.json').read_bytes()),'runtime_or_root_site_acceptance':False},
 'source_audit':{'audit_id':AUDIT_ID,'proposed_successor_sha256':sha((PREP/'proposed-accepted-audit.json').read_bytes()),'predecessor_sha256':AUDIT_BEFORE,'reviewer':ACTOR,'verdict':review['verdict'],'review_run':public3+'/review_run.json','review_run_sha256':sha(runraw),'reviewer_packet_canonical_sha256':proposal['source_review']['reviewer_packet_sha256'],'reviewer_packet_raw_sha256':proposal['source_review']['reviewer_packet_raw_sha256'],'publication_binding_sha256':old['publication_binding_sha256'],'checked_tree_chronology':proposal['successor_provenance']['chronology'],'scope':proposal['source_review']['scope']},
 'fake_closure_scan':{'receipt':public3+'/focused_fake_closure_receipt.json','sha256':sha((pub3/'focused_fake_closure_receipt.json').read_bytes()),'kernel_axioms':['propext','Classical.choice','Quot.sound']},
 'conceptual_mirror_audit':own['latest_evidence']['conceptual_mirror_audit'],
 'preserved_proved_local_evidence_sha256':sha(canonical(own['latest_evidence'])),
 'truth_boundary':own['truth_boundary'],
 'lifecycle_boundary':'Only own normal PROVED_LOCAL→VERIFIED event after exact root authorization. No frontier/STAB/root/site/Chrome/remote/model/README/discovery/purification mutation or acceptance.'
}
advance._validate_transition_evidence('VERIFIED',evidence,schema_version=4)
writejson(PREP/'normal-verification-evidence.json',evidence)
preflight=prospective(proposal)
preflight['canonical_audit_written']=False;preflight['normal_transition_API_called']=False
preflight['checked_candidate_commit']=HEAD
writejson(PREP/'prospective-preflight.json',preflight)
assert_protected(baseline)
assert sha(AUDIT.read_bytes())==AUDIT_BEFORE
assert LEDGER.read_bytes()==ledger_before
print(json.dumps({'prepared_proposal_sha256':sha((PREP/'proposed-accepted-audit.json').read_bytes()),'baseline_sha256':sha((PREP/'preservation-baseline.json').read_bytes()),'normal_evidence_sha256':sha((PREP/'normal-verification-evidence.json').read_bytes()),'preflight':preflight,'frozen_review_files_guarded':len(protected),'canonical_mutation_performed':False},ensure_ascii=False,indent=2))
if preflight['schema_errors'] or preflight['publication_errors']:raise SystemExit(1)
