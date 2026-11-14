"""Freeze exact code/provider bytes without compiler or review verdict inputs."""
from pathlib import Path
import hashlib
import json
import subprocess

base = Path('.astis/semantic-neutral-20261112/mm_src_8c31/code-only-inputs-v1')
base.mkdir(exist_ok=False)
roots = [Path('AutoSamplingTheory/ExampleCases/GaussianComplexity/FixedSpectrumSourceMatrixMean.lean'),
         Path('Tests/GaussianComplexityFixedSpectrumSourceMatrixMean.lean')]
sources = []
pending = list(roots)
while pending:
    path = pending.pop(0)
    if path in sources:
        continue
    sources.append(path)
    for line in path.read_text().splitlines():
        if line.startswith('import AutoSamplingTheory.'):
            pending.append(Path(line.removeprefix('import ').replace('.', '/') + '.lean'))
assert len(sources) == 7
sources += [Path('.lake/packages/mathlib/Mathlib') / name for name in [
    'Probability/Distributions/Gaussian/Multivariate.lean',
    'MeasureTheory/Constructions/Pi.lean',
    'MeasureTheory/Integral/Bochner/Basic.lean',
    'MeasureTheory/Integral/Bochner/ContinuousLinearMap.lean',
    'MeasureTheory/Function/L1Space/Integrable.lean',
    'LinearAlgebra/Matrix/Kronecker.lean',
    'Analysis/CStarAlgebra/Matrix.lean',
]]
entries = []
for i, source in enumerate(sources):
    raw = source.read_bytes()
    destination = base / (str(i).zfill(2) + '-' + str(source).replace('/', '__') + '.raw.txt')
    with destination.open('xb') as out:
        out.write(raw)
    entries.append({'source': str(source), 'destination': str(destination),
                    'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()})
manifest = {
    'role': 'Whole-code-only exact input snapshots; no compiler/decoder/source-review/topology verdict.',
    'worktree_HEAD_at_capture': subprocess.check_output(['git', 'rev-parse', 'HEAD']).decode().strip(),
    'new_math_files_are_uncommitted_worktree_bytes': True,
    'actual_new_math_commit_claimed': False,
    'all_ASTIS_transitive_import_sources': 7, 'whole_source_files': len(entries),
    'entries': entries,
    'unapproved_inputs': 'No earlier implementation version, failure diagnosis, compiler output/receipt, semantic/source graph, prior review or repair. Preserve own raw/type freezes.',
}
path = base / 'input-manifest.json'
raw = (json.dumps(manifest, ensure_ascii=False, indent=2) + '\n').encode()
with path.open('xb') as out:
    out.write(raw)
print(json.dumps({'path': str(path), 'sha256': hashlib.sha256(raw).hexdigest(), 'whole_source_files': len(entries)}))
