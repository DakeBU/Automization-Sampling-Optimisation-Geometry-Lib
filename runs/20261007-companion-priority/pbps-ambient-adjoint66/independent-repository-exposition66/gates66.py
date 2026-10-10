import os,sys,pathlib,subprocess,json,datetime,hashlib
ROOT=pathlib.Path('E:/Samplinglib');O=ROOT/'runs/20261007-companion-priority/pbps-ambient-adjoint66/independent-repository-exposition66'
def sha(b):return hashlib.sha256(b).hexdigest()
def pin(p):
 b=p.read_bytes();return {'path':p.as_posix(),'RAW_bytes':len(b),'RAW_sha256':sha(b),'LF_sha256':sha(b.replace(b'\r\n',b'\n'))}
commands=[('publication-cell-packet',['tools/astis_publication.py','packet','--cell','ASTIS-SW-PBPS-ambient-adjoint-corrector']),('publication-current-context',['tools/astis_publication.py','review-context','--declaration','AutoSamplingTheory.ExampleCases.ProximalBPS.AmbientAdjointCorrector.actual_ambient_adjoint_centered_decomposition']),('affected-cell-graph',['tools/astis_publication.py','graph-check','--cell','ASTIS-SW-PBPS-ambient-adjoint-corrector']),('local-site-readonly',['website/scripts/check_site.py'])]
results=[json.loads((O/'independent-gates-v2/publication-cell-packet/receipt.json').read_bytes())]
for label,args in commands[1:]:
 if label=='publication-current-context':args += ['--item','pbps-ambient-adjoint-corrector']
 cmd=['C:/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe','-X','utf8',*args];p=O/'independent-gates-v3'/label;p.mkdir(parents=True,exist_ok=True);start=datetime.datetime.now(datetime.timezone.utc).isoformat()
 with (p/'stdout.RAW.log').open('wb') as out,(p/'stderr.RAW.log').open('wb') as err:
  child=subprocess.Popen(cmd,cwd=ROOT,stdout=out,stderr=err);pid=child.pid;print(json.dumps({'label':label,'actual_foreground_PID':pid}),flush=True);rc=child.wait()
 j={'schema':'repo66-observed-foreground-readonly-gate-v1','label':label,'wrapper_PID':os.getpid(),'actual_foreground_PID':pid,'exit':rc,'started_utc':start,'finished_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'command':cmd,'cwd':ROOT.as_posix(),'terminal_closed':True,'checked_scoped_INT':'eb3d5ffbb6853f2a0aa4a8c66aefce19d8050176','future67_proof_publication_credit':False,'stdout':pin(p/'stdout.RAW.log'),'stderr':pin(p/'stderr.RAW.log')}
 (p/'receipt.json').write_bytes(json.dumps(j,sort_keys=True,ensure_ascii=False,indent=2).encode()+b'\n');results.append(j)
 assert rc==0,(label,rc)
(O/'independent-gates.result.json').write_bytes(json.dumps({'schema':'repo66-scoped-independent-gates-v1','actual_wrapper_PID':os.getpid(),'gates':results,'status':'PASS','fresh_whole_Lean_build_claimed':False,'root_full_build_and_Python296_reuse_separately_bound':True},sort_keys=True,ensure_ascii=False,indent=2).encode()+b'\n')
print(json.dumps({'PID':os.getpid(),'status':'PASS','gates':len(results)}))
