import datetime,hashlib,json,pathlib,subprocess,sys,time
ROOT=pathlib.Path('/Users/zhouhuanjian/ASTIS-GC');OUT=pathlib.Path(__file__).resolve().parent
label=sys.argv[1];argv=sys.argv[2:];d=OUT/'receipts';d.mkdir(exist_ok=True)
assert not (d/(label+'.json')).exists(),'Version failed prechecks; never automatically replay a mutation.'
start=datetime.datetime.now(datetime.timezone.utc).isoformat();t=time.monotonic()
p=subprocess.run(argv,cwd=ROOT,capture_output=True)
r={'label':label,'argv':argv,'cwd':str(ROOT),'started_utc':start,'elapsed_seconds':time.monotonic()-t,'exit_code':p.returncode}
for kind,b in [('stdout',p.stdout),('stderr',p.stderr)]:
 path=d/(label+'.'+kind);path.write_bytes(b);r[kind]={'path':str(path.relative_to(ROOT)),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
(d/(label+'.json')).write_text(json.dumps(r,indent=2)+'\n')
print(json.dumps(r,indent=2));print(p.stdout.decode(errors='replace'));print(p.stderr.decode(errors='replace'),file=sys.stderr)
sys.exit(p.returncode)
