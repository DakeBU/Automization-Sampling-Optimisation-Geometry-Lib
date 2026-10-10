from pathlib import Path
import json,hashlib,subprocess,sys,copy
root=Path.cwd();b=root/'runs/20261007-companion-priority/pbps-real-complex-lift-preproof60';d=b/'independent-preproof60';s=d/'cap-source-readback'
load=lambda p:json.loads(Path(p).read_bytes());sha=lambda x:hashlib.sha256(x).hexdigest();can=lambda x:json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def path(x):
 p=Path(str(x).replace('\\','/'));return p if p.is_absolute() else root/p
def pin(p):
 p=path(p);raw=p.read_bytes();lf=raw.replace(b'\r\n',b'\n');return dict(path=p.relative_to(root).as_posix(),bytes=len(raw),lf_bytes=len(lf),raw_sha256=sha(raw),lf_sha256=sha(lf))
def key(q):return (path(q['path']).as_posix().lower(),q['raw_sha256'],q['lf_sha256'])
def write(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
maps={};manifest=load(d/'input.manifest.json')
for q in manifest['qualified_inputs']:maps[key(q['original'])]=q['raw_snapshot']
admin=load(root/'runs/20261007-companion-priority/pbps-centered-defect59/integration59/accepted-closeout/closeout.json')['administrative_exact_history']
maps[key(admin['original'])]=admin['exact_raw_snapshot']
seen={};history=[]
def walk(x):
 if isinstance(x,dict):
  if {'path','raw_sha256','lf_sha256'}<=x.keys():
   k=key(x)
   if k not in seen:
    q=pin(x['path'])
    if q['raw_sha256']!=x['raw_sha256'] or q['lf_sha256']!=x['lf_sha256']:
     assert k in maps,('UNMAPPED',x);q=pin(maps[k]['path']);history.append(dict(original=x,exact_raw_snapshot=q))
    assert all(q[z]==x[z] for z in ['raw_sha256','lf_sha256']) and all(q[z]==x[z] for z in ['bytes','lf_bytes'] if z in x),x
    seen[k]=q
  for v in x.values():walk(v)
 elif isinstance(x,list):
  for v in x:walk(v)
for folder,expected in [(d,'acdb686187465251ef1588205cf2c3b413bb2db0b02871a3076012739aa644af'),(s,'519144bcddb1403ee72223acbb28451603420b7ad996df75bf0cfd3410d1bf2f')]:
 run=load(folder/'run.json');lease=load(folder/'lease.json');assert lease['status']=='CLOSED' and lease['closed_last'] and lease['actual_foreground_readback_exit_code']==0
 assert sha(can({k:v for k,v in run.items() if k!='run_sha256'}))==run['run_sha256']==lease['native_run_sha256']==expected
 walk(run);walk(lease)
named=pin(d/'named-preproof-source.payload.json');assert named['raw_sha256']==load(d/'run.json')['named_payload_sha256']=='ece2c5edb9a005f601ce3f5caeac26f6c9c812337feaef8c9faee8de0c7c6ccb'
assert pin(s/'named-cap.payload.json')['raw_sha256']=='3eeaf46ae23a6a402b95094509271f1eab0e218c636492f40ecc169a229f23ab'
for name in ['input.manifest.json','statement.review.json','source.coverage.json','source.graph.json']:walk(load(d/name))
review=load(d/'statement.review.json');assert review['header0_verdict']==review['header1_verdict']=='equivalent-after-elaboration' and not review['blocking_deltas'] and not review['repairs']
hashes=['4bf52d8b3490776b52eaeaa69c9ac730d1ec9594fc95ed822b5ba8b29bcead39','e69e6101b8171ff93504b01f23490263f54d92406a1036178e518f18aa41f57c']
for i in range(2):assert pin(b/f'header{i}.lean')['raw_sha256']==hashes[i]
seal=dict(status='STATEMENT60_SEALED_SOURCE_TOPOLOGY_ACCEPTED_NOT_PROVED',headers=[pin(b/f'header{i}.lean') for i in range(2)],native_run=pin(d/'run.json'),native_lease=pin(d/'lease.json'),cap_supplement_run=pin(s/'run.json'),cap_supplement_lease=pin(s/'lease.json'),named_payload=named,unique_qualified_pin_readbacks=len(seen),explicit_historical_resolutions=history,source_graph=pin(d/'source.graph.json'),coverage=pin(d/'source.coverage.json'),cap_source=pin(s/'cap.source.supplement.json'),type_evidence_only=True,proof_search_preceded_by_seal=True,no_proof_credit=True)
write(b/'root.statement-seal60.json',seal)
sys.path.insert(0,str(root/'tools'));import astis_advance as adv
r=root/'runs/20261007-companion-priority/pbps-real-complex-lift60';r.mkdir(exist_ok=False)
cfg=load(b/'statement-candidate.json');files=cfg['owned_files'];decls=['AutoSamplingTheory.TechnicalLemmas.Measure.L2RealComplexOperator.exists_positive_complex_lift','AutoSamplingTheory.ExampleCases.ProximalBPS.DefectComplexLift.actual_positive_defect_complex_lift'];cells=['ASTIS-SHARED-l2-real-complex-positive-lift','ASTIS-SW-PBPS-positive-defect-complex-lift'];parents=['ASTIS-SW-PBPS-centered-selfadjoint-defect'];aid='ASTIS-SA-20261008-PBPSPositiveDefectComplexLift';owner='companion_root_20261005';boundary=cfg['truth_boundary']
proposal=adv.AdvanceProposal(advance_id=aid,task_id='ASTIS-SW-PBPS-2026',goal='Construct genuine positive complexification of real L2 operators and consume actual PBPS positive D under original source hypotheses.',source_anchor=cfg['anchor'],theorem_delta='Actual positive L2 complex lift with isometric real embedding, exact pointwise-conjugation fixed range, literal two-component operator formula/intertwining/conjugation compatibility.',truth_boundary=boundary,created_by=owner,dag_inputs=tuple(parents),proposed_files=tuple(files),focused_checks=('lake build Tests.ProximalBPSDefectComplexLift',),modes=('faithfulPaper',),priority=100,frontier_cell=cells[1],target_declarations=tuple(decls))
# Preserve the exact prior ledger used by closed59 evidence before new work.
p=root/'runs/substantive_advances.jsonl';old=pin(p);snap=r/'ledger.before60.exactraw.snapshot';snap.write_bytes(p.read_bytes());write(r/'ledger-history.json',dict(original=old,exact_raw_snapshot=pin(snap)))
adv.propose_advance(proposal);adv.transition_advance(aid,'CLAIMED',worker_id=owner,evidence={'preproof_seal':str((b/'root.statement-seal60.json').relative_to(root)),'owned_files':files});adv.transition_advance(aid,'EXPLORING',worker_id=owner,evidence={'route':'actual quotient L2 real/imag bounded complexification and positive quadratic-form adapter'})
template=load(root/'research-wiki/frontier-cells/ASTIS-SHARED-l2-pullback-range.json')
for i,cid in enumerate(cells):
 c=copy.deepcopy(template);c.update(cell_id=cid,route='shared' if i==0 else 'samplewiki-route',title=['Positive real L2 operator complexification','Actual PBPS positive squared-defect complex lift'][i],source_anchor=cfg['anchor'],target_statement=(b/f'header{i}.lean').read_text(encoding='utf-8'),status='claimed',parents=parents if i==1 else [],consumers=['Actual PBPS D=I-T*T from centered_selfadjoint_defect; same real kernel lifted before true Gamma root.','Planned exact PBPS conditional projection P on real L2(J) in B1/B5; common complex root/block calculus substrate, not an existing Lean consumer.'],blocked=dict(status=False,reason='Preproof accepted; theorem bodies not yet implemented.'),evidence=dict(substantive_advance=aid,statement_seal=str((b/'root.statement-seal60.json').relative_to(root)),focused_checks=[],owned_files=files,truth_boundary=boundary))
 if i==1:c['parents']=[cells[0],*parents]
 c['shared_floor_audit']=dict(searched=['Actual local Measure/L2Expectation/L2PullbackRange and current module cards; bounded local L2 complexification search empty. Fixed Mathlib LpSpace.compLpL, Complex scalar CLMs, L2 inner integral, Positive complex criterion. Existing complexOfReal only domain C, not arbitrary complex L2.'],classification='adapt',decision='new_canonical_shared' if i==0 else 'reuse_existing',canonical_declaration=decls[i],canonical_shared_cell=cells[0],reason='One generic actual quotient complex lift reused by real paper kernel; no supplied paper operator/CFC/root certificate or copied probability proof.')
 c['reuse_plan']=dict(searched_existing=c['shared_floor_audit']['searched'],reused_declarations=[] if i==0 else ['AutoSamplingTheory.ExampleCases.ProximalBPS.CenteredDefectOperator.actual_centered_selfadjoint_defect',decls[0]],new_shared_declarations=[decls[0]] if i==0 else [],known_consumers=[decls[1]],planned_consumers=c['consumers'][1:],no_duplicate_wrapper=True,decision_reason=c['shared_floor_audit']['reason'])
 c['statement_seal']=dict(evidence=str((b/'root.statement-seal60.json').relative_to(root)),source_revision='2609.06905v1/Lean4.33.0/Mathlibdb584cd6',statement_version=1,signature_digest=hashes[i],binder_audit=str((d/'statement.review.json').relative_to(root)),definition_kind=cfg['definition_audit'])
 c['source_proof_coverage']=dict(source_graph=str((d/'source.graph.json').relative_to(root)),source_inventory=str((d/'source.coverage.json').relative_to(root)),coverage_report=str((d/'statement.review.json').relative_to(root)),coverage_status='Independent22region43item bounded NODE/EXCLUDED plus literalcap primary supplement: combined23regions44items; printed block route separate from ASTIS scalar lift route.')
 c['source_detail_audit'].update(primary_anchor=cfg['anchor'],fidelity_boundary=boundary,gap='ASTIS complexification prerequisite; B10 real root and B11 still unproved.',consulted=[dict(source='Pinned Mathlib LpSpace/L2Space/Positive/Complex',anchor='compLpL and complex positive quadratic criterion',hypothesis_adapter=cfg['binder_audit']['canonical_node' if i==0 else 'paper_consumer'])])
 c['learning_contract']['parallelism'].update(decision='serial',direction_fingerprints=['quotient-real-L2-positive-complexification'],shared_verified_context_digest=load(d/'run.json')['run_sha256'],expected_information_gain='One writer plus required independent mathematical/source reviews, not parallel theorem implementations.')
 c['learning_contract']['reader_backpressure'].update(exposition_seal_status='pending',exposition_evidence='',source_expansion_nodes=[q['id'] for q in load(d/'source.graph.json')['nodes']],lean_expansion_nodes=[decls[i]])
 c['learning_contract']['salvage'].update(reason='No proof60 failed yet; original source-only index supplemented independently without header changes.')
 c['graph_contribution'].update(lean_view='new-node',overview_view='updated',functor_view='none-found',focus_targets=[decls[i]],visual_review='Pending actual compiled complex-lift branch; no root/transport certificate.')
 c.pop('conceptual_mirror_audit',None)
 p=root/'research-wiki/frontier-cells'/f'{cid}.json';assert not p.exists();write(p,c)
write(r/'claim.json',proposal.as_event());write(r/'preproof-admission.json',seal)
print(aid,'EXPLORING: two exact statements independently sealed; no60 proof or mathematical completion yet.')
