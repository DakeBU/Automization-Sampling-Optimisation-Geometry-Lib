from pathlib import Path
import json,hashlib,runpy
r=Path('runs/20261007-companion-priority/pbps-marginal-poincare57');q=r/'repository-seal57'
j=lambda p:json.loads(Path(p).read_text(encoding='utf-8'));H=lambda b:hashlib.sha256(b).hexdigest()
canon=lambda d:json.dumps(d,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def require_repository():
 count=0
 def check(row,prefix=False):
  nonlocal count
  b=Path(row['path']).read_bytes()
  if prefix:b=b[:row['bytes']]
  lf=b.replace(b'\r\n',b'\n')
  assert len(b)==row['bytes'] and H(b)==row['raw_sha256'] and H(lf)==row['lf_sha256'],row['path']
  if 'lf_bytes' in row:assert len(lf)==row['lf_bytes'],row['path']
  count+=1
 def logical(d,key):
  x=dict(d);h=x.pop(key);assert H(canon(x))==h;return h
 p,d,l,o,n=[j(q/x) for x in ['receipt.json','run.json','lease.json','outputs.final.json','checks.json']]
 for fn,h in [('receipt.json','d1af06e20fcd6e532c7aae3d340e762e7533bb7910e209dcf7aa4aab399a949a'),('run.json','98e5a043e1498ed79d549c6ef16c6c49bcb3cd0e714b2d3623fcebfd95defc94'),('lease.json','2a8e983ffcfa6ef0f23a2d29d379bafc2579b9571ebe4e52ae9591a8f776daa9')]:assert H((q/fn).read_bytes())==h
 science='e8a9044ba5a945eaa4b4aecd110b63494fe6c68e';integration='f311e4296fb5295a2e56e3214d3bd2585f849dcf'
 for obj in [p,d,l]:assert obj['checked_science_commit']==science and obj['checked_integration_commit']==integration
 assert p['verdict']=='ACCEPT_SCOPED_NO_REPOSITORY_MATHEMATICAL_BLOCKER' and n['source_math_blockers']==[]
 assert l['status']=='CLOSED' and all(l[k]=='CLOSED' for k in ['read','write','Python']) and l['compiler']=='NOT_STARTED_CLOSED' and l['actual_foreground_exit_code']==0 and l['actual_finalizer_PID']==52436
 logical(p,'receipt_sha256');logical(l,'lease_sha256');logical(o,'content_self_sha256')
 assert logical(d,'run_sha256')==l['complete_run_minus_run_sha256']=='ea6afa122a3cc8f2240534d2d24b2a16246b10437e0a930aeb5f24b8d427b75d'
 assert H(canon(d['repository_binding_payload']))==d['repository_binding_payload_sha256']==l['repository_binding_payload_sha256']=='70652242bee066fa820313d5c5636cc298b92a78c70346b8aa557e176e279465'
 assert len(d['inputs'])==l['input_count']==3915 and len(l['outputs'])==l['output_count']==21
 for row in d['inputs']+d['actual_outputs_before_run']+l['outputs']+o['outputs']:check(row)
 for k in ['receipt','run','readback','output_manifest']:check(l[k])
 assert n['actual_pin_check_count']==len(n['actual_pin_checks'])==l['actual_raw_LF_pin_check_count']==8325
 for row in n['actual_pin_checks']:
  check(row['actual']);orig=row['original']
  if row['route']=='exact_append_only_ledger_prefix':
   assert Path(orig['path']).resolve()==Path(row['actual']['path']).resolve()==Path(row['exact_snapshot']['path']).resolve()
   assert row['exact_snapshot']==orig;check(orig,prefix=True)
  else:
   for k in ['bytes','raw_sha256','lf_sha256']:assert row['actual'][k]==orig[k],row['route']
   if row['route']=='actual_current':assert Path(orig['path']).resolve()==Path(row['actual']['path']).resolve()
   else:
    assert row['route'] in ['source_admission','decoder_original_OPEN','exact_transition'] and row['exact_snapshot']==row['actual'];check(row['exact_snapshot'])
 assert n['native_selfcheck_count']==len(n['native_selfchecks'])==l['native_complete_selfcheck_count']==67
 for row in n['native_selfchecks']:check(row['input']);assert logical(j(row['input']['path']),row['self_field'])==row['logical_sha256']
 for row in n['named_payload_checks']:
  check(row['input']);obj=j(row['input']['path']);assert H(canon(obj[row['payload_field']]))==obj[row['digest_field']]==row['logical_sha256']
 assert len(n['actual12gates'])==12
 for g in n['actual12gates']:assert g['actual_status']['exit_code']==0
 assert (n['root_jobs'],n['Tests_jobs'],n['Registry_count'])==(9160,9449,498)
 assert (n['science_entries'],n['integration_entries'],n['math_originals'],n['math_distinct_inputs'],n['source_originals'],n['source_terminal_outputs'],n['source_predecessor_outputs'])==(1923,123,602,611,614,1252,1251)
 assert n['graph_digest']=='3dd2be3f8193761d47c76292d33490f981e078746a219b41ce572808d78a92cd'
 runpy.run_path('.astis/pbps-marginal-gradient51/require-verification57.py')['require_verified']()
 return dict(status='NATIVE_SCOPED_REPOSITORY57_STRICTLY_ADOPTED',science_commit=science,integration_commit=integration,native_pin_checks=count,native_selfchecks=67,run_sha256=d['run_sha256'],repository_binding_payload_sha256=d['repository_binding_payload_sha256'],closed_lease_raw_sha256=H((q/'lease.json').read_bytes()),graph_digest=n['graph_digest'],debts=p['debts'])
if __name__=='__main__':print(json.dumps(require_repository(),ensure_ascii=False))
