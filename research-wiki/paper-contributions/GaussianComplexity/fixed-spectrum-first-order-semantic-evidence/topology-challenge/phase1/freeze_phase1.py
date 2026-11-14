from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import runpy
import shutil

ROOT = Path('/Users/zhouhuanjian/ASTIS-GC')
PRIVATE = ROOT / '.astis/huanjian-gc-fixed-spectrum-first-order-20261108/topology-challenge/phase1'
PUBLIC = ROOT / 'research-wiki/paper-contributions/GaussianComplexity/fixed-spectrum-first-order-semantic-evidence/topology-challenge/phase1'
if (PRIVATE / 'PHASE1-FREEZE.json').exists() or (PUBLIC / 'PHASE1-FREEZE.json').exists():
    raise SystemExit('Phase 1 is already frozen; use a successor phase for changes.')

m = runpy.run_path(str(PRIVATE / 'extract_raw.py'))
source = m['SOURCE'].read_bytes()
source_sha = hashlib.sha256(source).hexdigest()
assert len(source) == 951991
assert source_sha == '6bc5ddc1e19cea9ba1dfe862fa79bc69fe861dff045d6ad1c7baa4a113c37915'
assert m['RAW'].encode('utf-8') == source, 'Parser text must preserve the original bytes.'

def sha(data):
    return hashlib.sha256(data).hexdigest()

def write_json(path, value):
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n')

instructions = [
    'AGENTS.md',
    '.agents/skills/astis-source-dependency-audit/SKILL.md',
    'docs/proof-digestion-protocol.md',
    'docs/evidence-routed-memory-protocol.md',
    'docs/theorem-publication-protocol.md',
    'docs/contributor-codex-contract.md',
    'research-wiki/paper-contributions/README.md',
]
(PRIVATE / 'instructions').mkdir(exist_ok=True)
instruction_records = []
for index, rel in enumerate(instructions, 1):
    data = (ROOT / rel).read_bytes()
    dest = PRIVATE / 'instructions' / f'{index:02d}-{rel.replace("/", "__")}.raw'
    dest.write_bytes(data)
    instruction_records.append({'source': rel, 'snapshot': str(dest.relative_to(PRIVATE)), 'bytes': len(data), 'sha256': sha(data)})

excerpt_ids = [
    'S2', 'S4', 'A3.SS4',
    'S1.p2', 'S1.Thmtheorem2', 'S1.Thmtheorem3',
    'bib.bib20', 'bib.bib3',
]
(PRIVATE / 'raw-excerpts').mkdir(exist_ok=True)
excerpt_records = []
for ident in excerpt_ids:
    n = m['PARSER'].ids[ident]
    data = m['RAW'][n.start:n.end].encode('utf-8')
    start = len(m['RAW'][:n.start].encode('utf-8'))
    end = len(m['RAW'][:n.end].encode('utf-8'))
    assert source[start:end] == data
    dest = PRIVATE / 'raw-excerpts' / f'{ident}.raw.html'
    dest.write_bytes(data)
    excerpt_records.append({'element_id': ident, 'snapshot': str(dest.relative_to(PRIVATE)), 'source_byte_start_inclusive': start, 'source_byte_end_exclusive': end, 'source_line_start': m['RAW'][:n.start].count('\n') + 1, 'bytes': len(data), 'sha256': sha(data)})
readable = ''.join(f'===== {ident} =====\n' + m['blocks'](m['PARSER'].ids[ident]) + '\n' for ident in excerpt_ids)
(PRIVATE / 'source-readable-excerpts.txt').write_text(readable)
write_json(PRIVATE / 'raw-excerpts.json', {'source': str(m['SOURCE'].relative_to(ROOT)), 'source_bytes': len(source), 'source_sha256': source_sha, 'excerpts': excerpt_records, 'instructions': instruction_records, 'readable_extraction_rule': 'Original HTML paragraph/table/heading content; math replaced with its original alttext; whitespace collapsed. Exact raw slices are authoritative.'})

nodes = [
    {'id': 'raw-global-domain', 'anchors': ['S2.Ex1', 'S2.SS0.SSS0.Px1.p1.1'], 'kind': 'source-definition-and-hypotheses', 'meaning': 'Symmetric centered Gaussian precision class; d>=1, kappa>=1.'},
    {'id': 'raw-global-potential-target', 'anchors': ['S2.SS0.SSS0.Px1.p1.2'], 'kind': 'literal-source-definition', 'meaning': 'f_A(x)=x^T A x/2 and pi_A=N(0,A^-1).'},
    {'id': 'raw-global-FO', 'anchors': ['S2.E1'], 'kind': 'literal-source-formula', 'meaning': 'FO=(f,gradient f)=(quadratic,Ax). Actual formal gradient existence is a semantics-expansion obligation.'},
    {'id': 'raw-exact-oracle-equivalence', 'anchors': ['S2.SS0.SSS0.Px1.p2.1'], 'kind': 'literal-source-argument', 'meaning': 'Project exact reply or recover value by exact inner product; same-matrix equivalence.'},
    {'id': 'raw-algorithm-model', 'anchors': ['S2.SS0.SSS0.Px2.p1.1', 'S2.E2', 'S2.SS0.SSS0.Px4.p1.2'], 'kind': 'standing-model', 'meaning': 'Borel adaptivity/output; input-independent seed; deterministic per-run cap; uniform input TV after seed averaging.'},
    {'id': 'raw-grid-domain', 'anchors': ['S4.SS1.p1.1', 'S4.E11'], 'kind': 'source-definition-and-hypotheses', 'meaning': 'd>=2,kappa>=2; half-shifted cosine grid, fixed diagonal spectrum.'},
    {'id': 'raw-rotation-model', 'anchors': ['S2.p2.1', 'S4.SS1.p1.2', 'S4.SS1.p2.1'], 'kind': 'standing-model-and-literal-definition', 'meaning': 'Full O(d); A=O Lambda O^T; Haar independent of seed only for lower-bound experiment; unknown rotation/public spectrum.'},
    {'id': 'raw-affine-same-O', 'anchors': ['S4.Thmtheorem2.p1.1'], 'kind': 'literal-source-formula-and-argument', 'meaning': 'Same O comparison A_k=(k-1)A_2-(k-2)I and bidirectional exact matvec reply determination.'},
    {'id': 'raw-admissibility', 'anchors': ['S4.Thmtheorem6.p1.1', 'A3.SS4.p1.1'], 'kind': 'source-theorem-and-proof', 'meaning': 'For every O in full O(d); angle/cosine/lambda bounds and orthogonal conjugation.'},
    {'id': 'raw-C4-calculus', 'anchors': ['A3.SS4.p2.1'], 'kind': 'literal-source-calculus-claims', 'meaning': 'Quadratic is C-infinity, Hessian=A, strong convexity/smoothness, zero unique minimizer. Gradient not separately displayed here.'},
    {'id': 'expanded-quadratic-gradient', 'anchors': ['S2.E1', 'A3.SS4.p2.1'], 'kind': 'elementary-semantics-expansion', 'meaning': 'Actual derivative/gradient existence and equality; discharge symmetry from the definition, never a free desired-conclusion binder.'},
    {'id': 'raw-C4-normalizer', 'anchors': ['A3.SS4.p3.1', 'A3.Ex160', 'A3.SS4.p3.2'], 'kind': 'literal-source-claim-and-argument', 'meaning': 'Gaussian integral and determinant invariance; fixed spectrum implies O-independent known normalizer.'},
    {'id': 'raw-main-parameters', 'anchors': ['S4.Thmtheorem1.p1.1', 'S4.Ex9', 'S4.SS3.p2.1'], 'kind': 'source-theorem-hypotheses', 'meaning': 'Fixed delta, large d(delta), kappa<=d^(1-delta), epsilon<=1/10; downstream only.'},
    {'id': 'raw-method-limitations', 'anchors': ['S4.SS4', 'S4.Thmtheorem8.p1.1'], 'kind': 'source-failure-boundary', 'meaning': 'Uniform Krylov obstruction and no epsilon growth for this test; stronger family bounds remain open.'},
]
edges = [
    {'consumer': 'raw-global-FO', 'use_site': 'S2.E1', 'and_parents': ['raw-global-domain', 'raw-global-potential-target'], 'note': 'Source formula scope; actual calculus semantics is not legalized by defining a pair.'},
    {'consumer': 'expanded-quadratic-gradient', 'use_site': 'Formal semantics of S2.E1 specialized to S4.E11', 'or_routes': [
        {'id': 'general-formula-specialization', 'and_parents': ['raw-global-FO', 'raw-admissibility', 'raw-global-potential-target'], 'obligation': 'A real general-gradient theorem and actual membership/same-body specialization, not an assumed equality.'},
        {'id': 'direct-quadratic-calculus', 'and_parents': ['raw-grid-domain', 'raw-rotation-model', 'raw-global-potential-target'], 'obligation': 'Derive symmetry internally; actual elementary differentiation. Positivity and normalizer unnecessary.'}
    ], 'note': 'Alternative sufficient formal expansions; do not claim both are author-literal independent proof routes.'},
    {'consumer': 'raw-exact-oracle-equivalence', 'use_site': 'S2.SS0.SSS0.Px1.p2.1', 'and_parents': ['raw-global-FO'], 'expansion_obligations': ['Projection and exact scalar reconstruction', 'For an algorithmic complexity claim, preservation of raw-algorithm-model']},
    {'consumer': 'raw-affine-same-O', 'use_site': 'S4.Thmtheorem2.p1.1', 'and_parents': ['raw-grid-domain', 'raw-rotation-model'], 'expansion_obligations': ['Same O at kappa and 2', 'Nonzero kappa-1 from local domain', 'Exact forward and inverse reply algebra']},
    {'consumer': 'raw-admissibility', 'use_site': 'A3.SS4.p1.1', 'and_parents': ['raw-grid-domain', 'raw-rotation-model'], 'expansion_obligations': ['Angle range', 'Cosine range', 'Eigenvalue interval', 'Symmetry and orthogonal quadratic-form bounds']},
    {'consumer': 'raw-C4-calculus', 'use_site': 'A3.SS4.p2.1', 'and_parents': ['raw-global-potential-target', 'raw-admissibility'], 'note': 'Spectral bounds are used for convexity/smoothness/coercivity; not all subclaims require them.'},
    {'consumer': 'raw-C4-normalizer', 'use_site': 'A3.SS4.p3.1-A3.SS4.p3.2', 'and_parents': ['raw-admissibility', 'raw-grid-domain', 'raw-rotation-model'], 'expansion_obligations': ['Gaussian integral', 'Determinant invariance'], 'note': 'A separate branch, never a necessary parent of pointwise first-order calculus.'},
]
write_json(PRIVATE / 'source-only-dependencies.json', {'status': 'phase1-source-only-challenge-not-candidate-verdict', 'scope': 'Bounded dependency shapes and adversarial tests, not exhaustive paper coverage', 'nodes': nodes, 'closure_shapes': edges, 'challenge_ids': [f'TC{i:02d}' for i in range(1,16)], 'challenge_meanings': 'See source-only-challenge.md, frozen with this JSON.', 'forbidden_implicit_AND_parents_of_pointwise_FO': ['raw-C4-normalizer', 'raw-affine-same-O', 'raw-main-parameters', 'raw-method-limitations', 'Krylov representation', 'target moments', 'concentration', 'public spectrum']})

PUBLIC.mkdir(parents=True, exist_ok=True)
for path in PRIVATE.rglob('*'):
    if path.is_file() and '__pycache__' not in path.parts:
        rel = path.relative_to(PRIVATE)
        target = PUBLIC / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(path, target)

files = []
for path in sorted(PUBLIC.rglob('*')):
    if path.is_file():
        data = path.read_bytes()
        rel = str(path.relative_to(PUBLIC))
        assert (PRIVATE / rel).read_bytes() == data
        files.append({'path': rel, 'bytes': len(data), 'sha256': sha(data)})
manifest = {'schema_version': 1, 'phase': 'source-only-phase1', 'source': {'path': str(m['SOURCE'].relative_to(ROOT)), 'bytes': len(source), 'sha256': source_sha}, 'private_root': str(PRIVATE.relative_to(ROOT)), 'public_root': str(PUBLIC.relative_to(ROOT)), 'files': files, 'candidate_or_graph_exposure': False, 'verdict_scope': 'Frozen independent raw-source cognition only; no producer, consumer, source graph or Lean result reviewed.'}
for base in [PRIVATE, PUBLIC]:
    write_json(base / 'manifest.json', manifest)
manifest_bytes = (PUBLIC / 'manifest.json').read_bytes()
seal = {'schema_version': 1, 'freeze_id': 'fixed-spectrum-first-order-topology-challenge-phase1-v1', 'frozen_at_utc': datetime.now(timezone.utc).isoformat(), 'source_sha256': source_sha, 'source_bytes': len(source), 'manifest_sha256': sha(manifest_bytes), 'report_sha256': sha((PUBLIC / 'source-only-challenge.md').read_bytes()), 'dependency_record_sha256': sha((PUBLIC / 'source-only-dependencies.json').read_bytes()), 'prohibited_inputs_opened': [], 'phase2_rule': 'Preserve phase1 bytes; all later graph/candidate findings are successor overlays.', 'status': 'frozen-source-only-not-admitted-not-source-VERIFIED'}
for base in [PRIVATE, PUBLIC]:
    write_json(base / 'PHASE1-FREEZE.json', seal)
print(json.dumps({'freeze_sha256': sha((PUBLIC / 'PHASE1-FREEZE.json').read_bytes()), **seal}, indent=2))
