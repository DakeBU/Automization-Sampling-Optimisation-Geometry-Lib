from pathlib import Path
import json,hashlib,os
O=Path(__file__).parent;ROOT=Path('E:/Samplinglib')
H=lambda b:hashlib.sha256(b).hexdigest()
C=lambda d:H(json.dumps(d,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode())
def read(n):return json.loads((O/n).read_bytes())
assert not (O/'lease.final.json').exists()
run=read('review-run.json');core=dict(run);del core['run_sha256'];assert C(core)==run['run_sha256']
for label in ['finalize','readback']:
 r=read('foreground-'+label+'.receipt.json');assert r['actual_exit']==0 and r['observed_by_communicate'] and not r['detached']
 for k in ['stdout','stderr']:
  b=(O/r[k]['name']).read_bytes();assert H(b)==r[k]['RAW_sha256'];assert len(b)==r[k]['bytes']
 result=json.loads((O/r['stdout']['name']).read_bytes());assert result['actual_pid']==r['actual_foreground_pid'];assert result['whole_logical_run_sha256']==run['run_sha256']
for row in read('review-payload-pins.json').values():
 if isinstance(row,dict) and 'RAW_sha256' in row:assert H((O/row['name']).read_bytes())==row['RAW_sha256']
for row in run['owned_pre_finalization_RAW_LF_bindings']:assert H((O/row['name']).read_bytes())==row['RAW_sha256']
current=read('math-freeze1.metadata-overlay.RAW.json')
for row in current['current_inputs']+current['compiled_inputs_unchanged']:assert H((ROOT/row['path']).read_bytes())==row['raw_sha256']
for row in read('closed-header-representation-reuse-pins.json')['parents']:assert H(Path(row['path']).read_bytes())==row['RAW_sha256']
assert read('decision.json')['verdict']=='equivalent-after-elaboration';assert read('decision.json')['source_coverage']['missing_source_items']==0
assert not any(f.is_dir() for f in O.iterdir())
print(json.dumps(dict(schema='source66-actual-foreground-close-validator-v1',actual_pid=os.getpid(),whole_logical_run_sha256=run['run_sha256'],finalizer_and_readback_actual_EXIT0_verified=True,all_owned_pre_finalization_bindings_verified=True,all_current_inputs_stable=True,closed_parent_pins_unchanged=True,source_items=310,literal_BODY_regions=6,source_mathematical_repair=False,ready_for_CLOSED_LAST=True),sort_keys=True))
