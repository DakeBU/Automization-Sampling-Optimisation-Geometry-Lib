"""Carry the one actual R9 PL append and complete original payload/receipt, no replay."""
from pathlib import Path
import hashlib
import json
import subprocess
W = Path(__file__).resolve().parent.relative_to(Path.cwd())
E = Path('research-wiki/paper-contributions/GaussianComplexity/source-matrix-variance-semantic-evidence')
C = Path('research-wiki/frontier-cells/ASTIS-SW-GAUSSIAN-COMPLEXITY-source-matrix-variance.json')
LEDGER = Path('runs/substantive_advances.jsonl')
sha = lambda raw:hashlib.sha256(raw).hexdigest()
git = lambda *args:subprocess.check_output(['git',*args])
dump = lambda obj:(json.dumps(obj,ensure_ascii=False,indent=2)+'\n').encode()
def create(p,raw):
    with p.open('xb') as f:f.write(raw)
head = git('rev-parse','HEAD').decode().strip()
assert head == 'e005ec6c0976f829261d5519a51f260afd64a877'
assert not git('diff','--cached','--name-only')
assert set(git('diff','HEAD','--name-only').decode().splitlines()) == {str(C),str(LEDGER)}
rpath = Path('.astis/huanjian-resume-20261103/20261112T175445593895Z-source-matrix-variance-normal-PROVED-LOCAL.receipt.json')
rraw = rpath.read_bytes(); r = json.loads(rraw)
assert r['exit_code'] == 0 and r['head_before'] == r['head_after'] == head
log = Path(r['log']).read_bytes(); assert sha(log) == r['log_sha256']
ap = E/'actual-PROVED_LOCAL-append.exact.jsonl'
ep = E/'actual-PROVED_LOCAL-evidence.full.json'
append,payload = ap.read_bytes(),ep.read_bytes()
assert len(append.splitlines()) == 1
event = json.loads(append)
assert event['advance_id'] == 'ASTIS-SA-20261112-GaussianComplexitySourceMatrixVariance'
assert event['from_state'] == 'EXPLORING' and event['to_state'] == 'PROVED_LOCAL'
assert event['evidence'] == json.loads(payload)
assert LEDGER.read_bytes() == git('show',f'{head}:{LEDGER}')+append
assert sha(append) == '011b52b7b0b53b29544512a44923d8991530b293025f224c2ec1b067eb4e20c6'
assert sha(payload) == '6d33efc87376f754034dcf4acf6f9acc6d6995a748f80d43a6a1302412d6e3e1'
originals = {
    E/'actual-PROVED_LOCAL-run.receipt.json':rraw,
    E/'actual-PROVED_LOCAL-run.log':log,
    E/'actual-PROVED_LOCAL-attempted.once.json':(W/'local-proof-transition-attempted.once.json').read_bytes(),
    E/'record-local-proof.py.txt':(W/'record_full_variance_local_proof.py').read_bytes(),
}
for p,raw in originals.items():create(p,raw)
paths = [C,LEDGER,ap,ep,*originals]
subprocess.run(['git','add','-f','--',*map(str,paths)],check=True)
assert set(git('diff','--cached','--name-only').decode().splitlines()) == set(map(str,paths))
subprocess.run(['git','diff','--cached','--check','--',str(C),str(LEDGER)],check=True)
subprocess.run(['git','commit','--quiet','-m','Carry original actual Gaussian matrix variance local proof event'],check=True)
commit = git('rev-parse','HEAD').decode().strip()
for p in paths:assert git('show',f'{commit}:{p}') == p.read_bytes()
assert not git('diff','HEAD','--name-only')
result = {'actual_math_commit':'e654e98642350a615c473bc8190fbc1d47fe52bd',
    'reader_commit':'1d0dedf3aac3c2ff72ee96566461e29e38a2eeae','source_metadata_commit':head,
    'local_proof_commit':commit,'actual_append_sha256':sha(append),
    'actual_full_payload_sha256':sha(payload),'full_payload_field_count':len(event['evidence']),
    'actual_receipt_sha256':sha(rraw),'actual_log_sha256':sha(log),
    'normal_PL_calls':1,'normal_V_calls':0,'root_VERIFIED_calls':0,'replayed':False}
create(W/'actual-full-variance-local-proof-commit.json',dump(result))
print(json.dumps(result))
