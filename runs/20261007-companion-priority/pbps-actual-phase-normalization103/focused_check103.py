from pathlib import Path
import os,sys,subprocess,json,hashlib,datetime
r=Path(__file__).parent;f=r/sys.argv[1];o=r/'focused103'/sys.argv[2];o.mkdir(parents=True,exist_ok=False)
b=f.read_bytes();(o/'input.exactraw.lean').write_bytes(b)
e=os.environ.copy();e['PATH']=str(Path('.astis/toolchain/lean-4.33.0-windows/bin').resolve())+os.pathsep+e['PATH'];e.pop('ELAN_TOOLCHAIN',None);e['LEAN_NUM_THREADS']='2';e['PYTHONUTF8']='1'
a=[str(Path('.astis/toolchain/lean-4.33.0-windows/bin/lake.exe').resolve()),'env','lean',str(f)];p=subprocess.run(a,env=e,capture_output=True)
(o/'stdout.log').write_bytes(p.stdout);(o/'stderr.log').write_bytes(p.stderr)
(o/'receipt.json').write_text(json.dumps(dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),argv=a,exit_code=p.returncode,terminal_closed=True,input_raw_sha256=hashlib.sha256(b).hexdigest(),complete_SAU=False),indent=2)+'\n',encoding='utf8',newline='\n')
print(p.stdout.decode(errors='replace')[-6500:]);print(p.stderr.decode(errors='replace'));raise SystemExit(p.returncode)
