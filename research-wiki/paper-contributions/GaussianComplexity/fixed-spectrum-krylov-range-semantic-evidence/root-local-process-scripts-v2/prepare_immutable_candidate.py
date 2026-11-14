from pathlib import Path
import hashlib, json, shutil, subprocess

W = Path(__file__).resolve().parent.relative_to(Path.cwd())
E = Path('research-wiki/paper-contributions/GaussianComplexity/fixed-spectrum-krylov-range-semantic-evidence')
sha = lambda b: hashlib.sha256(b).hexdigest()
assert subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip() == '6a7a3a454b3ded093e335f57032227d3de02663f'
assert not subprocess.check_output(['git', 'diff', '--cached', '--name-only']).strip(), 'Preserve foreign staged work; do not clear it.'
capsule = json.loads((E/'local-proof-capsule.json').read_bytes())
assert capsule['state'] == 'PROVED_LOCAL_NOT_SOURCE_VERIFIED'
assert capsule['append_sha256'] == '9c72a978e91690e65d11c3f47da6e85f50355c5af232f7406a23c160f1a4a21b'
event = (E/'actual-PROVED_LOCAL-append.exact.jsonl').read_bytes()
assert sha(event) == capsule['append_sha256']
assert Path('runs/substantive_advances.jsonl').read_bytes().endswith(event)
scripts = ['seal_exact_statements.py', 'correct_unsealed_reserved_identifier.py', 'elaborate_unsealed_actual_Euclidean_consumer.py', 'correct_definition_locator_metadata_overlay.py', 'reserve_frontier_and_selective_types.py', 'prepare_normal_intake.py', 'admit_normal_intake_prepared.py', 'prepare_prospective_admission_request.py', 'confirm_actual_intake_success.py', 'author_publication.py', 'complete_publication_after_wording_enum.py', 'complete_publication_after_wording_enum_v2.py', 'attach_independent_decoder.py', 'attach_independent_source_map.py', 'archive_preproof_and_actual_checks.py', 'record_proved_local.py', 'prepare_immutable_candidate.py']
dest = E/'root-local-process-scripts'
assert not dest.exists()
dest.mkdir()
for name in scripts:
    p = W/name
    data = p.read_bytes()
    assert b'xwechat_files' not in data and b'wxid_' not in data
    (dest/name).write_bytes(data)
    (dest/name).chmod(0o444)
for name in ['late-process-observations.json', 'root-confirmed-actual-intake-success.json']:
    (E/name).write_bytes((W/name).read_bytes())
readme = '''# Actual cosine-feature Krylov range: local proof candidate

The exact sealed producer proves range(B)=K_q for the literal affine cosine
spectrum, arbitrary deterministic starts, kappa>=2, and2q+1<d, includingq=0.
The private consumer materially uses it to obtain one c with Bc=v and derives
both actual Euclidean quadratic identities with that same coefficient vector.

The real module build and bounded kernel check succeeded. The two handwritten
roots and two generated internal certificates are closed reachable theorems
using only the standard3 axioms; generated certificates grant no extra results.
The producer has no public ASTIS proof parents. The consumer's sole public
ASTIS parent is this producer. Canonical Mathlib polynomial/span/matrix facts
are reused directly; the separate cosine Gram and Gaussian moments are not
forced formal parents.

Normal PROVED_LOCAL succeeded once. Its exact append and preservation capsule
are retained. Independent source-blind reconstruction is attached byte-exact;
fresh source review read raw source, then froze exact-type review, and is now
reviewing the full proof/lesson. Independent fresh native/static-reader review
at this immutable candidate is pending. Root has made no VERIFIED transition.

The source graph and repaired topology are in the complete530-file original
archive; the198-file mapping-author archive is a proposal, not acceptance.
The map's historical absolute paths are retained unchanged. Any public
machine-independent adaptation needs separate reviewed integration. All failed
root proof/metadata attempts and independent process failures remain inspectable.

Concentration/absoluteC, full Lemma4.4, both main lower bounds, real joint/adaptive
oracle/precision/TV/cost adapters and final reader delivery remain open. The
original global stabilization owner retains its lease. All twelve previous
source VERIFIED objects, other queues/frontiers and reader HOLDs are preserved.
No global site, shared imports, Registry, graph, clean-port, push, publication,
purification, Exposition Seal or whole-Goal completion is claimed here.
'''
(E/'README.md').write_text(readme)
stems = ['20261110T194412958713Z-krylov-range-producer-real-module-build', '20261110T194618916593Z-krylov-range-producer-and-genuine-consumer-real-module-build', '20261110T194651267045Z-krylov-range-exact-sealed-types-all-owned-closed-kernel-and-actual-parents', '20261110T200824013068Z-krylov-range-one-normal-PROVED_LOCAL-after-real-math-and-publication']
rpaths = []
for stem in stems:
    rp = Path('.astis/huanjian-resume-20261103')/(stem+'.receipt.json')
    x = json.loads(rp.read_bytes())
    assert x['exit_code'] == 0 and sha(Path(x['log']).read_bytes()) == x['log_sha256']
    rpaths.extend([rp, Path(x['log']).relative_to(Path.cwd())])
paths = [Path(p) for p in ['AutoSamplingTheory/ExampleCases/GaussianComplexity/FixedSpectrumKrylovRange.lean', 'Tests/GaussianComplexityFixedSpectrumKrylovRange.lean', 'research-wiki/frontier-cells/ASTIS-SW-GAUSSIAN-COMPLEXITY-fixed-spectrum-krylov-range.json', 'research-wiki/paper-contributions/GaussianComplexity/fixed-spectrum-krylov-range-statement-seal.json', 'website/content/declaration_lessons/huanjian-fixed-spectrum-krylov-range.json', 'website/content/publications/huanjian-fixed-spectrum-krylov-range.json', 'research-wiki/semantic-roundtrip/audits/huanjian-fixed-spectrum-krylov-range.json', 'runs/substantive_advances.jsonl']]
paths += sorted(p for p in E.rglob('*') if p.is_file())
paths += rpaths
assert len(paths) == len(set(paths))
for p in paths:
    assert p.is_file() and not p.is_symlink()
    assert p.stat().st_size < 20_000_000, p
    assert 'private-phase' not in str(p) and not p.name.endswith('.private.json'), p
record = {'intended_base': '6a7a3a454b3ded093e335f57032227d3de02663f', 'files': {str(p): {'sha256': sha(p.read_bytes()), 'bytes': p.stat().st_size} for p in paths}, 'scope': 'Exact selected local mathematical candidate only. No foreign staged work, private baselines, global/stabilization/publication acceptance or remote action.'}
out = W/'immutable-candidate-selected-files.private.json'
assert not out.exists()
out.write_text(json.dumps(record, ensure_ascii=False, indent=2)+'\n')
print(json.dumps({'selected_files': len(paths), 'candidate_manifest': str(out), 'private_manifest_not_exported': True, 'PLOCAL': True, 'sourceV': False}))
