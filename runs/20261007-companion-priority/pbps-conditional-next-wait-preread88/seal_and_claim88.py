from pathlib import Path
import json, hashlib, copy, datetime, sys, subprocess
R=Path('E:/Samplinglib'); pre=Path(__file__).parent
r=pre.parent/'pbps-actual-conditional-next-wait-survival88'
load=lambda p:json.loads(p.read_bytes())
def pin(p):
 b=p.read_bytes();return dict(path=p.relative_to(R).as_posix(),raw_sha256=hashlib.sha256(b).hexdigest(),bytes=len(b))
def new(p,x):
 assert not p.exists(),p;p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
def verify(x):
 if isinstance(x,dict):
  if 'path' in x and 'raw_sha256' in x:
   p=Path(x['path']);p=p if p.is_absolute() else R/p
   assert pin(p)['raw_sha256']==x['raw_sha256'],p
   if 'bytes' in x:assert p.stat().st_size==x['bytes'],p
  for v in x.values():verify(v)
 elif isinstance(x,list):
  for v in x:verify(v)
expected={'header-math88/decision88.json':'48ce83827af56a15aea29438b7dfe3142f381217638dd51b846f4dcf059a6fca','header-math88/closed-RAW-manifest88.json':'651e27de31564c25e91683c930a25bf4dff92762127325b5afb57f08cf1bfa0d','header-source88/header88.source-decision.native.json':'38a95c5cd4c34d1861fdce32ec3c506afd41a58abef7430fe3815b10e30dc228','header-source88/closed-raw-manifest.header-source88.native.json':'2f2c49e16104d098e24fb99c5ff45db849245cf26e0008407bd8193a7d1b80fa','independent-source-first88/closed-raw-manifest.source-first88.native.json':'fedbc429c2e3cc01aa92a2b5dd94a0f5c4c431f005564bcb50631822681432f5'}
for rel,h in expected.items():
 p=pre/rel;assert pin(p)['raw_sha256']==h;verify(load(p))
header=pre/'header88.proposed.lean';assert pin(header)['raw_sha256']=='89890948b0716e9e8a0a4e4d5c634aa166361b7fb1575f57e751d49e024aeed3'
baseline=load(pre/'pre-fetch88.workspace-RAW.json')['tracked_modified']
for p,h in baseline.items():assert pin(R/p)['raw_sha256']==h
sys.path.insert(0,str(R/'tools'));import astis_advance as adv
aid='ASTIS-SA-20261011-PBPSActualConditionalNextWaitSurvival';cid='ASTIS-SW-PBPS-actual-conditional-next-wait-survival';owner='companion_root_20261005'
states=adv.current_advances();assert aid not in states
assert states['ASTIS-SA-20261011-PBPSActualFiniteHistoryTailLaw']['state']=='VERIFIED'
assert [k for k,v in states.items() if v['state']=='STABILIZING']==['ASTIS-SA-20261005-SPHMCImplementedPhaseKernel']
file='AutoSamplingTheory/ExampleCases/ProximalBPS/ActualConditionalNextWaitSurvival.lean';assert not (R/file).exists()
decl='AutoSamplingTheory.ExampleCases.ProximalBPS.ActualConditionalNextWaitSurvival.actual_conditional_next_wait_survival'
parents=['AutoSamplingTheory.ExampleCases.ProximalBPS.ActualFiniteHistoryTailLaw.actual_finite_history_tail_law','AutoSamplingTheory.ExampleCases.ProximalBPS.ActualHazardClock.actual_integrated_hazard_clock_laws','AutoSamplingTheory.TechnicalLemmas.Probability.UnitExponentialProduct.unit_exponential_product_laws']
delta='Derive the live-guarded unnormalized next-wait survival identity for every Borel duration of the complete actual deterministic-depth finite history; prove event/weight measurability and weight at most one.'
anchor='Chen-Chewi-Lu-Zhang arXiv2609.06905v1 AppendixA.1 (A.1),(A.2), conditional survival factor implicit in (A.7), and AppendixA.2 measurable recursion. History-dependent duration product integration is attributed ASTIS source-implicit completion.'
boundary='Same six original analytic hypotheses and literal stopped actual recursion. Deterministic event depth n; Borel finite-valued duration d of complete history and Borel event A are admissible test objects, not extra analytic hypotheses or probability/regularity providers. Stopped histories have zero survival weight; live infinite waits survive every finite duration. Unnormalized identity includes null A, n0, rank0 and unbounded duration functions. Only S87-I4 closes when proved; S87-I5 conditional finite-wait density, ordered-time iteration, final factor assembly, fullA7, physical-time residual restart/Markovness/invariance/nonexplosion/hypocoercivity/implementation/cost/main/composition/wholepaper/Goal remain OPEN. No proof credit at seal.'
r.mkdir(exist_ok=False)
seal=dict(status='SEALED_BEFORE_BODY_AFTER_DISTINCT_PREPROOF_MATH_SOURCE_AND_TOPOLOGY_ACCEPTANCE',sealed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),statement_version=1,header=pin(header),expanded_literal_Prop=header.read_text(encoding='utf8').split('private def ',1)[1].split('\n#check',1)[0],public_theorem=decl,primary_first_freeze=pin(pre/'independent-source-first88/source-first88.freeze.native.json'),source_graph=pin(pre/'independent-source-first88/source-proof-slice88.native.json'),source_coverage=pin(pre/'independent-source-first88/source-coverage88.native.json'),independent_reviews=[pin(pre/rel) for rel in expected],reuse_search=pin(pre/'retrieval88.json'),toolchain=pin(R/'lean-toolchain'),lake_manifest=pin(R/'lake-manifest.json'),truth_boundary=boundary,proof_BODY_created=False,collaborator_RAW_preservation_count=len(baseline),chronology_disclosure='Source-graph author froze primary reconstruction before header exposure. Distinct topology reviewer saw prospective candidate earlier, reconstructed directly from primary before author graph read, and saw no implementation or source-acceptance verdict. No implementation existed. Root generic API retrieval before seal adds no mathematical evidence or proof credit.')
new(r/'root.statement-seal88.json',seal)
p=adv.AdvanceProposal(advance_id=aid,task_id='ASTIS-SW-PBPS-2026',goal=delta,source_anchor=anchor,theorem_delta=delta,truth_boundary=boundary,created_by=owner,dag_inputs=tuple(parents),proposed_files=(file,),focused_checks=('lake build AutoSamplingTheory.ExampleCases.ProximalBPS.ActualConditionalNextWaitSurvival',),modes=('faithfulPaper',),priority=100,frontier_cell=cid,target_declarations=(decl,))
adv.propose_advance(p);adv.transition_advance(aid,'CLAIMED',worker_id=owner,evidence=dict(statement_seal=str(r/'root.statement-seal88.json'),owned_files=[file]))
adv.transition_advance(aid,'EXPLORING',worker_id=owner,evidence=dict(route='Actual87 joint history/tail product, actual75 joint measurable clock and deterministic survival, actual77 coordinate law, product-section integration.',truth_boundary=boundary))
new(r/'claim.json',p.as_event())
c=copy.deepcopy(load(R/'research-wiki/frontier-cells/ASTIS-SW-PBPS-actual-finite-history-tail-law.json'))
c.update(cell_id=cid,title='Actual PBPS conditional next-wait survival',source_anchor=anchor,target_statement=header.read_text(encoding='utf8'),status='claimed',parents=parents,consumers=load(pre/'retrieval88.json')['planned_consumers'],source_targets=[decl],blocked=dict(status=False,reason='Preproof exact header and source topology accepted; proof pending.'))
c['evidence']=dict(substantive_advance=aid,statement_seal=str(r/'root.statement-seal88.json'),focused_checks=[],owned_files=[file],truth_boundary=boundary)
searches=[x['stdout']['path'] for x in load(pre/'retrieval88.json')['checks']]
reason='Actual87/75/77 supply probability and hazard producers. Generic product/map integration already belongs to pinned Mathlib; new actual adapter remains route-local, with no duplicate generic lemma or upstream port.'
c['shared_floor_audit']=dict(searched=searches,classification='adapt',decision='adapt_existing',canonical_declaration=decl,canonical_shared_cell='',reason=reason)
c['reuse_plan']=dict(searched_existing=searches,reused_declarations=parents,new_shared_declarations=[],known_consumers=[],planned_consumers=c['consumers'],no_duplicate_wrapper=True,decision_reason=reason)
c['statement_seal']=dict(evidence=str(r/'root.statement-seal88.json'),source_revision='arXiv2609.06905v1/Lean4.33.0/Mathlibdb584cd6d46c92f209a44c0f1c829460d327499d',statement_version=1,signature_digest=pin(header)['raw_sha256'],binder_audit=['Original six analytic binders unchanged.','Borel d and A classify deterministic tests; no extra analytic source assumptions.','No measurable-state, independence or conditional-law provider premise.'],definition_kind='Eleven literal actual recursion/input/history definitions and two live-guarded observable definitions; stopped weight zero, infinity guard unchanged.')
c['source_proof_coverage']=dict(source_graph=str(pre/'independent-source-first88/source-proof-slice88.native.json'),source_inventory='runs/20261007-companion-priority/pbps-actual-finite-first-event-law86/independent-source86/source-inventory86.exhaustive-successor.json',coverage_report=str(pre/'header-math88/topology-review88.json'),reviewed_adapter_overlay=str(pre/'header-source88/header88.source-decision.native.json'),coverage_status='Independent primary-first 9node/10AND local slice and distinct coverage/topology review accepted; global unchanged inventory retained. S87-I4 target only, S87-I5/global path assembly OPEN. No BODY credit.')
c['source_detail_audit']=dict(primary_edition=c['statement_seal']['source_revision'],primary_anchor=anchor,fidelity_boundary=boundary,detail_status='omitted',gap='Source iterates clock densities without explicit history-dependent unnormalized survival/product integration. Finite-wait density and ordered-time iteration remain separate.',consulted=[dict(source='Pinned primary A.1/A.2, compiled actual87/75/77 and pinned Mathlib product integration',anchor='A1.E1;A1.E2;A1.E7;A1.SS2',hypothesis_adapter='No extra analytic source assumption; admissible Borel duration/event classes explicit.')])
c['proof_digestion']=dict(existing_substrate=parents,bookkeeping=['Measurable live-guarded event and exponential weight.','Obtain fixed-history survival fiber from actual75 and coordinate0 law.','Consume actual87 joint history/tail product and product-section integration.'],new_reusable=[],new_topology=delta)
c['purification']=dict(status='pending',dead_code_audit='Proof pending',duplicate_semantics_audit='No actual conditional-survival duplicate found; generic product APIs reused.',canonicalization=reason,compressed_spine_delta=delta,reader_default_view='Complete attributed statement and formula proof; exact folded Lean adjacent.',scope=boundary)
c['learning_contract']['salvage'].update(required=False,status='not-applicable',reason='No BODY before statement seal.',promoted_fragments=[],discarded_fragments=[])
c['learning_contract']['parallelism'].update(decision='serial',direction_fingerprints=['actual-history/random-duration/live-guard/product-section-survival'],shared_verified_context_digest=seal['primary_first_freeze']['raw_sha256'])
c['learning_contract']['reader_backpressure'].update(purification_status='pending',exposition_seal_status='pending',exposition_evidence='',source_expansion_nodes=['S88-A1','S88-A2','S88-P1','S88-P2','S87-I4:TARGET','S87-I5:OPEN'],lean_expansion_nodes=[decl],assumptions_preserved=False,boundary_preserved=False)
c['graph_contribution'].update(focus_targets=[decl],lean_view='new-node',overview_view='no-change-with-reason',functor_view='none-found',visual_review='Pending proof/publication and inspectable affected branch; no formal credit for source overlays.')
c['conceptual_mirror_audit']=dict(status='pending',discovery_ids=[],reason='Required before PROVED_LOCAL; no new transport asserted.')
new(R/'research-wiki/frontier-cells'/(cid+'.json'),c)
for label,args in [('publication-packet-before-proof88',['tools/astis_publication.py','packet','--cell',cid]),('frontier-before-proof88',['tools/astis_frontier_cells.py','check'])]:
 q=subprocess.run([sys.executable,'-X','utf8',*args],cwd=R,capture_output=True)
 (r/(label+'.stdout.json')).write_bytes(q.stdout);(r/(label+'.stderr.log')).write_bytes(q.stderr)
 new(r/(label+'.receipt.json'),dict(exit_code=q.returncode,terminal_closed=True));assert q.returncode==0,(q.stdout+q.stderr).decode(errors='replace')[-3000:]
print('88 sealed and claimed, bounded publication/frontier PASS; no proof credit; sole lane unchanged.')
