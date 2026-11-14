"""Pin full current source-only code inputs for the fresh independent reviewer."""
from pathlib import Path
import hashlib
import json

phase = Path('.astis/semantic-neutral-20261112/ri_src_5ab9/phase3-code-only-inputs-v1')
phase.mkdir(exist_ok=False)
files = [
    'AutoSamplingTheory/ExampleCases/GaussianComplexity/FixedSpectrumSourceRowIndependence.lean',
    'Tests/GaussianComplexityFixedSpectrumSourceRowIndependence.lean',
    'AutoSamplingTheory/ExampleCases/GaussianComplexity/FixedSpectrumSourceRowLaw.lean',
    '.lake/packages/mathlib/Mathlib/Probability/Distributions/Gaussian/Multivariate.lean',
    '.lake/packages/mathlib/Mathlib/MeasureTheory/Constructions/Pi.lean',
    '.lake/packages/mathlib/Mathlib/Probability/ProductMeasure.lean',
    '.lake/packages/mathlib/Mathlib/Probability/Independence/Basic.lean',
    '.lake/packages/mathlib/Mathlib/Probability/Independence/Kernel/IndepFun.lean',
]
entries = []
for i, name in enumerate(files):
    source = Path(name)
    raw = source.read_bytes()
    target = phase / (str(i).zfill(2) + '-' + source.name + '.raw.txt')
    with target.open('xb') as out:
        out.write(raw)
    entries.append({'source': name, 'copy': str(target), 'bytes': len(raw),
                    'sha256': hashlib.sha256(raw).hexdigest()})
manifest = {
    'scope': 'Current full producer/private consumer, actual canonical row-law provider and exact pinned Mathlib product/Gaussian/independence sources. No compiler/kernel, decoder, publication or prior audit verdict.',
    'producer_sha256': entries[0]['sha256'], 'private_consumer_sha256': entries[1]['sha256'],
    'mathlib_pin': 'db584cd6d46c92f209a44c0f1c829460d327499d',
    'inputs': entries,
}
path = phase / 'input-manifest.json'
raw = (json.dumps(manifest, ensure_ascii=False, indent=2) + '\n').encode()
with path.open('xb') as out:
    out.write(raw)
print(json.dumps({'manifest': str(path), 'sha256': hashlib.sha256(raw).hexdigest(),
                  'full_input_copies': len(entries), 'producer_sha256': entries[0]['sha256'],
                  'private_consumer_sha256': entries[1]['sha256']}))
