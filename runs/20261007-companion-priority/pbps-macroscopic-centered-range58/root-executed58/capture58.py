from pathlib import Path
import subprocess,json,datetime,hashlib
run=Path('runs/20261007-companion-priority/pbps-macroscopic-centered-range58')
j=lambda p:json.loads(Path(p).read_text(encoding='utf-8'))
assert j(run/'root.integration.1.lease.json')['status']=='CLOSED' and j(run/'root.integration.1.lease.json')['exit_code']==0
now=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
lease=run/'root.desktop-capture58.lease.json';assert not lease.exists()
def w(p,d):Path(p).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
d=dict(status='OPEN',read='OPEN',write='OPEN',Python='OPEN',compiler='NOT_STARTED_CLOSED',opened_utc=now(),scope='Bounded actual local desktop companion/proof/exact source-declaration branch screenshots; two owned isolated headless browsers and HTTP servers, user browser untouched.')
w(lease,d);code=1
try:
 for label,name in [('companion','inspect-cdp58.mjs'),('proof','inspect-proof-cdp58.mjs')]:
  cmd=[r'C:\Users\admin\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\bin\node.exe',str(Path('.astis/pbps-marginal-gradient51')/name)]
  log=run/('desktop58.'+label+'.log');assert not log.exists();start=now()
  with log.open('wb') as out:
   p=subprocess.Popen(cmd,stdout=out,stderr=subprocess.STDOUT);d.update(active_owned_node_pid=p.pid,active_command=cmd);w(lease,d);rc=p.wait()
  w(run/('desktop58.'+label+'.status.json'),dict(command=cmd,owned_node_pid=p.pid,exit_code=rc,started_utc=start,closed_utc=now(),log_raw_sha256=hashlib.sha256(log.read_bytes()).hexdigest(),scope='Successful Node exit occurs only after Browser.close/owned child exit and local HTTP server finally close. No physical-device/live/source/full-reader acceptance.'))
  print(label+' actual capture exit '+str(rc),flush=True)
  if rc:print(log.read_text(encoding='utf-8',errors='replace')[-3500:],flush=True);raise SystemExit(rc)
 code=0
finally:
 d.update(status='CLOSED',read='CLOSED',write='CLOSED',Python='CLOSED',compiler='NOT_STARTED_CLOSED',closed_utc=now(),exit_code=code);w(lease,d)
