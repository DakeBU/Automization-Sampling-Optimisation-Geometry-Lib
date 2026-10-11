from pathlib import Path
import subprocess,json,datetime
r=Path(__file__).parent
commit=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip();assert commit=='e8d38b3002f4562ef254205135c0d213f9efe410'
assert not subprocess.check_output(['git','diff','--cached','--name-only'],text=True).strip()
argv=['git','push','origin','HEAD:refs/heads/codex/sphmc-standardized-rgo'];q=subprocess.run(argv,capture_output=True)
for suffix,b in [('stdout.log',q.stdout),('stderr.log',q.stderr)]:
 p=r/('push-archive-successor90.'+suffix);assert not p.exists();p.write_bytes(b)
assert q.returncode==0,(q.stdout+q.stderr).decode(errors='replace')
remote=subprocess.check_output(['git','ls-remote','origin','refs/heads/codex/sphmc-standardized-rgo'],text=True).strip();assert remote.split()[0]==commit
p=r/'push-archive-successor90.receipt.json';assert not p.exists()
p.write_text(json.dumps(dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),argv=argv,exit_code=0,commit=commit,remote_exact=remote,mathematics_unchanged=True,VERIFIED=False,Goal_complete=False),indent=2)+'\n',encoding='utf8',newline='\n')
print('PUSHED_ARCHIVE_COMPLETE_SCIENCE90',commit)
