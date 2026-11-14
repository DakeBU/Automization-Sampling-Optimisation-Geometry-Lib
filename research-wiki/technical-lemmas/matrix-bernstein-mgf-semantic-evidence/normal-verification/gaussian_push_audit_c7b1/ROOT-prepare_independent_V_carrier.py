"""Copy exact selected independent V originals; never call an advance API."""
from pathlib import Path
import hashlib
import json
import subprocess

R = Path('/Users/zhouhuanjian/ASTIS-GC')
E = R / 'research-wiki/technical-lemmas/matrix-bernstein-mgf-semantic-evidence'
S = R / '.astis/semantic-neutral-20261114/weighted_mgf_native_8c2d/verification-6abc'
D = E / 'normal-verification/gaussian_push_audit_c7b1'
sha = lambda b: hashlib.sha256(b).hexdigest()
manifest_path = S / 'normal-V-public-selected-originals.manifest.v1.json'
manifest_bytes = manifest_path.read_bytes()
assert sha(manifest_bytes) == '1b52c243f7ff2f366e026278a4f0ba04229bde3dc66e128ffab66d721cfab05f'
m = json.loads(manifest_bytes)
assert m['file_count'] == 15 and m['normal_API_invocations'] == 1
old = subprocess.check_output(['git', 'show', '6abc79ed4c012c1d506c17b9824257769c18c635:runs/substantive_advances.jsonl'])
current = (R / 'runs/substantive_advances.jsonl').read_bytes()
append = (S / 'VERIFIED-exact-canonical-append.jsonl').read_bytes()
assert current == old + append
assert sha(append) == '4e55fac68014ab22c212ddeee4d53cd7027b402dce93149efd9728e612c3e27f'
event = json.loads(append)
vbytes = (S / 'VERIFIED-evidence.full.v2.json').read_bytes()
assert sha(vbytes) == 'ae0004612dbe6c05a7861b51dd3a8416162cce31697670d413b164b456e5ff39'
v = json.loads(vbytes)
pl = json.loads((E / 'PROVED_LOCAL-evidence.full.json').read_text())
assert len(pl) == 24 and all(v[k] == value for k, value in pl.items())
assert event['advance_id'] == 'ASTIS-SA-20261114-MatrixBernsteinMgf' and event['to_state'] == 'VERIFIED'
assert event['worker_id'] == v['verifier_id'] == '/root/gaussian_push_audit_c7b1'
assert event['evidence'] == v and v['verified_commit'] == '6abc79ed4c012c1d506c17b9824257769c18c635'
assert subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip() == v['verified_commit']
rows = {x['path']: x for x in m['files']}
for name, row in rows.items():
    p = Path(name)
    assert not p.is_absolute() and '..' not in p.parts and 'private.guard' not in name
    raw = (S / p).read_bytes()
    assert len(raw) == row['bytes'] and sha(raw) == row['sha256']
D.mkdir(parents=True, exist_ok=False)
(D / manifest_path.name).write_bytes(manifest_bytes)
direct = ['VERIFIED-evidence.full.v2.json', 'VERIFIED-exact-canonical-append.jsonl',
    'normal-V-actual-process-receipt.v1.json', 'normal-V-preservation-summary.v1.json',
    'pre-V-independent-acceptance.v1.json', 'pre-V-carrier-portable-byte-review.public.v1.json']
for name in direct:
    assert name in rows
    (D / name).write_bytes((S / name).read_bytes())
print(json.dumps({'source_verifier': v['verifier_id'], 'verified_commit': v['verified_commit'],
    'selected_leaves': len(rows), 'direct_exact_index_copies': direct,
    'canonical_append_exact_original': True, 'PL24_fields_unchanged': True, 'ROOT_API_calls': 0}))
