from pathlib import Path
import copy, datetime, hashlib, json

root=Path('E:/Samplinglib')
lane=root/'runs/20261007-companion-priority/pbps-ordered-iteration-preread92'
out=lane/'primary-first';reviews=lane/'independent-target-review'
def sha(b):return hashlib.sha256(b).hexdigest()
def info(p):return {'path':str(p).replace('\\','/'),'raw_sha256':sha(p.read_bytes()),'bytes':p.stat().st_size}
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def write(name,o):
    with (out/name).open('x',encoding='utf-8',newline='\n') as f:
        json.dump(o,f,ensure_ascii=False,indent=2);f.write('\n')
expected={
'recommendation92.md':'65be1648d45ed8316fe0bf06179693584c4c18ad33b550dd8416018997ed376e',
'recommendation92.native.json':'f613531e8b5f6fc3c02d6d151716ccab8225552f5d2898a9599add9ee0f41fce',
'closed-RAW92.native.json':'4ce38186002a058cb77d88206931fe2adbb5bfd78bc2de90ec1805359302a713',
'candidate-source-proof-graph92.native.json':'cca8cb916815783b6e1bc52664d989f8f7b2f5715c42f9ebbf2bcb8c383955bf',
'candidate-source-coverage92.native.json':'bcbf841e0f99614ce315553984dddb9c9c7fef0f035de21b6ea981dc0edd6aca',
'candidate-graph-closed-RAW92.native.json':'9f053b5d6edb12684317027b98f8a4b44194032757e4f7865a5c16bded587df8'}
for name,h in expected.items():assert sha((out/name).read_bytes())==h
review_hashes={'target-review92.native.json':'036cceb4c8fb1fdce88818c1d070b6bc3276043258adc1f7605f4348f3fb3952','candidate-topology-review92.native.json':'f614eed71a611e0661280d5e4677dbb69db550fada6765db685571d5977bd57c','closed-RAW92.native.json':'5871230f0627f066bfae5b94c799a8f8851335dd311b04b163c85c497b26f4fb'}
for name,h in review_hashes.items():assert sha((reviews/name).read_bytes())==h
primary=root/'runs/20261007-companion-priority/phase-pbps-gamma-preread57/primary-pbps.exactraw.snapshot.html'
raw=primary.read_bytes();assert sha(raw)=='d81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760'

oldmd=(out/'recommendation92.md').read_text(encoding='utf-8')
statement=r'''Let d be a finite dimension, V in C^2(R^d), 0<alpha<=beta, and assume

    alpha |v|^2 <= D^2 V(x)[v,v] <= beta |v|^2   for every x,v in R^d.
    0 < eta <= 1/beta.

These are the original six standing analytic conditions from (1.1) and Section 2.2. Write Phase=R^d x R^d with its Borel structure. Fix arbitrary y,r in R^d and z0=(x0,p0) in Phase. Define the actual source objects by

    c = y - eta grad V(r),       h(x) = grad V(x)-grad V(r),
    lambda(x,p) = sqrt(eta) max(<p,h(x)>,0),
    Phi_s(x,p) = (c+(x-c)cos(s)+sqrt(eta)p sin(s),
                  -(x-c)sin(s)/sqrt(eta)+p cos(s)),
    R_v p = p - (2<p,v>/|v|^2) v  if v != 0,    R_0 p = p,
    B(x,p) = (x,R_(h(x)) p),
    L_z(u) = integral_0^u lambda(Phi_s(z)) ds  for u>=0,
    tau_z(e) = inf{u>=0 : L_z(u)>=e} in [0,infinity],  e>=0,

where an empty crossing set has infimum infinity. The closed threshold convention includes equality and tau_z(0)=0. The bounce need only be Borel, not continuous; the zero-normal convention is literal and lambda(x,p)=0 whenever h(x)=0.

Use the canonical actual clock space and law, defined rather than supplied as theorem hypotheses:

    Omega = R^N,    P = infinitePi_(k in N) Exp(1),
    epsilon_k(w) = max(w_k,0) in NNReal.

The product carries its product Borel sigma algebra. Index k starts at zero; epsilon_k represents the source clock E_(k+1). Clipping extends the definition to raw negative inputs. The product law makes every coordinate strictly positive almost surely; this is a consequence of P, not an extra public good-input assumption.

Set Rec=(NNReal x Phase) sum Unit, with Borel product and disjoint-sum structures, writing live(a,z) and stopped for its tags. The actual total finite recursion is literal:

    R_0(w) = live(0,z0),
    R_(k+1)(w) = stopped                              if R_k(w)=stopped,
    R_(k+1)(w) = stopped                              if R_k(w)=live(a,z)
                                                        and tau_z(epsilon_k(w))=infinity,
    R_(k+1)(w) = live(a+v, B(Phi_v(z)))               if R_k(w)=live(a,z)
                                                        and tau_z(epsilon_k(w))=v<infinity.

Thus the absorbing stopped tag totalizes the source's terminated recursion. It never denotes a finite event or a phase point at infinite time. On live records the first component is the actual cumulative time from (A.2). Define Hist_n=Fin(n+1)->Rec with its product Borel structure and H_n(w)_j=R_j(w), for j=0,...,n. Tests below range over all ambient histories, including unrealizable tagged tuples; equality of laws is restricted to the literal strict-prefix event.

Let n>=0 and T>=0 be deterministic, with T finite. Use the Borel simplex subtype

    Delta_n(T) = {t in R^n : 0<t1<...<tn<T}.

Delta_0(T) is the singleton empty tuple for every T>=0, carrying mass one. Its measure m_(n,T) is the restriction of n-fold real Lebesgue measure to the simplex, regarded on that subtype. At n=0 use the mass-one empty product measure. No value of the prescribed history or weight outside this subtype is needed or silently invented.

For t in Delta_n(T), put t0=0, z_0^t=z0 and recursively

    delta_j = t_j-t_(j-1),
    z_j^- = Phi_(delta_j)(z_(j-1)^t),
    z_j^t = B(z_j^-),                         j=1,...,n.

Define K_n(t) in Hist_n by K_n(t)_0=live(0,z0) and K_n(t)_j=live(t_j,z_j^t) for j=1,...,n. Here t_j is regarded as NNReal using its positivity on the subtype. Define E_n(T) literally as the event that the first n actual records R_1,...,R_n are live and their stored cumulative times satisfy 0<T1<...<Tn<T; E_0(T)=Omega. This is the **strict first-n prefix event**. It places no condition on R_(n+1) or T_(n+1). A count interpretation as at least n interior events is valid only almost surely on the positive-clock event; it is not asserted pointwise on raw zero-clock inputs and is not needed for the prefix theorem. In particular this is not an exactly-n-at-horizon event.

Define the finite nonnegative real weight and its extended-nonnegative embedding:

    qReal_n(t) = product_(j=1)^n [lambda(z_j^-) exp(-L_(z_(j-1)^t)(delta_j))],
    q_n(t) = ENNReal.ofReal(qReal_n(t)),
    qReal_0(empty) = 1,       q_0(empty) = 1.

Then E_n(T) and H_n are Borel measurable. For every fixed V,eta,n,T satisfying the preceding conditions, the maps (y,r,z0,t)->K_n(t) and (y,r,z0,t)->q_n(t) are jointly Borel on R^d x R^d x Phase x Delta_n(T). This does not assert regularity in V or eta or a new joint parameter-integral identity.

For every fixed y,r,z0 and every Borel F:Hist_n->[0,infinity], with possibly infinite values,

    integral_(E_n(T)) F(H_n(w)) P(dw)
      = integral_(Delta_n(T)) F(K_n(t)) q_n(t) m_(n,T)(dt).

Equivalently, the pushforward of P restricted to E_n(T) under H_n equals the pushforward of the measure q_n*m_(n,T) under K_n. In particular integral q_n = P(E_n(T))<=1. Multiplication and integration use ENNReal conventions, including 0*infinity=0. Restrictions are unnormalized; P(E_n(T)) may be zero. The identity covers n=0, T=0, zero hazard, stopped histories, and an infinite next wait. F can inspect all recorded times and poststates, not only the terminal position. Measurability, the density law, positive-clock support and finite-prefix bookkeeping are conclusions/dependencies, not new source hypotheses.

A coordinate-free finite-dimensional real inner-product version remains possible as an explicitly identified extension. It must preserve all six original analytic conditions and the same literal input and tagged-history construction. No exact Lean header is sealed by this recommendation.
'''
start=oldmd.index('### Exact mathematical statement\n\n')+len('### Exact mathematical statement\n\n')
end=oldmd.index('\n## Primary anchors',start)
md=oldmd[:start]+statement+oldmd[end:]
md=md.replace('# Source-first recommendation: actual finite ordered-prefix law','# Source-first recommendation v2: actual finite ordered-prefix law',1)
md=md.replace('This is a bounded mathematical preread, not an SAU claim, theorem seal, proof, or canonical status change.','This v2 successor responds to the independently reviewed local candidate corrections; it remains a bounded mathematical preread, not an accepted topology, SAU claim, theorem seal, proof, or canonical status change. All v1 artifacts remain immutable.',1)
md=md.replace('Preserve the at-least-n event interpretation and the absent final survival factor.','Preserve the literal strict first-n prefix event and the absent final survival factor. Any at-least-n interior-count interpretation is only almost sure on the positive-clock event, not pointwise on totalized inputs.')
md=md.replace('It converts the first-n-event law to an exactly-n-event-at-horizon law, with the chosen strict/non-strict endpoint convention justified.','After the relevant count/good-clock and endpoint identifications, it supplies the exactly-n-event-at-horizon term from the strict-prefix law. Those identifications must be proved or reused; they are not pointwise consequences on every totalized raw clock sequence.')
md=md.replace('This source route needs only the actual one-step complete-history finite-event law, prescribed-history identification, Borel parameter integration, finite product-coordinate bookkeeping and induction.','This source route needs only the actual one-step complete-history finite-event law, prescribed-history identification, Borel parameter integration, finite product-coordinate bookkeeping and induction. The measurability node explicitly depends on the defined actual clock/record recurrence, not only on smoothness and flow formulas.')
md+='''\n## Exact v2 source-coverage corrections\n\nThe source residual bound |grad V(x)-grad V(r)|<=beta|x-r| is assigned to the existing source energy/rate-cap ingredient. The full conditional-force recombination in Section 3.2 is explicitly excluded from the prefix dependency graph as generator/background explanation. Bounce involution in A.1 is explicitly excluded as downstream reflection/reversal algebra, while rate zero at a zero residual normal is recorded as a literal-rate consequence in O92. Reflection still requires only Borel measurability. These are distinct source dispositions, not new theorem assumptions or proof claims.\n\nThe independent target reviewer gave a null-input counterexample to the old unqualified count gloss: for V(x)=x^2/2, alpha=beta=eta=1, y=r=0, z0=(1,1), T=pi/2 and clocks e1=0,e2=1/4, the first jump time is 0 and the second is 5pi/12 in (0,T). Thus E_1(T) is false despite an interior event. The canonical exponential law assigns these zero-clock inputs probability zero. The density identity was not refuted; v2 restricts the count gloss to its correct almost-sure scope.\n\nDistinct reviewer recheck is required for this successor. No acceptance follows from its creator applying these corrections.\n'''
with (out/'recommendation92.v2.md').open('x',encoding='utf-8',newline='\n') as f:f.write(md)

precisions=[
{'id':'P92-1','action':'Define Omega=R^N, literal infinitePi Exp(1), clipped epsilon and actual stopped recursion rather than abstract probability/providers.'},
{'id':'P92-2/R92-COUNT','action':'Use literal strict first-n prefix everywhere; any at-least-n count gloss is AE on positive-clock inputs, not pointwise.'},
{'id':'P92-3','action':'Expand reflection including zero normal, Rec Sum and Hist Fin product Borel carriers, simplex subtype, and q=ofReal finite product.'},
{'id':'P92-4','action':'Quantify joint Borel K,q in y,r,z0,t for each fixed V,eta,n,T; no hidden regularity in V/eta or parameter-integral output.'},
{'id':'R92-REC-MEAS','action':'Add I92->M92 exact actual-recursion definition/proof-ingredient edge.'},
{'id':'R92-RESIDUAL-COVERAGE','action':'Add separate source rows for residual Lipschitz estimate and excluded full-force recombination.'},
{'id':'R92-BOUNCE-COVERAGE','action':'Add separate rows for excluded bounce involution and O92 zero-normal-zero-rate definition consequence.'}]

r=read(out/'recommendation92.native.json')
r.update({'version':2,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'V2_CANDIDATE_FOR_DISTINCT_RECHECK_NOT_ACCEPTED_NOT_SEALED','predecessor':info(out/'recommendation92.native.json'),'independent_feedback':[info(reviews/'target-review92.native.json'),info(reviews/'candidate-topology-review92.native.json')],'applied_precisions':precisions,'statement':statement,'statement_text_sha256':sha(statement.encode()),'input_construction':'Literal Omega=R^N, P=infinitePi Exp(1), epsilon_k=max(w_k,0); Rec=(NNReal x Phase) sum Unit; actual stopped recursion and Hist_n=Fin(n+1)->Rec. No arbitrary probability/independence/density provider.','target_event':'Literal strict first-n prefix: first n records live and 0<T1<...<Tn<T; E0=Omega. Count gloss only AE on the positive-clock event; no condition on next record.','target_density':'qReal_n is the finite nonnegative product of pre-bounce rate times segment survival; q_n=ENNReal.ofReal(qReal_n), q0=1 on the singleton simplex.','target_identity':'For every Borel F:Hist_n->ENNReal, integral_E_n F(H_n)dP = integral_Delta_n(T) F(K_n(t)) q_n(t) dm_(n,T). K,q jointly Borel in y,r,z0,t for fixed V,eta,n,T; no V/eta or parameter-integral regularity claimed.','recommendation_document':info(out/'recommendation92.v2.md'),'distinct_recheck_required':True})
write('recommendation92.v2.native.json',r)

g=read(out/'candidate-source-proof-graph92.native.json')
g.update({'version':2,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'V2_CANDIDATE_FOR_DISTINCT_RECHECK_NOT_ACCEPTED_NOT_SEALED_NOT_PROVED','predecessor':info(out/'candidate-source-proof-graph92.native.json'),'recommendation':info(out/'recommendation92.v2.native.json'),'revision_feedback':[info(reviews/'target-review92.native.json'),info(reviews/'candidate-topology-review92.native.json')],'applied_precisions':precisions})
byid={x['id']:x for x in g['nodes']}
byid['I92']['claim']='Literal Omega=R^N, P=infinitePi Exp(1), epsilon_k=max(w_k,0); source E_(k+1) is coordinate k. Actual A1 closed threshold infimum; A2 cumulative time plus finite wait and reflected flowed poststate; empty hit gives stopped.'
byid['T92']['claim']='Rec=(NNReal x Phase) sum Unit with Borel sum/product structure; Hist_n=Fin(n+1)->Rec. Literal initial live(0,z0), finite next live(a+v,B(Phi_v z)), infinite-wait next stopped, and absorbing stopped tag define complete finite histories.'
byid['T92']['boundary']='Stopped is not a finite event or a phase point at infinity. No arbitrary time-zero reader is needed for E_n; all its stored-time comparisons are guarded by live tags.'
byid['E92']['claim']='E_n(T): first n actual records live with stored times 0<T1<...<Tn<T; E0=Omega. This literal strict first-n prefix has an at-least-n-interior-count interpretation only AE on the positive-clock event, never on every totalized input.'
byid['K92']['claim']='On the Borel simplex subtype, construct all live prescribed records by z_j^-=Phi_(t_j-t_(j-1))z_(j-1), z_j=B(z_j^-). For each fixed V,eta,n,T, prove jointly Borel (y,r,z0,t)->K_n; no off-simplex extension or regularity in V/eta is asserted.'
byid['Q92']['claim']='qReal_n=product_j lambda(z_j^-)exp(-L_(z_(j-1))(t_j-t_(j-1))); q_n=ENNReal.ofReal(qReal_n), q0=1. Jointly Borel in y,r,z0,t on the simplex for fixed V,eta,n,T.'
byid['O92']['claim']='Fixed y,r,z0; center y-eta gradV(r), residual gradient, harmonic Phi, rate sqrt(eta)[p dot h]+; R_v p=p-(2<p,v>/norm(v)^2)v for v!=0 and R0 p=p. Zero residual normal entails zero rate; bounce need only be Borel.'
byid['ENERGY92']['claim']='Harmonic flow and reflection preserve shifted harmonic energy. Source residual estimate norm(gradV(x)-gradV(r))<=beta norm(x-r), then Cauchy-Schwarz and energy bounds, control rate along each actual or prescribed fixed-initial trajectory.'
for e in g['edges']:
    if (e['from'],e['to'])==('SURV92','TERM92'):e['consumer_use']='Add missing final no-event factor to the strict first-n prefix; the exactly-n count interpretation additionally uses the good-clock/count and endpoint identifications, not a pointwise raw-input gloss.'
g['edges'].append({'from':'I92','to':'M92','consumer_use':'The defined actual threshold/clock/record recursion is the object whose joint Borel measurability is proved; finite composition uses this exact recurrence.','relation':'source-proof-ingredient-not-Lean-edge'})
g['structural_checks']['edge_count']=len(g['edges'])
g['source_vs_ASTIS']['printed_claim_dispositions_v2']={'residual_lipschitz':'NODE ENERGY92, source smoothness consequence','full_force_recombination':'EXCLUDED from prefix graph: generator/background explanation','bounce_involution':'EXCLUDED from prefix graph: downstream algebra/reversal','zero_normal_zero_rate':'NODE O92, literal rate consequence'}
g['count_gloss_boundary']='Strict E_n definition is pointwise; count interpretation is only AE on positive-clock inputs and is not a new good-input theorem binder.'
write('candidate-source-proof-graph92.v2.native.json',g)

c=read(out/'candidate-source-coverage92.native.json')
c.update({'version':2,'status':'V2_CANDIDATE_FOR_DISTINCT_RECHECK_NOT_ACCEPTED','predecessor':info(out/'candidate-source-coverage92.native.json'),'graph':info(out/'candidate-source-proof-graph92.v2.native.json'),'applied_precisions':precisions})
bycid={x['id']:x for x in c['coverage']}
bycid['C92-25']['reason']='Separate composition after strict-prefix law. q_n omits terminal survival; it is not an exactly-n law. An at-least-n interior-count gloss holds only AE on the positive-clock event, not pointwise for zero-clock totalizations.'
bycid['C92-37']['reason']='M92 now has explicit I92->M92 dependency: measurability is about the defined actual threshold/record recursion, as well as the rate and flow.'
new_rows=[
('C92-43','S3.SS2.p4','The beta-Lipschitz residual estimate norm(gradV(x)-gradV(r))<=beta norm(x-r).','NODE',['ENERGY92'],'Explicit source ingredient of the energy-shell rate bound; not an additional public prefix assumption.'),
('C92-44','S3.SS2.p4','The harmonic and residual force terms recombine to the full conditional force sqrt(eta) grad V_y(x).','EXCLUDED',[],'Generator/background explanation for the chosen dynamics; the prefix-law recurrence is already defined literally and does not need this recombination theorem as a parent.'),
('C92-45','A1.SS1.p1','The source bounce map is an involution.','EXCLUDED',[],'Downstream reflection/reversal algebra; finite-prefix density and Borel forward append do not need the inverse/involution as a premise.'),
('C92-46','A1.SS1.p1','At zero residual normal h_r(x)=0 the source event rate vanishes.','NODE',['O92'],'Immediate consequence of the literal rate and the zero-normal convention. It creates no continuity assumption on the Borel reflection.')]
for id,region,desc,disposition,nodes,reason in new_rows:
    c['coverage'].append({'id':id,'source_region':copy.deepcopy(c['source_regions'][region]),'source_content':desc,'disposition':disposition,'nodes':nodes,'reason':reason})
c['coverage_count']=len(c['coverage'])
c['prior_native_files_unchanged']=expected
c['review_requirements']='Distinct reviewer must recheck v2 corrections and candidate topology before acceptance. The creator does not declare topology or Statement Seal accepted.'
write('candidate-source-coverage92.v2.native.json',c)

nodes={x['id'] for x in g['nodes']}
assert len(nodes)==len(g['nodes'])
assert all(e['from'] in nodes and e['to'] in nodes for e in g['edges'])
assert all(n in nodes for row in c['coverage'] for n in row['nodes'])
for s in g['source_regions'].values():assert sha(raw[s['byte_start']:s['byte_end_exclusive']])==s['raw_sha256']
for name,h in expected.items():assert sha((out/name).read_bytes())==h
assert len(g['nodes'])==29 and len(g['edges'])==57 and len(c['coverage'])==46
outputs=['recommendation92.v2.md','recommendation92.v2.native.json','candidate-source-proof-graph92.v2.native.json','candidate-source-coverage92.v2.native.json','build-candidate-source-v2-92.py']
inputs=[primary]+[out/n for n in expected]+[reviews/n for n in review_hashes]
manifest={'schema_version':1,'version':2,'record_kind':'RAW','closed':True,'author':'/root/primary_source91','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'V2_SUCCESSOR_FOR_DISTINCT_RECHECK_NOT_ACCEPTED','inputs':[info(p) for p in inputs],'outputs':[info(out/n) for n in outputs],'exact_corrections':precisions,'checks':{'all_original_hashes_preserved':True,'all_primary_spans_rehashed':True,'graph_nodes':29,'graph_edges':57,'coverage_dispositions':46,'new_analytic_binders':False,'production_Lean_read':False,'canonical_state_write':False,'source_or_91_mutation':False},'closure':'Only separately named v2 successors and this script created. Originals and independent reviews remain immutable. Manifest excludes its own bytes. No creator acceptance of topology, Statement Seal or theorem.'}
write('candidate-v2-closed-RAW92.native.json',manifest)
for name in outputs[:-1]+['candidate-v2-closed-RAW92.native.json']:print(name,sha((out/name).read_bytes()))
