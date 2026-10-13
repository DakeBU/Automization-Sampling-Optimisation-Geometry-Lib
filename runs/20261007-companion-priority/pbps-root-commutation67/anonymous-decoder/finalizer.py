import hashlib,json,os
from pathlib import Path
R=Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()
def write(n,v): (R/n).write_bytes((json.dumps(v,sort_keys=True,indent=2,ensure_ascii=False)+'\n').encode('utf-8'))
def entries(ns):
 out=[]
 for n in ns:
  b=(R/n).read_bytes(); out.append({'path':n,'bytes':len(b),'raw_sha256':sha(b)})
 return out
assert not (R/'lease.json').exists()
base=sorted(p.name for p in R.iterdir())
expected={'input.lease.raw.json','input.lease.lf.json','input_pin_map.json','reconstruction_payload.json','reconstruction.packet0.md','reconstruction.packet1.md','failures.json','finalizer.py','terminal_readback.py','close.py'}
for i in [0,1]: expected|={f'input.packet{i}.raw.json',f'input.packet{i}.lf.json',f'input.packet{i}.canonical.json',f'packet{i}.approved_definition_context.canonical.json'}
assert set(base)==expected
payload=json.loads((R/'reconstruction_payload.json').read_bytes()); recs=payload['reconstructions']; assert len(recs)==2
for r in recs:
 assert all(r['seven_slot_coverage'].values())
 assert r['source_text_visible'] is False and r['source_identity_visible'] is False
 assert sha(r['reconstructed_theorem_text'].encode('utf-8'))==r['reconstructed_text_sha256']
manifest={'schema_version':1,'kind':'self-layer-manifest','root':str(R),'finalizer_pid':os.getpid(),'artifacts':entries(base),'rule':'Binds all finite input pins, approved contexts, two reconstruction decisions, complete payload, failure record and scripts. Finalizer and terminal/closure layers bind this manifest without self-hash recursion.'}
write('self_manifest.json',manifest)
result={'schema_version':1,'kind':'foreground-finalizer-result','status':'EXIT0','finalizer_pid':os.getpid(),'foreground':True,'self_manifest_raw_sha256':sha((R/'self_manifest.json').read_bytes()),'reconstruction_payload_raw_sha256':sha((R/'reconstruction_payload.json').read_bytes()),'source_text_visible':False,'source_identity_visible':False,'compiler_started':False,'compilation_claimed':False,'seven_slot_coverage':{r['packet_id']:r['seven_slot_coverage'] for r in recs},'reconstruction_decisions':2}
write('finalizer_result.json',result)
print(json.dumps(result,sort_keys=True))