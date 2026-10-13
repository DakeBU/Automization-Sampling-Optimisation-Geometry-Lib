"""Run only after native independent whole-header reviews are adopted."""
from pathlib import Path
import copy,datetime,hashlib,json,subprocess,sys
r=Path(__file__).parent;pre=r.parent/'pbps-transition-kernel-preread85'
load=lambda p:json.loads(Path(p).read_bytes())
def pin(p):
 p=Path(p);b=p.read_bytes();return dict(path=p.as_posix(),RAW_bytes=len(b),RAW_sha256=hashlib.sha256(b).hexdigest())
def new(p,x):
 assert not p.exists(),p;p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
adoption=load(r/'independent-review-adoption85.json');assert adoption['accepted']
header=Path(adoption['accepted_header']['path']);assert pin(header)==adoption['accepted_header']
for p in adoption['frozen_native_inputs']:assert pin(p['path'])==p
file='AutoSamplingTheory/ExampleCases/ProximalBPS/ActualPhaseTransitionKernel.lean'
assert not Path(file).exists()
sys.path.insert(0,str(Path.cwd()/'tools'));import astis_advance as adv
owner='companion_root_20261005';aid='ASTIS-SA-20261011-PBPSActualPhaseTransitionKernel';cid='ASTIS-SW-PBPS-actual-phase-transition-kernel'
states=adv.current_advances()
assert states['ASTIS-SA-20261011-PBPSActualOuterBoundedL2Continuity']['state']=='VERIFIED'
assert [k for k,v in states.items() if v['state']=='STABILIZING']==['ASTIS-SA-20261005-SPHMCImplementedPhaseKernel']
assert aid not in states
decl='AutoSamplingTheory.ExampleCases.ProximalBPS.ActualPhaseTransitionKernel.actual_phase_transition_kernel'
parents=['AutoSamplingTheory.ExampleCases.ProximalBPS.ActualPhysicalTimeMeasurability.actual_physical_time_measurable_phase','AutoSamplingTheory.TechnicalLemmas.Probability.UnitExponentialProduct.unit_exponential_product_laws']
delta='Derive one jointly indexed actual finite-physical-time full-phase probability kernel from the same actual80 phase Z and literal iidExp1 clocks, exact pushforward/event laws, zero-time Dirac initialization and bounded Borel real-test dual integrability and expectation transfer.'
anchor='Chen-Chewi-Lu-Zhang arXiv2609.06905v1 AppendixA.1 actual transition operators and bounded measurable tests p3.1/p5.2/p6.1. ASTIS all-finite jointly indexed full-phase probability-kernel elaboration.'
boundary='Original six analytic hypotheses and all eleven literal actual algorithm definitions/fullactual80 phase clauses retained. Same actual Z precedes the jointly indexed K and every bounded Borel real test. Exact iidExp1 fiber laws, measurable-event identity, probability fibers, Dirac0 and both clock/law integrability with exact expectation transfer only. Source failed-limit0 versus uncovered-z0 conventions agree only at each fixed-parameter AE law. No uniform-parameter AE or arbitrary correlated input substitution. IsMarkovKernel is a probability-fiber class, not process Markov/restart/Chapman-Kolmogorov. Invariance/path-law reversal/fullL2/Jensen contraction/density/hypocoercivity/implemented sampler/error/unbounded expected cost/composition/main/PURIFIED/live/fullpaper/Goal remain OPEN.'
seal=dict(status='SEALED_BEFORE_PROOF_AFTER_INDEPENDENT_HEADER_MATH_SOURCE_AND_TOPOLOGY_REVIEW',sealed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),statement_version=1,header=pin(header),expanded_literal_Prop=header.read_text(encoding='utf8').split('private def ',1)[1].split('\nend\n',1)[0],public_theorem=decl,source_first_freeze=pin(pre/'source-first-run-manifest85.json'),source_graph=pin(pre/'source-proof-graph85.reviewed-effective.json'),source_inventory=pin(pre/'source-inventory85.reviewed-effective.json'),reviewed_topology_overlay=pin(pre/'root.topology-adoption85.json'),independent_header_adoption=pin(r/'independent-review-adoption85.json'),reuse_search=pin(pre/'retrieval85/reuse-decision85.json'),toolchain=pin('lean-toolchain'),lake_manifest=pin('lake-manifest.json'),truth_boundary=boundary,proof_BODY_created=False)
new(r/'root.statement-seal85.json',seal)
p=adv.AdvanceProposal(advance_id=aid,task_id='ASTIS-SW-PBPS-2026',goal=delta,source_anchor=anchor,theorem_delta=delta,truth_boundary=boundary,created_by=owner,dag_inputs=tuple(parents),proposed_files=(file,),focused_checks=('lake build AutoSamplingTheory.ExampleCases.ProximalBPS.ActualPhaseTransitionKernel',),modes=('faithfulPaper',),priority=100,frontier_cell=cid,target_declarations=(decl,))
adv.propose_advance(p)
adv.transition_advance(aid,'CLAIMED',worker_id=owner,evidence=dict(statement_seal=(r/'root.statement-seal85.json').as_posix(),owned_files=[file]))
adv.transition_advance(aid,'EXPLORING',worker_id=owner,evidence=dict(route='Consume actual80 Z; selected id-times-constant-clock map realization; actual fiber identity, AE initialization gives Dirac0, bounded Borel probability integrability and integral_map.',truth_boundary=boundary))
new(r/'claim.json',p.as_event())
c=copy.deepcopy(load('research-wiki/frontier-cells/ASTIS-SW-PBPS-actual-outer-bounded-l2-continuity.json'))
c.update(cell_id=cid,title='Actual PBPS finite-time full-phase probability kernel',source_anchor=anchor,target_statement=header.read_text(encoding='utf8'),status='claimed',parents=parents,consumers=['AppendixA.1 actual transition-law/test interface: represent literal-clock bounded Borel expectations as the same full-phase law, with zero-time Dirac initialization. Future invariance may use this representation or direct pushforwards; neither representation alone proves invariance.'],source_targets=[decl],blocked=dict(status=False,reason='Independent source topology and separately reviewed exact overlay plus whole-header mathematics/type/source accepted. Root is sole writer; BODY pending.'))
c['evidence']=dict(substantive_advance=aid,statement_seal=(r/'root.statement-seal85.json').as_posix(),focused_checks=[],owned_files=[file],truth_boundary=boundary)
reuse=load(pre/'retrieval85/reuse-decision85.json');search=[x['output'] for x in reuse['queries']]
c['shared_floor_audit']=dict(searched=search,classification='adapt',decision='adapt_existing',canonical_declaration=decl,canonical_shared_cell='',reason=reuse['reason'])
c['reuse_plan']=dict(searched_existing=search,reused_declarations=parents,new_shared_declarations=[],known_consumers=[],planned_consumers=c['consumers'],no_duplicate_wrapper=True,decision_reason=reuse['reason'])
c['statement_seal']=dict(evidence=(r/'root.statement-seal85.json').as_posix(),source_revision='arXiv2609.06905v1/Lean4.33.0/Mathlibdb584cd6d46c92f209a44c0f1c829460d327499d',statement_version=1,signature_digest=pin(header)['RAW_sha256'],binder_audit=['Original six analytic standing source binders unchanged.','Actual P/Z/joint measurability/init and K probability are derived outputs, never added premises.','Bounded Borel real g with explicit nonnegative M are test variables, not hidden dynamics regularity.'],definition_kind='Eleven literal actual algorithm definitions and fullactual80 phase contract retained; same iidExp1 input and explicit exceptional fallback. Joint kernel packaging is an attributed ASTIS elaboration.')
c['source_proof_coverage']=dict(source_graph=(pre/'source-proof-graph85.reviewed-effective.json').as_posix(),source_inventory=(pre/'source-inventory85.reviewed-effective.json').as_posix(),coverage_report=(r/'independent-review-adoption85.json').as_posix(),reviewed_adapter_overlay=(pre/'root.topology-adoption85.json').as_posix(),coverage_status='Independent16inventory/21nodes/29relations:26dependencies including6futureOPEN and3excludedassociations. Selected id/const/map route ingredients AND; alternative representation unselected, no invariance/Markov implication. BODY source review still OPEN.')
c['source_detail_audit']=dict(primary_edition=c['statement_seal']['source_revision'],primary_anchor=anchor,fidelity_boundary=boundary,detail_status='omitted',gap='Source transition tests suppress the explicit joint kernel packaging, fixed-parameter exceptional-law handling and bounded Borel integrability. Actual n-jump path law/reversal/invariance and AE-safe fullL2 extension remain future obligations.',consulted=[dict(source='Pinned primary AppendixA.1, actual80/UnitExp and pinned Mathlib kernel/measure/integral APIs',anchor='A1.SS2.p3.1;A1.SS1.SSS0.Px1.p5.2;A1.SS1.SSS0.Px1.p6.1',hypothesis_adapter='Retain source dynamics hypotheses; derive literal-clock law, Dirac0 and integrability from actual producer. No supplied measurable arbitrary process premise.')])
c['proof_digestion']=dict(existing_substrate=parents,bookkeeping=['Retain actual phase and fixed-parameter commonAE/init clauses.','Derive jointly indexed actual full-phase law via existing generic kernel APIs.','Derive Dirac0 and bounded Borel dual integrability/expectation transfer.'],new_reusable=[],new_topology=delta)
c['purification']=dict(status='pending',dead_code_audit='Pending proof',duplicate_semantics_audit='Existing81 is ideal random-reference/momentum position law at pi. Actual80/83/84 provide Z/expectations, no exported actual full-phase kernel.',canonicalization='Reuse fixed generic Mathlib kernel and integration APIs; no new generic wrappers.',compressed_spine_delta=delta,reader_default_view='Attributed full statement/formula proof, exact initially folded Lean adjacent.',scope=boundary)
c['learning_contract']['parallelism'].update(decision='serial',direction_fingerprints=['actual80-Z/actual-Exp1/id-const-map/Dirac0/bounded-Borel-transfer'],shared_verified_context_digest=seal['source_first_freeze']['RAW_sha256'])
c['learning_contract']['process_memory_ids']=[]
c['learning_contract']['salvage'].update(reason='No BODY search before full independently accepted source topology/overlay and whole-header/type/source review.')
c['learning_contract']['reader_backpressure'].update(purification_status='pending',exposition_seal_status='pending',exposition_evidence='',source_expansion_nodes=['actual80-phase','actual-joint-law-kernel','fixed-parameter-AE-Dirac0','bounded-Borel-integrability','actual-expectation-transfer'],lean_expansion_nodes=[decl])
c['graph_contribution'].update(focus_targets=[decl],lean_view='new-node',visual_review='Pending proof/publication/affected reference graph coverage and actual page acceptance. Source-name scanning is not an elaborated dependency certificate.')
c['conceptual_mirror_audit']=dict(status='pending',discovery_ids=[],reason='Required before PROVED_LOCAL; no new conceptual bridge claimed.')
new(Path('research-wiki/frontier-cells')/(cid+'.json'),c)
for label,args in [('publication-packet-before-proof85',['tools/astis_publication.py','packet','--cell',cid]),('frontier-before-proof85',['tools/astis_frontier_cells.py','check'])]:
 q=subprocess.run([sys.executable,'-X','utf8',*args],capture_output=True)
 (r/(label+'.stdout.json')).write_bytes(q.stdout);(r/(label+'.stderr.log')).write_bytes(q.stderr)
 new(r/(label+'.receipt.json'),dict(exit_code=q.returncode,terminal_closed=True))
 assert q.returncode==0,(q.stdout+q.stderr).decode(errors='replace')[-5000:]
print('85 exact independently reviewed statement sealed and claimed; no proof credit')
