from pathlib import Path
import subprocess,json,datetime
r=Path(__file__).parent;out=r/'integration87';commit=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()
assert subprocess.check_output(['git','show','-s','--format=%s'],text=True).strip()=='Integrate verified actual PBPS history and unused-clock tail law'
assert not subprocess.check_output(['git','diff','--cached','--name-only'],text=True).strip()
argv=['git','push','origin','HEAD:refs/heads/codex/sphmc-standardized-rgo'];q=subprocess.run(argv,capture_output=True)
for name,b in [('push.stdout.log',q.stdout),('push.stderr.log',q.stderr)]:
 p=out/name;assert not p.exists();p.write_bytes(b)
assert q.returncode==0,(q.stdout+q.stderr).decode(errors='replace')
remote=subprocess.check_output(['git','ls-remote','origin','refs/heads/codex/sphmc-standardized-rgo'],text=True).strip();assert remote.split()[0]==commit
p=out/'push.receipt.json';assert not p.exists();p.write_text(json.dumps(dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),argv=argv,exit_code=0,commit=commit,remote_exact=remote,main_merged=False,purified=False,Goal_complete=False),indent=2)+'\n',encoding='utf8',newline='\n')
argv=['gh','pr','edit','315','--title','Formalize actual PBPS physical-time process and finite-history clock law','--body-file',str(out/'pr315.body.md')]
q=subprocess.run(argv,capture_output=True)
for name,b in [('pr.stdout.log',q.stdout),('pr.stderr.log',q.stderr)]:
 p=out/name;assert not p.exists();p.write_bytes(b)
assert q.returncode==0,(q.stdout+q.stderr).decode(errors='replace')
(out/'pr.receipt.json').write_text(json.dumps(dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),argv=argv,exit_code=0,commit=commit,PR='https://github.com/DakeBU/Automization-Sampling-Optimisation-Geometry-Lib/pull/315'),indent=2)+'\n',encoding='utf8',newline='\n')
print('PUSHED_INTEGRATION87',commit)
