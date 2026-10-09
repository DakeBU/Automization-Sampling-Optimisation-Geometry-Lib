from pathlib import Path
import json,hashlib,base64,os,sys,re,html
O=Path(__file__).parent
H=lambda b:hashlib.sha256(b).hexdigest()
C=lambda d:H(json.dumps(d,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode())
def read(n):return json.loads((O/n).read_bytes())
run=read('review-run.json');core=dict(run);del core['run_sha256'];assert C(core)==run['run_sha256'];d=read('primary-source-decision.json');cored=dict(d);del cored['review_run_sha256'];assert cored==run['complete_source_decision'];assert d['review_run_sha256']==run['run_sha256']
assert len(d['semantic_slots'])==7 and d['source_candidate_verdict'] is None and not d['mathematical_completion_claim'];assert d['source_coverage']['classified']==344 and d['source_coverage']['missing']==0
for v in d['semantic_slots'].values():assert v['original'] and v['reconstructed'] and v['evidence']
for row in read('review-payload-pins.json').values():
 if isinstance(row,dict) and 'RAW_sha256' in row:assert H((O/row['name']).read_bytes())==row['RAW_sha256']
for row in run['owned_pre_finalization_RAW_LF_bindings']:
 b=(O/row['name']).read_bytes();assert H(b)==row['RAW_sha256'];assert H(b.replace(b'\r\n',b'\n'))==row['LF_sha256']
inp=read('RAW-input-payload.json');assert inp==run['complete_named_RAW_INPUT_payload']
for row in inp['inputs']:assert base64.b64decode(row['complete_RAW_bytes_base64'])==(O/row['pin']['name']).read_bytes()
whole=inp['whole_primary_binding'];p=Path(whole['path']);b=p.read_bytes();assert H(b)==whole['RAW_sha256']=='d81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760'
regions=read('source-input-regions.json')['regions']
for r in regions:
 a,z=r['source_RAW_range_end_exclusive'];raw=b[a:z];assert H(raw)==r['RAW_sha256'];assert raw==(O/('source.'+r['name']+'.RAW.html')).read_bytes();assert raw.replace(b'\r\n',b'\n')==(O/('source.'+r['name']+'.LF.html')).read_bytes()
inventory=read('source-coverage-inventory.json')
for x in inventory['math_items']:
 a,z=x['source_RAW_range_end_exclusive'];assert H(b[a:z])==x['RAW_sha256'];assert x['alttext']==x['annotation_tex'];assert x['classification']
reuse=read('primary-first-process.json')['prior_source_only_reuse']
for key in ['source_inventory','source_graph','lease']:
 r=reuse[key];assert H(Path(r['path']).read_bytes())==r['RAW_sha256']
reuse66=read('finite-existing66-reuse-signatures.json')
for key in ['closed_source66_lease','closed_source66_manifest']:
 r=reuse66[key];assert H(Path(r['path']).read_bytes())==r['RAW_sha256']
for x in reuse66['existing_interfaces']:
 for key in ['module_pin','exact_existing_expanded_contract']:
  r=x[key];assert H(Path(r['path']).read_bytes())==r['RAW_sha256']
if '--close' in sys.argv:
 for label in ['finalize','readback']:
  r=read('foreground-'+label+'.receipt.json');assert r['actual_exit']==0
  for k in ['stdout','stderr']:assert H((O/r[k]['name']).read_bytes())==r[k]['RAW_sha256']
print(json.dumps(dict(schema='primary67-actual-foreground-readback-v1',actual_pid=os.getpid(),mode='close-validator' if '--close' in sys.argv else 'readback',whole_logical_run_sha256=run['run_sha256'],whole_object_deleting_ONLY_top_level_run_sha256=True,complete_RAW_REVIEW_and_DECISION_all7slots=True,complete_finite_RAW_INPUT_bytes_verified=True,all_owned_pre_finalization_files_checked=True,all344_source_RAW_and_alttext_pins_checked=True,source_regions=6,source_missing=0,closed_parents_unchanged=True,no_candidate67_seen=True,no_mathematical_completion_claim=True),sort_keys=True))
