#!/opt/anaconda3/bin/python
import copy,hashlib,json,pathlib,subprocess,sys
sys.dont_write_bytecode=True
BASE=pathlib.Path(__file__).resolve().parent;ROOT=pathlib.Path('/Users/zhouhuanjian/ASTIS-GC')
sys.path.insert(0,str(BASE));import preservation_guard as guard
old=(guard.PRIVATE/'ledger-before.raw.jsonl').read_bytes();now=(ROOT/guard.LEDGER).read_bytes()
assert now.startswith(old)
append=(BASE/'normal-VERIFIED-append.exact.jsonl').read_bytes();assert now==old+append
event=json.loads(append);assert event['advance_id']==guard.ADV and event['to_state']=='VERIFIED'
assert event['worker_id']=='/root/cosine_gram_fresh_source_7e41d9'
states=guard.states(now)
assert states[guard.ADV]['owner_id']=='huanjian_gc_20261110_fixed_spectrum_cosine_gram'
assert states[guard.ADV]['latest_evidence']==event['evidence']
plocal=json.loads((BASE/'original-PROVED_LOCAL-event.exact.jsonl').read_text())
assert event['evidence']['original_proved_local_event']==plocal
assert event['evidence']['original_proved_local_evidence']==plocal['evidence']
allrecords=[json.loads(line) for line in now.splitlines()]
V=[r for r in allrecords if r.get('event')=='transition' and r.get('to_state')=='VERIFIED']
assert len(V)==316 and V[-1]==event
assert len([r for r in V if r['advance_id']==guard.ADV])==1
preserved=guard.verify_preserved(allow_own_append=True)
(guard.PRIVATE/'full-states-after.private.json').write_text(json.dumps(states,ensure_ascii=False,sort_keys=True)+'\n')
(BASE/'actual-normal-VERIFIED-event.json').write_text(json.dumps(event,ensure_ascii=False,indent=2)+'\n')
before=json.loads((BASE/'own-frontier-before.raw.json').read_text());after=json.loads((ROOT/guard.FRONTIER).read_text())
def diffs(a,b,prefix=''):
    if isinstance(a,dict) and isinstance(b,dict):
        out=[]
        for key in sorted(set(a)|set(b)):
            path=prefix+'.'+key if prefix else key
            if key not in a or key not in b:out.append(path)
            else:out+=diffs(a[key],b[key],path)
        return out
    return [] if a==b else [prefix]
changed=diffs(before,after)
assert changed==['evidence.integration_boundary','status'],changed
assert (ROOT/guard.FRONTIER).read_bytes()==(BASE/'own-frontier-after.raw.json').read_bytes()
current_head=subprocess.run(['git','rev-parse','HEAD'],cwd=ROOT,capture_output=True)
assert current_head.returncode==0 and current_head.stdout.decode().strip()=='7359f552e3b9bdf27c2253703d879783f331c4e9'
result={'actual_event_created_at':event['created_at'],'normal_VERIFIED_API_calls':1,
        'actual_event_sha256':hashlib.sha256(append).hexdigest(),'actual_append_bytes':len(append),
        'whole_ledger_before_bytes':len(old),'whole_ledger_after_bytes':len(now),
        'whole_ledger_before_records':len(allrecords)-1,'whole_ledger_after_records':len(allrecords),
        'whole_repo_prior_V_count':315,'whole_repo_after_V_count':len(V),
        'whole_repo_after_V_distinct_advances':len({r['advance_id'] for r in V}),
        'own_V_count':1,'foreign_and_old_events_raw_prefix_preserved':True,
        'source_actor':event['worker_id'],'original_owner_unchanged':states[guard.ADV]['owner_id'],
        'mathematical_native_checked_commit':event['evidence']['verified_commit'],
        'metadata_checked_carrier':event['evidence']['metadata_checked_commit'],
        'current_HEAD_unchanged':current_head.stdout.decode().strip(),
        'frontier_exact_changed_paths':changed,'normal_sourceV_preservation':preserved,
        'private_full_snapshots_excluded_from_portable_phase5':True,
        'private_snapshot_directory':str(guard.PRIVATE.relative_to(ROOT)),
        'all_six_reader_HOLD_remote_STABILIZING_lease_and_global_boundaries_retained':True,
        'future_post_integration_authority':'Only this same original source actor may add post_integration while preserving every original V value.'}
(BASE/'final-normal-sourceV-verification.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
