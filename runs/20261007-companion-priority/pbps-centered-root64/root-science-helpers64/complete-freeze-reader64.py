from pathlib import Path
import copy,hashlib,json,sys
root=Path.cwd();sys.path.insert(0,str(root/'tools'))
import astis_advance as adv,astis_publication as pub,astis_semantic_roundtrip as rt
r=root/'runs/20261007-companion-priority/pbps-centered-root64';pre=root/'runs/20261007-companion-priority/pbps-centered-root-preproof64'
load=lambda p:json.loads(Path(p).read_bytes())
def write(p,x):
 p=Path(p);assert not p.exists();p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
def replace(p,x):Path(p).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
def pin(p):
 p=Path(p);b=p.read_bytes();return dict(path=p.resolve().as_posix(),raw_bytes=len(b),raw_sha256=hashlib.sha256(b).hexdigest(),lf_sha256=hashlib.sha256(b.replace(b'\r\n',b'\n')).hexdigest())
c=load(r/'claim.json');plan=load(r/'publication-plan.json');names=plan['mathematical_declarations'];fr=r/'focused64-v1';receipt=load(fr/'receipt.json')
assert receipt['exit_code']==0 and receipt['terminal_closed']
mainid=c['frontier_cell'];sharedid='ASTIS-SHARED-l2-real-positive-square-order'
mp=root/'research-wiki/frontier-cells'/f'{mainid}.json';m=load(mp)
write(r/'cell.before-canonical-publication-target64.snapshot.json',m)
g=copy.deepcopy(m);g.update(cell_id=sharedid,title='Positive square order on arbitrary real L2',source_anchor='PBPS2609.06905v1 AppendixD1 square-root monotonicity; ASTIS real-L2 consequence for actual B15',target_statement=(pre/'header0.lean').read_text(encoding='utf-8'),parents=['ASTIS-SHARED-l2-real-complex-positive-lift'],consumers=[names[1]],source_targets=[names[0]])
g['shared_floor_audit'].update(canonical_declaration=names[0],canonical_shared_cell=sharedid,reason='Canonical arbitrary-real-L2 Loewner-square adapter; actual centered-root order is the real consumer; original complex lift remains its existing canonical parent.')
g['reuse_plan'].update(reused_declarations=['AutoSamplingTheory.TechnicalLemmas.Measure.L2RealComplexOperator.exists_positive_complex_lift'],new_shared_declarations=[names[0]],known_consumers=[names[1]],planned_consumers=[])
g['statement_seal'].update(signature_digest=pin(pre/'header0.lean')['raw_sha256'],definition_kind='Arbitrary-measure real L2 bounded positive operators; three canonical complex lifts and internal CFC only. No caller nontriviality/commutation/finiteness premise.')
g['proof_digestion'].update(existing_substrate=g['reuse_plan']['reused_declarations'],new_reusable=[names[0]],new_topology='Canonical complexification transports real positive-square order through complex square-root monotonicity and back to real quadratic forms.')
g['graph_contribution'].update(focus_targets=[names[0]],lean_view='reusable-interface')
g['evidence'].update(owned_files=[c['proposed_files'][0]],truth_boundary='Arbitrary-real-L2 positive-square-order auxiliary result, with actual B15 consumer; independent reviews pending.')
g['source_detail_audit'].update(primary_anchor=g['source_anchor'],gap='No proof gap in focused compiled64; independent source/mathematical/publication admission pending.',fidelity_boundary=g['evidence']['truth_boundary'])
g['purification'].update(scope=g['evidence']['truth_boundary'],canonicalization='One public real-L2 positive-square-order declaration; existing complex lift retained.',compressed_spine_delta=g['proof_digestion']['new_topology'])
write(root/'research-wiki/frontier-cells'/f'{sharedid}.json',g)
m['shared_floor_audit'].update(canonical_declaration=names[1],canonical_shared_cell=mainid)
m['parents'].append(sharedid);m['source_targets']=[names[1]];replace(mp,m)
write(r/'publication-target-metadata64.diagnosis.json',dict(reason='Every publication binding requires its exact canonical declaration owner. One SAU owns the two connected outputs; the reused complex-lift cell is preserved, while the genuine new real-square-order interface receives its own canonical cell and the actual consumer depends on it.',shared_cell=sharedid,actual_cell=mainid,no_parallel_SAU_or_Goal=True,original_exact_headers_and_proofs_unchanged=True,freeze_failure='Initial authoring completed drafts and anonymous packets but final freeze used nonexistent generic run/lease names for the independently owned header review; corrected to exact independent-header64.review.json and owned-lease.json.'))
for slug,aid,cid in zip(plan['slugs'],plan['audit_ids'],[sharedid,mainid]):
 pp=root/'website/content/publications'/f'{slug}.json';p=load(pp);p['items'][0]['bindings'][0]['cell']=cid;replace(pp,p)
pub.inputs.cache_clear();pub.load.cache_clear();data=pub.inputs()
for i,(slug,aid) in enumerate(zip(plan['slugs'],plan['audit_ids'])):
 ap=root/'research-wiki/semantic-roundtrip/audits'/f'{aid}.json';a=load(ap);assert a['state']=='draft'
 item=next(x for x in pub.load() if x['id']==slug);binding=item['bindings'][0]
 a['publication_binding_sha256']=pub.binding_digest(item,binding,data);a['publication_context']=pub.review_context(item,binding,data);replace(ap,a)
 assert rt.decoder_packet(a)==load(root/'.astis/decoder-64'/f'packet{i}.json')
plan['active_cells']=[sharedid,mainid];replace(r/'publication-plan.json',plan)
parents=['AutoSamplingTheory/ExampleCases/ProximalBPS/MacroscopicDefectRoot.lean','AutoSamplingTheory/ExampleCases/ProximalBPS/RoughMeanGradient.lean','AutoSamplingTheory/TechnicalLemmas/FunctionalInequalities/GaussianMarginalPoincare.lean','AutoSamplingTheory/TechnicalLemmas/Measure/L2RealComplexOperator.lean']
inputs=[root/f for f in c['proposed_files']+parents+['lean-toolchain','lake-manifest.json','Libraries/conceptual-mirror-protocol.json','website/content/graph_memory_index.json','website/content/functor_hypergraph.json','Libraries/frontloaded-shared-spine.json']]
inputs += [fr/n for n in ['receipt.json','stdout.log','stderr.log']]+[r/n for n in ['claim.json','frozen-cell0.json','conceptual-mirror-audit64.json','exposition.draft.json','test.statement-seal64.json','publication-plan.json','publication-target-metadata64.diagnosis.json']]
inputs += [pre/n for n in ['header0.lean','header1.lean','root.statement-seal64.json','independent-primary64/source-proof-graph.json','independent-primary64/source-coverage-inventory.json','independent-header64/independent-header64.review.json','independent-header64/owned-lease.json','independent-header64/review-digests.json']]
for cid in plan['active_cells']:inputs.append(root/'research-wiki/frontier-cells'/f'{cid}.json')
for slug,aid in zip(plan['slugs'],plan['audit_ids']):inputs += [root/'website/content/publications'/f'{slug}.json',root/'website/content/declaration_lessons'/f'{slug}.json',root/'research-wiki/semantic-roundtrip/audits'/f'{aid}.json']
write(r/'math-freeze.json',dict(schema_version=1,advance_id=c['advance_id'],checked_base_commit=receipt['checked_science_parent'],inputs=[pin(p) for p in inputs],mathematical_declarations=names,genuine_consumer='Tests.ProximalBPSCenteredRootOrderInverse.genuine_actual_centered_inverse_consumer',private_providers=[],actual_ASTIS_parents=c['dag_inputs'],focused_build_jobs=3944,status='FOCUSED_COMPILED_ONLY_INDEPENDENT_MATH_DECODER_SOURCE_PUBLICATION_PENDING',remaining_boundary=plan['remaining_boundary'],compiler_lease='All root proof/focused sessions terminal closed; negative routes retained without proof credit.'))
adv.checkpoint_advance(c['advance_id'],worker_id=c['created_by'],route_fingerprint='three-canonical-lifts/actual-C4/same-full-scalar-constant-projection/centered-order-derived-unit',progress_signature='3944EXIT0-two-exact-production-statements-real-original-input-norm-and-kernel-consumer-standard3',mathematical_delta=c['theorem_delta'],exact_residual='Independent math, blind reconstruction, anti-anchored source/publication review and serialized integration remain pending; full paper/cost/composition boundary unchanged.')
pub.check_advance(names,reviewed=False)
print('Completed exact64 mathematical freeze and canonical two-target metadata. Two neutral packets unchanged. Draft-publication gate PASS; no PROVED_LOCAL/VERIFIED.')
