"""Commit the original local proof event and its real receipt without replay."""
from pathlib import Path
import hashlib
import json
import subprocess

workspace = Path(__file__).resolve().parent.relative_to(Path.cwd())
evidence = Path('research-wiki/paper-contributions/GaussianComplexity/source-matrix-mean-semantic-evidence')
cell = Path('research-wiki/frontier-cells/ASTIS-SW-GAUSSIAN-COMPLEXITY-source-matrix-mean.json')
ledger = Path('runs/substantive_advances.jsonl')
runner = Path('.astis/huanjian-resume-20261103')
sha = lambda raw: hashlib.sha256(raw).hexdigest()
git = lambda *args: subprocess.check_output(['git', *args])


def create(path, raw):
    with path.open('xb') as out:
        out.write(raw)


receipts = list(runner.glob('*-source-matrix-mean-normal-PROVED-LOCAL.receipt.json'))
assert len(receipts) == 1
receipt_raw = receipts[0].read_bytes()
receipt = json.loads(receipt_raw)
head = git('rev-parse', 'HEAD').decode().strip()
source = json.loads((workspace / 'actual-independent-source-review-commit.json').read_bytes())
assert head == receipt['head_before'] == receipt['head_after'] == source['source_review_metadata_commit']
assert receipt['exit_code'] == 0
log = Path(receipt['log']).read_bytes()
assert sha(log) == receipt['log_sha256']
assert not git('diff', '--cached', '--name-only')
assert set(git('diff', 'HEAD', '--name-only').decode().splitlines()) == {str(cell), str(ledger)}
append_path = evidence / 'actual-PROVED_LOCAL-append.exact.jsonl'
payload_path = evidence / 'actual-PROVED_LOCAL-evidence.full.json'
append, payload_raw = append_path.read_bytes(), payload_path.read_bytes()
assert len(append.splitlines()) == 1
event = json.loads(append)
assert ledger.read_bytes() == git('show', f'{head}:{ledger}') + append
assert event['evidence'] == json.loads(payload_raw)
assert event['advance_id'] == 'ASTIS-SA-20261112-GaussianComplexitySourceMatrixMean'
assert event['worker_id'] == 'huanjian_gc_20261112_source_matrix_mean'
assert event['from_state'] == 'EXPLORING' and event['to_state'] == 'PROVED_LOCAL'
state = json.loads(cell.read_bytes())
assert state['status'] == 'proved_locally'
assert state['evidence']['actual_PROVED_LOCAL_append_sha256'] == sha(append)
originals = {
    evidence / 'actual-PROVED_LOCAL-run.receipt.json': receipt_raw,
    evidence / 'actual-PROVED_LOCAL-run.log': log,
    evidence / 'actual-PROVED_LOCAL-attempted.once.json':
        (workspace / 'local-proof-transition-attempted.once.json').read_bytes(),
    evidence / 'record-local-proof.py.txt': (workspace / 'record_local_proof.py').read_bytes(),
}
for path, raw in originals.items():
    create(path, raw)
files = [cell, ledger, append_path, payload_path, *originals]
subprocess.run(['git', 'add', '-f', '--', *map(str, files)], check=True)
assert set(git('diff', '--cached', '--name-only').decode().splitlines()) == set(map(str, files))
subprocess.run(['git', 'diff', '--cached', '--check', '--', str(cell), str(ledger)], check=True)
subprocess.run(['git', 'commit', '-m', 'Carry original actual Gaussian matrix-mean local proof event'], check=True)
commit = git('rev-parse', 'HEAD').decode().strip()
for path in files:
    assert git('show', f'{commit}:{path}') == path.read_bytes()
assert not git('diff', 'HEAD', '--name-only')
record = {
    'mathematical_candidate': '5fb1440f771bdae77ad31f27b2275447fe3e89e5',
    'reviewed_metadata_commit': head, 'local_proof_commit': commit,
    'event_sha256': sha(append), 'full_original_evidence_sha256': sha(payload_raw),
    'receipt_sha256': sha(receipt_raw), 'log_sha256': sha(log),
    'state': 'PROVED_LOCAL', 'event_replayed': False, 'byte_exact_files': len(files),
}
create(workspace / 'actual-local-proof-commit.json', (json.dumps(record, indent=2) + '\n').encode())
print(json.dumps(record))
