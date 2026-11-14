from pathlib import Path
from datetime import datetime, timezone
import json, hashlib, subprocess, sys
sys.dont_write_bytecode = True
sys.path.insert(0, 'tools')
import astis_advance as adv
W = Path(__file__).parent
cmd = ['/Users/zhouhuanjian/.local/bin/gh', 'pr', 'view', 'codex/slc-lsi-weighted-radial-mgf-release', '--json', 'number,url,state,headRefOid,mergeCommit,mergedAt,statusCheckRollup']
r = subprocess.run(cmd, capture_output=True)
assert r.returncode == 0, r.stderr.decode()
with (W/'original-owner-PR403-actual-gh.raw.json').open('xb') as f:
    f.write(r.stdout)
x = json.loads(r.stdout)
main = subprocess.check_output(['git', 'rev-parse', 'origin/main'], text=True).strip()
raw = subprocess.check_output(['git', 'show', main+':runs/substantive_advances.jsonl'])
states = adv._replay_advances([json.loads(z) for z in raw.splitlines()])
ancestor = subprocess.run(['git', 'merge-base', '--is-ancestor', x['headRefOid'], main]).returncode
assert ancestor in [0, 1]
out = {'observed_utc': datetime.now(timezone.utc).isoformat(), 'actual_gh_command': cmd,
       'actual_gh_stdout_sha256': hashlib.sha256(r.stdout).hexdigest(),
       'PR': {k: x[k] for k in ['number', 'url', 'state', 'headRefOid', 'mergeCommit', 'mergedAt']},
       'fresh_origin_main': main, 'PR_head_is_ancestor_of_fresh_origin_main': ancestor == 0,
       'main_ledger_sha256': hashlib.sha256(raw).hexdigest(),
       'actual_stabilizing': [{'advance_id': a, 'owner_id': s.get('owner_id'), 'state': s['state']} for a, s in states.items() if s['state'] == 'STABILIZING'],
       'checks': [{'name': z.get('name'), 'status': z.get('status'), 'conclusion': z.get('conclusion'), 'detailsUrl': z.get('detailsUrl')} for z in x.get('statusCheckRollup', [])],
       'boundary': 'Merged PR and successful individual checks do not release the normal STABILIZING ledger lease. No takeover, rerun, comment, release, shared integration or publication action was executed.'}
with (W/'original-owner-merged-PR-and-unreleased-ledger-observation.json').open('x') as f:
    json.dump(out, f, ensure_ascii=False, indent=2)
    f.write('\n')
print(json.dumps(out))
