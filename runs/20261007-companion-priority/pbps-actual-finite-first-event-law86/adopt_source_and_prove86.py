from pathlib import Path
import hashlib,json,sys
sys.path.insert(0,str(Path.cwd()/'tools'))
import astis_semantic_roundtrip as rt,astis_publication as pub,astis_advance as adv
r=Path(__file__).parent;d=r/'independent-source86';load=lambda p:json.loads(Path(p).read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest()
def save(p,x):Path(p).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
def new(p,x):assert not Path(p).exists(),p;save(p,x)
def pin(p):p=Path(p);b=p.read_bytes();return dict(path=p.as_posix(),RAW_bytes=len(b),RAW_sha256=sha(b))
n=load(d/'source-review86.final-successor.decision.json');m=load(d/'source-review86.final-successor.native-RAW-manifest.json');run=load(d/'source-review86.final-successor.run.json')
assert pin(d/'source-review86.final-successor.decision.json')['RAW_sha256']=='86d9a734d1e995f118759f9aaf850271b597795b43b83d5093388263bc66937d'
assert pin(d/'source-review86.final-successor.native-RAW-manifest.json')['RAW_sha256']=='0e7883dfda2d2114b3ec0e0f3b00bbf561159c978e24db606cf43855e89d09b7'
for group in ['inputs','outputs']:
 for x in m[group]:assert sha(Path(x['path']).read_bytes())==x['raw_sha256'],x['path']
runhash=pin(d/'source-review86.final-successor.run.json')['RAW_sha256'];assert runhash==n['review_run_sha256']=='6fc704d2f49f0af36143e74adf58d1bb5837cd3aeb5342d850a882abc4d817db'
assert n['verdict']=='equivalent-after-elaboration' and not n['repairs']
assert n['independent_from_formalizer'] and n['independent_from_decoder']
assert all(not x['blocking'] for x in n['deltas'])
g=n['source_graph_coverage'];s=n['authored_step_coverage'];p=n['public_statement_coverage'];cov=g['coverage']
assert (cov['nodes'],cov['relations'],cov['dependency_edges'],cov['excluded_associations'],cov['accounted_explicit_anchors'])==(38,76,73,3,72) and cov['missing']==[]
assert s['total']==s['reviewed']==s['exact_contiguous_code_regions']==11
assert all(x['exact_contiguous_region'] and x['mathematical_explanation_matches_code'] for x in s['steps'])
assert p['all14_definitions_audited'] and p['all_six_analytic_binders_audited'] and p['candidate_layout_verified'] and not p['layout_verified']
assert load(r/'root.exhaustive-topology86.adoption.json')['status']=='COMPOSED_DISTINCT_EXACT_SOURCE_TOPOLOGY_REVIEWS_ACCEPTED'
assert load(r/'root.reader-adjacency86.adoption.json')['canonical_changed'] is False
ap=Path('research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261011-PBPSActualFiniteFirstEventLaw.json');a=load(ap);assert a['state']=='blind-reconstructed'
packet=rt.semantic_reviewer_packet(a);assert packet==load(r/'source-review86.packet.json')
assert packet['packet_sha256']==n['reviewer_packet_sha256'] and a['publication_binding_sha256']==n['publication_binding_sha256']
assert sha(Path(a['lean']['file']).read_bytes())==n['full_module_sha256']
assert load(r/'root.math86.adoption.json')['status']=='ACCEPTED_INDEPENDENT_MATH_ONLY'
(r/'audit.before-source86.json').write_bytes(ap.read_bytes())
deltas=[dict(slot=x['slot'],severity='blocking' if x['blocking'] else 'informational',description=x['description'],evidence=f"Native independent review slot {x['slot']} in {d.as_posix()}/source-review86.final-successor.decision.json; exact module and all eleven BODY/formula regions bound by run {runhash}.",native_classification=x['classification']) for x in n['deltas']]
assert set(n['semantic_slots'])==set(rt.SEMANTIC_SLOTS)
assert all(all(isinstance(v.get(k),str) and v[k].strip() for k in ['original','reconstructed','evidence','relation']) for v in n['semantic_slots'].values())
a.update(state='accepted',semantic_slots=n['semantic_slots'],deltas=deltas,verdict=n['verdict'],source_review=dict(state='accepted',reviewer=n['reviewer'],independent_from_formalizer=True,independent_from_decoder=True,evidence=n['reason'],review_run_sha256=runhash,reviewer_packet_sha256=n['reviewer_packet_sha256'],run_artifact=(d/'source-review86.final-successor.run.json').as_posix(),native_manifest=pin(d/'source-review86.final-successor.native-RAW-manifest.json')))
save(ap,a);pub.inputs.cache_clear();pub.load.cache_clear();pub.check_advance([a['lean']['declaration']],reviewed=True)
new(r/'root.source86.adoption.json',dict(status='ACCEPTED_INDEPENDENT_SOURCE_FIDELITY_ONLY',native_result=pin(d/'source-review86.final-successor.decision.json'),native_manifest=pin(d/'source-review86.final-successor.native-RAW-manifest.json'),native_run_evidence=pin(d/'source-review86.final-successor.run.json'),canonical_packet_sha256=packet['packet_sha256'],publication_binding_unchanged=True,publication_binding_sha256=a['publication_binding_sha256'],reviewer=n['reviewer'],full_current_module_RAW_sha256=n['full_module_sha256'],semantic_verdict=n['verdict'],source_graph_coverage=g,VERIFIED=False))
claim=load(r/'claim.json');cp=Path('research-wiki/frontier-cells')/(claim['frontier_cell']+'.json');c=load(cp)
c['evidence'].update(proof_review=(r/'independent-math86/decision86.json').as_posix(),source_review=(d/'source-review86.final-successor.decision.json').as_posix())
c['source_proof_coverage'].update(compiled_source_review=(d/'source-review86.final-successor.decision.json').as_posix(),coverage_status='Composed distinct source-only topology repairs accepted,47inventory/38nodes/76relations=73deps+3excluded,all72independent anchors. Independent final theorem source review7slots/14defs/6original analytic hypotheses/11exactregions accepted. Actual first finite-event density/post-bounce law/mass and bounded Borel integrals only; canonical V4 renderer application/site/browser and all global source conclusions remain pending.')
c['blocked']['reason']='Focused compile and independent mathematics/blind/source accepted. Exact-commit verification and sole-lane aggregation pending.'
e=dict(result_kind='theorem-edge',theorem_delta=claim['theorem_delta'],lean_declarations=claim['target_declarations'],publication_declarations=claim['target_declarations'],lean_files=claim['proposed_files'],focused_checks=[pin(r/'focused-complete86.attempt1/receipt.json')],truth_boundary=claim['truth_boundary'],conceptual_mirror_audit=c['conceptual_mirror_audit'],statement_seal=c['statement_seal'],source_proof_coverage=c['source_proof_coverage'],proof_digestion=c['proof_digestion'],purification=c['purification'],independent_math=pin(r/'root.math86.adoption.json'),blind_decoder=pin(r/'root.decoder86.adoption.json'),source_review=pin(r/'root.source86.adoption.json'),integration_notes='Actual Exp1 coordinate0 and actual flow/bounce/hazard produce finite first-event density, exact marked law, subprobability mass and three bounded Borel real-test L1 outputs with weighted Lebesgue identity. Five keylemmas and six public BODY regions; unused-tail/fullA7/path/reversal/invariance/Markov/allL2/main/error/unboundedcost/composition OPEN. Apply distinct reviewed V4 renderer only in existing sole lane; no self-VERIFIED or page/browser credit.')
adv.transition_advance(claim['advance_id'],'PROVED_LOCAL',worker_id=claim['created_by'],evidence=e)
c['status']='proved_locally';save(cp,c);new(r/'proved-local86.json',e)
print('PROVED_LOCAL86; independent exact-commit verification pending')
