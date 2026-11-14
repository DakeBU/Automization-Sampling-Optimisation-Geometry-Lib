#!/usr/bin/env python3
"""Perform the one explicitly authorized independent VERIFIED transition."""
from __future__ import annotations

import contextlib
import hashlib
import io
import json
import subprocess
import sys
import traceback
from datetime import datetime, timezone
from pathlib import Path

sys.dont_write_bytecode = True
ROOT = Path('/Users/zhouhuanjian/ASTIS-GC')
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / 'tools'))
from tools import astis_advance as api
from tools import astis_semantic_roundtrip_core as semantic

OUT = Path(__file__).resolve().parent
ADVANCE = 'ASTIS-SA-20261106-GaussianComplexityAveragedBlockLaw'
VERIFIER = '/root/eq6_fresh_source_module_review'
OWNER = 'huanjian_gc_20261106_eq6'
COMMIT = '98cc6c8953d38dd54bc4e4ef7a547fd68a381ac8'
DECL = ('AutoSamplingTheory.ExampleCases.GaussianComplexity.'
        'AveragedBlockLaw.actual_averaged_block_product')
LEDGER = ROOT / 'runs/substantive_advances.jsonl'
AUDIT = ROOT / 'research-wiki/semantic-roundtrip/audits/huanjian-averaged-block-law.json'
PREFIX_RECORD = OUT / 'verified-ledger-prefix.before.json'
PROTECTED_RECORD = OUT / 'verified-protected-inputs.before.json'
PROJECTION_RECORD = OUT / 'verified-projected-advances.before.json'
EVIDENCE_RECORD = OUT / 'verified-normal-api-evidence.json'
APPEND_RECORD = OUT / 'verified-ledger.exact-append.RAW.jsonl'
RECEIPT = OUT / 'verified-normal-api.receipt.json'
PROTECTION_RESULT = OUT / 'verified-protection-checks.json'
SUMMARY = OUT / 'verified-transition-summary.json'


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def canonical(value: object) -> str:
    return semantic.sha256_json(value)


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def write_new(path: Path, value: object) -> None:
    with path.open('x', encoding='utf-8', newline='\n') as handle:
        handle.write(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def pin(path: Path) -> dict:
    raw = path.read_bytes()
    return {'path': rel(path), 'physical_raw_sha256': sha(raw), 'bytes': len(raw)}


def git(*args: str) -> bytes:
    return subprocess.check_output(['git', *args], cwd=ROOT)


def protect() -> dict:
    groups = {
        'production_lean': sorted((ROOT / 'AutoSamplingTheory').rglob('*.lean')),
        'consumer_lean': sorted((ROOT / 'Tests').rglob('*.lean')),
        'frontier_cells': sorted((ROOT / 'research-wiki/frontier-cells').rglob('*.json')),
        'authored_lessons': sorted((ROOT / 'website/content/declaration_lessons').rglob('*.json')),
        'publications': sorted((ROOT / 'website/content/publications').rglob('*.json')),
        'semantic_audits': sorted((ROOT / 'research-wiki/semantic-roundtrip/audits').rglob('*.json')),
    }
    named = [
        'AutoSamplingTheory.lean', 'Tests.lean', 'lakefile.lean',
        'lean-toolchain', 'lake-manifest.json',
        'research-wiki/semantic-roundtrip/registry.json',
        'website/content/samplewiki_companion_frontiers.json',
        'website/content/samplewiki_frontier_audit.json',
        'website/content/samplewiki_example_cases.json',
        'runs/substantive_discoveries.jsonl',
        '.astis/huanjian-resume-20261103/2610.20492v1.html',
    ]
    groups['root_control_case_and_source'] = [ROOT / p for p in named if (ROOT / p).is_file()]
    manifest = {}
    for group, paths in groups.items():
        manifest[group] = {rel(p): pin(p) for p in paths if p.is_file()}
    return manifest


def project(raw: bytes) -> dict:
    assert raw.endswith(b'\n'), 'Refuse an interrupted/non-newline ledger tail.'
    rows = [json.loads(line) for line in raw.splitlines() if line.strip()]
    assert all(isinstance(row, dict) for row in rows)
    return api._replay_advances(rows)


def main() -> None:
    for path in [PREFIX_RECORD, PROTECTED_RECORD, PROJECTION_RECORD, EVIDENCE_RECORD,
                 APPEND_RECORD, RECEIPT, PROTECTION_RESULT, SUMMARY]:
        assert not path.exists(), f'Refuse to repeat this one-shot publication: {path}'
    assert git('rev-parse', 'HEAD').decode().strip() == COMMIT
    assert sha(AUDIT.read_bytes()) == '7f96a0c943f73010c9ef75b19070394a6037f80d769db52e66ab0ed09f1377da'
    assert not (OUT / 'FreshExpandedProbe.lean').exists()
    assert sha((OUT / 'FreshExpandedProbe.archived.txt').read_bytes()) == (
        '0ce0113c80dcf8a4d9428a78a4ceb5ef3bd37ab9e8305221533587d36b6a2ac7')

    # Exact existing prefix is already an immutable reachable Git blob. Preserve
    # its object reference and SHA256 before invoking any mutable API operation.
    before_raw = LEDGER.read_bytes()
    blob = git('rev-parse', f'{COMMIT}:runs/substantive_advances.jsonl').decode().strip()
    blob_raw = git('cat-file', 'blob', blob)
    assert before_raw == blob_raw, 'Current prefix must be the exact saved Git blob.'
    prefix = {
        'saved_at_utc': now(), 'ledger': rel(LEDGER),
        'preservation': 'exact immutable Git blob, reachable from checked commit; no redundant large copy',
        'git_commit': COMMIT, 'git_blob_oid': blob,
        'recovery_command': ['git', 'cat-file', 'blob', blob],
        'raw_prefix_sha256': sha(before_raw), 'raw_prefix_bytes': len(before_raw),
        'raw_prefix_line_count': len(before_raw.splitlines()),
        'git_blob_exact_byte_comparison': True,
    }
    write_new(PREFIX_RECORD, prefix)
    before = project(before_raw)
    assert len(before) == 276
    target_before = before[ADVANCE]
    assert target_before['state'] == 'PROVED_LOCAL'
    assert target_before['owner_id'] == OWNER
    assert target_before['publication_declarations'] == [DECL]
    other_before = {k: v for k, v in before.items() if k != ADVANCE}
    assert len(other_before) == 275
    write_new(PROJECTION_RECORD, {
        'source_prefix': pin(PREFIX_RECORD),
        'projection_implementation': 'tools.astis_advance._replay_advances, the same projection used by the normal API',
        'advance_count': len(before), 'other_advance_count': len(other_before),
        'all_other_projected_objects_canonical_sha256': canonical(other_before),
        'other_projected_objects': {
            k: {'canonical_sha256': canonical(v), 'state': v.get('state')}
            for k, v in sorted(other_before.items())
        },
        'target': {'advance_id': ADVANCE, 'state': target_before['state'],
                   'owner_id': target_before['owner_id'], 'publication_declarations': [DECL],
                   'canonical_sha256': canonical(target_before)},
    })
    protected_before = protect()
    write_new(PROTECTED_RECORD, protected_before)

    # All gate claims here come from this verifier's previously executed checks.
    report_path = OUT / 'fresh-wholemodule-parent-reader-review.json'
    report = json.loads(report_path.read_text())
    assert report['blocking_findings'] == 0
    assert report['checked_commit'] == COMMIT
    assert report['fidelity_verdict'] == 'equivalent-after-elaboration'
    assert sha(report_path.read_bytes()) == '021beec31dedd613aeeb76fa299ff79eb46d84b20ef27800f07bcdbfcad4be99'
    audit = json.loads(AUDIT.read_text())
    assert audit['source_review']['state'] == 'accepted'
    assert audit['source_review']['review_run_sha256'] == '0776e427c8956dd926e32cd282714b0f1922cc3019dfcd92b103737f71972e1b'
    assert semantic.semantic_reviewer_packet(audit)['packet_sha256'] == '90fe267ec15537e216b458a39dc7d671468cf004cf82e45aa76f4c6b49695a8e'
    checks = {}
    for label in ['fresh-focused-build', 'fresh-direct-production',
                  'fresh-direct-consumer', 'fresh-expanded-probe']:
        path = OUT / (label + '.receipt.json')
        receipt = json.loads(path.read_text())
        assert receipt['exit_code'] == 0
        checks[label] = {'receipt': pin(path), 'command': receipt['command'],
                         'exit_code': 0, 'stdout_sha256': receipt['stdout_sha256'],
                         'execution_kind': ('successful cache replay' if label == 'fresh-focused-build'
                                            else 'actual direct current-source Lean elaboration')}
    evidence = {
        'verifier_id': VERIFIER, 'verified_commit': COMMIT,
        'gate': {
            'status': 'PASS',
            'scope': 'bounded Eq6 focused/direct Lean, independent source and whole-module/parent checks, static reader; not root/global/integration gate',
            'actual_checks': checks,
            'normal_api_publication_admission': {
                'method': 'transition_advance calls check_advance(publication_declarations, reviewed=True) before its append',
                'publication_binding_sha256': audit['publication_binding_sha256'],
            },
        },
        'source_audit': {
            'status': 'accepted',
            'raw_source_prefreeze': pin(OUT / 'raw-source-prefreeze.json'),
            'seven_slot_prefreeze': pin(OUT / 'source-vs-reconstruction-seven-slot-freeze.json'),
            'wholemodule_parent_static_reader_report': pin(report_path),
            'raw_source_sha256': '6bc5ddc1e19cea9ba1dfe862fa79bc69fe861dff045d6ad1c7baa4a113c37915',
            'scope': 'actual Eq6 law and only its probability/positive-support elaboration; downstream Ex70/71/72 and main lower bounds excluded',
        },
        'semantic_audit': {
            'audit_id': audit['id'], 'fragment': pin(AUDIT),
            'fidelity_verdict': audit['verdict'], 'source_review_state': 'accepted',
            'canonical_reviewer_packet_sha256': audit['source_review']['reviewer_packet_sha256'],
            'review_run_canonical_sha256': audit['source_review']['review_run_sha256'],
            'run_record': pin(OUT / 'fresh-review-run.json'),
            'result': pin(OUT / 'fresh-source-review-result.json'),
        },
        'fake_closure_scan': {
            'status': 'PASS', 'report': pin(report_path),
            'forbidden_closure_hits': 0,
            'axiom_evidence': pin(OUT / 'fresh-expanded-probe.stdout.RAW'),
            'actual_axioms_anchor_and_six_parent_specs': ['propext', 'Classical.choice', 'Quot.sound'],
            'scope': 'reviewed exact module and actual used parent specifications; no sorryAx or added mathematical axiom',
        },
        'publication_declarations': [DECL],
        'truth_boundary': {
            'verified': 'exact checked-commit bounded Eq6 theorem/source/wholemodule/parent/staticreader and actual focused/direct Lean evidence',
            'not_claimed': ['root9638', 'Registry integration', 'browser/layout', 'graph integration',
                            'remote/live publication', 'MERGED', 'PURIFIED', 'Exposition Seal',
                            'main acceptance', 'main lower bounds', 'whole-Goal completion'],
        },
        'preserved_ledger_prefix': pin(PREFIX_RECORD),
        'independent_reviewer_id': VERIFIER,
    }
    write_new(EVIDENCE_RECORD, evidence)
    assert LEDGER.read_bytes() == before_raw
    assert protect() == protected_before

    stdout, stderr = io.StringIO(), io.StringIO()
    started = now()
    error = None
    try:
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            # The sole mutation of repository truth in this script. No patched
            # validator, copied event or private append primitive is used.
            api.transition_advance(
                ADVANCE, 'VERIFIED', worker_id=VERIFIER,
                modes=['independent-verification'], evidence=evidence,
                path=LEDGER,
            )
    except Exception:
        error = traceback.format_exc()
        stderr.write(error)
    stdout_raw, stderr_raw = stdout.getvalue().encode(), stderr.getvalue().encode()
    (OUT / 'verified-normal-api.stdout.RAW').write_bytes(stdout_raw)
    (OUT / 'verified-normal-api.stderr.RAW').write_bytes(stderr_raw)
    write_new(RECEIPT, {
        'script': pin(Path(__file__).resolve()), 'api': 'tools.astis_advance.transition_advance',
        'started_at_utc': started, 'finished_at_utc': now(),
        'advance_id': ADVANCE, 'from_state': 'PROVED_LOCAL', 'to_state': 'VERIFIED',
        'worker_id': VERIFIER, 'verified_commit': COMMIT,
        'exit_code': 1 if error else 0,
        'stdout_sha256': sha(stdout_raw), 'stderr_sha256': sha(stderr_raw),
        'normal_api_reviewed_publication_gate_passed': error is None,
        'evidence': pin(EVIDENCE_RECORD), 'error': error,
    })
    if error:
        raise RuntimeError('Normal API rejected the authorized transition; inspect preserved receipt.')

    after_raw = LEDGER.read_bytes()
    assert after_raw.startswith(before_raw), 'Historical ledger bytes changed.'
    tail = after_raw[len(before_raw):]
    assert tail.endswith(b'\n') and len(tail.splitlines()) == 1
    event = json.loads(tail)
    assert event['event'] == 'transition'
    assert event['advance_id'] == ADVANCE
    assert event['from_state'] == 'PROVED_LOCAL' and event['to_state'] == 'VERIFIED'
    assert event['worker_id'] == VERIFIER and event['evidence'] == evidence
    with APPEND_RECORD.open('xb') as handle:
        handle.write(tail)
    after = project(after_raw)
    assert set(after) == set(before)
    assert {k: v for k, v in after.items() if k != ADVANCE} == other_before
    assert after[ADVANCE]['state'] == 'VERIFIED'
    assert after[ADVANCE]['owner_id'] == OWNER
    assert after[ADVANCE]['latest_evidence']['verifier_id'] == VERIFIER
    protected_after = protect()
    assert protected_after == protected_before
    checks_result = {
        'checked_at_utc': now(),
        'prefix_before': pin(PREFIX_RECORD),
        'exact_original_prefix_preserved': True,
        'original_prefix_sha256': sha(before_raw), 'original_prefix_bytes': len(before_raw),
        'after_ledger_sha256': sha(after_raw), 'after_ledger_bytes': len(after_raw),
        'exactly_one_appended_jsonl_event': True, 'exact_append': pin(APPEND_RECORD),
        'all_275_other_full_projected_objects_identical': True,
        'other_projection_before_and_after_canonical_sha256': canonical(other_before),
        'protected_manifest': pin(PROTECTED_RECORD),
        'protected_before_and_after_canonical_sha256': canonical(protected_before),
        'protected_counts_by_group': {k: len(v) for k, v in protected_before.items()},
        'all_protected_raw_bytes_and_file_sets_identical': True,
        'changed_protected_files': [], 'owner_preserved': OWNER,
        'source_tests_lessons_publications_audits_frontiers_cases_roots_registry_unchanged': True,
        'declared_concurrent_metadata_outside_protection': 'coordinator remote-readonly-readback and integration-reader reports; no blanket evidence-directory freeze',
    }
    write_new(PROTECTION_RESULT, checks_result)
    summary = {
        'advance_id': ADVANCE, 'state': after[ADVANCE]['state'],
        'proving_owner': OWNER, 'verifier_id': VERIFIER, 'verified_commit': COMMIT,
        'normal_api_receipt': pin(RECEIPT), 'exact_append': pin(APPEND_RECORD),
        'protection_checks': pin(PROTECTION_RESULT),
        'reviewed_publication_binding_sha256': audit['publication_binding_sha256'],
        'scope': evidence['truth_boundary'],
        'all_other_275_projected_states_identical': True,
        'all_protected_content_identical': True,
        'frontier_or_integration_state_written': False,
    }
    write_new(SUMMARY, summary)
    print(json.dumps({'summary': pin(SUMMARY), **summary}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
