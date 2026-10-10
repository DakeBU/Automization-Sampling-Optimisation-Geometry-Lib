from pathlib import Path
import datetime, hashlib, json, os, subprocess, sys

out=Path(__file__).resolve().parent
child=(out/sys.argv[1]).resolve()
assert child.parent==out
stem=child.stem
argv=[sys.executable,'-B','-X','utf8',str(child)]
started=datetime.datetime.now(datetime.timezone.utc).isoformat()
with (out/(stem+'.stdout.raw')).open('wb') as stdout, (out/(stem+'.stderr.raw')).open('wb') as stderr:
    process=subprocess.Popen(argv,cwd=out,stdout=stdout,stderr=stderr)
    pid=process.pid
    exit_code=process.wait()
receipt={'runner_pid':os.getpid(),'runner_parent_pid':os.getppid(),'writer_pid':pid,'foreground':True,'start_utc':started,'end_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'argv':argv,'exit_code':exit_code,'stdout_file':stem+'.stdout.raw','stderr_file':stem+'.stderr.raw','stdout_sha256':hashlib.sha256((out/(stem+'.stdout.raw')).read_bytes()).hexdigest(),'stderr_sha256':hashlib.sha256((out/(stem+'.stderr.raw')).read_bytes()).hexdigest()}
(out/(stem+'.foreground-exit.json')).write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
print(json.dumps(receipt,ensure_ascii=False,indent=2))
raise SystemExit(exit_code)
