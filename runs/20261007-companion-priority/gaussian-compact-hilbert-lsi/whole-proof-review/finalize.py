import datetime, hashlib, json, pathlib, re, subprocess
ROOT=pathlib.Path('E:/Samplinglib')
RUN=ROOT/'runs/20261007-companion-priority/gaussian-compact-hilbert-lsi/whole-proof-review'
BASE='63855958426a195b8444942887a9bd415241ce88'
PROD='AutoSamplingTheory/TechnicalLemmas/FunctionalInequalities/GaussianCompactHilbertLogSobolev.lean'
TEST='Tests/GaussianCompactHilbertLogSobolev.lean'
PUB='AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.GaussianCompactHilbertLogSobolev.compact_stdGaussian_logSobolev'
def sha(b):return hashlib.sha256(b).hexdigest()
def lf(b):return b.replace(b'\r\n',b'\n').replace(b'\r',b'\n')
def rel(p):return p.relative_to(ROOT).as_posix()
def load(p):return json.loads(p.read_text(encoding='utf-8'))
def save(n,j):
 with (RUN/n).open('xb') as f:f.write((json.dumps(j,indent=2,ensure_ascii=False)+'\n').encode())
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=str(ROOT)).decode().strip()==BASE
initial=load(RUN/'inputs.initial.json')['inputs']
analysis=load(RUN/'reachability.analysis.json')
assert not analysis['compiled_local_axiom_declarations'] and not analysis['fake_closure_hits'] and not analysis['unmapped_constants']
bindings=list(initial)
additional=[rel(RUN.parent/'math-freeze.json')]
additional += [v['path'] for v in analysis['reached_modules'].values()]
additional += ['.lake/packages/mathlib/Mathlib/Analysis/InnerProductSpace/Dual.lean','.lake/packages/mathlib/Mathlib/Util/PrintSorries.lean']
known={x['path'] for x in bindings}
for path in additional:
 if path in known:continue
 raw=(ROOT/path).read_bytes();normalized=lf(raw);i=len(bindings);prefix='input.%03d'%i
 for suffix,b in [('.raw.snapshot',raw),('.lf.snapshot',normalized)]:
  with (RUN/(prefix+suffix)).open('xb') as f:f.write(b)
 bindings.append({'path':path,'raw_sha256':sha(raw),'lf_sha256':sha(normalized),'bytes':len(raw),'raw_snapshot':rel(RUN/(prefix+'.raw.snapshot')),'lf_snapshot':rel(RUN/(prefix+'.lf.snapshot')),'freeze_hash_match':None,'additional_read_scope':'Compiled reachable ASTIS source token scan or bounded actual Riesz/diagnostic API evidence; not old-parent new proof credit'})
 known.add(path)
for b in bindings:
 raw=(ROOT/b['path']).read_bytes()
 assert sha(raw)==b['raw_sha256'] and sha(lf(raw))==b['lf_sha256'],b['path']
 g=subprocess.run(['git','show',BASE+':'+b['path']],cwd=str(ROOT),capture_output=True)
 b['exists_at_working_base']=g.returncode==0
 b['working_equals_base_LF']=lf(g.stdout)==lf(raw) if g.returncode==0 else None
 b['base_blob_raw_sha256']=sha(g.stdout) if g.returncode==0 else None
 # New41 production/Test and task artifacts are the exact frozen working delta, not a proof commit.
save('inputs.json',{'checked_working_base':BASE,'math_freeze_inputs':39,'total_bound_inputs':len(bindings),'bindings':bindings,'base_scope':'Exact working base plus frozen uncommitted mathematical delta; no exact proof-commit or VERIFIED admission'})
source=(ROOT/PROD).read_text(encoding='utf-8')
sig=(ROOT/'runs/20261007-companion-priority/gaussian-hilbert-lsi-preproof/signature.prospective.txt').read_bytes()
assert sha(sig)=='b3a26c148088b619c982765873e4087b184812bf459a5af5305c10ea3bba538c'
assert source[source.index('theorem compact_stdGaussian_logSobolev'):].startswith(sig.decode().rstrip()+' := by')
assert len(re.findall(r'^private theorem ',source,re.M))==1
private=[x['name'] for x in analysis['compiled_rows'] if 'GaussianCompactHilbertLogSobolev.pullback_energy' in x['name']]
assert len(private)==1
for label in ['focused','direct','reachability.0']:
 assert load(RUN/(label+'.status.json'))['exit_code']==0
direct=(RUN/'direct.log').read_text(encoding='utf-8')
sets=re.findall(r"'([^']+)' depends on axioms: \[([^\]]+)\]",direct,re.S)
assert len(sets)==4
axioms=[]
for name,aset in sets:
 a=[x.strip() for x in aset.split(',')]
 assert set(a)=={'propext','Classical.choice','Quot.sound'}
 axioms.append({'declaration':name,'axioms':a})
assert (RUN/'reachability.0.log').read_text(encoding='utf-8').count('Declarations are sorry-free!')==2
api=[
 {'file':'.lake/packages/mathlib/Mathlib/Probability/Distributions/Gaussian/Multivariate.lean','lines':[55,73],'actual_name':'ProbabilityTheory.stdGaussian','role':'Literal Measure.pi variance-one Gaussian map by sum x_i basis_i; no supplied law identity'},
 {'file':'.lake/packages/mathlib/Mathlib/Topology/Algebra/Module/FiniteDimension.lean','lines':[430,452],'actual_name':'Module.Basis.equivFunL','role':'Continuous linear equivalence to finite coordinates; symmetry homeomorphism transports support'},
 {'file':'.lake/packages/mathlib/Mathlib/LinearAlgebra/Basis/Defs.lean','lines':[239,245],'actual_name':'Module.Basis.equivFun_symm_apply','role':'Inverse coordinate equivalence equals sum x_i basis_i; produces literal Gaussian law and unit-coordinate images'},
 {'file':'.lake/packages/mathlib/Mathlib/Analysis/Calculus/Gradient/Basic.lean','lines':[77,83,290,292],'actual_name':'_root_.gradient; _root_.inner_gradient_left','role':'Actual total gradient is inverse Riesz applied to fderiv; exact inner-product evaluation identity'},
 {'file':'.lake/packages/mathlib/Mathlib/Analysis/InnerProductSpace/Dual.lean','lines':[129,179],'actual_name':'InnerProductSpace.toDual; InnerProductSpace.toDual_symm_apply','role':'Real complete Hilbert Frechet-Riesz linear isometry equivalence, not a supplied gradient representative'},
 {'file':'.lake/packages/mathlib/Mathlib/Analysis/InnerProductSpace/PiL2.lean','lines':[529,540],'actual_name':'OrthonormalBasis.sum_sq_inner_left','role':'Finite real Parseval sum of squared scalar inner products = Hilbert norm squared, including empty basis'},
 {'file':'.lake/packages/mathlib/Mathlib/MeasureTheory/Function/L1Space/Integrable.lean','lines':[356,360],'actual_name':'MeasureTheory.integrable_map_measure','role':'True L1 equivalence with AE-measurable transport and AE-strong measurable observer'},
 {'file':'.lake/packages/mathlib/Mathlib/MeasureTheory/Integral/Bochner/Basic.lean','lines':[1043,1053],'actual_name':'MeasureTheory.integral_map','role':'Actual Bochner transport; three true L1 outputs already established before final comparison'},
 {'file':'AutoSamplingTheory/TechnicalLemmas/Analysis/Calculus/Gradient.lean','lines':[114,119],'actual_name':'AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Gradient.continuous_gradient_of_contDiff_one','role':'Actual Riesz inverse continuity composed with continuous fderiv; C2 supplies C1 internally'},
 {'file':'AutoSamplingTheory/TechnicalLemmas/Analysis/Calculus/Cutoff.lean','lines':[198,230,324,330],'actual_name':'radialSmoothCutoff_contDiff; radialSmoothCutoff_hasCompactSupport','role':'Genuine smoothness at origin via locally constant1; nonzero points norm smoothness; closed-ball compact support in finite dimension'},
 {'file':'AutoSamplingTheory/TechnicalLemmas/Measure/GaussianSqrtDensityDomain.lean','lines':[64,110,211,283],'actual_name':'density_calculus; gaussian_sqrt_density_domain','role':'Actual32 positive Z and actual exponential sqrt-density C2/identity domains; Test uses genuine derived C2, not an arbitrary surrogate'}]
save('api-evidence.json',{'scope':'Actual direct proof/calculus/measure semantics; imported unexpanded primitives are not new producer certificates','apis':api,'all_files_raw_LF_bound_in_inputs':True})
checks=[
 {'id':'sole-private-provider','lines':[15,39],'result':'T=b.toBasis.equivFunL.symm takes Pi.single i1 to b_i. Genuine C2 differentiability and linear derivative chain rule identify each scalar coordinate derivative with inner(gradient f(Tx),b_i); real Parseval gives exact sum squares=Hilbert norm-square. One private provider is reachable in compiled public proof; no norm-equivalence loss/sup-norm identification or certificate binder.'},
 {'id':'law-and-pullback','lines':[56,71],'result':'n=finrank, b=actual stdOrthonormalBasis, T=canonical inverse coordinates. Unfolded stdGaussian is exactly piGaussian.map T through the basis sum formula. Continuous-linear composition gives C2; homeomorphism gives compact support. Actual40 theorem called on f composed T, with its real square/Phi/full coordinate-energy domains.'},
 {'id':'domains-before-integrals','lines':[72,93],'result':'Square/Phi continuous incl zero; actual C1 gradient continuity from C2. T is measurable for actual finite Gaussian measure. integrable_map_measure transports three genuine L1 facts before integral_map. Energy transport uses the proved pointwise Parseval identity. No totalized integral fallback closes a missing domain.'},
 {'id':'coefficient-and-boundary','lines':[43,54,89,93],'result':'Only original f,C2,compact hypotheses plus finite-real-Hilbert/Borel/complete structures. Three true L1 outputs and homogeneous entropy<=2 integral norm gradient squared on actual stdGaussian. Signed f and zero mass have tlogt continuous value0; rank0 empty basis/true probability singleton included. No positive dimension/mass/normalization/basis/LSI premise.'},
 {'id':'meaningful-Tests','lines':[12,38],'result':'Generic zero on every finite Hilbert space and actual negative constant -2 on Euclidean Fin0 (square mass4) invoke the genuine theorem.'},
 {'id':'actual-paper-cutoff-consumer','lines':[43,80],'result':'Unit specialization of actual32 source producer chooses genuine proximal stationary p, actual rho, actual positive normalization Z and its actual sqrt-density C2. A positive-scale radial cutoff supplies C2/compact support internally, then new41 theorem yields all3L1/entropy on cutoff sqrt-density. No raw noncompact LSI, cutoff limit, KL/Fisher or T2 inference is made.'}]
save('checks.json',{'checked_working_base':BASE,'exact640_statement_matches_frozen_public_header':True,'checks':checks,'sole_private_compiled_identity':private[0],
 'fresh_checks':[load(RUN/(x+'.status.json')) for x in ['focused','direct','reachability.0']],
 'standard3_axioms':axioms,'compiled_source_scan':{k:analysis[k] for k in ['root_targets','compiled_reachable_ASTIS_Test_constants','compiled_local_axiom_declarations','compiled_reachable_source_modules','unmapped_constants','fake_closure_hits','scope']},
 'whole_new_module_reachability':{'public':PUB,'private_providers':private,'dead_private_providers':[],'proof_parent_ASTIS_names':['AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.GaussianCompactProductLogSobolev.compact_gaussian_pi_logSobolev','AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Gradient.continuous_gradient_of_contDiff_one']},
 'conceptual_mirror_audit':{'status':'none-found','scope':'Canonical basis Gaussian law and Riesz/Parseval transport are actual internal compiled mathematics here; no additional weaker cross-domain conceptual candidate surfaced in this bounded delta. No conceptual functor certification.'}})
save('reviewer-tool-failures.json',{'Lean_compiler_failures':[],'read_helper_failures':[{'kind':'Reviewer read-range IndexError','detail':'One bounded source read asked Support.lean lines551-575 although file ends568; output through568 retained in tool transcript, subsequent needed cutoff/Riesz/API reads completed. No mathematical or source change, no theorem route failure.'}],'production_repairs':[]})
index={b['path']:b for b in bindings}
def bind(p):return {k:index[p][k] for k in ['path','raw_sha256','lf_sha256','bytes']}
review={'schema_version':1,'verdict':'ACCEPTED_SCOPED_WHOLE_MATHEMATICAL_PROOF','status':'accepted-scoped','reviewer':'gaussian_domain_preproof_reviewer_29',
 'advance_id':'ASTIS-SA-20261007-GaussianCompactHilbertLogSobolev','checked_working_base':BASE,
 'scope':'Complete root-authored41 production and Tests, sole private provider, actual direct canonical parents/API semantics, fresh focused/direct checks and compiled local reachability/fake scan. Not source fidelity/blind/prose/graph validation or exactcommit VERIFIED.',
 'independent_from_proving_writer':True,'prior_sourcegraph_authorship':'Reviewer authored independent41 source graph before implementation; distinct phase admitted its repaired topology. This mathematical review does not validate that graph and does not use source-fidelity or blind verdicts as proof evidence.',
 'mathematical_declarations':[PUB],'exact_sealed_statement_bytes':640,'exact_signature_sha256':sha(sig),'production':bind(PROD),'Tests':bind(TEST),
 'frozen_input_count':39,'total_input_bindings':len(bindings),'inputs':'inputs.json','checks':'checks.json','actual_API_evidence':'api-evidence.json','compiled_dependency_inventory':'reachability.analysis.json',
 'conclusion':'Correct compact finite-real-Hilbert Gaussian LSI: internally produced f-square/Phi-square/gradient-square L1, homogeneous entropy<=2 true gradient-square integral. Literal canonical Gaussian law, actual C2/homeomorphic support and real chain-rule/Riesz/Parseval adapter preserve all constants. Rank0/signedzero and genuine32 posterior-cutoff Tests compile.',
 'blockers':[],'mathematical_repairs_required':[],
 'fresh_checks':{'focused':'focused.status.json','direct_Test_axioms':'direct.status.json','compiled_reachability_sorry_scan':'reachability.0.status.json','all_exit_codes':0,'standard3_only':True,'private_provider_reachable':True,'source_fake_closure_hits':0},
 'proof_boundary':{'accepted':'Compact C2 function theorem on actual stdGaussian in all finite real Hilbert dimensions, and actual32 cutoff Test consumer only',
 'remaining_OPEN':['Raw noncompact32 square-root-density LSI and actual cutoff mass/entropy/energy convergence','Coherent33 actual KL/Fisher adapter and full Gaussian W12 LSI','GaussianT2 and FIRST SPHMC4.6 W2/bias','Paper algorithms/main/error/work/cost/composition','Source-fidelity/blind/publication/exactcommit independent admission and human-facing/postmerge PURIFIED'],
 'old_parent_credit':'Reused actual40/32 canonical parents retain their prior status; fresh closure checks do not add theorem/source credit to old31/30/LSI readiness.',
 'no_VERIFIED_transition':True},
 'canonical_mutations':[],'source_fidelity_or_blind_evidence_read':False,'compiler_lease':'CLOSED','lease':'lease.json'}
save('math.review.json',review)
outputnames=['inputs.initial.json','inputs.json','math-freeze.raw.snapshot.json','ReachabilityProbe.lean','fresh-check.py','finalize.py','focused.log','focused.status.json','direct.log','direct.status.json','reachability.0.log','reachability.0.status.json','reachability.analysis.json','api-evidence.json','checks.json','reviewer-tool-failures.json','math.review.json']
payload={'checked_working_base':BASE,'inputs':[{k:b[k] for k in ['path','raw_sha256','lf_sha256']} for b in bindings],
 'outputs':[{'path':rel(RUN/n),'raw_sha256':sha((RUN/n).read_bytes()),'lf_sha256':sha(lf((RUN/n).read_bytes()))} for n in outputnames]}
runhash=sha(json.dumps(payload,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode())
save('run.json',{'schema_version':1,'run_sha256':runhash,'deterministic_payload':payload,'verdict':review['verdict'],'all_leases_CLOSED':True,'canonical_mutations':[]})
for b in bindings:
 raw=(ROOT/b['path']).read_bytes();assert sha(raw)==b['raw_sha256'] and sha(lf(raw))==b['lf_sha256']
lease=load(RUN/'lease.json');lease.update({'status':'CLOSED','read_lease':'CLOSED','write_lease':'CLOSED','Python_lease':'CLOSED','compiler_lease':'CLOSED','completed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'inputs_rechecked_unchanged':True,'verdict':review['verdict'],'run_sha256':runhash,'canonical_mutations':[]})
(RUN/'lease.json').write_bytes((json.dumps(lease,indent=2,ensure_ascii=False)+'\n').encode());save('lease.closed.json',lease)
print(json.dumps({'verdict':review['verdict'],'review_raw_LF_sha256':sha((RUN/'math.review.json').read_bytes()),'run_sha256':runhash,'inputs':len(bindings),'frozen':39,'leases':'ALL_CLOSED'}))
