from pathlib import Path
import hashlib, json, os, sys
sys.dont_write_bytecode = True
sys.path.insert(0, '.astis/huanjian-gc-fixed-spectrum-detector-20261110')
from lossless_frozen_bundle import archive_exact, put_new, sha
W = Path(__file__).resolve().parent.relative_to(Path.cwd())
E = Path('research-wiki/paper-contributions/GaussianComplexity/fixed-spectrum-cosine-gram-semantic-evidence/disabled-reader-overlay-evidence')
dump = lambda x: (json.dumps(x, ensure_ascii=False, indent=2)+'\n').encode()
assert not E.exists()
E.mkdir()
reviews = [
    ('v3-partial', 'disabled-v3-scope-review-0a91de', 'c6acf949addc8f25957bea7118cd4acc9a0379d0003c0eab59692b1855acb7d6'),
    ('v4-Unicode-defect', 'reader-step-neighbor-v4-independent-0a91de', 'e1cd945656648863a028686541b375f4c7a9a824518fbcc45ebc5215e81ed057'),
    ('v5-CRLF-regression', 'reader-step-neighbor-v5-independent-0a91de', 'cad0f2483e829a3d15383f5236455eb45ea87da2d49cd3fae10093b393f41fd1'),
    ('v6-bounded-static-pass', 'reader-step-neighbor-v6-independent-0a91de', 'fb05f1c7198e161fdcf4eade684410ff4b598a7707d8490bef2521c2c071e7e9'),
]
records = []
for label, dirname, expected in reviews:
    D = W/dirname
    assert sha((D/'findings.json').read_bytes()) == expected
    files, links = {}, []
    for p in sorted(D.rglob('*')):
        if p.is_symlink():
            links.append({'path': str(p.relative_to(D)), 'literal_target': os.readlink(p), 'target_not_dereferenced': True})
        elif p.is_file():
            assert p.stat().st_mode & 0o777 == 0o444
            files[str(p.relative_to(D))] = p.read_bytes()
    ar = archive_exact(files, E/(label+'-all-original-regular-files.lossless-file-bytes.tar.gz'))
    ar.update({'original_findings_sha256': expected, 'symlink_fixtures_metadata_only': links,
               'scope': 'Complete separately frozen prospective UI review. No original mathematical/native/sourceV value is replaced, no live renderer or reader-HOLD release.'})
    put_new(E/(label+'-archive-manifest.json'), dump(ar))
    put_new(E/(label+'-original-findings.json'), files['findings.json'])
    records.append({'label': label, 'regular_files': len(files), 'symlink_fixtures': len(links), 'archive_sha256': ar['sha256'], 'findings_sha256': expected})
authored = {}
for v in [4, 5, 6]:
    D = W/f'reader-step-neighbor-proposal-v{v}'
    for n in ['proposal.json', 'reader-step-neighbor.patch', 'proposed/website/scripts/declaration_lessons.py']:
        p = D/n
        assert p.stat().st_mode & 0o777 == 0o444
        authored[f'v{v}/'+n] = p.read_bytes()
for n in ['prepare_reader_step_proposal_v4.py', 'prepare_reader_step_proposal_v5.attempt1.executed.py',
          'prepare_reader_step_proposal_v5.py', 'prepare_reader_step_proposal_v6.py',
          'check_disabled_v4_static_cg.py', 'check_disabled_v5_static_cg.py', 'check_disabled_v6_static_cg.py',
          'prepare_v5_static_regression.py', 'add_v6_CRLF_static_regression.py']:
    authored['author-scripts/'+n] = (W/n).read_bytes()
for dirname in ['disabled-v4-cosine-gram-static', 'disabled-v5-cosine-gram-static', 'disabled-v6-cosine-gram-static']:
    for p in sorted((W/dirname).rglob('*')):
        if p.is_file() and not p.is_symlink():
            authored['author-static/'+str(p.relative_to(W))] = p.read_bytes()
R = Path('.astis/huanjian-resume-20261103')
for p in sorted(R.glob('*cosine-gram-disabled*v[456]*.receipt.json')):
    x = json.loads(p.read_bytes())
    log = Path(x['log']).read_bytes()
    assert sha(log) == x['log_sha256']
    authored['actual-author-executions/'+p.name] = p.read_bytes()
    authored['actual-author-executions/'+Path(x['log']).name] = log
ar = archive_exact(authored, E/'all-authored-v4-through-v6-inputs-and-actual-checks.lossless-file-bytes.tar.gz')
put_new(E/'all-authored-v4-through-v6.archive-manifest.json', dump(ar))
v6 = W/'reader-step-neighbor-proposal-v6'
for n in ['proposal.json', 'reader-step-neighbor.patch', 'proposed/website/scripts/declaration_lessons.py']:
    put_new(E/'latest-disabled-v6'/n, (v6/n).read_bytes())
index = {'scope': 'DISABLED prospective overlays only. V6 bounded static acceptance is separate from unchanged-production reader HOLD, actual clipboard/JS/MathJax/browser/desktop/mobile/site/global delivery and original sourceV. Apply only after a real serialized lease and then-current main/context revalidation.',
         'original_all_six_reader_HOLD_retained': True, 'original_sourceV_values_unchanged': True,
         'original_v3_partial_v4_Unicode_and_v5_CRLF_HOLDs_retained': True,
         'latest_proposed_renderer_sha256': '28a6ac850ebc8bea4fc9dfb928a7dfd1025941a959b570db6979cf991c2293fe',
         'actual_production_renderer_unchanged_sha256': sha(Path('website/scripts/declaration_lessons.py').read_bytes()),
         'reviews': records, 'authored_archive_sha256': ar['sha256'],
         'author_v5_report_label_limit': 'The actual first v5 root static report inherited the literal v4 scope label. Its proposed renderer path/hash bind v5; original bytes retained. Independent v5 and v6 findings supply their own exact proposal bindings.',
         'normal_sourceV_or_shared_change_by_this_packager': False}
put_new(E/'index.json', dump(index))
print(json.dumps(index))
