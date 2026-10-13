from pathlib import Path
import datetime,hashlib,json
R=Path('E:/Samplinglib');B=R/'runs/20261007-companion-priority/pbps-bounded-test-preread83';O=B/'independent-topology83'
def info(p):
 p=Path(p);b=p.read_bytes();return dict(path=p.relative_to(R).as_posix(),RAW_bytes=len(b),RAW_sha256=hashlib.sha256(b).hexdigest())
def load(p):return json.loads(p.read_text(encoding='utf8'))
def save(n,d):
 with (O/n).open('x',encoding='utf8',newline='\n') as f:json.dump(d,f,ensure_ascii=False,indent=2);f.write('\n')
def canon(v):return json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf8')
mf=B/'source_freeze83.closed-raw-manifest.json';manifest=load(mf)
assert info(mf)['RAW_sha256']=='6f0e838a8c3ada6dec3d3e842be55252885f0ba49f861256309963d5e8b6201d'
for e in manifest['raw_inputs']+manifest['raw_outputs']:
 p=Path(e['path']);assert info(p)['RAW_sha256']==e['raw_sha256'] and info(p)['RAW_bytes']==e['bytes']
inv=load(B/'source_inventory83.json');graph=load(B/'source_proof_graph83.json');supp=load(B/'optional-route-topology-supplement83.json');candidate=load(B/'bounded_candidate83.json')
readback=load(O/'independent-all-inventory-region-readback83.json');by_id={e['inventory_id']:e for e in readback}
assert len(inv['items'])==30 and len(graph['nodes'])==17 and len(graph['edges'])==28 and len(supp['added_edges'])==2
nodeids={e['id'] for e in graph['nodes']};edges=graph['edges']+supp['added_edges'];edgeids={e['id'] for e in edges}
assert len(edgeids)==30 and all(e['ingredient'] in nodeids and e['consumer'] in nodeids for e in edges)
assert all(set(e['source_graph_nodes'])<=nodeids for e in inv['items'])
patches=[
 dict(artifact='optional-route-topology-supplement83.json',selector='added_edges[id=E83-29].status',before='OPTIONAL_OR',after='OPTIONAL_ROUTE_AND_INGREDIENT',
      reason='Free-flow convergence is jointly needed with hazard smalltime and defect control inside the optional probability route. It is not an independently sufficient alternative.'),
 dict(artifact='optional-route-topology-supplement83.json',selector='added_edges[id=E83-30].status',before='OPTIONAL_OR',after='OPTIONAL_ROUTE_AND_INGREDIENT',
      reason='Vanishing hazard probability is jointly needed inside the same optional branch, not OR against free-flow convergence.'),
 dict(artifact='source_proof_graph83.json',selector='edges[id=E83-28]',
      before=next(e for e in graph['edges'] if e['id']=='E83-28'),
      after=dict(id='E83-28',ingredient='G83-16',consumer='G83-17',status='EXCLUDED_BOUNDARY_ASSOCIATION',dependency_edge=False,
                 reason='Scope adjacency only: the broad G83-17 excluded obligations remain separate. No source or Lean implication from L2 extension/contraction to Markov, restart, invariance, reversal, cost, or composition. Source A1.SS1.p3.7 constructs Markov first; A1.Thmtheorem1 starts with those Markov operators.'),
      reason='The original umbrella consumer combines prerequisites and later consumers. Its broad direction cannot be a proof-ingredient implication.')]
junctions=[
 dict(id='J83-main-expectation',consumer='G83-12',route='preferred integrated-defect route',AND_edges=['E83-18','E83-19','E83-20'],
      meaning='Vanishing q_t AND the integrated bounded-test defect estimate AND deterministic test-flow convergence imply expectation convergence.'),
 dict(id='J83-optional-tail',consumer='G83-13',route='optional bounded-continuous probability/locality route',AND_edges=['E83-21','E83-22','E83-23','E83-29','E83-30'],
      meaning='Actual measurable probability realization, continuous bounded test, phase-flow defect bound, free-flow continuity and hazard smalltime are jointly available. Actual82 internally derives the positive-threshold tails used here; G83-07 alone denotes the defect bound, not the whole stochastic-continuity conclusion. Integrability follows from the same G83-03/G83-08 inputs through G83-09.'),
 dict(id='J83-expectation-alternatives',consumer='G83-12',OR_routes=[dict(junction='J83-main-expectation'),dict(edge='E83-24',producer='G83-13')],
      meaning='Either sufficient branch may prove the limit. The optional branch is never an additional mandatory conjunct of the preferred route.')]
overlay=dict(schema_version=1,status='PROPOSED_MINIMAL_TOPOLOGY_CLARIFICATION_NOT_APPLIED',proposer='/root/exact_verify77',
 original_graph=info(B/'source_proof_graph83.json'),original_supplement=info(B/'optional-route-topology-supplement83.json'),
 patches=patches,junctions=junctions,original_files_unchanged=True,
 row_count_note='Keep all original17node/30relation rows. E83-28 becomes a nondependency boundary association:29 ingredient/dependency rows plus1 association. No new theorem, source hypothesis, graph node or proof credit.',
 source_author_separate_exact_overlay_review_required=True,StatementSeal=False,VERIFIED=False)
save('proposed-minimal-topology-overlay83.json',overlay)

inventory_findings=[
 'Pinned v1 provenance, not a mathematical binder or result.',
 'Source fixes C2 potential and0<alpha<=beta; retain the original split source binders.',
 'Exact Hessian sandwich supplies the standing curvature assumptions, no higher derivatives.',
 'eta in(0,1/beta] preserves eta>0 and beta eta<=1, independently read at this anchor.',
 'The center/residual definitions have the actual eta and reference argument; no changed flow normalization.',
 'The argument is at fixed deterministic y/reference and initial phase, not arbitrary correlated random-state substitution.',
 'Actual rate has sqrt(eta) and positive-part inner product; no source rate cap is supplied publicly.',
 'Harmonic flow has sqrt(eta) and reciprocal scale and is continuous at0 with identity value.',
 'Reflection is the actual total R0=identity convention; no jump at infinity is evaluated.',
 'Source warns of bounce discontinuity at vanishing normal; test continuity does not require bounce continuity.',
 'Actual iid Exp1 clocks and initial live record atT0=0; implementation index0 corresponds to source next-clock index.',
 'Actual threshold integral and empty-hit infinity first wait are exact.',
 'Finite wait update only, then reflection at endpoint; stopped alternative is auxiliary.',
 'Half-open source arcs and last live infinite-wait arc are preserved at every finite elapsed time.',
 'Direct Exp mean1 SLLN and then memoryless Markov are separate source steps. Inherited indicator-SLLN alternative cannot silently close the direct author route or Markov.',
 'Source terminal Borel version uses zero on failed limit; actual chosen uncovered-z0 representative is a labelled exceptional adapter, harmless only under each fixed-parameter AE agreement.',
 'Source C_c, deterministic flow continuity, and first-event control genuinely feed the pointwise test ingredient; initial invariance/Jensen clause remains excluded.',
 'q_t=1-exp(-Lambda_t)->0 is the exact first-event formula; phase-flow defect is contained in that event, not equal to it.',
 'Pointwise expected-test convergence is the hidden prerequisite before the source outer-state DCT. C_c real tests are continuous and bounded.',
 'Outer-state DCT is a distinct integral over an initial-phase law. Probability convergence over clocks is not samplewise AS convergence.',
 'Invariance AND Jensen yield contraction; neither is a premise or output of fixed-state clock expectation convergence.',
 'Density AND already-established contraction/representative independence extend C_c L2 continuity to allL2.',
 'A1 transition-operator proposition assumes Markov operators already constructed; expectation convergence does not produce those laws.',
 'The outer source law is conditional Gibbs position times standard Gaussian momentum. No outer invariant measure is needed for the present fixed-state clock integral.',
 'Path reversal then F=1 yields source invariance; leave this scientific proof boundary OPEN.',
 'Full jump-path expansion/Tonelli/change of variables is separate; first-event split is insufficient to prove it.',
 'All bounded continuous real tests are a valid explicitly labelled ASTIS extension of the source C_c pointwise class, not literal source quotation.',
 'Integrate a bounded discrepancy<=2M times measurable defect indicator under actual probabilityP; integrability and the bound are internal obligations.',
 'Optional epsilon/delta probability split is valid only with local continuity and global bound. No ordinary AS-DCT from probability convergence.',
 'Ideal random-reference H_y averaging, global random process law and implemented reference-sampling/cost claims remain outside this fixed-reference test edge.'
]
inventory_reviews=[]
for e,f in zip(inv['items'],inventory_findings):
 n=by_id[e['id']];inventory_reviews.append(dict(id=e['id'],source_id=e['source_id'],source_graph_nodes=e['source_graph_nodes'],
  classification=e['classification'],status='REVIEWED_NODE_OR_EXCLUDED_BOUNDARY',finding=f,
  independently_reread_anchor=bool(n['text']),own_normalized_text_sha256=n['own_anchor_sha256'],
  extractor_normalized_text_sha256=n['extractor_normalized_anchor_sha256'],normalized_digest_matches=n['normalized_digest_matches']))
node_findings={
 'G83-01':'Six analytic binders plus fixed deterministic parameters are correct. Test-class continuity/boundedness is separately labelled extension, not a new potential/dynamics hypothesis.',
 'G83-02':'Correct actual live initialized record, guarded finite update, strict half-open interpolation and last live infinity arc.',
 'G83-03':'Correct inherited measurable actual probability realization. Per-fixed-parameter common AE allfinite/init; no arbitrary supplied process premise or uniform-parameter exceptional event.',
 'G83-04':'Correct continuous free flow with Phi0=id, including rank0.',
 'G83-05':'Correct actual firstwait survival and Lambda0/continuity. Actual product coordinate law is inherited, not abstract replacement.',
 'G83-06':'Correct no-first-event phase equality for strict t<wait including wait infinity; t=wait is outside the no-event interval.',
 'G83-07':'Correct measurable phase-flow defect inequality; do not mistake this node alone for the entire positive-threshold stochastic-continuity conclusion consumed in optional G83-13.',
 'G83-08':'Correct bounded continuous real test class. Source C_c inclusion follows from continuity plus compact support; no unbounded continuous-test extension without additional integrability control.',
 'G83-09':'Measurability of composition and finite probability plus uniform bound yield integrability at every finite time; bounded discrepancy is integrable too.',
 'G83-10':'Valid genuine new estimate: absolute integral difference<=integral absolute discrepancy<=2M P(defect)<=2M q_t. Needs derived integrability, not a supplied quantitative estimate.',
 'G83-11':'Correct continuity of f at initial phase applied to deterministic flow; global uniform continuity is unnecessary.',
 'G83-12':'Valid new fixed-state expectation limit with ordinary NNReal neighborhood0, including t0 by actual AE initialization. Bind M explicitly in any later quantitative header.',
 'G83-13':'Mathematically valid optional epsilon/delta probability route. Inputs are jointly required inside this branch; branch output is OR versus the preferred route. No AS-DCT shortcut.',
 'G83-14':'Correct immediate source consumer via C_c specialization. Pointwise integral may be called operator value only without implying Markov/semigroup properties.',
 'G83-15':'Correct excluded outer-L2 step: jointly measurable state integral, exact finite outer source law, pointwise convergence and squared domination4M^2 are still required. Invariance is not needed merely for this bounded outer DCT.',
 'G83-16':'Correct excluded full operator step: invariance/Jensen, representative independence, contractivity and C_c density.',
 'G83-17':'Correct umbrella OPEN boundary, but it is not universally downstream of G83-16. Markov/restart/invariance precede parts of the operator argument; E83-28 must be a nondependency association.'}
node_reviews=[dict(id=n['id'],status='REVIEWED_EXCLUDED_OPEN' if n['kind']=='EXCLUDED_OPEN' else 'REVIEWED_SOURCE_OR_LABELLED_ADAPTER',finding=node_findings[n['id']]) for n in graph['nodes']]
edge_reviews=[]
for e in edges:
 status='ACCEPTED_SCOPED_INGREDIENT';finding=e['reason']
 if e['id']=='E83-24':status='ACCEPTED_OR_BETWEEN_SUFFICIENT_ROUTES';finding='Only the optional branch output competes by OR with the main sufficient conjunction at G83-12.'
 elif e['id'] in {'E83-29','E83-30'}:status='REQUIRES_EXPLICIT_AND_WITHIN_OPTIONAL_BRANCH';finding='Valid ingredient direction, but OPTIONAL_OR must mean optional branch membership, never an OR between free-flow and hazard inputs. Exact proposed status/junction overlay provided.'
 elif e['id']=='E83-28':status='REQUIRES_NONDEPENDENCY_BOUNDARY_ASSOCIATION';finding='Broad global node contains prerequisites and later consumers; no universal source/Lean implication from L2 extension. Exact retag supplied.'
 elif e['id'] in {'E83-26','E83-27'}:status='ACCEPTED_EXCLUDED_OPEN_PARTIAL_DEPENDENCY';finding='Direction is a prospective necessary ingredient only; outer measurability/finite domination and independent contraction/density must also be supplied. No current theorem credit.'
 elif e['id']=='E83-23':finding='Defect bound combines with free-flow/hazard smalltime inside inherited actual82 stochastic continuity; positive-threshold probability tails are not the bare conclusion of G83-07 alone.'
 edge_reviews.append(dict(id=e['id'],ingredient=e['ingredient'],consumer=e['consumer'],status=status,finding=finding))
save('topology-review83.json',dict(schema_version=1,status='BOUNDED_SCOPE_ACCEPTED_TOPOLOGY_CONDITIONALLY_ACCEPTED_WITH_EXACT_MINIMAL_OVERLAY',
 reviewer_id='/root/exact_verify77',created_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
 primary=info(Path(manifest['raw_inputs'][0]['path'])),source_closed_manifest=info(mf),
 inventory=info(B/'source_inventory83.json'),original_graph=info(B/'source_proof_graph83.json'),supplement=info(B/'optional-route-topology-supplement83.json'),bounded_candidate=info(B/'bounded_candidate83.json'),
 primary_first=info(O/'independent-primary-reread83.json'),independent_preinventory_reconstruction=info(O/'before-inventory-topology83.json'),
 all_regions_readback=info(O/'independent-all-inventory-region-readback83.json'),inventory_reviews=inventory_reviews,node_reviews=node_reviews,edge_reviews=edge_reviews,
 coverage=dict(inventory_reviewed=30,nodes_reviewed=17,original_edges_reviewed=28,supplement_edges_reviewed=2,unmapped_inventory_items=[],unmapped_nodes=[],unmapped_edges=[],all_source_regions_NODE_or_EXCLUDED=True,full_paper_coverage_claim=False),
 mathematical_scope=dict(verdict='ACCEPTED_PROSPECTIVE_SOURCE_FAITHFUL_ELABORATION',
  genuine_delta='Actual bounded test integrability and expectation estimate/limit are new internal consumers of actual82, rather than a wrapper that assumes its own expectation conclusion.',
  source_class='Source C_c real tests; all C_b real tests are an explicitly labelled ASTIS extension of the pointwise ingredient.',
  hidden_assumptions='No new potential/trajectory/Markov/nonexplosion/cap/provider premise. Test continuity and a global nonnegative bound define the chosen test class. Finite actual probability and actual phase measurability/defect estimates must be consumed internally.',
  strict_smaller_dependencies=['Actual82 measurable realization and defect probability bound, including AE initialization','Existing harmonic and integrated-hazard continuity/zero-time identities for preferred quantitative estimate-to-limit route','Basic measurable composition, bounded finite-measure integrability, integral comparison and scalar squeeze/continuity','C_c boundedness for an explicit source-class specialization'],
  bound_constant='Exactly2M; M must be nonnegative and quantify a bound on |f| for every phase. In the future header, quantify every valid M or choose/exhibit a single witness M internally before placing it in the estimate. M=0 and negative-valued tests cause no exception.',
  probability_warning='Never infer AS sample convergence from convergence in probability for direct ordinary samplewise DCT. Preferred defect integration avoids that inference; optional epsilon/delta event split is valid.',
  edge_cases=['rank0 singleton phase allowed','zero rate/cap/energy and infinity firstwait handled without cap division','zero raw waits and nonpositive exceptional inputs retained; actual per-parameter AE init gives expectation at0','half-open endpoint uses only strict pre-event equality','uncovered-z0 versus source failed-limit-zero labelled as representative adapter, no uniform parameter nullset','ordinary nonpunctured NNReal neighborhood0, fixed deterministic state/test only']),
 required_topology_overlay=info(O/'proposed-minimal-topology-overlay83.json'),overlay_canonical_sha256=hashlib.sha256(canon(overlay)).hexdigest(),
 overlay_separate_source_author_review_pending=True,original_extractor_artifacts_unchanged=True,
 normalized_parser_drift=dict(count=7,diagnostic=info(O/'normalized-anchor-negative83.json'),authority='Full exact pinned primary RAW and independently read source region; normalized citation-token hash mismatch is not a source mutation or proof conclusion.'),
 remaining_obligations=['Separate exact-overlay review before any Statement Seal','Future exact header and complete definition/binder review before proof','Actual integrability/2M estimate/expectation limit still unproved for83','Outer L2 state measurability and exact finite law/squared DCT; invariance/Jensen contractivity; C_c density/equivalence-class operators','Markov/restart/semigroup/reversal/path law/hypocoercivity/ideal-kernel invariance/implementation/error/cost/main/composition remain OPEN'],
 role_limits=dict(extractor_private_script_rationale_or_verdict_read=False,extractor_script_hashed_only=True,Lean83_or_header_read=False,Lean83_proof_search=False,StatementSeal=False,SAU_claim=False,VERIFIED=False,shared_state_mutation=False,source_final_BODY_acceptance=False)))
save('decision83.json',dict(status='PROSPECTIVE_BOUNDED_SCOPE_ACCEPTED_REQUIRED_TOPOLOGY_OVERLAY_PENDING_SEPARATE_REVIEW',reviewer_id='/root/exact_verify77',
 primary_RAW_sha256=info(Path(manifest['raw_inputs'][0]['path']))['RAW_sha256'],source_closed_manifest=info(mf),
 review=info(O/'topology-review83.json'),minimal_overlay=info(O/'proposed-minimal-topology-overlay83.json'),
 original_counts=[30,17,28],supplemented_counts=[30,17,30],
 new_mathematical_hypotheses_required=[],topology_repairs=['AND inside optional branch/OR between sufficient branches','E83-28 broad global boundary is association, not proof implication'],
 StatementSeal=False,proof_or_completion=False,VERIFIED=False,whole_goal=False))
for e in manifest['raw_inputs']+manifest['raw_outputs']:assert info(Path(e['path']))['RAW_sha256']==e['raw_sha256']
save('closed-RAW-manifest83.json',dict(status='CLOSED_NONCIRCULAR_INDEPENDENT_SOURCE_TOPOLOGY_REVIEW',reviewer_id='/root/exact_verify77',
 frozen_source_inputs=[info(mf)]+[info(Path(e['path'])) for e in manifest['raw_inputs']+manifest['raw_outputs']],
 owned_outputs=[info(p) for p in sorted(O.iterdir()) if p.is_file()],self_hash_excluded=True,
 dependencies='Manifest binds native review/decision/proposed overlay and independently read source pins. No artifact hashes this manifest. Frozen source originals are unchanged.',
 source_only=True,StatementSeal=False,proof=False,VERIFIED=False))
print(json.dumps({n:info(O/n)['RAW_sha256'] for n in ['decision83.json','topology-review83.json','proposed-minimal-topology-overlay83.json','closed-RAW-manifest83.json']},indent=2))
