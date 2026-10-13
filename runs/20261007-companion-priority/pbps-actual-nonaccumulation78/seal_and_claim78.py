"""Freeze reviewed header and claim one actual-input integration edge before proof."""
from pathlib import Path
import copy, datetime, hashlib, json, os, subprocess, sys
ROOT = Path.cwd()
RUN = Path('runs/20261007-companion-priority/pbps-actual-nonaccumulation78')
load = lambda p: json.loads(Path(p).read_bytes())
def write(p, x):
    p = Path(p); assert not p.exists(), p
    p.write_text(json.dumps(x, ensure_ascii=False, indent=2)+'\n', encoding='utf8', newline='\n')
def pin(p):
    p = Path(p); b=p.read_bytes()
    return dict(path=p.as_posix(), RAW_bytes=len(b), RAW_sha256=hashlib.sha256(b).hexdigest())
def run(label, args):
    cmd=[sys.executable,'-B','-X','utf8',*args]
    with (RUN/(label+'.stdout.json')).open('wb') as out, (RUN/(label+'.stderr.log')).open('wb') as err:
        p=subprocess.Popen(cmd, stdout=out, stderr=err); code=p.wait()
    write(RUN/(label+'.receipt.json'),dict(command=cmd,actual_PID=p.pid,exit_code=code,terminal_closed=True))
    assert code==0, label
header=RUN/'header-review78/header78.private-syntax-only.lean'
assert pin(header)['RAW_sha256']=='b94c3c35220873d034467b16d0ebd4c618cfbfc96b6ef26318a8f4e88d7b9c43'
assert load(RUN/'header-review78/private-visibility-typecheck.receipt.json')['exit_code']==0
assert pin(RUN/'syntax-overlay-review78/private-visibility-preservation.result.json')['RAW_sha256']=='85206120c72aad669ae3bb13b35bbb086a09d1d92d70714db807a0c849c44a81'
source=load(RUN/'source-preread78/source-freeze78.json')
review=load(RUN/'header-review78/independent-source-topology-review78.json')
overlay=dict(artifact_kind='reviewed source edge refinements and ASTIS conclusion adapters',source_freeze=pin(RUN/'source-preread78/source-freeze78.json'),review=pin(RUN/'header-review78/independent-source-topology-review78.json'),edges=review['reviewer_edge_clarifications'],source_graph_unchanged=True,compiled=False)
write(RUN/'reviewed-source-adapter-overlay78.json',overlay)
cid='ASTIS-SW-PBPS-actual-event-time-nonaccumulation'
aid='ASTIS-SA-20261010-PBPSActualNonaccumulation'
owner='companion_root_20261005'
file='AutoSamplingTheory/ExampleCases/ProximalBPS/ActualNonaccumulation.lean'
decl='AutoSamplingTheory.ExampleCases.ProximalBPS.ActualNonaccumulation.actual_fixed_reference_event_time_nonaccumulation'
parents=['AutoSamplingTheory.ExampleCases.ProximalBPS.ActualFiniteJumpRecursion.actual_fixed_reference_finite_jump_recursion','AutoSamplingTheory.TechnicalLemmas.Probability.UnitExponentialProduct.unit_exponential_product_laws']
assert not Path(file).exists()
delta='Actual fixed-reference PBPS A.2 event times with canonical countable Exp1 thresholds: almost surely escape every finite horizon, and only finitely many event indices lie below each finite horizon, including initialization index0.'
anchor='arXiv2609.06905v1 Appendix A.1 (A.2), Ex8-Ex9 and following SLLN/nonaccumulation clauses; Algorithm1 actual flow/bounce/rate and standing six analytic conditions.'
boundary='Only actual fixed-reference recursion nonaccumulation and finite bounded-horizon indices. No global physical-time path existence/uniqueness/measurability, Markov/invariance/kernel/hypocoercivity, PBPS main accuracy/implementation error/expected queries or PBPS-SPHMC composition. Author direct Exp mean-one SLLN remains an alternative open route; ASTIS uses verified bounded-indicator divergence. No merged/stabilized/purified/live/full-paper/Goal credit.'
seal=dict(status='SEALED_BEFORE_PROOF_AFTER_DISTINCT_HEADER_AND_OVERLAY_REVIEWS',sealed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),actual_root_PID=os.getpid(),statement_version=1,header=pin(header),public_theorem=decl,expanded_literal_Prop=header.read_text(encoding='utf8').split('private def ',1)[1].split('\nend\n',1)[0],primary=dict(path=source['primary_path'],RAW_sha256=source['primary_raw_sha256']),source_first_freeze=pin(RUN/'source-preread78/source-freeze78.json'),source_graph_overlay=pin(RUN/'reviewed-source-adapter-overlay78.json'),header_math=pin(RUN/'header-review78/header-math-review78.json'),source_topology_review=pin(RUN/'header-review78/independent-source-topology-review78.json'),syntax_overlay_review=pin(RUN/'syntax-overlay-review78/syntax-overlay-preservation.result.json'),private_overlay_review=pin(RUN/'syntax-overlay-review78/private-visibility-preservation.result.json'),typecheck=pin(RUN/'header-review78/private-visibility-typecheck.receipt.json'),binder_inventory=source['binder_map'],definition_audit=source['definitions'],dag_parents=[pin('AutoSamplingTheory/ExampleCases/ProximalBPS/ActualFiniteJumpRecursion.lean'),pin('AutoSamplingTheory/TechnicalLemmas/Probability/UnitExponentialProduct.lean')],toolchain=pin('lean-toolchain'),lake_manifest=pin('lake-manifest.json'),truth_boundary=boundary,proof_BODY_created=False,VERIFIED=False)
write(RUN/'root.statement-seal78.json',seal)
run('harness-reconcile78',['tools/astis.py','harness-reconcile','--json'])
run('capsule78',['tools/astis_advance.py','capsule'])
sys.path.insert(0,str(ROOT/'tools')); import astis_advance as adv
proposal=adv.AdvanceProposal(advance_id=aid,task_id='ASTIS-SW-PBPS-2026',goal=delta,source_anchor=anchor,theorem_delta=delta,truth_boundary=boundary,created_by=owner,dag_inputs=tuple(parents),proposed_files=(file,),focused_checks=('lake build AutoSamplingTheory.ExampleCases.ProximalBPS.ActualNonaccumulation',),modes=('faithfulPaper',),priority=100,frontier_cell=cid,target_declarations=(decl,))
adv.propose_advance(proposal)
adv.transition_advance(aid,'CLAIMED',worker_id=owner,evidence=dict(statement_seal=(RUN/'root.statement-seal78.json').as_posix(),owned_files=[file]))
adv.transition_advance(aid,'EXPLORING',worker_id=owner,evidence=dict(route='Actual finite stopped recursion plus actual Exp product; C0 absorbing stop or Cpositive scaled partial-sum comparison; finite-index-set adapter.',truth_boundary=boundary))
write(RUN/'claim.json',proposal.as_event())
template=load('research-wiki/frontier-cells/ASTIS-SW-PBPS-actual-finite-jump-recursion.json')
searched=['Samplinglib ActualFiniteJumpRecursion and UnitExponentialProduct actual parents; source-consumer nonaccumulation is not yet present. Related abstract SLLN/clock consumers cannot replace actual A.2 inputs.','Pinned Mathlib NNReal coe_sum / Real.toNNReal_div / WithTop coe_add / Filter eventually_atTop and finite Iio set; no upstream transplant needed.','Current shared Frontier Cells, Registry and module cards reuse Probability canonical exponential product; no new stochastic foundation copy.']
consumers=['PBPS AppendixA.1 all-physical-time path construction requires actual finite-horizon nonaccumulation before measurable path/Markov/invariance proofs.']
c=dict(schema_version=3,cell_id=cid,route='samplewiki-route',title='Actual PBPS event-time nonaccumulation',mode='faithfulPaper',source_anchor=anchor,target_statement=header.read_text(encoding='utf8'),status='claimed',parents=parents,consumers=consumers,source_targets=[decl],declaration_level='source-anchor',blocked=dict(status=False,reason='Sealed reviewed exact statement; sole writer implementing the source dependency-ready integration.'),reader_contract=copy.deepcopy(template['reader_contract']))
c['evidence']=dict(substantive_advance=aid,statement_seal=(RUN/'root.statement-seal78.json').as_posix(),focused_checks=[],owned_files=[file],truth_boundary=boundary)
c['shared_floor_audit']=dict(searched=searched,classification='missing',decision='new_route_local',canonical_declaration=decl,canonical_shared_cell='',reason='Actual PBPS consumer joining two compiled parents; no supplied cap/probability/SLLN/recurrence witness.')
c['reuse_plan']=dict(searched_existing=searched,reused_declarations=parents,new_shared_declarations=[],known_consumers=[],planned_consumers=consumers,no_duplicate_wrapper=True,decision_reason=c['shared_floor_audit']['reason'])
c['statement_seal']=dict(evidence=(RUN/'root.statement-seal78.json').as_posix(),source_revision='arXiv2609.06905v1/Lean4.33.0/Mathlibdb584cd6d46c92f209a44c0f1c829460d327499d',statement_version=1,signature_digest=seal['header']['RAW_sha256'],binder_audit=source['binder_map'],definition_kind='Private complete literal Prop, eleven actual definitions, original six analytic binders, two almost-sure conclusions; specification only.')
c['source_proof_coverage']=dict(source_graph=(RUN/'source-preread78/source-freeze78.json').as_posix(),source_inventory=(RUN/'source-preread78/source-freeze78.json').as_posix(),coverage_report=(RUN/'header-review78/independent-source-topology-review78.json').as_posix(),reviewed_adapter_overlay=(RUN/'reviewed-source-adapter-overlay78.json').as_posix(),coverage_status='Prospective complete scoped source inventory and reviewed adapters only. Actual proof coverage OPEN.')
c['source_detail_audit']=dict(primary_edition=c['statement_seal']['source_revision'],primary_anchor=anchor,fidelity_boundary=boundary,detail_status='omitted',gap='Partial sum clock comparison, C0 stopping and finite-index adapter are background source steps to close. Direct author Exp moment route remains distinct from the verified indicator route.',consulted=[dict(source='Fixed Mathlib and actual PBPS finite recursion/Exp product local parents',anchor='A1.Ex8-Ex9; WithTop/NNReal/Filter/Nat finite sets',hypothesis_adapter='Six source analytic binders only; positive cap and good input event are derived internally. Stopped records have eventTime top, no phase at infinity.')])
c['proof_digestion']=dict(existing_substrate=parents,bookkeeping=['Stopped-as-top representation; source E1 is coordinate0; initial event index0 counts in the finite sublevel set.'],new_reusable=[],new_topology=delta)
c['purification']=dict(status='pending',dead_code_audit='Pending proof',duplicate_semantics_audit='Two parents do not themselves prove actual source clock nonaccumulation.',canonicalization='Actual PBPS consumer of shared canonical exponential product.',compressed_spine_delta=delta,reader_default_view='Full attributed statement/formula proof with adjacent folded exact Lean.',scope=boundary)
lc=copy.deepcopy(template['learning_contract']); lc['salvage'].update(reason='No mathematical proof attempt before seal. Syntax/name/private overlays independently reviewed; original negatives preserved.')
lc['parallelism'].update(decision='serial',direction_fingerprints=['actual-clock/zero-cap-or-positive-cap/Exp1-product/finite-horizon'],shared_verified_context_digest=seal['source_first_freeze']['RAW_sha256'])
lc['reader_backpressure'].update(source_expansion_nodes=['actual-recursion','actual-Exp1-inputs','zero-cap-stop','scaled-partial-sums','finite-horizon-escape','finite-index-set'],lean_expansion_nodes=[decl]); c['learning_contract']=lc
c['graph_contribution']=dict(lean_view='integration-node',overview_view='updated',functor_view='none-found',edge_semantics='formal-solid; overlays-dashed',color_semantics='evidence-status; library-scope',focus_targets=[decl],visual_review='Pending proof/publication/local graph checks.')
c['conceptual_mirror_audit']=dict(status='pending',discovery_ids=[],reason='Required before PROVED_LOCAL; no new transport claim from combining actual parents.')
write(Path('research-wiki/frontier-cells')/(cid+'.json'),c)
run('publication-packet-before-proof78',['tools/astis_publication.py','packet','--cell',cid])
run('frontier-before-proof78',['tools/astis_frontier_cells.py','check'])
print('SEALED and CLAIMED/EXPLORING; no theorem proof credit')
