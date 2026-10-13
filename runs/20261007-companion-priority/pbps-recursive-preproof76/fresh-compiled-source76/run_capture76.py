from pathlib import Path
import datetime, hashlib, json, os, subprocess, sys

out=Path(__file__).resolve().parent
child=(out/sys.argv[1]).resolve()
assert child.parent==out
stem=child.stem
if (out/(stem+'.stdout.raw')).exists():
    attempt=2
    while (out/(stem+'.attempt'+str(attempt)+'.stdout.raw')).exists():
        attempt+=1
    stem=stem+'.attempt'+str(attempt)
argv=[sys.executable,'-B','-X','utf8',str(child)]
started=datetime.datetime.now(datetime.timezone.utc).isoformat()
with (out/(stem+'.stdout.raw')).open('wb') as stdout, (out/(stem+'.stderr.raw')).open('wb') as stderr:
    process=subprocess.Popen(argv,cwd=out,stdout=stdout,stderr=stderr)
    pid=process.pid
    exit_code=process.wait()
receipt={'runner_pid':os.getpid(),'runner_parent_pid':os.getppid(),'writer_pid':pid,'foreground':True,'start_utc':started,'end_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'argv':argv,'exit_code':exit_code,'stdout_file':stem+'.stdout.raw','stderr_file':stem+'.stderr.raw','stdout_sha256':hashlib.sha256((out/(stem+'.stdout.raw')).read_bytes()).hexdigest(),'stderr_sha256':hashlib.sha256((out/(stem+'.stderr.raw')).read_bytes()).hexdigest()}
if child.name=='write_source_freeze76.py' and exit_code==0:
    freeze_path=out/'source-only.freeze76.json'
    freeze=json.loads(freeze_path.read_text(encoding='utf-8'))
    assert freeze['foreground_writer']['writer_pid']==pid
    freeze['foreground_writer']=receipt.copy()
    freeze['foreground_writer']['exit_provenance']='Actual foreground subprocess Popen.wait result recorded after the writer terminated; no self-asserted exit.'
    freeze_path.write_text(json.dumps(freeze,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
    receipt['completed_freeze_sha256']=hashlib.sha256(freeze_path.read_bytes()).hexdigest()
(out/(stem+'.foreground-exit.json')).write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
print(json.dumps(receipt,ensure_ascii=False,indent=2))
raise SystemExit(exit_code)
