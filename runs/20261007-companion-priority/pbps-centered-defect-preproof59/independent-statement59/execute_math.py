from common import *
write(D/'math-reader.0.diagnosis.json',dict(status='RETIRED_METADATA_READER_NEGATIVE',actual_tool_chunk='15e6a9',actual_exit_code=1,original_reader=pin(D/'math-reader.0.failed.raw.snapshot.py'),diagnosis='Header intentionally contains let definitions := for actual laws/operators/H0. Initial no-body reader incorrectly rejected every := token; corrected criterion rejects theorem proof delimiter := by, preserving genuine definitions. No signature changed; no mathematical blocker or convenience premise.',strict_reduction='Exact original header raw/LF pins still match candidate.'))
with (D/'math.actual.log').open('wb') as out:
 p=subprocess.Popen([sys.executable,'-B','-X','utf8',str(D/'math_review.py')],stdout=out,stderr=subprocess.STDOUT,env=dict(os.environ,PYTHONUTF8='1',PYTHONDONTWRITEBYTECODE='1'));pid=p.pid;rc=p.wait()
write(D/'math.actual.status.json',dict(actual_worker_PID=pid,actual_wrapper_PID=os.getpid(),exit_code=rc,resource='CLOSED',compiler='NOT_STARTED_CLOSED',log=pin(D/'math.actual.log')))
print((D/'math.actual.log').read_text(encoding='utf8'));sys.exit(rc)
