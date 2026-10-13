from pathlib import Path
import hashlib, json, os, subprocess, sys

base=Path('runs/20261007-companion-priority')
pre=base/'pbps-iid-product-preproof77'
r=base/'pbps-unit-exponential-product77'
load=lambda p: json.loads(Path(p).read_bytes())
sha=lambda b: hashlib.sha256(b).hexdigest()
def new(p,x):
 p=Path(p); assert not p.exists(); p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
seal=load(pre/'root.statement-seal77.json')
header=Path(seal['header']['path']); assert sha(header.read_bytes())==seal['header']['RAW_sha256']
adoption=load(pre/'root.header-reviews77.adoption.json')
assert adoption['prospective_header_accepted'] and not adoption['theorem_proved']
for z in adoption['native_leases']:
 assert sha(Path(z['path']).read_bytes())==z['RAW_sha256']
head=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()
assert head=='10ca06b04634e95ff67b461c7b37c9cee0931998'
assert subprocess.check_output(['git','rev-parse','origin/codex/sphmc-standardized-rgo'],text=True).strip()==head
assert subprocess.run(['git','merge-base','--is-ancestor','origin/main','HEAD']).returncode==0
file='AutoSamplingTheory/TechnicalLemmas/Probability/UnitExponentialProduct.lean'
decl='AutoSamplingTheory.TechnicalLemmas.Probability.UnitExponentialProduct.unit_exponential_product_laws'
assert not Path(file).exists()
cid='ASTIS-SHARED-unit-exponential-product'; aid='ASTIS-SA-20261010-UnitExponentialProduct'; owner='companion_root_20261005'
delta='Actual countable Exp(1) product: probability, Borel coordinate and clamped threshold maps, exact real coordinate marginals, mutual independence, simultaneous a.s. positivity/clamp equality and divergent clamped real partial sums.'
source='Chen--Chewi--Lu--Zhang arXiv2609.06905v1 AppendixA.1 independent Exp1 inputs and Ex9/SLLN clause; concrete background realization for actual PBPS event-time nonaccumulation.'
boundary='Countable unit-exponential input law only. No event-time nonaccumulation, global physical-time path/PDMP/Markov/invariance/kernel/hypocoercivity/main/error/expected-query cost/actual-input composition. Source author direct Exp-SLLN/mean-one route remains separate from any sufficient ASTIS bounded-indicator SLLN alternative. No full Exposition/PURIFIED/main/live/whole-paper/Goal credit.'
searched=['Samplinglib Probability.lean, TechnicalLemmas/Probability and Measure/Product module cards, current shared Frontier Cells: no existing actual countable Exp1 input-law producer; existing finite products are distinct.', 'Pinned Mathlib Exponential.expMeasure/isProbabilityMeasure_expMeasure/cdf_expMeasure_eq; ProductMeasure.infinitePi/infinitePi_map_eval; Independence.InfinitePi.iIndepFun_infinitePi; StrongLaw.strong_law_ae_real; no floating upstream.', 'Source-only77 original A1 graph and exact support/index/background gaps; actual finite PBPS recursion76 is a later consumer substrate, not a formal parent of this generic probability theorem.']
consumers=['PBPS AppendixA.1 Ex9: next actual event-time nonaccumulation adapter combines this realized threshold sequence with the compiled recursion76 original-energy waiting increment.']
reused=['ProbabilityTheory.expMeasure','ProbabilityTheory.isProbabilityMeasure_expMeasure','MeasureTheory.Measure.infinitePi','MeasureTheory.Measure.infinitePi_map_eval','ProbabilityTheory.iIndepFun_infinitePi','ProbabilityTheory.strong_law_ae_real']
reason='Adapt canonical pinned Mathlib probability/product/independence/SLLN APIs once at the route-neutral probability layer for the real PBPS consumer. There is only one currently evidenced consuming paper route; no invented second consumer or copied paper-local probability foundation.'
r.mkdir(exist_ok=False)
def run(label,args):
 with (r/(label+'.stdout.json')).open('wb') as s,(r/(label+'.stderr.log')).open('wb') as e:
  cmd=[sys.executable,'-B','-X','utf8',*args]; p=subprocess.Popen(cmd,stdout=s,stderr=e); code=p.wait()
 new(r/(label+'.receipt.json'),dict(command=cmd,actual_PID=p.pid,exit_code=code,terminal_closed=True)); assert code==0
run('harness-reconcile',['tools/astis.py','harness-reconcile','--json'])
run('capsule',['tools/astis_advance.py','capsule'])
sys.path.insert(0,str(Path.cwd()/'tools')); import astis_advance as adv
ledger=Path('runs/substantive_advances.jsonl'); before=ledger.read_bytes()
proposal=adv.AdvanceProposal(advance_id=aid,task_id='ASTIS-SW-PBPS-2026',goal=delta,source_anchor=source,theorem_delta=delta,truth_boundary=boundary,created_by=owner,dag_inputs=(),proposed_files=(file,),focused_checks=('lake build AutoSamplingTheory.TechnicalLemmas.Probability.UnitExponentialProduct',),modes=('faithfulPaper',),priority=100,frontier_cell=cid,target_declarations=(decl,))
adv.propose_advance(proposal)
adv.transition_advance(aid,'CLAIMED',worker_id=owner,evidence=dict(statement_seal=(pre/'root.statement-seal77.json').as_posix(),owned_files=[file]))
adv.transition_advance(aid,'EXPLORING',worker_id=owner,evidence=dict(route='Actual infinite product, derived coordinate laws, support/CDF, optional sufficient bounded-indicator iid SLLN and pointwise domination.',truth_boundary=boundary))
after=ledger.read_bytes(); assert after[:len(before)]==before
(r/'ledger.claim77.append.exactraw.jsonl').write_bytes(after[len(before):]); new(r/'claim.json',proposal.as_event())
graph=(pre/'fresh-source77/source-topology.json').as_posix(); inventory=(pre/'fresh-source77/source-coverage.json').as_posix()
c=dict(schema_version=3,cell_id=cid,route='shared',title='Actual countable unit-exponential product inputs',mode='faithfulPaper',source_anchor=source,target_statement=header.read_text(encoding='utf8'),status='claimed',parents=[],consumers=consumers,source_targets=[decl],
 shared_floor_audit=dict(searched=searched,classification='adapt',decision='adapt_existing',canonical_declaration=decl,canonical_shared_cell=cid,reason=reason),
 reuse_plan=dict(searched_existing=searched,reused_declarations=reused,new_shared_declarations=[decl],known_consumers=[],planned_consumers=consumers,no_duplicate_wrapper=True,decision_reason=reason),
 evidence=dict(substantive_advance=aid,statement_seal=(pre/'root.statement-seal77.json').as_posix(),focused_checks=[],owned_files=[file],truth_boundary=boundary),
 blocked=dict(status=False,reason='Distinct prospective header math and source review complete; proof and compiled semantic roundtrip still pending.'),
 statement_seal=dict(evidence=(pre/'root.statement-seal77.json').as_posix(),source_revision='arXiv2609.06905v1/Lean4.33.0/Mathlibdb584cd6d46c92f209a44c0f1c829460d327499d',statement_version=2,signature_digest=seal['header']['RAW_sha256'],binder_audit=dict(public_premises=[],literal_definitions=3,conclusion_groups=5),definition_kind='Three actual literal definitions P/X/epsilon and five groups; no assumed probability, iid, support, moment, SLLN or divergent-sum provider.'),
 source_proof_coverage=dict(source_graph=graph,source_inventory=inventory,coverage_status='Prospective source-only23/23-item disposition; graph/coverage are extractor candidates awaiting distinct compiled-source review. No theorem proof credit.'),
 source_detail_audit=dict(primary_edition='arXiv2609.06905v1',primary_anchor=source,fidelity_boundary=boundary,detail_status='omitted',gap='Source omits actual product construction, support/moment/SLLN instantiation. Direct author Exp mean-one route remains identifiable; an optional bounded-indicator route may prove the same divergence without adding public premises.',consulted=[dict(source='Pinned Mathlib Probability Exponential/ProductMeasure/Independence/StrongLaw',anchor='Exp1 support CDF; infinite product evaluation laws; integrable real iid strong law',hypothesis_adapter='Derive factor/product probability, measurability, iid and integrability internally. Total NNReal clamp is a.e. equal to positive real coordinates; index k means source E_(k+1).')]),
 proof_digestion=dict(existing_substrate=reused,bookkeeping=['Countable product and total measurable NNReal clamp.'],new_reusable=[decl],new_topology=delta),
 purification=dict(status='pending',dead_code_audit='Pending implementation.',duplicate_semantics_audit='No local countable Exp1 realization found.',canonicalization=reason,compressed_spine_delta=delta,reader_default_view='Complete attributed statement and formula proof with adjacent initially folded exact Lean.',scope=boundary),
 reader_contract=dict(reference_standard='textbook/chapter-01/section-1-3.html',source_ordered=True,source_statement_adjacent=True,natural_language_formula_proof=True,hidden_assumptions_visible=True,lean_collapsed=True,external_dependencies_visible=True),
 graph_contribution=dict(lean_view='reusable-interface',overview_view='updated',functor_view='pending',edge_semantics='formal-solid; overlays-dashed',color_semantics='evidence-status; library-scope',focus_targets=[decl],visual_review='Pending proof/review; no source topology edge receives formal Lean credit.'),
 conceptual_mirror_audit=dict(status='pending',discovery_ids=[],reason='Audit before PROVED_LOCAL; source author route and ASTIS optional route remain separately identified.'),
 learning_contract=dict(control_plane_math_authority=False,process_memory_checked=True,process_memory_ids=[],failure_class='NONE',salvage=dict(required=False,status='not-applicable',reason='Before theorem proof; original header missing NNReal scope retained and independently checked exact scope-only v2 repair. Existing process memory entries concern other domains and add no premise here.',promoted_fragments=[],discarded_fragments=[]),parallelism=dict(decision='serial',direction_fingerprints=['countable-Exp1-product/support/indicator-SLLN/domination'],expected_information_gain='One writer; independent math/blind decoder/fresh source review after focused compile.',shared_verified_context_digest=seal['header']['RAW_sha256']),cross_route_blind_spot_audit=dict(required=False,status='not-applicable',evidence='',canonical_route='shared',selection_reason=reason),reader_backpressure=dict(purification_status='pending',exposition_seal_status='pending',exposition_evidence='',source_expansion_nodes=['source-exp1-input','author-SLLN-route','actual-product-background','AE-support-and-clamp','optional-ASTIS-OR-route','later-event-time-consumer-open'],lean_expansion_nodes=[decl],assumptions_preserved=True,boundary_preserved=True)))
new(Path('research-wiki/frontier-cells')/(cid+'.json'),c)
new(r/'preproof-admission.json',dict(status='CLAIMED_EXPLORING_NOT_PROVED',actual_root_PID=os.getpid(),checked_parent=head,statement_seal=(pre/'root.statement-seal77.json').as_posix(),theorem_delta=delta,truth_boundary=boundary,Goal_complete=False))
run('publication-packet-before-proof',['tools/astis_publication.py','packet','--cell',cid])
run('frontier-before-proof',['tools/astis_frontier_cells.py','check'])
print('PASS77 CLAIMED/EXPLORING actual Exp1 product; bounded publication packet before proof complete.')
