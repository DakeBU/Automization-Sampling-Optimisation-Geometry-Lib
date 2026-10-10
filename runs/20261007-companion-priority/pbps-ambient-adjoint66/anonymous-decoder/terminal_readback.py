import hashlib,json,os
from pathlib import Path
R=Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()
canon=lambda v:json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode('utf-8')
def read(n): return json.loads((R/n).read_bytes())
def write(n,v): (R/n).write_bytes((json.dumps(v,sort_keys=True,indent=2,ensure_ascii=False)+'\n').encode('utf-8'))
assert not (R/'lease.json').exists()
selfm=read('self_manifest.json')
for e in selfm['artifacts']:
 b=(R/e['path']).read_bytes(); assert len(b)==e['bytes'] and sha(b)==e['raw_sha256']
f=read('finalizer_result.json'); assert f['status']=='EXIT0'
assert f['self_manifest_raw_sha256']==sha((R/'self_manifest.json').read_bytes())
payload=read('reconstruction_payload.json'); rec=payload['reconstruction']
assert f['reconstruction_payload_raw_sha256']==sha((R/'reconstruction_payload.json').read_bytes())
assert sha(rec['reconstructed_theorem_text'].encode('utf-8'))==rec['reconstructed_text_sha256']
assert all(rec['seven_slot_coverage'].values())
assert set(rec['seven_slot_coverage'])==set(payload['semantic_slots'])
assert rec['source_text_visible'] is False and rec['source_identity_visible'] is False
pins=read('input_pin_map.json')
assert len(pins['entries'])==3
for m in pins['entries']:
 raw=(R/m['raw_path']).read_bytes(); lf=raw.replace(b'\r\n',b'\n').replace(b'\r',b'\n')
 assert len(raw)==m['raw_bytes'] and sha(raw)==m['raw_sha256']
 assert len(lf)==m['lf_bytes'] and sha(lf)==m['lf_sha256'] and (R/m['lf_path']).read_bytes()==lf
 if m['input_name']=='packet0.json':
  p=json.loads(raw); d=dict(p); d.pop('packet_sha256'); ctx=canon(p['lean']['approved_definition_context'])
  assert sha(canon(d))==m['canonical_packet_sha256']==m['declared_packet_sha256']
  assert (R/m['canonical_packet_path']).read_bytes()==canon(d)
  assert sha(canon(p))==m['full_canonical_packet_sha256']
  assert sha(ctx)==m['approved_definition_context_canonical_sha256']
  assert (R/m['approved_definition_context_canonical_path']).read_bytes()==ctx
  assert sha(p['lean']['statement'].encode('utf-8'))==m['statement_sha256']
 else:
  assert json.loads(raw)['status']=='OPEN'
assert read('failures.json')['observed_failures']==[]
expected={e['path'] for e in selfm['artifacts']}|{'self_manifest.json','finalizer_result.json'}
assert {p.name for p in R.iterdir()}==expected
receipt={'schema_version':1,'kind':'foreground-terminal-readback','status':'EXIT0','readback_pid':os.getpid(),'finalizer_pid':f['finalizer_pid'],'foreground':True,'checked_artifact_count':len(expected),'self_manifest_raw_sha256':sha((R/'self_manifest.json').read_bytes()),'finalizer_result_raw_sha256':sha((R/'finalizer_result.json').read_bytes()),'reconstruction_payload_raw_sha256':sha((R/'reconstruction_payload.json').read_bytes()),'input_pin_map_raw_sha256':sha((R/'input_pin_map.json').read_bytes()),'seven_slot_coverage':rec['seven_slot_coverage'],'source_text_visible':False,'source_identity_visible':False,'compiler_started':False,'observer_failures':[],'limits':'Byte bindings, slot presence and fresh anonymous input linkage only; no source-fidelity verdict or proof credit.'}
write('terminal_readback.json',receipt)
print(json.dumps(receipt,sort_keys=True))