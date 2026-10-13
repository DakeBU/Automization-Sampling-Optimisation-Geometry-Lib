import sys
sys.dont_write_bytecode=True
sys.stdout.reconfigure(encoding='utf-8')
import pathlib,json,os
O=pathlib.Path(__file__).resolve().parent;R=O.parent;I=R/'integration70'
print('actual_pid',os.getpid())
for p in [R/'integration.notes.json',R/'verified.json',R/'root.exact-verification70.adoption.json',I/'final-admin.json',I/'generator-sideeffects/receipt.json',I/'resume-after-science-verification.json',R/'visual.inspection.json',I/'visual70/render-capture.json',I/'visual70/copy-capture.json',I/'visual70/inspection-actual-visual-readback.json']:
 if not p.exists(): print('MISSING',str(p));continue
 x=json.loads(p.read_bytes());print('\nFILE',str(p),'KEYS',list(x))
 if p.name in ['verified.json','root.exact-verification70.adoption.json','final-admin.json','inspection-actual-visual-readback.json']:print(json.dumps(x,ensure_ascii=False,indent=2))
 elif p.name=='receipt.json': print(json.dumps({k:v for k,v in x.items() if k not in ['restored','removed','backups','inputs','files']},ensure_ascii=False,indent=2)[:16000])
 elif p.name=='integration.notes.json':
  for k,v in x.items(): print(k,json.dumps(v,ensure_ascii=False)[:7000])
 else:
  for k,v in x.items(): print(k,json.dumps(v,ensure_ascii=False)[:1600])
print('\nGATES')
pins=json.loads((O/'packet140.current-input-pins.json').read_bytes())['inputs']
for q in pins:
 p=pathlib.Path(q['path'])
 if p.name=='receipt.json' and I in p.parents:
  x=json.loads(p.read_bytes()); print(p.parent.name,json.dumps(x,ensure_ascii=False)[:1600]);out=p.parent/'stdout.log';err=p.parent/'stderr.log'
  if out.exists(): print('stdout TAIL',out.read_text(encoding='utf-8',errors='replace')[-2800:])
  if err.exists() and err.stat().st_size: print('stderr TAIL',err.read_text(encoding='utf-8',errors='replace')[-1000:])
