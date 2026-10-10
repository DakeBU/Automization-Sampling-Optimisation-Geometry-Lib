from pathlib import Path
import hashlib,json,os,sys
root=Path.cwd();sys.path.insert(0,str(root/'tools'));import astis_semantic_roundtrip as rt
r=Path('runs/20261007-companion-priority/pbps-b4-corrector-perturbation72');owned=Path('.astis/decoder-72/independent')
load=lambda p:json.loads(Path(p).read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest();can=lambda x:json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def new(p,x):
 p=Path(p);assert not p.exists(),p;p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
def pin(p):
 p=Path(p);b=p.read_bytes();return dict(path=p.resolve().as_posix(),RAW_bytes=len(b),RAW_sha256=sha(b),LF_sha256=sha(b.replace(b'\r\n',b'\n')))
lease=load(owned/'CLOSED_LAST.json');manifest=load(owned/'manifest.json');run=load(owned/'run.json');recon=load(owned/'reconstruction.json');decision=load(owned/'decision.json')
assert sha((owned/'CLOSED_LAST.json').read_bytes())=='c54208fc266a22909fc914cc72826c630b78d6aa29315d1f0b6de51fa83e456c'
actual={p.relative_to(owned).as_posix() for p in owned.rglob('*') if p.is_file()}
assert lease['status']=='CLOSED_LAST' and len(actual)==lease['owned_file_count']==5 and actual==set(lease['owned_files'])==set(manifest['owned_files'])
assert actual=={z['path'] for z in lease['sealed_files_except_self']}|{'CLOSED_LAST.json'}
for z in lease['sealed_files_except_self']:
 p=owned/z['path'];b=p.read_bytes();assert len(b)==z['bytes'] and sha(b)==z['raw_sha256'] and sha(b.replace(b'\r\n',b'\n'))==z['lf_sha256']
 assert p.stat().st_mtime_ns<=(owned/'CLOSED_LAST.json').stat().st_mtime_ns
for z in manifest['payload_files']:
 b=(owned/z['path']).read_bytes();assert len(b)==z['bytes'] and sha(b)==z['raw_sha256'] and sha(b.replace(b'\r\n',b'\n'))==z['lf_sha256']
h=sha(can({k:v for k,v in run.items() if k!='run_sha256'}))
assert h==run['run_sha256']==lease['run_sha256']==recon['decoder_run_sha256']==decision['decoder_run_sha256']=='23b058be5d13493b869e9b1966e00552bdef6b3e77db2124b5d764e61d7d7948'
for k in ['implementation_bodies_visible','named_declaration_identity_visible','source_text_visible','source_identity_visible','source_anchor_visible','compiler_commands_run','compiler_output_visible','prior_reviews_or_repairs_visible','other_agent_output_visible','repository_or_AGENTS_or_skills_read','source_fidelity_verdict_issued']:assert run['exposure'][k] is False,k
assert decision['source_fidelity_verdict'] is None and decision['mathematical_truth_verdict'] is None
assert len(recon['outputs'])==len(run['reconstructions'])==2
plan=load(r/'publication-plan.json');audits=[];packets=[]
for i in range(2):
 p=Path(f'.astis/decoder-72/packet{i}.json');packet=load(p);ip=run['input_pins'][i]
 assert len(p.read_bytes())==ip['bytes'] and sha(p.read_bytes())==ip['raw_sha256'] and sha(p.read_bytes().replace(b'\r\n',b'\n'))==ip['lf_sha256']
 official=rt.sha256_json({k:v for k,v in packet.items() if k!='packet_sha256'})
 assert official==packet['packet_sha256']==ip['canonical_packet_sha256']
 z=recon['outputs'][i];base={k:v for k,v in z.items() if k!='decoder_run_sha256'}
 assert base==run['reconstructions'][i] and z['decoder_run_sha256']==h and z['source_text_visible'] is False
 assert sha(z['reconstructed_theorem_text'].encode())==z['reconstructed_text_sha256']
 for k in ['objects','domains','quantifiers','assumptions','conclusion','scopes','constant_dependencies']:assert z[k]
 ap=Path('research-wiki/semantic-roundtrip/audits')/(plan['audit_ids'][i]+'.json');audit=load(ap)
 assert audit['state']=='draft' and rt.decoder_packet(audit)==packet==load(r/f'anonymous.{i}.decoder.json')
 audits.append((ap,audit,z,official));packets.append(packet)
archive=r/'anonymous-decoder';archive.mkdir(exist_ok=False)
for name in sorted(actual):(archive/name).write_bytes((owned/name).read_bytes())
for i in range(2):(archive/f'parent-packet{i}.json').write_bytes(Path(f'.astis/decoder-72/packet{i}.json').read_bytes())
for i,(ap,audit,z,official) in enumerate(audits):
 adapter=archive/f'decoded{i}.root-adapter.json'
 new(adapter,dict(native_complete_reconstruction=z,native_complete_run=run,native_complete_named_RAW=pin(archive/'reconstruction.json'),native_whole_logical_run_sha256=h,official_decoder_packet_payload_sha256=official,hash_convention='Official packet hashes omit ONLY top-level packet_sha256; native whole run omits ONLY top-level run_sha256. Native bytes unchanged.',actual_root_PID=os.getpid()))
 before=r/f'audit.{i}.before-decoder72.exactraw.snapshot.json';assert not before.exists();before.write_bytes(ap.read_bytes())
 audit.update(state='blind-reconstructed',reconstruction=dict(text=z['reconstructed_theorem_text'],text_sha256=z['reconstructed_text_sha256'],decoder=z['decoder'],decoder_run_sha256=h,decoder_packet_sha256=official,source_text_visible=False,lean_statement_sha256=audit['lean']['statement_sha256'],input_artifacts=['lean-statement','approved-definition-context'],observed_input_artifacts=[pin(archive/f'parent-packet{i}.json')],run_artifact=adapter.as_posix(),run_binding=(archive/'CLOSED_LAST.json').as_posix(),native_named_payload_sha256=sha((owned/'reconstruction.json').read_bytes()),unresolved_semantics=z['unresolved_semantics'],run_hash_recipe=run['run_sha256_recipe']))
 ap.write_text(json.dumps(audit,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
 new(r/f'source-review.packet.{i}.json',rt.semantic_reviewer_packet(audit))
new(r/'root.decoder72.adoption.json',dict(status='CLOSED_BLIND_DECODER72_ADOPTED_ONLY',actual_root_PID=os.getpid(),native_whole_logical_run_sha256=h,native_owned_files=5,native_lease=pin(owned/'CLOSED_LAST.json'),native_complete_payload=pin(owned/'run.json'),reported_native_writer_PID=26264,reported_native_writer_EXIT=0,reported_native_external_readonly_PID=37156,reported_native_external_readonly_EXIT=0,source_verdict=False,VERIFIED=False))
names=[r/f'source-review.packet.{i}.json' for i in range(2)]+[p for p,_,_,_ in audits]
names += [Path(x) for x in load(r/'claim.json')['proposed_files']]
names += [Path('website/content/'+kind+'/'+slug+'.json') for slug in plan['slugs'] for kind in ['publications','declaration_lessons']]
names += [Path('research-wiki/frontier-cells')/(x+'.json') for x in plan['active_cells']]
new(r/'source-review.freeze72.json',dict(status='TWO_CURRENT72_SOURCE_REVIEW_PACKETS_FROZEN',inputs=[pin(p) for p in names],native_reconstruction=pin(archive/'reconstruction.json'),source_review=False,VERIFIED=False))
print('PASS root adoption: CLOSED5 unchanged two-packet blind reconstruction; two canonical source reviewer packets frozen. Source/VERIFIED pending.')
