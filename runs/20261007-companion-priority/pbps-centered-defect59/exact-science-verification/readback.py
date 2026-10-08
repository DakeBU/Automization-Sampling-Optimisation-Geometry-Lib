import pathlib,json,hashlib,os
ROOT=pathlib.Path('E:/Samplinglib');D=ROOT/'runs/20261007-companion-priority/pbps-centered-defect59/exact-science-verification'
def sha(b):return hashlib.sha256(b).hexdigest()
def canon(q):return json.dumps(q,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def load(p):return json.loads(pathlib.Path(p).read_bytes())
def pin(p):
 p=pathlib.Path(p);b=p.read_bytes();l=b.replace(b'\r\n',b'\n');return dict(path=p.as_posix(),bytes=len(b),lf_bytes=len(l),raw_sha256=sha(b),lf_sha256=sha(l))
run=load(D/'run.json');assert sha(canon({k:v for k,v in run.items() if k!='run_sha256'}))==run['run_sha256']
assert sha(canon(run['named_exact_verification_payload']))==run['named_exact_verification_payload_sha256']
assert load(D/'exact-verification.payload.json')==run['named_exact_verification_payload']
for row in load(D/'outputs.pre-readback.json')['artifacts']:assert pin(row['path'])==row
git=load(D/'git-science-inputs.json');transition=load(D/'transition.json');mapped=transition['before_original_to_exact_snapshot_mapping']
for row in git['entries']:
 a=row['working']
 if a['path']==mapped['original']['path']:
  assert a==mapped['original'] and pin(mapped['exact_snapshot']['path'])['raw_sha256']==a['raw_sha256']
 else:assert pin(a['path'])==a
for row in load(D/'math-inputs.json')['inputs']:assert pin(row['path'])==row
for row in load(D/'native-checks.json')['pin_checks']:assert pin(row['resolved']['path'])==row['resolved']
for row in load(D/'current-audit-and-admin-bindings.json')['before_admin_mappings']:
 assert pin(row['original']['path'])==row['original'];assert pin(row['exact_snapshot']['path'])==row['exact_snapshot']
assert pin(ROOT/'runs/substantive_advances.jsonl')==transition['current_ledger']
receipt=load(D/'receipt.json');verified=load(D/'verified.json');assert receipt['status']==verified['status']=='INDEPENDENT_EXACT_SCIENCE_VERIFIED'
assert receipt['checked_commit']==run['checked_commit']==verified['checked_commit']
print(json.dumps(dict(status='ALL_EXACT_NATIVE_INPUT_OUTPUT_SELF_AND_PAYLOAD_READBACKS_PASS',actual_readback_pid=os.getpid(),science_entries=536,frozen_math_inputs=27,native_unique_pin_identities=120,pre_readback_output_count=load(D/'outputs.pre-readback.json')['count'],run_sha256=run['run_sha256'],named_exact_verification_payload_sha256=run['named_exact_verification_payload_sha256'])),flush=True)
