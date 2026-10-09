from pathlib import Path
import hashlib,json,os,subprocess,sys
root=Path.cwd();sys.path.insert(0,str(root/'tools'));import astis_semantic_roundtrip as rt,astis_publication as pub
r=root/'runs/20261007-companion-priority/pbps-centered-root64';n=root/'.astis/decoder-64';d=n/'independent'
load=lambda p:json.loads(Path(p).read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest()
can=lambda x:json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def pin(p):
 p=Path(p);b=p.read_bytes();return dict(path=p.resolve().as_posix(),raw_bytes=len(b),lf_bytes=len(b.replace(b'\r\n',b'\n')),raw_sha256=sha(b),lf_sha256=sha(b.replace(b'\r\n',b'\n')))
def w(p,x):
 assert not p.exists(),p;p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
assert load(r/'independent-math64/lease.json')['status']=='CLOSED_LAST'
assert load(r/'step6-presentation-repair64/supplement.json')['status'].startswith('STEP6_BODY_EXCERPT_CORRECTED')
run,lease,payload=[load(d/k) for k in ['final_run.json','lease.json','reconstruction_payload.json']]
assert lease['status']=='CLOSED_LAST' and run['finalizer_pid']==lease['finalizer_pid']==47444
assert sha(can({k:v for k,v in run.items() if k!='run_sha256'}))==run['run_sha256']==lease['run_sha256']=='dfa4906527c35c1684d8ce626c56cbcc41985f2bfb517f65d17c5cba1dd3f2ad'
named=sha((d/'reconstruction_payload.json').read_bytes());assert named==lease['reconstruction_payload_raw_sha256']=='ecbae83485126a3f9f25492b9b22d0c8f30059fabdcd64f2d18631d3a72d6c77'
assert run['reconstructions']==payload['reconstructions']
for x in [run,lease]:
 for k in ['source_text_visible','source_identity_visible','compiler_started']:assert x[k] is False
initial=(n/'initial-lease.raw.snapshot.json').read_bytes()
assert initial==(n/'lease.json').read_bytes()==(d/'input_lease.raw.json').read_bytes()
assert sha(initial)==run['input_lease_raw_sha256'] and load(n/'lease.json')['status']=='OPEN'
observed=subprocess.Popen([sys.executable,'-X','utf8',str(d/'terminal_readback.py')],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
stdout,stderr=observed.communicate();assert observed.returncode==0,stderr.decode(errors='replace')
terminal=json.loads(stdout);assert terminal['readback_pid']==observed.pid and terminal['owned_artifact_count']==18
assert terminal['run_sha256']==run['run_sha256'] and terminal['lease_raw_sha256']==sha((d/'lease.json').read_bytes())
assert {p.name for p in d.iterdir()}=={x['path'] for x in load(d/'closure_manifest.json')['artifacts']}|{'closure_manifest.json','lease.json'}
plan=load(r/'publication-plan.json');aids=['ASTIS-RT-20261009-RealL2PositiveSquareOrder','ASTIS-RT-20261009-PBPSCenteredRootOrderInverse'];audits=[]
pub.inputs.cache_clear();pub.load.cache_clear();data=pub.inputs()
for i,aid in enumerate(aids):
 p=root/'research-wiki/semantic-roundtrip/audits'/f'{aid}.json';audit=load(p);packet=load(n/f'packet{i}.json')
 assert audit['state']=='draft' and rt.decoder_packet(audit)==packet==load(r/f'anonymous.{i}.decoder.json')
 assert (n/f'packet{i}.json').read_bytes()==(d/f'packet{i}.raw.json').read_bytes()
 assert rt.sha256_json({k:v for k,v in packet.items() if k!='packet_sha256'})==packet['packet_sha256']
 item=next(x for x in pub.load() if x['id']==plan['slugs'][i]);assert pub.binding_digest(item,item['bindings'][0],data)==audit['publication_binding_sha256']
 decoded=next(x for x in payload['reconstructions'] if x['packet_id']==packet['packet_id'])
 assert sha(decoded['reconstructed_theorem_text'].encode())==decoded['reconstructed_text_sha256']
 assert set(decoded['seven_slot_coverage'])==set(payload['semantic_slots']) and all(decoded['seven_slot_coverage'].values())
 assert all(decoded[k] for k in payload['semantic_slots'])
 assert sha(packet['lean']['statement'].encode())==packet['lean']['statement_sha256']
 audits.append((p,audit,packet,decoded))
dest=r/'anonymous-decoder';dest.mkdir(exist_ok=False);maps=[]
for p in [*sorted(d.iterdir()),n/'packet0.json',n/'packet1.json',n/'lease.json',n/'initial-lease.raw.snapshot.json']:
 target=dest/('parent-lease.open.json' if p==n/'lease.json' else p.name);assert not target.exists();target.write_bytes(p.read_bytes());maps.append(dict(original=pin(p),explicit_exact_raw_snapshot=pin(target)))
w(dest/'root-observed-terminal-readback.json',dict(actual_observer_pid=os.getpid(),actual_readback_pid=observed.pid,exit_code=observed.returncode,terminal_closed=True,stdout=terminal,stderr=stderr.decode('utf-8')))
for i,(ap,audit,packet,decoded) in enumerate(audits):
 adapter=dest/f'decoded{i}.root-adapter.json';w(adapter,dict(native_payload=pin(dest/'reconstruction_payload.json'),native_complete_payload=payload,selected_packet_id=packet['packet_id'],whole_logical_run_sha256=run['run_sha256'],native_named_payload_RAW_sha256=named,native_bytes_unchanged=True,root_observed_terminal=pin(dest/'root-observed-terminal-readback.json')))
 snap=r/f'audit.{i}.before-decoder.exactraw.snapshot.json';snap.write_bytes(ap.read_bytes());maps.append(dict(original=pin(ap),explicit_exact_raw_snapshot=pin(snap)))
 audit.update(state='blind-reconstructed',reconstruction=dict(text=decoded['reconstructed_theorem_text'],text_sha256=decoded['reconstructed_text_sha256'],decoder='/root/anonymous_decoder64',decoder_run_sha256=run['run_sha256'],decoder_packet_sha256=packet['packet_sha256'],source_text_visible=False,lean_statement_sha256=audit['lean']['statement_sha256'],input_artifacts=['lean-statement','approved-definition-context'],observed_input_artifacts=[pin(dest/f'packet{i}.json')],run_artifact=adapter.relative_to(root).as_posix(),run_binding=(dest/'lease.json').relative_to(root).as_posix(),native_named_payload_sha256=named,run_hash_recipe=run['run_hash_recipe'] if 'run_hash_recipe' in run else 'SHA256 sorted compact UTF8 whole logical final_run removing ONLY run_sha256'))
 ap.write_text(json.dumps(audit,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
 w(r/f'source.{i}.reviewer-packet.json',rt.semantic_reviewer_packet(audit))
w(r/'root.decoder64.adoption.json',dict(status='CLOSED_FRESH_ANONYMOUS_DECODER64_ADOPTED',actual_adopter_pid=os.getpid(),native_whole_run_sha256=run['run_sha256'],native_complete_named_RAW_sha256=named,native_owned_files=18,raw_snapshot_mappings=maps,observed_readback=pin(dest/'root-observed-terminal-readback.json'),source_text_visible=False,source_identity_visible=False,compiler_started=False,native_parent_lease_preserved_OPEN=True,source_verdict=False,VERIFIED_transition=False))
print('PASS closed blind decoder64:18 unchanged native files, two complete seven-slot reconstructions, fresh anti-anchored packets; source review pending.')
