"""Original-source-actor preparation and guarded, grant-required, once-only API.

Default command is read-only preflight. Preparation writes only private evidence.
This script has NOT been granted execution of the VERIFIED transition.
Never archive phase4-private: it contains raw foreign state and control snapshots.
"""
from __future__ import annotations
import argparse
import copy
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys
import tarfile
import traceback

if sys.flags.optimize != 0:
    raise RuntimeError('PYTHONOPTIMIZE/-O must be zero; assertions must remain active')
assert os.environ.get('PYTHONOPTIMIZE') == '0', 'Set PYTHONOPTIMIZE=0 explicitly'
assert sys.flags.optimize == 0
ROOT = Path('/Users/zhouhuanjian/ASTIS-GC')
OUT = ROOT / '.astis/semantic-neutral-20261110/d_fresh_a6c943'
PRIVATE = OUT / 'phase4-private'
MATH = '65776f88e92b9680e6afe0d4c20b7390e4521241'
CARRIER = '34576d8b98a58568e1619185ac88ee762b999caa'
BASE = '8c88749c51c87ce54c22e7910b366c0f9f3fba6d'
ACTOR = '/root/detector_fresh_source'
OWNER = 'huanjian_gc_20261110_fixed_spectrum_detector'
NATIVE_ACTOR = '/root/detector_module_reader_72c9e4'
ADV = 'ASTIS-SA-20261110-GaussianComplexityFixedSpectrumDetector'
NAME = 'AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumDetector.actual_chebyshev_matrix_cosine'
CELL = 'research-wiki/frontier-cells/ASTIS-SW-GAUSSIAN-COMPLEXITY-fixed-spectrum-detector.json'
LEDGER = 'runs/substantive_advances.jsonl'
E = 'research-wiki/paper-contributions/GaussianComplexity/fixed-spectrum-detector-semantic-evidence/'
NATIVE = ROOT / '.astis/semantic-neutral-20261110/d_module_72c9e4'
FRAGMENT = 'research-wiki/semantic-roundtrip/audits/huanjian-fixed-spectrum-detector.json'
BOUNDARY = (
    'Normal independent source VERIFIED for the declared matrix-Chebyshev/cosine auxiliary and '
    'private literal rotated-pushforward strict-event/Borel component; original source actor '
    + ACTOR + '; proof owner remains ' + OWNER + '. Metadata carrier ' + CARRIER
    + ' preserves mathematical candidate ' + MATH + ' bytes. Independent native/kernel and isolated '
    'static checks occurred at the mathematical candidate; no fresh native run at the metadata '
    'carrier is asserted. Original source/native/PROVED_LOCAL evidence keys and nested values are '
    'retained. Gaussian pi_A law recognition, target probability/concentration/Krylov/Haar/adaptive '
    'algorithm/TV/query/cost and both full main lower bounds, STAB/integration/public browser delivery/'
    'purification/Exposition Seal/global/wholeGoal remain separate. Future post_integration may only '
    'be appended by this same original source actor, preserving every original evidence field.'
)
sys.path.insert(0, str(ROOT / 'tools'))
sys.path.insert(0, str(ROOT))
from tools import astis_advance as advance
import astis_semantic_roundtrip as roundtrip
from tools.astis_publication import check_advance

def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def canonical(obj) -> str:
    return sha(json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode())

def digest(path: Path) -> dict:
    h = hashlib.sha256()
    with path.open('rb') as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b''):
            h.update(chunk)
    return {'path': str(path.relative_to(ROOT)) if path.is_relative_to(ROOT) else str(path),
            'bytes': path.stat().st_size, 'sha256': h.hexdigest()}

def write(path: Path, data: bytes):
    assert path.is_relative_to(PRIVATE), path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)
    path.chmod(0o600)

def dump(path: Path, obj):
    write(path, (json.dumps(obj, ensure_ascii=False, indent=2) + '\n').encode())

def load(path: Path):
    return json.loads(path.read_bytes())

def git(*args) -> bytes:
    return subprocess.run(['git', *args], cwd=ROOT, check=True,
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                          env={**os.environ, 'GIT_OPTIONAL_LOCKS': '0'}).stdout

def replay(raw: bytes) -> dict:
    assert raw.endswith(b'\n'), 'No interrupted ledger tail recovery is authorized'
    records = [json.loads(line) for line in raw.splitlines() if line.strip()]
    return advance._replay_advances(records)

def tracked_names() -> list[str]:
    return [os.fsdecode(p) for p in git('ls-files', '-z').split(b'\0') if p]

def file_signature(path: Path) -> dict:
    info = path.lstat()
    if stat.S_ISLNK(info.st_mode):
        return {'kind': 'symlink', 'target': os.readlink(path), 'mode': stat.S_IMODE(info.st_mode)}
    assert stat.S_ISREG(info.st_mode), path
    d = digest(path)
    return {'kind': 'file', 'bytes': d['bytes'], 'sha256': d['sha256'],
            'mode': stat.S_IMODE(info.st_mode)}

def controls() -> list[str]:
    paths = set(p.relative_to(ROOT).as_posix() for p in
                (ROOT / 'research-wiki/frontier-cells').rglob('*') if p.is_file())
    paths |= {p.relative_to(ROOT).as_posix() for p in (ROOT / 'runs').iterdir() if p.is_file()}
    paths.add('website/content/samplewiki_companion_frontiers.json')
    # Repository-local live queue/control surfaces, if present. Historical run
    # directories are not treated as mutable global control planes.
    for p in (ROOT / '.astis').iterdir():
        if p.is_file() and any(s in p.name.lower() for s in
                               ['queue', 'control', 'global', 'goal', 'steer', 'execution']):
            paths.add(p.relative_to(ROOT).as_posix())
    for name in ['control', 'queues', 'runtime', 'harness', 'state', 'locks']:
        d = ROOT / '.astis' / name
        if d.is_dir():
            paths |= {p.relative_to(ROOT).as_posix() for p in d.rglob('*') if p.is_file()}
    return sorted(paths)

def own_and_foreign(raw: bytes):
    states = replay(raw)
    assert len(states) == 296 and ADV in states
    own = states[ADV]
    assert own['owner_id'] == OWNER
    return own, {k: v for k, v in states.items() if k != ADV}

def math_and_metadata_checks() -> dict:
    assert git('rev-parse', 'HEAD').decode().strip() == CARRIER
    assert git('rev-parse', CARRIER + '^').decode().strip() == MATH
    relevant = [
        'AutoSamplingTheory/ExampleCases/GaussianComplexity/FixedSpectrumDetector.lean',
        'Tests/GaussianComplexityFixedSpectrumDetector.lean',
        'website/content/declaration_lessons/huanjian-fixed-spectrum-detector.json',
        'website/content/publications/huanjian-fixed-spectrum-detector.json',
        E + 'source-to-lean-map-v1.json', E + 'fresh-source-reviewer-packet.json',
        E + 'producer-signature.txt', E + 'consumer-signature.txt',
        'research-wiki/paper-contributions/GaussianComplexity/fixed-spectrum-detector-statement-seal.json',
        'lean-toolchain', 'lake-manifest.json',
    ]
    signatures = {}
    for name in relevant:
        expected = git('show', MATH + ':' + name)
        assert git('show', CARRIER + ':' + name) == expected
        assert (ROOT / name).read_bytes() == expected
        signatures[name] = sha(expected)
    proposal = load(OUT / 'phase3-proposal.json')
    merged = roundtrip.load_registry()
    matches = [a for a in merged['audits'] if a.get('id') ==
               'ASTIS-RT-20261110-HuanjianFixedSpectrumDetector']
    assert len(matches) == 1
    audited = matches[0]
    assert all(audited.get(k) == v for k, v in proposal.items())
    before = load(ROOT / (E + 'audit-before-independent-full-source-application.raw.json'))
    assert {k: v for k, v in audited.items() if k not in proposal} == \
           {k: v for k, v in before.items() if k not in proposal}
    assert load(ROOT / FRAGMENT) == audited
    check_advance([NAME], reviewed=True)
    return {'mathematical_file_sha256': signatures, 'own_fragment': digest(ROOT / FRAGMENT),
            'merged_audit_id': audited['id'], 'original_five_fields_value_equal': True,
            'all_other_audit_fields_value_equal_to_before': True,
            'actual_wrapper_publication_reviewed_gate_passed': True}

def verify_originals() -> dict:
    pinned = {'freeze-receipt.json': 'c9fcba354e8a55a20111e8ccc461da6d74afac96d85f3ab5f374db6f64cbdcc3',
              'freeze-manifest.json': '0b09e4f7ac6446e62b6529972a6c87d103994c1dcf333e8aa62e3f0d50566d76',
              'independent-report.json': '2e6e606960aaabbde77722a6cb1473ccd6079092798d36e00b4b6e630191696c'}
    for name, expected in pinned.items():
        assert digest(NATIVE / name)['sha256'] == expected
    manifest = load(NATIVE / 'freeze-manifest.json')
    for row in manifest['lossless_carry_required'] + manifest['native_cache_retained_in_place']:
        p = NATIVE / row['path_relative_to_bundle']
        d = digest(p)
        assert d['bytes'] == row['byte_length'] and d['sha256'] == row['raw_sha256']
        assert stat.S_IMODE(p.stat().st_mode) == 0o444
    report = load(NATIVE / 'independent-report.json')
    assert report['candidate_commit'] == MATH and report['actual_final_head'] == MATH
    assert report['whole_module_review']['P_sha256'] == '98d055da8ca5a10fe56874b19a58fb523511b9fc7c5ae13e20225e18340ed75a'
    for command in report['commands_and_evidence']:
        receipt = load(NATIVE / command['receipt'])
        log = (NATIVE / command['log']).read_bytes()
        assert sha(log) == command['log_raw_sha256'] and len(log) == command['log_byte_length']
        assert receipt['exit_code'] == command['exit_code']
        assert receipt['head_before'] == MATH == receipt['head_after']
    archive_results = []
    for archive_name, manifest_name, base, expected_sha, count in [
        ('independent-native-fullmodule-static.lossless-file-bytes.tar.gz',
         'independent-native-fullmodule-static.archive-manifest.json', NATIVE,
         'eaf9bb161fb1a1fed28746e349b0ea2c3024dd9f3b8487c489590d416e75ab42', 128),
        ('independent-full-source-all-phases.lossless-file-bytes.tar.gz',
         'independent-full-source-all-phases.archive-manifest.json', OUT,
         '5e543e11b0b5be188bb5b1435a20649fa0919eef401277b91161b43df42c6582', 63),
    ]:
        archive = ROOT / (E + archive_name)
        assert digest(archive)['sha256'] == expected_sha
        am = load(ROOT / (E + manifest_name))
        assert not am['raw_foreign_snapshots_included'] and am['file_count'] == count
        with tarfile.open(archive, 'r:gz') as tf:
            members = {m.name: m for m in tf.getmembers() if m.isfile()}
            assert len(members) == count
            for row in am['files']:
                name = row['path']
                assert not Path(name).is_absolute() and '..' not in Path(name).parts
                payload = tf.extractfile(members[name]).read()
                assert payload == (base / name).read_bytes()
                assert sha(payload) == row['sha256'] and len(payload) == row['bytes']
        archive_results.append({'archive': digest(archive), 'file_count': count,
                                'all_original_file_bytes_rechecked': True})
    return {'native_actor': NATIVE_ACTOR, 'native_report': digest(NATIVE / 'independent-report.json'),
            'native_original_126_carry_plus_2_control': True,
            'native_6_caches_0444_retained_in_place': True, 'archives': archive_results}

def snapshot():
    assert not (PRIVATE / 'baseline.json').exists(), 'Never overwrite the private baseline'
    PRIVATE.mkdir(mode=0o700, parents=True, exist_ok=True)
    PRIVATE.chmod(0o700)
    write(PRIVATE / 'DO_NOT_ARCHIVE_FOREIGN_RAW',
          b'PRIVATE ONLY. Raw foreign replayed states/ledger/frontier/global/queue controls. Never archive or publish.\n')
    assert git('rev-parse', 'HEAD').decode().strip() == CARRIER
    assert not git('diff', '--name-only', 'HEAD'), 'Pre-API tracked working bytes must be clean'
    ledger_raw = (ROOT / LEDGER).read_bytes()
    own, foreign = own_and_foreign(ledger_raw)
    assert own['state'] == 'PROVED_LOCAL'
    assert own['publication_declarations'] == [NAME]
    write(PRIVATE / 'ledger-prefix.raw.jsonl', ledger_raw)
    dump(PRIVATE / 'all-295-foreign-replayed-values.private.json', foreign)
    dump(PRIVATE / 'own-advance-before.private.json', own)
    tracked = {name: file_signature(ROOT / name) for name in tracked_names()}
    control_names = controls()
    for name in control_names:
        write(PRIVATE / 'raw-controls' / name, (ROOT / name).read_bytes())
    cell_raw = (ROOT / CELL).read_bytes()
    cell = json.loads(cell_raw)
    assert cell['status'] == 'proved_locally' and cell['owner_id'] == OWNER
    assert 'integration_boundary' not in cell['evidence']
    write(PRIVATE / 'own-C-before.raw.json', cell_raw)
    dump(PRIVATE / 'baseline.json', {
        'carrier': CARRIER, 'mathematical_candidate': MATH, 'actor': ACTOR, 'owner': OWNER,
        'advance': ADV, 'ledger_prefix_bytes': len(ledger_raw), 'ledger_prefix_sha256': sha(ledger_raw),
        'foreign_count': len(foreign), 'tracked': tracked, 'controls': control_names,
        'own_cell': CELL, 'own_cell_sha256': sha(cell_raw),
        'all_foreign_frontier_count': sum(1 for p in control_names if
            p.startswith('research-wiki/frontier-cells/') and p != CELL),
    })
    print(json.dumps({'private_snapshot_created': True, 'tracked_files': len(tracked),
                      'foreign_states': len(foreign), 'raw_control_files': len(control_names),
                      'ledger_prefix_bytes': len(ledger_raw)}), flush=True)

def guard(stage='before') -> dict:
    assert stage in {'before', 'after-api', 'after-closeout'}
    b = load(PRIVATE / 'baseline.json')
    assert b['actor'] == ACTOR and b['owner'] == OWNER and b['carrier'] == CARRIER
    assert git('rev-parse', 'HEAD').decode().strip() == CARRIER
    prefix = (PRIVATE / 'ledger-prefix.raw.jsonl').read_bytes()
    raw = (ROOT / LEDGER).read_bytes()
    own, foreign = own_and_foreign(raw)
    assert foreign == load(PRIVATE / 'all-295-foreign-replayed-values.private.json')
    assert own['owner_id'] == OWNER and own['publication_declarations'] == [NAME]
    if stage == 'before':
        assert raw == prefix and own == load(PRIVATE / 'own-advance-before.private.json')
        assert own['state'] == 'PROVED_LOCAL'
    else:
        assert raw.startswith(prefix) and len(raw) > len(prefix)
        suffix = raw[len(prefix):]
        rows = [json.loads(line) for line in suffix.splitlines() if line.strip()]
        assert len(rows) == 1
        event = rows[0]
        assert event['event'] == 'transition' and event['advance_id'] == ADV
        assert event['from_state'] == 'PROVED_LOCAL' and event['to_state'] == 'VERIFIED'
        assert event['worker_id'] == ACTOR
        assert event['evidence'] == load(PRIVATE / 'normal-VERIFIED-evidence.complete.json')
        assert own['state'] == 'VERIFIED'
    assert set(tracked_names()) == set(b['tracked'])
    allowed = set() if stage == 'before' else {LEDGER}
    if stage == 'after-closeout':
        allowed.add(CELL)
    for name, expected in b['tracked'].items():
        if name not in allowed:
            assert file_signature(ROOT / name) == expected, 'Tracked bytes/mode changed: ' + name
        elif stage != 'before':
            assert stat.S_IMODE((ROOT / name).stat().st_mode) == expected['mode'], name
    assert controls() == b['controls'], 'Global/frontier/queue control path set changed'
    for name in b['controls']:
        if name not in allowed:
            assert (ROOT / name).read_bytes() == (PRIVATE / 'raw-controls' / name).read_bytes(), name
    if stage == 'after-closeout':
        old = json.loads((PRIVATE / 'own-C-before.raw.json').read_bytes())
        current = load(ROOT / CELL)
        expected = copy.deepcopy(old)
        expected['status'] = 'independently_verified'
        expected['evidence']['integration_boundary'] = BOUNDARY
        assert current == expected and current['owner_id'] == OWNER
    return {'stage': stage, 'all_295_foreign_values_identical': True,
            'complete_ledger_raw_prefix_preserved': True,
            'all_protected_tracked_bytes_modes_identical': True,
            'foreign_frontier_global_queue_raw_identical': True,
            'owner_and_exact_publication_target_unchanged': True,
            'normal_post_API_ledger_dirty_allowed': stage != 'before'}

def run_gate(label, args):
    started = datetime.now(timezone.utc).isoformat()
    result = subprocess.run([sys.executable, *args], cwd=ROOT,
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                            env={**os.environ, 'PYTHONOPTIMIZE': '0',
                                 'PYTHONDONTWRITEBYTECODE': '1', 'GIT_OPTIONAL_LOCKS': '0'})
    log = PRIVATE / ('gates/' + label + '.log')
    write(log, result.stdout)
    receipt = {'command': [sys.executable, *args], 'actual_HEAD': CARRIER,
               'started_utc': started, 'finished_utc': datetime.now(timezone.utc).isoformat(),
               'exit_code': result.returncode, 'log': digest(log),
               'scope': 'actual read-only metadata/control gate at carrier; no new Lean/native claim'}
    dump(PRIVATE / ('gates/' + label + '.receipt.json'), receipt)
    assert result.returncode == 0, label + ' gate failed; inspect retained private log'
    return receipt

def prepare():
    assert not (PRIVATE / 'execution-attempted.json').exists()
    start_guard = guard('before')
    checked = math_and_metadata_checks()
    originals = verify_originals()
    gates = [run_gate(label, args) for label, args in [
        ('contributor', ['tools/astis_contributor_contract.py', 'check', '--base', BASE]),
        ('publication', ['tools/astis_publication.py', 'check', '--base', BASE]),
        ('semantic-wrapper', ['tools/astis_semantic_roundtrip.py', 'check']),
        ('frontier', ['tools/astis_frontier_cells.py', 'check']),
    ]]
    end_guard = guard('before')
    old = load(PRIVATE / 'own-advance-before.private.json')['latest_evidence']
    evidence = copy.deepcopy(old)
    additions = {
        'gate': {'actual_carrier_metadata_gates': gates,
                 'native_checked_mathematical_commit': MATH,
                 'accepted_review_metadata_carrier': CARRIER,
                 'no_fresh_native_at_carrier_claim': True},
        'verifier_id': ACTOR,
        'verified_commit': CARRIER,
        'native_checked_commit': MATH,
        'source_audit': load(OUT / 'phase3-proposal.json'),
        'fake_closure_scan': copy.deepcopy(load(NATIVE / 'independent-report.json')['native']),
        'original_source_review_run_complete': load(OUT / 'phase3-source-review-run.json'),
        'original_native_wholemodule_static_report_complete': load(NATIVE / 'independent-report.json'),
        'original_source_exposure_manifest_complete': load(OUT / 'phase3-input-exposure-manifest.json'),
        'original_PROVED_LOCAL_evidence_complete': copy.deepcopy(old),
        'original_native_and_source_archives': originals,
        'metadata_exact_identity_checks': checked,
        'verification_actor_identity': {'source_actor_full': ACTOR,
            'native_actor_full': NATIVE_ACTOR, 'native_report_shortlabel_is_same_actor': True,
            'proof_owner_retained': OWNER},
        'verification_scope': BOUNDARY,
        'original_evidence_retention_policy': 'Every original key and nested value is retained without a fixed key whitelist. Historical PROVED_LOCAL flags remain historical. Only the same original source actor may later append post_integration; no root/new-actor schema projection.',
    }
    assert not (set(evidence) & set(additions)), 'Never overwrite an original evidence key'
    evidence.update(additions)
    assert all(evidence[k] == v for k, v in old.items())
    advance._validate_transition_evidence('VERIFIED', evidence, schema_version=4)
    dump(PRIVATE / 'normal-VERIFIED-evidence.complete.json', evidence)
    dump(PRIVATE / 'read-only-preflight.json', {
        'state': 'READY_FOR_FINAL_EXECUTION_GRANT_ONLY', 'API_executed': False,
        'actor': ACTOR, 'owner': OWNER, 'advance': ADV, 'carrier': CARRIER,
        'mathematical_candidate': MATH, 'before_guard': start_guard,
        'after_gate_guard': end_guard, 'metadata': checked, 'originals': originals,
        'actual_read_only_gate_receipts': gates,
        'evidence': digest(PRIVATE / 'normal-VERIFIED-evidence.complete.json'),
        'diagnoses_retained': ['raw/canonical packet hash distinction in prior frozen phase',
          'core old registry versus public wrapper merged fragment entry; no mathematical failure',
          'normal future API append makes ledger dirty, so post-API guard allows that exact append'],
        'next': 'Do not execute. Parent must review frozen preparation hashes and issue final grant.'})
    print(json.dumps({'read_only_preflight_passed': True, 'API_executed': False,
                      'evidence': digest(PRIVATE / 'normal-VERIFIED-evidence.complete.json')}, indent=2))

def grant_check(path: Path):
    grant = load(path)
    assert grant['authorized_action'] == 'ONE_NORMAL_PROVED_LOCAL_TO_VERIFIED_THEN_OWN_C_TWO_FIELDS'
    assert grant['advance_id'] == ADV and grant['actor'] == ACTOR and grant['owner'] == OWNER
    assert grant['carrier'] == CARRIER and grant['mathematical_candidate'] == MATH
    assert grant['script_sha256'] == digest(Path(__file__).resolve())['sha256']
    assert grant['evidence_sha256'] == digest(PRIVATE / 'normal-VERIFIED-evidence.complete.json')['sha256']
    assert grant['explicit_parent_execution_grant_received'] is True
    assert str(grant['original_parent_grant_text']).strip()
    return grant

def observe_api_outcome(error=None):
    prefix = (PRIVATE / 'ledger-prefix.raw.jsonl').read_bytes()
    raw = (ROOT / LEDGER).read_bytes()
    write(PRIVATE / 'post-api-observed-ledger.private.raw.jsonl', raw)
    suffix = raw[len(prefix):] if raw.startswith(prefix) else b''
    write(PRIVATE / 'post-api-observed-append.exact.jsonl', suffix)
    dump(PRIVATE / 'API-observation.json', {
        'normal_api_was_attempted_once': True, 'ledger_starts_with_original_prefix': raw.startswith(prefix),
        'ledger': digest(ROOT / LEDGER), 'suffix_bytes': len(suffix), 'suffix_sha256': sha(suffix),
        'own_observed_state': replay(raw).get(ADV, {}).get('state'),
        'error': error, 'NEVER_REPLAY_API': True})

def closeout(grant_path):
    grant_check(grant_path)
    assert (PRIVATE / 'execution-attempted.json').exists()
    guard('after-api')
    raw = (PRIVATE / 'own-C-before.raw.json').read_bytes()
    current = (ROOT / CELL).read_bytes()
    assert current == raw
    # Preserve raw text for every existing field; replace only status and append
    # the permitted new evidence.integration_boundary field.
    text = raw.decode()
    decoder = json.JSONDecoder()
    def members(start):
        i = start
        while text[i].isspace(): i += 1
        assert text[i] == '{'
        i += 1
        result = {}
        while True:
            while text[i].isspace(): i += 1
            if text[i] == '}': return result, i
            key, end = decoder.raw_decode(text, i)
            i = end
            while text[i].isspace(): i += 1
            assert text[i] == ':'
            i += 1
            while text[i].isspace(): i += 1
            start_value = i
            _, end_value = decoder.raw_decode(text, i)
            result[key] = (start_value, end_value)
            i = end_value
            while text[i].isspace(): i += 1
            if text[i] == ',': i += 1
            else: assert text[i] == '}'
    top, _ = members(0)
    ev, ev_close = members(top['evidence'][0])
    assert 'integration_boundary' not in ev
    edits = [(top['status'][0], top['status'][1], json.dumps('independently_verified')),
             (ev_close, ev_close, ',"integration_boundary":' + json.dumps(BOUNDARY, ensure_ascii=False))]
    for start, end, value in sorted(edits, reverse=True):
        text = text[:start] + value + text[end:]
    wanted = copy.deepcopy(json.loads(raw))
    wanted['status'] = 'independently_verified'
    wanted['evidence']['integration_boundary'] = BOUNDARY
    assert json.loads(text) == wanted and wanted['owner_id'] == OWNER
    assert (ROOT / CELL).read_bytes() == raw
    temp = PRIVATE / 'own-C-two-field-closeout.pending.json'
    write(temp, text.encode())
    temp.chmod(stat.S_IMODE((ROOT / CELL).stat().st_mode))
    os.replace(temp, ROOT / CELL)
    result = guard('after-closeout')
    dump(PRIVATE / 'own-closeout-result.json', {'normal_API_calls': 1,
        'own_two_field_closeout_only': True, 'guard': result,
        'original_full_evidence_values_preserved': True,
        'future_post_integration_same_original_source_actor_only': ACTOR})

def execute(grant_path):
    grant_check(grant_path)
    guard('before')
    math_and_metadata_checks()
    evidence = load(PRIVATE / 'normal-VERIFIED-evidence.complete.json')
    assert evidence['verifier_id'] == ACTOR and evidence['verified_commit'] == CARRIER
    fd = os.open(PRIVATE / 'execution-attempted.json', os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(fd, 'w') as handle:
        json.dump({'actor': ACTOR, 'advance': ADV, 'carrier': CARRIER,
                   'stage': 'NORMAL_API_ABOUT_TO_BE_CALLED',
                   'permanent_no_replay_marker': True}, handle)
        handle.flush(); os.fsync(handle.fileno())
    try:
        # THE SINGLE NORMAL API CALL. Never replace this with a manual ledger append.
        advance.transition_advance(ADV, 'VERIFIED', worker_id=ACTOR,
            modes=['independent-source-review', 'native-evidence-verification', 'reader-verification'],
            evidence=evidence)
    except BaseException:
        observe_api_outcome(traceback.format_exc())
        raise
    observe_api_outcome()
    # If any later guard fails, the permanent marker and exact observed append
    # remain. Only readonly diagnosis / own closeout is permitted; NEVER replay.
    guard('after-api')
    closeout(grant_path)

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', nargs='?', default='preflight',
                        choices=['snapshot', 'prepare', 'preflight', 'execute', 'closeout'])
    parser.add_argument('--grant-file', type=Path)
    args = parser.parse_args()
    if args.command == 'snapshot': snapshot()
    elif args.command == 'prepare': prepare()
    elif args.command == 'preflight':
        print(json.dumps({'guard': guard('before'), 'metadata': math_and_metadata_checks(),
                          'API_executed': False}, indent=2))
    else:
        assert args.grant_file is not None, 'Explicit final execution grant file is mandatory'
        if args.command == 'execute': execute(args.grant_file)
        else: closeout(args.grant_file)

if __name__ == '__main__': main()
