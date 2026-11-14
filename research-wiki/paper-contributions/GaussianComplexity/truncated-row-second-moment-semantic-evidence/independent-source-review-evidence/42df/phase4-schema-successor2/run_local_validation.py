from pathlib import Path
import datetime
import hashlib
import json
import subprocess
import sys

HERE = Path(__file__).resolve().parent
REPO = Path('/Users/zhouhuanjian/ASTIS-GC')
script = HERE / 'validate_local_registry.py'
started = datetime.datetime.now(datetime.timezone.utc).isoformat()
result = subprocess.run([sys.executable, str(script)], cwd=REPO, capture_output=True)
ended = datetime.datetime.now(datetime.timezone.utc).isoformat()
stdout = HERE / 'local-registry-validation.stdout.log'
stderr = HERE / 'local-registry-validation.stderr.log'
stdout.write_bytes(result.stdout)
stderr.write_bytes(result.stderr)
def evidence(path):
    raw = path.read_bytes()
    return {'path': str(path), 'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}
receipt = {
    'kind': 'Actual local-only single-audit core validation subprocess receipt',
    'argv': [sys.executable, str(script)],
    'cwd': str(REPO), 'started_utc': started, 'ended_utc': ended,
    'exit_code': result.returncode,
    'script': evidence(script),
    'runner': evidence(Path(__file__).resolve()),
    'stdout': evidence(stdout), 'stderr': evidence(stderr),
    'own_audit_input': evidence(HERE / 'own-audit-before-schema-successor2.input.json'),
    'overlay': evidence(HERE / 'independent-source-review-overlay.core-validated.json'),
    'registry': evidence(HERE / 'local-own-audit-registry.json') if (HERE / 'local-own-audit-registry.json').exists() else None,
    'validator_modules': [evidence(REPO / 'tools/astis_semantic_roundtrip.py'), evidence(REPO / 'tools/astis_semantic_roundtrip_core.py')],
    'canonical_writes_performed': False,
    'foreign_audits_in_registry': False,
    'normal_proof_V_performed': False,
}
(HERE / 'local-registry-validation.receipt.json').write_text(json.dumps(receipt, indent=2) + '\n')
sys.stdout.buffer.write(result.stdout)
sys.stderr.buffer.write(result.stderr)
raise SystemExit(result.returncode)
