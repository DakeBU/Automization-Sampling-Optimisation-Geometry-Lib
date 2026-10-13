from pathlib import Path
import hashlib,json,os,sys
root=Path.cwd();sys.path.insert(0,str(root/'tools'))
import astis_publication as pub,astis_semantic_roundtrip as rt
r=Path('runs/20261007-companion-priority/pbps-ambient-adjoint66');d=r/'presentation-overlay66'
load=lambda p:json.loads(p.read_bytes())
sha=lambda b:hashlib.sha256(b).hexdigest()
def pin(p):
    b=p.read_bytes();return dict(path=p.as_posix(),bytes=len(b),raw_sha256=sha(b))
def write(p,x):
    assert not p.exists(),p
    p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
proposal=load(d/'proposal.json');vp=r/'independent-source66/metadata-overlay.verdict.json';verdict=load(vp)
assert sha((d/'proposal.json').read_bytes())=='0a7b70c41f8bb726aeafde2a6e2d3341e35e1f253ddd00a55d27260c03d19e99'
assert sha(vp.read_bytes())=='c28617df958e8a53e9d711778127368e9b4b3770e350f33ff7c228921b45ea15'
assert verdict['status']=='ACCEPTED_EXACT_METADATA_ONLY' and verdict['independent_from_overlay_author']
assert not verdict['source_mathematical_repair'] and not verdict['new_proof_or_Lean_change'] and not verdict['new_source_hypothesis']
assert verdict['formula_changes']==0 and len(proposal['changes'])==4
for x in proposal['entries']:
    assert pin(Path(x['canonical']))['raw_sha256']==x['before']['raw_sha256']
    assert pin(Path(x['proposed']['path']))['raw_sha256']==x['proposed']['raw_sha256']
    assert Path(x['before_snapshot']['path']).read_bytes()==Path(x['canonical']).read_bytes()
for x in proposal['compiled_proof_inputs']:
    assert pin(Path(x['path']))==x
assert not (d/'applied.json').exists()
(d/'independent.verdict.exactraw.json').write_bytes(vp.read_bytes())
ap=Path('research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261009-PBPSAmbientAdjointCorrector.json')
audit=load(ap);assert audit['state']=='blind-reconstructed'
(d/'audit.before-overlay.exactraw.snapshot.json').write_bytes(ap.read_bytes())
for x in proposal['entries']:
    Path(x['canonical']).write_bytes(Path(x['proposed']['path']).read_bytes())
pub.inputs.cache_clear();pub.load.cache_clear();data=pub.inputs()
item=next(x for x in pub.load() if x['id']=='pbps-ambient-adjoint-corrector')
before_binding=audit['publication_binding_sha256']
audit['publication_binding_sha256']=pub.binding_digest(item,item['bindings'][0],data)
audit['publication_context']=pub.review_context(item,item['bindings'][0],data)
assert audit['publication_binding_sha256']!=before_binding
assert rt.decoder_packet(audit)==load(Path('.astis/decoder-66/packet0.json'))
ap.write_text(json.dumps(audit,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
write(r/'source.1.reviewer-packet.json',rt.semantic_reviewer_packet(audit))
write(d/'applied.json',dict(status='EXACT_INDEPENDENTLY_REVIEWED_FOUR_CATALOGUE_FIELDS_APPLIED',actual_root_pid=os.getpid(),proposal=pin(d/'proposal.json'),separate_independent_overlay_verdict=pin(d/'independent.verdict.exactraw.json'),changes=proposal['changes'],canonical_after=[pin(Path(x['canonical'])) for x in proposal['entries']],compiled_proof_inputs_unchanged=proposal['compiled_proof_inputs'],formula_changes=0,source_mathematical_repair=False,prior_binding=before_binding,current_binding=audit['publication_binding_sha256'],current_context_sha256=pub.digest(audit['publication_context']),blind_packet_unchanged=True,final_source_verdict_pending=True,original_frozen_bundle_preserved=True))
write(r/'math-freeze1.metadata-overlay.json',dict(status='ORIGINAL_COMPILED_MATHEMATICS_UNCHANGED_SEPARATELY_REVIEWED_CATALOGUE_OVERLAY',original_frozen_bundle=pin(r/'math-freeze.json'),explicit_old_to_approved_current_maps=proposal['entries'],overlay_adoption=pin(d/'applied.json'),current_inputs=[pin(Path(x['canonical'])) for x in proposal['entries']]+[pin(ap),pin(r/'source.1.reviewer-packet.json')],compiled_inputs_unchanged=proposal['compiled_proof_inputs'],source_mathematical_repair=False,formula_changes=0,final_source_verdict_pending=True))
print('PASS exact four catalogue fields applied after independent review; proof/statement/formulas/blind packet unchanged; fresh source.1 binding ready.')
