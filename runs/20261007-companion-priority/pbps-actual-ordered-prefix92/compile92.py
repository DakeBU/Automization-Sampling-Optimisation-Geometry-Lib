from pathlib import Path
import subprocess,os,sys,json,hashlib,datetime,time
root=Path(__file__).resolve().parents[3]
run=Path(__file__).resolve().parent
label=sys.argv[1]
f=run/(sys.argv[2] if len(sys.argv)>2 else 'Geometry92.lean')
d=run/'focused'/label
d.mkdir(parents=True,exist_ok=False)
b=f.read_bytes();(d/f.name).write_bytes(b)
env=os.environ.copy();env.pop('ELAN_TOOLCHAIN',None)
bindir=root/'.astis/toolchain/lean-4.33.0-windows/bin'
env['PATH']=str(bindir)+os.pathsep+env.get('PATH','')
args=[str(bindir/'lake.exe'),'env','lean',str(f)]
start=time.monotonic()
with (d/'stdout.log').open('wb') as out,(d/'stderr.log').open('wb') as err:
 p=subprocess.run(args,cwd=root,env=env,stdout=out,stderr=err)
r={'command':args,'exit_code':p.returncode,'seconds':time.monotonic()-start,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'source':{'path':f.as_posix(),'raw_sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b)}}
(d/'receipt.json').write_text(json.dumps(r,indent=2)+'\n')
print(json.dumps(r));print((d/'stdout.log').read_text(encoding='utf8'));print((d/'stderr.log').read_text(encoding='utf8'))
sys.exit(p.returncode)
