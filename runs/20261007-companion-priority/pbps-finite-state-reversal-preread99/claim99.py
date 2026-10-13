"""Claim one reviewed actual finite-state reversal edge after the Statement Seal."""
from pathlib import Path
import copy,json,sys
root=Path.cwd();sys.path.insert(0,str(root/'tools'))
import astis_advance as adv
pre=Path(__file__).parent
load=lambda p:json.loads(Path(p).read_bytes())
seal=load(pre/'root.statement-seal99.json')
r=pre.parent/'pbps-actual-prescribed-state-reversal99';r.mkdir(exist_ok=False)
source=pre.parent/'pbps-actual-prescribed-gibbs-survival98/next-primary99-source-completion'
aid='ASTIS-SA-20261012-PBPSActualPrescribedStateReversal'
cid='ASTIS-SW-PBPS-actual-prescribed-state-reversal'
decl=seal['proposed_public_theorem'];module=decl.rsplit('.',1)[0]
lean=module.replace('.','/')+'.lean'
parents=['AutoSamplingTheory.ExampleCases.ProximalBPS.ActualPhaseReversalVolume.actual_phase_reversal_volume_laws','AutoSamplingTheory.ExampleCases.ProximalBPS.ActualEndpointTimeReversal.actual_endpoint_time_reversal_laws']
assert not any(s['advance_id']==aid for s in adv.current_advances().values())
assert [s['advance_id'] for s in adv.current_advances().values() if s['state']=='STABILIZING']==['ASTIS-SA-20261011-PBPSActualPrescribedPathDensity']
checks=['lake build '+module]
searched=['Samplinglib and pinned Mathlib/core, compatible library catalog: '+str(source/'retrieval99.native.json'),str(pre/'independent-header-math99/reuse-api-audit99.native.json'),str(pre/'independent-header-math99/topology99/source-topology-decision99.native.json'),str(pre/'independent-header-source99/header-source-decision99.native.json')]
old=load('research-wiki/frontier-cells/ASTIS-SW-PBPS-actual-prescribed-gibbs-survival.json')
cell=dict(schema_version=3,cell_id=cid,route='samplewiki-route',title='Actual PBPS finite prescribed-state reversal and incoming-rate product',mode='faithfulPaper',source_anchor=seal['source_anchor'],target_statement=Path(seal['header']['path']).read_text(encoding='utf8'),status='claimed',parents=parents,target_declarations=[decl],evidence=dict(owner=seal['owner'],statement_seal=str(pre/'root.statement-seal99.json'),focused_checks=checks,owned_files=[lean],truth_boundary=seal['truth_boundary']),shared_floor_audit=dict(searched=searched,classification='adapt',decision='adapt_existing',canonical_declaration=decl,canonical_shared_cell='',reason='Reuse actual96 algebra and97 tuple/terminal producers; derive finite intermediate state reversal internally.'),reuse_plan=dict(searched_existing=searched,reused_declarations=parents,planned_dependencies=[],new_shared_declarations=[],known_consumers=[],planned_consumers=[seal['consumer']],no_duplicate_wrapper=True,decision_reason='New intermediate actual state correspondence and incoming factor product, beyond existing terminal inversion; no new provider premises.'),reader_contract=copy.deepcopy(old['reader_contract']))
cell['consumers']=[seal['consumer']]
cell['blocked']=dict(status=False,reason='Sealed candidate; implementation is beginning. No mathematical blocker found.')
cell['statement_seal']=dict(evidence=str(pre/'root.statement-seal99.json'),source_revision=seal['source_revision'],statement_version=1,signature_digest=seal['header']['raw_sha256'],binder_audit=['Original six analytic assumptions and finite real Hilbert Borel typing; no excess.'],definition_kind=seal['definition_audit'])
cell['source_proof_coverage']=dict(source_graph=seal['source_graph']['path'],source_inventory=seal['source_coverage']['path'],coverage_report=str(pre/'independent-header-math99/topology99/source-topology-decision99.native.json'),coverage_status='Prospective source graph and exact candidate accepted; no Lean proof or compiled source coverage yet. EVENT99 internal; paired state identities and product public.')
cell['source_detail_audit']=dict(primary_edition=seal['source_revision'],primary_anchor=seal['source_anchor'],fidelity_boundary=seal['truth_boundary'],detail_status='omitted',gap='Printed reversal notation must distinguish incoming/post-event states at genuine jumps; finite index induction and product permutation are explicit internal obligations.',consulted=[dict(source='Pinned PBPS v1 and fixed core/Mathlib',anchor='Appendix A1 event convention, pre-A5 reversal, A5 and A8',hypothesis_adapter='Original literal state recursion; all zero cases retained; no right-continuous pointwise reversal premise.')])
cell['proof_digestion']=dict(existing_substrate=parents,bookkeeping=['Finite index and reversed-gap identities','Internal finite state induction','Fin.rev product permutation'],new_reusable=[],new_topology=seal['core_delta'])
cell['purification']=dict(status='pending',dead_code_audit='No implementation yet.',duplicate_semantics_audit='Independent local/Mathlib/compatible catalog retrieval complete.',canonicalization='Use public actual96/97 and core Fin/Mathlib product APIs; no private mangled cross-module calls.',compressed_spine_delta=seal['core_delta'],reader_default_view='Complete source-attributed statement and formula proof with adjacent folded Lean.',scope=seal['truth_boundary'])
lc=copy.deepcopy(old['learning_contract'])
lc['parallelism']=dict(decision='serial',direction_fingerprints=['actual-finite-state-reversal/zero-safe-bounce/incoming-product'],expected_information_gain='One implementation owner; separate source/header/topology reviews complete.',shared_verified_context_digest=seal['header']['raw_sha256'])
lc['reader_backpressure']=dict(purification_status='pending',exposition_seal_status='pending',exposition_evidence='',source_expansion_nodes=['A1.E5','A1.E8'],lean_expansion_nodes=[decl],assumptions_preserved=False,boundary_preserved=False)
cell['learning_contract']=lc
cell['graph_contribution']=dict(lean_view='integration-node',overview_view='no-change-with-reason',functor_view='none-found',edge_semantics='formal-solid; overlays-dashed',color_semantics='evidence-status; library-scope',focus_targets=[decl],visual_review='Pending implementation and publication.')
cell['conceptual_mirror_audit']=dict(status='none-found',reason='Source-specific finite PBPS event reversal; no new cross-domain formal adapter or mirror claimed.',discovery_ids=[])
cp=Path('research-wiki/frontier-cells')/(cid+'.json');assert not cp.exists()
cp.write_text(json.dumps(cell,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
p=adv.AdvanceProposal(advance_id=aid,task_id='ASTIS-SW-PBPS-2026',goal=seal['core_delta'],source_anchor=seal['source_anchor'],theorem_delta=seal['core_delta'],truth_boundary=seal['truth_boundary'],created_by=seal['owner'],dag_inputs=tuple(parents),proposed_files=(lean,),focused_checks=tuple(checks),modes=('faithfulPaper',),priority=100,frontier_cell=cid,target_declarations=(decl,))
adv.propose_advance(p)
evidence=dict(statement_seal=str(pre/'root.statement-seal99.json'),source_graph=seal['source_graph']['path'],owner_files=[lean],upstream98_remote_delivery='runs/20261007-companion-priority/pbps-actual-prescribed-gibbs-survival98/integration98/postpush-binding98.json')
for state in ['CLAIMED','EXPLORING']:adv.transition_advance(aid,state,worker_id=seal['owner'],modes=['faithfulPaper'],evidence=evidence)
(r/'claim.json').write_text(json.dumps(p.as_event(),ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
print('One99 owner claimed; original sole94 stabilization lane unchanged; no proof credit.')
