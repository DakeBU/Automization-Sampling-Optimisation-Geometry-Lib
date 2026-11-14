"""Capture PRIVATE full-foreign preservation data outside portable evidence.

Read-only with respect to project ledgers, frontiers, tracked files and queue.
No transition API is called. No private raw values are printed or published.
"""
from pathlib import Path
from hashlib import sha256
from datetime import datetime, timezone
import base64
import json
import os
import stat
import subprocess
import sys

sys.dont_write_bytecode = True
REPO = Path.cwd().resolve()
sys.path.insert(0, str(REPO))
from tools import astis_advance as adv

ROOT = Path(__file__).resolve().parent.parent
PORTABLE = ROOT / 'normal-sourceV'
PRIVATE = ROOT / 'PRIVATE-normal-sourceV-baseline'
PRIVATE.mkdir(exist_ok=True)
assert not list(PRIVATE.iterdir()), 'Do not replace an existing private baseline'
AID = 'ASTIS-SA-20261110-GaussianComplexityFixedSpectrumTargetLaw'
CP = 'research-wiki/frontier-cells/ASTIS-SW-GAUSSIAN-COMPLEXITY-fixed-spectrum-target-law.json'
LEDGER = Path('runs/substantive_advances.jsonl')

def file_record(name):
    path = Path(name)
    if path.is_symlink():
        return {'kind':'symlink', 'target':os.readlink(path)}
    if path.is_file():
        raw = path.read_bytes()
        return {'kind':'regular', 'bytes':len(raw), 'sha256':sha256(raw).hexdigest(),
                'mode':stat.S_IMODE(path.stat().st_mode)}
    return {'kind':'missing'}

raw = LEDGER.read_bytes()
assert raw.endswith(b'\n')
records = [json.loads(line) for line in raw.splitlines() if line.strip()]
states = adv._replay_advances(records)
own = states[AID]
foreign = {key:value for key,value in states.items() if key != AID}
assert len(foreign) == 296
assert own['state'] == 'PROVED_LOCAL'
assert own['owner_id'] == 'huanjian_gc_20261110_fixed_spectrum_target_law'
historical_v = [item for item in records if item.get('event') == 'transition'
                and item.get('to_state') == 'VERIFIED']
current_v = {key:value for key,value in states.items() if value.get('state') == 'VERIFIED'}
preproof = json.loads(Path('.astis/huanjian-gc-fixed-spectrum-target-law-20261110/preproof-baseline.private.json').read_bytes())
assert foreign == preproof['all296_foreign_states']
tracked = subprocess.run(['git','ls-files','-z'],capture_output=True,check=True).stdout
protected = {name.decode():file_record(name.decode()) for name in tracked.split(b'\0')
             if name and name.decode() not in [str(LEDGER), CP]}
frontiers = {str(path):{'sha256':sha256(path.read_bytes()).hexdigest(),
                       'value':json.loads(path.read_bytes())}
             for path in sorted(Path('research-wiki/frontier-cells').rglob('*.json'))
             if str(path) != CP}
untracked_all = subprocess.run(['git','ls-files','--others','--exclude-standard','-z'],capture_output=True,check=True).stdout
own_prefix = str(ROOT.relative_to(REPO)) + '/'
foreign_untracked_names = [name for name in untracked_all.split(b'\0')
                           if name and not name.decode().startswith(own_prefix)]
untracked_raw = b'\0'.join(foreign_untracked_names) + (b'\0' if foreign_untracked_names else b'')
untracked = {name.decode():file_record(name.decode()) for name in foreign_untracked_names}
cellraw = Path(CP).read_bytes()
cell = json.loads(cellraw)
baseline = {
    'PRIVATE_FULL_FOREIGN_RAW_DO_NOT_PUBLISH':True,
    'created_utc':datetime.now(timezone.utc).isoformat(),
    'head':subprocess.run(['git','rev-parse','HEAD'],capture_output=True,check=True).stdout.decode().strip(),
    'ledger_path':str(LEDGER), 'ledger_prefix_bytes':len(raw),
    'ledger_prefix_sha256':sha256(raw).hexdigest(),
    'all_foreign_states':foreign,
    'all_historical_VERIFIED_events_full_original_evidence':historical_v,
    'all_current_VERIFIED_states_full_original_evidence':current_v,
    'protected_tracked_files':protected,
    'all_foreign_frontiers':frontiers,
    'foreign_untracked_queue_raw_base64':base64.b64encode(untracked_raw).decode(),
    'foreign_untracked_files':untracked,
    'own_state':own, 'own_frontier_path':CP, 'own_frontier_value':cell,
    'own_frontier_raw_base64':base64.b64encode(cellraw).decode(),
    'preproof_foreign_states_equal':True,
}
assert baseline['head'] == '56dbffcda73fa78539777059f26a964d9b53fa0c'
(PRIVATE/'ledger-prefix.raw.jsonl').write_bytes(raw)
(PRIVATE/'baseline.private.json').write_text(json.dumps(baseline,ensure_ascii=False,indent=2)+'\n')
(PRIVATE/'DO-NOT-PUBLISH.txt').write_text('PRIVATE FULL FOREIGN RAW. Never copy this directory or its files into E, portable/public evidence, archives or commits. Read-only preservation baseline only.\n')
for path in PRIVATE.iterdir():
    path.chmod(0o444)
gaussian_v = [key for key in current_v if 'GaussianComplexity' in key]
summary = {
    'private_baseline_outside_portable_directory':True,
    'private_baseline_published':False,
    'baseline_sha256':sha256((PRIVATE/'baseline.private.json').read_bytes()).hexdigest(),
    'raw_ledger_prefix_bytes':len(raw), 'raw_ledger_prefix_sha256':sha256(raw).hexdigest(),
    'foreign_state_count':len(foreign), 'historical_VERIFIED_events':len(historical_v),
    'current_VERIFIED_states':len(current_v), 'GaussianComplexity_current_V_ids_all_preserved':gaussian_v,
    'pending_nine_covered_by_all_Gaussian_V_and_all_foreign_states':True,
    'foreign_frontier_count':len(frontiers), 'protected_tracked_count':len(protected),
    'foreign_untracked_count':len(untracked), 'preproof_foreign_states_equal':True,
    'target_state':own['state'], 'proof_owner':own['owner_id'],
    'own_frontier_status':cell.get('status'),
    'own_frontier_evidence_keys':list(cell.get('evidence',{})),
}
(PORTABLE/'private-baseline-public-safe-summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({key:value for key,value in summary.items()
                  if key != 'GaussianComplexity_current_V_ids_all_preserved'},ensure_ascii=False,indent=2))
