from pathlib import Path
import hashlib,json,sys
sys.path.insert(0,str(Path.cwd()/'tools'))
import astis_semantic_roundtrip as rt,astis_publication as pub,astis_advance as adv
r=Path(__file__).parent;d=r/'independent-source88';load=lambda p:json.loads(Path(p).read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest()
def save(p,x):Path(p).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
def new(p,x):assert not Path(p).exists(),p;save(p,x)
def pin(p):p=Path(p);b=p.read_bytes();return dict(path=p.as_posix(),raw_sha256=sha(b),bytes=len(b))
dp=d/'source-review88.decision.native.json';mp=d/'closed-raw-manifest.source-review88.native.json';rp=d/'source-review88.run.native.json'
assert sha(dp.read_bytes())=='aa702e1bc0972f90b77b3527ba6e3c68e4ba6e45760cd0221e683548f1bf9da6'
assert sha(mp.read_bytes())=='e9c1c450aa255b65dba3ac3f8423ee02463165d54ed383b8b38328c80fcea332'
m=load(mp);n=load(dp)
for group in ['inputs','outputs']:
 for x in m[group]:
  b=Path(x['path']).read_bytes();assert sha(b)==x['raw_sha256'] and len(b)==x['bytes'],x['path']
runhash=sha(rp.read_bytes());assert runhash==n['review_run_sha256']=='dd99702bb970341f85f740bfcaaac30286d086d82c3f38ba6d1afadd74b011a7'
assert n['verdict']=='equivalent-after-elaboration' and not n['repairs']
assert n['reviewer']=='/root/fresh_source87' and n['independent_from_formalizer'] and n['independent_from_decoder']
assert len(n['complete_definition_audit'])==13 and len(n['complete_analytic_binder_audit'])==6
assert all(not x['blocking'] for x in n['deltas'])
assert len(n['exact_body_exposition_audit'])==5
for x in n['exact_body_exposition_audit']:
 assert x['verdict']=='accepted' and x['exact_code_matches'] and x['mathematics'] and x['exposition']
 raw=Path(x['path']).read_bytes();assert sha(raw)==x['source_raw_sha256']
 region=b''.join(raw.splitlines(keepends=True)[x['start_line']-1:x['end_line']]);assert sha(region)==x['exact_code_raw_sha256']
assert n['accepted_truth_boundary']['target_source_node']=='S87-I4'
assert 'S87-I5' in n['accepted_truth_boundary']['open'] and 'full A.7' in n['accepted_truth_boundary']['open']
ap=Path('research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261011-PBPSActualConditionalNextWaitSurvival.json');a=load(ap);assert a['state']=='blind-reconstructed'
packet=rt.semantic_reviewer_packet(a);assert packet==load(r/'source-review88.packet.json')
assert packet['packet_sha256']==n['reviewer_packet_sha256'] and a['publication_binding_sha256']==n['publication_binding_sha256']
assert sha(Path(a['lean']['file']).read_bytes())==n['lean_module_raw_sha256']
assert sha(Path('website/content/declaration_lessons/pbps-actual-conditional-next-wait-survival.json').read_bytes())==n['lesson_raw_sha256']
assert sha(Path('website/content/publications/pbps-actual-conditional-next-wait-survival.json').read_bytes())==n['publication_raw_sha256']
assert load(r/'root.math88.adoption.json')['status']=='ACCEPTED_INDEPENDENT_MATH_ONLY'
assert all(x['verdict']=='accepted' for x in n['exact_body_exposition_audit'])
assert set(n['semantic_slots'])==set(rt.SEMANTIC_SLOTS)
assert all(all(isinstance(v.get(k),str) and v[k].strip() for k in ['original','reconstructed','evidence','relation']) for v in n['semantic_slots'].values())
(r/'audit.before-source88.json').write_bytes(ap.read_bytes())
deltas=[dict(slot=x['slot'],severity='informational',description=x['description'],evidence=f"Native independent source review {dp.as_posix()}, run {runhash}; exact seven slots, thirteen definitions and five BODY/exposition regions.",native_classification=x['classification']) for x in n['deltas']]
a.update(state='accepted',semantic_slots=n['semantic_slots'],deltas=deltas,verdict=n['verdict'],source_review=dict(state='accepted',reviewer=n['reviewer'],independent_from_formalizer=True,independent_from_decoder=True,evidence=n['review_evidence'],review_run_sha256=runhash,reviewer_packet_sha256=n['reviewer_packet_sha256'],run_artifact=rp.as_posix(),native_manifest=pin(mp)))
save(ap,a);pub.inputs.cache_clear();pub.load.cache_clear();pub.check_advance([a['lean']['declaration']],reviewed=True)
new(r/'root.source88.adoption.json',dict(status='ACCEPTED_INDEPENDENT_SOURCE_FIDELITY_ONLY',native_result=pin(dp),native_manifest=pin(mp),native_run_evidence=pin(rp),canonical_packet_sha256=packet['packet_sha256'],publication_binding_sha256=a['publication_binding_sha256'],reviewer=n['reviewer'],module_RAW_sha256=n['lean_module_raw_sha256'],accepted_truth_boundary=n['accepted_truth_boundary'],VERIFIED=False))
claim=load(r/'claim.json');cp=Path('research-wiki/frontier-cells')/(claim['frontier_cell']+'.json');c=load(cp)
c['evidence'].update(proof_review=(r/'independent-math88/decision88.json').as_posix(),source_review=dp.as_posix())
c['source_proof_coverage'].update(compiled_source_review=dp.as_posix(),coverage_status='Independent whole-source/kernel mathematics, blind decoder, primary-first anti-anchored source review7slots/13defs/6original analytic binders/5exactBODYregions accepted. Only S87-I4 history-dependent conditional next-wait survival closed; S87-I5/density/ordered-time iteration/final factor/fullA7 and all global source conclusions remain OPEN.')
c['blocked']['reason']='Focused compile and independent mathematics/blind/source accepted. Named exact-science commit verification and existing sole-lane aggregation pending.'
e=dict(result_kind='theorem-edge',theorem_delta=claim['theorem_delta'],lean_declarations=claim['target_declarations'],publication_declarations=claim['target_declarations'],lean_files=claim['proposed_files'],focused_checks=[pin(r/'focused/production6-sum-observable-equality/receipt.json')],truth_boundary=claim['truth_boundary'],conceptual_mirror_audit=c['conceptual_mirror_audit'],statement_seal=c['statement_seal'],source_proof_coverage=c['source_proof_coverage'],proof_digestion=c['proof_digestion'],purification=c['purification'],independent_math=pin(r/'root.math88.adoption.json'),blind_decoder=pin(r/'root.decoder88.adoption.json'),source_review=pin(r/'root.source88.adoption.json'),integration_notes='Actual deterministic-depth history-dependent conditional next-wait survival, joint event/Borel bounded weight and unnormalized null-event identity. Only S87-I4 closes; density/final factor/ordered-time iteration/fullA7, physical-time residual memorylessness/random stop/restart/Markov/invariance/allL2/main/errors/unboundedcost/composition OPEN. Existing sole lane; reader browser/main/PURIFIED/live/wholepaper/Goal separate. No self-VERIFIED.')
adv.transition_advance(claim['advance_id'],'PROVED_LOCAL',worker_id=claim['created_by'],evidence=e)
c['status']='proved_locally';save(cp,c);new(r/'proved-local88.json',e)
print('PROVED_LOCAL88; named exact-commit independent verification and sole-lane aggregation pending.')
