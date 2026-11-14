import contextlib, io, json, sys
from pathlib import Path
from preflight import ROOT, REPO, PUB, PRIVATE, ADVANCE, FRONTIER, AUDIT, VERIFIER, LEDGER, DISCOVERY, CARRIER, canonical, sha, write, git, foreign_controls

def main():
    actual=PUB/'actual-v2'
    marker=actual/'api-call-attempt.json'
    assert not marker.exists(), 'Do not call the normal transition API twice.'
    pre=json.loads((PUB/'preflight.json').read_text())
    evidence=json.loads((actual/'actual-V-evidence.original.raw.json').read_text())
    assert sha(canonical(evidence))=='e8e02a491a04c1086161278f6aa5027783c1ecfc4fa9a84408867f600000c3f9'
    assert evidence['fake_closure_scan']['native_actor']=='/root/module_reader_f35b7d'
    before=(PRIVATE/'advances.before.raw.jsonl').read_bytes()
    assert LEDGER.read_bytes()==before
    assert DISCOVERY.read_bytes()==(PRIVATE/'discoveries.before.raw.jsonl').read_bytes()
    assert FRONTIER.read_bytes()==(PUB/'own-frontier.before.raw.json').read_bytes()
    assert AUDIT.read_bytes()==(PRIVATE/'own-audit.before.raw.json').read_bytes()
    assert git('rev-parse','HEAD').decode().strip()==CARRIER
    assert not git('status','--porcelain=v1','--untracked-files=no')
    assert git('ls-files','--stage','-z')==(PRIVATE/'git-index.before.raw').read_bytes()
    assert sha(canonical({k:sha(v) for k,v in foreign_controls().items()}))==pre['private_preservation_guards']['foreign_control_file_hashes_sha256']
    for r in pre['source_math_and_exposition_bytes_identical_at_math_carrier_and_worktree']:
        assert sha((REPO/r['path']).read_bytes())==r['sha256']
    sys.path.insert(0,str(REPO))
    from tools import astis_advance as advance
    state=advance._replay_advances(json.loads(z) for z in before.splitlines())
    assert state[ADVANCE]['state']=='PROVED_LOCAL'
    assert state[ADVANCE]['owner_id'] != VERIFIER
    write(marker,{'normal_transition_API_call_number':1,'API':'tools.astis_advance.transition_advance','advance_id':ADVANCE,'from_state':'PROVED_LOCAL','to_state':'VERIFIED','worker_id':VERIFIER,'evidence_canonical_sha256':sha(canonical(evidence)),'no_retry_authorized':True})
    captured=io.StringIO()
    try:
        with contextlib.redirect_stdout(captured),contextlib.redirect_stderr(captured):
            advance.transition_advance(ADVANCE,'VERIFIED',worker_id=VERIFIER,modes=('independent-source-verification','bounded-normal-sourceV'),evidence=evidence)
    except BaseException as exc:
        (actual/'api.stdout-stderr.log').write_text(captured.getvalue())
        write(actual/'api-error.json',{'type':type(exc).__name__,'message':str(exc),'normal_API_calls':1,'retry_performed':False})
        raise
    (actual/'api.stdout-stderr.log').write_text(captured.getvalue())
    after=LEDGER.read_bytes()
    assert after.startswith(before)
    appended=after[len(before):]
    assert appended.endswith(b'\n') and len(appended.splitlines())==1
    event=json.loads(appended)
    assert event['event']=='transition' and event['advance_id']==ADVANCE
    assert event['from_state']=='PROVED_LOCAL' and event['to_state']=='VERIFIED' and event['worker_id']==VERIFIER
    assert event['evidence']==evidence and canonical(event['evidence'])==canonical(evidence)
    assert appended==canonical(event)+b'\n'
    newstate=advance._replay_advances(json.loads(z) for z in after.splitlines())
    assert newstate[ADVANCE]['state']=='VERIFIED'
    foreign={k:v for k,v in newstate.items() if k!=ADVANCE}
    assert canonical(foreign)==(PRIVATE/'foreign-advances.before.canonical.json').read_bytes()
    assert DISCOVERY.read_bytes()==(PRIVATE/'discoveries.before.raw.jsonl').read_bytes()
    assert FRONTIER.read_bytes()==(PUB/'own-frontier.before.raw.json').read_bytes()
    assert AUDIT.read_bytes()==(PRIVATE/'own-audit.before.raw.json').read_bytes()
    assert not git('status','--porcelain=v1','--untracked-files=no')
    assert git('ls-files','--stage','-z')==(PRIVATE/'git-index.before.raw').read_bytes()
    assert sha(canonical({k:sha(v) for k,v in foreign_controls().items()}))==pre['private_preservation_guards']['foreign_control_file_hashes_sha256']
    (PRIVATE/'advances.after-API.raw.jsonl').write_bytes(after)
    (PRIVATE/'foreign-advances.after-API.canonical.json').write_bytes(canonical(foreign))
    (actual/'normal-VERIFIED-event.exact.raw.jsonl').write_bytes(appended)
    (actual/'normal-VERIFIED-event.canonical.json').write_bytes(canonical(event))
    write(actual/'normal-VERIFIED-event.readable.json',event)
    write(actual/'own-sau.after-API.json',newstate[ADVANCE])
    result={'normal_API_call_count':1,'API':'tools.astis_advance.transition_advance','actual_state':'VERIFIED','advance_id':ADVANCE,'actual_worker':VERIFIER,'created_at':event['created_at'],'execution_HEAD':CARRIER,'checked_mathematical_commit':evidence['verified_commit'],'accepted_metadata_carrier':evidence['accepted_metadata_carrier'],'actual_event_raw_sha256':sha(appended),'actual_event_canonical_sha256':sha(canonical(event)),'original_evidence_raw_sha256':sha((actual/'actual-V-evidence.original.raw.json').read_bytes()),'original_evidence_canonical_sha256':sha(canonical(evidence)),'all_original_24_keys_and_all_nested_values_in_actual_event_identical':True,'ledger_before_sha256':sha(before),'ledger_after_API_sha256':sha(after),'ledger_before_bytes':len(before),'ledger_after_API_bytes':len(after),'append_bytes':len(appended),'ledger_before_row_count':len(before.splitlines()),'ledger_after_row_count':len(after.splitlines()),'exactly_one_appended_event':True,'entire_prior_ledger_raw_prefix_preserved':True,'all294_foreign_advance_states_equal':True,'discovery_raw_unchanged':True,'all770_foreign_control_file_bytes_unchanged':True,'git_index_unchanged':True,'no_tracked_file_changed_during_API':True,'own_audit_unchanged':True,'own_frontier_still_before_state_pending_separate_closeout':True,'no_STAB_or_global_credit':True,'only_future_root_post_integration_extension_by_original_source_verifier':True}
    write(actual/'api-execution-result.json',result)
    names=['api-call-attempt.json','api.stdout-stderr.log','normal-VERIFIED-event.exact.raw.jsonl','normal-VERIFIED-event.canonical.json','normal-VERIFIED-event.readable.json','own-sau.after-API.json','api-execution-result.json']
    write(actual/'API-execution-freeze.json',{'schema':1,'normal_API_calls':1,'state':'VERIFIED_API_COMPLETED_BEFORE_SEPARATE_FRONTIER_CLOSEOUT','files':[{'path':n,'sha256':sha((actual/n).read_bytes()),'bytes':(actual/n).stat().st_size} for n in names],'no_foreign_raw_publication':True})
    for n in names+['API-execution-freeze.json']:(actual/n).chmod(0o444)
    for p in PRIVATE.iterdir():
        if p.is_file():p.chmod(0o600)
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
