from pathlib import Path
import hashlib,json,re,datetime,subprocess
R=Path('E:/Samplinglib');O=Path(__file__).resolve().parent;P=O.parent;N=P.parent/'pbps-actual-endpoint-time-reversal97/next-primary98'
sha=lambda b:hashlib.sha256(b).hexdigest();load=lambda p:json.loads(p.read_bytes())
def info(p):return dict(path=p.relative_to(R).as_posix(),raw_sha256=sha(p.read_bytes()),bytes=p.stat().st_size)
def write(n,v):
 p=O/n;assert not p.exists();p.write_bytes((json.dumps(v,ensure_ascii=False,indent=2)+'\n').encode())
H=P/'Header98.lean';h=H.read_text(encoding='utf8');assert info(H)['raw_sha256']=='50c6999fe069f4cf648832a804b71bb8e447b7a3aea0f0c42a836f81650c6ad0'
H97=P.parent/'pbps-endpoint-time-reversal-preread97/Header97.lean';old=H97.read_text(encoding='utf8')
bind=lambda t:t[t.index('{E : Type*}'):t.index(': Prop := by')].strip()
assert bind(h)==bind(old)
def let(t,name):
 s=re.search(r'^    let '+re.escape(name)+r'\s',t,re.M);assert s,name
 e=re.search(r'^    (?:let |∀ )',t[s.end():],re.M);return t[s.start():s.end()+e.start()].strip()
names=['c','Φ','S','Rec','Hist','Δ','Prefix','m','zAt','K','Path','Ψ','Γ']
for n in names:assert let(h,n)==let(old,n),n
f=P/'typechecks98/type-only1';rc=load(f/'receipt.json');assert rc['exit_code']==0 and rc['terminal_closed'] and rc['input_raw_sha256']==info(H)['raw_sha256'] and (f/'input.exactraw.lean').read_bytes()==H.read_bytes() and not (f/'stderr.log').read_bytes()
prod94=R/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualPrescribedPathDensity.lean';t94=prod94.read_text(encoding='utf8')
clamp='⟨min (Real.toNNReal s) T, min_le_right _ _⟩';assert clamp in h and clamp in t94
assert 'Γ y r z n T t '+clamp in h and 'Γ y xRef z₀ n T t '+clamp in t94
G=N/'source-proof-graph98.v2.native.json';g=load(G);edges={(x['from'],x['to']) for x in g['edges']}
assert ('B98','WEIGHT99') not in edges
required={('H98','DARC98'),('U98','DARC98'),('FLOW','DARC98'),('RATE','DARC98'),('U98','B98'),('BOUNCE','B98'),('DARC98','IARC98'),('RATE','IARC98'),('FLOW','IARC98'),('PATH93','RINT98'),('RATE','RINT98'),('FLOW','RINT98'),('IARC98','FINITE98'),('B98','FINITE98'),('PATH93','FINITE98'),('TERM97','FINITE98'),('RINT98','FINITE98'),('FORWARD94','FINITE98')}
assert required<=edges and all(not x['certified_lean_edge'] for x in g['edges'])
cov=load(N/'source-coverage98.native.json');primary=R/cov['primary']['path'];pb=primary.read_bytes();assert sha(pb)==cov['primary']['raw_sha256']
regions=[];slices=O/'primary-regions';slices.mkdir()
for x in cov['regions']:
 raw=pb[x['byte_start']:x['byte_end_exclusive']];assert sha(raw)==x['raw_sha256'],x['id']
 q=slices/(x['id']+'.raw.html');q.write_bytes(raw);regions.append(dict(**x,snapshot=info(q)))
api=['Analysis/Calculus/Deriv/Comp.lean','Analysis/InnerProductSpace/Calculus.lean','Analysis/Calculus/Gradient/Basic.lean','MeasureTheory/Integral/IntervalIntegral/FundThmCalculus.lean','MeasureTheory/Integral/IntervalIntegral/Basic.lean']
prods=['ActualHarmonicFlow','ActualBounceRate','ActualFiniteCountPath','ActualPrescribedPathDensity','ActualPhaseReversalVolume','ActualEndpointTimeReversal']
paths=[H,H97,f/'receipt.json',f/'input.exactraw.lean',f/'stdout.log',f/'stderr.log',N/'next-edge-recommendation98.native.json',N/'source-first-reconstruction98.native.json',N/'source-coverage98.native.json',N/'reuse-search98.native.json',G,N/'closed-raw-addendum98.native.json',N/'closed-raw-manifest98.native.json',R/'lean-toolchain',R/'lake-manifest.json']+[R/'AutoSamplingTheory/ExampleCases/ProximalBPS'/(n+'.lean') for n in prods]+[R/'.lake/packages/mathlib/Mathlib'/p for p in api]
inp=O/'inputs';inp.mkdir();inputs=[]
for i,p in enumerate(paths):
 q=inp/(str(i).zfill(2)+'.'+p.name+'.exactraw');q.write_bytes(p.read_bytes());inputs.append(dict(**info(p),snapshot=q.relative_to(R).as_posix()))
route=[
 'Consume actual harmonic coordinate derivatives/continuity and actual bounce position/norm and continuous rate laws under the six original assumptions.',
 'Differentiate target U along Phi using V chain rule and norm-square derivatives; cancel the centered force to obtain sqrt(eta)<p,grad V(x)-grad V(r)>=rate(z)-rate(Rz). Prove U and exp(-U) invariant under S and R.',
 'Use continuous arc rates and oriented FTC to obtain target-energy increments on each deterministic real arc.',
 'Identify the exact clamped actual Gamma with translated continuous arcs on each open grid interval using the public93 interpolation law. Apply finite adjacent-interval integration to the reversed rate; consume94 for forward integrability/sum.',
 'Telescope the n+1 arc energy increments through actual zAt, cancel bounce energy changes, and use Phi0 plus actual97 terminal Gamma identity to identify the two endpoints.',
 'Subtract the two finite hazard sums and use exp_add with -U(z)-Iplus=-U(A)-Iminus to prove the exact homogeneous Gibbs/survival identity.',
 'Keep reversed-path survival identification, event-product pairing, weighted sector substitution and normalized invariance as separate later obligations.'
]
checks=[
 dict(topic='six binders and original literals',result='PASS',details='Structural and six analytic binders match Header97 byte-for-byte as decoded text; all13 c/Phi/S/Rec/Hist/Delta/Prefix/m/zAt/K/Path/Psi/Gamma let declarations text-identical. No provider assumption added. R is explicit momentum negation; rate is actual sqrt eta positive-part gradient defect. Clamp agrees with94 up to bound-variable names.'),
 dict(topic='target energy versus harmonic energy',result='PASS',details='U=V(x)+norm(x-y)^2/(2 eta)+norm(p)^2/2 is source3.1 target negative log density up to a constant, not the conserved centered H(y,r). From dx=sqrt eta p and dp=-(x-y)/sqrt eta-sqrt eta grad V(r), dU=sqrt eta inner(p,grad V(x)-grad V(r)). SourceA4 is derivative log nu=-dU; Header energy sign is therefore positive Iplus-Iminus.'),
 dict(topic='positive-part identity and exponential sign',result='PASS',details='rate(Rz)=sqrt eta max(0,-a), so rate(z)-rate(Rz)=sqrt eta a for every real a. U(A)-U(z)=Iplus-Iminus gives -U(z)-Iplus=-U(A)-Iminus, hence the stated exp-product equality. Neither U>=0 nor rate>0 nor finite normalizer is needed.'),
 dict(topic='piecewise path and intervals',result='PASS_FEASIBLE',details='The actual path is post-bounce and may be discontinuous at finite event times. Equality to each continuous arc is only required on Ioo. Lebesgue interval integrals ignore finite endpoints; congr_uIoo and integral_congr_Ioo_of_le support integrability/equality. m is retained exactly although this pointwise target does not integrate over m. The clamp affects no time in [0,T]. Reversal of the entire right-continuous path is not needed for98.'),
 dict(topic='producer limitations',result='PASS_WITH_EXPLICIT_NEW_OBLIGATIONS',details='Public94 supplies forward rate integrability/sum only. Its private arc_integral/finite_arc_integral/actual_arc cannot be imported by their source names. R-rate whole-path integrability and energy telescoping are genuinely new finite adapters; use public93 live-arc law or a separately justified shared extraction. Public97 provides terminal identity but its full product-volume result is not a premise of98.'),
 dict(topic='zero cases',result='PASS',details='n0 has one arc and empty tuple. T0,n0 gives A=z and zero integrals. T0,n>0 admits no strict tuple. Rank0 has U=V(0), which may be nonzero or negative, but constant phase and zero rates/increment. Zero reflection normal gives S=id and rate0 at that phase, without a nonzero-normal or positive-event premise. Norm-square derivative works at zero vectors.'),
 dict(topic='pinned APIs and feasibility',result='PASS_FEASIBLE_NOT_PROVED',details='Confirmed HasFDerivAt.comp_hasDerivAt, HasDerivAt.norm_sq, inner_gradient_left/right, intervalIntegral.integral_eq_sub_of_hasDerivAt, integral_comp_sub_right, integral_congr_Ioo_of_le and the existing94 finite adjacent-arc proof. ContDiff2 implies the needed V differentiability/gradient continuity. Eta>0 supplies sqrt positivity and (sqrt eta)^2=eta. No further analytic assumption identified.')
]
write('header-math-decision98.native.json',dict(kind='independent-prospective-header-mathematical-review',reviewer='/root/exact_verifier96',decision='ACCEPT_EXACT_HEADER98_AS_MATHEMATICALLY_CORRECT_AND_FEASIBLE',header=info(H),checks=checks,required_header_repairs=[],six_original_binders_exact=True,thirteen_literal_definitions_exact=names,clamp94_alpha_equivalent=True,type_only_evidence=info(f/'receipt.json'),type_only_reused_without_duplicate_build=True,proof_route_max7=route,strictly_smaller_exact_dependency=dict(name='Actual A4 target-energy harmonic-arc balance',statement='Under exactly the same six binders and literal U/Phi/rate/S/R: U(Sz)=U(z), U(Rz)=U(z); for every real s HasDerivAt (u -> U(Phi_u z)) (rate(Phi_s z)-rate(R(Phi_s z))) s; for every a,b both arc rates are IntervalIntegrable and U(Phi_b z)-U(Phi_a z)=integral_a^b(rate(Phi_s z)-rate(R(Phi_s z))).',consumer='Finite98 actual prescribed survival balance',reason='Strictly removes the new sourceA4 calculus/FTC substrate without pretending that94 exports the reversed-rate adapter.',failure_policy='After repeated same-shape finite adapter failures, diagnose and split at this exact boundary; do not insert derivative/integrability/path-provider hypotheses.'),inputs=inputs,primary=info(primary),source_regions=regions,scope='Prospective mathematical judgment only. No implementation, Statement Seal, SAU claim, proof certificate, source final admission or VERIFIED transition. Independent topology decision is separate.',observed_head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=R,text=True).strip()))
write('graph-v2-negative98.native.json',dict(kind='independent-source-graph-validation',reviewer='/root/exact_verifier96',review_mode='independent validation, not blind reconstruction; own pregraph reasoning was recorded after source-only recommendation/primary and before graph inspection',graph=info(G),header=info(H),decision='FINITE98_SUBGRAPH_ACCEPTED_DOWNSTREAM_WEIGHT99_EDGE_REPAIR_REQUIRED',bounded98_required_edges_present=sorted([list(e) for e in required]),missing_edges=[dict(from_node='B98',to_node='WEIGHT99',projection='U/w invariance under momentum reversal R',reason='FINITE98 exports w(z) exp(-Iplus)=w(A) exp(-Iminus), whereas WEIGHT99 compares Gibbs times density at Theta phase R(A). It also requires w(R(A))=w(A). The R-invariance part of B98 is not a conclusion of the current FINITE98 header, so B98->FINITE98 does not deliver that ingredient to WEIGHT99.',effect='Graph-only correction; Header98 unchanged; later weighted theorem remains unproved')],later_scope_caution='INV99 and L2EXT are schematic future obligations, not approved complete proof plans. When promoted, expose T_t(1)=1 and nu momentum-reversal invariance used by F=1, plus the actual density/contraction/continuity contracts for L2. This is not a new98 prerequisite.',no_source_credit=True,no_self_authored_graph=True))
for x in inputs:assert sha((R/x['path']).read_bytes())==x['raw_sha256']
write('closed-RAW-manifest98.native.json',dict(kind='closed-independent-header98-mathematics-and-v2-negative-topology',hash_recipe='SHA256 of exact original bytes without newline normalization',self_hash_omitted=True,inputs=inputs,primary=info(primary),files=[info(p) for p in sorted(O.rglob('*')) if p.is_file()]))
for n in ['header-math-decision98.native.json','graph-v2-negative98.native.json','closed-RAW-manifest98.native.json']:print(json.dumps(info(O/n)))
