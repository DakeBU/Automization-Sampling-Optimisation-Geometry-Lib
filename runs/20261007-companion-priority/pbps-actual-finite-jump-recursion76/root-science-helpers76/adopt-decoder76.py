from pathlib import Path
import hashlib,json,os,sys
root=Path.cwd();sys.path.insert(0,str(root/'tools'));import astis_semantic_roundtrip as rt
r=Path('runs/20261007-companion-priority/pbps-actual-finite-jump-recursion76');o=Path('.astis/decoder-76/result')
load=lambda p:json.loads(Path(p).read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest()
can=lambda x:json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def new(p,x):
 p=Path(p);assert not p.exists(),p;p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
def pin(p):
 p=Path(p);b=p.read_bytes();return dict(path=p.resolve().as_posix(),RAW_bytes=len(b),RAW_sha256=sha(b),LF_sha256=sha(b.replace(b'\r\n',b'\n')))
def check(z):
 p=Path(z['path']);b=p.read_bytes();assert len(b)==z['raw_bytes'] and sha(b)==z['raw_sha256'] and sha(b.replace(b'\r\n',b'\n'))==z['lf_sha256'],p
 return b
expected_run,expected_lease,expected_payload=sys.argv[1:]
lease=load(o/'CLOSED_LAST.json');run=load(o/'run.json');recon=load(o/'reconstruction.json')
assert sha((o/'run.json').read_bytes())==expected_payload and sha((o/'CLOSED_LAST.json').read_bytes())==expected_lease
assert lease['status']=='CLOSED' and lease['final_write_rule'].startswith('CLOSED_LAST.json is the last owned write')
rows=lease['bound_prior_owned_files'];assert len(rows)==3 and lease['no_extra_owned_files']
assert {p.resolve() for p in o.rglob('*') if p.is_file()}=={Path(z['path']).resolve() for z in rows}|{(o/'CLOSED_LAST.json').resolve()}
for z in rows:
 check(z);assert Path(z['path']).stat().st_mtime_ns==z['mtime_ns']<=(o/'CLOSED_LAST.json').stat().st_mtime_ns
assert lease['closed_exit_receipt']['exit_code']==0 and lease['closed_exit_receipt']['state']=='EXIT'
logical=run['logical_run_payload'];preimage=run['canonical_logical_run_utf8'].encode()
assert preimage==can({k:v for k,v in logical.items() if k!='decoder_run_sha256'})
h=sha(preimage);assert len(preimage)==run['canonical_logical_run_utf8_bytes'] and h==run['decoder_run_sha256']==logical['decoder_run_sha256']==lease['decoder_run_sha256']==recon['decoder_run_sha256']==expected_run
reconstruction_object={k:v for k,v in recon.items() if k!='decoder_run_sha256'}
assert logical['reconstruction_without_decoder_run_sha256']==reconstruction_object
assert sha(can(reconstruction_object))==logical['reconstruction_without_decoder_run_sha256_utf8_sha256']
assert len(can(reconstruction_object))==logical['reconstruction_without_decoder_run_sha256_utf8_bytes']
assert recon['sole_input_receipt']==logical['sole_input_receipt']==lease['sole_input_receipt']
check(recon['sole_input_receipt']);assert logical['input_evidence']['authorized_input_count']==1
assert all(recon[k] is False for k in ['source_text_visible','source_identity_visible','proof_visible'])
exposure=recon['decoder'];assert exposure==logical['decoder']
assert all(exposure[k] is False for k in ['repository_search_performed','compiler_used','web_used','other_agents_consulted','source_text_visible','source_identity_visible','proof_visible'])
assert recon['semantic_slot_count']==7 and all(recon[k] for k in rt.SEMANTIC_SLOTS)
assert set(recon['semantic_slot_names'])=={'objects','domains','quantifiers','assumptions','conclusion','scopes_senses','constant_dependencies'}
assert recon['scopes']==recon['scopes_senses']
assert recon['literal_let_count']==11 and recon['conclusion_group_count']==10
text=recon['reconstructed_theorem_text'];assert sha(text.encode())==recon['reconstructed_text_sha256']
assert text in (o/'reconstruction.md').read_text(encoding='utf8')
packet=load('.astis/decoder-76/packet.json');official=rt.sha256_json({k:v for k,v in packet.items() if k!='packet_sha256'})
assert packet['packet_sha256']==official==recon['sole_input_receipt']['embedded_official_packet_sha256']
assert packet['lean']['statement_sha256']==logical['input_evidence']['actual_statement_utf8_sha256']
ap=Path('research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261010-PBPSActualFiniteJumpRecursion.json');audit=load(ap)
assert audit['state']=='draft' and rt.decoder_packet(audit)==packet==load(r/'anonymous.decoder.json')
archive=r/'anonymous-decoder';archive.mkdir(exist_ok=False)
for p in o.iterdir():
 if p.is_file():(archive/p.name).write_bytes(p.read_bytes())
(archive/'parent-packet.json').write_bytes(Path('.astis/decoder-76/packet.json').read_bytes())
adapter=archive/'decoded.root-adapter.json'
recipe='Compact sorted-key UTF8 JSON of native logical_run_payload excluding only its explicit decoder_run_sha256; native canonical preimage is checked byte-for-byte. Native reconstruction_without_decoder_run_sha256 is the complete reconstruction object, separately bound by its native utf8_sha256 and byte-count fields. No native bytes were changed; the first root adapter expected that object field to be a hash string and failed before canonical writes.'
new(adapter,dict(native_complete_reconstruction=recon,native_complete_run=run,native_whole_logical_run_sha256=h,official_decoder_packet_payload_sha256=official,hash_convention=recipe,semantic_slot_alias=dict(native='scopes_senses',canonical='scopes',both_native_fields_present_and_identical=True,native_bytes_unchanged=True),actual_root_PID=os.getpid()))
(r/'audit.before-decoder76.exactraw.snapshot.json').write_bytes(ap.read_bytes())
audit.update(state='blind-reconstructed',reconstruction=dict(text=text,text_sha256=recon['reconstructed_text_sha256'],decoder=exposure['agent_identity'],decoder_run_sha256=h,decoder_packet_sha256=official,source_text_visible=False,lean_statement_sha256=audit['lean']['statement_sha256'],input_artifacts=['lean-statement','approved-definition-context'],observed_input_artifacts=[pin(archive/'parent-packet.json')],run_artifact=adapter.as_posix(),run_binding=(archive/'CLOSED_LAST.json').as_posix(),native_named_payload_sha256=sha((o/'run.json').read_bytes()),unresolved_semantics=[],run_hash_recipe=recipe))
ap.write_text(json.dumps(audit,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
new(r/'root.decoder76.adoption.json',dict(status='CLOSED_BLIND_DECODER76_ADOPTED_ONLY',actual_root_PID=os.getpid(),native_whole_logical_run_sha256=h,native_owned_files=4,native_lease=pin(o/'CLOSED_LAST.json'),native_complete_payload=pin(o/'run.json'),native_writer_process_receipt=lease['closed_exit_receipt'],root_readonly_validation_PID=os.getpid(),root_readonly_validation_PASS=True,semantic_slot_alias_only='Native contains identical scopes and scopes_senses fields; canonical reader uses scopes. No native or mathematical content changed.',source_verdict=False,VERIFIED=False))
new(r/'source-review.packet.json',rt.semantic_reviewer_packet(audit))
print('PASS76 CLOSED4 strict-blind reconstruction adopted without native changes; canonical anti-anchored reviewer packet generated. Clean finite source dispatch remains pending.')
