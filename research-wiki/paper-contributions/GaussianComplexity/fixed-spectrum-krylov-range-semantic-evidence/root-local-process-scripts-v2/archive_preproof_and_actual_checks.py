from pathlib import Path
import gzip, hashlib, io, json, tarfile

W = Path(__file__).resolve().parent.relative_to(Path.cwd())
E = Path('research-wiki/paper-contributions/GaussianComplexity/fixed-spectrum-krylov-range-semantic-evidence')
R = Path('.astis/huanjian-resume-20261103')
sha = lambda b: hashlib.sha256(b).hexdigest()

def archive(paths, name, scope):
    target = E/(name+'.tar.gz')
    assert not target.exists()
    entries = {}
    with target.open('xb') as raw:
        with gzip.GzipFile(filename='', fileobj=raw, mode='wb', mtime=0) as gz:
            with tarfile.open(fileobj=gz, mode='w') as tf:
                for p in sorted(set(paths)):
                    assert p.is_file() and not p.is_symlink(), p
                    assert p.stat().st_size < 10_000_000, p
                    data = p.read_bytes()
                    assert b'xwechat_files' not in data and b'wxid_' not in data, p
                    info = tarfile.TarInfo(str(p))
                    info.size = len(data)
                    info.mode = p.stat().st_mode & 0o777
                    info.mtime = int(p.stat().st_mtime)
                    tf.addfile(info, io.BytesIO(data))
                    entries[str(p)] = {'sha256': sha(data), 'bytes': len(data), 'original_mode': oct(info.mode)}
    with tarfile.open(target, 'r:gz') as tf:
        assert set(tf.getnames()) == set(entries)
        for member in tf:
            assert member.isfile()
            assert sha(tf.extractfile(member).read()) == entries[member.name]['sha256']
    manifest = {'archive': str(target), 'sha256': sha(target.read_bytes()), 'files': entries, 'scope': scope, 'original_bytes_preserved': True, 'no_symlinks_or_private_foreign_baselines': True}
    mp = E/(name+'.json')
    assert not mp.exists()
    mp.write_text(json.dumps(manifest, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps({'archive': str(target), 'sha256': manifest['sha256'], 'members': len(entries)}))

roots = [Path('.astis/semantic-neutral-20261110')/n for n in ['kr_sg_31f8c2', 'kr_sg_31f8c2_phase2', 'kr_sg_31f8c2_phase3_revision', 'kr_tc_72a0bf']]
paths = []
for root in roots:
    assert root.is_dir() and not root.is_symlink()
    for p in root.rglob('*'):
        assert not p.is_symlink(), p
        if p.is_file():
            assert p.stat().st_mode & 0o777 == 0o444, p
            paths.append(p)
archive(paths, 'independent-preproof-source-topology-archive', 'Complete original frozen source-author phases1/2/versioned3 and distinct topology phases1/2a/2b/2c/3. Includes both repair requests, author revised graph, exact qualified process grant and all original outputs/failures; not sourceV or proof acceptance.')

checks = []
for rp in sorted(R.glob('*krylov-range*.receipt.json')):
    x = json.loads(rp.read_bytes())
    lp = Path(x['log'])
    assert sha(lp.read_bytes()) == x['log_sha256'], lp
    checks += [rp, lp]
files = ['producer-proof-attempt1.lean.txt', 'producer-proof-attempt2.lean.txt', 'producer-proof-attempt3.lean.txt', 'producer-proof-attempt4.lean.txt', 'consumer-proof-attempt1.lean.txt', 'consumer-proof-attempt2.lean.txt', 'author_publication.py', 'complete_publication_after_wording_enum.py', 'complete_publication_after_wording_enum_v2.py', 'root-confirmed-actual-intake-success.json', 'normal-intake-attempted.once.json', 'admit_normal_intake_prepared.py', 'prepared-intake-safe-summary.json', 'prospective-admission-request.json', 'confirm_actual_intake_success.py', 'postseal-abstract-planning-disclosure.json', 'preseal-exposure-qualified-complete.json', 'actual-environment-before-statement-formation.json', 'StatementFormation.lean.attempt1.raw.txt', 'StatementFormation.lean.coordinate-energy-v2.raw.txt', 'StatementFormation.raw.lean.txt', 'producer-signature.draft.txt.attempt1.raw.txt', 'consumer-signature.draft.txt.attempt1.raw.txt', 'consumer-signature.draft.txt.coordinate-energy-v2.raw.txt']
checks += [W/f for f in files]
archive(checks, 'actual-local-checks-lossless-archive', 'All real root Krylov receipts/logs available at this archive point, including failed parsing/import/scalar/coercion/metadata attempts and successful actual sealed P/T builds/kernel checks; exact proof attempts and format repairs. Private foreign-state/tracked/control baselines and source-role working directories are excluded. Later checks are separate, never silently claimed included.')
