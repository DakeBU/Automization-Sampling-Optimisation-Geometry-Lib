from pathlib import Path
import hashlib,json,sys
sys.path.insert(0,str(Path.cwd()/'tools'))
import astis_semantic_roundtrip as rt,astis_publication as pub,astis_advance as adv
r=Path(__file__).parent;d=r/'independent-source89';load=lambda p:json.loads(Path(p).read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest()
def save(p,x):Path(p).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
def new(p,x):assert not Path(p).exists(),p;save(p,x)
def pin(p):p=Path(p);b=p.read_bytes();return dict(path=p.as_posix(),raw_sha256=sha(b),bytes=len(b))
dp=d/'source-review89.decision.v2.native.json';mp=d/'closed-raw-manifest.source-review89.v2.native.json';rp=d/'source-review89.run.v2.native.json'
assert sha(dp.read_bytes())==sys.argv[1]
assert sha(mp.read_bytes())==sys.argv[2]
m=load(mp);n=load(dp)
for group in ['inputs','outputs']:
 for x in m[group]:
  b=Path(x['path']).read_bytes();assert sha(b)==x['raw_sha256'] and len(b)==x['bytes'],x['path']
original_manifest=load(d/'closed-raw-manifest.source-review89.native.json')
for group in ['inputs','outputs']:
 for x in original_manifest[group]:
  b=Path(x['path']).read_bytes();assert sha(b)==x['raw_sha256'] and len(b)==x['bytes'],x['path']
runhash=sha(rp.read_bytes());assert runhash==n['review_run_sha256']==sys.argv[3]
assert n['verdict']=='equivalent-after-elaboration' and not n['repairs']
assert n['reviewer']=='/root/fresh_source87' and n['independent_from_formalizer'] and n['independent_from_decoder']
assert len(n['literal_definition_audit'])==23 and len(n['analytic_binder_audit'])==6
assert all(not x['blocking'] for x in n['deltas'])
assert len(n['body_audit'])==6
for x in n['body_audit']:
 assert x['verdict']=='accepted' and x['exact_code_matches'] and x['mathematics'] and x['exposition']
 raw=Path(x['path']).read_bytes();assert sha(raw)==x['source_raw_sha256']
 region=b''.join(raw.splitlines(keepends=True)[x['start_line']-1:x['end_line']]);assert sha(region)==x['exact_code_raw_sha256']
assert 'density' in str(n['accepted_truth_boundary']).lower()
assert 'full A.7' in str(n['accepted_truth_boundary']['open'])
ap=Path('research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261011-PBPSActualConditionalNextWaitDensity.json');a=load(ap);assert a['state']=='blind-reconstructed'
packet=rt.semantic_reviewer_packet(a);assert packet==load(r/'source-review89.packet.json')
assert packet['packet_sha256']==n['reviewer_packet_sha256'] and a['publication_binding_sha256']==n['publication_binding_sha256']
assert sha(Path(a['lean']['file']).read_bytes())==n['module']['raw_sha256']
assert sha(Path('website/content/declaration_lessons/pbps-actual-conditional-next-wait-density.json').read_bytes())==n['lesson']['raw_sha256']
assert sha(Path('website/content/publications/pbps-actual-conditional-next-wait-density.json').read_bytes())==n['publication']['raw_sha256']
assert load(r/'root.math89.adoption.json')['status']=='ACCEPTED_INDEPENDENT_MATH_ONLY'
assert all(x['verdict']=='accepted' for x in n['body_audit'])
assert set(n['semantic_slots'])==set(rt.SEMANTIC_SLOTS)
assert all(all(isinstance(v.get(k),str) and v[k].strip() for k in ['original','reconstructed','evidence','relation']) for v in n['semantic_slots'].values())
(r/'audit.before-source89.json').write_bytes(ap.read_bytes())
deltas=[dict(slot=x['slot'],severity='informational',description=x['description'],evidence=f"Native independent source review {dp.as_posix()}, run {runhash}; exact seven slots, twenty-three definitions and six BODY/exposition regions.",native_classification=x['classification']) for x in n['deltas']]
a.update(state='accepted',semantic_slots=n['semantic_slots'],deltas=deltas,verdict=n['verdict'],source_review=dict(state='accepted',reviewer=n['reviewer'],independent_from_formalizer=True,independent_from_decoder=True,evidence=n['review_evidence'],review_run_sha256=runhash,reviewer_packet_sha256=n['reviewer_packet_sha256'],run_artifact=rp.as_posix(),native_manifest=pin(mp)))
save(ap,a);pub.inputs.cache_clear();pub.load.cache_clear();pub.check_advance([a['lean']['declaration']],reviewed=True)
new(r/'root.source89.adoption.json',dict(status='ACCEPTED_INDEPENDENT_SOURCE_FIDELITY_ONLY',native_result=pin(dp),native_manifest=pin(mp),native_run_evidence=pin(rp),canonical_packet_sha256=packet['packet_sha256'],publication_binding_sha256=a['publication_binding_sha256'],reviewer=n['reviewer'],module_RAW_sha256=n['module']['raw_sha256'],accepted_truth_boundary=n['accepted_truth_boundary'],VERIFIED=False))
claim=load(r/'claim.json');cp=Path('research-wiki/frontier-cells')/(claim['frontier_cell']+'.json');c=load(cp)
c['evidence'].update(proof_review=(r/'independent-math89/decision89.json').as_posix(),source_review=dp.as_posix())
c['source_proof_coverage'].update(compiled_source_review=dp.as_posix(),coverage_status='Independent whole-source/kernel mathematics, blind decoder, primary-first anti-anchored source review7slots/23defs/6original analytic binders/6exactBODYregions accepted. Only density component of S87-I5/G86-11 closed; ordered-time iteration/final factor/fullA7 and all global source conclusions remain OPEN.')
c['blocked']['reason']='Focused compile and independent mathematics/blind/source accepted. Named exact-science commit verification and existing sole-lane aggregation pending.'
e=dict(result_kind='theorem-edge',theorem_delta=claim['theorem_delta'],lean_declarations=claim['target_declarations'],publication_declarations=claim['target_declarations'],lean_files=claim['proposed_files'],focused_checks=[pin(r/'focused/production6-explicit-order-comparisons/receipt.json')],truth_boundary=claim['truth_boundary'],conceptual_mirror_audit=c['conceptual_mirror_audit'],statement_seal=c['statement_seal'],source_proof_coverage=c['source_proof_coverage'],proof_digestion=c['proof_digestion'],purification=c['purification'],independent_math=pin(r/'root.math89.adoption.json'),blind_decoder=pin(r/'root.decoder89.adoption.json'),source_review=pin(r/'root.source89.adoption.json'),integration_notes='Actual jointly Borel strict finite next-wait density, genuine all-history subprobability kernel, joint measure identity and all nonnegative extended joint tests on all history events. Only density component of S87-I5/G86-11 closes; final factor/ordered-time iteration/fullA7, physical-time residual memorylessness/random stop/restart/Markov/invariance/allL2/main/errors/unboundedcost/composition OPEN. Existing sole lane; reader browser/main/PURIFIED/live/wholepaper/Goal separate. No self-VERIFIED.')
adv.transition_advance(claim['advance_id'],'PROVED_LOCAL',worker_id=claim['created_by'],evidence=e)
c['status']='proved_locally';save(cp,c);new(r/'proved-local89.json',e)
print('PROVED_LOCAL89; named exact-commit independent verification and sole-lane aggregation pending.')
