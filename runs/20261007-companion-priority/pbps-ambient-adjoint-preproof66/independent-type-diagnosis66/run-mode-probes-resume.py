from pathlib import Path
import json,subprocess,hashlib,datetime,os
O=Path(r'E:/Samplinglib/runs/20261007-companion-priority/pbps-ambient-adjoint-preproof66/independent-type-diagnosis66')
H=lambda b:hashlib.sha256(b).hexdigest()
for kind in ['async-false','inline-def']:
 for i in range(2):
  src=(O/('valid-fail%d.lean'%i)).read_text(encoding='utf-8')
  if kind=='async-false':
   src=src.replace('set_option maxHeartbeats 2000000','set_option maxHeartbeats 2000000\nset_option Elab.async false').replace('theorem deliberate_fail%d'%i,'theorem async_false_deliberate_fail%d'%i)
  else:
   src=src.replace('theorem deliberate_fail%d'%i,'def inline_def_deliberate_fail%d'%i)
  name='%s%d'%(kind,i);p=O/(name+'.lean')
  if (O/(name+'.receipt.json')).exists():
   print('REUSE completed '+name,flush=True);continue
  p.write_bytes(src.encode('utf-8'))
  start=datetime.datetime.now(datetime.timezone.utc).isoformat();proc=subprocess.Popen(['lake','env','lean',str(p)],cwd='E:/Samplinglib',stdout=subprocess.PIPE,stderr=subprocess.PIPE);out,err=proc.communicate();(O/(name+'.stdout.log')).write_bytes(out);(O/(name+'.stderr.log')).write_bytes(err)
  d=dict(schema='diagnosis66-neutral-TYPE-terminal-v1',probe=name,actual_foreground_pid=proc.pid,actual_exit_code=proc.returncode,terminal_closed=True,observer_pid=os.getpid(),started_utc=start,finished_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),input_RAW_sha256=H(p.read_bytes()),stdout_RAW_sha256=H(out),stderr_RAW_sha256=H(err),proof_search=False,source_math_change=False)
  (O/(name+'.receipt.json')).write_bytes((json.dumps(d,sort_keys=True,indent=2)+'\n').encode());print(json.dumps(d,sort_keys=True),flush=True);print(out.decode('utf-8')[-4500:],flush=True)