from pathlib import Path
import hashlib,json,os,sys
root=Path.cwd();sys.path.insert(0,str(root/'tools'));import astis_semantic_roundtrip as rt
r=Path('runs/20261007-companion-priority/pbps-actual-corrector-change71');neutral=Path('.astis/decoder-71');owned=neutral/'independent'
load=lambda p:json.loads(Path(p).read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest();can=lambda x:json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def pin(p):
 p=Path(p);b=p.read_bytes();return dict(path=p.resolve().as_posix(),RAW_bytes=len(b),RAW_sha256=sha(b),LF_sha256=sha(b.replace(b'\r\n',b'\n')))
def new(p,x):
 p=Path(p);assert not p.exists(),p;p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
lease=load(owned/'lease.closed.json');manifest=load(owned/'manifest.json');run=load(owned/'decoder-run.json');decoded=load(owned/'decoded0.json')
assert sha((owned/'lease.closed.json').read_bytes())=='6160826050ccb3d4ba63428b1e551bcee4f4b2d9f828be76e9fc3d184a019042'
assert lease['status']=='CLOSED_LAST' and lease['last_owned_write'] and lease['source_text_visible'] is False
actual={p.relative_to(owned).as_posix() for p in owned.rglob('*') if p.is_file()}
assert len(actual)==lease['owned_file_count_including_lease']==10 and actual=={z['name'] for z in lease['covered_files']}|{'lease.closed.json'}
assert sha((owned/'manifest.json').read_bytes())==lease['manifest_raw_sha256']
for z in lease['covered_files']:
 p=owned/z['name'];b=p.read_bytes();assert len(b)==z['byte_count'] and sha(b)==z['raw_sha256']
 assert p.stat().st_mtime_ns<=(owned/'lease.closed.json').stat().st_mtime_ns
assert len(manifest['files'])==8 and {z['name'] for z in manifest['files']}==actual-{'manifest.json','lease.closed.json'}
for z in manifest['files']:
 b=(owned/z['name']).read_bytes();assert len(b)==z['byte_count'] and sha(b)==z['raw_sha256']
h=sha(can({k:v for k,v in run.items() if k!='run_sha256'}));assert h==run['run_sha256']==lease['decoder_run_sha256']==decoded['decoder_run_sha256']=='c846e44be094734fda524a511d088f70358100518df56260ccaae31dc76add97'
assert all(run[k] is False for k in ['source_text_visible','source_identity_visible','proof_BODY_visible','search_performed','compiler_invoked','external_source_used'])
assert run['slot_count']==decoded['slot_count']==51 and decoded['unresolved_count']==0 and not decoded['source_fidelity_assessed']
for key in ['objects','domains','quantifiers','assumptions','conclusion','scopes','constant_dependencies']:assert isinstance(decoded[key],(str,list,dict)) and decoded[key]
text=decoded['reconstructed_theorem_text'];assert text.encode()==(owned/'reconstruction.utf8.txt').read_bytes() and sha(text.encode())==decoded['reconstructed_text_sha256']==run['reconstructed_text_sha256']
packet=load(neutral/'packet0.json');full=sha(can(packet));official=rt.sha256_json({k:v for k,v in packet.items() if k!='packet_sha256'})
assert full==decoded['packet_sha256']==lease['packet_sha256']=='b40612aa42fec0d1ccecc0780f358189c4930ff0fb9f76dc113f72cd8c17906a'
assert official==packet['packet_sha256']==decoded['embedded_packet_sha256']=='40f89c5d744327796abf647c5e6fafbb2e22aa4ad14a4a1d2cae016f0d7420c9'
assert (owned/'packet0.json.raw.sealed').read_bytes()==(neutral/'packet0.json').read_bytes()
assert (owned/'lease.open.json.raw.sealed').read_bytes()==(neutral/'lease.open.json').read_bytes()
payload=load(owned/'input-payload.json');assert payload['lean_statement']==packet['lean']['statement'] and payload['approved_definition_context']==packet['lean']['approved_definition_context']
assert payload['lean_statement_utf8_sha256']==sha(packet['lean']['statement'].encode())==decoded['input_statement_utf8_sha256']
ap=Path('research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261010-PBPSActualCorrectorChange.json');audit=load(ap)
assert audit['state']=='draft' and rt.decoder_packet(audit)==packet==load(r/'anonymous.0.decoder.json')
archive=r/'anonymous-decoder';archive.mkdir(exist_ok=False);maps=[]
for name in sorted(actual):
 p=archive/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes((owned/name).read_bytes());maps.append(dict(original=pin(owned/name),exact_RAW_archive=pin(p)))
for name in ['packet0.json','lease.open.json']:(archive/('parent-'+name)).write_bytes((neutral/name).read_bytes())
adapter=archive/'decoded0.root-adapter.json'
new(adapter,dict(native_complete_decoded0=decoded,native_complete_run=run,native_complete_named_RAW=pin(archive/'decoded0.json'),native_whole_logical_run_sha256=h,native_full_packet_canonical_sha256=full,official_decoder_packet_payload_sha256=official,hash_convention_mapping='Native hashes whole packet including embedded field; official protocol hashes exact packet with ONLY top-level packet_sha256 omitted. Both independently computed, native bytes preserved.',native_bytes_unchanged=True,actual_root_adopter_PID=os.getpid()))
before=r/'audit.before-decoder71.exactraw.snapshot.json';assert not before.exists();before.write_bytes(ap.read_bytes())
audit.update(state='blind-reconstructed',reconstruction=dict(text=text,text_sha256=decoded['reconstructed_text_sha256'],decoder=decoded['decoder'],decoder_run_sha256=h,decoder_packet_sha256=official,source_text_visible=False,lean_statement_sha256=audit['lean']['statement_sha256'],input_artifacts=['lean-statement','approved-definition-context'],observed_input_artifacts=[pin(archive/'parent-packet0.json')],run_artifact=adapter.as_posix(),run_binding=(archive/'lease.closed.json').as_posix(),native_named_payload_sha256=sha((owned/'decoded0.json').read_bytes()),native_full_packet_canonical_sha256=full,run_hash_recipe=run['run_hash_rule']))
ap.write_text(json.dumps(audit,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
new(r/'root.decoder71.adoption.json',dict(status='CLOSED_BLIND_DECODER71_ADOPTED_ONLY',actual_root_PID=os.getpid(),native_whole_logical_run_sha256=h,native_owned_files=10,native_lease_RAW_sha256=sha((owned/'lease.closed.json').read_bytes()),native_complete_named_RAW_sha256=sha((owned/'decoded0.json').read_bytes()),native_full_packet_canonical_sha256=full,official_decoder_packet_payload_sha256=official,exact_RAW_mappings=maps,source_text_visible=False,source_identity_visible=False,source_verdict=False,VERIFIED=False))
new(r/'source-review.packet.0.json',rt.semantic_reviewer_packet(audit))
new(r/'source-review.freeze71.json',dict(status='EXACT_CURRENT71_SOURCE_REVIEW_PACKET_FROZEN',packet=pin(r/'source-review.packet.0.json'),audit=pin(ap),source_body=pin(audit['lean']['file']),publication=pin('website/content/publications/pbps-actual-corrector-change.json'),lesson=pin('website/content/declaration_lessons/pbps-actual-corrector-change.json'),frontier=pin('research-wiki/frontier-cells/ASTIS-SW-PBPS-actual-corrector-change.json'),source_review=False,VERIFIED=False))
print('PASS native CLOSED10 blind reconstruction71 adopted; both packet hash recipes explicit; official source packet frozen. Source/VERIFIED pending.')
