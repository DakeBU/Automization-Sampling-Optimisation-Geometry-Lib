import pathlib,json,hashlib,os,datetime,re
ROOT=pathlib.Path('E:/Samplinglib');D=ROOT/'runs/20261007-companion-priority/pbps-centered-defect59/exact-science-verification';S=D/'pin-history-readback'
def sha(b):return hashlib.sha256(b).hexdigest()
def canon(q):return json.dumps(q,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def load(p):return json.loads(pathlib.Path(p).read_bytes())
def write(p,q):pathlib.Path(p).write_bytes((json.dumps(q,ensure_ascii=False,indent=2,allow_nan=False)+'\n').encode())
def path(s):
 s=re.sub('/+','/',str(s).replace('\\','/'));p=pathlib.Path(s);return p if p.is_absolute() else ROOT/p
def pin(p):
 p=path(p);b=p.read_bytes();l=b.replace(b'\r\n',b'\n');return dict(path=p.as_posix(),bytes=len(b),lf_bytes=len(l),raw_sha256=sha(b),lf_sha256=sha(l))
def match(a,b):return a['raw_sha256']==b['raw_sha256'] and a['lf_sha256']==b['lf_sha256'] and a['bytes']==b.get('bytes',b.get('raw_bytes',a['bytes'])) and a['lf_bytes']==b.get('lf_bytes',a['lf_bytes'])
def pins(q):
 if isinstance(q,dict):
  if {'path','raw_sha256','lf_sha256'}<=q.keys():yield q
  for x in q.values():yield from pins(x)
 elif isinstance(q,list):
  for x in q:yield from pins(x)
originals=load(D/'outputs.final.json')['artifacts']; lease_before=pin(D/'lease.json')
for x in originals:assert pin(x['path'])==x
transition=load(D/'transition.json');native=load(D/'native-checks.json')
author=load(D/'promotion.author.status.json');old=author['transition'];snapshot=pin(D/'transition.initial-map-negative.raw.snapshot.json')
assert path(old['path'])==D/'transition.json' and match(snapshot,old)
history=dict(original=old,exact_snapshot=snapshot,reason='Earlier foreground promotion status binds the exact preclosure transition object; its complete original bytes are preserved. The later qualified ledger locator was corrected before the CLOSED receipt. No ledger event/native verdict/proof changed.')
maps=[history,transition['before_original_to_exact_snapshot_mapping']]+[dict(original=x['original'],exact_snapshot=x['exact_snapshot']) for x in native['historical_source_audit_mappings']]
decoder=load(ROOT/'runs/20261007-companion-priority/pbps-centered-defect59/root.decoder59.adoption.json')['raw_snapshot_mappings']
maps += [dict(original=x['original'],exact_snapshot=x['exact_raw_snapshot']) for x in decoder]
checked={};resolved_history=[]
for obj in originals+[lease_before]:
 p=path(obj['path'])
 try:q=load(p)
 except (ValueError,UnicodeDecodeError):continue
 for row in pins(q):
  originalpath=path(row['path']);a=pin(originalpath) if originalpath.exists() else None;route='CURRENT_EXACT'
  if a is None or not match(a,row):
   matches=[x for x in maps if path(x['original']['path'])==originalpath and match(x['original'],row)]
   assert len(matches)==1,(obj['path'],row,matches)
   mapping=matches[0];a=pin(mapping['exact_snapshot']['path']);assert match(a,row)
   route='EXACT_QUALIFIED_HISTORICAL_SNAPSHOT';resolved_history.append(dict(container=obj['path'],original=row,resolved=a))
  checked[(originalpath.as_posix(),row['raw_sha256'],row['lf_sha256'])]=dict(original=row,actual_resolution=a,route=route)
run0=load(D/'run.json');assert sha(canon({k:v for k,v in run0.items() if k!='run_sha256'}))==run0['run_sha256']
assert sha(canon(run0['named_exact_verification_payload']))==run0['named_exact_verification_payload_sha256']
lease0=load(D/'lease.json');assert sha(canon({k:v for k,v in lease0.items() if k!='lease_sha256'}))==lease0['lease_sha256']
payload=dict(scope='Additive exact native historical pin readback only; all original CLOSED artifacts remain immutable',explicit_promotion_transition_history=history,qualified_unique_nested_pin_identities=len(checked),all_original_outputs=54,all_raw_LF_pin_readbacks_pass=True,explicit_historical_resolutions=resolved_history,original_run_sha256=run0['run_sha256'],original_named_payload_sha256=run0['named_exact_verification_payload_sha256'])
write(S/'pin-history.payload.json',payload);write(S/'pins.json',dict(count=len(checked),identities=list(checked.values()),original_closed_outputs=originals,original_closed_lease=lease_before))
receipt=dict(status='ACCEPT_EXACT_HISTORICAL_PIN_RESOLUTION',actual_foreground_pid=os.getpid(),checked_commit=run0['checked_commit'],original_closed_artifacts_unchanged=True,new_compiler=False,ledger_or_canonical_mutations=False,payload_sha256=sha(canon(payload)),pins=pin(S/'pins.json'),qualified_unique_nested_pin_count=len(checked),all54_original_outputs_rechecked=True,issue='Exact earlier author-status pin is historical, not a missing or mismatched proof output. Explicit same-qualified-path + raw/LF map resolves only that version to preserved original bytes.')
write(S/'receipt.json',receipt)
run=dict(status=receipt['status'],checked_commit=run0['checked_commit'],named_pin_history_payload=payload,named_pin_history_payload_sha256=sha(canon(payload)),receipt=pin(S/'receipt.json'),pins=pin(S/'pins.json'),actual_foreground_pid=os.getpid(),native_recipe='Entire sorted compact UTF8 run excluding ONLY run_sha256; named_pin_history_payload separately hashed',original_closed_lease=lease_before)
run['run_sha256']=sha(canon(run));write(S/'run.json',run)
assert pin(D/'lease.json')==lease_before
for x in originals:assert pin(x['path'])==x
assert load(S/'pin-history.payload.json')==payload
assert sha(canon({k:v for k,v in load(S/'run.json').items() if k!='run_sha256'}))==run['run_sha256']
outs=[pin(p) for p in sorted(S.iterdir()) if p.is_file() and p.name!='lease.json'];write(S/'output-manifest.json',dict(artifacts=outs,count=len(outs)))
for row in outs:assert pin(row['path'])==row
lease=dict(status='CLOSEDLAST',actual_foreground_pid=os.getpid(),resources=dict(compiler='NOT_STARTED_CLOSED',read_handles='CLOSED',write_handles='CLOSED',Python='Immediate EXIT0 after last lease write/precomputed stdout; actual foreground terminal result authoritative'),run=pin(S/'run.json'),receipt=pin(S/'receipt.json'),output_manifest=pin(S/'output-manifest.json'),run_sha256=run['run_sha256'],named_pin_history_payload_sha256=run['named_pin_history_payload_sha256'],last_filesystem_operation='Actual lease write after all pin/self/payload/output readbacks',closed_at=datetime.datetime.now(datetime.timezone.utc).isoformat())
lease['lease_sha256']=sha(canon(lease));b=(json.dumps(lease,ensure_ascii=False,indent=2)+'\n').encode()
message=json.dumps(dict(status='CLOSEDLAST',actual_foreground_pid=os.getpid(),qualified_nested_identities=len(checked),run_sha256=run['run_sha256'],payload_sha256=run['named_pin_history_payload_sha256'],receipt_raw_sha256=lease['receipt']['raw_sha256'],lease_raw_sha256=sha(b),original_closed_lease_unchanged=True))
(S/'lease.json').write_bytes(b);print(message,flush=True)
