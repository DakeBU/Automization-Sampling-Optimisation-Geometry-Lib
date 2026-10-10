import hashlib
import json
import os
from pathlib import Path

OUT=Path('E:/Samplinglib/.astis/decoder-63/independent')
sha=lambda b:hashlib.sha256(b).hexdigest()
canonical=lambda d:json.dumps(d,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf-8')
capture=json.loads((OUT/'capture.json').read_bytes())
hashes=json.loads((OUT/'payload.hashes.json').read_bytes())
payload=json.loads((OUT/'decoded.payload.json').read_bytes())
assert set(payload['slots'])==set(['hypotheses','definitions','domains','quantifiers','scopes','conclusions','invariants'])
assert sha((OUT/'decoded.payload.json').read_bytes())==hashes['decoded_payload_raw_sha256']
assert sha((OUT/'statement.raw.txt').read_bytes())==capture['statement_declared_sha256']
assert json.loads((OUT/'lease.json').read_bytes())['status']=='OPEN'
manifest={p.name:sha(p.read_bytes()) for p in sorted(OUT.iterdir()) if p.is_file() and p.name!='lease.json'}
run={
 'schema_version':1,'status':'NATIVE_DECODE_COMPLETED',
 'allowed_inputs':['packet0.json'],
 'input_digests':capture,
 'decoded_payload_raw_sha256':hashes['decoded_payload_raw_sha256'],
 'reconstructed_text_sha256':hashes['reconstructed_text_sha256'],
 'slots_completed':list(payload['slots']),
 'source_text_visible':False,'source_identity_visible':False,'compiler_started':False,
 'finalizer_pid':os.getpid(),
 'events':[{'event':'initial_whole_packet_and_lease_foreground_reader','pid':5164,'observed_exit_code':0},
           {'event':'whole_statement_and_approved_context_foreground_reader_completed','pid':capture['reader_pid'],'observed_exit_code':0},
           {'event':'native_finalizer_constructs_run_and_receipt','pid':os.getpid()}],
 'owned_artifacts_before_finalization':manifest,
 'manifest_layering':'Run pins prior outputs and all prewritten helpers; receipt pins run and finalizer stdout; CLOSED_LAST lease pins every completed file except its own exact-byte snapshot and self, covered by same-byte identity.',
 'logical_run_hash_encoding':'SHA256 of sorted compact UTF-8 JSON of WHOLE native.run.json object excluding ONLY top-level run_sha256',
}
run['run_sha256']=sha(canonical(run))
run_raw=(json.dumps(run,ensure_ascii=False,indent=2)+'\n').encode('utf-8')
(OUT/'native.run.json').write_bytes(run_raw)
stdout='FINALIZER_PID='+str(os.getpid())+'\nRAW_PAYLOAD_SHA256='+hashes['decoded_payload_raw_sha256']+'\nWHOLE_LOGICAL_RUN_SHA256='+run['run_sha256']+'\nNATIVE_RUN_RAW_SHA256='+sha(run_raw)+'\nFINALIZER_COMPLETED\n'
(OUT/'finalizer.stdout.txt').write_bytes(stdout.encode('utf-8'))
receipt={'status':'FINALIZER_OUTPUTS_WRITTEN','finalizer_pid':os.getpid(),
 'allowed_inputs':['packet0.json'],'decoded_payload_raw_sha256':hashes['decoded_payload_raw_sha256'],
 'whole_logical_run_sha256':run['run_sha256'],'native_run_raw_sha256':sha(run_raw),
 'owned_artifacts':dict(manifest,**{'native.run.json':sha(run_raw),'finalizer.stdout.txt':sha(stdout.encode('utf-8'))}),
 'compiler_started':False,'source_identity_visible':False,'source_text_visible':False}
(OUT/'native.receipt.json').write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8')
print(stdout,end='')
