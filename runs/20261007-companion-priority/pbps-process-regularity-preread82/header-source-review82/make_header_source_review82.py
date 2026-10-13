"""Source-only82 exact prospective header scope audit; no implementation input."""
import json,hashlib,pathlib
from datetime import datetime,timezone
ROOT=pathlib.Path('E:/Samplinglib')
PRE=ROOT/'runs/20261007-companion-priority/pbps-process-regularity-preread82'
OWN=PRE/'header-source-review82'
HEADER=ROOT/'runs/20261007-companion-priority/pbps-actual-small-time-continuity82/header82.proposed.lean'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):return json.loads(p.read_text('utf8'))
def raw(p):return {'path':p.as_posix(),'raw_sha256':sha(p),'bytes':p.stat().st_size}
def write(n,d):
 p=OWN/n;assert not p.exists();p.write_bytes((json.dumps(d,ensure_ascii=False,indent=2)+'\n').encode('utf8'));return p
manifest=load(PRE/'source_freeze82.raw-manifest.json')
assert sha(PRE/'source_freeze82.raw-manifest.json')=='45253a0383bebeffe048730edfd738b4578f281d1a6b764e95abb2388253d3c1'
for x in manifest['raw_inputs']+manifest['raw_outputs']:assert sha(pathlib.Path(x['path']))==x['raw_sha256']
inv=load(PRE/'source_inventory82.json');graph=load(PRE/'source_proof_graph82.json')
assert (len(inv['items']),len(graph['nodes']),len(graph['edges']))==(36,13,20)
assert sha(HEADER)=='0333cf3e488effe1fa6f516553bb1e63a3bb650bfe09aca234ed20375cf85e64'
header=HEADER.read_text('utf8')
assert 'private def actual_small_time_stochastic_continuity_statement' in header
assert not any(line.lstrip().startswith(('theorem ', 'lemma ')) for line in header.splitlines())
for fragment in ['(hα : 0 < (α : ℝ))','(hαβ : α ≤ β)','(hV : ContDiff ℝ 2 V)',
 '(hη : 0 < η)','(hβη : (β : ℝ) * η ≤ 1)','(hH : ∀ x v : E,','P.real {sample : ℕ → ℝ |',
 '1 - Real.exp (-Λ y xRef z₀ t)','(𝓝 0) (𝓝 0)']:assert fragment in header,fragment
now=datetime.now(timezone.utc).isoformat()
slots={
 'objects':{'relation':'explicit-elaboration','original':'Actual harmonic Phi, residual reflection/rate, integrated hazard threshold, initialized stopped recurrence and actual physical phase; source Ex22 first-event probability.',
  'candidate':'Literal source maps and P/epsilon/next/record/eventTime internally defined. One Z retains actual80-style clauses; new actual phase-flow defect event and norm-tail.',
  'assessment':'Faithful actual construction; no abstract process/law/cap certificate premise. Defect event need not equal first-event event: trivial bounce or later return can leave phases equal, so upper bound is the correct adapter.'},
 'domains':{'relation':'explicit-elaboration','original':'Euclidean finite-dimensional phase, finite t>=0 and top wait for empty hit; stochastic smalltime right limit.',
  'candidate':'FiniteDimensional real inner product Borel E (rank0 allowed), phase E×E, NNReal finite times, WithTop NNReal waits, countable real Exp input and measurable clamp.',
  'assessment':'Finite time distinct from infinite wait and stopped dummy. Intrinsic/rank0 coding is harmless; no added positive dimension or bounce continuity.'},
 'quantifiers':{'relation':'explicit-elaboration','original':'For each fixed y,r,z0 the actual process is constructed from iid Exp clocks; source flow/firstevent smalltime argument is pointwise fixed initial phase.',
  'candidate':'Exists one joint Borel Z; deterministic allraw covered/fallback clauses; for each fixed y,r,z0 clock-AE common allfinite/init. For each fixed y,r,z0 allfinite t measurable defect bound and every real delta>0 measurable tail with limit0.',
  'assessment':'Correct fixedparams semantics, no uniform probability limit/nullset or arbitrary correlated random parameter substitution. Includes t=0 by retained AE initialization.'},
 'assumptions':{'relation':'equivalent','original':'C2 potential, 0<alpha<=beta, full Hessian sandwich and eta in(0,1/beta].',
  'candidate':'Exact six hα,hαβ,hV,hH,hη,hβη binders; normed real finite-dimensional Borel carrier.',
  'assessment':'No integrability, energy cap, phase provider, normalizer, kernel, invariance or Markov premise added. Some original analytic assumptions are unused by the local estimate but remain source standing context.'},
 'conclusion':{'relation':'explicit-elaboration','original':'Ex22 firstevent probability 1-exp(-Lambda_t)->0 is one explicit ingredient in source strong continuity proof; actual interpolation identifies no-event path with flow.',
  'candidate':'P.real{Z_t!=Phi_t z0}<=1-exp(-Lambda_t) plus fixedparam stochastic continuity at0 for each positive norm threshold; measurable events explicit.',
  'assessment':'Honest bounded source prerequisite and actual-input integration; full Ex22 firstwait equality is a required proof ingredient, not an asserted new conclusion. No full L2 result claimed.'},
 'scopes':{'relation':'explicit-elaboration','original':'Source p6.1–p6.2 uses invariance/Jensen, pointwise smalltime convergence, dominated convergence, Cc density and contractivity for full L2 continuity.',
  'candidate':'Only actual first-event defect control and zero-time stochastic continuity, with all prior Z properties retained.',
  'assessment':'Full Markov/restart/semigroup/invariance/L2/adjoint, alltime path cadlag/rightcontinuity, bounded-test expectation theorem and implemented cost/composition/main results remain OPEN.'},
 'constant_dependencies':{'relation':'equivalent','original':'sqrt eta and inverse sqrt eta flow scales; sqrt eta rate; center y-eta gradV(r); Exp rate1; source time approaching0.',
  'candidate':'Literal signs/scales and source threshold coordinate n=E_(n+1); RHS exact1-exp(-Lambda_t); no extra constant or terminal pi law.',
  'assessment':'Correct source scales; optional cap Ct omitted without changing the selected smalltime scope.'}}
deltas=[
 {'id':'H82-D01','slot':'domains','classification':'notation-resolution','blocking':False,'description':'Intrinsic finite-dimensional E and canonical Exp real sequence/NNReal clamp code Euclidean source; rank0 allowed, source E1 is coordinate0.'},
 {'id':'H82-D02','slot':'conclusion','classification':'source-implicit','blocking':False,'description':'Source firstevent probability becomes actual phase-flow disagreement upper bound via deterministic first halfopen interval. Not an equality with probability of nontrivial phase motion.'},
 {'id':'H82-D03','slot':'quantifiers','classification':'quantifier-clarification','blocking':False,'description':'NNReal nonpunctured nhds0 extends source right limit using P-real norm-tail at0=0 for delta>0, which follows retained AE Z0=z0. It does not assert raw-sample initialization for exceptional zero thresholds.'},
 {'id':'H82-D04','slot':'scopes','classification':'admissible-bounded-refinement','blocking':False,'description':'G82-09 optional quantitative <=C(z0)t omitted; exact exponential bound and limit remain. No division by zero cap needed.'},
 {'id':'H82-D05','slot':'scopes','classification':'strict-source-boundary','blocking':False,'description':'G82-11 bounded continuous expectation, G82-12 fullL2 semigroup and G82-13 global/path/restart package excluded. Existing H81 probability-kernel existence is neither duplicated nor used to infer Markovness.'},
 {'id':'H82-D06','slot':'objects','classification':'formalization-convention','blocking':False,'description':'Source failed-limit zero versus actual80 uncovered z0 fallback remains explicit; firstwait infinity retains first live arc and no source phase comes from stopped Sum dummy.'}
]
node_coverage=[]
for n in graph['nodes']:
 i=int(n['id'][-2:])
 status='PROSPECTIVE_BODY_INGREDIENT_NOT_PROVED' if i<=7 else 'PROSPECTIVE_NEW_HEADER_CONCLUSION_NOT_PROVED' if i in [8,10] else 'PROSPECTIVE_LIMIT_INGREDIENT_OPTIONAL_CAP_EXCLUDED' if i==9 else 'EXCLUDED_OPEN'
 node_coverage.append({'id':n['id'],'frozen_obligation':n['obligation'],'status':status,
  'mapping':'Retained literal actual definitions and Z contracts'if i<=7 else 'Measurable actual defect bound final conjunction'if i==8 else 'Lambda0/continuity needed for exponential limit; optional Ct absent'if i==9 else 'Positive real delta norm-tail measurability/Tendsto on NNReal nhds0'if i==10 else 'Not claimed in header; remains separate source consumer/alternative',
  'blocking':False})
edges=[]
for e in graph['edges']:
 b=int(e['consumer'][-2:])
 edges.append({'id':e['id'],'ingredient':e['ingredient'],'consumer':e['consumer'],'reason':e['reason'],
  'status':'EXCLUDED_OPEN_FUTURE_SUBSTRATE_NOT_IMPLICATION'if b>=11 else 'PRESERVED_PROSPECTIVE_BODY_INGREDIENT_NOT_PROVED',
  'refinement':'Optional cap edge not needed: Lambda continuity suffices'if e['ingredient']=='G82-01'and b==9 else None})
items=[{'id':i['id'],'source_id':i['source_id'],'frozen_scope':i['scope'],'source_graph_nodes':i['source_graph_nodes'],
 'header_scope_status':'EXCLUDED_OPEN_OR_CONTEXT'if i['scope'].startswith(('EXCLUDED','CONSUMER'))else'PROVENANCE'if i['scope']=='PROVENANCE'else'SOURCE_CONDITION_INGREDIENT_OR_BOUNDARY_PRESERVED',
 'finding':i['paraphrase'],'blocking':False}for i in inv['items']]
result=write('header-source-review82.result.json',{
 'schema':'independent-prospective-header-source-scope-review-v1','created_utc':now,'reviewer':'/root/fresh_source78',
 'verdict':'source-compatible-with-explicit-bounded-refinement','header':raw(HEADER),
 'verdict_reason':'Header honestly states an actual firstevent/flow-coupling probability prerequisite of source Ex22 and its zero-time stochastic-continuity elaboration. Six source conditions and all actual80-style Z properties retained. No necessary mathematical or scope repair identified.',
 'semantic_slots':slots,'deltas':deltas,'repairs':[],'blocking_deltas':[],'no_required_header_repairs':True,
 'source_graph_coverage':{'items_expected':36,'items_reviewed':36,'items':items,'nodes_expected':13,'nodes_reviewed':13,'nodes':node_coverage,'edges_expected':20,'edges_reviewed':20,'edges':edges,'unmapped':[],
  'topology_original_bytes_unchanged':True,'scope_refinements':['Optional quantitative cap Ct omitted fromG82-09','G82-11 bounded-test expectation future consumer','G82-12 fullL2 semigroupOPEN','G82-13 rightcontinuity/restart/global packageOPEN']},
 'body_obligations_not_reviewed':['Consume actual firstwait survival plus true coordinate0 Exp marginal','Show eventTime1=actualfirstwait, including top guard','Use actual firstinterval covered identity to prove defect subset firsteventbytime','Prove probability finite and event measurability, preventing P.real toReal top artifacts','Prove Lambda_t->0 and Phi_tz0->z0','Positive threshold tail at0=0 from AE initialization; justify NNReal nhds0 squeeze'],
 'boundary_audit':{'source_timeline':'Ex22 appears after source invariance/Jensen as strong-continuity ingredient; advancing the independent probability ingredient first is honest and does not prove preceding invariance.',
  'firstwait_infinite':'t<top on every finite first arc, so actual Z_t=Phi_tz0; stopped next record has no infinity phase.',
  'zero_threshold':'Immediate waits/raw exceptional initialization allowed; actual Exp-positive AE supplies source initialization. Defect upper bound remains appropriate at0.',
  'fallback':'Uncovered z0 convention is retained; no firstevent survival covered point is replaced by fallback.',
  'filter':'NNReal nhds0 means right-neighborhood convergence including value0; positive delta and retained AEinit give value0 exactly.',
  'fixedparams':'No arbitrary correlated random initialization or uniformparams convergence/nullset claim.',
  'rank0':'No positive dimension needed; zero rate/infinitefirstwait gives zero defect.',
  'not_fullL2':'Invariance/Jensen/contractivity/density/semigroup and bounded-test expectation remain separate OPEN consumers.'},
 'independence':{'source_first_primary_and_frozen_pins_rechecked_before_header':True,'source_only_inventory_created_utc':inv['created_utc'],
  'own_frozen_inventory_graph_used':True,'proving_worker':False,'implementation_body_seen':False,'other_review_verdicts_seen':False,'root_adoption_or_math_verdict_seen':False,
  'owned_outputs_only':True,'no_statement_seal_or_proof_or_VERIFIED_credit':True},
 'truthboundary':'Header/source scope only. No implementation, compilation, blind reconstruction, final source proof review or formal verification performed. Original four-paper Goal unchanged.'})
inputs=[pathlib.Path(x['path'])for x in manifest['raw_inputs']+manifest['raw_outputs']]+[PRE/'source_freeze82.raw-manifest.json',HEADER]
outmanifest=write('header-source-review82.raw-manifest.json',{
 'schema':'noncircular-header-source-review-raw-manifest-v1','created_utc':now,'reviewer':'/root/fresh_source78',
 'raw_inputs':[raw(p)for p in inputs],'raw_outputs':[raw(pathlib.Path(__file__).resolve()),raw(result)],
 'source_first_chronology':'Primary and own frozen36/13/20 inventory/graph rechecked before exact header read. No body/other reviewers/implementation input.',
 'self_hash_omitted':True,'original_source_freeze_unchanged':True,'source_scope_only_no_proof_credit':True})
for x in load(outmanifest)['raw_inputs']+load(outmanifest)['raw_outputs']:assert sha(pathlib.Path(x['path']))==x['raw_sha256']
print(json.dumps({'verdict':load(result)['verdict'],'raw_result':raw(result),'raw_manifest':raw(outmanifest),'raw_script':raw(pathlib.Path(__file__).resolve()),'coverage':[36,13,20]},indent=2))
