import hashlib,json,pathlib,subprocess,time
from datetime import datetime,timezone
R=pathlib.Path('E:/Samplinglib');B=R/'runs/20261007-companion-priority/pbps-actual-ordered-prefix92';D=B/'independent-event-algebra-fragments92'
def bind(p):
 b=p.read_bytes();return dict(path=p.as_posix(),raw_sha256=hashlib.sha256(b).hexdigest(),bytes=len(b))
specs=[('Events92','ffe309d308e3b82c20a15af38f397c57c5b29ea567589e986d8740f43f6aac92','OrderedEvents92',['guard_snoc','record_history_snoc','record_guard_step','record_event_step']),('Algebra92','cf995959ce0db6164101ace8f02a47e7f126e6edc3b7e37ce0cbe8cbb3b21395','OrderedAlgebra92',['state_snoc_prefix','state_snoc_last','weight_snoc','timedHistory_snoc','ordered_last_nonneg','weight_snoc_ofReal'])]
for stem,expected,ns,names in specs:
 source=B/(stem+'.lean');raw=source.read_bytes();assert bind(source)['raw_sha256']==expected
 suffix='\nset_option pp.deepTerms true\n'+''.join('#check @'+ns+'.'+n+'\n#print axioms '+ns+'.'+n+'\n' for n in names)
 copy=D/('Fresh'+stem+'.lean')
 with copy.open('xb') as f:f.write(raw+suffix.encode())
 argv=[str(R/'.astis/toolchain/lean-4.33.0-windows/bin/lake.exe'),'env','lean',str(copy.relative_to(R))]
 start=time.monotonic();outpath=D/(stem+'.stdout.log');errpath=D/(stem+'.stderr.log')
 with outpath.open('xb') as out,errpath.open('xb') as err:result=subprocess.run(argv,cwd=R,stdout=out,stderr=err)
 receipt=dict(argv=argv,cwd=R.as_posix(),exit_code=result.returncode,duration_seconds=time.monotonic()-start,finished_utc=datetime.now(timezone.utc).isoformat(),terminal_closed=True,source=bind(source),copy=bind(copy),lake_manifest=bind(R/'lake-manifest.json'),stdout=bind(outpath),stderr=bind(errpath),scope='Private event/algebra fragment compilation and type/axiom inspection only')
 with (D/(stem+'.receipt.json')).open('x',encoding='utf-8') as f:json.dump(receipt,f,indent=2)
 print(json.dumps(receipt,indent=2),flush=True)
 if result.returncode:raise SystemExit(result.returncode)
