from pathlib import Path
import json,hashlib,re
R=Path('E:/Samplinglib');O=Path(__file__).resolve().parent;RUN=O.parent;P=R/'runs/20261007-companion-priority/pbps-normalized-endpoint-preread104'
M=R/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualNormalizedEndpointSector.lean'
sha=lambda b:hashlib.sha256(b).hexdigest()
def load(p):return json.loads(Path(p).read_bytes())
def info(p):return dict(path=p.relative_to(R).as_posix(),raw_sha256=sha(p.read_bytes()),bytes=p.stat().st_size)
def save(n,v):
 p=O/n;assert not p.exists();p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
prepared=load(O/'prepared-inputs104.native.json')
for x in prepared['inputs']:assert info(R/x['path'])==x,x['path']
kernel=load(O/'fresh-kernel-receipt104.native.json');assert kernel['exit_code']==0 and kernel['terminal_closed']
out=(O/'fresh-kernel.stdout.log').read_text(encoding='utf-8')
axioms=re.findall(r"'([^']+)' depends on axioms:\s*\[([^]]*)\]",out)
assert len(axioms)==2 and all({x.strip() for x in a.split(',')}=={'propext','Classical.choice','Quot.sound'} for _,a in axioms),axioms
root=RUN/'focused104/production1';receipt=load(root/'receipt.json');assert receipt['exit_code']==0 and receipt['terminal_closed'];assert receipt['input_raw_sha256']==sha(M.read_bytes());assert (root/'input.exactraw.lean').read_bytes()==M.read_bytes()
assert load(O/'fake-closure-scan104.native.json')['decision']=='PASS'
raw=M.read_bytes();lines=raw.splitlines(keepends=True)
spec=[(1,19,'Imports and namespace; only actual102/103 imports, public93/97 available transitively.'),(20,97,'Private literal proposition exactly equals original Header104 and seal; six original assumptions, 25 outer plus five inner definitions.'),(98,115,'One public theorem with exactly those six assumptions; no helper/provider premises.'),(116,129,'Public97/public102 extracted with identical original assumptions. Coordinate extensionality identifies existential time witnesses before using endpoint and weighted laws.'),(130,142,'Actual endpoint A and Theta measurable by explicit parameter embedding; B,J measurable; B o Theta = J o B from actual97 endpoint inverse.'),(143,150,'Public93 actual joint rho measurability extracted at exact conjunction position and specialized with same embedding.'),(151,172,'Literal Delta measurable from all finite ordered-coordinate inequalities and terminal bounds. map_comap_subtype_coe identifies restriction; SigmaFinite.of_map discharges product measure side condition internally.'),(173,190,'Actual target energy and partition inverse, measurable Gibbs and weighted densities; public103 last conjunct is exactly the normalized phase density equality.'),(191,200,'sigma equals (ell.prod m).withDensity(cNorm*W), using product density and density multiplication with both factors measurable; reassociation only.'),(201,216,'Explicit internal hsector: measurable Theta and map equality via all measurable ENNReal test functions; density formula and lintegral_const_mul transfer actual102 identity with no finite mass/integral premise.'),(217,len(lines),'Actual endpoint pushforward preserved by J using map_map twice and pointwise intertwining, then hsector.map_eq; public theorem axiom print and namespace closure.')]
regions=[]
for a,b,note in spec:
 bts=b''.join(lines[a-1:b]);regions.append(dict(line_start=a,line_end=b,raw_sha256=sha(bts),bytes=len(bts),review=note))
save('reviewed-code-regions104.native.json',dict(production=info(M),regions=regions,full_module_covered=True))
trials=[]
for d in sorted((RUN/'focused104').iterdir()):
 p=d/'receipt.json'
 if p.exists():
  v=load(p);trials.append({'name':d.name,'receipt':info(p),'exit_code':v.get('exit_code'),'artifacts':[info(x) for x in sorted(d.iterdir()) if x.is_file()]})
save('whole-math-decision104.native.json',{
 'decision':'ACCEPT_WHOLE_MATHEMATICS_AND_EXACT_SEALED_KERNEL','reviewer':'/root/exact_verifier96','production':info(M),'header':info(P/'Header104.lean'),'seal':info(P/'root.statement-seal104.json'),'fresh_kernel':info(O/'fresh-kernel-receipt104.native.json'),'root_terminal_production':info(root/'receipt.json'),
 'kernel_contract':{'production_prefix_exact_bytes':True,'target_module_not_imported':True,'original_header_candidate_present':True,'witness_checks_expanded_Prop':True,'axioms':[{ 'declaration':n,'axioms':[x.strip() for x in a.split(',')]} for n,a in axioms],'no_sorryAx':True},
 'whole_module_ownership':'Exactly one private statement definition and one public theorem. Every local have/let lies inside the public proof. No hidden private producer API, generic provider hypothesis or extra theorem is exported.',
 'genuine_direct_parents':[
 {'declaration':'ActualEndpointTimeReversal.actual_endpoint_time_reversal_laws','use':'Same public witness coordinates; actual endpoint and Theta joint measurability; endpoint inverse.'},
 {'declaration':'ActualWeightedSector.actual_weighted_sector_lintegral','use':'All measurable ENNReal weighted tests for its coordinate-defined reversal, aligned before use.'},
 {'declaration':'ActualFiniteCountPath.actual_finite_count_path_law','use':'Joint actual prescribed density measurability.'},
 {'declaration':'ActualPhaseNormalization.actual_phase_gibbs_normalization','use':'Actual normalized Gibbs density equals piY.prod stdGaussian. Its upstream positivity and finiteness justify actual normalization;104 uses the equality directly and needs no new finiteness argument.'}],
 'assumption_audit':'All four public calls receive exactly hAlpha,hAlphaBeta,hV,hH,hEta,hBetaEta from sealed statement. No additional source condition or positive dimension/event/rate assumption.',
 'mathematical_findings':[
 'Exact actual density q times terminal survival and actual Gamma(T), position-first phase measure and phase-first simplex product preserved.',
 'Subtype witness equality is coordinatewise and simultaneous for all parameters; no use of measure preservation alone to identify coordinates.',
 'The finite strict-simplex measurability proof handles proof-indexed intersections and Fin0. Restriction volume is sigma-finite, and the measurable subtype map transfers this property back to exact comap volume.',
 'Internal sigma rewrite preserves the precise partition inverse, target energy and multiplication order. All withDensity product and nested density measurability conditions are supplied.',
 'Internal hsector proves stable SECTOR100 rather than bypassing it; both nonnegative integrals can be infinite, since constant multiplication and equality transport need no cancellation.',
 'Actual97 gives the second coordinate of B(Theta x)=J(B x); the first is definitional. Two measurable map compositions then prove the exact endpoint-pair measure preservation.',
 'No countable sector summation, finite-sector probability normalization, signed integral exchange or full process invariance is asserted.'
 ],
 'edge_cases':{'n0':'Empty coordinate function/extensionality and empty products remain valid; no positivity of count assumed.','T0_npositive':'Empty strict simplex and zero sector measures; no chosen tuple, inverse sector mass or nonempty assumption.','T0_n0':'Actual endpoint equals initial state; flipped diagonal follows same uniform proof.','rank0':'All finite-dimensional volume/Gaussian producers include dimension zero; no determinant/rank division introduced.','zero_normal_or_rate':'Literal total reflection and nonnegative actual density unchanged; never divide by rate or density.','infinite_tests':'ENNReal all-test equality, with no finite-integral assumption or subtraction.'},
 'warning':'Only harmless letI-versus-let proposition-instance style suggestion. No mathematical or kernel issue; no cosmetic production change requested.',
 'retained_failures':trials,'failure_scope':'Earlier error-bearing scratch attempts that print sorryAx are negative compiler evidence, not accepted proofs. Only final exact production and fresh kernel witness have standard three axioms.',
 'reused_header_topology':info(P/'independent-header-math104/closed-RAW-review104.native.json'),'code_regions':info(O/'reviewed-code-regions104.native.json'),'fake_closure':info(O/'fake-closure-scan104.native.json'),'defects':[],'source_review_verdict_issued':False,'publication_used':False,'VERIFIED_transition':False,
 'remaining':'Mathematical acceptance only. Independent final source/decoder/publication review and frozen exact science commit admission remain; no integration/main/purification/full-paper claim.'})
inputs={x['path']:x for x in prepared['inputs']}
for trial in trials:
 for x in trial['artifacts']:inputs[x['path']]=x
save('closed-RAW-manifest104.native.json',{'kind':'closed independent whole mathematical and kernel review','reviewer':'/root/exact_verifier96','inputs':list(inputs.values()),'outputs':[info(p) for p in sorted(O.iterdir()) if p.is_file()],'no_shared_mutations':True,'no_new_primary_archive':True,'VERIFIED_transition':False})
for n in ['whole-math-decision104.native.json','fresh-kernel-receipt104.native.json','closed-RAW-manifest104.native.json']:print(n,info(O/n)['raw_sha256'])
