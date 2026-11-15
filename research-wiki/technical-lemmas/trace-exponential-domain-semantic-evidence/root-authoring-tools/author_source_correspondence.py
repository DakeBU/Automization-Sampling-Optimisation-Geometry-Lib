from pathlib import Path
import hashlib, json

r=Path.cwd(); w=r/'.astis/huanjian-gc-trace-mgf-domain-20261115'
e=r/'research-wiki/technical-lemmas/trace-exponential-domain-semantic-evidence'
digest=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
P='AutoSamplingTheory.TechnicalLemmas.Analysis.MatrixTraceExponentialBounds.trace_exp_pos_and_le_card_mul_exp_abs_mul_norm'
T='AutoSamplingTheory.Tests.GaussianComplexityTraceMgfDomain.actual_source_four_trace_mgfs_integrable_positive_and_bounded'
R='AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumSourceMatrixRadius.actual_source_truncated_matrix_norm_bounds'
S='AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumSourceMatrixStructure.actual_source_centered_matrix_structure'
pf=r/'AutoSamplingTheory/TechnicalLemmas/Analysis/MatrixTraceExponentialBounds.lean'
tf=r/'Tests/GaussianComplexityTraceMgfDomain.lean'
assert digest(pf)=='1ef6f49fa5f0a8b3b61ba42d31bca1bb744bebb64e433075d0ca25ab82570b76'
assert digest(tf)=='72311555e65cacc8b129510f2158abc9e2e6a230882a2169f6504e80f394fedb'
sg=r/'.astis/semantic-neutral-20261115/trace_mgf_source_graph_4c71/phase1/source-proof-graph.json'
routes=sg.with_name('sufficient-or-routes.json')
nodes={n['id'] for n in json.loads(sg.read_text())['nodes']}
rows=[]
def row(ids, disposition, declaration, lines, explanation):
    assert set(ids)<=nodes
    rows.append(dict(source_nodes=ids,disposition=disposition,declaration=declaration,
        LF_lines_1based_inclusive=lines,explanation=explanation))
row(['T:2.1:p4','T:2.3:p1','T:2.3:eq2.1','T:2.3:p2','T:2.4:p1','T:2.4:series','T:2.4:p2'],
    'NEW_CANONICAL_BACKGROUND_INSTANCE_NOT_ENTIRE_PRINTED_COMPLEX_THEOREM',P,[18,37],
    'Finite nonempty REAL Hermitian matrix, ordinary unnormalized trace, actual Euclidean induced operator norm. Same-A continuous functional calculus identifies scalar exp(sx) with algebra power-series exp(sA), proves strict positive definiteness, then positive trace. Every real s, including zero/negative. These background conventions are reused from Mathlib, not independently re-proved as all of Tropp.')
row(['T:2.1:p4','T:2.3:p3','T:2.3:eq2.2','T:2.3:p4'],
    'NEW_CANONICAL_UPPER_ENVELOPE_FROM_SAME_OPERATOR_TRANSFER',P,[38,58],
    'For each actual spectral value x, |x|<=||A||op and sx<=|s|||A||op. Same-A CFC yields exp(sA)<=exp(|s|||A||op)I. The PSD difference has nonnegative trace, giving the exact card(I) factor. No arbitrary cross-matrix exponential operator monotonicity is used.')
row(['G:S4.Thmtheorem4.p1.1','G:S4.E11','G:S4.Ex12','G:A3.SS2.p1.1','G:A3.Ex85','G:A3.SS2.p1.2','G:A3.SS2.p10.1','G:A3.Ex107','G:A3.SS2.p13.1'],
    'LITERAL_PRIVATE_CONSUMER_DEFINITIONS_NO_NEW_PUBLIC_SOURCE_CREDIT',T,[21,52],
    'The sealed sole hq:2q+1<d and q=0 are retained. Full unconditional (q+1)-fold standard Gaussian law on (R^d)^(q+1); physical row i.val+1, Gaussian-first/feature-second Kronecker order, inclusive own-row cutoff <=L, true full-law Bochner mean, ordinary/cosine weights and two independent global-sign cases. A let defining EY does not prove its closed formula.')
row(['G:A3.Ex111'], 'REUSE_EXISTING_CANONICAL_Y_AND_TRUE_MEAN_NORM_BOUNDS',R,[106,110],
    'T calls R with hq and aligns its literal Y and true full-law mean. Existing bounds ||Yi||<=2rL/d and ||EY_i||<=2r/d supply the two inputs. These are Ex111, not the centered bound Ex112; no duplicate theorem or renewed old credit.')
row(['G:A3.SS2.p13.1','G:A3.SS2.p13.2','G:A3.Ex112','G:A3.SS2.p13.3'],
    'ABSORBED_BOOKKEEPING_IN_PRIVATE_CONSUMER',T,[111,136],
    'norm_sub derives ||Zi||<=Rstar=2r(L+1)/d; |cos|<=1, norm(global sign)=1 and finite-sum triangle give ||S||<=d Rstar. Canonical Structure supplies actual Zi measurability and Hermitian values; unneeded independence/centering outputs are discarded. No source proof ingredient is an added public binder.')
row(['GAP:trace-domain','T:3.1:p2:caveat'],
    'LOCAL_COMPILED_NARROW_SCALAR_DOMAIN_OUTPUT_SOURCE_REVIEW_PENDING',T,[137,181],
    'P materially supplies 0<tr exp(sS)<=r^2 exp(|s|dRstar) pointwise for all s/four Boolean cases. Scalar Integrable and 0<ordinary integral<=same finite cap are emitted. Exact dimension r^2; no normalized trace, full matrix-valued MGF, equality of signed laws, or sharp tail result.')
row(['GAP:measurability','T:2.2:p1'],
    'REUSED_REGULARITY_PLUS_INTERNAL_SCALAR_CONTINUITY_AND_DOMINATION',T,[98,105,127,136,161,181],
    'Canonical Structure supplies measurable Zi and Hermitian Zi. Internal finite sums give measurable S; analytic matrix exponential and continuous ordinary trace give measurable scalar f. Bounded domination on a probability law gives Integrable f. Pointwise positivity makes support f=univ, with probability mass1 giving positive ordinary integral. No positive uniform lower envelope is needed or emitted, and no separate public Measurable/matrix-MGF leaf is credited.')
row(['T:2.4:p3','T:2.4:eq2.5','T:2.4:Pet94'],
    'SOURCE_CONTEXT_NOT_IMPLEMENTED_NOT_REQUIRED_BY_ACTUAL_ROUTE','',[],
    'Global trace-exponential convexity/Loewner monotonicity and the Petz citation remain background context. The implementation proves its scalar cap using SAME-A CFC then PSD trace_nonneg, not these full general claims. A source-graph NODE is not automatically a closed Lean node.')
row(['GAP:Bernstein-external','G:matrix-Bernstein-name','G:A3.SS2.p15.1','G:A3.Ex121','G:A3.SS2.p15.2'],
    'DOWNSTREAM_OPEN', '', [],
    'No independent-sum matrix MGF, Lieb/Jensen/Golden-Thompson, master-tail/Bernstein rate or norm tail is proved. Ex121->p15.2 is a source continuation repeating the concentration application for the weighted sequence, not an implication from ordinary-tail to weighted-tail or a signed-law symmetry.')
obj={
 'schema_version':1,'kind':'root-authored-source-to-Lean-correspondence',
 'state':'LOCAL_MATHEMATICS_COMPILED_INDEPENDENT_SOURCE_REVIEW_PENDING',
 'candidate_commit':'30172847ec40c24426f0b39afc4887719810eca0',
 'scope':'One canonical real deterministic P plus one private material literal Gaussian consumer T; no extra public T publication edge.',
 'files':[{'path':str(p.relative_to(r)),'sha256':digest(p)} for p in [pf,tf]],
 'source_graph_original':{'file':str(sg.relative_to(r)),'sha256':digest(sg),'unchanged':True},
 'source_routes_original':{'file':str(routes.relative_to(r)),'sha256':digest(routes),'unchanged':True},
 'correspondence':rows,
 'actual_compiled_value_parents':{'P':[],'private_T':[P,R,S],
    'authority':'Independent native report51481e488bee3d6de641a61a5dced0bd9bfaa6f7666e64d5c36595f3b0c5c1ca; [] means no external ASTIS value parents, not no Mathlib dependencies.'},
 'route_refinement':{
    'OR_A':'Only its same-operator spectral/CFC upper-envelope component is implemented. The stronger m exp(-|s|K) lower envelope in the frozen sufficient-route proposal is NOT EMITTED, NOT CLAIMED proved, and not needed for sealed P/T.',
    'OR_B':'Exp-series operator-norm upper alternative NOT implemented. A bounded library search did not provide the needed generic API; no mathematical refutation is claimed.',
    'actual_sufficient_route':'CFC positive definiteness + same-A CFC upper bound; exact N-scaled ordinary trace; internal scalar continuity/measurability + bounded domination; support=univ and probability mass1 for positive ordinary integral.',
    'preservation':'No source graph or old route proposal is rewritten to match the implementation. This separate authored refinement is subject to independent fresh review.'},
 'proof_digestion':{
    'existing_substrate':['Mathlib CFC/order/trace/analytic-exponential/integral APIs',R,S],
    'bookkeeping':'Literal experiment alignment, radius subtraction, finite weighted signed sum cap, r^2 cardinality, probability normalization and scalar domination stay inside private T.',
    'new_reusable':[P],
    'new_topology':'Material application of P to four literal full-law Gaussian sums closes their narrow scalar trace-exponential domain, not a new concentration architecture.',
    'canonicality':'Bounded local search found only P itself and its T use for this exact all-real strict-positive trace envelope; old trace-exp-sum/Laplace/single-matrix MGF results are reused unchanged, not wrapped or recounted.'},
 'purification':{'status':'pending','reason':'Whole-module/source/reader review, normal PL/V, shared integration and post-merge purification are separate remaining gates. No PURIFIED/Exposition Seal claimed.',
    'reader_default':'Short envelope statement/formula; assumptions, mathematical steps and exact adjacent P/T Lean folded in layers. All243 lines remain drill-down evidence.'},
 'global_boundary':'Two full Gaussian lower bounds, oracle/TV/precision/dimension/condition-number/deterministic worst-query cap and explicit expected-cost adaptations, shared Registry/sourceIndex/graph/site/main integration and final acceptance remain open; no Goal completion.'}
out=e/'source-to-lean.correspondence.authored-v1.json';assert not out.exists()
out.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'file':str(out.relative_to(r)),'sha256':digest(out),'source_graph_unchanged':True,'normal_PL_calls':0,'normal_V_calls':0}))
