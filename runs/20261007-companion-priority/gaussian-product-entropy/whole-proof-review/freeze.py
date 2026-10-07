from pathlib import Path
import json,hashlib,subprocess
R=Path('runs/20261007-companion-priority/gaussian-product-entropy');O=R/'whole-proof-review'
def j(p):return json.loads(Path(p).read_text(encoding='utf-8'))
def sha(b):return hashlib.sha256(b).hexdigest()
def d(p):
 b=Path(p).read_bytes();return dict(path=Path(p).as_posix(),raw_sha256=sha(b),lf_sha256=sha(b.replace(b'\r\n',b'\n')),bytes=len(b))
def put(p,x):
 assert not p.exists(),p
 p.write_bytes((json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode());return d(p)
freeze=j(R/'math-freeze.json');C=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip();assert C==freeze['checked_base_commit'] and len(freeze['inputs'])==26
put(O/'lease.json',dict(status='OPEN',actor='picard_commit_verifier_20261005',checked_base_commit=C,read='OPEN mathematics only',write='OPEN owned evidence',compiler='EXCLUSIVE_FOREGROUND',Python='OPEN',new_decoder_source_verdict_read=False,initial_exposure='Initial production/Test/mathfreeze read, then exact unchanged26 snapshot before further API inspection or compiler. Root declared mathematical bytes frozen.'))
rows=[]
for i,row in enumerate(freeze['inputs']):
 assert d(row['path'])['raw_sha256']==row['raw_sha256'] and d(row['path'])['lf_sha256']==row['lf_sha256'],row
 raw=Path(row['path']).read_bytes();a=O/f'input.{i:03d}.raw.snapshot';b=O/f'input.{i:03d}.lf.snapshot';assert not a.exists() and not b.exists();a.write_bytes(raw);b.write_bytes(raw.replace(b'\r\n',b'\n'));rows.append(dict(row,raw_snapshot=a.as_posix(),lf_snapshot=b.as_posix()))
put(O/'input-bindings.initial.json',dict(actor='picard_commit_verifier_20261005',checked_base_commit=C,inputs=rows,original26_unchanged=True))
print('26 inputs frozen')
