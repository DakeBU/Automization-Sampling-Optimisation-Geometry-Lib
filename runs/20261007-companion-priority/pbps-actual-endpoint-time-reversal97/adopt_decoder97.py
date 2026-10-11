from pathlib import Path
import json,hashlib,sys
r=Path(__file__).parent;sys.path.insert(0,str(Path.cwd()/'tools'))
import astis_semantic_roundtrip as rt
import astis_publication as pub
load=lambda p:json.loads(Path(p).read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest()
def save(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
ap=Path('research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261012-PBPSActualEndpointTimeReversal.json')
a=load(ap);assert 'reconstruction' not in a
(r/'audit-before-decoder97.json').write_bytes(ap.read_bytes())
lp=Path('website/content/declaration_lessons/pbps-actual-endpoint-time-reversal.json');lesson=load(lp)
(r/'lesson-before-exact-api-names97.json').write_bytes(lp.read_bytes())
deps=lesson['units'][0]['mathlib_dependencies'];assert 'MeasurePreserving.pi' in deps
deps.remove('MeasurePreserving.pi');deps += ['volume_preserving_pi','volume_measurePreserving_piCongrLeft','Measure.measurePreserving_sub_left']
save(lp,lesson)
pp=Path('website/content/publications/pbps-actual-endpoint-time-reversal.json');item=load(pp)['items'][0]
pub.inputs.cache_clear();pub.load.cache_clear();a['publication_binding_sha256']=pub.binding_digest(item,item['bindings'][0],pub.inputs());a['publication_context']=pub.review_context(item,item['bindings'][0],pub.inputs())
dpath=Path('runs/semantic-roundtrip/anonymous97/decoder/decision.json');d=load(dpath)
run=Path('runs/semantic-roundtrip/anonymous97/decoder/decoder-run.json');manifest=Path('runs/semantic-roundtrip/anonymous97/decoder/manifest.json')
packet=rt.decoder_packet(a);assert packet==load('runs/semantic-roundtrip/anonymous97/input.json')
assert sha(run.read_bytes())==d['decoder_run_sha256'];assert packet['packet_sha256']==d['packet_sha256']
text=d['reconstructed_theorem_text'];assert sha(text.encode())==d['reconstructed_text_sha256']
a['reconstruction']=dict(text=text,text_sha256=d['reconstructed_text_sha256'],decoder=d['decoder']['agent'],decoder_run_sha256=d['decoder_run_sha256'],decoder_packet_sha256=d['packet_sha256'],source_text_visible=False,lean_statement_sha256=a['lean']['statement_sha256'],input_artifacts=['lean-statement','approved-definition-context'],observed_input_artifacts=[dict(path='runs/semantic-roundtrip/anonymous97/input.json',raw_sha256=d['input_sha256'])],run_artifact=run.as_posix(),native_structured_payload=dpath.as_posix(),native_named_payload_sha256=sha(dpath.read_bytes()),native_run_manifest_RAW_sha256=sha(manifest.read_bytes()),native_semantic_slots={k:d[k] for k in ['objects','domains','quantifiers','assumptions','conclusion','scopes','constant_dependencies']})
a['lean']['statement_representation']['kernel_header_and_literal_expansion_checked']=True
a['lean']['statement_representation']['independent_kernel_evidence']=(r/'independent-whole-math97/whole-math-decision97.native.json').as_posix()
save(ap,a)
review=rt.semantic_reviewer_packet(a);rp=r/'reviewer-packet97.json';assert not rp.exists();save(rp,review)
save(r/'decoder-admission97.json',dict(decoder_native=dpath.as_posix(),decoder_run_raw_sha256=sha(run.read_bytes()),packet_sha256=d['packet_sha256'],reviewer_packet_sha256=review['packet_sha256'],publication_binding_sha256=a['publication_binding_sha256'],metadata_correction='Mathlib dependency labels name actual volume_preserving_pi / volume_measurePreserving_piCongrLeft / Measure.measurePreserving_sub_left; proof and six steps unchanged.',source_verdict='pending'))
print(rp.as_posix(),review['packet_sha256'],a['publication_binding_sha256'])
