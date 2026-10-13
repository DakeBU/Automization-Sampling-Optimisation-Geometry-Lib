from pathlib import Path
import datetime, hashlib, json, os, subprocess, sys

out=Path(__file__).resolve().parent
assert not (out/'lease.final.json').exists()
stdout=out/'preparation.stdout.RAW'; stderr=out/'preparation.stderr.RAW'
assert not stdout.exists() and not stderr.exists()
started=datetime.datetime.now(datetime.timezone.utc).isoformat()
argv=[sys.executable,'-B','-X','utf8',str(out/'prepare_reader76.py')]
with stdout.open('xb') as a,stderr.open('xb') as b:
    child=subprocess.Popen(argv,cwd=out,stdout=a,stderr=b)
    exit_code=child.wait()
receipt={'operation':'PREPARATION_ONLY','actual_foreground_PID':child.pid,'actual_driver_PID':os.getpid(),'Popen_wait_used':True,'terminal_closed':True,'terminal_EXIT':exit_code,'started_UTC':started,'finished_UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'argv':argv,'stdout_file':stdout.name,'stdout_RAW_sha256':hashlib.sha256(stdout.read_bytes()).hexdigest(),'stderr_file':stderr.name,'stderr_RAW_sha256':hashlib.sha256(stderr.read_bytes()).hexdigest(),'current_reader_checks_run':False}
path=out/'preparation.foreground-exit.json'; assert not path.exists()
path.write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
print(json.dumps(receipt,ensure_ascii=False,indent=2))
raise SystemExit(exit_code)
