from pathlib import Path
import hashlib, json, subprocess

W = Path(__file__).resolve().parent.relative_to(Path.cwd())
E = Path('research-wiki/paper-contributions/GaussianComplexity/fixed-spectrum-krylov-range-semantic-evidence')
base = '972d8994a816bc63d2dd6fb2db1c2c638fa9a48f'
sha = lambda b: hashlib.sha256(b).hexdigest()
assert subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip() == base
record = json.loads((W/'reviewed-metadata-selected-files.private.json').read_bytes())
exceptions = [str(Path(root)/p) for root in ['.astis/semantic-neutral-20261111/kr_src_c47e12', str(E/'independent-source-c47e12')] for p in ['phase3/mathematical-source-proof-reader-judgment.json', 'phase4/mapping-and-adapter-process-judgment.json']]
for name in exceptions:
    b = Path(name).read_bytes()
    assert b.endswith(b'\n\n') and sha(b) == record[name]['sha256'], name
    json.loads(b)
note = {'scope': 'Exactly four original independent-source JSON evidence artifacts; originals and portable copies remain byte-exact.', 'exception': 'Command-local Git blank-at-eof check disabled only for these four artifacts. Every other staged file uses default whitespace check; all other whitespace diagnostics still apply to these four. No Git config or source/proof/semantic payload is normalized.', 'files': {n: record[n] for n in exceptions}, 'actual_initial_failed_receipt': '.astis/huanjian-resume-20261103/20261110T205203711761Z-krylov-range-immutable-carrier-original-source-native-reviews-no-normal-V.receipt.json', 'sourceV_or_global': False}
np = E/'original-source-evidence-exact-EOF-preservation.json'
assert not np.exists()
np.write_text(json.dumps(note, ensure_ascii=False, indent=2)+'\n')
sp = E/'postcandidate-root-process-scripts'/Path(__file__).name
assert not sp.exists()
sp.write_bytes(Path(__file__).read_bytes())
for p in [np, sp]:
    record[str(p)] = {'sha256': sha(p.read_bytes()), 'bytes': p.stat().st_size}
subprocess.run(['git', 'add', '-f', '--', str(np), str(sp)], check=True)
staged = subprocess.check_output(['git', 'diff', '--cached', '--name-only', '-z']).decode().rstrip('\0').split('\0')
assert staged and set(staged) <= set(record)
for name in staged:
    assert sha(Path(name).read_bytes()) == record[name]['sha256']
    assert sha(subprocess.check_output(['git', 'show', ':'+name])) == record[name]['sha256']
subprocess.run(['git', 'diff', '--cached', '--check', '--', '.', *[':(exclude)'+n for n in exceptions]], check=True)
subprocess.run(['git', '-c', 'core.whitespace=-blank-at-eof', 'diff', '--cached', '--check', '--', *exceptions], check=True)
subprocess.run(['git', 'commit', '-m', 'docs(gaussian): carry independent Krylov source and native reviews'], check=True)
commit = subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip()
assert subprocess.check_output(['git', 'rev-parse', 'HEAD^'], text=True).strip() == base
for name in staged:
    assert sha(subprocess.check_output(['git', 'show', commit+':'+name])) == record[name]['sha256']
out = {'mathematical_candidate': base, 'reviewed_metadata_commit': commit, 'selected_changed_files': len(staged), 'all_staged_bytes_exact_in_Git': True, 'original_cited_source_run_paths_carried': 5, 'exact_original_EOF_exceptions': exceptions, 'no_Lean_lesson_publication_or_ledger_bytes_changed': True, 'sourceV': False, 'global': False}
(W/'actual-reviewed-metadata-commit.json').write_text(json.dumps(out, indent=2)+'\n')
print(json.dumps(out))
