from pathlib import Path
import datetime,hashlib,json,re,sys
R=Path('E:/Samplinglib');O=Path(__file__).parent
sys.path[:0]=[str(R),str(R/'tools')]
from tools import astis
def pin(p):
 p=Path(p);b=p.read_bytes();return {'path':p.relative_to(R).as_posix(),'raw_sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b)}
def put(n,v):
 with (O/n).open('x',encoding='utf8',newline='\n') as f:json.dump(v,f,ensure_ascii=False,indent=2);f.write('\n')
t=(O/'fresh-whole-source-kernel.stdout.log').read_text('utf8')
def vals(marker):return re.findall('^'+re.escape(marker)+r' (.+)$',t,re.M)
owned=vals('LOCAL_PROOF_CONSTANT');direct=vals('EXTERNAL_ASTIS_DEPENDENCY');trans=vals('TRANSITIVE_ASTIS_CONSTANT');edges=vals('TRANSITIVE_ASTIS_EDGE');generic=vals('GENERIC_DEPENDENCY')
assert owned and direct and trans and not vals('LOCAL_NO_VALUE') and not vals('PROJECT_NO_VALUE')
am=re.search(r'depends on axioms:\s*\[([^]]+)\]',t,re.S);assert am
axioms=[s.strip() for s in am.group(1).split(',')]
assert set(axioms)=={'propext','Classical.choice','Quot.sound'} and len(axioms)==3
public=[s for s in direct if s.startswith('AutoSamplingTheory.')]
expected={f'AutoSamplingTheory.ExampleCases.ProximalBPS.{a}.{b}' for a,b in [('ActualConditionalNextWaitDensity','actual_conditional_next_wait_density'),('ActualFiniteHistoryTailLaw','actual_finite_history_tail_law'),('ActualHarmonicFlow','actual_harmonic_flow_laws'),('ActualBounceRate','actual_bounce_rate_energy_laws')]}
assert set(public)==expected
assert not any('ActualConditionalNextWaitSurvival' in s for s in owned+direct+trans)
def source_for(n):
 n=n[n.rfind('AutoSamplingTheory.'):];a=n.split('.')
 for k in range(len(a),0,-1):
  p=R/('/'.join(a[:k])+'.lean')
  if p.is_file():return p
 raise AssertionError(n)
files=sorted({source_for(n) for n in owned+direct+trans})
put('kernel-dependency90.json',{
 'status':'ACCEPTED_NATIVE_ELABORATED_KERNEL_CLOSURE','reviewer_id':'/root/exact_verify77',
 'module':pin(R/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualFiniteHistoryExtension.lean'),
 'probe':pin(O/'FreshWholeSourceKernelClosure90.lean'),'native_log':pin(O/'fresh-whole-source-kernel.stdout.log'),
 'standard_axioms_only':True,'axioms':axioms,'owned_constants':owned,'owned_constant_count':len(owned),
 'owned_generated_constants_included':True,'immediate_ASTIS_dependencies':direct,'immediate_public_producers':public,
 'immediate_public_count':len(public),'immediate_private_generated_count':len(direct)-len(public),
 'transitive_ASTIS_constants':trans,'transitive_ASTIS_constant_count':len(trans),'transitive_ASTIS_edges':edges,'transitive_ASTIS_edge_count':len(edges),
 'generic_direct_dependencies':generic,'generic_direct_count':len(generic),'ASTIS_source_files':[pin(p) for p in files],'ASTIS_source_file_count':len(files),
 'constant_source_bindings':[{'constant':n,'source':pin(source_for(n))} for n in sorted(set(owned+direct+trans))],
 'all_project_constants_have_value':True,'actual88_absent':True,
 'method':'Fresh elaboration of exact whole production source plus observational commands. Traverse public theorem and owned generated constants in type/value, then recursively every ASTIS constant type/value. Bind actual source files via longest existing namespace prefix. Generic Lean/Mathlib constants kept separate; no name-scan graph used as proof evidence.',
 'public_parent_roles':{'ActualConditionalNextWaitDensity':'Actual strict history/relative-wait law, Borel observable and all nonnegative tests internally consumed.','ActualFiniteHistoryTailLaw':'Actual H_n and H_(n+1) Borel finite histories. iid/product law stays within89 dependency closure.','ActualHarmonicFlow':'Joint continuous actual Phi; fixed-parameter Borel pullback of time/state.','ActualBounceRate':'Actual zero-safe S Borel; no false continuity claim at normal0.'},
 'generic_roles':'Finite tuple last/castSucc, measurable Sum/product equivalence and finite products, map composition/congruence, restrict AE equality, map-univ mass, set-lintegral congruence. No public provider premises added.',
 'no_VERIFIED_or_exact_science_commit_credit':True})
hits=astis.forbidden_pattern_hits();assert not hits,hits
put('fake-closure90.json',{'reviewer_id':'/root/exact_verify77','function':'tools.astis.forbidden_pattern_hits','scanner':pin(R/'tools/astis.py'),'scope':'All current production ASTIS Lean/root/Tests files; canonical comments/string stripping. Not an aggregate build.','source_file_count':len(astis.lean_source_files()),'hits':hits,'pass':True,'module':pin(R/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualFiniteHistoryExtension.lean')})
M=R/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualFiniteHistoryExtension.lean'
m=M.read_text('utf8');seal=json.loads((O.parent/'root.statement-seal90.json').read_text('utf8'))
assert seal['expanded_literal_Prop'] in m
header=(R/'runs/20261007-companion-priority/pbps-next-history-extension-preread90/header90.v2.proposed.lean').read_text('utf8')
def literal(s):
 a=s.index('private def actual_finite_history_extension_statement');b=s.index('\n\n',s.index('∂μ)))',a));return s[a:b]
assert literal(header)==literal(m)
p89=(R/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualConditionalNextWaitDensity.lean').read_text('utf8')
def binders(s):return s[s.index('    {E : Type*}'):s.index('    let c :')]
def model(s):return s[s.index('    let c :'):s.index('    ∀ y xRef : E, ∀ z₀ : E × E, ∀ n : ℕ,')]
assert binders(m)==binders(p89) and model(m)==model(p89)
findings=[
 {'ingredient':'Sealed literal and actual definitions','finding':'Entire private literal equals independently reviewed V2 and Seal. Six source analytic conditions and14 model lets equal89. Body repeats actual c/Phi/S/rate/hazard/hitting-time/absorbing recursion/productP/clipping/history/wait/time/density; subsequent change unfolds only that literal. No extra public regularity, probability, Borel, identity or kernel provider hypothesis.'},
 {'ingredient':'Actual Borel histories','finding':'At deterministic depths n and n+1 the actual87 producer yields H and Hnext measurable. This is finite-history measurability, not nonexplosion or all-time path. The proof later shadows hH with Measurable H only after all original source hH parent applications; no public-binder substitution.'},
 {'ingredient':'Borel append on all abstract histories','finding':'Live update composes actual jointly continuous Phi with ((y,ref),s,state), then zero-safe Borel S with (ref,Phi); cumulative NNReal time adds toNNReal(s). SumProdDistrib plus Sum.elim treats stopped as constant stopped. Fin.lastCases uses exactly snoc_last for new coordinate and snoc_castSucc for old coordinates; every old coordinate is retained. lift is append paired with untouched relative time.'},
 {'ingredient':'Actual guarded record equality','finding':'On B, split literal record_n into live/stopped. Live upper strict finite cutoff rules out tau=top; Fin.lastCases reduces final actual H_(n+1) coordinate to literal next. simp identifies actual epsilon_n and real coercion of finite untopD and its toNNReal. Old coordinates agree definitionally. Stopped branch contradicts0<waitObs=0. No AE-only shortcut: equality holds for every w in B, including any raw exceptional input satisfying that guard.'},
 {'ingredient':'Restricted joint law','finding':'From89 map X(P|B)=nu, map_map for measurable lift/X gives map(lift∘X)(P|B). hYactual is an everywhere-on-B equality, hence AE for P.restrict B via B Borel. map_congr concludes actual joint Y law. No convention outside B is used to identify actual updates.'},
 {'ingredient':'Restricted marginal and subprobability','finding':'The marginal proof composes measurable append with X directly and uses same hactual; no density on the new history carrier is asserted. map lift nu of univ equals nu univ≤1 from89; finite mass is inherited without renormalizing or asserting a strict mass formula.'},
 {'ingredient':'All joint nonnegative tests and old-history events','finding':'For every measurable F:HistNext×real→ENNReal, F∘lift is admissible89 test. Its parameter integral measurability is returned directly. On B∩H^-1A, setLIntegral_congr_fun uses hYactual.89 identity then gives desired nested integral. This uses no subtraction, L1 or positive-event division, so F=top and nullA remain included.'},
 {'ingredient':'Definitions outside transported support','finding':'Negative real update s may have Phi_s with time increment0; this is a Borel totalization only. D=0 outside0<s<d(h); stopped D=0. Actual equality and laws are restricted to B, so default timeObs0 at infinity/stopped never becomes an actual finite post-jump assertion.'},
 {'ingredient':'Source graph and strict smaller boundary','finding':'Reviewed source graph construction/Borel A2/guarded A2 update/89 transport AND edges match implemented ingredients. Own former2string scope overlay is admitted solely by distinct review. Optional direct87/86 route remains OR and unused; survival88 absent from complete kernel closure. Ordered absolute-time iteration, last survival factor, sum over paths/jump counts, fullA7, random stopping/physical-time restart and global operator claims remain open.'}
]
put('whole-mathematics90.pre-exposition.json',{
 'status':'MATHEMATICS_AND_KERNEL_ACCEPTED_EXPOSITION_NOT_YET_REVIEWED','reviewer_id':'/root/exact_verify77','module':pin(M),'seal':pin(O.parent/'root.statement-seal90.json'),
 'whole_private_Prop_exact_seal_and_header':True,'all_six_source_conditions_and14_model_lets_exact_parent89':True,
 'public_analytic_binders':['hα','hαβ','hV','hH','hη','hβη'],'full_28_literal_lets_reviewed':True,'findings':findings,
 'cases':{'n0':'HistFin1 and HistNextFin2; last/castSucc well-typed and recursion argument unchanged.',
 'rank0_zero_normal':'No nonempty/nonzero-dimensional or nonzero reflection normal hypothesis; total zero-safe actual S is Borel.',
 'flat_hazard_infinite_wait':'Upper finite strict cutoff excludes infinite wait. No finite-wait guarantee asserted.',
 'd0_zero_wait_endpoint':'Strict guards exclude each; no noatom or open/closed mass equivalence argument needed.',
 'stopped':'waitObs0 contradicts positive guard; total abstract append stopped remains Borel.',
 'nullA':'Unnormalized restriction and set-lintegrals remain valid without dividing by event probability.',
 'allF':'Joint Borel ENNReal tests, including infinite values, use nonnegative integrals only.',
 'unbounded_d':'Finite-valued pointwise NNReal d, with no uniform bound needed.',
 'unrealizable_histories':'Borel append and density totalizations on all Hist; actual identification only on realized guarded histories.'},
 'required_mathematical_repairs':[],'native_fresh_focused_exit':0,'native_fresh_whole_source_exit':0,'standard_axioms_only':True,
 'kernel':pin(O/'kernel-dependency90.json'),'fake_closure':pin(O/'fake-closure90.json'),
 'final_exposition_decision_pending':True,'no_final_decoder_or_source_verdict_read':True,'no_VERIFIED_or_canonical_writes':True})
print(json.dumps({'owned':len(owned),'immediate_public':public,'immediate_private':len(direct)-len(public),'transitive':len(trans),'edges':len(edges),'generic':len(generic),'ASTIS_files':len(files),'axioms':axioms,'fake_closure':'PASS','exposition_pending':True},ensure_ascii=False,indent=2))
