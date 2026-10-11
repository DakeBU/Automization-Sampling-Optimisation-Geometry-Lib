import hashlib,json,pathlib,re,subprocess
from datetime import datetime,timezone
R=pathlib.Path('E:/Samplinglib')
B=R/'runs/20261007-companion-priority/pbps-actual-ordered-prefix92'
D=B/'independent-fragments92'
def bind(p):
 b=p.read_bytes();return dict(path=p.as_posix(),raw_sha256=hashlib.sha256(b).hexdigest(),bytes=len(b))
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def put(name,obj):
 p=D/name
 with p.open('x',encoding='utf-8',newline='\n') as f:
  if isinstance(obj,str):f.write(obj)
  else:json.dump(obj,f,ensure_ascii=False,indent=2);f.write('\n')
 return p
geo=B/'Geometry92.lean';seal_path=B/'root.statement-seal92.json'
assert bind(geo)['raw_sha256']=='a415510aa496843c723f7dea200a1532714277db9e026cabec4b521efd3c6dd4'
s=geo.read_text(encoding='utf-8');seal=read(seal_path);prop=seal['expanded_literal_Prop']
canonical=prop[prop.index('    let c :'):prop.index('    ∀ n :')]
declarations=['ordered_prefix_borel_data','actual_prefix_identification']
for name in declarations:
 part=s.split('private theorem '+name,1)[1]
 block=part[part.index('    let c :'):part.index('    ∀ n :')]
 assert block==canonical,name
 assert re.findall(r'^    let (\S+)\s',block,re.M)==['c','Φ','S','rate','Λ','τ','next','record','P','ε','history','Rec','Hist','readTime','Δ','Prefix','m','zAt','K','qReal','q','A']
 header=part[:part.index('    let c :')]
 assert re.findall(r'\((h[^\s:]+)\s*:',header)==['hα','hαβ','hV','hH','hη','hβη']
clean=re.sub(r'/\-[\s\S]*?\-/','',s)
assert not re.search(r'\b(sorry|admit|axiom)\b|Prop\s*:=\s*True|:=\s*trivial',clean)
receipt=read(D/'kernel.receipt.json');assert receipt['exit_code']==0
log=(D/'kernel.stdout.log').read_text(encoding='utf-8')
assert ': error' not in log
assert log.count('depends on axioms: [propext,\n Classical.choice,\n Quot.sound]')==2
paths=[geo,seal_path,B/'focused/geometry10-zero-time/receipt.json',R/'lake-manifest.json',R/'lean-toolchain',R/'.astis/toolchain/lean-4.33.0-windows/bin/lake.exe',R/'.astis/toolchain/lean-4.33.0-windows/bin/lean.exe']
paths += [R/('AutoSamplingTheory/ExampleCases/ProximalBPS/'+name+'.lean') for name in ['ActualAbsoluteNextEventTime','ActualHarmonicFlow','ActualBounceRate','ActualHazardClock']]
inputs=[bind(p) for p in paths]
report={
 'schema_version':1,'reviewer':'/root/independent_math91','utc':datetime.now(timezone.utc).isoformat(),
 'decision':'ACCEPT_TWO_INTERNAL_FRAGMENTS_ONLY',
 'checked_HEAD':subprocess.run(['git','rev-parse','HEAD'],cwd=R,capture_output=True,text=True,check=True).stdout.strip(),
 'geometry':bind(geo),'statement_seal':bind(seal_path),'inputs':inputs,
 'scope':'Review of ordered_prefix_borel_data and actual_prefix_identification in frozen internal Geometry92.lean only. Not acceptance of the complete sealed actual_ordered_prefix_law, not PROVED_LOCAL/VERIFIED/SAU completion.',
 'seal_comparison':{'both_22_outer_literal_let_blocks_exact':True,'six_original_analytic_binders_exact':['hα','hαβ','hV','hH','hη','hβη'],'source_hypothesis_additions':[],'actual_history_equals_prescribed_history_assumed':False,'arbitrary_density_measurability_or_probability_provider_assumed':False,'explanation':'Both theorem statements copy all22 outer lets of the sealed proposition byte-for-byte after newline normalization; identification also uses the same literal H/B/obs definitions. Fragment conclusions are genuine subclaims of the seal.'},
 'ordered_prefix_borel_data':{
  'accepted_conclusions':['MeasurableSet Delta(n,T)','MeasurableSet A(n,T)','Joint Measurable K in y,xRef,z0,t on the simplex subtype for fixed V,eta,n,T','Joint Measurable q in the same variables','qReal>=0 at every simplex point'],
  'proof_audit':[
   'measurable_cons_zero splits Fin0/successor and uses measurable coordinate evaluation. simplex_measurable expresses strict monotonicity and horizon bounds as finite/countable intersections of Borel strict inequalities.',
   'readTime is measurable by Sum elimination; the live tag is the measurable range of Sum.inl. history_guard_measurable combines live-tag predicates, strict coordinate ordering and horizon cutoffs. It does not assume realizability of abstract histories.',
   'hd constructs measurable elapsed differences from subtype coordinates. hz is an actual Fin.induction proof: base state is z0, successor composes previous state with joint harmonic flow and Borel reflection. There is no continuity-of-bounce assumption.',
   'K measurability follows coordinatewise from toNNReal of stored times and hz, followed by Sum.inl. Parameter tuple projections encode y,xRef,z0 without dropping any parameter.',
   'hf is the pre-bounce flowed state. q measurability follows finite product of joint rate and exp of negative joint integrated hazard, then ENNReal.ofReal. Each elapsed duration is the preceding simplex-coordinate difference.',
   'qReal nonnegativity is proved directly by Finset.prod_nonneg, sqrt_nonneg, max0 nonnegativity and exp_pos. It is not supplied by a density-law hypothesis.'
  ],
  'direct_ASTIS_proof_ingredients':[
   {'declaration':'AutoSamplingTheory.ExampleCases.ProximalBPS.ActualHarmonicFlow.actual_harmonic_flow_laws','projection':'.2.1','use':'joint flow measurability'},
   {'declaration':'AutoSamplingTheory.ExampleCases.ProximalBPS.ActualBounceRate.actual_bounce_rate_energy_laws','projection':'.1 and .2.2.1','use':'joint Borel reflection and rate measurability'},
   {'declaration':'AutoSamplingTheory.ExampleCases.ProximalBPS.ActualHazardClock.actual_integrated_hazard_clock_laws','projection':'.2.1','use':'joint integrated-hazard measurability'}
  ],
  'dependency_note':'The import ActualAbsoluteNextEventTime makes these parents available; its next-event density theorem is not directly invoked in this fragment. Dependency list here is source proof-reference inspection, not a separately computed transitive Lean constant census.'
 },
 'actual_prefix_identification':{
  'accepted_conclusion':'For every n,T,y,xRef,z0 and every raw w in B=H^-1(A), there exists simplex t with t.val=obs(w) and H(w)=K(t) as complete finite histories.',
  'proof_audit':[
   'Set H to the literal actual history. tv reads records1..n. htimes proves cons0tv equals all actual record times by Fin.cases; initial time0 is definitional from Nat.rec live(0,z0), not an extra premise about arbitrary histories.',
   'hmem transfers strict ordering and all horizon inequalities from hw (membership in the actual guard pullback) to tv. The constructed t=(tv,hmem) is the same observed time vector; existential equality t.val=obs is reflexivity.',
   'Function extensionality and Fin.induction prove equality at every record. At zero, unfolding literal record/Fin.induction/K proves initial time and state equality. No positive-time assumption is imposed at n0.',
   'At successor, induction hypothesis identifies the previous actual record with live(a,z) where z is the prescribed previous poststate. Definitional actual recursion gives H(i.succ)=next(e_i,H(i.castSucc)). This is not an assumed history correspondence.',
   'hfinite derives non-top wait from the next actual record being live: a top wait would be stopped and contradict Sum constructor disjointness. This excludes the top branch before the default-valued time observer can be used.',
   'Reading times from hprev and hrec gives a=s and a+d=tv(i); arithmetic derives d=tv(i)-s. Nonnegativity of a+d justifies Real.toNNReal(tv(i))=a+d without truncating a genuine recorded time.',
   'Substitution of the time and duration identities into the actual next-record equation gives the prescribed successor including both stored cumulative time and reflected poststate. The equality is whole-history, not just terminal phase or position.'
  ],
  'pointwise_scope':'All raw w in B, including off-probability-support inputs; no almost-sure qualifier, no positive-clock support premise, no nonaccumulation premise.',
  'direct_ASTIS_proof_ingredients':[],
  'dependency_note':'Proof unfolds literal stopped recursion and uses elementary Sum/Fin/NNReal/arithmetic facts. All six analytic premises remain in the internal theorem statement although the deterministic identification proof does not need their analytic strength.'
 },
 'boundary_and_counterexample_audit':[
  'n0: guard pullback includes all actual histories because initial record is live0 and Fin1 strictness is vacuous; t is the empty vector and initial record equality is proved. qReal empty-product nonnegativity holds. This fragment does not prove the mass-one subtype measure identity.',
  'T0,n>0: the strict prefix pullback is impossible, and the simplex is empty. The conditional identification is correctly vacuous; no branch asserts a finite positive event below0.',
  'Any zero/negative clipped clock among required first-n events yields a zero wait and violates strict ordering, unless n0 has no required event. No raw count-equivalence is asserted. The earlier null-input T1=0,T2=5pi/12 counterexample therefore remains outsideB for n1.',
  'A stopped required record violates the explicit live guard; infinite waits are contradicted locally before using untopD0. Later clocks and records aftern are unrestricted.',
  'Abstract A does not constrain initial time/state, but identification applies only to H(w), whose initial record is fixed. Joint Borel statements apply to all prescribed parameters and simplex points, not only actual attainable histories.',
  'Rank0 and zero residual normals are supported: reflection is Borel from its parent, no continuity or nonzero-normal premise is inserted. Empty or zero-rate cases do not undermine the finite product or deterministic reconstruction.'
 ],
 'kernel':{'receipt':bind(D/'kernel.receipt.json'),'exit_code':0,'duration_seconds':receipt['duration_seconds'],'fresh_exact_source_prefix':True,'both_types_expanded':True,'axioms_for_each':['propext','Classical.choice','Quot.sound'],'no_sorryAx_or_extra_axiom':True,'source_fake_closure_scan_passed':True},
 'remaining_sealed_conclusions_not_closed_by_these_fragments':[
  'Actual H/B/obs measurability as packaged conclusions of the final public theorem',
  'Subtype comap-volume transport and n0 probability/density base case',
  'Inductive actual complete-history pushforward density law on the strict simplex',
  'Every ENNReal complete-history integral identity and total-mass equality/bound',
  'Assembly into the exact sealed public theorem and its independent source/publication admission'
 ],
 'findings_requiring_changes':[],
 'canonical_or_production_mutation':False
}
decision=put('fragment-review92.native.json',report)
put('fragment-review92.md','''# Independent internal-fragment review92

Accepted only the two frozen Geometry92 fragments (RAW a415510aa496843c723f7dea200a1532714277db9e026cabec4b521efd3c6dd4). Their22 outer definitions exactly match the seal, and both retain only the six original analytic premises.

ordered_prefix_borel_data proves the simplex/history guards Borel, K and q jointly Borel in all specified parameters, and qReal nonnegative. It composes fixed harmonic-flow, reflection/rate and hazard measurability parents, with finite-state induction and finite products.

actual_prefix_identification proves, for every raw input in the strict actual prefix event, the observed time vector belongs to the simplex and the entire actual history equals its prescribed counterpart. The equality is derived from the literal recursion; it is not a premise. The proof explicitly uses initial live(0,z0), excludes the top/stopped branch from the live guard, and derives elapsed time from consecutive stored times. The n0 and off-support/zero-clock boundaries are preserved.

Fresh pinned Lean compilation and type/axiom printing passed in10.454s; both fragments use only propext, Classical.choice and Quot.sound. No mathematical repairs found. Subtype-measure transport, density induction, all-test integral laws, mass conclusions and final public theorem assembly remain open in this reviewed file. No SAU/VERIFIED transition or canonical edit was made.
''')
outputs=[bind(p) for p in sorted(D.iterdir()) if p.is_file()]
manifest=put('fragment-review-closed-RAW92.native.json',{'schema_version':1,'closed':True,'reviewer':'/root/independent_math91','utc':datetime.now(timezone.utc).isoformat(),'inputs':inputs,'outputs':outputs,'closure':'Owned review/check files only; manifest excludes itself. Frozen geometry and canonical state untouched. Two internal fragments accepted, not the entire SAU or sealed density theorem.'})
print(json.dumps({'decision':bind(decision),'manifest':bind(manifest)},indent=2))
