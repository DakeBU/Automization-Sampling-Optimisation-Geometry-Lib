from pathlib import Path
import datetime,hashlib,json,os,re,subprocess
R=Path('E:/Samplinglib');O=Path(__file__).parent;B=O.parent;H=B/'header84.proposed.lean';P=R/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualBoundedTestContinuity.lean'
def info(p):
 b=p.read_bytes();return dict(path=p.relative_to(R).as_posix(),RAW_bytes=len(b),RAW_sha256=hashlib.sha256(b).hexdigest())
def save(n,d):
 with (O/n).open('x',encoding='utf8',newline='\n') as f:json.dump(d,f,ensure_ascii=False,indent=2);f.write('\n')
def load(p):return json.loads(p.read_text(encoding='utf8'))
assert info(H)['RAW_sha256']=='936b76036df8d283acb212f2f1ba780c4446aa2e1c7dc84bfdff0ff9c02f29b0' and info(H)['RAW_bytes']==7652
assert info(P)['RAW_sha256']=='0a88a2071df983f791899b01b0de40f52241b06ba452eea3751e471396adec6b'
h=H.read_text(encoding='utf8');p=P.read_text(encoding='utf8')
def binders(t):
 a=t.index('    {E : Type*}');return t[a:t.index(' : Prop :=',a)]
def defs(t):
 a=t.index('    let ');z=t.index('    ∃ Z',a);parts=re.split(r'(?=^    let )',t[a:z],flags=re.M)
 return {re.match(r'    let (\S+) ',v)[1]:v.rstrip() for v in parts if v}
assert binders(h)==binders(p) and defs(h)==defs(p) and len(defs(h))==11
def prefix(t):
 a=t.index('    {E : Type*}');return t[a:t.index('\n\n\nset_option maxHeartbeats',a)]
assert prefix(h)==prefix(p)
assert h.count('private def ')==1 and not re.search(r'^theorem |\b(sorry|admit|axiom)\b',h,re.M)
S=R/'runs/20261007-companion-priority/pbps-outer-bounded-l2-preread84'
paths=[H,P,R/'lean-toolchain',R/'lake-manifest.json',R/'AutoSamplingTheory/ExampleCases/ProximalBPS/GibbsAugmentation.lean',R/'AutoSamplingTheory/TechnicalLemmas/Probability/GaussianConditionalKernel.lean',R/'AutoSamplingTheory/TechnicalLemmas/Probability/UnitExponentialProduct.lean',S/'source_freeze84.raw-manifest.json',S/'source_inventory84.json',S/'source_proof_graph84.json',S/'source_inventory84.reviewed-effective.json',S/'source_proof_graph84.reviewed-effective.json',S/'overlay-review84/topology-overlay.decision84.json',S/'overlay-review84/topology-overlay.run-manifest84.json']
for t in ['.lake/packages/mathlib/Mathlib/MeasureTheory/Integral/Prod.lean','.lake/packages/mathlib/Mathlib/MeasureTheory/Integral/DominatedConvergence.lean','.lake/packages/mathlib/Mathlib/MeasureTheory/Measure/Tilted.lean','.lake/packages/mathlib/Mathlib/Probability/Distributions/Gaussian/Multivariate.lean']:paths.append(R/t)
frozen=[info(q) for q in paths];mc=subprocess.check_output(['git','-C',str(R/'.lake/packages/mathlib'),'rev-parse','HEAD']).decode().strip();assert mc=='db584cd6d46c92f209a44c0f1c829460d327499d'
save('input-freeze84.json',dict(reviewer='/root/exact_verify77',created_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),inputs=frozen,fixed_mathlib_commit=mc,scope='Prospective full-header only; no84 BODY or proof credit.'))
save('definition-readback84.json',dict(status='PASS_LITERAL_AND_QUANTIFIER_REVIEW_PENDING_TYPECHECK',header=info(H),actual83=info(P),six_analytic_binders_exact=True,eleven_actual_definitions_exact=True,full83_private_Prop_prefix_exact_except_name=True,literal_definitions=defs(h),analytic_binders=binders(h),new_public_provider_premises=[],new_q_nu='Exact volume tilt(-V-quadratic), q times stdGaussian; probability outputs precede test binders.',new_test_quantifiers='For each fixed y,xRef, all continuous real f, all M>=0 globalbound, all finite t measured state expectation and genuine integrable squared discrepancy<=4M2; ordinary NNReal0 squared-integral limit.',syntax_concern='Inherited standalone set_option maxHeartbeats1600000 in occurs before appended conjunction, to be diagnosed on exact original.'))
snap=O/'header84.exactraw.lean'
with snap.open('xb') as f:f.write(H.read_bytes())
env=dict(os.environ,PYTHONUTF8='1',PYTHONIOENCODING='utf8');env.pop('ELAN_TOOLCHAIN',None)
args=[str(R/'.astis/toolchain/lean-4.33.0-windows/bin/lake.exe'),'env',str(R/'.astis/toolchain/lean-4.33.0-windows/bin/lean.exe'),str(snap)];start=datetime.datetime.now(datetime.timezone.utc).isoformat()
with (O/'original-typecheck84.stdout.log').open('xb') as out,(O/'original-typecheck84.stderr.log').open('xb') as err:
 child=subprocess.Popen(args,cwd=R,env=env,stdout=out,stderr=err);print('Exact original header foreground PID',child.pid,flush=True);code=child.wait()
save('original-typecheck84.receipt.json',dict(status='PASS' if code==0 else 'FAIL',command_argv=args,cwd=str(R),actual_foreground_PID=child.pid,exit_code=code,terminal_closed=True,start_utc=start,end_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),header=info(H),exact_snapshot=info(snap),stdout=info(O/'original-typecheck84.stdout.log'),stderr=info(O/'original-typecheck84.stderr.log'),complete_original_private_definition=True,proof_BODY=False))
for q,e in zip(paths,frozen):assert info(q)==e
print('EXACT ORIGINAL FULL HEADER EXIT',code,flush=True)
