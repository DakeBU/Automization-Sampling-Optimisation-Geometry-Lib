#!/opt/anaconda3/bin/python
import copy,datetime,hashlib,json,os,pathlib,subprocess,sys,traceback
sys.dont_write_bytecode=True
BASE=pathlib.Path(__file__).resolve().parent
ROOT=pathlib.Path('/Users/zhouhuanjian/ASTIS-GC')
sys.path.insert(0,str(BASE));import preservation_guard as guard
sys.path.insert(0,str(ROOT));from tools import astis_advance
from tools.astis_publication import check_advance
ACTOR='/root/cosine_gram_fresh_source_7e41d9'
OWNER='huanjian_gc_20261110_fixed_spectrum_cosine_gram'
ADV=guard.ADV;MATH='72e5d1405284f729f4eb600c5ae5dd556365b7e2';CARRIER='7359f552e3b9bdf27c2253703d879783f331c4e9'
def sha(data):return hashlib.sha256(data).hexdigest()
def write(name,value):(BASE/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
marker=BASE/'normal-V-once.permanent-marker.json'
assert not marker.exists(),'Permanent once marker exists: inspect ledger; never replay.'
head=subprocess.run(['git','rev-parse','HEAD'],cwd=ROOT,capture_output=True)
(BASE/'preflight-head.stdout').write_bytes(head.stdout);(BASE/'preflight-head.stderr').write_bytes(head.stderr)
assert head.returncode==0 and head.stdout.decode().strip()==CARRIER
selected=json.loads((BASE/'inputs/accepted-review-metadata-commit.json').read_text())['all_selected_files_exact_in_Git_tree']
for row in selected:
    data=(ROOT/row['path']).read_bytes()
    assert len(data)==row['bytes'] and sha(data)==row['sha256'],row['path']
plocal=json.loads((BASE/'original-PROVED_LOCAL-event.exact.jsonl').read_text())
capsule=json.loads((ROOT/'research-wiki/paper-contributions/GaussianComplexity/fixed-spectrum-cosine-gram-semantic-evidence/local-proof-capsule.json').read_text())
assert sha((BASE/'original-PROVED_LOCAL-event.exact.jsonl').read_bytes())==capsule['append_sha256']
audit_path='research-wiki/semantic-roundtrip/audits/huanjian-fixed-spectrum-cosine-gram.json'
audit_bytes=(ROOT/audit_path).read_bytes();audit=json.loads(audit_bytes)
assert sha(audit_bytes)=='d6e279e86e26f8a763739b72aacadb41692af10593f68ba9b0f10c3efb1304cc'
assert audit['state']=='accepted' and audit['source_review']['reviewer']==ACTOR
assert audit['source_review']['review_run_sha256']=='49236e7104295ef18d2f0ebf5522fa7d1ce81651a642449dc65e7b9f529a132a'
before=guard.verify_preserved(allow_own_append=False)
current=guard.states((ROOT/guard.LEDGER).read_bytes())[ADV]
assert current['state']=='PROVED_LOCAL' and current['owner_id']==OWNER
assert current['latest_evidence']==plocal['evidence']
evidence={
    'verifier_id':ACTOR,'verified_commit':MATH,'metadata_checked_commit':CARRIER,
    'original_owner_id_preserved':OWNER,'publication_declarations':copy.deepcopy(plocal['evidence']['publication_declarations']),
    'gate':{
        'independent_native':{'state':'PASS','mathematical_checked_commit':MATH,
            'findings':'research-wiki/paper-contributions/GaussianComplexity/fixed-spectrum-cosine-gram-semantic-evidence/fresh-native-0a91de-original-findings.json',
            'findings_sha256':'7287d0d751f44786643207352cf326a9f5d7300070a13b8b8596c81da2111052',
            'all_original_native_archive_sha256':'eef1e3597a76509f5ae76b47ac52ba5e0d9597b20680bc036fc357e7f363cca4',
            'source_role_postfreeze_native_evidence_verification':'.astis/semantic-neutral-20261110/cg_src_7e41d9/phase4/postfreeze_closure_verification.json'},
        'reviewed_metadata_carrier_gates':json.loads((BASE/'carrier-and-gates-acceptance.json').read_text())['all_four_gates_at_exact_carrier'],
        'metadata_carrier':CARRIER,'reader_delivery':'HOLD for all six unchanged-production step code source/copy/download neighbors; no browser/MathJax/desktop/mobile/global acceptance.'},
    'source_audit':{'state':'accepted','verdict':audit['verdict'],'audit':audit_path,'audit_raw_sha256':sha(audit_bytes),
        'publication_binding_sha256':audit['publication_binding_sha256'],'reviewer':ACTOR,
        'reviewer_packet_sha256':audit['source_review']['reviewer_packet_sha256'],
        'review_run_sha256':audit['source_review']['review_run_sha256'],'run_artifact':audit['source_review']['run_artifact'],
        'original_mathematical_judgment_sha256':'9664e70ced3c4c5be22866341ba565f70522d0f1d799dada13554ec1a3be2589',
        'original_source_all403_file_archive_sha256':'da7caa0e80bb367620b42c5f2834a02933147dd4d23511ece26e81da814d3963',
        'independent_from_formalizer':True,'independent_from_decoder':True,'repairs':[]},
    'fake_closure_scan':{'state':'PASS','scope':'Complete immutable P/T and canonical G inspected, exact closed root Props kernel checked in independent fresh native build; all26 owned closed Prop theorem types/recursive axioms/reachability expanded.',
        'authored_roots':2,'compiler_generated_certificates':24,'generated_providers_are_not_new_source_results':True,
        'recursive_axioms_allowed':['propext','Classical.choice','Quot.sound'],
        'native_actual_kernel_stdout_sha256':'737133e03aadb018309c1932e71bc0960aa77d4ca9a81cefd7921699f6c532d2',
        'native_exact_allowned_types_stdout_sha256':'26e77af429787cb723fc69417921b20710652e989c44d4074f9b3e4e71ae6dcd'},
    'original_proved_local_event':copy.deepcopy(plocal),
    'original_proved_local_evidence':copy.deepcopy(plocal['evidence']),
    'original_proved_local_event_sha256':capsule['append_sha256'],
    'original_local_proof_capsule':copy.deepcopy(capsule),
    'truth_boundary':plocal['evidence']['truth_boundary'],
    'reader_delivery':'HOLD: all six step copy/download/exact-module-source neighbors; no browser or global acceptance.',
    'integration_boundary':'Normal independent source VERIFIED only. Original owner unchanged; remote original owner remains STABILIZING and merged PR403 does not release the lease. No STABILIZING/global/imports/root Tests/Registry/site/index/graph/push/purification/Goal completion.',
    'preservation_before':before,
    'normal_sourceV_once_marker':str(marker.relative_to(ROOT)),
    'portable_execution_directory':str(BASE.relative_to(ROOT)),
    'post_integration_authority':'Only the same original independent source actor may later add post_integration; preserve every original V value and all other foreign/history fields.'
}
astis_advance._validate_transition_evidence('VERIFIED',evidence,schema_version=4)
astis_advance._assert_worker_lane_owner(current,current='PROVED_LOCAL',to_state='VERIFIED',worker_id=ACTOR)
assert current['publication_declarations']==evidence['publication_declarations']
check_advance(evidence['publication_declarations'],reviewed=True)
write('normal-V-evidence.proposed.json',evidence)
guard.verify_preserved(allow_own_append=False)
preflight={'head':CARRIER,'math_checked_commit':MATH,'actor':ACTOR,'owner':OWNER,'state_before':'PROVED_LOCAL',
           'source_audit_exact':True,'four_real_gates_exact':True,'check_advance_reviewed_actual_preflight':'PASS',
           'preservation':before,'API_not_yet_called':True,'once_marker_absent':True}
write('normal-V-preflight.json',preflight)
# Permanent O_EXCL marker is created and fsynced BEFORE the single API call.
marker_record={'phase':'permanent-before-API-once-marker','advance_id':ADV,'verifier_id':ACTOR,'owner_id':OWNER,
               'mathematical_checked_commit':MATH,'metadata_checked_carrier':CARRIER,
               'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
               'ledger_prefix_sha256':sha((ROOT/guard.LEDGER).read_bytes()),
               'exact_execution_script_sha256':sha(pathlib.Path(__file__).read_bytes()),
               'proposed_evidence_sha256':sha((BASE/'normal-V-evidence.proposed.json').read_bytes()),
               'rule':'Permanent O_EXCL; at most one transition_advance call. Any uncertain result requires ledger inspection, never replay.'}
fd=os.open(marker,os.O_CREAT|os.O_EXCL|os.O_WRONLY,0o444)
with os.fdopen(fd,'wb') as file:
    file.write((json.dumps(marker_record,indent=2)+'\n').encode());file.flush();os.fsync(file.fileno())
call_started=datetime.datetime.now(datetime.timezone.utc).isoformat();error=None
try:
    # Exactly one normal state-machine API invocation. Never repeat this call.
    astis_advance.transition_advance(ADV,'VERIFIED',worker_id=ACTOR,evidence=evidence)
except BaseException:
    error=traceback.format_exc();(BASE/'normal-V-API.actual-exception.txt').write_text(error)
# Independently inspect actual ledger after every result, including uncertainty.
old=(guard.PRIVATE/'ledger-before.raw.jsonl').read_bytes();now=(ROOT/guard.LEDGER).read_bytes()
(guard.PRIVATE/'ledger-after.raw.jsonl').write_bytes(now)
assert now.startswith(old),'Raw old ledger prefix was not preserved; no replay.'
suffix=now[len(old):];(BASE/'normal-VERIFIED-append.exact.jsonl').write_bytes(suffix)
appended=[json.loads(line) for line in suffix.splitlines() if line.strip()]
outcome={'call_started_utc':call_started,'call_returned_without_exception':error is None,'API_invocations':1,
         'permanent_once_marker_sha256':sha(marker.read_bytes()),'actual_appended_record_count':len(appended),
         'exact_append_sha256':sha(suffix),'uncertainty_policy':'Actual ledger inspected; no replay.'}
write('normal-V-API.actual-outcome.json',outcome)
if error is not None:
    print(json.dumps(outcome,indent=2));sys.stderr.write(error);raise SystemExit(1)
assert len(appended)==1 and appended[0]['event']=='transition'
event=appended[0]
assert event['advance_id']==ADV and event['from_state']=='PROVED_LOCAL' and event['to_state']=='VERIFIED'
assert event['worker_id']==ACTOR and event['evidence']==evidence
assert event['evidence']['original_proved_local_evidence']==plocal['evidence']
assert event['evidence']['original_proved_local_event']==plocal
assert event['evidence']['original_local_proof_capsule']==capsule
after_state=guard.states(now)[ADV]
assert after_state['state']=='VERIFIED' and after_state['owner_id']==OWNER
assert after_state['latest_evidence']==evidence
preserved=guard.verify_preserved(allow_own_append=True)
# Own frontier closeout is limited to precisely two JSON paths.
frontier=ROOT/guard.FRONTIER;raw_frontier=frontier.read_bytes()
assert raw_frontier==(BASE/'own-frontier-before.raw.json').read_bytes()
old_frontier=json.loads(raw_frontier);new_frontier=copy.deepcopy(old_frontier)
new_frontier['status']='independently_verified'
new_frontier['evidence']['integration_boundary']={
    'normal_sourceV':'VERIFIED','advance_id':ADV,'verifier_id':ACTOR,'original_owner_id':OWNER,
    'exact_event_sha256':sha(suffix),'mathematical_native_checked_commit':MATH,'metadata_checked_carrier':CARRIER,
    'reader_delivery':'HOLD all six corresponding step copy/download/exact-source neighbors; no browser/MathJax/desktop/mobile/global acceptance.',
    'remaining_source_boundary':evidence['truth_boundary'],
    'serialization_boundary':'Original remote owner remains STABILIZING; merged PR403 is not lease release. No STAB, global changes, Registry/site/index/graph/push or purification/Goal completion.',
    'historical_values':'All previous nested frontier values remain exactly preserved; earlier pending prose is retained as original history.'}
def strip_two(obj):
    out=copy.deepcopy(obj);out.pop('status',None);out['evidence'].pop('integration_boundary',None);return out
assert strip_two(old_frontier)==strip_two(new_frontier)
frontier.write_text(json.dumps(new_frontier,ensure_ascii=False,indent=2)+'\n')
(BASE/'own-frontier-after.raw.json').write_bytes(frontier.read_bytes())
preserved=guard.verify_preserved(allow_own_append=True)
write('normal-V-preservation-verification.json',preserved)
summary={'advance_id':ADV,'state':'VERIFIED','verifier_id':ACTOR,'owner_id_unchanged':OWNER,
         'mathematical_native_checked_commit':MATH,'metadata_checked_carrier':CARRIER,
         'normal_API_invocations':1,'permanent_O_EXCL_marker':str(marker.relative_to(ROOT)),
         'exact_append_bytes':len(suffix),'exact_append_sha256':sha(suffix),
         'whole_raw_ledger_old_prefix_preserved':True,'preservation':preserved,
         'complete_original_PLOCAL_evidence_event_and_capsule_nested_unchanged':True,
         'own_frontier_changed_JSON_paths':['status','evidence.integration_boundary'],
         'frontier_before_sha256':sha(raw_frontier),'frontier_after_sha256':sha(frontier.read_bytes()),
         'reader_HOLD_all_six_and_remote_STABILIZING_lease_preserved':True,
         'no_STAB_global_publication_purification_or_Goal_completion':True}
write('normal-V-closeout.json',summary)
print(json.dumps(summary,indent=2))
