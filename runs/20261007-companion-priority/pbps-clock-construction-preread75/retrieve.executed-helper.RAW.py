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
def launch(action):
 assert not (OWN/'lease.final.json').exists();(OWN/(action+'.executed-helper.RAW.py')).write_bytes(SELF.read_bytes());argv=[PY,'-B','-X','utf8',str(SELF),'_child',action]
 with (OWN/(action+'.stdout.log')).open('wb') as o,(OWN/(action+'.stderr.log')).open('wb') as e:
  p=subprocess.Popen(argv,cwd=ROOT,stdout=o,stderr=e);print(json.dumps(dict(status='RUNNING',actual_PID=p.pid,action=action,runner_PID=os.getpid())),flush=True);code=p.wait()
 write(action+'.receipt.json',dict(action=action,actual_PID=p.pid,runner_PID=os.getpid(),command=argv,exit_code=code,terminal_closed=True,stdout=pin(OWN/(action+'.stdout.log')),stderr=pin(OWN/(action+'.stderr.log')),executed_helper=pin(OWN/(action+'.executed-helper.RAW.py'))));print(json.dumps(dict(status='TERMINAL',actual_PID=p.pid,action=action,exit_code=code)));return code
if __name__=='__main__':
 action=sys.argv[-1]
 if sys.argv[1]=='_child':sys.exit(globals()[action]() or 0)
 else:sys.exit(launch(action))
