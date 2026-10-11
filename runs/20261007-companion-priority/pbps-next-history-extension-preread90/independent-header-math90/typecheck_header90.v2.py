from pathlib import Path
import datetime,hashlib,json,os,subprocess
R=Path('E:/Samplinglib');O=Path(__file__).parent;B=O.parent
def pin(p):
 b=p.read_bytes();return {'path':p.relative_to(R).as_posix(),'raw_sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b)}
def put(n,v):
 with (O/n).open('x',encoding='utf8',newline='\n') as f:json.dump(v,f,ensure_ascii=False,indent=2);f.write('\n')
H=B/'header90.v2.proposed.lean';assert pin(H)['raw_sha256']=='5c976dcfe91fe074db71ddbf13385086735c41c273e937b0c6ef432b7dba9037'
old=(O/'Header90.original.exactraw.lean').read_bytes();closing=b'end AutoSamplingTheory.ExampleCases.ProximalBPS.ActualFiniteHistoryExtension\n'
assert old.endswith(closing) and H.read_bytes()==old[:-len(closing)]+b'end\n'+closing
q=O/'Header90.v2.root-proposed.exactraw.lean';assert not q.exists();q.write_bytes(H.read_bytes())
probe=O/'Header90.v2.full-private-check.lean';assert not probe.exists();probe.write_bytes(H.read_bytes().replace(b'\nend\n'+closing,b'\n#check actual_finite_history_extension_statement\nend\n'+closing,1))
put('scope-only-successor90.diagnosis.json',{'status':'ORIGINAL_SCOPE_SYNTAX_FAILURE_ROOT_INDEPENDENT_SUCCESSOR_REVIEWED','original':pin(O/'Header90.original.exactraw.lean'),'original_receipt':pin(O/'header-original90.receipt.json'),'root_candidate':pin(H),'own_exact_v2_snapshot':pin(q),'whole_private_Prop_and_all_other_bytes_identical':True,'only_delta':'Insert standalone end LF before named namespace end to close anonymous noncomputable section.','root_is_exact_successor_proposer':'Root supplied candidate before reviewer created any own proposal; this reviewer assesses it independently.','local_probe':pin(probe),'probe_overlay':'Only add local #check privateProp inside its namespace; no proof theorem/body/placeholder or mathematical change.'})
env=dict(os.environ,PYTHONUTF8='1',PYTHONIOENCODING='utf8');env.pop('ELAN_TOOLCHAIN',None);env['PATH']=str(R/'.astis/toolchain/lean-4.33.0-windows/bin')+os.pathsep+env['PATH']
for n,p in [('header-v2-exact90',q),('header-v2-private-check90',probe)]:
 args=[str(R/'.astis/toolchain/lean-4.33.0-windows/bin/lake.exe'),'env',str(R/'.astis/toolchain/lean-4.33.0-windows/bin/lean.exe'),str(p)];start=datetime.datetime.now(datetime.timezone.utc).isoformat()
 with (O/(n+'.stdout.log')).open('xb') as out,(O/(n+'.stderr.log')).open('xb') as err:
  child=subprocess.Popen(args,cwd=R,env=env,stdout=out,stderr=err);print(n,'foreground PID',child.pid,flush=True);code=child.wait()
 put(n+'.receipt.json',{'command':args,'cwd':str(R),'actual_foreground_PID':child.pid,'started_utc':start,'finished_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'exit_code':code,'terminal_closed':True,'source':pin(p),'stdout':pin(O/(n+'.stdout.log')),'stderr':pin(O/(n+'.stderr.log')),'typecheck_only_no_proof_credit':True})
 print(n,'EXIT',code,flush=True);assert code==0
