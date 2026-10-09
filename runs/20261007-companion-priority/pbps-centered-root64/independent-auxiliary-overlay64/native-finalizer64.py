from pathlib import Path
import json,hashlib,sys,os,datetime
ROOT=Path(__file__).resolve().parent
sys.stdout.reconfigure(encoding='utf-8')
def sha(b):return hashlib.sha256(b).hexdigest()
def digest(x):return sha(json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode())
def read(n):return json.loads((ROOT/n).read_bytes())
def enc(x):return (json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode()
def validate():
 run=read('review-run.json');x=dict(run);x.pop('run_sha256');assert digest(x)==run['run_sha256']
 d=read('decision.0.json');assert d.pop('review_run_sha256')==run['run_sha256'];assert d==run['native_decision']==read('decision.0.frozen.json')
 assert len(d['semantic_slots'])==7 and all(v['evidence'] and v['relation']!='not-audited' for v in d['semantic_slots'].values())
 assert d['source_statement_mathematical_repair'] is False and d['full_ExpositionSeal'] is False and d['PURIFIED'] is False
 check=read('finite-diff-checks.json');assert check==run['finite_diff_checks']
 for key in ['historical_before_pins_match_adoption','old_packet_raw_matches_original_seal','fresh_packet_hash_match','publication_binding_match','candidate_context_match_current','mathematical_source_statement_unchanged','lean_statement_unchanged','blind_reconstruction_and_decoder_packet_unchanged','generic_statement_formulae_assumptions_unchanged','all_three_generic_steps_unchanged','all_nine_actual_steps_unchanged','three_lean_hashes_match_original','peer_packet1_raw_unchanged','peer_publication_binding_unchanged','source_attribution_now_exact_background_not_printed_auxiliary','only_two_actual_mathlib_dependencies_remain']:assert check[key],key
 assert check['closed_original_folder_reopened'] is False
 for v in check['all12_literal_body_region_checks']:
  for k in ['source_hash_match','literal_code_match','excerpt_hash_match','inside_proof_body']:assert v[k]
 assert len(check['all12_literal_body_region_checks'])==12
 payload=(ROOT/check['complete_named_RAW_INPUT_payload']['path']).read_bytes();assert sha(payload)==check['complete_named_RAW_INPUT_payload']['raw_sha256']
 for v in check['input_maps']:
  assert 'independent-source64' not in Path(v['source_path']).parts
  raw=(ROOT/v['raw_snapshot']).read_bytes();lf=(ROOT/v['lf_snapshot']).read_bytes();assert sha(raw)==v['raw_sha256'];assert sha(lf)==v['lf_sha256'];assert lf==raw.replace(b'\r\n',b'\n').replace(b'\r',b'\n');assert raw==payload[v['payload_byte_start']:v['payload_byte_end_exclusive']]
 assert all(v['pass'] for v in read('negative-controls.json')['checks'])
 return {'status':'PASS','actual_validation_pid':os.getpid(),'logical_run_sha256':run['run_sha256'],'complete_named_RAW_REVIEW':{'path':'review-run.json','raw_bytes':(ROOT/'review-run.json').stat().st_size,'raw_sha256':sha((ROOT/'review-run.json').read_bytes()),'deletion':'NONE'},'complete_named_RAW_INPUT':check['complete_named_RAW_INPUT_payload'],'seven_slots':7,'literal_regions':12,'input_RAW_LF_pairs':len(check['input_maps']),'closed_original_folder_reopened':False,'source_mathematical_repair':False,'full_ExpositionSeal':False,'PURIFIED':False}
def close():
 result=validate()
 for n in ['foreground-finalizer.receipt.json','foreground-readback.receipt.json']:
  d=read(n);assert d['exit_code']==0 and d['terminal_closed'] and d['actual_foreground_pid']>0
  for k in ['stdout','stderr']:assert sha((ROOT/d[k]['relative_path']).read_bytes())==d[k]['raw_sha256']
 assert not (ROOT/'lease.final.json').exists()
 lease={'schema':'astis-independent-owned-lease-v1','state':'CLOSED_LAST','owner':'/root/independent_source64','owned_root':str(ROOT),'closed_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'actual_close_pid':os.getpid(),'logical_run_sha256':result['logical_run_sha256'],'complete_named_RAW_REVIEW':result['complete_named_RAW_REVIEW'],'complete_named_RAW_INPUT':result['complete_named_RAW_INPUT'],'owned_manifest':'full-owned-manifest.json','terminal_receipts':['foreground-finalizer.receipt.json','foreground-readback.receipt.json'],'last_owned_write':'lease.final.json','postclose_policy':'READ_ONLY; no further owned write','closed_original_folder_reopened':False,'source_statement_mathematical_repair':False,'full_ExpositionSeal':False,'PURIFIED':False}
 data=enc(lease);files=[]
 for p in sorted(ROOT.rglob('*')):
  if p.is_file():files.append({'relative_path':p.relative_to(ROOT).as_posix(),'raw_bytes':p.stat().st_size,'raw_sha256':sha(p.read_bytes())})
 files.append({'relative_path':'lease.final.json','raw_bytes':len(data),'raw_sha256':sha(data)})
 manifest={'schema':'source64-auxiliary-overlay-full-owned-manifest-v1','files':sorted(files,key=lambda x:x['relative_path']),'self_file':'full-owned-manifest.json','self_binding':'Its exact RAW hash is returned in the actual foreground close/postclose terminal output; every other owned file including the final lease is enumerated here.','includes_all_negatives_and_RAW_LF_maps':True,'write_order':'manifest first, CLOSED_LAST final lease last; read-only afterwards'}
 (ROOT/'full-owned-manifest.json').write_bytes(enc(manifest));(ROOT/'lease.final.json').write_bytes(data)
 result.update({'lease_state':'CLOSED_LAST','actual_close_pid':os.getpid(),'owned_files':len(files)+1,'manifest_raw_sha256':sha((ROOT/'full-owned-manifest.json').read_bytes()),'lease_raw_sha256':sha(data)})
 return result
def postclose():
 result=validate();m=read('full-owned-manifest.json');lease=read('lease.final.json');assert lease['state']=='CLOSED_LAST';listed={x['relative_path'] for x in m['files']};actual={p.relative_to(ROOT).as_posix() for p in ROOT.rglob('*') if p.is_file()};assert actual==listed|{'full-owned-manifest.json'}
 for x in m['files']:
  p=ROOT/x['relative_path'];assert p.stat().st_size==x['raw_bytes'] and sha(p.read_bytes())==x['raw_sha256']
 last=(ROOT/'lease.final.json').stat().st_mtime_ns;assert all(p.stat().st_mtime_ns<=last for p in ROOT.rglob('*') if p.is_file())
 result.update({'phase':'READ_ONLY_POSTCLOSE','lease_state':'CLOSED_LAST','original_close_pid':lease['actual_close_pid'],'owned_files':len(m['files'])+1,'manifest_raw_sha256':sha((ROOT/'full-owned-manifest.json').read_bytes()),'lease_raw_sha256':sha((ROOT/'lease.final.json').read_bytes()),'no_postclose_owned_writes':True})
 return result
mode=sys.argv[1]
if mode=='close':out=close()
elif mode=='postclose':out=postclose()
else:
 out=validate();out['phase']=mode
 if mode=='finalizer':(ROOT/'validation-summary.json').write_bytes(enc(out))
print(json.dumps(out,ensure_ascii=False,indent=2))
