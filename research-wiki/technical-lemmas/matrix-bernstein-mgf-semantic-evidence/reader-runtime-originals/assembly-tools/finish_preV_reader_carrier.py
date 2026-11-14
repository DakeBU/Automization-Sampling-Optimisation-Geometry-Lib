"""Complete bounded portable custody and current PL memory; no API/Git mutation."""
from pathlib import Path
import json
import hashlib
import gzip

R = Path('/Users/zhouhuanjian/ASTIS-GC')
W = R / '.astis/huanjian-gc-weighted-mgf-20261114'
E = R / 'research-wiki/technical-lemmas/matrix-bernstein-mgf-semantic-evidence'
D = E / 'reader-runtime-originals'
RUN = R / '.astis/huanjian-resume-20261103'
sha = lambda b: hashlib.sha256(b).hexdigest()
def write(p, x):
    assert not p.exists(), p
    p.write_text(json.dumps(x, ensure_ascii=False, indent=2) + '\n')
archives = []
for stem, members in [('native-runtime', 360), ('reader-replay', 737), ('fresh-reader-review', 335)]:
    p = D / (stem + '.selected.v1.tar.gz')
    c = D / (stem + '.ROOT-container-custody.v1.json')
    x = json.loads(c.read_text())
    assert x['member_count'] == members and x['archive_sha256'] == sha(p.read_bytes())
    assert x['exact_member_set_and_every_leaf_bytes_sha256_verified_after_pack'] is True
    archives.append({'path': str(p.relative_to(R)), 'sha256': sha(p.read_bytes()),
        'bytes': p.stat().st_size, 'selected_regular_members': members,
        'custody': str(c.relative_to(R)), 'custody_sha256': sha(c.read_bytes())})
tools = D / 'assembly-tools'
tools.mkdir()
for p in [W / 'prepare_portable_reader_carrier.py', W / 'refresh_owned_cell_before_independent_V.py',
    W / 'finish_preV_reader_carrier.py',
    R / '.astis/semantic-neutral-20261114/mgf_public_progress_audit_73af/lossless_allowlist_container.py']:
    (tools / p.name).write_bytes(p.read_bytes())
assert sha((tools / 'lossless_allowlist_container.py').read_bytes()) == '70d7bdd834117fb180c3a7ab450153565a3d4f6b39fefbe998eeb913ffddbe8a'
audit = R / '.astis/semantic-neutral-20261114/mgf_public_progress_audit_73af/runtime-v4-explicit-allowlist-review.json'
assert sha(audit.read_bytes()) == 'dbdc415605e0ae5fcded327fbfc90d23ba07e06b99a9e7622f7b92499307733c'
(D / 'independent-runtime-reader-allowlist-review.json').write_bytes(audit.read_bytes())
actual_runs = D / 'ROOT-assembly-actual-runs'
actual_runs.mkdir()
run_names = [
    '20261114T093958621697Z-matrix-mgf-prepare-portable-actual-reader-carrier',
    '20261114T094010708567Z-matrix-mgf-package-exact-native-runtime-originals',
    '20261114T094021902068Z-matrix-mgf-refresh-only-owned-cell-on-independent-reader-acceptance',
    '20261114T094037289528Z-matrix-mgf-package-exact-reader-replay-originals',
    '20261114T094049967619Z-matrix-mgf-package-exact-fresh-reader-review-originals',
]
runs = []
for name in run_names:
    rp, lp = RUN / (name + '.receipt.json'), RUN / (name + '.log')
    data = lp.read_bytes()
    rec = json.loads(rp.read_text())
    assert rec['exit_code'] == 0 and rec['log_sha256'] == sha(data)
    (actual_runs / rp.name).write_bytes(rp.read_bytes())
    packed = gzip.compress(data, mtime=0)
    assert gzip.decompress(packed) == data
    (actual_runs / (lp.name + '.gz')).write_bytes(packed)
    runs.append({'receipt': str((actual_runs / rp.name).relative_to(R)), 'receipt_sha256': sha(rp.read_bytes()),
        'raw_log_gzip': str((actual_runs / (lp.name + '.gz')).relative_to(R)),
        'decoded_raw_log_sha256': sha(data), 'exit_code': 0})
write(D / 'portable-originals-custody.v1.json', {
    'kind': 'Later ROOT exact-selected-leaf packaging; not a new mathematical, source, native or runtime judgment',
    'archives': archives,
    'native_alias_resolution': 'Use native-runtime-selected.manifest.v4.json preservation_aliases to resolve historical attempt mirrors to selected exact bytes. No flags or raw outputs were recreated.',
    'reader_multi_root_resolution': 'The independent original multi-root manifest is carried unchanged. The ROOT normalized manifest only prefixes each selected leaf with its actual path relative to the repository root; all737 original hashes/bytes match.',
    'fresh_source_resolution': 'The phase5-through-final independent manifest is exact and supplements the unchanged earlier through-phase4 manifest. All335 selected original leaves retain their bytes.',
    'actual_assembly_runs': runs,
    'excluded': ['Browser profiles/cookies/cache', 'complete workspace/index/foreign-state guards', 'unselected leaves'],
    'original_actor_created_these_later_archives': False,
    'normal_proof_V_calls_by_ROOT': 0,
    'build_identity': 'Lean/native evidence remains attached to original source4869 and exact source bytes, not these later metadata/container/public export identities.',
    'main_site_integration_and_whole_goal_completion': False})
(D / 'README.md').write_text('''These are later ROOT lossless containers of explicit independent actor selections. Every regular leaf is checked against the original actor manifest by bytes and SHA-256; no raw output is trimmed or normalized. The independent actors did not create these later archives. See `portable-originals-custody.v1.json` and each container custody file for exact hashes and actual packaging receipts.

`native-runtime.selected.v1.tar.gz` uses the native runtime root. Its unchanged selection manifest also maps historical attempt mirrors to exact selected leaves. `reader-replay.selected.v1.tar.gz` uses paths relative to the original repository root; its original four-root manifest and separate ROOT normalization are both retained. `fresh-reader-review.selected.v1.tar.gz` uses the fresh review actor root and carries phase5 through the final limited visual judgment, including every selected failed predecessor. The existing105-member native mathematics archive and earlier51-file source review remain unchanged.

Inspect or extract each archive into a separate new directory. Original absolute environment/root locators are historical evidence. Relocation or replay requires explicit mappings on copies and a separately authorized browser environment; installed Chrome, Python/Playwright environments and caches are not packaged. Do not overwrite evidence originals or regenerate old receipts. The existing input snapshot permits renderer replay without access to private historical Git commits.

Current acceptance is the exact isolated desktop/mobile fixture and its tested source/copy/download/formula/graph navigation. Default graph fit is small; zoomed SVG labels can have ellipses or mobile clipping, and complete identifiers are read in the detail inspector. No physical touch, production website, post-V status pixels, full Bernstein/C6/main theorem, purification or whole-Goal acceptance is asserted.
''')
boundary = json.loads((E / 'local-proof-publication-boundary.json').read_text())
assert boundary['state'] == 'PROVED_LOCAL' and boundary['proof_VERIFIED_calls'] == 0
boundary['actual_browser_runtime'] = 'Exact isolated reader-v2/native-v4 actually passed and was independently visually accepted; see reader-current-acceptance.v1.json. No production/global integration or post-V-pixel acceptance.'
boundary['portable_reader_originals'] = 'reader-runtime-originals/portable-originals-custody.v1.json'
(E / 'local-proof-publication-boundary.json').write_text(json.dumps(boundary, ensure_ascii=False, indent=2) + '\n')
memory = json.loads((E / 'local-cycle-memory.json').read_text())
memory['current_state'] = 'PROVED_LOCAL; one normalPL, no proofV. Code/source/native/seven-slot and current isolated reader independently accepted; immutable pre-V carrier being prepared.'
memory['reader'] = 'Actual reader-v2/native-v4 passed343 checks and independent limited PNG review. Exact selected originals, all failures and reader replay inputs are portable lossless containers; original production/shared renderer remains unchanged.'
memory['current_reader_evidence'] = 'reader-current-acceptance.v1.json'
memory['next_required_action'] = 'Freeze this portable pre-V carrier, then independent verifier checks its exact committed source/evidence and records one normal VERIFIED if accepted. ROOT must not self-V. Public incremental export/push follows the safe a350 parent policy after independent payload/commit review.'
(E / 'local-cycle-memory.json').write_text(json.dumps(memory, ensure_ascii=False, indent=2) + '\n')
print(json.dumps({'archives': [{k:v for k,v in x.items() if k != 'custody_sha256'} for x in archives],
    'copied_actual_assembly_runs': len(runs), 'normal_API_calls': 0, 'Git_calls': 0}, ensure_ascii=False, indent=2))
