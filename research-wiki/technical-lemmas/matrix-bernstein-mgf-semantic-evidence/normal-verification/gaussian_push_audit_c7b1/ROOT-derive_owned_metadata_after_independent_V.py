"""Derive only owned metadata from the actual independent V event; no API call."""
from pathlib import Path
import json
import hashlib
import gzip

R = Path('/Users/zhouhuanjian/ASTIS-GC')
E = R / 'research-wiki/technical-lemmas/matrix-bernstein-mgf-semantic-evidence'
D = E / 'normal-verification/gaussian_push_audit_c7b1'
C = R / 'research-wiki/frontier-cells/ASTIS-SHARED-MATRIX-BERNSTEIN-MGF.json'
W = R / '.astis/huanjian-gc-weighted-mgf-20261114'
sha = lambda b: hashlib.sha256(b).hexdigest()
v = json.loads((D / 'VERIFIED-evidence.full.v2.json').read_text())
pl = json.loads((E / 'PROVED_LOCAL-evidence.full.json').read_text())
assert all(v[k] == x for k, x in pl.items()) and len(pl) == 24
event = json.loads((D / 'VERIFIED-exact-canonical-append.jsonl').read_text())
assert event['evidence'] == v and event['worker_id'] == v['verifier_id'] == '/root/gaussian_push_audit_c7b1'
assert event['to_state'] == 'VERIFIED' and v['verified_commit'] == '6abc79ed4c012c1d506c17b9824257769c18c635'
target = [json.loads(x) for x in (R / 'runs/substantive_advances.jsonl').read_bytes().splitlines()
    if json.loads(x).get('advance_id') == event['advance_id']]
assert target[-1] == event and sum(x.get('to_state') == 'VERIFIED' for x in target) == 1
archive = D / 'selected-independent-V-originals.v1.tar.gz'
assert sha(archive.read_bytes()) == '9c4568a60e173af6c320eb01f0f01f2ebbebfaa92a4c5adbb3e9f8097d885591'
cell = json.loads(C.read_text())
assert cell['status'] == 'proved_locally' and isinstance(cell['evidence']['focused_checks'], list)
info = {
    'verifier_id': v['verifier_id'], 'verified_commit': v['verified_commit'],
    'normal_API_calls': 1, 'ROOT_API_calls': 0,
    'payload': {'file': str((D / 'VERIFIED-evidence.full.v2.json').relative_to(R)),
        'sha256': sha((D / 'VERIFIED-evidence.full.v2.json').read_bytes())},
    'exact_append': {'file': str((D / 'VERIFIED-exact-canonical-append.jsonl').relative_to(R)),
        'sha256': sha((D / 'VERIFIED-exact-canonical-append.jsonl').read_bytes())},
    'actual_process_receipt': {'file': str((D / 'normal-V-actual-process-receipt.v1.json').relative_to(R)),
        'sha256': sha((D / 'normal-V-actual-process-receipt.v1.json').read_bytes())},
    'selected_originals_archive': {'file': str(archive.relative_to(R)), 'sha256': sha(archive.read_bytes()), 'members': 15},
    'scope': 'Bounded P/T local mathematical component and exact isolated reader acceptance only; original build identities and historical PL pending-reader snapshot preserved; production/main/purification/whole Goal remain separate.'}
cell['status'] = 'independently_verified'
cell['evidence']['independent_verification'] = info
cell['evidence']['actual_normal_VERIFIED'] = info
cell['consumer_scope']['current_candidate']['state'] = 'ACTUAL_PRIVATE_COMPILED; INDEPENDENT_NATIVE_SOURCE_AND_SCOPED_READER_ACCEPTED; INCLUDED_IN_ONE_NORMAL_V_WITH_NO_SEPARATE_PUBLIC_NODE'
cell['phase_snapshot'] = 'One normal PROVED_LOCAL and one actual independent normal VERIFIED at frozen6abc. Public P and private actual-Gaussian fixed +cos T accepted within the exact recorded scope. Native/compiler evidence remains tied to original4869/earlier exact worktree hashes. Shared original-owner main/site integration, full matrix-sum Bernstein/C6/main bounds and post-merge purification remain unfinished.'
C.write_text(json.dumps(cell, ensure_ascii=False, indent=2) + '\n')
boundary = json.loads((E / 'local-proof-publication-boundary.json').read_text())
boundary['state'] = 'VERIFIED'
boundary['proof_VERIFIED_calls'] = 1
boundary['actual_independent_VERIFIED'] = info
(E / 'local-proof-publication-boundary.json').write_text(json.dumps(boundary, ensure_ascii=False, indent=2) + '\n')
memory = json.loads((E / 'local-cycle-memory.json').read_text())
memory['current_state'] = 'VERIFIED by independent actor at frozen6abc; one normalPL and one independent normalV. No ROOT self-V or whole-Goal completion.'
memory['actual_independent_VERIFIED'] = info
memory['next_required_action'] = 'Commit exact independent V append/originals and derived owned metadata; safely export only the owned delta onto previous publica350 after independent public-commit review, then push. Next mathematical candidate is a separately sealed spectral-tail/trace-exponential edge; preliminary source intake is not admission. Preserve held original stabilization lane.'
(E / 'local-cycle-memory.json').write_text(json.dumps(memory, ensure_ascii=False, indent=2) + '\n')
for name in ['prepare_independent_V_carrier.py', 'derive_owned_metadata_after_independent_V.py']:
    (D / ('ROOT-' + name)).write_bytes((W / name).read_bytes())
actual = D / 'ROOT-carrier-actual-runs'
actual.mkdir()
for name in ['20261114T095920895400Z-matrix-mgf-copy-exact-independent-normalV-originals',
    '20261114T095932982431Z-matrix-mgf-package-independent-normalV-selected-originals']:
    b = R / '.astis/huanjian-resume-20261103'
    rp, lp = b / (name + '.receipt.json'), b / (name + '.log')
    rec = json.loads(rp.read_text())
    assert rec['exit_code'] == 0 and rec['log_sha256'] == sha(lp.read_bytes())
    (actual / rp.name).write_bytes(rp.read_bytes())
    raw = lp.read_bytes()
    packed = gzip.compress(raw, mtime=0)
    assert gzip.decompress(packed) == raw
    (actual / (lp.name + '.gz')).write_bytes(packed)
(D / 'README.md').write_text('''Exactly one normal VERIFIED was executed by independent actor `/root/gaussian_push_audit_c7b1`, bound to immutable source/evidence carrier6abc. ROOT copied these originals later and derived owned cell/memory from that event; ROOT did not execute the transition. All24 original PROVED_LOCAL fields remain unchanged inline, including their historical runtime-pending snapshot. Separate post-PL fields supply current bounded isolated-reader evidence.

The unchanged independent15-leaf selection is preserved in `selected-independent-V-originals.v1.tar.gz`; direct JSON/append index copies are byte-identical. The container is later ROOT packaging and every leaf matches the independent original selection by size and SHA-256. The original receipt and actual stdout/stderr are retained, not reconstructed. Private complete before/after workspace/index/foreign guards remain local and are excluded. The payload's relative portable-byte-review locator resolves beside the direct full payload or at the same member in the archive.

Actual Lean/native build evidence belongs to recorded4869/earlier exact source bytes, the earlier four metadata CLI gates to2cc25, and the refreshed metadata checks to56f8 with the recorded worktree. No later carrier/export build identity is invented. Reader acceptance remains the pre-V exact isolated fixture, with graph default-fit/ellipsis/mobile-clipping and existing-UI zoom/detail limitations; no post-V pixels, physical touch, production/main integration, full Bernstein/C6/main lower bounds, purification or whole-Goal completion is claimed.
''')
print(json.dumps({'derived_cell_status': cell['status'], 'normal_independent_V_calls': 1,
    'ROOT_transition_calls': 0, 'original_PL_fields_unchanged': True}))
