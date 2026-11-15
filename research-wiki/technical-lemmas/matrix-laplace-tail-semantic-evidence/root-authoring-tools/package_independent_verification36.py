from pathlib import Path
import json,hashlib,subprocess
r=Path.cwd();w=r/'.astis/huanjian-gc-matrix-laplace-20261114'
n=r/'.astis/semantic-neutral-20261114/laplace_native_61e4/verification-execution-999b'
e=r/'research-wiki/technical-lemmas/matrix-laplace-tail-semantic-evidence/normal-verification/laplace_native_61e4'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
m=n/'public-safe-selected-originals.manifest.v1.json'
assert sha(m)=='26b02a40e4606e53cd1676ea0de3ee8d2a92aeb88a034e4071f721f497739d76'
x=json.loads(m.read_text());assert len(x['leaves'])==36 and x['normal_API_calls']==1
assert x['window1_actual_exit_code']==0 and x['window2_actual_exit_code']==0
outcome=json.loads((n/'normal-V-outcome.public-summary.json').read_text())
assert sha(n/'normal-V-outcome.public-summary.json')=='c39eda8a5bfb0dd694f12b1e25d13711d30e64168afb1c38be35481f8a367025'
assert outcome['original24_top_level_fields_unchanged'] is True
append=(n/'normal-V-exact-target-append.jsonl').read_bytes()
assert hashlib.sha256(append).hexdigest()=='bf3c4ab12753e6eb2a70b70f25efbca7ac23f045373a8b03155bc116935eefd4'
before=subprocess.check_output(['git','show','999b89925e95e463e0269148010f794dc27bb26a:runs/substantive_advances.jsonl'])
assert (r/'runs/substantive_advances.jsonl').read_bytes()==before+append
row=json.loads(append);assert row['event']=='transition' and row['schema_version']==4
assert row['from_state']=='PROVED_LOCAL' and row['to_state']=='VERIFIED'
assert row['worker_id']==outcome['verifier_id'] and row['evidence']['verified_commit']==outcome['verified_commit']
pl=json.loads((r/'research-wiki/technical-lemmas/matrix-laplace-tail-semantic-evidence/PROVED_LOCAL-evidence.full.json').read_text())
assert len(pl)==24 and all(row['evidence'][k]==v for k,v in pl.items())
cell=r/'research-wiki/frontier-cells/ASTIS-SHARED-REAL-MATRIX-LAPLACE-TAIL.json'
assert cell.read_bytes()==(n/'target-cell.projected.exact.json').read_bytes()
assert sha(cell)=='75ad5982cd285a92c3804fd22b5bfc66af7ba11b17ccb88b177e7ce6596d3b6d'
e.mkdir(parents=True,exist_ok=True)
selection=e/'ROOT-selected-independent-verification36.v1.json';assert not selection.exists()
selection.write_text(json.dumps({'scope':'ROOT later lossless container of36 exact independent normalV and separate target-cell projection originals. Original24 and raw OS streams/receipts/actual append remain exact. Full private guards/index/foreign maps remain excluded.','files':x['leaves']},ensure_ascii=False,indent=2)+'\n')
archive=e/'selected-independent-verification-originals36.v1.tar.gz'
subprocess.run(['python3',str(w/'lossless_allowlist_container.native-dag-v2.py'),
 '--source-base',str(n),'--manifest',str(selection),'--output-archive',str(archive),
 '--custody-json',str(e/'ROOT-independent-verification36-container-custody.v1.json')],check=True)
readable=['public-safe-selected-originals.manifest.v1.json','normal-V-outcome.public-summary.json',
 'target-cell-projection.public-summary.json','normal-V-final-payload.full.json',
 'normal-V-exact-target-append.jsonl','target-cell.projection-delta.json']
for name in readable:
    target=e/name;assert not target.exists();target.write_bytes((n/name).read_bytes())
aliases=[]
for v in x['leaves']:
    aliases.append({'original_actor_relative_path':str((n/v['path']).relative_to(r)),
      'original_absolute_path':str(n/v['path']),'archive_member':v['path'],
      'bytes':v['bytes'],'sha256':v['sha256'],
      'readable_public_copy':str((e/v['path']).relative_to(r)) if v['path'] in readable else None})
resolution={'scope':'Portable identity resolution for the original independent actor references. The exact independent cell projection and normal ledger event keep their original bytes; no status/verdict is recreated by ROOT.',
 'archive':{'file':str(archive.relative_to(r)),'bytes':archive.stat().st_size,'sha256':sha(archive)},
 'actor_selected_manifest':{'file':str((e/m.name).relative_to(r)),'sha256':sha(m)},
 'aliases':aliases,'private_guard_snapshots_not_portable_or_published':True,
 'actual_normal_API_calls':1,'ROOT_normal_V_calls':0,
 'original24_inline_unchanged':True,'no_new_build_identity_claimed':True}
(e/'ROOT-original-reference-portable-resolution.v1.json').write_text(json.dumps(resolution,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'members':36,'actual_independent_normal_V':1,'ROOT_normal_V':0,
 'exact_target_cell_projection_unchanged':True,'archive_sha256':sha(archive)}))
