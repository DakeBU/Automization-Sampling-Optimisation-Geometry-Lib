from pathlib import Path
import json,hashlib,zlib
B=Path(__file__).resolve().parent;R=Path('/Users/zhouhuanjian/ASTIS-GC')
def rd(p):return json.loads(p.read_bytes())
def sha(b):return hashlib.sha256(b).hexdigest()
a=rd(B/'private/before.snapshot.private.json');z=rd(B/'private/after.snapshot.private.json');CELL='research-wiki/frontier-cells/ASTIS-SW-GAUSSIAN-COMPLEXITY-source-matrix-variance.json';LED='runs/substantive_advances.jsonl';S='research-wiki/frontier-cells/ASTIS-SHARED-REAL-MATRIX-POSITIVE-INTEGRAL.json'
fixed=['HEAD','all_full_foreign_advance_states','all_full_discoveries','discovery_raw','index','index_stage_raw','foreign_cells'];assert all(a[k]==z[k] for k in fixed)
changed={}
for name in ['tracked','controls']:
 assert a[name].keys()==z[name].keys(),name+' pathset'
 changed[name]=[p for p in a[name] if a[name][p]!=z[name][p]]
 assert set(changed[name])<=set([CELL,LED]),name
 for p in changed[name]:
  assert a[name][p]['mode']==z[name][p]['mode']
  if name=='tracked':
   for k in ['index_mode','index_oid','stage','kind']:assert a[name][p][k]==z[name][p][k]
assert set(changed['tracked'])==set([CELL,LED]);assert a['own_V_history_count']==0 and z['own_V_history_count']==1
assert a['foreign_cells'][S]['sha256']==z['foreign_cells'][S]['sha256']=='5918990bf0a5fc8c1da2522bf8d02d456dbe443fa0d4eaf9bd56322900533138'
raw=zlib.decompress((B/'private/blobs'/(a['advance_raw']['sha256']+'.zlib')).read_bytes());rawafter=zlib.decompress((B/'private/blobs'/(z['advance_raw']['sha256']+'.zlib')).read_bytes());append=(B/'actual-VERIFIED-append.exact.jsonl').read_bytes();assert rawafter==raw+append and len(append.splitlines())==1
for adv,want in [('ASTIS-SA-20261112-RealMatrixPositiveIntegral','24cc7ea161d32a42a78e3b2e4d10a091faffe604bb1d1c419ee4b943d6d1ab78')]:
 lines=[l for l in raw.splitlines(keepends=True) if l.strip() and json.loads(l).get('advance_id')==adv and json.loads(l).get('to_state')=='VERIFIED'];assert len(lines)==1 and sha(lines[0])==want
pllines=[l for l in raw.splitlines(keepends=True) if l.strip() and json.loads(l).get('advance_id')=='ASTIS-SA-20261112-GaussianComplexitySourceMatrixVariance' and json.loads(l).get('to_state')=='PROVED_LOCAL'];assert len(pllines)==1 and sha(pllines[0])=='011b52b7b0b53b29544512a44923d8991530b293025f224c2ec1b067eb4e20c6'
v=rd(B/'VERIFIED-evidence.final.full.json');event=json.loads(append);assert event['evidence']==v
cb=rd(B/'ownC.before.exact.json');cz=rd(B/'ownC.after.exact.json');expected=json.loads(json.dumps(cb));expected['status']='independently_verified'
for k in ['independent_verification','independent_verification_details']:expected['evidence'][k]=cz['evidence'][k]
assert cz==expected and isinstance(cz['evidence']['independent_verification'],str) and bool(cz['evidence']['independent_verification'].strip())
assert cb['owner_id']==cz['owner_id'] and z['own_advance']['owner_id']==a['own_advance']['owner_id'];assert z['own_advance']['state']=='VERIFIED'
pl=rd(B/'inputs/actual-PROVED_LOCAL-evidence.full.json');assert len(pl)==21 and all(v[k]==x for k,x in pl.items());assert rd(B/'actual-postwrite-fullfrontier-schema-check.json')['errors']==[]
out={'all_pass':True,'held_HEAD':z['HEAD'],'full_foreign_advances_preserved':309,'full_discoveries_and_raw_preserved':43,'all_foreign_regular_frontier_files_including_README_preserved':469,'tracked_count':len(z['tracked']),'qualified_historical_and_control_count':len(z['controls']),'tracked_changed_only':changed['tracked'],'qualified_controls_changed_only':changed['controls'],'tracked_index_raw_modes_stages_unchanged':True,'all_other_tracked_bytes_modes_unchanged':True,'all_foreign_control_bytes_and_pathsets_unchanged':True,'ledger_exact_original_prefix_plus_one_line':True,'PL21_original_values_inline_unchanged':True,'only_ownedC_status_and_required_STRING_plus_details_verification_evidence_changed':True,'actual_postwrite_fullfrontier_schema_errors':0,'owner_retained':True,'foreign_S_exact5918990b_preserved':True,'foreign_S_original_normalV_append24cc_preserved':True,'originalR9_PL_append011b_preserved':True,'API_calls':1,'API_failures':0,'pre_V_count':0,'post_V_count':1,'private_snapshot_hashes':{label:sha((B/'private'/(label+'.snapshot.private.json')).read_bytes()) for label in ['before','precall','after']},'full_private_foreign_control_index_snapshots_exported':False}
with (B/'postguard-comparison.json').open('x') as f:f.write(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
