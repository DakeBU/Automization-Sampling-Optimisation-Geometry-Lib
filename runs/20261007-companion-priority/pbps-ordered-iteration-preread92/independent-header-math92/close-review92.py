import hashlib,json,pathlib,re,subprocess
from datetime import datetime,timezone
R=pathlib.Path('E:/Samplinglib')
B=R/'runs/20261007-companion-priority/pbps-ordered-iteration-preread92'
D=B/'independent-header-math92'
def bind(p):
 b=p.read_bytes();return dict(path=p.as_posix(),raw_sha256=hashlib.sha256(b).hexdigest(),bytes=len(b))
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def put(name,obj):
 p=D/name
 with p.open('x',encoding='utf-8',newline='\n') as f:
  if isinstance(obj,str):f.write(obj)
  else:json.dump(obj,f,ensure_ascii=False,indent=2);f.write('\n')
 return p
packet_path=B/'prospective-header/review-packet92.v2.json'
packet=read(packet_path)
inputs=[bind(packet_path)]
for k in ['header','source_recommendation','source_graph','source_coverage','source_target_acceptance']:
 entry=packet[k];actual=bind(R/entry['path']);assert actual['raw_sha256']==entry['raw_sha256'] and actual['bytes']==entry['bytes'];inputs.append(actual)
more=[R/'lake-manifest.json',R/'lean-toolchain',R/'.astis/toolchain/lean-4.33.0-windows/bin/lake.exe',R/'.astis/toolchain/lean-4.33.0-windows/bin/lean.exe',R/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualAbsoluteNextEventTime.lean',R/'.lake/packages/mathlib/Mathlib/MeasureTheory/Measure/Comap.lean',R/'.lake/packages/mathlib/Mathlib/MeasureTheory/Measure/Restrict.lean',R/'.lake/packages/mathlib/Mathlib/MeasureTheory/Constructions/Pi.lean',R/'.lake/packages/mathlib/Mathlib/Probability/Process/HittingTime.lean',R/'.astis/toolchain/lean-4.33.0-windows/src/lean/Init/Data/Fin/Lemmas.lean',R/'.lake/packages/mathlib/Mathlib/Data/Fin/Tuple/Basic.lean',R/'runs/20261007-companion-priority/phase-pbps-gamma-preread57/primary-pbps.exactraw.snapshot.html',B/'independent-target-review/v2-recheck-closed-RAW92.native.json',R/packet['compiler_receipt']]
inputs += [bind(p) for p in more]
header=(R/packet['header']['path']).read_text(encoding='utf-8')
parent=(R/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualAbsoluteNextEventTime.lean').read_text(encoding='utf-8')
names=re.findall(r'^\s+let (\S+)\s',header,re.M)
assert names==packet['literal_let_names'] and len(names)==25
shared=header[header.index('    let c :'):header.index('    let Rec :=')]
assert shared==parent[parent.index('    let c :'):parent.index('    let waitObs :')]
assert not re.search(r'\b(sorry|admit|axiom|theorem)\b',re.sub(r'/\-[\s\S]*?\-/','',header))
receipt=read(D/'kernel-v3.receipt.json');assert receipt['exit_code']==0 and receipt['terminal_closed']
log=(D/'kernel-v3.stdout.log').read_text()
assert ': error' not in log
assert "depends on axioms: [propext, Classical.choice.{u}, Quot.sound.{u}]" in log
assert '∫⁻ (t : Prefix n T)' in log and 'P B) 1' in log
let_audit=[
 ('c','E -> E -> E','Literal center y - eta grad V(xRef).'),
 ('Φ','E -> E -> Real -> Phase -> Phase','Source harmonic flow, sqrt eta factors and momentum sign correct; all real auxiliary durations defined.'),
 ('S','E -> Phase -> Phase','Expanded reflection. Lean real division by zero equals zero, giving identity momentum at zero residual; no continuity assumption.'),
 ('rate','E -> Phase -> Real','sqrt eta times max 0 inner(p,residual); pre-bounce evaluation used below.'),
 ('Λ','E -> E -> Phase -> NNReal -> Real','Interval integral from zero to nonnegative duration; continuous rate along flow makes the finite integral the ordinary cumulative hazard.'),
 ('τ','E -> E -> Phase -> NNReal -> WithTop NNReal','hittingAfter of Lambda-e in Ici0 from time0 is the closed threshold infimum, top on empty crossing, zero at e0.'),
 ('next','E -> E -> NNReal -> Rec -> Rec','Stopped is absorbing; top threshold stops; finite threshold adds to stored time and reflects flowed phase. untopD0 is used only on finite branch.'),
 ('record','E -> E -> Phase -> (Nat -> NNReal) -> Nat -> Rec','Nat.rec initial live(0,z0), step k consumes clock k. Matches source E_(k+1).'),
 ('P','Measure (Nat -> Real)','Literal infinitePi of expMeasure1, not a supplied probability or law provider.'),
 ('ε','(Nat -> Real) -> Nat -> NNReal','Real.toNNReal equals max(raw,0) and preserves canonical positive clocks almost surely.'),
 ('history','E -> E -> Phase -> (n:Nat) -> (Nat -> Real) -> (Fin(n+1) -> Rec)','Every record at j.val is retained, including initial record.'),
 ('Rec','Type','Sum (NNReal x Phase) Unit with standard measurable Sum/product structures; stopped is not an event.'),
 ('Hist','Nat -> Type','Full ambient finite product Fin(n+1) -> Rec; no reachable-history restriction on tests.'),
 ('readTime','Rec -> Real','Live stored NNReal coerces to Real; stopped returns0 auxiliary only. Live guard in A blocks false finite events.'),
 ('Δ','(n:Nat) -> NNReal -> Set (Fin n -> Real)','StrictMono of Fin.cons0t gives 0<t1<...<tn; every t_i<T. At n0 conditions are vacuous, including T0.'),
 ('Prefix','(n:Nat) -> NNReal -> Type','Exact Borel strict-simplex subtype. No off-simplex values of K or q are introduced.'),
 ('m','(n:Nat) -> (T:NNReal) -> Measure(Prefix n T)','Comap along injective measurable subtype inclusion. map_comap_subtype_coe, once Delta measurability is proved, identifies pushforward with restricted finite-product real volume. Empty-product volume is Dirac via Measure.volume_pi_eq_dirac.'),
 ('zAt','E -> E -> Phase -> (n:Nat) -> (T:NNReal) -> Prefix n T -> Fin(n+1) -> Phase','Fin.induction_zero gives z0. Fin.induction_succ advances state at i.castSucc by t_i-(cons0t at i.castSucc), then reflects; indices yield preceding prescribed poststate and correct elapsed duration.'),
 ('K','E -> E -> Phase -> (n:Nat) -> (T:NNReal) -> Prefix n T -> Hist n','All prescribed records live at cons0t and zAt. toNNReal is exact for zero/positive subtype times.'),
 ('qReal','E -> E -> Phase -> (n:Nat) -> (T:NNReal) -> Prefix n T -> Real','Product binder contains both rate(Phi_delta preceding poststate) and exp(-Lambda(preceding poststate,delta)). Delta positivity makes toNNReal duration exact. Empty product1; no terminal survival or factorial.'),
 ('q','E -> E -> Phase -> (n:Nat) -> (T:NNReal) -> Prefix n T -> ENNReal','ofReal of finite nonnegative real product. Product nonnegativity is concluded, not assumed.'),
 ('A','(n:Nat) -> NNReal -> Set(Hist n)','All records live, all readTimes strictly increasing, positive-index times belowT. Abstract A does not fix record0 time/state; only its pullback along literal actual H denotes the prefix event.'),
 ('H','(Nat -> Real) -> Hist n','Literal actual history for fixed y,xRef,z0,n, with H(w)(0)=live(0,z0) for all raw inputs.'),
 ('B','Set(Nat -> Real)','H preimage A. Consequently exactly the first n actual records are live with0<T1<...<Tn<T, no condition on record(n+1); n0 gives all inputs.'),
 ('obs','(Nat -> Real) -> Fin n -> Real','Stored times of actual records1 throughn. OnB they determine a unique simplex value; all-input measurable observer has auxiliary stopped0 values.')
]
assert [x[0] for x in let_audit]==names
conclusions=[
 'MeasurableSet Delta and A: finite coordinate strict inequalities and live Sum-tag membership are Borel.',
 'Joint Measurable K and q: parameter domain ((E x E) x Phase) x Prefix unpacks to y,xRef,z0,t exactly; V,eta,n,T fixed. C2 yields continuous gradient, Borel zero-normal reflection, continuous parameter hazard integrals, hence finite recursive Borel maps. No regularity in V or eta asserted.',
 'For every y,xRef,z0,n,T: H, B and obs are measurable under the literal actual recursion; no input measurability provider.',
 'qReal nonnegative for each simplex point follows nonnegative rate and positive exponential; finite by finite coordinates and finite-time continuous hazard.',
 'For every raw w in B, exists t with t.val=obs(w) and H(w)=K(t): deterministic induction on finite records; strict times ensure each recorded finite wait equals successive stored-time differences. No almost-sure exception or positive-clock premise is needed for this reconstruction.',
 'Pushforward of P restricted to B under H equals pushforward of m.withDensity(q) under K: the complete-history finite-prefix law, not an endpoint marginal or an exactly-n count law.',
 'Every measurable F:Hist n -> ENNReal satisfies the unnormalized integral identity. Infinite test values and null-event restrictions are allowed; multiplication follows ENNReal including0*infinity0. No integrability binder.',
 'Integral q=P(B), and P(B)<=1: consistent mass corollaries from F1 and canonical probability normalization; no external normalization premise.'
]
report={
 'schema_version':1,'reviewer':'/root/independent_math91','utc':datetime.now(timezone.utc).isoformat(),
 'checked_HEAD':subprocess.run(['git','rev-parse','HEAD'],cwd=R,capture_output=True,text=True,check=True).stdout.strip(),
 'decision':'ACCEPT_PROSPECTIVE_HEADER92_MATHEMATICS_AND_ELABORATED_STATEMENT',
 'header':bind(R/packet['header']['path']), 'inputs':inputs,
 'scope':'Independent whole prospective proposition review against accepted target92v2; proposition definition elaborated and inspected. No theorem BODY exists, no truth proof/kernel proof acceptance, no canonical SAU transition, no accepted seal artifact asserted.',
 'analytic_binder_audit':{'names':['hα','hαβ','hV','hH','hη','hβη'],'exactly_original_six':True,'explanation':'Positive alpha, alpha<=beta, C2, global two-sided Hessian quadratic form bounds, positive eta, beta*eta<=1. Since beta>=alpha>0, last bound is equivalent to source eta<=1/beta. NNReal alpha/beta encoding adds no source restriction. Finite-dimensional real inner-product generalization including rank0 is the explicitly accepted typing extension.','extra_provider_binders':[],'unused_parameter_warnings':'Expected for a Prop-valued definition whose predicate does not inspect proof witnesses. These premises remain in its declaration telescope and must remain on the proving theorem.'},
 'literal_shared_actual_object_block_matches_verified91':True,
 'let_audit':[dict(name=n,type=t,semantic_check=s) for n,t,s in let_audit],
 'whole_conclusion_audit':conclusions,
 'edge_case_and_counterexample_audit':[
  'n0: Delta0 is singleton for everyT, Fin1 StrictMono is vacuous, B=univ, H=K deterministic initial record, q=1; comap of empty-product volume has mass1.',
  'n>0,T0: Delta empty and B impossible because actual record0 has time0 and strict monotonicity forces later time positive while horizon requires negative.',
  'Rank0 or zero hazard: positive clocks stop; zero clocks give zero waits excluded by strict B; n>0 density0 and restricted law0.',
  'Infinite wait/stopped histories cannot enterB at required indices; stopped time0 totalization cannot fabricate a strict live prefix.',
  'Raw zero/negative clocks are included in the ambient space; first-n strict event need not equal a raw interior-event count. V=x^2/2,z0=(1,1),e1=0,e2=1/4,T=pi/2 retains T1=0,T2=5pi/12 counterexample to pointwise counting, but no such counting clause exists in header.',
  'Full history includes all earlier poststates and times. Abstract A may contain initial positive times or unrelated states; only actual pullbackB is claimed to be E_n, so this is not an excess theorem obligation or a false equality on all ambient histories.'
 ],
 'kernel_check':{'receipt':bind(D/'kernel-v3.receipt.json'),'exit_code':0,'duration_seconds':receipt['duration_seconds'],'definition_axioms':['propext','Classical.choice','Quot.sound'],'all25_lets_and_final_conjuncts_printed':True,'no_placeholder_closure':True,'qualification':'Axiom census concerns definitions of the proposition; it is not evidence that the proposition is proved.','retained_negatives':[bind(D/'kernel.receipt.json'),bind(D/'kernel-v2.receipt.json')],'negative_cause':'Inspection-only unsupported pp.width and guessed namespaces of root-level map_comap_subtype_coe; corrected suffix, exact header bytes unchanged.'},
 'findings_requiring_header_change':[],
 'remaining_proof_obligations':'All mathematical conclusions still require proof, including subtype-volume transport, finite induction/product coordinate transport, joint measurability, and actual prefix law. Full terminal survival/count partition/path-functionalA7 remain outside this header.',
 'authorized_changes_made':'New files only in independent-header-math92; no production/canonical/header edits.'
}
decision=put('header-math-review92.native.json',report)
put('header-math-review92.md','''# Independent prospective-header92 mathematical review

Accepted the exact 6445-byte header, SHA256 9ad92c3ba89af78f3096342f7663bc547e6c03b6ce8173645cc13030d24bcd1f, as a mathematically correct elaboration of the accepted v2 target. All 25 let definitions and every conclusion were reviewed; the original six analytic premises remain, with no extra provider.

The literal clock/actual-recursion block matches verified91. The subtype comap measure is restricted product Lebesgue, including mass one at n=0. Fin.induction and the rate product use the preceding poststate and pre-bounce rate. Abstract A need not fix its first record because the actual H does; its pullback is exactly the strict first-n prefix. Pointwise actual/prescribed identification on that event and all ENNReal complete-history tests are correct. The zero-clock counting counterexample remains outside any claimed pointwise counting equivalence.

Fresh pinned Lean elaboration/kernel printing passed (exit0,10.921s), with only standard propext/Classical.choice/Quot.sound axioms for the proposition definition. Two failed inspection suffixes are retained: unsupported pp.width and wrong namespaces for the root-level map_comap_subtype_coe. Neither changed or refuted the prospective header.

No theorem body exists and no theorem has been proved by this check. This review does not create or accept a nonexistent Statement Seal artifact and makes no canonical transition. All proof obligations remain with the proving worker.
''')
outputs=[bind(p) for p in sorted(D.iterdir()) if p.is_file()]
manifest=put('header-review-closed-RAW92.native.json',{'schema_version':1,'closed':True,'reviewer':'/root/independent_math91','utc':datetime.now(timezone.utc).isoformat(),'inputs':inputs,'outputs':outputs,'closure':'All owned scripts, copies, logs, receipts and review outputs included; original negative inspections preserved. Self excluded. No production or canonical modification.'})
print(json.dumps({'decision':bind(decision),'closed_manifest':bind(manifest)},indent=2))
