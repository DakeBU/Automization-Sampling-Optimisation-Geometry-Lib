# coding: utf-8
import pathlib,json,hashlib,datetime,sys
sys.stdout.reconfigure(encoding='utf-8')
R=pathlib.Path('E:/Samplinglib');O=R/'runs/20261007-companion-priority/pbps-after-macroscopic-preread51'
def sha(b):return hashlib.sha256(b).hexdigest()
def put(n,x): (O/n).write_bytes((json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode())
def text(n,s): (O/n).write_bytes(s.encode('utf-8'))
assert json.loads((O/'lease.json').read_text())['status']=='OPEN'
(O/'lease.open.historical.json').write_bytes((O/'lease.json').read_bytes())
selections=[
 ('GaussianConvolutionRegularity','AutoSamplingTheory/TechnicalLemmas/Measure/GaussianConvolutionRegularity.lean',[(29,36),(144,144),(251,262)]),
 ('WeightedGradient','AutoSamplingTheory/TechnicalLemmas/FunctionalInequalities/WeightedGradient.lean',[(26,41)]),
 ('WeightedC1GradientDomain','AutoSamplingTheory/TechnicalLemmas/FunctionalInequalities/WeightedC1GradientDomain.lean',[(147,154)]),
 ('Adjoint',' .lake/packages/mathlib/Mathlib/Analysis/InnerProductSpace/Adjoint.lean'.strip(),[(304,308)]),
 ('Positive','.lake/packages/mathlib/Mathlib/Analysis/InnerProductSpace/Positive.lean',[(266,275),(371,373),(459,491),(544,549)]),
 ('CStarCLM','.lake/packages/mathlib/Mathlib/Analysis/CStarAlgebra/ContinuousLinearMap.lean',[(18,21)]),
 ('CFCinstances','.lake/packages/mathlib/Mathlib/Analysis/CStarAlgebra/ContinuousFunctionalCalculus/Instances.lean',[(227,238),(255,259),(320,328)]),
 ('CFCsqrt','.lake/packages/mathlib/Mathlib/Analysis/SpecialFunctions/ContinuousFunctionalCalculus/Rpow/Basic.lean',[(81,85),(236,241),(265,267)]),
 ('Tilted','.lake/packages/mathlib/Mathlib/MeasureTheory/Measure/Tilted.lean',[(34,43)]),
 ('Density','.lake/packages/mathlib/Mathlib/MeasureTheory/Measure/WithDensity.lean',[(44,45)]),
 ('Integrable','.lake/packages/mathlib/Mathlib/MeasureTheory/Function/L1Space/Integrable.lean',[(934,936)]),
 ('RealIntegral','.lake/packages/mathlib/Mathlib/MeasureTheory/Integral/Bochner/Basic.lean',[(702,703)]),
 ('Map','.lake/packages/mathlib/Mathlib/MeasureTheory/Measure/Map.lean',[(203,204)]),
 ('Snd','.lake/packages/mathlib/Mathlib/MeasureTheory/Measure/Prod.lean',[(1147,1149)]),
 ('MeasureCard','research-wiki/sampling-sde-library/cards/AutoSamplingTheory.TechnicalLemmas.Measure.md',[(1,40)]),
 ('FunctionalCard','research-wiki/sampling-sde-library/cards/AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.md',[(1,26)]),
 ('Handoff','docs/companion-papers-handoff.md',[(1505,1520)]),
 # Honest incidental exposure; excluded from mathematical prerequisite expansion.
 ('INCIDENTAL-Gaussian-private','AutoSamplingTheory/TechnicalLemmas/Measure/GaussianConvolutionRegularity.lean',[(1,100),(247,277)]),
 ('INCIDENTAL-conditional-gradient','AutoSamplingTheory/ExampleCases/ProximalBPS/ConditionalGradient.lean',[(1,53)])]
pins=[]
for label,rel,ranges in selections:
 p=R/rel;b=p.read_bytes();ls=b.splitlines(keepends=True);row={'path':str(p),'raw_bytes':len(b),'raw_sha256':sha(b),'lf_sha256':sha(b.replace(b'\r\n',b'\n')),'fragments':[]}
 for a,z in ranges:
  f=b''.join(ls[a-1:z]);stem=f'{label}.{a}-{z}';(O/(stem+'.raw')).write_bytes(f);(O/(stem+'.lf')).write_bytes(f.replace(b'\r\n',b'\n'))
  row['fragments'].append({'physical_lines1':[a,z],'start_utf8_byte0':sum(map(len,ls[:a-1])),'end_utf8_byte0_exclusive':sum(map(len,ls[:z])),'snapshot':stem,'raw_sha256':sha(f),'lf_sha256':sha(f.replace(b'\r\n',b'\n')),'role':'EXCLUDED incidental exposure' if label.startswith('INCIDENTAL') else 'selected API/source context; definitions versus theorem contracts distinguished in source-contract'})
 pins.append(row)
# Opaque actual50 public contract, never reading new51 implementation (none exists).
p=R/'AutoSamplingTheory/ExampleCases/ProximalBPS/MacroscopicEnergy.lean';b=p.read_bytes();a=b.index(b'theorem actual_macroscopic_gradient_energy_blocks');z=b.index(b':= by',a);f=b[a:z]
(O/'actual50.public.raw').write_bytes(f);(O/'actual50.public.lf').write_bytes(f.replace(b'\r\n',b'\n'))
pins.append({'path':str(p),'raw_sha256':sha(b),'lf_sha256':sha(b.replace(b'\r\n',b'\n')),'scope':'whole hash identity; public header only now; prior whole-body50 reviewer exposure explicitly retained','public_raw_sha256':sha(f),'public_lf_sha256':sha(f.replace(b'\r\n',b'\n'))})
assert sha(b)=='4cd87c85f195774c4182894629e2f24efb3c1c1955447833d686d6826b5bab3a'
meta=[];ls=(R/'runs/substantive_advances.jsonl').read_bytes().splitlines()
for n in [180,181,182,843]:
 f=ls[n-1];x=json.loads(f);e=x.get('evidence',{});meta.append({'physical_line1':n,'advance_id':x['advance_id'],'to_state':x.get('to_state'),'verified_commit':e.get('verified_commit'),'historical_focused_weighted_raw_pin':e.get('focused_checks',[{}])[0].get('hashes',{}).get('AutoSamplingTheory/TechnicalLemmas/FunctionalInequalities/WeightedGradient.lean') if n==180 else None,'raw_row_sha256':sha(f),'scope':'status and exact parent pin only; no theorem approval or route prerequisite from prose'})
put('parent-status.selected.json',meta)
put('input-bindings.json',{'schema':'raw-LF-selected-preread51-v1','primary_before_api':json.loads((O/'primary-before-api.json').read_text()),'inputs':pins,'conventions':'Whole hashes identify files; only listed selected physical spans/public prefixes read as prerequisites. Lines one-based inclusive; UTF8 byte offsets zero-based start inclusive/end exclusive; LF replaces CRLF with LF only. No source graph coverage admission is attempted.'})
text('prospective-shape.txt','''SOURCE/API CANDIDATE SHAPE ONLY; not sealed, not compiled, not a named Lean declaration.
Suggested namespace/file: AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.GaussianMarginalGradient
Suggested name: gaussian_marginal_gradient_closable
Minimal imports: Measure.GaussianConvolutionRegularity; FunctionalInequalities.WeightedGradient.

{E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
[FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]
(μ : Measure E) [IsProbabilityMeasure μ] {η : ℝ} (hη : 0 < η) :
let J := (μ.prod (stdGaussian E)).map
  (fun p : E × E => (p.1, p.1 + Real.sqrt η • p.2))
let ν := J.snd
∃ D : Lp ℝ 2 ν →ₗ.[ℝ] Lp E 2 ν,
  Dense (D.domain : Set (Lp ℝ 2 ν)) ∧ D.IsClosable ∧ D.closure.IsClosed ∧
  ∀ (u : Lp ℝ 2 ν) (v : Lp E 2 ν), (u,v) ∈ D.graph ↔
    ∃ f : E → ℝ, ContDiff ℝ ∞ f ∧ HasCompactSupport f ∧
      u =ᵐ[ν] f ∧ v =ᵐ[ν] gradient f

No caller potential, exponential-integrability, closed-gradient, CFC, transport,
spectral-gap, Tf-domain, or desired-energy certificate is a binder.
Actual PBPS specialization uses μ=volume.tilted(-V) from actual50's probability output.
This is a generic background integration node with that exact consumer; not full B.13.
''')
contract={
 'mode':'source/API preread only; independent future51 uncertainty; no theorem credit',
 'decision':'RECOMMEND actual Gaussian outer-marginal dense closable compact gradient producer',
 'actual_consumer':'PBPS C.1 physical4573-4576 density/closedness sentence toward B.13 physical3779-3786; actual50 SAME literal μ/J/ν, not fiber S_y domain. Adds missing actualν domain producer to smooth50 energy; rough extension remains separate.',
 'primary_facts':{'B10':'3736-3747: Γ_P=(I-U_PP²)^(1/2) on H_P=ranP. Not I-A² on full joint L2.','B11':'3750-3757: U_perpP*U_perpP=Γ_P² and equality of norms.','B12':'3765-3773: ρ=(1-αη)/(1+αη), γgap=2sqrt(αη)/(1+αη); spectral lower bound independent.','B13':'3779-3786: f∈L2ν => U_PP f∈H1ν and 4η gradient norm² <= normdefect = Γnorm² = Bnorm².','C1':'4573-4576: source smooth compact reduction invokes density and closedness. 4662-4664 actual integrated normdefect consumer. Formula(C.2) in C.1; subsectionC.2 halfturn excluded.'},
 'source_extensions':['Source position R^d extended to finite-dimensional real Hilbert E, including rank0.','Generic arbitrary probability μ background producer is authored strengthening of actual Gibbs μ consumer; no source α/β restrictions are needed for this background closure. Actual50 retains α>0, α≤β, V C2, Hessian bounds, η>0, βη≤1.','No finite-dimensional assumption is transferred to Lp ℝ 2 J: for nontrivial positive-density laws it is infinite-dimensional even when E is finite-dimensional; rank0 is degenerate and included.'],
 'real_domains':{'D':'smooth compact genuine scalar gradient graph in L2ν × L2ν(E); densely defined closable linear partial map with closed closure.','not_claimed':'No equality between Differentiable+L2-gradient and weighted closure. No claim literal Tf belongs to D.closure. No full rough H1/T2/main/cost or Γ bound.','representative':'AE class equality permits mean/Lp transport only, never pointwise derivative transport.'},
 'producer_chain':['GaussianConvolutionRegularity.gaussian_convolution_potential_c2: actual add-noise law = positive density C Z, Z C2, W=-log(C Z) C2; μ probability and η>0 only.','WeightedGradient.compact_gradient_closable: W C1 and actual Integrable exp(-W) w.r.t.volume produce D for volume.tilted(-W).','Mathlib Measure.snd definition/map_map; withDensity_apply; lintegral_ofReal_ne_top_iff_integrable; ofReal_integral_eq_lintegral_ofReal; Measure.tilted definition identify actualν with this normalized tilt internally.'],
 'normalization':'C=((sqrt(2*pi*η))^-1)^finrank(E), Z(y)=∫exp(-||y-x||²/(2η))dμ. Positive actual density ρ=C Z, W=-logρ, exp(-W)=ρ pointwise including rank0. νprobability yields ∫ρdy=1 and Integrableρ; normalization denominator=1, so tilted density equals actualν. No α,β or energy coefficient in D target.',
 'route_at_most_7_steps':[
  '1. Map actualJ by snd; map_map gives actual Gaussian add-noise ν. μ probability and measurable add-noise give ν probability.',
  '2. Invoke actual Gaussian convolution potential C2 producer; set ρ=C Z>0 and W=-logρ.',
  '3. C2ρ/W gives measurable positiveρ and C1W; use massν=1 and withDensity_apply(univ) to get lintegral(ofRealρ)=1.',
  '4. lintegral_ofReal_ne_top_iff_integrable produces actual Integrableρ; ofReal_integral_eq_lintegral_ofReal and positivity give integralρ=1.',
  '5. exp(-W)=ρ and denominator1 identify volume.tilted(-W)=ν exactly. No caller normalizer or regularity premise.',
  '6. Invoke compact_gradient_closable W, transport measure equality; obtain actualD density/closability/closedclosure/exactgenuinegraph.'
 ],
 'Gamma_typed_boundary':{'available':'ContinuousLinearMap CStarRing over RCLike exists (Adjoint307); real operator positivity/order exists (Positive266,463-474); adjoint_comp_self positive (371). Existing joint block identities give B*B=P-A², a real nonnegative candidate.','missing':'Pinned CFC.exists_sqrt requires real nonunital continuous functional calculus; ordered CFC.sqrt also requires StarOrderedRing and NonnegSpectrumClass. Positive.lean459-491 explicitly says the StarOrderedRing instance remains future work, so Loewner PartialOrder is not that instance. Inspected real-selfadjoint CFC instance227-238 is derived from Algebra ℂ A + complexCFC; inspected CLM CStarAlgebra instance20-21 is complexHilbert only. Actual real L2(J) operator algebra has CStarRing but inspected chain does not supply these stronger instances.','alternative':'A genuine real-Hilbert positive-square-root construction/complexification adapter must be produced; cannot add caller Γ/CFC/spectral root certificate or use finite-dimensional spectral theorem on L2(J). No whole-Mathlib absence claim; no compiler instance search performed.'},
 'rough_domain_typed_boundary':{'available':'c1_in_closed_gradient147-154 accepts actual closableD/genuinegraph plus ContDiff ℝ1 f, MemLp f2 and MemLp gradientf2.','missing':'actual50 only Differentiable ℝ literalTf and L2 truegradient; neither this nor AE operator agreement supplies C1Tf or actual graph membership. After recommendedD edge, next real obligation is literalTf C1 for compactobserver (or direct distributional closure membership), then density/closed graph + smooth estimate extend T to allL2.','no_mirror':'No new cross-domain mechanism proposed; same Gaussian-smoothing/weighted-gradient source chain. No conceptual mirror self-validation.'},
 'exposure':[
  'Prior own49sourcegraph/whole-body49 and whole-body50/parent review exposure retained. Source/API50 originals CLOSED immutable. No51 implementation exists or was read; not freshblind.',
  'Current API locator accidentally printed GaussianConvolutionRegularity private prefixes1-100 and body context247-277; pinned as EXCLUDED incidental exposure. Current conditional-gradient first53 also includes beginning of existing parent proof; excluded as implementation prerequisite.',
  'Current WeightedC1 locator earlier emitted proof snippets174-217 and GaussianSmoothing first65/context; not promoted to exported contracts. Unavailable guessed filenames led to rg errors, then actual paths were resolved; no absence inferred.',
  'An overly broad rg against substantive_advances output huge historical metadata (truncated210725tokens), honestly retained as accidental metadata exposure; no proof/source verdict is inferred from it. Subsequent bounded JSON projection uses only actual parent IDs/status/pin.',
  'Memory registry553-554 used only repository truth-boundary/process orientation, not current mathematical evidence. No prior reviewer/blind/finalsource50 verdict read for this target.'
 ],
 'search_scope':['Actual FunctionalInequalities and PBPS filenames for Gaussian/Marginal/Outer gradient/Sobolev; scoped declarations for convolution or outer closability. No matching actual outer Gaussian marginal producer was returned; only existing Gaussian LSI filenames and irrelevant tilted AC contexts. No whole-library absence claim.','Exact Adjoint/Positive/CStarCLM/CFC Instances/Rpow Basic contracts; no proof search or instance compiler.','Actual module cards and bounded parent ledger projections confirm WeightedGradient historical focused3296 raw matches current c2495b6a and later VERIFIED/STABILIZING; GaussianConvolutionRegularity VERIFIED6e84711c. Parent status is provenance, not source mathematics.'],
 'remaining':'Statement/type/topology/implementation/independent verification all future. This capsule proposes one source-backed integration edge; no SAU/Goal/claim/source admission/compiler.',
}
put('source-contract.json',contract)
text('capsule.md','''Recommendation: produce the actual Gaussian outer marginal's dense closable smooth-compact gradient, with its closed graph closure. This is a substantive missing normalization/law-to-domain join, not a restatement of the smooth energy bound.

Primary fixed PBPSv1: C.1 lines4573–4576 explicitly uses density and gradient closedness for B.13 lines3779–3786. Existing gaussian_convolution_potential_c2 produces the actual marginal's positive C² potential for any probability μ, η>0. Existing compact_gradient_closable produces the true compact-gradient graph for an integrable C¹ Gibbs potential. Derive mass1, exp(-W)=ρ and tilted(-W)=ν internally; invoke those parents. Six-step source route and exact binders are in source-contract.json and prospective-shape.txt. No compiler or proof work was run.

This supplies an actual outer ν-domain, whereas old conditional_gradient_closable supplies fiber S_y domains. Actual50's μ/J/ν binds the immediate paper consumer. It does not yet put literal Tf into the closed graph, extend the estimate to rough all-L² input, or prove fullB.13.

The Γ option is larger: actual joint real L² operators have CStarRing and positivity, but the inspected pinned CFC producer chain requires a real CFC instance not supplied by its complex-Hilbert CStarAlgebra instance. Position dimension cannot make L²(J) finite-dimensional. The rough-domain option also remains incomplete: c1_in_closed_gradient needs C¹, while50 yields Differentiable+gradientL²; AE kernel agreement does not transfer pointwise derivatives.

Selected source/API raw/LF fragments and whole-file identity hashes are bound separately. Prior49/50 body exposure, current incidental parent snippets and accidental historical metadata output are disclosed. No new51 implementation exists. Generic probability input/finiteHilbert/rank0 are authored background extensions with the exactPBPS actual50 consumer, not new paper premises. FullΓ/H¹/halfturn/main/cost are excluded.
''')
# Bind exact exposure snippets omitted above, without treating them as mathematical contracts.
for label,rel,a,z in [('INCIDENTAL-C1body','AutoSamplingTheory/TechnicalLemmas/FunctionalInequalities/WeightedC1GradientDomain.lean',174,217),('INCIDENTAL-smoothing','AutoSamplingTheory/TechnicalLemmas/Measure/GaussianSmoothing.lean',1,65)]:
 p=R/rel
 if p.exists():
  b=p.read_bytes();f=b''.join(b.splitlines(keepends=True)[a-1:z]);(O/(label+'.raw')).write_bytes(f);(O/(label+'.lf')).write_bytes(f.replace(b'\r\n',b'\n'))
put('run.json',{'schema':'bounded-source-api-preread51-v1','mode':'source/API only','created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'primary_before_candidate_api':True,'outcome':'RECOMMEND_TRUE_OUTER_MARGINAL_GRADIENT_CLOSURE_INTEGRATION','source_graph_created':False,'proof_search':False,'compiler':'NOT_STARTED_CLOSED','declaration_created':False,'source_or_theorem_admission':False,'canonical_changes':False,'output_hash_recipe':'SHA256 exact raw bytes; LF hash CRLF->LF only; logical run hash whole run object minus run_sha256 sortedcompact UTF8 ensure_ascii=False. Lease final closure excluded from output manifest to avoid circular hash; parent receives actual final lease hash.','outputs':{p.name:{'raw_sha256':sha(p.read_bytes()),'lf_sha256':sha(p.read_bytes().replace(b'\r\n',b'\n')),'bytes':p.stat().st_size} for p in O.iterdir() if p.is_file() and p.name not in ['lease.json','run.json']}})
x=json.loads((O/'run.json').read_text());x['run_sha256']=sha(json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode());put('run.json',x)
print('CAPSULE',sha((O/'capsule.md').read_bytes()));print('CONTRACT',sha((O/'source-contract.json').read_bytes()));print('RUN',sha((O/'run.json').read_bytes()),'LOGICAL',x['run_sha256'])
# Final filesystem operation: actual lease closure, after every artifact read/write.
lease=json.loads((O/'lease.json').read_text());lease.update(status='CLOSED',read='CLOSED',write='CLOSED',python='CLOSED',compiler='NOT_STARTED_CLOSED',closed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),final_operation='This actual lease closure is final filesystem write; no filesystem reads after closure.')
closed=(json.dumps(lease,ensure_ascii=False,indent=2)+'\n').encode();(O/'lease.json').write_bytes(closed)
print('CLOSED_LEASE_RAW_LF',sha(closed))
