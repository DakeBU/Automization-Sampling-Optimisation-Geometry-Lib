from verify import *
assert git('rev-parse','HEAD')==COMMIT
gates=[]
specs=[('publication',['tools/astis_publication.py','check','--base','origin/main']),('semantic',['tools/astis_semantic_roundtrip.py','check']),('frontier',['tools/astis_frontier_cells.py','check']),('contributor',['tools/astis_contributor_contract.py','check','--base','origin/main'])]
env=dict(os.environ);env['PYTHONUTF8']='1'
for name,args in specs:
 command=[sys.executable,'-B',*args];start=utc()
 with (O/('post.'+name+'.log')).open('wb') as log:
  p=subprocess.Popen(command,cwd=R,env=env,stdout=log,stderr=subprocess.STDOUT);code=p.wait()
 status=dict(command=command,actual_python_process_id=p.pid,exit_code=code,started_utc=start,finished_utc=utc(),log=pin(O/('post.'+name+'.log')),checked_commit=COMMIT,compiler_started=False);dump('post.'+name+'.status.json',status);assert code==0,name;gates.append(status)
dump('post.gates.json',dict(status='PASS',checked_commit=COMMIT,compiler_invocations=0,gates=gates))
strict('inputs.post-gates.json');print(json.dumps(dict(status='PASS',real_post_metadata_gates=4,actual_python_pid=os.getpid(),compiler_invocations=0)))
