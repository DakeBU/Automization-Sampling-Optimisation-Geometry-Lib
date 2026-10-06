import pathlib,json,hashlib,re,subprocess,sys,datetime
root=pathlib.Path('.');run=root/'runs/20261007-companion-priority/positive-step-proximal-rgo'
sha=lambda b:hashlib.sha256(b).hexdigest()
def rec(p):
 b=pathlib.Path(p).read_bytes()
 return {'path':str(p).replace('\\','/'),'raw_sha256':sha(b),'lf_sha256':sha(b.replace(b'\r\n',b'\n')),'bytes':len(b)}
base=subprocess.check_output(['git','rev-parse','HEAD']).decode().strip()
assert base=='2cde5ce8753272af91fc1b1c613c16edd9a15265'
freeze=json.loads((run/'math-freeze.json').read_text(encoding='utf8'))
inputs=[]
for i,x in enumerate(freeze['inputs']):
 rr=rec(x['path']);assert all(rr[k]==x[k] for k in ['raw_sha256','lf_sha256','bytes']),(x['path'],rr,x)
 snap=run/f'reviewer.math-input.{i:03d}.raw.snapshot'
 assert snap.read_bytes()==pathlib.Path(x['path']).read_bytes()
 inputs.append(dict(rr,reviewer_snapshot=str(snap).replace('\\','/'),scope='context-only-not-decoder-proof-evidence' if i in [13,14,15,16,17,18] else 'reviewed-stable-input'))
sys.path.insert(0,'tools');import astis
todo=['Tests/FullRangeProximalGaussianOracle.lean','Tests/StandardizedRGOPositionFisher.lean'];seen=set();hits=[]
while todo:
 p=todo.pop()
 if p in seen:continue
 seen.add(p)
 for m in re.findall(r'^\s*import\s+((?:AutoSamplingTheory|Tests)\S+)\s*$',pathlib.Path(p).read_text(encoding='utf8'),re.M):
  q=m.replace('.','/')+'.lean'
  if pathlib.Path(q).exists():todo.append(q)
for p in sorted(seen):
 s=astis.strip_lean_comments_and_strings(pathlib.Path(p).read_text(encoding='utf8'))
 for i,l in enumerate(s.splitlines(),1):
  if astis.FORBIDDEN_REGEX.search(l):hits.append({'path':p,'line':i,'text':l})
assert not hits
seal=json.loads((run/'preproof/statement-seals.accepted.json').read_text(encoding='utf8'))
sigchecks=[]
for x,p in zip(seal['signatures'],[freeze['inputs'][0]['path'],freeze['inputs'][1]['path']]):
 text=pathlib.Path(p).read_text(encoding='utf8');name=x['full_declaration'].split('.')[-1]
 sig=text[text.index('theorem '+name):].split(' := by',1)[0].rstrip()
 assert sig==x['signature_text'];assert sha(sig.encode())==x['signature_lf_sha256']
 prior=(run/'prior-version'/p.replace('/','__')).with_name(p.replace('/','__')+'.raw.snapshot')
 old=prior.read_text(encoding='utf8');old_sig=old[old.index('theorem '+name):].split(' := by',1)[0].rstrip()
 assert old_sig.replace(' (hsmall : ∀ s, eta s ≤ 1)','')==sig
 sigchecks.append({'declaration':x['full_declaration'],'signature_lf_sha256':sha(sig.encode()),'prior_signature_lf_sha256':sha(old_sig.encode()),'only_public_signature_delta':'delete (hsmall : ∀ s, eta s ≤ 1)','exact_sealed_text_match':True})
mathlib=['.lake/packages/mathlib/Mathlib/Topology/MetricSpace/Contracting.lean','.lake/packages/mathlib/Mathlib/MeasureTheory/Constructions/BorelSpace/Metrizable.lean','.lake/packages/mathlib/Mathlib/MeasureTheory/Measure/Tilted.lean','.lake/packages/mathlib/Mathlib/MeasureTheory/Measure/Haar/NormedSpace.lean','.lake/packages/mathlib/Mathlib/MeasureTheory/Group/Integral.lean','.lake/packages/mathlib/Mathlib/MeasureTheory/Function/L2Space.lean']
extras=[rec(p) for p in mathlib]+[rec('runs/20261006-companion-priority/smoothed-hessian-lower-preread/source-primary.sphmc-v1.raw.html')]
oldrun=pathlib.Path('runs/20261006-companion-priority/standardized-rgo-position-fisher/whole-math-review.json')
old=json.loads(oldrun.read_text(encoding='utf8')); oldmap={}
for field in ['frozen_inputs','reachable_source_inputs','additional_read_parent_and_pinned_API_inputs']:
 for x in old.get(field,[]):
  if isinstance(x,dict) and 'path' in x:oldmap[x['path']]=x
parent_checks=[]
changed={freeze['inputs'][i]['path'] for i in [0,1,2,3]}
for p in sorted(seen-changed):
 x=rec(p);b=subprocess.check_output(['git','show',base+':'+p])
 assert sha(b.replace(b'\r\n',b'\n'))==x['lf_sha256'],p
 prior=oldmap.get(p)
 parent_checks.append(dict(x,base_git_raw_sha256=sha(b),base_git_lf_match=True,prior_whole_math_lf_match=bool(prior and prior['lf_sha256']==x['lf_sha256']),prior_whole_math_raw_match=bool(prior and prior['raw_sha256']==x['raw_sha256'])))
affine='AutoSamplingTheory/TechnicalLemmas/Measure/AffineGibbs.lean'
assert rec(affine)['lf_sha256']==oldmap[affine]['lf_sha256']
log=rec(run/'reviewer.independent-focused.log')
txt=(run/'reviewer.independent-focused.log').read_text(encoding='utf8')
assert 'Build completed successfully (3729 jobs)' in txt
ax=re.findall(r"'([^']+)' depends on axioms: \[([^\]]+)\]",txt)
assert len(ax)==12,len(ax)
assert all(set(a.split(', '))=={'propext','Classical.choice','Quot.sound'} for _,a in ax)
manifest=json.loads(pathlib.Path('lake-manifest.json').read_text(encoding='utf8'))
pin=[x for x in manifest['packages'] if x['name']=='mathlib'][0]['rev'];assert pin=='db584cd6d46c92f209a44c0f1c829460d327499d'
body=[]
for p in [freeze['inputs'][i]['path'] for i in [0,1,2,3,27]]:
 s=pathlib.Path(p).read_text(encoding='utf8')
 body.append({'path':p,'lines':len(s.splitlines()),'private_declarations':len(re.findall(r'^private (?:theorem|def)',s,re.M)),'public_theorems':len(re.findall(r'^theorem ',s,re.M)),'entire_body_read':True})
receipt={
 'schema_version':1,'advance_id':'ASTIS-SA-20261007-PositiveStepProximalRGO','reviewer_id':'picard_commit_verifier_20261005','reviewer_role':'independent-whole-mathematics-reviewer','status':'passed-scoped','verification_status':'passed-scoped','review_phase':'pre-PROVED_LOCAL-whole-mathematics-only','checked_base_commit':base,'checked_HEAD':base,'production_changes_are_uncommitted':True,
 'frozen_inputs':inputs,'original_freeze':rec(run/'math-freeze.json'),'before_after_inputs':{'count':36,'all_raw_and_LF_match_original':True,'all_reviewer_raw_snapshots_match':True},
 'reachable_source_inputs':[rec(p) for p in sorted(seen)],'pinned_API_and_primary_inputs':extras,'unchanged_parent_checks':parent_checks,'prior_whole_math_reuse':{'receipt':rec(oldrun),'scope':'Only matched normalized parent bytes; raw match recorded separately per path. Changed source proof and both Tests read completely anew; prior generic affine theorem receives no new proof credit.'},
 'pins':{'lean_toolchain':pathlib.Path('lean-toolchain').read_text().strip(),'mathlib_revision':pin,'LEAN_NUM_THREADS':2},
 'signature_checks':sigchecks,'whole_body_review':body,'reader_review':{'lessons':3,'steps':[9,7,3],'all_statement_assumptions_formulas_proof_steps_and_listed_direct_provenance_read':True,'issues':[]},
 'mathematical_checks':[
 {'name':'actual gradient estimates','result':'C2 signed Hessian bounds produce genuine gradient Lip1, monotonicity and id-minus-gradient Lip1 by the retained convex gradient-step theorem with step=1, alpha=0,beta=1. This internal step is unrelated to smoothing eta.'},
 {'name':'pointwise damped contraction','result':'For each finite eta>0, T=(y+eta*(id-gradV))/(1+eta) has nonnegative coefficient c=eta/(1+eta)<1 exactly. The changed helper proves the exact coefficient, and never uses sup c<1, uniform convergence or eta<=1.'},
 {'name':'measurable pointwise Banach selector','result':'Starting at actual zero, every iterate is measurable by parameter scalar inverse/add/smul and continuous id-minus-gradient. Mathlib pointwise Banach convergence plus tendsto_pi_nhds and measurable_of_tendsto_metrizable gives measurable p on arbitrary measurable S. Neither fixed-point proof selection nor measurability of the proof-dependent c witness is used as a supplied certificate. E is complete/nonempty via actual normed additive group; Borel metric limit applies including E0.'},
 {'name':'genuine minimum and uniqueness','result':'Multiply fixed-point equation by 1+eta to obtain p+eta gradV(p)=y. True quadratic derivative gives gradientF(p)=0; regularization curvature kappa^-1+eta^-1 gives exact half coefficient. It is positive for every eta>0, so a lower competitor forces z=p. No final argmin premise.'},
 {'name':'same eta nonexpansivity and real kernel','result':'Only equal-eta inputs are compared. Monotonicity gives normdp^2<=inner(dy,dp); Cauchy-Schwarz and zero/nonzero norm branches give Lip1. Literal joint measurable G=gradV(p+sqrteta*z) satisfies exact combined bound and maps identity times standard Gaussian kernel to an actual Markov law. It is not the true RGO or HMC transition.'},
 {'name':'all-positive actual standardized calculus','result':'Both full private derivative proofs remain valid for every eta>0: real a=sqrteta, a^2=eta, rho gradient cancellation at zero, Hessrho=eta HV, HessQ=I+eta HV. Thus 0<=Hrho<=eta I and I<=HQ<=(1+eta)I. Actual NNReal beta=1+eta is finite separately at each s, not uniformly bounded.'},
 {'name':'true affine posterior normalization','result':'Positive lower source curvature internally produces hiV/base probability. Actual GibbsPositionMoment applied with alpha=1,beta=1+eta,mode0 internally yields positive partition/hiQ/Qprob. Literal tilted_tilted uses hiV. Proximal optimality gives W(p+sqrteta*u)=Q(u)+C with exact C; actual affine signed Haar transport cancels Jacobian, and hiQ/Qprob cancel additive C. Posterior likelihood<=1 under true base probability yields R probability. No normalizer/law/integrability/moment estimate supplied publicly.'},
 {'name':'real L2 and exact squared Fisher constants','result':'Canonical noncompact position IBP uses genuine ordinary-volume L1 products and full-space Fubini/IBP, without cutoff. It gives integral normu^2<=d and actual MemLp id2. Actual gradientrho eta-Lip and gradientrho0=0 give pointwise squared eta^2 domination. Strong measurability/actual position L1 prove Fisher L1/MemLp2 before integral_mono; two squared comparisons are equivalent to the last two source 4.6 norm comparisons, not the first W2 bound.'},
 {'name':'unchanged generic affine semantics','result':'Read all54lines. Arbitrary F/nonzero signed real scale identity is of totalized normalized volume tilts, no probability asserted. True inverse and nonzero absolute Jacobian multiply numerator and partition equally. Dimension zero Jacobian1 is legal. Current proof matches earlier whole-math and base Git LF; only consumer-range reader prose changes.'}],
 'independent_compile':{'command':'lake build Tests.FullRangeProximalGaussianOracle Tests.StandardizedRGOPositionFisher','exit_code':0,'jobs':3729,'log':log,'printed_axiom_declarations':[{'declaration':d,'axioms':a.split(', ')} for d,a in ax],'meaning':'Independent focused build invocation; cached/replayed targets are reused against exact unchanged bytes. Not claimed fresh direct re-elaboration or whole-repository/source-faithfulness gate. Existing ancestor linter warnings retained; no current production/Test warnings.'},
 'stress_checks':[
 {'name':'unbounded eta family','producer':'Tests.FullRangeProximalGaussianOracle.quadratic_unbounded_eta','result':'Actual eta(n)=n+2,y=3 produces Markov map z->3/(n+3)+sqrt(n+2)z and genuine centered Gaussian-output moment n+2. Sup contraction factor is1 and moment unbounded; no hidden uniform eta cap.'},
 {'name':'true eta2 posterior/Fisher','producer':'Tests.StandardizedRGOPositionFisher.quadratic_eta_two','result':'Actual mu=tilt(-x^2/2),R=mu.tilt(-norm(x-3)^2/4),p=1 yields r=tilt(-3u^2/2), probability and actual integrable moment<=1, Fisher exactly4 times position moment. This tests eta>1 and distinguishes Gaussian-output centered moment2. Test does not claim sharp eta2 moment equality1/3.'},
 {'name':'eta1 sharp normalization','producer':'Tests.StandardizedRGOPositionFisher.quadratic_eta_one_sharp','result':'Genuine accepted IBP gives moment1/2 for true r=tilt(-u^2), unlike gradient-output moment1.'},
 {'name':'negative scale and E0','result':'Arbitrary F negative scale s=-2 inverse (3-x)/2 remains exact. E0 constant7 original nonzero Gibbs volume produces true posterior probability, dirac0 and norm-square moment0 at arbitrary positive eta; Gaussian-output E0 is actual dirac0. No Nontrivial assumption/zero measure.'}],
 'primary_check':{'raw_primary':extras[-1],'literal_items_read':['S2.p2.2','S3.SS1.p1.1','S4.Thmtheorem2','S4.Ex8','S4.SS1.p4.2','S4.E6','S4.SS1.p4.3'],'scope':'Primary confirms analytic eta>0, separate computational cap, literal rho/true standardized density, only4.4/4.5 and lastTWO4.6. Not final encoder-denoiser source verdict or full source coverage certification.'},
 'fake_closure_scan':{'command':'canonical astis.strip_lean_comments_and_strings and FORBIDDEN_REGEX per line on recursive actual ASTIS/Test import closure','reachable_files':len(seen),'hits':hits,'standard_axioms':['propext','Classical.choice','Quot.sound'],'production_imports_tests':False},
 'conceptual_mirror_audit':{'status':'none-found','scope':'Independent bounded mathematical inspection; no new conceptual mirror created/validated.'},
 'exposure':{'entire_new_body_read':True,'prior_26_27_whole_math_exposure':True,'anonymous_reconstruction_or_final_source_verdict_read':False,'frozen_anonymous_inputs_hashed_only':True,'source_only_preproof_seals_and_primary_contract_read':True,'future_prototypes_read':False},
 'remaining_boundary':['FIRST4.6 Gaussian Talagrand/LSI/W2, source bias4.2, centered directional MGF4.3 and fullLemma4.2 remain OPEN.','Posterior joint Markov-family measurability/sampling, histories/Picard/Wp/warmness and both main results remain OPEN.','Numerical proximal cap eta<=1/(2beta), implementation/runtime/expected query work, initialization and actual input-precision/cost composition remain independent OPEN; TV does not transfer unbounded cost.','Independent final blind/source admission, exact committed VERIFIED, serialized root integration/repository ProofSeal/purification/Exposition/renderedQA/CI not certified by this pre-PROVED_LOCAL mathematics receipt.'],
 'leases':{'compiler':'CLOSED','sessions':'CLOSED','writes':'CLOSED','live_background_processes':False},
 'authorized_writes_only':'reviewer mathematical snapshots/logs/script and whole-math-review.json under this run; no production/Test/lessons/publications/cells/audits/ledger/shared/Goal changes',
 'no_state_transitions_or_shared_mutations':True,'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
out=run/'whole-math-review.json';assert not out.exists()
out.write_bytes((json.dumps(receipt,ensure_ascii=False,indent=2)+'\n').encode('utf8'))
print(json.dumps({'receipt':rec(out),'stable_input_count':len(inputs),'reachable_file_count':len(seen),'parent_count':len(parent_checks),'mathlib_and_primary':len(extras),'axiom_declarations':len(ax),'status':receipt['status'],'leases':receipt['leases']}))
