from pathlib import Path
from datetime import datetime, timezone
import hashlib,html,json,os,re,subprocess,sys
ROOT=Path('E:/Samplinglib');OWN=ROOT/'runs/20261007-companion-priority/pbps-clock-construction-preread75';SELF=Path(__file__)
PY='C:/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe'
PRIMARY=ROOT/'runs/20261007-companion-priority/phase-pbps-gamma-preread57/primary-pbps.exactraw.snapshot.html'
EXPECTED='d81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760'
ACTOR='/root/exact_science63';RECIPE='Replace CRLF byte pairs with LF only; retain bare CR and every other byte.'
def sha(b):return hashlib.sha256(b).hexdigest()
def canon(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def load(p):return json.loads(p.read_bytes())
def read(n):return load(OWN/n)
def write(n,x):(OWN/n).write_bytes(json.dumps(x,ensure_ascii=False,sort_keys=True,indent=2).encode()+b'\n')
def pin(p):
 b=p.read_bytes();return dict(path=p.relative_to(ROOT).as_posix(),RAW_bytes=len(b),RAW_sha256=sha(b),LF_sha256=sha(b.replace(b'\r\n',b'\n')))
def check(row):
 p=ROOT/row['path'];q=pin(p)
 for k in ['RAW_bytes','RAW_sha256','LF_sha256']:assert row[k]==q[k],(p,k)
 return q
def git(args):return subprocess.run(['git',*args],cwd=ROOT,capture_output=True,check=True).stdout
def textof(raw):
 s=raw.decode();s=re.sub(r'<math\b[^>]*alttext="([^"]*)".*?</math>',lambda m:' $'+html.unescape(m.group(1))+'$ ',s,flags=re.S)
 return html.unescape(re.sub('<[^>]+>','',s))
def source():
 assert pin(PRIMARY)['RAW_sha256']==EXPECTED
 write('lease.open.json',dict(status='OPEN_SOURCE_FIRST_PROSPECTIVE_PLANNING_ONLY',actual_PID=os.getpid(),actor=ACTOR,no_SAU_Lean_Git_ledger_canonical_writes=True))
 write('observer.initial-shell-parser-negative.json',dict(status='RETAINED_READONLY_OBSERVER_COMMAND_FAILURE',tool_chunk='4b20a2',exit_code=1,actual_PID=None,PID_exposed_by_tool=False,diagnostic="PowerShell ParserError Missing type name after '[' in nested Python regex command; no source/canonical/owned mutation occurred.",repair='Use exact saved helper and direct Python invocation; not mathematical evidence.'))
 raw=PRIMARY.read_bytes();ls=raw.splitlines(keepends=True);spans=[('algorithm-and-prop31',1465,1653),('appendixA1-construction',2852,3025),('davis-reference',6198,6217)];rows=[]
 for name,a,b in spans:
  q=OWN/(name+'.exactraw.html');q.write_bytes(b''.join(ls[a-1:b]));txt=OWN/(name+'.readable.txt');txt.write_bytes(textof(q.read_bytes()).encode())
  rows.append(dict(anchor=name,start_line=a,end_line=b,whole_source=pin(PRIMARY),literal_RAW_slice=pin(q),readable_derivative=pin(txt),derivative_recipe='HTML math alttext preserved; tags removed and entities decoded; exact HTML remains authority.'))
 write('source.regions.json',dict(status='PRIMARY_READ_BEFORE_INTERFACE_OR_ROOT_IDEAS',primary=pin(PRIMARY),regions=rows))
 print(json.dumps(dict(status='SOURCE_SLICES_FROZEN',actual_PID=os.getpid(),primary=pin(PRIMARY),source_regions=len(rows))))
def launch(action):
 assert not (OWN/'lease.final.json').exists();(OWN/(action+'.executed-helper.RAW.py')).write_bytes(SELF.read_bytes());argv=[PY,'-B','-X','utf8',str(SELF),'_child',action]
 with (OWN/(action+'.stdout.log')).open('wb') as o,(OWN/(action+'.stderr.log')).open('wb') as e:
  p=subprocess.Popen(argv,cwd=ROOT,stdout=o,stderr=e);print(json.dumps(dict(status='RUNNING',actual_PID=p.pid,action=action,runner_PID=os.getpid())),flush=True);code=p.wait()
 write(action+'.receipt.json',dict(action=action,actual_PID=p.pid,runner_PID=os.getpid(),command=argv,exit_code=code,terminal_closed=True,stdout=pin(OWN/(action+'.stdout.log')),stderr=pin(OWN/(action+'.stderr.log')),executed_helper=pin(OWN/(action+'.executed-helper.RAW.py'))));print(json.dumps(dict(status='TERMINAL',actual_PID=p.pid,action=action,exit_code=code)));return code
if __name__=='__main__':
 action=sys.argv[-1]
 if sys.argv[1]=='_child':sys.exit(globals()[action]() or 0)
 else:sys.exit(launch(action))
