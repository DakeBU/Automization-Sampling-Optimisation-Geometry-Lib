from pathlib import Path
import os,sys,json,hashlib,subprocess,datetime
r=Path(__file__).parent;label=sys.argv[1];target=sys.argv[2]
out=r/'checks97'/label;out.mkdir(parents=True,exist_ok=False)
env=os.environ.copy();env['PATH']=str(Path('.astis/toolchain/lean-4.33.0-windows/bin').resolve())+os.pathsep+env['PATH'];env.pop('ELAN_TOOLCHAIN',None);env['LEAN_NUM_THREADS']='2';env['PYTHONUTF8']='1'
argv=[str(Path('.astis/toolchain/lean-4.33.0-windows/bin/lake.exe').resolve()),'env','lean',target]
if '--build' in sys.argv[3:]:
    argv=[argv[0],'build',target.removesuffix('.lean').replace('/','.').replace('\\','.')]
q=subprocess.run(argv,env=env,capture_output=True)
(out/'stdout.log').write_bytes(q.stdout);(out/'stderr.log').write_bytes(q.stderr)
d=dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),argv=argv,exit_code=q.returncode,terminal_closed=True,target_raw_sha256=hashlib.sha256(Path(target).read_bytes()).hexdigest())
(out/'receipt.json').write_text(json.dumps(d,indent=2)+'\n',encoding='utf8',newline='\n')
(out/'input.lean').write_bytes(Path(target).read_bytes())
print(q.stdout.decode(errors='replace')[-11000:]);print(q.stderr.decode(errors='replace')[-1500:]);print(json.dumps(d));sys.exit(q.returncode)
