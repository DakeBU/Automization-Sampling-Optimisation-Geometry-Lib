from pathlib import Path
import hashlib,json,sys
sys.path.insert(0,str(Path('tools').resolve()));import astis_semantic_roundtrip as rt,astis_publication as pub
r=Path('runs/20261007-companion-priority/pbps-real-root-unique62');n=Path('.astis/decoder-62');d=n/'independent';load=lambda p:json.loads(Path(p).read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest()
def w(p,x):
 p=Path(p);assert not p.exists(),p;p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
def pin(p):
 p=Path(p);b=p.read_bytes();return dict(path=p.resolve().as_posix(),raw_bytes=len(b),raw_sha256=sha(b),lf_sha256=sha(b.replace(b'\r\n',b'\n')))
receipt=load(d/'native-receipt.json');closed=load(d/'lease.CLOSEDLAST.native.json');live=load(n/'lease.json');manifest=load(d/'input-pins.before-semantic-read.json');payload=load(d/'decoder62.statements.payload.raw.json')
assert closed['status']==live['status']=='CLOSED' and closed['closed_last'] and live['closed_last'];assert sha((d/'lease.CLOSEDLAST.native.json').read_bytes())==live['closedlast_native_raw_sha256']=='4baaa8f0fb3ee4ea19ad6dc6f4bc917a267830d20559575540fcbcc0d113c499'
assert sha((d/'decoder62.statements.payload.raw.json').read_bytes())==receipt['payload_raw_sha256']==closed['payload_raw_sha256']=='021383477ab1b11fc0d60acea53a049036a8c6f89d0e4dbe196db25ee42fba94'
assert sha((d/'native-decoder-run.raw.txt').read_bytes())==receipt['decoder_run_sha256']==closed['decoder_run_sha256']=='f0d9a86c64fb8c87677bf5ebf3e7d41a471cb462c9afc851146a735d9c914130'
assert (d/'decoder62.statements.payload.raw.json').read_bytes() in (d/'native-decoder-run.raw.txt').read_bytes()
assert not manifest['semantic_reads_before_receipt'] and manifest['native_pid']==25888 and receipt['native_pid']==9656
assert live['native_terminal_exit_code']==0 and all(x['observed_exit_code']==0 for x in closed['native_terminal_receipts'])
assert not any(receipt[k] or payload[k] or closed[k] for k in ['source_text_visible','source_identity_visible','compiler_started'])
seen=[];history=[]
for q in manifest['inputs']:
 p=Path(q['qualified_input']);snap=Path(q['raw_snapshot']);b=snap.read_bytes();assert sha(b)==q['raw_sha256'] and len(b)==q['raw_bytes'];z=b.decode('utf-8').replace('\r\n','\n').replace('\r','\n').encode();assert sha(z)==q['lf_sha256'] and Path(q['lf_snapshot']).read_bytes()==z and len(z)==q['lf_bytes']
 if p.resolve()==(n/'lease.json').resolve():history.append(dict(original=q,exact_raw_snapshot=pin(snap)))
 else:assert p.read_bytes()==b
 seen.append(q)
for q in closed['closed_output_pins']:
 b=Path(q['path']).read_bytes();assert sha(b)==q['sha256'] and len(b)==q['bytes'];seen.append(q)
plan=load(r/'publication-plan.json');audits=[];pub.inputs.cache_clear();pub.load.cache_clear();data=pub.inputs()
for i,(aid,slug) in enumerate(zip(plan['audit_ids'],plan['slugs'])):
 packet=load(n/f'packet{i}.json');assert packet==load(r/f'anonymous.{i}.decoder.json');assert rt.sha256_json({k:v for k,v in packet.items() if k!='packet_sha256'})==packet['packet_sha256'];q=payload['statements'][i];assert q['input']==f'packet{i}.json' and q['statement_sha256']==packet['lean']['statement_sha256']==receipt['statement_hashes'][i] and q['reconstructed_theorem_text']
 p=Path('research-wiki/semantic-roundtrip/audits')/(aid+'.json');a=load(p);assert a['state']=='draft' and rt.decoder_packet(a)==packet;item=next(x for x in pub.load() if x['id']==slug);assert pub.binding_digest(item,item['bindings'][0],data)==a['publication_binding_sha256'];audits.append((p,a,packet,q))
dest=r/'anonymous-decoder';dest.mkdir(exist_ok=False);mappings=[]
for p in [*d.iterdir(),n/'packet0.json',n/'packet1.json',n/'lease.json',n/'initial-lease.raw.snapshot.json']:
 if p.is_file():
  target=dest/('input-lease.json' if p==n/'lease.json' else p.name);assert not target.exists();target.write_bytes(p.read_bytes());mappings.append(dict(original=pin(p),exact_raw_snapshot=pin(target)))
w(r/'root.decoder62.adoption.json',dict(status='ACTUAL_CLOSED_ANONYMOUS_DECODER_ADOPTED',decoder=payload['decoder'],native_run_sha256=receipt['decoder_run_sha256'],named_decoder_payload_sha256=receipt['payload_raw_sha256'],run_hash_recipe=receipt['run_hash_recipe'],payload_hash_recipe=receipt['payload_hash_recipe'],qualified_pin_readbacks=len(seen),historical_lease_resolution=history,source_text_visible=False,source_identity_visible=False,raw_snapshot_mappings=mappings,native_receipt=pin(dest/'native-receipt.json'),CLOSEDLAST=pin(dest/'lease.CLOSEDLAST.native.json')))
for i,(p,a,packet,q) in enumerate(audits):
 (r/f'audit.{i}.before-decoder.raw.snapshot.json').write_bytes(p.read_bytes());adapter=dest/f'decoded{i}.root-adapter.json';w(adapter,dict(native_payload=pin(dest/'decoder62.statements.payload.raw.json'),native_statement_index=i,native_statement=q,decoder_run_sha256=receipt['decoder_run_sha256'],named_payload_sha256=receipt['payload_raw_sha256'],reconstructed_text_sha256=sha(q['reconstructed_theorem_text'].encode()),native_bytes_unchanged=True))
 a.update(state='blind-reconstructed',reconstruction=dict(text=q['reconstructed_theorem_text'],text_sha256=sha(q['reconstructed_theorem_text'].encode()),decoder=payload['decoder'],decoder_run_sha256=receipt['decoder_run_sha256'],decoder_packet_sha256=packet['packet_sha256'],source_text_visible=False,lean_statement_sha256=a['lean']['statement_sha256'],input_artifacts=['lean-statement','approved-definition-context'],observed_input_artifacts=[pin(dest/f'packet{i}.json')],run_artifact=adapter.as_posix(),run_binding=(dest/'native-receipt.json').as_posix(),native_named_payload_sha256=receipt['payload_raw_sha256'],run_hash_recipe=receipt['run_hash_recipe']))
 p.write_text(json.dumps(a,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n');w(r/f'source.{i}.reviewer-packet.json',rt.semantic_reviewer_packet(a))
print('Fresh native anonymous62 exact raw whole-run/named-payload recipes adopted;',len(seen),'qualified pins; source packets ready. No source verdict/verification.')
