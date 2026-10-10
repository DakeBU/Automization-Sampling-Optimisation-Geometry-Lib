from pathlib import Path
import copy,datetime,hashlib,json,subprocess
R=Path('E:/Samplinglib');O=Path(__file__).parent;B=O.parent
def load(p):return json.loads(Path(p).read_text(encoding='utf8'))
def info(p):
 p=Path(p);p=p if p.is_absolute() else R/p;b=p.read_bytes();return dict(path=p.relative_to(R).as_posix(),RAW_bytes=len(b),RAW_sha256=hashlib.sha256(b).hexdigest())
def save(n,v):
 with (O/n).open('x',encoding='utf8',newline='\n') as f:json.dump(v,f,ensure_ascii=False,indent=2);f.write('\n')
pins={'source_inventory84.json':'c9e17b30fd27cc9c2b30f4707d9e63c11404a6642bd6348a4bd1c5605cec6265','source_proof_graph84.json':'d05d7fd9b77f49acd939d31fa858585552956a6793dc4c3e0ab3063d944fafcb','bounded_candidate84.json':'64d2a26607af9e6e426ca5d0830b592404dca4c516cbac0869bc6c656f3e9e0f','source_freeze84.seal.json':'80f8c14962a0bc21b7969341e415acc1ee8663220552d799c6f373b732eb8883','source_freeze84.raw-manifest.json':'b5ebfdb08166f55881ee2eadc4b9faf7844e97608b79abb5a07116b095e47c1b'}
for p,h in pins.items():assert info(B/p)['RAW_sha256']==h
manifest=load(B/'source_freeze84.raw-manifest.json');frozen=[]
for e in manifest['raw_inputs']+manifest['raw_outputs']:
 q=info(e['path']);assert q['RAW_sha256']==e['raw_sha256'] and q['RAW_bytes']==e['bytes'];frozen.append(q)
frozen.append(info(B/'source_freeze84.raw-manifest.json'))
anchors=load(O/'independent-26-anchor-readback84.json')['anchors'];assert len(anchors)==26 and all(x['normalized_hash_equal'] for x in anchors)
inv=load(B/'source_inventory84.json');graph=load(B/'source_proof_graph84.json');scope=load(B/'bounded_candidate84.json')
assert (len(inv['items']),len(graph['nodes']),len(graph['edges']))==(47,22,38)
nodes={x['id']:x for x in graph['nodes']};edges={x['id']:x for x in graph['edges']};junctions={x['id']:x for x in graph['junctions']}
assert sum(x['dependency_edge'] for x in edges.values())==36 and sum(x['route']=='FUTURE_OPEN' for x in edges.values())==4
assert set(x['inventory_id'] for x in graph['scope_coverage'])==set(x['id'] for x in inv['items'])
for row in graph['scope_coverage']:assert all(n in nodes for n in row['graph_nodes'])
assert junctions['NORMALIZE_OR']['operation']=='OR' and junctions['NORMALIZE_OR']['edges']==['E84-11','E84-12']
for j in graph['junctions']:
 for e in j['edges']:assert edges[e]['junction_group']==j['id']
assert all(not edges[e]['dependency_edge'] and edges[e]['status']=='EXCLUDED_BOUNDARY_ASSOCIATION' for e in ['E84-37','E84-38'])
findings=[
 'Source identity/license context is explicitly covered; no mathematical premise or completion credit.',
 'Source fixed y/reference and Euclidean phase retained; finite-dimensional intrinsic Borel/rank0 is explicit ASTIS generalization.',
 'Positive alpha matches standing source; supplies real coercivity, not alpha=0.',
 'alpha<=beta matches source and is retained even where normalization needs fewer conditions.',
 'C2 is source regularity; implies needed continuity/differentiability internally.',
 'Both Hessian inequalities retain all points/directions; lower bound feeds actual normalization API.',
 'eta>0 source scale supplies nonnegative quadratic weight and square-root conventions.',
 'beta eta<=1 is the standing source upper scale, retained without new cap or higher derivative.',
 'Exact conditional potential V+norm(x-y)^2/(2eta), same sign and factor2.',
 'Exact q_y is normalized volume tilt; finite positive normalizer must be proved, not totalized-zero density.',
 'Exact nu_y=q_y times standard momentum; xRef is fixed and not a factor of this outer law.',
 'Harmonic scales/signs and Phi0 identity match primary and actual83 literal.',
 'R0=I convention is preserved, including zero normal; no continuity of bounce required.',
 'Actual rate and initial freeflow integrated hazard match source, with sqrteta and positive part.',
 'Canonical iidExp1 product and zero-index source E_(n+1) adapter retained; actual probability internally produced.',
 'Threshold inf and empty-set infinity preserved; no assumed positive finite wait for every raw clock.',
 'Live start and finite update; stopped dummy has no phase, with parent semantics retained.',
 'Half-open arcs include last live arc whose next wait is infinite; finite elapsed constraint inherited.',
 'Source direct Exp mean-one SLLN route is accurately identified; inherited sufficient indicator-SLLN formal route is distinct. Direct author route remainsOPEN, no new84 proof credit.',
 'Source terminal Borel construction supports scope; stronger joint actual80/83 map is explicitly ASTIS parent, genuinely consumed by state expectation measurability.',
 'Source zero failed-limit vs actual uncovered-z0 representative difference explicitly labelled; fixed-state AE initialization/alltime retained.',
 'Primary first-event probability tends0; actual phase-flow defect is bounded by it, not asserted equal.',
 'Actual83 is genuine inner-test producer for every state with six original conditions; no extra public convergence premise.',
 'Source C_c class accurately retained as specialization, not replaced silently by all L2.',
 'C_b extension is valid over derived finite outer probability; M>=0/global bound are test-class hypotheses, M0 included.',
 'A_t is actual canonical-clock integral of actual Z; pointwise representative before any L2 quotient operator.',
 'Joint strongly measurable real integrand plus SFinite P yields measurable state expectation via exact public integral_prod_right API.',
 'Base Gibbs integrability/positive mass follow C2+positive lower Hessian through existing public APIs; no supplied minimizer or normalizer.',
 'Preferred route uses actual base probability, GaussianConditionalKernel fibers and tilted_tilted; kernel Markov denotes normalized fibers, not phase-process Markov.',
 'Optional direct route has continuous positive exponential dominated by integrable exp(-V); complete route OR preferred, ingredients inside each AND.',
 'Actual stdGaussian has probability instance and identity covariance; no eta momentum scaling, rank0 valid.',
 'Product outer probability is derived; independent outer phase/clock interpretation is allowed, arbitrary correlations excluded.',
 'Every-state/time true clock integrability inherited from actual83, so no integral_undef shortcut.',
 'Integral norm bound under P probability gives abs A<=M and then discrepancy<=2M.',
 'State expectation measurability plus continuous f gives measurable squared discrepancy.',
 'Squared discrepancy bounded by4M2; actual outer probability supplies integrable constant, no invariance premise.',
 'Every-state actual83 expectation limit gives every-state square limit; no pathwise AS implication from convergence in probability.',
 'Filter DCT applies to ordinary countably generated NNReal nhds0 using eventual measurability/domination and outer-AE limit, all supplied by stronger all-state/time facts.',
 'Each squared discrepancy is genuinely integrable under actual nu via measurable bounded domination.',
 'NNReal0 is ordinary/nonpunctured; actual AE init makes A0=f, no negative-time or uniform-time conclusion.',
 'M0/rank0/zero normal/hazard/infinite wait/rawzero/stopped cases need no new premise; parent fallback remains measurable and bounded.',
 'Correlated/random-parameter/uniformAE/alltime-law/version-uniqueness claims explicitly excluded.',
 'Source invariance/Jensen contraction separateOPEN; normalized nu alone proves none of them.',
 'L2 quotient operator/AE-representative domain work separateOPEN; bounded real map not promoted.',
 'REQUIRED_FUTURE_TOPOLOGY_OVERLAY: source independently invokes C_c density; G21 and E36/background bundle it with contraction. Add separate OPEN G23/E39 AND ingredient, with no candidate target change.',
 'Full global process/semigroup/reversal/hypocoercivity boundary explicitly excludedOPEN.',
 'Ideal exact-reference law distinct from implementable sampler/cost; no main/composition claim.'
]
assert len(findings)==47
rows=[]
for item,finding in zip(inv['items'],findings):
 rows.append(dict(inventory_id=item['id'],source_ids=item['source_ids'],graph_nodes=item['graph_nodes'],finding=finding,status='REQUIRED_FUTURE_TOPOLOGY_OVERLAY' if item['id']=='I84-45' else 'ACCEPTED_PROSPECTIVELY'))
edge_rows=[]
for e in graph['edges']:
 state='ACCEPTED_PROSPECTIVELY';finding='Correct source/API ingredient direction and consumer node; no implementation proof credit.'
 if e['id'] in ['E84-07','E84-08','E84-09','E84-10']:finding='AND inside one complete normalization route; exact scale and positive finite mass are discharged by public APIs or direct density arguments.'
 if e['id'] in ['E84-11','E84-12']:finding='Correct OR between complete exact q normalization routes; optional direct route not required alongside preferred route.'
 if e['id'] in ['E84-28','E84-29','E84-30']:finding='AND at bounded outer DCT: measurable dominated square, every-state limit and actual normalized outer measure; no stationarity or samplewise AS input.'
 if e['route']=='FUTURE_OPEN':finding='Correct future-only direction; no candidate84 credit. Source consumer use site is p6.2 all-L2 extension (E33 supports representative/operator admission).'
 if e['id']=='E84-36':state='REQUIRED_FUTURE_TOPOLOGY_OVERLAY';finding='Retain contraction input, remove bundled density phrase; independent density must have its own OPEN incoming edge to G21.'
 if not e['dependency_edge']:finding='Correct nondependency exclusion association; no implication to global boundary.'
 edge_rows.append(dict(edge_id=e['id'],consumer=e['to'],route=e['route'],dependency_edge=e['dependency_edge'],status=state,finding=finding))
review=dict(schema='astis.independent-source-topology-review84.v1',created_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),reviewer='/root/exact_verify77',status='BOUNDED_SCOPE_ACCEPTED_PROSPECTIVELY_FULL_GRAPH_REQUIRES_MINIMAL_FUTURE_OVERLAY',
 source_first_reconstruction=info(O/'independent-reconstruction84.json'),primary_independent_read=info(O/'independent-primary-read84.json'),conditional_independent_read=info(O/'independent-primary-conditional-read84.json'),exact_anchor_readback=info(O/'independent-26-anchor-readback84.json'),normalized_anchors_matching=26,
 frozen_inputs=[info(B/p) for p in pins],inventory_review=rows,edge_review=edge_rows,
 node_review=[dict(node_id=n['id'],status='ACCEPTED_PROSPECTIVELY',finding='Source/explicit ASTIS elaboration scope preserved; OPEN/EXCLUDED nodes carry no proof credit.') for n in graph['nodes']],
 main_branch='Accepted prospective: actual83 statewise inner expectation + actual state measurability + normalized q_y x stdGaussian +4M2 bound => outer squared-integral DCT. All six dynamics binders/eleven definitions and actual Z clauses retained; full header still required.',
 normalization='Preferred public conditional-kernel/tilted_tilted route OR optional direct density route; each internal conjunction correct. GibbsAugmentation public positive ZV plus Integrable.of_integral_ne_zero derives true base integrability; no private proof-local witness exported. stdGaussian probability valid at rank0.',
 exact_API_reads=['GibbsAugmentation.normalized_augmentation_density','StrongConvexGibbsIntegrability.integrable_exp_neg_of_strongConvexOn','GaussianConditionalKernel.exists_tilted_isCondKernel','MeasureTheory.tilted_tilted','MeasureTheory.isProbabilityMeasure_tilted','ProbabilityTheory.isProbabilityMeasure_stdGaussian','MeasureTheory.StronglyMeasurable.integral_prod_right','MeasureTheory.tendsto_integral_filter_of_dominated_convergence'],
 constant_and_quantifier_audit='M>=0 global abs bound; |A_t|<=M, squared error<=4M2; every fixed deterministic y/reference/test/bound. Actual83 every-state expectation limit suffices; no uniformparameter null set or random correlated initialization. Ordinary NNReal nhds0 includes0; rank0/M0/infinite waits preserved.',
 source_class='Source C_c, explicit ASTIS bounded continuous real C_b extension. Source p6.2 bounded representative squared-integral ingredient only; no completed all-L2 operator claim.',
 required_repairs=[dict(id='T84-01',scope='Future OPEN all-L2 graph only',proposal=info(O/'proposed-minimal-topology-overlay84.json'),reason='Source p6.2 independent density hidden in background rather than independent dependency edge. Proposer cannot accept own overlay.')],
 original_counts=graph['counts'],proposed_counts=dict(inventory=47,nodes=23,relations=39,dependency_edges=37,excluded_associations=2),
 independence=dict(distinct_from_extractor=True,extractor_private_script_or_rationale_read=False,source_first_before_inventory_graph_candidate=True,implementation84_read=False,header84_exists_or_reviewed=False,source_graph_not_inferred_from_parent_Lean=True,parent_API_read_after_primary_only=True,own_overlay_selfaccepted=False),
 not_statement_seal=True,no_proof_or_verified_credit=True,no_shared_state_writes=True,
 remaining_obligations=['Distinct exact overlay review and mechanical original-preserving adoption','Prospective whole private Prop/header type and source audit then Statement Seal before proof','Actual84 proof/source-blind/fullBODY/exposition/commit admission','Independent all-L2 density/operator/invariance/Jensen contraction/Markov/cost/main/whole Goal remainOPEN'])
save('topology-review84.json',review)
save('decision84.json',dict(status=review['status'],reviewer_id='/root/exact_verify77',created_utc=review['created_utc'],review=info(O/'topology-review84.json'),proposal=info(O/'proposed-minimal-topology-overlay84.json'),required_repairs=review['required_repairs'],bounded_candidate_mathematical_scope_accepted_prospectively=True,frozen_full_graph_unconditionally_accepted=False,exact_overlay_acceptance_pending_distinct_reviewer=True,statement_seal=False,Lean_proof=False,VERIFIED=False))
for e in frozen:assert info(e['path'])==e
save('closed-RAW-manifest84.json',dict(schema='astis.independent-topology84.noncircular-raw-manifest.v1',status='CLOSED',reviewer='/root/exact_verify77',created_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),frozen_inputs=frozen,owned_artifacts=[info(p) for p in sorted(O.iterdir()) if p.is_file()],original_extractor_artifacts_unchanged=True,self_hash_omitted=True,no_claim_seal_proof_state_transition=True))
print('CLOSED',info(O/'decision84.json')['RAW_sha256'],info(O/'topology-review84.json')['RAW_sha256'],info(O/'proposed-minimal-topology-overlay84.json')['RAW_sha256'],info(O/'closed-RAW-manifest84.json')['RAW_sha256'])
