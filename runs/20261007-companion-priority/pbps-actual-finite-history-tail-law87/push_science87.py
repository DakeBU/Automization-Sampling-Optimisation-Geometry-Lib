from pathlib import Path
import subprocess,json,datetime
r=Path(__file__).parent;assert (r/'proved-local87.json').exists()
commit=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()
assert subprocess.check_output(['git','show','-s','--format=%s',commit],text=True).strip()=='Prove actual PBPS finite-history and unused-clock tail law'
argv=['git','push','origin','HEAD:refs/heads/codex/sphmc-standardized-rgo'];q=subprocess.run(argv,capture_output=True)
for suffix,b in [('stdout.log',q.stdout),('stderr.log',q.stderr)]:
 p=r/('push-science87.'+suffix);assert not p.exists();p.write_bytes(b)
assert q.returncode==0,(q.stdout+q.stderr).decode(errors='replace')
remote=subprocess.check_output(['git','ls-remote','origin','refs/heads/codex/sphmc-standardized-rgo'],text=True).strip();assert remote.split()[0]==commit
p=r/'push-science87.receipt.json';assert not p.exists();p.write_text(json.dumps(dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),argv=argv,exit_code=q.returncode,commit=commit,remote_exact=remote,scope='PROVED_LOCAL science only. Independent exact-commit VERIFIED, existing sole-lane aggregation, main/PURIFIED/live/wholepaper/Goal pending.'),indent=2)+'\n',encoding='utf8',newline='\n');print('PUSHED_SCIENCE87',commit)
