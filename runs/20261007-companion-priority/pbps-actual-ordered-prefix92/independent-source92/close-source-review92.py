from pathlib import Path
import json,hashlib,re,datetime

ROOT=Path('E:/Samplinglib')
BASE=ROOT/'runs/20261007-companion-priority/pbps-actual-ordered-prefix92'
OUT=BASE/'independent-source92'
def sha(b):return hashlib.sha256(b).hexdigest()
def canon(o):return sha(json.dumps(o,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode())
def load(p):return json.loads(p.read_text(encoding='utf8'))
def bind(p):
 b=p.read_bytes();return {'path':p.relative_to(ROOT).as_posix(),'raw_sha256':sha(b),'bytes':len(b)}
def write(n,o):
 p=OUT/n
 with p.open('x',encoding='utf8',newline='\n') as f:json.dump(o,f,ensure_ascii=False,indent=2);f.write('\n')
 return bind(p)
packetpath=BASE/'anti-anchored.review92.json';packet=load(packetpath)
assert sha(packetpath.read_bytes())=='cfd2f6652d62c88eafe29649ecf0c324490048990466acf2f4527af5b839253d'
assert canon({k:v for k,v in packet.items() if k!='packet_sha256'})==packet['packet_sha256']=='28315ec56b562246bf9ee88dce8c7e4923d8db1d5e2b4651cc0afa2bd07595bb'
module=ROOT/packet['lean']['file'];raw=module.read_bytes();text=module.read_text(encoding='utf8');lines=raw.splitlines(keepends=True)
assert sha(raw)=='46c637205d601786472e789bf4706a77b18ea6dad423ab33d1ac39491e71e111'
pubpath=ROOT/'website/content/publications/pbps-actual-ordered-prefix.json';pub=load(pubpath)['items'][0]
lessonpath=ROOT/'website/content/declaration_lessons/pbps-actual-ordered-prefix.json';lesson=load(lessonpath)['units'][0]
payload={
 'file':sha(text.encode()),'current_lean_module':text,
 'toolchain':sha((ROOT/'lean-toolchain').read_text().encode()),'dependencies':sha((ROOT/'lake-manifest.json').read_text().encode()),
 **{k:pub[k] for k in ['source','statement','formulae','assumptions','obligations']},'lesson':lesson,
 'binding':{k:v for k,v in pub['bindings'][0].items() if k not in ['audit_id','legacy_audit_debt']}}
assert canon(payload)==packet['publication_binding_sha256']=='3cacdf93c8234e8701b836e6622764fc2b4351078e424ea98ca6c97255c69efb'
assert packet['candidate_publication_context']['current_lean_module']==text
assert packet['candidate_publication_context']['lesson']=={k:v for k,v in lesson.items() if k not in ['boundary','source_history_boundary']}
sealpath=BASE/'root.statement-seal92.json';seal=load(sealpath)
decl=text.split('def actual_ordered_prefix_statement',1)[1].split('\n\n\nset_option',1)[0]
assert decl==seal['expanded_literal_Prop'].rstrip('\n')
expanded=decl.replace(' : Prop :=',' :',1)+'\n'
assert expanded==packet['lean']['statement']
assert sha(expanded.encode())==packet['lean']['statement_sha256']
decoderbase=ROOT/'runs/semantic-roundtrip/anonymous92'
decoderinput=decoderbase/'input.json';decoderpath=decoderbase/'decoder/decoder-result.native.json';decoder=load(decoderpath)
decmanifestpath=decoderbase/'decoder/closed-RAW.native.json';decm=load(decmanifestpath)
reconpath=decoderbase/'decoder/reconstruction.md'
assert reconpath.read_text(encoding='utf8')==packet['blind_reconstruction']['text']==decoder['reconstructed_theorem_text']
assert sha(reconpath.read_bytes())==packet['blind_reconstruction']['text_sha256']
assert sha(decoderinput.read_bytes())==decm['input_raw_sha256']
assert canon(decm['run_manifest'])==packet['blind_reconstruction']['decoder_run_sha256']
assert not packet['blind_reconstruction']['source_text_visible']
graphpath=ROOT/'runs/20261007-companion-priority/pbps-ordered-iteration-preread92/primary-first/candidate-source-proof-graph92.v2.native.json'
coveragepath=graphpath.with_name('candidate-source-coverage92.v2.native.json');graph=load(graphpath);coverage=load(coveragepath)
primary=ROOT/'runs/20261007-companion-priority/phase-pbps-gamma-preread57/primary-pbps.exactraw.snapshot.html';source=primary.read_bytes()
assert sha(source)=='d81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760'
for r in graph['source_regions'].values():assert sha(source[r['byte_start']:r['byte_end_exclusive']])==r['raw_sha256']
def region(a,b):
 part=b''.join(lines[a-1:b]);return {'path':module.relative_to(ROOT).as_posix(),'source_raw_sha256':sha(raw),'start_line':a,'end_line':b,'exact_code_raw_sha256':sha(part)}

explanations=[
 'Finite Borel coordinate/live-tag guards and composition with actual harmonic flow, bounce/rate and hazard produce joint K/q measurability; proof proves real factor positivity directly. Source requires Borel bounce, never continuity.',
 'Actual first record supplies zero. The strict guard makes observed tuple a simplex point. Finite-record induction excludes top via live successor, extracts elapsed time from cumulative sum, and identifies each poststate and tag pointwise.',
 'Actual depth-zero event and empty simplex are universal including T=0; comap mass is proved by map_comap_subtype_coe and empty finite product volume. q0=1; canonical probability normalization makes both integrals equal even for infinite test value.',
 'Finite snoc and strict-monotone split prove exact guarded event equality on all raw inputs. This is a literal prefix event equality, not event-count equivalence or an a.e. replacement.',
 'The actual absolute next-time parent is instantiated at constant T and whole-next-history test; localization to old guard and setLIntegral_map yield measurable J and actual probability recurrence. No conditional-law provider is a public premise.',
 'Exact coordinate insertion preserves product Lebesgue. Simplex indicator, nonnegative Tonelli and measurable extension of a subtype test yield the exact nested subtype comap identity. Arbitrary extension values outside the simplex do not alter restricted integrals. This is finite-product coordinate splitting, not an unproved general shear theorem.',
 'Algebra preserves every old state and appends the source flow/bounce. Nonnegative old time and positive gap justify toNNReal addition; Fin.prod_univ_castSucc and ofReal_mul factor q. Generic private step/factor assumptions are instantiated by actual dynamics.',
 'Natural-number induction uses actual base, actual one-step recurrence and measurable J; finite q permits multiplication inside lintegral. Indicator support, complete append and q factorization match integrands under exact subtype simplex disintegration. No boundedness/integrability premise is introduced.',
 'Measure.ext_of_lintegral, map integrals and withDensity turn the proved all-test identity into equality of full-history measures; F=1 yields density mass and canonical probability yields <=1. The private htest input is supplied by actual_prefix_all_integrals.',
 'Public theorem retains the six original assumptions and literal target, obtains H/obs/event measurability, passes proved all-n integrals to measure closure, and invokes pointwise history identification. Full path, final survival, count assembly and operator conclusions remain absent.' ]
expositions=[]
assert len(lesson['steps'])==10
for i,s in enumerate(lesson['steps']):
 r=s['lean_source_region'];actual=region(r['start_line'],r['end_line']);assert actual==r
 assert b''.join(lines[r['start_line']-1:r['end_line']]).decode()==s['lean']
 expositions.append({'step':i+1,'title':s['title'],'lesson_json_pointer':f'/units/0/steps/{i}',
  'lesson_raw_sha256':bind(lessonpath)['raw_sha256'],'body_region':actual,
  'exposition_formula_digest':canon({k:s[k] for k in ['title','text','formula','detail']}),
  'formula':s['formula'],'verdict':'faithful','reason':explanations[i],
  'conditions_preserved':True,'exposition_requires_repair':False})
expositionbinding=write('exposition-review92.native.json',{'record_kind':'whole-reader-ten-region-source-audit','packet_sha256':packet['packet_sha256'],
 'publication_binding_sha256':packet['publication_binding_sha256'],'module':bind(module),'lesson':bind(lessonpath),'publication':bind(pubpath),
 'steps':expositions,'statement_and_assumptions':'Complete publication/lesson statement explicitly defines literal dynamics, clocks, tagged histories, actual event, prescribed whole histories, reference measure, density and all test/mass conclusions. Exactly six original analytic assumptions retained; Hilbert/rank-zero and extended-test scope disclosed.',
 'formula_context':'s0=0 and empty tuple conventions are provided before the steps. A_abs denotes full history append, D_T the guarded actual next-event density, and rho the pre-bounce-rate times elapsed-survival factor; steps 5,7,8 describe these operations and adjacent literal Lean expands each exactly. No additional density/certificate premise appears.',
 'scope':'Content and exact adjacent Lean reviewed; no browser DOM/render inspection performed. Initial folding/render gates remain integration evidence, not certified by this content audit.',
 'verdict':'ACCEPTED_CONTENT_FIDELITY','findings':[]})

# Mapping onto the preexisting primary-derived graph does not alter its topology.
mapped={
 'H92':('SOURCE_ASSUMPTIONS_RETAINED',[(1459,1466),(1555,1563)],'Exactly six original analytic binders; beta eta<=1 equivalent to eta<=1/beta because beta>0.'),
 'O92':('LITERAL_OBJECTS_RETAINED',[(1467,1478)],'Center, harmonic flow, residual rate and reflection are literal. Total zero division realizes R0 identity.'),
 'I92':('LITERAL_OBJECTS_AND_REUSED_LAW',[(1479,1499),(955,960)],'Closed hazard crossing, stopped actual record recursion and canonical real exponential product; actual one-step law is an exact existing dependency.'),
 'T92':('ASTIS_ENCODING_REALIZED',[(1484,1504)],'Absorbing Sum stopped tag and complete Fin history, no fabricated finite event.'),
 'M92':('EXACT_REUSE_AND_NEW_COMPOSITION',[(24,282),(955,965),(1654,1665)],'Existing actual-flow/rate/hazard and actual-next-history measurability composed with literal recursions/coordinates. I92->M92 retained.'),
 'W92':('EXACT_EXISTING_DEPENDENCY_USED',[(955,991)],'ActualAbsoluteNextEventTime whole-next-history integral at constant horizon T, localized to old guard.'),
 'D92':('REALIZED_AND_BASE_MEASURE_PROVED',[(30,37),(662,681),(1505,1509)],'Strict simplex and subtype comap; empty measure mass1 explicitly proved.'),
 'K92':('PROVED_FOR_PRESCRIBED_RECORDS',[(244,271),(1510,1516)],'All prescribed records jointly Borel. Does not claim entire-path observable measurability.'),
 'Q92':('PROVED_PREFIX_WEIGHT',[(272,282),(1183,1190),(1517,1526)],'Finite nonnegative pre-bounce-rate/segment-survival product; ofReal and snoc factorization.'),
 'E92':('LITERAL_STRICT_PREFIX_REALIZED',[(58,72),(695,752),(1527,1540)],'Actual B pulls auxiliary A back through actual zero-initialized H; no raw pointwise count gloss.'),
 'B92':('PROVED_BASE',[(642,692)],'All T including zero; single initial history and unit empty-simplex mass.'),
 'A92':('PROVED_COMPLETE_APPEND_IDENTIFICATION',[(435,489),(1101,1190),(1423,1434)],'Pointwise actual-to-prescribed records and complete snoc agreement; every older time/state/tag kept.'),
 'J92':('PROVED_ACTUAL_SUCCESSOR',[(955,991),(1341,1435)],'Genuine deterministic-index law localizes old guard; measurable J is fed to induction, not assumed.'),
 'FUB92':('BACKGROUND_ROUTE_INSTANTIATED',[(1010,1098)],'Fixed finite product Lebesgue insertion, nonnegative Tonelli, subtype extension and comap integral identity.'),
 'SEC92':('PROVED_EXACT_SIMPLEX_SECTION',[(994,1098)],'Snoc coordinate sections and reference-measure equality including empty prefix.'),
 'PREFIX92':('PROVED_BOUNDED_TARGET',[(1194,1455),(1554,1683)],'All finite strict-prefix history tests, whole-history pushforward and exact unnormalized mass.'),
 'REL92':('ALTERNATIVE_ROUTE_NOT_USED',[],'Relative-wait vector induction is optional; absolute-coordinate induction is sufficient.'),
 'TRI92':('ALTERNATIVE_ROUTE_NOT_USED',[],'No finite cumulative-sum triangular transport theorem needed or claimed on chosen route.'),
 'SURV92':('OPEN_OUTSIDE_PREFIX',[],'Missing final no-further-event survival at T-last event.'),
 'ALG92':('OPEN_OUTSIDE_PREFIX',[],'Full-path integrated-hazard and pre-jump rate stitching not claimed.'),
 'END92':('OPEN_IF_ENDPOINT_CONVERSION_REQUIRED',[],'No strict/non-strict horizon or raw count identification claimed.'),
 'ENERGY92':('EXISTING_SOURCE_INGREDIENT_NOT_NEW_CREDIT',[],'Energy/rate-cap source mechanism retained for later full-path consumers; no new proof assigned by this module.'),
 'N92':('EXISTING_ACTUAL_INPUT_RESULT_PRESERVED',[],'Existing actual-input nonaccumulation/coverage remain separate; no reproof or new global-process claim here.'),
 'PATH92':('OPEN_OUTSIDE_PREFIX',[],'Complete records supply necessary data, but full actual/prescribed trajectory and arbitrary path-functional composition still required.'),
 'COUNT92':('OPEN_OUTSIDE_PREFIX',[],'Finite event-count partition and a.e. endpoint/positive-clock interpretation still required for full A7.'),
 'TERM92':('OPEN_OUTSIDE_PREFIX',[],'Full nth A7 term needs prefix plus survival, hazard stitching and path identification.'),
 'CAP92':('OPEN_FULL_A7_ASSEMBLY',[],'Printed cap/simplex absolute-convergence route not proved by finite-prefix law.'),
 'MASS92':('OPEN_ALTERNATIVE_FULL_A7_ASSEMBLY',[],'Optional nonnegative count-mass/Tonelli signed assembly not conflated with prefix mass<=1.'),
 'A7':('OPEN_FULL_PATH_FUNCTIONAL_IDENTITY',[],'Printed full-path bounded measurable functional identity remains a genuine future consumer.')}
assert set(mapped)=={n['id'] for n in graph['nodes']}
nodes=[{'id':n['id'],'source_claim':n['claim'],'source_regions':n['source_regions'],'review_disposition':mapped[n['id']][0],
 'actual_proof_regions':[region(*p) for p in mapped[n['id']][1]],'reason':mapped[n['id']][2]} for n in graph['nodes']]
edges=[]
for e in graph['edges']:
 edges.append({**e,'implementation_review': 'realized chosen prefix route' if e['to'] in ['O92','I92','T92','M92','W92','K92','Q92','E92','B92','A92','J92','FUB92','SEC92','PREFIX92'] and e['from'] not in ['TRI92','REL92'] else 'preserved source dependency or optional route; no closure claimed here'})
rows=[]
for r in coverage['coverage']:
 part=source[r['source_region']['byte_start']:r['source_region']['byte_end_exclusive']];assert sha(part)==r['source_region']['raw_sha256']
 statuses=[mapped[n][0] for n in r['nodes']]
 rows.append({**r,'review_verdict':'DISPOSITION_PRESERVED','actual_node_dispositions':statuses,
  'proof_region_evidence':[region(*p) for n in r['nodes'] for p in mapped[n][1]],
  'reason_after_proof':r.get('reason','') or '; '.join(mapped[n][2] for n in r['nodes']),
  'excluded_not_used_to_close_target':r['disposition']=='EXCLUDED'})
coveragebinding=write('source-proof-coverage92.native.json',{'record_kind':'independent-actual-proof-versus-primary-graph-coverage','packet_sha256':packet['packet_sha256'],
 'primary':bind(primary),'frozen_graph':bind(graphpath),'frozen_inventory':bind(coveragepath),'module':bind(module),
 'nodes':nodes,'edges':edges,'coverage':rows,'node_count':len(nodes),'edge_count':len(edges),'coverage_count':len(rows),
 'AND_routes':graph['AND_routes'],'OR_routes':graph['OR_routes'],
 'route_decision':'Production instantiates frozen preferred absolute-coordinate induction. The relative-vector/triangular alternative is not a missing mandatory dependency. Full-A7 alternatives remain open.',
 'coverage_verdict':'EXHAUSTIVE_WITHIN_FROZEN_SELECTED_SOURCE_SLICE','unmapped_nodes':[],'unmapped_rows':[],
 'genuine_consumer':'PREFIX92 now supplies complete-history probability weights needed by TERM92. TERM92 still AND-requires terminal survival, hazard/path stitching and whole-path functional identification, then COUNT92 and one justified signed-series assembly route feed A7.',
 'existing_nonaccumulation_boundary':'The source cap/nonaccumulation mechanism and actual-input78/79 are preserved, not treated as an unresolved reproof or as proof of full A7.',
 'canonical_graph_mutated':False,'topology_derived_from_Lean':False})

originals={
 'objects':'Source actual harmonic PBPS with fixed y,r,z0, independent unit-exponential thresholds, closed hazard clock and cumulative bounce recursion; finite prescribed histories unpack the source iteration sentence. Full A7 itself concerns whole paths.',
 'domains':'Source Euclidean phase R^d x R^d and Borel structures; nonnegative finite times and strict ordered simplex. Explicit ASTIS finite-dimensional Hilbert/rank-zero, stopped Sum history and ENNReal test extensions are part of the bounded target.',
 'quantifiers':'Original six assumptions globally in x,v; arbitrary fixed y,r,z0; bounded finite-prefix target for every n and finite nonnegative T, every measurable nonnegative extended complete-history test; joint K/q in parameters and simplex times with V,eta fixed.',
 'assumptions':'Global C2 V; alpha>0; alpha<=beta; Hessian sandwich for every x,v; eta>0; eta<=1/beta. No law, independence, density, measurability, nonexplosion, integrability or positive-history-mass provider.',
 'conclusion':'Strict first-n complete-history law with product pre-bounce rate and completed-segment survival density; Borel facts, pointwise actual/prescribed record identity and unnormalized mass<=1. This elaborates an ingredient of A7 rather than claiming A7.',
 'scopes':'Absolute stored times, elapsed positive gaps, post-bounce stored states and pre-bounce rate factors; no final survival or exactly-n count claim. n0 includes empty singleton at T0; stopped infinity excluded by live strict guard.',
 'constant_dependencies':'Exactly unit-rate independent exponentials. Dynamics/density depend on V,eta,y,r,z0 and time tuple; alpha,beta enter source constraints, not additional runtime constants. No asymptotic or unnamed constants.'}
slot_evidence={
 'objects':'A1.E1/E2; production1458-1550 literal25 lets; full decoder deterministic/random object reconstruction; lesson complete statement.',
 'domains':'S1.p1, A1.Ex19, Appendix A2; production1459-1461 and1495-1509; subtype comap proof671-681 and1069-1098; explicit extensions in publication.',
 'quantifiers':'Production1531-1550 and public1554-1563; decoder Full theorem items1-7 exactly retain all n,T,y,r,z0,F quantifiers and pointwise w in B.',
 'assumptions':'S1.p1/S2.SS2.p1 versus public1558-1562; beta>0 follows alpha>0 and alpha<=beta, so beta eta<=1 is equivalent. Private measurable/test hypotheses discharged1650-1683.',
 'conclusion':'Induction1341-1435, map/mass1438-1455, public assembly1650-1683; decoder says complete tagged-history unnormalized law, all ENNReal tests and no terminal survival.',
 'scopes':'A1.Ex19/A1.E7; guard event split695-752; definition A1527-1530 and actual H1538; base642-692; publication and decoder explicitly preserve count/path boundary.',
 'constant_dependencies':'Literal P1495; q1517-1526; six assumptions1462-1466; no variable exponential parameter or added constants; decoder last paragraph agrees.'}
semantics={k:{'original':originals[k],'reconstructed':decm['semantic_slots'][k],'relation':'explicit-elaboration' if k in ['objects','domains','conclusion','scopes'] else 'equivalent','evidence':slot_evidence[k]} for k in packet['review_contract']['semantic_slots']}
definition_reason={
 'c':'Source center y-eta gradient(reference).','Φ':'Source harmonic flow signs and sqrt scaling.','S':'Source reflection; total real division yields identity at zero residual.','rate':'Positive-part residual inner-product rate, not full force.','Λ':'Actual finite nonnegative elapsed integrated rate.','τ':'Closed hazard crossing, empty crossing top.','next':'Top tested before untopD; finite time additive, flow then bounce; absorbing stopped.','record':'Literal initialized finite Nat recursion consuming index-k clock.','P':'Canonical countable Exp(1) product.','ε':'Raw toNNReal totalization, source agreement a.e.','history':'All deterministic-depth records, no replacement terminal object.','Rec':'Borel Sum live/stopped representation.','Hist':'Fin(n+1) ambient tagged record tuples.','readTime':'Guarded live time with stopped zero observer only.','Δ':'StrictMono(0::times) and every time<T; empty convention correct.','Prefix':'Borel simplex subtype.','m':'Comap of actual product real Lebesgue, not normalization.','zAt':'Finite prescribed poststate recursion along successive gaps.','K':'Every live time/state plus initial record; toNNReal exact on simplex.','qReal':'Product pre-bounce rates times survival over completed segments.','q':'ofReal real finite nonnegative product, q0=1.','A':'Auxiliary all-live ordered/capped history guard, no fixed initial condition until actual pullback.','H':'Literal actual history specialization.','B':'Actual H pullback of A; fixed initial record supplies time0.','obs':'Actual postinitial stored times.'}
lets=re.findall(r'(?m)^\s*let ([^\s:]+)',expanded);assert len(lets)==25 and set(lets)==set(definition_reason)
definitions=[{'name':n,'classification':'source-literal' if n in ['c','Φ','S','rate','Λ','τ','record'] else 'explicit-ASTIS-representation-or-completion','verdict':'faithful','evidence':definition_reason[n]} for n in lets]

mathbase=BASE/'independent-math92';receiptpath=mathbase/'kernel.receipt.native.json';receipt=load(receiptpath)
for k in ['source','copy','lake_manifest','stdout','stderr']:
 b=receipt[k];actual=bind(Path(b['path']));assert actual['raw_sha256']==b['raw_sha256'] and actual['bytes']==b['bytes']
assert receipt['exit_code']==0 and receipt['terminal_closed']
assert (mathbase/'FreshWholeSourceKernel92.lean').read_bytes().startswith(raw)
log=(mathbase/'kernel.stdout.log').read_text(encoding='utf8')
assert 'depends on axioms: [propext,' in log and 'Classical.choice' in log and 'Quot.sound' in log and 'sorryAx' not in log
inputs=[primary,packetpath,module,pubpath,lessonpath,sealpath,graphpath,coveragepath,decoderinput,decoderpath,decmanifestpath,reconpath,
 receiptpath,mathbase/'FreshWholeSourceKernel92.lean',mathbase/'kernel.stdout.log',mathbase/'kernel.stderr.log',mathbase/'static-check92.native.json',
 ROOT/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualAbsoluteNextEventTime.lean',ROOT/'AutoSamplingTheory/TechnicalLemmas/Probability/UnitExponentialProduct.lean',
 ROOT/'lean-toolchain',ROOT/'lake-manifest.json',ROOT/'tools/astis_publication.py',
 OUT/'primary-first-expectation92.native.json',OUT/'primary-source-slices92.native.json',OUT/'primary-first-RAW92.native.json']
run=write('review-run92.native.json',{'record_kind':'independent-anti-anchored-whole-source-review-run','reviewer':'/root/primary_source91','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'canonical_packet_sha256':packet['packet_sha256'],'packet_raw_sha256':sha(packetpath.read_bytes()),'publication_binding_sha256':packet['publication_binding_sha256'],
 'inputs':[bind(p) for p in inputs],
 'chronology':'Primary-only expectation and21slice binding frozen before new packet. Then original full packet statement, complete blind reconstruction, whole1686line production module, full reader statements/ten exact regions, immutable primary graph29nodes57edges and inventory46rows compared. Supplemental original reversal/operator source regions reread solely to validate excluded dispositions. No prior source verdict or repair used as mathematical authority.',
 'independence':'Reviewer differs from formalizer and current blind decoder; prior source-only candidate/header exposure disclosed in primary freeze. Frozen graph authored before implementation and distinctly reviewed; present task audits its use, does not self-approve topology.',
 'compiler_scope':'Existing independent fresh-whole-source kernel receipt checked against exact production prefix and raw log hashes; exit0 and standard propext/Classical.choice/Quot.sound axioms. No compiler rerun or whole repository gate claimed by this source reviewer.',
 'no_canonical_mutation':True})
report={
 'schema_version':1,'record_kind':'independent-anti-anchored-source-and-exposition-review','reviewer':'/root/primary_source91',
 'independent_from_formalizer':True,'independent_from_decoder':True,'reviewer_packet_sha256':packet['packet_sha256'],
 'reviewer_packet_raw_sha256':sha(packetpath.read_bytes()),'publication_binding_sha256':packet['publication_binding_sha256'],
 'review_run_sha256':run['raw_sha256'],'review_run_binding':run,
 'module':bind(module),'publication':bind(pubpath),'lesson':bind(lessonpath),'primary':bind(primary),
 'semantic_slots':semantics,'verdict':'equivalent-after-elaboration',
 'decision':'ACCEPT_BOUNDED_ACTUAL_STRICT_PREFIX_SOURCE_AND_EXPOSITION',
 'deltas':[
 {'slot':'domains','classification':'explicit-elaboration','source':'Printed Euclidean R^d.','lean':'Finite-dimensional real Hilbert carrier including rank zero.','assessment':'Disclosed ASTIS extension; no extra analytic assumption.'},
 {'slot':'objects','classification':'explicit-elaboration','source':'Source iid clocks and recursion stop at infinite wait.','lean':'Literal canonical product, clipped raw inputs, absorbing Sum record and complete finite histories.','assessment':'Source-faithful realization and null-input totalization; no hidden law provider.'},
 {'slot':'conclusion','classification':'explicit-elaboration','source':'A7 states whole-path bounded measurable functional infinite expansion, with omitted finite clock iteration.','lean':'Unnormalized first-n strict complete-history law for all ENNReal Borel tests, without final survival or count sum.','assessment':'Explicit attributed intermediate completion and test extension; not represented as a proof of full A7.'}],
 'repairs':[],
 'six_binder_audit':[{'name':n,'classification':'original-source-assumption','source_anchor':a,'meaning':s,'verdict':'same-after-equivalent-real-encoding'} for n,a,s in [
 ('hα','S1.p1','alpha>0'),('hαβ','S1.p1','alpha<=beta'),('hV','S1.p1','global C2 V'),('hH','S1.p1','both Hessian quadratic-form bounds everywhere'),('hη','S2.SS2.p1','eta>0'),('hβη','S2.SS2.p1','beta eta<=1 equivalent to eta<=1/beta since beta>0')]],
 'definition_audit':definitions,
 'statement_seal_audit':{'seal':bind(sealpath),'full_Prop_exact_match':True,'packet_expanded_statement_exact_match':True,'statement_sha256':packet['lean']['statement_sha256'],'no_added_public_provider':True},
 'actual_proof_audit':{'scope':'Entire production source read, including all private interfaces and their public discharge.','chosen_route':'Original-source-derived absolute-coordinate induction, not a terminal-marginal or normalized-event surrogate.',
 'critical_checks':['Actual clock recursion is literal and unchanged across private/public lets.','Pointwise reconstruction preserves all records and excludes infinite waits through live guard.','B0=univ even T0 and subtype empty-product mass1 proved.','Exact successor event equality is all-raw-input strict prefix, never a count assertion.','Actual one-step theorem supplies measurable J and localized whole-history law.','True finite-product Lebesgue insertion and Tonelli, including subtype extension, supply simplex measure identity.','Generic snoc/state/weight helpers are applied to actual PBPS step and factor; no private premise escapes.','Finite q scalar enables ENNReal integral multiplication; arbitrary infinite tests retained.','All-test identity is proved by induction before generic measure closure consumes it.','UnitExponentialProduct is directly used only through its probability projection, in base and final mass closure. No source nonexplosion credit inferred from that projection.'],
 'kernel_receipt':bind(receiptpath),'kernel_log':bind(mathbase/'kernel.stdout.log'),'axioms':['propext','Classical.choice','Quot.sound'],
 'proof_not_replaced_by_compilation':'Source/reader reasoning was independently compared; build log establishes only formal acceptance of the exact mathematical implementation.'},
 'source_proof_coverage':coveragebinding,'exposition_audit':expositionbinding,
 'review_evidence':['Immutable fresh primary-first expectation and21source slices','Canonical packet RAW/canonical hashes and publication binding recomputed','Exact whole module and sealed expanded statement','Complete fresh anonymous reconstruction and native decoder hash/run chain','Frozen29node57edge source graph and all46source coverage dispositions','Ten lesson proof region hashes, exact code equality, formula/prose comparison','Independent kernel receipt exact source prefix, standard axiom log, and static fake-closure receipt'],
 'limitations':['Only bounded actual strict first-n complete-history law accepted.','Terminal survival, path/hazard stitching, endpoint/count identification and infinite bounded whole-path A7 assembly remain OPEN.','Existing actual-input nonaccumulation78/coverage79 preserved; not re-audited or re-awarded here.','No physical-time restart, invariance, mixing, cost, implementation error, paper composition or whole-paper completion.','No whole-repository gate, public deployment, rendered-page inspection or postmerge purification claimed.','The source graph records selected A1/A2 scope and explicit excluded claims, not whole-paper exhaustive coverage.'],
 'canonical_state_changed':False,'VERIFIED_transition_performed':False}
reportbinding=write('source-review92.native.json',report)
manifest=write('closed-RAW92.native.json',{'record_kind':'closed-RAW-independent-whole-source-review','reviewer':'/root/primary_source91','canonical_packet_sha256':packet['packet_sha256'],
 'publication_binding_sha256':packet['publication_binding_sha256'],'inputs':[bind(p) for p in inputs],
 'outputs':[expositionbinding,coveragebinding,run,reportbinding,bind(OUT/'close-source-review92.py')],
 'closure':'Raw bytes checked for every input/output. No earlier immutable file changed. Manifest excludes itself; reported externally by RAW SHA. Source result bounded as in report; canonical states untouched.'})
for b in load(OUT/'closed-RAW92.native.json')['inputs']+load(OUT/'closed-RAW92.native.json')['outputs']:assert bind(ROOT/b['path'])==b
print(json.dumps({'report':reportbinding,'run':run,'coverage':coveragebinding,'exposition':expositionbinding,'closed_manifest':manifest},indent=2))
