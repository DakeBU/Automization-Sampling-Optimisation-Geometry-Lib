from pathlib import Path
import hashlib,json,sys
R=Path('E:/Samplinglib');r=Path(__file__).parent;d=r/'independent-source91'
sys.path.insert(0,str(R/'tools'))
import astis_semantic_roundtrip as rt,astis_publication as pub,astis_advance as adv
sha=lambda b:hashlib.sha256(b).hexdigest()
load=lambda p:json.loads(p.read_bytes())
def save(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
def fresh(p,x):assert not p.exists(),p;save(p,x)
def pin(p):return dict(path=p.relative_to(R).as_posix(),raw_sha256=sha(p.read_bytes()),bytes=p.stat().st_size)
expected={'source-review91.native.json':'f4c5518262e3373ce206532c8fd16d2bed0ddf80c16c76351c90508c370bac87',
          'review-run91.native.json':'4015dc4b614116c0acf7edbdd0285ef7e3eca784850b51a52ed6ba4b95d3c47f',
          'closed-RAW91.native.json':'7b9aa6a8350e93c0fd986674c36c2517c1fd667af6b807401395ea4a1c3afe1d'}
for name,h in expected.items():assert sha((d/name).read_bytes())==h,name
m=load(d/'closed-RAW91.native.json');n=load(d/'source-review91.native.json')
assert m['closed']
for x in m['inputs']+m['outputs']:
    b=Path(x['path']).read_bytes();assert sha(b)==x['raw_sha256'],x['path']
    if 'bytes' in x:assert len(b)==x['bytes'],x['path']
assert n['reviewer']=='/root/primary_source91' and n['accepted'] and n['independent_from_formalizer'] and n['independent_from_decoder']
assert n['verdict']=='equivalent-after-elaboration' and not n['repairs'] and all(not x['blocking'] for x in n['deltas'])
assert len(n['literal_definition_audit'])==35 and len(n['binder_audit'])==6 and not n['additional_binders']['EXCESS']
assert len(n['body_exposition_audit'])==7
raw=Path(n['production_module']['path']).read_bytes()
for x in n['body_exposition_audit']:
    assert x['exact_BODY_matches_lesson'] and x['source_and_exposition_verdict']=='accepted-for-bounded-coordinate'
    assert sha(b''.join(raw.splitlines(keepends=True)[x['start_line']-1:x['end_line']]))==x['exact_BODY_raw_sha256']
assert set(n['semantic_slots'])==set(rt.SEMANTIC_SLOTS)
for v in n['semantic_slots'].values():
    assert all(isinstance(v[k],str) and v[k].strip() for k in ['original','reconstructed','relation','evidence'])
    assert v['relation'] in rt.SLOT_RELATIONS
ap=R/'research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261011-PBPSActualAbsoluteNextEventTime.json'
a=load(ap);assert a['state']=='blind-reconstructed'
packet=rt.semantic_reviewer_packet(a);assert packet==load(r/'anti-anchored.review91.json')
assert packet['packet_sha256']==n['reviewer_packet_sha256']
assert a['publication_binding_sha256']==n['publication_binding_sha256']
assert n['review_run_sha256']==expected['review-run91.native.json']
assert load(r/'root.math91.adoption.json')['status']=='ACCEPTED_INDEPENDENT_MATH_ONLY'
(r/'audit.before-source91.json').write_bytes(ap.read_bytes())
slots=['objects','domains','quantifiers','scopes','scopes']
deltas=[dict(slot=slot,severity='informational',description=x['description'],evidence=n['review_evidence'],
    native_classification=x['classification'],native_id=x['id']) for slot,x in zip(slots,n['deltas'])]
a.update(state='accepted',semantic_slots=n['semantic_slots'],deltas=deltas,verdict=n['verdict'],
    source_review=dict(state='accepted',reviewer=n['reviewer'],independent_from_formalizer=True,independent_from_decoder=True,
        evidence=n['review_evidence'],review_run_sha256=n['review_run_sha256'],reviewer_packet_sha256=n['reviewer_packet_sha256'],
        run_artifact=(d/'review-run91.native.json').relative_to(R).as_posix(),native_manifest=pin(d/'closed-RAW91.native.json')))
save(ap,a);pub.inputs.cache_clear();pub.load.cache_clear();pub.check_advance([a['lean']['declaration']],reviewed=True)
fresh(r/'root.source91.adoption.json',dict(status='ACCEPTED_INDEPENDENT_SOURCE_FIDELITY_ONLY',native_hashes=expected,
    reviewer=n['reviewer'],acceptance_scope=n['acceptance_scope'],source_graph_mapping=n['source_graph_audit']['S91_T_mapping'],
    canonical_packet_sha256=packet['packet_sha256'],publication_binding_sha256=a['publication_binding_sha256'],VERIFIED=False))
claim=load(r/'claim.json');cp=R/'research-wiki/frontier-cells'/f"{claim['frontier_cell']}.json";c=load(cp)
c['conceptual_mirror_audit']=load(r/'conceptual-mirror-audit91.json')
c['evidence'].update(proof_review=(d.parent/'independent-math91/decision91.native.json').relative_to(R).as_posix(),
    source_review=(d/'source-review91.native.json').relative_to(R).as_posix(),
    focused_checks=[dict(command=claim['focused_checks'][0],result='PASS; independent whole mathematical/kernel/leaf and source review accepted.',evidence=(r/'independent-math91/leaf-build.receipt.native.json').relative_to(R).as_posix())])
c['source_proof_coverage'].update(compiled_source_review=(d/'source-review91.native.json').relative_to(R).as_posix(),
    coverage_status='Independent whole proof/kernel, source-blind reconstruction and primary-first source review accepted:35 literal definitions,6 original analytic binders,7 exact BODY/exposition regions. Only strict actual next absolute-time coordinate law closes. S91-T weighted fiber realization is accepted, not a separate broader unweighted shear theorem; full A7/global/main/composition remain OPEN.')
c['blocked']['reason']='Independent mathematical/decoder/source acceptance complete; exact science-commit verification and sole-lane aggregation pending.'
e=dict(result_kind='theorem-edge',theorem_delta=claim['theorem_delta'],lean_declarations=claim['target_declarations'],publication_declarations=claim['target_declarations'],
    lean_files=claim['proposed_files'],focused_checks=[pin(r/'independent-math91/leaf-build.receipt.native.json')],truth_boundary=claim['truth_boundary'],
    conceptual_mirror_audit=c['conceptual_mirror_audit'],statement_seal=c['statement_seal'],source_proof_coverage=c['source_proof_coverage'],
    proof_digestion=c['proof_digestion'],purification=c['purification'],independent_math=pin(r/'root.math91.adoption.json'),
    blind_decoder=pin(r/'root.decoder91.adoption.json'),source_review=pin(r/'root.source91.adoption.json'),
    actual_dependencies=c['parents'],integration_notes='One strict actual absolute event-time/history density law with every-history fiber mass, actual guarded clock equality, joint/marginal laws and all ENNReal tests. Original source graph immutable; broader unweighted shear theorem not claimed. Finite ordered iteration, terminal survival/full path/count/A7, restart/Markov/invariance/hypocoercivity/errors/cost/main/composition remain OPEN. Exact-commit verification and unique-lane aggregate/publication/visual gates pending; no self-VERIFIED.')
adv.transition_advance(claim['advance_id'],'PROVED_LOCAL',worker_id=claim['created_by'],evidence=e)
c['status']='proved_locally';save(cp,c);fresh(r/'proved-local91.json',e)
print('PROVED_LOCAL91 with independent mathematics/decoder/source acceptance. Exact-commit verification and stabilization pending.')
