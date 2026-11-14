from pathlib import Path
import hashlib,json,subprocess
W=Path(__file__).resolve().parent.relative_to(Path.cwd())
E=Path('research-wiki/paper-contributions/GaussianComplexity/source-gram-realization-semantic-evidence')
C=Path('research-wiki/frontier-cells/ASTIS-SW-GAUSSIAN-COMPLEXITY-source-gram-realization.json')
P=Path('AutoSamplingTheory/ExampleCases/GaussianComplexity/FixedSpectrumSourceGramRealization.lean')
T=Path('Tests/GaussianComplexityFixedSpectrumSourceGramRealization.lean')
sha=lambda b:hashlib.sha256(b).hexdigest()
dump=lambda o:(json.dumps(o,ensure_ascii=False,indent=2)+'\n').encode()
git=lambda *a:subprocess.check_output(['git',*a])
def create(p,b):
    p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('xb') as f:f.write(b)
head=git('rev-parse','HEAD').decode().strip();assert head=='de206b055cb8589c4c760b62209741ac62ad243a'
assert not git('diff','HEAD','--name-only') and not git('diff','--cached','--name-only')
expected={P:'b68d9d7d6e385355391a8bf93653e9bbee1843be897f63563e0aa8af0e91d537',T:'ac57194ab0cff3708609549581146a1fca91ec31dea2d6fbce95260158e616e5'}
seal=json.loads((W/'statement-seal-v1.unclaimed.json').read_bytes())
for (p,h),k in zip(expected.items(),['producer','actual_private_consumer']):
    assert sha(p.read_bytes())==h and seal[k]['signature'] in p.read_text()
dest=E/'math-originals'
for p in sorted(W.iterdir()):
    if not p.is_file() or '.private.' in p.name or p.suffix not in {'.py','.lean','.txt','.json'}:continue
    b=p.read_bytes()
    if p.suffix=='.json':
        v=json.loads(b)
        if isinstance(v,dict):assert not set(v)&{'tracked_git_index','all_foreign_states','all_existing_tracked_fingerprints','actual_control_fingerprints'}
    create(dest/'task-files'/p.name,b)
for p in [P,T]:create(dest/('final-'+p.name),p.read_bytes())
runs=Path('.astis/huanjian-resume-20261103');receipts=[]
for rp in sorted(runs.glob('*source-gram-realization-*.receipt.json')):
    r=json.loads(rp.read_bytes());lp=Path(r['log']);assert sha(lp.read_bytes())==r['log_sha256']
    for f in [rp,lp]:create(dest/'actual-runs'/f.name,f.read_bytes())
    receipts.append({'file':str(dest/'actual-runs'/rp.name),'sha256':sha(rp.read_bytes()),'command':r['command'],'exit_code':r['exit_code'],'log_sha256':r['log_sha256'],'executed_HEAD':r['head_before']})
build=next(x for x in receipts if 'second-full-P-T-Lake-build-abstract-bias-algebra' in x['file']);strict=next(x for x in receipts if 'kernel-after-successful-full-build' in x['file'])
assert build['exit_code']==strict['exit_code']==0
log=(runs/'20261113T122411551128Z-source-gram-realization-exact-proof-value-kernel-after-successful-full-build.log').read_text()
assert 'ACTUAL_R12_ALL_OWNED_KERNEL_INSPECTED 4 HANDWRITTEN 2 GENERATED 2' in log
assert log.count('ACTUAL_R12_ROOT_PROOF_VALUE_SEALED_KERNEL_APPLICATION_PASS')==2
parents=['AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumSourceMatrixMean.actual_source_truncated_matrix_means','AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumCosineGram.actual_cosine_frame_gram']
record={'scope':'Actual local P and privateT mathematics, independent postproof semantic/native/reader reviews pending. Ledger remains EXPLORING.','executed_base_HEAD':head,'source_files':[{'path':str(p),'sha256':h,'lines':len(p.read_text().splitlines())} for p,h in expected.items()],'actual_runs':receipts,'actual_final_build':build,'actual_final_proof_value_kernel':strict,'sealed_statement_sha256':'7b2f71cf9e89a41da4f66b2b3908222c875cd2fec2f8b2ca6533fe61b3bb3ce9','canonical_P_parents':parents,'private_T_parents':[seal['producer']['name'],'AutoSamplingTheory.TechnicalLemmas.Probability.StdGaussianMoment.integrable_norm_sq_and_integral_stdGaussian'],'kernel':{'full_universal_root_proof_values_at_literal_sealed_types':2,'raw_literal_Expr_equalities':[False,False],'kernel_definitional_conversion':'passed','all_owned_type_value_rechecks':4,'handwritten':2,'generated':2,'all_owned_reachable':True,'nonstandard_axioms':[],'real_q0_applications':2},'iteration_qualification':'First P function-head feature alias caused Matrix dot-notation inference errors; proof-body alias retyped as definitionally identical Matrix. Second P removed redundant solved-goal rfl and exposed outer weighted entry before diagonal reduction. Private T replaced implicit-transparency entry ext with abstract module bias algebra and used two-component add_le_add. Exact signatures/objects/binders unchanged; all failures preserved. Full successful P/T Lake build0 preceded strict complete proof-value kernel0. Pre-API intake label/context errors retained; no intake API was replayed.','no_new_source_binders':True,'matrix_norm':'Actual real Euclidean L2Operator matrix norm; same topology as existing actual mean/frame APIs.','placement':'Public P actual centered/unweighted and weighted Gram identities on original G, private real-Delta Ex126 actual norm consequence; no publicT/probability/main credit.','build_commit_qualification':'Runs executed at the intake HEAD with exact listed worktree source bytes; future immutable math carrier is not retroactively claimed to be an executed build HEAD.'}
create(E/'local-math-candidate.json',dump(record))
cell=json.loads(C.read_bytes());cell['evidence']['local_math_candidate']={'file':str(E/'local-math-candidate.json'),'sha256':sha((E/'local-math-candidate.json').read_bytes()),'independent_semantic':'pending','independent_native':'pending'}
cell['evidence']['target_proof_calls_at_intake']=cell['evidence'].pop('target_proof_calls')
cell['statement_seal']['status']='EXACT_UNCHANGED_LITERAL_GRAM_TYPES;LOCAL_P_T_COMPILED;POSTPROOF_REVIEW_PENDING'
cell['reservation_only']='Normal ledger remains EXPLORING; actual local P/T proof values compiled, independent source/native/reader admission pending.'
cell['reuse_plan']['reused_declarations']=parents;cell['reuse_plan']['actual_private_consumer_parents']=[seal['producer']['name'],'AutoSamplingTheory.TechnicalLemmas.Probability.StdGaussianMoment.integrable_norm_sq_and_integral_stdGaussian']
C.write_bytes(dump(cell))
paths=[P,T,C,E/'local-math-candidate.json',*[p for p in sorted(dest.rglob('*')) if p.is_file()]]
spec=W/'math-candidate-paths.private.nul';create(spec,b'\0'.join(str(p).encode() for p in paths)+b'\0')
subprocess.run(['git','add','-f','--pathspec-from-file='+str(spec),'--pathspec-file-nul'],check=True)
assert set(git('diff','--cached','--name-only').decode().splitlines())==set(map(str,paths))
subprocess.run(['git','diff','--cached','--check','--',str(P),str(T),str(C)],check=True)
subprocess.run(['git','commit','--quiet','-m','Prove actual source Gaussian Gram identities and eventwise deviation bounds'],check=True)
commit=git('rev-parse','HEAD').decode().strip()
for p in paths:assert git('show',f'{commit}:{p}')==p.read_bytes()
out={'math_candidate_commit':commit,'executed_base_HEAD':head,'exact_owned_files':len(paths),'ledger_mutations':0,'ROOT_V_calls':0,'independent_postproof_acceptance':'pending'}
create(W/'actual-math-candidate-commit.json',dump(out));print(json.dumps(out))
