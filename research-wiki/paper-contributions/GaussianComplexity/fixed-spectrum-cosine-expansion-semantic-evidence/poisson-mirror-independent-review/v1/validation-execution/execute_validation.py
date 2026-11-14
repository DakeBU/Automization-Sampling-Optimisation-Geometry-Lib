"""One authorized normal conceptual-Discovery validation; no manual ledger writes."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import sys

ROOT = Path('/Users/zhouhuanjian/ASTIS-GC')
OUT = Path(__file__).resolve().parent
REVIEW = OUT.parent
DISCOVERY_ID = 'ASTIS-DISC-20261109-GaussianComplexityPoissonCosineMirror'
ACTOR = '/root/cosine_topology_challenge'
LEDGER = ROOT / 'runs/substantive_discoveries.jsonl'
CANDIDATE = ROOT / 'research-wiki/paper-contributions/GaussianComplexity/fixed-spectrum-cosine-expansion-semantic-evidence/poisson-cosine-mirror-candidate-v1.json'
SOURCE = ROOT / '.astis/huanjian-resume-20261103/2610.20492v1.html'
CANDIDATE_SHA = 'bcd24a72d1409f6b0b6747d85116d3317cb51c0d0612d5789d0affd5b317cd1e'
FREEZE_SHA = '89ef036a8295a1f513f981fe789013fb1c48f29ce13f664d476040d478810f4b'
SOURCE_SHA = '6bc5ddc1e19cea9ba1dfe862fa79bc69fe861dff045d6ad1c7baa4a113c37915'


def sha(data):
    return hashlib.sha256(data).hexdigest()


def save(name, value):
    (OUT / name).write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + '\n')


def pins():
    assert sha(CANDIDATE.read_bytes()) == CANDIDATE_SHA
    assert sha((REVIEW / 'SHA256SUMS').read_bytes()) == FREEZE_SHA
    for line in (REVIEW / 'SHA256SUMS').read_text().splitlines():
        expected, name = line.split('  ', 1)
        assert sha((REVIEW / name).read_bytes()) == expected, name
    raw_source = SOURCE.read_bytes()
    assert len(raw_source) == 951991 and sha(raw_source) == SOURCE_SHA
    return json.loads(CANDIDATE.read_text())


def strict_replay(raw):
    assert raw and raw.endswith(b'\n'), 'Incomplete/non-newline tail: STOP, no recovery.'
    records = [json.loads(line) for line in raw.splitlines() if line.strip()]
    assert all(isinstance(r, dict) for r in records)
    from tools import astis_advance
    return records, astis_advance._replay_discoveries(records)


def protected():
    paths = {
        ROOT / 'README.md', ROOT / 'runs/substantive_advances.jsonl', SOURCE, CANDIDATE,
        ROOT / 'website/content/graph_memory_index.json',
        ROOT / 'website/content/functor_hypergraph.json',
        ROOT / 'Libraries/frontloaded-shared-spine.json',
        ROOT / 'Libraries/conceptual-mirror-protocol.json',
        ROOT / 'docs/conceptual-mirror-protocol.md',
        ROOT / 'tools/astis_advance.py', ROOT / 'tools/astis_harness.py',
        ROOT / 'Tests/GaussianComplexityFixedSpectrumCosineExpansion.lean',
        ROOT / 'Tests/GaussianComplexitySphericalPoisson.lean',
        REVIEW / 'review.md', REVIEW / 'input-manifest.json',
        REVIEW / 'spherical-poisson-signature.txt', REVIEW / 'SHA256SUMS',
    }
    # These two bounded directory inventories protect shared frontiers and the
    # relevant paper sources; no repository-wide scan or semantic source read.
    paths.update((ROOT / 'research-wiki/frontier-cells').glob('*.json'))
    paths.update((ROOT / 'AutoSamplingTheory/ExampleCases/GaussianComplexity').glob('*.lean'))
    return {
        str(p.relative_to(ROOT)): {'bytes': p.stat().st_size, 'sha256': sha(p.read_bytes())}
        for p in sorted(paths)
    }


def own_and_foreign(states, candidate, expected_status):
    assert len(states) == 40, 'Unexpected total Discovery state count: STOP.'
    own = states[DISCOVERY_ID]
    assert own['status'] == expected_status and own['kind'] == 'conceptual-mirror'
    assert own['metadata'] == candidate['metadata'], 'Candidate metadata drift: STOP.'
    assert own['created_by'] != ACTOR, 'Creator cannot self-validate.'
    foreign = {k: v for k, v in states.items() if k != DISCOVERY_ID}
    assert len(foreign) == 39
    return own, foreign


def main(mode):
    candidate = pins()
    if mode == 'prepare':
        assert not (OUT / 'before-receipt.json').exists(), 'Existing preparation: STOP.'
        raw = LEDGER.read_bytes()
        records, states = strict_replay(raw)
        own, foreign = own_and_foreign(states, candidate, 'raw')
        (OUT / 'discovery-ledger.before.jsonl').write_bytes(raw)
        save('own-state.before.json', own)
        save('foreign39-states.before.json', foreign)
        save('protected-files.before.json', protected())
        save('before-receipt.json', {
            'run': 'POISSON-COSINE-MIRROR-NORMAL-VALIDATION-20261109-v1',
            'time_utc': datetime.now(timezone.utc).isoformat(),
            'discovery_id': DISCOVERY_ID, 'actor': ACTOR,
            'ledger_bytes': len(raw), 'ledger_sha256': sha(raw),
            'complete_records': len(records), 'discovery_states': len(states),
            'foreign_states': len(foreign), 'own_status': own['status'],
            'created_by': own['created_by'], 'metadata_exactly_matches_candidate': True,
            'candidate_sha256': CANDIDATE_SHA, 'review_freeze_sha256': FREEZE_SHA,
            'raw_source_sha256': SOURCE_SHA, 'pure_replay_no_recovery_called': True,
        })
        print(json.dumps({'prepared': True, 'status': own['status'], 'foreign_states': 39,
                          'ledger_bytes': len(raw), 'ledger_sha256': sha(raw),
                          'protected_files': len(protected())}))
        return
    assert mode == 'apply'
    assert not (OUT / 'api-invocation-intent.json').exists(), 'Prior API attempt: STOP; no retry.'
    before = (OUT / 'discovery-ledger.before.jsonl').read_bytes()
    assert LEDGER.read_bytes() == before, 'Ledger changed after preflight: STOP.'
    records_before, states_before = strict_replay(before)
    own_before, foreign_before = own_and_foreign(states_before, candidate, 'raw')
    assert protected() == json.loads((OUT / 'protected-files.before.json').read_text()), 'Protected-file drift: STOP.'
    note = (
        'Independent exact-content ACCEPT_CONCEPTUAL_ONLY by ' + ACTOR + '. '
        'Candidate sha256=' + CANDIDATE_SHA + '; '
        'review.md sha256=f2713fe98f49dab01172ca70b0a7489e2fa5fc93714239318d583f3eb5931c7d; '
        'review SHA256SUMS sha256=' + FREEZE_SHA + '; raw source sha256=' + SOURCE_SHA + '. '
        'Source-backed conceptual interpretation only; no Lean implication or formal transport certificate, '
        'no source-V/old-source-audit upgrade or Goal credit. Preserve all reviewed failure boundaries: '
        + candidate['metadata']['failure_boundary'] + ' '
        'Auxiliary circle dimension2, negative-pole rotation and angular/surface-measure adapters remain uncertified; '
        'raw A1 moments require normalization by 1-r^2. No compiled-use or new theorem certification. '
        'Review/input manifest: .astis/huanjian-gc-fixed-spectrum-moments-20261109/'
        'poisson-mirror-independent-review/v1/review.md and input-manifest.json.'
    )
    save('api-invocation-intent.json', {'api': 'tools.astis_advance.transition_discovery',
         'discovery_id': DISCOVERY_ID, 'to_status': 'validated', 'actor': ACTOR, 'note': note,
         'authorized_calls': 1, 'manual_ledger_append': False})
    from tools import astis_advance
    astis_advance.transition_discovery(DISCOVERY_ID, 'validated', actor=ACTOR, note=note)
    after = LEDGER.read_bytes()
    assert after.startswith(before), 'Original ledger byte prefix changed.'
    appended = after[len(before):]
    assert appended.endswith(b'\n') and len(appended.splitlines()) == 1, 'Not exactly one append.'
    event = json.loads(appended)
    assert event['event'] == 'discovery_transition' and event['discovery_id'] == DISCOVERY_ID
    assert event['from_status'] == 'raw' and event['to_status'] == 'validated'
    assert event['actor'] == ACTOR and event['note'] == note
    records_after, states_after = strict_replay(after)
    assert len(records_after) == len(records_before) + 1
    own_after, foreign_after = own_and_foreign(states_after, candidate, 'validated')
    assert foreign_after == foreign_before, 'Foreign Discovery state changed.'
    allowed_own_changes = {'status', 'updated_at', 'latest_note', 'latest_actor'}
    assert {k: v for k, v in own_before.items() if k not in allowed_own_changes} == {
        k: v for k, v in own_after.items() if k not in allowed_own_changes}
    assert own_after['latest_actor'] == ACTOR
    assert protected() == json.loads((OUT / 'protected-files.before.json').read_text())
    (OUT / 'append.jsonl').write_bytes(appended)
    save('own-state.after.json', own_after)
    save('foreign39-states.after.json', foreign_after)
    save('protected-files.after.json', protected())
    save('execution-receipt.json', {
        'time_utc': datetime.now(timezone.utc).isoformat(), 'result': 'VALIDATED_CONCEPTUAL_ONLY',
        'discovery_id': DISCOVERY_ID, 'actor': ACTOR, 'api_calls': 1,
        'api_returned_normally': True, 'manual_ledger_append': False,
        'before_bytes': len(before), 'before_sha256': sha(before),
        'after_bytes': len(after), 'after_sha256': sha(after),
        'append_bytes': len(appended), 'append_sha256': sha(appended), 'appended_records': 1,
        'original_raw_prefix_unchanged': True, 'foreign39_states_unchanged': True,
        'own_metadata_unchanged': True, 'own_status': own_after['status'],
        'protected_files_unchanged': True, 'protected_file_count': len(protected()),
        'no_tail_repair': after.startswith(before) and before.endswith(b'\n'),
        'source_V_or_Lean_or_Goal_credit': False,
    })
    print(json.dumps({'result': 'validated', 'actor': ACTOR, 'append_records': 1,
                      'foreign39_unchanged': True, 'protected_files_unchanged': True,
                      'after_sha256': sha(after)}))


if __name__ == '__main__':
    sys.path.insert(0, str(ROOT))
    main(sys.argv[1])
