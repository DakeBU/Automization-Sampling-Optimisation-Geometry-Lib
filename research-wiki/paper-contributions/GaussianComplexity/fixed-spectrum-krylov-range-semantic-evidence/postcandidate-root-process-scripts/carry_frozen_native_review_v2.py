from pathlib import Path
import gzip, hashlib, io, json, re, tarfile

W = Path(__file__).resolve().parent.relative_to(Path.cwd())
E = Path('research-wiki/paper-contributions/GaussianComplexity/fixed-spectrum-krylov-range-semantic-evidence')
N = W/'independent-native-reader-5f09a3'
D = N/'phase1-972d8994'
sha = lambda b: hashlib.sha256(b).hexdigest()
assert sha((D/'phase1-final-manifest.json').read_bytes()) == '5543a7e6f317557106a77717d7e6867a7d2060f93d2dadeb012e92c0028dd757'
assert sha((D/'independent-verdict.json').read_bytes()) == '613d4fa7616619fb2b2ec8c4d2bbcc59275b61e1704a083cc3282093138b5fd9'
m = json.loads((D/'phase1-final-manifest.json').read_bytes())
assert m['candidate'] == '972d8994a816bc63d2dd6fb2db1c2c638fa9a48f'
for name, row in m['files'].items():
    p = D/name
    assert sha(p.read_bytes()) == row['sha256'] and p.stat().st_size == row['bytes'], p
    assert p.stat().st_mode & 0o777 == 0o444, p
actual = {str(p.relative_to(D)) for p in D.rglob('*') if p.is_file()}
assert actual == set(m['files']) | {'phase1-final-manifest.json'}
assert len(m['files']) == 352 and len(actual) == 353
v = json.loads((D/'independent-verdict.json').read_bytes())
assert v['all_owned_closed_Prop'] and v['all_owned_values_closed'] and v['all_owned_std3_only']
assert v['owned_count'] == 4 and v['generated_math_credit'] == 0 and v['unreachable_owned'] == []
assert v['exact_source_signatures_match_seal'] and v['independently_elaborated_literal_types_closed_Prop_and_defeq']
assert v['strict_raw_Expr_structural_equality'] is False
assert v['locator_count'] == 186 and v['locator_failures'] == 0
assert v['canonical_named_records'] == 50 and v['canonical_actual_direct_use_failures'] == 0
assert v['six_step_folds_exact_and_initially_closed'] and v['entire_private_T_file_exact_in_step6']
assert len(v['static_control_gaps']) == 2
files = [p for p in N.rglob('*') if p.is_file()]
assert not any(p.is_symlink() for p in N.rglob('*'))
target = E/'fresh-native-5f09a3-all-original-files.lossless-file-bytes.tar.gz'
assert not target.exists()
entries = {}
with target.open('xb') as out:
    with gzip.GzipFile(filename='', fileobj=out, mode='wb', mtime=0) as gz:
        with tarfile.open(fileobj=gz, mode='w') as tf:
            for p in sorted(files):
                assert p.stat().st_size < 10_000_000, p
                data = p.read_bytes()
                assert (b'/xwechat' + b'_files/') not in data and not re.search(rb'wx' + rb'id_[a-z0-9]{5,}', data), p
                info = tarfile.TarInfo(str(p.relative_to(N)))
                info.size = len(data)
                info.mode = p.stat().st_mode & 0o777
                tf.addfile(info, io.BytesIO(data))
                entries[info.name] = {'sha256': sha(data), 'bytes': len(data), 'original_mode': oct(info.mode)}
with tarfile.open(target, 'r:gz') as tf:
    assert set(tf.getnames()) == set(entries)
    for member in tf:
        assert sha(tf.extractfile(member).read()) == entries[member.name]['sha256']
record = {'archive': str(target), 'sha256': sha(target.read_bytes()), 'files': entries, 'original_actor': '/root/krylov_native_reader_5f09a3', 'all_original_files_byte_exact': True, 'phase1_manifest_payload_files': 352, 'phase1_frozen_files_including_manifest': 353, 'scope': 'All original native phase0 and exact-candidate phase1 files, including bounded inventory/compiled outputs/failures and static-reader gaps. No source-fidelity or live website acceptance. No original bytes normalized.'}
(E/'fresh-native-5f09a3-all-original-files.archive-manifest.json').write_text(json.dumps(record, ensure_ascii=False, indent=2)+'\n')
for name in ['independent-verdict.json', 'phase1-final-manifest.json', 'native-independent-boundary.json']:
    q = E/('independent-native-5f09a3-'+name)
    assert not q.exists()
    q.write_bytes((D/name).read_bytes())
attachment = {'actor': '/root/krylov_native_reader_5f09a3', 'candidate': m['candidate'], 'all_original_files': len(entries), 'phase1_manifest_payload_files': 352, 'phase1_all_files_including_manifest': 353, 'native_actual_result': v['native_result'], 'exact_seal_raw_signatures_and_kernel_defeq': True, 'raw_Expr_structural_equality': False, 'raw_Expr_diagnostic': v['raw_Expr_diagnostic'], 'actual_public_ASTIS_parents': v['actual_public_ASTIS_parents'], 'all186_locator_checks_and50_actual_direct_uses': True, 'reader_HOLD': v['static_control_gaps'], 'no_browser_runtime_or_publication_credit': True, 'root_sourceV_API_calls': 0}
(E/'independent-native-5f09a3-mechanical-attachment.json').write_text(json.dumps(attachment, ensure_ascii=False, indent=2)+'\n')
print(json.dumps({'original_files': len(entries), 'archive_sha256': record['sha256'], 'phase1_files_including_manifest': 353, 'candidate': m['candidate'], 'reader_HOLD': True, 'sourceV': False}))
