from pathlib import Path
import datetime,hashlib,json,re
R=Path('E:/Samplinglib');O=Path(__file__).parent;B=O.parent
PRE=R/'runs/20261007-companion-priority/pbps-conditional-next-wait-density-preread89'
M=R/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualConditionalNextWaitDensity.lean'
def pin(p):
 p=Path(p);b=p.read_bytes();return dict(path=p.relative_to(R).as_posix(),raw_sha256=hashlib.sha256(b).hexdigest(),bytes=len(b))
def read(p):return json.loads(p.read_text('utf8'))
def put(n,v):
 with (O/n).open('x',encoding='utf8',newline='\n') as f:json.dump(v,f,ensure_ascii=False,indent=2);f.write('\n')
 return pin(O/n)
assert pin(M)['raw_sha256']=='36813b659cbdbb4b31c6300abd1300858d42afe683046b8c06ff9c22806e8e37'
seal=read(B/'root.statement-seal89.json');assert seal['expanded_literal_Prop'].encode() in M.read_bytes()
text=M.read_text('utf8');lines=text.splitlines();literal=text[text.index('private def '):text.index('\n\nset_option maxHeartbeats')].rstrip()
header=(PRE/'header89.proposed.lean').read_text('utf8');old=header[header.index('private def '):header.index('\n#check')].rstrip()
assert literal==old
defs=re.findall(r'^    let (\S+)',literal,re.M)
assert defs==['c','Φ','S','rate','Λ','τ','next','record','P','ε','history','waitObs','timeObs','density']
pack=re.findall(r'^        let (\S+)',literal,re.M)
assert pack==['Hist','last','H','μ','D','K','B','X','ν']
audit=[
 {'lines':[115,204],'stage':'Exact target and actual parent extraction','finding':'Proof repeats the literal14model definitions and full9packaging target, then Lean change checks definitional equality to the sealed private statement. Six original analytic assumptions are passed to actual75/73/74/86/87, not replaced by public providers. UnitExp internally makes concrete P a probability measure. No density/regularity/finite-wait/independence premise added.'},
 {'lines':[205,259],'stage':'Joint total observables before integration','finding':'SumProdDistrib is a Borel equivalence, not a continuity assertion for reflection. hw composes actual75 joint tau with fixed parameter, live state and clipped raw real threshold; stopped branch is constant0. ht uses measurable untopD0 and real coercion. hρ combines actual73 joint flow, actual74 joint rate and actual75 joint hazard, exp/ofReal, then Sum case split. hρfin includes every real time and both tags, from ofReal_ne_top/zero_ne_top. Negative times remain harmless total-density values because later D is zero there.'},
 {'lines':[260,306],'stage':'Complete actual history and genuine measurable kernel branch','finding':'H is actual history0..n, Y(w)(k)=w(n+k), mu=map H P. Actual87 supplies both measurable H/Y and exact joint product law. Hist last has value n, so last(H w)=record_n and Y(w)0=w n definitionally. Q/G are measurable before any fiber integration; B is joint-product pullback of Q and X=G after(H,Y). hD is joint Borel via open guard0<s<d(h) and last record evaluation. hK invokes Kernel.withDensity_apply with hD, identifying actual volume.withDensity fibers and excluding the definition zero fallback.'},
 {'lines':[307,358],'stage':'Exact strict finite fiber law','finding':'Every abstract history is split by last tag. Stopped gives empty Q fiber and zero D. Live state uses actual86 at a.2, supplying f measurable and map f(P restrict A_closed)=rho on0<U<=d(h). hset explicitly splits U=top and U=coe s; top cannot satisfy finite upper cutoff, finite s uses exact WithTop/NNReal coercion equivalences. No AE endpoint shortcut. Restrict_map plus restrict_restrict changes A_closed by f^-1 Iio(d), exactly Q fiber. Restrict_withDensity and Iio(d) intersection Ioc(0,d)=Ioo(0,d) produce the density indicator. No equality of closed/open masses, no no-atom premise and no strict mass1-exp claim.'},
 {'lines':[359,366],'stage':'Uniform all-history subprobability and finite kernel','finding':'Rewrite K fiber using hK and hfiber, apply map/univ/restrict identities. Its mass is P(Q_h)<=1 from actual probability P for every h, including unrealizable histories and unbounded finite d across h. Bound1 is a uniform finite bound and constructs IsFiniteKernel. No erroneous bound density<=1.'},
 {'lines':[367,406],'stage':'Joint restricted measure identity and mass','finding':'For arbitrary Borel C in Hist×real, L=G^-1(C) intersect Q is Borel. Map X(P restrict B)(C) equals map(H,Y)P(L) by exact pullback identities. Actual87 product law, Measure.prod_apply and hfiber evaluate every section. withDensity/indicator and Tonelli turn the section expression into nu(C); Measure.ext gives full measure equality, not merely rectangular events or a statewise AE substitution. hnu mass rewrites through the actual restricted probability pushforward, retaining missing infinite-wait mass without normalization.'},
 {'lines':[407,436],'stage':'All nonnegative joint tests and arbitrary Borel history events','finding':'F*D is jointly measurable; sigma-finite real volume gives measurable parameter lintegral. The first-coordinate indicator of A is measurable on Hist×real. Restrict_restrict/indicator exactly encode B intersect H^-1(A), then lintegral_map uses hmap, withDensity and Tonelli give history/time integrals. Final cases h in A and h outside A match indicator pointwise. ENNReal multiplication is commuted explicitly. All operations are nonnegative, so F/integrals may be infinity and null A remains valid without integrability or positive-mass hypotheses.'}
]
for a in audit:
 a['region_LF_sha256']=hashlib.sha256(('\n'.join(lines[a['lines'][0]-1:a['lines'][1]])+'\n').encode()).hexdigest()
result=put('whole-mathematics89.json',{
 'schema':1,'status':'ACCEPTED_INDEPENDENT_WHOLE_BODY_MATHEMATICS_EXPOSITION_NOT_YET_CLOSED',
 'reviewer_id':'/root/exact_verify77','created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'checked_workspace_commit':'7c108c3181cee58bb9305445f903c5f71efda9c5','module':pin(M),'statement_seal':pin(B/'root.statement-seal89.json'),
 'exact_private_Prop_matches_reviewed_header':True,'fourteen_model_lets':defs,'nine_packaging_lets':pack,
 'six_original_source_analytic_binders_retained':True,'no_additional_provider_binders':True,
 'whole_body_audit':audit,
 'all_cases':{'n0':'Actual87 supplies deterministic initial history/fresh tail, hence same fiber calculation. No positive-depth assumption.',
  'already_stopped':'Stopped waitObs0 fails strict lower bound; density0. No next phase at stopped state.',
  'live_wait_top':'Explicitly excluded in hset by finite NNReal upper bound. timeObs0 fallback cannot create an atom under restricted B.',
  'd0':'Ioo(0,0) and actual strict event empty, all finite measures/integrals0.',
  'wait_equal_cutoff':'Excluded on both sides by exact restriction, no closed/strict mass identification.',
  'raw_nonpositive_threshold':'Clipped epsilon0 gives wait0, excluded by positive guard. Actual law still P, never a replacement probability.',
  'rank0_zero_or_flat_hazard':'First-event parent permits infinite wait and zero density mass; no invertibility/strict-rate/positive dimension required.',
  'zero_normal':'Literal reflection is total and inherited from actual recursion; density uses actual rate, not arbitrary bounce law.',
  'null_or_empty_A':'Unnormalized restriction identities valid without division; infinity-valued F integrates to0 on null restricted measure.',
  'all_abstract_histories':'Fiber law requires only last live state or stopped tag, not past consistency or realizability.',
  'unbounded_finite_d':'Pointwise finite NNReal cutoff with measurable dependency; uniform kernel mass1 independent of time size.',
  'all_ENNReal_F':'Arbitrary jointly Borel nonnegative extended F, not separately measurable or signed/integrable claim.',
  'fixed_depth_and_parameters':'No random stopping index, physical-time residual clock, arbitrary correlated random parameter substitution or uniform all-parameters AE event.'},
 'source_boundary':{'primary_first_reconstruction_reused':pin(PRE/'header-math89/primary-source-reconstruction89.json'),
  'distinct_preproof_topology':pin(PRE/'header-math89/source-topology89.decision.json'),
  'graph':pin(PRE/'independent-source-first89/source-proof-graph89.native.json'),
  'coverage':pin(PRE/'independent-source-first89/source-coverage89.native.json'),
  'body_to_source_route':{'S89-D1':'Literal14model definitions and tagged finite history retained','S89-A1':'Joint Borel flow/rate/hazard/clock and density proved from actual parent APIs','S89-A2':'Verified86 internally consumed as hclosed','S87-I3':'Verified87 internally consumed as hjoint','S89-P1':'hQ/hG/hD/hK and nonnegative measurable parameter integration','S89-P2':'hfiber, explicit top/finite guard and Ioc restricted by Iio','S89-T':'hfinite/hmass/hmap/hnumass and all F/A identity','S87-I5-assembly':'FutureOPEN, no iteration/final-factor/count/path claim'},
  'no_new_source_topology_from_BODY':True,'source_author_implicit_elaboration':'One actual deterministic-depth conditional density component of A7, not printed standalone theorem.',
  'no_actual88_false_AND':True,'global_OR_and_future_OPEN_preserved':True},
 'kernel':pin(O/'kernel-dependency89.json'),'fake_closure':pin(O/'fake-closure89.json'),
 'focused_receipt':pin(O/'fresh-focused-build.receipt.json'),'whole_source_receipt':pin(O/'fresh-whole-source-kernel.receipt.json'),
 'required_mathematical_repairs':[],
 'exposition_review':'Await exact author six-step lesson/publication and frozen bindings before final closure.',
 'no_final_source_or_decoder_verdict_read':True,'credit':'Mathematical review only; no VERIFIED/aggregate/PURIFIED/reader/main/whole-paper/Goal.'})
print(json.dumps(result,ensure_ascii=False))
