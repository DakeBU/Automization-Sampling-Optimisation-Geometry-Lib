import pathlib,json,hashlib,subprocess,os,sys,shutil,re,datetime
ROOT=pathlib.Path('E:/Samplinglib');R=ROOT/'runs/20261007-companion-priority/pbps-real-defect-root61';D=R/'independent-math61'
def sha(b):return hashlib.sha256(b).hexdigest()
def canon(q):return json.dumps(q,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def pin(p):
 p=pathlib.Path(p);b=p.read_bytes();l=b.replace(b'\r\n',b'\n');return dict(path=p.as_posix(),raw_bytes=len(b),lf_bytes=len(l),raw_sha256=sha(b),lf_sha256=sha(l))
def load(p):return json.loads(pathlib.Path(p).read_bytes())
def write(p,q):pathlib.Path(p).write_bytes((json.dumps(q,ensure_ascii=False,indent=2)+'\n').encode())
freeze=load(R/'math-freeze.json');before=[]
for row in freeze['inputs']:
 a=pin(row['path']);assert all(a[k]==row[k] for k in ['raw_bytes','raw_sha256','lf_sha256']);before.append(a)
assert len(before)==27 and (ROOT/'lean-toolchain').read_text().strip()=='leanprover/lean4:v4.33.0'
manifest=load(ROOT/'lake-manifest.json');mathlib=next(p for p in manifest['packages'] if p['name']=='mathlib');assert mathlib['rev'].startswith('db584')
api=[ROOT/'.lake/packages/mathlib/Mathlib'/x for x in ['Analysis/InnerProductSpace/Positive.lean','Analysis/InnerProductSpace/StarOrder.lean','Analysis/CStarAlgebra/ContinuousFunctionalCalculus/Instances.lean','Analysis/CStarAlgebra/ContinuousLinearMap.lean','Analysis/SpecialFunctions/ContinuousFunctionalCalculus/Rpow/Basic.lean']]
apipins=[pin(p) for p in api];lake=shutil.which('lake');assert lake
env=dict(os.environ);env.pop('ELAN_TOOLCHAIN',None);env.update(LEAN_NUM_THREADS='2',PYTHONUTF8='1',PYTHONDONTWRITEBYTECODE='1')
write(D/'compiler.inputs.before.json',dict(actual_PID=os.getpid(),checked_base=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT).decode().strip(),frozen_before=before,count=27,api_before=apipins,Mathlib_revision=mathlib['rev'],lake=pin(lake),environment={'ELAN_TOOLCHAIN':'UNSET','LEAN_NUM_THREADS':'2','PYTHONUTF8':'1'},timing='Actual source/toolchain/manifest and selected API bytes before independent compiler child'))
def run(label,args):
 start=datetime.datetime.now(datetime.timezone.utc).isoformat()
 with (D/(label+'.stdout.log')).open('wb') as out,(D/(label+'.stderr.log')).open('wb') as err:
  p=subprocess.Popen(args,cwd=ROOT,env=env,stdout=out,stderr=err);pid=p.pid;code=p.wait()
 q=dict(command=args,cwd=ROOT.as_posix(),actual_PID=pid,exit_code=code,terminal_closed=True,started_utc=start,finished_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),stdout=pin(D/(label+'.stdout.log')),stderr=pin(D/(label+'.stderr.log')));write(D/(label+'.status.json'),q);assert code==0,q;return q
version=run('toolchain',[lake,'env','lean','--version']);assert '4.33.0' in (D/'toolchain.stdout.log').read_text()
compiler=run('compiler',[lake,'build','Tests.ProximalBPSRealDefectRoot'])
after=[pin(row['path']) for row in freeze['inputs']];assert before==after and apipins==[pin(p) for p in api]
log=(D/'compiler.stdout.log').read_text(encoding='utf8');assert 'Build completed successfully (3916 jobs).' in log and 'sorryAx' not in log
closures=[]
for name in freeze['mathematical_declarations']:
 m=re.search("'"+re.escape(name)+r"' depends on axioms: \[([^\]]+)\]",log);assert m;ax=[x.strip() for x in m.group(1).split(',')];assert set(ax)=={'propext','Classical.choice','Quot.sound'};closures.append(dict(declaration=name,actual_axioms=ax))
sys.dont_write_bytecode=True;sys.path.insert(0,str(ROOT/'tools'));import astis
scans=[]
for row in freeze['inputs'][:5]:
 p=pathlib.Path(row['path']);text=astis.strip_lean_comments_and_strings(p.read_text());hits=re.findall(r'\b(?:axiom|sorry|admit|sorryAx)\b|\bProp\s*:=\s*True\b|:=\s*(?:by\s*)?trivial\b',text);assert not hits
 scans.append(dict(source=pin(p),fake_hits=hits,comments_strings_removed=True))
signatures=[]
for i,row in enumerate(freeze['inputs'][:2]):
 s=pathlib.Path(row['path']).read_text();header=(ROOT/'runs/20261007-companion-priority/pbps-real-defect-root-preproof61'/('header'+str(i)+'.lean')).read_text().rstrip();assert header+' := by' in s
 signatures.append(dict(declaration=freeze['mathematical_declarations'][i],actual_source=pin(row['path']),sealed_header=pin(ROOT/'runs/20261007-companion-priority/pbps-real-defect-root-preproof61'/('header'+str(i)+'.lean')),exact_header_unchanged=True))
write(D/'compiler.validation.json',dict(status='PASS',actual_wrapper_PID=os.getpid(),actual_compiler=compiler,toolchain=version,post_frozen=after,post_api=apipins,focused_jobs=3916,invocations=1,forced_rebuild=False,cached_replay='Lake nonforced build output is actual invocation, not a fresh rebuild of all dependencies',actual_standard3=closures,anonymous_Test='Compiled genuine original-input contractivity consumer; no invented named Test axiom print',fake_scans=scans,fake_closure_count=0,exact_signatures=signatures))
print(json.dumps(dict(status='INDEPENDENT_FOCUSED61_PASS',actual_wrapper_PID=os.getpid(),actual_compiler_PID=compiler['actual_PID'],exit_code=0,freeze_count=27,focused_jobs=3916,Mathlib_revision=mathlib['rev'])),flush=True)
