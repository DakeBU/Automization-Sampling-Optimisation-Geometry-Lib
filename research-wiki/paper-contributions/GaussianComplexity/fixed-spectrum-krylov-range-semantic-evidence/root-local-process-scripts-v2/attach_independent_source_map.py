from pathlib import Path
import gzip, hashlib, io, json, tarfile

W = Path(__file__).resolve().parent.relative_to(Path.cwd())
E = Path('research-wiki/paper-contributions/GaussianComplexity/fixed-spectrum-krylov-range-semantic-evidence')
D = W/'source-map-author-31f8c2'
sha = lambda b: hashlib.sha256(b).hexdigest()
checks = {'source-to-lean-map.v1.json': '1d1292073bb4469d69a1953b7cc12d47fd780ea1377ee59cb63b8e6ecc186c3a', 'candidate-exposition-source-map.json': '6903412ea8b2ec8223e3fc11b6792d6dfaed8bf95620dace8a03fb23a0d179bc', 'canonical-declaration-inventory.json': '34f7f1db6f7930d2e4837742a395462a36e0379a9a6b5b1196843b5ab1e8dc9e', 'payload-manifest.json': '58c057254c61fe67c5db8d2e1e60530c517fe3e38417a03f6f5f91e45dc53d9b', 'freeze-execution.receipt.json': '78b9ea1a78ef4a343b53a734cee76278f0015e62beee5e5fbf17bd110f7f53ed'}
for name, h in checks.items():
    assert sha((D/name).read_bytes()) == h, name
manifest = json.loads((D/'payload-manifest.json').read_bytes())
envelope = json.loads((D/'freeze-envelope-hashes.json').read_bytes())
for row in manifest['files'] + envelope['files']:
    p = D/row['path']
    assert sha(p.read_bytes()) == row['sha256'] and p.stat().st_size == row['bytes'], p
files = [p for p in D.rglob('*') if p.is_file()]
assert len(files) == 198
for p in D.rglob('*'):
    assert not p.is_symlink(), p
    assert p.stat().st_mode & 0o777 == (0o555 if p.is_dir() else 0o444), p
assert D.stat().st_mode & 0o777 == 0o555
expected = {r['path'] for r in manifest['files']} | set(manifest['envelope_files'])
assert {str(p.relative_to(D)) for p in files} == expected
raw_source = Path('.astis/huanjian-resume-20261103/2610.20492v1.html').read_bytes()
assert sha(raw_source) == '6bc5ddc1e19cea9ba1dfe862fa79bc69fe861dff045d6ad1c7baa4a113c37915'
source_text = raw_source.decode()
cache = {}
spans = set()
raw_pins = set()
def walk(x):
    if isinstance(x, dict):
        if 'character_span_0based_halfopen' in x:
            p = Path(x.get('file', x.get('original_file', '')))
            assert p.is_absolute() and p.is_relative_to(Path.cwd()), p
            assert '.atlas' not in str(p).lower(), p
            if p not in cache:
                b = p.read_bytes()
                cache[p] = (b, b.decode())
            b, text = cache[p]
            assert sha(b) == x['file_raw_sha256'], p
            a, z = x['character_span_0based_halfopen']
            ba, bz = x['utf8_byte_span_0based_halfopen']
            literal = text[a:z]
            assert b[ba:bz] == literal.encode(), p
            assert sha(literal.encode()) == x['raw_span_sha256'], p
            assert [text[:a].count('\n')+1, text[:z-1].count('\n')+1] == x['lf_lines_1based_inclusive'], p
            assert literal.endswith('\n') == x['terminal_LF_included'], p
            spans.add((str(p.relative_to(Path.cwd())), a, z))
        if 'raw_pin' in x:
            pin = x['raw_pin']
            a, z = pin['char_span_0based_halfopen']
            ba, bz = pin['utf8_span_0based_halfopen']
            literal = source_text[a:z]
            assert raw_source[ba:bz] == literal.encode()
            assert sha(literal.encode()) == pin['sha256_raw_utf8']
            assert [source_text[:a].count('\n')+1, source_text[:z-1].count('\n')+1] == pin['lf_lines_1based_inclusive']
            raw_pins.add((pin['id'], a, z))
        for v in x.values():
            walk(v)
    elif isinstance(x, list):
        for v in x:
            walk(v)
for name in ['source-to-lean-map.v1.json', 'canonical-declaration-inventory.json', 'lean-proof-region-spans.json', 'owned-declaration-spans.json', 'candidate-exposition-source-map.json']:
    walk(json.loads((D/name).read_bytes()))
canonical = json.loads((D/'canonical-declaration-inventory.json').read_bytes())['records']
assert len(canonical) == len({r['name'] for r in canonical}) == 50
for row in canonical:
    b, text = cache[Path(row['span']['file'])]
    a, z = row['span']['character_span_0based_halfopen']
    assert (D/row['snapshot_path']).read_bytes() == text[a:z].encode(), row['name']
proposal = json.loads((D/'source-to-lean-map.v1.json').read_bytes())
assert len(proposal['mapping_records']) == 11
assert proposal['production_sha256'] == sha(Path('AutoSamplingTheory/ExampleCases/GaussianComplexity/FixedSpectrumKrylovRange.lean').read_bytes())
assert proposal['private_consumer_sha256'] == sha(Path('Tests/GaussianComplexityFixedSpectrumKrylovRange.lean').read_bytes())
target = E/'postproof-map-author-all-original-files.lossless-file-bytes.tar.gz'
assert not target.exists()
inventory = {}
with target.open('xb') as out:
    with gzip.GzipFile(filename='', fileobj=out, mode='wb', mtime=0) as gz:
        with tarfile.open(fileobj=gz, mode='w') as tf:
            for p in sorted(files):
                data = p.read_bytes()
                assert b'xwechat_files' not in data and b'wxid_' not in data, p
                info = tarfile.TarInfo(str(p.relative_to(D)))
                info.size = len(data)
                info.mode = 0o444
                tf.addfile(info, io.BytesIO(data))
                inventory[info.name] = {'sha256': sha(data), 'bytes': len(data), 'original_mode': '0444'}
with tarfile.open(target, 'r:gz') as tf:
    assert set(tf.getnames()) == set(inventory)
    for member in tf:
        assert sha(tf.extractfile(member).read()) == inventory[member.name]['sha256']
archive_record = {'archive': str(target), 'sha256': sha(target.read_bytes()), 'files': inventory, 'all198_original_files_byte_exact': True, 'scope': 'Frozen map author proposal only; not source or native acceptance. Absolute original locator paths are historical evidence; public machine-independent locator adaptation remains a separate reviewed integration obligation.'}
(E/'postproof-map-author-all-original-files.archive-manifest.json').write_text(json.dumps(archive_record, ensure_ascii=False, indent=2)+'\n')
for source, dest in [('source-to-lean-map.v1.json', 'source-to-lean-map-v1.json'), ('canonical-declaration-inventory.json', 'canonical-declaration-inventory.json'), ('candidate-exposition-source-map.json', 'candidate-exposition-source-map.json')]:
    p = E/dest
    assert not p.exists()
    p.write_bytes((D/source).read_bytes())
record = {'original_actor': '/root/krylov_range_source_graph_31f8c2', 'all198_original_files_byte_exact': True, 'unique_Lean_and_canonical_spans_checked': len(spans), 'unique_source_raw_pin_spans_checked': len(raw_pins), 'canonical_names_unique': 50, 'source_mapping_records': 11, 'offsets': 'Decoded Unicode character offsets and raw UTF8 byte offsets checked independently; LF lines1-based inclusive, terminalLF belongs to previous line.', 'no_source_or_native_verdict': True, 'original_locator_path_scope': archive_record['scope']}
(E/'source-to-lean-map-mechanical-byte-attachment.json').write_text(json.dumps(record, ensure_ascii=False, indent=2)+'\n')
print(json.dumps(record))
