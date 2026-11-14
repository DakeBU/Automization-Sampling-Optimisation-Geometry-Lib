"""Preserve the first implementation and supply the standard real star-order instance."""
from pathlib import Path
import hashlib
import json

workspace = Path(__file__).resolve().parent
path = Path('AutoSamplingTheory/TechnicalLemmas/Probability/RealMatrixPositiveIntegral.lean')
raw = path.read_bytes()
assert hashlib.sha256(raw).hexdigest() == '34961091b8c8c8201561825d8ed715abbb61707b318e5879894fcf5d4f5b777c'
with (workspace / 'producer-implementation-attempt1.original.lean').open('xb') as out:
    out.write(raw)
fixed = b'import Mathlib.Algebra.Order.Star.Real\n' + raw
path.write_bytes(fixed)
diagnosis = {'classification': 'IMPLEMENTATION_FAILED', 'cause': 'Minimal imports did not bring Real.instStarOrderedRing into scope for the PSD scalar-closure application.', 'actual_missing_provider': 'Mathlib.Algebra.Order.Star.Real:Real.instStarOrderedRing', 'change': 'Add only the standard provider import.', 'sealed_signature_unchanged': True, 'mathematical_route_unchanged': True, 'no_new_binder_or_source_repair': True, 'first_attempt_source_preserved': True}
with (workspace / 'producer-firstbuild-diagnosis.json').open('x') as out:
    out.write(json.dumps(diagnosis, indent=2) + '\n')
print(json.dumps(diagnosis))
