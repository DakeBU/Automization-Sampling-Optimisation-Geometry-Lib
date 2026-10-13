import datetime,hashlib,json,os
from pathlib import Path
ROOT=Path(r'E:\Samplinglib\.astis\decoder-64')
R=ROOT/'independent'
sha=lambda b:hashlib.sha256(b).hexdigest()
canon=lambda v:json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode('utf-8')
def write(n,v): (R/n).write_bytes((json.dumps(v,sort_keys=True,indent=2,ensure_ascii=False)+'\n').encode('utf-8'))
def entries(ns):
 es=[]
 for n in ns:
  b=(R/n).read_bytes(); es.append({'path':n,'bytes':len(b),'raw_sha256':sha(b)})
 return es
assert not (R/'lease.json').exists(),'Owned lease already exists; refusing writes'
meta=[]
for n in [0,1]:
 raw=(ROOT/f'packet{n}.json').read_bytes(); lf=raw.replace(b'\r\n',b'\n').replace(b'\r',b'\n')
 p=json.loads(raw); d=dict(p); declared=d.pop('packet_sha256'); pc=canon(d); ctx=canon(p['lean']['approved_definition_context'])
 assert sha(pc)==declared
 assert sha(p['lean']['statement'].encode('utf-8'))==p['lean']['statement_sha256']
 assert p['non_disclosure']['source_text_included'] is False and p['non_disclosure']['source_identity_included'] is False
 for name,b in [(f'packet{n}.raw.json',raw),(f'packet{n}.lf.json',lf),(f'packet{n}.canonical-without-packet-sha256.json',pc),(f'packet{n}.approved-definition-context.canonical.json',ctx)]:
  (R/name).write_bytes(b)
 meta.append({'packet_id':p['packet_id'],'input_name':f'packet{n}.json','raw_path':f'packet{n}.raw.json','raw_bytes':len(raw),'raw_sha256':sha(raw),'lf_path':f'packet{n}.lf.json','lf_bytes':len(lf),'lf_sha256':sha(lf),'canonical_packet_path':f'packet{n}.canonical-without-packet-sha256.json','canonical_packet_sha256':sha(pc),'canonical_full_packet_sha256':sha(canon(p)),'declared_packet_sha256':declared,'statement_sha256':p['lean']['statement_sha256'],'approved_definition_context_canonical_path':f'packet{n}.approved-definition-context.canonical.json','approved_definition_context_canonical_sha256':sha(ctx),'compiled_flag_in_supplied_packet':p['lean']['compiled']})
rawlease=(ROOT/'lease.json').read_bytes(); oldlease=json.loads(rawlease)
assert oldlease['status']=='OPEN' and oldlease['source_text_visible'] is False and oldlease['source_identity_visible'] is False
(R/'input_lease.raw.json').write_bytes(rawlease)
payloadraw=(R/'reconstruction_payload.json').read_bytes(); payload=json.loads(payloadraw)
assert all(all(r['seven_slot_coverage'].values()) for r in payload['reconstructions'])
assert all(sha(r['reconstructed_theorem_text'].encode('utf-8'))==r['reconstructed_text_sha256'] for r in payload['reconstructions'])
base=sorted(p.name for p in R.iterdir() if p.is_file())
assert set(base)=={'finalizer.py','terminal_readback.py','input_lease.raw.json','reconstruction_payload.json','reconstruction.packet0.md','reconstruction.packet1.md','packet0.raw.json','packet0.lf.json','packet0.canonical-without-packet-sha256.json','packet0.approved-definition-context.canonical.json','packet1.raw.json','packet1.lf.json','packet1.canonical-without-packet-sha256.json','packet1.approved-definition-context.canonical.json'}
selfm={'schema_version':1,'kind':'self-layer-manifest','root':str(R),'finalizer_pid':os.getpid(),'artifacts':entries(base),'layer_rule':'Binds every input snapshot, reconstruction, complete payload and both scripts. Bound by final_run and closure_manifest rather than recursively by itself.'}
write('self_manifest.json',selfm); selfhash=sha((R/'self_manifest.json').read_bytes())
run={'schema_version':1,'kind':'native-independent-source-blind-decoder-run','run_id':'independent-decoder-64','decoder':'independent-source-blind-decoder-64','finished_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'finalizer_pid':os.getpid(),'foreground_finalizer':True,'source_text_visible':False,'source_identity_visible':False,'compiler_started':False,'source_fidelity_claimed':False,'verified_transition_claimed':False,'permitted_original_inputs':[str(ROOT/'packet0.json'),str(ROOT/'packet1.json'),str(ROOT/'lease.json')],'original_input_policy':'Only the three permitted original inputs were read; generated owned artifacts were read for reconstruction/sealing. No repository sources, source text/identities, prior reviews or repair proposals read.','packet_bindings':meta,'input_lease_raw_sha256':sha(rawlease),'reconstruction_payload_path':'reconstruction_payload.json','reconstruction_payload_raw_sha256':sha(payloadraw),'reconstruction_payload_hash_rule':'SHA256 of complete named reconstruction_payload.json RAW bytes: no deletion, normalization or reserialization.','reconstructions':payload['reconstructions'],'semantic_slots':payload['semantic_slots'],'self_manifest_path':'self_manifest.json','self_manifest_raw_sha256':selfhash,'closing_layers':{'closure_manifest_path':'closure_manifest.json','lease_path':'lease.json','rule':'Closure binds all self-layer files plus self_manifest and final_run; CLOSED_LAST lease binds closure/self/final-run/payload. Lease is the final owned write. Terminal readback is foreground/read-only. No circular self-hash for terminal lease is claimed.'},'canonicalization':'UTF-8 JSON; recursive sort_keys=true; compact comma/colon separators; ensure_ascii=false; no trailing newline in canonical bytes.','packet_hash_rule':'Canonical packet hash deletes only top-level packet_sha256. Full canonical packet hash is separately retained.','context_hash_rule':'Canonical hash of approved_definition_context JSON array alone, separate from statement and packet hashes.','run_hash_rule':'SHA256 of canonical whole logical final_run after deleting ONLY top-level run_sha256; no recursive or other deletion.','limits':['Anonymous statements and approved definition context only. Packet compiled flags were not rerun. No source-fidelity, original-proof, source-identity or VERIFIED assessment. Byte-seal/readback consistency is not a source-equivalence certificate.']}
run['run_sha256']=sha(canon(run)); write('final_run.json',run)
logical=dict(run); logical.pop('run_sha256'); assert sha(canon(logical))==run['run_sha256']
closure={'schema_version':1,'kind':'closure-layer-manifest','root':str(R),'finalizer_pid':os.getpid(),'run_sha256':run['run_sha256'],'artifacts':entries(base+['self_manifest.json','final_run.json']),'layer_rule':'Binds all owned files except this manifest and terminal lease. The final terminal lease binds this manifest. No circular self-hash is asserted.'}
write('closure_manifest.json',closure)
lease={'schema_version':1,'kind':'owned-independent-decoder-terminal-lease','status':'CLOSED_LAST','last_owned_write':True,'finalizer_pid':os.getpid(),'foreground_finalizer':True,'source_text_visible':False,'source_identity_visible':False,'compiler_started':False,'run_sha256':run['run_sha256'],'reconstruction_payload_raw_sha256':sha(payloadraw),'self_manifest_raw_sha256':selfhash,'closure_manifest_raw_sha256':sha((R/'closure_manifest.json').read_bytes()),'final_run_raw_sha256':sha((R/'final_run.json').read_bytes()),'owner_root':str(R),'original_lease_unchanged':True,'post_close_policy':'No owned writes after this final lease; terminal readback is foreground and read-only.'}
write('lease.json',lease)
# CLOSED_LAST: no owned writes below this line.
print(json.dumps({'status':'FINALIZER_EXIT0','finalizer_pid':os.getpid(),'run_sha256':run['run_sha256'],'reconstruction_payload_raw_sha256':lease['reconstruction_payload_raw_sha256'],'owned_lease_status':'CLOSED_LAST'},sort_keys=True))