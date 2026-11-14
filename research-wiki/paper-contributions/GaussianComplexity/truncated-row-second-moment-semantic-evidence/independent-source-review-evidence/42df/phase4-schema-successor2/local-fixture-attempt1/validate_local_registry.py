from pathlib import Path
import hashlib
import json
import sys

HERE = Path(__file__).resolve().parent
REPO = Path('/Users/zhouhuanjian/ASTIS-GC')
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / 'tools'))
from tools import astis_semantic_roundtrip as rt
from tools import astis_semantic_roundtrip_core as core

audit = json.loads((HERE / 'own-audit-before-schema-successor2.input.json').read_bytes())
overlay = json.loads((HERE / 'independent-source-review-overlay.core-validated.json').read_bytes())
assert set(overlay) == {'state', 'semantic_slots', 'deltas', 'verdict', 'source_review', 'repairs'}
assert overlay['source_review']['review_run_sha256'] == '86207f4e0ddacfd449765baa82e5b2e5364eb9cf42a81b4705d707dd4ce3c74f'
assert overlay['source_review']['reviewer_packet_sha256'] == 'c7580b10335851b283623638ef1b70e025547a4ee134c481acd75c5deae81b8b'
assert overlay['source_review']['publication_binding_sha256'] == 'cc869c78be53c6197a600c399d0c9822665e9125b4c3db9a7437283903d94382'
for key, value in overlay.items():
    audit[key] = value
registry = {
    'schema_version': 1,
    'protocol': {key: 'required' for key in [
        'decoder_blindness', 'decoder_context_content_scan',
        'independent_source_review', 'source_review_packet_binding',
        'independent_repair_review', 'repair_review_packet_binding']},
    'semantic_slots': list(core.SEMANTIC_SLOTS),
    'decoder_allowed_inputs': list(core.DECODER_INPUT_ARTIFACTS),
    'audits': [audit],
}
output = HERE / 'local-own-audit-registry.json'
output.write_text(json.dumps(registry, ensure_ascii=False, indent=2) + '\n')
errors = rt.validate_registry(registry)
print(json.dumps({
    'validator': 'tools.astis_semantic_roundtrip.validate_registry',
    'audit_count': 1,
    'audit_id': audit['id'],
    'registry_path': str(output),
    'registry_sha256': hashlib.sha256(output.read_bytes()).hexdigest(),
    'overlay_sha256': hashlib.sha256((HERE / 'independent-source-review-overlay.core-validated.json').read_bytes()).hexdigest(),
    'result': 'valid' if not errors else 'invalid',
    'errors': errors,
}, ensure_ascii=False, indent=2))
raise SystemExit(1 if errors else 0)
