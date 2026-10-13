from pathlib import Path
import json,hashlib
r=Path('runs/20261007-companion-priority/pbps-marginal-poincare57');q=r/'exposition-locator-overlay-review57'
j=lambda p:json.loads(Path(p).read_text(encoding='utf-8'));H=lambda b:hashlib.sha256(b).hexdigest();canon=lambda d:json.dumps(d,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def require_locator():
 count=0
 def check(row):
  nonlocal count
  b=Path(row['path']).read_bytes();lf=b.replace(b'\r\n',b'\n');assert len(b)==row['bytes'] and H(b)==row['raw_sha256'] and H(lf)==row['lf_sha256']
  if 'lf_bytes' in row:assert len(lf)==row['lf_bytes']
  count+=1
 def logical(obj,key):
  x=dict(obj);h=x.pop(key);assert H(canon(x))==h;return h
 p,d,l,n,o=[j(q/x) for x in ['receipt.json','run.json','lease.json','checks.json','outputs.final.json']]
 for name,h in [('receipt.json','a37a689f4866930f2d96d0442780f71d78639c9416627bdee9eaa77352b51a6c'),('run.json','d2ac41fa2910d13b459d66fc83d58547cdf21e5b9482d4f91928dce9d21ced79'),('lease.json','9158c0318b7d1634301303ee788bc9d0c1501f77ec52983dea8ef6fd1cd2b01b')]:assert H((q/name).read_bytes())==h
 assert p['verdict']=='ACCEPT_EXACT_ONE_POINTER_FULLROW_LOCATOR_MAP_ONLY' and p['reviewer']==d['reviewer']==l['actor']=='whole_math52_operational_locator57'
 assert l['status']=='CLOSED' and all(l[k]=='CLOSED' for k in ['read','write','Python']) and l['compiler']=='NOT_STARTED_CLOSED' and l['actual_finalizer_PID']==496 and l['actual_foreground_exit_code']==0
 logical(p,'receipt_sha256');logical(l,'lease_sha256');logical(o,'content_self_sha256')
 assert logical(d,'run_sha256')==l['complete_run_minus_run_sha256']=='4763cedd0f54b5143c1d9b20702d8176ea901de2bba64a7576bdaa198ac1434e'
 assert H(canon(d['operational_binding_payload']))==d['operational_binding_payload_sha256']==l['operational_binding_payload_sha256']=='138e557e25388f9f635da4d5443b2c283b40374f397d596be54ab15bea994be6'
 assert len(d['inputs'])==l['input_count']==10 and len(l['outputs'])==l['output_count']==7
 for row in d['inputs']+l['outputs']+o['outputs']:check(row)
 for k in ['receipt','run','readback']:check(l[k])
 assert len(n['native_selfchecks'])==5 and len(n['actual_raw_LF_pin_checks'])==9
 for row in n['native_selfchecks']:check(row['input']);assert logical(j(row['input']['path']),row['self_field'])==row['logical_sha256']
 for row in n['actual_raw_LF_pin_checks']:
  check(row['actual']);assert Path(row['expected']['path']).resolve()==Path(row['actual']['path']).resolve();assert all(row['expected'][k]==row['actual'][k] for k in ['bytes','raw_sha256','lf_sha256'])
 overlay=j(r/'exposition-locator-overlay57/locator-overlay.json');logical(overlay,'content_self_sha256');assert len(overlay['mappings'])==1
 m=overlay['mappings'][0];ev=j(r/'exposition-seal57/verification.json');assert m['json_pointer']==p['json_pointer']==n['json_pointer']=='/git_files/0/science_snapshot'
 assert m['original']==p['fullrow_original']==n['original_expected']==ev['git_files'][0]['science_snapshot']
 assert m['exact_raw_snapshot']==p['fullrow_replacement']==n['exact_replacement'];check(m['exact_raw_snapshot'])
 for k in ['bytes','raw_sha256','lf_bytes','lf_sha256']:assert m['original'][k]==m['exact_raw_snapshot'][k]
 assert Path(m['original']['path']).read_bytes()==Path(ev['git_files'][1]['current']['path']).read_bytes()
 assert Path(m['exact_raw_snapshot']['path']).read_bytes()==Path(ev['git_files'][0]['current']['path']).read_bytes()
 assert n['collision_is_actual_Test_bytes'] and n['no_native_rewrite_or_reclose'] and n['no_mathematical_source_statement_formula_repair']
 assert H((r/'exposition-seal57/lease.json').read_bytes())=='21f43b92af29555e1e9e0ee146111cd32485cba8abd41ea682553e30457d3359'
 return dict(mapping=m,native_pin_checks=count,run_sha256=d['run_sha256'],operational_binding_payload_sha256=d['operational_binding_payload_sha256'],receipt_path=(q/'receipt.json').as_posix())
