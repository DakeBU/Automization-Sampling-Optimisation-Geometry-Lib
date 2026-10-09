import hashlib
import json
import os
from pathlib import Path

BASE = Path('E:/Samplinglib/.astis/decoder-63')
OUT = BASE / 'independent'
OUT.mkdir(exist_ok=True)
sha = lambda b: hashlib.sha256(b).hexdigest()
raw = (BASE / 'packet0.json').read_bytes()
parent = (BASE / 'lease.json').read_bytes()
packet = json.loads(raw)
statement = packet['lean']['statement'].encode('utf-8')
context = packet['lean']['approved_definition_context']
context_bytes = json.dumps(context, ensure_ascii=False, separators=(',', ':')).encode('utf-8')
assert sha(statement) == packet['lean']['statement_sha256']
(OUT / 'packet0.raw.json').write_bytes(raw)
(OUT / 'parent-lease.open.raw.json').write_bytes(parent)
(OUT / 'statement.raw.txt').write_bytes(statement)
(OUT / 'statement.lf.txt').write_bytes(statement.replace(b'\r\n', b'\n'))
(OUT / 'approved-context.canonical.json').write_bytes(context_bytes)
capture = {
    'reader_pid': os.getpid(),
    'packet_raw_sha256': sha(raw),
    'packet_lf_sha256': sha(raw.replace(b'\r\n', b'\n')),
    'packet_declared_sha256': packet.get('packet_sha256'),
    'statement_raw_sha256': sha(statement),
    'statement_lf_sha256': sha(statement.replace(b'\r\n', b'\n')),
    'statement_declared_sha256': packet['lean']['statement_sha256'],
    'context_sha256': sha(context_bytes),
    'context_hash_encoding': 'UTF-8 compact JSON list, ensure_ascii=False, separators=(comma,colon)',
    'context_declared_sha256': packet['lean'].get('context_sha256'),
    'context_declared_sha256_status': 'not supplied in anonymous packet',
    'parent_lease_open_raw_sha256': sha(parent),
    'compiler_started': False,
    'source_text_visible': False,
    'source_identity_visible': False,
}
lease = {'status':'OPEN','allowed_inputs':['packet0.json'],'source_text_visible':False,
         'source_identity_visible':False,'compiler_started':False,
         'parent_lease_open_raw_sha256':sha(parent)}
(OUT / 'lease.json').write_text(json.dumps(lease, indent=2)+'\n', encoding='utf-8')
(OUT / 'capture.json').write_text(json.dumps(capture, indent=2)+'\n', encoding='utf-8')
output = 'READER_PID='+str(os.getpid())+'\nCAPTURE_BEGIN\n'+json.dumps(capture,indent=2)+'\nCAPTURE_END\nWHOLE_STATEMENT_BEGIN\n'+statement.decode('utf-8')+'\nWHOLE_STATEMENT_END\nWHOLE_APPROVED_CONTEXT_BEGIN\n'+json.dumps(context,ensure_ascii=False,indent=2)+'\nWHOLE_APPROVED_CONTEXT_END\nREADER_COMPLETED\n'
(OUT / 'reader.stdout.txt').write_bytes(output.encode('utf-8'))
print(output,end='')
