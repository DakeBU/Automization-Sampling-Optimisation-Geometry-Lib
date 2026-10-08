import verify as v,subprocess,sys,os,json
env=dict(os.environ);env['PYTHONUTF8']='1';results=[];prefix=sys.argv[1] if len(sys.argv)>1 else ''
for name,args in [('publication',['tools/astis_publication.py','check','--base','origin/main']),('semantic',['tools/astis_semantic_roundtrip.py','check']),('frontier',['tools/astis_frontier_cells.py','check']),('contributor',['tools/astis_contributor_contract.py','check','--base','origin/main'])]:
 cmd=[sys.executable,*args];opened=v.utc()
 with (v.O/(prefix+name+'.log')).open('wb') as log:
  p=subprocess.Popen(cmd,cwd=v.R,env=env,stdout=log,stderr=subprocess.STDOUT);code=p.wait()
 s=dict(command=cmd,python_pid=p.pid,exit_code=code,opened_utc=opened,closed_utc=v.utc(),log=v.pin(v.O/(prefix+name+'.log')),compiler_started=False)
 v.dump(prefix+name+'.status.json',s);results.append(s);print(json.dumps(dict(name=prefix+name,pid=p.pid,exit_code=code)),flush=True);assert code==0
v.dump(prefix+'protocol-checks.status.json',dict(status='PASS',actual_python_pid=os.getpid(),origin_main=v.git('rev-parse','origin/main'),checked_commit=v.COMMIT,checks=results))
