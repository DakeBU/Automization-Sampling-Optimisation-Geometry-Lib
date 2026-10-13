from pathlib import Path
import json,hashlib,subprocess,os,sys,datetime,re
R=Path('E:/Samplinglib');O=R/'runs/20261007-companion-priority/pbps-actual-physical-time-cover79/independent-math79'
def info(p):
 p=Path(p);b=p.read_bytes();return dict(path=str(p),RAW_bytes=len(b),RAW_sha256=hashlib.sha256(b).hexdigest())
def load(p):return json.loads(p.read_text(encoding='utf-8'))
def save(n,v):
 p=O/n;assert not p.exists();p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
rec=load(O/'fresh-whole-module-attempt2.receipt.json');assert rec['exit_code']==0 and rec['terminal_closed']
for e in rec['inputs']+[rec['stdout'],rec['stderr']]:assert info(e['path'])['RAW_sha256']==e['RAW_sha256']
log=(O/'fresh-whole-module-attempt2.stdout.log').read_text(encoding='utf-8')
names=[x.strip() for x in re.search(r'depends on axioms:\s*\[([^\]]+)\]',log,re.S).group(1).split(',')]
assert set(names)=={'propext','Classical.choice','Quot.sound'}
save('dependency-closure-attempt1-diagnosis79.json',dict(classification='VERIFIER_RESERVED_IDENTIFIER',finding='Dependency-only probe used Lean reserved command prefix as a local variable. New immutable probe alpha-renames it to proofStem. Complete-source attempt2 is already EXIT0. No source or proof changed.',receipt=info(O/'kernel-local-proof-closure.receipt.json')))
probe=O/'KernelLocalProofClosure79.alpha.lean';assert not probe.exists()
probe.write_text('''import AutoSamplingTheory.ExampleCases.ProximalBPS.ActualPhysicalTimeCover
open Lean Elab Command in
run_cmd do
  let env ← getEnv
  let proofStem := "AutoSamplingTheory.ExampleCases.ProximalBPS.ActualPhysicalTimeCover.actual_fixed_reference_physical_time_cover"
  let mut todo := #[`AutoSamplingTheory.ExampleCases.ProximalBPS.ActualPhysicalTimeCover.actual_fixed_reference_physical_time_cover]
  let mut seen : Array Name := #[]
  let mut externalDeps : Array Name := #[]
  while !todo.isEmpty do
    let name := todo.back!
    todo := todo.pop
    if !seen.contains name then
      seen := seen.push name
      logInfo m!"LOCAL_PROOF_CONSTANT {name}"
      let some ci := env.find? name | throwError "Missing local proof constant"
      let some value := ci.value? true | throwError "Missing local proof value"
      for dep in value.getUsedConstants do
        if dep.toString.startsWith proofStem then
          todo := todo.push dep
        else if dep.toString.startsWith "AutoSamplingTheory." && !externalDeps.contains dep then
          externalDeps := externalDeps.push dep
          logInfo m!"EXTERNAL_ASTIS_DEPENDENCY {dep}"
  logInfo m!"LOCAL_PROOF_CONSTANT_COUNT {seen.size}"
''',encoding='utf-8')
env=dict(os.environ,PYTHONUTF8='1');env.pop('ELAN_TOOLCHAIN',None)
cmd=[str(R/'.astis/toolchain/lean-4.33.0-windows/bin/lake.exe'),'env',str(R/'.astis/toolchain/lean-4.33.0-windows/bin/lean.exe'),str(probe)]
start=datetime.datetime.now(datetime.timezone.utc).isoformat()
with (O/'kernel-local-proof-closure-attempt2.stdout.log').open('xb') as out,(O/'kernel-local-proof-closure-attempt2.stderr.log').open('xb') as err:
 child=subprocess.Popen(cmd,cwd=R,env=env,stdout=out,stderr=err);print('Local-proof dependency closure foreground PID',child.pid,flush=True);code=child.wait()
save('kernel-local-proof-closure-attempt2.receipt.json',dict(command=cmd,actual_foreground_PID=child.pid,exit_code=code,terminal_closed=True,started_utc=start,
 finished_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),inputs=rec['inputs']+[info(probe)],
 stdout=info(O/'kernel-local-proof-closure-attempt2.stdout.log'),stderr=info(O/'kernel-local-proof-closure-attempt2.stderr.log'),scope='Inspect imported complete kernel BODY dependency closure through generated local proofs; fresh complete-source elaboration recorded separately.'))
assert code==0
closure=(O/'kernel-local-proof-closure-attempt2.stdout.log').read_text(encoding='utf-8')
deps=re.findall(r'EXTERNAL_ASTIS_DEPENDENCY (\S+)',closure)
expected=['AutoSamplingTheory.ExampleCases.ProximalBPS.ActualFiniteJumpRecursion.actual_fixed_reference_finite_jump_recursion','AutoSamplingTheory.ExampleCases.ProximalBPS.ActualNonaccumulation.actual_fixed_reference_event_time_nonaccumulation']
assert set(deps)==set(expected),deps
sys.path[:0]=[str(R),str(R/'tools')];from tools import astis
hits=astis.forbidden_pattern_hits();M=R/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualPhysicalTimeCover.lean'
save('fake-closure-scan79.json',dict(reviewer='/root/exact_verify77',algorithm='tools.astis.forbidden_pattern_hits same production scan as astis.py check',scanned_files=len(astis.lean_source_files()),hits=hits,module=info(M),aggregate_Lake_gate_not_run=True))
assert not hits
save('fresh-compiler-dependency-summary79.json',dict(status='PASS_FULL_SOURCE_STANDARD_THREE_EXACT_ACTUAL_PARENTS',module=info(M),axioms=names,
 direct_ASTIS_dependencies=deps,local_generated_proof_constants=re.findall(r'LOCAL_PROOF_CONSTANT (\S+)',closure),
 public_stochastic_provider_premises=[],receipt=info(O/'fresh-whole-module-attempt2.receipt.json'),dependency_closure_receipt=info(O/'kernel-local-proof-closure-attempt2.receipt.json'),
 direct_unused_import='UnitExponentialProduct imported explicitly but no direct BODY dependency; actual78 already supplies input-event escape. Optional later import cleanup only.',
 fake_closure_scan=info(O/'fake-closure-scan79.json'),proof_reviewer='/root/exact_verify77',source_review=False,VERIFIED=False,Goal_complete=False))
print('FRESH SOURCE / AXIOMS / LOCAL PROOF CLOSURE / FAKECLOSURE PASS',flush=True)
