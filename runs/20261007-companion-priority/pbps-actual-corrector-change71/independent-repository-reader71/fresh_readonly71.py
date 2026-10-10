import concurrent.futures,hashlib,json,os,pathlib,subprocess,datetime
ROOT=pathlib.Path('E:/Samplinglib')
OWN=ROOT/'runs/20261007-companion-priority/pbps-actual-corrector-change71/independent-repository-reader71'
PY='C:/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe'
CHECKS={'publication-reviewed':['tools/astis_publication.py','check','--base','origin/main'],'graph-actual':['tools/astis_publication.py','graph-check','--cell','ASTIS-SW-PBPS-actual-corrector-change'],'site-final':['website/scripts/check_site.py'],'contributor-reviewed':['tools/astis_contributor_contract.py','check','--base','origin/main']}
def pin(p):
 b=p.read_bytes();return {'path':p.as_posix(),'RAW_bytes':len(b),'RAW_sha256':hashlib.sha256(b).hexdigest(),'LF_sha256':hashlib.sha256(b.replace(b'\r\n',b'\n')).hexdigest()}
def check(pair):
 label,args=pair;cmd=[PY,'-B','-X','utf8']+args
 out=OWN/(label+'.stdout');err=OWN/(label+'.stderr');start=datetime.datetime.now(datetime.timezone.utc).isoformat();env=dict(os.environ);env['PYTHONDONTWRITEBYTECODE']='1'
 with out.open('wb') as a,err.open('wb') as b:
  proc=subprocess.Popen(cmd,cwd=ROOT,stdout=a,stderr=b,env=env);pid=proc.pid;rc=proc.wait()
 d={'label':label,'command':cmd,'cwd':ROOT.as_posix(),'actual_foreground_PID':pid,'driver_PID':os.getpid(),'exit_code':rc,'terminal_closed':True,'started_UTC':start,'finished_UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'stdout':pin(out),'stderr':pin(err),'read_only':True}
 (OWN/(label+'.receipt.json')).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
 print(json.dumps({k:d[k] for k in ['label','actual_foreground_PID','driver_PID','exit_code','terminal_closed']}),flush=True);return d
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex: results=list(ex.map(check,CHECKS.items()))
(OWN/'fresh-checks71.json').write_text(json.dumps({'driver_PID':os.getpid(),'checks':results,'all_terminal_EXIT0':all(x['exit_code']==0 for x in results)},ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
raise SystemExit(0 if all(x['exit_code']==0 for x in results) else 1)
