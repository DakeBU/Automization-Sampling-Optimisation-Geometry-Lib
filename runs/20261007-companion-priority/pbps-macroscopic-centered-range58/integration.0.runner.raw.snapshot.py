from pathlib import Path
import subprocess,json,os,datetime,sys,hashlib,re
sys.stdout.reconfigure(encoding='utf-8')
r=Path('runs/20261007-companion-priority/pbps-macroscopic-centered-range58')
j=lambda p:json.loads(Path(p).read_text(encoding='utf-8'))
def w(p,d):Path(p).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
now=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
head=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()
v=j(r/'root.exact-verification58.adoption.json');assert v['verified_commit']==head and v['native_verified']
assert j(r/'exact-verification58/lease.json')['status']=='CLOSED'
lease=r/'root.integration.0.lease.json';assert not lease.exists()
d=dict(status='OPEN',compiler='OPEN',Python='OPEN',read='OPEN',write='OPEN',opened_utc=now(),proof_commit=head,scope='Serialized58 actual PBPS macroscopic centered range Registry500/shared Measure/ExampleCases/root Tests; originalPhaseKernel sole stabilization owner.')
w(lease,d);code=1
env=os.environ.copy();env.update(PYTHONUTF8='1',LEAN_NUM_THREADS='2',ASTIS_PUBLIC_SOURCE_LINKS='1',ELAN_TOOLCHAIN='leanprover/lean4:v4.33.0')
commands=[('tests',['lake','build','Tests']),('mandatory',[sys.executable,'tools/astis.py','check']),('pycompile',[sys.executable,'-m','py_compile','tools/astis.py']),('whitespace',['git','-c','core.whitespace=cr-at-eol','diff','--check']),('publication',[sys.executable,'tools/astis_publication.py','check','--base','origin/main']),('semantic',[sys.executable,'tools/astis_semantic_roundtrip.py','check']),('frontier',[sys.executable,'tools/astis_frontier_cells.py','check']),('contributor',[sys.executable,'tools/astis_contributor_contract.py','check','--base','origin/main']),('site-build',[sys.executable,'website/scripts/build_site.py']),('official-graph',[sys.executable,'website/scripts/underlying_lean_graph.py']),('graph',[sys.executable,'tools/astis_publication.py','graph-check','--cell','ASTIS-SHARED-l2-pullback-range','--output','_site']),('graph-macro',[sys.executable,'tools/astis_publication.py','graph-check','--cell','ASTIS-SW-PBPS-macroscopic-centered-range','--output','_site']),('graph-consumer',[sys.executable,'tools/astis_publication.py','graph-check','--cell','ASTIS-SW-PBPS-centered-macro-defect-gap','--output','_site']),('site-check',[sys.executable,'website/scripts/check_site.py'])]
try:
 for label,args in commands:
  log=r/('integration.0.'+label+'.log');assert not log.exists();start=now();print('Starting '+label,flush=True)
  with log.open('wb') as out:p=subprocess.run(args,env=env,stdout=out,stderr=subprocess.STDOUT)
  status=dict(exit_code=p.returncode,command=args,proof_commit=head,started_utc=start,finished_utc=now(),log_raw_sha256=hashlib.sha256(log.read_bytes()).hexdigest())
  w(r/('integration.0.'+label+'.status.json'),status)
  if p.returncode:print(log.read_text(encoding='utf-8',errors='replace')[-4500:],flush=True);raise SystemExit(p.returncode)
  if label=='mandatory':
   text=log.read_text(encoding='utf-8');jobs=[int(x) for x in re.findall(r'Build completed successfully \((\d+) jobs\)',text)];assert len(jobs)>=2 and 'ASTIS check passed' in text
   for cid in j(r/'publication-plan.json')['active_cells']:
    cp=Path('research-wiki/frontier-cells')/(cid+'.json');c=j(cp);assert c['status']=='independently_verified'
    c['evidence']['serialized_shared_gate']=dict(evidence=(r/'integration.0.mandatory.status.json').as_posix(),root_jobs=jobs[0],test_jobs=jobs[1],registry_count=500,status='PASS',proof_commit=head,scope='Actual serialized root/Test aggregate58; main/live/PURIFIED separate.')
    w(cp,c)
   d['compiler']='CLOSED';d['compiler_closed_utc']=now();w(lease,d)
  print('PASS '+label,flush=True)
 code=0
finally:
 d.update(status='CLOSED',compiler='CLOSED',Python='CLOSED',read='CLOSED',write='CLOSED',closed_utc=now(),exit_code=code);w(lease,d)
