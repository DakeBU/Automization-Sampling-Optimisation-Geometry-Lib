import hashlib,json,os,sys
from pathlib import Path
R=Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()
canon=lambda v:json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode('utf-8')
def read(n): return json.loads((R/n).read_bytes())
def verify(es):
 for e in es:
  b=(R/e['path']).read_bytes()
  assert len(b)==e['bytes'],e['path']+' length'
  assert sha(b)==e['raw_sha256'],e['path']+' hash'
selfm=read('self_manifest.json'); verify(selfm['artifacts'])
closure=read('closure_manifest.json'); verify(closure['artifacts'])
run=read('final_run.json'); digest=run.pop('run_sha256'); assert sha(canon(run))==digest
lease=read('lease.json'); assert lease['status']=='CLOSED_LAST'
assert lease['finalizer_pid']==run['finalizer_pid']
assert lease['run_sha256']==digest
for n,key in [('closure_manifest.json','closure_manifest_raw_sha256'),('self_manifest.json','self_manifest_raw_sha256'),('final_run.json','final_run_raw_sha256'),('reconstruction_payload.json','reconstruction_payload_raw_sha256')]:
 assert lease[key]==sha((R/n).read_bytes())
assert run['reconstruction_payload_raw_sha256']==lease['reconstruction_payload_raw_sha256']
assert run['self_manifest_raw_sha256']==lease['self_manifest_raw_sha256']
payload=read('reconstruction_payload.json'); assert run['reconstructions']==payload['reconstructions']
assert run['source_text_visible'] is False and run['source_identity_visible'] is False
assert run['compiler_started'] is False
for r in payload['reconstructions']:
 assert r['source_text_visible'] is False and r['source_identity_visible'] is False
 assert sha(r['reconstructed_theorem_text'].encode('utf-8'))==r['reconstructed_text_sha256']
 assert all(r['seven_slot_coverage'].values())
 assert set(r['seven_slot_coverage'])==set(payload['semantic_slots'])
for m in run['packet_bindings']:
 b=(R/m['raw_path']).read_bytes(); lf=b.replace(b'\r\n',b'\n').replace(b'\r',b'\n')
 p=json.loads(b); d=dict(p); d.pop('packet_sha256'); ctx=p['lean']['approved_definition_context']
 assert sha(b)==m['raw_sha256'] and sha(lf)==m['lf_sha256']
 assert (R/m['lf_path']).read_bytes()==lf
 assert sha(canon(d))==m['canonical_packet_sha256']==m['declared_packet_sha256']
 assert (R/m['canonical_packet_path']).read_bytes()==canon(d)
 assert sha(canon(p))==m['canonical_full_packet_sha256']
 assert sha(canon(ctx))==m['approved_definition_context_canonical_sha256']
 assert (R/m['approved_definition_context_canonical_path']).read_bytes()==canon(ctx)
 assert sha(p['lean']['statement'].encode('utf-8'))==m['statement_sha256']
expected={e['path'] for e in closure['artifacts']}|{'closure_manifest.json','lease.json'}
actual={p.name for p in R.iterdir()}
assert actual==expected,{'unexpected':sorted(actual-expected),'missing':sorted(expected-actual)}
assert {e['path'] for e in closure['artifacts']}=={e['path'] for e in selfm['artifacts']}|{'self_manifest.json','final_run.json'}
assert all((R/'lease.json').stat().st_mtime_ns >= (R/n).stat().st_mtime_ns for n in expected if n!='lease.json')
print(json.dumps({'status':'EXIT0','readback_pid':os.getpid(),'finalizer_pid':run['finalizer_pid'],'source_text_visible':False,'source_identity_visible':False,'compiler_started':False,'seven_slot_coverage':{r['packet_id']:r['seven_slot_coverage'] for r in payload['reconstructions']},'packet_bindings':run['packet_bindings'],'reconstructed_text_sha256':{r['packet_id']:r['reconstructed_text_sha256'] for r in payload['reconstructions']},'run_sha256':digest,'reconstruction_payload_raw_sha256':lease['reconstruction_payload_raw_sha256'],'self_manifest_raw_sha256':lease['self_manifest_raw_sha256'],'closure_manifest_raw_sha256':lease['closure_manifest_raw_sha256'],'final_run_raw_sha256':lease['final_run_raw_sha256'],'lease_raw_sha256':sha((R/'lease.json').read_bytes()),'owned_artifact_count':len(expected),'owned_lease_status':lease['status']},sort_keys=True))
sys.exit(0)