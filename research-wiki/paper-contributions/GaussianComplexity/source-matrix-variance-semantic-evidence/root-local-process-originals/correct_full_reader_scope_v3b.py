"""Correct two independently identified stale reader scopes and one map endpoint."""
from pathlib import Path
import hashlib
import json
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
T=Path('Tests/GaussianComplexityFixedSpectrumSourceMatrixVariance.lean')
sha=lambda raw:hashlib.sha256(raw.encode() if isinstance(raw,str) else raw).hexdigest()
dump=lambda obj:(json.dumps(obj,ensure_ascii=False,indent=2)+'\n').encode()
def create(p,raw):
    p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('xb') as f:f.write(raw)
old_record=json.loads((E/'full-consumer-reader-v3a.record.json').read_bytes())
originals={}
for i,p in enumerate([LP,PP,AP,E/'anti-anchored-reviewer-packet.full-consumer-v3a.json',E/'anti-anchored-private-centered-consumer.full-v3a.json',E/'private-centered-consumer-supplement.full-v3a.json',E/'source-lean-map.full-consumer-v3a.draft.json']):
    raw=p.read_bytes(); dest=E/'reader-v3a-blocked-inputs.originals'/(str(i)+'-'+p.name)
    create(dest,raw); originals[str(p)]={'path':str(dest),'sha256':sha(raw)}
lesson=json.loads(LP.read_bytes()); pub=json.loads(PP.read_bytes())
assert 'still unimplemented' in lesson['units'][0]['sources'][1]['scope']
assert 'still unimplemented' in pub['items'][0]['bindings'][0]['boundary']
scope=('The public declaration is the actual uncentered squared-moment producer. '
    'The separate private Tests consumer now implements centered and cosine-weighted square integrability and both true operator-norm comparisons in the same original experiment. '
    'Its extended independent source/native/reader acceptance is pending, and the full R9 SAU remains EXPLORING. '
    'Public API placement, matrix concentration, main lower bounds, exact oracle/precision/TV/query-cap/cost adapters, serialized integration/publication and purification remain open.')
lesson['units'][0]['sources'][1]['scope']=scope
pub['items'][0]['bindings'][0]['boundary']=scope
LP.write_bytes(dump(lesson)); PP.write_bytes(dump(pub))
assert 'still unimplemented' not in LP.read_text() and 'still unimplemented' not in PP.read_text()
audit=json.loads(AP.read_bytes()); old_decoder=semantic.decoder_packet(audit)
publication.inputs.cache_clear(); publication.load.cache_clear()
item=pub['items'][0]; binding=item['bindings'][0]
audit['publication_binding_sha256']=publication.binding_digest(item,binding)
audit['publication_context']=publication.review_context(item,binding)
assert semantic.decoder_packet(audit)==old_decoder and audit['state']=='blind-reconstructed'
AP.write_bytes(dump(audit))
pPacket=semantic.semantic_reviewer_packet(audit)
pPath=E/'anti-anchored-reviewer-packet.full-consumer-v3b.json'
create(pPath,dump(pPacket))
supp=json.loads((E/'private-centered-consumer-supplement.full-v3a.json').read_bytes())
old_t_decoder=semantic.decoder_packet(supp)
supp['publication_binding_sha256']=audit['publication_binding_sha256']
supp['publication_context']=audit['publication_context']
assert semantic.decoder_packet(supp)==old_t_decoder
suppPath=E/'private-centered-consumer-supplement.full-v3b.json'
create(suppPath,dump(supp))
tPacket=semantic.semantic_reviewer_packet(supp)
tPath=E/'anti-anchored-private-centered-consumer.full-v3b.json'
create(tPath,dump(tPacket))
mp=json.loads((E/'source-lean-map.full-consumer-v3a.draft.json').read_bytes())
raw=T.read_bytes(); lines=raw.splitlines(keepends=True)
changed=0
for mapping in mp['mappings']:
    for span in mapping['lean']:
        if span['path']==str(T) and span['LF_lines_1based']==[150,177]:
            pre=b''.join(lines[:149]); chunk=b''.join(lines[149:178])
            span.update({'LF_lines_1based':[150,178],'raw_UTF8_byte_span':[len(pre),len(pre)+len(chunk)],
                'decoded_char_span':[len(pre.decode()),len(pre.decode())+len(chunk.decode())],'span_sha256':sha(chunk)})
            changed+=1
assert changed==1
mp['map_coverage_note']='Weighted interval includes its final algebraic cancellation L178; full T module also remains reproduced exactly in the last3 reader folds. Empty L149 needs no separate mathematical node.'
mapPath=E/'source-lean-map.full-consumer-v3b.draft.json'
create(mapPath,dump(mp))
record={**old_record,'publication_binding_sha256':audit['publication_binding_sha256'],
    'anti_anchored_packet':str(pPath),'anti_raw_sha256':sha(pPath.read_bytes()),'anti_canonical_packet_sha256':pPacket['packet_sha256'],
    'private_T_supplement':str(suppPath),'private_T_anti_packet':str(tPath),
    'private_T_anti_raw_sha256':sha(tPath.read_bytes()),'private_T_anti_canonical_sha256':tPacket['packet_sha256'],
    'full_source_map':str(mapPath),'full_source_map_sha256':sha(mapPath.read_bytes()),
    'independent_blocker_actor':'/root/mv_fresh_source_6e28',
    'independent_v3a_blocker_sha256':'e097cb29403f78a30a1dd91e9219e4f93cc02c1a3f32b5efc17798b85dcc47b5',
    'independent_v3a_finding_freeze_sha256':'cc64e91c61a54eeb88ec375f5826d18d68eae389b3e41cfd6d28d71d66a17e57',
    'v3a_blocked_originals':originals,
    'v3b_correction':'Only two current author scope strings corrected from unimplemented to actual private implementation/pending independent acceptance, and weighted map extends177 to178. Public P conclusion, private T statement/code, source law/definitions/constant, both anonymous decoders and prior findings unchanged.',
    'source_review':'pending-v3b','root_fidelity_verdicts':0}
create(E/'full-consumer-reader-v3b.record.json',dump(record))
cell=json.loads(C.read_bytes())
cell['evidence']['partial_public_producer_publication_binding_sha256']=audit['publication_binding_sha256']
cell['evidence']['full_consumer_reader_draft']=str(E/'full-consumer-reader-v3b.record.json')
C.write_bytes(dump(cell))
publication.inputs.cache_clear(); publication.load.cache_clear()
publication.check_advance([audit['lean']['declaration']],reviewed=False)
print(json.dumps({k:record[k] for k in ['publication_binding_sha256','anti_anchored_packet','anti_raw_sha256','anti_canonical_packet_sha256','private_T_anti_packet','private_T_anti_raw_sha256','private_T_anti_canonical_sha256','full_source_map_sha256','root_fidelity_verdicts']}))
