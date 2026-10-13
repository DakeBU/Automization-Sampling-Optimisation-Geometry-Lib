"""Publish only the gated integration commit and verify its remote identity."""
from pathlib import Path
import json,subprocess,datetime
r=Path(__file__).parent;out=r/'integration93'
note=json.loads((r/'integration.notes.json').read_bytes());assert note['state_distinctions']['local_aggregate_and_generated_site_gates']
commit=subprocess.check_output(['git','rev-parse','HEAD']).decode().strip()
assert subprocess.check_output(['git','show','-s','--format=%s']).decode().strip()=='Integrate verified actual PBPS finite-count complete-path law'
assert not subprocess.check_output(['git','diff','--cached','--name-only']).strip()
cmd=['git','push','origin','HEAD:refs/heads/codex/sphmc-standardized-rgo'];q=subprocess.run(cmd,capture_output=True)
(out/'push.stdout.log').write_bytes(q.stdout);(out/'push.stderr.log').write_bytes(q.stderr)
assert q.returncode==0,(q.stdout+q.stderr).decode(errors='replace')
remote=subprocess.check_output(['git','ls-remote','origin','refs/heads/codex/sphmc-standardized-rgo']).decode().strip();assert remote.split()[0]==commit
(out/'push.receipt.json').write_text(json.dumps(dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),argv=cmd,exit_code=0,commit=commit,remote_exact=remote,main_merged=False,purified=False,Goal_complete=False),indent=2)+'\n',encoding='utf8',newline='\n')
cmd=['gh','pr','edit','315','--title','Formalize actual PBPS finite-count history and path laws','--body-file',str(out/'pr315.body.md')];q=subprocess.run(cmd,capture_output=True)
(out/'pr.stdout.log').write_bytes(q.stdout);(out/'pr.stderr.log').write_bytes(q.stderr)
assert q.returncode==0,(q.stdout+q.stderr).decode(errors='replace')
(out/'pr.receipt.json').write_text(json.dumps(dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),argv=cmd,exit_code=0,commit=commit,PR='https://github.com/DakeBU/Automization-Sampling-Optimisation-Geometry-Lib/pull/315'),indent=2)+'\n',encoding='utf8',newline='\n')
print('PUSHED_INTEGRATION93',commit)
