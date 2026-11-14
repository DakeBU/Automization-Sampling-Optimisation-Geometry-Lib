"""Keep mathematical reader scope independent of mutable Harness lifecycle labels."""
from pathlib import Path
import hashlib
import json
import subprocess
import sys
sys.dont_write_bytecode=True
sys.path.insert(0,'tools')
import astis_publication as publication
import astis_semantic_roundtrip as semantic
W=Path(__file__).resolve().parent.relative_to(Path.cwd())
E=Path('research-wiki/paper-contributions/GaussianComplexity/source-matrix-variance-semantic-evidence')
slug='huanjian-gaussian-source-matrix-variance'
LP=Path('website/content/declaration_lessons')/(slug+'.json')
PP=Path('website/content/publications')/(slug+'.json')
AP=Path('research-wiki/semantic-roundtrip/audits')/(slug+'.json')
C=Path('research-wiki/frontier-cells/ASTIS-SW-GAUSSIAN-COMPLEXITY-source-matrix-variance.json')
sha=lambda raw:hashlib.sha256(raw.encode() if isinstance(raw,str) else raw).hexdigest()
dump=lambda obj:(json.dumps(obj,ensure_ascii=False,indent=2)+'\n').encode()
git=lambda *args:subprocess.check_output(['git',*args])
def create(p,raw):
    p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('xb') as f:f.write(raw)
head=git('rev-parse','HEAD').decode().strip()
assert head=='e654e98642350a615c473bc8190fbc1d47fe52bd'
assert not git('diff','HEAD','--name-only') and not git('diff','--cached','--name-only')
old=json.loads((E/'full-consumer-reader-v3b.record.json').read_bytes())
for i,p in enumerate([LP,PP,AP,E/'anti-anchored-reviewer-packet.full-consumer-v3b.json',E/'private-centered-consumer-supplement.full-v3b.json',E/'anti-anchored-private-centered-consumer.full-v3b.json']):
    create(E/'reader-v3b-accepted-snapshot.originals'/(str(i)+'-'+p.name),p.read_bytes())
lesson=json.loads(LP.read_bytes()); pub=json.loads(PP.read_bytes())
scope=('The public declaration proves the actual uncentered squared-moment comparison. '
    'The separate private Tests consumer proves centered and cosine-weighted square integrability and both true operator-norm comparisons in the same original experiment. '
    'Only the uncentered declaration is a public API; the centered and weighted theorem is a private implementation consumer. '
    'Verification and publication evidence is recorded separately in the existing Frontier Cell and semantic audit. '
    'Public API canonicalization, matrix concentration, main lower bounds, exact oracle/precision/TV/query-cap/cost adapters and serialized integration/purification are distinct later obligations.')
assert 'remains EXPLORING' in lesson['units'][0]['sources'][1]['scope']
assert 'remains EXPLORING' in pub['items'][0]['bindings'][0]['boundary']
lesson['units'][0]['sources'][1]['scope']=scope
pub['items'][0]['bindings'][0]['boundary']=scope
LP.write_bytes(dump(lesson)); PP.write_bytes(dump(pub))
assert 'remains EXPLORING' not in LP.read_text()+PP.read_text()
audit=json.loads(AP.read_bytes()); pdecoder=semantic.decoder_packet(audit)
publication.inputs.cache_clear(); publication.load.cache_clear()
item=pub['items'][0]; binding=item['bindings'][0]
audit['publication_binding_sha256']=publication.binding_digest(item,binding)
audit['publication_context']=publication.review_context(item,binding)
assert semantic.decoder_packet(audit)==pdecoder
AP.write_bytes(dump(audit))
ppacket=semantic.semantic_reviewer_packet(audit)
ppath=E/'anti-anchored-reviewer-packet.full-consumer-v3c.json'
create(ppath,dump(ppacket))
supp=json.loads((E/'private-centered-consumer-supplement.full-v3b.json').read_bytes()); tdecoder=semantic.decoder_packet(supp)
supp['publication_binding_sha256']=audit['publication_binding_sha256']; supp['publication_context']=audit['publication_context']
assert semantic.decoder_packet(supp)==tdecoder
spath=E/'private-centered-consumer-supplement.full-v3c.json'; create(spath,dump(supp))
tpacket=semantic.semantic_reviewer_packet(supp)
tpath=E/'anti-anchored-private-centered-consumer.full-v3c.json'; create(tpath,dump(tpacket))
record={**old,'publication_binding_sha256':audit['publication_binding_sha256'],
    'anti_anchored_packet':str(ppath),'anti_raw_sha256':sha(ppath.read_bytes()),'anti_canonical_packet_sha256':ppacket['packet_sha256'],
    'private_T_supplement':str(spath),'private_T_anti_packet':str(tpath),'private_T_anti_raw_sha256':sha(tpath.read_bytes()),'private_T_anti_canonical_sha256':tpacket['packet_sha256'],
    'v3c_reason':'Remove only two hardcoded current lifecycle-state sentences from mathematical scope text, so normalPL/V cannot make it stale. Mathematical/interface scope remains exact; verification evidence stays dynamic in existing controls.',
    'v3c_unchanged':'All Lean/source/definitions/assumptions/formulas/seven-fold code/two anonymous decoders/source map unchanged. Preserve the accepted-v3b snapshot as historical evidence.',
    'source_review':'pending-reader-only-v3c','actual_compiled_commit':head,'root_fidelity_verdicts':0}
rpath=E/'full-consumer-reader-v3c.record.json'; create(rpath,dump(record))
cell=json.loads(C.read_bytes()); cell['evidence']['partial_public_producer_publication_binding_sha256']=audit['publication_binding_sha256']
cell['evidence']['full_consumer_reader_draft']=str(rpath); C.write_bytes(dump(cell))
publication.inputs.cache_clear(); publication.load.cache_clear(); publication.check_advance([audit['lean']['declaration']],reviewed=False)
paths=[LP,PP,AP,C,rpath,ppath,spath,tpath,*sorted(p for p in (E/'reader-v3b-accepted-snapshot.originals').iterdir())]
subprocess.run(['git','add','-f','--',*map(str,paths)],check=True)
assert set(git('diff','--cached','--name-only').decode().splitlines())==set(map(str,paths))
subprocess.run(['git','diff','--cached','--check','--',str(LP),str(PP),str(AP),str(C)],check=True)
subprocess.run(['git','commit','--quiet','-m','Keep actual variance reader scope stable across verification lifecycle'],check=True)
commit=git('rev-parse','HEAD').decode().strip()
out={k:record[k] for k in ['publication_binding_sha256','anti_anchored_packet','anti_raw_sha256','anti_canonical_packet_sha256','private_T_anti_packet','private_T_anti_raw_sha256','private_T_anti_canonical_sha256','full_source_map_sha256']}
out.update({'reader_metadata_commit':commit,'actual_compiled_commit':head,'changed_Lean_files':0,'root_VERIFIED_calls':0})
create(W/'actual-stable-reader-v3c-metadata-commit.json',dump(out))
print(json.dumps(out))
