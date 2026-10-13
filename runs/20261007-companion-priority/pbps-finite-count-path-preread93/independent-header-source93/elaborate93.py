from pathlib import Path
import json,hashlib,subprocess,datetime,time
root=Path('E:/Samplinglib');out=Path(__file__).parent
p=root/'runs/20261007-companion-priority/pbps-finite-count-path-preread93/Header93.lean';b=p.read_bytes()
assert hashlib.sha256(b).hexdigest()=='90bca17fbb11d9a8fea226bd0dca6494ef9a61f3db31beaf52c0ef2999cf9cfe'
snapshot=out/'Header93.exactraw.snapshot.lean';assert not snapshot.exists();snapshot.write_bytes(b)
argv=[str(root/'.astis/toolchain/lean-4.33.0-windows/bin/lake.exe'),'env','lean',str(snapshot.relative_to(root))]
t=time.monotonic();r=subprocess.run(argv,cwd=root,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
(out/'elaboration.stdout.log').write_bytes(r.stdout);(out/'elaboration.stderr.log').write_bytes(r.stderr)
def bind(q):
 x=q.read_bytes();return {'path':q.relative_to(root).as_posix(),'raw_sha256':hashlib.sha256(x).hexdigest(),'bytes':len(x)}
receipt={'record_kind':'independent-source-review-signature-only-elaboration','argv':argv,'exit_code':r.returncode,'terminal_closed':True,'duration_seconds':time.monotonic()-t,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'header':bind(p),'snapshot':bind(snapshot),'stdout':bind(out/'elaboration.stdout.log'),'stderr':bind(out/'elaboration.stderr.log'),'proof_or_theorem_compilation':False}
(out/'elaboration.receipt.native.json').write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf8');print(json.dumps(receipt,indent=2))
