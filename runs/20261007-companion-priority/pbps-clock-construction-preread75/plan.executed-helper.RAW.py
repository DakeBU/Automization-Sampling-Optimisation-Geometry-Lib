from pathlib import Path
from datetime import datetime, timezone
import hashlib,html,json,os,re,subprocess,sys
ROOT=Path('E:/Samplinglib');OWN=ROOT/'runs/20261007-companion-priority/pbps-clock-construction-preread75';SELF=Path(__file__)
PY='C:/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe'
PRIMARY=ROOT/'runs/20261007-companion-priority/phase-pbps-gamma-preread57/primary-pbps.exactraw.snapshot.html'
EXPECTED='d81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760'
ACTOR='/root/exact_science63';RECIPE='Replace CRLF byte pairs with LF only; retain bare CR and every other byte.'
def sha(b):return hashlib.sha256(b).hexdigest()
def canon(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def load(p):return json.loads(p.read_bytes())
def read(n):return load(OWN/n)
def write(n,x):(OWN/n).write_bytes(json.dumps(x,ensure_ascii=False,sort_keys=True,indent=2).encode()+b'\n')
def pin(p):
 b=p.read_bytes();return dict(path=p.relative_to(ROOT).as_posix(),RAW_bytes=len(b),RAW_sha256=sha(b),LF_sha256=sha(b.replace(b'\r\n',b'\n')))
def check(row):
 p=ROOT/row['path'];q=pin(p)
 for k in ['RAW_bytes','RAW_sha256','LF_sha256']:assert row[k]==q[k],(p,k)
 return q
def git(args):return subprocess.run(['git',*args],cwd=ROOT,capture_output=True,check=True).stdout
def textof(raw):
 formulas=[]
 def replace(m):
  formulas.append(html.unescape(m.group(1)));return ' [MATH_'+str(len(formulas)-1)+'] '
 s=re.sub(r'<math\b[^>]*alttext="([^"]*)".*?</math>',replace,raw.decode(),flags=re.S);s=html.unescape(re.sub('<[^>]+>','',s))
 for i,f in enumerate(formulas):s=s.replace('[MATH_'+str(i)+']','$'+f+'$')
 return s
def source():
 assert pin(PRIMARY)['RAW_sha256']==EXPECTED
 write('lease.open.json',dict(status='OPEN_SOURCE_FIRST_PROSPECTIVE_PLANNING_ONLY',actual_PID=os.getpid(),actor=ACTOR,no_SAU_Lean_Git_ledger_canonical_writes=True))
 write('observer.initial-shell-parser-negative.json',dict(status='RETAINED_READONLY_OBSERVER_COMMAND_FAILURE',tool_chunk='4b20a2',exit_code=1,actual_PID=None,PID_exposed_by_tool=False,diagnostic="PowerShell ParserError Missing type name after '[' in nested Python regex command; no source/canonical/owned mutation occurred.",repair='Use exact saved helper and direct Python invocation; not mathematical evidence.'))
 raw=PRIMARY.read_bytes();ls=raw.splitlines(keepends=True);spans=[('algorithm-and-prop31',1465,1653),('appendixA1-construction',2852,3025),('davis-reference',6198,6217)];rows=[]
 for name,a,b in spans:
  q=OWN/(name+'.exactraw.html');q.write_bytes(b''.join(ls[a-1:b]));txt=OWN/(name+'.readable.txt');txt.write_bytes(textof(q.read_bytes()).encode())
  rows.append(dict(anchor=name,start_line=a,end_line=b,whole_source=pin(PRIMARY),literal_RAW_slice=pin(q),readable_derivative=pin(txt),derivative_recipe='HTML math alttext preserved; tags removed and entities decoded; exact HTML remains authority.'))
 write('source.regions.json',dict(status='PRIMARY_READ_BEFORE_INTERFACE_OR_ROOT_IDEAS',primary=pin(PRIMARY),regions=rows))
 print(json.dumps(dict(status='SOURCE_SLICES_FROZEN',actual_PID=os.getpid(),primary=pin(PRIMARY),source_regions=len(rows))))
def expectations():
 assert read('source.regions.json')['primary']['RAW_sha256']==EXPECTED
 write('source-first.expectations.json',dict(status='SOURCE_FIRST_BEFORE_LOCAL_INTERFACE_RETRIEVAL',actual_PID=os.getpid(),source_revision='arXiv:2609.06905v1 fixed local primary',
  actual_objects=dict(center='c=y-eta*gradientV(xRef)',residual='h(x)=gradientV(x)-gradientV(xRef)',phase_state='z=(x,p) in original finite real Hilbert H x H',
  flow='Phi_t(z)=(c+(x-c)cos t+sqrt(eta)p sin t, -eta^(-1/2)(x-c)sin t+p cos t)',bounce='S(z)=(x,R_h(x) p), R_0=I',rate='lambda(z)=sqrt(eta)*max(inner(p,h(x)),0)',
  energy='H(z)=(eta^(-1)*norm(x-c)^2+norm(p)^2)/2',cap='C_E=sqrt(eta)*beta*sqrt(2E)*(sqrt(2eta E)+norm(c-xRef))'),
  exact_construction=['Independent Exp(1) sequence E_(n>=1).','T_0=0, zeta_0=z_0.','S_(n+1)=inf{u>=0: integral_0^u lambda(Phi_s(zeta_Tn)) ds >= E_(n+1)}; empty set means infinity, not zero.','If S finite, T_(n+1)=T_n+S_(n+1) and zeta_T(n+1)=S_bounce(Phi_S(zeta_Tn)); if infinite, retain deterministic flow forever.','Between jumps use the same flow from the postjump state.','Energy preserved across flow and bounce produces one fixed initial-energy cap for the entire recursion.','C_E=0 => no jumps; C_E>0 => every finite waiting time >= E_(n+1)/C_E.','Infinite iid Exp(1) sum diverges a.s. by SLLN, therefore no finite-time accumulation.','Memorylessness plus measurable path construction, not cap alone, supplies homogeneous Markov property.'],
  algorithm_refresh='Algorithm1 draws reference and Gaussian initial momentum independently once. No refresh clock or refresh rate appears in (3.5)/(3.9)/AppendixA.1; adding one changes the process.',
  no_credit=['Unique Markov process','nonexplosion','stationarity','path reversal','L2 semigroup','averaged/terminal kernels','bounce-query costs','actual-input composition','paper/Goal completion'],
  initial_next_delta='Actual cumulative-hazard generalized-inverse clock on the real phase space, with measurable dependence and exact first-crossing/lower-bound/zero-cap laws; stochastic iid recursion remains separate.',
  source_omissions=['Extended waiting-time carrier and infinity branch are implicit in inf notation.','Measurability of state/clock/path recursion and independent clock realization are suppressed by Davis citation.','Zero residual-normal reflection is specified as identity; discontinuity is tolerated only because rate vanishes.','Fixed initial energy cap must be propagated through actual recursion; pointwise cap alone is not nonexplosion.']))
 print(json.dumps(dict(status='SOURCE_EXPECTATIONS_FROZEN_BEFORE_INTERFACES',actual_PID=os.getpid())))
def retrieve():
 views=[]
 for row in read('source.regions.json')['regions']:
  q=ROOT/row['literal_RAW_slice']['path'];p=OWN/(row['anchor']+'.readable.v2.txt');p.write_bytes(textof(q.read_bytes()).encode());views.append(dict(source=row['literal_RAW_slice'],old_view=row['readable_derivative'],corrected_view=pin(p)))
 write('observer.readable-view-repair.json',dict(status='DERIVATIVE_ONLY_REPAIR_RAW_SOURCE_UNCHANGED',actual_PID=os.getpid(),issue='V1 stripped HTML tags after injecting TeX, so TeX less-than could consume following tag; no RAW source or frozen expectations changed.',repair='Use opaque math placeholders while stripping tags, then restore literal alttext.',views=views))
 paths=[PRIMARY,ROOT/'lean-toolchain',ROOT/'lake-manifest.json',ROOT/'.lake/packages/mathlib/LICENSE',ROOT/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualHarmonicFlow.lean',ROOT/'runs/20261007-companion-priority/pbps-actual-harmonic-flow73/verified.json',ROOT/'runs/20261007-companion-priority/pbps-bounce-rate-preproof74/header74.proposed.lean',ROOT/'runs/20261007-companion-priority/pbps-bounce-rate-preproof74/root.statement-seal74.json',ROOT/'AutoSamplingTheory/Probability.lean',ROOT/'AutoSamplingTheory/SDE.lean',ROOT/'AutoSamplingTheory/TechnicalLemmas/Probability.lean',ROOT/'AutoSamplingTheory/TechnicalLemmas/Probability/GaussianConditionalKernel.lean']
 paths += [ROOT/'.lake/packages/mathlib/Mathlib'/x for x in ['Probability/Distributions/Exponential.lean','Probability/Distributions/Gamma.lean','Probability/StrongLaw.lean','Probability/Independence/InfinitePi.lean','Probability/ProductMeasure.lean','Probability/Process/HittingTime.lean','MeasureTheory/Integral/DominatedConvergence.lean','MeasureTheory/Integral/IntervalIntegral/Basic.lean','MeasureTheory/Constructions/BorelSpace/Order.lean','Topology/Order/Monotone.lean']]
 paths += [ROOT/'runs/20261007-companion-priority/pbps-half-turn-construction-preread73'/x for x in ['lease.final.json','api.retrieval.json']]
 write('inputs.manifest.json',dict(input_count=len(paths),inputs=[pin(p) for p in paths],LF_recipe=RECIPE,storage='Exact finite references, small source RAW slices only; no whole primary or historical payload copies.'))
 controls=[]
 for name in ['docs/companion-papers-handoff.md','website/content/samplewiki_companion_frontiers.json','research-wiki/frontier-cells/ASTIS-SW-PBPS-actual-harmonic-flow.json']:
  p=ROOT/name;q=OWN/('control.'+str(len(controls))+'.exactraw.snapshot');q.write_bytes(p.read_bytes());controls.append(dict(current_at_read=pin(p),historical_snapshot=pin(q),classification='Mutable process/serialized integration metadata, not new mathematical premise; original read bytes authoritative.'))
 write('finite.control-snapshots.json',dict(rows=controls,version_rule='No blanket fallback. Each exact before snapshot is retained; source/Lean/header/API inputs must remain exactly pinned.'))
 commands=[('local-clock-inventory',['rg','-n','-i','integrated.?hazard|expMeasure|waiting.?time|non.?explos|hittingAfter','AutoSamplingTheory/Probability.lean','AutoSamplingTheory/SDE.lean','AutoSamplingTheory/TechnicalLemmas/Probability','AutoSamplingTheory/ExampleCases/ProximalBPS/ActualHarmonicFlow.lean']),
 ('canonical-clock-APIs',['rg','-n','hittingAfter|hittingAfter_eq_top_iff|notMem_of_lt_hittingAfter|isStoppingTime_hittingAfter','.lake/packages/mathlib/Mathlib/Probability/Process/HittingTime.lean']),
 ('hazard-integral-order-APIs',['rg','-n','continuous_parametric_primitive_of_continuous|continuous_primitive|integral_mono_on|integral_const |measurable_of_Iic|IsClosed.csInf_mem','.lake/packages/mathlib/Mathlib/MeasureTheory/Integral/DominatedConvergence.lean','.lake/packages/mathlib/Mathlib/MeasureTheory/Integral/IntervalIntegral/Basic.lean','.lake/packages/mathlib/Mathlib/MeasureTheory/Constructions/BorelSpace/Order.lean','.lake/packages/mathlib/Mathlib/Topology/Order/Monotone.lean']),
 ('iid-Exp-SLLN-APIs',['rg','-n','def expMeasure|isProbabilityMeasure_expMeasure|cdf_expMeasure_eq |strong_law_ae_real|theorem strong_law_ae |iIndepFun_infinitePi|infinitePi_map_eval','.lake/packages/mathlib/Mathlib/Probability/Distributions/Exponential.lean','.lake/packages/mathlib/Mathlib/Probability/StrongLaw.lean','.lake/packages/mathlib/Mathlib/Probability/Independence/InfinitePi.lean','.lake/packages/mathlib/Mathlib/Probability/ProductMeasure.lean']),
 ('bounded-memoryless-and-moment-gap',['rg','-n','memoryless|memory.?less|integrable.*expMeasure|integral.*expMeasure|integrable.*gammaMeasure|integral_id.*gammaMeasure','.lake/packages/mathlib/Mathlib/Probability/Distributions/Exponential.lean','.lake/packages/mathlib/Mathlib/Probability/Distributions/Gamma.lean'])]
 receipts=[]
 f=OWN/'retrieval';f.mkdir(exist_ok=True)
 for label,argv in commands:
  out=f/(label+'.stdout.RAW');err=f/(label+'.stderr.RAW')
  with out.open('wb') as o,err.open('wb') as e:p=subprocess.Popen(argv,cwd=ROOT,stdout=o,stderr=e);code=p.wait()
  assert code in [0,1];r=dict(label=label,command=argv,actual_PID=p.pid,exit_code=code,terminal_closed=True,stdout=pin(out),stderr=pin(err),no_match_means='Bounded absence only; no global nonexistence claim.');receipts.append(r)
 write('retrieval.receipts.json',dict(status='BOUNDED_NATIVE_RETRIEVAL_ONLY_NO_COMPILE',actual_PID=os.getpid(),queries=receipts))
 write('repository.pins.json',dict(HEAD_at_read=git(['rev-parse','HEAD']).decode().strip(),mathlib_commit=git(['-C','.lake/packages/mathlib','rev-parse','HEAD']).decode().strip(),no_Git_writes=True,header74_credit='Sealed prospective only; not proved or VERIFIED.',source_expectations_before_interfaces=pin(OWN/'source-first.expectations.json')))
 write('observer.retrieval-negatives.json',dict(actual_PID=os.getpid(),prior_readonly_tool_failures=[dict(tool_chunk='e91185',exit_code=1,actual_PID=None,diagnosis='Mistyped MeasureTheory/Integral/ParametricIntegral.lean location; actual calculus location subsequently read. No source or mathematical failure.'),dict(tool_chunk='fa3894',exit_code=1,actual_PID=None,diagnosis='Bounded no-match rg for Exp moment/memoryless names, retained as bounded absence.'),dict(tool_chunk='a747f8',aggregate_exit_code=0,actual_rg_EXIT=2,actual_PID=None,diagnosis='Nonexistent IntervalIntegral/Continuity.lean; correct DominatedConvergence.lean API found and pinned; shell aggregate0 is not rg success.')],PID_unknown_when_not_exposed=True))
 print(json.dumps(dict(status='FINITE_INPUTS_AND_RETRIEVAL_FROZEN',actual_PID=os.getpid(),input_count=len(paths),queries=len(receipts))))
def recheck():
 for row in read('inputs.manifest.json')['inputs']:check(row)
 for row in read('source.regions.json')['regions']:check(row['literal_RAW_slice'])
def plan():
 recheck();header=ROOT/'runs/20261007-companion-priority/pbps-bounce-rate-preproof74/header74.proposed.lean';seal=load(header.parent/'root.statement-seal74.json');check(seal['header'])
 source_text=(OWN/'appendixA1-construction.readable.v2.txt').read_text(encoding='utf-8');assert 'S_{n+1}<\\infty' in source_text and 'If the set is empty' in source_text
 specs=[('hitting-definition','Probability/Process/HittingTime.lean',64,87),('continuous-time-API-limit','Probability/Process/HittingTime.lean',228,245),('discrete-stopping-limit','Probability/Process/HittingTime.lean',415,424),('joint-hazard-continuity','MeasureTheory/Integral/DominatedConvergence.lean',494,500),('integral-cap','MeasureTheory/Integral/IntervalIntegral/Basic.lean',1420,1435),('Borel-clock-criterion','MeasureTheory/Constructions/BorelSpace/Order.lean',637,645),('closed-first-crossing','Topology/Order/Monotone.lean',415,434),('actual-Exp-law','Probability/Distributions/Exponential.lean',90,100),('Exp-CDF','Probability/Distributions/Exponential.lean',163,172),('iid-clock-realization','Probability/Independence/InfinitePi.lean',125,137),('SLLN-contract','Probability/StrongLaw.lean',593,605)]
 regions=[];folder=OWN/'API';folder.mkdir(exist_ok=True)
 for name,rel,a,b in specs:
  p=ROOT/'.lake/packages/mathlib/Mathlib'/rel;raw=p.read_bytes();q=folder/(name+'.exactraw.lean-fragment');q.write_bytes(b''.join(raw.splitlines(keepends=True)[a-1:b]));regions.append(dict(name=name,start_line=a,end_line=b,whole_source=pin(p),literal_RAW_span=pin(q),credit='Retrieved library source signature only; no new compile/proof credit.'))
 write('API.regions.json',dict(regions=regions))
 verified=load(ROOT/'runs/20261007-companion-priority/pbps-actual-harmonic-flow73/verified.json');assert verified['verified_commit']=='d7e00a7c0e8b0f37fcc2dbe99f6b646d3a7b1de6'
 ledger=ROOT/'runs/substantive_advances.jsonl';lb=ledger.read_bytes();target=[]
 for line in lb.splitlines():
  if line.strip():
   x=json.loads(line)
   if x.get('advance_id')=='ASTIS-SA-20261010-PBPSActualHarmonicFlow':target.append(x)
 assert target[-1]['to_state']=='VERIFIED'
 write('capsule.slice.json',dict(ledger_read_pin=dict(RAW_bytes=len(lb),RAW_sha256=sha(lb)),actual73=dict(state='VERIFIED',checked_commit=verified['verified_commit'],declaration='AutoSamplingTheory.ExampleCases.ProximalBPS.ActualHarmonicFlow.actual_harmonic_flow_laws',module_RAW=pin(ROOT/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualHarmonicFlow.lean')),sealed74=dict(header=pin(header),prospective_declaration='AutoSamplingTheory.ExampleCases.ProximalBPS.ActualBounceRate.actual_bounce_rate_energy_laws',proof_or_VERIFIED_credit=False),all_other_ledger_records_omitted=True))
 apis=[dict(name='intervalIntegral.continuous_parametric_primitive_of_continuous',classification='mathlib-available',use='Continuous actual rate∘flow gives jointly continuous Lambda with variable endpoint; internally supplies integrability, not a new caller.',file='MeasureTheory/Integral/DominatedConvergence.lean:494'),
 dict(name='MeasureTheory.hittingAfter',classification='mathlib-available',use='Reuse actual first-hit definition with WithTop nonnegative-real time; empty crossing set is top.',file='Probability/Process/HittingTime.lean:68'),
 dict(name='MeasureTheory.hittingAfter_eq_top_iff / hittingAfter_le_of_mem',classification='mathlib-available',use='General nonempty/empty boundary and one-sided bound. Full hittingAfter_le_iff requires WellFoundedLT, unavailable for real times.',file='Probability/Process/HittingTime.lean:157,217,236'),
 dict(name='IsClosed.csInf_mem / IsClosed.isLeast_csInf',classification='mathlib-available',use='New continuous-time first-crossing proof must use closedness and bounded-below threshold set, not the discrete WellFoundedLT lemma.',file='Topology/Order/Monotone.lean:428'),
 dict(name='MeasureTheory.measurable_of_Iic',classification='mathlib-available',use='Clock sublevel sets reduce to e <= Lambda(t), giving Borel measurability, including top branch.',file='MeasureTheory/Constructions/BorelSpace/Order.lean:689'),
 dict(name='intervalIntegral.integral_mono_on / integral_const',classification='mathlib-available',use='Propagate actual74 cap along actual73 energy-preserving flow to Lambda<=C_E*t.',file='MeasureTheory/Integral/IntervalIntegral/Basic.lean:1432,836'),
 dict(name='ProbabilityTheory.expMeasure / isProbabilityMeasure_expMeasure / cdf_expMeasure_eq',classification='mathlib-available',use='Actual Exp(1) threshold law and survival calculation; no exponential-law premise on source caller.',file='Probability/Distributions/Exponential.lean:96,98,165'),
 dict(name='ProbabilityTheory.iIndepFun_infinitePi / Measure.infinitePi_map_eval',classification='mathlib-available',use='Future canonical clock sequence on Omega=Nat->Real with infinitePi(expMeasure1); not supplied iid input to actual source theorem.',file='Probability/Independence/InfinitePi.lean:132'),
 dict(name='ProbabilityTheory.strong_law_ae_real / strong_law_ae',classification='mathlib-available',use='Future iid-clock divergence needs Integrable(E0), Pairwise independence and IdentDistrib; Exp integrability/mean1 must be produced, not assumed.',file='Probability/StrongLaw.lean:598,787'),
 dict(name='AutoSamplingTheory.Probability / AutoSamplingTheory.SDE',classification='source-contract-gap',use='Law transport and string SDE contracts exist; inspected regions provide no actual integrated-hazard PDMP/path constructor.'),
 dict(name='GaussianConditionalKernel.exists_tilted_isCondKernel',classification='existing-local-lemma',use='Actual every-y reference law and same-J disintegration already exist. Not the missing clock/path edge; do not duplicate.',file='AutoSamplingTheory/TechnicalLemmas/Probability/GaussianConditionalKernel.lean:35')]
 write('api.retrieval.json',dict(status='FINITE_LIBRARY_RETRIEVAL_NOT_LOCAL_PROOF',actual_PID=os.getpid(),libraries=read('repository.pins.json'),items=apis,bounded_absence='No local clock/path constructor in exact queried surfaces; no global Mathlib nonexistence claim.',no_compile=True))
 contract=dict(proposed_name='actual_integrated_hazard_clock_laws',status='PROSPECTIVE_UNSEALED_UNCLAIMED_UNPROVED',production_home_if_later_admitted='AutoSamplingTheory/ExampleCases/ProximalBPS/ActualHazardClock.lean',
 caller='Exactly original six analytic callers hα,hαβ,hV,hH,hη,hβη on the same finite real Hilbert/Borel carrier. All smoothness, rate continuity, cap and integrability are derived inside.',
 quantifiers='For all y,xRef,x,p on the SAME E and every nonnegative threshold e, all t>=0. No supplied flow/rate/energy/kernel/probability/nonexplosion premise.',
 definitions=dict(Lambda='Lambda(y,xRef,z,t)=integral from0 to t of rate(xRef,Phi(y,xRef,s,z)) ds; domain t>=0.',
 clock='tau(y,xRef,z,e)=MeasureTheory.hittingAfter (fun t a => Lambda(a.y,a.xRef,a.z,t)-a.e) (Ici0) 0 (y,xRef,z,e), with index NNReal and codomain WithTop NNReal.',
 exponential_clock_law='map (fun e:Real => tau(y,xRef,z,Real.toNNReal e)) (ProbabilityTheory.expMeasure1). This is a real first-waiting-time law, not a terminal/Markov transition kernel.',
 C='C_E actual74 expression evaluated at E=H(y,xRef,z), no independently chosen cap.'),
 conclusions=['Lambda jointly continuous/Borel; finite on every finite interval, Lambda0=0, nonnegative and nondecreasing.',
 'Exact first crossing: tau<=t iff e<=Lambda(t); empty crossing set iff tau=top. For tau finite Lambda(tau)=e; e>0 implies tau>0.',
 'tau jointly Borel in (y,xRef,z,e). Reuse hittingAfter definition; prove continuous-time threshold identities by closedness, not WellFoundedLT.',
 'P_Exp1(tau>t)=exp(-Lambda(t)); probability waiting-time law from the actual Exp threshold, no iid or integrability hypotheses for this one-clock law.',
 'Lambda(t)<=C_E*t. If C_E>0, tau>=e/C_E in extended time. If C_E=0 and e>0, tau=top; e=0 gives tau=0.',
 'Zero dimension/zero energy permitted: zero rate and infinite positive-threshold wait. alpha*eta=1 remains permitted. No assumption of almost-sure finite waiting time.'],
 real_consumer='AppendixA.1 (A.1): substitute postjump actual state zeta_Tn and next Exp(1) threshold E_(n+1). Its measurable clock and bound are needed before (A.2) recursive paths/nonexplosion.',
 dependent_on_74='Structurally ready AFTER actual74 is proved/source accepted; current74 is sealed only. Do not call or credit it as existing truth.',
 route_steps=['Consume exact73 Phi continuity/energy and future exact74 rate continuity/nonnegativity/cap without extra caller.',
 'Apply continuous_parametric_primitive_of_continuous; establish nonnegativity/monotonicity/zero/finite-interval integrability of actual Lambda.',
 'Instantiate canonical hittingAfter on NNReal; closed threshold set gives attained first crossing and top for empty set.',
 'Derive clock sublevel identities and Borel measurability; do not use discrete WellFoundedLT or assume unbounded hazard.',
 'Push forward expMeasure1 and use its exact CDF to derive first-clock survival.',
 'Use conserved actual energy and actual74 cap in integral_mono_on to derive waiting lower bound and zero-cap branch.',
 'Stop before recursive path, iid summation, Markov property, invariance or endpoint kernel.'])
 options=[dict(option='SELECTED actual integrated-hazard first-clock with Exp survival',reason='Earliest missing actual constructor with direct A.1 consumer, reuses canonical hittingAfter and fixed law; bounded before path recursion.'),dict(option='Actual finite-event recursion and joint measurable path map',reason='Next after selected clock and actual bounce74; needs infinity/termination branch and state/time recursion; currently premature.'),dict(option='Actual iid-clock divergence and nonexplosion',reason='After clock+path induction: propagate one energy cap through every actual postjump state, construct iid Exp sequence and discharge its moment/SLLN contracts. Pointwise cap alone insufficient.')]
 write('selected.contract.json',contract)
 write('dependency-audit.json',dict(status='READY_PROSPECTIVE_SOURCE_FIRST_CONTRACT',actual_PID=os.getpid(),source=read('source.regions.json'),source_first_expectations=pin(OWN/'source-first.expectations.json'),selected=contract,at_most_three_options=options,
 nodes=[dict(id='FLOW73',status='VERIFIED_DETERMINISTIC_ONLY'),dict(id='BOUNCE_RATE74',status='SEALED_NOT_PROVED'),dict(id='ACTUAL_HAZARD_FIRST_CLOCK',status='SELECTED_UNPROVED'),dict(id='IID_EXP_SEQUENCE',status='FUTURE_CONSTRUCT_FROM_INFINITE_PRODUCT'),dict(id='ACTUAL_RECURSIVE_PATH',status='FUTURE_UNPROVED'),dict(id='NONEXPLOSION',status='FUTURE_UNPROVED'),dict(id='HOMOGENEOUS_MARKOV',status='FUTURE_MEMORYLESS_AND_MEASURABLE_RECURSION'),dict(id='INVARIANCE_TERMINAL_KERNEL',status='EXCLUDED_LATER_A1_A2')],
 edges=['FLOW73+BOUNCE_RATE74 -> actual continuous hazard and one-step energy cap','actual hazard + canonical hittingAfter -> actual first clock','first clock + bounce74 + iid source -> actual recursion','actual recursion + both energy invariances -> same initial-energy cap for every event','actual clock bound + iid Exp moment/SLLN -> no accumulation','measurable recursion + exponential memorylessness -> homogeneous Markov','nonexplosion + joint construction -> actual terminal state/kernel; invariance separately'],
 source_hypotheses=dict(SOURCE=['Original V C2 and two Hessian bounds, 0<alpha<=beta, eta>0 and beta*eta<=1; same y,xRef and phase state.','Independent Exp(1) source clocks; one initial independent reference and Gaussian momentum draw when Algorithm1 is randomized.'],STANDING=['Real finite Hilbert state and Borel structures; nonnegative extended time including infinity; standard probability product/volume integration.'],TYPING=['Nonnegative threshold/time subtype; no Nontrivial E; no extra finite-dimensional L2 premise.'],RULED=['Flow and rate continuity, compact-interval integrability and hazard measurability derived from73+74.','Future independent clocks, Exp moments and memorylessness produced from canonical law; never new paper caller.'],EXCESS_FORBIDDEN=['supplied Markov kernel/path/nonexplosion','uniform global cap unrelated to initial actual energy','unbounded cumulative hazard or finite clock a.s.','extra refresh intensity','new regularity or onto assumption']),
 missing_bridges=[dict(kind='internal-paper-step',problem='Continuous-time first-crossing/Borel theorem missing locally; Mathlib hittingAfter_le_iff needs WellFoundedLT, cannot apply to real time.'),dict(kind='internal-paper-step',problem='Actual postjump recursion with stopped/infinite branch and measurable finite prefixes not constructed.'),dict(kind='internal-paper-step',problem='IID Exp sequence product exists in Mathlib substrate; exact Exp integrability and mean1 not found in queried Exponential/Gamma files and must be checked/derived before SLLN.'),dict(kind='external-cited-result',problem='Davis Section2 cited for integrated-hazard construction/Markov memorylessness; no local Davis theorem admitted.')],
 Davis=dict(citation='M.H.A.Davis1984, Piecewise-deterministic Markov processes: a general class of non-diffusion stochastic models, JRSS SeriesB46(3),353-388,Section2',DOI='10.1111/j.2517-6161.1984.tb01308.x',version='Bibliography in fixed PBPSv1 only; Davis full text/edition not fetched or inspected.',license='Davis reuse license unverified; no Davis text/code copied or ported, no external proof certificate used.',role='External-cited construction boundary; proposed first-clock route uses inspected Mathlib primitives and rederives local bridge.'),
 licenses=dict(primary='PBPS2609.06905v1; canonical execution records arXiv nonexclusive-distrib1.0. Only exact bounded source slices retained, no relicensing claim.',mathlib='Apache2.0 per pinned LICENSE and file headers; commit '+read('repository.pins.json')['mathlib_commit']),
 no_refresh_clock=True,no_reference_law_duplicate=True,cap_not_nonexplosion=True,no_Lean_or_proof_search=True,source_whole_paper_coverage=False,SAU_claim=False,VERIFIED=False,Goal_complete=False))
 text='Source-first READY: select the actual integrated-hazard first clock, with canonical hittingAfter on WithTop NNReal and exact Exp(1) survival.\n\n'
 text+='The literal Algorithm1 has no refresh clock. Fixed reference and initial Gaussian momentum are drawn once; only residual-gradient bounces occur. The clock may be infinite, including every positive threshold at zero energy/rank0.\n\n'
 text+='73 is a verified deterministic parent;74 is sealed only. The shortest follow-up is conditional on74 becoming proved/source accepted. Existing Q_y/disintegration is reused; it is not the missing path constructor.\n\n'
 text+='Neither a pointwise rate cap nor a first-clock law proves nonexplosion: actual recursive state/time measurability, common energy cap induction, constructed iid Exp clocks, their integrability/positive mean and SLLN remain. Homogeneous Markov memorylessness, invariance, actual terminal kernels and whole-paper/Goal results receive no credit.\n'
 (OWN/'named.source-first-dependency-audit75.md').write_bytes(text.encode())
 print(json.dumps(dict(status='READY_PROSPECTIVE_SOURCE_FIRST_CONTRACT',actual_PID=os.getpid(),selected='actual_integrated_hazard_clock_laws',no_proof_credit=True)))
def launch(action):
 assert not (OWN/'lease.final.json').exists();(OWN/(action+'.executed-helper.RAW.py')).write_bytes(SELF.read_bytes());argv=[PY,'-B','-X','utf8',str(SELF),'_child',action]
 with (OWN/(action+'.stdout.log')).open('wb') as o,(OWN/(action+'.stderr.log')).open('wb') as e:
  p=subprocess.Popen(argv,cwd=ROOT,stdout=o,stderr=e);print(json.dumps(dict(status='RUNNING',actual_PID=p.pid,action=action,runner_PID=os.getpid())),flush=True);code=p.wait()
 write(action+'.receipt.json',dict(action=action,actual_PID=p.pid,runner_PID=os.getpid(),command=argv,exit_code=code,terminal_closed=True,stdout=pin(OWN/(action+'.stdout.log')),stderr=pin(OWN/(action+'.stderr.log')),executed_helper=pin(OWN/(action+'.executed-helper.RAW.py'))));print(json.dumps(dict(status='TERMINAL',actual_PID=p.pid,action=action,exit_code=code)));return code
if __name__=='__main__':
 action=sys.argv[-1]
 if sys.argv[1]=='_child':sys.exit(globals()[action]() or 0)
 else:sys.exit(launch(action))
