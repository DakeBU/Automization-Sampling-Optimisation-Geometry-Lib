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
def expectations():
 assert read('source.regions.json')['primary']['RAW_sha256']==EXPECTED
 write('source-first.expectations.json',dict(status='SOURCE_FIRST_BEFORE_LOCAL_INTERFACE_RETRIEVAL',actual_PID=os.getpid(),source_revision='arXiv:2609.06905v1 fixed local primary',
  actual_objects=dict(center='c=y-eta*gradientV(xRef)',residual='h(x)=gradientV(x)-gradientV(xRef)',phase_state='z=(x,p) in original finite real Hilbert H x H',
  flow='Phi_t(z)=(c+(x-c)cos t+sqrt(eta)p sin t, -eta^(-1/2)(x-c)sin t+p cos t)',bounce='S(z)=(x,R_h(x) p), R_0=I',rate='lambda(z)=sqrt(eta)*max(inner(p,h(x)),0)',
  energy='H(z)=(eta^(-1)*norm(x-c)^2+norm(p)^2)/2',cap='C_E=sqrt(eta)*beta*sqrt(2E)*(sqrt(2eta E)+norm(c-xRef))'),
  exact_construction=['Independent Exp(1) sequence E_(n>=1).','T_0=0, zeta_0=z_0.','S_(n+1)=inf{u>=0: integral_0^u lambda(Phi_s(zeta_Tn)) ds >= E_(n+1)}; empty set means infinity, not zero.','If S finite, T_(n+1)=T_n+S_(n+1) and zeta_T(n+1)=S_bounce(Phi_S(zeta_Tn)); if infinite, retain deterministic flow forever.','Between jumps use the same flow from the postjump state.','Energy preserved across flow and bounce produces one fixed initial-energy cap for the entire recursion.','C_E=0 => no jumps; C_E>0 => every finite waiting time >= E_(n+1)/C_E.','Infinite iid Exp(1) sum diverges a.s. by SLLN, therefore no finite-time accumulation.','Memorylessness plus measurable path construction, not cap alone, supplies homogeneous Markov property.'],
  algorithm_refresh='Algorithm1 draws reference and Gaussian initial momentum independently once. No refresh clock or refresh rate appears in (3.5)/(3.9)/AppendixA.1; adding one changes the process.',
  no_credit=['Unique Markov process','nonexplosion','stationarity','path reversal','L2 semigroup','averaged/terminal kernels','bounce-query costs','actual-input composition','paper/Goal completion'],
  initial_next_delta='Actual cumulative-hazard generalized-inverse clock on the real phase space, with measurable dependence and exact first-crossing/lower-bound/zero-cap laws; stochastic iid recursion remains separate.',
  source_omissions=['Extended waiting-time carrier and infinity branch are implicit in inf notation.','Measurability of state/clock/path recursion and independent clock realization are suppressed by Davis citation.','Zero residual-normal reflection is specified as identity; discontinuity is tolerated only because rate vanishes.','Fixed initial energy cap must be propagated through actual recursion; pointwise cap alone is not nonexplosion.']))
 print(json.dumps(dict(status='SOURCE_EXPECTATIONS_FROZEN_BEFORE_INTERFACES',actual_PID=os.getpid())))
def launch(action):
 assert not (OWN/'lease.final.json').exists();(OWN/(action+'.executed-helper.RAW.py')).write_bytes(SELF.read_bytes());argv=[PY,'-B','-X','utf8',str(SELF),'_child',action]
 with (OWN/(action+'.stdout.log')).open('wb') as o,(OWN/(action+'.stderr.log')).open('wb') as e:
  p=subprocess.Popen(argv,cwd=ROOT,stdout=o,stderr=e);print(json.dumps(dict(status='RUNNING',actual_PID=p.pid,action=action,runner_PID=os.getpid())),flush=True);code=p.wait()
 write(action+'.receipt.json',dict(action=action,actual_PID=p.pid,runner_PID=os.getpid(),command=argv,exit_code=code,terminal_closed=True,stdout=pin(OWN/(action+'.stdout.log')),stderr=pin(OWN/(action+'.stderr.log')),executed_helper=pin(OWN/(action+'.executed-helper.RAW.py'))));print(json.dumps(dict(status='TERMINAL',actual_PID=p.pid,action=action,exit_code=code)));return code
if __name__=='__main__':
 action=sys.argv[-1]
 if sys.argv[1]=='_child':sys.exit(globals()[action]() or 0)
 else:sys.exit(launch(action))
