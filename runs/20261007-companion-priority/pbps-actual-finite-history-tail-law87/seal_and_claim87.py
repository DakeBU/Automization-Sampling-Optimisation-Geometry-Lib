from pathlib import Path
import json,hashlib,copy,datetime,sys,subprocess
R=Path('E:/Samplinglib');r=Path(__file__).parent;pre=r.parent/'pbps-clock-tail-preread87'
load=lambda p:json.loads(p.read_bytes())
def pin(p):
 b=p.read_bytes();return {'path':str(p.relative_to(R)).replace('\\','/'),'raw_sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b)}
def new(p,x):
 assert not p.exists(),p;p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
def verify_nested(x):
 if isinstance(x,dict):
  if 'path' in x and 'raw_sha256' in x:
   p=Path(x['path']);p=p if p.is_absolute() else R/p
   assert hashlib.sha256(p.read_bytes()).hexdigest()==x['raw_sha256'],p
   if 'bytes' in x:assert p.stat().st_size==x['bytes'],p
  for v in x.values():verify_nested(v)
 elif isinstance(x,list):
  for v in x:verify_nested(v)
expected=[('header-math87/decision87.json','3e2f917922bbc3de7aa759205be42dd4b3738033350881110600952a9245f23f'),('header-math87/closed-RAW-manifest87.json','03373ac3972009c5268a14ecbef91bc8990af97433d4b662ba2ca66feece640e'),('header-source87/exact-header.source-decision.native.json','743a74a62e0a6cd54800e98c04c208a8915322138022f1aee6586a9bbcf46102'),('header-source87/closed-raw-manifest.header-source87.native.json','fc16c22a0557768866d972f5a1891cd62e9cc629dbd2a8a7827393276bcf74ee'),('header-source87/source-slice87.v2.topology-decision.native.json','f570b1f52260f4d34852d0a688c3f715001598e05aac477c0f3cbf06b53f4b64')]
for rel,h in expected:
 p=r/rel;assert pin(p)['raw_sha256']==h;verify_nested(load(p))
header=r/'header87.proposed.lean';assert pin(header)['raw_sha256']=='1048a4bf0d171d52a2eb834f4281621e0101c8d4700c7eae60edc5e64cd3c39b'
baseline=load(pre/'pre-fetch87.workspace-RAW.json')['tracked_modified']
for p,h in baseline.items():assert pin(R/p)['raw_sha256']==h
sys.path.insert(0,str(R/'tools'));import astis_advance as adv
owner='companion_root_20261005';aid='ASTIS-SA-20261011-PBPSActualFiniteHistoryTailLaw';cid='ASTIS-SW-PBPS-actual-finite-history-tail-law'
states=adv.current_advances();assert aid not in states
assert states['ASTIS-SA-20261011-PBPSActualFiniteFirstEventLaw']['state']=='VERIFIED'
assert [k for k,v in states.items() if v['state']=='STABILIZING']==['ASTIS-SA-20261005-SPHMCImplementedPhaseKernel']
file='AutoSamplingTheory/ExampleCases/ProximalBPS/ActualFiniteHistoryTailLaw.lean';assert not (R/file).exists()
decl='AutoSamplingTheory.ExampleCases.ProximalBPS.ActualFiniteHistoryTailLaw.actual_finite_history_tail_law'
parents=['AutoSamplingTheory.ExampleCases.ProximalBPS.ActualFiniteJumpRecursion.actual_fixed_reference_finite_jump_recursion','AutoSamplingTheory.TechnicalLemmas.Probability.UnitExponentialProduct.unit_exponential_product_laws']
delta='Derive actual finite stopped-history prefix causality and consumed-prefix measurability, unchanged full unused-clock tail distribution, independence/product law and unnormalized history-restricted tail law for every deterministic event depth.'
anchor='Chen-Chewi-Lu-Zhang arXiv2609.06905v1 AppendixA.1 actual iidExp1 construction (A.1),(A.2), deterministic iteration implicit in (A.7), and AppendixA.2 explicit joint-Borel recursion. Prefix/tail sigma-algebra argument and restriction identity are attributed ASTIS source-implicit completion.'
boundary='Retain original six analytic hypotheses and literal actual stopped recursion; deterministic y/reference/initial state and n. History includes records0..n, consumes raw coordinates k<n; raw tail starts at n=source E_(n+1). Full countable product tail, not only finite cylinder events. Prefix measurability/independence/laws are derived, never provider premises. Real.toNNReal extends coordinates on a P-null nonpositive-clock set; guarded infinity carries no fictitious phase state. n0/stopped/zero probability A included via unnormalized restriction identity. Only probability substrate of G86-11 is closed by proposed theorem; conditional random-hazard next-wait survival, finite-event iteration/final survival/fullA7/path reversal/invariance/physical-time residual memorylessness/random stopping/restart/Markovness/allL2/hypocoercivity/implemented errors/unbounded cost/main/composition/wholepaper/Goal remain OPEN. No proof credit at seal.'
seal={'status':'SEALED_BEFORE_PROOF_AFTER_DISTINCT_WHOLE_HEADER_MATH_SOURCE_AND_SOURCE_SLICE_REVIEW','sealed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'statement_version':1,'header':pin(header),'expanded_literal_Prop':header.read_text(encoding='utf-8').split('private def ',1)[1].split('\n#check',1)[0],'public_theorem':decl,'primary_first_freeze':pin(pre/'independent-source-first87/source-first.freeze.native.json'),'source_graph':pin(pre/'source-slice87.v2.json'),'source_inventory_reused':load(pre/'retrieval87.json')['global_source_inventory_reused_unchanged'],'global_source_graph_reused':load(pre/'retrieval87.json')['global_source_graph_reused_unchanged'],'independent_reviews':[pin(r/rel) for rel,_ in expected],'reuse_search':pin(pre/'retrieval87.json'),'toolchain':pin(R/'lean-toolchain'),'lake_manifest':pin(R/'lake-manifest.json'),'truth_boundary':boundary,'proof_BODY_created':False,'collaborator_RAW_preservation_count':len(baseline)}
new(r/'root.statement-seal87.json',seal)
p=adv.AdvanceProposal(advance_id=aid,task_id='ASTIS-SW-PBPS-2026',goal=delta,source_anchor=anchor,theorem_delta=delta,truth_boundary=boundary,created_by=owner,dag_inputs=tuple(parents),proposed_files=(file,),focused_checks=('lake build AutoSamplingTheory.ExampleCases.ProximalBPS.ActualFiniteHistoryTailLaw',),modes=('faithfulPaper',),priority=100,frontier_cell=cid,target_declarations=(decl,))
adv.propose_advance(p);adv.transition_advance(aid,'CLAIMED',worker_id=owner,evidence={'statement_seal':str(r/'root.statement-seal87.json'),'owned_files':[file]})
adv.transition_advance(aid,'EXPLORING',worker_id=owner,evidence={'route':'Prefix-causal actual recursion, prefix measurable factorization, fixed Mathlib disjoint sigma-algebra independence, injective tail reindex and restricted map extensionality.','truth_boundary':boundary})
new(r/'claim.json',p.as_event())
c=copy.deepcopy(load(R/'research-wiki/frontier-cells/ASTIS-SW-PBPS-actual-finite-first-event-law.json'))
c.update(cell_id=cid,title='Actual PBPS finite-history and unused-clock tail law',source_anchor=anchor,target_statement=header.read_text(encoding='utf-8'),status='claimed',parents=parents,consumers=['G86-13 successive finite-event density factor iteration (planned; additionally needs conditional random-hazard integration).','G86-14 final no-event survival (planned; remains open).'],source_targets=[decl],blocked={'status':False,'reason':'Exact whole header and bounded source slice independently accepted; proof pending.'})
c['evidence']={'substantive_advance':aid,'statement_seal':str(r/'root.statement-seal87.json'),'focused_checks':[],'owned_files':[file],'truth_boundary':boundary}
searches=['Samplinglib: actual finite recursion/UnitExponentialProduct and shared Frontier Cells; exact search outputs below.']+[v['stdout']['path'] for v in load(pre/'retrieval87.json')['checks']]
c['shared_floor_audit']={'searched':searches,'classification':'adapt','decision':'adapt_existing','canonical_declaration':decl,'canonical_shared_cell':'','reason':'Existing actual78 recursion and actual77 iid product supply producers; generic tail independence already belongs to pinned Mathlib. No new generic duplicate or external port.'}
c['reuse_plan']={'searched_existing':searches,'reused_declarations':parents,'new_shared_declarations':[],'known_consumers':[],'planned_consumers':c['consumers'],'no_duplicate_wrapper':True,'decision_reason':c['shared_floor_audit']['reason']}
c['statement_seal']={'evidence':str(r/'root.statement-seal87.json'),'source_revision':'arXiv2609.06905v1/Lean4.33.0/Mathlibdb584cd6d46c92f209a44c0f1c829460d327499d','statement_version':1,'signature_digest':pin(header)['raw_sha256'],'binder_audit':['Original six analytic binders unchanged.','No measurability/causality/independence/law provider hypothesis.','History event A is quantified with Borel condition; zero probability included.'],'definition_kind':'Eight literal actual recursion definitions and five P/epsilon/history/tail/past definitions. Infinity stopped sum and guarded untopD unchanged.'}
c['source_proof_coverage']={'source_graph':str(pre/'source-slice87.v2.json'),'source_inventory':seal['source_inventory_reused']['path'],'coverage_report':str(r/'header-source87/source-slice87.v2.topology-decision.native.json'),'reviewed_adapter_overlay':str(r/'header-source87/exact-header.source-decision.native.json'),'coverage_status':'Five local source nodes/four dependency edges independently reviewed from primary-first source. Unchanged exhaustive global47inventory/38nodes/76relations reused. Only I1/I2/I3 probability substrate targeted; I4/I5 and global G11 residual remain OPEN.'}
c['source_detail_audit']={'primary_edition':c['statement_seal']['source_revision'],'primary_anchor':anchor,'fidelity_boundary':boundary,'detail_status':'omitted','gap':'Authors iterate exponential clock construction without spelling consumed-prefix sigma measurability and unused-tail conditioning. Full random-hazard conditional integration is not discharged by independence alone.','consulted':[{'source':'Pinned primary-first AppendixA.1/A.2; compiled ActualFiniteJumpRecursion/UnitExponentialProduct; fixed Mathlib independence/infinitePi APIs','anchor':'A1.SS1.p2;A1.E1;A1.E2;A1.E7;A1.SS2','hypothesis_adapter':'No new source assumptions; actual deterministic-depth measurable prefix derivation.'}]}
c['proof_digestion']={'existing_substrate':parents,'bookkeeping':['Induct actual record finite-prefix causality.','Factor history through consumed prefix and derive past-sigma measurability.','Consume disjoint sigma-algebra independence and injective infinitePi tail law.','Derive joint product and history-event restricted tail law.'],'new_reusable':[],'new_topology':delta}
c['purification']={'status':'pending','dead_code_audit':'Proof pending','duplicate_semantics_audit':'Actual record measurability already78; not recredited. Search found no actual finite-prefix/tail law.','canonicalization':c['shared_floor_audit']['reason'],'compressed_spine_delta':delta,'reader_default_view':'Complete attributed mathematical statement and stepwise formula proof; exact initially folded statement/expandedProp/proof adjacent.','scope':boundary}
c['learning_contract']['parallelism'].update(decision='serial',direction_fingerprints=['actual-recursion-prefix/sigma-past/independent-countable-tail/restrict-map'],shared_verified_context_digest=seal['primary_first_freeze']['raw_sha256'])
c['learning_contract']['salvage'].update(reason='No BODY before exact header math/source and bounded source topology accepted.')
c['learning_contract']['reader_backpressure'].update(purification_status='pending',exposition_seal_status='pending',exposition_evidence='',source_expansion_nodes=['S87-I1','S87-I2','S87-I3','S87-I4:OPEN','S87-I5:OPEN'],lean_expansion_nodes=[decl],assumptions_preserved=False,boundary_preserved=False)
c['graph_contribution'].update(focus_targets=[decl],lean_view='new-node',overview_view='no-change-with-reason',visual_review='Pending proof/publication. Source sigma-algebra mechanism is not a certified formal graph edge.')
c['conceptual_mirror_audit']={'status':'pending','discovery_ids':[],'reason':'Required before PROVED_LOCAL; no new conceptual transport claimed.'}
new(R/'research-wiki/frontier-cells'/(cid+'.json'),c)
for label,args in [('publication-packet-before-proof87',['tools/astis_publication.py','packet','--cell',cid]),('frontier-before-proof87',['tools/astis_frontier_cells.py','check'])]:
 q=subprocess.run([sys.executable,'-X','utf8',*args],cwd=R,capture_output=True)
 (r/(label+'.stdout.json')).write_bytes(q.stdout);(r/(label+'.stderr.log')).write_bytes(q.stderr)
 new(r/(label+'.receipt.json'),{'exit_code':q.returncode,'terminal_closed':True});assert q.returncode==0,(q.stdout+q.stderr).decode(errors='replace')[-2000:]
print('87 exact independently reviewed statement sealed, claimed, exploring; no proof credit; sole stabilization lane unchanged.')
