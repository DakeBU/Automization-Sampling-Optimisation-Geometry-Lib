import hashlib
import json
from pathlib import Path

ROOT = Path('E:/Samplinglib')
BASE = ROOT / 'runs/20261007-companion-priority/pbps-marginal-poincare57'
OUT = BASE / 'source-review57'
RECIPE = 'SHA256 UTF8 json.dumps(complete object minus only the named self-hash field, ensure_ascii=False, sort_keys=True, separators=(comma,colon)); no newline. Exact raw bytes and CRLF->LF-only bytes are separate receipts.'

def canonical(obj):
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode('utf8')

def sha(data):
    return hashlib.sha256(data).hexdigest()

def load(path):
    return json.loads(Path(path).read_bytes().decode('utf8'))

def seal(obj, field='content_self_sha256'):
    assert field not in obj
    return dict(obj, **{field: sha(canonical(obj))})

def check_self(obj, field='content_self_sha256'):
    assert obj[field] == sha(canonical({k: v for k, v in obj.items() if k != field})), field

def write(path, obj):
    path = Path(path)
    assert path.resolve().is_relative_to(OUT.resolve()), str(path)
    assert not path.exists(), 'No overwrite during sealing: ' + str(path)
    path.write_bytes((json.dumps(obj, ensure_ascii=False, indent=2) + '\n').encode('utf8'))
    assert load(path) == obj

def pin(path):
    path = Path(path).resolve()
    data = path.read_bytes()
    lf = data.replace(b'\r\n', b'\n')
    return {'path': path.as_posix(), 'bytes': len(data), 'raw_sha256': sha(data), 'lf_bytes': len(lf), 'lf_sha256': sha(lf)}

def check_pin(receipt):
    actual = pin(receipt['path'])
    for key in ('bytes', 'raw_sha256', 'lf_bytes', 'lf_sha256'):
        if key in receipt:
            assert actual[key] == receipt[key], (receipt['path'], key)
    return actual

def check_inputs():
    manifest = load(OUT / 'input.manifest.json')
    check_self(manifest)
    assert len(manifest['pins']) == manifest['count'] == 614
    for receipt in manifest['pins']:
        check_pin(receipt)
    return manifest

def files(exclude=()):
    return sorted(p for p in OUT.rglob('*') if p.is_file() and p.name not in exclude and '__pycache__' not in p.parts)

