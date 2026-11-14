import datetime,hashlib,json,pathlib,subprocess,sys,time
ROOT=pathlib.Path('/Users/zhouhuanjian/ASTIS-GC')
OUT=pathlib.Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()
def run(label,argv):
 d=OUT/'receipts';d.mkdir(exist_ok=True)
 assert not (d/(label+'.json')).exists(), 'Receipt exists: never automatically rerun a mutation.'
 start=datetime.datetime.now(datetime.timezone.utc).isoformat();t=time.monotonic()
 p=subprocess.run(argv,cwd=ROOT,capture_output=True)
 record={'label':label,'argv':argv,'cwd':str(ROOT),'started_utc':start,'elapsed_seconds':time.monotonic()-t,'exit_code':p.returncode}
 for kind,data in [('stdout',p.stdout),('stderr',p.stderr)]:
  path=d/(label+'.'+kind);path.write_bytes(data);record[kind]={'path':str(path.relative_to(ROOT)),'bytes':len(data),'sha256':sha(data)}
 (d/(label+'.json')).write_text(json.dumps(record,indent=2)+'\n')
 print(json.dumps(record,indent=2));print(p.stdout.decode(errors='replace'));print(p.stderr.decode(errors='replace'),file=sys.stderr)
 return p.returncode
if __name__=='__main__':sys.exit(run(sys.argv[1],sys.argv[2:]))
