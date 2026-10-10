from common import *
env=dict(os.environ);env.pop('ELAN_TOOLCHAIN',None);env.update(PYTHONUTF8='1',PYTHONDONTWRITEBYTECODE='1',LEAN_NUM_THREADS='2')
assert git('rev-parse','HEAD')==BASE
commands=[('reviewed-publication',[sys.executable,'-B','-X','utf8','-c',"from tools.astis_publication import check_advance; check_advance(['"+TARGET+"'],reviewed=True); print('PASS actual reviewed check_advance')"]),
 ('publication-base',[sys.executable,'-B','-X','utf8','tools/astis_publication.py','check','--base','origin/main']),
 ('semantic',[sys.executable,'-B','-X','utf8','tools/astis_semantic_roundtrip.py','check']),
 ('frontier',[sys.executable,'-B','-X','utf8','tools/astis_frontier_cells.py','check']),
 ('contributor',[sys.executable,'-B','-X','utf8','tools/astis_contributor_contract.py','check','--base','origin/main'])]
records=[]
for name,cmd in commands:
 log=O/('gate.'+name+'.log');start=utc()
 with log.open('wb') as f:
  proc=subprocess.Popen(cmd,cwd=R,env=env,stdout=f,stderr=subprocess.STDOUT);code=proc.wait()
 record=dict(name=name,command=cmd,process_id=proc.pid,exit_code=code,status='PASS' if code==0 else 'FAILED',started_utc=start,finished_utc=utc(),process_resource='CLOSED',log=pin(log))
 records.append(record);dump('gate.'+name+'.status.json',record)
 dump('gates.json',dict(status='PASS' if all(r['exit_code']==0 for r in records) else 'FAILED',actual_python_driver_PID=os.getpid(),records=records,compiler_started=False,shared_aggregate='NOT_RUN; belongs subsequent root serial integration',checked_commit=BASE))
 print(json.dumps(dict(name=name,PID=proc.pid,exit_code=code)),flush=True)
 assert code==0,(name,log.read_text(encoding='utf-8'))
print('PASS all five actual noncompiler gates; Python children CLOSED')
