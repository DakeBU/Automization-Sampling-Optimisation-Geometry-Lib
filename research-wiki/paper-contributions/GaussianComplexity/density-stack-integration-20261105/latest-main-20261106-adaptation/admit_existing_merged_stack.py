"""Publish only normal integration transitions for the already merged stack.

No VERIFIED transition, mathematical proof, foreign state change or ledger reset.
"""
from pathlib import Path
import hashlib
import json
import subprocess
import sys

ROOT = Path.cwd()
sys.path.insert(0, str(ROOT))
from tools import astis_advance as advance
from tools import astis_publication as publication
from tools import astis_site

OUT = Path(__file__).resolve().parent
MERGE = '994992ba220c1e7080eb184b1de662e857b9ff1c'
LATEST = '0804c29747e334f1d6175f6494135be4b164de80'
ACTOR = 'huanjian_gc_20261105_stack_integration'
PRIMARY = 'ASTIS-SA-20261105-GaussianComplexityMixtureDensities'
IDS = [PRIMARY,
       'ASTIS-SA-20261019-HuanjianPoissonHarmonicity',
       'ASTIS-SA-20261019-HuanjianSphericalMeanValue',
       'ASTIS-SA-20261019-HuanjianRadialGreenData',
       'ASTIS-SA-20261019-HuanjianBallFlux',
       'ASTIS-SA-20261103-GaussianComplexitySphericalPoissonMoments',
       'ASTIS-SA-20261103-GaussianComplexityEvaluatedEq24',
       'ASTIS-SA-20261104-GaussianComplexitySingleBlockSeparation']


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def save(name, value):
    (OUT / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def git(*args):
    return subprocess.check_output(['git', *args], text=True).strip()


head = git('rev-parse', 'HEAD')
assert git('rev-parse', 'origin/main') == LATEST
subprocess.run(['git', 'merge-base', '--is-ancestor', LATEST, 'HEAD'], check=True)
subprocess.run(['git', 'merge-base', '--is-ancestor', MERGE, LATEST], check=True)
seal_path = OUT.parent / 'postmerge-density-purification/exposition-seal.json'
assert sha(seal_path.read_bytes()) == 'af73e5ee7b6309b8ecf294d1468a68e47e18d9c6ea2731a62fd341d86a2ebf8d'
seal = json.loads(seal_path.read_text())
assert seal['status'] == 'accepted' and seal['blocking_findings'] == []
assert seal['reviewer_id'] == '/root/density_fresh_source_module_review'
assert seal['canonical_main_merge'] == MERGE
gate_path = ROOT / '.astis/site-lean-gate.json'
gate = json.loads(gate_path.read_text())
assert gate['passed'] and gate['commit'] == head
assert gate['source_digest'] == astis_site.source_digest()
ledger = advance.DEFAULT_ADVANCE_LEDGER
discovery = advance.DEFAULT_DISCOVERY_LEDGER
before = ledger.read_bytes()
before_discovery = discovery.read_bytes()
assert before == subprocess.check_output(['git', 'show', LATEST + ':runs/substantive_advances.jsonl'])
states = advance.current_advances()
assert [k for k, v in states.items() if v['state'] == 'STABILIZING'] == [PRIMARY]
assert states[PRIMARY]['latest_evidence']['integration_owner'] == ACTOR
assert all(states[k]['state'] == 'VERIFIED' for k in IDS[1:])
foreign_frontiers = {str(p): sha(p.read_bytes()) for p in
                     (ROOT / 'research-wiki/frontier-cells').glob('*.json')}
for ident in IDS:
    # Validate all exact current reviewed targets before making any mutation.
    targets = states[ident].get('publication_declarations')
    assert targets, ident
    publication.check_advance(list(targets), reviewed=True)
save('normal-api-admission-preflight.json', {
    'checked_HEAD': head, 'latest_main': LATEST, 'actual_source_merge': MERGE,
    'ledger_before_bytes': len(before), 'ledger_before_sha256': sha(before),
    'ledger_before_git_blob': git('rev-parse', LATEST + ':runs/substantive_advances.jsonl'),
    'state_count': len(states), 'owned_targets': IDS,
    'other_states_before': {k: v for k, v in states.items() if k not in IDS},
    'discovery_sha256': sha(before_discovery),
    'all_frontier_hashes_before': foreign_frontiers,
    'gate_snapshot': gate, 'independent_density_seal_sha256': sha(seal_path.read_bytes()),
    'boundary': 'These are existing independently VERIFIED results whose source is already in main via PR380. No VERIFIED admission is performed here.'})

for ident in IDS:
    if ident != PRIMARY:
        advance.transition_advance(ident, 'STABILIZING', worker_id=ACTOR, evidence={
            'canonical_branch': git('branch', '--show-current'),
            'integration_owner': ACTOR,
            'already_published_source_merge': MERGE,
            'reason': 'Serialize final integration accounting of this existing independently VERIFIED component of actual PR380; no new proof credit.'})
    advance.transition_advance(ident, 'MERGED', worker_id=ACTOR, evidence={
        'pr': 'https://github.com/DakeBU/Automization-Sampling-Optimisation-Geometry-Lib/pull/380',
        'commit': MERGE,
        'integration_owner': ACTOR,
        'latest_main_preserved': LATEST,
        'current_adapted_build_HEAD': head,
        'current_adapted_source_digest': gate['source_digest'],
        'gate': 'Actual canonical Lean/Tests/fake-closure/ASTIS gate passed9632jobs at ' + head,
        'direct_original_main_CI': 'https://github.com/DakeBU/Automization-Sampling-Optimisation-Geometry-Lib/actions/runs/42036682449',
        'independent_local_and_public_reader_review': str(OUT.parent / 'postmerge-density-purification/exposition-seal.json') if ident == PRIMARY else str(OUT.parent / 'independent-integration-reader-review.json'),
        'purification_scope': 'Only density has accepted independent Exposition Seal; other components retain their separate purification debt.',
        'goal_complete': False})

after = ledger.read_bytes()
assert after.startswith(before)
tail = after[len(before):]
events = [json.loads(line) for line in tail.splitlines()]
assert len(events) == 15 and {e['advance_id'] for e in events} == set(IDS)
assert all(e['event'] == 'transition' and e['to_state'] in ['STABILIZING', 'MERGED'] for e in events)
now = advance.current_advances()
assert all(now[k]['state'] == 'MERGED' for k in IDS)
assert not [k for k, v in now.items() if v['state'] == 'STABILIZING']
assert {k: v for k, v in now.items() if k not in IDS} == {k: v for k, v in states.items() if k not in IDS}
assert discovery.read_bytes() == before_discovery
assert all(sha(Path(p).read_bytes()) == digest for p, digest in foreign_frontiers.items())
(OUT / 'normal-api-admission.exact-append.jsonl').write_bytes(tail)
save('normal-api-admission-postcheck.json', {
    'actual_source_merge': MERGE, 'checked_adapted_HEAD': head,
    'ledger_before_bytes': len(before), 'ledger_after_bytes': len(after),
    'ledger_before_sha256': sha(before), 'ledger_after_sha256': sha(after),
    'old_raw_prefix_exactly_preserved': True, 'append_events': len(events),
    'append_sha256': sha(tail), 'all_owned_states': {k: now[k]['state'] for k in IDS},
    'all_other_states_exactly_preserved': True, 'discovery_exactly_preserved': True,
    'all_frontiers_unchanged_by_this_API_operation': True, 'stabilization_lane': [],
    'no_VERIFIED_transition': True, 'whole_Goal_complete': False})
print('Normal API admission passed: already-merged eight components recorded; exact old ledger prefix and all other states preserved; stabilization lane empty.')
