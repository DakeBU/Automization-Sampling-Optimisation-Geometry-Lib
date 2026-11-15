"""PREPARED ONLY: one independent normal API call, only after exact ROOT window1 authorization."""
from verification_common import *
import argparse

def payload(a,x,authpath):
    extra={
      'verifier_id':VERIFIER,'verified_commit':a['carrier_commit'],
      'gate':{'checked_source_metadata_carrier':a['carrier_commit'],'six_actual_exit0_gate_records':x['gates']['records'],'gate_summary':a['gate_summary'],'normal_API_publication_gate':'transition_advance invokes check_advance(reviewed=True); no manual append','new_Lean_build_at_checked_carrier':False},
      'source_audit':{'current_binding':a['source_binding'],'source_public':x['pins']['source_public'],'source_private':x['pins']['source_private'],'whole_module_and_reader_spans_run':x['pins']['source_run'],'canonical_public_audit':x['pins']['public_audit'],'private_consumer_audit':x['pins']['private_audit'],'current_independent_inspection':a['independent_source_review_summary'],'no_new_source_review_from_native_flags':True},
      'fake_closure_scan':{'actual_built_math_commit':MATH,'native_original':x['pins']['native_original'],'native_exact_carried':x['pins']['native_carried'],'canonical_scan':x['pins']['native_fake_scan'],'exact_ASTIS_modules_freshly_recompiled':6,'old_ASTIS_olean_reused':False,'target_recursive_type_value_declarations':34481,'standard_axioms':['Classical.choice','Quot.sound','propext'],'target_unsafe':0,'target_partial':0,'compiler_partial_execution_body_preserved_not_claimed_safely_kernel_checked':True,'no_new_kernel_or_build_at_carrier':True},
      'current_independent_reader_acceptance':{'original_report':x['pins']['reader_original'],'exact_carried_report':x['pins']['reader_carried'],'explicit_manifest':x['pins']['reader_manifest_original'],'actual_independent_inspection':a['independent_reader_review_summary'],'no_production_physical_touch_or_normalV_credit':True},
      'original_PL_retention':{'original':x['pins']['PL'],'original_sha256':a['original_PL_sha256'],'actual_original_top_level_field_count':len(x['pl']),'all_original_fields_inline_structurally_equal':True,'historical_pending_fields_unchanged':True},
      'verified_carrier_vs_actual_build':{'checked_metadata_carrier':a['carrier_commit'],'actual_native_build_identity':MATH,'bare_parent_or_future_carrier_not_retroactively_built':True},
      'actual_verified_scope':'Measurable finite-fuel seeded adaptive oracle simulation with full terminal state/Option/count joint laws and actual expected costs; literal fixed-spectrum FO/MV two-direction application with genuine internal gradient, all full O and fuel0 included. No source-algorithm representation/class-uniform success/query lower bound/Haar/TV/QG/2T/C6/main bound/purification/whole-Goal credit.',
      'independent_window_authorization':ident(authpath)
    }
    assert a['independent_source_review_summary'] and a['independent_reader_review_summary']
    assert not(set(extra)&set(x['pl']))
    value=copy.deepcopy(x['pl']);value.update(extra)
    assert all(value[k]==v for k,v in x['pl'].items())
    return value

def normal_window(a,authpath):
    marker=PRIVATE/'normal-V-attempted.once.json';assert not marker.exists()
    x=evidence_inputs(a);before=snapshot('window1-before',a);target=inspect_target(before,x['pl'],'PROVED_LOCAL')
    assert sha(before['araw'])==a['expected_advance_ledger_sha256'] and sha(before['draw'])==a['expected_discovery_ledger_sha256']
    assert not git('window1-clean-worktree','diff','--name-only','HEAD','-z') and not git('window1-clean-index','diff','--cached','--name-only','-z')
    assert file_sha(REPO/CELL)==a['expected_target_cell_sha256'] and read(REPO/CELL)['status']=='proved_locally'
    for i,(raw,h) in enumerate(SOURCES.items()):assert sha(git('window1-carrier-source'+str(i),'show',a['carrier_commit']+':'+raw))==h
    original=OWN/'PROVED_LOCAL-original.exact.json'
    if not original.exists():exact(original,x['pl_raw'])
    assert original.read_bytes()==x['pl_raw'] and file_sha(original)==a['original_PL_sha256']
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
    write(OWN/'window1-postguards.public.json',{'advance_id':ADV,'all_postguards_passed':True,'all_frontiers_including_target_unchanged':True,'all_original_PL_top_level_fields_unchanged':True,'actual_original_PL_field_count':len(x['pl']),'exact_appended_record_sha256':sha(suffix),'exact_appended_record_bytes':len(suffix),'actual_normal_API_returned':True,'normal_API_calls':1,'post_advance_ledger_sha256':sha(after['araw']),'post_discovery_ledger_sha256':sha(after['draw']),'guards':g,'all_full_maps_raw_ledgers_index_API_OS_logs_local_private':True,'actual_math_build_identity':MATH,'new_native_source_or_reader_run':False})

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--authorization',type=Path,required=True);p.add_argument('--authorization-sha256',required=True);p.add_argument('--child',action='store_true');args=p.parse_args()
    return run_captured(args,'NORMAL_PROOF_V_ONCE',normal_window)
if __name__=='__main__':sys.exit(main())
