from pathlib import Path
import json,hashlib,sys
sys.path.insert(0,str(Path('tools').resolve()))
import astis_semantic_roundtrip as rt,astis_publication as pub
r=Path('runs/20261007-companion-priority/pbps-real-complex-lift60');n=Path('.astis/decoder-60');d=n/'independent';load=lambda p:json.loads(Path(p).read_bytes());sha=lambda a:hashlib.sha256(a).hexdigest();can=lambda x:json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def w(p,x):
 p=Path(p);assert not p.exists(),p;p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
def pin(p):
 p=Path(p);a=p.read_bytes();return dict(path=p.resolve().as_posix(),raw_bytes=len(a),raw_sha256=sha(a),lf_sha256=sha(a.replace(b'\r\n',b'\n')))
seen=set();history=[]
def walk(x):
 if isinstance(x,dict):
  if {'path','raw_sha256'}<=x.keys():
   p=Path(x['path']);key=(p.resolve().as_posix(),x['raw_sha256'],x.get('lf_sha256'))
   if key not in seen:
    q=pin(p)
    if q['raw_sha256']!=x['raw_sha256']:
     assert p.resolve()==(n/'lease.json').resolve();q=pin(n/'initial-lease.raw.snapshot.json');assert q['raw_sha256']==x['raw_sha256'];history.append(dict(original=x,exact_raw_snapshot=q))
    assert q['raw_sha256']==x['raw_sha256']
    if 'lf_sha256' in x:assert q['lf_sha256']==x['lf_sha256']
    for k in ['bytes','raw_bytes','raw_byte_count']:
     if k in x:assert q['raw_bytes']==x[k]
    seen.add(key)
  for v in x.values():walk(v)
 elif isinstance(x,list):
  for v in x:walk(v)
m=r/'independent-math60';mr=load(m/'run.json');ml=load(m/'lease.json');mp=load(m/'payload.json');assert ml['status']=='CLOSEDLAST' and ml['compiler_exit_code']==ml['readback_exit_code']==0
assert sha(can({k:v for k,v in mr.items() if k!='run_sha256'}))==mr['run_sha256']=='118a9fcc70b76ddfb9ac9a5a65aba50b24a3b94b3a78211290990970578f392f';assert sha(can(mr['named_mathematics_payload']))==mr['named_mathematics_payload_sha256']=='3be958e33d66b76d95b031891cf071974b3f46f0052866cd8e5030db5d419662';assert mp['verdict']=='ACCEPT_SCOPED_COMPLETE_MATHEMATICS_NO_BLOCKER'
for p in m.glob('*.json'):walk(load(p))
w(r/'root.math60.adoption.json',dict(status='INDEPENDENT_PRECOMMIT_SCOPED_MATHEMATICS_ACCEPTED',run_sha256=mr['run_sha256'],named_mathematics_payload_sha256=mr['named_mathematics_payload_sha256'],qualified_pin_readbacks=len(seen),complete_proofs_reviewed=True,focused_build='Actual20996 EXIT0 PASS3915; own pre-run input hashes; standard3.',checked_base_commit=mr['checked_base_commit'],VERIFIED=False,full_paper=False))
seen.clear();dr=load(d/'run.json');dl=load(n/'lease.json');dp=load(d/'decoder-payload.json');assert dl['status']=='CLOSED' and dl['final_readback_exit_code']==dl['first_readback_exit_code']==0;assert dr['source_text_visible']==dr['source_identity_visible']==dr['compiler_started']==False;assert not dr['repo_bodies_history_audits_or_memory_read'];assert sha(can({k:v for k,v in dr.items() if k!='run_sha256'}))==dr['run_sha256']==dl['run_sha256']=='5f24bed1022150105b9c2eebb93ec1a975203a81ffced3ae1e9afb8aa52539c7';assert sha(can(dp['payload']))==dp['payload_sha256']==dr['payload_sha256']=='d3a6e3dd1faa57f0c8242e1305e36c86a1fca54024025af1a88304ab82eed4d9'
for p in d.glob('*.json'):walk(load(p))
plan=load(r/'publication-plan.json');audits=[];packets=[];pub.inputs.cache_clear();pub.load.cache_clear();data=pub.inputs()
for i,(aid,slug) in enumerate(zip(plan['audit_ids'],plan['slugs'])):
 packet=load(n/f'packet{i}.json');assert packet==load(r/f'anonymous.{i}.decoder.json');assert rt.sha256_json({k:v for k,v in packet.items() if k!='packet_sha256'})==packet['packet_sha256'];q=load(d/f'decoded{i}.json');assert q['decoder_run_sha256']==dp['payload_sha256'];assert q['source_text_visible']==q['source_identity_visible']==False;assert sha(q['reconstructed_theorem_text'].encode())==q['reconstructed_text_sha256'];assert all(q[k] for k in ['objects','domains','quantifiers','assumptions','conclusion','scopes','constant_dependencies']);inp=dr['actual_input_manifest']['inputs'][i];assert inp['canonical_decoder_packet_sha256']==packet['packet_sha256'] and inp['statement_sha256']==packet['lean']['statement_sha256']
 p=Path('research-wiki/semantic-roundtrip/audits')/(aid+'.json');a=load(p);assert a['state']=='draft' and rt.decoder_packet(a)==packet;item=next(x for x in pub.load() if x['id']==slug);assert pub.binding_digest(item,item['bindings'][0],data)==a['publication_binding_sha256'];audits.append((p,a,packet,q))
dest=r/'anonymous-decoder';assert not dest.exists();dest.mkdir();mappings=[]
for p in [*d.iterdir(),n/'packet0.json',n/'packet1.json',n/'lease.json',n/'initial-lease.raw.snapshot.json']:
 if p.is_file():
  target=dest/('input-lease.json' if p==n/'lease.json' else p.name);assert not target.exists();target.write_bytes(p.read_bytes());mappings.append(dict(original=pin(p),exact_raw_snapshot=pin(target)))
w(r/'root.decoder60.adoption.json',dict(status='ACTUAL_CLOSED_ANONYMOUS_DECODER_ADOPTED',decoder=dr['decoder'],native_whole_run_sha256=dr['run_sha256'],named_decoder_payload_sha256=dp['payload_sha256'],decoder_run_sha256_field_recipe='Native decoder uses named payload hash in decoded records, explicitly distinguished from full run hash; preserved exactly.',qualified_pin_readbacks=len(seen),historical_lease_resolution=history,source_text_visible=False,source_identity_visible=False,raw_snapshot_mappings=mappings))
for i,(p,a,packet,q) in enumerate(audits):
 (r/f'audit.{i}.before-decoder.raw.snapshot.json').write_bytes(p.read_bytes());a.update(state='blind-reconstructed',reconstruction=dict(text=q['reconstructed_theorem_text'],text_sha256=q['reconstructed_text_sha256'],decoder=dr['decoder'],decoder_run_sha256=q['decoder_run_sha256'],decoder_packet_sha256=packet['packet_sha256'],source_text_visible=False,lean_statement_sha256=a['lean']['statement_sha256'],input_artifacts=['lean-statement','approved-definition-context'],observed_input_artifacts=[pin(dest/f'packet{i}.json')],run_artifact=(dest/f'decoded{i}.json').as_posix(),run_binding=(dest/'run.json').as_posix(),native_whole_run_sha256=dr['run_sha256'],run_hash_recipe='decoder_run_sha256 is named decoder payload; native_whole_run_sha256 is complete native run minus ONLY run_sha256.'));p.write_text(json.dumps(a,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n');sp=rt.semantic_reviewer_packet(a);w(r/f'source.{i}.reviewer-packet.json',sp);packets.append(sp)
pre=Path('runs/20261007-companion-priority/pbps-real-complex-lift-preproof60');primary=pre/'independent-preproof60'
sourceinputs=[primary/'primary.exact-regions.json',primary/'source.graph.json',primary/'source.coverage.json',primary/'cap-source-readback/cap.source.supplement.json']+[Path(x) for x in load(r/'claim.json')['proposed_files']]+[r/f'source.{i}.reviewer-packet.json' for i in range(2)]+[Path('research-wiki/semantic-roundtrip/audits')/(aid+'.json') for aid in plan['audit_ids']]+[r/'publication-plan.json']+[Path('website/content')/folder/(slug+'.json') for folder in ['publications','declaration_lessons'] for slug in plan['slugs']]
w(r/'source.review.lease.json',dict(status='OPEN',reviewer='/root/next_primary59',input_artifacts=[pin(p) for p in sourceinputs],reviewer_packet_sha256=[p['packet_sha256'] for p in packets],compiler_started=False,scope='Primary-first anti-anchored current exact signatures/bodies/formula proofs; no prior postproof semantic verdict or repair. Source graph independently reconstructed before proof and kept distinct from current Lean route.',allowed_outputs=['source-review60/*'],final_closure_order='Original OPEN lease immutable; reviewer own CLOSEDLAST after actual readbacks.'))
pub.inputs.cache_clear();pub.load.cache_clear();pub.check_advance(plan['mathematical_declarations'],reviewed=False)
print('Independent complete mathematics adopted; fresh anonymous decoder bound; two anti-anchored source packets and',len(sourceinputs),'inputs ready. No PROVED_LOCAL/VERIFIED transition yet.')
