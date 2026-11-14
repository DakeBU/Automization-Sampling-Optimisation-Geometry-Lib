from pathlib import Path
import hashlib, json, subprocess

W = Path(__file__).resolve().parent.relative_to(Path.cwd())
E = Path('research-wiki/paper-contributions/GaussianComplexity/fixed-spectrum-krylov-range-semantic-evidence')
S = Path('.astis/semantic-neutral-20261111/kr_src_c47e12')
C = Path('research-wiki/frontier-cells/ASTIS-SW-GAUSSIAN-COMPLEXITY-fixed-spectrum-krylov-range.json')
A = Path('research-wiki/semantic-roundtrip/audits/huanjian-fixed-spectrum-krylov-range.json')
base = '972d8994a816bc63d2dd6fb2db1c2c638fa9a48f'
sha = lambda b: hashlib.sha256(b).hexdigest()
assert subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip() == base
assert not subprocess.check_output(['git', 'diff', '--cached', '--name-only']).strip()
assert json.loads(A.read_bytes())['state'] == 'source-reviewed'
assert json.loads(C.read_bytes())['status'] == 'proved_locally'
for p in ['AutoSamplingTheory/ExampleCases/GaussianComplexity/FixedSpectrumKrylovRange.lean', 'Tests/GaussianComplexityFixedSpectrumKrylovRange.lean', 'website/content/declaration_lessons/huanjian-fixed-spectrum-krylov-range.json', 'website/content/publications/huanjian-fixed-spectrum-krylov-range.json', 'runs/substantive_advances.jsonl']:
    assert Path(p).read_bytes() == subprocess.check_output(['git', 'show', base+':'+p]), p
readme = E/'README.md'
old = readme.read_bytes()
prefix = b'''# Independent bounded review carried; normal source VERIFIED pending

Exact mathematical candidate972d8994 has genuine raw-first/type-first/full-proof
source acceptance by /root/krylov_fresh_source_c47e12 and independent fresh native
P->T->kernel/static checks by /root/krylov_native_reader_5f09a3. The source role
independently reproduced the full binding7b97440e and preserved the intentional
anti-anchored context redactions and original failed trials.

Native exact raw signatures and kernel definitional equality pass. Literal raw
Expr structural equality is FALSE because numeral/index proof packaging differs;
this diagnostic is retained rather than called syntactic equality. Four closed
Prop declarations are reachable and std3-only: two handwritten roots and two
generated implementation certificates, with zero extra mathematical credit.

All186 native locator checks and50 canonical actual-direct-use checks pass.
Six closed exact code folds and full4803-byte Test in step6 pass. Individual step
copy/download/context controls and the private numbered provenance-page controls
remain deficient. No live browser, MathJax, clipboard, mobile, final shell or
website acceptance is granted. The disabled reader overlay has not been applied.

This is a metadata/evidence carrier. Root sourceV API calls remain ZERO. The
advance stays PROVED_LOCAL pending the original independent actor's separately
authorized normal verification. Original global owner remains STABILIZING; no
shared imports/Registry/graph/site, clean-port, remote push, publication,
purification, Exposition Seal or whole-Goal completion is claimed.

The earlier candidate README follows byte-exact as historical context.

'''
readme.write_bytes(prefix+old)
dest = E/'postcandidate-root-process-scripts'
assert not dest.exists()
dest.mkdir()
for n in ['commit_exact_candidate.py', 'carry_frozen_native_review.py', 'carry_frozen_native_review_v2.py', 'attach_frozen_source_review.py', 'commit_reviewed_metadata.py']:
    (dest/n).write_bytes((W/n).read_bytes())
    (dest/n).chmod(0o444)
original_refs = [S/n for n in ['phase3/mathematical-source-proof-reader-judgment.json', 'phase3/original-execution-receipt.json', 'phase4/canonical-semantic-review-result.v2.json', 'phase4/mapping-and-adapter-process-judgment.json', 'phase4/exact-binding-reproduction.json']]
before_changes = subprocess.check_output(['git', 'diff', '--name-only', '-z']).decode().rstrip('\0').split('\0')
assert all(p in {str(C), str(A)} or p.startswith(str(E)+'/') for p in before_changes), before_changes
paths = [C, A]+sorted(p for p in E.rglob('*') if p.is_file())+original_refs
record = {str(p): {'sha256': sha(p.read_bytes()), 'bytes': p.stat().st_size} for p in paths}
(W/'reviewed-metadata-selected-files.private.json').write_text(json.dumps(record, ensure_ascii=False, indent=2)+'\n')
subprocess.run(['git', 'add', '-f', '--', *record], check=True)
staged = subprocess.check_output(['git', 'diff', '--cached', '--name-only', '-z']).decode().rstrip('\0').split('\0')
assert set(staged) <= set(record) and staged
for name in staged:
    assert sha(subprocess.check_output(['git', 'show', ':'+name])) == record[name]['sha256'], name
subprocess.run(['git', 'diff', '--cached', '--check'], check=True)
subprocess.run(['git', 'commit', '-m', 'docs(gaussian): carry independent Krylov source and native reviews'], check=True)
commit = subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip()
assert subprocess.check_output(['git', 'rev-parse', 'HEAD^'], text=True).strip() == base
for name in staged:
    assert sha(subprocess.check_output(['git', 'show', commit+':'+name])) == record[name]['sha256'], name
out = {'mathematical_candidate': base, 'reviewed_metadata_commit': commit, 'selected_changed_files': len(staged), 'all_staged_bytes_exact_in_Git': True, 'original_cited_source_run_paths_carried': len(original_refs), 'no_Lean_lesson_publication_or_ledger_bytes_changed': True, 'sourceV': False, 'global': False}
(W/'actual-reviewed-metadata-commit.json').write_text(json.dumps(out, indent=2)+'\n')
print(json.dumps(out))
