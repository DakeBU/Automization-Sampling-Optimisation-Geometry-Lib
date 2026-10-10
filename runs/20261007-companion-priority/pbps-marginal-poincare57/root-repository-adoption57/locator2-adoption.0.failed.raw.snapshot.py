from pathlib import Path
import json,hashlib,runpy
r=Path('runs/20261007-companion-priority/pbps-marginal-poincare57');q=r/'exposition-locator-overlay-review57-2'
j=lambda p:json.loads(Path(p).read_text(encoding='utf-8'));H=lambda b:hashlib.sha256(b).hexdigest();canon=lambda d:json.dumps(d,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def require_locators():
 first=runpy.run_path('.astis/pbps-marginal-gradient51/require-locator57.py')['require_locator']();count=0
 def check(row):
  nonlocal count
  b=Path(row['path']).read_bytes();lf=b.replace(b'\r\n',b'\n');assert len(b)==row['bytes'] and H(b)==row['raw_sha256'] and H(lf)==row['lf_sha256'],row['path']
  if 'lf_bytes' in row:assert len(lf)==row['lf_bytes']
  count+=1
 def logical(obj,key):
  x=dict(obj);h=x.pop(key);assert H(canon(x))==h;return h
 p,d,l,n,o=[j(q/x) for x in ['receipt.json','run.json','lease.json','checks.json','outputs.final.json']]
 for name,h in [('receipt.json','de41ab622f902f080e83e6c877ce584cbf3090aeb084384fcc2f979a06f65b55'),('run.json','68714bad9fec47e996bf9045ff207ceee87ef9cb995547ad55058c819afd073f'),('lease.json','c8aa180f012c6871922520d82b5e9beea80309712a51c7b612bcad4861e93fa7')]:assert H((q/name).read_bytes())==h
 assert p['verdict']=='ACCEPT_EXACT_SECOND_ONE_POINTER_FULLROW_MAP_ALL_OTHER_PINS_MATCH' and p['reviewer']==d['reviewer']==l['actor']=='whole_math52_operational_locator57_2'
 assert l['status']=='CLOSED' and all(l[k]=='CLOSED' for k in ['read','write','Python']) and l['compiler']=='NOT_STARTED_CLOSED' and l['actual_finalizer_PID']==51908 and l['actual_foreground_exit_code']==0
 logical(p,'receipt_sha256');logical(l,'lease_sha256');logical(o,'content_self_sha256')
 assert logical(d,'run_sha256')==l['complete_run_minus_run_sha256']=='c5bc00e903cc6d5ffca962efcfc27061d789348e2ae23312a68becc623df3ac5'
 assert H(canon(d['operational_binding_payload']))==d['operational_binding_payload_sha256']==l['operational_binding_payload_sha256']=='552885b8a22adb4cf693e06f2ff8029fcebf9d8e11f83507fbefe31c7aa81b9e'
 assert len(d['inputs'])==l['input_count']==226 and len(l['outputs'])==l['output_count']==7
 for row in d['inputs']+l['outputs']+o['outputs']:check(row)
 for k in ['receipt','run','readback']:check(l[k])
 assert len(n['native_fullself_checks'])==n['native_fullself_count']==13 and len(n['raw_LF_pin_checks'])==n['raw_LF_pin_check_count']==849
 for row in n['native_fullself_checks']:check(row['input']);assert logical(j(row['input']['path']),row['self_field'])==row['logical_sha256']
 for row in n['raw_LF_pin_checks']:
  check(row['actual']);assert row['route']=='actual_current' and Path(row['expected']['path']).resolve()==Path(row['actual']['path']).resolve();assert all(row['expected'][k]==row['actual'][k] for k in ['bytes','raw_sha256','lf_sha256'])
 overlay=j(r/'exposition-locator-overlay57-2/locator-overlay.json');logical(overlay,'content_self_sha256');assert len(overlay['mappings'])==1
 m=overlay['mappings'][0];ev=j(r/'exposition-seal57/verification.json');assert m['json_pointer']==p['new_json_pointer']=='/git_files/2/science_snapshot'
 assert m['original']==p['new_fullrow_original']==ev['git_files'][2]['science_snapshot'];assert m['exact_raw_snapshot']==p['new_fullrow_replacement'];check(m['exact_raw_snapshot'])
 for k in ['bytes','raw_sha256','lf_bytes','lf_sha256']:assert m['original'][k]==m['exact_raw_snapshot'][k]
 assert Path(m['original']['path']).read_bytes()==Path(ev['git_files'][3]['current']['path']).read_bytes();assert Path(m['exact_raw_snapshot']['path']).read_bytes()==Path(ev['git_files'][2]['current']['path']).read_bytes()
 assert n['scanned_native_artifacts']==8 and n['unmapped_original_mismatches_exactly']==n['explicitly_approved_resolutions']==2 and n['all_other_pin_rows_match_actual'] and n['operational_only'] and n['no_source_math_or_formula_repair'] and n['no_native_mutation_or_reclose']
 check(p['first_review_unchanged']);check(n['first_review_closed_lease'])
 return dict(mappings=[first['mapping'],m],native_pin_checks=count,first_independent_adoption=first,run_sha256=d['run_sha256'],operational_binding_payload_sha256=d['operational_binding_payload_sha256'],receipt_path=(q/'receipt.json').as_posix())
