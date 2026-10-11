import hashlib,json,pathlib,re,subprocess
from datetime import datetime,timezone
R=pathlib.Path('E:/Samplinglib');B=R/'runs/20261007-companion-priority/pbps-actual-ordered-prefix92';D=B/'independent-coordinate-fragments92'
def bind(p):
 b=p.read_bytes();return dict(path=p.as_posix(),raw_sha256=hashlib.sha256(b).hexdigest(),bytes=len(b))
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def put(name,v):
 p=D/name
 with p.open('x',encoding='utf-8',newline='\n') as f:
  if isinstance(v,str):f.write(v)
  else:json.dump(v,f,ensure_ascii=False,indent=2);f.write('\n')
 return p
expected={'Coordinates92':'e28598019893fa1fc2d870f16ddef33160c1f8e3e554d382976e14e4f8a3a162','Recursion92':'dcbdec1d2b48dce5d7dff734fd3a83321b9a97c4035334d4846a41c188d48ee7'}
receipts=[]
for name,h in expected.items():
 p=B/(name+'.lean');assert bind(p)['raw_sha256']==h
 s=re.sub(r'/\-[\s\S]*?\-/','',p.read_text(encoding='utf-8'))
 assert not re.search(r'\b(sorry|admit|axiom)\b|Prop\s*:=\s*True|:=\s*trivial',s)
 receipt=read(D/(name+'.receipt.json'));assert receipt['exit_code']==0 and receipt['terminal_closed']
 log=(D/(name+'.stdout.log')).read_text();assert ': error' not in log
 assert log.count('depends on axioms: [propext,\n Classical.choice,\n Quot.sound]')==(4 if name=='Coordinates92' else 3)
 receipts.append(bind(D/(name+'.receipt.json')))
seal=read(B/'root.statement-seal92.json')
delta='{t | StrictMono (Fin.cons (0 : ℝ) t) ∧ ∀ i, t i < (T : ℝ)}'
assert delta in seal['expanded_literal_Prop'] and delta in (B/'Coordinates92.lean').read_text(encoding='utf-8')
paths=[B/'Coordinates92.lean',B/'Recursion92.lean',B/'root.statement-seal92.json',B/'Geometry92.lean',B/'independent-fragments92/fragment-review92.native.json',B/'focused/coordinates7-typed-interval/receipt.json',B/'focused/recursion3-folded-state/receipt.json',R/'lake-manifest.json',R/'lean-toolchain',R/'.astis/toolchain/lean-4.33.0-windows/bin/lake.exe',R/'.astis/toolchain/lean-4.33.0-windows/bin/lean.exe']
inputs=[bind(p) for p in paths]
report={
 'schema_version':1,'reviewer':'/root/independent_math91','utc':datetime.now(timezone.utc).isoformat(),
 'decision':'ACCEPT_PRIVATE_COORDINATE_AND_RECURSION_FRAGMENTS_ONLY',
 'checked_HEAD':subprocess.run(['git','rev-parse','HEAD'],cwd=R,capture_output=True,text=True,check=True).stdout.strip(),
 'inputs':inputs,
 'scope':'Seven private lemmas in two frozen internal files. No literal-step/factor instantiation or complete actual prefix density law is claimed proved; no SAU VERIFIED or canonical transition.',
 'coordinates':{
  'strictMono_snoc':'Correct equivalence for nonempty prior vector Fin(n+1): strict monotonicity after append iff prior strictness and last previous coordinate<u. Adjacent-index characterization and Fin.succ/castSucc rewrites preserve all comparisons.',
  'simplex_snoc':'Exact ambient-coordinate identity Delta_(n+1) contains snoc(t,u) iff t lies in Delta_n and last(cons0t)<u<T. cons/snoc commute correctly, the original coordinate horizon bounds are retained, and both final inequalities are strict. Delta definition exactly matches the seal.',
  'snoc_volume_preserving':'Correctly maps R x (Fin n -> R) with real product Lebesgue to (Fin(n+1) -> R) with finite-product Lebesgue, sending (u,t) to snoc(t,u). Proof uses inverse volume_preserving_piFinSuccAbove at Fin.last n and insertNth_last. The first product coordinate is the new last time; no Jacobian factor is omitted.',
  'simplex_lintegral_snoc':'Proves the full nonnegative extended-integral iteration identity for every measurable ambient F, including infinite values, using Delta_(n+1).indicator F, measure-preserving integral transport, lintegral_prod_symm and pointwise indicator section equality. Product symmetry gives old vector t outermost and new scalar u innermost. No boundedness, finiteness, signed integrability, or Fubini integrability premise is introduced.',
  'off_simplex_branch':'When t is outside Delta_n, simplex_snoc excludes every snoc(t,u) from Delta_(n+1), so the entire inner indicator integral is zero. This is proved rather than discarded by an unsupported almost-everywhere claim.',
  'measurable_set_premises':'hn and hs are private proof-ingredient premises. Geometry92.ordered_prefix_borel_data supplies the same literal Delta measurability at n and n+1. They must be instantiated from that result, not propagated as new sealed public binders.',
  'edge_cases':['n0: old coordinate space Fin0->R is a singleton with its empty-product mass1; last(cons0t)=0, so the first-event interval is exactly (0,T). All four coordinate lemmas quantify n0.','T0: for n0 the inner interval is (0,0) and both event integrals vanish; for n>0 Delta_n(0) is empty. There is no positive-horizon premise.','All nonnegative integral identities remain meaningful when either side is infinite; this is a Tonelli-type identity, not a finite-integral estimate.']
 },
 'recursion':{
  'state_definition':'Generic Fin.induction from z0, stepping by current absolute time minus preceding cons0 coordinate. It is intentionally total for arbitrary real vectors/durations; no physical support assertion is attached to negative durations.',
  'state_snoc_prefix':'Induction on every old state index j proves extension by u preserves state(j) after castSucc. Initial state is definitional; successor uses the induction hypothesis and exact cons/snoc coordinate identities. It preserves all earlier states, not only the endpoint.',
  'state_snoc_last':'The newly appended final state equals step(u-last(cons0t), old final state). The final Fin index equals successor of old last; state_snoc_prefix supplies the preceding state. Off-by-one and n0 indices are correct.',
  'weight_definition':'Finite real product of factor(previous poststate, elapsed interval). It evaluates factors at state(i.castSucc) before the new step, which is the right location for later rate(Phi_delta(state)) times survival.',
  'weight_snoc':'Fin.prod_univ_castSucc splits exactly one last factor from the previous product. state_snoc_prefix and cons/snoc identities identify all old factors and the last elapsed interval. The result is an equality for arbitrary real factors, with no positivity or measurability premise needed for this algebra.',
  'private_parameters':'Z, step and factor are generic internal algebra parameters. They are not substitutes for the literal dynamics or new hypotheses of the sealed theorem. The later proof must explicitly instantiate them.',
  'n0':'state0 is z0, old weight is the empty product1, last(cons0empty)=0. The last-state and weight formulas reduce to step(u,z0) and factor(z0,u), including u0 or negative auxiliary u.',
  'zero_or_negative_factor':'Real algebra remains valid with zero or negative factors. Nonnegativity needed when relating weight to ENNReal.ofReal must come from the concrete factor, not from this generic lemma.'
 },
 'necessary_integration_adapters_still_open':[
  'Coordinate lintegral lemma is on ambient restricted real volume, while the seal uses the simplex subtype comap measure. Supply measurable-subtype transport and a measurable ambient extension/indicator of the concrete simplex test, or an equivalent subtype adapter; no such adapter is proved in these two files.',
  'Instantiate step(delta,z)=S(xRef,Phi(y,xRef,delta,z)) and identify generic state with sealed zAt, then identify all tagged K records after snoc.',
  'Instantiate factor(z,delta)=rate(xRef,Phi(y,xRef,delta,z))*exp(-Lambda(y,xRef,z,toNNReal(delta))) and identify generic weight with sealed qReal.',
  'Use concrete nonnegativity to transport the real product decomposition through ENNReal.ofReal and obtain the required q recurrence.',
  'Combine these with the actual one-step conditional/history law, measurable-test construction and induction to prove the actual strict-prefix pushforward/density identity; then derive all ENNReal test and mass conclusions.'
 ],
 'kernel':{'receipts':receipts,'both_exit_code_zero':True,'coordinate_seconds':10.344,'recursion_seconds':9.906,'seven_types_inspected':True,'axioms_for_all_seven':['propext','Classical.choice','Quot.sound'],'no_placeholder_closure':True},
 'mathematical_repair_required':False,'findings_requiring_changes':[],
 'canonical_or_production_changes':False,
 'truth_boundary':'Compiled internal coordinates and generic algebra accepted. Full SAU, literal density-law assembly, source/publication admission, VERIFIED, fullA7 and whole-paper results receive no completion credit.'
}
decision=put('coordinate-fragment-review92.native.json',report)
put('coordinate-fragment-review92.md','''# Independent coordinate/recursion fragment review92

Accepted all seven private lemmas in the frozen Coordinates92.lean and Recursion92.lean. Fresh pinned Lean compilation, full type inspection and axiom checks passed for both files; only propext, Classical.choice and Quot.sound appear.

The strict simplex has the correct last-coordinate section (last(cons0t),T). snoc preserves real product Lebesgue, and the nonnegative extended-integral identity places the old vector outside the last-time integral. Its off-simplex branch, n=0 and T=0 cases are correct. The measurable-set premises are internal obligations already supplied by Geometry's Delta measurability result.

The recursive algebra preserves every earlier state, computes the appended last state from the old last state, and splits the real product into the old weight and exactly one final factor. Generic step/factor parameters remain private algebra arguments.

The subtype-comap integral adapter, concrete step/factor and tagged-history instantiations, ENNReal weight decomposition, and actual density induction remain to be assembled. These fragments do not prove the full sealed density law or complete the SAU. No canonical or production file was changed.
''')
outputs=[bind(p) for p in sorted(D.iterdir()) if p.is_file()]
manifest=put('coordinate-review-closed-RAW92.native.json',{'schema_version':1,'closed':True,'reviewer':'/root/independent_math91','utc':datetime.now(timezone.utc).isoformat(),'inputs':inputs,'outputs':outputs,'closure':'Owned check scripts, exact source copies, terminal logs/receipts and review outputs only; excludes own bytes. Frozen inputs and canonical state unchanged. Private-fragment acceptance only.'})
print(json.dumps({'decision':bind(decision),'manifest':bind(manifest)},indent=2))
