"""Supply the independent reviewer's precise missing upstream providers; preserve original20."""
from pathlib import Path
import hashlib
import json

root = Path('.astis/semantic-neutral-20261112/mv_src_6e28')
prior_path = root / 'shared-code-only-inputs-v1/input-manifest.json'
prior_raw = prior_path.read_bytes()
sha = lambda raw: hashlib.sha256(raw).hexdigest()
assert sha(prior_raw) == 'a732bbf0514472df4ddbc24daf24bc8a2aa6059ff3f8eca46cb98d0f767d203b'
prior = json.loads(prior_raw)
for item in prior['entries']:
    raw = Path(item['destination']).read_bytes()
    assert len(raw) == item['bytes'] and sha(raw) == item['sha256']
    assert Path(item['source']).read_bytes() == raw
base = root / 'shared-code-only-provider-supplement-v1'
base.mkdir(exist_ok=False)
entries = []
for i, name in enumerate([
    'Probability/Distributions/Gaussian/Real.lean',
    'Probability/Distributions/Gaussian/Fernique.lean',
    'Probability/Independence/Integration.lean',
    'MeasureTheory/Integral/Pi.lean',
    'MeasureTheory/SpecificCodomains/Pi.lean',
    'Probability/Moments/MGFAnalytic.lean',
    'Probability/Moments/IntegrableExpMul.lean',
]):
    source = Path('.lake/packages/mathlib/Mathlib') / name
    raw = source.read_bytes()
    dest = base / (str(i).zfill(2) + '-' + name.replace('/', '__') + '.raw.txt')
    with dest.open('xb') as out:
        out.write(raw)
    entries.append({'source': str(source), 'destination': str(dest), 'bytes': len(raw), 'sha256': sha(raw)})
manifest = {'role': 'Exact reviewer-requested upstream code providers only; no compiler/review verdict/exposition.', 'prior_manifest': str(prior_path), 'prior_manifest_sha256': sha(prior_raw), 'all_original20_sources_and_snapshots_unchanged': True, 'whole_source_files': len(entries), 'entries': entries, 'requested_MGF_provider_locations': ['Probability/Moments/MGFAnalytic.lean:92:iteratedDeriv_mgf_zero', 'Probability/Moments/IntegrableExpMul.lean:535:integrable_pow_of_mem_interior_integrableExpSet']}
path = base / 'input-manifest.json'
raw = (json.dumps(manifest, ensure_ascii=False, indent=2) + '\n').encode()
with path.open('xb') as out:
    out.write(raw)
print(json.dumps({'path': str(path), 'sha256': sha(raw), 'additional_full_sources': len(entries), 'original20_unchanged': True}))
