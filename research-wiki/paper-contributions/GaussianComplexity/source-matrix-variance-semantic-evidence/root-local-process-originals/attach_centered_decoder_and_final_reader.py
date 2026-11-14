"""Bind complete original anonymous T reconstruction to the final reader draft."""
from pathlib import Path
import copy
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
N=Path('.astis/semantic-neutral-20261113/t_decode_vr_91ad')
sha=lambda raw:hashlib.sha256(raw.encode() if isinstance(raw,str) else raw).hexdigest()
dump=lambda obj:(json.dumps(obj,ensure_ascii=False,indent=2)+'\n').encode()
def create(p,raw):
    p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('xb') as f:f.write(raw)

# Only whitespace readability fixes before any new reader/anti exposure.
prior=json.loads((E/'full-consumer-reader-v3.record.json').read_bytes())
for i,p in enumerate([LP,AP,E/'anti-anchored-reviewer-packet.full-consumer-v3.json',E/'source-lean-map.full-consumer-v3.draft.json']):
    create(E/'reader-v3a-pre-inputs.originals'/(str(i)+'-'+p.name),p.read_bytes())
lesson=LP.read_text()
for old,new in [('gives0<=wi','gives 0<=wi'),('in[0,C]','in [0,C]'),('bounds2r(r+2)/d','bounds 2r(r+2)/d')]:
    assert lesson.count(old)==1,old
    lesson=lesson.replace(old,new)
LP.write_text(lesson)
audit=json.loads(AP.read_bytes()); oldPpacket=semantic.decoder_packet(audit)
item=json.loads(PP.read_bytes())['items'][0]; binding=item['bindings'][0]
publication.inputs.cache_clear(); publication.load.cache_clear()
audit['publication_binding_sha256']=publication.binding_digest(item,binding)
audit['publication_context']=publication.review_context(item,binding)
assert semantic.decoder_packet(audit)==oldPpacket
AP.write_bytes(dump(audit))
pPacket=semantic.semantic_reviewer_packet(audit)
pPath=E/'anti-anchored-reviewer-packet.full-consumer-v3a.json'
create(pPath,dump(pPacket))

# Preserve the old map, but include the full CFC theorem header at L1058.
mp=json.loads((E/'source-lean-map.full-consumer-v3.draft.json').read_bytes())
path=Path('.lake/packages/mathlib/Mathlib/Analysis/CStarAlgebra/ContinuousFunctionalCalculus/Unital.lean')
raw=path.read_bytes(); ls=raw.splitlines(keepends=True)
for entry in mp['mappings']:
    for src in entry['source']:
        if src['source_id']=='Mathlib.real_upper_spectrum_bound':
            start,end=1058,1061; pre=b''.join(ls[:start-1]); span=b''.join(ls[start-1:end])
            src.update({'lf_line_start':start,'lf_line_end':end,'raw_utf8_start':len(pre),'raw_utf8_end':len(pre)+len(span),'char_start':len(pre.decode()),'char_end':len(pre.decode())+len(span.decode()),'span_sha256':sha(span)})
mapPath=E/'source-lean-map.full-consumer-v3a.draft.json'
create(mapPath,dump(mp))

expected={'reconstruction.md':'c18fa40440f59293278af7a857aff8255cc23abd87a1a73a1a7d571b09ee54b0',
    'decoder-run.json':'12b1d9e3e5eac97c57ae70f0dee529d9b3eac68db7f90f1172b616f442ed463a',
    'freeze-manifest.json':'1deef0ffb0cdf4859001d74e6fc7eba9f7e397eaddb55d6ed5dd761e2ab26680'}
for n,h in expected.items():assert sha((N/'output'/n).read_bytes())==h,n
run=json.loads((N/'output/decoder-run.json').read_bytes())
text=(N/'output/reconstruction.md').read_bytes()
inp=(N/'input.json').read_bytes(); packet=json.loads(inp)
assert sha(inp)=='76d9e55ce528f4452e2512093467e4caa0cfa9af462ec200a598d53429290261'
assert run['mathematical_evidentiary_input_count']==1 and run['source_text_visible'] is False
assert run['sole_input_raw_sha256']==sha(inp) and run['sole_input_canonical_packet_sha256']==packet['packet_sha256']
contract=run['output_contract']
assert contract['decoder']=='/root/neutral_decode_t_91ad'
assert contract['reconstructed_theorem_text']==text.decode() and contract['reconstructed_text_sha256']==sha(text)
assert contract['decoder_run_sha256']=='' and run['reconstruction']['abridged'] is False
assert all(isinstance(contract[k],str) and contract[k].strip() for k in ['objects','domains','quantifiers','assumptions','conclusion','scopes','constant_dependencies'])
assert run['inputs_and_exposure']['source_identity_visible'] is False and run['inputs_and_exposure']['AGENTS_read'] is False
assert run['inputs_and_exposure']['proof_visible'] is False and run['inputs_and_exposure']['other_files_read'] is False
for x in json.loads((N/'output/freeze-manifest.json').read_bytes())['files']:
    q=Path(x['path']); assert q.stat().st_size==x['bytes'] and sha(q.read_bytes())==x['sha256']
dest=E/'decoder-originals/neutral_decode_t_91ad'
create(dest/'input.json',inp)
for n in expected:create(dest/n,(N/'output'/n).read_bytes())
supp=json.loads((W/'private-centered-consumer-supplement.audit-draft.json').read_bytes())
supp['state']='blind-reconstructed'
supp['reconstruction']={'text':text.decode(),'text_sha256':sha(text),'decoder':contract['decoder'],
    'decoder_run_sha256':expected['decoder-run.json'],'decoder_packet_sha256':packet['packet_sha256'],
    'source_text_visible':False,'lean_statement_sha256':run['sole_input_statement_sha256'],
    'input_artifacts':['lean-statement','approved-definition-context'],'run_artifact':str(dest/'decoder-run.json')}
supp['publication_binding_sha256']=audit['publication_binding_sha256']
supp['publication_context']=audit['publication_context']
supp['parent_public_binding_note']='This hash binds the unchanged public P plus its authored private-consumer code/explanation. T has no separate public declaration binding/status.'
assert semantic.decoder_packet(supp)==packet
suppPath=E/'private-centered-consumer-supplement.full-v3a.json'
create(suppPath,dump(supp))
tPacket=semantic.semantic_reviewer_packet(supp)
tPath=E/'anti-anchored-private-centered-consumer.full-v3a.json'
create(tPath,dump(tPacket))
record={**prior,'publication_binding_sha256':audit['publication_binding_sha256'],
    'anti_anchored_packet':str(pPath),'anti_raw_sha256':sha(pPath.read_bytes()),
    'anti_canonical_packet_sha256':pPacket['packet_sha256'],
    'full_source_map':str(mapPath),'full_source_map_sha256':sha(mapPath.read_bytes()),
    'private_T_supplement':str(suppPath),'private_T_anti_packet':str(tPath),
    'private_T_anti_raw_sha256':sha(tPath.read_bytes()),'private_T_anti_canonical_sha256':tPacket['packet_sha256'],
    'private_T_original_decoder_run_sha256':expected['decoder-run.json'],
    'private_T_original_reconstruction_sha256':sha(text),'supplement_has_public_binding_credit':False,
    'v3a_changes':'Three plain prose spacing corrections and exact upper-spectrum provider header L1058–1061 included. All preceding draft inputs preserved; no mathematical statement/code/definition/decoder changed.',
    'root_fidelity_verdicts':0,'normal_R9_PROVED_LOCAL_or_VERIFIED_calls':0}
create(E/'full-consumer-reader-v3a.record.json',dump(record))
cell=json.loads(C.read_bytes())
cell['evidence']['partial_public_producer_publication_binding_sha256']=audit['publication_binding_sha256']
cell['evidence']['full_consumer_reader_draft']=str(E/'full-consumer-reader-v3a.record.json')
C.write_bytes(dump(cell))
publication.inputs.cache_clear(); publication.load.cache_clear()
publication.check_advance([audit['lean']['declaration']],reviewed=False)
print(json.dumps({k:record[k] for k in ['publication_binding_sha256','anti_anchored_packet','anti_raw_sha256','anti_canonical_packet_sha256','private_T_anti_packet','private_T_anti_raw_sha256','private_T_anti_canonical_sha256','full_source_map_sha256','root_fidelity_verdicts']}))
