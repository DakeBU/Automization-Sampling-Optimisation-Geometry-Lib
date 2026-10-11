from pathlib import Path
import hashlib,json,shutil
O=Path(__file__).resolve().parent;T=O/'trial949bd4c';T.mkdir(exist_ok=False)
outputs=[p for p in O.iterdir() if p.is_file() and p.suffix in {'.json','.log'} and p.name!='prepared96.native.json']
rows=[]
for p in sorted(outputs):
 b=p.read_bytes();rows.append(dict(path=p.name,raw_sha256=hashlib.sha256(b).hexdigest(),bytes=len(b)));p.rename(T/p.name)
for p in sorted(O.glob('*.py')):shutil.copyfile(p,T/(p.name+'.exactraw'))
(T/'closed-trial96.json').write_bytes((json.dumps(dict(status='CONTRIBUTOR_METADATA_GATE_FAILED_NO_ADMISSION',checked_commit='949bd4cb5e780c590055aefe327358d7ffe8f2e8',outputs=rows,production_and_fresh_kernel_passed=True,shared_state_mutation=False),indent=2)+'\n').encode())
print('Preserved',len(rows),'original trial outputs and exact verifier script snapshots')
