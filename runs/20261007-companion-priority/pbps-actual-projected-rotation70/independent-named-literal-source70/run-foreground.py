import datetime,json,os,pathlib,subprocess,sys
out=pathlib.Path(__file__).resolve().parent;label,script=sys.argv[1:3]
start=datetime.datetime.now(datetime.timezone.utc).isoformat()
p=subprocess.Popen([sys.executable,str(out/script)],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
stdout,stderr=p.communicate();(out/(label+'.stdout.log')).write_bytes(stdout);(out/(label+'.stderr.log')).write_bytes(stderr)
r=dict(schema='named-literal-source70-foreground-terminal-v1',wrapper_pid=os.getpid(),actual_pid=p.pid,actual_exit=p.returncode,
    foreground=True,completed=True,script=script,start_utc=start,end_utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
(out/(label+'.receipt.json')).write_text(json.dumps(r,sort_keys=True,indent=2)+'\n',encoding='utf-8')
sys.stdout.buffer.write(stdout);sys.stderr.buffer.write(stderr);print(json.dumps(r,sort_keys=True));raise SystemExit(p.returncode)
