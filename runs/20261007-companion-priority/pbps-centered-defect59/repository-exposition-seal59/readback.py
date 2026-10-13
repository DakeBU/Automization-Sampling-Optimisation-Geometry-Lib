import pathlib,json,hashlib,os
D=pathlib.Path('E:/Samplinglib/runs/20261007-companion-priority/pbps-centered-defect59/repository-exposition-seal59')
def sha(b):return hashlib.sha256(b).hexdigest()
def canon(q):return json.dumps(q,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def load(p):return json.loads(pathlib.Path(p).read_bytes())
def check(row):
 b=pathlib.Path(row['path']).read_bytes();l=b.replace(b'\r\n',b'\n');assert len(b)==row['bytes'] and len(l)==row['lf_bytes'] and sha(b)==row['raw_sha256'] and sha(l)==row['lf_sha256']
inputs=load(D/'input.manifest.json');assert len(inputs['artifacts'])==inputs['count']
for x in inputs['artifacts']:check(x)
q=load(D/'run.json');assert sha(canon({k:v for k,v in q.items() if k!='run_sha256'}))==q['run_sha256'];assert sha(canon(q['named_repository_exposition_payload']))==q['named_repository_exposition_payload_sha256']
assert load(D/'payload.json')==q['named_repository_exposition_payload']
check(q['receipt']);check(q['input_manifest'])
r=load(D/'receipt.json');assert r['named_repository_exposition_payload_sha256']==q['named_repository_exposition_payload_sha256']
for x in r['evidence']+[r['inputs'],r['payload']]:check(x)
out=dict(status='ACTUAL_RAW_LF_AND_COMPLETE_RUN_PAYLOAD_READBACK_PASS',actual_pid=os.getpid(),input_count=inputs['count'],run_sha256=q['run_sha256'],named_repository_exposition_payload_sha256=q['named_repository_exposition_payload_sha256'])
(D/'readback.json').write_bytes((json.dumps(out,ensure_ascii=False,indent=2)+'\n').encode());print(json.dumps(out),flush=True)
