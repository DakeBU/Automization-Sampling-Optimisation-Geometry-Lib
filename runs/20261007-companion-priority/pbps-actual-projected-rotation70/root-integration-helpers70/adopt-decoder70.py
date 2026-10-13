from pathlib import Path
import base64,hashlib,json,os,sys
root=Path.cwd();sys.path.insert(0,str(root/'tools'));import astis_semantic_roundtrip as rt
r=Path('runs/20261007-companion-priority/pbps-actual-projected-rotation70');neutral=Path('.astis/decoder-70');owned=neutral/'independent'
load=lambda p:json.loads(Path(p).read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest();can=lambda x:json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def pin(p):
 p=Path(p);b=p.read_bytes();return dict(path=p.resolve().as_posix(),raw_bytes=len(b),raw_sha256=sha(b),lf_sha256=sha(b.replace(b'\r\n',b'\n')))
def new(p,x):
 p=Path(p);assert not p.exists();p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
lease=load(owned/'lease.json');manifest=load(owned/'native-manifest.json');run=load(owned/'review-run.json');decoded=load(owned/'decoded0.json')
assert sha((owned/'lease.json').read_bytes())=='0e3ebaabee5bdfd8d133ecf3a7426d9fad79a13ae4b557e1f321fec382caeb75'
assert lease['status']=='CLOSED_LAST' and lease['last_owned_write']=='lease.json' and lease['no_further_owned_writes']
assert lease['decoder']=='/root/anonymous_decoder70'
actual={p.relative_to(owned).as_posix() for p in owned.rglob('*') if p.is_file()}
assert len(actual)==lease['owned_count']==12 and actual==set(manifest['owned_paths_including_manifest_and_final_lease'])
assert actual=={z['path'] for z in lease['bindings']}|{'lease.json'}
assert sha((owned/'native-manifest.json').read_bytes())==lease['native_manifest_raw_sha256']=='c6a4f042436905f9c7fd7e6906e08dd90a17d71e6c805caabe77fff893b0d803'
for z in lease['bindings']:
 p=owned/z['path'];b=p.read_bytes();assert len(b)==z['bytes'] and sha(b)==z['raw_sha256']
 assert p.stat().st_mtime_ns<=(owned/'lease.json').stat().st_mtime_ns
h=sha(can({k:v for k,v in run.items() if k!='run_sha256'}))
assert h==run['run_sha256']==lease['whole_logical_run_sha256']==decoded['decoder_run_sha256']=='3aad134994eb41f93585de3a3a346bf38fd04ad1273a8b72c30e39e96fbd848e'
assert not any(run['visibility'].values()) and not decoded['source_text_visible'] and not decoded['source_identity_visible']
assert all(t['exit_code']==0 for t in run['terminal_receipts']) and len(run['slot_decisions'])==23
for key in ['objects','domains','quantifiers','assumptions','conclusion','scopes','constant_dependencies']:assert isinstance(decoded[key],str) and decoded[key]
assert decoded['text']==run['reconstruction']['text'] and sha(decoded['text'].encode())==decoded['reconstructed_text_sha256']
complete=load(owned/'complete-reconstruction-decision-input.raw.json')
assert sha((owned/'complete-reconstruction-decision-input.raw.json').read_bytes())=='b1488832d93b7f03096cb4e6c71a3300a70e7aa4330877e831096ac9e3dc18cc'
assert complete['whole_review_run']==run and complete['decoded0']==decoded
for z in complete['exact_finite_inputs']:
 assert z['encoding']=='base64';b=base64.b64decode(z['payload'],validate=True)
 assert len(b)==z['bytes'] and sha(b)==z['raw_sha256'] and b==(owned/z['name']).read_bytes()
packet=load(neutral/'packet0.json');assert rt.sha256_json({k:v for k,v in packet.items() if k!='packet_sha256'})==packet['packet_sha256']==decoded['decoder_packet_sha256']
assert (owned/'packet0.raw.json').read_bytes()==(neutral/'packet0.json').read_bytes()
assert (owned/'packet0.lf.json').read_bytes()==(neutral/'packet0.json').read_bytes().replace(b'\r\n',b'\n')
assert (owned/'statement.utf8.txt').read_bytes()==packet['lean']['statement'].encode()
assert json.loads((owned/'approved-definition-context.utf8.json').read_bytes())==packet['lean']['approved_definition_context']
assert load(neutral/'lease.json')['status']=='OPEN' and (neutral/'lease.json').read_bytes()==(neutral/'initial-lease.raw.snapshot.json').read_bytes()
ap=Path('research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261009-PBPSActualProjectedRotation.json');audit=load(ap)
assert audit['state']=='draft' and rt.decoder_packet(audit)==packet==load(r/'anonymous.0.decoder.json')
archive=r/'anonymous-decoder';archive.mkdir(exist_ok=False);maps=[]
for name in sorted(actual):
 p=archive/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes((owned/name).read_bytes());maps.append(dict(original=pin(owned/name),exact_RAW_archive=pin(p)))
for name in ['packet0.json','initial-lease.raw.snapshot.json','lease.json']:
 p=archive/('parent-lease.open.json' if name=='lease.json' else 'parent-'+name);p.write_bytes((neutral/name).read_bytes())
adapter=archive/'decoded0.root-adapter.json'
new(adapter,dict(native_complete_payload=complete,native_named_payload=pin(archive/'complete-reconstruction-decision-input.raw.json'),native_whole_logical_run_sha256=h,native_bytes_unchanged=True,actual_root_adopter_PID=os.getpid()))
before=r/'audit.before-decoder70.exactraw.snapshot.json';assert not before.exists();before.write_bytes(ap.read_bytes())
audit.update(state='blind-reconstructed',reconstruction=dict(text=decoded['text'],text_sha256=decoded['reconstructed_text_sha256'],decoder=decoded['decoder'],decoder_run_sha256=h,decoder_packet_sha256=packet['packet_sha256'],source_text_visible=False,lean_statement_sha256=audit['lean']['statement_sha256'],input_artifacts=['lean-statement','approved-definition-context'],observed_input_artifacts=[pin(archive/'parent-packet0.json')],run_artifact=adapter.as_posix(),run_binding=(archive/'lease.json').as_posix(),native_named_payload_sha256='b1488832d93b7f03096cb4e6c71a3300a70e7aa4330877e831096ac9e3dc18cc',run_hash_recipe='Canonical sorted compact UTF8 whole review-run deleting ONLY top-level run_sha256.'))
ap.write_text(json.dumps(audit,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
new(r/'root.decoder70.adoption.json',dict(status='CLOSED_BLIND_DECODER70_ADOPTED_ONLY',actual_root_PID=os.getpid(),native_whole_logical_run_sha256=h,native_owned_files=12,native_lease_RAW_sha256=sha((owned/'lease.json').read_bytes()),native_complete_named_RAW_sha256='b1488832d93b7f03096cb4e6c71a3300a70e7aa4330877e831096ac9e3dc18cc',exact_RAW_mappings=maps,source_text_visible=False,source_identity_visible=False,source_verdict=False,VERIFIED=False))
official=rt.semantic_reviewer_packet(audit);new(r/'source-review.packet.0.json',official)
new(r/'source-review.freeze70.json',dict(status='EXACT_CURRENT70_SOURCE_REVIEW_PACKET_FROZEN',packet=pin(r/'source-review.packet.0.json'),audit=pin(ap),source_body=pin(audit['lean']['file']),publication=pin('website/content/publications/pbps-actual-projected-rotation.json'),lesson=pin('website/content/declaration_lessons/pbps-actual-projected-rotation.json'),frontier=pin('research-wiki/frontier-cells/ASTIS-SW-PBPS-actual-projected-rotation.json'),source_review=False,VERIFIED=False))
print('PASS native CLOSED12 source-blind reconstruction70 adopted; official current whole-module/source/publication reviewer packet frozen. Source verdict and VERIFIED pending.')
