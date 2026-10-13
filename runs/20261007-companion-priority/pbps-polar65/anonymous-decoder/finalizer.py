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
assert set(base)=={'input.packet0.raw.json','input.packet0.lf.json','input.packet0.canonical.json','approved_definition_context.canonical.json','input.lease.raw.json','input.lease.lf.json','input_pin_map.json','reconstruction_payload.json','reconstruction.md','failures.json','finalizer.py','terminal_readback.py','close.py'}
payload=json.loads((R/'reconstruction_payload.json').read_bytes()); r=payload['reconstruction']
assert all(r['seven_slot_coverage'].values())
assert r['source_text_visible'] is False and r['source_identity_visible'] is False
assert sha(r['reconstructed_theorem_text'].encode('utf-8'))==r['reconstructed_text_sha256']
manifest={'schema_version':1,'kind':'self-layer-manifest','root':str(R),'finalizer_pid':os.getpid(),'artifacts':entries(base),'rule':'Binds every initial input pin, definition context, reconstruction, failure record and all three scripts. The finalizer result and terminal/closure layers bind this manifest without recursive self-hashing.'}
write('self_manifest.json',manifest)
result={'schema_version':1,'kind':'foreground-finalizer-result','status':'EXIT0','finalizer_pid':os.getpid(),'foreground':True,'self_manifest_raw_sha256':sha((R/'self_manifest.json').read_bytes()),'reconstruction_payload_raw_sha256':sha((R/'reconstruction_payload.json').read_bytes()),'source_text_visible':False,'source_identity_visible':False,'compiler_started':False,'seven_slot_coverage':r['seven_slot_coverage']}
write('finalizer_result.json',result)
print(json.dumps(result,sort_keys=True))