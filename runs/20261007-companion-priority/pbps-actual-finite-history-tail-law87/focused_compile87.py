from pathlib import Path
import sys,os,subprocess,json,hashlib,datetime
R=Path('E:/Samplinglib');r=Path(__file__).parent/'focused';r.mkdir(exist_ok=True)
label=sys.argv[1];out=r/label;assert not out.exists();out.mkdir()
p=R/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualFiniteHistoryTailLaw.lean'
if not p.exists(): p=r.parent/'implementation87.lean'
b=p.read_bytes();(out/'module.exactraw.lean').write_bytes(b)
env=os.environ.copy();env['PATH']=str(R/'.astis/toolchain/lean-4.33.0-windows/bin')+os.pathsep+env['PATH'];env.pop('ELAN_TOOLCHAIN',None)
args=[str(R/'.astis/toolchain/lean-4.33.0-windows/bin/lake.exe'),'env','lean',str(p)]
if len(sys.argv)>2 and sys.argv[2]=='build':
 args=[str(R/'.astis/toolchain/lean-4.33.0-windows/bin/lake.exe'),'build','AutoSamplingTheory.ExampleCases.ProximalBPS.ActualFiniteHistoryTailLaw']
q=subprocess.run(args,cwd=R,env=env,capture_output=True)
(out/'stdout.log').write_bytes(q.stdout);(out/'stderr.log').write_bytes(q.stderr)
(out/'receipt.json').write_text(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'argv':args,'exit_code':q.returncode,'terminal_closed':True,'module_raw_sha256':hashlib.sha256(b).hexdigest(),'statement_seal_unchanged':True},indent=2)+'\n',encoding='utf-8',newline='\n')
print(q.stdout.decode(errors='replace'));print(q.stderr.decode(errors='replace'));sys.exit(q.returncode)
