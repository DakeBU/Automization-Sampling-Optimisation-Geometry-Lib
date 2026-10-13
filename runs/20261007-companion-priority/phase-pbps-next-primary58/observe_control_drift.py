import hashlib,json,difflib,sys
from pathlib import Path
from datetime import datetime,timezone
sys.stdout.reconfigure(encoding='utf8')
R=Path('E:/Samplinglib');O=R/'runs/20261007-companion-priority/phase-pbps-next-primary58'
def sha(b):return hashlib.sha256(b).hexdigest()
def canon(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf8')
def pin(p):
 p=Path(p).resolve();b=p.read_bytes();l=b.replace(b'\r\n',b'\n');return {'path':p.as_posix(),'bytes':len(b),'raw_sha256':sha(b),'lf_bytes':len(l),'lf_sha256':sha(l)}
allowed={'docs/companion-papers-handoff.md','website/content/samplewiki_companion_frontiers.json','research-wiki/frontier-cells/ASTIS-SHARED-gaussian-marginal-poincare.json'}
rows=json.loads((O/'input.manifest.json').read_text(encoding='utf8'))['inputs'];observations=[]
(O/'control-observations').mkdir()
def diff(a,b,p=''):
 if type(a)!=type(b):return [p]
 if isinstance(a,dict):return [q for k in sorted(set(a)|set(b)) for q in (diff(a[k],b[k],p+'/'+k) if k in a and k in b else [p+'/'+k])]
 if isinstance(a,list):return [p] if a!=b else []
 return [p] if a!=b else []
for row in rows:
 p=Path(row['actual_input']['path']);rel=p.relative_to(R).as_posix();current=pin(p)
 if current==row['actual_input']:continue
 assert rel in allowed, 'Immutable source/interface input changed: '+rel
 before=Path(row['exactraw_snapshot']['path']).read_bytes();after=p.read_bytes();q=O/'control-observations'/(p.name+'.current.exactraw.snapshot');q.write_bytes(after);ql=q.with_name(q.name+'.crlf-to-lf.snapshot');ql.write_bytes(after.replace(b'\r\n',b'\n'))
 text=''.join(difflib.unified_diff(before.decode('utf8').splitlines(True),after.decode('utf8').splitlines(True),fromfile=rel+'@original-read',tofile=rel+'@current-observation'))
 d=q.with_name(q.name+'.diff.txt');d.write_bytes(text.encode('utf8'))
 observations.append({'classification':'mutable-root-owned-serialized57-integration-control','original_actual_read_receipt':row['actual_input'],'original_exactraw_snapshot':row['exactraw_snapshot'],'original_LF_snapshot':row['crlf_to_lf_snapshot'],'current_actual_read_receipt':current,'current_exactraw_snapshot':pin(q),'current_LF_snapshot':pin(ql),'exact_text_diff':pin(d),'changed_JSON_pointers':diff(json.loads(before),json.loads(after)) if p.suffix=='.json' else None,'input_time_policy':'Both receipts are actual read-time snapshots. Live root control path may legitimately advance; verify preserved exact bytes, never silently replace original source58 input or require control state to remain historically unchanged.'})
assert len(observations)==3
x={'schema_version':1,'native_schema':'explicit-historical-control-input-observation','actor':'/root/next_primary56','observed_at_utc':datetime.now(timezone.utc).isoformat(),'original_sealing_negative':{'actual_native_exec_chunk':'bd1dd0','actual_exit_code':1,'failed_script_preserved':pin(O/'seal_diagnosis.failed.0.raw.snapshot.py'),'cause':'Actual shared handoff/execution/cell57 control updates during root serialized integration. No mathematical input drift; collection56original raw/LF snapshots retained.'},'observations':observations,'current_control_read_events':3,'strictly_current_original_inputs':53,'historical_original_control_inputs':3,'mathematical_repair':False,'source_theorem_changed':False,'parent_authorization_context':'Root explicitly confirmed serialized57 shared integration only and read-time control snapshot policy. Independent actual diffs captured; no reliance on parent assertion for byte matching.'}
x['content_self_sha256']=sha(canon(x));(O/'mutable-control-observation.json').write_bytes((json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode('utf8'))
print(json.dumps({'status':'CONTROL_DRIFT_TYPED_AND_SNAPSHOTTED','controls':3,'unchanged_other_original_inputs':53,'changed_pointers':{Path(z['current_actual_read_receipt']['path']).name:z['changed_JSON_pointers'] for z in observations}},ensure_ascii=False))
