from pathlib import Path
import json,hashlib,os
O=Path(__file__).parent
H=lambda b:hashlib.sha256(b).hexdigest()
C=lambda d:H(json.dumps(d,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode())
def read(n):return json.loads((O/n).read_bytes())
def pin(p):
 b=p.read_bytes();return dict(name=p.name,RAW_bytes=len(b),RAW_sha256=H(b),LF_sha256=H(b.replace(b'\r\n',b'\n')))
lease=read('lease.final.json');manifest=read('owned-manifest.json');assert lease['status']=='CLOSED_LAST' and lease['last_owned_write'] and not lease['postclose_writes_permitted'];assert H((O/'owned-manifest.json').read_bytes())==lease['manifest_RAW_sha256']
files=sorted(f for f in O.iterdir() if f.is_file());assert len(files)==lease['owned_file_count']==manifest['total_owned_files_including_self_and_final_lease']
assert set(f.name for f in files)==set(r['name'] for r in manifest['regular_file_entries'])|{'owned-manifest.json','lease.final.json'}
for r in manifest['regular_file_entries']:
 b=(O/r['name']).read_bytes();assert H(b)==r['RAW_sha256'] and len(b)==r['RAW_bytes'];assert H(b.replace(b'\r\n',b'\n'))==r['LF_sha256']
assert (O/'lease.final.json').stat().st_mtime_ns>=max(f.stat().st_mtime_ns for f in files if f.name!='lease.final.json')
run=read('review-run.json');core=dict(run);del core['run_sha256'];assert C(core)==run['run_sha256']==lease['whole_logical_run_sha256']
for k in ['COMPLETE_RAW_REVIEW','COMPLETE_RAW_DECISION','SEPARATE_COMPLETE_RAW_INPUT','native_semantic_decision']:
 r=lease[k];assert H((O/r['name']).read_bytes())==r['RAW_sha256']
d=read('decision.json');assert len(d['semantic_slots'])==7 and d['review_run_sha256']==run['run_sha256'];assert d['source_coverage']['classified']==310 and d['literal_BODY_coverage']['checked']==6
print(json.dumps(dict(schema='source66-external-readonly-postclose-receipt-v1',actual_postclose_pid=os.getpid(),read_only=True,owned_writes=0,all_owned_files_checked=len(files),self_manifest_exact_bound_by_lease=True,lease_last_mtime=True,lease=pin(O/'lease.final.json'),manifest=pin(O/'owned-manifest.json'),whole_logical_run_sha256=run['run_sha256'],COMPLETE_RAW_REVIEW=lease['COMPLETE_RAW_REVIEW'],COMPLETE_RAW_DECISION=lease['COMPLETE_RAW_DECISION'],SEPARATE_COMPLETE_RAW_INPUT=lease['SEPARATE_COMPLETE_RAW_INPUT'],source_items=310,source_missing=0,BODY_regions=6,verdict=d['verdict'],source_mathematical_repair=False,full_Exposition=False,PURIFIED=False,status='CLOSED_LAST'),sort_keys=True))
