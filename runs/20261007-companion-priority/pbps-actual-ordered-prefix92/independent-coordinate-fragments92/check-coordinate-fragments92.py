import hashlib,json,pathlib,subprocess,time
from datetime import datetime,timezone
R=pathlib.Path('E:/Samplinglib')
B=R/'runs/20261007-companion-priority/pbps-actual-ordered-prefix92'
D=B/'independent-coordinate-fragments92'
def bind(p):
 b=p.read_bytes();return dict(path=p.as_posix(),raw_sha256=hashlib.sha256(b).hexdigest(),bytes=len(b))
specs=[('Coordinates92','e28598019893fa1fc2d870f16ddef33160c1f8e3e554d382976e14e4f8a3a162','OrderedCoordinates92',['strictMono_snoc','simplex_snoc','snoc_volume_preserving','simplex_lintegral_snoc']),('Recursion92','dcbdec1d2b48dce5d7dff734fd3a83321b9a97c4035334d4846a41c188d48ee7','OrderedRecursion92',['state_snoc_prefix','state_snoc_last','weight_snoc'])]
receipts=[]
for stem,expected,ns,names in specs:
 source=B/(stem+'.lean');raw=source.read_bytes();assert bind(source)['raw_sha256']==expected
 suffix='\nset_option pp.deepTerms true\n'+''.join('#check @'+ns+'.'+name+'\n#print axioms '+ns+'.'+name+'\n' for name in names)
 copy=D/('Fresh'+stem+'.lean')
 with copy.open('xb') as f:f.write(raw+suffix.encode())
 argv=[str(R/'.astis/toolchain/lean-4.33.0-windows/bin/lake.exe'),'env','lean',str(copy.relative_to(R))]
 start=time.monotonic()
 stdout=D/(stem+'.stdout.log');stderr=D/(stem+'.stderr.log')
 with stdout.open('xb') as out,stderr.open('xb') as err:
  result=subprocess.run(argv,cwd=R,stdout=out,stderr=err)
 receipt=dict(argv=argv,cwd=R.as_posix(),exit_code=result.returncode,duration_seconds=time.monotonic()-start,finished_utc=datetime.now(timezone.utc).isoformat(),terminal_closed=True,source=bind(source),copy=bind(copy),lake_manifest=bind(R/'lake-manifest.json'),stdout=bind(stdout),stderr=bind(stderr),scope='Internal fragment compile/type/axiom inspection only')
 with (D/(stem+'.receipt.json')).open('x',encoding='utf-8') as f:json.dump(receipt,f,indent=2)
 receipts.append(receipt)
 print(json.dumps(receipt,indent=2),flush=True)
 if result.returncode:raise SystemExit(result.returncode)
