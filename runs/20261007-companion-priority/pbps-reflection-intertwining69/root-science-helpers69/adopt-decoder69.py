from pathlib import Path
import hashlib,json,os,sys
sys.path.insert(0,'tools')
import astis_semantic_roundtrip as rt,astis_publication as pub
root=Path.cwd();r=Path('runs/20261007-companion-priority/pbps-reflection-intertwining69');n=Path('.astis/decoder-69');d=n/'independent'
load=lambda p:json.loads(Path(p).read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest()
can=lambda x:json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def pin(p):
 p=Path(p);b=p.read_bytes();return dict(path=p.resolve().as_posix(),raw_bytes=len(b),raw_sha256=sha(b),lf_sha256=sha(b.replace(b'\r\n',b'\n')))
def w(p,x):
 p=Path(p);assert not p.exists(),p;p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
lease=load(d/'lease.json');m=load(d/'manifest.json');run=load(d/'review-run.json');decoded=load(d/'decoded0.json')
assert sha((d/'lease.json').read_bytes())=='d0bd3726d7d2fe513be150d663ceb6e4aa729d2b409360acbe585a7ecadc9c86'
assert lease['status']=='CLOSED_LAST' and lease['last_owned_write']=='lease.json' and lease['owner']=='/root/anonymous_decoder69'
assert sha((d/'manifest.json').read_bytes())==lease['manifest_raw_sha256']=='a318296d19bd654f4c32c875c882e066f6f8331f0ee7270052bc213c2ae699f6'
actual={p.relative_to(d).as_posix() for p in d.rglob('*') if p.is_file()}
assert actual==set(m['all_owned_files']) and len(actual)==lease['owned_regular_file_count']==17
assert len(m['entries'])==15 and actual=={z['path'] for z in m['entries']}|{'manifest.json','lease.json'}
last=(d/'lease.json').stat().st_mtime_ns
for z in m['entries']:
 p=d/z['path'];b=p.read_bytes();assert len(b)==z['raw_bytes'] and sha(b)==z['raw_sha256'] and p.stat().st_mtime_ns<=last,p
assert (d/'manifest.json').stat().st_mtime_ns<=last
h=run['run_sha256'];assert sha(can({k:v for k,v in run.items() if k!='run_sha256'}))==h==lease['whole_logical_sha256']=='e660f49813646393e7ccc2c927545e0ad62ef84f63cd10e0874c0adf00f2d05b'
assert sha((d/'anonymous_reconstruction_69.json').read_bytes())=='95f81b646e7cdbecb588f14acd070caa65394cde323028a3b8291b408fbc8700'
assert not decoded['source_text_visible'] and not run['source_text_visible']
assert decoded['decoder']=='/root/anonymous_decoder69'
assert all(isinstance(decoded[k],str) and decoded[k] for k in ['objects','domains','quantifiers','assumptions','conclusion','scopes','constant_dependencies'])
assert sha(decoded['text'].encode())==decoded['reconstructed_text_sha256']==sha(run['reconstructed_theorem_text'].encode())
assert decoded['decoder_run_sha256']==h
for z in run['observed_input_artifacts'].values():
 b=(d/z['raw_path']).read_bytes();lf=b.replace(b'\r\n',b'\n')
 assert len(b)==z['raw_bytes'] and sha(b)==z['raw_sha256'] and sha(lf)==z['lf_sha256'] and (d/z['lf_path']).read_bytes()==lf
packet=load(n/'packet0.json')
assert (d/'inputs/packet0.raw.json').read_bytes()==(n/'packet0.json').read_bytes()
assert (d/'inputs/lean-statement.raw.txt').read_bytes()==packet['lean']['statement'].encode()
assert json.loads((d/'inputs/approved-definition-context.raw.json').read_bytes())==packet['lean']['approved_definition_context']
assert rt.sha256_json({k:v for k,v in packet.items() if k!='packet_sha256'})==packet['packet_sha256']==decoded['decoder_packet_sha256']
assert load(n/'lease.json')['status']=='OPEN' and (n/'lease.json').read_bytes()==(n/'initial-lease.raw.snapshot.json').read_bytes()
ap=Path('research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261009-PBPSActualReflectionIntertwining.json');audit=load(ap)
assert audit['state']=='draft' and rt.decoder_packet(audit)==packet==load(r/'anonymous.0.decoder.json')
assert decoded['lean_statement_sha256']==audit['lean']['statement_sha256']
dest=r/'anonymous-decoder';dest.mkdir(exist_ok=False);maps=[]
for rel in sorted(actual):
 target=dest/rel;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes((d/rel).read_bytes());maps.append(dict(original=pin(d/rel),explicit_exact_raw_snapshot=pin(target)))
for name in ['packet0.json','initial-lease.raw.snapshot.json','lease.json']:
 target=dest/('parent-lease.open.json' if name=='lease.json' else name);target.write_bytes((n/name).read_bytes())
adapter=dest/'decoded0.root-adapter.json'
w(adapter,dict(native_complete_payload=load(dest/'anonymous_reconstruction_69.json'),native_payload=pin(dest/'anonymous_reconstruction_69.json'),whole_logical_run_sha256=h,native_named_payload_RAW_sha256='95f81b646e7cdbecb588f14acd070caa65394cde323028a3b8291b408fbc8700',native_bytes_unchanged=True,actual_root_read_only_adopter_pid=os.getpid()))
(r/'audit.0.before-decoder.exactraw.snapshot.json').write_bytes(ap.read_bytes())
audit.update(state='blind-reconstructed',reconstruction=dict(text=decoded['text'],text_sha256=decoded['reconstructed_text_sha256'],decoder=decoded['decoder'],decoder_run_sha256=h,decoder_packet_sha256=packet['packet_sha256'],source_text_visible=False,lean_statement_sha256=audit['lean']['statement_sha256'],input_artifacts=['lean-statement','approved-definition-context'],observed_input_artifacts=[pin(dest/'packet0.json')],run_artifact=adapter.as_posix(),run_binding=(dest/'lease.json').as_posix(),native_named_payload_sha256='95f81b646e7cdbecb588f14acd070caa65394cde323028a3b8291b408fbc8700',run_hash_recipe='Canonical sorted compact UTF8 whole review-run after deleting ONLY top-level run_sha256.'))
ap.write_text(json.dumps(audit,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
w(r/'root.decoder69.adoption.json',dict(status='CLOSED_BLIND_DECODER69_ADOPTED',actual_adopter_pid=os.getpid(),native_whole_logical_run_sha256=h,native_complete_named_RAW_sha256='95f81b646e7cdbecb588f14acd070caa65394cde323028a3b8291b408fbc8700',native_owned_files=17,raw_snapshot_mappings=maps,source_text_visible=False,source_identity_visible=False,compiler_started=False,native_parent_lease_preserved_OPEN=True,source_verdict=False,VERIFIED=False,official_reviewer_packet_deferred_until_exact_reader_overlay=True))
print('PASS CLOSED17 source-blind reconstruction69 adopted; exact source reviewer packet awaits reviewed reader metadata overlay.')
