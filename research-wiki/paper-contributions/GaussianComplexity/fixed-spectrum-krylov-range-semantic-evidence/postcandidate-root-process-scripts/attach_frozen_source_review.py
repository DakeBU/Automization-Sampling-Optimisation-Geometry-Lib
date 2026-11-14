from pathlib import Path
import copy, gzip, hashlib, io, json, re, tarfile

W = Path(__file__).resolve().parent.relative_to(Path.cwd())
E = Path('research-wiki/paper-contributions/GaussianComplexity/fixed-spectrum-krylov-range-semantic-evidence')
S = Path('.astis/semantic-neutral-20261111/kr_src_c47e12')
sha = lambda b: hashlib.sha256(b).hexdigest()
checks = {'phase4/hash-manifest.json': '5146a75767e8d9f5a45fd4b3d0c5c636c5bfb08fabf0cac13735719595317638', 'phase4/original-execution-receipt.json': '6a847f04406a75d0ff3d06037cb2f8e7de9efb6fe0ceff79da0d09d4d9ed2b67', 'phase4/source-review-overlay.json': '3663e0bf0dff78c58d9e72d4a8c099a30e41b8528c7bad1d91b233c2a2a47e48', 'phase4/canonical-semantic-review-result.v2.json': 'd5814088694230353bf8b3943f67ee4f56079cee0289c352526e4ae820f83cb7'}
for n, h in checks.items():
    assert sha((S/n).read_bytes()) == h, n
for phase in ['phase1', 'phase2', 'phase3', 'phase4']:
    m = json.loads((S/phase/'hash-manifest.json').read_bytes())
    for row in m['files']:
        p = S/phase/row['path']
        assert sha(p.read_bytes()) == row['sha256'] and p.stat().st_size == row['bytes'], p
        assert p.stat().st_mode & 0o777 == 0o444, p
    for p in [S/phase]+[p for p in (S/phase).rglob('*') if p.is_dir()]:
        assert p.stat().st_mode & 0o777 == 0o555, p
assert not any('private-phase' in str(p.relative_to(S)) for p in S.rglob('*'))
files = [p for p in S.rglob('*') if p.is_file()]
assert not any(p.is_symlink() for p in S.rglob('*'))
target = E/'fresh-source-c47e12-phases1-4-all-original-files.lossless-file-bytes.tar.gz'
assert not target.exists()
entries = {}
with target.open('xb') as out:
    with gzip.GzipFile(filename='', fileobj=out, mode='wb', mtime=0) as gz:
        with tarfile.open(fileobj=gz, mode='w') as tf:
            for p in sorted(files):
                assert p.stat().st_size < 10_000_000, p
                data = p.read_bytes()
                assert (b'/xwechat' + b'_files/') not in data and not re.search(rb'wx' + rb'id_[a-z0-9]{5,}', data), p
                info = tarfile.TarInfo(str(p.relative_to(S)))
                info.size = len(data)
                info.mode = p.stat().st_mode & 0o777
                tf.addfile(info, io.BytesIO(data))
                entries[info.name] = {'sha256': sha(data), 'bytes': len(data), 'original_mode': oct(info.mode)}
with tarfile.open(target, 'r:gz') as tf:
    assert set(tf.getnames()) == set(entries)
    for member in tf:
        assert sha(tf.extractfile(member).read()) == entries[member.name]['sha256']
archive = {'archive': str(target), 'sha256': sha(target.read_bytes()), 'files': entries, 'actual_actor': '/root/krylov_fresh_source_c47e12', 'all_original_bytes_preserved': True, 'scope': 'Complete original source phases1-4 plus their original outer execution files/scripts, BEFORE any phase5/private operational preservation directory is created. Includes every failure, exposure qualification, mathematical freeze, schema/binding adapter, original unapplied overlay and exact map review. Not a normal VERIFIED transition or reader delivery.'}
(E/'fresh-source-c47e12-phases1-4-all-original-files.archive-manifest.json').write_text(json.dumps(archive, ensure_ascii=False, indent=2)+'\n')
overlay = json.loads((S/'phase4/source-review-overlay.json').read_bytes())
result = json.loads((S/'phase4/canonical-semantic-review-result.v2.json').read_bytes())
assert overlay['checked_commit'] == '972d8994a816bc63d2dd6fb2db1c2c638fa9a48f'
assert overlay['canonical_semantic_result_raw_sha256'] == sha((S/'phase4/canonical-semantic-review-result.v2.json').read_bytes())
assert overlay['source_review']['reviewer'] == result['reviewer'] == '/root/krylov_fresh_source_c47e12'
assert overlay['source_review']['state'] == 'accepted'
assert result['verdict'] == 'equivalent-after-elaboration'
assert overlay['applied'] is False and overlay['normal_VERIFIED_or_source_cell_transition_authorized'] is False
for n in ['phase4/source-review-overlay.json', 'phase4/canonical-semantic-review-result.v2.json', 'phase3/mathematical-source-proof-reader-judgment.json', 'phase3/original-execution-receipt.json', 'phase4/mapping-and-adapter-process-judgment.json', 'phase4/exact-binding-reproduction.json']:
    q = E/'independent-source-c47e12'/n
    q.parent.mkdir(parents=True, exist_ok=True)
    assert not q.exists()
    q.write_bytes((S/n).read_bytes())
    q.chmod(0o444)
ap = Path('research-wiki/semantic-roundtrip/audits/huanjian-fixed-spectrum-krylov-range.json')
old = ap.read_bytes()
a = json.loads(old)
assert a['state'] == 'blind-reconstructed'
assert a['publication_binding_sha256'] == overlay['publication_binding_sha256']
protected = {k: copy.deepcopy(a[k]) for k in ['id', 'source', 'lean', 'reconstruction', 'publication_binding_sha256', 'publication_context']}
(E/'audit-before-independent-source-overlay.raw.json').write_bytes(old)
a['state'] = 'source-reviewed'
for key in ['semantic_slots', 'deltas', 'verdict', 'repairs']:
    a[key] = copy.deepcopy(result[key])
a['source_review'] = copy.deepcopy(overlay['source_review'])
assert {k: a[k] for k in protected} == protected
ap.write_text(json.dumps(a, ensure_ascii=False, indent=2)+'\n')
C = Path('research-wiki/frontier-cells/ASTIS-SW-GAUSSIAN-COMPLEXITY-fixed-spectrum-krylov-range.json')
raw = C.read_bytes()
c = json.loads(raw)
assert c['status'] == 'proved_locally'
(E/'frontier-before-source-overlay.raw.json.gz').write_bytes(gzip.compress(raw, mtime=0))
c['evidence']['source_review'] = 'Accepted bounded source/whole-module/exposition review by original independent actor /root/krylov_fresh_source_c47e12 at exact mathematical candidate972d. Original mathematical freezes, process redaction/binding qualification and unchanged six-field semantic lineage retained; no normal VERIFIED yet.'
c['evidence']['independent_source_review_overlay'] = str(E/'independent-source-c47e12/phase4/source-review-overlay.json')
c['evidence']['independent_native_static_findings'] = str(E/'independent-native-5f09a3-independent-verdict.json')
c['evidence']['reader_HOLD'] = ['Individual six corresponding code folds lack copy/download/context controls.', 'Private Test numbered provenance page lacks copy/download controls; exact standalone full module/download checked only in isolated static scope.', 'No live browser/MathJax/clipboard/mobile/final shell/global site acceptance.']
C.write_text(json.dumps(c, ensure_ascii=False, indent=2)+'\n')
record = {'actual_actor': overlay['source_review']['reviewer'], 'actual_original_review_run_sha256': overlay['source_review']['review_run_sha256'], 'source_overlay_raw_sha256': checks['phase4/source-review-overlay.json'], 'canonical_result_raw_sha256': checks['phase4/canonical-semantic-review-result.v2.json'], 'all_original_source_files_archived': len(entries), 'archive_sha256': archive['sha256'], 'protected_original_source_lean_reconstruction_and_binding_unchanged': True, 'canonical_source_review_value_copied_exact': a['source_review'] == overlay['source_review'], 'audit_state': a['state'], 'sourceV_API_calls_by_root': 0, 'source_advance_state_remains_PROVED_LOCAL': True, 'actual_reader_HOLD_retained': True, 'global_publication_purification_Goal_complete': False}
(E/'independent-source-c47e12-exact-attachment.json').write_text(json.dumps(record, ensure_ascii=False, indent=2)+'\n')
print(json.dumps(record))
