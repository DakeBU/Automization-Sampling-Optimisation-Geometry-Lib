from pathlib import Path
import hashlib, json, os, sys
root=Path.cwd();sys.path.insert(0,str(root/'tools'));import astis_semantic_roundtrip as rt
r=Path('runs/20261007-companion-priority/pbps-actual-harmonic-flow73');o=Path('.astis/decoder-73/result')
load=lambda p:json.loads(Path(p).read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest()
can=lambda x:json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def new(p,x):
 p=Path(p);assert not p.exists(),p;p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
def pin(p):
 p=Path(p);b=p.read_bytes();return dict(path=p.resolve().as_posix(),RAW_bytes=len(b),RAW_sha256=sha(b),LF_sha256=sha(b.replace(b'\r\n',b'\n')))
def check(z):
 p=Path(z['path']);b=p.read_bytes()
 assert len(b)==z['bytes'] and sha(b)==z['raw_sha256'] and sha(b.replace(b'\r\n',b'\n'))==z['lf_sha256'],z['path']
 return b
lease=load(o/'CLOSED_LAST.json');run=load(o/'run.json');recon=load(o/'reconstruction.json')
assert sha((o/'CLOSED_LAST.json').read_bytes())=='11559b67f3e4ead69c710f506ca2ce07b78051fdf19bc3f46d87c6253c13b908'
assert lease['status']=='CLOSED_LAST' and lease['further_owned_writes_prohibited']
actual={p.resolve() for p in o.rglob('*') if p.is_file()}
assert len(actual)==4 and actual=={Path(z['path']).resolve() for z in lease['prior_owned_files']}|{(o/'CLOSED_LAST.json').resolve()}
for z in lease['prior_owned_files']:
 check(z);assert Path(z['path']).stat().st_mtime_ns<=(o/'CLOSED_LAST.json').stat().st_mtime_ns
check(lease['sole_input_receipt'])
preimage=run['canonical_logical_run_utf8'].encode()
assert json.loads(preimage)==run['logical_run_payload']
assert preimage==can(run['logical_run_payload'])
h=sha(preimage)
assert len(preimage)==run['canonical_preimage_bytes']
assert h==run['decoder_run_sha256']==lease['decoder_run_sha256']==recon['decoder_run_sha256']=='14a2f94fc0a24d4011e23362b9bbe052ba8c4ed77fe47628728281756e61d273'
assert {k:v for k,v in recon.items() if k!='decoder_run_sha256'}==run['logical_run_payload']['reconstruction_without_decoder_run_sha256']
assert all(recon[k] is False and run[k] is False for k in ['source_text_visible','source_identity_visible','proof_visible'])
exposure=recon['decoder']
assert all(exposure[k] is False for k in ['repository_search_performed','compiler_used','web_used','other_agents_consulted'])
assert recon['semantic_slot_count']==7 and set(recon['semantic_slot_names'])==set(rt.SEMANTIC_SLOTS)
assert all(recon[k] for k in rt.SEMANTIC_SLOTS)
text=recon['reconstructed_theorem_text'];assert sha(text.encode())==recon['reconstructed_text_sha256']==sha((o/'reconstruction.md').read_bytes())
packet=load('.astis/decoder-73/packet.json');official=rt.sha256_json({k:v for k,v in packet.items() if k!='packet_sha256'})
assert packet['packet_sha256']==official==run['logical_run_payload']['embedded_packet_sha256_value']
assert sha(Path('.astis/decoder-73/packet.json').read_bytes())==recon['packet_raw_sha256']
ap=Path('research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261010-PBPSActualHarmonicFlow.json');audit=load(ap)
assert audit['state']=='draft' and rt.decoder_packet(audit)==packet==load(r/'anonymous.decoder.json')
archive=r/'anonymous-decoder';archive.mkdir(exist_ok=False)
for p in o.iterdir():
 if p.is_file():(archive/p.name).write_bytes(p.read_bytes())
(archive/'parent-packet.json').write_bytes(Path('.astis/decoder-73/packet.json').read_bytes())
adapter=archive/'decoded.root-adapter.json'
new(adapter,dict(native_complete_reconstruction=recon,native_complete_run=run,
 native_whole_logical_run_sha256=h,official_decoder_packet_payload_sha256=official,
 hash_convention='Native run hashes its explicit canonical logical_run_payload; native preimage is independently equal to compact sorted-key UTF8 JSON. Official packet omits only packet_sha256. Native bytes unchanged.',actual_root_PID=os.getpid()))
(r/'audit.before-decoder73.exactraw.snapshot.json').write_bytes(ap.read_bytes())
audit.update(state='blind-reconstructed',reconstruction=dict(text=text,text_sha256=recon['reconstructed_text_sha256'],
 decoder=exposure['agent_identity'],decoder_run_sha256=h,decoder_packet_sha256=official,source_text_visible=False,
 lean_statement_sha256=audit['lean']['statement_sha256'],input_artifacts=['lean-statement','approved-definition-context'],
 observed_input_artifacts=[pin(archive/'parent-packet.json')],run_artifact=adapter.as_posix(),run_binding=(archive/'CLOSED_LAST.json').as_posix(),
 native_named_payload_sha256=sha((o/'run.json').read_bytes()),unresolved_semantics=[],run_hash_recipe=run['canonical_recipe']))
ap.write_text(json.dumps(audit,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
new(r/'source-review.packet.json',rt.semantic_reviewer_packet(audit))
new(r/'root.decoder73.adoption.json',dict(status='CLOSED_BLIND_DECODER73_ADOPTED_ONLY',actual_root_PID=os.getpid(),
 native_whole_logical_run_sha256=h,native_owned_files=4,native_lease=pin(o/'CLOSED_LAST.json'),native_complete_payload=pin(o/'run.json'),
 reported_native_writer_PID=52648,reported_native_writer_EXIT=0,reported_native_external_readonly_PID=34464,reported_native_external_readonly_EXIT=0,
 native_validation_negative='Initial readonly PowerShell timestamp conversion rejected; string-preserving readonly validation passed with no sealed writes. Agent terminal chunks retained in conversation; no source or compiler failure.',source_verdict=False,VERIFIED=False))
plan=load(r/'publication-plan.json')
paths=[r/'source-review.packet.json',ap,Path(plan['active_cells'][0] and 'research-wiki/frontier-cells/'+plan['active_cells'][0]+'.json'),
 Path(load(r/'claim.json')['proposed_files'][0]),Path('website/content/publications/pbps-actual-harmonic-flow.json'),
 Path('website/content/declaration_lessons/pbps-actual-harmonic-flow.json'),r/'implementation-source-map73.json']
new(r/'source-review.freeze73.json',dict(status='CURRENT73_ANTI_ANCHORED_PACKET_AND_WHOLE_MODULE_LESSON_FROZEN',inputs=[pin(p) for p in paths],
 native_reconstruction=pin(archive/'reconstruction.json'),source_review=False,VERIFIED=False))
print('PASS73 CLOSED4 strict blind reconstruction adopted; official anti-anchored source packet frozen; source/VERIFIED pending.')
