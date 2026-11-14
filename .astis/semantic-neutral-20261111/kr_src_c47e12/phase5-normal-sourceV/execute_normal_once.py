from pathlib import Path
import sys,json,hashlib,datetime,os,stat,copy
ROOT=Path('/Users/zhouhuanjian/ASTIS-GC');P=Path("/Users/zhouhuanjian/ASTIS-GC/.astis/semantic-neutral-20261111/kr_src_c47e12/phase5-normal-sourceV")
sys.path.insert(0,str(ROOT));sys.path.insert(0,str(P))
import preservation_guard as g
from tools import astis_advance as api
h=lambda b:hashlib.sha256(b).hexdigest()
req=json.loads((g.W/'exact-normal-sourceV-request.json').read_text());pre=json.loads((P/'final-independent-bounded-preflight.json').read_text())
assert pre['final_bounded_review_accepted']is True
old_event=json.loads((P/'original-inputs/actual-PROVED_LOCAL-append.exact.jsonl').read_bytes())
capsule=json.loads((P/'original-inputs/local-proof-capsule.json').read_text())
audit=json.loads((P/'original-inputs/own-source-reviewed-audit.before.raw.json').read_text())
frontier=json.loads((P/'original-inputs/own-frontier.before.raw.json').read_text())
baseline_summary=json.loads((P/'private-preservation-baseline-bounded-summary.json').read_text())
evidence={
 'verifier_id':g.ACTOR,
 'verified_commit':req['metadata_checked_commit'],
 'mathematical_candidate':req['mathematical_candidate'],
 'native_checked_commit':req['mathematical_candidate'],
 'metadata_checked_commit':req['metadata_checked_commit'],
 'original_proof_owner_id':req['owner_id_preserve'],
 'gate':{'kind':'independent bounded native/source verification plus exact reviewed-metadata gates','final_preflight':pre,'independent_native_archive_sha256':'56da548027aa97260f91d51c0ffb27d81b3d981a7290a7c2799ad05d28826684','original_source_phases1_4_archive_sha256':'ccbf41ebdcbd7119b2dc07f96dc5c83576515aa052948afb679b89688402f3c1','global_or_root_Tests_or_site_gate_claim':False},
 'source_audit':{'actual_original_source_actor':g.ACTOR,'own_audit_full_before_normal':audit,'original_source_review_overlay':json.loads((g.S/'phase4/source-review-overlay.json').read_text()),'original_canonical_semantic_result':json.loads((g.S/'phase4/canonical-semantic-review-result.v2.json').read_text()),'phase3_mathematical_freeze_sha256':'1739d07708cc6e6d21ccdabf99fe08e9144c2104ed7db31d3936ee38a2001f7b','phase3_original_actual_execution_receipt_sha256':'e9147c56d0e646c93284d1b1b6477f5f29119f5f776bd6afb7ac676fb2ca1f5d','canonical_reviewer_packet_sha256':req['canonical_reviewer_packet_sha256'],'publication_binding_sha256':req['publication_binding_sha256'],'source_lean_reconstruction_context_binding_unchanged':True,'no_new_mathematical_repair':True},
 'fake_closure_scan':{'actual_native_owned_results_full':pre['actual_native_full_bounded_summary'],'actual_independent_native_inventory_program_sha256':pre['native_program_sha256'],'actual_native_compile_receipts_full':pre['actual_native_compile_receipts'],'criterion':'All4 actual owned constants are closed Prop theorems with closed values and recursive axioms only propext/Classical.choice/Quot.sound; exact raw signatures match sealed strings; independently elaborated literal propositions are closed Prop and definitionally equal. Raw Expr structural equality is FALSE and preserved; no raw-AST equality claim. Full raw types/proofs/original failures retained in immutable original native archive, never replaced by a summary.','all_source_placeholders_absent':True},
 'publication_declarations':old_event['evidence']['publication_declarations'],
 'lean_declarations':old_event['evidence']['lean_declarations'],
 'lean_files':old_event['evidence']['lean_files'],
 'conceptual_mirror_audit':old_event['evidence']['conceptual_mirror_audit'],
 'original_PROVED_LOCAL_event_full':old_event,
 'original_PROVED_LOCAL_evidence_full':old_event['evidence'],
 'original_local_proof_capsule_full':capsule,
 'truth_boundary':req['truth_boundary'],
 'original_boundary_and_reader_HOLD_full_values':pre['reader_and_global_boundary_full_values'],
 'frontier_reader_contract_full_unchanged':frontier['reader_contract'],
 'frontier_reader_HOLD_full_unchanged':frontier['evidence']['reader_HOLD'],
 'native_raw_Expr_structural_equality':False,
 'native_literal_Prop_defeq':True,
 'local_verified_scope':'Only actual pointwise affine-cosine feature range equality and private same-witness real Euclidean coordinate application. No C6/absoluteC/full uniform Lemma4.4, adaptive/Haar/oracle/precision/TV/cap/cost adapter or either main lower bound.',
 'preservation':baseline_summary|{'full_private_foreign_values_location':'sibling private-phase5-preservation only; never portable','guard_semantics':'Complete raw old ledger prefix, full foreign state/latest_evidence and every existing VERIFIED object compared, not a whitelist projection. All tracked index/regular bytes, old/current frontier/control paths and ordinary nonignored untracked work guarded. Restricted ATLAS/C8/private/nested scope remains metadata-only.','full_private_baseline_exported':False},
 'reader_delivery':'HOLD: keep complete original code-fold/private source-page control gaps and all browser/MathJax/clipboard/mobile/global exclusions; no reader or website closure.',
 'normal_VERIFIED_API_actor':g.ACTOR,
 'normal_VERIFIED_attempt_budget':1,
 'root_sourceV_API_calls':0,
 'global_STABILIZING_lease_transfer_or_STAB_or_clean_port_or_remote_or_Goal_completion':False
}
payload=P/'normal-VERIFIED-evidence.full.json';payload.write_text(json.dumps(evidence,ensure_ascii=False,indent=2)+'\n')
api._validate_transition_evidence('VERIFIED',evidence,schema_version=4)
preguard=g.check('immediate-before-one-normal')
(P/'immediate-pre-normal-preservation-result.json').write_text(json.dumps(preguard,indent=2)+'\n')
marker=P/'normal-VERIFIED-attempted-once.PERMANENT.json'
marker_value={'actor':g.ACTOR,'advance_id':g.ADV,'action':'exactly one normal transition_advance to VERIFIED','created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'metadata_commit':req['metadata_checked_commit'],'mathematical_candidate':req['mathematical_candidate'],'evidence_file_sha256':h(payload.read_bytes()),'private_old_ledger_sha256':preguard['old_ledger_sha256'],'no_replay_under_uncertainty_or_rejection':True}
fd=os.open(marker,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o444)
with os.fdopen(fd,'wb')as f:
 f.write((json.dumps(marker_value,indent=2)+'\n').encode());f.flush();os.fsync(f.fileno())
dirfd=os.open(P,os.O_RDONLY);os.fsync(dirfd);os.close(dirfd)
try:
 api.transition_advance(g.ADV,'VERIFIED',worker_id=g.ACTOR,modes=('independent-source-native-verification',),evidence=evidence)
except BaseException as exc:
 (P/'normal-attempt-exception.NEVER-REPLAY.json').write_text(json.dumps({'type':type(exc).__name__,'message':str(exc),'marker_created':True,'retry_forbidden':True,'next_action':'Inspect actual ledger first; no replay and no fabricated V.'},indent=2)+'\n')
 raise
post=g.check('after-one-normal-before-frontier',after=True)
append_raw=post.pop('append_raw');event=post.pop('new_event')
assert event['evidence']==evidence
(P/'actual-normal-VERIFIED-append.exact.jsonl').write_bytes(append_raw)
(P/'actual-normal-VERIFIED-event.full.json').write_text(json.dumps(event,ensure_ascii=False,indent=2)+'\n')
(P/'actual-normal-VERIFIED-evidence.full.json').write_text(json.dumps(event['evidence'],ensure_ascii=False,indent=2)+'\n')
fp=ROOT/g.FRONT;old=(g.PRIVATE/'old-own-frontier.raw').read_bytes()
assert fp.read_bytes()==old
old_status=b'"status": "proved_locally"';new_status=b'"status": "independently_verified"'
assert old.count(old_status)==1
new=old.replace(old_status,new_status,1);fvalue=json.loads(new);expected=json.loads(old);expected['status']='independently_verified';assert fvalue==expected
tmp=P/'own-frontier-status-update.atomic.tmp'
with tmp.open('wb')as f:f.write(new);f.flush();os.fsync(f.fileno())
os.chmod(tmp,stat.S_IMODE(fp.stat().st_mode));os.replace(tmp,fp)
dfd=os.open(fp.parent,os.O_RDONLY);os.fsync(dfd);os.close(dfd)
(P/'own-frontier.after.exact.json').write_bytes(new)
final=g.check('after-normal-and-own-frontier',after=True)
tail=final.pop('append_raw');actual_event=final.pop('new_event');assert tail==append_raw and actual_event==event
actualf=json.loads(fp.read_text());assert actualf==expected and actualf['owner_id']==g.OWNER
assert actualf['truth_boundary']==frontier['truth_boundary']and actualf['reader_contract']==frontier['reader_contract']and actualf['evidence']['reader_HOLD']==frontier['evidence']['reader_HOLD']
fullresult=final|{'normal_API_calls_by_actual_source_actor':1,'root_sourceV_API_calls':0,'advance_id':g.ADV,'owner_id_preserved':g.OWNER,'verifier_id':g.ACTOR,'mathematical_candidate':req['mathematical_candidate'],'metadata_checked_commit':req['metadata_checked_commit'],'actual_append_sha256':h(append_raw),'actual_event_raw_sha256':h((P/'actual-normal-VERIFIED-event.full.json').read_bytes()),'frontier_status':'independently_verified','frontier_only_status_value_changed':True,'frontier_original_EOF_bytes_preserved':True,'reader_HOLD_full_values_preserved':True,'original_PLOCAL_event_evidence_capsule_full_retained':True,'all_old_foreign_advance_states_latest_evidence_and_existing_V_objects_full_values_preserved':True,'normal_state':'VERIFIED','global_STABILIZING_owner_and_controls_preserved':True,'reader_or_global_acceptance':False}
(P/'normal-VERIFIED-postguards.full-bounded-result.json').write_text(json.dumps(fullresult,ensure_ascii=False,indent=2)+'\n')
records,state=g.replay((ROOT/g.LEDGER).read_bytes());(P/'own-advance-after.actual.full.json').write_text(json.dumps(state[g.ADV],ensure_ascii=False,indent=2)+'\n')
print(json.dumps(fullresult,indent=2))

