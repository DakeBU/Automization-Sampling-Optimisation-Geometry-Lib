from pathlib import Path
import datetime,hashlib,json,os,subprocess,sys
R=Path('E:/Samplinglib');O=Path(__file__).parent;B=O.parent
M=R/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualFiniteHistoryTailLaw.lean'
MR='01fcff944f1dbd42be2af30063b9baf4e191e2cde959e008724387cadb4fc899'
D='AutoSamplingTheory.ExampleCases.ProximalBPS.ActualFiniteHistoryTailLaw.actual_finite_history_tail_law'
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def pin(p):
 p=Path(p);b=p.read_bytes();return dict(path=p.relative_to(R).as_posix(),raw_sha256=hashlib.sha256(b).hexdigest(),bytes=len(b))
def read(p):return json.loads(p.read_text('utf8'))
def put(n,x):
 with (O/n).open('x',encoding='utf8',newline='\n') as f:json.dump(x,f,ensure_ascii=False,indent=2);f.write('\n')
assert pin(M)['raw_sha256']==MR
seal=B/'root.statement-seal87.json';h=B/'header87.proposed.lean'
ss=read(seal);assert ss['expanded_literal_Prop'].encode() in M.read_bytes()
assert ss['header']['raw_sha256']==pin(h)['raw_sha256']=='1048a4bf0d171d52a2eb834f4281621e0101c8d4700c7eae60edc5e64cd3c39b'
slice=R/'runs/20261007-companion-priority/pbps-clock-tail-preread87/source-slice87.v2.json'
assert pin(slice)['raw_sha256']=='7c9873ef87bfb75c7a2ec86ecbb40b589384bc41bc197030acf7fa088fd611d9'
baseline=R/'runs/20261007-companion-priority/pbps-clock-tail-preread87/pre-fetch87.workspace-RAW.json';prior=read(baseline)['tracked_modified'];assert len(prior)==21
for p,v in prior.items():assert pin(R/p)['raw_sha256']==v
put('collaborator-preservation87.json',dict(baseline=pin(baseline),count=21,RAWs=[pin(R/p) for p in prior]))
inputs=[M,h,seal,slice,B/'focused/final-production8/receipt.json',B/'header-math87/decision87.json',B/'header-math87/closed-RAW-manifest87.json',R/'lean-toolchain',R/'lake-manifest.json',R/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualFiniteJumpRecursion.lean',R/'AutoSamplingTheory/TechnicalLemmas/Probability/UnitExponentialProduct.lean',R/'.lake/packages/mathlib/Mathlib/Probability/Independence/Basic.lean',R/'.lake/packages/mathlib/Mathlib/Probability/Independence/InfinitePi.lean',R/'.lake/packages/mathlib/Mathlib/MeasureTheory/MeasurableSpace/Basic.lean']
assert pin(R/'lean-toolchain')['raw_sha256']=='b2b5068d5a4835675e651ce83b29c0ddb308d28b80076e7c007aef4630af0477'
assert pin(R/'lake-manifest.json')['raw_sha256']=='b1f16b43aaf4a886cfe0382d5e3ae63d6904281c00afd8f35af20f0270a747e2'
head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=R,text=True).strip()
assert subprocess.check_output(['git','-C',str(R/'.lake/packages/mathlib'),'rev-parse','HEAD'],text=True).strip()=='db584cd6d46c92f209a44c0f1c829460d327499d'
put('input-freeze87.json',dict(status='FROZEN_BEFORE_INDEPENDENT_FULL_SOURCE_COMPILATION',created_utc=now(),reviewer_id='/root/exact_verify77',observed_head=head,current_frozen_module=pin(M),actual_inputs=[pin(p) for p in inputs],source_slice_only=True,no_final_source_or_decoder_verdict_read=True,whole_private_Prop_exact_seal=True,mathematical_role='Full BODY independent mathematics, distinct from prospective header acceptance; no VERIFIED or scientific commit admission.'))
with (O/'module87.exactraw.lean').open('xb') as f:f.write(M.read_bytes())
suffix='''
#print axioms AutoSamplingTheory.ExampleCases.ProximalBPS.ActualFiniteHistoryTailLaw.actual_finite_history_tail_law
#check AutoSamplingTheory.ExampleCases.ProximalBPS.ActualFiniteHistoryTailLaw.actual_finite_history_tail_law
open Lean Elab Command in
run_cmd do
  let env ← getEnv
  let isProject := fun n : Name => n.toString.startsWith "AutoSamplingTheory." ||
    (n.toString.startsWith "_private." && (n.toString.splitOn ".").contains "AutoSamplingTheory")
  let isLocal := fun n : Name => (n.toString.splitOn ".").contains "ActualFiniteHistoryTailLaw"
  let mut todo := #[`AutoSamplingTheory.ExampleCases.ProximalBPS.ActualFiniteHistoryTailLaw.actual_finite_history_tail_law]
  let mut seen : Array Name := #[]
  let mut externalDeps : Array Name := #[]
  let mut genericDeps : Array Name := #[]
  while !todo.isEmpty do
    let name := todo.back!
    todo := todo.pop
    if !seen.contains name then
      seen := seen.push name
      logInfo m!"LOCAL_PROOF_CONSTANT {name}"
      let some ci := env.find? name | throwError "Missing owned constant"
      let mut expressions := #[ci.type]
      if let some value := ci.value? true then
        expressions := expressions.push value
      else
        logInfo m!"LOCAL_NO_VALUE {name}"
      for expr in expressions do
        for dep in expr.getUsedConstants do
          if isLocal dep then
            logInfo m!"LOCAL_EDGE {name} -> {dep}"
            todo := todo.push dep
          else if isProject dep && !externalDeps.contains dep then
            externalDeps := externalDeps.push dep
            logInfo m!"EXTERNAL_ASTIS_DEPENDENCY {dep}"
          else if !isProject dep && !genericDeps.contains dep then
            genericDeps := genericDeps.push dep
            logInfo m!"GENERIC_DEPENDENCY {dep}"
  logInfo m!"LOCAL_PROOF_CONSTANT_COUNT {seen.size}"
  let mut projectTodo := externalDeps
  let mut projectSeen : Array Name := #[]
  while !projectTodo.isEmpty do
    let name := projectTodo.back!
    projectTodo := projectTodo.pop
    if !projectSeen.contains name then
      projectSeen := projectSeen.push name
      logInfo m!"TRANSITIVE_ASTIS_CONSTANT {name}"
      let some ci := env.find? name | throwError "Missing ASTIS dependency"
      let mut expressions := #[ci.type]
      if let some value := ci.value? true then
        expressions := expressions.push value
      else
        logInfo m!"PROJECT_NO_VALUE {name}"
      for expr in expressions do
        for dep in expr.getUsedConstants do
          if isProject dep then
            logInfo m!"TRANSITIVE_ASTIS_EDGE {name} -> {dep}"
            projectTodo := projectTodo.push dep
  logInfo m!"TRANSITIVE_ASTIS_CONSTANT_COUNT {projectSeen.size}"
'''
probe=O/'FreshWholeSourceKernelClosure87.lean'
with probe.open('xb') as f:f.write(M.read_bytes()+suffix.encode('utf8'))
env=dict(os.environ,PYTHONUTF8='1',PYTHONIOENCODING='utf8');env.pop('ELAN_TOOLCHAIN',None)
env['PATH']=str(R/'.astis/toolchain/lean-4.33.0-windows/bin')+os.pathsep+env['PATH']
lake=str(R/'.astis/toolchain/lean-4.33.0-windows/bin/lake.exe');lean=str(R/'.astis/toolchain/lean-4.33.0-windows/bin/lean.exe')
for n,cmd in [('fresh-focused-build',[lake,'build','AutoSamplingTheory.ExampleCases.ProximalBPS.ActualFiniteHistoryTailLaw']),('fresh-whole-source-kernel',[lake,'env',lean,str(probe)])]:
 start=now()
 with (O/(n+'.stdout.log')).open('xb') as out,(O/(n+'.stderr.log')).open('xb') as err:
  child=subprocess.Popen(cmd,cwd=R,env=env,stdout=out,stderr=err);print(n,'foreground PID',child.pid,flush=True);code=child.wait()
 put(n+'.receipt.json',dict(command=cmd,cwd=str(R),observed_head=head,actual_foreground_PID=child.pid,exit_code=code,terminal_closed=True,started_utc=start,finished_utc=now(),source=pin(M),probe=pin(probe) if n=='fresh-whole-source-kernel' else None,stdout=pin(O/(n+'.stdout.log')),stderr=pin(O/(n+'.stderr.log')),native_reasoning_trajectory_claimed=False))
 print(n,'TERMINAL_EXIT',code,flush=True);assert code==0
assert pin(M)['raw_sha256']==MR
for e in read(O/'input-freeze87.json')['actual_inputs']:assert pin(R/e['path'])==e
for p,v in prior.items():assert pin(R/p)['raw_sha256']==v
print('FRESH WHOLE SOURCE AND FOCUSED COMPILE CLOSED',flush=True)
