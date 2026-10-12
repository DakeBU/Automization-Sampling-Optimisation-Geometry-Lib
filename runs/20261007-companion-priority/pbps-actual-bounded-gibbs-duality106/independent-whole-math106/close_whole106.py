from pathlib import Path
import json,hashlib,re
R=Path('E:/Samplinglib');O=Path(__file__).resolve().parent;B=O.parent
P=R/'runs/20261007-companion-priority/pbps-bounded-gibbs-duality-preread106'
M=R/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualBoundedGibbsDuality.lean'
sha=lambda b:hashlib.sha256(b).hexdigest()
def info(p):return dict(path=p.relative_to(R).as_posix(),raw_sha256=sha(p.read_bytes()),bytes=p.stat().st_size)
def load(p):return json.loads(p.read_bytes())
def save(n,v):
 p=O/n;assert not p.exists();p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
prep=load(O/'prepared-inputs106.native.json')
for x in prep['inputs']:assert info(R/x['path'])==x
k=load(O/'fresh-kernel-receipt106.native.json');assert k['exit_code']==0 and k['terminal_closed']
axes=re.findall(r"'([^']+)' depends on axioms:\s*\[([^]]*)\]",(O/'fresh-kernel.stdout.log').read_text(encoding='utf-8'))
assert len(axes)==2 and all({a.strip() for a in v.split(',')}=={'propext','Classical.choice','Quot.sound'} for _,v in axes)
root=B/'focused106/production1';r=load(root/'receipt.json');assert r['exit_code']==0 and r['terminal_closed'] and r['module_raw_sha256']==info(M)['raw_sha256']
assert (root/'input.exactraw.lean').read_bytes()==M.read_bytes()
assert load(O/'fake-closure-scan106.native.json')['decision']=='PASS'
lines=M.read_bytes().splitlines(keepends=True)
regions=[(1,11,'Imports, namespace and options; actual105 and unit-clock imports.'),(12,147,'Private exact sealed literal proposition, six original analytic binders,37 actual lets, one global witness and all identification clauses; bounded observables occur only within the conclusion.'),(148,163,'One public theorem with original binders; unfolds only its own private statement and introduces exact literal definitions.'),(164,168,'Extracts105 once and returns the SAME global Z, joint measurability, raw-arc/fallback and parameterwise zero-time law before y,r,T.'),(169,185,'Public103 transfers probability to literal nu; unit-clock producer supplies P probability. Explicit measurable embedding gives endpoint and M measurability. Actual Q,J are literal105 objects with its probability and preservation projections.'),(186,193,'Actual momentum R is measurable and preserves nu by stdGaussian_map for negation isometry and product-map equality. Position tilt untouched; no symmetry hypothesis.'),(194,204,'Direct marginal proof: M maps input measure to Q, fst maps Q to nu using P mass1. Compose R, fst, J, M; double negation gives endpoint pointwise, yielding actual endpoint MeasurePreserving.'),(205,219,'Internal htest for bounded real measurable F,G. Product H has measurable bound CF*CG, hence genuine product Integrable. Integrable.integral_prod_left and integral_const_mul give outer L1; no arbitrary integrability provider.'),(220,228,'Measurable pair test and signed integral_prod with hHi identify outer integral with Q integral via measurable map M. Integral_map is used with its real AEStronglyMeasurable contract.'),(229,243,'Apply htest to F,G and G composed R,F composed R with exchanged bounds. Return both L1 conclusions. J map equality plus real integral_map transforms pair test; multiplication commutativity gives the exact required flipped-duality ordering.'),(244,247,'Public axiom print and namespace closure; no further theorem/helper export.')]
assert regions[0][0]==1 and regions[-1][1]==len(lines)
for a,b in zip(regions,regions[1:]):assert a[1]+1==b[0]
save('reviewed-code-regions106.native.json',{'production':info(M),'full_module_covered':True,'regions':[dict(line_start=a,line_end=b,raw_sha256=sha(b''.join(lines[a-1:b])),bytes=len(b''.join(lines[a-1:b])),review=t) for a,b,t in regions]})
trials=[]
for d in sorted((B/'focused106').iterdir()):
 p=d/'receipt.json'
 if p.exists():trials.append({'name':d.name,'receipt':info(p),'exit_code':load(p).get('exit_code'),'artifacts':[info(x) for x in sorted(d.iterdir()) if x.is_file()]})
save('whole-math-decision106.native.json',{
 'decision':'ACCEPT_WHOLE_MATHEMATICS_AND_EXACT_SEALED_KERNEL','reviewer':'/root/exact_verifier96','production':info(M),'header':info(P/'Header106.lean'),'seal':info(P/'root.statement-seal106.json'),'fresh_kernel':info(O/'fresh-kernel-receipt106.native.json'),'root_terminal_production':info(root/'receipt.json'),
 'kernel_contract':{'production_prefix_exact_bytes':True,'target_module_not_imported':True,'original_header_candidate_present':True,'literal_header_seal_privateProp_equal':True,'witness_checks_expanded_Prop':True,'axioms':[{'declaration':n,'axioms':[a.strip() for a in v.split(',')]} for n,v in axes],'no_sorryAx':True},
 'whole_module_ownership':'Exactly one private statement and one public theorem. htest and all have/let objects are internal; no mangled private producer access or additional public provider.',
 'genuine_direct_parents':[{'declaration':'ActualCountableEndpointLaw.actual_countable_endpoint_law','use':'Same global actual Z and its complete identification contract; exact endpoint Q probability and J preservation.'},{'declaration':'ActualPhaseNormalization.actual_phase_gibbs_normalization','use':'Actual normalized phase probability transported through exact phase-product equality.'},{'declaration':'UnitExponentialProduct.unit_exponential_product_laws','use':'Probability of exact P, discharging finite/SFinite products and the first-marginal mass-one identity.'}],
 'assumption_audit':'All parameterized actual parents receive exactly the original six analytic assumptions. Measurable/bounded F,G and CF,CG are precisely sealed observable hypotheses, nested after the single global witness. No new count, normalizer, positivity, integrability, arbitrary process, kernel or phase-symmetry premise.',
 'mathematical_findings':[
  'One extraction from105 supplies Z before parameter specialization. No independent93/83 process witness is introduced or identified.',
  'nu remains literal tilted position times standard Gaussian momentum. Public103 supplies probability; negation linear isometry plus product map independently proves actual R symmetry in every dimension.',
  'The direct marginal composition is R o fst o J o M = endpoint. Its domains and measures align: input -> Q -> Q -> nu -> nu. P probability makes fst_*Q=nu. Double momentum negation is pointwise, with no path reversal or extra AE assertion.',
  'The bounded product integrand H(z,w)=F(z)G(endpoint(z,w)) is genuinely integrable under nu.prod P. Its absolute value is bounded by CF*CG. The outer integral is integrable by the product-integral theorem, then factored by integral_const_mul. Sections are also bounded measurable on finite P; no totalized-integral shortcut is used to justify Fubini.',
  'Signed Fubini is invoked with hHi. The real pair test is measurable, so integral_map applies to M and J without any unjustified measurable-embedding hypothesis.',
  'The right htest exchanges bounds and uses G composed R,F composed R. The final J action gives F(Rend)G(Rstart), commuted into G(Rstart)F(Rend), exactly matching the sealed right side.',
  'Both outer L1 conclusions are established before integral equality. Probability of Q is true via105; the proof does not introduce finiteness as an observable premise.',
  'No signed count-series exchange is repeated. No equality with83 kernel, restart, semigroup, L2/operator extension, convergence or complete-paper result is asserted.'
 ],
 'selected_invariance_route':{'receipt':info(B/'selected-invariance-route106.json'),'mathematical_status':'ACCEPT_DIRECT_MARGINAL_ALTERNATIVE','formula':'R composed fst composed J composed M = endpoint','source_relation':'The printed F=1 route follows from the independently proved bounded duality, but is not the actual Lean dependency of hinvariant.'},
 'source_graph_followup':{'status':'REQUIRES_APPEND_ONLY_SELECTED_ROUTE_EDGE_BEFORE_FINAL_COMPILED_COVERAGE','missing_selected_direct_edge':['ENDPOINT-LAW105','INV100'],'reason':'Prospective62-node122-edge graph permitted direct marginal alternative in prose but its INV100 incoming incidences use AVG100, clock, COUNT93, NORM and PHASE-FLIP106. Actual selected hinvariant directly consumes105 endpoint law; make that direct ingredient explicit without deleting printed AVG100-to-INV100 source route.','reported_to_root':True,'production_or_header_change_needed':False,'scope':'Metadata/topology coverage followup, not a mathematical defect or replacement of the original header/topology audit.'},
 'edge_cases':{'rank0':'Negation isometry, normalized Gaussian and product map include zero dimension. No rank division.','T0':'Same inherited parameterwise P-a.e. zero-time identity returned. Distributional endpoint invariance uses105 and is valid without a uniform all-z null event.','zero_bounds':'Bounds may vanish. No division by CF,CG, rates, sector mass or density.','zero_rate_or_infinite_wait':'Total actual process/reflection/stopping/fallback unchanged.','jumps':'Fixed-time law only, with inherited right-continuous covering convention. No pathwise reversal at jumps.','signed_observables':'Negative values allowed; global finite real bounds and product probability provide honest L1/Fubini.'},
 'warnings':'Unused binder and proposition letI style warnings are nonmathematical; no cosmetic proof changes requested.',
 'retained_failures':trials,'failure_scope':'Assembly1 API/elaboration failures retained as negative evidence. Assembly2, exact production and fresh expanded sealed witness pass with standard three axioms.',
 'code_regions':info(O/'reviewed-code-regions106.native.json'),'fake_closure':info(O/'fake-closure-scan106.native.json'),'defects':[],'publication_used':False,'source_review_verdict_issued':False,'VERIFIED_transition':False,
 'remaining':'Selected-route graph overlay and independent final source/decoder/publication review, then frozen exact-science admission. No shared integration, main/purification/browser or whole-paper credit.'})
inputs={x['path']:x for x in prep['inputs']}
for t in trials:
 for x in t['artifacts']:inputs[x['path']]=x
save('closed-RAW-manifest106.native.json',{'kind':'closed independent whole mathematical and exact kernel review','reviewer':'/root/exact_verifier96','inputs':list(inputs.values()),'outputs':[info(p) for p in sorted(O.iterdir()) if p.is_file()],'no_shared_mutations':True,'no_new_primary_archive':True,'VERIFIED_transition':False})
for n in ['whole-math-decision106.native.json','fresh-kernel-receipt106.native.json','closed-RAW-manifest106.native.json']:print(n,info(O/n)['raw_sha256'])
