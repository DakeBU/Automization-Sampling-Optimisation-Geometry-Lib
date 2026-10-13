import datetime,hashlib,json,os
from pathlib import Path
R=Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()
canon=lambda v:json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode('utf-8')
def read(n): return json.loads((R/n).read_bytes())
def write(n,v): (R/n).write_bytes((json.dumps(v,sort_keys=True,indent=2,ensure_ascii=False)+'\n').encode('utf-8'))
def entries(ns):
 out=[]
 for n in ns:
  b=(R/n).read_bytes(); out.append({'path':n,'bytes':len(b),'raw_sha256':sha(b)})
 return out
def verify(es):
 for e in es:
  b=(R/e['path']).read_bytes(); assert len(b)==e['bytes'] and sha(b)==e['raw_sha256'],e['path']
assert not (R/'lease.json').exists()
s=read('self_manifest.json'); verify(s['artifacts'])
f=read('finalizer_result.json'); t=read('terminal_readback.json')
assert f['status']=='EXIT0' and t['status']=='EXIT0'
assert f['finalizer_pid']==t['finalizer_pid']==s['finalizer_pid']
assert t['finalizer_result_raw_sha256']==sha((R/'finalizer_result.json').read_bytes())
assert t['self_manifest_raw_sha256']==f['self_manifest_raw_sha256']==sha((R/'self_manifest.json').read_bytes())
assert t['reconstruction_payload_raw_sha256']==f['reconstruction_payload_raw_sha256']==sha((R/'reconstruction_payload.json').read_bytes())
assert t['input_pin_map_raw_sha256']==sha((R/'input_pin_map.json').read_bytes())
assert read('failures.json')['observed_failures']==[] and t['observer_failures']==[]
for i in [0,1]: assert (R.parent/f'packet{i}.json').read_bytes()==(R/f'input.packet{i}.raw.json').read_bytes()
assert (R.parent/'lease.json').read_bytes()==(R/'input.lease.raw.json').read_bytes()
assert json.loads((R.parent/'lease.json').read_bytes())['status']=='OPEN'
base=sorted({e['path'] for e in s['artifacts']}|{'self_manifest.json','finalizer_result.json','terminal_readback.json'})
assert {p.name for p in R.iterdir()}==set(base)
terminal={'schema_version':1,'kind':'terminal-layer-manifest','root':str(R),'finalizer_pid':f['finalizer_pid'],'readback_pid':t['readback_pid'],'close_pid':os.getpid(),'artifacts':entries(base),'rule':'Binds all initial files and actual foreground finalizer/self/readback evidence; native final run binds this complete manifest by RAW hash.'}
write('terminal_manifest.json',terminal)
payloadraw=(R/'reconstruction_payload.json').read_bytes(); payload=json.loads(payloadraw)
run={'schema_version':1,'kind':'native-independent-source-blind-decoder-run','run_id':'independent-decoder-67','decoder':'independent-source-blind-decoder-67','closed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'source_text_visible':False,'source_identity_visible':False,'compiler_started':False,'compilation_claimed':False,'source_verdict_claimed':False,'theorem_verdict_claimed':False,'proof_credit_claimed':False,'finalizer_pid':f['finalizer_pid'],'readback_pid':t['readback_pid'],'close_pid':os.getpid(),'foreground_phases':True,'finalizer_terminal_status':f['status'],'readback_terminal_status':t['status'],'close_terminal_status':'EXIT0 if final postclose read-only validator and process exit succeed','postclose_validator':'Read-only block in close.py after CLOSED_LAST lease write, checking all owned file bindings and whole logical run SHA.','allowed_original_inputs':[str(R.parent/'packet0.json'),str(R.parent/'packet1.json'),str(R.parent/'lease.json')],'original_input_scope':'Only the two fresh anonymous packets and local neutral OPEN lease read. No canonical directories, source identity, original source, other actor verdict, compiler, repo search or sibling evidence. Owned artifacts read solely for construction/sealing.','original_inputs_unchanged_on_close':True,'input_pin_map':read('input_pin_map.json'),'input_pin_map_raw_sha256':sha((R/'input_pin_map.json').read_bytes()),'initial_lease_preserved_path':'input.lease.raw.json','initial_lease_raw_sha256':sha((R/'input.lease.raw.json').read_bytes()),'complete_named_reconstruction_payload_path':'reconstruction_payload.json','reconstruction_payload_raw_sha256':sha(payloadraw),'reconstruction_payload_hash_rule':'SHA256 of complete named reconstruction_payload.json RAW file; no deletion, normalization or reserialization.','reconstructions':payload['reconstructions'],'reconstruction_decisions':2,'semantic_slots':payload['semantic_slots'],'observed_failures':read('failures.json'),'self_manifest_raw_sha256':sha((R/'self_manifest.json').read_bytes()),'terminal_manifest_raw_sha256':sha((R/'terminal_manifest.json').read_bytes()),'terminal_layer_path':'terminal_manifest.json','closure_layer_path':'closure_manifest.json','terminal_lease_path':'lease.json','binding_rule':'Self binds initial data/scripts/failures. Terminal binds self/finalizer/readback and all initial artifacts. Native final run binds terminal manifest. Closure binds every previous file including final run. CLOSED_LAST lease binds closure/native/self/terminal/payload and is the last owned write. No recursive terminal-lease self-hash.','canonicalization':'UTF-8 JSON; recursively sorted keys; compact comma/colon separators; ensure_ascii=false; no canonical newline.','run_hash_rule':'SHA256 of canonical complete logical final_run JSON after deleting ONLY its top-level run_sha256; no recursive or other deletion.','limits':['Two anonymous statements and their own approved contexts reconstructed separately. No source/source-correctness, theorem certification, proof or compilation claim. Literal Prop representation contributes no proof or mathematical premise. Byte/slot/readback checks establish sealed artifact consistency only.']}
run['run_sha256']=sha(canon(run)); write('final_run.json',run)
logical=dict(run); logical.pop('run_sha256'); assert sha(canon(logical))==run['run_sha256']
assert run['run_sha256']!=run['reconstruction_payload_raw_sha256']
closure_files=base+['terminal_manifest.json','final_run.json']
closure={'schema_version':1,'kind':'closure-layer-manifest','root':str(R),'close_pid':os.getpid(),'run_sha256':run['run_sha256'],'artifacts':entries(closure_files),'rule':'Binds every owned file except this manifest and terminal lease. Terminal lease binds this manifest. No recursive self-hash.'}
write('closure_manifest.json',closure)
lease={'schema_version':1,'kind':'owned-independent-decoder-terminal-lease','status':'CLOSED_LAST','last_owned_write':True,'finalizer_pid':f['finalizer_pid'],'readback_pid':t['readback_pid'],'close_pid':os.getpid(),'foreground_phases':True,'source_text_visible':False,'source_identity_visible':False,'compiler_started':False,'compilation_claimed':False,'initial_lease_raw_sha256':run['initial_lease_raw_sha256'],'initial_lease_preserved_path':'input.lease.raw.json','parent_open_lease_unchanged':True,'original_inputs_unchanged':True,'run_sha256':run['run_sha256'],'reconstruction_payload_raw_sha256':sha(payloadraw),'self_manifest_raw_sha256':sha((R/'self_manifest.json').read_bytes()),'terminal_manifest_raw_sha256':sha((R/'terminal_manifest.json').read_bytes()),'closure_manifest_raw_sha256':sha((R/'closure_manifest.json').read_bytes()),'final_run_raw_sha256':sha((R/'final_run.json').read_bytes()),'post_close_policy':'No owned writes after this lease. The postclose validator and terminal output are read-only.'}
write('lease.json',lease)
# CLOSED_LAST: read-only postclose validator; no writes below this line.
verify(read('closure_manifest.json')['artifacts'])
final=read('final_run.json'); finalhash=final.pop('run_sha256'); assert sha(canon(final))==finalhash
for name,key in [('self_manifest.json','self_manifest_raw_sha256'),('terminal_manifest.json','terminal_manifest_raw_sha256'),('closure_manifest.json','closure_manifest_raw_sha256'),('final_run.json','final_run_raw_sha256'),('reconstruction_payload.json','reconstruction_payload_raw_sha256')]: assert sha((R/name).read_bytes())==lease[key]
expected=set(closure_files)|{'closure_manifest.json','lease.json'}
assert {p.name for p in R.iterdir()}==expected
assert len(expected)==25
assert all((R/'lease.json').stat().st_mtime_ns >= (R/n).stat().st_mtime_ns for n in expected if n!='lease.json')
assert (R.parent/'lease.json').read_bytes()==(R/'input.lease.raw.json').read_bytes()
print(json.dumps({'status':'CLOSE_EXIT0','postclose_validator':'EXIT0','finalizer_pid':f['finalizer_pid'],'readback_pid':t['readback_pid'],'close_pid':os.getpid(),'run_sha256':finalhash,'reconstruction_payload_raw_sha256':sha(payloadraw),'self_manifest_raw_sha256':lease['self_manifest_raw_sha256'],'terminal_manifest_raw_sha256':lease['terminal_manifest_raw_sha256'],'closure_manifest_raw_sha256':lease['closure_manifest_raw_sha256'],'final_run_raw_sha256':lease['final_run_raw_sha256'],'lease_raw_sha256':sha((R/'lease.json').read_bytes()),'input_pin_map':run['input_pin_map'],'reconstructed_text_sha256':{r['packet_id']:r['reconstructed_text_sha256'] for r in payload['reconstructions']},'owned_artifact_count':len(expected),'reconstruction_decisions':2,'lease_status':'CLOSED_LAST','parent_open_lease_unchanged':True,'source_text_visible':False,'source_identity_visible':False,'compiler_started':False,'compilation_claimed':False,'observer_failures':[]},sort_keys=True))