"""PREPARED ONLY: one independent normal API call, only after exact ROOT window1 authorization."""
from verification_common import *
import argparse

def payload(a,x,authpath):
    extra={
        'verifier_id':VERIFIER,'verified_commit':a['carrier_commit'],
        'gate':{'checked_source_metadata_carrier':a['carrier_commit'],'six_actual_exit0_gate_records':x['gates']['records'],'gate_summary':a['gate_summary'],'normal_API_publication_gate':'transition_advance executes check_advance(reviewed=True) before append; no manual ledger append.','new_Lean_build_at_checked_carrier':False},
        'source_audit':{'current_binding':BINDING,'source_public':x['pins']['source_public'],'source_private':x['pins']['source_private'],'whole_module_seven_slot_five_step_run':x['pins']['source_run'],'canonical_public_audit':x['pins']['public_audit'],'private_consumer_audit':x['pins']['private_audit'],'source_blind_decoder_and_locator_originals':'Preserved unchanged inline in original PL25 fields. No new native/reader inference substitutes for them.','new_source_review_claimed':False},
        'fake_closure_scan':{'actual_built_math_commit':MATH,'native_original':x['pins']['native_original'],'native_exact_carried':x['pins']['native_carried'],'canonical_scan':x['pins']['native_fake_scan'],'all13_exact_ASTIS_modules_freshly_recompiled':True,'prior_ASTIS_olean_reused':False,'recursive_type_value_closure_declarations':58889,'standard_axioms':['Classical.choice','Quot.sound','propext'],'unsafe':0,'sorryAx_or_unauthorized_axiom':False,'no_new_Lean_kernel_or_scan_run_at_carrier':True},
        'current_independent_reader_acceptance':{'original_report':x['pins']['reader_original'],'exact_carried_report':x['pins']['reader_carried'],'original_explicit103_leaf_manifest':x['pins']['reader_manifest_original'],'status':'PASS_BOUNDED_ISOLATED_READER','necessary_reader_residuals':0,'actual_OS_exit_code':0,'actual_checks':523,'actual_false_checks':0,'actual_original_PNGs_viewed':50,'actual_natural_stability_traces':22,'limits':copy.deepcopy(x['reader']['explicit_limits']),'old_v3_FAIL_and_observational_diagnostic':copy.deepcopy(x['reader']['old_findings_resolution_for_this_successor_only']),'not_production_or_physical_touch_or_normalV':True},
        'original_PL_retention':{'original':x['pins']['PL'],'original_sha256':PLSHA,'actual_original_top_level_field_count':25,'all_original_fields_inline_structurally_equal':True,'original_reader_pending_snapshot_is_historical_and_unchanged':True},
        'verified_carrier_vs_actual_build':{'verified_source_metadata_evidence_carrier':a['carrier_commit'],'actual_fresh_native_build_identity':MATH,'bare960c_and_any_metadata_or_public_carrier_not_retroactively_called_built':True},
        'actual_verified_scope':'Generic finite real AE-PD matrix Bochner probability integral, including empty index, and actual private literal Gaussian four-family all-real matrix-exponential mean domain, trace commutation/strict positivity and r²exp(|s|dRstar) cap. No separate public T node, matrix-log/Lieb/Bernstein/C6/main lower bound/cost adapter/main or production integration/purification/whole-Goal completion.',
        'independent_window_authorization':ident(authpath)
    }
    assert not(set(extra)&set(x['pl']))
    v=copy.deepcopy(x['pl']);v.update(extra);assert all(v[k]==value for k,value in x['pl'].items());return v

def normal_window(a,authpath):
    marker=PRIVATE/'normal-V-attempted.once.json';assert not marker.exists()
    x=evidence_inputs(a);before=snapshot('window1-before',a);target=inspect_target(before,x['pl'],'PROVED_LOCAL')
    assert sha(before['araw'])==a['expected_advance_ledger_sha256'] and sha(before['draw'])==a['expected_discovery_ledger_sha256']
    assert not git('window1-clean-worktree','diff','--name-only','HEAD','-z') and not git('window1-clean-index','diff','--cached','--name-only','-z')
    assert file_sha(REPO/CELL)==a['expected_target_cell_sha256'] and read(REPO/CELL)['status']=='proved_locally'
    for i,(raw,h) in enumerate(SOURCES.items()):assert sha(git('window1-carrier-source'+str(i),'show',a['carrier_commit']+':'+raw))==h
    original=OWN/'PROVED_LOCAL-original25.exact.json'
    if not original.exists():exact(original,x['pl_raw'])
    assert original.read_bytes()==x['pl_raw'] and file_sha(original)==PLSHA
    v=payload(a,x,authpath);write(OWN/'normal-V-evidence.full.json',v)
    sys.path.insert(0,str(REPO));from tools import astis_advance as api
    assert api.DEFAULT_ADVANCE_LEDGER==REPO/ADVPATH and api.DEFAULT_DISCOVERY_LEDGER==REPO/DISCPATH
    write(marker,{'local_private_do_not_publish':True,'advance_id':ADV,'verifier_id':VERIFIER,'carrier':a['carrier_commit'],'authorization_sha256':file_sha(authpath),'payload_sha256':file_sha(OWN/'normal-V-evidence.full.json'),'API_attempt_about_to_begin_once':True,'utc':dt.datetime.now(dt.timezone.utc).isoformat()})
    returned=False;error=None
    try:
        api.transition_advance(ADV,'VERIFIED',worker_id=VERIFIER,modes=tuple(target.get('modes',())),evidence=v)
        returned=True
    except BaseException:error=traceback.format_exc();print(error,file=sys.stderr)
    # Actual suffix is inspected after return or failure. No replay, repair, retry or rollback.
    current=(REPO/ADVPATH).read_bytes();exact(PRIVATE/'window1-actual-ledger-after-call.jsonl',current)
    suffix=current[len(before['araw']):] if current.startswith(before['araw']) else None
    if suffix is not None:exact(PRIVATE/'window1-actual-suffix.raw',suffix)
    write(PRIVATE/'window1-API-return.private.json',{'returned':returned,'exception':error,'old_prefix_preserved':suffix is not None,'actual_suffix_sha256':sha(suffix) if suffix is not None else None,'automatic_retry_or_rollback':False})
    after=snapshot('window1-after',a);g=postguards(before,after,a,{ADVPATH})
    write(OWN/'window1-observed-preservation.public.json',{'advance_id':ADV,'guards':g,'actual_normal_API_returned':returned,'actual_suffix_exists':bool(suffix),'old_A_ledger_prefix_preserved':suffix is not None,'no_success_claim':True})
    assert returned and error is None and suffix and suffix.endswith(b'\n') and len(suffix.splitlines())==1
    assert g['only_changed_tracked_paths']==[ADVPATH]
    appended=json.loads(suffix)
    assert appended['event']=='transition' and appended['advance_id']==ADV and appended['from_state']=='PROVED_LOCAL' and appended['to_state']=='VERIFIED' and appended['worker_id']==VERIFIER and appended['evidence']==v
    assert all(appended['evidence'][k]==value for k,value in x['pl'].items())
    final=inspect_target(after,x['pl'],'VERIFIED');assert final['modes']==target['modes']
    exact(OWN/'normal-V-exact-append.jsonl',suffix)
    write(OWN/'window1-postguards.public.json',{'advance_id':ADV,'all_postguards_passed':True,'all_frontiers_including_target_unchanged':True,'all_original_PL_top_level_fields_unchanged':True,'actual_original_PL_field_count':25,'exact_appended_record_sha256':sha(suffix),'exact_appended_record_bytes':len(suffix),'actual_normal_API_returned':True,'normal_API_calls':1,'post_advance_ledger_sha256':sha(after['araw']),'post_discovery_ledger_sha256':sha(after['draw']),'guards':g,'all_full_maps_raw_ledgers_index_API_OS_logs_local_private':True,'actual_math_build_identity':MATH,'new_native_source_or_reader_run':False})

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--authorization',type=Path,required=True);p.add_argument('--authorization-sha256',required=True);p.add_argument('--child',action='store_true');args=p.parse_args()
    return run_captured(args,'NORMAL_PROOF_V_ONCE',normal_window)
if __name__=='__main__':sys.exit(main())
