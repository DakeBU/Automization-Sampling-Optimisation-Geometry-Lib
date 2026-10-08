from pathlib import Path
import json,hashlib,runpy
r=Path('runs/20261007-companion-priority/pbps-marginal-poincare57/exposition-seal57')
j=lambda p:json.loads(Path(p).read_text(encoding='utf-8'))
H=lambda b:hashlib.sha256(b).hexdigest()
canon=lambda d:json.dumps(d,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def require_exposition():
 checks=[]
 approved=runpy.run_path('.astis/pbps-marginal-gradient51/require-locator57-2.py')['require_locators']();mappings=approved['mappings'];mapped=0
 def check(row):
  b=Path(row['path']).read_bytes();lf=b.replace(b'\r\n',b'\n')
  assert len(b)==row['bytes'] and H(b)==row['raw_sha256'] and H(lf)==row['lf_sha256'],row['path']
  if 'lf_bytes' in row:assert len(lf)==row['lf_bytes']
  checks.append(row)
 def pins(d,pointer="",allow_map=False):
  nonlocal mapped
  if isinstance(d,dict):
   if {'path','bytes','raw_sha256','lf_sha256'}<=d.keys():
    matching=[m for m in mappings if allow_map and pointer==m['json_pointer']]
    if matching:
     assert len(matching)==1 and d==matching[0]['original'];check(matching[0]['exact_raw_snapshot']);mapped+=1
    else:check(d)
   else:
    for k,v in d.items():pins(v,pointer+"/"+k,allow_map)
  elif isinstance(d,list):
   for i,v in enumerate(d):pins(v,pointer+"/"+str(i),allow_map)
 def logical(d):
  x=dict(d);h=x.pop('complete_object_sha256');assert H(canon(x))==h;return h
 names=['exposition.review.json','reviewer.exposition.run.json','lease.json','manifest.json','complete.json','verification.json','input.manifest.json','input.readbacks.json']
 v,er,el,em,ec,ev,im,ir=[j(r/n) for n in names]
 assert H((r/'lease.json').read_bytes())=='21f43b92af29555e1e9e0ee146111cd32485cba8abd41ea682553e30457d3359'
 for obj in [v,er,el,em,ec,ev,im,ir]:logical(obj);pins(obj,allow_map=(obj is ev))
 assert mapped==2
 assert er['complete_object_sha256']==el['run_COMPLETE_native_minus_complete_object_sha256']=='2c1ed4cd2583df82a85907456b18ab0708aec12c1b5cf17cf5869c81e20ca5be'
 assert v['verdict']==er['verdict']=='ACCEPT_SCOPED_DESKTOP_EXPOSITION_WITH_RETAINED_DEBT' and not v['blockers']
 assert v['independent_from_proving_writer_and_root_visual_creator'] and v['reviewer']==er['trusted_actor']==el['trusted_actor']=='/root/fresh_blind_decoder56'
 science='e8a9044ba5a945eaa4b4aecd110b63494fe6c68e';integration='f311e4296fb5295a2e56e3214d3bd2585f849dcf'
 for obj in [v,er,ec,ev]:assert obj['science_commit']==science and obj['integration_commit']==integration
 assert el['status']=='CLOSED' and all(el[k]=='CLOSED' for k in ['read','write','Python'])
 assert el['compiler']=='NOT_STARTED_CLOSED' and el['browser']=='NOT_STARTED_BY_REVIEWER_CLOSED' and el['actual_preparation_exit_code']==0 and el['finalizer_pid']==44920
 assert er['no_new_compiler_or_browser'] and er['no_separately_named_run_payload'] and er['named_payload_is_not_native_run_hash']
 assert er['input_count']==el['input_count']==ec['input_count']==im['input_count']==len(im['inputs'])==66
 assert len(em['pins'])==em['preceding_output_count']==147 and el['output_readback_count']==150
 for row in im['inputs']:
  assert Path(row['raw_snapshot']['path']).read_bytes()==Path(row['input']['path']).read_bytes()
  assert Path(row['lf_snapshot']['path']).read_bytes()==Path(row['input']['path']).read_bytes().replace(b'\r\n',b'\n')
 assert len(ev['images'])==er['independent_viewed_images']==4 and all(x['width']==1440 and x['height']==1800 for x in ev['images'])
 assert len(ev['checks'])==12 and all(x['exit_code']==0 for x in ev['checks'])
 assert (ev['registry_count'],ev['root_jobs'],ev['test_jobs'])==(498,9160,9449)
 assert ev['rendered']['proof_steps']==6 and ev['rendered']['formula_containers']==8 and ev['rendered']['all_details_initially_closed']==11 and ev['rendered']['statement_exact'] and ev['rendered']['whole_theorem_proof_exact']
 assert ec['checked12_exit0'] and ec['images4_independently_viewed'] and ec['six_formula_steps_losslessly_bound'] and ec['scoped_acceptance'] and not ec['full_reader_or_purified']
 return dict(status='NATIVE_SCOPED_EXPOSITION57_STRICTLY_ADOPTED',science_commit=science,integration_commit=integration,native_pin_checks=len(checks),run_complete_object_sha256=er['complete_object_sha256'],closed_lease_raw_sha256=H((r/'lease.json').read_bytes()),input_count=66,output_readback_count=150,independently_reviewed_operational_locator_overlay=approved,presentation_debt=v['presentation_debt'])
if __name__=='__main__':print(json.dumps(require_exposition(),ensure_ascii=False))
