import hashlib,json,pathlib,re,subprocess
from datetime import datetime,timezone
R=pathlib.Path('E:/Samplinglib');B=R/'runs/20261007-companion-priority/pbps-actual-ordered-prefix92';D=B/'independent-measure-closure-fragment92'
def bind(p):
 b=p.read_bytes();return dict(path=p.as_posix(),raw_sha256=hashlib.sha256(b).hexdigest(),bytes=len(b))
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def put(name,v):
 p=D/name
 with p.open('x',encoding='utf-8',newline='\n') as f:
  if isinstance(v,str):f.write(v)
  else:json.dump(v,f,ensure_ascii=False,indent=2);f.write('\n')
 return p
source=B/'MeasureClosure92.lean';assert bind(source)['raw_sha256']=='0aeb5f6e6ac9b04b0deb724755f2bd241047634b86dc60fadba3f12fecd9b19d'
clean=re.sub(r'/\-[\s\S]*?\-/','',source.read_text());assert not re.search(r'\b(sorry|admit|axiom)\b|Prop\s*:=\s*True|:=\s*trivial',clean)
receipt=read(D/'kernel.receipt.json');assert receipt['exit_code']==0
log=(D/'kernel.stdout.log').read_text();assert ': error' not in log and 'depends on axioms: [propext,\n Classical.choice,\n Quot.sound]' in log
paths=[source,B/'focused/closure2-explicit-integrand/receipt.json',B/'root.statement-seal92.json',R/'.lake/packages/mathlib/Mathlib/MeasureTheory/Measure/Restrict.lean',R/'lake-manifest.json',R/'lean-toolchain',R/'.astis/toolchain/lean-4.33.0-windows/bin/lake.exe',R/'.astis/toolchain/lean-4.33.0-windows/bin/lean.exe']
inputs=[bind(p) for p in paths]
report={
 'schema_version':1,'reviewer':'/root/independent_math91','utc':datetime.now(timezone.utc).isoformat(),
 'decision':'ACCEPT_GENERIC_PRIVATE_ALL_TESTS_TO_LAW_AND_MASS_CONVERSION',
 'checked_HEAD':subprocess.run(['git','rev-parse','HEAD'],cwd=R,capture_output=True,text=True,check=True).stdout.strip(),
 'inputs':inputs,'source':bind(source),
 'scope':'Frozen private law_and_mass_of_all_tests only. It consumes an already-proved all-test identity. It does not prove the actual all-n history density law and is not a new source-backed SAU or VERIFIED result. Active Induction92 was not read or modified.',
 'expanded_interface':{'spaces':'Arbitrary measurable Omega,X,H','measures':'P probability on Omega; arbitrary m onX','maps':'Measurable history:Omega->H, K:X->H, q:X->ENNReal','event':'Arbitrary B subsetOmega','premise':'For every measurable ENNReal F onH, integral_B F(history) dP equals integral F(K)*q dm','conclusions':['map history (P.restrict B) = map K (m.withDensity q)','integral q dm = P(B)','P(B)<=1']},
 'proof_audit':[
  {'step':'measure extensionality','finding':'Measure.ext_of_lintegral reduces equality of the two history measures to equality against every measurable ENNReal test F. This does not require either resulting measure to be a probability measure or a supplied density certificate.'},
  {'step':'pushforward integrals','finding':'lintegral_map is applied with measurable F and each proved/measurable map, respectively history under P.restrict B and K under m.withDensity q. Both domains and restrictions remain exactly those of the private interface.'},
  {'step':'weighted measure','finding':'lintegral_withDensity_eq_lintegral_mul uses hq and the explicitly typed measurable integrand t->F(K(t)), obtained by hF.comp hK. The formula has density-first multiplication; a pointwise mul_comm integral equality aligns it with the premise F(K(t))*q(t). Infinite values obey ENNReal conventions and no integrability is introduced.'},
  {'step':'mass','finding':'Specializes htest to constant1, reverses the resulting equality, and simplifies one_mul and lintegral_const. (P.restrict B)(univ)=P(univ intersectB)=P(B) by restrict_apply at measurable univ. The equality is derived from the test law, not assumed as normalization.'},
  {'step':'bound','finding':'prob_le_one supplies P(B)<=1 solely from IsProbabilityMeasure P. No positive probability of B or normalization of P.restrict B is required.'}
 ],
 'edge_case_audit':[
  'B may be null or empty, and test/density values may be infinity. The proof uses nonnegative integrals only, so no boundedness, signed integrability or finite-value premise is hidden.',
  'The generic theorem does not require MeasurableSet B: restrict_apply here needs measurability of its evaluated set univ, not of B. The actual application separately produces measurability of its prefix event.',
  'm need not be probability or sigma-finite. No such instance is inferred or inserted in the elaborated type.',
  'Measurable q and K suffice for the withDensity integrand transformation. No assertion that q itself is normalized is used before taking F1.',
  'No parameter n or horizon enters this generic interface. Coverage of n0/T0 or other actual-process boundaries depends on the all-test identity supplied by the concrete proof, not this conversion alone.'
 ],
 'public_binder_boundary':'Every generic parameter/premise is an internal interface ingredient. The main theorem must instantiate P,m,B,history,K,q with its sealed literal objects, produce their measurability and canonical probability normalization, and provide htest from the actual induction. In particular htest is not permitted to become a new public premise or be counted as the density-law proof.',
 'kernel':{'receipt':bind(D/'kernel.receipt.json'),'exit_code':0,'duration_seconds':receipt['duration_seconds'],'full_generic_type_inspected':True,'axioms':['propext','Classical.choice','Quot.sound'],'no_placeholder_closure':True},
 'findings_requiring_changes':[],
 'remaining_open':'Actual all-n ENNReal test integral law and concrete instantiation/assembly into the sealed public theorem, followed by whole-result independent/source/publication review. No full mathematical completion follows from this private conversion.',
 'canonical_or_production_mutation':False
}
decision=put('measure-closure-review92.native.json',report)
put('measure-closure-review92.md','''# Independent measure-closure fragment92 review

Accepted the frozen private law_and_mass_of_all_tests conversion. Fresh pinned Lean full-type and axiom checking passed (exit0,9.641s), with only propext, Classical.choice and Quot.sound.

The proof uses nonnegative-test measure extensionality, measurable pushforward integrals and the withDensity formula with explicit composed integrand. Multiplication order is reconciled correctly. Constant test1 yields integral q=P(B), and the probability property of P yields P(B)<=1. Null events, infinite test values and arbitrary m are supported; no normalization of the restricted law is assumed.

The all-test identity is a genuine private premise of this conversion and must be constructed by the actual induction. It cannot be added to the sealed public theorem as an assumption. This review does not establish the all-n density law. The active induction file and canonical/production state were untouched.
''')
outputs=[bind(p) for p in sorted(D.iterdir()) if p.is_file()]
manifest=put('measure-closure-closed-RAW92.native.json',{'schema_version':1,'closed':True,'reviewer':'/root/independent_math91','utc':datetime.now(timezone.utc).isoformat(),'inputs':inputs,'outputs':outputs,'closure':'Owned generic-closure review and fresh checks only; excludes itself. Frozen inputs unchanged. Private conversion acceptance only.'})
print(json.dumps({'decision':bind(decision),'manifest':bind(manifest)},indent=2))
