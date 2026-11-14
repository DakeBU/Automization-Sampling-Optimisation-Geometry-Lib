import json, sys
from preflight import REPO,PUB,PRIVATE,ADVANCE,FRONTIER,AUDIT,VERIFIER,LEDGER,DISCOVERY,CARRIER,canonical,sha,write,git,foreign_controls

def main():
    actual=PUB/'actual-v2'
    pre=json.loads((PUB/'preflight.json').read_text())
    marker=json.loads((actual/'api-call-attempt.json').read_text())
    assert marker['normal_transition_API_call_number']==1
    evidence=json.loads((actual/'actual-V-evidence.original.raw.json').read_text())
    before=(PRIVATE/'advances.before.raw.jsonl').read_bytes();after=LEDGER.read_bytes()
    assert after.startswith(before)
    app=after[len(before):];assert len(app.splitlines())==1 and app.endswith(b'\n')
    event=json.loads(app);assert app==canonical(event)+b'\n'
    assert event['advance_id']==ADVANCE and event['from_state']=='PROVED_LOCAL' and event['to_state']=='VERIFIED'
    assert event['worker_id']==VERIFIER and event['evidence']==evidence
    assert canonical(event['evidence'])==(actual/'actual-V-evidence.original.canonical.json').read_bytes()
    sys.path.insert(0,str(REPO))
    from tools import astis_advance as advance
    state=advance._replay_advances(json.loads(z) for z in after.splitlines())
    assert state[ADVANCE]['state']=='VERIFIED'
    foreign={k:v for k,v in state.items() if k!=ADVANCE}
    assert canonical(foreign)==(PRIVATE/'foreign-advances.before.canonical.json').read_bytes()
    assert DISCOVERY.read_bytes()==(PRIVATE/'discoveries.before.raw.jsonl').read_bytes()
    assert FRONTIER.read_bytes()==(PUB/'own-frontier.before.raw.json').read_bytes()
    assert AUDIT.read_bytes()==(PRIVATE/'own-audit.before.raw.json').read_bytes()
    assert git('rev-parse','HEAD').decode().strip()==CARRIER
    changed=git('diff','--name-only').decode().splitlines();assert changed==['runs/substantive_advances.jsonl'],changed
    assert git('ls-files','--stage','-z')==(PRIVATE/'git-index.before.raw').read_bytes()
    assert sha(canonical({k:sha(v) for k,v in foreign_controls().items()}))==pre['private_preservation_guards']['foreign_control_file_hashes_sha256']
    contract=json.loads((actual/'original-evidence-retention-contract.json').read_text())
    def lookup(pointer):
        x=evidence
        for part in pointer.lstrip('/').split('/') if pointer else []:
            part=part.replace('~1','/').replace('~0','~');x=x[int(part)] if isinstance(x,list) else x[part]
        return x
    assert list(evidence)==contract['all_original_top_level_keys']
    for n in contract['nodes']:assert sha(canonical(lookup(n['json_pointer'])))==n['canonical_value_sha256']
    (PRIVATE/'advances.after-API.raw.jsonl').write_bytes(after)
    (PRIVATE/'foreign-advances.after-API.canonical.json').write_bytes(canonical(foreign))
    (actual/'normal-VERIFIED-event.exact.raw.jsonl').write_bytes(app)
    (actual/'normal-VERIFIED-event.canonical.json').write_bytes(canonical(event))
    write(actual/'normal-VERIFIED-event.readable.json',event)
    write(actual/'own-sau.after-API.json',state[ADVANCE])
    (actual/'api-wrapper-original-source.py').write_bytes((PUB.parent/'execute_one_api.py').read_bytes())
    write(actual/'postflight-guard-diagnostic.json',{'failure_class':'IMPLEMENTATION_FAILED','scope':'local postflight guard implementation only','normal_API_success':True,'normal_API_call_count':1,'not_a_mathematical_failure':True,'not_an_unexecuted_or_failed_normal_API':True,'original_wrapper_exit_code':1,'failed_source_line':55,'original_assertion':"assert not git('status','--porcelain=v1','--untracked-files=no')",'actual_tracked_delta':['runs/substantive_advances.jsonl'],'reason':'The guard incorrectly required a clean tracked worktree after the authorized normal API. The API legitimately appends the tracked advance ledger. No foreign tracked change occurred.','corrected_read_only_postflight_policy':'Require exactly the normal ledger path before the separate authorized frontier closeout. Verify raw prefix, one own event and all foreign state/control bytes independently.','API_retry_or_replay_performed':False,'original_API_stdout_stderr_file':'api.stdout-stderr.log','original_source_preserved':'api-wrapper-original-source.py'})
    result={'normal_API_call_count':1,'API':'tools.astis_advance.transition_advance','API_return':'returned without exception before the separate postguard assertion','wrapper_original_exit_code':1,'postflight_recovery':'read-only; no transition API call','actual_state':'VERIFIED','advance_id':ADVANCE,'actual_worker':VERIFIER,'created_at':event['created_at'],'execution_HEAD':CARRIER,'checked_mathematical_commit':evidence['verified_commit'],'accepted_metadata_carrier':evidence['accepted_metadata_carrier'],'actual_event_raw_sha256':sha(app),'actual_event_canonical_sha256':sha(canonical(event)),'original_evidence_raw_sha256':sha((actual/'actual-V-evidence.original.raw.json').read_bytes()),'original_evidence_canonical_sha256':sha(canonical(evidence)),'all_original_top_level_key_count':len(evidence),'all_original_nested_node_count':len(contract['nodes']),'all_original_keys_and_all_nested_values_in_actual_event_identical':True,'ledger_before_sha256':sha(before),'ledger_after_API_sha256':sha(after),'ledger_before_bytes':len(before),'ledger_after_API_bytes':len(after),'append_bytes':len(app),'ledger_before_row_count':len(before.splitlines()),'ledger_after_row_count':len(after.splitlines()),'exactly_one_appended_event':True,'entire_prior_ledger_raw_prefix_preserved':True,'all294_foreign_advance_states_equal':True,'discovery_raw_unchanged':True,'all770_foreign_control_file_bytes_unchanged':True,'git_index_unchanged':True,'tracked_delta_only_authorized_normal_ledger':True,'own_audit_unchanged':True,'own_frontier_still_before_state_pending_separate_closeout':True,'no_STAB_or_global_credit':True,'guard_failure_class':'IMPLEMENTATION_FAILED; local guard only, no mathematical/API failure'}
    write(actual/'api-execution-result.json',result)
    names=['api-call-attempt.json','api.stdout-stderr.log','api-wrapper-original-source.py','postflight-guard-diagnostic.json','normal-VERIFIED-event.exact.raw.jsonl','normal-VERIFIED-event.canonical.json','normal-VERIFIED-event.readable.json','own-sau.after-API.json','api-execution-result.json']
    write(actual/'API-execution-freeze.json',{'schema':1,'normal_API_calls':1,'state':'VERIFIED_API_COMPLETED_BEFORE_SEPARATE_FRONTIER_CLOSEOUT','files':[{'path':n,'sha256':sha((actual/n).read_bytes()),'bytes':(actual/n).stat().st_size} for n in names],'guard_implementation_failure_preserved_not_mathematical_or_API_failure':True,'no_foreign_raw_publication':True})
    for n in names+['API-execution-freeze.json']:(actual/n).chmod(0o444)
    for p in PRIVATE.iterdir():
        if p.is_file():p.chmod(0o600)
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
