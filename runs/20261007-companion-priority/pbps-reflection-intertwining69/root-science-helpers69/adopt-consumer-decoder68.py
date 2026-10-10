from pathlib import Path
import copy,hashlib,json,os,sys
sys.path.insert(0,'tools')
import astis_semantic_roundtrip as rt,astis_publication as pub
root=Path.cwd();r=root/'runs/20261007-companion-priority/pbps-sharp-energy68';n=root/'.astis/decoder-68-consumer';d=n/'independent'
load=lambda p:json.loads(p.read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest();can=lambda x:json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def pin(p):
 b=p.read_bytes();return dict(path=p.resolve().as_posix(),raw_bytes=len(b),raw_sha256=sha(b),lf_sha256=sha(b.replace(b'\r\n',b'\n')))
def write(p,x):
 assert not p.exists(),p;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
lease=load(d/'lease.json');run=load(d/'final_run.json');payload=load(d/'reconstruction_payload.json')
assert sha((d/'lease.json').read_bytes())=='88e2db1d000bebe33f41562f588b79e02220592aea29b52c17e74275d7149d4d' and lease['status']=='CLOSED_LAST' and lease['last_owned_write']=='lease.json'
assert sha(can({k:v for k,v in run.items() if k!='run_sha256'}))==run['run_sha256']==lease['whole_logical_run_sha256']==payload['decoder_run_sha256']=='7e00c6e9c5c7676c60691009426cf5bdf71dfa8563ed49e12de180f692e06924'
assert sha((d/'reconstruction_payload.json').read_bytes())==lease['reconstruction_payload_raw_sha256']=='a91155a9f55f74950f236feb16a27853abd63f80d4cc7d6bf04dc464cf0786de'
assert sha((d/'raw_input_manifest.json').read_bytes())==lease['raw_input_manifest_raw_sha256']=='18566063830dbd9ce161f4b90ffb60239ba22bfb175ece90e74e92aa3e802b2a'
rows=lease['immutable_file_rows'];files={p.relative_to(d).as_posix():p for p in d.rglob('*') if p.is_file()}
assert len(rows)==24 and len(files)==25 and set(files)=={z['path'] for z in rows}|{'lease.json'}
assert sha(can(rows))==lease['closure_sha256']=='81db19971bb8742b27d05895316bf10b0583fe9a45a872e5d2d80cd8207a35b8'
assert sha((d/'closure_manifest.json').read_bytes())=='79dd885ac76a9b41151320bddd11dfe0eee0809d528284dc328fb308fae476e5'
for z in rows:
 p=files[z['path']];b=p.read_bytes();assert len(b)==z['bytes'] and sha(b)==z['raw_sha256'] and p.stat().st_mtime_ns==z['mtime_ns']
assert (d/'lease.json').stat().st_mtime_ns>=max(p.stat().st_mtime_ns for p in files.values())
for x in [lease,run,payload]:assert all(x[k] is False for k in ['source_text_visible','source_identity_visible','compiler_started'])
for stage,pid in [('build',28776),('finalizer',26792),('readback',1724)]:
 q=load(d/f'terminal_{stage}.json');assert q['actual_process_completed'] and q['exit_code']==0 and q['process_id']==pid
manifest=load(d/'raw_input_manifest.json');pins=load(d/'finite_pin_mappings.json')['pins'];assert len(pins)==3
for z in pins:
 b=(d/z['raw_snapshot']).read_bytes();lf=b.replace(b'\r\n',b'\n');m=manifest['inputs'][z['input']];original=n/z['input']
 assert original.read_bytes()==b and original.stat().st_mtime_ns==m['mtime_ns'] and sha(b)==z['raw_sha256']==m['raw_sha256'] and sha(lf)==z['lf_sha256'] and (d/z['lf_snapshot']).read_bytes()==lf
assert load(n/'lease.json')['status']=='OPEN' and (n/'lease.json').read_bytes()==(n/'initial-lease.raw.snapshot.json').read_bytes()
audit=load(r/'consumer.semantic-audit68.draft.json');packet=load(n/'packet0.json');assert rt.decoder_packet(audit)==packet==load(r/'anonymous.consumer.decoder.json')
assert rt.sha256_json({k:v for k,v in packet.items() if k!='packet_sha256'})==packet['packet_sha256']
decoded=payload['reconstructions'][packet['packet_id']];slots={'objects','domains','assumptions','quantifiers','conclusion','constant_dependencies','scopes'}
assert set(decoded['seven_slot_coverage'])==slots and all(decoded[k] and decoded['seven_slot_coverage'][k]['status']=='covered' for k in slots)
assert sha(decoded['reconstructed_theorem_text'].encode())==decoded['reconstructed_text_sha256']==sha((d/decoded['named_reconstruction_file']).read_bytes())=='7991bffbdb03f971abc695ebb9fc14e5b88441cd16284feee2737ca764e61857'
assert decoded['lean_statement_sha256']==audit['lean']['statement_sha256']
dest=r/'anonymous-consumer-decoder';dest.mkdir(exist_ok=False);maps=[]
for rel,p in sorted(files.items()):
 target=dest/rel;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(p.read_bytes());maps.append(dict(original=pin(p),explicit_exact_raw_snapshot=pin(target)))
for name in ['packet0.json','lease.json','initial-lease.raw.snapshot.json']:
 target=dest/('parent-lease.open.json' if name=='lease.json' else name);target.write_bytes((n/name).read_bytes());maps.append(dict(original=pin(n/name),explicit_exact_raw_snapshot=pin(target)))
adapter=dest/'decoded.root-adapter.json';write(adapter,dict(native_complete_payload=payload,native_payload=pin(dest/'reconstruction_payload.json'),selected_packet_id=packet['packet_id'],whole_logical_run_sha256=run['run_sha256'],native_named_payload_RAW_sha256=lease['reconstruction_payload_raw_sha256'],native_bytes_unchanged=True,actual_root_read_only_adopter_pid=os.getpid()))
production=load(root/'research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261009-PBPSSharpCorrectorEnergy.json')
context=copy.deepcopy(production['publication_context']);context['file']=pub.file_digest(audit['lean']['file']);context['current_lean_module']=(root/audit['lean']['file']).read_text(encoding='utf-8');context['binding']=dict(declaration=audit['lean']['declaration'],role='genuine-compiled-original-input-source-consumer',supports=['modified-energy-equivalence'])
audit['publication_context']=context;audit['publication_binding_sha256']=sha(can(context));audit['standalone_test_consumer_scope']['binding_recipe']='SHA256 of canonical complete standalone Test-consumer context; no new production publication node.'
audit.update(state='blind-reconstructed',reconstruction=dict(text=decoded['reconstructed_theorem_text'],text_sha256=decoded['reconstructed_text_sha256'],decoder='/root/anonymous_decoder68',decoder_run_sha256=run['run_sha256'],decoder_packet_sha256=packet['packet_sha256'],source_text_visible=False,lean_statement_sha256=audit['lean']['statement_sha256'],input_artifacts=['lean-statement','approved-definition-context'],observed_input_artifacts=[pin(dest/'packet0.json')],run_artifact=adapter.relative_to(root).as_posix(),run_binding=(dest/'lease.json').relative_to(root).as_posix(),native_named_payload_sha256=lease['reconstruction_payload_raw_sha256'],run_hash_recipe=run['hash_rule']))
assert rt.decoder_packet(audit)==packet
write(r/'consumer.semantic-audit68.blind.json',audit);write(r/'source.consumer.reviewer-packet.json',rt.semantic_reviewer_packet(audit))
write(r/'root.consumer-decoder68.adoption.json',dict(status='CLOSED_FRESH_CONSUMER_BLIND_DECODER68_ADOPTED',actual_adopter_pid=os.getpid(),native_whole_logical_run_sha256=run['run_sha256'],native_complete_named_RAW_sha256=lease['reconstruction_payload_raw_sha256'],native_owned_files=25,native_immutable_files_excluding_final_lease=24,finite_raw_snapshot_mappings=maps,standalone_consumer_audit=pin(r/'consumer.semantic-audit68.blind.json'),source_verdict=False,VERIFIED_transition=False,production_metadata_or_Lean_changes=False))
print('PASS closed consumer decoder68:25 native files,complete7-slot modified-energy statement; source.consumer reviewer packet ready; code unchanged.')
