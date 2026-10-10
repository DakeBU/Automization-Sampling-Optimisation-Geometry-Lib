from pathlib import Path
import copy,hashlib,json,os,subprocess,sys
root=Path.cwd();base=Path('runs/20261007-companion-priority')
pre=base/'pbps-reflection-rotation-preproof69';r=base/'pbps-reflection-intertwining69';prior=base/'pbps-sharp-energy68'
load=lambda p:json.loads(Path(p).read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest()
def w(p,x):
 p=Path(p);assert not p.exists(),p
 p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
seal=load(pre/'root.statement-seal69.json')
assert seal['status']=='STATEMENT69_SEALED_NOT_CLAIMED_NOT_PROVED'
assert load(prior/'root.repository68.adoption.json')['accepted_scoped_aggregate']
assert load(prior/'integration.notes.json')['registry_count']==516
for key in ['statement_seal','private_literal_Prop','public_original_caller','source_first_adoption','independent_header_admission']:
 row=seal[key];assert sha(Path(row['path']).read_bytes())==row['RAW_sha256']
assert load(pre/'root.library-retrieval69.json')['no_new_shared_leaf_claim']
assert load(pre/'root.library-retrieval69.extension.json')['same_U_identity_required']
reflection_parent='ASTIS-SW-PBPS-reflection-l2-blocks'
assert load(Path('research-wiki/frontier-cells')/(reflection_parent+'.json'))['status']=='independently_verified'
assert load(pre/'root.primary69.adoption.json')['source_items']==419
owner='companion_root_20261005';aid='ASTIS-SA-20261009-PBPSActualReflectionIntertwining'
parent='ASTIS-SW-PBPS-actual-root-inverse-commutation';cid='ASTIS-SW-PBPS-actual-reflection-intertwining'
files=[seal['planned_file']];names=[seal['exact_target']]
assert all(not Path(p).exists() for p in files)
source='PBPS2609.06905v1 Appendix B1/B3, source graph P11 actual micro intertwining, B21 rotation A2.Ex15.m2 and B4 A2.SS3.p8.m10; exact source graph independently reconstructed over419 math items.'
delta=seal['exact_delta'];boundary=seal['remaining_truth_boundary']
r.mkdir(exist_ok=False);sys.path.insert(0,str(root/'tools'));import astis_advance as adv
ledger=Path('runs/substantive_advances.jsonl');before=ledger.read_bytes()
w(r/'ledger.before69.pin.json',dict(path=ledger.as_posix(),raw_bytes=len(before),raw_sha256=sha(before)))
p=adv.AdvanceProposal(advance_id=aid,task_id='ASTIS-SW-PBPS-2026',goal=delta,source_anchor=source,theorem_delta=delta,truth_boundary=boundary,created_by=owner,dag_inputs=(parent,reflection_parent),proposed_files=tuple(files),focused_checks=('lake build AutoSamplingTheory.ExampleCases.ProximalBPS.ReflectionIntertwining',),modes=('faithfulPaper',),priority=100,frontier_cell=cid,target_declarations=tuple(names))
adv.propose_advance(p)
adv.transition_advance(aid,'CLAIMED',worker_id=owner,evidence=dict(statement_seal=(pre/'root.statement-seal69.json').as_posix(),owned_files=files))
adv.transition_advance(aid,'EXPLORING',worker_id=owner,evidence=dict(route='Actual involution block cancellation, SAME centered adjoint/polar and inverse commutation',truth_boundary=boundary))
after=ledger.read_bytes();assert after[:len(before)]==before
(r/'ledger.claim69.append.exactraw.jsonl').write_bytes(after[len(before):]);w(r/'claim.json',p.as_event())
c=copy.deepcopy(load(Path('research-wiki/frontier-cells')/(parent+'.json')))
assert c['status']=='independently_verified'
header=Path(seal['statement_seal']['path']).read_text(encoding='utf-8');signature=header[header.index('theorem '):]
searched=['Samplinglib Analysis module card, ReflectionL2, AmbientAdjointCorrector and ActualRootCommutation searched; existing theorem-local block algebra cannot be invoked as an exported declaration or used to replace SAME U. Fixed Mathlib adjoint_comp/adjoint inner/linear map APIs inspected. Exact retrieval69 snapshots retained; no SLT/OpenAI/floating source.']
reused=[seal['real_parent'],'AutoSamplingTheory.ExampleCases.ProximalBPS.ReflectionL2.actual_reflection_block_identities']
c.update(cell_id=cid,route='samplewiki-route',title='Actual PBPS reflection intertwining on the full conditional-complement space',source_anchor=source,target_statement=signature,status='claimed',parents=[parent,reflection_parent],consumers=seal['source_consumers'],blocked=dict(status=False,reason='Independent source-first header and type formation sealed; target not yet proved.'),evidence=dict(substantive_advance=aid,statement_seal=(pre/'root.statement-seal69.json').as_posix(),focused_checks=[],owned_files=files,truth_boundary=boundary),source_targets=names)
c['shared_floor_audit']=dict(searched=searched,classification='adapt',decision='adapt_existing',canonical_declaration=reused[0],canonical_shared_cell=parent,reason='Extend SAME actual witnesses with the missing full micro intertwining; no generic duplicate or sharp-energy dependency.')
c['reuse_plan']=dict(searched_existing=searched,reused_declarations=reused,new_shared_declarations=[],known_consumers=seal['source_consumers'],planned_consumers=seal['source_consumers'],no_duplicate_wrapper=True,decision_reason=c['shared_floor_audit']['reason'])
c['statement_seal']=dict(evidence=(pre/'root.statement-seal69.json').as_posix(),source_revision='2609.06905v1/Lean4.33.0/Mathlibdb584cd6',statement_version=1,signature_digest=sha(signature.encode()),binder_audit=(pre/'independent-header-source69/binder-and-definition-audit.json').as_posix(),definition_kind='One full literal Prop, unchanged original callers and all SAME12 actual witnesses; no additional premise.')
c['source_proof_coverage']=dict(source_graph=(pre/'independent-primary69/source-proof-graph.json').as_posix(),source_inventory=(pre/'independent-primary69/source-coverage-inventory.json').as_posix(),coverage_report=(pre/'root.header69.adoption.json').as_posix(),coverage_status='419/419 source math items over7 RAW regions;22 source graph nodes/49 edges; independent source-only graph then header math/source reviews before proof search.')
c['source_detail_audit'].update(primary_anchor=source,fidelity_boundary=boundary,gap='Full actual V0*D=-A0 V0* not yet proved.',source_preread=c['source_proof_coverage']['source_graph'],consulted=[dict(source='PBPSv1 pinned primary and fixed Mathlib',anchor='B1; B21; B4',hypothesis_adapter='All micro inputs in kerP; no onto-V assumption; same reflection and centered inverse.',expanded_binder_audit=(pre/'root.header69.adoption.json').as_posix())])
c['proof_digestion']=dict(existing_substrate=reused,bookkeeping=['D=R U inclusion on SAME kerP; all original callers unchanged.'],new_reusable=[],new_topology=delta)
c['purification']=dict(status='pending',dead_code_audit='One actual integration theorem planned, no private provider or wrapper consumer.',duplicate_semantics_audit='Reuse original-input67 and fixed canonical objects.',canonicalization='Same actual PBPS reflection compression.',compressed_spine_delta=delta,reader_default_view='Complete attributed formulas with adjacent exact folded Lean.',scope=boundary)
lc=c['learning_contract'];lc['failure_class']='IMPLEMENTATION_FAILED'
lc['salvage']=dict(required=True,status='completed',reason='Same original full Prop header/type/source accepted before search; no69 proof failures yet.',promoted_fragments=[],discarded_fragments=[])
lc['parallelism'].update(decision='serial',direction_fingerprints=['same-actual-reflection/full-micro-intertwining'],shared_verified_context_digest=load(base/'pbps-root-commutation67/root.exact-verification67.adoption.json')['native_whole_logical_run_sha256'],expected_information_gain='One proof writer; independent math, blind decoder and anti-anchored source review.')
lc['reader_backpressure'].update(purification_status='pending',exposition_seal_status='pending',exposition_evidence='',lean_expansion_nodes=names,source_expansion_nodes=['actual-reflection','conditional-projection','full-micro-space','same-centered-inverse','same-polar','P11-intertwining','B21-pending','B4-pending'])
c['graph_contribution'].update(lean_view='integration-node',overview_view='updated',functor_view='none-found',focus_targets=names,visual_review='Pending69 proof and independent review; no graph extension blocks mathematics.')
c['conceptual_mirror_audit']=dict(status='pending',discovery_ids=[],reason='Audit before PROVED_LOCAL; no transport certificate claimed.')
w(Path('research-wiki/frontier-cells')/(cid+'.json'),c)
w(r/'preproof-admission.json',dict(status='CLAIMED_EXPLORING_NOT_PROVED',actual_root_pid=os.getpid(),checked_parent=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),statement_seal=(pre/'root.statement-seal69.json').as_posix(),theorem_delta=delta,truth_boundary=boundary,active_cells=[cid],production_declarations=names,no_sharp_energy68_proof_parent=True))
print(aid,'EXPLORING; one actual theorem, same witnesses and genuine source consumers; no proof credit.')
