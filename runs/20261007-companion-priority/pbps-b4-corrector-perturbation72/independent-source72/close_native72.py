from pathlib import Path
import json,hashlib,os,sys,traceback,datetime
sys.dont_write_bytecode=True
ROOT=Path('E:/Samplinglib');OWN=ROOT/'runs/20261007-companion-priority/pbps-b4-corrector-perturbation72/independent-source72'
def sha(b):return hashlib.sha256(b).hexdigest()
def canon(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def load(p):return json.loads(p.read_bytes())
def write(n,x):(OWN/n).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
def pin(p):
 b=p.read_bytes();lf=b.replace(b'\r\n',b'\n');return {'path':p.relative_to(OWN).as_posix(),'raw_bytes':len(b),'raw_sha256':sha(b),'lf_bytes':len(lf),'lf_sha256':sha(lf),'lf_recipe':'bytewise CRLF-to-LF only'}
def exact(p,r):
 b=p.read_bytes();assert len(b)==r['raw_bytes'] and sha(b)==r['raw_sha256'],str(p)
 lf=b.replace(b'\r\n',b'\n');assert len(lf)==r['lf_bytes'] and sha(lf)==r['lf_sha256'],str(p)
def checks():
 prior=load(OWN/'preparation.inputs.json')['inputs']
 for r in prior:exact(ROOT/r['path'],r)
 snapshots=0
 for name in ['StageB.current-inputs.manifest.json','StageB.final-current-inputs.manifest.json','StageB.overlay-history.inputs.json']:
  for r in load(OWN/name)['inputs']:
   a=(OWN/r['raw_snapshot']).read_bytes();b=(OWN/r['lf_snapshot']).read_bytes()
   assert len(a)==r['raw_bytes'] and sha(a)==r['raw_sha256'];assert b==a.replace(b'\r\n',b'\n');assert len(b)==r['lf_bytes'] and sha(b)==r['lf_sha256'];snapshots+=1
 # The final current set is checked as current; historical input snapshots are
 # not falsely required to equal canonical files replaced by approved overlay.
 for r in load(OWN/'StageB.final-current-inputs.manifest.json')['inputs']:exact(ROOT/r['path'],r)
 initial=load(OWN/'StageB.current-inputs.manifest.json')['inputs']
 changed={r['path'] for r in load(OWN/'StageB.final-current-inputs.manifest.json')['inputs'] if any(z['path']==r['path'] and z['raw_sha256']!=r['raw_sha256'] for z in initial)}
 assert len(changed)==8
 for r in initial:
  if r['path'] not in changed:exact(ROOT/r['path'],r)
 for r in load(OWN/'StageB.overlay-history.inputs.json')['inputs']:exact(ROOT/r['path'],r)
 run=load(OWN/'source72.run.json');logical=dict(run);logical.pop('run_sha256');assert sha(canon(logical))==run['run_sha256']
 for n in [0,1]:
  d=load(OWN/f'source.{n}.decision.json');ad=load(OWN/f'source.{n}.admission-fields.json')
  assert d['review_run_sha256']==run['run_sha256']==ad['native_review_run_sha256']
  assert d['verdict']=='equivalent-after-elaboration' and d['blocking_deltas']==0
  assert all(x['severity']=='informational' and set(x)=={'slot','severity','description','evidence'} for x in d['deltas'])
  assert len(d['semantic_slots'])==7
  for field in ['publication_source_proof_coverage','cell_source_proof_coverage']:
   for key in ['source_graph','source_inventory','coverage_report']:
    s=ad[field][key];assert ':' not in s and '\\' not in s and (ROOT/s).is_file()
  for key in ['evidence','run_artifact']:
   s=ad['audit_fields']['source_review'][key];assert ':' not in s and '\\' not in s and (ROOT/s).is_file()
 payload=load(OWN/'complete-named-review-decision-input-payload.json');manifest=load(OWN/'named-payload.manifest.json')
 assert payload['manifest']==manifest
 assert payload['named_manifest']['raw_sha256']==sha((OWN/'named-payload.manifest.json').read_bytes())
 for n,r in payload['named_files'].items():
  b=(OWN/n).read_bytes();assert b==r['RAW_utf8'].encode('utf-8') and sha(b)==r['RAW_sha256'] and len(b)==r['RAW_bytes']
 for r in manifest['files']:exact(ROOT/r['path'],r)
 for r in payload['finite_coverage_pins']:exact(ROOT/r['path'],r)
 assert load(OWN/'StageB.source361.coverage.json')['source_count']==361
 assert len(load(OWN/'StageB.whole494-line-coverage.json')['rows'])==494
 assert load(OWN/'StageB.exact10-BODY-formula-coverage.json')['count']==10
 assert load(OWN/'StageB.all27-obligations.decisions.json')['count']==27
 assert load(OWN/'StageB.native-schema-and-admission-checks.json')['schema_errors']==[]
 return {'RAW_LF_snapshot_pairs':snapshots,'prior_immutable_reference_pins':len(prior),'final_current_input_pins':len(load(OWN/'StageB.final-current-inputs.manifest.json')['inputs']),'initial_to_final_replaced_canonical_objects':len(changed),'whole_logical_run_sha256':run['run_sha256']}
try:
 if '--verify-only' in sys.argv:
  lease=load(OWN/'lease.final.json');manifest=load(OWN/'native.manifest.json')
  assert lease['status']=='CLOSED_LAST';assert sha((OWN/'native.manifest.json').read_bytes())==lease['manifest_RAW_sha256']
  for r in manifest['entries']:exact(OWN/r['path'],r)
  expected={r['path'] for r in manifest['entries']}|{'native.manifest.json','lease.final.json'}
  actual={p.relative_to(OWN).as_posix() for p in OWN.rglob('*') if p.is_file()};assert expected==actual
  assert len(actual)==lease['closed_file_count']
  result=checks()
  print(json.dumps({'readonly_postclose_actual_pid':os.getpid(),'exit_code':0,'owned_writes':0,'closed_file_count':len(actual),'lease_RAW_sha256':sha((OWN/'lease.final.json').read_bytes()),'manifest_RAW_sha256':sha((OWN/'native.manifest.json').read_bytes()),'manifest_entry_count':len(manifest['entries']),'checks':result},indent=2))
 else:
  assert not (OWN/'lease.final.json').exists() and not (OWN/'native.manifest.json').exists()
  result=checks()
  receipt={'actual_pid':os.getpid(),'exit_code':0,'argv':sys.argv,'background':False,'checks':result,'last_write_after_this_receipt':'native.manifest.json then lease.final.json; no writes afterward'}
  write('native-close.terminal.json',receipt)
  entries=[pin(p) for p in sorted(OWN.rglob('*')) if p.is_file()]
  manifest={'schema':'source72-whole-owned-finite-RAW-LF-manifest-v1','entry_count':len(entries),'entries':entries,'excludes_only_self_and_final_lease':True,'logical_manifest_sha256':sha(canon(entries))}
  write('native.manifest.json',manifest)
  lease={'schema':'source72-native-CLOSED-LAST-lease-v1','status':'CLOSED_LAST','closed_at_UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'actual_close_pid':os.getpid(),'terminal_exit_code':0,'owned_scope':OWN.relative_to(ROOT).as_posix(),'manifest_path':'native.manifest.json','manifest_RAW_sha256':sha((OWN/'native.manifest.json').read_bytes()),'manifest_logical_entries_sha256':manifest['logical_manifest_sha256'],'manifest_entry_count':len(entries),'closed_file_count':len(entries)+2,'count_contract':'all manifested files + native.manifest.json + this final lease; lease self hash external only','run_sha256':result['whole_logical_run_sha256'],'complete_named_payload_RAW_sha256':sha((OWN/'complete-named-review-decision-input-payload.json').read_bytes()),'last_write_contract':'THIS FILE IS THE LAST OWNED WRITE. Further commands may only read. No background processes or mutable completion markers.','old_CLOSED_and_canonical_writes':False,'native_run_hash_recipe':'delete ONLY top-level run_sha256; canonical sorted UTF8 JSON ensure_ascii=False separators comma/colon','independent_source_only':True,'verdicts':['equivalent-after-elaboration','equivalent-after-elaboration'],'blocking_deltas':[0,0],'open_boundary':'Actual H/K/r_rho/B27/B28/B4/main/fullpaper/errors/cost/composition; no SCI/VERIFIED/PURIFIED/Exposition Seal/Goal credit.'}
  write('lease.final.json',lease)
  print(json.dumps({'actual_close_pid':os.getpid(),'exit_code':0,'status':'CLOSED_LAST','closed_file_count':lease['closed_file_count'],'manifest_entry_count':len(entries),'manifest_RAW_sha256':lease['manifest_RAW_sha256'],'lease_RAW_sha256':sha((OWN/'lease.final.json').read_bytes()),'whole_logical_run_sha256':lease['run_sha256'],'complete_named_payload_RAW_sha256':lease['complete_named_payload_RAW_sha256'],'checks':result},indent=2))
except BaseException:
 traceback.print_exc();sys.exit(1)
