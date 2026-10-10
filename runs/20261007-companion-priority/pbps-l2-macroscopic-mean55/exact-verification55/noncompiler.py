from common import *
env=dict(os.environ);env.update(PYTHONUTF8='1',PYTHONDONTWRITEBYTECODE='1');results=[]
commands=[('publication',['tools/astis_publication.py','check','--base','origin/main']),('semantic',['tools/astis_semantic_roundtrip.py','check']),('frontier',['tools/astis_frontier_cells.py','check']),('contributor',['tools/astis_contributor_contract.py','check','--base','origin/main'])]
for name,args in commands:
 cmd=[sys.executable,'-B']+args;started=utc()
 with (O/(name+'.log')).open('wb') as out:
  p=subprocess.Popen(cmd,cwd=R,env=env,stdout=out,stderr=subprocess.STDOUT);code=p.wait()
 r=dict(name=name,command=cmd,process_id=p.pid,exit_code=code,started_utc=started,closed_utc=utc(),compiler_started=False,Python='CLOSED',log=pin(O/(name+'.log')));results.append(r);dump('noncompiler.status.json',dict(status='PASS' if all(x['exit_code']==0 for x in results) else 'BLOCKED',results=results));assert code==0,r
print(json.dumps(dict(status='PASS',actual_noncompiler_gates=len(results),exits=[r['exit_code'] for r in results])))
