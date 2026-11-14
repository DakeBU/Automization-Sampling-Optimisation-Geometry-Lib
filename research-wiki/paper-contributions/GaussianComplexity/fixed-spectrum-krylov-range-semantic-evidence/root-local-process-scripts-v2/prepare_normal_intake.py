"""Prepare a process-only exact intake script; do not execute its API body."""
from pathlib import Path
import hashlib, json, os, subprocess, sys
sys.dont_write_bytecode = True
assert os.environ.get('PYTHONOPTIMIZE') == '0' and sys.flags.optimize == 0
W = Path(__file__).resolve().parent.relative_to(Path.cwd())
sha = lambda b: hashlib.sha256(b).hexdigest()
dump = lambda x: (json.dumps(x, ensure_ascii=False, indent=2)+'\n').encode()
target = W/'admit_normal_intake_prepared.py'
assert not target.exists() and not (W/'intake-baseline.private.json').exists()
s = Path('.astis/huanjian-gc-fixed-spectrum-cosine-gram-20261110/admit_normal_intake_prepared.py').read_text()
s = s.replace('fixed-spectrum-cosine-gram', 'fixed-spectrum-krylov-range').replace('FixedSpectrumCosineGram', 'FixedSpectrumKrylovRange').replace('fixed_spectrum_cosine_gram', 'fixed_spectrum_krylov_range')
s = s.replace('a5e464a34ee276e62267d21f0965c1a0b1ef905bed27e679a85ecee3cd7fd45c', 'f47e23a601d1a8e0ff4760224676313e0f1999877a97156841a65c01847e5d82')
s = s.replace("assert states['ASTIS-SA-20261110-GaussianComplexityZeroQuerySeparation']['state'] == 'VERIFIED'", "assert states['ASTIS-SA-20261110-GaussianComplexityZeroQuerySeparation']['state'] == 'VERIFIED'\nassert states['ASTIS-SA-20261110-GaussianComplexityFixedSpectrumCosineGram']['state'] == 'VERIFIED'")
a, b = s.index('def controls():'), s.index('\nassert len(sys.argv)')
controls = '''def controls():
    import stat
    regular = lambda p: p.exists() and stat.S_ISREG(p.lstat().st_mode)
    names = {str(p) for p in Path('research-wiki/frontier-cells').rglob('*') if regular(p)}
    names |= {str(p) for p in Path('runs').iterdir() if regular(p)}
    names.add('website/content/samplewiki_companion_frontiers.json')
    for p in Path('.astis').iterdir():
        if regular(p) and any(t in p.name.lower() for t in ['queue','control','global','goal','steer','execution']):
            names.add(str(p))
    for n in ['control','queues','runtime','harness','state','locks']:
        d = Path('.astis')/n
        if d.is_dir() and not d.is_symlink():
            names |= {str(p) for p in d.rglob('*') if regular(p)}
    # Reuse only exact known older control PATHS. Never export their private values.
    known = json.loads(Path('.astis/huanjian-gc-fixed-spectrum-cosine-gram-20261110/intake-baseline.private.json').read_bytes())
    names |= set(known['foreign_control_hashes'])
    # Latest original sourceV portable paths only; never glob its PRIVATE sibling.
    root = Path('.astis/semantic-neutral-20261110/cg_src_7e41d9')
    manifest = root/'phase5-normal-sourceV-archive-manifest.json'
    m = json.loads(manifest.read_bytes())
    assert m['full_private_foreign_snapshots_included'] is False
    for x in m['files']:
        n = x['original_repo_path']
        assert 'private-phase5-preservation' not in n
        names.add(n)
    names |= {str(root/n) for n in ['phase5_package_execution.json','phase5_package_execution.stdout','phase5_package_execution.stderr','phase5-normal-sourceV-archive-manifest.json','phase5-normal-sourceV-all-portable-original-files.lossless-file-bytes.tar.gz']}
    own_roots = ['research-wiki/paper-contributions/GaussianComplexity/fixed-spectrum-krylov-range-semantic-evidence/']
    own_exact = {
        'research-wiki/paper-contributions/GaussianComplexity/fixed-spectrum-krylov-range-statement-seal.json',
        'AutoSamplingTheory/ExampleCases/GaussianComplexity/FixedSpectrumKrylovRange.lean',
        'Tests/GaussianComplexityFixedSpectrumKrylovRange.lean',
        'website/content/declaration_lessons/huanjian-fixed-spectrum-krylov-range.json',
        'website/content/publications/huanjian-fixed-spectrum-krylov-range.json',
        'research-wiki/semantic-roundtrip/audits/huanjian-fixed-spectrum-krylov-range.json'}
    for raw in subprocess.check_output(['git','ls-files','--others','--exclude-standard','-z']).split(b'\\0'):
        if not raw:
            continue
        n = raw.decode()
        if n not in own_exact and not any(n.startswith(p) for p in own_roots) and regular(Path(n)):
            names.add(n)
    # Nested repositories/directories/symlinks are not followed or hashed.
    return sorted(n for n in names if regular(Path(n)))
'''
s = s[:a]+controls+s[b:]
a, b = s.index('boundary = ('), s.index('\nproposal = ')
s = s[:a]+'''boundary = ('Prove the actual pointwise cosine-feature image=Krylov equality at source kappa>=2 '
    'and natural d,q with2q+1<d includingq0, materially consumed by actual Euclidean norm and '
    'signed weighted-inner coefficient identities for every actual Krylov vector. Unscaled source g; '
    'B alone has d^-1/2. No supplied polynomial/invertibility/normalization/rank/span/Gram/moment '
    'certificate. No concentration/absoluteC/C6/full Lemma4.4, Haar/joint/adaptive/measurable-choice/'
    'oracle/exact-matvec/precision/TV/dimension-condition-number/deterministic worst-query-cap/'
    'explicit expected-cost adapter, either full main bound, sourceV/global/site/browser/publication/'
    'purification/ExpositionSeal or Goal completion. All twelve prior original sourceV values and '
    'all other states/frontiers/queues/other ASTIS chat and current reader HOLDs are preserved; '
    'the original foreign global lease is not transferred.')'''+s[b:]
s = s.replace("goal='Prove actual cosine-frame Gram orthogonality, weighted cancellation and row-norm identities, materially consumed by integrable actual Gaussian Gram means.'", "goal='Prove the actual hard-family cosine-feature Krylov range, materially consumed by actual Euclidean energy coordinates.'")
a, b = s.index('    dag_inputs='), s.index('    proposed_files=')
s = s[:a]+'''    dag_inputs=('source:arXiv2610.20492v1 S4.SS1.p1; S4.SS2.SSS0.Px1.p2; A3.Thmtheorem5/A3.SS2.2 range and A3.SS2.p19 exact pointwise energy equalities',
        'Literal canonical finite-matrix/span/Euclidean definitions. General proof-API retrieval only after exact independent qualified admission; actual compiled parents remain unknown.'),
'''+s[b:]
s = s.replace("C.write_bytes(dump(cell))", "cell['truth_boundary'] = boundary\nC.write_bytes(dump(cell))")
assert 'integrable actual Gaussian Gram means' not in s
assert 'orthogonality, weighted cancellation' not in s
assert 'GaussianComplexityFixedSpectrumKrylovRange' in s
compile(s, str(target), 'exec')
target.write_text(s)
target.chmod(0o444)
namespace = {'__file__': str(target), '__name__': 'prepared_controls_only'}
exec(compile(s.split('assert len(sys.argv)')[0], str(target), 'exec'), namespace)
paths = namespace['controls']()
pre = W/'preproof-baseline.private.json'
pb = pre.read_bytes()
x = json.loads(pb)
assert subprocess.check_output(['git','rev-parse','HEAD'], text=True).strip() == x['head']
C, L = namespace['C'], namespace['L']
assert sha(L.read_bytes()) == x['ledger_sha256']
for p, h in x['all_tracked_regular_file_hashes'].items():
    assert sha(Path(p).read_bytes()) == h, p
for p, h in x['all_existing_frontier_hashes'].items():
    assert sha(Path(p).read_bytes()) == h, p
baseline = {'state': 'PRIVATE_FOREIGN_CONTROL_SNAPSHOT_NEVER_EXPORT',
            'preproof_snapshot': {'path': str(pre), 'sha256': sha(pb)},
            'own_frontier': {'path': str(C), 'sha256': sha(C.read_bytes())},
            'control_paths': paths,
            'foreign_control_hashes': {n: sha(Path(n).read_bytes()) for n in paths if n not in {str(C), str(L)}},
            'normal_API_calls_so_far': 0,
            'restricted_nested_repositories': 'Metadata only, no traversal/read/hash of contents/index/projections/derivatives. Ordinary foreign untracked regular files and exact older control/portable-sourceV paths are guarded; original PRIVATE sourceV snapshots are excluded.'}
p = W/'intake-baseline.private.json'
p.write_bytes(dump(baseline))
p.chmod(0o444)
out = {'prepared_intake_script': str(target), 'prepared_intake_script_sha256': sha(target.read_bytes()),
       'private_baseline_sha256': sha(p.read_bytes()), 'private_preproof_baseline_sha256': sha(pb),
       'control_path_count': len(paths), 'foreign_control_count': len(baseline['foreign_control_hashes']),
       'normal_API_calls': 0, 'target_proof_API_authority': False,
       'rule': 'Do not execute before distinct topology mathematical freezes, source-graph challenge and exact qualified prospective process grant. Assertions require PYTHONOPTIMIZE=0; permanent O_EXCL once marker and full postguards precede any target proof/API retrieval.'}
(W/'prepared-intake-safe-summary.json').write_bytes(dump(out))
print(json.dumps(out))
