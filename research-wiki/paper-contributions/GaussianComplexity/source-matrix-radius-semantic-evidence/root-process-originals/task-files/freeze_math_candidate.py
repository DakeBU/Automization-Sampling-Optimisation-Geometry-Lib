"""Carry the exact R10 mathematical candidate; no ledger transition or fidelity claim."""
from pathlib import Path
import hashlib, json, subprocess
W=Path(__file__).resolve().parent.relative_to(Path.cwd())
E=Path('research-wiki/paper-contributions/GaussianComplexity/source-matrix-radius-semantic-evidence')
C=Path('research-wiki/frontier-cells/ASTIS-SW-GAUSSIAN-COMPLEXITY-source-matrix-radius.json')
P=Path('AutoSamplingTheory/ExampleCases/GaussianComplexity/FixedSpectrumSourceMatrixRadius.lean')
T=Path('Tests/GaussianComplexityFixedSpectrumSourceMatrixRadius.lean')
sha=lambda b:hashlib.sha256(b).hexdigest()
dump=lambda o:(json.dumps(o,ensure_ascii=False,indent=2)+'\n').encode()
git=lambda *a:subprocess.check_output(['git',*a])
def create(p,b):
    p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('xb') as f:f.write(b)
head=git('rev-parse','HEAD').decode().strip()
assert head=='50097800f60ad4a95cab1e47be200b629ce5e7a6'
assert not git('diff','--name-only') and not git('diff','--cached','--name-only')
expected={P:'b81c079a78e08325cea951c38a62520e3c5dea19309673f02e050009d3483d31',T:'2984ec31b11fa446b6f8330cb964cb72d49252590f950acd88104c9e9a4e6dca'}
for p,h in expected.items():assert sha(p.read_bytes())==h
originals=E/'math-originals'
names=['RankOneNormDraft.lean','RankOneNormDraft.attempt1.original.lean','RankOneNormDraft.attempt2.original.lean','RankOneNormDraft.v3.passed.original.lean','IdentityTensorNormDraft.attempt1.original.lean','rankone-draft-attempt1-diagnosis.json','rankone-draft-attempt2-diagnosis.json','identity-tensor-attempt1-diagnosis.json','Producer.attempt1.original.lean','Producer.v2.first-passed.original.lean','producer-attempt1-diagnosis.json','producer-first-attempt-source.json','Consumer.first-passed.original.lean','consumer-first-attempt-source.json','first-P-T-local-pass.json','write_radius_producer.py','write_radius_consumer.py','make_radius_kernel_probe.py','FinalRadiusKernelProbe.lean','PostAdmissionAPIProbe.lean','freeze_math_candidate.py']
for n in names:create(originals/n,(W/n).read_bytes())
for p in [P,T]:create(originals/('final-'+p.name),p.read_bytes())
runs=Path('.astis/huanjian-resume-20261103')
receipts=[]
for rp in sorted(runs.glob('*source-matrix-radius-*.receipt.json')):
    if rp.name<'20261113T003300':continue
    r=json.loads(rp.read_bytes()); lp=Path(r['log'])
    assert sha(lp.read_bytes())==r['log_sha256']
    for p in [rp,lp]:create(originals/'actual-runs'/p.name,p.read_bytes())
    receipts.append({'receipt':str(originals/'actual-runs'/rp.name),'receipt_sha256':sha(rp.read_bytes()),'command':r['command'],'exit_code':r['exit_code'],'log_sha256':r['log_sha256'],'executed_head':r['head_before']})
assert any('final-P-T-Lake-build' in r['receipt'] and r['exit_code']==0 for r in receipts)
assert any('exact-proof-value-kernel-first' in r['receipt'] and r['exit_code']==0 for r in receipts)
strict=(runs/'20261113T010907901431Z-source-matrix-radius-exact-proof-value-kernel-first.log').read_text()
assert strict.count('ACTUAL_R10_ROOT_PROOF_VALUE_SEALED_KERNEL_APPLICATION_PASS')==2
assert 'ACTUAL_R10_ALL_OWNED_KERNEL_INSPECTED 7 HANDWRITTEN 5 GENERATED 2' in strict
parent='AutoSamplingTheory.ExampleCases.GaussianComplexity.'
summary={'scope':'Exact local mathematical candidate, independent semantic/native checks pending; no PROVED_LOCAL or VERIFIED API call.', 'executed_base_head':head,'executed_worktree_sources':[{ 'path':str(p),'sha256':h,'lines':len(p.read_text().splitlines())} for p,h in expected.items()], 'actual_runs':receipts,'kernel':{'complete_sealed_universal_proof_bodies_checked':2,'raw_literal_expr_equality':[False,False],'equality_meaning':'Kernel definitional equality passed for actual proof bodies at full sealed types; raw syntax equality is false and is not claimed.', 'owned_type_body_kernel_rechecks':7,'handwritten':5,'generated':2,'all_owned_root_reachable':True,'q_zero_real_applications':2,'nonstandard_axioms':[]}, 'canonical_ASTIS_P_parents':[parent+'FixedSpectrumSourceMatrixMean.actual_source_truncated_matrix_means',parent+'FixedSpectrumCosineGram.actual_cosine_frame_gram','AutoSamplingTheory.TechnicalLemmas.Probability.StdGaussianMoment.integrable_norm_sq_and_integral_stdGaussian'],'private_T_ASTIS_parent':parent+'FixedSpectrumSourceMatrixRadius.actual_source_truncated_matrix_norm_bounds','placement':'P is the sole public new canonical declaration. Three private representation/algebra helpers share P review. T is a real private Tests consumer with no public API/registry credit.', 'build_commit_qualification':'Actual runs above checked the stated source bytes at the intake HEAD. The following immutable carrier is not retroactively claimed to be their executed HEAD; a fresh native verifier must rebuild it.'}
create(E/'local-math-candidate.json',dump(summary))
c=json.loads(C.read_bytes())
c['evidence']['local_math_candidate']={'file':str(E/'local-math-candidate.json'),'sha256':sha((E/'local-math-candidate.json').read_bytes()),'independent_fidelity':'pending','independent_native':'pending'}
c['evidence']['target_proof_calls_at_intake']=c['evidence'].pop('target_proof_calls')
c['statement_seal']['status']='EXACT_SEALED_TYPES;LOCAL_MATH_COMPILED;INDEPENDENT_POSTPROOF_REVIEW_PENDING'
c['reservation_only']='Normal ledger remains EXPLORING; actual local proof bodies exist, independent semantic/native acceptance and publication admission pending.'
c['reader_contract']['status']='Local P/T mathematics compiled; authored formula proof, folded Lean, and independent reader acceptance pending. Global integration and production delivery remain open.'
c['graph_contribution']['visual_review']='Exact compiled local P parents and private T consumer recorded in local-math-candidate.json; no generated graph/runtime reader acceptance yet.'
c['learning_contract']['salvage']['reason']='All failed draft/proof attempts and diagnostics retained. Rank-one adapters, exact universal P and literal centered/weighted T compiled. No failed elaboration is treated as a mathematical counterexample.'
C.write_bytes(dump(c))
paths=[P,T,C,E/'local-math-candidate.json',*[p for p in sorted(originals.rglob('*')) if p.is_file()]]
manifest=[{'path':str(p),'sha256':sha(p.read_bytes()),'bytes':p.stat().st_size} for p in paths]
create(W/'math-candidate-files.json',dump(manifest))
spec=W/'math-candidate-paths.private.nul';create(spec,b'\0'.join(str(p).encode() for p in paths)+b'\0')
subprocess.run(['git','add','-f','--pathspec-from-file='+str(spec),'--pathspec-file-nul'],check=True)
assert set(git('diff','--cached','--name-only').decode().splitlines())==set(map(str,paths))
subprocess.run(['git','diff','--cached','--check','--',str(P),str(T),str(C)],check=True)
subprocess.run(['git','commit','--quiet','-m','Prove actual Gaussian summand and centered matrix radius bounds'],check=True)
commit=git('rev-parse','HEAD').decode().strip()
for p in paths:assert git('show',f'{commit}:{p}')==p.read_bytes()
result={'math_candidate_commit':commit,'parent':head,'byte_exact_files':len(paths),'ledger_mutations':0,'independent_acceptance':'pending','production_CSS_changed':False}
create(W/'actual-math-candidate-commit.json',dump(result))
print(json.dumps(result))
