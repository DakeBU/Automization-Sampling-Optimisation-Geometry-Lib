from common import *
sys.stdout.reconfigure(encoding='utf-8')
assert git('rev-parse','HEAD')==BASE
env=dict(os.environ);env.pop('ELAN_TOOLCHAIN',None);env.update(PYTHONUTF8='1',PYTHONDONTWRITEBYTECODE='1',LEAN_NUM_THREADS='2')
jobs=[('publication',['tools/astis_publication.py','check','--base','origin/main']),('semantic',['tools/astis_semantic_roundtrip.py','check']),('frontier',['tools/astis_frontier_cells.py','check']),('contributor',['tools/astis_contributor_contract.py','check','--base','origin/main'])]
results=[]
for name,args in jobs:
 command=[sys.executable,'-B',*args];start=utc()
 with (O/(name+'.log')).open('wb') as log:
  p=subprocess.Popen(command,cwd=R,env=env,stdout=log,stderr=subprocess.STDOUT);code=p.wait()
 result={'name':name,'command':command,'actual_process_PID':p.pid,'exit_code':code,'status':'PASS' if code==0 else 'FAILED','started_utc':start,'closed_utc':utc(),'actual_log':pin(O/(name+'.log')),'compiler_started':False,'background_children':False,'Python':'CLOSED','source':pin(args[0])};dump(name+'.status.json',result);results.append(result);assert code==0,result
dump('gates.json',{'status':'PASS','checked_commit':BASE,'comparison_base':'origin/main','actual_origin_main':git('rev-parse','origin/main'),'gates':results,'remaining_aggregate':'Full shared root/Tests/Registry497/ASTIS mandatory gate only after root serialized integration; not run or credited at exact-science stage.'})
print(json.dumps({'status':'PASS','gates':[{'name':r['name'],'actual_PID':r['actual_process_PID'],'exit_code':r['exit_code']} for r in results]},ensure_ascii=False))
