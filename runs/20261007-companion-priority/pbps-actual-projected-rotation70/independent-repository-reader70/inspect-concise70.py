import sys
sys.dont_write_bytecode=True
sys.stdout.reconfigure(encoding='utf-8')
import pathlib,json,os
O=pathlib.Path(__file__).resolve().parent;R=O.parent;I=R/'integration70';B=pathlib.Path('E:/Samplinglib')
print('PID',os.getpid())
for q in json.loads((O/'packet140.current-input-pins.json').read_bytes())['inputs']:
 p=pathlib.Path(q['path'])
 if p.name=='receipt.json' and I in p.parents:
  x=json.loads(p.read_bytes());print('GATE',p.parent.name,{k:x.get(k) for k in ['actual_foreground_PID','exit_code','terminal_closed','checked_parent','command']})
  if p.parent.name in ['mandatory-astis-check-final','browser-full-current','python-regression-suite','reader-cdp-capture','reader-copy-download']:
   print('STDOUT', (p.parent/'stdout.log').read_text(encoding='utf-8')[-3500:])
for n in ['integration70/visual70/render-capture.json','integration70/visual70/copy-capture.json','visual.inspection.json','resume-state70/receipt.json']:
 p=R/n;x=json.loads(p.read_bytes());print('\nRECORD',n)
 for k,v in x.items():
  if isinstance(v,list): print(k,'list',len(v),json.dumps(v[:2],ensure_ascii=False)[:2500])
  elif isinstance(v,dict):print(k,'dict',list(v),json.dumps(v,ensure_ascii=False)[:1200])
  else:print(k,v)
for n in ['website/content/publications/pbps-actual-projected-rotation.json','website/content/declaration_lessons/pbps-actual-projected-rotation.json','research-wiki/frontier-cells/ASTIS-SW-PBPS-actual-projected-rotation.json']:
 x=json.loads((B/n).read_bytes());print('\nMETADATA',n)
 for k,v in x.items():
  print(k,json.dumps(v,ensure_ascii=False)[:2000])
