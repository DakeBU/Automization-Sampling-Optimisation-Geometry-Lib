from pathlib import Path
import hashlib, json, sys

r = Path(__file__).parent
sys.path.insert(0, str(Path.cwd() / 'tools'))
from astis_advance import checkpoint_advance

production = Path('AutoSamplingTheory/ExampleCases/ProximalBPS/ActualL2Expectation.lean')
assert hashlib.sha256(production.read_bytes()).hexdigest() == '4c35e0b71362bec3563e3d07c9f122d6b7ca4cae604f7a88aad397d2a028f4d6'
out = r / 'checkpoint-full-compiled107.json'
assert not out.exists()
record = checkpoint_advance(
    'ASTIS-SA-20261012-PBPSActualL2Expectation',
    worker_id='companion_root_20261005',
    route_fingerprint='actual106-joint-clock-integral-and-adjoint-L2-averaging',
    progress_signature='full-sealed-target-compiled-independent-whole-math-accepted',
    mathematical_delta='The complete sealed same-process theorem compiles. Joint Borel expectation, bounded every-section L1, arbitrary MemLp AE section L1, internally constructed L2 contraction family, exact quotient identification, square-integral contraction and A0=id are proved. Independent whole mathematics and exact sealed-header kernel accepted; standard three axioms only.',
    exact_residual='Blind decoding and final source/exposition admission, independently reviewed selected representative-independence route overlay, exact-commit verification and sole-lane aggregate publication remain pending. Full L2 flip identity, actual restart/semigroup, hypocoercivity, errors, costs, composition and all four complete papers remain open.',
)
out.write_text(json.dumps(record, ensure_ascii=False, indent=2) + '\n', encoding='utf8', newline='\n')
print('Recorded full compiled checkpoint; no admission status promoted.')
