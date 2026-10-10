from pathlib import Path
import json
O=Path(r'E:/Samplinglib/runs/20261007-companion-priority/pbps-ambient-adjoint-preproof66/independent-type-diagnosis66')
p=O/'run-mode-probes.py'
s=p.read_text(encoding='ascii')
s=s.replace("name='%s%d'%(kind,i);p=O/(name+'.lean');p.write_bytes(src.encode('utf-8'))", "name='%s%d'%(kind,i);p=O/(name+'.lean')\n  if (O/(name+'.receipt.json')).exists():\n   print('REUSE completed '+name,flush=True);continue\n  p.write_bytes(src.encode('utf-8'))")
(O/'run-mode-probes-resume.py').write_bytes(s.encode('ascii'))
(O/'runner-output-encoding-negative.json').write_bytes((json.dumps(dict(schema='diagnosis66-observer-negative-v1',runner='run-mode-probes.py',observer_pid=28832,tool_session_id=33077,observed_exit=1,completed_Lean_probe='async-false0',Lean_pid=29640,Lean_exit=1,observer_error='UnicodeEncodeError gbk printing unicode dagger; complete compiler stdout/stderr/receipt already saved; no compiler failure reclassification',resume_policy='skip completed receipt; do not rerun'),sort_keys=True,indent=2)+'\n').encode())