from pathlib import Path
import hashlib,json,sys
R=Path('E:/Samplinglib');r=Path(__file__).resolve().parent;d=r/'independent-source92/visibility-transfer92'
sys.path.insert(0,str(R/'tools'))
import astis_semantic_roundtrip as rt,astis_publication as pub,astis_advance as adv
sha=lambda b:hashlib.sha256(b).hexdigest()
load=lambda p:json.loads(p.read_bytes())
def save(p,x):p.write_bytes((json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode())
def fresh(p,x):assert not p.exists(),p;save(p,x)
def pin(p):return dict(path=p.relative_to(R).as_posix(),raw_sha256=sha(p.read_bytes()),bytes=p.stat().st_size)
expected={'source-review92.v3.native.json':'5d0cc8a922ecd1a9a2c9dc3f299e087b5152a7ca92fe0b629b82f09c87e60b94',
 'review-run92.v3.native.json':'75c19b604a7105c0d7f6f01103154a283445eb698838e897408ff248d5e37772',
 'closed-RAW92.v3.native.json':'abc0f06a8c62ff637f6f997bdc6b0aa51e1975cd818b2ecdb3f2c9481e720bb2'}
for name,h in expected.items():assert sha((d/name).read_bytes())==h,name
m=load(d/'closed-RAW92.v3.native.json');n=load(d/'source-review92.v3.native.json')
for x in m['inputs']+m['outputs']:
    p=Path(x['path']);p=p if p.is_absolute() else R/p
    b=p.read_bytes();assert sha(b)==x['raw_sha256'],x['path']
    if 'bytes' in x:assert len(b)==x['bytes'],x['path']
assert n['reviewer']=='/root/primary_source91' and n['independent_from_formalizer'] and n['independent_from_decoder']
assert n['decision']=='ACCEPT_BOUNDED_ACTUAL_STRICT_PREFIX_SOURCE_AND_EXPOSITION'
assert n['verdict']=='equivalent-after-elaboration' and not n['repairs']
assert len(n['definition_audit'])==25 and len(n['six_binder_audit'])==6
assert n['statement_seal_audit']['full_Prop_exact_match'] and n['statement_seal_audit']['no_added_public_provider']
ex=load(R/n['exposition_audit']['path']);assert len(ex['steps'])==10
raw=(R/n['module']['path']).read_bytes()
for x in ex['steps']:
    reg=x['body_region'];code=b''.join(raw.splitlines(keepends=True)[reg['start_line']-1:reg['end_line']])
    assert sha(code)==reg['exact_code_raw_sha256']
assert set(n['semantic_slots'])==set(rt.SEMANTIC_SLOTS)
for v in n['semantic_slots'].values():
    assert all(isinstance(v[k],str) and v[k].strip() for k in ['original','reconstructed','relation','evidence'])
    assert v['relation'] in rt.SLOT_RELATIONS
ap=R/'research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261011-PBPSActualOrderedPrefix.json'
a=load(ap);assert a['state']=='blind-reconstructed'
packet=rt.semantic_reviewer_packet(a);assert packet==load(r/'anti-anchored.review92.v3.json')
assert packet['packet_sha256']==n['reviewer_packet_sha256']
assert a['publication_binding_sha256']==n['publication_binding_sha256']
assert n['review_run_sha256']==expected['review-run92.v3.native.json']
assert load(r/'root.math92.visibility-adoption.json')['status']=='ACCEPTED_INDEPENDENT_MATH_ONLY'
fresh(r/'audit.before-source92.v3.json',a)
evidence='; '.join(n['review_evidence'])
deltas=[dict(slot=x['slot'],severity='informational',description=x['source']+' Lean: '+x['lean']+' '+x['assessment'],
    evidence=evidence,native_classification=x['classification']) for x in n['deltas']]
a.update(state='accepted',semantic_slots=n['semantic_slots'],deltas=deltas,verdict=n['verdict'],
    source_review=dict(state='accepted',reviewer=n['reviewer'],independent_from_formalizer=True,independent_from_decoder=True,
        evidence=evidence,review_run_sha256=n['review_run_sha256'],reviewer_packet_sha256=n['reviewer_packet_sha256'],
        run_artifact=(d/'review-run92.v3.native.json').relative_to(R).as_posix(),native_manifest=pin(d/'closed-RAW92.v3.native.json')))
save(ap,a);pub.inputs.cache_clear();pub.load.cache_clear();pub.check_advance([a['lean']['declaration']],reviewed=True)
fresh(r/'root.source92.visibility-adoption.json',dict(status='ACCEPTED_INDEPENDENT_SOURCE_FIDELITY_ONLY',native_hashes=expected,
    reviewer=n['reviewer'],acceptance_scope=n['limitations'],source_graph_mapping=n['source_proof_coverage'],
    canonical_packet_sha256=packet['packet_sha256'],publication_binding_sha256=a['publication_binding_sha256'],VERIFIED=False))
claim=load(r/'claim.json');cp=R/'research-wiki/frontier-cells'/f"{claim['frontier_cell']}.json";c=load(cp)
c['conceptual_mirror_audit']=load(r/'conceptual-mirror-audit92.json')
leaf=r/'independent-visibility92/leaf-build.receipt.native.json'
c['evidence'].update(proof_review=(r/'independent-visibility92/visibility-review92.native.json').relative_to(R).as_posix(),
    source_review=(d/'source-review92.v3.native.json').relative_to(R).as_posix(),
    focused_checks=[dict(command=claim['focused_checks'][0],result='PASS; independent whole mathematical/kernel/leaf and source review accepted.',evidence=leaf.relative_to(R).as_posix())])
c['source_proof_coverage'].update(compiled_source_review=(d/'source-review92.v3.native.json').relative_to(R).as_posix(),
    coverage_status='Independent whole proof/kernel, source-blind reconstruction and primary-first source review accepted:25 literal definitions,6 original analytic binders,10 exact BODY/exposition regions,29 source nodes/57 edges/46 coverage rows. Strict first-n complete-history law only. Final survival/count/path/full A7/global/main/composition remain OPEN.')
c['blocked']['reason']='Independent mathematical/decoder/source acceptance complete; exact science-commit verification and sole-lane aggregation pending.'
e=dict(result_kind='theorem-edge',theorem_delta=claim['theorem_delta'],lean_declarations=claim['target_declarations'],publication_declarations=claim['target_declarations'],
    lean_files=claim['proposed_files'],focused_checks=[pin(leaf)],truth_boundary=claim['truth_boundary'],
    conceptual_mirror_audit=c['conceptual_mirror_audit'],statement_seal=c['statement_seal'],source_proof_coverage=c['source_proof_coverage'],
    proof_digestion=c['proof_digestion'],purification=c['purification'],independent_math=pin(r/'root.math92.visibility-adoption.json'),
    blind_decoder=pin(r/'root.decoder92.adoption.json'),source_review=pin(r/'root.source92.visibility-adoption.json'),actual_dependencies=c['parents'],
    integration_notes='Actual all finite n strict ordered-prefix full-history law with product density, Borel construction, pointwise reconstruction, all ENNReal tests and mass. Public seal unchanged; independently checked private alpha-renaming for inventory. Final survival/count/path/A7, restart/Markov/invariance/hypocoercivity/errors/cost/main/composition remain OPEN. Exact-commit verification and unique-lane aggregate/publication/visual gates pending; no self-VERIFIED.')
adv.transition_advance(claim['advance_id'],'PROVED_LOCAL',worker_id=claim['created_by'],evidence=e)
c['status']='proved_locally';save(cp,c);fresh(r/'proved-local92.v3.json',e)
print('PROVED_LOCAL92: independent mathematics/decoder/source accepted; exact commit and stabilization pending.')
