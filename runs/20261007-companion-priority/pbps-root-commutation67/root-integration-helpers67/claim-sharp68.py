from pathlib import Path
import copy, hashlib, json, os, subprocess, sys

root=Path.cwd(); base=Path('runs/20261007-companion-priority')
pre=base/'pbps-sharp-energy-preproof68'; r=base/'pbps-sharp-energy68'; prior=base/'pbps-root-commutation67'
load=lambda p:json.loads(Path(p).read_bytes()); sha=lambda b:hashlib.sha256(b).hexdigest()
def w(p,x):
    p=Path(p); assert not p.exists(),p
    p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')

seal=load(pre/'root.statement-seal68.json')
assert seal['status']=='STATEMENT68_SEALED_NOT_CLAIMED_NOT_PROVED'
assert load(prior/'root.exact-verification67.adoption.json')['native_verified']
assert load(prior/'root.repository67.adoption.json')['accepted_scoped_aggregate']
assert load(prior/'integration.notes.json')['registry_count']==514
for row in seal['headers']:
    for item in row.values():assert sha(Path(item['path']).read_bytes())==item['RAW_sha256']
assert load(pre/'root.header68.adoption.json')['status']=='THREE_REPAIRED_HEADER68_DRAFTS_ACCEPTED_NO_PROOF'
owner='companion_root_20261005'; aid='ASTIS-SA-20261009-PBPSSharpCorrectorEnergy'
parent='ASTIS-SW-PBPS-actual-root-inverse-commutation'
cid='ASTIS-SW-PBPS-sharp-corrector-energy'; shared='ASTIS-SHARED-hilbert-corrector-square-bound'
files=['AutoSamplingTheory/TechnicalLemmas/Analysis/HilbertCorrectorBound.lean',
       'AutoSamplingTheory/ExampleCases/ProximalBPS/SharpCorrectorEnergy.lean',
       'Tests/ProximalBPSSharpCorrectorEnergy.lean']
names=['AutoSamplingTheory.TechnicalLemmas.Analysis.HilbertCorrectorBound.quadratic_corrector_bound_of_square_identity',
       'AutoSamplingTheory.ExampleCases.ProximalBPS.SharpCorrectorEnergy.actual_sharp_corrector_bound',
       'Tests.ProximalBPSSharpCorrectorEnergy.genuine_actual_modified_energy_equivalence']
assert all(not Path(p).exists() for p in files)
source='PBPS2609.06905v1 AppendixB3 LemmaB.3 and B19/B20/B22/B23/B24; exact sharp two-component Hilbert energy bound and actual centered PBPS consumer.'
delta='Prove sharp |C(u,v)| <= (||u||²+||v||²)/(2gamma) for SAME actual root/inverse/coefficient, then actual centered |C(fP,fV)| <= ||f||²/(2gamma). Genuine original-input consumer proves half/three-halves modified energy equivalence and perturbation bound for every0<omegaWeight<=gamma.'
boundary='Sharp first-corrector energy/LemmaB.3 only. B21 rotation,B2/weakH1,B4 dynamics,hypocoercivity/main,invariance/nonexplosion,errors,caps,expectedquery costs and actual-input composition remain independent. All original finite real Hilbert/Borel/C2/two Hessians/positive capped eta callers retained; no new provider/coercivity/strict endpoint/Nontrivial premise. Rank0 and alphaeta1 legal.'
r.mkdir(exist_ok=False)
sys.path.insert(0,str(root/'tools'));import astis_advance as adv
ledger=Path('runs/substantive_advances.jsonl');before=ledger.read_bytes()
w(r/'ledger.before68.pin.json',dict(path=ledger.as_posix(),raw_bytes=len(before),raw_sha256=sha(before)))
p=adv.AdvanceProposal(advance_id=aid,task_id='ASTIS-SW-PBPS-2026',goal=delta,source_anchor=source,theorem_delta=delta,
    truth_boundary=boundary,created_by=owner,dag_inputs=(parent,),proposed_files=tuple(files),
    focused_checks=('lake build Tests.ProximalBPSSharpCorrectorEnergy',),modes=('faithfulPaper',),priority=100,
    frontier_cell=cid,target_declarations=tuple(names))
adv.propose_advance(p)
adv.transition_advance(aid,'CLAIMED',worker_id=owner,evidence=dict(statement_seal=(pre/'root.statement-seal68.json').as_posix(),owned_files=files))
adv.transition_advance(aid,'EXPLORING',worker_id=owner,evidence=dict(route='Selfadjoint block energy cancellation and two-component Cauchy-Schwarz, actual norm budget, weighted norm equivalence',truth_boundary=boundary))
after=ledger.read_bytes();assert after[:len(before)]==before
(r/'ledger.claim68.append.exactraw.jsonl').write_bytes(after[len(before):]);w(r/'claim.json',p.as_event())
searched=['Samplinglib: Analysis module card, TechnicalLemmas and actual67 coefficient/global-domain proofs searched; no existing sharp Hilbert corrector lemma. Fixed Mathlib real_inner/norm_add_sq_real/norm_sub_sq_real/IsSelfAdjoint/ContinuousLinearMap operator norm APIs inspected in preproof68. No SLT/OpenAI/floating upstream used.']
reused=['AutoSamplingTheory.ExampleCases.ProximalBPS.ActualRootCommutation.actual_same_root_inverse_commutation']
for i,cell_id in enumerate([shared,cid]):
    c=copy.deepcopy(load(Path('research-wiki/frontier-cells')/(parent+'.json')))
    assert c['status']=='independently_verified'
    header=(pre/f'header{i}-expanded.lean').read_text(encoding='utf-8');signature=header[header.index('theorem '):]
    c.update(cell_id=cell_id,title=['Sharp quadratic corrector bound from a selfadjoint square identity','Same actual PBPS sharp first-corrector energy and LemmaB3 consumer'][i],
        source_anchor=source,target_statement=signature,status='claimed',parents=[] if i==0 else [parent,shared],
        consumers=[names[1]] if i==0 else [names[2],'PBPS LemmaB4 one-step hypocoercivity; unproved'],
        blocked=dict(status=False,reason='Independent source-first headers sealed and type formed; mathematics not yet proved.'),
        evidence=dict(substantive_advance=aid,statement_seal=(pre/'root.statement-seal68.json').as_posix(),focused_checks=[],owned_files=files,truth_boundary=boundary),
        source_targets=[names[i]])
    c['shared_floor_audit']=dict(searched=searched,classification='missing' if i==0 else 'adapt',
        decision='new_canonical_shared' if i==0 else 'adapt_existing',canonical_declaration=names[0] if i==0 else reused[0],
        canonical_shared_cell=shared if i==0 else parent,reason='One general sharp Hilbert block estimate with an actual original-input PBPS consumer; same witnesses retained.')
    c['reuse_plan']=dict(searched_existing=searched,reused_declarations=[] if i==0 else reused,
        new_shared_declarations=[names[0]],known_consumers=[names[1],names[2]],planned_consumers=c['consumers'],
        no_duplicate_wrapper=True,decision_reason=c['shared_floor_audit']['reason'])
    c['statement_seal']=dict(evidence=(pre/'root.statement-seal68.json').as_posix(),source_revision='2609.06905v1/Lean4.33.0/Mathlibdb584cd6',
        statement_version=1,signature_digest=sha(signature.encode()),binder_audit=(pre/'independent-header-source68/complete-RAW-verdict.json').as_posix(),
        definition_kind='Generic exact selfadjoint square identity' if i==0 else 'Full literal Prop with SAME actual callers and complete internal witnesses; no additional paper premise')
    c['source_proof_coverage']=dict(source_graph=seal['source_graph'],source_inventory=(base/'pbps-first-corrector-energy-preproof67/independent-primary67/source-coverage-inventory.json').as_posix(),
        coverage_report=(pre/'independent-header-source68/complete-RAW-verdict.json').as_posix(),coverage_status='Reused independently closed primary graph;344/344 exact math items over6 RAW regions;21 new header/source slots accepted before68 proof search.')
    c['source_detail_audit'].update(primary_anchor=source,fidelity_boundary=boundary,gap='Sharp energy bound and modified-energy equivalence unproved.',source_preread=seal['source_graph'],
        consulted=[dict(source='PBPSv1 pinned primary and fixed Mathlib',anchor='B19/B20/B22/B23/B24',hypothesis_adapter='K/Inv square identity and norm budget produced internally from SAME actual inputs.',expanded_binder_audit=(pre/'independent-header-source68/complete-RAW-verdict.json').as_posix())])
    c['proof_digestion']=dict(existing_substrate=reused,bookkeeping=['Exact same Gamma/Inv/A0/HP0/fP/fV; original input parameters unchanged.'],new_reusable=[names[0]],new_topology=delta)
    c['purification']=dict(status='pending',dead_code_audit='One useful leaf and actual integration/Test planned; no private mathematical provider.',duplicate_semantics_audit='Canonical67 roots/inverse reused; production never imports Tests.',canonicalization='Same actual PBPS corrector.',compressed_spine_delta=delta,reader_default_view='Complete attributed formulas with adjacent exact folded Lean.',scope=boundary)
    lc=c['learning_contract'];lc['failure_class']='IMPLEMENTATION_FAILED'
    lc['salvage']=dict(required=True,status='completed',reason='Reviewed full literal Prop staging and omegaWeight alpha-name adopted before proof search; no68 proof failures yet.',promoted_fragments=[],discarded_fragments=[])
    lc['parallelism'].update(decision='serial',direction_fingerprints=['same-actual-corrector/sharp-block-square/modified-energy'],shared_verified_context_digest=load(prior/'root.exact-verification67.adoption.json')['native_whole_logical_run_sha256'],expected_information_gain='One proof writer; independent math, blind decoder and source review retain separate uncertainty.')
    lc['reader_backpressure'].update(purification_status='pending',exposition_seal_status='pending',exposition_evidence='',lean_expansion_nodes=names)
    c['graph_contribution'].update(lean_view='integration-node',overview_view='updated',functor_view='none-found',focus_targets=[names[i]],visual_review='Pending68 proof/review; no graph extension blocks mathematics.')
    c['conceptual_mirror_audit']=dict(status='pending',discovery_ids=[],reason='Audit before PROVED_LOCAL; no conceptual transport certified.')
    w(Path('research-wiki/frontier-cells')/(cell_id+'.json'),c)
w(r/'preproof-admission.json',dict(status='CLAIMED_EXPLORING_NOT_PROVED',actual_root_pid=os.getpid(),checked_parent=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),statement_seal=(pre/'root.statement-seal68.json').as_posix(),theorem_delta=delta,truth_boundary=boundary,active_cells=[shared,cid],production_declarations=names[:2],test_declaration=names[2]))
print(aid,'EXPLORING; independent header68 seal retained; one owner and no proof credit.')
