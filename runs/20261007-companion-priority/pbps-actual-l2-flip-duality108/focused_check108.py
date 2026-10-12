from pathlib import Path
import subprocess,os,json,hashlib,sys
r=Path(__file__).parent;p=Path(sys.argv[1]);out=r/'focused108'/sys.argv[2];out.mkdir(parents=True,exist_ok=False);raw=p.read_bytes();(out/'input.exactraw.lean').write_bytes(raw)
env=os.environ.copy();env['PATH']=str(Path('.astis/toolchain/lean-4.33.0-windows/bin').resolve())+os.pathsep+env['PATH'];env.pop('ELAN_TOOLCHAIN',None);env['LEAN_NUM_THREADS']='2'
cmd=[str(Path('.astis/toolchain/lean-4.33.0-windows/bin/lake.exe').resolve()),'env','lean',str(p)]
q=subprocess.run(cmd,env=env,capture_output=True);(out/'stdout.log').write_bytes(q.stdout);(out/'stderr.log').write_bytes(q.stderr);(out/'receipt.json').write_text(json.dumps(dict(argv=cmd,exit_code=q.returncode,input_RAW_sha256=hashlib.sha256(raw).hexdigest(),terminal_closed=True),indent=2)+'\n',encoding='utf8',newline='\n');print(q.stdout.decode(errors='replace')[-7500:]);print(q.stderr.decode(errors='replace')[-1200:]);sys.exit(q.returncode)
