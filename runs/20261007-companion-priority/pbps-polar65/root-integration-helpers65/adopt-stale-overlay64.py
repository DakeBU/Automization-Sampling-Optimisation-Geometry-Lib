from pathlib import Path
import hashlib,json,os
root=Path.cwd();r=root/'runs/20261007-companion-priority/pbps-centered-root64';d=r/'independent-stale-cell-overlay64'
load=lambda p:json.loads(Path(p).read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest()
lease,run,decision,manifest=[load(d/n) for n in ['lease.final.json','review-run.json','decision.json','owned-manifest.json']]
assert lease['status']=='CLOSED_LAST' and lease['last_owned_write']
assert sha(json.dumps({k:v for k,v in run.items() if k!='run_sha256'},ensure_ascii=False,sort_keys=True,separators=(',',':')).encode())==run['run_sha256']==lease['logical_run_sha256']=='1eb66a2a8d2ee654f2ec3c017f1705b621873aabf77695da9193ee34a0abdefc'
assert sha((d/'decision.json').read_bytes())=='17635f14fe001ee2045d09bfc54accd63e5841943f7b670b3c5b2c4429f231af'
assert sha((d/'review-run.json').read_bytes())=='1da80acadd01d95ac7f051711ab03de16193d2a43838806233623dafebd03acc'
assert sha((d/'owned-manifest.json').read_bytes())==lease['manifest_RAW_sha256']=='a8121bcbbbfdfe208e00b2e3521bcf28df3edf059d9dfa667ef1ef4342035d24'
assert sha((d/'lease.final.json').read_bytes())=='00c78c64a72e8cf4d8d79396fa9b15357d249c02ea4dd84de569136ba0dbaca3'
listed={x['filename'] for x in manifest['all_preclosure_owned_files']}|{'owned-manifest.json','lease.final.json'}
assert listed=={p.name for p in d.iterdir()} and len(listed)==51
for x in manifest['all_preclosure_owned_files']:
 b=(d/x['filename']).read_bytes();lf=b.replace(b'\r\n',b'\n').replace(b'\r',b'\n')
 assert len(b)==x['RAW_bytes'] and sha(b)==x['RAW_sha256'] and len(lf)==x['LF_bytes'] and sha(lf)==x['LF_sha256']
inputs=load(d/'inputs.manifest.json')['inputs'];assert len(inputs)==14
for x in inputs:
 b=Path(x['source_path']).read_bytes();raw=(d/x['raw_snapshot']).read_bytes();lf=(d/x['LF_snapshot']).read_bytes()
 assert b==raw and sha(raw)==x['raw_sha256'] and sha(lf)==x['LF_sha256']
 assert lf==raw.replace(b'\r\n',b'\n').replace(b'\r',b'\n')
assert decision['overlay_decision']=='ACCEPT_EXACT_TWO_FIELD_METADATA_OVERLAY' and decision['repairs']==[]
assert decision['approved_changed_fields']==['source_anchor','evidence.truth_boundary']
for n in ['foreground-finalizer.receipt.json','foreground-readback.receipt.json']:
 x=load(d/n);assert x['exit_code']==0 and x['foreground_waited']
out=r/'root.stale-cell-overlay64.adoption.json';assert not out.exists()
out.write_text(json.dumps(dict(status='EXACT_TWO_FIELD_OVERLAY_ACCEPTED_NOT_YET_APPLIED',actual_root_readback_pid=os.getpid(),native_whole_logical_run_sha256=run['run_sha256'],native_complete_RAW_decision_sha256=sha((d/'decision.json').read_bytes()),native_owned_files=51,finite_inputs=14,approved_fields=decision['approved_changed_fields'],canonical_applied=False,source_math_changed=False,remaining='Apply only at serialized65 stabilization; other canonical reader/purification debt remains explicit.'),indent=2)+'\n',encoding='utf-8',newline='\n')
print('PASS separate CLOSED overlay64:51 owned,14 finite inputs,exact2 fields; canonical untouched.')
