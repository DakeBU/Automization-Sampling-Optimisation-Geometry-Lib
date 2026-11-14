from pathlib import Path
import json, sys
sys.dont_write_bytecode = True
sys.path.insert(0, '.astis/huanjian-gc-fixed-spectrum-detector-20261110')
from lossless_frozen_bundle import archive_exact, put_new, sha
S = Path('.astis/semantic-neutral-20261110/cg_src_7e41d9')
E = Path('research-wiki/paper-contributions/GaussianComplexity/fixed-spectrum-cosine-gram-semantic-evidence')
A = Path('research-wiki/semantic-roundtrip/audits/huanjian-fixed-spectrum-cosine-gram.json')
C = Path('research-wiki/frontier-cells/ASTIS-SW-GAUSSIAN-COMPLEXITY-fixed-spectrum-cosine-gram.json')
dump = lambda x: (json.dumps(x, ensure_ascii=False, indent=2)+'\n').encode()
contract = json.loads((S/'phase4/attachment_contract.json').read_bytes())
old = A.read_bytes()
assert sha(old) == contract['baseline_audit_raw_sha256']
overlay_raw = (S/'phase4/canonical-audit-attachment-overlay.json').read_bytes()
proposed_raw = (S/'phase4/proposed-canonical-audit.json').read_bytes()
assert sha(overlay_raw) == contract['overlay_sha256'] == 'a5d9f16f2b884b33e02c04fcd675e34832c8b27430161a1c28391ef343504848'
assert sha(proposed_raw) == contract['proposed_audit_sha256'] == 'd6e279e86e26f8a763739b72aacadb41692af10593f68ba9b0f10c3efb1304cc'
before = json.loads(old)
overlay = json.loads(overlay_raw)
proposed = json.loads(proposed_raw)
assert set(overlay) == set(contract['allowed_top_level_replacement_fields'])
assert proposed == {**before, **overlay}
for key in contract['protected_unchanged_top_level_fields']:
    assert proposed[key] == before[key], key
assert proposed['source_review']['reviewer'] == '/root/cosine_gram_fresh_source_7e41d9'
assert proposed['source_review']['review_run_sha256'] == sha((S/'phase3_freeze_execution.json').read_bytes())
assert proposed['source_review']['reviewer_packet_sha256'] == '68eb57daeb019b886f64e96ea800777ac04f83af39d582ae8ff9a01c3d497921'
files = {}
for p in sorted(S.rglob('*')):
    assert not p.is_symlink(), p
    if p.is_file():
        assert p.stat().st_mode & 0o777 == 0o444, p
        assert 'PRIVATE' not in str(p)
        files[str(p.relative_to(S))] = p.read_bytes()
assert len(files) == 403
archive = archive_exact(files, E/'fresh-source-7e41d9-phases1-through4-all-original-files.lossless-file-bytes.tar.gz')
archive.update({'original_actor': '/root/cosine_gram_fresh_source_7e41d9',
                'scope': 'All403 current original frozen regular files, all four phases and outer actual command/execution artifacts, before any normal-sourceV/private foreign baseline. Original raw-first/selective/full-code/native-closure phase boundaries and reader HOLD remain unchanged.',
                'normal_sourceV_API_calls_in_these_phases': 0})
put_new(E/'fresh-source-7e41d9-all-original-files.archive-manifest.json', dump(archive))
copies = {
    'phase3/mathematical_judgment.json': 'fresh-source-7e41d9-original-mathematical-judgment.json',
    'phase3/mathematical_source_module_exposition_judgment.md': 'fresh-source-7e41d9-original-mathematical-judgment.md',
    'phase3_freeze_execution.json': 'fresh-source-7e41d9-original-actual-source-run.json',
    'phase4/canonical-audit-attachment-overlay.json': 'fresh-source-7e41d9-original-canonical-audit-overlay.json',
    'phase4/attachment_contract.json': 'fresh-source-7e41d9-original-attachment-contract.json',
    'phase4_freeze_execution.json': 'fresh-source-7e41d9-original-closure-run.json',
}
for original, dest in copies.items():
    put_new(E/dest, files[original])
put_new(E/'audit-before-independent-source-attachment.raw.json', old)
A.write_bytes(proposed_raw)
cell_raw = C.read_bytes()
put_new(E/'frontier-before-independent-source-attachment.raw.json', cell_raw)
c = json.loads(cell_raw)
assert c['status'] == 'proved_locally'
c['evidence']['independent_verification'] = str(E/'fresh-native-0a91de-original-findings.json')
c['evidence']['source_review'] = 'Independent fresh raw-first/selective/full-module source review accepted equivalent-after-elaboration at candidate72e5d140; exact independently authored canonical audit attached. Normal sourceV still pending. All-six-fold production reader HOLD and global/publication/purification boundaries remain.'
c['evidence']['independent_source_review'] = str(E/'fresh-source-7e41d9-original-mathematical-judgment.json')
c['evidence']['reader_delivery'] = 'HOLD: all six unchanged-production corresponding code folds lack adjacent copy/source/download actions. Disabled prospective repairs do not release this HOLD; no actual browser/MathJax/desktop/mobile/global acceptance.'
C.write_bytes(dump(c))
record = {'source_actor': proposed['source_review']['reviewer'], 'audit_before_sha256': sha(old),
          'audit_after_sha256': sha(proposed_raw), 'exact_independent_overlay_sha256': sha(overlay_raw),
          'all_six_fields_attached_without_root_authored_verdict': True,
          'all_protected_fields_unchanged': contract['protected_unchanged_top_level_fields'],
          'original_source_files': len(files), 'source_archive_sha256': archive['sha256'],
          'original_native_archive_sha256': 'eef1e3597a76509f5ae76b47ac52ba5e0d9597b20680bc036fc357e7f363cca4',
          'original_run_artifact_exact_path_to_force_carry': str(S/'phase3_freeze_execution.json'),
          'normal_SourceV_calls_by_root': 0, 'reader_HOLD_global_purification_Goal_pending': True}
put_new(E/'mechanical-independent-source-attachment.json', dump(record))
print(json.dumps(record))
