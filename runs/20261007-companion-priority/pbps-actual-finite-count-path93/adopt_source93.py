"""Adopt immutable independent reviews; the owner stops at PROVED_LOCAL."""
from pathlib import Path
import hashlib,json,sys
R=Path(__file__).resolve().parents[3]; r=Path(__file__).resolve().parent
sys.path.insert(0,str(R/'tools'))
import astis_semantic_roundtrip as rt, astis_publication as pub, astis_advance as adv
load=lambda p:json.loads(p.read_bytes())
sha=lambda b:hashlib.sha256(b).hexdigest()
def save(p,x):p.write_bytes((json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode())
def fresh(p,x):assert not p.exists(),p;save(p,x)
def pin(p):return dict(path=p.relative_to(R).as_posix(),raw_sha256=sha(p.read_bytes()),bytes=p.stat().st_size)
def verify(rows):
    for x in rows:
        p=Path(x['path']);p=p if p.is_absolute() else R/p
        b=p.read_bytes();assert sha(b)==x['raw_sha256'],x['path']
        if 'bytes' in x:assert len(b)==x['bytes'],x['path']
d=r/'primary-source93'; n=load(d/'source-review-decision93.native.json')
assert sha((d/'source-review-decision93.native.json').read_bytes())=='dd06d39bfb10e9161b36dfba75dcfa212a7a8c0f484291ebea8e823cc904d3c8'
mp=d/'closed-RAW-review93.native.json'
assert sha(mp.read_bytes())=='9343776de5efd5c418ab5f13ffc447d4d2899fa468bac48eddb6d84d59a82523'
m=load(mp);verify(m['inputs']+m['outputs'])
rr=load(d/'review-run93.native.json')
assert rt.sha256_json({k:v for k,v in rr.items() if k!='review_run_sha256'})==rr['review_run_sha256']==n['review_run_sha256']
assert rt.sha256_json({k:v for k,v in n.items() if k not in ['review_run_sha256','review_run_artifact']})==rr['decision_payload_sha256']
assert n['reviewer']=='/root/primary_source93' and n['independent_from_formalizer'] and n['independent_from_decoder']
assert n['source_review_status']=='accepted' and n['verdict']=='equivalent-after-elaboration'
assert not n['repairs'] and not n['blocking_findings'] and len(n['binder_audit'])==6
assert set(n['semantic_slots'])==set(rt.SEMANTIC_SLOTS)
for v in n['semantic_slots'].values():
    assert all(isinstance(v[k],str) and v[k].strip() for k in ['original','reconstructed','relation','evidence'])
    assert v['relation'] in rt.SLOT_RELATIONS
ex=load(R/n['coverage_artifact'])
assert (ex['node_count'],ex['edge_count'],ex['disposition_count'])==(35,94,55)
t=r/'independent-whole-math93/metadata-transfer93'
tm=t/'closed-RAW-metadata-transfer93.native.json'
assert sha(tm.read_bytes())=='587cf87b3d68b19b993325bb3873adba3b1013f2612c85696e6abfd0d5cfb5a9'
verify(load(tm)['artifacts']);tr=load(t/'metadata-transfer-decision93.native.json')
assert tr['decision']=='ACCEPT_EXACT_METADATA_ONLY_EXPOSITION_TRANSFER'
verify([tr[k] for k in ['new_publication','production','lesson']])
fresh(r/'root.math93.metadata-adoption.json',dict(status='ACCEPTED_INDEPENDENT_MATH_EXPOSITION_TRANSFER_ONLY',decision=pin(t/'metadata-transfer-decision93.native.json'),manifest=pin(tm),original_adoption=pin(r/'root.math93.adoption.json'),VERIFIED=False))
ap=R/'research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261011-PBPSActualFiniteCountPath.json';a=load(ap)
assert a['state']=='blind-reconstructed'
packet=rt.semantic_reviewer_packet(a)
assert packet==load(r/'anti-anchored.review93.v2.json') and packet['packet_sha256']==n['reviewer_packet_sha256']
assert a['publication_binding_sha256']==n['publication_binding_sha256']
fresh(r/'audit.before-source93.json',a)
a.update(state='accepted',semantic_slots=n['semantic_slots'],deltas=n['deltas'],verdict=n['verdict'],source_review=dict(state='accepted',reviewer=n['reviewer'],independent_from_formalizer=True,independent_from_decoder=True,evidence=n['review_evidence'],review_run_sha256=n['review_run_sha256'],reviewer_packet_sha256=n['reviewer_packet_sha256'],run_artifact=n['review_run_artifact'],native_manifest=pin(mp)))
save(ap,a);pub.inputs.cache_clear();pub.load.cache_clear();pub.check_advance([a['lean']['declaration']],reviewed=True)
fresh(r/'root.source93.adoption.json',dict(status='ACCEPTED_INDEPENDENT_SOURCE_FIDELITY_ONLY',decision=pin(d/'source-review-decision93.native.json'),manifest=pin(mp),reviewer=n['reviewer'],acceptance_scope=ex['scope'],nonclaims=n['nonclaims'],canonical_packet_sha256=packet['packet_sha256'],publication_binding_sha256=a['publication_binding_sha256'],VERIFIED=False))
old=load(r.parent/'pbps-actual-ordered-prefix92/conceptual-mirror-audit92.json');verify(old['checked'])
mirror=dict(status='none-found',discovery_ids=[],checked=old['checked'],unchanged_family_inventory_reused=True,reason='Terminal survival weights the existing finite-history law, then measurable interpolation and fixed-horizon endpoint nullity identify actual count sectors. This composes existing measure/probability mechanisms within one source route; no new cross-domain correspondence or certified transport is proposed.')
fresh(r/'conceptual-mirror-audit93.json',mirror)
claim=load(r/'claim.json');cp=R/'research-wiki/frontier-cells'/f"{claim['frontier_cell']}.json";c=load(cp)
c['conceptual_mirror_audit']=mirror
leaf=r/'checks93/leaf-build/receipt.json'
c['evidence'].update(proof_review=(r/'independent-whole-math93/whole-math-decision93.native.json').relative_to(R).as_posix(),source_review=(d/'source-review-decision93.native.json').relative_to(R).as_posix(),focused_checks=[dict(command=claim['focused_checks'][0],result='PASS; independent whole mathematics/kernel, blind reconstruction and source/exposition acceptance.',evidence=leaf.relative_to(R).as_posix())])
c['source_proof_coverage'].update(compiled_source_review=(d/'source-review-decision93.native.json').relative_to(R).as_posix(),coverage_status='Independent mathematics/kernel, blind reconstruction and primary-first source review accepted: six analytic binders, 36 literal lets, nine exact BODY/exposition regions and exhaustive 35-node/94-edge/55-disposition coverage. Only bounded finite-count complete history/coordinate-path law; full A7 and downstream results remain OPEN.')
c['blocked']['reason']='Independent review accepted; exact science-commit verification and sole-lane aggregation pending.'
c['purification']['dead_code_audit']='Whole production and all 25 private proof helpers independently reviewed; postmerge purification remains pending.'
c['learning_contract']['reader_backpressure'].update(exposition_evidence=n['coverage_artifact'],assumptions_preserved=True,boundary_preserved=True)
e=dict(result_kind='theorem-edge',theorem_delta=claim['theorem_delta'],lean_declarations=claim['target_declarations'],publication_declarations=claim['target_declarations'],lean_files=claim['proposed_files'],focused_checks=[pin(leaf)],truth_boundary=claim['truth_boundary'],conceptual_mirror_audit=mirror,statement_seal=c['statement_seal'],source_proof_coverage=c['source_proof_coverage'],proof_digestion=c['proof_digestion'],purification=c['purification'],independent_math=pin(r/'root.math93.metadata-adoption.json'),blind_decoder=pin(r/'root.decoder93.adoption.json'),source_review=pin(r/'root.source93.adoption.json'),actual_dependencies=c['parents'],integration_notes='Six-assumption finite-count complete-history/coordinate-path law, endpoint/count identification and measurability. Exact commit verification, unique stabilization, actual reader visual acceptance and postmerge purification pending. No self-VERIFIED; full papers and Goal open.')
adv.transition_advance(claim['advance_id'],'PROVED_LOCAL',worker_id=claim['created_by'],evidence=e)
c['status']='proved_locally';save(cp,c);fresh(r/'proved-local93.json',e)
print('PROVED_LOCAL93: independent math/decoder/source adopted; exact commit verification pending.')
