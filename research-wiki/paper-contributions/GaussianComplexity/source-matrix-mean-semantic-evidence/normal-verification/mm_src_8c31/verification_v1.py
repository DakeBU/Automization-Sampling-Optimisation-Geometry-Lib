#!/usr/bin/env python3
"""Bounded normal verification, with digest-only preservation of foreign state."""
from pathlib import Path
import copy
import hashlib
import json
import os
import stat
import subprocess
import sys
import tarfile
import time
from datetime import datetime, timezone

sys.dont_write_bytecode = True
ROOT = Path('/Users/zhouhuanjian/ASTIS-GC')
E = ROOT / 'research-wiki/paper-contributions/GaussianComplexity/source-matrix-mean-semantic-evidence'
OUT = E / 'normal-verification/mm_src_8c31'
SOURCE = E / 'source-review/mm_src_8c31'
NATIVE = E / 'native-review/mm_native_4a62'
CELL = ROOT / 'research-wiki/frontier-cells/ASTIS-SW-GAUSSIAN-COMPLEXITY-source-matrix-mean.json'
ADV = 'ASTIS-SA-20261112-GaussianComplexitySourceMatrixMean'
OWNER = 'huanjian_gc_20261112_source_matrix_mean'
ACTOR = '/root/mm_fresh_source_8c31'
HEAD = '94116ada2dad7de1d31ca9c67189ee734a72ed16'
MATH = '5fb1440f771bdae77ad31f27b2275447fe3e89e5'
LEDGER = ROOT / 'runs/substantive_advances.jsonl'
DISC = ROOT / 'runs/substantive_discoveries.jsonl'
DECISION = E / 'actual-VERIFIED-independent-decision.json'
sys.path.insert(0, str(ROOT))
from tools import astis_advance as advance


def now():
    return datetime.now(timezone.utc).isoformat()


def sha(b):
    return hashlib.sha256(b).hexdigest()


def canonical(x):
    return json.dumps(x, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()


def dump(path, x):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(x, ensure_ascii=False, sort_keys=True, indent=2) + '\n')


def git(*args, cwd=ROOT):
    return subprocess.run(['git', *args], cwd=cwd, capture_output=True, check=True).stdout


def filehash(path):
    h = hashlib.sha256()
    size = 0
    with path.open('rb') as f:
        while True:
            b = f.read(8 * 1024 * 1024)
            if not b:
                break
            h.update(b)
            size += len(b)
    return {'bytes': size, 'sha256': h.hexdigest()}


def exactcopy(src, dst):
    b = src.read_bytes()
    dst.parent.mkdir(parents=True, exist_ok=True)
    if dst.exists():
        assert dst.read_bytes() == b, f'No nonidentical overwrite: {dst}'
    else:
        dst.write_bytes(b)
    return {'source': str(src.relative_to(ROOT)), 'destination': str(dst.relative_to(ROOT)),
            'bytes': len(b), 'sha256': sha(b)}


def source_preservation():
    checks = []
    for name, digest, count in [
        ('portable-manifest.json', '4274f43b2e7a7edb9fe87ae39a1cee0ff4ce93739b9620a7a59bc0dc08f86e71', 66),
        ('portable-manifest-v2.json', '6947a4f6995c0657a4aaed172533003fc35f40ed0a35135c246c37603b17276d', 77),
    ]:
        b = (SOURCE / name).read_bytes()
        assert sha(b) == digest
        m = json.loads(b)
        assert m['exact_count'] == count
        for entry in m['entries']:
            h = filehash(ROOT / entry['destination'])
            assert h == {k: entry[k] for k in ('bytes', 'sha256')}
        checks.append({'manifest': str((SOURCE / name).relative_to(ROOT)), 'sha256': digest,
                       'exact_count': count, 'manifest_in_addition': True})
    actual = [p for p in SOURCE.rglob('*') if p.is_file()]
    assert len(actual) == 78
    return {'checks': checks, 'physical_regular_files': len(actual), 'all_original_bytes_unchanged': True}


def state_snapshot():
    ab = LEDGER.read_bytes()
    db = DISC.read_bytes()
    assert ab.endswith(b'\n') and db.endswith(b'\n')
    ar = [json.loads(b) for b in ab.splitlines() if b]
    dr = [json.loads(b) for b in db.splitlines() if b]
    states = advance._replay_advances(ar)
    discoveries = advance._replay_discoveries(dr)
    foreign = {k: sha(canonical(v)) for k, v in states.items() if k != ADV}
    frontier = []
    for p in sorted((ROOT / 'research-wiki/frontier-cells').rglob('*')):
        if stat.S_ISREG(p.lstat().st_mode):
            frontier.append({'path': str(p.relative_to(ROOT)), **filehash(p),
                             'mode': stat.S_IMODE(p.lstat().st_mode)})
    tracked = []
    for line in git('ls-files', '--stage', '-z').split(b'\0'):
        if not line:
            continue
        meta, rawpath = line.split(b'\t', 1)
        mode, oid, stage = meta.decode().split()
        path = os.fsdecode(rawpath)
        p = ROOT / path
        st = p.lstat()
        if stat.S_ISLNK(st.st_mode):
            b = os.fsencode(os.readlink(p))
            h = {'bytes': len(b), 'sha256': sha(b)}
            kind = 'symlink target bytes'
        else:
            assert stat.S_ISREG(st.st_mode), f'Unsupported tracked type: {path}'
            h, kind = filehash(p), 'regular file'
        tracked.append({'path': path, 'index_mode': mode, 'index_oid': oid, 'stage': stage,
                        'filesystem_mode': stat.S_IMODE(st.st_mode), 'kind': kind, **h})
    refs = {}
    for line in git('for-each-ref', '--format=%(refname) %(objectname)').decode().splitlines():
        name, commit = line.split()
        if name.endswith('/main'):
            refs[name] = commit
    cell = json.loads(CELL.read_text())
    other = copy.deepcopy(cell)
    other.pop('status')
    other['evidence'].pop('independent_verification')
    result = {
        'observed_utc': now(), 'HEAD': git('rev-parse', 'HEAD').decode().strip(),
        'actual_main_refs': refs, 'foreign_advance_full_state_digests': foreign,
        'foreign_advance_count': len(foreign), 'all_advance_count': len(states),
        'discovery_complete_state_digests': {k: sha(canonical(v)) for k, v in discoveries.items()},
        'discovery_count': len(discoveries),
        'advance_ledger_raw': {'bytes': len(ab), 'sha256': sha(ab), 'lines': len(ar)},
        'discovery_ledger_raw': {'bytes': len(db), 'sha256': sha(db), 'lines': len(dr)},
        'physical_regular_frontier_files': frontier, 'physical_regular_frontier_count': len(frontier),
        'frontier_README_present': any(p['path'] == 'research-wiki/frontier-cells/README.md' for p in frontier),
        'all_tracked_worktree_bytes_and_modes': tracked, 'tracked_count': len(tracked),
        'target_cell_raw': filehash(CELL), 'target_cell_status': cell['status'],
        'target_cell_independent_verification': cell['evidence']['independent_verification'],
        'target_cell_all_other_fields_digest': sha(canonical(other)),
        'target_advance_complete_state_digest': sha(canonical(states[ADV])),
        'target_advance_state': states[ADV]['state'], 'target_owner_id': states[ADV]['owner_id'],
        'target_transition_counts': {s: sum(r.get('advance_id') == ADV and r.get('to_state') == s for r in ar)
                                     for s in ('PROVED_LOCAL', 'VERIFIED')},
        'source_v1_v2_preservation': source_preservation(),
        'privacy': 'Only digests/counts of complete foreign states, raw ledgers and private/control files; no full snapshots exported.'}
    return result, states[ADV], ab


def receipt_run(label, command):
    receipt = OUT / f'{label}.receipt.json'
    assert not receipt.exists(), f'No receipt reuse: {label}'
    before = git('rev-parse', 'HEAD').decode().strip()
    start = time.monotonic()
    result = subprocess.run(command, cwd=ROOT, capture_output=True,
                            env={**os.environ, 'PYTHONDONTWRITEBYTECODE': '1', 'LEAN_NUM_THREADS': '2'})
    stdout, stderr = OUT / f'{label}.stdout', OUT / f'{label}.stderr'
    stdout.write_bytes(result.stdout)
    stderr.write_bytes(result.stderr)
    data = {'command': [str(x) for x in command], 'cwd': str(ROOT), 'exit_code': result.returncode,
            'elapsed_seconds': time.monotonic() - start, 'head_before': before,
            'head_after': git('rev-parse', 'HEAD').decode().strip(),
            'stdout': str(stdout.relative_to(ROOT)), 'stdout_sha256': sha(result.stdout),
            'stderr': str(stderr.relative_to(ROOT)), 'stderr_sha256': sha(result.stderr)}
    dump(receipt, data)
    assert result.returncode == 0, f'{label} exit {result.returncode}; preserve original receipt/streams'
    return data


def evidence_checks():
    results = {'source': source_preservation()}
    binding = json.loads((NATIVE / 'relevant-input-binding.json').read_text())
    assert binding['candidate'] == MATH
    current = []
    for e in binding['repository_inputs']:
        p = ROOT / e['repository_relative_path']
        assert filehash(p) == {k: e[k] for k in ('bytes', 'sha256')}
        islocal = e['repository_relative_path'].startswith('.astis/')
        if not islocal:
            b = git('show', MATH + ':' + e['repository_relative_path'])
            assert sha(b) == e['sha256'] and len(b) == e['bytes']
            assert git('show', HEAD + ':' + e['repository_relative_path']) == b
        current.append({**e, 'current_worktree_exact': True, 'candidate_and_hold_HEAD_exact': not islocal})
    assert len(current) == 50
    results['relevant_inputs'] = current
    results['binary'] = filehash(Path(binding['native_binary']['path']))
    assert results['binary'] == {k: binding['native_binary'][k] for k in ('bytes', 'sha256')}
    packages = []
    for e in binding['actual_package_pins']:
        actual = git('rev-parse', 'HEAD', cwd=Path(e['root'])).decode().strip()
        clean = not git('status', '--porcelain=v1', '--untracked-files=all', cwd=Path(e['root']))
        assert actual == e['expected'] == e['actual'] and clean
        packages.append({'name': e['name'], 'revision': actual, 'clean_including_untracked': clean})
    assert len(packages) == 9
    results['packages'] = packages
    seal = json.loads((NATIVE / 'final-seal.json').read_text())
    assert seal['candidate'] == MATH
    for name, e in seal['raw_hashes'].items():
        assert filehash(NATIVE / name) == {k: e[k] for k in ('bytes', 'sha256')}
    manifest = json.loads((NATIVE / 'portable-manifest.json').read_text())
    expected = {e['path']: e for e in manifest['payload']}
    receipt_count = 0
    own_receipts = 0
    with tarfile.open(NATIVE / 'mm_native_4a62-portable.tar.gz', 'r:gz') as archive:
        members = archive.getmembers()
        assert len(members) == 441
        seen = set()
        for member in members:
            assert member.isfile()
            b = archive.extractfile(member).read()
            if member.name == 'portable-manifest.json':
                assert b == (NATIVE / 'portable-manifest.json').read_bytes()
            else:
                e = expected[member.name]
                assert len(b) == e['bytes'] and sha(b) == e['sha256']
                seen.add(member.name)
            if member.name.endswith('.receipt.json'):
                receipt_count += 1
                if member.name.startswith('receipts/'):
                    own_receipts += 1
        assert seen == set(expected)
    assert own_receipts == manifest['own_receipt_count'] == 109
    results['native_archive'] = {'payload': len(expected), 'members': len(members),
                                 'own_receipts': own_receipts, 'all_receipts_including_history': receipt_count,
                                 'raw': filehash(NATIVE / 'mm_native_4a62-portable.tar.gz')}
    report = json.loads((NATIVE / 'report.json').read_text())
    assert report['native']['fresh_compile_exit_codes'] == [0] * 7
    assert report['native']['whole_module_constant_count'] == 39
    assert report['native']['new_owned_count'] == 3
    assert report['native']['allowed_axioms_only'] == ['propext', 'Classical.choice', 'Quot.sound']
    results['native_scope'] = {'candidate_only': MATH, 'modules': 7, 'full_types_bodies': 39,
                              'root_reachable': 32, 'old_generated_outside': 7, 'new_owned': 3,
                              'static_reader_only': True, 'browser_publicsite_purification': False,
                              'failures_retained': report['receipts'], 'no_later_HEAD_recompile_claim': True}
    dump_path = ROOT / '.astis/semantic-neutral-20261112/mm_native_4a62/local/native-wholemodule.json'
    if dump_path.is_file():
        h = filehash(dump_path)
        assert h == {k: report['large_local_dump'][k] for k in ('bytes', 'sha256')}
        results['large_native_local_dump'] = {'path': str(dump_path), **h, 'stream_hashed_not_exported': True}
    else:
        results['large_native_local_dump'] = {'not_locally_available_at_expected_original_path': True,
                                              'no_dump_exported': True, 'pinned_report_metadata': report['large_local_dump']}
    gate_specs = [
        ('20261112T132602824054Z-source-matrix-mean-final-reviewed-publication', 'bc8a4ccfac2e212eb5d187599a80b188fb0eb5b551eae30f9930e87c006b2143'),
        ('20261112T132602823955Z-source-matrix-mean-final-semantic', 'c1c4a5c5b01e7391fdfe40bb3878a9fbb710274fc739885d31d27fa1597edc07'),
        ('20261112T132602823951Z-source-matrix-mean-final-contributor', '64169613ce224659c2169dc75380d00dd4930b4386f143838238c17a6be098fe'),
        ('20261112T132602823955Z-source-matrix-mean-final-frontier', '76ef50cdad59549b7d95c0663405e8fef7cf2ac29f5ab39a6660de9f34d6b06c'),
    ]
    results['final_gates'] = []
    for stem, digest in gate_specs:
        path = ROOT / '.astis/huanjian-resume-20261103' / (stem + '.receipt.json')
        b = path.read_bytes()
        e = json.loads(b)
        assert e['head_before'] == e['head_after'] == HEAD and e['exit_code'] == 0
        assert e['log_sha256'] == digest and filehash(Path(e['log']))['sha256'] == digest
        exactcopy(path, OUT / 'inputs/final-gates' / path.name)
        exactcopy(Path(e['log']), OUT / 'inputs/final-gates' / Path(e['log']).name)
        results['final_gates'].append({'receipt': str(path.relative_to(ROOT)), 'receipt_sha256': sha(b),
                                       'exit_code': 0, 'log_sha256': digest, 'HEAD': HEAD})
    for name in ['report.json', 'report.md', 'final-seal.json', 'portable-manifest.json',
                 'mm_native_4a62-portable.tar.gz', 'relevant-input-binding.json',
                 'metadata-carrier-byte-comparison.json', 'REPRODUCE.md']:
        exactcopy(NATIVE / name, OUT / 'inputs/native' / name)
    for p in sorted(SOURCE.rglob('*')):
        if p.is_file():
            exactcopy(p, OUT / 'inputs/source-review-originals' / p.relative_to(SOURCE))
    return results


def precheck():
    assert git('rev-parse', 'HEAD').decode().strip() == HEAD
    assert not git('status', '--porcelain=v1', '-uno')
    assert not (OUT / 'api-once-v1.started.json').exists()
    results = evidence_checks()
    prefrontier = receipt_run('pre-frontier-v1', [sys.executable, '-B', 'tools/astis_frontier_cells.py', 'check'])
    snapshot, item, ab = state_snapshot()
    assert snapshot['HEAD'] == HEAD and snapshot['target_advance_state'] == 'PROVED_LOCAL'
    assert snapshot['target_owner_id'] == OWNER and snapshot['target_cell_status'] == 'proved_locally'
    assert snapshot['target_cell_independent_verification'] == ''
    assert snapshot['foreign_advance_count'] >= 307 and snapshot['discovery_count'] >= 43
    assert snapshot['physical_regular_frontier_count'] >= 467 and snapshot['frontier_README_present']
    assert snapshot['target_transition_counts'] == {'PROVED_LOCAL': 1, 'VERIFIED': 0}
    raw = (E / 'actual-PROVED_LOCAL-append.exact.jsonl').read_bytes()
    pb = (E / 'actual-PROVED_LOCAL-evidence.full.json').read_bytes()
    assert sha(raw) == '54c848e162b60fd716874be23acde307fba9e5cd09915913aa369c569ee1cd6d'
    assert sha(pb) == '917c02437299ae4b3848bc0fa01affa46afa3b3c74ee5d0a472c701bccb8e291'
    assert raw in ab.splitlines(keepends=True)
    original = json.loads(pb)
    assert len(original) == 20 and json.loads(raw)['evidence'] == original == item['latest_evidence']
    exactcopy(E / 'actual-PROVED_LOCAL-evidence.full.json', OUT / 'PROVED_LOCAL-original-evidence.full.json')
    exactcopy(E / 'actual-PROVED_LOCAL-append.exact.jsonl', OUT / 'PROVED_LOCAL-original-append.exact.jsonl')
    dump(OUT / 'pre-preservation-digests-v1.json', snapshot)
    dump(OUT / 'precheck-v1.json', {'status': 'PASS', 'metadata_HEAD': HEAD, 'compiled_math_candidate': MATH,
                                   'checks': results, 'pre_frontier': prefrontier,
                                   'original_20_fields_inline_count': len(original), 'normal_API_calls_so_far': 0})
    evidence = copy.deepcopy(original)
    assert not set(evidence) & {'gate', 'verifier_id', 'verified_commit', 'source_audit', 'fake_closure_scan'}
    evidence.update({
        'gate': {'final_four_exit0_at_metadata_HEAD': results['final_gates'],
                 'independent_native_report': str((NATIVE / 'report.json').relative_to(ROOT)),
                 'independent_native_report_sha256': '82efcb654cdbd8e65e11dc17a5136d3c516b8730a92bcdc36416aaaf13f9a65e',
                 'normal_pre_frontier_exit': 0},
        'verifier_id': ACTOR, 'verified_commit': MATH,
        'verification_metadata_HEAD': HEAD,
        'source_audit': {'reviewer': ACTOR, 'verdict': 'equivalent-after-elaboration',
                         'report': str((SOURCE / 'phase4-final-report.md').relative_to(ROOT)),
                         'report_sha256': '89550a6307ff2d651fc906d342d6690f1bf37c0559623f10966268f2a257b2dd',
                         'overlay_v2': str((SOURCE / 'canonical-overlay-v2.json').relative_to(ROOT)),
                         'overlay_v2_sha256': '272a6337202644e922299cf2199a6b3d643eca3f58b710f41ab09c4d89027793',
                         'publication_binding_sha256': original['publication_binding_sha256']},
        'fake_closure_scan': {'scope': 'Fresh seven modules,39 closed full types/bodies,3 new all reachable; standard axioms only',
                              'allowed_axioms': ['propext', 'Classical.choice', 'Quot.sound'],
                              'native_report_sha256': '82efcb654cdbd8e65e11dc17a5136d3c516b8730a92bcdc36416aaaf13f9a65e'},
        'PROVED_LOCAL_original_payload_raw_sha256': sha(pb),
        'PROVED_LOCAL_original_20_fields_inline_preserved': True,
        'independent_decision_artifact': str(DECISION.relative_to(ROOT)),
        'normal_VERIFIED_scope': 'Bounded local source/native verification only; no stabilization, release, integration, main-bound, public delivery or purification credit.',
    })
    assert all(evidence[k] == original[k] for k in original)
    dump(OUT / 'actual-VERIFIED-evidence.full.json', evidence)
    print(json.dumps({'precheck': 'PASS', 'physical_regular_frontier_files': snapshot['physical_regular_frontier_count'],
                      'foreign_complete_states': snapshot['foreign_advance_count'], 'complete_discoveries': snapshot['discovery_count'],
                      'tracked_files': snapshot['tracked_count'], 'HEAD': HEAD,
                      'actual_main_refs': snapshot['actual_main_refs'], 'normal_API_calls': 0}, ensure_ascii=False))


def readback_and_cell():
    pre = json.loads((OUT / 'pre-preservation-digests-v1.json').read_text())
    ab = LEDGER.read_bytes()
    n = pre['advance_ledger_raw']['bytes']
    assert sha(ab[:n]) == pre['advance_ledger_raw']['sha256']
    append = ab[n:]
    assert append.endswith(b'\n') and len(append.splitlines()) == 1
    event = json.loads(append)
    payload = json.loads((OUT / 'actual-VERIFIED-evidence.full.json').read_text())
    assert event['event'] == 'transition' and event['advance_id'] == ADV
    assert event['from_state'] == 'PROVED_LOCAL' and event['to_state'] == 'VERIFIED'
    assert event['worker_id'] == ACTOR and event['evidence'] == payload
    records = [json.loads(x) for x in ab.splitlines()]
    item = advance._replay_advances(records)[ADV]
    assert item['state'] == 'VERIFIED' and item['last_actor'] == ACTOR
    assert sum(r.get('advance_id') == ADV and r.get('to_state') == 'VERIFIED' for r in records) == 1
    (OUT / 'actual-VERIFIED-append.exact.jsonl').write_bytes(append)
    dump(OUT / 'actual-outcome-before-any-further-action-v1.json',
         {'state': item['state'], 'last_actor': item['last_actor'], 'owner_unchanged': item['owner_id'] == OWNER,
          'one_normal_VERIFIED_append': True, 'append_bytes': len(append), 'append_sha256': sha(append),
          'original_prefix_sha256_unchanged': True, 'actual_event_full_payload_equal': True})
    before = CELL.read_bytes()
    assert filehash(CELL) == pre['target_cell_raw']
    after = before.replace(b'"status": "proved_locally"', b'"status": "independently_verified"', 1)
    needle = b'"independent_verification": ""'
    assert before.count(needle) == 1
    replacement = ('"independent_verification": "' + str(DECISION.relative_to(ROOT)) + '"').encode()
    after = after.replace(needle, replacement, 1)
    bobj, aobj = json.loads(before), json.loads(after)
    check = copy.deepcopy(aobj)
    check['status'] = bobj['status']
    check['evidence']['independent_verification'] = bobj['evidence']['independent_verification']
    assert check == bobj and aobj['status'] == 'independently_verified'
    CELL.write_bytes(after)
    dump(OUT / 'cell-two-field-delta-v1.json', {'path': str(CELL.relative_to(ROOT)), 'before': {'bytes': len(before), 'sha256': sha(before)},
        'after': {'bytes': len(after), 'sha256': sha(after)}, 'only_structural_paths_changed': ['status', 'evidence.independent_verification'],
        'all_other_fields_equal': True, 'textual_replacement_only_preserved_other_bytes': True})
    print('Actual ledger outcome read back VERIFIED once; only then changed the two authorized cell fields.')


def postcheck():
    pre = json.loads((OUT / 'pre-preservation-digests-v1.json').read_text())
    frontier = receipt_run('post-frontier-v1', [sys.executable, '-B', 'tools/astis_frontier_cells.py', 'check'])
    post, item, ab = state_snapshot()
    assert post['HEAD'] == pre['HEAD'] == HEAD
    for key in ['actual_main_refs', 'foreign_advance_full_state_digests', 'foreign_advance_count',
                'discovery_complete_state_digests', 'discovery_count', 'discovery_ledger_raw',
                'physical_regular_frontier_count', 'frontier_README_present', 'target_cell_all_other_fields_digest',
                'source_v1_v2_preservation', 'tracked_count']:
        assert post[key] == pre[key], key
    cell_path = str(CELL.relative_to(ROOT))
    for key in ['physical_regular_frontier_files', 'all_tracked_worktree_bytes_and_modes']:
        before = {e['path']: e for e in pre[key]}
        after = {e['path']: e for e in post[key]}
        assert before.keys() == after.keys()
        for path in before:
            if path not in [cell_path, str(LEDGER.relative_to(ROOT))]:
                assert before[path] == after[path], path
            elif key == 'all_tracked_worktree_bytes_and_modes':
                for field in ['index_mode', 'index_oid', 'stage', 'filesystem_mode', 'kind']:
                    assert before[path][field] == after[path][field]
    n = pre['advance_ledger_raw']['bytes']
    assert sha(ab[:n]) == pre['advance_ledger_raw']['sha256']
    append = ab[n:]
    assert append == (OUT / 'actual-VERIFIED-append.exact.jsonl').read_bytes()
    assert post['target_advance_state'] == 'VERIFIED' and post['target_owner_id'] == OWNER
    assert post['target_transition_counts'] == {'PROVED_LOCAL': 1, 'VERIFIED': 1}
    assert post['target_cell_status'] == 'independently_verified'
    assert post['target_cell_independent_verification'] == str(DECISION.relative_to(ROOT))
    dump(OUT / 'post-preservation-digests-v1.json', post)
    proof = {'status': 'PASS', 'HEAD': HEAD, 'actual_main_refs': post['actual_main_refs'],
             'physical_regular_frontier_count': post['physical_regular_frontier_count'],
             'foreign_advance_complete_states_unchanged': post['foreign_advance_count'],
             'discovery_complete_states_and_raw_bytes_unchanged': post['discovery_count'],
             'all_prior_frontier_regular_files_including_README_preserved_except_two_authorized_C_fields': True,
             'all_other_tracked_bytes_and_all_modes_unchanged': True, 'tracked_count': post['tracked_count'],
             'advance_ledger_original_raw_prefix_unchanged': True, 'exactly_one_normal_VERIFIED_append': True,
             'original_20_payload_fields_all_inline_unchanged': True, 'source_v1_67_and_v2_78_all_unchanged': True,
             'pre_frontier_exit': 0, 'post_frontier_exit': frontier['exit_code'], 'API_not_replayed': True,
             'privacy': 'No full foreign/control/private snapshots exported.'}
    dump(OUT / 'preservation-readback-v1.json', proof)
    print(json.dumps(proof, ensure_ascii=False))


if __name__ == '__main__':
    {'precheck': precheck, 'readback-and-cell': readback_and_cell, 'postcheck': postcheck}[sys.argv[1]]()
