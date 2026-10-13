from pathlib import Path
import hashlib,json,sys
sys.path.insert(0,str(Path.cwd()/'tools'));import astis_publication as pub,astis_semantic_roundtrip as rt
r=Path(__file__).parent;d=r/'eof-whitespace-repair86';load=lambda p:json.loads(Path(p).read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest()
def save(p,x):Path(p).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
def pin(p):p=Path(p);return dict(path=p.as_posix(),RAW_sha256=sha(p.read_bytes()),bytes=p.stat().st_size)
checks=[(r/'eof-math-review86/closed-RAW-manifest86.json','cbe9400b4cb36dacc26f90f4a4ac3573380fb0223a1e4f419d627991b6062362'),(r/'eof-source-review86/eof-source-review86.native-RAW-manifest.json','a3a9f78c5bafbb7d319c4cb075f44f66ee4426701f3374a154b4a120cd1905a7'),(r/'eof-source-review86/eof-source-review86.metadata-supplement.native-RAW-manifest.json','efc68f048acbffc6bf064d5bf170437aaa84a1e4927da3ac4f049e5c2e9c5374')]
for p,h in checks:
 assert pin(p)['RAW_sha256']==h
 for rows in load(p).values():
  if isinstance(rows,list):
   for x in rows:
    if isinstance(x,dict) and 'path' in x and ('raw_sha256' in x or 'RAW_sha256' in x):assert sha(Path(x['path']).read_bytes())==(x.get('raw_sha256') or x['RAW_sha256']),x['path']
m=Path('AutoSamplingTheory/ExampleCases/ProximalBPS/ActualFiniteFirstEventLaw.lean');old=m.read_bytes();new=(d/'module.proposed.exactraw.lean').read_bytes();assert old==new+b'\n'
lp=Path('website/content/declaration_lessons/pbps-actual-finite-first-event-law.json');ap=Path('research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261011-PBPSActualFiniteFirstEventLaw.json')
assert not (d/'lesson.before.exactraw.json').exists()
(d/'lesson.before.exactraw.json').write_bytes(lp.read_bytes());(d/'audit.before.exactraw.json').write_bytes(ap.read_bytes())
l=load(lp);a=load(ap);packet=rt.decoder_packet(a);count=0
for step in l['units'][0]['steps']:
 region=step['lean_source_region'];assert region['source_raw_sha256']==sha(old);region['source_raw_sha256']=sha(new);count+=1
assert count==11 and l==load(r/'eof-source-review86/eof-lesson-metadata.expected-structure.json')
m.write_bytes(new);save(lp,l)
a.update(state='blind-reconstructed',source_review=dict(state='pending'))
for k in ['semantic_slots','deltas','verdict']:a.pop(k,None)
a['lean']['compiler_evidence']=(r/'eof-math-review86/fresh-proposed-source.receipt.json').as_posix()
pub.inputs.cache_clear();pub.load.cache_clear();data=pub.inputs();matches=[(item,b) for item in pub.load() for b in item['bindings'] if b['declaration']==a['lean']['declaration']];assert len(matches)==1;item,b=matches[0]
a['publication_binding_sha256']=pub.binding_digest(item,b,data);a['publication_context']=pub.review_context(item,b,data)
assert rt.decoder_packet(a)==packet==load(r/'anonymous.decoder86.json')
save(ap,a);review=rt.semantic_reviewer_packet(a);save(r/'source-review86.eof-successor.packet.json',review)
record=dict(status='DISTINCT_REVIEWED_EOF_AND11_PROVENANCE_FIELDS_APPLIED',math_manifest=pin(checks[0][0]),source_manifest=pin(checks[1][0]),metadata_manifest=pin(checks[2][0]),module=pin(m),lesson=pin(lp),original_module=pin(d/'module.before.exactraw.lean'),original_lesson=pin(d/'lesson.before.exactraw.json'),original_audit=pin(d/'audit.before.exactraw.json'),decoder_packet_byte_unchanged=True,source_proof_regions_unchanged=True,source_graph_unchanged=True,publication_binding_sha256=a['publication_binding_sha256'],new_review_packet=pin(r/'source-review86.eof-successor.packet.json'),new_review_packet_sha256=review['packet_sha256'],final_source_rebinding='pending',VERIFIED=False,Goal_complete=False)
save(r/'root.eof86.adoption.json',record);print('Applied exact EOF+11 metadata pins; blind unchanged; new source packet',review['packet_sha256'])
