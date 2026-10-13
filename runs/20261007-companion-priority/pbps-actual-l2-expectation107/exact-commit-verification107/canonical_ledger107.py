from context107 import *
import gzip
assert head()==C
path='runs/substantive_advances.jsonl';old=git('show',BASE+':'+path);current=git('show',C+':'+path);working=(R/path).read_bytes()
events=lambda b:[json.loads(x) for x in b.splitlines() if x.strip()]
assert current.startswith(old) and current==working
added=events(current[len(old):]);assert len(added)==6 and all(x['advance_id']==ID for x in added)
assert [x['event'] for x in added]==['proposal','transition','transition','checkpoint','checkpoint','transition']
assert [added[0]['state']]+[x['to_state'] for x in added if x['event']=='transition']==['PROPOSED','CLAIMED','EXPLORING','PROVED_LOCAL']
repair=load(B/'ledger-owned-tail-EOL107.json');archive=git('show',C+':'+repair['original_archive']);original=gzip.decompress(archive)
assert sha(original)==repair['before_raw_sha256'] and sha(current)==repair['after_raw_sha256']
assert original.startswith(old) and old+original[len(old):].replace(b'\r\n',b'\n')==current
assert original.splitlines()==current.splitlines() and original[len(old):].count(b'\r\n')==6
assert repair['events']==6 and repair['committed_prefix_unchanged'] and repair['all_record_payloads_unchanged'] and repair['only_owned_advance']==ID
stage=load(B/'science-staging107.json');assert path in stage['files']
assert not any(x['raw_path']==path and x['archive_only'] for x in stage['raw_archives'])
def states(ev):
 out={}
 for x in ev:
  if x.get('event')=='proposal':out[x['advance_id']]=x['state']
  if x.get('event')=='transition':out[x['advance_id']]=x['to_state']
 return out
before=states(events(old));after=states(events(current));assert ID not in before and after[ID]=='PROVED_LOCAL'
assert {k:v for k,v in after.items() if k!=ID}==before
assert [k for k,v in after.items() if v=='STABILIZING']==['ASTIS-SA-20261011-PBPSActualPrescribedPathDensity']
save('canonical-ledger-delivery107.native.json',dict(status='PASS',verified_commit=C,baseline=BASE,canonical_path=path,old_committed_raw_sha256=sha(old),current_committed_raw_sha256=sha(current),workspace_raw_sha256=sha(working),exact_prior_committed_prefix=True,only_six107_events_appended=True,science_state='PROVED_LOCAL',all_payloads_identical_after_owned_tail_EOL_normalization=True,exact_original_archive=repair['original_archive'],original_archive_raw_sha256=sha(archive),original_decompressed_raw_sha256=sha(original),only_six_owned_CRLF_endings_changed=True,archive_only=False,all_other_advance_states_unchanged=True,sole94_stabilizing_unchanged=True,append_VERIFIED_not_yet_performed=True))
print('PASS_CANONICAL_LEDGER_DELIVERY')
