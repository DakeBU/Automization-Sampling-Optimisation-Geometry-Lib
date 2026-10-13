from pathlib import Path
import os,subprocess,sys,json,hashlib,datetime
R=Path.cwd();r=Path(__file__).parent;out=r/sys.argv[1];out.mkdir(exist_ok=False)
p=r/'Header92.lean';b=p.read_bytes();(out/'Header92.snapshot.lean').write_bytes(b)
env=os.environ.copy();env['PATH']=str(R/'.astis/toolchain/lean-4.33.0-windows/bin')+os.pathsep+env['PATH'];env.pop('ELAN_TOOLCHAIN',None)
cmd=[str(R/'.astis/toolchain/lean-4.33.0-windows/bin/lake.exe'),'env','lean',str(p.resolve().relative_to(R))]
q=subprocess.run(cmd,capture_output=True,env=env)
(out/'stdout.log').write_bytes(q.stdout);(out/'stderr.log').write_bytes(q.stderr)
(out/'receipt.json').write_text(json.dumps(dict(argv=cmd,exit_code=q.returncode,header_raw_sha256=hashlib.sha256(b).hexdigest(),terminal_closed=True,utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),scope='Proposition elaboration only; no theorem proved or seal accepted.'),indent=2)+'\n',encoding='utf8',newline='\n')
print(q.stdout.decode(errors='replace')[-4000:]);print(q.stderr.decode(errors='replace')[-1000:]);sys.exit(q.returncode)
