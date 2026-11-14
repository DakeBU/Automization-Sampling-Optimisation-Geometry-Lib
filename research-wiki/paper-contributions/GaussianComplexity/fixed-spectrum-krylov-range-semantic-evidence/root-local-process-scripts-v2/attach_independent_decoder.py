from pathlib import Path
import hashlib, json

W = Path(__file__).resolve().parent.relative_to(Path.cwd())
E = Path('research-wiki/paper-contributions/GaussianComplexity/fixed-spectrum-krylov-range-semantic-evidence')
N = Path('.astis/semantic-neutral-20261111/p_kr_91de5a')
sha = lambda b: hashlib.sha256(b).hexdigest()
dump = lambda x: (json.dumps(x, ensure_ascii=False, indent=2)+'\n').encode()
assert sha((N/'input.json').read_bytes()) == '456c06a158477e5b3fed15fb6ed7d69a5c7a15e5776f26387f48478016f6224b'
assert sha((N/'run/final_manifest.json').read_bytes()) == '6ace8bc05e40c3073673b7061ebc0b207229dd0854d5864c5371c06b9c57d06a'
m = json.loads((N/'run/final_manifest.json').read_bytes())
for row in m['files']:
    p = N/'run'/row['path']
    assert p.stat().st_size == row['bytes'] and sha(p.read_bytes()) == row['sha256'], p
    assert p.stat().st_mode & 0o777 == 0o444 and p.stat().st_flags & 2, p
assert {str(p.relative_to(N/'run')) for p in (N/'run').rglob('*') if p.is_file()} == {r['path'] for r in m['files']} | {'final_manifest.json', 'final_receipt.json'}
recraw = (N/'run/original/reconstruction.json').read_bytes()
rec = json.loads(recraw)
canonical = json.dumps({k: v for k, v in rec.items() if k != 'decoder_run_sha256'}, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()
assert sha(canonical) == rec['decoder_run_sha256'] == 'd598f9c4d3d1b138036358a3b95df161242ee2efd5dc6e0da974d0864b66d02f'
md = (N/'run/original/reconstructed_theorem.md').read_bytes()
assert sha(md) == rec['reconstructed_text_sha256'] == 'f56c7a92022f341b5b628d35cca0a33667b40f6b0fd96f739616db0d64726c03'
assert md.decode() == rec['reconstructed_theorem_text']
assert rec['source_text_visible'] is False and rec['decoder'] == '/root/neutral_decoder_91de5a'
assert rec['canonical_packet_sha256'] == '32bf67858af5f659f26c451a9d323f971259d04f114d22cb88315a6327f62579'
assert sha((N/'presentation-overlay/manifest.json').read_bytes()) == 'a92f67cc8ec2d6a3876603dbf8e77a632b8806adec5ef8074ac7bbc7c74d02f7'
mapping = json.loads((N/'presentation-overlay/mapping.json').read_bytes())
assert mapping['transformation']['name'] == 'identity'
assert (N/'presentation-overlay/display.md').read_bytes() == md
assert b'\\\\(' not in md and b'\\\\[' not in md
dest = E/'independent-decoder-91de5a'
assert not dest.exists()
files = []
for p in sorted(N.rglob('*')):
    assert not p.is_symlink(), p
    if not p.is_file():
        continue
    data = p.read_bytes()
    assert b'xwechat_files' not in data and b'wxid_' not in data, p
    q = dest/p.relative_to(N)
    q.parent.mkdir(parents=True, exist_ok=True)
    q.write_bytes(data)
    q.chmod(0o444)
    assert q.read_bytes() == data
    files.append({'path': str(q), 'sha256': sha(data), 'bytes': len(data), 'original_mode': oct(p.stat().st_mode & 0o777), 'original_flags': p.stat().st_flags, 'portable_mode': '0444', 'portable_flags_are_not_claimed_equal': True})
ap = Path('research-wiki/semantic-roundtrip/audits/huanjian-fixed-spectrum-krylov-range.json')
old = ap.read_bytes()
a = json.loads(old)
assert a['state'] == 'draft' and a['reconstruction'] == {}
assert a['publication_binding_sha256'] == '7b97440eda9692f238e20ad1f0e985b5c38b4fc4f358ccffb02535b92df14ea7'
assert a['lean']['statement_sha256'] == rec['lean_statement_sha256']
(E/'audit-before-independent-decoder.raw.json').write_bytes(old)
a['reconstruction'] = {'text': md.decode(), 'text_sha256': sha(md), 'decoder': rec['decoder'], 'decoder_run_sha256': rec['decoder_run_sha256'], 'decoder_packet_sha256': rec['canonical_packet_sha256'], 'source_text_visible': False, 'lean_statement_sha256': rec['lean_statement_sha256'], 'input_artifacts': ['lean-statement', 'approved-definition-context'], 'run_artifact': str(dest/'run/original/reconstruction.json'), 'run_artifact_raw_sha256': sha(recraw), 'decoder_run_hash_convention': rec['decoder_run_hash_convention']}
a['state'] = 'blind-reconstructed'
ap.write_bytes(dump(a))
record = {'actual_actor': rec['decoder'], 'all_original_files_copied_byte_exact': files, 'original_reconstruction_raw_sha256': sha(recraw), 'original_mathematical_run_canonical_payload_sha256': rec['decoder_run_sha256'], 'hash_convention': rec['decoder_run_hash_convention'], 'original_final_receipt_sha256': sha((N/'run/final_receipt.json').read_bytes()), 'original_finalization_permission_failure_retained': True, 'root_escaping_suspicion': 'False alarm caused by rendered JSON escaping. Actual first TeX delimiter is bytes5c28; original Markdown has correct single delimiters. Decoder independently returned an identity-only presentation overlay, retaining required TeX row separator. No mathematical or presentation repair was applied.', 'root_did_not_normalize_original_bytes': True, 'source_fidelity_verdict': 'pending independent source reviewer', 'no_sourceV_or_global_acceptance': True}
(E/'independent-decoder-exact-attachment.json').write_bytes(dump(record))
print(json.dumps({'audit_state': a['state'], 'original_files_byte_exact': len(files), 'decoder_run_sha256': rec['decoder_run_sha256'], 'reconstruction_sha256': sha(md), 'sourceV': False}))
