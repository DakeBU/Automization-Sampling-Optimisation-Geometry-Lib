"""One normal next-packet intake after independent preproof admission and R15 push."""
from pathlib import Path
import sys,json,hashlib,datetime,subprocess,os
r=Path.cwd();w=r/'.astis/huanjian-gc-trace-mgf-domain-20261115'
sys.path.insert(0,str(r));from tools import astis_advance as api
E='research-wiki/technical-lemmas/trace-exponential-domain-semantic-evidence'
e=r/E;c=r/'research-wiki/frontier-cells/ASTIS-SHARED-REAL-TRACE-EXPONENTIAL-DOMAIN.json'
A='ASTIS-SA-20261115-TraceExponentialDomain';O='huanjian_20261115_trace_exponential_domain'
D='ASTIS-DISC-20261115-ScalarSelfadjointExponentialEnvelope'
sha=lambda b:hashlib.sha256(b).hexdigest()
read=lambda p:json.loads(p.read_text())
digest=lambda x:sha(json.dumps(x,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode())
env=dict(os.environ,GIT_OPTIONAL_LOCKS='0')
git=lambda *a:subprocess.check_output(['git',*a],env=env,text=True).strip()
assert not (w/'intake-attempted.once.json').exists(),'Inspect actual canonical ledgers before any retry.'
g=read(w/'preservation-baseline.private.json')
assert git('rev-parse','HEAD')==g['source_HEAD']=='1db9b48ff3572a159608dce9b062cc0ed841d633'
assert git('rev-parse','refs/heads/huanjian/gaussian-progress-public-20261114')==g['safe_public_ref']
assert not c.exists() and not e.exists()
seal=read(w/'statement-seal.sealed.v1.json')
assert sha((w/'statement-seal.sealed.v1.json').read_bytes())=='baac7a9074f869cdd98c6a027176f7d33ec7531c60f0a4709f0fc01bf81ee04d'
assert sha((w/'norm-scope-seal-supplement.v1.json').read_bytes())=='8bfdff76c638b419b502c667fcc3959fee50532f46a28e9df5fb45d846e97fd5'
tc=r/'.astis/semantic-neutral-20261115/trace_mgf_topology_29a6/preproof-topology-review.v1.json'
assert sha(tc.read_bytes())=='8e9c936125e699a4e616f61ccf58b3b8ffff0e5f8e7dc6109bd8e921aebb921b'
assert read(tc)['verdict']=='ADMITTED'
for key,file in [('canonical_producer','P.candidate.v2.txt'),('private_real_consumer','T.candidate.v2.txt')]:
    assert sha((w/file).read_bytes())==seal[key]['sha256']
    assert not (r/seal[key]['file']).exists()
for p,h in g['all_existing_frontier_sha256'].items():assert sha((r/p).read_bytes())==h
before_a=(r/'runs/substantive_advances.jsonl').read_bytes();before_d=(r/'runs/substantive_discoveries.jsonl').read_bytes()
for b,k in [(before_a,'advance_prefix'),(before_d,'discovery_prefix')]:
    assert b.endswith(b'\n') and len(b)==g[k]['bytes'] and sha(b)==g[k]['sha256']
states_a=api.current_advances();states_d=api.current_discoveries()
assert A not in states_a and D not in states_d
assert {k:digest(v) for k,v in states_a.items()}==g['all_existing_advance_state_digests']
assert {k:digest(v) for k,v in states_d.items()}==g['all_existing_discovery_state_digests']
proposal=read(w/'metadata-drafts/proposal-kwargs.candidate.v1.json')
# These are existing candidate inputs, not fabricated declaration strings and
# not a claim about compiled value dependencies. The newly produced P is not
# an input of its own advance.
proposal['dag_inputs']=[
 'Matrix.IsHermitian.cfc_eq',
 'AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumSourceMatrixRadius.actual_source_truncated_matrix_norm_bounds',
 'AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumSourceMatrixStructure.actual_source_centered_matrix_structure']
proposal['modes']=['source-review','library-retrieval','proof-design','compiler-diagnosis']
api.AdvanceProposal(**proposal).validate()
mirror=read(w/'conceptual-mirror-proposal.authored-v1.json')
assert mirror['advance_id']==A and mirror['discovery_id']==D and mirror['created_by']==O
api.Discovery(**mirror).validate()
cell=read(w/'metadata-drafts/frontier-cell.candidate.v1.json')
for key in ['draft_only','registration_pending','draft_status_qualification']:cell.pop(key,None)
cell['base_commit']=g['source_HEAD']
cell['base_commit_scope']='Actual next-intake source baseline after R15 independently verified public push. Original type/seal context3fdf preserved; only R15 metadata/evidence changed through1db9.'
cell['status']='queued'
cell['owned_files']=proposal['proposed_files']
cell['forbidden_shared_files']=['AutoSamplingTheory.lean','Tests.lean','AutoSamplingTheory/TechnicalLemmas/Analysis.lean','AutoSamplingTheory/TechnicalLemmas/Registry.lean','research-wiki/source-index/','website/content/source_correspondence.json','website/content/graph_memory_index.json','website/content/functor_hypergraph.json','website/static/','website/scripts/','AutoSamplingTheory/TechnicalLemmas/Probability/MatrixLaplaceTail.lean','Tests/GaussianComplexityLaplaceTail.lean','research-wiki/frontier-cells/ASTIS-SHARED-REAL-MATRIX-LAPLACE-TAIL.json','research-wiki/technical-lemmas/matrix-laplace-tail-semantic-evidence/']
cell['learning_contract']['process_memory_ids']=['ASTIS-PM-QUADRATIC-TILT-MEASURE-ROLES','ASTIS-NK-GRADIENT-FLOW-ZERO-TIME','ASTIS-NK-GD-INVERSE-DOMAIN']
cell['learning_contract']['process_memory_scope']='ROOT read the actual three-entry registry; none supplies a mathematical conclusion or retires this new target. Existing one-sided-MGF failure boundary is separately cited in the authored conceptual audit.'
cell['phase_snapshot']='Independent preproof admission only; new normal intake in progress; no target implementation or proof yet.'
e.mkdir(parents=True)
for src,dst in [
 (w/'statement-seal.sealed.v1.json',r/'research-wiki/technical-lemmas/trace-exponential-domain-statement-seal.json'),
 (w/'binder-definition-audit.sealed.v1.json',e/'binder-definition-audit.original.v1.json'),
 (w/'norm-scope-seal-supplement.v1.json',e/'norm-scope-seal-supplement.v1.json'),
 (w/'preproof-admission.v1.json',e/'preproof-source-admission.json'),
 (w/'conceptual-mirror-proposal.authored-v1.json',e/'conceptual-mirror-proposal.authored-v1.json'),
 (w/'conceptual-mirror-and-process-audit.authored-v1.json',e/'conceptual-mirror-and-process-audit.authored-v1.json')]:
    assert not dst.exists();dst.write_bytes(src.read_bytes())
cell['statement_seal']['file']='research-wiki/technical-lemmas/trace-exponential-domain-statement-seal.json'
cell['statement_seal']['binder_audit']=str((e/'binder-definition-audit.original.v1.json').relative_to(r))
cell['statement_seal']['norm_scope_supplement']=str((e/'norm-scope-seal-supplement.v1.json').relative_to(r))
c.write_text(json.dumps(cell,ensure_ascii=False,indent=2)+'\n')
(w/'intake-attempted.once.json').write_text(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'planned_normal_calls':['raw typed conceptual Discovery','proposal','CLAIMED','EXPLORING'],'target_proof_calls_before_admission':0},indent=2)+'\n')
api.publish_discovery(api.Discovery(**mirror))
cell['conceptual_mirror_audit']={'status':'candidates-published','discovery_ids':[D],
 'evidence':str((e/'conceptual-mirror-and-process-audit.authored-v1.json').relative_to(r)),
 'scope':'Actual raw typed candidate only. Creator does not validate it; no formal transport/global graph or mathematical V.'}
cell['graph_contribution']['functor_view']='candidate-published'
cell['graph_contribution']['classification_qualification']='One actual raw typed candidate under the existing bounded-single-variable-laplace family. Compiler parents/consumer, validation and global graph stabilization remain pending.'
c.write_text(json.dumps(cell,ensure_ascii=False,indent=2)+'\n')
api.propose_advance(api.AdvanceProposal(**proposal))
admission=read(w/'preproof-admission.v1.json')
api.transition_advance(A,'CLAIMED',worker_id=O,evidence={'preproof_admission':admission})
api.transition_advance(A,'EXPLORING',worker_id=O,modes=['proof-design','library-retrieval','compiler-diagnosis'],evidence={'preproof_admission':admission,'proof_implementation_not_started':True})
after_a=(r/'runs/substantive_advances.jsonl').read_bytes();after_d=(r/'runs/substantive_discoveries.jsonl').read_bytes()
assert after_a.startswith(before_a) and after_d.startswith(before_d)
da=[json.loads(q) for q in after_a[len(before_a):].splitlines()]
dd=[json.loads(q) for q in after_d[len(before_d):].splitlines()]
assert len(da)==3 and all(q['advance_id']==A for q in da)
assert len(dd)==1 and dd[0]['discovery_id']==D and dd[0]['status']=='raw'
now_a=api.current_advances();now_d=api.current_discoveries()
assert {k:v for k,v in now_a.items() if k!=A}==states_a
assert {k:v for k,v in now_d.items() if k!=D}==states_d
for p,h in g['all_existing_frontier_sha256'].items():assert sha((r/p).read_bytes())==h
cell['status']='claimed'
cell['evidence']['current_normal_stage']={'advance_state':'EXPLORING','cell_status':'claimed','normal_intake_pending':False,'normal_advance_intake_calls':3,'raw_conceptual_Discovery_calls':1,'theorem_PROVED_LOCAL':False,'theorem_VERIFIED':False}
cell['phase_snapshot']='One actual normal proposal/claim/exploring plus one raw typed conceptual Discovery after independent preproof admission; target proof not yet started. All proof/semantic/native/reader/V stages remain pending.'
c.write_text(json.dumps(cell,ensure_ascii=False,indent=2)+'\n')
(e/'normal-intake-advance-append.exact.jsonl').write_bytes(after_a[len(before_a):])
(e/'normal-intake-discovery-append.exact.jsonl').write_bytes(after_d[len(before_d):])
result={'state':now_a[A]['state'],'owner':now_a[A]['owner_id'],'normal_advance_intake_calls':3,'raw_Discovery_calls':1,'target_proof_calls_before_admission':0,
 'all316_prior_advance_states_unchanged':True,'all45_prior_discovery_states_unchanged':True,'all475_prior_frontiers_unchanged':True,'old_ledger_prefixes_exact':True,
 'R15_verified_and_public_result_preserved':True,'no_new_Goal_background_ASTIS_or_owner_takeover':True}
(e/'normal-intake-result.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result))
