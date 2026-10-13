"""Independent source reviewer81: close native noncircular evidence, without shared writes."""
import hashlib
import json
import pathlib
from datetime import datetime, timezone

ROOT = pathlib.Path('E:/Samplinglib')
OWN = ROOT / 'runs/20261007-companion-priority/pbps-actual-physical-time-law81/fresh-source81'
PRE = ROOT / 'runs/20261007-companion-priority/pbps-physical-time-law-preread81'
PACKET = OWN.parent / 'source-review81.packet.json'
MODULE = ROOT / 'AutoSamplingTheory/ExampleCases/ProximalBPS/IdealHalfTurnKernel.lean'
LESSON = ROOT / 'website/content/declaration_lessons/pbps-ideal-half-turn-kernel.json'
PRIMARY = ROOT / 'runs/20261007-companion-priority/phase-pbps-gamma-preread57/primary-pbps.exactraw.snapshot.html'
CANON = '345c5f2ae584f6aaf5ed9cfb0940cbc67c4855a6138eb0ef99b6c3ab1bf5c66b'
MODHASH = '5b3d639fbc49e06715ae8f768d5a5c714b7844dc20c5e5a8a16cb564e823df2f'
PUBHASH = '7f5a864122254a7e0a425edf37e8d68597b161492edb419507199bb24baf29d8'

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def load(p):
    return json.loads(p.read_text(encoding='utf8'))

def binding(p):
    return {'path': p.as_posix(), 'raw_sha256': sha(p), 'bytes': p.stat().st_size}

def write(name, obj):
    p = OWN / name
    assert not p.exists(), 'Closed outputs must not be overwritten: ' + name
    p.write_bytes((json.dumps(obj, ensure_ascii=False, indent=2) + '\n').encode('utf8'))
    return p

# Recheck pre-candidate source inventory, graph, additive scope clarification and chronology.
manifest = load(PRE / 'source_freeze81.complete-raw-manifest.json')
assert sha(PRIMARY) == 'd81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760'
for row in manifest['raw_inputs'] + manifest['raw_outputs']:
    assert sha(pathlib.Path(row['path'])) == row['raw_sha256'], row['path']
assert sha(PRE / 'source_freeze81.complete-raw-manifest.json') == '37eac290b63a76e10cba820d1f29a6e1da7b0f4fbd5ca4041769817993fdaca1'
inventory = load(PRE / 'source_inventory81.json')
graph = load(PRE / 'source_proof_graph81.json')
assert (len(inventory['scope_coverage']), len(graph['nodes']), len(graph['edges'])) == (65, 15, 29)
readiness = load(OWN / 'source-review81.prepacket-readiness.json')
assert readiness['canonical_packet_seen'] is False
assert readiness['candidate_body_or_new_exposition_seen_this_final_review'] is False
assert sha(PRE / 'header-source-review81/header-source-review81.result.json') == 'd9a6ee69fbffddd5404509999fe381b424b04e87154e9ace32c73ca440c81d1e'
assert sha(PRE / 'header-source-review81/header-source-review81.raw-manifest.json') == 'fb1e878b4f35c7b146446e446dd4b4807f21df6cb6705e5114852075d0daa971'

packet = load(PACKET)
canonical_payload = {k: v for k, v in packet.items() if k != 'packet_sha256'}
assert hashlib.sha256(json.dumps(canonical_payload, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()).hexdigest() == CANON
assert packet['packet_sha256'] == CANON
assert packet['publication_binding_sha256'] == PUBHASH
assert sha(MODULE) == MODHASH
assert MODULE.read_bytes() == packet['candidate_publication_context']['current_lean_module'].encode('utf8')
unit = load(LESSON)['units'][0]
context_lesson = packet['candidate_publication_context']['lesson']
assert {k: v for k, v in unit.items() if k != 'boundary'} == context_lesson

step_findings = [
    'Literal c/Phi/S/rate/Lambda/tau/next/record/eventTime are retained; exact q_y, unscaled standard Gaussian and actual iid Exp product are internal lets, never supplied law certificates.',
    'Actual80 produces one joint Borel Z with deterministic covered/fallback and per-fixedparameter AE allfinite/init properties. GibbsAugmentation proves positive Bochner integral exp(-V), hence L1 by integral-undef semantics; mu is genuine probability.',
    'GaussianConditionalKernel constructs everywhere probability R from derived mu. tilted_tilted hi gives literal volume tilt -V-quadratic, including exact normalization. q_y cannot exploit the nonintegrable zero branch.',
    'Pullback of R by y and constant gamma/P product kernels has exactly M_y as fiber. This proves actual joint parameter dependence and independent fresh input law.',
    'F uses actual Z at finite pi and first coordinate; joint Borel composition and kernel map construct probability H. Dirac-product/map-map establish actual fiber pushforward, beyond a wrapper with supplied output measurability.',
    'Actual76 record/time measurability, Actual73 Phi measurability, Actual77 tau measurability and measurable threshold clamp are retrieved with all six source conditions. Tuple projections match current private Props.',
    'L_n is a total measurable record projection; live-record predicate is preimage of range inl, so its dummy stopped branch cannot witness a physical source phase. Actual Z/tau/Phi compositions and finite elapsed are Borel.',
    'D_n includes both half-open clock inequalities, live equality, stored time <= pi, elapsed < tau and actual phase equality. G is init intersect countable union D_n, a Borel event; no uncountable intersection or existential over arbitrary phase records remains.',
    'ae_prod_iff_ae_ae applies only after hGM. For every fixed r,p, inherited hAE supplies init and terminal arc; L_n=a follows by record elimination. Fubini lifts to M_y common AE at 0 and pi only, then reconstructs the actual live witness.',
    'hgood gives AE initialization equality. map_congr, probability product marginal and Dirac-product/map identities derive phase0 law delta_x tensor gamma. The final result retains all Z/R/H clauses and does not assert random alltime path or process Markovness.'
]
lines = MODULE.read_bytes().splitlines(keepends=True)
regions = []
seen = set()
overlaps = []
for i, step in enumerate(unit['steps'], 1):
    r = step['lean_source_region']
    a, b = r['start_line'], r['end_line']
    code = b''.join(lines[a-1:b])
    assert code.decode('utf8') == step['lean']
    assert hashlib.sha256(code).hexdigest() == r['exact_code_raw_sha256']
    assert r['source_raw_sha256'] == MODHASH
    for n in range(a, b+1):
        if n in seen:
            overlaps.append(n)
        seen.add(n)
    regions.append({'step': i, 'title': step['title'], 'start_line': a, 'end_line': b,
                    'exact_code_raw_sha256': r['exact_code_raw_sha256'],
                    'formula_reviewed': True, 'prose_reviewed': True, 'body_reviewed': True,
                    'formula_body_exact_match': True, 'semantic_finding': step_findings[i-1]})
assert len(regions) == 10
gaps = sorted(set(range(110, 311)) - seen)
assert not gaps and not overlaps

semantic_slots = {
 'objects': {'relation': 'explicit-elaboration', 'source': 'Actual fixed-reference harmonic flow, residual reflection/rate, hazard hit recurrence, iid Exp1 clocks; exact conditional q_y and independent Gaussian momentum; returned-position H_y.', 'lean': 'Literal dynamics and actual80 Z, exact normalized volume tilt q_y, constructed R, M_y=(q_y×gamma)×P, actual returned-position H; private Prop and BODY agree.', 'blind': 'Reconstructs these exact objects and their source roles; does not replace q_y with q-hat or output with an arbitrary supplied observable.', 'assessment': 'Faithful ideal law integration; source A1.SS2.p4.1 explicitly averages actual terminal indicator over these inputs.'},
 'domains': {'relation': 'explicit-elaboration', 'source': 'Euclidean finite dimension with Borel sets, real positive eta, finite nonnegative physical time; extended waiting time for empty hit.', 'lean': 'FiniteDimensional real inner product Borel E; NNReal finite times and WithTop NNReal waits; E×E phases and countable real clock samples, measurable clamp.', 'blind': 'Identifies rank0 allowance, finite time versus top wait, stopped Sum record and no phase at infinity.', 'assessment': 'Intrinsic finite-dimensional coding preserves Euclidean source, with harmless rank0 extension and canonical volume/Gaussian. No positive dimension added.'},
 'quantifiers': {'relation': 'explicit-elaboration', 'source': 'Fixed V,alpha,beta,eta; fixed source y,r,z0 construction, independent random initialization and exact terminal law.', 'lean': 'One joint Borel Z; all deterministic covered/fallback clauses on raw samples; each fixed y,r,z0 has a common clock-AE event for all finite t plus init. For each fixed y,x, independent M_y has common AE init0 and pi live arc. Exists R,H with everywhere fibers.', 'blind': 'Correctly distinguishes per-fixedparam AEalltime from product AE{0,pi}, excludes uniformparams and arbitrary correlated substitution.', 'assessment': 'Measurable countable good predicate and Fubini prove exactly bounded lift. Full random allfinite law and separately quantified representative uniqueness remain OPEN.'},
 'assumptions': {'relation': 'equivalent', 'source': 'V C2, 0<alpha<=beta, alpha I<=HessV<=beta I and 0<eta<=1/beta.', 'lean': 'Six binders hα,hαβ,hV,hH,hη,hβη retain exact conditions; Gaussian/reference/clock normalization, independence, measurability, cap and nonaccumulation are constructed or consumed from actual parents.', 'blind': 'Lists all six; positivity/probability/measurability are derived, not hidden inputs.', 'assessment': 'No extra integrability, minimizer, moment, kernel, phase, energy or law certificate binder. eta scale beta*eta<=1 equivalent because beta>0 follows alpha>0<=beta.'},
 'conclusion': {'relation': 'explicit-elaboration', 'source': 'Source A1.SS2.p3.1-p4.1 gives Borel actual terminal representative and jointly Borel H_y(x,A) by averaging exact inputs; Algorithm1 ideal initialization and output.', 'lean': 'R_y=q_y probability kernel, H(y,x)=map actual first-coordinate Z_pi M_y probability kernel, phase0 law dirac x×gamma, product AE init and actual live pi arc; inherited full fixedparams Z properties retained.', 'blind': 'Accurately reconstructs the same law and initialization, no stationarity or sampler implementation conclusion.', 'assessment': 'Constructs a meaningful source law consumer beyond actual80; not merely restating supplied measurability. Subsumes source Borel fiber claim within strict bounded refinement.'},
 'scopes': {'relation': 'explicit-elaboration', 'source': 'Ideal exact-reference H_y law and Borel integration clauses selected from larger Algorithm1/Propositions3.1-3.2/Appendix A package.', 'lean': 'Bounded exact-reference returned law and initialization only; exception fallback z0, stopped auxiliary dummy and last-live infinite wait distinguished.', 'blind': 'Explicitly excludes process Markov/semigroup, invariance/reversal/L2, errors/cost, composition and alltime random law.', 'assessment': 'Full source results remain OPEN. Source zero-on-failed-limit versus ASTIS z0-on-uncovered totalization is harmless at used times after product-AE actual agreement. No general version-uniqueness theorem credited.'},
 'constant_dependencies': {'relation': 'equivalent', 'source': 'c=y-eta gradV(r); h=gradV(x)-gradV(r); flow sqrt eta and inverse sqrt eta; rate sqrt eta; q_y exponent -V-||r-y||²/(2eta); gamma N(0,I); Exp rate1; terminal pi.', 'lean': 'All literal scale, signs, denominators, distributions and terminal pi match. No stochastic cap or error/cost constants appear as supplied premises.', 'blind': 'Identifies exact normalizations, unscaled momentum, indexing coordinate0=E1 and finite terminal pi.', 'assessment': 'All scale dependencies retained; alpha/beta/eta source analytic context fixed, y/r/x/p clock variables correctly separated.'}
}

deltas = []
def delta(slot, classification, description):
    deltas.append({'id': 'D81-%02d' % (len(deltas)+1), 'slot': slot, 'classification': classification, 'blocking': False, 'description': description})
delta('objects', 'notation-resolution', 'Canonical Exp product coordinate n realizes source E_(n+1); clamp is identity on a common positive-support event. Literal source dynamics are internal, not abstract providers.')
delta('domains', 'domain-clarification', 'Intrinsic finite-dimensional Borel E with canonical volume and standard Gaussian is Euclidean source coding; rank0 allowed without a positive-dimension premise.')
delta('quantifiers', 'source-implicit', 'Source independent initialization is made literal M_y. Measurable G at 0 and pi legitimizes Fubini; no uniform parameter null event or arbitrary correlated random initialization is inferred.')
delta('assumptions', 'notation-resolution', 'Six binders preserve C2/Hessian sandwich/positive ordered alpha,beta and eta in (0,1/beta]. Exact q normalization follows existing analytic parent plus conditional kernel theorem, not a new premise.')
delta('conclusion', 'explicit-elaboration', 'Source terminal indicator integration becomes constructed joint probability kernels R,H, actual H fiber formula, derived phase0 law and product-AE actual terminal witness.')
delta('scopes', 'admissible-bounded-refinement', 'Independent source graph G81-10 is realized only for product AE at 0/pi; inherited fixedparams AE allfinite remains. Full random alltime law OPEN. G81-14 source-law identification uses this chosen actual Z; separate universal version uniqueness OPEN.')
delta('scopes', 'formalization-convention', 'Source failed-limit zero convention differs from ASTIS uncovered z0; both are exceptional totalizations. Actual source arcs at used times hold product AE. Auxiliary stopped dummy is never live; infinite wait continues last live harmonic arc.')
delta('scopes', 'strict-source-boundary', 'H is the ideal exact-reference law using genuine q_y, not an implemented exact/approximate reference sampler. IsMarkovKernel means probability fibers only, not a proved phase Markov process or semigroup/invariance/reversibility/cost.')
delta('constant_dependencies', 'notation-resolution', 'sqrt eta flow/rate scaling, inverse sqrt eta, 2eta Gibbs denominator, unscaled N(0,I), Exp1 and terminal pi retained exactly.')
delta('scopes', 'publication-context-binding-elaboration', 'Canonical packet lesson omits only native boundary metadata. All remaining lesson fields are exactly equal; actual native boundary was separately read and RAW-bound and agrees with strict scope. No mathematical repair follows.')

# Exhaustive item coverage: every item of the independently frozen primary inventory is mapped.
def coverage_for(i):
    if i == 1:
        return 'PROVENANCE_ONLY', [], 'Pinned primary license recorded; paraphrases and minimal formulas only, no raw primary duplicated.'
    if i in (2, 3, 4):
        return 'COVERED_EXACT_BINDERS', [1,2,3,6], 'Private Prop and theorem keep all six source conditions; analytic normalization and dynamics consumers use these exact binders.'
    if i in (5,14,15,22,23,24,26,27,30,31,32,33,34,35):
        return 'COVERED_LITERAL_AND_PARENT', [1,6,7,8,9], 'Literal center/residual/harmonic flow/reflection/rate retained; actual73/76/77/80 supply true Borel/guard/arc APIs. Zero-normal reflection identity, not blanket bounce continuity.'
    if i == 6:
        return 'PARTIAL_NORMALIZATION_DEPENDENCY_REST_OPEN', [2,3], 'GibbsAugmentation used only for positive Gibbs normalizer; full augmented sampling law not a new81 conclusion.'
    if i == 7:
        return 'EXCLUDED_OPEN_AUGMENTATION_CONSUMER', [3], 'GaussianConditionalKernel theorem has conditional augmentation certificate, discarded here; random Y=X+sqrt eta G realization/composition not claimed by81.'
    if i in (8,10,11):
        return 'COVERED_EXACT_CONDITIONAL_DISTRIBUTION', [1,2,3,4], 'Exact normalized q_y=tilt_volume(-V-quadratic) derived via actual Gibbs probability and successive tilt, everywhere probability R_y=q_y; no q-hat.'
    if i in (9,13,18,19,21):
        return 'COVERED_INDEPENDENT_SOURCE_INITIALIZATION', [1,4,9,10], 'Arbitrary fixed x,y; independent reference q_y, standard Gaussian p, actual Exp clocks represented by literal product; phase0 equality and delta_x×gamma law derived.'
    if i in (12,16,20,53,54,55,56,64,65):
        return 'EXCLUDED_OPEN', [], 'Excluded source clause: invariance/generator/cost/Markov transition operator/adjoint/semigroup/path density/L2 contraction-selfadjointness as applicable; no implication from mass-one H is credited.'
    if i in (17,25,29,58,59,60,61,63):
        return 'COVERED_BOUNDED_IDEAL_OUTPUT_LAW_OTHER_CLAUSES_OPEN', [3,4,5,9,10], 'Actual source returned position at pi averaged over q_y,gamma,P; joint Borel probability H and init law constructed. Reversibility, L2 contraction, augmented composition and implemented reference sampling/cost remain OPEN.'
    if i == 28:
        return 'PARTIAL_ACTUAL_FINITE_PHASE_ONLY_REST_OPEN', [2,5,9], 'Actual80 supplies Borel finite phase and per-fixedparam nonaccumulation/initialization;81 constructs ideal terminal law. Source global uniqueness/time-homogeneous Markov/invariance remain OPEN.'
    if i in (36,37,38,39):
        return 'COVERED_ACTUAL_RECURRENCE_AND_ARCS', [1,2,6,7,8,9], 'Actual76/77/79/80 contracts match init index0, threshold E_(n+1), finite postbounce update, empty-hit top and stop, half-open interpolation. Infinite next wait leaves final live arc, no top phase.'
    if 40 <= i <= 51:
        return 'COVERED_INHERITED_NONACCUMULATION_INGREDIENT', [2,6,9], 'Actual76/78/79/80 consume exact energy/cap/wait/threshold-sum nonaccumulation ingredients. Positive cap division and zero cap no-finite-jump split preserved; energy/cap not supplied binders. No new81 reproving credit.'
    if i == 52:
        return 'PARTIAL_OR_ROUTE_NONACCUMULATION_MARKOV_OPEN', [2,3,9], 'Source direct Exp mean1 SLLN route not implemented here; actual UnitExponentialProduct uses positive-mean bounded-indicator SLLN sufficient alternative. It preserves actual law/sum divergence; memoryless Markov/Davis identification OPEN.'
    if i == 57:
        return 'PARTIAL_BOREL_BACKGROUND_OTHER_CLAUSES_OPEN', [6,7,8], 'Actual Borel finite flow/bounce composition consumed. Measure preservation/Jacobian/reversal/invariance not credited.'
    if i == 62:
        return 'COVERED_WITH_EXCEPTION_CONVENTION', [2,5,7,8,9], 'Actual80 total jointly Borel interval selection realizes source phase on covered arcs; source zero-on-failed-limit versus ASTIS z0-on-uncovered explicitly recorded. Product-AE agreement at0/pi established; universal version uniqueness excluded.'
    raise AssertionError(i)

item_coverage = []
for i, item in enumerate(inventory['scope_coverage'],1):
    status, steps, finding = coverage_for(i)
    item_coverage.append({'inventory_index': i, 'source_id': item['source_id'], 'frozen_scope': item['scope'],
                          'frozen_source_role': item['source_role'], 'status': status, 'steps': steps,
                          'finding': finding, 'blocking': False})

node_maps = {
1: ('COVERED', [1,2,3,6], 'Exact six analytic binders and intrinsic finite-dimensional Borel carrier.'),
2: ('COVERED', [2,3,4], 'Gibbs probability and GaussianConditionalKernel construct exact normalized R_y=q_y, not arbitrary kernel input.'),
3: ('COVERED', [1,3,4,10], 'stdGaussian E genuine probability, unscaled, rank0 point law allowed.'),
4: ('COVERED_PARENT_INPUT', [1,3,6], 'Canonical Exp1 infinitePi, measured clamp and actual coordinate laws; n=0 is source E1.'),
5: ('COVERED_PARENT_DYNAMICS', [1,6,7,8], 'Literal Phi/S/rate/Lambda/tau, actual73/76/77 measurability and finite guards.'),
6: ('COVERED_PARENT_RECURSION', [1,6,7,8,9], 'Actual76 initialized Sum records with guarded live update and absorbing top stop, joint Borel record/time.'),
7: ('COVERED_PARENT_WITH_ALTERNATIVE_ROUTE', [2,9], 'Actual80/79 inherit78 actual nonaccumulation; energy/cap split, indicator-SLLN sufficient alternative; last live infinite-wait tail preserved.'),
8: ('COVERED', [2,5,9], 'Actual80 internally produces one Z joint Borel, all deterministic covered/fallback properties and each-fixedparam common AE allfinite/init.'),
9: ('COVERED', [1,3,4,9,10], 'Literal independent q_y×gamma×P; initial phase(x,p), reference fixed throughout source recursion.'),
10: ('COVERED_BOUNDED_REFINEMENT', [6,7,8,9], 'G init intersect union_n D_n is Borel; Fubini gives common product AE at0/pi only. Alltime product law OPEN.'),
11: ('COVERED', [5], 'Actual F=pr1 Z(y,r,(x,p),pi,omega) joint Borel composition.'),
12: ('COVERED', [3,4,5], 'H=(Kernel.id×Q).map F, probability fiber and exact actual source indicator law.'),
13: ('COVERED_PHASE0_POSITION_MARGINAL_NOT_SEPARATE_THEOREM', [9,10], 'Derived phase0 delta_x×gamma. Position0 delta_x follows its first marginal, but no extra named position0 theorem credited.'),
14: ('COVERED_BOUNDED_IDENTIFICATION_VERSION_UNIQUENESS_OPEN', [5,9,10], 'Chosen actual Z agrees source live arc productAE atpi and source init at0; H is ideal exact-reference returned law. Separate universal version-equivalence theorem OPEN.'),
15: ('EXCLUDED_OPEN', [], 'No phase Markov/restart/semigroup/invariance/reversibility/L2/cost/implementation/composition proof from kernel mass1.')
}
nodes = []
for i,node in enumerate(graph['nodes'],1):
    status, steps, finding = node_maps[i]
    nodes.append({'id':node['id'], 'source_ids':node['source_ids'], 'frozen_obligation':node['obligation'],
                  'status':status,'steps':steps,'finding':finding,'blocking':False})
edges = []
for i,e in enumerate(graph['edges'],1):
    a,b=int(e['ingredient'][-2:]),int(e['consumer'][-2:])
    target = node_maps[b]
    status = 'EXCLUDED_OPEN_FUTURE_SUBSTRATE_NOT_IMPLICATION' if b == 15 else target[0]
    refinement = (' Countable terminal predicate replaces prospective alltime/rational-horizon relation; full alltime mixture OPEN.' if b == 10 and a == 6 else
                  ' Separate version uniqueness OPEN; chosen actual Z source agreement at used times suffices.' if b == 14 else '')
    edges.append({'id':'E81-%02d'%i,'ingredient':e['ingredient'],'consumer':e['consumer'],
                  'frozen_reason':e['reason'],'frozen_kind':e['kind'],'status':status,
                  'steps':target[1], 'finding':target[2]+refinement,'blocking':False})

independence = {
 'reviewer':'/root/fresh_source78', 'role':'independent anti-anchored source reviewer81',
 'proving_worker':False, 'source_first':True,
 'source_first_created_utc':inventory['created_utc'],
 'source_freeze_verified_before_candidate_body':True,
 'source_freeze_original_bytes_unchanged':True,
 'source_inventory_items':65,'source_graph_nodes':15,'source_graph_edges':29,
 'prepacket_readiness':binding(OWN/'source-review81.prepacket-readiness.json'),
 'allowed_prior_scope':'Own source-only freeze and own header-source bounded refinement only; no prior result used as evidence of current proof.',
 'prohibited_materials_read':[],
 'not_read':['other reviewers math/source/header-math verdicts','root adoption reports','prior source extractors','prior78-80 source-review verdicts'],
 'candidate_and_blind_treated_as_untrusted_claims':True,
 'no_production_or_shared_writes':True,
 'no_proof_compiler_or_VERIFIED_transition_credit':True
}

input_paths = [PRIMARY, PACKET, MODULE, LESSON, ROOT/'lean-toolchain', ROOT/'lake-manifest.json']
input_paths += [PRE / pathlib.Path(row['path']).name for row in manifest['raw_outputs']]
input_paths += [PRE/'source_freeze81.complete-raw-manifest.json',
                PRE/'header-source-review81/header-source-review81.result.json',
                PRE/'header-source-review81/header-source-review81.raw-manifest.json']
parent_names=['ActualHarmonicFlow','ActualFiniteJumpRecursion','ActualHazardClock','ActualNonaccumulation','ActualPhysicalTimeCover','ActualPhysicalTimeMeasurability','GibbsAugmentation']
input_paths += [ROOT/f'AutoSamplingTheory/ExampleCases/ProximalBPS/{n}.lean' for n in parent_names]
input_paths += [ROOT/f'AutoSamplingTheory/TechnicalLemmas/Probability/{n}.lean' for n in ['GaussianConditionalKernel','UnitExponentialProduct']]
input_paths += [ROOT / ('.lake/packages/mathlib/Mathlib/'+n) for n in ['MeasureTheory/Measure/Tilted.lean','MeasureTheory/Measure/Prod.lean','Probability/Kernel/Defs.lean','Probability/Distributions/Gaussian/Multivariate.lean']]
raw_inputs = [binding(p) for p in dict.fromkeys(input_paths)]
coverage = {'inventory_expected':65,'inventory_reviewed':65,'inventory_items':item_coverage,
            'nodes_expected':15,'nodes_reviewed':15,'nodes':nodes,
            'edges_expected':29,'edges_reviewed':29,'edges':edges,
            'unmapped_inventory_items':[],'unmapped_nodes':[],'unmapped_edges':[],
            'scope_refinements':['G81-10 product AE0/pi only; random alltime OPEN','G81-14 chosen actual representative; separately quantified version uniqueness OPEN'],
            'topology_verdict':'Every frozen source ingredient mapped to exact local/inherited body consumer or explicit exclusion; no excluded global edge silently counted as proved.'}
authored = {'expected_steps':10,'reviewed_steps':10,'body_start_line':110,'body_end_line':310,
            'gaps':gaps,'overlaps':overlaps,'formula_body_exact_matches':10,'steps':regions,
            'full_module_including_literal_private_prop_reviewed':True,
            'remaining_module_lines':'Imports/namespace/options and complete private statement/theorem binders plus closing end lines read; no omitted mathematical BODY region.',
            'native_lesson_packet_comparison':'All fields equal after excluding only native boundary metadata, separately audited and RAW-bound.'}
truthboundary = {
 'accepted':'Bounded ideal exact-reference actual returned-position joint probability kernel H at pi, exact q_y probability R, independent product input and derived phase0 law with product AE source initialization/terminal live arc; actual80 fixedparams phase semantics retained.',
 'source_facts':['Source six standing analytic conditions','Literal actual recurrence/half-open harmonic arcs','Exact q_y and independent Gaussian/reference inputs','Source A1.SS2.p4.1 exact terminal indicator integration'],
 'astis_adapters':['Intrinsic finite-dimensional Borel carrier/rank0','Canonical actual Exp product indexing/clamp','Sum stopped records and NNReal finite elapsed','Actual80 Borel countable interval selection with z0 exceptional fallback','Explicit independent M_y, countable Borel terminal good event and Fubini','Typed R/H probability kernels derived via genuine Gibbs normalization'],
 'inherited_parent_route':'UnitExp bounded-indicator SLLN is a sufficient alternative to source direct Exp mean1 SLLN; the latter remains an open alternative, not a new81 claim.',
 'open':['Full source Proposition3.1 unique time-homogeneous Markov process','Filtration/adaptedness/stopping-time/restart/strong Markov and semigroup','Full arbitrary-correlated or alltime random initialization/path law','Separate universal version uniqueness','Invariance/stationarity/reversibility/L2/adjoint/strong continuity/hypocoercivity','Implemented exact or approximate reference sampler and Algorithm1 query/error/cost','Augmented/reflection/composition/main theorem/full Goal','Reader visual/main/PURIFIED/live publication completion'],
 'exception_checks':{'rank0':'Allowed; standard Gaussian empty basis is point law, rate zero and infinite first wait do not break kernel or initialization.',
                     'zero_wait':'Deterministic zero thresholds yield empty half-open intervals and postbounce records; actual Exp thresholds positive simultaneously AE, enabling initialization at first live interval.',
                     'infinite_wait':'Last live current record persists for every finite elapsed; next stopped record at top is not evaluated as a phase.',
                     'dummy':'L_n zero dummy is measurability helper; explicit live equality excludes it from physical witness.',
                     'exceptional':'z0 fallback only uncovered sample-time points; used physical0/pi source agreement holds product AE, no uniformparams or correlated substitution.'}
}

evidence = write('source-review.run-evidence81.json', {
 'schema':'independent-source-review-run-evidence-v1','created_utc':datetime.now(timezone.utc).isoformat(),
 'status':'closed-source-comparison','reviewer_packet_sha256':CANON,'publication_binding_sha256':PUBHASH,
 'full_module_sha256':MODHASH,'raw_inputs':raw_inputs,
 'prepacket_readiness':binding(OWN/'source-review81.prepacket-readiness.json'),
 'independence':independence,'authored_step_coverage':authored,
 'source_coverage_counts':{'inventory':65,'nodes':15,'edges':29},
 'source_binding_and_parent_semantics_checked':True,
 'noncircular_rule':'Evidence contains neither its own digest nor result/final-manifest digest. Result binds this file RAW; manifest binds both and omits only its own hash.',
 'compiler_status':'Source review inspected exact BODY and typing APIs; root supplied focused compiler PASS is not independent compiler execution or verification credit from this reviewer.'})
result = write('source-review.result81.json', {
 'schema_version':1,'task':'PBPS actual ideal half-turn physical-time returned law81',
 'reviewer':'/root/fresh_source78','verdict':'equivalent-after-elaboration',
 'verdict_reason':'Full exact module and ten authored formula/prose/BODY regions faithfully construct the bounded ideal exact-reference source law and independent initialization. No blocking source/mathematical mismatch found; excluded source global obligations remain OPEN.',
 'reviewer_packet_sha256':CANON,'reviewer_packet_raw_sha256':sha(PACKET),
 'publication_binding_sha256':PUBHASH,'full_module_sha256':MODHASH,
 'review_run_sha256':sha(evidence),'review_run_path':evidence.as_posix(),
 'semantic_slots':semantic_slots,'deltas':deltas,'blocking_deltas':[],
 'repairs':[],'no_required_mathematical_repairs':True,
 'authored_step_coverage':authored,'source_graph_coverage':coverage,
 'independence':independence,'truthboundary':truthboundary,
 'review_scope':'Independent source fidelity and actual exposition/BODY topology; no compiler rerun, proving-worker selfverification, state transition or whole-source theorem completion.',
 'publication_binding_audit':{'canonical_packet_checked':True,'current_module_equals_packet_exact_utf8':True,
                            'native_lesson_core_equals_packet':True,'native_boundary_separately_audited':True,
                            'raw_native_lesson':binding(LESSON)}})
outputs=[OWN/'source-review81.prepacket-readiness.json',pathlib.Path(__file__).resolve(),evidence,result]
finalmanifest = write('source-review.run-manifest81.json', {
 'schema':'independent-source-review-noncircular-raw-manifest-v1','status':'closed',
 'created_utc':datetime.now(timezone.utc).isoformat(),'reviewer':'/root/fresh_source78',
 'reviewer_packet_sha256':CANON,'publication_binding_sha256':PUBHASH,'full_module_sha256':MODHASH,
 'raw_inputs':raw_inputs,'raw_outputs':[binding(p)for p in outputs],
 'source_first_chronology':{'original_freeze':inventory['created_utc'],'original_freeze_manifest':binding(PRE/'source_freeze81.complete-raw-manifest.json'),
                            'prepacket':readiness['created_utc'],'original_frozen_bytes_unchanged':True},
 'self_hash_omitted':True,
 'noncircular_rule':'Manifest binds exact RAW inputs and all native owned outputs except itself; final manifest digest reported outside this file.'})
for row in raw_inputs + load(finalmanifest)['raw_outputs']:
    assert sha(pathlib.Path(row['path'])) == row['raw_sha256']
assert load(result)['review_run_sha256'] == sha(evidence)
print(json.dumps({'status':'closed','verdict':load(result)['verdict'],'output_raw_bindings':[binding(p)for p in [result,evidence,finalmanifest]],'coverage':[65,15,29,10]},indent=2))
