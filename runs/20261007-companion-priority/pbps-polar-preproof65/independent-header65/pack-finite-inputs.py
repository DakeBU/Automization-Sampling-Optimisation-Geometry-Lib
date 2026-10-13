import json,hashlib
from pathlib import Path
O=Path(__file__).resolve().parent
def load(n):return json.loads((O/n).read_text(encoding='utf-8-sig'))
def sha(b):return hashlib.sha256(b).hexdigest()
entries=[]
for x in load('source-first-seal.json')['source_snapshot_bindings']:entries.append({'name':'source/'+Path(x['path']).name,'original_path':x['path'],'raw_snapshot':x['snapshot'],'raw_sha256':x['raw_sha256'],'lf_sha256':x['lf_sha256']})
for x in load('candidate-inputs.json')['inputs']:entries.append({'name':'candidate/'+x['name'],'original_path':x['path'],'raw_snapshot':x['raw_snapshot'],'LF_snapshot':x['lf_snapshot'],'raw_sha256':x['raw_sha256'],'lf_sha256':x['lf_sha256']})
for x in load('finite-evidence-inputs.json')['inputs']:entries.append({'name':'evidence/'+x['name'],'original_path':x['source_path'],'raw_snapshot':x['raw_snapshot'],'LF_snapshot':x['lf_snapshot'],'raw_sha256':x['raw_sha256'],'lf_sha256':x['lf_sha256'],'source_full_raw_sha256':x['source_full_raw_sha256'],'source_raw_byte_range':x.get('source_raw_byte_range')})
payload=bytearray()
for x in entries:
 b=(O/x['raw_snapshot']).read_bytes();assert sha(b)==x['raw_sha256'];lf=b.replace(b'\r\n',b'\n').replace(b'\r',b'\n');assert sha(lf)==x['lf_sha256'];x['raw_bytes']=len(b);x['lf_bytes']=len(lf);h=json.dumps({'name':x['name'],'raw_bytes':len(b),'raw_sha256':sha(b)},sort_keys=True,separators=(',',':')).encode()+b'\n';x['payload_header_byte_start']=len(payload);payload.extend(h);x['payload_body_byte_start']=len(payload);payload.extend(b);x['payload_body_byte_end_exclusive']=len(payload);payload.extend(b'\n')
(O/'complete-inputs.named.raw.payload').write_bytes(payload)
v={'schema':'header65-complete-finite-input-manifest-v1','complete_named_RAW_INPUT_payload':{'filename':'complete-inputs.named.raw.payload','raw_bytes':len(payload),'raw_sha256':sha(payload),'format':'named JSON header LF; exact RAW bytes; LF'},'inputs':entries,'total_named_inputs':len(entries),'bounded_not_recursive':True,'largest_input_bytes':max(x['raw_bytes'] for x in entries),'all_input_bytes_below_100MB':all(x['raw_bytes']<100000000 for x in entries)}
(O/'inputs.manifest.json').write_bytes((json.dumps(v,ensure_ascii=False,sort_keys=True,indent=2)+'\n').encode());print(json.dumps(v['complete_named_RAW_INPUT_payload'],sort_keys=True))
