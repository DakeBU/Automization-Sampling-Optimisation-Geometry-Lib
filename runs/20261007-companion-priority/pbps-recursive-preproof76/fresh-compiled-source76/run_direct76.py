from pathlib import Path
import datetime, hashlib, json, os, shutil, subprocess
out=Path(__file__).resolve().parent
data=(out/'candidate-input03.raw').read_bytes()
expected='1f1ebc187676e0481247bc2f58ec0bf94b2fc6f02a563b87009a0fe7bfb4910c'
assert hashlib.sha256(data).hexdigest()==expected
probe=out/'direct-review-probe76.lean'
assert not probe.exists()
probe.write_bytes(data+b'\n#print axioms AutoSamplingTheory.ExampleCases.ProximalBPS.ActualFiniteJumpRecursion.actual_fixed_reference_finite_jump_recursion\n')
lake=shutil.which('lake')
assert lake
argv=[lake,'env','lean',str(probe)]
started=datetime.datetime.now(datetime.timezone.utc).isoformat()
with (out/'direct-review76.stdout.raw').open('wb') as stdout,(out/'direct-review76.stderr.raw').open('wb') as stderr:
    process=subprocess.Popen(argv,cwd='E:/Samplinglib',stdout=stdout,stderr=stderr)
    child_pid=process.pid
    code=process.wait()
canonical=Path('E:/Samplinglib/AutoSamplingTheory/ExampleCases/ProximalBPS/ActualFiniteJumpRecursion.lean').read_bytes()
assert hashlib.sha256(canonical).hexdigest()==expected
receipt={'runner_pid':os.getpid(),'runner_parent_pid':os.getppid(),'actual_foreground_PID':child_pid,'exit_code':code,'Popen_wait_used':True,'start_utc':started,'end_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'command':argv,'source_module_raw_sha256':expected,'probe_raw_sha256':hashlib.sha256(probe.read_bytes()).hexdigest(),'probe_semantics':'Exact entire frozen module followed only by #print axioms for its public theorem. No proof/definition/binder is changed.','stdout_file':'direct-review76.stdout.raw','stderr_file':'direct-review76.stderr.raw','stdout_sha256':hashlib.sha256((out/'direct-review76.stdout.raw').read_bytes()).hexdigest(),'stderr_sha256':hashlib.sha256((out/'direct-review76.stderr.raw').read_bytes()).hexdigest(),'canonical_module_unchanged_after_check':True}
(out/'direct-review76.foreground-exit.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
print(json.dumps(receipt,ensure_ascii=False,indent=2))
raise SystemExit(code)
