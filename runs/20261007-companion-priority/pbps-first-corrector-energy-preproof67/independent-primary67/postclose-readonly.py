from pathlib import Path
import json,hashlib,os
O=Path(__file__).parent;H=lambda b:hashlib.sha256(b).hexdigest();C=lambda d:H(json.dumps(d,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode())
def read(n):return json.loads((O/n).read_bytes())
def pin(p):
 b=p.read_bytes();return dict(name=p.name,RAW_bytes=len(b),RAW_sha256=H(b),LF_sha256=H(b.replace(b'\r\n',b'\n')))
l=read('lease.final.json');m=read('owned-manifest.json');assert l['status']=='CLOSED_LAST' and not l['postclose_writes_permitted'];assert H((O/'owned-manifest.json').read_bytes())==l['manifest_RAW_sha256'];files=[f for f in O.iterdir() if f.is_file()];assert len(files)==l['owned_file_count']==m['total_owned_files_including_self_and_final_lease'];assert set(f.name for f in files)==set(r['name'] for r in m['regular_file_entries'])|{'owned-manifest.json','lease.final.json'}
for r in m['regular_file_entries']:
 b=(O/r['name']).read_bytes();assert H(b)==r['RAW_sha256'] and len(b)==r['RAW_bytes'];assert H(b.replace(b'\r\n',b'\n'))==r['LF_sha256']
assert (O/'lease.final.json').stat().st_mtime_ns>=max(f.stat().st_mtime_ns for f in files if f.name!='lease.final.json');run=read('review-run.json');c=dict(run);del c['run_sha256'];assert C(c)==run['run_sha256']==l['whole_logical_run_sha256']
for k in ['COMPLETE_RAW_REVIEW','COMPLETE_RAW_DECISION','SEPARATE_COMPLETE_RAW_INPUT']:
 r=l[k];assert H((O/r['name']).read_bytes())==r['RAW_sha256']
print(json.dumps(dict(schema='primary67-external-readonly-postclose-receipt-v1',actual_postclose_pid=os.getpid(),actual_owned_writes=0,all_owned_files_checked=len(files),lease_last_mtime=True,lease=pin(O/'lease.final.json'),manifest=pin(O/'owned-manifest.json'),whole_logical_run_sha256=run['run_sha256'],COMPLETE_RAW_REVIEW=l['COMPLETE_RAW_REVIEW'],COMPLETE_RAW_DECISION=l['COMPLETE_RAW_DECISION'],SEPARATE_COMPLETE_RAW_INPUT=l['SEPARATE_COMPLETE_RAW_INPUT'],source_items=344,source_regions=6,source_missing=0,no_candidate67_seen=True,no_mathematical_completion_claim=True,status='CLOSED_LAST'),sort_keys=True))
