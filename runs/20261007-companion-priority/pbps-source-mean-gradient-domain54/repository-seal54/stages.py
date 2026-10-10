from common import *
assert load(O/'lease.json')['status']=='OPEN'
rows=[]
env=dict(os.environ); env['PYTHONUTF8']='1'; env['PYTHONDONTWRITEBYTECODE']='1'
for stage in ['check','integration','history','graph']:
 command=[sys.executable,'-B',str(O/(stage+'.py'))]; started=utc()
 with (O/(stage+'.1.log')).open('wb') as out:
  proc=subprocess.Popen(command,cwd=R,env=env,stdout=out,stderr=subprocess.STDOUT); code=proc.wait()
 result=dict(stage=stage,command=command,actual_python_PID=proc.pid,exit_code=code,started_utc=started,finished_utc=utc(),log=pin(O/(stage+'.1.log')),compiler_started=False)
 dump(stage+'.1.status.json',result); rows.append(dict(status=pin(O/(stage+'.1.status.json')),**result)); assert code==0,stage
dump('execution.json',dict(status='PASS',actual_runner_python_PID=os.getpid(),commands=rows,compiler_invocations=0,bytecode_disabled=True,PythonUTF8='1'))
print(json.dumps(dict(status='PASS',stages=[dict(stage=x['stage'],actual_python_PID=x['actual_python_PID'],exit_code=x['exit_code']) for x in rows],compiler_invocations=0)))
