from pathlib import Path
import copy,datetime,hashlib,json,subprocess,sys
r=Path(__file__).parent
pre=Path('runs/20261007-companion-priority/pbps-process-regularity-preread82')
load=lambda p:json.loads(Path(p).read_bytes())
def pin(p):
 p=Path(p);b=p.read_bytes();return dict(path=p.as_posix(),RAW_bytes=len(b),RAW_sha256=hashlib.sha256(b).hexdigest())
def write(p,x):
 assert not p.exists(),p
 p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
header=r/'header82.proposed.lean';hh=pin(header)['RAW_sha256']
assert hh=='0333cf3e488effe1fa6f516553bb1e63a3bb650bfe09aca234ed20375cf85e64'
assert load(r/'independent-review-adoption82.json')['accepted']
assert load(r/'prospective-statement82.json')['proof_started'] is False
sys.path.insert(0,str(Path.cwd()/'tools'));import astis_advance as adv
aid='ASTIS-SA-20261010-PBPSActualSmallTimeContinuity';cid='ASTIS-SW-PBPS-actual-small-time-continuity';owner='companion_root_20261005'
assert adv.current_advances()['ASTIS-SA-20261010-PBPSActualPhysicalTimeMeasurability']['state']=='VERIFIED'
assert [a['advance_id'] for a in adv.current_advances().values() if a['state']=='STABILIZING']==['ASTIS-SA-20261005-SPHMCImplementedPhaseKernel']
file='AutoSamplingTheory/ExampleCases/ProximalBPS/ActualSmallTimeContinuity.lean';assert not Path(file).exists()
base='AutoSamplingTheory.ExampleCases.ProximalBPS.'
decl=base+'ActualSmallTimeContinuity.actual_small_time_stochastic_continuity'
parents=[base+'ActualPhysicalTimeMeasurability.actual_physical_time_measurable_phase',base+'ActualHazardClock.actual_integrated_hazard_clock_laws',base+'ActualHarmonicFlow.actual_harmonic_flow_laws','AutoSamplingTheory.TechnicalLemmas.Probability.UnitExponentialProduct.unit_exponential_product_laws']
delta='For the actual jointly measurable PBPS phase, derive measurable phase-flow defect probability <=1-exp(-Lambda_t), then fixed-parameter zero-time stochastic continuity at every positive norm threshold.'
anchor='Chen-Chewi-Lu-Zhang arXiv2609.06905v1 Appendix A.1 Ex22, A1.SS1.SSS0.Px1.p6.1-p6.2; A1.E1 integrated hazard and actual halfopen interpolation A1.SS1.p2.2. Bounded first-event/smalltime prerequisite only.'
boundary='Actual phase-flow defect bound and zero-time stochastic continuity for fixed V/alpha/beta/eta,y,xRef,z0 under actual exponential product, retaining all physical-phase realization clauses. No uniform parameter nullset/limit or arbitrary correlated substitution. Full L2 strong continuity/Markov/restart/semigroup/invariance/hypocoercivity/implementation/main/cost/composition and actual reader visual/main/PURIFIED/live remain OPEN.'
seal=dict(status='SEALED_BEFORE_PROOF_AFTER_INDEPENDENT_HEADER_MATH_SOURCE_AND_TOPOLOGY_REVIEW',sealed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),statement_version=1,header=pin(header),expanded_literal_Prop=header.read_text(encoding='utf8').split('private def ',1)[1].split('\nend\n',1)[0],public_theorem=decl,source_first_freeze=pin(pre/'source_freeze82.raw-manifest.json'),source_graph=pin(pre/'source_proof_graph82.json'),source_inventory=pin(pre/'source_inventory82.json'),reviewed_title_overlay=pin(r/'independent-review-adoption82.json'),reuse_search=pin(r/'retrieval82/reuse-decision82.json'),toolchain=pin('lean-toolchain'),lake_manifest=pin('lake-manifest.json'),truth_boundary=boundary,proof_BODY_created=False)
write(r/'root.statement-seal82.json',seal)
proposal=adv.AdvanceProposal(advance_id=aid,task_id='ASTIS-SW-PBPS-2026',goal=delta,source_anchor=anchor,theorem_delta=delta,truth_boundary=boundary,created_by=owner,dag_inputs=tuple(parents),proposed_files=(file,),focused_checks=('lake build AutoSamplingTheory.ExampleCases.ProximalBPS.ActualSmallTimeContinuity',),modes=('faithfulPaper',),priority=100,frontier_cell=cid,target_declarations=(decl,))
adv.propose_advance(proposal)
adv.transition_advance(aid,'CLAIMED',worker_id=owner,evidence=dict(statement_seal=(r/'root.statement-seal82.json').as_posix(),owned_files=[file]))
adv.transition_advance(aid,'EXPLORING',worker_id=owner,evidence=dict(route='Actual80 realization; actual75 firstwait survival transported through actual input; first-arc defect inclusion; continuous Phi and Lambda plus probability squeeze.',truth_boundary=boundary))
write(r/'claim.json',proposal.as_event())
c=copy.deepcopy(load('research-wiki/frontier-cells/ASTIS-SW-PBPS-actual-physical-time-measurability.json'))
c.update(cell_id=cid,title='Actual PBPS phase-flow defect bound and zero-time stochastic continuity',source_anchor=anchor,target_statement=header.read_text(encoding='utf8'),status='claimed',parents=parents,consumers=['Source Appendix A.1 Ex22 pointwise small-time ingredient; full L2 continuity separately requires invariant law, contractivity, domination and density.'],source_targets=[decl],blocked=dict(status=False,reason='Independent exact header/math/source and distinct topology accepted; root sole writer, no proof credit.'))
c['evidence']=dict(substantive_advance=aid,statement_seal=(r/'root.statement-seal82.json').as_posix(),focused_checks=[],owned_files=[file],truth_boundary=boundary)
search=['Samplinglib actual80/75/73/UnitExponentialProduct and all active/shared cells; module card and shared foundations searched.','Pinned Mathlib probability pushforward/real complement/monotonicity and continuity/squeeze.','Pinned compatible upstream indexes searched; no external port used.']
c['shared_floor_audit']=dict(searched=search,classification='adapt',decision='adapt_existing',canonical_declaration=decl,canonical_shared_cell='',reason='Source-specific actual process probability consumer of existing generic Mathlib floors; no shared duplicate or assumed first-event certificate.')
c['reuse_plan']=dict(searched_existing=search,reused_declarations=parents,new_shared_declarations=[],known_consumers=[],planned_consumers=c['consumers'],no_duplicate_wrapper=True,decision_reason=c['shared_floor_audit']['reason'])
c['statement_seal']=dict(evidence=(r/'root.statement-seal82.json').as_posix(),source_revision='arXiv2609.06905v1/Lean4.33.0/Mathlibdb584cd6d46c92f209a44c0f1c829460d327499d',statement_version=1,signature_digest=hh,binder_audit=['Original six analytic source standing binders retained literally; no producer or probability estimate premise.'],definition_kind='Literal actual eleven definitions; same full joint Borel Z/covered/fallback/common-AE semantics as actual80. Product phase norm gives finite-dimensional phase topology.')
c['source_proof_coverage']=dict(source_graph=(pre/'source_proof_graph82.json').as_posix(),source_inventory=(pre/'source_inventory82.json').as_posix(),coverage_report=(pre/'header-source-review82/header-source-review82.result.json').as_posix(),reviewed_adapter_overlay=(r/'independent-review-adoption82.json').as_posix(),coverage_status='Independent prospective source inventory36/node13/edge20 and distinct topology review accepted with title-only live-record correction. BODY review still OPEN.')
c['source_detail_audit']=dict(primary_edition=c['statement_seal']['source_revision'],primary_anchor=anchor,fidelity_boundary=boundary,detail_status='omitted',gap='Source suppresses explicit measurable realization and actual-input phase-flow defect inclusion; full source L2 continuity is outside this bounded prerequisite.',consulted=[dict(source='Pinned primary Ex22 and compiled actual80/75/73; fixed Mathlib',anchor='Ex22, A1.E1 and A1.SS1.p2.2',hypothesis_adapter='All six source standing analytic hypotheses retained, first-event law derived from existing producer, not added as premise.')])
c['proof_digestion']=dict(existing_substrate=parents,bookkeeping=['First record live at0; top wait keeps last live physical arc; exact firstwait law from actual clocks.','At each positive threshold the norm-tail is eventually contained in the measurable phase-flow defect.'],new_reusable=[],new_topology=delta)
c['purification']=dict(status='pending',dead_code_audit='Pending proof',duplicate_semantics_audit='Actual80 constructs phase but no actual short-time probability estimate.',canonicalization='Reuse existing generic floors and actual process producers.',compressed_spine_delta=delta,reader_default_view='Full attributed statement and formula proof with adjacent folded exact Lean.',scope=boundary)
c['learning_contract']['parallelism'].update(decision='serial',direction_fingerprints=['actual-firstwait/first-arc/defect-probability/smalltime-squeeze'],shared_verified_context_digest=seal['source_first_freeze']['RAW_sha256'])
c['learning_contract']['process_memory_ids']=['ASTIS-DISC-20261010-ActualWaitCompositionElaboration','ASTIS-DISC-20261009-DependentPropStatementStaging']
c['learning_contract']['salvage'].update(reason='No proof attempt before exact independent header/source/topology seal.')
c['learning_contract']['reader_backpressure'].update(purification_status='pending',exposition_seal_status='pending',exposition_evidence='',source_expansion_nodes=['actual-firstwait','first-live-arc','phase-flow-defect','hazard-continuity','norm-tail-squeeze'],lean_expansion_nodes=[decl])
c['graph_contribution'].update(focus_targets=[decl],lean_view='theorem-edge',visual_review='Pending proof/publication/affected graph and page acceptance.')
c['conceptual_mirror_audit']=dict(status='pending',discovery_ids=[],reason='Required before PROVED_LOCAL; no new bridge claimed.')
write(Path('research-wiki/frontier-cells')/(cid+'.json'),c)
for label,args in [('publication-packet-before-proof82',['tools/astis_publication.py','packet','--cell',cid]),('frontier-before-proof82',['tools/astis_frontier_cells.py','check'])]:
 p=subprocess.run([sys.executable,'-X','utf8',*args],capture_output=True)
 (r/(label+'.stdout.json')).write_bytes(p.stdout);(r/(label+'.stderr.log')).write_bytes(p.stderr)
 write(r/(label+'.receipt.json'),dict(exit_code=p.returncode,terminal_closed=True));assert p.returncode==0,p.stdout.decode('utf8',errors='replace')[-5000:]
print('82 sealed and claimed; no proof credit')
