import os,sys,json,hashlib,pathlib,subprocess,datetime,re
ROOT=pathlib.Path('E:/Samplinglib'); os.chdir(ROOT)
R=ROOT/'runs/20261007-companion-priority/pbps-macroscopic-centered-range58'; D=R/'exact-verification58'
SCI='8c8847715c1d4c3033224b069d8dd694f2a4bd30'; ACTOR='whole_math52_exact58'
def canon(q): return json.dumps(q,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def sha(b): return hashlib.sha256(b).hexdigest()
def load(p): return json.loads(pathlib.Path(p).read_bytes())
def write(p,q): pathlib.Path(p).write_bytes((json.dumps(q,ensure_ascii=False,indent=2,allow_nan=False)+'\n').encode())
def pin(p):
 p=pathlib.Path(p); b=p.read_bytes(); l=b.replace(b'\r\n',b'\n')
 return dict(path=p.as_posix(),bytes=len(b),lf_bytes=len(l),raw_sha256=sha(b),lf_sha256=sha(l))
def path(p,base=ROOT):
 p=pathlib.Path(p); return p if p.is_absolute() else base/p
def sig(row): return (str(path(row['path'])).replace('\\','/').lower(),row.get('bytes',row.get('raw_bytes')),row['raw_sha256'],row['lf_sha256'])
def matches(row,p):
 a=pin(p)
 return a['bytes']==row.get('bytes',row.get('raw_bytes')) and a['raw_sha256']==row['raw_sha256'] and a['lf_sha256']==row['lf_sha256'] and ('lf_bytes' not in row or a['lf_bytes']==row['lf_bytes'])
def rows(q):
 if isinstance(q,dict):
  if 'path' in q and 'raw_sha256' in q and 'lf_sha256' in q and ('bytes' in q or 'raw_bytes' in q): yield q
  for v in q.values(): yield from rows(v)
 elif isinstance(q,list):
  for v in q: yield from rows(v)
def selfcheck(q,k): assert sha(canon({a:b for a,b in q.items() if a!=k}))==q[k],('self',k)
def command(name,args):
 env=os.environ.copy(); env.pop('ELAN_TOOLCHAIN',None);env.update(LEAN_NUM_THREADS='2',PYTHONUTF8='1',PYTHONDONTWRITEBYTECODE='1');env['PYTHONPATH']=str(ROOT/'tools')+os.pathsep+str(ROOT)
 start=datetime.datetime.now(datetime.timezone.utc).isoformat()
 with (D/(name+'.log')).open('wb') as f:
  p=subprocess.Popen(args,cwd=ROOT,env=env,stdout=f,stderr=subprocess.STDOUT); pid=p.pid; rc=p.wait()
 q=dict(command=args,actual_PID=pid,exit_code=rc,status='PASS' if rc==0 else 'FAIL',resource='CLOSED',started_utc=start,finished_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),log=pin(D/(name+'.log')))
 write(D/(name+'.status.json'),q); assert rc==0,(name,rc);return q
def prepare():
 assert subprocess.check_output(['git','rev-parse','HEAD']).decode().strip()==SCI
 write(D/'lease.open.json',dict(status='OPEN',actor=ACTOR,checked_commit=SCI,Python_PID=os.getpid(),compiler='NOT_STARTED',read='OPEN',write='OPEN'))
 maps={}; adopted=[]
 for folder in ['exposition-wording-overlay58','exposition-api-overlay58','exposition-assumption-overlay58']:
  q=load(R/folder/'proposal.json'); selfcheck(q,'proposal_sha256')
  for v in q.get('changes',[q]):
   if 'original' not in v: continue
   a=v['original']; b=pin(path(v.get('snapshot',v.get('original_snapshot'))));assert matches(a,path(b['path']));maps[sig(a)]=b
 for f in sorted(R.glob('root.*adoption.json')):
  q=load(f); adopted.append(pin(f))
  for v in q.get('historical_mutable_input_mappings',[]):
   a=v['original']; b=v['exactraw_snapshot']; assert matches(a,path(b['path'])) and matches(b,path(b['path']))
   maps[sig(a)]=b
 checks=[]; mappings=[]; inputs={}; selfs=[]
 def check(row,base=ROOT):
  p=path(row['path'],base); row=dict(row,path=p.as_posix()); s=sig(row)
  if matches(row,p): used=p
  else:
   assert s in maps,('unmapped',row)
   used=path(maps[s]['path']); assert matches(row,used); mappings.append(dict(original=row,exactraw_snapshot=pin(used)))
  checks.append(dict(expected=row,actual=pin(used),mapped=used!=p)); inputs[used.as_posix()]=pin(used)
 freeze=load(R/'math-freeze.json');assert len(freeze['inputs'])==72
 for a in freeze['inputs']:check(a)
 stages=['whole-math58','exposition-wording-overlay-review58','exposition-api-overlay-review58','exposition-assumption-overlay-review58','source-review58','source-successor-review58','source-final-review58','source-complete-review58','source0-verdict-addendum58','anonymous-decoder']
 for folder in stages:
  F=R/folder; run=load(F/'run.json');lease=load(F/'lease.json');assert lease['status']=='CLOSED',folder
  selfcheck(run,'run_sha256');selfs.append(dict(path=pin(F/'run.json'),field='run_sha256',value=run['run_sha256']))
  pk=next((k for k in ['review_binding_payload','editorial_binding_payload','API_binding_payload','assumption_binding_payload','source_review_payload','payload'] if k in run),None)
  if pk:assert sha(canon(run[pk]))==run[pk+'_sha256'];selfs.append(dict(path=pin(F/'run.json'),component=pk,value=run[pk+'_sha256']))
  for f in sorted(F.glob('*.json')):
   q=load(f);inputs[f.as_posix()]=pin(f)
   for k in ['receipt_sha256','lease_sha256','content_self_sha256']:
    if k in q:selfcheck(q,k);selfs.append(dict(path=pin(f),field=k,value=q[k]))
   # The actual artifact/input/output rows are native, including exact indexed source snapshots.
   for row in rows(q):check(row,F if folder=='anonymous-decoder' and not pathlib.Path(row['path']).is_absolute() and '/' not in row['path'] else ROOT)
 for a in adopted:check(a)
 # All explicit science entries use Git blobs through one bounded batch process.
 diff=subprocess.check_output(['git','diff-tree','--no-commit-id','--name-only','-r','-z',SCI]).split(b'\0');names=[v.decode() for v in diff if v];assert len(names)==1185,len(names)
 requests=''.join(SCI+':'+n+'\n' for n in names).encode();p=subprocess.Popen(['git','cat-file','--batch'],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE);out,err=p.communicate(requests);assert p.returncode==0
 pos=0;gitrows=[]
 for n in names:
  end=out.index(b'\n',pos); h=out[pos:end].decode().split();assert h[1]=='blob';size=int(h[2]);b=out[end+1:end+1+size];pos=end+size+2
  a=pin(ROOT/n);assert a['lf_sha256']==sha(b.replace(b'\r\n',b'\n')) and a['lf_bytes']==len(b.replace(b'\r\n',b'\n')),(n,'GitLF');inputs[a['path']]=a
  gitrows.append(dict(path=n,git_blob_oid=h[0],git_raw_bytes=len(b),git_raw_sha256=sha(b),git_lf_sha256=sha(b.replace(b'\r\n',b'\n')),current=a))
 write(D/'science.git.json',dict(status='PASS',checked_commit=SCI,count=len(names),actual_git_cat_file_PID=p.pid,exit_code=p.returncode,entries=gitrows))
 write(D/'native-checks.json',dict(status='PASS',math_originals=72,actual_pin_checks=len(checks),distinct_native_inputs=len(inputs),native_checks=checks,native_self_checks=selfs,historical_before_mappings=mappings,adoption_files=adopted))
 write(D/'inputs.pretransition.json',dict(status='PASS',inputs=list(inputs.values())))
 # Snapshots precede any canonical mutation and preserve exact committed administrative bytes.
 before=[]
 claim=load(R/'proved-local.json')
 audits=['research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261008-'+v+'.json' for v in ['L2PullbackRange','PBPSMacroscopicCenteredRange','PBPSCenteredMacroDefectGap']]
 for kind,paths in [('cell',claim['active_cells']),('audit',audits)]:
  for i,n in enumerate(paths):
   f=ROOT/('research-wiki/frontier-cells/'+n+'.json') if kind=='cell' else ROOT/n
   target=D/f'before-admin.{kind}.{i}.raw.snapshot.json';target.write_bytes(f.read_bytes());before.append(dict(original=pin(f),exactraw_snapshot=pin(target)))
 ledger=ROOT/'runs/substantive_advances.jsonl'; b=ledger.read_bytes(); target=D/'before-admin.ledger.raw.snapshot.jsonl';target.write_bytes(b)
 write(D/'before-admin.json',dict(canonical_mappings=before,ledger_prefix=pin(target),ledger_original=pin(ledger)))
 # Exact three signatures are measured from current Lean headers.
 exact=[]
 for i,n in enumerate(claim['lean_files']):
  t=(ROOT/n).read_bytes().replace(b'\r\n',b'\n').decode(); d=claim['lean_declarations'][i].split('.')[-1];m=re.search(r'theorem '+re.escape(d)+r'\b[\s\S]*?(?= := by)',t);assert m
  b=(m.group(0)+'\n').encode(); expected=[(339,'793cd5cc527fdc1a15f995a661a7698553c90507b8f390ebb32bc7dd7322b0c1'),(1404,'463b6d151c6169695063b62edde37a5e88fda4f3b58170cdf707dc069927212d'),(1457,'88ec792a664f0504820630acc96ffe5e07d0c61b28b51fa2d7360ea9b3005e37')][i];assert (len(b),sha(b))==expected
  exact.append(dict(declaration=claim['lean_declarations'][i],LF_bytes=len(b),LF_sha256=sha(b)))
 write(D/'signatures.json',dict(status='PASS',signatures=exact))
 print('PASS prepare',len(names),len(checks),len(inputs),flush=True)
def gates():
 py=sys.executable; claim=load(R/'proved-local.json')
 command('toolchain',[str(ROOT.parent/'unused')]) if False else None
 assert (ROOT/'lean-toolchain').read_text().strip()=='leanprover/lean4:v4.33.0'
 manifest=load(ROOT/'lake-manifest.json');assert any(q['name']=='mathlib' and q['rev']=='db584cd6d46c92f209a44c0f1c829460d327499d' for q in manifest['packages'])
 command('lean-version',['C:/Users/admin/.elan/bin/lean.exe','--version'])
 focused=command('focused',['C:/Users/admin/.elan/bin/lake.exe','build','Tests.ProximalBPSMacroscopicRange'])
 t=(D/'focused.log').read_text(encoding='utf8');assert 'Build completed successfully' in t
 print('COMPILER_CLOSED',focused['actual_PID'],focused['exit_code'],flush=True)
 out=[]
 cmds=[('reviewed-publication',[py,'-B','-X','utf8','-c','from tools.astis_publication import check_advance; check_advance('+repr(claim['lean_declarations'])+',reviewed=True); print("PASS reviewed=True actual declarations3")']),('publication-base',[py,'-B','-X','utf8','tools/astis_publication.py','check','--base','origin/main']),('semantic',[py,'-B','-X','utf8','tools/astis_semantic_roundtrip.py','check']),('frontier',[py,'-B','-X','utf8','tools/astis_frontier_cells.py','check']),('contributor',[py,'-B','-X','utf8','tools/astis_contributor_contract.py','check','--base','origin/main'])]
 for name,args in cmds:out.append(dict(name=name,**command('gate.'+name,args)))
 write(D/'gates.json',dict(status='PASS',focused=focused,records=out,actual_driver_PID=os.getpid()))
if __name__=='__main__':
 D.mkdir(exist_ok=True)
 {'prepare':prepare,'gates':gates}[sys.argv[1]]()
