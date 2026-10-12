from context106 import *
import gzip
assert head()==C
path='runs/substantive_advances.jsonl'
old=git('show',BASE+':'+path);current=git('show',C+':'+path);working=(R/path).read_bytes()
events=lambda b:[json.loads(x) for x in b.splitlines() if x.strip()]
assert current.startswith(old), 'Canonical science ledger must retain exact prior committed prefix'
added=events(current[len(old):]);assert len(added)==4 and all(x['advance_id']==ID for x in added)
assert [added[0]['state']]+[x['to_state'] for x in added[1:]]==['PROPOSED','CLAIMED','EXPLORING','PROVED_LOCAL']
assert events(current)==events(working)
stage=load(B/'science-staging106.json');assert path in stage['files']
row=next(x for x in stage['raw_archives'] if x['raw_path']==path);assert not row['archive_only']
archive=git('show',C+':'+row['archive']);assert sha(archive)==row['archive_sha256'] and gzip.decompress(archive)==working
assert sha(current)==row['public_text_sha256'] and sha(working)==row['raw_sha256']
def states(ev):
 out={}
 for x in ev:
  if x.get('event')=='proposal':out[x['advance_id']]=x['state']
  if x.get('event')=='transition':out[x['advance_id']]=x['to_state']
 return out
before=states(events(old));after=states(events(current));assert ID not in before and after[ID]=='PROVED_LOCAL'
assert {k:v for k,v in after.items() if k!=ID}==before
assert [k for k,v in after.items() if v=='STABILIZING']==['ASTIS-SA-20261011-PBPSActualPrescribedPathDensity']
save('canonical-ledger-delivery106.native.json',dict(status='PASS',verified_commit=C,baseline=BASE,canonical_path=path,old_committed_raw_sha256=sha(old),current_committed_raw_sha256=sha(current),workspace_raw_sha256=sha(working),exact_prior_committed_prefix=True,only_four106_events_appended=True,science_state='PROVED_LOCAL',same_payloads_in_canonical_workspace_and_archive=True,archive_only=False,all_other_advance_states_unchanged=True,sole94_stabilizing_unchanged=True,append_VERIFIED_not_yet_performed=True))
print('PASS_CANONICAL_LEDGER_DELIVERY')
