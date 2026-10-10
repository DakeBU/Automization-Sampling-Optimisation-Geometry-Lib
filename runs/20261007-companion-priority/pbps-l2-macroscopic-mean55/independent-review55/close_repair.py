import pathlib, json, hashlib, datetime
ROOT=pathlib.Path('E:/Samplinglib')
BASE=ROOT/'runs/20261007-companion-priority/pbps-l2-macroscopic-mean55'
OUT=BASE/'independent-review55'
PROVIDED=BASE/'source-metadata-repair55/source.repair.review.lease.json'
def sha(b): return hashlib.sha256(b).hexdigest()
def canonical(d): return json.dumps(d,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode('utf-8')
def logical(d,k): return sha(canonical({a:b for a,b in d.items() if a!=k}))
def load(p): return json.loads(pathlib.Path(p).read_bytes())
def location(s):
    p=pathlib.Path(s); return p if p.is_absolute() else ROOT/p
def rawpin(p):
    p=pathlib.Path(p); b=p.read_bytes()
    try: b.decode('utf-8'); lf=sha(b.replace(b'\r\n',b'\n'))
    except UnicodeDecodeError: lf=None
    return {'path':p.relative_to(ROOT).as_posix(),'bytes':len(b),'raw_sha256':sha(b),'lf_sha256':lf}
def verify(d,p=None):
    a=rawpin(location(p or d['path']))
    assert all(a[k]==d[k] for k in ('bytes','raw_sha256','lf_sha256') if k in d),(d,a)
def serial(d): return json.dumps(d,ensure_ascii=False,indent=2,allow_nan=False).encode('utf-8')+b'\n'
def write(p,d): pathlib.Path(p).write_bytes(serial(d))
def utc(): return datetime.datetime.now(datetime.timezone.utc).isoformat()

receipt=load(OUT/'source.1.review.json')
assert logical(receipt,'review_run_sha256')==receipt['review_run_sha256']
rootlease=load(PROVIDED)
assert rootlease['status']=='OPEN'
assert PROVIDED.read_bytes()==(OUT/'provided-opening.lease.raw.snapshot.json').read_bytes()
for d in rootlease['input_artifacts']: verify(d)
old=load(BASE/'source.0.review.json'); overlay=load(BASE/'source-metadata-repair55/overlay.json')
mapping=overlay['original_source_input_snapshot_mapping']
for d in old['input_artifacts']: verify(d,mapping.get(d['path']))
math=load(BASE/'math-freeze.json')
lookup={d['path']:d for d in old['input_artifacts']}
assert len(math['inputs'])==282
for d in math['inputs']:
    assert all(d.get(k)==lookup[d['path']].get(k) for k in ('bytes','raw_sha256','lf_sha256'))
    verify(d,mapping.get(d['path']))
own=load(OUT/'reviewer.source.repair.lease.json')
assert own['status']=='OPEN'
payload={'actor':'phase_source_reviewer_20261005','reviewer_packet_sha256':receipt['reviewer_packet_sha256'],
  'review_run_sha256':receipt['review_run_sha256'],'binding_sha256':receipt['publication_binding_sha256'],
  'metadata_operations':receipt['metadata_operations'],'historical_input_count':297,'current_input_count':321,
  'math_freeze_282_unchanged':True,'current_inputs_postverified':True,
  'source_or_math_change':False,'original_negative_immutable':True,
  'whole_math_verdict_read':False,'compiler_started':False,'canonical_mutation':False}
write(OUT/'payload.json',payload)
outputs=[rawpin(OUT/n) for n in ['source.1.review.json','checks.json','binding-payload.json',
  'helper47-115.raw.snapshot.py.txt','opening.lease.raw.snapshot.json',
  'provided-opening.lease.raw.snapshot.json','payload.json','review_repair.py','close_repair.py']]
run={'schema_version':'independent-source-repair55-run/v1','actor':'phase_source_reviewer_20261005',
  'status':'ACCEPTED_SCOPED_SOURCE_FIDELITY_AFTER_METADATA_REPAIR','opened_utc':own['opened_utc'],
  'completed_utc':utc(),'inputs':rootlease['input_artifacts'],'outputs':outputs,
  'historical_297_exact_reuse':'Two pub/cell descriptors map to exact independent before snapshots; all other295 live bytes unchanged. Wrong swapped mapping rejected.',
  'math_freeze_282_unchanged':True,'review_run_sha256':receipt['review_run_sha256'],
  'read':'CLOSED','write':'CLOSED','Python':'CLOSED','compiler':'NOT_STARTED_CLOSED',
  'whole_math_verdict_read':False,'canonical_mutation':False,
  'provided_lease_actual_path':PROVIDED.relative_to(ROOT).as_posix(),
  'run_payload_sha256':sha(canonical(payload)),
  'payload_hash_recipe':'run_payload_sha256 = SHA256 sorted compact UTF8 named payload.json object; not raw file SHA and not complete run logical SHA.',
  'run_hash_recipe':'run_sha256 = SHA256 sorted compact UTF8 entire run object minus run_sha256; ensure_ascii=False sort_keys=True separators=(comma,colon) allow_nan=False, no newline.',
  'review_hash_recipe':receipt['hash_recipe']}
run['run_sha256']=logical(run,'run_sha256')
write(OUT/'run.json',run)
assert logical(load(OUT/'run.json'),'run_sha256')==run['run_sha256']
for d in outputs: verify(d)
for d in rootlease['input_artifacts']: verify(d)
for d in old['input_artifacts']: verify(d,mapping.get(d['path']))
own.update({'status':'CLOSED','read':'CLOSED','write':'CLOSED','Python':'CLOSED',
  'compiler':'NOT_STARTED_CLOSED','compiler_started':False,'closed_utc':utc(),
  'input_artifacts':rootlease['input_artifacts'],
  'provided_opening_snapshot':rawpin(OUT/'provided-opening.lease.raw.snapshot.json'),
  'result':rawpin(OUT/'source.1.review.json'),'run':rawpin(OUT/'run.json'),
  'run_sha256':run['run_sha256'],'review_run_sha256':receipt['review_run_sha256'],
  'pre_post_inputs_match':True,
  'lease_hash_recipe':'lease_run_sha256 = SHA256 sorted compact UTF8 entire closed lease minus lease_run_sha256; no newline.'})
own['lease_run_sha256']=logical(own,'lease_run_sha256')
write(OUT/'reviewer.source.repair.lease.json',own)
assert logical(load(OUT/'reviewer.source.repair.lease.json'),'lease_run_sha256')==own['lease_run_sha256']
ownpin=rawpin(OUT/'reviewer.source.repair.lease.json')
rootlease.update({'status':'CLOSED','read_lease':'CLOSED','write_lease':'CLOSED','Python_lease':'CLOSED',
  'compiler_lease':'NOT_STARTED_CLOSED','compiler_started':False,'closed_utc':utc(),
  'independent_review_artifact':rawpin(OUT/'source.1.review.json'),
  'independent_run_artifact':rawpin(OUT/'run.json'),'independent_reviewer_closed_lease':ownpin,
  'review_run_sha256':receipt['review_run_sha256'],'independent_run_sha256':run['run_sha256'],
  'all_current_input_artifacts_pre_post_match':True,
  'closure_hash_recipe':'lease_run_sha256 = SHA256 sorted compact UTF8 entire closed lease minus lease_run_sha256; ensure_ascii=False sort_keys=True separators=(comma,colon) allow_nan=False, no newline.'})
rootlease['lease_run_sha256']=logical(rootlease,'lease_run_sha256')
rootbytes=serial(rootlease)
summary={'status':'equivalent-after-elaboration','review':rawpin(OUT/'source.1.review.json'),
  'review_run_sha256':receipt['review_run_sha256'],'run':rawpin(OUT/'run.json'),
  'run_sha256':run['run_sha256'],'run_payload_sha256':run['run_payload_sha256'],
  'own_closed_lease':ownpin,'provided_closed_lease':{
    'path':PROVIDED.relative_to(ROOT).as_posix(),'bytes':len(rootbytes),
    'raw_sha256':sha(rootbytes),'lf_sha256':sha(rootbytes)},
  'provided_lease_run_sha256':rootlease['lease_run_sha256'],
  'all_real_read_write_Python_compiler_roles':'CLOSED / NOT_STARTED_CLOSED',
  'provided_lease_final_filesystem_write':True}
assert logical(rootlease,'lease_run_sha256')==rootlease['lease_run_sha256']
# Last filesystem operation: close the provided source repair lease. No file reads or writes below.
PROVIDED.write_bytes(rootbytes)
print(json.dumps(summary,ensure_ascii=False))
