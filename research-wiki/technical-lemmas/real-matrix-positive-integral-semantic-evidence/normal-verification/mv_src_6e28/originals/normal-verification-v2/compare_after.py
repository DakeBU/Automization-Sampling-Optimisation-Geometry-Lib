from pathlib import Path
import json,hashlib,zlib
B=Path('/Users/zhouhuanjian/ASTIS-GC/.astis/semantic-neutral-20261112/mv_src_6e28/normal-verification-v2');R=Path('/Users/zhouhuanjian/ASTIS-GC')
a=json.loads((B/'private/before.snapshot.private.json').read_bytes());z=json.loads((B/'private/after.snapshot.private.json').read_bytes());CELL='research-wiki/frontier-cells/ASTIS-SHARED-REAL-MATRIX-POSITIVE-INTEGRAL.json';LED='runs/substantive_advances.jsonl'
fixed=['HEAD','all_full_foreign_advance_states','all_full_discoveries','discovery_raw','index','index_stage_raw','foreign_cells']
assert all(a[k]==z[k] for k in fixed)
changed={}
for name in ['tracked','controls']:
 assert a[name].keys()==z[name].keys(),name+' pathset'
 changed[name]=[p for p in a[name] if a[name][p]!=z[name][p]]
 assert set(changed[name])<=set([CELL,LED]),name
 for p in changed[name]:
  assert a[name][p]['mode']==z[name][p]['mode']
  if name=='tracked':
   for k in ['index_mode','index_oid','stage','kind']:assert a[name][p][k]==z[name][p][k]
assert a['own_V_history_count']==0 and z['own_V_history_count']==1
raw=zlib.decompress((B/'private/blobs'/(a['advance_raw']['sha256']+'.zlib')).read_bytes());rawafter=zlib.decompress((B/'private/blobs'/(z['advance_raw']['sha256']+'.zlib')).read_bytes());append=(B/'actual-VERIFIED-append.exact.jsonl').read_bytes();assert rawafter==raw+append and len(append.splitlines())==1
v=json.loads((B/'VERIFIED-evidence.full.json').read_bytes());event=json.loads(append);assert event['evidence']==v
cb=json.loads((B/'ownC.before.exact.json').read_bytes());cz=json.loads((B/'ownC.after.exact.json').read_bytes());expected=json.loads(json.dumps(cb));expected['status']='independently_verified';expected['evidence']['independent_verification']=cz['evidence']['independent_verification'];assert cz==expected
assert cb['owner_id']==cz['owner_id'] and z['own_advance']['owner_id']==a['own_advance']['owner_id'];assert z['own_advance']['state']=='VERIFIED'
pl=json.loads((B/'inputs/actual-PROVED_LOCAL-evidence.full.json').read_bytes());assert len(pl)==20 and all(v[k]==x for k,x in pl.items())
out={'all_pass':True,'held_HEAD':z['HEAD'],'full_foreign_advances_preserved':309,'full_discoveries_and_raw_preserved':43,'all_foreign_regular_frontier_files_including_README_preserved':469,'tracked_count':len(z['tracked']),'qualified_control_count':len(z['controls']),'tracked_changed_only':changed['tracked'],'qualified_controls_changed_only':changed['controls'],'tracked_index_raw_modes_stages_unchanged':True,'all_other_tracked_bytes_modes_unchanged':True,'all_foreign_control_bytes_and_pathsets_unchanged':True,'ledger_exact_original_prefix_plus_one_line':True,'PL20_original_values_inline_unchanged':True,'only_ownedC_status_and_verification_evidence_changed':True,'owner_retained':True,'API_calls':1,'API_failures':0,'pre_V_count':0,'post_V_count':1,'private_snapshot_hashes':{'before':hashlib.sha256((B/'private/before.snapshot.private.json').read_bytes()).hexdigest(),'precall':hashlib.sha256((B/'private/precall.snapshot.private.json').read_bytes()).hexdigest(),'after':hashlib.sha256((B/'private/after.snapshot.private.json').read_bytes()).hexdigest()},'full_private_foreign_control_index_snapshots_exported':False}
with (B/'postguard-comparison.json').open('x') as f:f.write(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
