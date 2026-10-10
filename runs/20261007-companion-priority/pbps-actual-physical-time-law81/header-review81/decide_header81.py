from pathlib import Path
import hashlib,json,re,datetime,subprocess
R=Path('E:/Samplinglib');B=R/'runs/20261007-companion-priority/pbps-actual-physical-time-law81';O=B/'header-review81'
def raw(p):
 b=p.read_bytes();return dict(path=p.relative_to(R).as_posix(),RAW_bytes=len(b),RAW_sha256=hashlib.sha256(b).hexdigest())
def load(p):return json.loads(p.read_text(encoding='utf-8'))
def save(n,d):
 p=O/n
 with p.open('x',encoding='utf-8',newline='\n') as f:json.dump(d,f,ensure_ascii=False,indent=2);f.write('\n')
 return raw(p)
freeze=load(O/'input-freeze81.json')
for e in freeze['inputs']:assert raw(R/e['path'])==e
H=B/'header81.proposed.lean';assert raw(H)['RAW_sha256']=='c3d1ad6107ad0aa812a99461d7dc48720ba83709104f699a908a77a89bec1e76'
assert load(O/'typecheck81.receipt.json')['exit_code']==0
assert subprocess.check_output(['git','-C',str(R/'.lake/packages/mathlib'),'rev-parse','HEAD']).decode().strip()=='db584cd6d46c92f209a44c0f1c829460d327499d'
parent76=R/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualFiniteJumpRecursion.lean';parent79=R/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualPhysicalTimeCover.lean';parent77=R/'AutoSamplingTheory/TechnicalLemmas/Probability/UnitExponentialProduct.lean'
def defs(p,end):
 t=p.read_text(encoding='utf-8');start=t.index('    let ');stop=t.index(end,start);parts=re.split(r'(?=^    let )',t[start:stop],flags=re.M)
 return {re.match(r'    let (\S+) ',v)[1]:v.rstrip() for v in parts if v}
dh=defs(H,'    ∃ Z');d79=defs(parent79,'    ∀ y');d76=defs(parent76,'    (∀ y')
assert all(dh[n]==d79[n] for n in d79) and all(dh[n]==d76[n] for n in ['c','Φ','S','rate','Λ','τ','next','record','eventTime'])
additional=[parent76,parent79,parent77,R/'runs/20261007-companion-priority/phase-pbps-gamma-preread57/primary-pbps.exactraw.snapshot.html',R/'runs/20261007-companion-priority/pbps-physical-time-law-preread81/primary_only81.py']
math=save('independent-header-math81.json',{
 'status':'ACCEPTED_PROSPECTIVE_MATHEMATICS_NO_REPAIR','reviewer':'/root/exact_verify77','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'header':raw(H),'complete_private_Prop_typecheck':raw(O/'typecheck81.receipt.json'),'definition_readback':raw(O/'definition-readback81.json'),
 'literal_contract':'Original six analytic proof arguments and carrier are exact80; all11 actual object lets exact79/80, nine physical/recursive lets exact76. Existing80 existential Z with joint measurability, all-covered deterministic arc/fallback characterization and perfixedparams common-AE alltime+origin is retained. No provider premise is added.',
 'new_law_semantics':[
 'q_y=volume.tilted(-V(x)-norm(x-y)^2/(2eta)) is the normalized source2.8 exact conditional law, not an unnormalized density or arbitrary input measure. The required IsMarkovKernel R and fiber equality force actual q_y to be a probability measure.',
 'gamma=stdGaussian E is source independent standard Gaussian momentum without eta-rescaling; eta scales the literal harmonic dynamics. M_y=(q_y product gamma) product P is exactly ((reference,momentum),fresh clock sample), with x,y fixed and reference held constant along a run.',
 'H is a Markov kernel on input(y,x), and its exact fiber is the terminal-position pushforward at finite pi of this actual product law. This gives joint Borel(y,x) dependence and total mass1 rather than merely one fixed-parameter measure.',
 'Phase0 pushforward equals dirac x product gamma, derived from product-AE actual physical initialization. This requires q_y and P probability mass1 and does not require any moment, density or stationary-input assumption on x.',
 'The final product-AE clause certifies initialization and the true actual live terminal arc with nonnegative finite elapsed strictly below actual tau. It does not assert a random all-time process law or an AE event uniform in y/x. Infinite next-wait last live arc and rank0 remain included.'
 ],
 'existing_parents_and_strict_internal_adapters':[
 {'parent':'HessianStrongConvexity.strongConvexOn_univ_of_fderiv2_lower + StrongConvexGibbsIntegrability.integrable_exp_neg_of_strongConvexOn','use':'C2 and positive lower Hessian derive integrability of exp(-V) and positive Gibbs normalizer on canonical finite-dimensional volume, without a minimizer or positive-dimension assumption. The original upper Hessian/scale conditions remain for actual dynamics.'},
 {'parent':'GaussianConditionalKernel.exists_tilted_isCondKernel + pinned Measure.tilted_tilted','use':'Apply the existing conditional kernel to the internally derived Gibbs probability volume.tilted(-V). Its quadratic tilt equals literal q_y by tilted_tilted under the derived exp(-V) integrability. Thus parameter measurability/Markov probability and exact conditional law have an existing source-compatible route; no missing larger parent has been identified.'},
 {'parent':'ActualPhysicalTimeMeasurability.actual_physical_time_measurable_phase (80), actual76/77/79 internally','use':'Provides jointly Borel actual Z and perfixedparams AE actual arcs/init. Retained actual definitions ensure direct interfaces; no supplied measurable interpolation, nonexplosion, clock or positivity certificate.'},
 {'parent':'Pinned Mathlib kernel product/map/comap and product measures','use':'Form the actual parameter-dependent initialization kernel R_y product const gamma product const P, retain fixed input(y,x), and push it through the joint Borel terminal observable. This is a distribution-construction adapter, not an implemented conditional-reference sampler.'},
 {'parent':'Pinned Measure.ae_prod_iff_ae_ae with measurable terminal+origin relation','use':'For fixed y,x, encode the full final predicate as a Borel relation in ((r,p),sample). Eliminate the apparent uncountable existential record a using the actual measurable Sum projection plus its inl predicate; then only countable exists n, order comparisons, joint actual tau/Phi/Z evaluations and equality in finite-dimensional Borel phase remain. Actual80 fixed(r,(x,p)) good sections imply P-AE this predicate. Fubini lifts those sections under (q_y product gamma) product P. No automatic measurability of forall real t good event is required for this smaller terminal law.'},
 {'parent':'Product-AE map congruence and Gaussian marginal','use':'The same Borel origin relation gives phase0 AE equality to (x,p); pushforward congruence and product marginal laws identify dirac x product gamma. No arbitrary sample-correlated parameter substitution is licensed.'}
 ],
 'consumer_assessment':'Substantive integration consumer: construct exact source-specific reference/output probability kernels, lift actual source path agreement under independently initialized randomness, and derive physical origin law. It is stronger than an abstract map(mu,f) wrapper because neither mu/f measurability/probability nor the source terminal/init agreement are supplied as premises.',
 'risk_boundaries':['Must prove Borel good relation before using Fubini; cannot interchange fixed-parameter AE and random parameters without it.','Must prove exact q_y equality/normalization; a zero-totalized tilt or arbitrary approximate reference law is unacceptable.','Must preserve ((reference,momentum),sample) product association and fixed y/x; no assumption x|Y~q_Y is required or permitted here.','Off-good z0 fallback differs from source zero-limit convention; product-AE actual terminal agreement ensures the intended source law, but explicit version-uniqueness is outside this header.','R/H are mathematical Markov kernels, not a Markov path or semigroup theorem, implemented sampler, invariant law or cost certificate.'],
 'repair_required':False,'necessary_larger_parent_identified':False,'proof_search_or_BODY_created':False,'Statement_Seal':False,'VERIFIED':False,'production_shared_state_modified':False
})
scope=save('independent-source-topology-scope81.json',{
 'status':'ACCEPTED_BOUNDED_IDEAL_EXACT_REFERENCE_LAW_SCOPE','reviewer':'/root/exact_verify77','header':raw(H),'primary_readback':raw(O/'primary-clause-readback81.json'),
 'reading_order':'Source-only candidate/graph and then header read before own pinned-primary reread. This is a prospective source-topology/math audit, not an anti-anchored final source reviewer or blind decoder.',
 'source_checks':[
 'Algorithm1 is explicitly ideal conditional half-turn: line2 independent exact q_y reference and standard Gaussian momentum; line4 initial position fixed x; line8 returns x_pi. No implemented exact reference producer is asserted.',
 'S2.E8 fixes q_y density proportional to exp(-V(x)-norm(x-y)^2/(2eta)). Literal volume.tilted expresses its normalized measure. Existing conditional-Gaussian kernel and Gibbs integrability supply normalization/measurability semantics.',
 'A1.SS1.p2.1 initializes the actual recurrence with iid Exp1 clocks, source E_(n+1) drives update n. A1.SS1.p2.2 finite/stopped and half-open live arcs persist in the header.',
 'A1.SS2.p3.1 constructs a Borel terminal version; source sets failing-limit outputs to zero. Header uses actual80 explicit uncovered z0 convention and proves product-AE real terminal arc, a legitimate selected ideal law realization with exceptional convention visible.',
 'A1.SS2.p4.1 integrates terminal-position indicators against exact reference, Gaussian momentum and exponential laws to make (y,x)->H_y(x,A) Borel. The header exact pushforward Markov kernel is this bounded source law consumer.'
 ],
 'graph_scope_refinement':{'retained':'G81-01..13 provide source assumptions, normalized exact laws, actual recursion/phase and product lift/output/init law; G81-14 is admitted only as source-good terminal law identification at pi. G81-15 remains excluded OPEN.','strictly_smaller_product_good_relation':'For this header, measurable origin+pi terminal relation suffices. Full rational-horizon alltime goodset is optional and not a required new parent. Actual80 alltime sections can be projected to the terminal predicate before Fubini.','outside_current_conclusion':['standalone exceptional-version uniqueness theorem','full randomly initialized alltime process law','arbitrary correlated random parameter law','path Markov/restart/semigroup','invariance/stationarity/reversibility','implemented approximate/exact reference sampler','runtime/query/accuracy/cost/composition/fullpaper']},
 'genuine_new_consumer':True,'extra_source_hypotheses':[],'independent_product_required':True,'repair_required':False,'final_source_acceptance':False,'proof_or_completion_credit':False
})
decision=save('decision81.json',{'status':'ACCEPTED_PROSPECTIVE_HEADER_NO_REPAIR','reviewer':'/root/exact_verify77','header':raw(H),'math_review':math,'distinct_source_topology_scope':scope,'typecheck':raw(O/'typecheck81.receipt.json'),'scope':'Complete exact private statement only, independently typechecked. No proof/BODY/claim/Seal/VERIFIED or source-final/completion credit.','necessary_larger_parent_identified':False})
for e in freeze['inputs']:assert raw(R/e['path'])==e
files=sorted([p for p in O.iterdir() if p.is_file()],key=lambda p:p.name)
manifest=save('closed-manifest81.json',{'status':'CLOSED_PROSPECTIVE_HEADER_REVIEW','reviewer':'/root/exact_verify77','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'header':raw(H),'decision':decision,'all_frozen_inputs_unchanged':True,'additional_primary_and_parent_inputs':[raw(p) for p in additional],'fixed_mathlib':'db584cd6d46c92f209a44c0f1c829460d327499d','artifacts':[raw(p) for p in files],'manifest_self_hash_omitted_to_avoid_cycle':True,'administrative_parser_cache':'Importing the frozen stdlib parser created one native .pyc under its source __pycache__; that runtime-only cache was relocated into this owned review directory. No source/parser mathematical bytes changed; .pyc is observability data, not proof evidence.','no_production_shared_state_or_theorem_BODY_edits':True})
print(json.dumps({'decision':decision,'closed_manifest':manifest,'math':math,'source_topology':scope},ensure_ascii=False))
