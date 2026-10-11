import hashlib,json,pathlib,re,subprocess
from datetime import datetime,timezone
R=pathlib.Path('E:/Samplinglib');B=R/'runs/20261007-companion-priority/pbps-actual-ordered-prefix92';D=B/'independent-actual-step-fragment92'
def bind(p):
 b=p.read_bytes();return dict(path=p.as_posix(),raw_sha256=hashlib.sha256(b).hexdigest(),bytes=len(b))
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def put(name,v):
 p=D/name
 with p.open('x',encoding='utf-8',newline='\n') as f:
  if isinstance(v,str):f.write(v)
  else:json.dump(v,f,ensure_ascii=False,indent=2);f.write('\n')
 return p
source=B/'Integrals92.lean';assert bind(source)['raw_sha256']=='7a14a8e37213b002f91902f1e8baa247d9242a6e984b524ca302a00aed82f6a3'
s=source.read_text(encoding='utf-8');part=s.split('private theorem actual_prefix_step_integral',1)[1];seal=read(B/'root.statement-seal92.json');prop=seal['expanded_literal_Prop']
assert part[part.index('    let c :'):part.index('    ∀ n :')]==prop[prop.index('    let c :'):prop.index('    ∀ n :')]
assert re.findall(r'\((h[^\s:]+)\s*:',part[:part.index('    let c :')])==['hα','hαβ','hV','hH','hη','hβη']
clean=re.sub(r'/\-[\s\S]*?\-/','',s);assert not re.search(r'\b(sorry|admit|axiom)\b|Prop\s*:=\s*True|:=\s*trivial',clean)
receipt=read(D/'kernel.receipt.json');assert receipt['exit_code']==0
log=(D/'kernel.stdout.log').read_text();assert ': error' not in log and 'depends on axioms: [propext,\n Classical.choice,\n Quot.sound]' in log
paths=[source,B/'root.statement-seal92.json',B/'Events92.lean',B/'focused/integrals3-explicit-guard-and-map/receipt.json',R/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualAbsoluteNextEventTime.lean',R/'.lake/packages/mathlib/Mathlib/MeasureTheory/Integral/Lebesgue/Map.lean',R/'lake-manifest.json',R/'lean-toolchain',R/'.astis/toolchain/lean-4.33.0-windows/bin/lake.exe',R/'.astis/toolchain/lean-4.33.0-windows/bin/lean.exe']
inputs=[bind(p) for p in paths]
report={
 'schema_version':1,'reviewer':'/root/independent_math91','utc':datetime.now(timezone.utc).isoformat(),
 'decision':'ACCEPT_ACTUAL_STRICT_PREFIX_ONE_STEP_INTEGRAL_RECURRENCE_FRAGMENT',
 'checked_HEAD':subprocess.run(['git','rev-parse','HEAD'],cwd=R,capture_output=True,text=True,check=True).stdout.strip(),
 'inputs':inputs,'source':bind(source),
 'scope':'Frozen Integrals92.lean only. Actual one-step recursion of restricted history-test integrals and measurability of its integrated test J are proved; simplex q_n density induction and full sealed theorem are not accepted here. Active Induction92.lean was not read or modified.',
 'seal_and_binders':{'22_outer_literal_lets_exact':True,'six_original_analytic_binders_retained':True,'IH_binder_added':False,'density_provider_added':False,'probability_law_provider_added':False,'comments':'F is an arbitrary measurable ENNReal test of Hist(n+1), the whole next finite history. The new a/append/D/J definitions are internal concrete constructions, not supplied premises.'},
 'actual_model_audit':[
  'Canonical P, clipped epsilon, literal stopped record recursion, history, actual guards A, prescribed K/q and subtype comap m remain the sealed definitions.',
  'a reads the last actual-history record time, with stopped0 only as an auxiliary totalization. append preserves the complete old history by Fin.snoc; a live last record adds toNNReal(u-a), evolves for u-a and reflects, while a stopped last record appends stopped.',
  'D has the exact strict cutoff a(h)<u<T and is zero for a stopped last record; otherwise it is ofReal(pre-bounce rate at Phi_(u-a) times exp(-hazard over u-a)). No terminal survival or event-count normalization enters.',
  'On the strict live interval the elapsed duration is positive, so its toNNReal is exact and the appended stored time equals u. Outside that interval D is zero; arbitrary values of the totalized append cannot contribute, even for infinite tests by ENNReal multiplication conventions.'
 ],
 'proof_audit':[
  {'step':'invoke actual91','finding':'Calls actual_absolute_next_event_time_law under exactly the six original premises for fixed y,xRef,z0,n. Uses its actual H measurability and specializes the measurable horizon to constant T. No IH or abstract next-step law parameter is used.'},
  {'step':'complete-history test','finding':'Selects the last91 test block on HistNext x Real, with test p->F(p.1). The first projection contains the complete next history, not just its last state. Its measurability is hF composed with measurable_fst. The returned integrated-test measurability is definitionally Measurable J.'},
  {'step':'old guard measurability','finding':'Reproves the ambient history guard measurable using Sum live-range membership, coordinate time measurability and finite strict comparisons. hread is function equality by case analysis, not a new hypothesis. This supplies hA needed for localization on all abstract histories.'},
  {'step':'localize91','finding':'Applies the91 history-localization theorem to A(n,T), producing the integral on C_n intersect H_n^-1(A_n) and the J integral over A_n under map(H_n,P). The density and append matchers coincide definitionally with the concrete definitions; change checks are accepted by the kernel.'},
  {'step':'exact event identity','finding':'hAeq identifies the literal A with the generic guard. record_event_step is instantiated with w->record(y,xRef,z0,epsilon(w)); it proves C_n intersect B_n = B_(n+1) pointwise. Both last records must be live and the inequalities are strictly increasing time and strictly belowT. No almost-sure counting or endpoint convention is substituted.'},
  {'step':'map integral back to clocks','finding':'setLIntegral_map uses the proved hA, hJ and hHist to turn integral_A J d(map H P) into integral_(H^-1A) J(H(w)) dP. This is the standard deterministic pushforward identity, with no conditioning or division by event probability.'},
  {'step':'final result','finding':'The returned conjunction contains actual Measurable J and the asserted equality between the next-prefix F integral and old-prefix J(H) integral under literal P. It is a genuine actual-model recurrence rather than a theorem assuming that recurrence.'}
 ],
 'measure_and_matcher_boundary':[
  'The only measure transport used in this proof is the history pushforward map(H,P) and setLIntegral_map. The copied simplex comap m is not used or altered; no simplex-density identity is smuggled through a measure definition.',
  'Both Sum branches and the strict cutoff are explicit in D and append. Type inspection confirms all branch terms survive elaboration.',
  'All ENNReal tests, including infinity-valued ones, remain admissible. J is produced measurable on the full ambient Hist n, not only almost surely or only on guard support.',
  'Null prefix events require no positive mass. n0 and T0 are within the quantifiers; when T0 the strict next-event domain is empty and D vanishes. Stopped and equal-time records are excluded by the precise event conjunction.',
  'The result is about the literal first-n prefix and the next strict event. It does not assert that every raw zero-clock sequence has the same interior-event count as its strict prefix length.'
 ],
 'direct_ASTIS_proof_ingredient':{'declaration':'AutoSamplingTheory.ExampleCases.ProximalBPS.ActualAbsoluteNextEventTime.actual_absolute_next_event_time_law','use':'H measurability and constant-horizon complete-next-history localized ENNReal test identity including measurability of its parameter integral'},
 'kernel':{'receipt':bind(D/'kernel.receipt.json'),'exit_code':0,'duration_seconds':receipt['duration_seconds'],'complete_private_type_and_final_conjunction_inspected':True,'axioms':['propext','Classical.choice','Quot.sound'],'no_placeholder_closure':True},
 'findings_requiring_changes':[],
 'remaining_open':'Apply the actual recurrence with the n-level proved simplex integral law; identify append and D on prescribed histories with concrete snocPrefix/K/q recurrence; use subtype coordinate transport; derive all-n integral, measure and mass laws and assemble exact sealed public theorem. No full-SA U or VERIFIED credit.',
 'canonical_or_production_mutation':False
}
decision=put('actual-step-review92.native.json',report)
put('actual-step-review92.md','''# Independent actual-step integral fragment92 review

Accepted the frozen actual_prefix_step_integral fragment. Its22 outer definitions and six analytic premises match the seal. Fresh pinned Lean compilation and complete type/axiom inspection passed (exit0,12.594s), with only propext, Classical.choice and Quot.sound.

The proof invokes actual91 at constant horizonT with a complete-next-history test, obtains Measurable J, localizes on the measurable old guard, identifies the exact strict next-event intersection with the next prefix event, and uses setLIntegral_map to return to literal clock space P. No IH, probability-law or density provider is assumed. Match branches, strict cutoffs and full-history dependence are preserved. The copied simplex comap measure is not altered or used to assert an unproved density.

This closes the actual one-step restricted-test recurrence, including all ENNReal tests and measurable J. It does not establish the all-n simplex density law. Active Induction92 was not read or modified; canonical and production files were untouched.
''')
outputs=[bind(p) for p in sorted(D.iterdir()) if p.is_file()]
manifest=put('actual-step-closed-RAW92.native.json',{'schema_version':1,'closed':True,'reviewer':'/root/independent_math91','utc':datetime.now(timezone.utc).isoformat(),'inputs':inputs,'outputs':outputs,'closure':'Owned review and fresh kernel-check artifacts only; self excluded. Frozen inputs and active induction file untouched. Actual one-step fragment acceptance only.'})
print(json.dumps({'decision':bind(decision),'manifest':bind(manifest)},indent=2))
