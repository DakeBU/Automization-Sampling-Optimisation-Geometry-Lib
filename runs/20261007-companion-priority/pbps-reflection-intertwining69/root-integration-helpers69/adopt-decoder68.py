from pathlib import Path
import hashlib,json,os,sys
sys.path.insert(0,'tools')
import astis_semantic_roundtrip as rt,astis_publication as pub
root=Path.cwd();r=root/'runs/20261007-companion-priority/pbps-sharp-energy68';n=root/'.astis/decoder-68';d=n/'independent'
load=lambda p:json.loads(p.read_bytes())
sha=lambda b:hashlib.sha256(b).hexdigest()
can=lambda x:json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def pin(p):
 b=p.read_bytes();return dict(path=p.resolve().as_posix(),raw_bytes=len(b),raw_sha256=sha(b),lf_sha256=sha(b.replace(b'\r\n',b'\n')))
def write(p,x):
 assert not p.exists(),p;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
lease=load(d/'lease.json');run=load(d/'final_run.json');payload=load(d/'reconstruction_payload.json')
assert sha((d/'lease.json').read_bytes())=='9e4fb200730cb8f867388997651e8a0aac78550a058c6dc22ec0d25d45775de6'
assert lease['status']=='CLOSED_LAST' and lease['last_owned_write']=='lease.json'
assert sha(can({k:v for k,v in run.items() if k!='run_sha256'}))==run['run_sha256']==lease['whole_logical_run_sha256']==payload['decoder_run_sha256']=='2d9b5f94adc0ed9cf5ec9b32253526d4b90defe1f7423e900da119bb16420745'
assert sha((d/'reconstruction_payload.json').read_bytes())==lease['reconstruction_payload_raw_sha256']=='4096f8970fab9c7a5481d0860f5a98849a2ee3c211a9802ccf6d6f5c6d3f9c94'
assert sha((d/'raw_input_manifest.json').read_bytes())==lease['raw_input_manifest_raw_sha256']=='193e28075ba7e4528072a3f49dd17791064dd63acb300a56cc115dc05a933e98'
rows=lease['immutable_file_rows'];files={p.relative_to(d).as_posix():p for p in d.rglob('*') if p.is_file()}
assert len(rows)==lease['closure_count']==30 and len(files)==31 and set(files)=={z['path'] for z in rows}|{'lease.json'}
assert sha(can(rows))==lease['closure_sha256']=='83806fc1d02d9aeec0a3af5cce31d35be9ade437c802d57aefb0b78c3f052816'
for z in rows:
 p=files[z['path']];b=p.read_bytes();assert len(b)==z['bytes'] and sha(b)==z['raw_sha256'] and p.stat().st_mtime_ns==z['mtime_ns'],z['path']
assert (d/'lease.json').stat().st_mtime_ns>=max(p.stat().st_mtime_ns for p in files.values())
for x in [run,payload,lease]:
 assert all(x[k] is False for k in ['source_text_visible','source_identity_visible','compiler_started'])
assert sha((d/'closure_manifest.json').read_bytes())==lease['closure_manifest_raw_sha256']=='60cd4cd885ab33807b1c39f37e3d77b8102dfc44905f22eaebd5b26783773749'
for stage,pid in [('build',24064),('finalizer',42668),('readback',38668)]:
 q=load(d/f'terminal_{stage}.json');assert q['actual_process_completed'] and q['exit_code']==0 and q['process_id']==pid and q['exit_status']=='EXIT0'
manifest=load(d/'raw_input_manifest.json');pins=load(d/'finite_pin_mappings.json')['pins'];assert len(pins)==4
for z in pins:
 b=(d/z['raw_snapshot']).read_bytes();lf=b.replace(b'\r\n',b'\n');original=n/z['input'];m=manifest['inputs'][z['input']]
 assert original.read_bytes()==b and original.stat().st_mtime_ns==m['mtime_ns']
 assert sha(b)==z['raw_sha256']==m['raw_sha256'] and sha(lf)==z['lf_sha256']==m['lf_sha256'] and (d/z['lf_snapshot']).read_bytes()==lf
assert load(n/'lease.json')['status']=='OPEN' and (n/'lease.json').read_bytes()==(n/'initial-lease.raw.snapshot.json').read_bytes()
pub.inputs.cache_clear();pub.load.cache_clear();data=pub.inputs();records=[]
slots={'objects','domains','assumptions','quantifiers','conclusion','constant_dependencies','scopes'}
for i,(aid,slug) in enumerate([('ASTIS-RT-20261009-HilbertSharpQuadraticCorrectorBound','hilbert-sharp-quadratic-corrector-bound'),('ASTIS-RT-20261009-PBPSSharpCorrectorEnergy','pbps-sharp-corrector-energy')]):
 ap=root/'research-wiki/semantic-roundtrip/audits'/f'{aid}.json';audit=load(ap);packet=load(n/f'packet{i}.json')
 assert audit['state']=='draft' and rt.decoder_packet(audit)==packet==load(r/f'anonymous.{i}.decoder.json')
 assert rt.sha256_json({k:v for k,v in packet.items() if k!='packet_sha256'})==packet['packet_sha256']
 item=next(x for x in pub.load() if x['id']==slug);assert pub.binding_digest(item,item['bindings'][0],data)==audit['publication_binding_sha256']
 decoded=payload['reconstructions'][packet['packet_id']]
 assert set(decoded['seven_slot_coverage'])==slots and all(decoded[k] and decoded['seven_slot_coverage'][k]['status']=='covered' for k in slots)
 assert sha(decoded['reconstructed_theorem_text'].encode())==decoded['reconstructed_text_sha256']==sha((d/decoded['named_reconstruction_file']).read_bytes())
 assert decoded['lean_statement_sha256']==audit['lean']['statement_sha256'] and decoded['decoder_run_sha256']==run['run_sha256']
 records.append((i,ap,audit,packet,decoded))
dest=r/'anonymous-decoder';dest.mkdir(exist_ok=False);maps=[]
for rel,p in sorted(files.items()):
 target=dest/rel;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(p.read_bytes());maps.append(dict(original=pin(p),explicit_exact_raw_snapshot=pin(target)))
for name in ['packet0.json','packet1.json','initial-lease.raw.snapshot.json','lease.json']:
 target=dest/('parent-lease.open.json' if name=='lease.json' else name);target.write_bytes((n/name).read_bytes());maps.append(dict(original=pin(n/name),explicit_exact_raw_snapshot=pin(target)))
for i,ap,audit,packet,decoded in records:
 adapter=dest/f'decoded{i}.root-adapter.json'
 write(adapter,dict(native_complete_payload=payload,native_payload=pin(dest/'reconstruction_payload.json'),selected_packet_id=packet['packet_id'],whole_logical_run_sha256=run['run_sha256'],native_named_payload_RAW_sha256=lease['reconstruction_payload_raw_sha256'],native_bytes_unchanged=True,actual_root_read_only_adopter_pid=os.getpid()))
 before=r/f'audit.{i}.before-decoder.exactraw.snapshot.json';assert not before.exists();before.write_bytes(ap.read_bytes())
 audit.update(state='blind-reconstructed',reconstruction=dict(text=decoded['reconstructed_theorem_text'],text_sha256=decoded['reconstructed_text_sha256'],decoder='/root/anonymous_decoder68',decoder_run_sha256=run['run_sha256'],decoder_packet_sha256=packet['packet_sha256'],source_text_visible=False,lean_statement_sha256=audit['lean']['statement_sha256'],input_artifacts=['lean-statement','approved-definition-context'],observed_input_artifacts=[pin(dest/f'packet{i}.json')],run_artifact=adapter.relative_to(root).as_posix(),run_binding=(dest/'lease.json').relative_to(root).as_posix(),native_named_payload_sha256=lease['reconstruction_payload_raw_sha256'],run_hash_recipe=run['hash_rule']))
 ap.write_text(json.dumps(audit,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
 write(r/f'source.{i}.reviewer-packet.json',rt.semantic_reviewer_packet(audit))
write(r/'root.decoder68.adoption.json',dict(status='CLOSED_FRESH_ANONYMOUS_DECODER68_ADOPTED',actual_adopter_pid=os.getpid(),native_whole_logical_run_sha256=run['run_sha256'],native_complete_named_RAW_sha256=lease['reconstruction_payload_raw_sha256'],native_owned_files=31,native_immutable_files_excluding_final_lease=30,raw_snapshot_mappings=maps,source_text_visible=False,source_identity_visible=False,compiler_started=False,native_parent_lease_preserved_OPEN=True,source_verdict=False,VERIFIED_transition=False))
print('PASS closed blind decoder68:31 unchanged native files,2 complete7-slot reconstructions, exact RAW/LF/mtime/input/terminal validation; source review pending.')
