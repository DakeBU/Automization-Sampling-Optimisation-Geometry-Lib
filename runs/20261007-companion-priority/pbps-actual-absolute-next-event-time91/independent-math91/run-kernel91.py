from pathlib import Path
import datetime,hashlib,json,os,subprocess,time
R=Path('E:/Samplinglib'); O=R/'runs/20261007-companion-priority/pbps-actual-absolute-next-event-time91/independent-math91'
M=R/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualAbsoluteNextEventTime.lean'
raw=M.read_bytes(); assert hashlib.sha256(raw).hexdigest()=='8e28fb218233358a9b1c7a2b41689071ca3c410faa58a0883a0885243d588ab2'
(O/'module.exactraw.snapshot.lean').write_bytes(raw)
prior=(R/'runs/20261007-companion-priority/pbps-actual-finite-history-extension90/independent-math90/FreshWholeSourceKernelClosure90.lean').read_text(encoding='utf8')
tail=prior[prior.index('#print axioms'):].replace('ActualFiniteHistoryExtension','ActualAbsoluteNextEventTime').replace('actual_finite_history_extension','actual_absolute_next_event_time_law')
extra='''
open Lean Elab Command in
run_cmd do
  let env ← getEnv
  let some ci := env.find? `AutoSamplingTheory.ExampleCases.ProximalBPS.ActualAbsoluteNextEventTime.actual_absolute_next_event_time_law | throwError "missing public theorem"
  logInfo m!"PUBLIC_TYPE {ci.type}"
  for dep in ci.type.getUsedConstants do
    if (dep.toString.splitOn ".").contains "actual_absolute_next_event_time_statement" then
      let some stmt := env.find? dep | throwError "missing private statement"
      let some body := stmt.value? true | throwError "statement has no body"
      logInfo m!"EXPANDED_PRIVATE_STATEMENT {body}"
'''
probe=O/'FreshWholeSourceKernelClosure91.lean'
probe.write_bytes(raw+b'\nset_option pp.universes true\nset_option pp.proofs false\nset_option pp.deepTerms true\nset_option pp.maxSteps 1000000\n'+tail.encode()+extra.encode())
paths=[M,R/'lean-toolchain',R/'lake-manifest.json',R/'runs/20261007-companion-priority/pbps-actual-absolute-next-event-time91/root.statement-seal91.json',R/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualFiniteHistoryExtension.lean',R/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualConditionalNextWaitDensity.lean',R/'AutoSamplingTheory/TechnicalLemmas/Probability/UnitExponentialProduct.lean',R/'runs/20261007-companion-priority/pbps-ordered-history-iteration-preread91/source-proof-graph91.accepted-successor.json',R/'runs/20261007-companion-priority/pbps-ordered-history-iteration-preread91/root.preproof91.authorization.json',probe]
inputs=[dict(path=str(p),raw_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),bytes=p.stat().st_size) for p in paths]
(O/'input-hashes.native.json').write_text(json.dumps(inputs,indent=2)+'\n',encoding='utf8')
env=os.environ.copy(); env['PATH']=str(R/'.astis/toolchain/lean-4.33.0-windows/bin')+os.pathsep+env['PATH'];env.pop('ELAN_TOOLCHAIN',None)
argv=[str(R/'.astis/toolchain/lean-4.33.0-windows/bin/lake.exe'),'env','lean',str(probe)]
head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=R).decode().strip()
t=time.monotonic(); start=datetime.datetime.now(datetime.timezone.utc).isoformat(); q=subprocess.run(argv,cwd=R,env=env,capture_output=True)
(O/'kernel.stdout.log').write_bytes(q.stdout);(O/'kernel.stderr.log').write_bytes(q.stderr)
receipt=dict(started_utc=start,ended_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),command=argv,checked_base_HEAD=head,exit_code=q.returncode,terminal_closed=True,seconds=time.monotonic()-t,production_unchanged=M.read_bytes()==raw,inputs=inputs,outputs=[dict(path=str(O/n),raw_sha256=hashlib.sha256((O/n).read_bytes()).hexdigest()) for n in ['kernel.stdout.log','kernel.stderr.log']])
(O/'kernel.receipt.native.json').write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf8');print(json.dumps({k:v for k,v in receipt.items() if k not in ['inputs','outputs']}));print(q.stdout.decode('utf8',errors='replace')[-3000:] if q.returncode else 'Fresh source elaboration, axioms, kernel dependencies and private Prop expansion completed.')
