"""Expose the existing Matrix alias in proof-local feature data; exact target stays sealed."""
from pathlib import Path
import hashlib
import json

workspace = Path(__file__).resolve().parent
path = Path('Tests/GaussianComplexityFixedSpectrumSourceMatrixMean.lean')
raw = path.read_bytes()
with (workspace / 'consumer-implementation-attempt1.original.lean').open('xb') as out:
    out.write(raw)
head, body = raw.decode().split(':= by\n', 1)
old = '  let t : Fin d → Fin (q + 1) → ℝ :='
assert body.count(old) == 1
body = body.replace(old, '  let t : Matrix (Fin d) (Fin (q + 1)) ℝ :=', 1)
path.write_text(head + ':= by\n' + body)
seal = json.loads((workspace / 'statement-seal-v1.json').read_bytes())
assert seal['actual_private_consumer']['signature'] in head
with (workspace / 'consumer-firstbuild-diagnosis.json').open('x') as out:
    out.write(json.dumps({
        'class': 'IMPLEMENTATION_FAILED', 'scope': 'Proof-local Matrix alias annotation',
        'reason': 'The literal feature function was proof-locally annotated as a bare function, so field notation resolved to Function.transpose and no matrix multiplication instance. Exposing definitionally equal Matrix annotation fixes elaboration only.',
        'original_sha256': hashlib.sha256(raw).hexdigest(),
        'original_source': str(workspace / 'consumer-implementation-attempt1.original.lean'),
        'sealed_signature_unchanged': True, 'producer_unchanged': True,
        'source_hypothesis_or_mathematical_route_change': False,
        'failed_actual_receipt': '.astis/huanjian-resume-20261103/20261112T124944789396Z-source-matrix-mean-real-consumer-firstbuild.receipt.json',
    }, ensure_ascii=False, indent=2) + '\n')
print('Only proof-local t annotation changed to the identical Matrix carrier; sealed type retained.')
