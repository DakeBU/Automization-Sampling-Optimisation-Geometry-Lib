#!/opt/anaconda3/bin/python
import datetime,hashlib,json,pathlib,subprocess,sys
BASE=pathlib.Path(__file__).resolve().parent
def run(label,argv):
    started=datetime.datetime.now(datetime.timezone.utc).isoformat()
    proc=subprocess.run(argv,cwd='/Users/zhouhuanjian/ASTIS-GC',capture_output=True)
    out=BASE/(label+'.stdout');err=BASE/(label+'.stderr')
    out.write_bytes(proc.stdout);err.write_bytes(proc.stderr)
    rec={'label':label,'started_utc':started,'cwd':'/Users/zhouhuanjian/ASTIS-GC','argv':argv,
         'returncode':proc.returncode,'stdout_file':out.name,'stderr_file':err.name,
         'stdout_bytes':len(proc.stdout),'stderr_bytes':len(proc.stderr),
         'stdout_sha256':hashlib.sha256(proc.stdout).hexdigest(),'stderr_sha256':hashlib.sha256(proc.stderr).hexdigest()}
    with (BASE/'actual_commands.jsonl').open('a') as f:f.write(json.dumps(rec)+'\n')
    print(json.dumps(rec));sys.stdout.write(proc.stdout.decode(errors='replace'));sys.stderr.write(proc.stderr.decode(errors='replace'))
    return proc.returncode
if __name__=='__main__':raise SystemExit(run(sys.argv[1],sys.argv[2:]))
