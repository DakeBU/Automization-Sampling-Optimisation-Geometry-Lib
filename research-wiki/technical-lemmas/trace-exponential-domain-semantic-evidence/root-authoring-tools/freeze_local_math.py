from pathlib import Path
import json,hashlib,subprocess,os,gzip,sys
r=Path.cwd();w=r/'.astis/huanjian-gc-trace-mgf-domain-20261115'
E='research-wiki/technical-lemmas/trace-exponential-domain-semantic-evidence/'
e=r/E;c=r/'research-wiki/frontier-cells/ASTIS-SHARED-REAL-TRACE-EXPONENTIAL-DOMAIN.json'
P='AutoSamplingTheory/TechnicalLemmas/Analysis/MatrixTraceExponentialBounds.lean'
T='Tests/GaussianComplexityTraceMgfDomain.lean'
sha=lambda b:hashlib.sha256(b).hexdigest()
env=dict(os.environ,GIT_OPTIONAL_LOCKS='0')
git=lambda *a:subprocess.check_output(['git',*a],env=env)
base='1db9b48ff3572a159608dce9b062cc0ed841d633'
assert git('rev-parse','HEAD').decode().strip()==base
assert not git('diff','--cached','--name-only','-z')
assert sha((r/P).read_bytes())=='1ef6f49fa5f0a8b3b61ba42d31bca1bb744bebb64e433075d0ca25ab82570b76'
assert sha((r/T).read_bytes())=='72311555e65cacc8b129510f2158abc9e2e6a230882a2169f6504e80f394fedb'
for path,candidate in [(P,'P.candidate.v2.txt'),(T,'T.candidate.v2.txt')]:
    assert (w/candidate).read_text() in (r/path).read_text()
    assert 'sorry' not in (r/path).read_text() and 'axiom ' not in (r/path).read_text()
records=[];originals=e/'local-math-originals';originals.mkdir(parents=True,exist_ok=True)
for p in sorted((r/'.astis/huanjian-resume-20261103').glob('*-gc-trace-*.receipt.json')):
    x=json.loads(p.read_text());log=Path(x['log']);raw=log.read_bytes();assert sha(raw)==x['log_sha256']
    dest=originals/p.name
    if dest.exists():assert dest.read_bytes()==p.read_bytes()
    else:dest.write_bytes(p.read_bytes())
    compressed=originals/(log.name+'.gz');b=gzip.compress(raw,mtime=0)
    if compressed.exists():assert gzip.decompress(compressed.read_bytes())==raw
    else:compressed.write_bytes(b)
    records.append({'receipt':str(dest.relative_to(r)),'receipt_sha256':sha(dest.read_bytes()),
      'original_log':x['log'],'lossless_log_gzip':str(compressed.relative_to(r)),
      'decoded_log_sha256':sha(raw),'actual_exit_code':x['exit_code'],'actual_command':x['command'],
      'actual_HEAD_before':x['head_before'],'actual_HEAD_after':x['head_after']})
focused=[]
for label in ['P-production-focused-module-build','T-production-focused-module-build']:
    found=[v for v in records if label in v['receipt']];assert len(found)==1 and found[0]['actual_exit_code']==0
    focused.append(found[0])
g=json.loads((w/'preservation-baseline.private.json').read_text())
for p,h in g['all_existing_frontier_sha256'].items():assert sha((r/p).read_bytes())==h
sys.path.insert(0,str(r));from tools import astis_advance as api
assert api.current_advances()['ASTIS-SA-20261115-TraceExponentialDomain']['state']=='EXPLORING'
assert api.current_advances()['ASTIS-SA-20261114-MatrixLaplaceTail']['state']=='VERIFIED'
checkpoint={'status':'ACTUAL_LOCAL_P_AND_LITERAL_PRIVATE_T_PROOFS_COMPILED_NO_NORMAL_PL_OR_INDEPENDENT_V_YET',
 'result_kind':'theorem-edge','source_P':{'file':P,'sha256':sha((r/P).read_bytes()),'lines':60},
 'private_T':{'file':T,'sha256':sha((r/T).read_bytes()),'lines':183,'public_node':False},
 'mathematical_delta':'All-real strict trace-exponential/cardinality/operator-norm bound and its literal original-Gaussian four-family pointwise cap/scalar integrability/positive capped ordinary expectation consumer. No regularity/radius/positivity result was added as a public consumer premise.',
 'actual_focused_builds':focused,'all_actual_root_records':records,
 'actual_build_identity_qualification':'Root compiled these exact owned worktree bytes while HEAD was1db9; those new files were not in bare1db9. The upcoming source commit freezes these bytes. No independent fresh build of that future commit has yet occurred.',
 'source_review':'Independent preproof admission only. Postproof decoder/fresh source/wholemodule/native/current reader/purification remain pending.',
 'native_axiom_type_value_kernel_audit':'PENDING; compiler success alone is not a completed independent audit.',
 'normal_PL_calls':0,'normal_V_calls':0,'Root_source_or_paper_completion_claimed':False,
 'truth_boundary':'Scalar E trace exp domain only, no full matrix MGF/Lieb/Jensen/master-tail/Bernstein/norm-tail/C6/main lowerbound/oracle/precision/cost or integration completion.'}
(e/'local-mathematics-checkpoint.v1.json').write_text(json.dumps(checkpoint,ensure_ascii=False,indent=2)+'\n')
cell=json.loads(c.read_text());assert cell['status']=='claimed'
cell['reuse_plan']['new_shared_declarations_status']='ACTUAL_LOCAL_WORKTREE_COMPILED_P_AND_PRIVATE_T; INDEPENDENT_DEPENDENCY_REVIEW_PENDING'
cell['reuse_plan']['known_consumers']=['AutoSamplingTheory.Tests.GaussianComplexityTraceMgfDomain.actual_source_four_trace_mgfs_integrable_positive_and_bounded']
cell['reuse_plan']['decision_reason']='One actual compiled deterministic shared P is materially consumed for strict positivity and exact dimension/operator-norm envelope in the private literal four-family T. Public P source imports only pinned Mathlib; exact native value dependencies remain pending. No separate public T credit.'
cell['evidence']['focused_checks']=[v['receipt'] for v in focused]
cell['evidence']['actual_local_mathematics']=str((e/'local-mathematics-checkpoint.v1.json').relative_to(r))
cell['evidence']['current_normal_stage'].update({'local_P_and_private_T_compiled':True,'theorem_PROVED_LOCAL':False,'theorem_VERIFIED':False})
cell['phase_snapshot']='One normal EXPLORING owner; exact admitted P and literal private four-family T compiled locally from owned worktree bytes. Postproof publication/semantic/native/reader and normalPL/V remain pending.'
c.write_text(json.dumps(cell,ensure_ascii=False,indent=2)+'\n')
for name in ['form_candidate_interfaces.py','form_minimal_interfaces_v2.py','seal_minimal_interfaces.py','audit_statement_norm_scope.py','author_conceptual_envelope_audit.py','intake_once.py','write_P_proof_attempt1.py','write_T_proof_attempt1.py','freeze_local_math.py']:
    p=e/'root-authoring-tools'/name;p.parent.mkdir(parents=True,exist_ok=True);assert not p.exists();p.write_bytes((w/name).read_bytes())
allowed={P,T,str(c.relative_to(r)),'research-wiki/technical-lemmas/trace-exponential-domain-statement-seal.json','runs/substantive_advances.jsonl','runs/substantive_discoveries.jsonl'}
paths={p.decode() for p in git('diff','--name-only','-z').split(b'\0') if p}
paths|={p.decode() for p in git('ls-files','--others','--exclude-standard','-z','--',P,T,str(c.relative_to(r)),'research-wiki/technical-lemmas/trace-exponential-domain-statement-seal.json',E).split(b'\0') if p}
assert paths and all(p in allowed or p.startswith(E) for p in paths),sorted(paths)
for p in sorted(paths):subprocess.run(['git','add','--',p],env=env,check=True)
assert {p.decode() for p in git('diff','--cached','--name-only','-z').split(b'\0') if p}==paths
subprocess.run(['git','diff','--cached','--check'],env=env,check=True)
subprocess.run(['git','commit','-m','Prove all-real trace exponential envelope and actual Gaussian domains'],env=env,check=True)
commit=git('rev-parse','HEAD').decode().strip();assert commit!=base
assert not git('status','--porcelain','--untracked-files=no').strip()
(w/'immutable-math.v1.json').write_text(json.dumps({'commit':commit,'parent':base,'P_sha256':sha((r/P).read_bytes()),'T_sha256':sha((r/T).read_bytes()),'actual_focused_builds_at_worktree_HEAD':base,'normal_PL_calls':0,'normal_V_calls':0,'independent_native_commit_build_pending':True},indent=2)+'\n')
print(json.dumps({'immutable_math_commit':commit,'P_lines':60,'T_lines':183,'actual_local_proof_builds':2,'normal_PL':0,'normal_V':0,'R15_verified_public_result_preserved':True}))
