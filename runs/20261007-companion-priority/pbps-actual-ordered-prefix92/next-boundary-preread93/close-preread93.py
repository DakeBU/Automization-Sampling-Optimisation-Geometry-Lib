from pathlib import Path
import hashlib,json,datetime
ROOT=Path('E:/Samplinglib')
OUT=ROOT/'runs/20261007-companion-priority/pbps-actual-ordered-prefix92/next-boundary-preread93'
def sha(b):return hashlib.sha256(b).hexdigest()
def bind(p):
 p=Path(p);p=p if p.is_absolute() else ROOT/p;b=p.read_bytes()
 return {'path':p.relative_to(ROOT).as_posix(),'raw_sha256':sha(b),'bytes':len(b)}
def write(n,x):
 p=OUT/n;assert not p.exists();p.write_bytes((json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode());return bind(p)
primary=ROOT/'runs/20261007-companion-priority/phase-pbps-gamma-preread57/primary-pbps.exactraw.snapshot.html'
raw=primary.read_bytes();assert sha(raw)=='d81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760'
graphpath=ROOT/'runs/20261007-companion-priority/pbps-ordered-iteration-preread92/primary-first/candidate-source-proof-graph92.v2.native.json'
graph=json.loads(graphpath.read_text())
ids=['S1.p1','S2.SS2.p1','A1.SS1.p1','A1.SS1.p2','A1.E1','A1.E2','A1.Ex19','A1.SS1.SSS0.Px1.p4.1','A1.SS1.SSS0.Px1.p4.2','A1.E7','A1.SS1.SSS0.Px1.p4.3','A1.SS2.p3']
sliceindex=ROOT/'runs/20261007-companion-priority/pbps-actual-ordered-prefix92/independent-source92/primary-source-slices92.native.json'
regionindex=dict(graph['source_regions']);regionindex.update({r['html_id']:r for r in json.loads(sliceindex.read_text())['regions']})
regions={k:regionindex[k] for k in ids}
for r in regions.values():assert sha(raw[r['byte_start']:r['byte_end_exclusive']])==r['raw_sha256']
items=[
 ('ActualConditionalNextWaitSurvival.lean','actual_conditional_next_wait_survival',16,80,87,'Exact live-guarded survival for arbitrary measurable history duration; set-law only. Localize and lift to all nonnegative history tests.'),
 ('ActualPhysicalTimeCover.lean','actual_fixed_reference_physical_time_cover',16,67,71,'AE simultaneous all-finite-time unique covering index and live record; already proves coverage and uniqueness.'),
 ('ActualPhysicalTimeMeasurability.lean','actual_physical_time_measurable_phase',17,78,83,'Exists joint Borel Z; pointwise covered-arc interpolation for arbitrary raw samples; AE common all-times version and time0.'),
 ('ActualOrderedPrefix.lean','actual_ordered_prefix_law',1458,1550,1554,'Complete strict-prefix history law, all ENNReal tests, exact observation/K identity and density on subtype Lebesgue.'),
 ('ActualFiniteJumpRecursion.lean','actual_fixed_reference_finite_jump_recursion',16,107,110,'Initialization, measurable times, monotonicity, stopped absorption and strict finite updates under positive thresholds.'),
 ('ActualNonaccumulation.lean','actual_fixed_reference_event_time_nonaccumulation',15,59,63,'Existing AE all-horizon finite-event bound, consumed through coverage; no repeated nonexplosion work.')]
interfaces=[]
for f,d,a,b,decl,use in items:
 p=ROOT/'AutoSamplingTheory/ExampleCases/ProximalBPS'/f;lines=p.read_bytes().splitlines(keepends=True)
 # The pointer identifies the literal expanded statement; theorem-line recorded separately.
 interfaces.append({'module':bind(p),'declaration':d,'declaration_line':decl,'statement_region':{'start_line':a,'end_line':b,'raw_sha256':sha(b''.join(lines[a-1:b]))},'reuse':use,'proof_reverified':False})
p=ROOT/'AutoSamplingTheory/TechnicalLemmas/Probability/UnitExponentialProduct.lean';lines=p.read_bytes().splitlines(keepends=True)
interfaces.append({'module':bind(p),'declaration':'unit_exponential_product_laws','declaration_line':32,'statement_region':{'start_line':16,'end_line':26,'raw_sha256':sha(b''.join(lines[15:26]))},'reuse':'Probability and one AE event with all clocks strictly positive. Fourth conjunct used for strict count; no need repeat strong law.','proof_reverified':False})
freeze=write('primary-first-chronology93.native.json',{'record_kind':'bounded-primary-first-next-boundary-preread','reviewer':'/root/primary_source91','utc_closed':datetime.datetime.now(datetime.timezone.utc).isoformat(),'primary':bind(primary),'expectation':bind(OUT/'primary-first-expectation93.md'),'chronology':['Re-read pinned A1.E1/E2/E7, A1.SS1.p1/p2/p4.1-p4.3 and A1.SS2 before current interfaces.','Wrote primary-first-expectation93.md before searching and opening current88/79/80.','Read exact current expanded88/79/80 then92; retrieved76/78/UnitExponentialProduct only to resolve positivity/strictness and count dependencies.','Checked existing source graph SURV/END/PATH/COUNT/ALG/TERM/A7, preserving topology and open-status distinctions.','Wrote one candidate integration recommendation; no Lean search, compilation, proof credit or state mutation.'],'correction_after_interface_read':'The primary-only expectation conservatively queried coverage uniqueness and simultaneous-time validity; current79/80 already provide these. They are not new blockers.','source_regions':regions,'prior_verdict_used_as_authority':False})
report=write('recommendation93.native.json',{'record_kind':'source-derived-next-unit-candidate-not-sealed','status':'PLANNING_ONLY_NOT_PROVED_OR_CLAIMED','reviewer':'/root/primary_source91','primary_first':freeze,'recommendation':bind(OUT/'recommendation93.md'),'source_graph':bind(graphpath),'source_anchor_regions':regions,'exact_reuse_interfaces':interfaces,
 'answer':'Yes: one coherent next integration unit can prove terminally survived finite-count complete-history/path law using92+88+79+80. No missing external analytic/source assumption prevents it. The endpoint and measurable count/path adapters are real remaining mathematics to prove inside the unit.',
 'candidate_formula':'For each fixed finite T>=0, n>=0 and measurable F:Hist_n x Path_T -> ENNReal, integral_{N_T=n} F(H_n,Z_T) dP = integral_{Delta_n(T)} F(K_n(t),Gamma_n,T(t)) q_n(t)*ofReal(exp(-Lambda(z_n,T-t_n))) dm_n,T(t).',
 'candidate_assumptions':['V globally C2','alpha>0','alpha<=beta','global lower and upper Hessian quadratic bounds','eta>0','eta<=1/beta (beta eta<=1 equivalent)'],
 'carrier_completion':'Finite-dimensional real Hilbert E including rank0; canonical stopped Sum and Exp(1) product; Path_T=([0,T]->Phase) with coordinate-generated product sigma-algebra; ENNReal tests. All explicit ASTIS completions/extensions.',
 'internal_obligations':[
 {'id':'SURV93','statement':'Use measurable d_T=T-lastTime and88 set-law to get a restricted weighted history law; compose with92 to insert terminal survival.','public_premise':False},
 {'id':'END93','statement':'For each fixed T, P(exists j>=1:T_j=T)=0. Positive clocks excludeT0; forT>0 use92 atT+1 and the last-coordinate singleton hyperplane.','public_premise':False},
 {'id':'COUNT93','statement':'Measurable unique-interval selector with0 fallback; use79, positivity/76 and END93 for AE equality with each strict-survival C_n and finite strict/non-strict counts.','public_premise':False},
 {'id':'PATH93','statement':'Measurable finite right-continuous interpolation Gamma into product path carrier;92 identification and80 pointwise arc law give path equality on every raw C_n.','public_premise':False}],
 'proof_route_AND':['88 measurable history-dependent survival localization','92 complete-history all-test law','finite measurable interpolation +80 pointwise covered-arc realization','positive clocks+76 strict finite times','92 hyperplane-null endpoint adapter','79 count selector/partition and finite count identification','joint history/path test pushforward'],
 'endpoint_quantifiers':'forall fixed finiteT, AE samples, forall finitej>=1 no event atT; never AE samples, forallT no event atT. Time0 initialization excluded from event index.',
 'zero_cases':'n0,T0 singleton integral and mass1 a.e.; n>0,T0 empty simplex/zero integral. Raw zero clocks are allowed by total recursion and preclude pointwise count gloss. C_n uses strict next-wait survival including infinity.',
 'actual_Z_binding':'Internally choose the existing theorem80 witness or restate an existential with strengthened properties; no external Z-law/regularity premise.',
 'source_graph_delta_candidate':{'joins':['PREFIX92','SURV92','END92','COUNT92','PATH92'],'not_claimed_closed':['ALG92','TERM92 in printed full-hazard form','A7'],'topology_mutated':False},
 'remaining_boundary':['Sum completed and terminal hazards into full path integral and identify pre-jump rates.','Countable functional assembly and bounded signed-test integrability/absolute convergence.','If using a cadlag/Skorokhod Borel path carrier instead, prove regularity and measurable-space compatibility;88/79/80 do not already supply it.','No restart, invariance, reversibility, mixing, cost or whole-paper claim.'],
 'canonical_state_changed':False,'production_changed':False,'new_ledger_created':False,'proof_credit':False})
inputs=[bind(primary),bind(graphpath),bind(sliceindex)]+[i['module'] for i in interfaces]
outputs=[bind(OUT/'primary-first-expectation93.md'),freeze,bind(OUT/'recommendation93.md'),report,bind(OUT/'close-preread93.py')]
manifest=write('closed-RAW93.native.json',{'record_kind':'closed-bounded-next-boundary-preread','inputs':inputs,'outputs':outputs,'scope':'Source-first recommendation only; exact interface inspection without proof re-verification. All prior92 artifacts unchanged; only this new directory written. Manifest excludes its own hash.'})
for i in inputs+outputs:assert bind(i['path'])==i
print(json.dumps({'report':report,'chronology':freeze,'manifest':manifest},indent=2))
