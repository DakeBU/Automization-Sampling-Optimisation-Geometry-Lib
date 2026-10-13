import hashlib,json,os
from pathlib import Path
OUT=Path(__file__).resolve().parent
def sha(b):return hashlib.sha256(b).hexdigest()
def load(name):return json.loads((OUT/name).read_text(encoding='utf-8'))
def canonical(d):return json.dumps(d,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf-8')
run=load('run.json');receipt=load('native.receipt.json');process=load('finalizer.process.receipt.json')
assert process['actual_exit_code']==0
assert sha((OUT/'finalizer.stdout.txt').read_bytes())==process['stdout_RAW_sha256']
assert sha((OUT/'finalizer.stderr.txt').read_bytes())==process['stderr_RAW_sha256']
assert not (OUT/'finalizer.stderr.txt').read_bytes()
stdout=json.loads((OUT/'finalizer.stdout.txt').read_bytes().decode('utf-8'))
assert stdout==receipt
logical=sha(canonical({k:v for k,v in run.items() if k!='run_sha256'}))
assert logical==run['run_sha256']==receipt['whole_run_sha256']==(OUT/'run.logical.sha256').read_text().strip()
assert sha((OUT/'run.json').read_bytes())==receipt['run_RAW_sha256']
assert sha((OUT/'review.payload.json').read_bytes())==run['complete_review_payload_RAW_sha256']==receipt['named_complete_payload_RAW_sha256']==(OUT/'review.payload.RAW.sha256').read_text().strip()
assert run['actual_finalizer_pid']==receipt['actual_finalizer_pid']
for n,h in run['artifacts_before_finalization'].items():assert sha((OUT/n).read_bytes())==h
print(json.dumps({'status':'ACTUAL_READ_ONLY_FOREGROUND_FINALIZER_READBACK_PASS','actual_reader_pid':os.getpid(),'finalizer_pid':receipt['actual_finalizer_pid'],'observed_finalizer_exit_code':process['actual_exit_code'],'whole_run_sha256':logical,'named_complete_payload_RAW_sha256':receipt['named_complete_payload_RAW_sha256'],'native_receipt_RAW_sha256':sha((OUT/'native.receipt.json').read_bytes()),'finalizer_stdout_RAW_sha256':process['stdout_RAW_sha256'],'all_bindings_passed':True},indent=2))
