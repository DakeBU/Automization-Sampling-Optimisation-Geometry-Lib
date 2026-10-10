from pathlib import Path
import hashlib,json,sys
sys.path.insert(0,str(Path.cwd()/'tools'))
import astis_semantic_roundtrip as rt,astis_publication as pub,astis_advance as adv
r=Path(__file__).parent;d=r/'independent-source85';load=lambda p:json.loads(Path(p).read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest()
def save(p,x):Path(p).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
def new(p,x):assert not Path(p).exists(),p;save(p,x)
def pin(p):p=Path(p);b=p.read_bytes();return dict(path=p.as_posix(),RAW_bytes=len(b),RAW_sha256=sha(b))
n=load(d/'source-review.result85.json');m=load(d/'source-review.run-manifest85.json');run=load(d/'source-review.run-evidence85.json')
assert pin(d/'source-review.result85.json')['RAW_sha256']=='0d1e0369d0650d845d8665482bb494698fc8d2559f6490e4dbd5bac4fde526d0'
assert pin(d/'source-review.run-manifest85.json')['RAW_sha256']=='5daf005621c56e1c6bead96a47edf28b770a1b461378c63756e67bbbe64da5fd'
assert m['status']=='closed'
for group in ['raw_inputs','raw_outputs']:
 for x in m[group]:assert sha(Path(x['path']).read_bytes())==x['raw_sha256'],x['path']
runhash=pin(d/'source-review.run-evidence85.json')['RAW_sha256'];assert runhash==n['review_run_sha256']=='2a98c62ccd15b723b80363d9e15439a56828d29aab3a1430b37a62017bd2d76a'
assert n['verdict']=='equivalent-after-elaboration' and not n['repairs'] and n['no_required_mathematical_repairs']
assert n['independent_from_formalizer'] and n['independent_from_decoder'] and run['source_first_chronology']
assert len(run['native_checks'])==83 and all(x['status']=='PASS' for x in run['native_checks'])
for k in ['independent_math_results_read','root_adoption_reports_read','full_canonical_audit_read','earlier_final_verdicts_read','anonymous_or_native_decoder_files_read']:assert n['independence'][k] is False
assert all(not x['blocking'] for x in n['deltas'])
g=n['source_graph_coverage'];s=n['authored_step_coverage'];p=n['public_statement_coverage']
assert not g['gaps'] and (g['inventory_count'],g['nodes_count'],g['relations_count'],g['dependency_count'],g['future_OPEN_dependency_count'],g['excluded_association_count'])==(16,21,29,26,6,3)
assert len(g['inventory'])==16 and len(g['nodes'])==21 and len(g['relations'])==29
assert (g['original_primary_anchors'],g['effective_primary_anchors'])==(28,31) and len(g['primary_anchors'])==31 and all(x['reparsed_exact_match'] for x in g['primary_anchors'])
assert s['gaps']==s['overlaps']==[] and s['expected_steps']==s['reviewed_steps']==s['formula_body_exact_matches']==6
assert p['whole_statement_reviewed'] and p['attribution_reviewed'] and not p['gaps']
assert p['condition_rows_expected']==p['condition_rows_reviewed']==9 and p['formulae_expected']==p['formulae_reviewed']==4
assert all(not x['blocking'] for x in p['conditions']+p['formulae'])
ap=Path('research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261011-PBPSActualPhaseTransitionKernel.json');a=load(ap);assert a['state']=='blind-reconstructed'
packet=rt.semantic_reviewer_packet(a);assert packet==load(r/'source-review85.packet.json')
assert packet['packet_sha256']==n['reviewer_packet_sha256'] and a['publication_binding_sha256']==n['publication_binding_sha256']
assert sha(Path(a['lean']['file']).read_bytes())==n['full_module_sha256']
assert load(r/'root.math85.adoption.json')['status']=='ACCEPTED_INDEPENDENT_MATH_ONLY'
(r/'audit.before-source85.json').write_bytes(ap.read_bytes())
deltas=[dict(slot=x['slot'],severity='blocking' if x['blocking'] else 'informational',description=x['description'],evidence=f"Native independent review {x['id']} in {d.as_posix()}/source-review.result85.json; exact module and all six BODY/formula regions bound by run {runhash}.",native_classification=x['classification']) for x in n['deltas']]
assert set(n['semantic_slots'])==set(rt.SEMANTIC_SLOTS)
assert all(all(isinstance(v.get(k),str) and v[k].strip() for k in ['original','reconstructed','evidence','relation']) for v in n['semantic_slots'].values())
a.update(state='accepted',semantic_slots=n['semantic_slots'],deltas=deltas,verdict=n['verdict'],source_review=dict(state='accepted',reviewer=n['reviewer'],independent_from_formalizer=True,independent_from_decoder=True,evidence=n['verdict_reason'],review_run_sha256=runhash,reviewer_packet_sha256=n['reviewer_packet_sha256'],run_artifact=(d/'source-review.run-evidence85.json').as_posix(),native_manifest=pin(d/'source-review.run-manifest85.json')))
save(ap,a);pub.inputs.cache_clear();pub.load.cache_clear();pub.check_advance([a['lean']['declaration']],reviewed=True)
new(r/'root.source85.adoption.json',dict(status='ACCEPTED_INDEPENDENT_SOURCE_FIDELITY_ONLY',native_result=pin(d/'source-review.result85.json'),native_manifest=pin(d/'source-review.run-manifest85.json'),native_run_evidence=pin(d/'source-review.run-evidence85.json'),canonical_packet_sha256=packet['packet_sha256'],publication_binding_unchanged=True,publication_binding_sha256=a['publication_binding_sha256'],reviewer=n['reviewer'],full_current_module_RAW_sha256=n['full_module_sha256'],semantic_verdict=n['verdict'],source_graph_coverage=g,VERIFIED=False))
claim=load(r/'claim.json');cp=Path('research-wiki/frontier-cells')/(claim['frontier_cell']+'.json');c=load(cp)
c['evidence'].update(proof_review=(r/'independent-math85/decision85.json').as_posix(),source_review=(d/'source-review.result85.json').as_posix())
c['source_proof_coverage'].update(compiled_source_review=(d/'source-review.result85.json').as_posix(),fresh_source_graph='runs/20261007-companion-priority/pbps-transition-kernel-preread85/source-proof-graph85.reviewed-effective.json',fresh_source_inventory='runs/20261007-companion-priority/pbps-transition-kernel-preread85/source-inventory85.reviewed-effective.json',coverage_status='Independent inventory16/node21/relation29 (26dependencies including6futureOPEN and3excluded associations), original28/effective31anchors and all six exact formula/BODY regions accepted. Actual jointly indexed full-phase probability kernel, exact law/events, Dirac0 and bounded Borel dual L1/expectation transfer only. Process Markov/restart/CK, path-law/reversal/invariance/fullL2/hypocoercivity/implemented/main/error/unbounded cost/composition remain OPEN.')
c['blocked']['reason']='Focused compile and independent mathematics/blind/source accepted. Exact-commit verification and sole-lane aggregation pending.'
e=dict(result_kind='theorem-edge',theorem_delta=claim['theorem_delta'],lean_declarations=claim['target_declarations'],publication_declarations=claim['target_declarations'],lean_files=claim['proposed_files'],focused_checks=[pin(r/'focused85-attempt2/receipt.json')],truth_boundary=claim['truth_boundary'],conceptual_mirror_audit=c['conceptual_mirror_audit'],statement_seal=c['statement_seal'],source_proof_coverage=c['source_proof_coverage'],proof_digestion=c['proof_digestion'],purification=c['purification'],independent_math=pin(r/'root.math85.adoption.json'),blind_decoder=pin(r/'root.decoder85.adoption.json'),source_review=pin(r/'root.source85.adoption.json'),integration_notes='Retain same actual80 physical phase and actual Exp1 probability; build jointly indexed full-phase pushforward probability kernel, derive every Borel event law and Dirac0 from fixed-parameter AE initialization, prove dual bounded Borel real-test integrability and exact integral transfer. Sole existing stabilization lane only; no self-VERIFIED or temporal Markov/invariance credit.')
adv.transition_advance(claim['advance_id'],'PROVED_LOCAL',worker_id=claim['created_by'],evidence=e)
c['status']='proved_locally';save(cp,c);new(r/'proved-local85.json',e)
print('PROVED_LOCAL85; independent exact-commit verification pending')
