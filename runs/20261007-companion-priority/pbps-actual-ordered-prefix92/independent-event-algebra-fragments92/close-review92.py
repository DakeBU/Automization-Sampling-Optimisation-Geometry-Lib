import hashlib,json,pathlib,re,subprocess
from datetime import datetime,timezone
R=pathlib.Path('E:/Samplinglib');B=R/'runs/20261007-companion-priority/pbps-actual-ordered-prefix92';D=B/'independent-event-algebra-fragments92'
def bind(p):
 b=p.read_bytes();return dict(path=p.as_posix(),raw_sha256=hashlib.sha256(b).hexdigest(),bytes=len(b))
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def put(name,v):
 p=D/name
 with p.open('x',encoding='utf-8',newline='\n') as f:
  if isinstance(v,str):f.write(v)
  else:json.dump(v,f,ensure_ascii=False,indent=2);f.write('\n')
 return p
expected={'Events92':'ffe309d308e3b82c20a15af38f397c57c5b29ea567589e986d8740f43f6aac92','Algebra92':'cf995959ce0db6164101ace8f02a47e7f126e6edc3b7e37ce0cbe8cbb3b21395'}
receipts=[]
for stem,h in expected.items():
 p=B/(stem+'.lean');assert bind(p)['raw_sha256']==h
 s=re.sub(r'/\-[\s\S]*?\-/','',p.read_text(encoding='utf-8'));assert not re.search(r'\b(sorry|admit|axiom)\b|Prop\s*:=\s*True|:=\s*trivial',s)
 receipt=read(D/(stem+'.receipt.json'));assert receipt['exit_code']==0 and receipt['terminal_closed']
 log=(D/(stem+'.stdout.log')).read_text();assert ': error' not in log
 assert log.count('depends on axioms: [propext,\n Classical.choice,\n Quot.sound]')==(4 if stem=='Events92' else 6)
 receipts.append(bind(D/(stem+'.receipt.json')))
old=(B/'Recursion92.lean').read_text(encoding='utf-8');new=(B/'Algebra92.lean').read_text(encoding='utf-8')
assert old[old.index('private def state'):old.index('\nend\n')].strip()==new[new.index('private def state'):new.index('private def timedHistory')].strip()
paths=[B/'Events92.lean',B/'Algebra92.lean',B/'Recursion92.lean',B/'root.statement-seal92.json',B/'Geometry92.lean',B/'focused/events2-forward-mono/receipt.json',B/'focused/algebra1-timed-history/receipt.json',B/'independent-coordinate-fragments92/coordinate-fragment-review92.native.json',B/'independent-fragments92/fragment-review92.native.json',R/'lake-manifest.json',R/'lean-toolchain',R/'.astis/toolchain/lean-4.33.0-windows/bin/lake.exe',R/'.astis/toolchain/lean-4.33.0-windows/bin/lean.exe']
inputs=[bind(p) for p in paths]
report={
 'schema_version':1,'reviewer':'/root/independent_math91','utc':datetime.now(timezone.utc).isoformat(),
 'decision':'ACCEPT_PRIVATE_EVENT_AND_ALGEBRA_FRAGMENTS_ONLY',
 'checked_HEAD':subprocess.run(['git','rev-parse','HEAD'],cwd=R,capture_output=True,text=True,check=True).stdout.strip(),
 'inputs':inputs,
 'scope':'Four generic event-decomposition theorems and six algebra theorems, including three retained previously reviewed theorems. No whole-SA U, all-n law, actual-model instantiation or VERIFIED acceptance.',
 'previous_recursion_body_retained_exact_after_newline_normalization':True,
 'event_audit':[
  {'declaration':'guard_snoc','finding':'The old guard and new live record plus strict last-old<new<T are exactly equivalent to the extended guard. Fin.snoc commutes with readTime pointwise; adjacent strict-monotonicity characterization splits all old comparisons and the new final comparison. All old horizon bounds and live tags remain.'},
  {'declaration':'record_history_snoc','finding':'For arbitrary record:Nat->Rec, the first n+2 records equal snoc of the first n+1 with record(n+1), by Fin.lastCases and coordinate values. No dynamics or recurrence premise is needed.'},
  {'declaration':'record_guard_step','finding':'Specializes guard_snoc and makes old record n live explicit. That old-live clause follows from guard_n at Fin.last n in the forward direction and is redundant in the reverse direction; adding it does not strengthen the event or assume a new process property.'},
  {'declaration':'record_event_step','finding':'Set extensionality yields an exact pointwise event equality for every raw w: next guard = old guard intersect old-live/new-live/strict next-time/strict horizon event. It is neither an almost-sure identity nor a counting interpretation.'}
 ],
 'event_edge_cases':[
  'n0: generic guard0 requires a live initial record; strict monotonicity and horizon comparisons are vacuous. It does not assert initial time0 for arbitrary record. Actual initial time0 must be supplied by literal record when instantiated.',
  'Zero wait gives equal successive stored times and fails the strict clause on both sides. Stopped records have readTime0 but cannot satisfy the required live clause.',
  'T0: no live nonnegative stored next time can be strictly below0, so extended event is empty. The generic initial live guard at n0 may still hold; the intersection correctly excludes the next event.',
  'Nothing is claimed about records after n+1, physical-time counts, path reconstruction or actual transition laws. Both exact old-history and next-history components remain visible.'
 ],
 'algebra_audit':[
  {'declaration':'state_snoc_prefix/state_snoc_last/weight_snoc','finding':'The previously accepted state/real-weight definitions and three proofs are retained exactly, apart from namespace context and newline representation. They preserve every old state, give the correct appended final state, and split one last real factor.'},
  {'declaration':'timedHistory','finding':'Generic complete tagged history stores toNNReal(cons0t_j) and state_j. It matches the sealed K after concrete step instantiation and restriction to the strict simplex; no such instantiation is claimed completed here.'},
  {'declaration':'timedHistory_snoc','finding':'Function extensionality splits old coordinates and the last coordinate. Every old coordinate retains both its time and state via cons/snoc and state_snoc_prefix. At the last coordinate, state_snoc_last supplies the new phase; NNReal equality and coercion use last>=0, u-last>=0 and u>=0 to prove toNNReal(u)=toNNReal(last)+toNNReal(u-last). No unguarded subtraction/truncation identity is used.'},
  {'declaration':'ordered_last_nonneg','finding':'StrictMono(cons0t) implies monotonicity; comparing Fin0 with Fin.last n gives0<=last. This correctly yields equality0 at n0, not an unavailable strict positive-time premise.'},
  {'declaration':'weight_snoc_ofReal','finding':'After exact real weight_snoc, ENNReal.ofReal_mul uses nonnegativity of the old real weight. No nonnegativity assumption for an arbitrary final factor is required: when final factor is negative the two sides both truncate to0, and old weight0 is also valid. Concrete rate-survival factors will in any case be nonnegative.'}
 ],
 'algebra_edge_cases':[
  'n0 timedHistory starts with live(0,z0), last=0 and hu supplies u>=0. The identity works even u0; an actual strict next-event application separately requires u>0.',
  'The timed-history theorem permits unordered or negative earlier coordinates provided last>=0 and u>=last. Earlier toNNReal values are preserved identically, so this generic extension creates no false claim that those auxiliary histories are physical.',
  'Without ht or hu the general time-addition identity can fail, so the explicit private hypotheses are mathematically meaningful and correctly used. In the strict simplex consumer they follow from ordered_last_nonneg and the last-time interval.',
  'The old-weight nonnegativity premise can be produced from Geometry92 after identifying generic weight with literal qReal on the simplex. It must not become a new public density or positivity provider.'
 ],
 'private_parameter_and_binder_boundary':{
  'parameters':['generic record and state space','generic step and factor','ht:last>=0','hu:last<=u','hweight:old real weight>=0'],
  'status':'Legitimate private algebra/event parameters. Actual record, step=S composed with Phi, factor=pre-bounce rate times segment survival, and the three support/nonnegativity facts must be supplied inside the main proof from literal definitions and accepted ingredients. None is authorized as a new sealed public hypothesis.',
  'no_assumed_history_correspondence':True,'no_actual_density_provider':True
 },
 'kernel':{'receipts':receipts,'all10_types_inspected':True,'both_exit_code_zero':True,'events_seconds':10.734,'algebra_seconds':9.797,'axioms_for_all10':['propext','Classical.choice','Quot.sound'],'no_placeholder_closure':True},
 'findings_requiring_changes':[],
 'remaining_open':'Actual-model instantiation of generic event and algebra lemmas; subtype integration adapters and measurable tests; application of91 one-step law; actual all-n density induction, all-test laws, measure/mass conclusions and sealed public-theorem assembly.',
 'canonical_or_production_mutation':False
}
decision=put('event-algebra-review92.native.json',report)
put('event-algebra-review92.md','''# Independent event/algebra fragments92 review

Accepted the frozen Events92 and Algebra92 private fragments. Fresh pinned Lean compilation, ten full types and all axiom lists passed; every theorem uses only propext, Classical.choice and Quot.sound.

The event equality exactly splits the extended guard into the old guard and both live records, strict time increase and strict cutoff. The old-live conjunct is explicitly derived from the old guard. This is pointwise for arbitrary record sequences, including the relevant zero-clock/stopped boundaries, without claiming a raw counting equivalence.

Algebra retains the previously reviewed recursion body exactly. timedHistory_snoc preserves every old tagged record, and its final time addition uses the explicit last>=0 and u>=last conditions. ordered_last_nonneg includes n0. weight_snoc_ofReal correctly needs only nonnegativity of the old real weight.

Generic record/step/factor and support/nonnegativity premises remain private ingredients to instantiate from the literal actual model and Geometry. Main density induction and all-n law are still open. No canonical or production changes were made.
''')
outputs=[bind(p) for p in sorted(D.iterdir()) if p.is_file()]
manifest=put('event-algebra-closed-RAW92.native.json',{'schema_version':1,'closed':True,'reviewer':'/root/independent_math91','utc':datetime.now(timezone.utc).isoformat(),'inputs':inputs,'outputs':outputs,'closure':'Owned review/check files only; manifest excludes itself. Frozen source and canonical state untouched. Acceptance restricted to private fragments.'})
print(json.dumps({'decision':bind(decision),'manifest':bind(manifest)},indent=2))
