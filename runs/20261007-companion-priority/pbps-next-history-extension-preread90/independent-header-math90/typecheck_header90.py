from pathlib import Path
import datetime,hashlib,json,os,subprocess
R=Path('E:/Samplinglib');O=Path(__file__).parent;B=O.parent
H=B/'header90.proposed.lean';MR='1262c82138eb3a7cc502fe4eb6182c10e4e33168a734333ffaec580585935750'
def pin(p):
 b=p.read_bytes();return {'path':p.relative_to(R).as_posix(),'raw_sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b)}
def save(n,v):
 with (O/n).open('x',encoding='utf8',newline='\n') as f:json.dump(v,f,ensure_ascii=False,indent=2);f.write('\n')
assert pin(H)['raw_sha256']==MR
q=O/'Header90.original.exactraw.lean';assert not q.exists();q.write_bytes(H.read_bytes())
save('input-freeze90.typecheck.json',{'status':'EXACT_ORIGINAL_HEADER_FROZEN_BEFORE_OWN_TYPECHECK','header':pin(H),'own_original_snapshot':pin(q),'lean_toolchain':pin(R/'lean-toolchain'),'lake_manifest':pin(R/'lake-manifest.json'),'whole_named_private_Prop':'actual_finite_history_extension_statement','theorem_BODY_created':False,'no_canonical_mutation':True})
env=dict(os.environ,PYTHONUTF8='1',PYTHONIOENCODING='utf8');env.pop('ELAN_TOOLCHAIN',None);env['PATH']=str(R/'.astis/toolchain/lean-4.33.0-windows/bin')+os.pathsep+env['PATH']
args=[str(R/'.astis/toolchain/lean-4.33.0-windows/bin/lake.exe'),'env',str(R/'.astis/toolchain/lean-4.33.0-windows/bin/lean.exe'),str(q)]
start=datetime.datetime.now(datetime.timezone.utc).isoformat()
with (O/'header-original90.stdout.log').open('xb') as out,(O/'header-original90.stderr.log').open('xb') as err:
 child=subprocess.Popen(args,cwd=R,env=env,stdout=out,stderr=err);print('whole original header foreground PID',child.pid,flush=True);code=child.wait()
save('header-original90.receipt.json',{'command':args,'cwd':str(R),'actual_foreground_PID':child.pid,'started_utc':start,'finished_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'exit_code':code,'terminal_closed':True,'source':pin(q),'stdout':pin(O/'header-original90.stdout.log'),'stderr':pin(O/'header-original90.stderr.log'),'typecheck_only_no_proof_credit':True})
print('WHOLE ORIGINAL HEADER EXIT',code,flush=True)
print((O/'header-original90.stdout.log').read_text('utf8')[-4500:])
