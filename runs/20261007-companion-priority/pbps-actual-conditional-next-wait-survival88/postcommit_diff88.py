from pathlib import Path
import json,subprocess,hashlib,datetime
r=Path(__file__).parent;out=r/'integration88'
assert subprocess.check_output(['git','show','-s','--format=%s'],text=True).strip()=='Integrate verified actual PBPS conditional next-wait survival'
args=['git','diff','--check'];q=subprocess.run(args,capture_output=True)
for name,b in [('postcommit-plain-diff-check.stdout.log',q.stdout),('postcommit-plain-diff-check.stderr.log',q.stderr)]:
 p=out/name;assert not p.exists();p.write_bytes(b)
p=out/'postcommit-plain-diff-check.receipt.json';assert not p.exists()
p.write_text(json.dumps(dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),argv=args,exit_code=q.returncode,terminal_closed=True,commit=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),stdout_sha256=hashlib.sha256(q.stdout).hexdigest(),stderr_sha256=hashlib.sha256(q.stderr).hexdigest(),preserved_other_worktree_edits=True),indent=2)+'\n',encoding='utf8',newline='\n')
assert q.returncode==0,(q.stdout+q.stderr).decode(errors='replace');print('Plain git diff --check PASS after integration commit.')
