from pathlib import Path
import json, sys
sys.dont_write_bytecode = True
sys.path.insert(0, '.astis/huanjian-gc-fixed-spectrum-detector-20261110')
from lossless_frozen_bundle import archive_exact, put_new, sha
W = Path(__file__).resolve().parent.relative_to(Path.cwd())
D = W/'independent-native-reader-0a91de'
E = Path('research-wiki/paper-contributions/GaussianComplexity/fixed-spectrum-cosine-gram-semantic-evidence')
expected = {'findings.json': '7287d0d751f44786643207352cf326a9f5d7300070a13b8b8596c81da2111052',
            'freeze-manifest.json': '613ca1b57a2a9bb65592a0d8998968c07d60bb2e86e722144cab4206c9c0fa6d',
            'freeze-outer-receipt.json': '4f982018a158fc9e1b4e2e270dcfd2fd0f9a4f0f5584158f0f053826448df7e5'}
for n, h in expected.items():
    assert sha((D/n).read_bytes()) == h, n
assert D.stat().st_mode & 0o777 == 0o555
files = {}
for p in sorted(D.rglob('*')):
    assert not p.is_symlink(), p
    if p.is_file():
        assert p.stat().st_mode & 0o777 == 0o444, p
        assert 'PRIVATE' not in str(p)
        files[str(p.relative_to(D))] = p.read_bytes()
    elif p.is_dir():
        assert p.stat().st_mode & 0o777 == 0o555, p
assert len(files) == 264
f = json.loads(files['findings.json'])
assert f['candidate'] == '72e5d1405284f729f4eb600c5ae5dd556365b7e2'
assert f['reader_delivery'] == 'HOLD'
archive = archive_exact(files, E/'fresh-native-0a91de-all-original-files.lossless-file-bytes.tar.gz')
archive.update({'original_actor': '/root/cosine_gram_native_reader_0a91de',
                'scope': 'All264 original frozen regular files:262 payload plus original manifest and outer receipt. Exact immutable candidate fresh canonical-parent/P/T/kernel/owned checks; unchanged-production static reader HOLD on all six step-action neighbors remains. No sourceV, production repair, browser/site/global/purification or Goal acceptance.',
                'original_finding_sha256': expected['findings.json'],
                'original_manifest_sha256': expected['freeze-manifest.json'],
                'original_outer_receipt_sha256': expected['freeze-outer-receipt.json']})
put_new(E/'fresh-native-0a91de-all-original-files.archive-manifest.json', (json.dumps(archive, ensure_ascii=False, indent=2)+'\n').encode())
for src, dst in [('findings.json', 'fresh-native-0a91de-original-findings.json'),
                 ('freeze-manifest.json', 'fresh-native-0a91de-original-freeze-manifest.json'),
                 ('freeze-outer-receipt.json', 'fresh-native-0a91de-original-outer-receipt.json')]:
    put_new(E/dst, files[src])
print(json.dumps({'original_files': len(files), 'archive_sha256': archive['sha256'],
                  'original_findings_sha256': expected['findings.json'],
                  'original_reader_HOLD_preserved': True, 'sourceV': False}))
