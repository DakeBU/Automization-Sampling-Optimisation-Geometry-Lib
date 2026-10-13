"""Adopt independently reviewed header bytes before any theorem proof body."""
from pathlib import Path
import hashlib, json, sys, datetime, subprocess

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from tools import astis_advance as advance

PRE = ROOT / 'runs/20261007-companion-priority/pbps-ordered-iteration-preread92'
RUN = ROOT / 'runs/20261007-companion-priority/pbps-actual-ordered-prefix92'
CELL = 'ASTIS-SW-PBPS-actual-ordered-prefix'
ID = 'ASTIS-SA-20261011-PBPSActualOrderedPrefix'
MODULE = 'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualOrderedPrefix.lean'
DECL = 'AutoSamplingTheory.ExampleCases.ProximalBPS.ActualOrderedPrefix.actual_ordered_prefix_law'
OWNER = 'companion_root_20261005'

def read(p):
    return json.loads(Path(p).read_text(encoding='utf-8-sig'))

def digest(p):
    p = Path(p)
    if not p.is_absolute(): p = ROOT / p
    b = p.read_bytes()
    return {'path': p.as_posix(), 'raw_sha256': hashlib.sha256(b).hexdigest(), 'bytes': len(b)}

checked = {}
def check_tree(o):
    if isinstance(o, dict):
        if 'path' in o and 'raw_sha256' in o:
            actual = digest(o['path'])
            assert actual['raw_sha256'] == o['raw_sha256'], o['path']
            if 'bytes' in o: assert actual['bytes'] == o['bytes'], o['path']
            checked[actual['path']] = actual
        for v in o.values(): check_tree(v)
    elif isinstance(o, list):
        for v in o: check_tree(v)

def write(p, o):
    assert not p.exists(), p
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(o, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')

math = PRE/'independent-header-math92/header-math-review92.native.json'
source = PRE/'independent-header-source92/source-decision92.native.json'
assert digest(math)['raw_sha256'] == '788650e78b48188c70f3d03616ef29071cfb30238bb2c3035b1a605901a0a885'
assert digest(source)['raw_sha256'] == '71731f0b4cc73fc54f8e2f68c263c6a78e7701ebd081fe3c968c915195423375'
for p in [math, source,
          PRE/'independent-header-math92/header-review-closed-RAW92.native.json',
          PRE/'independent-header-source92/closed-RAW92.native.json',
          PRE/'independent-target-review/v2-recheck92.native.json']:
    check_tree(read(p))
preserved = read(PRE/'resume-before-seal92/preserved-collaborator92.json')
check_tree(preserved)
assert len(preserved) == 21
header = PRE/'prospective-header/Header92.lean'
assert digest(header)['raw_sha256'] == '9ad92c3ba89af78f3096342f7663bc547e6c03b6ce8173645cc13030d24bcd1f'
assert not (ROOT/MODULE).exists()
text = header.read_text(encoding='utf-8')
literal = text.split('def actual_ordered_prefix_statement',1)[1].split('\nend\nend Header92',1)[0]
anchor = 'Chen-Chewi-Lu-Zhang arXiv2609.06905v1 Appendix A.1 (A.1),(A.2), strict finite-prefix iteration ingredient of (A.7), and Appendix A.2 joint Borel construction; attributed ASTIS completion.'
delta = 'Derive the actual strict first-n complete-history law on the ordered absolute-time simplex, with the product pre-bounce rate/survival density, joint parameter measurability, and every nonnegative extended Borel history test.'
boundary = ('Six original analytic hypotheses; canonical iid Exp(1) product and literal stopped recursion. '
    'Every finite deterministic n and NNReal horizon T, including n=0 and T=0. '
    'Simplex 0<t1<...<tn<T carries the subtype comap of finite-dimensional real Lebesgue measure. '
    'Density is the finite product of pre-bounce rates times elapsed-segment survivals; no terminal survival. '
    'Joint Borel K/q in y,reference,initial phase and simplex time. Pointwise actual/prescribed complete-history identification on the strict prefix event. '
    'Exact unnormalized history pushforward, all ENNReal tests and total mass are conclusions, not providers. '
    'Abstract A does not constrain record0; actual H0 is live(0,z0). Rank-zero Hilbert and ENNReal tests are explicit ASTIS extensions. '
    'This is not the exact-n count event or full A7. Terminal survival, a.e. count/endpoint identification, full path equality, hazard stitching, '
    'summability, physical-time restart/Markovness, invariance/hypocoercivity, implementation errors/unbounded costs/main/composition/four papers remain OPEN.')
parents = ['AutoSamplingTheory.ExampleCases.ProximalBPS.ActualAbsoluteNextEventTime.actual_absolute_next_event_time_law']
search = [(PRE/'reuse-search'/x).relative_to(ROOT).as_posix() for x in ['local.log','mathlib.log','frontier.log']]
seal = {
 'status':'SEALED_BEFORE_BODY_AFTER_DISTINCT_HEADER_MATH_SOURCE_AND_TOPOLOGY_ACCEPTANCE',
 'sealed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'statement_version':1,'header':digest(header),'expanded_literal_Prop':literal,
 'public_theorem':DECL,'production_name_visibility_change_only':True,
 'source_revision':'arXiv2609.06905v1/Lean4.33.0/Mathlibdb584cd6d46c92f209a44c0f1c829460d327499d',
 'primary':digest('runs/20261007-companion-priority/phase-pbps-gamma-preread57/primary-pbps.exactraw.snapshot.html'),
 'source_graph':digest(PRE/'primary-first/candidate-source-proof-graph92.v2.native.json'),
 'source_coverage':digest(PRE/'primary-first/candidate-source-coverage92.v2.native.json'),
 'source_topology_review':digest(PRE/'independent-target-review/v2-recheck92.native.json'),
 'independent_math_header':digest(math),'independent_source_header':digest(source),
 'all_review_bound_inputs_rehashed':list(checked.values()),
 'toolchain':digest('lean-toolchain'),'lake_manifest':digest('lake-manifest.json'),
 'truth_boundary':boundary,'proof_BODY_created':False,
 'collaborator_RAW_preservation_count':21,
 'binder_audit':['hα,hαβ,hV,hH,hη,hβη are original source analytic assumptions.',
   'E structure instances express the finite-dimensional real Hilbert ASTIS extension, explicitly including rank0.',
   'Measurable F defines admissible observables; no moment/boundedness/positive probability premise.',
   'All actual-law, simplex, measurability, pointwise identification and density facts are internal obligations.'],
 'definition_kind':'25 literal lets, including 3 observer/history lets inside quantified parameters; all accepted without repair.'}
write(RUN/'root.statement-seal92.json',seal)
write(RUN/'root.preproof92.adoption.json',{'status':'ACCEPTED_HEADER_AND_SOURCE_TOPOLOGY_ONLY','seal':digest(RUN/'root.statement-seal92.json'), 'reviews':[digest(math),digest(source)],'proved':False,'verified':False})
proposal = advance.AdvanceProposal(advance_id=ID,task_id='ASTIS-SW-PBPS-2026',goal=delta,
 source_anchor=anchor,theorem_delta=delta,truth_boundary=boundary,created_by=OWNER,
 dag_inputs=tuple(parents),proposed_files=(MODULE,),
 focused_checks=('lake build AutoSamplingTheory.ExampleCases.ProximalBPS.ActualOrderedPrefix',),
 modes=('faithfulPaper',),priority=100,frontier_cell=CELL,target_declarations=(DECL,))
cell = {
 'schema_version':3,'cell_id':CELL,'route':'samplewiki-route','title':'Actual PBPS strict ordered-prefix complete-history law',
 'mode':'faithfulPaper','source_anchor':anchor,'target_statement':text,'status':'claimed',
 'parents':parents,'consumers':['A1.E7 finite-n full path term after terminal-survival and path-identification composition (planned, unproved)'],
 'source_targets':[DECL],'declaration_level':'source-anchor','blocked':{'status':False,'reason':'Statement sealed; proof implementation starting.'},
 'evidence':{'substantive_advance':ID,'statement_seal':str((RUN/'root.statement-seal92.json').relative_to(ROOT)).replace('\\','/'),
  'focused_checks':[],'owned_files':[MODULE],'truth_boundary':boundary},
 'shared_floor_audit':{'searched':search+['Libraries/shared-foundations.yml','Libraries/frontloaded-shared-spine.json'],
  'classification':'adapt','decision':'adapt_existing','canonical_declaration':DECL,'canonical_shared_cell':'',
  'reason':'Compose existing actual one-step density/history law with fixed Mathlib finite product/comap machinery; no generic theorem duplication.'},
 'reuse_plan':{'searched_existing':search,'reused_declarations':[], 'planned_dependencies':parents,
  'new_shared_declarations':[],'known_consumers':[],'planned_consumers':['PBPS A1.E7 full finite-n path density'],
  'no_duplicate_wrapper':True,'decision_reason':'New actual n-event integration node; inherited one-step theorem alone does not give ordered n-event law.'},
 'reader_contract':{'reference_standard':'textbook/chapter-01/section-1-3.html','source_ordered':True,
  'source_statement_adjacent':True,'natural_language_formula_proof':True,'hidden_assumptions_visible':True,'lean_collapsed':True,'external_dependencies_visible':True},
 'statement_seal':{'evidence':str((RUN/'root.statement-seal92.json').relative_to(ROOT)).replace('\\','/'),
  'source_revision':seal['source_revision'],'statement_version':1,'signature_digest':digest(header)['raw_sha256'],
  'binder_audit':seal['binder_audit'],'definition_kind':seal['definition_kind']},
 'source_proof_coverage':{'source_graph':seal['source_graph']['path'],'source_inventory':seal['source_coverage']['path'],
  'coverage_report':seal['source_topology_review']['path'],'coverage_status':'Independent source topology and candidate/header accepted; no proof coverage claimed.'},
 'source_detail_audit':{'primary_edition':seal['source_revision'],'primary_anchor':anchor,'fidelity_boundary':boundary,
  'detail_status':'omitted','gap':'Actual finite complete-history induction, simplex law and all-test measure formulation are implicit in the source iteration sentence.',
  'consulted':[{'source':'Pinned PBPS v1 and fixed Mathlib','anchor':'A1.E1;A1.E2;A1.E7;A1.SS2',
   'hypothesis_adapter':'Six source binders unchanged; source review explicitly accepts Hilbert/rank0 and ENNReal test extensions.'}]},
 'proof_digestion':{'existing_substrate':parents,'bookkeeping':['Ordered simplex coordinates and whole-history recursion.'],
  'new_reusable':[],'new_topology':delta},
 'purification':{'status':'pending','dead_code_audit':'Proof not yet implemented.','duplicate_semantics_audit':'Bounded retrieval found no existing actual ordered-prefix law.',
  'canonicalization':'Reuse canonical fixed Mathlib product/comap and existing actual-process leaves.','compressed_spine_delta':delta,
  'reader_default_view':'Full attributed statement and formula proof with adjacent initially folded exact Lean.','scope':boundary},
 'learning_contract':{'control_plane_math_authority':False,'process_memory_checked':True,'process_memory_ids':[],
  'failure_class':'NONE','salvage':{'required':False,'status':'not-applicable','reason':'Preproof header elaboration fixes retained; no proof fragment discarded.','promoted_fragments':[],'discarded_fragments':[]},
  'parallelism':{'decision':'serial','direction_fingerprints':['actual-prefix/absolute-coordinate-induction/complete-history'],
   'expected_information_gain':'One proof owner; independent math and source reviewers examine distinct uncertainties.',
   'shared_verified_context_digest':digest(header)['raw_sha256']},
  'cross_route_blind_spot_audit':{'required':False,'status':'not-applicable','evidence':'','canonical_route':'samplewiki-route','selection_reason':'One selected implementation route; alternatives remain source OR routes, not parallel proof claims.'},
  'reader_backpressure':{'purification_status':'pending','exposition_seal_status':'pending','exposition_evidence':'',
   'source_expansion_nodes':['A1.E1','A1.E2','A1.E7'],'lean_expansion_nodes':[DECL],'assumptions_preserved':False,'boundary_preserved':False}},
 'graph_contribution':{'lean_view':'integration-node','overview_view':'no-change-with-reason','functor_view':'none-found',
  'edge_semantics':'formal-solid; overlays-dashed','color_semantics':'evidence-status; library-scope','focus_targets':[DECL],
  'visual_review':'Pending proof/publication; existing paper route retained. No new conceptual bridge proposed.'}}
write(ROOT/f'research-wiki/frontier-cells/{CELL}.json',cell)
advance.propose_advance(proposal)
write(RUN/'claim.json',proposal.as_event())
advance.transition_advance(ID,'CLAIMED',worker_id=OWNER,evidence={'statement_seal':digest(RUN/'root.statement-seal92.json')})
advance.transition_advance(ID,'EXPLORING',worker_id=OWNER,evidence={'proof_route':'Existing actual91 one-step law -> finite ordered-prefix induction; no terminal survival.'})
print(json.dumps({'advance':ID,'state':'EXPLORING','review_inputs_rehashed':len(checked),'seal':digest(RUN/'root.statement-seal92.json')},indent=2))
