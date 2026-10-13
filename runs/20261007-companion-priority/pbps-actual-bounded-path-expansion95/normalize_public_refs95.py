"""Normalize only canonical references; retain immutable native review evidence."""
from pathlib import Path
import hashlib, json, subprocess, sys
root = Path(__file__).resolve().parents[3]
run = Path(__file__).resolve().parent
sys.path.insert(0, str(root / 'tools'))
import astis_publication as pub
paths = [
    'website/content/publications/pbps-actual-bounded-path-expansion.json',
    'research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261011-PBPSActualBoundedPathExpansion.json',
    'research-wiki/frontier-cells/ASTIS-SW-PBPS-actual-bounded-path-expansion.json',
]
coverage = 'runs/20261007-companion-priority/pbps-actual-bounded-path-expansion95/primary-source95/compiled-source-coverage95.native.json'
assert (root / coverage).is_file()
rows = []
def normalize(value):
    if isinstance(value, dict):
        return {k: normalize(v) for k, v in value.items()}
    if isinstance(value, list):
        return [normalize(v) for v in value]
    if isinstance(value, str) and value.replace('\\', '/').startswith('E:/Samplinglib/'):
        return value.replace('\\', '/')[len('E:/Samplinglib/'):]
    return value
old_binding = json.loads((root / paths[1]).read_bytes())['publication_binding_sha256']
for name in paths:
    p = root / name
    before = p.read_bytes()
    data = normalize(json.loads(before))
    if name.startswith('website/'):
        data['items'][0]['source_proof_coverage']['coverage_report'] = coverage
    elif '/frontier-cells/' in name:
        data['source_proof_coverage']['coverage_report'] = coverage
    after = (json.dumps(data, ensure_ascii=False, indent=2) + '\n').encode()
    p.write_bytes(after)
    rows.append(dict(path=name, before_raw_sha256=hashlib.sha256(before).hexdigest(), after_raw_sha256=hashlib.sha256(after).hexdigest()))
pub.inputs.cache_clear()
pub.load.cache_clear()
item = json.loads((root / paths[0]).read_bytes())['items'][0]
binding = pub.binding_digest(item, item['bindings'][0], pub.inputs())
assert binding == old_binding, (binding, old_binding)
pub.check_advance([item['bindings'][0]['declaration']], reviewed=True)
receipt = dict(kind='canonical-reference-portability-correction', parent_commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=root).decode().strip(), changes=rows, publication_binding_sha256=binding, mathematical_inputs_unchanged=True, native_review_artifacts_unchanged=True, coverage_report=coverage, scope='Repository-relative canonical references and final compiled coverage pointer only; historical native paths retained as provenance.')
(run / 'public-reference-correction95.json').write_bytes((json.dumps(receipt, indent=2)+'\n').encode())
print(json.dumps(receipt))
