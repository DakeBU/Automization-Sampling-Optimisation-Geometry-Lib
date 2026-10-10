from pathlib import Path
import copy,hashlib,json,os,subprocess,sys
root=Path.cwd();base=Path('runs/20261007-companion-priority')
pre=base/'pbps-b4-perturbation-preproof72';prior=base/'pbps-actual-corrector-change71';r=base/'pbps-b4-corrector-perturbation72'
load=lambda p:json.loads(Path(p).read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest()
def write(p,x):
 p=Path(p);assert not p.exists(),p
 p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
seal=load(pre/'root.statement-seal72.json')
assert seal['status']=='SEALED_BEFORE_PROOF_SEARCH_NOT_A_PROOF'
for z in seal['exact_headers']:assert sha(Path(z['path']).read_bytes())==z['RAW_sha256']
assert load(prior/'root.exact-verification71.adoption.json')['native_verified']
assert load(prior/'root.repository71.adoption.json')['accepted_scoped_aggregate']
assert load(prior/'integration71/github-push-record/summary.json')['status']=='SUCCESS'
for name in ['root.source-first72.adoption.json','root.header-math72.adoption.json','root.header-source72.adoption.json']:assert (pre/name).is_file(),name
files=seal['proposed_files'];names=seal['declarations'];assert all(not Path(p).exists() for p in files)
parent='ASTIS-SW-PBPS-actual-corrector-change';cid='ASTIS-SW-PBPS-actual-corrector-perturbation'
pc=load(Path('research-wiki/frontier-cells')/(parent+'.json'));assert pc['status']=='independently_verified'
aid='ASTIS-SA-20261010-PBPSActualCorrectorPerturbation';owner='companion_root_20261005'
delta=seal['mathematical_delta'];source=seal['source_anchor'];boundary=seal['truth_boundary']
r.mkdir(exist_ok=False)
for label,args in [('harness-reconcile',['tools/astis.py','harness-reconcile','--json']),('capsule',['tools/astis_advance.py','capsule'])]:
 with (r/(label+'.stdout.json')).open('wb') as out,(r/(label+'.stderr.log')).open('wb') as err:
  cmd=[sys.executable,'-X','utf8',*args];p=subprocess.Popen(cmd,stdout=out,stderr=err);code=p.wait()
 write(r/(label+'.receipt.json'),dict(command=cmd,actual_PID=p.pid,exit_code=code,terminal_closed=True))
 assert code==0,(label,code)
sys.path.insert(0,str(root/'tools'));import astis_advance as adv
ledger=Path('runs/substantive_advances.jsonl');before=ledger.read_bytes()
write(r/'ledger.before72.pin.json',dict(path=ledger.as_posix(),RAW_bytes=len(before),RAW_sha256=sha(before)))
p=adv.AdvanceProposal(advance_id=aid,task_id='ASTIS-SW-PBPS-2026',goal=delta,source_anchor=source,theorem_delta=delta,truth_boundary=boundary,created_by=owner,dag_inputs=(parent,),proposed_files=tuple(files),focused_checks=('lake build AutoSamplingTheory.TechnicalLemmas.Analysis.HilbertCorrectorPerturbation','lake build AutoSamplingTheory.ExampleCases.ProximalBPS.ActualCorrectorPerturbation'),modes=('faithfulPaper',),priority=100,frontier_cell=cid,target_declarations=tuple(names))
adv.propose_advance(p)
adv.transition_advance(aid,'CLAIMED',worker_id=owner,evidence=dict(statement_seal=(pre/'root.statement-seal72.json').as_posix(),owned_files=files))
adv.transition_advance(aid,'EXPLORING',worker_id=owner,evidence=dict(route='Generic real-Hilbert expansion: Inv G=I, selfadjoint transport, A²+G²=I; internal application to same actual71 witnesses.',truth_boundary=boundary))
after=ledger.read_bytes();assert after[:len(before)]==before
(r/'ledger.claim72.append.exactraw.jsonl').write_bytes(after[len(before):]);write(r/'claim.json',p.as_event())
c=copy.deepcopy(pc)
consumers=[names[1],'PBPS Appendix B4 B28 perturbation summand, after separate actual r_rho/B27 producer']
searched=['Samplinglib and fixed Mathlib: preproof72/library-retrieval72 exact finite pins and bounded rg logs; no matching named local perturbation target in those searches. Existing sharp bound68 is a different theorem, not a dependency.']
reused=['AutoSamplingTheory.ExampleCases.ProximalBPS.ActualCorrectorChange.actual_corrector_change']
c.update(schema_version=3,cell_id=cid,title='Exact corrector perturbation on the same actual PBPS Hilbert space',source_anchor=source,target_statement='\n\n'.join(Path(z['path']).read_text(encoding='utf8') for z in seal['exact_headers']),status='claimed',parents=[parent],consumers=consumers,blocked=dict(status=False,reason='Sealed source and mathematical headers; proof not yet implemented.'),source_targets=names)
c['evidence']=dict(substantive_advance=aid,statement_seal=(pre/'root.statement-seal72.json').as_posix(),focused_checks=[],owned_files=files,truth_boundary=boundary)
c['shared_floor_audit']=dict(searched=searched,classification='missing',decision='new_route_local',canonical_declaration=names[0],canonical_shared_cell='',reason='Write the generic Hilbert leaf once in TechnicalLemmas and consume it inside actual72. There is one presently concrete production caller; no invented second route or shared-foundation completion claim.')
c['reuse_plan']=dict(searched_existing=searched,reused_declarations=reused,new_shared_declarations=[names[0]],known_consumers=[names[1]],planned_consumers=consumers[1:],no_duplicate_wrapper=True,decision_reason=c['shared_floor_audit']['reason'])
c['statement_seal']=dict(evidence=(pre/'root.statement-seal72.json').as_posix(),source_revision=seal['source_revision'],statement_version=1,signature_digest=sha(json.dumps(seal['exact_headers'],sort_keys=True,separators=(',',':')).encode()),binder_audit=seal['binder_audit'],definition_kind='Literal generic C and complete private actual Prop; both exact headers sealed independently; no provider premise.')
c['source_proof_coverage']=dict(source_graph=seal['source_graph']['path'],source_inventory=(pre/'independent-header-source72/stageA.finite-source255-plus-supplemental-coverage72.frozen.json').as_posix(),coverage_report=seal['binder_audit'],coverage_status='Prospective headers only: independent source-first primary255 and supplemental106 unique items=361 classified;24 source nodes53 edges,20 formulas27 obligations. Implementation/decoder/source coverage remains pending.')
c['source_detail_audit']=dict(primary_edition=seal['source_revision'],primary_anchor=source,fidelity_boundary=boundary,detail_status='cites_external',gap='Generic perturbation and same-actual consumer not yet compiled; actual r_rho/H/K/B27/B28 remain separate.',source_preread=seal['source_expectations']['path'],consulted=[dict(source='PBPS fixed v1 Appendix B and fixed Mathlib real Hilbert APIs',anchor='B20, Appendix B4 Ex28--Ex34; B1/B2 domain and root background',hypothesis_adapter='Generic same-space structural hypotheses are all produced internally from actual71; original six actual callers and twelve common witnesses retained.',expanded_binder_audit=seal['binder_audit'])])
c['proof_digestion']=dict(existing_substrate=reused,bookkeeping=['Retain every actual71 clause and the same C.'],new_reusable=[names[0]],new_topology=delta)
c['purification']=dict(status='pending',dead_code_audit='One new algebra leaf plus one actual mathematical consumer; no test wrapper.',duplicate_semantics_audit='Perturbation differs from B21 rotation change and sharp bound68.',canonicalization='One generic Hilbert implementation, internally consumed on actual centered HP0.',compressed_spine_delta=delta,reader_default_view='Full attributed assumptions and stepwise formulas; adjacent exact initially folded Lean.',scope=boundary)
lc=c['learning_contract'];lc['failure_class']='NONE'
lc['salvage']=dict(required=False,status='not-applicable',reason='No proof attempt before claim; sealed headers and independent reviews preserved.',promoted_fragments=[],discarded_fragments=[])
lc['parallelism'].update(decision='serial',direction_fingerprints=['same-C/perturbation/Hilbert-expansion'],shared_verified_context_digest=load(prior/'root.exact-verification71.adoption.json')['native_whole_logical_run_sha256'],expected_information_gain='Sole writer; independent mathematical verification, fresh strict blind decoder and anti-anchored source reviewer after focused compile.')
lc['reader_backpressure'].update(purification_status='pending',exposition_seal_status='pending',exposition_evidence='',lean_expansion_nodes=names,source_expansion_nodes=['B20-corrector','B4-perturbation-expansion','B27-actual-residual-open','B28-open'],assumptions_preserved=True,boundary_preserved=True)
c['graph_contribution'].update(lean_view='integration-node',overview_view='updated',functor_view='none-found',focus_targets=names,visual_review='Pending proof and independent review; mathematics first.')
c['conceptual_mirror_audit']=dict(status='pending',discovery_ids=[],reason='Audit before PROVED_LOCAL; no new formal transport inferred.')
write(Path('research-wiki/frontier-cells')/(cid+'.json'),c)
write(r/'preproof-admission.json',dict(status='CLAIMED_EXPLORING_NOT_PROVED',actual_root_PID=os.getpid(),checked_parent=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),statement_seal=(pre/'root.statement-seal72.json').as_posix(),theorem_delta=delta,truth_boundary=boundary,active_cells=[cid],production_declarations=names,Goal_complete=False))
print(aid,'EXPLORING; generic exact perturbation plus actual consumer, no proof credit.')
