from pathlib import Path
import gzip,hashlib,json,os
r=Path('runs/20261007-companion-priority/pbps-reflection-intertwining69')
o=r/'independent-native-transport69'
load=lambda p:json.loads(Path(p).read_bytes())
sha=lambda b:hashlib.sha256(b).hexdigest()
canonical=lambda x:json.dumps(x,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()
l=load(o/'lease.final.json');m=load(o/'manifest.final.json');d=load(o/'decision.json')
assert sha((o/'lease.final.json').read_bytes())=='fced5063fc3e97e457e97e838eda6b0e72ba534718cb9c560a4d8ed25da12f94'
assert l['status']=='CLOSED_LAST' and l['last_owned_write'] and l['owner']=='/root/independent_primary69'
assert sha((o/'manifest.final.json').read_bytes())==l['manifest_RAW_sha256']=='4456a43306393738ec0db7baa9b558d1d2f4a0c4727e824005507e352a220072'
rows=m['entries'];assert len(rows)==17 and sha(canonical(rows))==l['finite_owned_closure_sha256']
assert {p.name for p in o.iterdir() if p.is_file()}=={z['name'] for z in rows}|{'manifest.final.json','lease.final.json'}
last=(o/'lease.final.json').stat().st_mtime_ns
for z in rows:
 p=o/z['name'];b=p.read_bytes();assert len(b)==z['RAW_bytes'] and sha(b)==z['RAW_sha256']
 assert len(b.replace(b'\r\n',b'\n'))==z['LF_bytes'] and sha(b.replace(b'\r\n',b'\n'))==z['LF_sha256']
 assert p.stat().st_mtime_ns<=last
run=load(o/'review-run.json');h=run.pop('run_sha256');assert sha(canonical(run))==h==l['whole_logical_run_sha256']
assert sha((o/'decision.json').read_bytes())==l['decision_RAW_sha256']=='f8e40f74be3e07ee9a868ad194ee81dd0f6583a4a77ead68ddbaadbd5aacf914'
assert d['verdict']=='ACCEPT_EXACT_GZIP_TRANSPORT_ONLY' and d['old_native_paths_sizes_hashes_mtimes_unchanged']
t=load(r/'integration69/native-transport69/manifest.json')
packed=Path(t['transport_path']).read_bytes();assert sha(packed)==t['transport_RAW_sha256']==d['transport_RAW_sha256']
raw=gzip.decompress(packed);assert sha(raw)==t['original_RAW_sha256']==d['original_RAW_sha256']
assert len(raw)==t['original_RAW_bytes']==167233478 and raw==Path(t['original_path']).read_bytes()
assert Path(d['materialized_RAW_path']).read_bytes()==raw
assert sha((r/'independent-repository-reader69/lease.final.json').read_bytes())==t['native_CLOSED_lease_RAW_sha256']
assert not d['Git_RAW_object_identity_for_oversized_file'] and not d['original_close_chronology_replayed'] and not d['new_math_or_source_admission']
p=r/'root.native-transport69.adoption.json';assert not p.exists()
p.write_text(json.dumps(dict(accepted_exact_transport=True,actual_root_PID=os.getpid(),
 native_owned_count=19,native_lease_RAW_sha256=sha((o/'lease.final.json').read_bytes()),
 whole_logical_run_sha256=h,exact_oversized_exclusion=t['original_path'],
 original_RAW_sha256=t['original_RAW_sha256'],transport_RAW_sha256=t['transport_RAW_sha256'],
 native_trees_mutated=False,Git_RAW_identity=False,chronology_replayed=False,new_math_or_source_admission=False),indent=2)+'\n',encoding='utf-8',newline='\n')
print('PASS independent CLOSED19 exact gzip transport adopted; original CLOSED335 and all167233478 RAW bytes retained.')
