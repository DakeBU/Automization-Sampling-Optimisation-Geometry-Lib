from pathlib import Path
import gzip, hashlib, json, subprocess, sys
sys.dont_write_bytecode = True
sys.path.insert(0, 'tools')
import astis_publication as pub
W = Path(__file__).resolve().parent.relative_to(Path.cwd())
E = Path('research-wiki/paper-contributions/GaussianComplexity/fixed-spectrum-cosine-gram-semantic-evidence')
A = Path('research-wiki/semantic-roundtrip/audits/huanjian-fixed-spectrum-cosine-gram.json')
C = Path('research-wiki/frontier-cells/ASTIS-SW-GAUSSIAN-COMPLEXITY-fixed-spectrum-cosine-gram.json')
sha = lambda b: hashlib.sha256(b).hexdigest()
dump = lambda x: (json.dumps(x, ensure_ascii=False, indent=2)+'\n').encode()
def put(p, data):
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open('xb') as f:
        f.write(data)
base = '72e5d1405284f729f4eb600c5ae5dd556365b7e2'
assert not (W/'accepted-review-metadata-commit.json').exists()
assert subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip() == base
assert not subprocess.check_output(['git', 'diff', '--cached', '--name-only'])
assert set(subprocess.check_output(['git', 'diff', '--name-only'], text=True).splitlines()) == {str(A), str(C)}
audit = json.loads(A.read_bytes())
name = audit['lean']['declaration']
pub.check_advance([name], reviewed=True)
assert sha(A.read_bytes()) == 'd6e279e86e26f8a763739b72aacadb41692af10593f68ba9b0f10c3efb1304cc'
for p in ['AutoSamplingTheory/ExampleCases/GaussianComplexity/FixedSpectrumCosineGram.lean',
          'Tests/GaussianComplexityFixedSpectrumCosineGram.lean',
          'website/content/declaration_lessons/huanjian-fixed-spectrum-cosine-gram.json',
          'website/content/publications/huanjian-fixed-spectrum-cosine-gram.json',
          'lake-manifest.json', 'lean-toolchain', 'runs/substantive_advances.jsonl']:
    assert Path(p).read_bytes() == subprocess.check_output(['git', 'show', base+':'+p]), p
for n in ['attach_frozen_source_review.py', 'carry_frozen_native_review.py',
          'package_postcandidate_process_only.py', 'observe_original_owner_merged_pr.py',
          'observe_owner_from_actual_authorized_capture.py', 'create_review_metadata_carrier.py']:
    put(E/'root-local-process-scripts'/n, (W/n).read_bytes())
for n in ['original-owner-PR403-actual-gh.raw.json', 'original-owner-PR403-actual-gh.tool-return.json',
          'original-owner-merged-PR-and-unreleased-ledger-observation.json']:
    put(E/n, (W/n).read_bytes())
stems = [
    '20261110T165218474132Z-cosine-gram-immutable-mathematical-candidate-v2-real-identifier-guard',
    '20261110T170110378472Z-cosine-gram-package-postcandidate-process-with-original-failures',
    '20261110T170631322760Z-cosine-gram-carry-entire-frozen-fresh-native-with-reader-HOLD',
    '20261110T171006064541Z-cosine-gram-original-owner-merged-PR-ledger-release-boundary',
    '20261110T173243248241Z-cosine-gram-exact-independent-source-overlay-and-all-original-byte-carry',
    '20261110T173331369783Z-cosine-gram-original-owner-authorized-actual-GH-capture-local-readback',
]
for stem in stems:
    rp = Path('.astis/huanjian-resume-20261103')/(stem+'.receipt.json')
    x = json.loads(rp.read_bytes())
    raw = Path(x['log']).read_bytes()
    assert sha(raw) == x['log_sha256']
    assert x['exit_code'] == (1 if stem.startswith('20261110T171006') else 0)
    put(E/(stem+'.receipt.json'), rp.read_bytes())
    put(E/(stem+'.log.gz'), gzip.compress(raw, mtime=0))
run = Path('.astis/semantic-neutral-20261110/cg_src_7e41d9/phase3_freeze_execution.json')
assert sha(run.read_bytes()) == audit['source_review']['review_run_sha256']
scope = {'mathematical_candidate': base, 'source_actor': audit['source_review']['reviewer'],
         'source_audit_sha256': sha(A.read_bytes()), 'binding_sha256': audit['publication_binding_sha256'],
         'mathematics_lesson_manifest_toolchain_and_ledger_unchanged': True,
         'original_source_run_force_carried_at_exact_canonical_audit_path': str(run),
         'fresh_native_all264_original_files_and_fresh_source_all403_original_files_lossless': True,
         'original_reader_HOLD': 'All six unchanged-production step code controls; no browser/MathJax/desktop/mobile/global acceptance.',
         'normal_SourceV_calls_by_root': 0,
         'scope': 'Metadata carrier only. Exact independent source attachment, complete original evidence archives and owner observation. Actual aggregate metadata gates will run at the resulting immutable commit. Independent source role must inspect that carrier before any normal sourceV. Private renderer proposals are excluded and disabled.'}
put(E/'review-metadata-carrier-scope.json', dump(scope))
paths = sorted(set([A, C, run] + [p for p in E.rglob('*') if p.is_file()]))
raws = {str(p): p.read_bytes() for p in paths}
subprocess.run(['git', 'add', '-f', '--']+list(raws), check=True)
staged = set(subprocess.check_output(['git', 'diff', '--cached', '--name-only'], text=True).splitlines())
assert staged <= set(raws) and {str(A), str(C), str(run)} <= staged
for n, raw in raws.items():
    assert subprocess.check_output(['git', 'show', ':'+n]) == raw, n
subprocess.run(['git', 'diff', '--cached', '--check'], check=True)
subprocess.run(['git', 'commit', '-m', 'Attach independent cosine-Gram source and fresh-native review evidence'], check=True)
commit = subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip()
assert subprocess.check_output(['git', 'rev-parse', commit+'^'], text=True).strip() == base
for n, raw in raws.items():
    assert subprocess.check_output(['git', 'show', commit+':'+n]) == raw, n
record = {**scope, 'commit': commit, 'parent': base,
          'all_selected_files_exact_in_Git_tree': [{'path': n, 'bytes': len(raw), 'sha256': sha(raw)} for n, raw in raws.items()],
          'changed_files': len(staged), 'selected_original_ignored_logs_force_carried': True}
put(W/'accepted-review-metadata-commit.json', dump(record))
print(json.dumps({'metadata_carrier': commit, 'mathematical_candidate': base, 'changed_files': len(staged), 'all_selected_exact': len(raws), 'sourceV': False}))
