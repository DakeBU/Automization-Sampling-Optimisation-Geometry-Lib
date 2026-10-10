"""Seal the independently reviewed exact header, then claim one actual SAU."""
from pathlib import Path
import copy,datetime,hashlib,json,os,subprocess,sys
r=Path('runs/20261007-companion-priority/pbps-actual-physical-time-measurability80')
pre=Path('runs/20261007-companion-priority/pbps-physical-time-measurability-preread80')
load=lambda p:json.loads(Path(p).read_bytes())
def pin(p):
 p=Path(p);b=p.read_bytes();return dict(path=p.as_posix(),RAW_bytes=len(b),RAW_sha256=hashlib.sha256(b).hexdigest())
def write(p,x):
 p=Path(p);assert not p.exists(),p;p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
def check(label,args):
 p=subprocess.run([sys.executable,'-X','utf8',*args],capture_output=True)
 (r/(label+'.stdout.json')).write_bytes(p.stdout);(r/(label+'.stderr.log')).write_bytes(p.stderr)
 write(r/(label+'.receipt.json'),dict(exit_code=p.returncode,terminal_closed=True));assert p.returncode==0,p.stdout.decode('utf8',errors='replace')[-8000:]
header=r/'header80.proposed.lean'
assert pin(header)['RAW_sha256']=='1b51f58a987d8b59bcb1b5280a8817af984d7fad4b09962ad8a229198f9f5215'
# Root writes independent-review-adoption80.json only after checking native artifacts.
adopt=load(r/'independent-review-adoption80.json');assert adopt['accepted'] and adopt['exact_header_RAW_sha256']==pin(header)['RAW_sha256']
assert load(r/'prospective-inputs80.json')['proof_BODY_created'] is False
sys.path.insert(0,str(Path.cwd()/'tools'));import astis_advance as adv
owner='companion_root_20261005';aid='ASTIS-SA-20261010-PBPSActualPhysicalTimeMeasurability';cid='ASTIS-SW-PBPS-actual-physical-time-measurability'
assert adv.current_advances()['ASTIS-SA-20261010-PBPSActualPhysicalTimeCover']['state']=='VERIFIED'
assert [a['advance_id'] for a in adv.current_advances().values() if a['state']=='STABILIZING']==['ASTIS-SA-20261005-SPHMCImplementedPhaseKernel']
file='AutoSamplingTheory/ExampleCases/ProximalBPS/ActualPhysicalTimeMeasurability.lean';assert not Path(file).exists()
decl='AutoSamplingTheory.ExampleCases.ProximalBPS.ActualPhysicalTimeMeasurability.actual_physical_time_measurable_phase'
parents=['AutoSamplingTheory.ExampleCases.ProximalBPS.ActualFiniteJumpRecursion.actual_fixed_reference_finite_jump_recursion','AutoSamplingTheory.ExampleCases.ProximalBPS.ActualHarmonicFlow.actual_harmonic_flow_laws','AutoSamplingTheory.ExampleCases.ProximalBPS.ActualPhysicalTimeCover.actual_fixed_reference_physical_time_cover','AutoSamplingTheory.TechnicalLemmas.Probability.UnitExponentialProduct.unit_exponential_product_laws']
delta='Construct a total phase jointly Borel in y/reference/initial phase/finite physical time/actual threshold sample, exactly interpolate each actual covered live arc, explicitly take initial phase on uncovered pairs, and prove per-parameter common-AE all-time actual arc realization and initialization.'
anchor='Chen-Chewi-Lu-Zhang arXiv2609.06905v1 Algorithm1 and AppendixA1 A.2/A1.E2/A1.SS1.p2.2 between-jump prescription; original six analytic conditions; actual source implicit measurable realization adapter.'
boundary='Actual total jointly measurable finite-physical-time representative and common-AE all-time actual arc agreement/initialization per fixed parameter triple. V/alpha/beta/eta fixed. Uncovered fallback is explicit ASTIS convention. No uniform AE all parameters or arbitrary correlated random parameter substitution; path regularity/adaptedness/Markov/invariance/laws/kernel/hypocoercivity/full sampler errors/cost/composition, full Exposition Seal/main merge/PURIFIED/live/whole Goal remain open.'
seal=dict(status='SEALED_BEFORE_PROOF_AFTER_INDEPENDENT_EXACT_HEADER_REVIEW',sealed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),actual_root_PID=os.getpid(),statement_version=1,header=pin(header),expanded_literal_Prop=header.read_text(encoding='utf8').split('private def ',1)[1].split('\nend\n',1)[0],public_theorem=decl,source_first_freeze=pin(pre/'source-freeze80.json'),source_topology_clarification=pin(pre/'source-topology-clarification80.json'),independent_scope=pin(pre/'independent-scope-review80/review-manifest80-final.json'),exact_header_review=pin(r/'independent-review-adoption80.json'),reuse_search=pin(r/'retrieval80/reuse-decision80.json'),toolchain=pin('lean-toolchain'),lake_manifest=pin('lake-manifest.json'),truth_boundary=boundary,proof_BODY_created=False)
write(r/'root.statement-seal80.json',seal)
proposal=adv.AdvanceProposal(advance_id=aid,task_id='ASTIS-SW-PBPS-2026',goal=delta,source_anchor=anchor,theorem_delta=delta,truth_boundary=boundary,created_by=owner,dag_inputs=tuple(parents),proposed_files=(file,),focused_checks=('lake build AutoSamplingTheory.ExampleCases.ProximalBPS.ActualPhysicalTimeMeasurability',),modes=('faithfulPaper',),priority=100,frontier_cell=cid,target_declarations=(decl,))
adv.propose_advance(proposal);adv.transition_advance(aid,'CLAIMED',worker_id=owner,evidence=dict(statement_seal=(r/'root.statement-seal80.json').as_posix(),owned_files=[file]));adv.transition_advance(aid,'EXPLORING',worker_id=owner,evidence=dict(route='Countable disjoint measurable actual intervals and measurable harmonic branch gluing, with explicit uncovered complement; actual79 common-AE cover and77 positive inputs for origin.',truth_boundary=boundary));write(r/'claim.json',proposal.as_event())
c=copy.deepcopy(load('research-wiki/frontier-cells/ASTIS-SW-PBPS-actual-physical-time-cover.json'))
c.update(cell_id=cid,title='Actual PBPS jointly measurable physical-time phase',source_anchor=anchor,target_statement=header.read_text(encoding='utf8'),status='claimed',parents=parents,consumers=['Algorithm1 later actual finite-time evaluation with conditional random reference/initial phase and horizon; law/independence adapters not yet proved.'],source_targets=[decl],blocked=dict(status=False,reason='One independently reviewed sealed statement; sole writer root.'))
c['evidence']=dict(substantive_advance=aid,statement_seal=(r/'root.statement-seal80.json').as_posix(),focused_checks=[],owned_files=[file],truth_boundary=boundary)
search=['Samplinglib actual76 joint record/clocks, actual73 joint harmonic flow, actual79 common-AE interval cover and77 canonical actual thresholds/support; module cards and current Frontier Cells inspected, no existing actual physical-time phase representative.','Pinned Mathlib countable exists_measurable_piecewise, Sum elimination measurability, order comparison, NNReal subtraction and coordinate clamp.','Compatible upstream indexes inspected: LMC/SALD interpolation and law references are distinct; no OAI/SLT transplant used.']
c['shared_floor_audit']=dict(searched=search,classification='missing',decision='new_route_local',canonical_declaration=decl,canonical_shared_cell='',reason='Generic measurable gluing already exists in pinned Mathlib. New theorem realizes the actual PBPS source recurrence, includes genuine measurable witness and actual-input AE origin/all-time semantics; no supplied selector/nonexplosion premise.')
c['reuse_plan']=dict(searched_existing=search,reused_declarations=parents,new_shared_declarations=[],known_consumers=[],planned_consumers=c['consumers'],no_duplicate_wrapper=True,decision_reason=c['shared_floor_audit']['reason'])
c['statement_seal']=dict(evidence=(r/'root.statement-seal80.json').as_posix(),source_revision='arXiv2609.06905v1/Lean4.33.0/Mathlibdb584cd6d46c92f209a44c0f1c829460d327499d',statement_version=1,signature_digest=pin(header)['RAW_sha256'],binder_audit=load(pre/'source-freeze80.json')['binders'],definition_kind='Original six analytic binders and eleven literal actual definitions. Joint parameter domain is separately reviewed source-implicit adapter; no extra source premise.')
c['source_proof_coverage']=dict(source_graph=(pre/'source-freeze80.json').as_posix(),source_inventory=(pre/'source-freeze80.json').as_posix(),coverage_report=(pre/'independent-scope-review80/independent-source-topology-review80.json').as_posix(),reviewed_adapter_overlay=(pre/'source-topology-clarification80.json').as_posix(),coverage_status='Prospective scoped source topology reviewed; implementation and final fresh source coverage OPEN.')
c['source_detail_audit'].update(primary_anchor=anchor,fidelity_boundary=boundary,gap='Source suppresses measurable assembly/exceptional representatives. ASTIS finite-time realization is current delta; process regularity/Markov/laws remain separate.')
c['proof_digestion']=dict(existing_substrate=parents,bookkeeping=['All-input interval measurability and monotone disjointness are deterministic; actual coverage is common-AE per parameter.','Last live infinite-wait arc is covered, not fallback; actual positivity required for source origin.'],new_reusable=[],new_topology=delta)
c['purification'].update(status='pending',dead_code_audit='Pending proof',duplicate_semantics_audit='Actual79 only proves interval/live-record coverage; no measurable phase witness.',compressed_spine_delta=delta,scope=boundary)
c['learning_contract']['parallelism'].update(decision='serial',direction_fingerprints=['actual-clock/countable-measurable-gluing/exceptional-initial-phase/common-AE-arc-and-origin'],shared_verified_context_digest=seal['source_first_freeze']['RAW_sha256'])
c['learning_contract']['salvage'].update(reason='No proof attempt before independently reviewed exact header seal.')
c['learning_contract']['reader_backpressure'].update(source_expansion_nodes=['joint-actual-record-clock','measurable-interval-partition','harmonic-branch','uncovered-complement','common-AE-all-time-realization','actual-positive-origin'],lean_expansion_nodes=[decl])
c['graph_contribution'].update(focus_targets=[decl],visual_review='Pending proof/publication/affected graph and page acceptance.')
c['conceptual_mirror_audit']=dict(status='pending',discovery_ids=[],reason='Required before PROVED_LOCAL; source actual same-domain measurable assembly, no new conceptual transport.')
write(Path('research-wiki/frontier-cells')/(cid+'.json'),c)
check('publication-packet-before-proof80',['tools/astis_publication.py','packet','--cell',cid]);check('frontier-before-proof80',['tools/astis_frontier_cells.py','check'])
print('SAU80 sealed and claimed; no proof credit')
