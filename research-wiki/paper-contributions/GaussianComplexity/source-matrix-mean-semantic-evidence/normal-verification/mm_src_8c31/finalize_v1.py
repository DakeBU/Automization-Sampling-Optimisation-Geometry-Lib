#!/usr/bin/env python3
"""Seal the already completed, single-call normal verification. Never call API."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import os
import subprocess
import sys
import tarfile

sys.dont_write_bytecode = True
ROOT = Path('/Users/zhouhuanjian/ASTIS-GC')
E = ROOT / 'research-wiki/paper-contributions/GaussianComplexity/source-matrix-mean-semantic-evidence'
OUT = Path(__file__).resolve().parent
sys.path.insert(0, str(OUT))
from verification_v1 import ACTOR, ADV, HEAD, MATH, CELL, DECISION, OWNER, source_preservation


def sha(b):
    return hashlib.sha256(b).hexdigest()


def dump(path, value):
    assert not path.exists(), f'Preserve an existing original: {path}'
    path.write_text(json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + '\n')


def identity(path):
    b = path.read_bytes()
    return {'path': str(path.relative_to(ROOT)), 'bytes': len(b), 'sha256': sha(b)}


def main():
    api = json.loads((OUT / 'normal-VERIFIED-API-original-v2.receipt.json').read_text())
    pre = json.loads((OUT / 'precheck-wrapper-v1.receipt.json').read_text())
    post = json.loads((OUT / 'postcheck-wrapper-v1.receipt.json').read_text())
    proof = json.loads((OUT / 'preservation-readback-v1.json').read_text())
    outcome = json.loads((OUT / 'actual-outcome-before-any-further-action-v1.json').read_text())
    assert api['exit_code'] == pre['exit_code'] == post['exit_code'] == 0
    assert proof['status'] == 'PASS' and outcome['state'] == 'VERIFIED'
    original = json.loads((OUT / 'PROVED_LOCAL-original-evidence.full.json').read_text())
    payload = json.loads((OUT / 'actual-VERIFIED-evidence.full.json').read_text())
    assert len(original) == 20 and all(payload[k] == original[k] for k in original)
    event = json.loads((OUT / 'actual-VERIFIED-append.exact.jsonl').read_text())
    assert event['evidence'] == payload and event['worker_id'] == ACTOR
    assert subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT).decode().strip() == HEAD
    preserved = source_preservation()
    native_report = json.loads((OUT / 'inputs/native/report.json').read_text())
    checks = json.loads((OUT / 'precheck-v1.json').read_text())
    decision = {
        'kind': 'Actual independent normal VERIFIED decision and readback',
        'advance_id': ADV, 'verifier_id': ACTOR, 'owner_id_unchanged': OWNER,
        'decision': 'ACCEPT bounded normal VERIFIED',
        'normal_transition_advance_calls': 1, 'normal_API_exit_code': api['exit_code'],
        'actual_ledger_state': 'VERIFIED', 'actual_from_state': 'PROVED_LOCAL',
        'actual_normal_append': identity(OUT / 'actual-VERIFIED-append.exact.jsonl'),
        'actual_full_VERIFIED_evidence': identity(OUT / 'actual-VERIFIED-evidence.full.json'),
        'original_PROVED_LOCAL_payload_raw': identity(OUT / 'PROVED_LOCAL-original-evidence.full.json'),
        'original_PROVED_LOCAL_all20fields_inline_unchanged': True,
        'compiled_and_source_reviewed_math_candidate': MATH,
        'held_metadata_HEAD_pre_post': HEAD,
        'later_metadata_HEAD_recompile_claimed': False,
        'source_audit': payload['source_audit'],
        'native_review': {'report': identity(OUT / 'inputs/native/report.json'),
                          'verdict': native_report['verdict'], 'fresh_modules': 7,
                          'full_closed_types_and_bodies': 39, 'root_reachable': 32,
                          'older_generated_outside_retained': 7, 'new_owned_all_reachable': 3,
                          'allowed_axioms': ['propext', 'Classical.choice', 'Quot.sound'],
                          'literal_root_applications': 2, 'root_original_probe_replayed': True,
                          'portable_archive_payload': 440, 'portable_archive_members': 441,
                          'own_receipts': 109, 'all_receipts_including_history': 114,
                          'normal_verifier_stream_hashed_large_local_dump_not_exported': checks['checks']['large_native_local_dump']},
        'relevant_input_binding': {'actual_inputs_equal': 50, 'tracked_candidate_to_hold_HEAD_equal': 48,
                                   'pinned_local_equal': 2, 'actual_packages_equal_and_clean': 9,
                                   'actual_binary_equal': True},
        'four_actual_final_gates_exit0_at_hold_HEAD': checks['checks']['final_gates'],
        'pre_frontier_exit': 0, 'post_frontier_exit': 0,
        'preservation': proof, 'source_originals': preserved,
        'only_cell_fields_changed': ['status', 'evidence.independent_verification'],
        'failures': {'this_normal_verification': [], 'precheck_exit': 0, 'API_exit': 0,
                     'outcome_and_cell_exit': 0, 'postcheck_exit': 0,
                     'producer_original_firstbuild_exit': 0,
                     'consumer_historical_attempt_exits': [1, 1, 0], 'strict_original_probe_exit': 0,
                     'native_verifier_failures_retained': native_report['receipts'],
                     'source_v1_schema_failure_and_v2_core_correction_retained': True,
                     'original_payload_failure_labels_and_formalizer_preseal_API_pristine_false_unchanged': True},
        'permission_boundary': {'owner_release': False, 'integration': False, 'Git_commit_or_push': False,
                                'overall_Goal_completion': False, 'public_delivery': False, 'purification': False,
                                'browser_mobile_MathJax_runtime': False},
        'next_action': 'Return originals to coordinator; stabilization and public-reader/purification work remain with the authorized owner after release. Do not replay successful normal API.',
        'artifacts_directory': str(OUT.relative_to(ROOT)),
    }
    local_decision = OUT / 'actual-VERIFIED-independent-decision.json'
    dump(local_decision, decision)
    assert not DECISION.exists()
    DECISION.write_bytes(local_decision.read_bytes())
    assert json.loads(CELL.read_text())['evidence']['independent_verification'] == str(DECISION.relative_to(ROOT))
    dump(OUT / 'authorization-and-exposure-v1.json', {
        'actor': ACTOR, 'new_role_authorization': 'Independent normal VERIFIED task only after own final checks accepted',
        'held_metadata_HEAD': HEAD, 'math_candidate': MATH,
        'normal_API_limit': 1, 'normal_API_calls_actual': 1,
        'allowed_canonical_mutations': ['one normal ledger append', 'C.status', 'C.evidence.independent_verification'],
        'new_exposures': ['Owned C complete current metadata, after immutable source review',
                          'Independent native report/seal/portable archive and actual relevant-input binding',
                          'Four final gate original receipts/logs', 'Own original PROVED_LOCAL event/full20field payload',
                          'Canonical transition/readback and frontier checker implementation',
                          'Complete foreign/discovery states only in memory for digests and preservation',
                          'All tracked file bytes/modes only for streamed digests',
                          'Current actual local main and origin/main refs'],
        'no_full_foreign_control_private_snapshots_exported': True,
        'native_816509484_byte_dump_stream_hashed_not_exported': True,
        'source_v1_v2_packages_kept_original': True,
        'no_registry_source_shared_site_Git_or_owner_release_write': True,
        'no_new_native_compile_or_browser_claim': True,
    })
    dump(OUT / 'version-and-failure-diagnosis-v1.json', {
        'verification_v1.py': 'Executed precheck/readback-and-cell/postcheck, all exit0; immutable script receipt hashes retained.',
        'invoke_VERIFIED_once_v1.py': 'Preserved initial unexecuted wrapper; no API call and no failure attributed.',
        'invoke_VERIFIED_once_v2.py': 'Before any call, added full immediate hold-state comparison. Executed exactly once, exit0.',
        'this_normal_verification_failed_invocations': [],
        'successful_API_never_replayed': True,
        'historical_formalizer_and_native_failures': 'Retained in original20fields and original native archive/report, never relabeled or erased.',
        'source_schema_v1_failure': 'Original minimum-schema claim and true-core evidence-key correction v2 retained unchanged in complete source originals.',
    })
    input_entries = []
    for p in sorted((OUT / 'inputs').rglob('*')):
        if p.is_file():
            input_entries.append(identity(p))
    input_entries += [identity(OUT / 'PROVED_LOCAL-original-append.exact.jsonl'),
                      identity(OUT / 'PROVED_LOCAL-original-evidence.full.json')]
    dump(OUT / 'input-manifest-v1.json', {'kind': 'Actual exact normal-verification inputs',
        'candidate': MATH, 'metadata_HEAD': HEAD, 'exact_input_count': len(input_entries), 'entries': input_entries,
        'foreign_control_preservation': 'digest-only, never full snapshots',
        'native_large_dump': 'local-only stream-hashed; omitted from portable inputs',
        'normal_API_evidence_original20fields': 'Copied as original raw bytes and additionally all20fields inline unchanged in VERIFIED evidence'})
    report = f'''# Independent normal VERIFIED result

`{ADV}` is actually **VERIFIED** by `{ACTOR}` through one normal `transition_advance` call, exit 0. The actual ledger append was read back before the two authorized C-field changes. The successful API was never replayed.

Mathematical/native candidate: `{MATH}`. Held metadata HEAD: `{HEAD}`, unchanged. No fresh compile credit is assigned to the later metadata HEAD. The independent source v2 review and the native 7-module/39-full-closed-type-and-body review are accepted in their recorded bounded scopes. All 50 relevant inputs, the actual binary and all 9 clean package revisions match. The 816509484-byte local full-body dump was independently stream-hashed and is not exported.

The four original final gates at the held HEAD were exit 0. This verifier's actual precheck, pre-frontier, normal API, outcome/readback, post-frontier and postcheck all returned exit 0. Own normal-verification failures: none. The original producer first build 0, consumer historical 1/1/0, strict probe 0, native verifier/probe/preparer failures and the source v1 schema correction remain in their original records and labels.

Actual physical inventory is **468 regular frontier files**, comprising this C and **467 other files including README**, rather than the checker's 464 registered-cell count. All 307 foreign advances' complete states, all 43 discoveries' complete states and raw bytes, the entire advance-ledger prior raw prefix, all other frontier file bytes/modes, and all other tracked bytes/modes are unchanged. The tracked inventory contains 130418 files; only the permitted C and the single-append advance ledger changed bytes, with their modes/index identities preserved. HEAD and actual refs remain local main `a7cc97fc2376896ad6a666b87ca611dc4b815a49` and origin/main `4db0f863340a1710446c86a6e9db1994cd8bceb3`.

The original source v1 package's 67 files and v2 package's 78 files remain byte-identical. The original 20 PROVED_LOCAL payload fields are all inline, unchanged, in the actual VERIFIED payload, with the original raw payload/append separately preserved. Only C.status and its existing evidence.independent_verification changed; every other C field and byte outside those textual substitutions is unchanged.

The full normal API stdout/stderr/receipt, exact actual append/full payload, scripts, inputs, exposures, pre/post digest-only preservation and independent decision are carried by this package. No full foreign/control/private snapshot is exported. See the portable manifest and external seal for exact file counts and hashes.

No owner release, stabilization, Git commit/push, registry/source/shared/site modification, integration, whole Goal completion, browser/mobile/MathJax runtime, public delivery or purification is authorized or credited. Return originals to the coordinator and leave remaining integration/reader work with its authorized owner. Do not replay the successful API.
'''
    (OUT / 'report.md').write_text(report)
    dump(OUT / 'final-readback-v1.json', {
        'HEAD': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT).decode().strip(),
        'actual_normal_API_exit': 0, 'normal_calls': 1, 'actual_V_append': identity(OUT / 'actual-VERIFIED-append.exact.jsonl'),
        'full_payload': identity(OUT / 'actual-VERIFIED-evidence.full.json'),
        'canonical_decision': identity(DECISION), 'canonical_decision_equal_original': DECISION.read_bytes() == local_decision.read_bytes(),
        'source_v1_v2_originals_again': source_preservation(),
        'tracked_paths_changed': subprocess.check_output(['git', 'diff', '--name-only'], cwd=ROOT).decode().splitlines(),
        'no_more_API_actions': True,
    })
    excluded_root_outputs = {OUT / 'portable-manifest.json', OUT / 'final-seal.json',
                             OUT / 'mm_src_8c31-normal-verification-portable.tar.gz'}
    payload_files = sorted(p for p in OUT.rglob('*') if p.is_file() and p not in excluded_root_outputs)
    entries = [{'path': str(p.relative_to(OUT)), 'source': str(p.relative_to(ROOT)),
                'destination': str(p.relative_to(ROOT)), 'bytes': p.stat().st_size,
                'sha256': sha(p.read_bytes())} for p in payload_files]
    manifest = {'schema_version': 1, 'actor': ACTOR, 'math_candidate': MATH, 'held_metadata_HEAD': HEAD,
                'exact_count': len(entries), 'payload_file_count': len(entries),
                'manifest_destination': str((OUT / 'portable-manifest.json').relative_to(ROOT)),
                'manifest_not_self_hashed': True, 'archive_member_count_expected': len(entries) + 1,
                'entries': entries, 'external_seal': 'final-seal.json',
                'privacy': 'Complete foreign states/ledgers/frontier/private tracked bytes preserved by digests only; no full snapshots.',
                'native_dump_and_oleans_excluded': True}
    dump(OUT / 'portable-manifest.json', manifest)
    archive_path = OUT / 'mm_src_8c31-normal-verification-portable.tar.gz'
    assert not archive_path.exists()
    with tarfile.open(archive_path, 'w:gz') as archive:
        for p in payload_files + [OUT / 'portable-manifest.json']:
            archive.add(p, arcname=str(p.relative_to(OUT)), recursive=False)
    expected = {e['path']: e for e in entries}
    with tarfile.open(archive_path, 'r:gz') as archive:
        members = archive.getmembers()
        assert len(members) == len(entries) + 1
        for member in members:
            b = archive.extractfile(member).read()
            if member.name == 'portable-manifest.json':
                assert b == (OUT / 'portable-manifest.json').read_bytes()
            else:
                assert len(b) == expected[member.name]['bytes'] and sha(b) == expected[member.name]['sha256']
    for entry in entries:
        p = OUT / entry['path']
        assert p.stat().st_size == entry['bytes'] and sha(p.read_bytes()) == entry['sha256']
    seal = {'actor': ACTOR, 'advance_id': ADV, 'actual_normal_VERIFIED': True,
            'normal_API_calls': 1, 'normal_API_exit': 0, 'precheck_exit': 0, 'postcheck_exit': 0,
            'pre_frontier_exit': 0, 'post_frontier_exit': 0,
            'math_candidate': MATH, 'held_metadata_HEAD': HEAD,
            'payload_file_count': len(entries), 'archive_member_count': len(entries) + 1,
            'physical_directory_file_count_with_manifest_archive_seal': len(entries) + 3,
            'raw_hashes': {p.name: identity(p) for p in [local_decision, OUT / 'report.md',
                OUT / 'portable-manifest.json', archive_path, OUT / 'actual-VERIFIED-append.exact.jsonl',
                OUT / 'actual-VERIFIED-evidence.full.json', OUT / 'preservation-readback-v1.json']},
            'source_v1_v2_original_bytes_preserved': True,
            'no_circular_self_hash': True, 'owner_release_or_integration_permission': False,
            'public_delivery_or_purification_credit': False}
    dump(OUT / 'final-seal.json', seal)
    assert len([p for p in OUT.rglob('*') if p.is_file()]) == len(entries) + 3
    print(json.dumps({'payload_exact_count': len(entries), 'archive_members': len(entries) + 1,
                      'physical_files': len(entries) + 3,
                      'decision': identity(local_decision), 'manifest': identity(OUT / 'portable-manifest.json'),
                      'archive': identity(archive_path), 'seal': identity(OUT / 'final-seal.json')}, ensure_ascii=False))


if __name__ == '__main__':
    main()
