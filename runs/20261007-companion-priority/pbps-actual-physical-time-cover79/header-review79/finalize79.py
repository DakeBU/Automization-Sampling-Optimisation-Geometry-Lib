from pathlib import Path
import json,hashlib,datetime
R=Path('E:/Samplinglib');B=R/'runs/20261007-companion-priority/pbps-actual-physical-time-cover79';O=B/'header-review79';S=R/'runs/20261007-companion-priority/pbps-physical-time-preread79'
def info(p):
 b=p.read_bytes();return dict(path=str(p),RAW_bytes=len(b),RAW_sha256=hashlib.sha256(b).hexdigest())
def load(p):return json.loads(p.read_text(encoding='utf-8'))
def save(n,v):
 p=O/n;assert not p.exists();p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
assert load(O/'typecheck.receipt.json')['exit_code']==0
H=B/'header79.proposed.lean';assert info(H)['RAW_sha256']=='4b3b12a9e83195cfca5c02466b51f838b0e175fad23a9665ab32df7553968a1a'
boundary='Prospective header/mathematics and distinct source-topology review only. No theorem BODY/proof search/implementation, blind decoding, final compiled source review, VERIFIED transition, stabilization or Goal credit.'
math=dict(status='ACCEPTED_PROSPECTIVE_HEADER_MATHEMATICS79',reviewer='/root/exact_verify77',header=info(H),
 compiler=info(O/'typecheck.receipt.json'),signature_definition_readback=info(O/'signature-definition-readback79.json'),
 conclusions=['For each fixed y,xRef,z0, on one AE actual-input event, every finite t lies in exactly one half-open event interval.',
 'Every covering interval has exactly one actual live stored record with stored time<=t and finite nonnegative elapsed<toward actual next wait.'],
 mathematical_audit=[
 {'case':'objects and binders','finding':'All six source analytic hypotheses retained, including alpha/upper eta standing context; no cap/positive-energy/nonexplosion/index/clock/support/measurability provider introduced. Eleven definitions byte-identical to parent78; nine deterministic recurrence definitions byte-identical to parent76.'},
 {'case':'AE order','finding':'For each fixed deterministic parameter triple, actual78 supplies a common AE event for all finite horizons. The quantifier order does not require an uncountable intersection over data or times.'},
 {'case':'existence and uniqueness of interval','finding':'Initialized monotone extended clocks and finite-horizon escape give a finite nonempty initial active-index set. Its maximal index has Tn<=t<T(n+1). Two such half-open intervals cannot overlap by monotonicity. Zero-length intervals are empty; strict positive waits are not a necessary added hypothesis.'},
 {'case':'finite live record','finding':'Tn<=finite t excludes the stopped Sum.inr case since its eventTime is top. Thus actual record is Sum.inl a, whose time is Tn. Uniqueness of a follows from the functional stored record and injectivity of Sum.inl, without a selected-state provider.'},
 {'case':'finite next waiting time','finding':'Guarded next/record recurrence makes next clock a.time+wait when wait is finite. The strict upper interval inequality and a.time<=t imply the NNReal elapsed t-a.time is strictly less than this wait; subtraction does not conceal a negative elapsed duration.'},
 {'case':'infinite next waiting time','finding':'The next record is stopped with top clock. The currently selected a remains live and supplies every finite elapsed offset on the final unbounded arc. No phase at top and no untopD0 of an infinite elapsed time is introduced.'},
 {'case':'endpoint and initialization','finding':'A finite jump endpoint is excluded from the old interval and belongs to its next nonempty half-open interval. On source positive-threshold event it is the immediate postbounce state. Header asserts interval/live-record coverage, not an explicit n(t0)=0 or global Phi0 interpolation value. Such stronger initialization claims would require internally derived input support, not another premise.'},
 {'case':'rank0/cap0','finding':'Zero dimensional/zero-energy data retained. Parent78 cap0 branch leaves initial live record and next time top; that initial interval covers all finite t. No division by positive cap occurs in this target.'},
 {'case':'exceptional samples','finding':'Clamped nonpositive coordinates define legitimate total inputs but can produce zero waits. No all-sample source claim is made. The header AE coverage does not assert strict waits or n(t0)=0 on exceptional inputs.'},
 {'case':'bounded target','finding':'No global state X(t,sample), measurable selector, path regularity/adaptedness, Markov, invariance, kernel, expectation/query cost or full process uniqueness result is claimed.'}],
 no_mathematical_or_syntax_repair_needed=True,proposals=[],warnings='Unused-hypothesis lints on private Prop are expected: the source standing hypotheses are retained as declaration binders while the literal specification body uses V/eta. They are not authorization to remove source assumptions.',
 proof_route_only_as_mathematical_review=True,proof_search=False,production_edits=False,boundary=boundary)
save('header-math-review79.json',math)
freeze=load(S/'source-freeze79.json');nodes=freeze['source_graph']['nodes']
core={'standing','center-residual','flow','bounce','rate-hazard','input-initialization','finite-jump-recursion','stopping','arc-interpolation','nonaccumulation-parent','physical-time-globality','finite-active-set','unique-covering-index','live-state-at-index','elapsed-offset','stopped-last-arc'}
future={'positive-finite-waits','endpoint-selection','pathwise-uniqueness','measurable-active-index','measurable-interpolation','good-event-representative','path-regularity'}
coverage=[]
for n in nodes:
 k=n['id'];assert k in core or k in future or n['disposition']=='EXCLUDED',k
 coverage.append(dict(extractor_node=k,source_disposition=n['disposition'],independent_review='retained scoped source or source-implicit adapter' if k in core else 'retained later obligation; no current header completion credit' if k in future else 'exclusion independently agrees with source scope',anchor=n['anchor']))
overlay=dict(status='REVIEWER_TOPOLOGY_CLARIFICATIONS_NO_SOURCE_OR_HEADER_MUTATION',reviewer='/root/exact_verify77',source_freeze=info(S/'source-freeze79.json'),
 direct_definition_edges=[dict(parents=['center-residual'],consumer='flow',kind='source-definition-ingredient',anchor='S3.E4 -> A1.Ex2'),
 dict(parents=['center-residual'],consumer='bounce',kind='source-definition-ingredient',anchor='S3.E4 -> A1.Ex3'),
 dict(parents=['center-residual'],consumer='rate-hazard',kind='source-definition-ingredient',anchor='S3.E4 -> A1.Ex1/S3.E9')],
 scope_clarifications=[
 'The physical-time-globality source node names the broader source assertion. Candidate79 closes only unique-covering-index/live-state-at-index/elapsed-offset/stopped-last-arc bookkeeping, not the full source process node.',
 'Positive-finite-waits remains a distinct support/hazard bridge. It is unnecessary for unique half-open interval selection from monotone escaping clocks, but is needed if endpoint-selection is strengthened to n(0)=0 and immediate postbounce indexing at every endpoint. Add positive-finite-waits -> endpoint-selection for that later stronger claim.',
 'Pathwise phase-value uniqueness is a later explicit interpolation consumer of the unique record and finite elapsed duration; candidate79 does not define a phase process or certify Phi0 endpoints.',
 'The finite-active-set/max route and the first-escaping-index route are equivalent elementary adapters. Neither adds a public premise or proves source strict positivity.',
 'Stopped and continuing paths are OR cases; cap0 is a stopped special case. Author direct Exp mean1-SLLN and verified indicator-SLLN remain sufficient OR alternatives upstream.'],
 necessary_header_repairs=[],frozen_extractor_not_modified=True)
save('reviewer-source-topology-overlay79.json',overlay)
review=dict(status='ACCEPTED_DISTINCT_SCOPED_SOURCE_TOPOLOGY79_WITH_EXPLICIT_REVIEWER_OVERLAY',reviewer='/root/exact_verify77',extractor='/root/source_review77',
 primary=info(R/'runs/20261007-companion-priority/phase-pbps-gamma-preread57/primary-pbps.exactraw.snapshot.html'),
 independent_preheader_graph=info(O/'independent-source-topology-before-header79.json'),primary_first_read=info(O/'primary-first-read79.json'),
 extractor_freeze=info(S/'source-freeze79.json'),bounded_capsule=info(S/'bounded-capsule79.json'),native_primary_range_validation=info(O/'extractor-range-readback79.json'),
 coverage=coverage,coverage_count=len(coverage),missing_required_scoped_source_nodes=[],source_error_found=False,
 reviewer_overlay=info(O/'reviewer-source-topology-overlay79.json'),
 chronological_independence='Exact primary regions reread and own topology written before candidate/extractor reads; parent76/78 statement-only extracts inspected after source topology. Parent proofs had been reviewed in earlier tasks, but were not consulted or used to choose this source graph.',
 proof_BODY_used=False,creator_self_approval=False,header_mathematics_separate=info(O/'header-math-review79.json'),boundary=boundary)
save('independent-source-topology-review79.json',review)
save('prospective-review-manifest79.json',dict(status='ACCEPTED_PROSPECTIVE_ONLY',reviewer='/root/exact_verify77',created_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
 header=info(H),math_review=info(O/'header-math-review79.json'),source_topology_review=info(O/'independent-source-topology-review79.json'),
 source_topology_overlay=info(O/'reviewer-source-topology-overlay79.json'),typecheck_receipt=info(O/'typecheck.receipt.json'),
 outputs=[info(p) for p in sorted(O.iterdir()) if p.is_file()],no_immutable_inputs_changed=True,production_edits=False,proof_credit=False,boundary=boundary))
for n in ['header-math-review79.json','independent-source-topology-review79.json','reviewer-source-topology-overlay79.json','prospective-review-manifest79.json']:
 print(n,info(O/n)['RAW_sha256'])
