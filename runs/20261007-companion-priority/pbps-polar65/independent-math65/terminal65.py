import datetime,json,os,pathlib,subprocess,sys
O=pathlib.Path(__file__).resolve().parent
PY='C:/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe'
mode=sys.argv[1];assert mode in ['finalize','readback']
name={'finalize':'finalizer','readback':'readback'}[mode]
assert not (O/'lease.final.json').exists() and not (O/(name+'.terminal.json')).exists()
start=datetime.datetime.now(datetime.timezone.utc).isoformat()
with (O/(name+'.stdout.log')).open('wb') as out,(O/(name+'.stderr.log')).open('wb') as err:
    p=subprocess.Popen([PY,'-B','-X','utf8',str(O/'closure65.py'),mode],cwd='E:/Samplinglib',stdout=out,stderr=err)
    print(json.dumps({'event':'START','stage':name,'actual_worker_pid':p.pid,'actual_runner_pid':os.getpid()}),flush=True)
    code=p.wait()
receipt={'stage':name,'actual_worker_pid':p.pid,'actual_runner_pid':os.getpid(),'exit_code':code,'terminal_closed':True,'started_utc':start,'finished_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'command':[PY,'-B','-X','utf8',str(O/'closure65.py'),mode]}
(O/(name+'.terminal.json')).write_bytes((json.dumps(receipt,ensure_ascii=False,sort_keys=True,indent=2)+'\n').encode('utf-8'))
print(json.dumps({'event':'TERMINAL',**receipt}),flush=True)
sys.exit(code)
