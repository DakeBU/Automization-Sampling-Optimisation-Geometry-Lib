"""Snapshot complete ASTIS code closure and selected pinned external providers, without verdicts."""
from pathlib import Path
import hashlib
import json
import subprocess

base = Path('.astis/semantic-neutral-20261112/mv_src_6e28/shared-code-only-inputs-v1')
base.mkdir(exist_ok=False)
roots = [Path('AutoSamplingTheory/TechnicalLemmas/Probability/RealMatrixPositiveIntegral.lean'),
         Path('AutoSamplingTheory/ExampleCases/GaussianComplexity/FixedSpectrumSourceMatrixVariance.lean'),
         Path('Tests/RealMatrixPositiveIntegral.lean')]
sources, pending = [], list(roots)
while pending:
    path = pending.pop(0)
    if path in sources:
        continue
    sources.append(path)
    for line in path.read_text().splitlines():
        if line.startswith('import AutoSamplingTheory.'):
            pending.append(Path(line.removeprefix('import ').replace('.', '/') + '.lean'))
astis_count = len(sources)
assert astis_count == 9
sources += [Path('.lake/packages/mathlib/Mathlib') / name for name in [
    'Probability/Distributions/Gaussian/Multivariate.lean',
    'MeasureTheory/Constructions/Pi.lean',
    'MeasureTheory/Integral/Bochner/Basic.lean',
    'MeasureTheory/Integral/Bochner/ContinuousLinearMap.lean',
    'MeasureTheory/Function/L1Space/Integrable.lean',
    'LinearAlgebra/Matrix/Kronecker.lean',
    'Analysis/CStarAlgebra/Matrix.lean',
    'Analysis/Convex/Integral.lean',
    'Algebra/Order/Star/Real.lean',
    'LinearAlgebra/Matrix/PosDef.lean',
    'Analysis/Matrix/Order.lean',
]]
entries = []
for i, source in enumerate(sources):
    raw = source.read_bytes()
    dest = base / (str(i).zfill(2) + '-' + str(source).replace('/', '__') + '.raw.txt')
    with dest.open('xb') as out:
        out.write(raw)
    entries.append({'source': str(source), 'destination': str(dest), 'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()})
record = {'role': 'Whole-code-only exact snapshots; no compiler/decoder/source-review/topology verdict or authored exposition.',
          'worktree_HEAD_at_capture': subprocess.check_output(['git', 'rev-parse', 'HEAD']).decode().strip(),
          'new_math_files_are_uncommitted_worktree_bytes': True, 'actual_new_math_commit_claimed': False,
          'all_ASTIS_transitive_import_sources_including_build_entry': astis_count,
          'whole_source_files': len(entries), 'entries': entries,
          'unapproved_inputs': 'Do not open previous implementation versions, failure diagnosis, compiler results/receipts, canonical audits, source graphs, prior reviewers or later exposition. Preserve own earlier raw/type files.'}
path = base / 'input-manifest.json'
raw = (json.dumps(record, ensure_ascii=False, indent=2) + '\n').encode()
with path.open('xb') as out:
    out.write(raw)
print(json.dumps({'path': str(path), 'sha256': hashlib.sha256(raw).hexdigest(), 'whole_source_files': len(entries), 'complete_ASTIS_modules': astis_count}))
