from pathlib import Path
import json,hashlib,datetime,os,sys,subprocess,copy
r=Path('runs/20261007-companion-priority/pbps-actual-physical-time-cover79')
source=Path('runs/20261007-companion-priority/pbps-physical-time-preread79/source-freeze79.json')
load=lambda p:json.loads(Path(p).read_bytes())
def pin(p):
 p=Path(p);b=p.read_bytes();return dict(path=p.as_posix(),RAW_bytes=len(b),RAW_sha256=hashlib.sha256(b).hexdigest())
def write(p,x):
 p=Path(p);assert not p.exists(),p;p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
def command(label,args):
 with (r/(label+'.stdout.json')).open('wb') as out,(r/(label+'.stderr.log')).open('wb') as err:
  process=subprocess.Popen([sys.executable,'-B','-X','utf8',*args],stdout=out,stderr=err);code=process.wait()
 write(r/(label+'.receipt.json'),dict(exit_code=code,terminal_closed=True,actual_PID=process.pid));assert code==0,label
header=r/'header79.proposed.lean';assert pin(header)['RAW_sha256']=='4b3b12a9e83195cfca5c02466b51f838b0e175fad23a9665ab32df7553968a1a'
assert load(r/'header-review79/typecheck.receipt.json')['exit_code']==0
assert load(r/'header-review79/header-math-review79.json')['no_mathematical_or_syntax_repair_needed']
assert load(r/'header-review79/independent-source-topology-review79.json')['missing_required_scoped_source_nodes']==[]
assert load('runs/20261007-companion-priority/pbps-actual-nonaccumulation78/integration.notes.json')['state_distinctions']['local_aggregate_and_generated_site_gates']
command('harness-reconcile79',['tools/astis.py','harness-reconcile','--json'])
command('capsule79',['tools/astis_advance.py','capsule'])
sys.path.insert(0,str(Path.cwd()/'tools'));import astis_advance as adv
cid='ASTIS-SW-PBPS-actual-physical-time-cover';aid='ASTIS-SA-20261010-PBPSActualPhysicalTimeCover';owner='companion_root_20261005'
assert adv.current_advances()['ASTIS-SA-20261010-PBPSActualNonaccumulation']['state']=='VERIFIED'
file='AutoSamplingTheory/ExampleCases/ProximalBPS/ActualPhysicalTimeCover.lean';assert not Path(file).exists()
decl='AutoSamplingTheory.ExampleCases.ProximalBPS.ActualPhysicalTimeCover.actual_fixed_reference_physical_time_cover'
parents=['AutoSamplingTheory.ExampleCases.ProximalBPS.ActualFiniteJumpRecursion.actual_fixed_reference_finite_jump_recursion','AutoSamplingTheory.ExampleCases.ProximalBPS.ActualNonaccumulation.actual_fixed_reference_event_time_nonaccumulation']
delta='For each fixed source parameter triple, almost surely every finite physical time lies in a unique half-open actual event interval and that interval has a unique actual live record with nonnegative finite elapsed time strictly below its actual next waiting time.'
anchor='Chen-Chewi-Lu-Zhang arXiv2609.06905v1 AppendixA1 A.2, A1.E2 and between-jump A1.SS1.p2.2; nonaccumulation p3.7; original Algorithm1 and six analytic conditions.'
boundary='Only actual interval/live-record/elapsed coverage on a common AE actual-input event per fixed deterministic parameter triple. No measurable index or interpolated process, explicit index0 initialization, global path uniqueness/regularity, Markov/invariance/kernel/hypocoercivity/main/errors/cost/composition. Stopped next jump leaves last live arc; no phase at infinity. No full-paper/Goal, stabilized, merged, purified or live credit.'
frozen=load(source)
seal=dict(status='SEALED_BEFORE_PROOF_AFTER_INDEPENDENT_HEADER_AND_SOURCE_TOPOLOGY_REVIEW',sealed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),actual_root_PID=os.getpid(),statement_version=1,header=pin(header),public_theorem=decl,expanded_literal_Prop=header.read_text(encoding='utf8').split('private def ',1)[1].split('\nend\n',1)[0],primary=dict(path=frozen['primary_path'],RAW_sha256=frozen['primary_raw_sha256']),source_first_freeze=pin(source),source_graph_overlay=pin(r/'header-review79/reviewer-source-topology-overlay79.json'),header_math=pin(r/'header-review79/header-math-review79.json'),source_topology_review=pin(r/'header-review79/independent-source-topology-review79.json'),definition_audit=pin(r/'header-review79/signature-definition-readback79.json'),typecheck=pin(r/'header-review79/typecheck.receipt.json'),binder_inventory=frozen['binder_map'],dag_parents=[pin('AutoSamplingTheory/ExampleCases/ProximalBPS/ActualFiniteJumpRecursion.lean'),pin('AutoSamplingTheory/ExampleCases/ProximalBPS/ActualNonaccumulation.lean')],toolchain=pin('lean-toolchain'),lake_manifest=pin('lake-manifest.json'),truth_boundary=boundary,proof_BODY_created=False,VERIFIED=False)
write(r/'root.statement-seal79.json',seal)
proposal=adv.AdvanceProposal(advance_id=aid,task_id='ASTIS-SW-PBPS-2026',goal=delta,source_anchor=anchor,theorem_delta=delta,truth_boundary=boundary,created_by=owner,dag_inputs=tuple(parents),proposed_files=(file,),focused_checks=('lake build AutoSamplingTheory.ExampleCases.ProximalBPS.ActualPhysicalTimeCover',),modes=('faithfulPaper',),priority=100,frontier_cell=cid,target_declarations=(decl,))
adv.propose_advance(proposal);adv.transition_advance(aid,'CLAIMED',worker_id=owner,evidence=dict(statement_seal=(r/'root.statement-seal79.json').as_posix(),owned_files=[file]));adv.transition_advance(aid,'EXPLORING',worker_id=owner,evidence=dict(route='Least clock crossing minus one and monotone initialized actual times; finite live-record and finite/top wait split.',truth_boundary=boundary));write(r/'claim.json',proposal.as_event())
c=copy.deepcopy(load('research-wiki/frontier-cells/ASTIS-SW-PBPS-actual-event-time-nonaccumulation.json'))
c.update(cell_id=cid,title='Actual PBPS finite physical-time interval coverage',source_anchor=anchor,target_statement=header.read_text(encoding='utf8'),status='claimed',parents=parents,consumers=['Measurable actual active-index and finite-time harmonic interpolation; later full path/Markov/invariance consumer.'],source_targets=[decl],blocked=dict(status=False,reason='Sealed reviewed bounded target; sole writer root.'))
c['evidence']=dict(substantive_advance=aid,statement_seal=(r/'root.statement-seal79.json').as_posix(),focused_checks=[],owned_files=[file],truth_boundary=boundary)
search=['ActualFiniteJumpRecursion76 initialized monotone event clocks, live finite/top updates; ActualNonaccumulation78 actual finite-horizon escape. No existing actual finite physical-time interval-cover declaration.','Pinned Mathlib Nat.find/spec/min and natural ordering; NNReal subtraction, WithTop finite coercions. No upstream transplant needed.','Current shared cells, canonical probability product, Registry and module cards: no duplicate stochastic input foundation.']
c['shared_floor_audit']=dict(searched=search,classification='missing',decision='new_route_local',canonical_declaration=decl,canonical_shared_cell='',reason='Actual PBPS consumer of two verified exact parents; interval existence and actual elapsed offset are new conclusions, not supplied premises.')
c['reuse_plan']=dict(searched_existing=search,reused_declarations=parents,new_shared_declarations=[],known_consumers=[],planned_consumers=c['consumers'],no_duplicate_wrapper=True,decision_reason=c['shared_floor_audit']['reason'])
c['statement_seal']=dict(evidence=(r/'root.statement-seal79.json').as_posix(),source_revision='arXiv2609.06905v1/Lean4.33.0/Mathlibdb584cd6d46c92f209a44c0f1c829460d327499d',statement_version=1,signature_digest=seal['header']['RAW_sha256'],binder_audit=frozen['binder_map'],definition_kind='Private literal Prop; original six analytic binders, eleven exact actual definitions; unique interval and actual live record/elapsed conclusions.')
c['source_proof_coverage']=dict(source_graph=source.as_posix(),source_inventory=source.as_posix(),coverage_report=(r/'header-review79/independent-source-topology-review79.json').as_posix(),reviewed_adapter_overlay=(r/'header-review79/reviewer-source-topology-overlay79.json').as_posix(),coverage_status='Complete scoped prospective source inventory; implementation coverage OPEN.')
c['source_detail_audit'].update(primary_anchor=anchor,fidelity_boundary=boundary,gap='Source suppresses active-index selection and stopped-last-arc bookkeeping; actual unique interval/live record/elapsed adapter is current bounded delta. Measurable process and full uniqueness remain later obligations.')
c['proof_digestion']=dict(existing_substrate=parents,bookkeeping=['Least first crossing gives covering predecessor; half-open endpoints and empty zero-length intervals.','Current finite record remains live on final infinite-wait arc.'],new_reusable=[],new_topology=delta)
c['purification'].update(status='pending',dead_code_audit='Pending proof',duplicate_semantics_audit='Existing parents do not select an actual finite physical-time interval or live record.',compressed_spine_delta=delta,scope=boundary)
c['learning_contract']['parallelism'].update(decision='serial',direction_fingerprints=['actual-clock/least-first-crossing/live-record/finite-or-top-next-wait'],shared_verified_context_digest=seal['source_first_freeze']['RAW_sha256'])
c['learning_contract']['salvage'].update(reason='No proof attempt before independently reviewed seal. No statement repair needed.')
c['learning_contract']['reader_backpressure'].update(source_expansion_nodes=['initialized-monotone-clocks','actual-finite-horizon-escape','unique-half-open-interval','actual-live-record','finite-or-infinite-next-wait'],lean_expansion_nodes=[decl])
c['graph_contribution'].update(focus_targets=[decl],visual_review='Pending proof/publication/local graph checks.')
c['conceptual_mirror_audit']=dict(status='pending',discovery_ids=[],reason='Required before PROVED_LOCAL; same-domain actual interval adapter is not a new conceptual transport.')
write(Path('research-wiki/frontier-cells')/(cid+'.json'),c)
command('publication-packet-before-proof79',['tools/astis_publication.py','packet','--cell',cid]);command('frontier-before-proof79',['tools/astis_frontier_cells.py','check'])
print('SAU79 sealed and claimed; no proof credit')
