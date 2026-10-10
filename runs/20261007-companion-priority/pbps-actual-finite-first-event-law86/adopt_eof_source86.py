from pathlib import Path
import hashlib,json,sys
sys.path.insert(0,str(Path.cwd()/'tools'))
import astis_semantic_roundtrip as rt,astis_publication as pub
r=Path(__file__).parent;d=r/'independent-source86'
load=lambda p:json.loads(Path(p).read_bytes())
sha=lambda b:hashlib.sha256(b).hexdigest()
def save(p,x):Path(p).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
def pin(p):p=Path(p);return dict(path=p.as_posix(),RAW_sha256=sha(p.read_bytes()),RAW_bytes=p.stat().st_size)
stem=d/'source-review86.eof-rebound.final'
decision=Path(str(stem)+'.decision.json');manifest=Path(str(stem)+'.native-RAW-manifest.json');run=Path(str(stem)+'.run.json')
assert pin(decision)['RAW_sha256']=='a3b010d144852bac09f5bd2593df6c679ad9a76d211bfbf58ed6521ab707c30c'
assert pin(manifest)['RAW_sha256']=='9858b71471853117b1f959ce1efb2a9405722ce461c6559ee9782e0ff0b1ee0e'
for group in ['inputs','outputs']:
 for x in load(manifest)[group]:assert sha(Path(x['path']).read_bytes())==x['raw_sha256'],x['path']
n=load(decision);assert n['verdict']=='equivalent-after-elaboration' and not n['repairs']
assert n['independent_from_formalizer'] and n['independent_from_decoder']
assert pin(run)['RAW_sha256']==n['review_run_sha256']
ap=Path('research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261011-PBPSActualFiniteFirstEventLaw.json');a=load(ap)
assert a['state']=='blind-reconstructed'
packet=rt.semantic_reviewer_packet(a);assert packet==load(r/'source-review86.eof-successor.packet.json')
assert packet['packet_sha256']==n['reviewer_packet_sha256'] and a['publication_binding_sha256']==n['publication_binding_sha256']
assert sha(Path(a['lean']['file']).read_bytes())==n['full_module_sha256']
assert (r/'anonymous.decoder86.json').read_bytes()==(r/'eof-whitespace-repair86/anonymous.eof-successor.packet.json').read_bytes()
assert set(n['semantic_slots'])==set(rt.SEMANTIC_SLOTS)
deltas=[dict(slot=x['slot'],severity='blocking' if x['blocking'] else 'informational',description=x['description'],evidence=decision.as_posix(),native_classification=x['classification']) for x in n['deltas']]
assert all(x['severity']=='informational' for x in deltas)
a.update(state='accepted',semantic_slots=n['semantic_slots'],deltas=deltas,verdict=n['verdict'],source_review=dict(state='accepted',reviewer=n['reviewer'],independent_from_formalizer=True,independent_from_decoder=True,evidence=n['review_evidence'],review_run_sha256=n['review_run_sha256'],reviewer_packet_sha256=n['reviewer_packet_sha256'],run_artifact=run.as_posix(),native_manifest=pin(manifest)))
save(ap,a);pub.inputs.cache_clear();pub.load.cache_clear();pub.check_advance([a['lean']['declaration']],reviewed=True)
out=r/'root.source86.eof-adoption.json';assert not out.exists()
save(out,dict(status='ACCEPTED_INDEPENDENT_SOURCE_EOF_REBINDING',publication_binding_current=True,publication_binding_sha256=a['publication_binding_sha256'],native_decision=pin(decision),native_manifest=pin(manifest),native_run=pin(run),full_current_module_RAW_sha256=n['full_module_sha256'],anonymous_byte_identical=True,VERIFIED=False))
claim=load(r/'claim.json');cp=Path('research-wiki/frontier-cells')/(claim['frontier_cell']+'.json');c=load(cp)
c['evidence']['source_review']=decision.as_posix();c['source_proof_coverage']['compiled_source_review']=decision.as_posix();save(cp,c)
print('Accepted independent EOF source rebinding; exact-commit verification remains pending')
