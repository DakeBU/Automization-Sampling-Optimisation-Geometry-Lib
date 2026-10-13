from pathlib import Path
import hashlib,json,os,subprocess,sys
o=Path('runs/20261007-companion-priority/pbps-iid-nonaccumulation-preread77');r=o.parent/'pbps-actual-finite-jump-recursion76'
load=lambda p:json.loads(Path(p).read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest();can=lambda x:json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
lp=o/'CLOSED_LAST.json';l=load(lp);assert sha(lp.read_bytes())=='137236e7bb1c2183504ec443ea6854367ce2b2c432f5b36327e8482acccbb5fa'
assert l['status']=='CLOSED_LAST' and l['actor']=='/root/header_math72' and not l['theorem_proved'] and not l['VERIFIED']
run=load(o/'run.json');h=sha(can({k:v for k,v in run.items() if k!='run_sha256'}));assert h==run['run_sha256']==l['run_sha256']=='76f9b495b886013752ae83c769c55ba7d7ae8b5cab3688e342d9d46b68e3db1c'
assert run['complete_named_RAW_payload']['RAW_sha256']=='04e7257e72105cf980295cb716da0e475511f72d5b5a352021ec329fb7b97fe7'
out=Path(os.environ['ASTIS_FOREGROUND_OBSERVER_DIR'])
with (out/'native-readonly.stdout.log').open('wb') as s,(out/'native-readonly.stderr.log').open('wb') as e:
 p=subprocess.Popen([sys.executable,'-B','-X','utf8',str(o/'finalize77.py'),'readonly'],stdout=s,stderr=e);code=p.wait()
assert code==0
v=json.loads((out/'native-readonly.stdout.log').read_text(encoding='utf8').splitlines()[-1]);assert v['status']=='PASS' and v['no_owned_writes'] and v['owned_files']==55 and v['inputs']==22
dest=r/'root.preread77.adoption.json';assert not dest.exists()
dest.write_text(json.dumps(dict(status='SOURCE_API_PLAN_ONLY_NOT_SOURCE_THEOREM_ADMISSION',actual_root_PID=os.getpid(),native_files=55,native_inputs=22,native_run_sha256=h,native_lease=dict(path=lp.as_posix(),RAW_sha256=sha(lp.read_bytes())),native_complete_payload=run['complete_named_RAW_payload'],native_readonly_PID=p.pid,native_readonly_EXIT=code,selected_contract=run['selected_contract'],real_consumer='ActualFiniteJumpRecursion actual finite stopped recursion original-energy waiting increment, then event-time nonaccumulation.',root_binding_to_current_compiled76='Current module frozen1f1ebc18; whole math accepted; source/exactSCI/serialized delivery still pending.',no_SAU_header_proof_or_VERIFIED=True,Goal_complete=False),ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
print('PASS77 CLOSED55 source/API prospective plan adopted only; no claim/header/proof/source/VERIFIED credit.')
