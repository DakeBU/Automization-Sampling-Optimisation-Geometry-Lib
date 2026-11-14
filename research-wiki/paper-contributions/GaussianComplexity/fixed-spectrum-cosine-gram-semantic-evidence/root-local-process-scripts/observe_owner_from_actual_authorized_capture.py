from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, subprocess, sys
sys.dont_write_bytecode = True
sys.path.insert(0, 'tools')
import astis_advance as adv
W = Path(__file__).parent
sha = lambda b: hashlib.sha256(b).hexdigest()
tool = json.loads((W/'original-owner-PR403-actual-gh.tool-return.json').read_bytes())
assert tool['exit_code'] == 0
raw_gh = (W/'original-owner-PR403-actual-gh.raw.json').read_bytes()
assert raw_gh == tool['output'].encode()
x = json.loads(raw_gh)
main = subprocess.check_output(['git', 'rev-parse', 'origin/main'], text=True).strip()
raw = subprocess.check_output(['git', 'show', main+':runs/substantive_advances.jsonl'])
states = adv._replay_advances([json.loads(z) for z in raw.splitlines()])
ancestor = subprocess.run(['git', 'merge-base', '--is-ancestor', x['headRefOid'], main]).returncode
assert ancestor in [0, 1]
out = {'recorded_utc': datetime.now(timezone.utc).isoformat(),
       'network_provenance': 'Read-only gh pr view was run directly with require_escalated using the already approved gh/pr/view prefix after a Python-wrapped sandbox network error. The actual tool return is retained byte-for-byte in its output field; this script performs only local readback and does not recreate a network execution receipt.',
       'actual_gh_tool_return_sha256': sha((W/'original-owner-PR403-actual-gh.tool-return.json').read_bytes()),
       'actual_gh_stdout_sha256': sha(raw_gh),
       'PR': {k: x[k] for k in ['number', 'url', 'state', 'headRefOid', 'mergeCommit', 'mergedAt']},
       'fresh_fetched_origin_main': main, 'PR_head_ancestor_of_main': ancestor == 0,
       'main_ledger_sha256': sha(raw),
       'stabilizing': [{'advance_id': a, 'owner_id': s.get('owner_id'), 'state': s['state']} for a, s in states.items() if s['state'] == 'STABILIZING'],
       'boundary': 'PR403 merged into eb005d3e; successful individual checks do not release the still-active original ledger lease. No takeover, rerun, comment, release, shared write or publication.',
       'retained_wrapper_network_failure_log_sha256': '87f0e3916d6a5ab55c81b7579e385e6655ebb8b596ecc7dc25e3635e746d8552'}
p = W/'original-owner-merged-PR-and-unreleased-ledger-observation.json'
with p.open('x') as f:
    json.dump(out, f, ensure_ascii=False, indent=2)
    f.write('\n')
print(json.dumps(out))
