from pathlib import Path
import json
O=Path(r'E:/Samplinglib/runs/20261007-companion-priority/pbps-ambient-adjoint66/independent-source66');p=O/'check-decoded-TeX.py';s=p.read_text(encoding='ascii');(O/'check-decoded-TeX.failed-layout.py').write_bytes(p.read_bytes());start=s.index(" if 'items' in d:");end=s.index('\n out.append',start)
new=""" fields=[]
 def walk(v,path=''):
  if isinstance(v,dict):
   for k,x in v.items():
    q=path+'.'+k if path else k
    if k in ['formula','tex'] and isinstance(x,str):fields.append((q,x))
    else:walk(x,q)
  elif isinstance(v,list):
   for j,x in enumerate(v):walk(x,path+'[%d]'%j)
 walk(d)"""
s=s[:start]+new+s[end:];p.write_bytes(s.encode('ascii'));(O/'negative.TeX-observer-layout.json').write_bytes((json.dumps(dict(schema='source66-preserved-observer-negative-v1',tool_chunk='8f72b1',actual_tool_exit=1,pid_not_captured=True,issue='Exposition draft units differ from lesson-unit shape; KeyError in observer, no candidate defect. Bounded recursive formula-field collector used next.',candidate_failure=False),sort_keys=True,indent=2)+'\n').encode())