from pathlib import Path
import hashlib,json,subprocess,datetime,os
p=Path(r'E:/Samplinglib/runs/20261007-companion-priority/pbps-centered-root-preproof64/independent-header64');py=r'C:/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe';cmd=[py,'-X','utf8',str(p/'source_first_reread.py')]
start=datetime.datetime.now(datetime.timezone.utc).isoformat();child=subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,cwd=r'E:/Samplinglib');stdout,stderr=child.communicate();end=datetime.datetime.now(datetime.timezone.utc).isoformat()
(p/'source-reread.stdout.txt').write_bytes(stdout);(p/'source-reread.stderr.txt').write_bytes(stderr)
r={'schema':1,'role':'actual-foreground-source-reread-process-receipt','parent_pid':os.getpid(),'actual_child_pid':child.pid,'command':cmd,'start_utc':start,'end_utc':end,'actual_exit_code':child.returncode,'terminal':child.poll() is not None,'stdout_raw_sha256':hashlib.sha256(stdout).hexdigest(),'stderr_raw_sha256':hashlib.sha256(stderr).hexdigest(),'source_before_header_receipt_raw_sha256':hashlib.sha256((p/'primary-before-header-reread-receipt.json').read_bytes()).hexdigest(),'exact_header_read':False}
(p/'source-reread.process-receipt.json').write_bytes((json.dumps(r,indent=2)+'\n').encode());assert child.returncode==0;assert not stderr;print(json.dumps(r,indent=2))
