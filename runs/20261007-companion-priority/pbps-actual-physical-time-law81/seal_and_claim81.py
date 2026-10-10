from pathlib import Path
import copy,datetime,hashlib,json,subprocess,sys
r=Path('runs/20261007-companion-priority/pbps-actual-physical-time-law81');pre=Path('runs/20261007-companion-priority/pbps-physical-time-law-preread81')
load=lambda p:json.loads(Path(p).read_bytes())
def pin(p):
 p=Path(p);b=p.read_bytes();return dict(path=p.as_posix(),RAW_bytes=len(b),RAW_sha256=hashlib.sha256(b).hexdigest())
def write(p,x):
 assert not p.exists(),p
 p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
header=r/'header81.proposed.lean';hh=pin(header)['RAW_sha256']
assert hh=='c3d1ad6107ad0aa812a99461d7dc48720ba83709104f699a908a77a89bec1e76'
assert load(r/'independent-review-adoption81.json')['accepted']
assert load(r/'prospective-statement81.json')['proof_started'] is False
assert load(r/'header-review81/decision81.json')['status']=='ACCEPTED_PROSPECTIVE_HEADER_NO_REPAIR'
sr=load(pre/'header-source-review81/header-source-review81.result.json')
assert not sr['blocking_deltas'] and not sr['required_mathematical_repairs']
sys.path.insert(0,str(Path.cwd()/'tools'));import astis_advance as adv
owner='companion_root_20261005';aid='ASTIS-SA-20261010-PBPSIdealHalfTurnKernel';cid='ASTIS-SW-PBPS-ideal-half-turn-kernel'
assert adv.current_advances()['ASTIS-SA-20261010-PBPSActualPhysicalTimeMeasurability']['state']=='VERIFIED'
assert [a['advance_id'] for a in adv.current_advances().values() if a['state']=='STABILIZING']==['ASTIS-SA-20261005-SPHMCImplementedPhaseKernel']
file='AutoSamplingTheory/ExampleCases/ProximalBPS/IdealHalfTurnKernel.lean';assert not Path(file).exists()
base='AutoSamplingTheory.ExampleCases.ProximalBPS.'
decl=base+'IdealHalfTurnKernel.ideal_half_turn_returned_position_kernel'
parents=[base+'ActualPhysicalTimeMeasurability.actual_physical_time_measurable_phase',base+'ActualFiniteJumpRecursion.actual_fixed_reference_finite_jump_recursion',base+'ActualHarmonicFlow.actual_harmonic_flow_laws',base+'ActualEventTimeNonaccumulation.actual_fixed_reference_event_time_nonaccumulation',base+'GibbsAugmentation.normalized_augmentation_density','AutoSamplingTheory.TechnicalLemmas.Probability.GaussianConditionalKernel.exists_tilted_isCondKernel','AutoSamplingTheory.TechnicalLemmas.Probability.UnitExponentialProduct.unit_exponential_product_laws']
delta='Construct the ideal Algorithm1 returned-position probability kernel at pi, with exact derived conditional reference q_y, independent Gaussian momentum and actual exponential clocks; derive initial phase law and actual live-arc agreement under this product law.'
anchor='Chen-Chewi-Lu-Zhang arXiv2609.06905v1 Algorithm1, (2.8), AppendixA.1 A1.SS2.p3.1-p4.1 ideal H_y returned-position law; literal actual recurrence and original six analytic hypotheses.'
boundary='Ideal exact-reference probability kernel at pi and product-input AE actual origin/terminal arc only. Fixed V/alpha/beta/eta; no arbitrary correlated input substitution. Full random all-time path law/version uniqueness, implementation/reference approximation/oracle costs, phase Markov/semigroup/invariance/reversibility/hypocoercivity/main/composition and reader visual/main/PURIFIED/live remain OPEN.'
seal=dict(status='SEALED_BEFORE_PROOF_AFTER_INDEPENDENT_EXACT_HEADER_REVIEW',sealed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),statement_version=1,header=pin(header),expanded_literal_Prop=header.read_text(encoding='utf8').split('private def ',1)[1].split('\nend\n',1)[0],public_theorem=decl,source_first_freeze=pin(pre/'source_freeze81.complete-raw-manifest.json'),source_graph=pin(pre/'source_proof_graph81.json'),source_inventory=pin(pre/'source_inventory81.json'),source_topology_clarification=pin(pre/'source_scope_clarification81.json'),exact_header_review=pin(r/'independent-review-adoption81.json'),reuse_search=pin(r/'retrieval81/reuse-decision81.json'),toolchain=pin('lean-toolchain'),lake_manifest=pin('lake-manifest.json'),truth_boundary=boundary,proof_BODY_created=False)
write(r/'root.statement-seal81.json',seal)
proposal=adv.AdvanceProposal(advance_id=aid,task_id='ASTIS-SW-PBPS-2026',goal=delta,source_anchor=anchor,theorem_delta=delta,truth_boundary=boundary,created_by=owner,dag_inputs=tuple(parents),proposed_files=(file,),focused_checks=('lake build AutoSamplingTheory.ExampleCases.ProximalBPS.IdealHalfTurnKernel',),modes=('faithfulPaper',),priority=100,frontier_cell=cid,target_declarations=(decl,))
adv.propose_advance(proposal)
adv.transition_advance(aid,'CLAIMED',worker_id=owner,evidence=dict(statement_seal=(r/'root.statement-seal81.json').as_posix(),owned_files=[file]))
adv.transition_advance(aid,'EXPLORING',worker_id=owner,evidence=dict(route='Canonical Gibbs/conditional kernel; actual80 jointly measurable phase; measurable fixed-time live-arc relation with product Fubini; kernel product/map.',truth_boundary=boundary))
write(r/'claim.json',proposal.as_event())
c=copy.deepcopy(load('research-wiki/frontier-cells/ASTIS-SW-PBPS-actual-physical-time-measurability.json'))
c.update(cell_id=cid,title='Ideal PBPS half-turn returned-position probability kernel',source_anchor=anchor,target_statement=header.read_text(encoding='utf8'),status='claimed',parents=parents,consumers=['Source AppendixA.1 ideal H_y mixing/invariance analysis; implementation comparison and PBPS/SPHMC composition require separate adapters.'],source_targets=[decl],blocked=dict(status=False,reason='Exact prospective header independently reviewed and sealed; root sole writer.'))
c['evidence']=dict(substantive_advance=aid,statement_seal=(r/'root.statement-seal81.json').as_posix(),focused_checks=[],owned_files=[file],truth_boundary=boundary)
search=['Samplinglib actual80/76/75/73/77 and canonical GibbsAugmentation/GaussianConditionalKernel; current shared cells and module cards inspected.','Pinned Mathlib kernel products/maps/comaps, tilted_tilted, product AE and product marginals.','Bounded compatible upstream index search empty; no port used.']
c['shared_floor_audit']=dict(searched=search,classification='adapt',decision='adapt_existing',canonical_declaration=decl,canonical_shared_cell='',reason='Generic probability kernel floor already Mathlib; construct source H_y using actual recurrence with genuine normalized reference and initialization/product-AE proof, no assumed map/law/certificate.')
c['reuse_plan']=dict(searched_existing=search,reused_declarations=parents,new_shared_declarations=[],known_consumers=[],planned_consumers=c['consumers'],no_duplicate_wrapper=True,decision_reason=c['shared_floor_audit']['reason'])
c['statement_seal']=dict(evidence=(r/'root.statement-seal81.json').as_posix(),source_revision='arXiv2609.06905v1/Lean4.33.0/Mathlibdb584cd6d46c92f209a44c0f1c829460d327499d',statement_version=1,signature_digest=hh,binder_audit=['Six original analytic binders: hAlpha, hAlphaBeta, C2 V, two-sided Hessian, positive eta, beta eta <=1; no producer premise.'],definition_kind='Literal actual recurrence, exact normalized q_y and independent product q_y x Gaussian x exponential clocks; ideal H_y not implemented sampler.')
c['source_proof_coverage']=dict(source_graph=(pre/'source_proof_graph81.json').as_posix(),source_inventory=(pre/'source_inventory81.json').as_posix(),coverage_report=(pre/'header-source-review81/header-source-review81.result.json').as_posix(),reviewed_adapter_overlay=(pre/'source_scope_clarification81.json').as_posix(),coverage_status='Prospective bounded refinement source-reviewed; BODY/final fresh source coverage OPEN.')
c['source_detail_audit'].update(primary_anchor=anchor,fidelity_boundary=boundary,gap='Source suppresses normalized reference-kernel and product-measurable realization details; fixed-time ideal law adapter only.')
c['proof_digestion']=dict(existing_substrate=parents,bookkeeping=['Countable live-arc predicate measurable before Fubini; initialization equality under actual product law.','Exact q_y is normalized internally, not q-hat or externally assumed.'],new_reusable=[],new_topology=delta)
c['purification'].update(status='pending',dead_code_audit='Pending proof',duplicate_semantics_audit='Actual80 phase is not a returned-position law/kernel.',compressed_spine_delta=delta,scope=boundary)
c['learning_contract']['parallelism'].update(decision='serial',direction_fingerprints=['ideal-reference/kernel-product-map/fixed-time-AE/initial-law'],shared_verified_context_digest=seal['source_first_freeze']['RAW_sha256'])
c['learning_contract']['salvage'].update(reason='No proof attempt before exact independent header seal.')
c['learning_contract']['reader_backpressure'].update(purification_status='pending',exposition_seal_status='pending',exposition_evidence='',source_expansion_nodes=['actual-conditional-reference','independent-input-law','measurable-finite-time-relation','product-Fubini','terminal-kernel','phase-initialization-law'],lean_expansion_nodes=[decl])
c['graph_contribution'].update(focus_targets=[decl],visual_review='Pending proof/publication/affected graph and page acceptance.')
c['conceptual_mirror_audit']=dict(status='pending',discovery_ids=[],reason='Audit required before PROVED_LOCAL; no new bridge asserted.')
write(Path('research-wiki/frontier-cells')/(cid+'.json'),c)
for label,args in [('publication-packet-before-proof81',['tools/astis_publication.py','packet','--cell',cid]),('frontier-before-proof81',['tools/astis_frontier_cells.py','check'])]:
 p=subprocess.run([sys.executable,'-X','utf8',*args],capture_output=True)
 (r/(label+'.stdout.json')).write_bytes(p.stdout);(r/(label+'.stderr.log')).write_bytes(p.stderr)
 write(r/(label+'.receipt.json'),dict(exit_code=p.returncode,terminal_closed=True));assert p.returncode==0,p.stdout.decode('utf8',errors='replace')[-5000:]
print('81 sealed and claimed; no proof credit')
