from common_v2 import *
phase=sys.argv[1];s,lb,states,cell=snapshot()
if phase=='pre':
 assert s['own_state']=='PROVED_LOCAL' and s['own_owner']==OWNER and s['own_V_events']==0 and s['own_PL_events']==1
 assert cell['status']=='proved_locally' and cell['evidence']['independent_verification']==''
 plb=(E/'actual-PROVED_LOCAL-evidence.full.json').read_bytes();pl=json.loads(plb)
 assert sha(plb)=='7e5b58b1066292ae3c5ca14534a00f4d86e3c39bd74d241916791f6a613b215e' and len(pl)==20
 assert states[TARGET]['latest_evidence']==pl
 matches=[line for line in lb.splitlines(keepends=True) if json.loads(line).get('advance_id')==TARGET and json.loads(line).get('to_state')=='PROVED_LOCAL']
 assert len(matches)==1 and sha(matches[0])=='4b7c00216d84f2a29a9431703c3aa2559da01369963b31326379326b5ebed806'
 assert matches[0]==(E/'actual-PROVED_LOCAL-append.exact.jsonl').read_bytes()
 (OUT/'actual-PROVED_LOCAL-append.original.jsonl').write_bytes(matches[0])
 (OUT/'own-cell.before.original.json').write_bytes((ROOT/CELL).read_bytes())
 write(OUT/'pre-invariants.json',s)
elif phase=='post':
 pre=json.loads((OUT/'pre-invariants.json').read_bytes());payload=json.loads((OUT/'actual-VERIFIED-evidence.full.json').read_bytes())
 for k in ['HEAD','local_main','origin_main','advances_total','foreign_full_states','discovery_full_states','discovery_ledger','all_other_tracked_files','all_regular_frontier_files_total','prior_other_regular_frontier_files_including_README','own_owner','own_state_rest_sha256','source_package_59_entries_unchanged','source_package_manifest_sha256','stabilizing_identity_summary']:
  assert s[k]==pre[k],k
 assert s['own_state']=='VERIFIED' and s['own_V_events']==1 and s['own_PL_events']==1
 assert cell['status']=='independently_verified' and cell['evidence']['independent_verification']==rel(E/'actual-VERIFIED-independent-decision.json')
 assert s['own_cell']['semantic_rest_sha256']==pre['own_cell']['semantic_rest_sha256']
 assert sha(lb[:pre['ledger']['bytes']])==pre['ledger']['sha256']
 suffix=lb[pre['ledger']['bytes']:];ev=records(suffix);assert len(ev)==1 and suffix.endswith(b'\n')
 e=ev[0];assert e['advance_id']==TARGET and e['from_state']=='PROVED_LOCAL' and e['to_state']=='VERIFIED' and e['worker_id']==WORKER and e['evidence']==payload
 assert suffix==(OUT/'actual-VERIFIED-append.original.jsonl').read_bytes() and states[TARGET]['latest_evidence']==payload
 pl=json.loads((E/'actual-PROVED_LOCAL-evidence.full.json').read_bytes());assert len(pl)==20 and all(payload[k]==v for k,v in pl.items())
 assert payload['formalizer_preseal_API_pristine'] is False and payload['preseal_exposure']['formalizer_API_pristine'] is False
 (OUT/'own-cell.after.original.json').write_bytes((ROOT/CELL).read_bytes())
 s.update({'result':'pass','normal_API_calls':1,'sole_new_ledger_event':True,'append_sha256':sha(suffix),'all_20_original_PL_fields_preserved_inline':True,'only_C_status_and_IV_pointer_changed':True,'no_full_foreign_control_snapshots_exported':True})
 write(OUT/'post-invariants.json',s)
else:raise AssertionError(phase)
print(json.dumps(s,indent=2))
