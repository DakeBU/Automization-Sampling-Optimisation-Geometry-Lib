import os,json,hashlib,datetime
from pathlib import Path
O=Path('E:/Samplinglib/runs/20261007-companion-priority/pbps-centered-root64/independent-stale-cell-overlay64');P=O.parent/'stale-cell-metadata-overlay64/proposal.json'
def sha(b):return hashlib.sha256(b).hexdigest()
lease={'schema':'stale-cell-overlay64-owned-lease-v1','status':'OPEN','owner':'/root/independent_source64','owned_root':O.as_posix(),'actual_create_pid':os.getpid(),'opened_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'This NEW owned folder only; no closed-scope/canonical/Git/ledger/source/math writes'}
(O/'lease.open.json').write_bytes((json.dumps(lease,sort_keys=True,indent=2)+'\n').encode());b=P.read_bytes();(O/'proposal.exactraw.json').write_bytes(b);(O/'proposal.LF.json').write_bytes(b.replace(b'\r\n',b'\n').replace(b'\r',b'\n'));print('PROPOSAL RAW SHA256 '+sha(b));print(b.decode('utf-8-sig'))
