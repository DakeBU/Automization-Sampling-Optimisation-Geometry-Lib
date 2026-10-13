from pathlib import Path
import hashlib,json,sys
sys.path.insert(0,str(Path.cwd()/'tools'))
import astis_semantic_roundtrip as rt,astis_publication as pub,astis_advance as adv
r=Path(__file__).parent;d=r/'fresh-source82';load=lambda p:json.loads(Path(p).read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest()
def save(p,x):Path(p).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
def new(p,x):assert not Path(p).exists(),p;save(p,x)
def pin(p):p=Path(p);b=p.read_bytes();return dict(path=p.as_posix(),RAW_bytes=len(b),RAW_sha256=sha(b))
n=load(d/'source-review.result82.json');m=load(d/'source-review.run-manifest82.json')
assert sha((d/'source-review.result82.json').read_bytes())=='9324f048b3b557ef585791b0db1549107cd444c61d9541299d845b13795e7776'
assert sha((d/'source-review.run-manifest82.json').read_bytes())=='3b165cf2b3bb121c547878b24e959e87b94ed832be15efddfe2e346e1b5caa6f'
assert m['status']=='closed'
for group in ['raw_inputs','raw_outputs']:
 for x in m[group]:assert sha(Path(x['path']).read_bytes())==x['raw_sha256'],x['path']
runhash=sha((d/'source-review.run-evidence82.json').read_bytes());assert runhash==n['review_run_sha256']=='90f6416500e968bdc387c0c42143f4c67472e4af3a5cddfd9df08454ec021948'
assert n['verdict']=='equivalent-after-elaboration' and not n['repairs'] and n['no_required_mathematical_repairs'] and n['no_unresolved_exposition_repairs']
assert n['independence']['source_first'] and n['independence']['source_pins_verified_before_fullBODY']
assert all(not x['blocking'] for x in n['deltas'])
g=n['source_graph_coverage'];s=n['authored_step_coverage']
assert not g['unmapped_inventory_items'] and not g['unmapped_nodes'] and not g['unmapped_edges']
assert g['inventory_expected']==g['inventory_reviewed']==36
assert s['gaps']==s['overlaps']==[] and s['expected_steps']==s['reviewed_steps']==s['formula_body_exact_matches']==9
ap=Path('research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261010-PBPSActualSmallTimeContinuity.json');a=load(ap);assert a['state']=='blind-reconstructed'
packet=rt.semantic_reviewer_packet(a);assert packet==load(r/'source-review82.packet.json')
assert packet['packet_sha256']==n['reviewer_packet_sha256'] and a['publication_binding_sha256']==n['publication_binding_sha256']
assert sha(Path(a['lean']['file']).read_bytes())==n['full_module_sha256']
assert load(r/'root.math82.adoption.json')['status']=='ACCEPTED_INDEPENDENT_MATH_ONLY'
(r/'audit.before-source82.json').write_bytes(ap.read_bytes())
deltas=[dict(slot=x['slot'],severity='blocking' if x['blocking'] else 'informational',description=x['description'],evidence=f"Native independent review {x['id']} in {d.as_posix()}/source-review.result82.json, exact current module and nine BODY regions bound by run {runhash}.",native_classification=x['classification']) for x in n['deltas']]
assert all(all(v.get(k) for k in ['original','reconstructed','evidence','relation']) for v in n['semantic_slots'].values())
a.update(state='accepted',semantic_slots=n['semantic_slots'],deltas=deltas,verdict=n['verdict'],source_review=dict(state='accepted',reviewer=n['reviewer'],independent_from_formalizer=True,independent_from_decoder=True,evidence=n['verdict_reason'],review_run_sha256=runhash,reviewer_packet_sha256=n['reviewer_packet_sha256'],run_artifact=(d/'source-review.run-evidence82.json').as_posix(),native_manifest=pin(d/'source-review.run-manifest82.json')))
save(ap,a);pub.inputs.cache_clear();pub.load.cache_clear();pub.check_advance([a['lean']['declaration']],reviewed=True)
new(r/'root.source82.adoption.json',dict(status='ACCEPTED_INDEPENDENT_SOURCE_FIDELITY_ONLY',native_result=pin(d/'source-review.result82.json'),native_manifest=pin(d/'source-review.run-manifest82.json'),native_run_evidence=pin(d/'source-review.run-evidence82.json'),canonical_packet_sha256=packet['packet_sha256'],publication_binding_unchanged=True,publication_binding_sha256=a['publication_binding_sha256'],reviewer=n['reviewer'],full_current_module_RAW_sha256=n['full_module_sha256'],semantic_verdict=n['verdict'],source_graph_coverage=g,VERIFIED=False))
claim=load(r/'claim.json');cp=Path('research-wiki/frontier-cells')/(claim['frontier_cell']+'.json');c=load(cp)
c['evidence'].update(proof_review=(r/'independent-math82/decision82.json').as_posix(),source_review=(d/'source-review.result82.json').as_posix())
c['source_proof_coverage'].update(compiled_source_review=(d/'source-review.result82.json').as_posix(),fresh_source_graph='runs/20261007-companion-priority/pbps-process-regularity-preread82/source_proof_graph82.json',fresh_source_inventory='runs/20261007-companion-priority/pbps-process-regularity-preread82/source_inventory82.json',coverage_status='Independent source inventory36/node13/edge20 and allnine exact formula/BODY regions accepted. Actual firstwait/firstarc defect bound and fixedparameter zero-time stochastic continuity only; full L2/Markov/restart/semigroup/invariance/main/implementation/error/cost/composition remain OPEN.')
c['blocked']['reason']='Focused compile and independent mathematics/blind/source accepted. Exact-commit verification and sole-lane aggregation pending.'
e=dict(result_kind='theorem-edge',theorem_delta=claim['theorem_delta'],lean_declarations=claim['target_declarations'],publication_declarations=claim['target_declarations'],lean_files=claim['proposed_files'],focused_checks=[pin(r/'focused82-attempt6/receipt.json')],truth_boundary=claim['truth_boundary'],conceptual_mirror_audit=c['conceptual_mirror_audit'],statement_seal=c['statement_seal'],source_proof_coverage=c['source_proof_coverage'],proof_digestion=c['proof_digestion'],purification=c['purification'],independent_math=pin(r/'root.math82.adoption.json'),blind_decoder=pin(r/'root.decoder82.adoption.json'),source_review=pin(r/'root.source82.adoption.json'),integration_notes='Actual input survival transported from inverse-hazard producer, deterministic initial live arc identifies no-event phase, measurable defect and norm-tail squeeze; retain complete actual phase semantics. Sole existing stabilization lane only; no self-VERIFIED.')
adv.transition_advance(claim['advance_id'],'PROVED_LOCAL',worker_id=claim['created_by'],evidence=e)
c['status']='proved_locally';save(cp,c);new(r/'proved-local82.json',e)
print('PROVED_LOCAL82; independent exact-commit verification pending')
