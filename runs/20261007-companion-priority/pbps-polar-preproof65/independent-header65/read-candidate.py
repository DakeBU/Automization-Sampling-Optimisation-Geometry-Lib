import os,json,hashlib,datetime
from pathlib import Path
O=Path('E:/Samplinglib/runs/20261007-companion-priority/pbps-polar-preproof65/independent-header65');R=O.parent
assert (O/'source-first-seal.json').exists()
def sha(b):return hashlib.sha256(b).hexdigest()
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
start=now();refs=[];payload=bytearray()
for n in ['header0.lean','header1.lean','header.candidate.lean','test.candidate.lean','type-candidates.json','root.type-only65.adoption.json']:
 b=(R/n).read_bytes();assert len(b)<100000000;lf=b.replace(b'\r\n',b'\n').replace(b'\r',b'\n');(O/('candidate.'+n+'.raw')).write_bytes(b);(O/('candidate.'+n+'.lf')).write_bytes(lf);h=json.dumps({'name':n,'path':(R/n).as_posix(),'raw_bytes':len(b),'raw_sha256':sha(b)},sort_keys=True,separators=(',',':')).encode()+b'\n';hs=len(payload);payload.extend(h);bs=len(payload);payload.extend(b);payload.extend(b'\n');refs.append({'path':(R/n).as_posix(),'name':n,'raw_snapshot':'candidate.'+n+'.raw','lf_snapshot':'candidate.'+n+'.lf','raw_sha256':sha(b),'lf_sha256':sha(lf),'raw_bytes':len(b),'header_byte_start':hs,'payload_body_start':bs,'payload_body_end_exclusive':bs+len(b)})
 print('\nEXACT CANDIDATE '+n+'\n'+b.decode('utf-8-sig'))
(O/'complete-candidate-inputs.named.raw.payload').write_bytes(payload)
x={'schema':'header65-candidate-inputs-v1','first_candidate_read_start_utc':start,'candidate_read_end_utc':now(),'source_first_seal_raw_sha256':sha((O/'source-first-seal.json').read_bytes()),'source_content_read_tool_chunk':'5611ef','source_seal_tool_chunk':'91e48f','inputs':refs,'complete_named_raw_input_payload':{'filename':'complete-candidate-inputs.named.raw.payload','raw_bytes':len(payload),'raw_sha256':sha(payload)}}
(O/'candidate-inputs.json').write_bytes((json.dumps(x,ensure_ascii=False,sort_keys=True,indent=2)+'\n').encode())
