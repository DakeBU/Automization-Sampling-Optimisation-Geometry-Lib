from pathlib import Path
import json,hashlib
ROOT=Path('E:/Samplinglib');OUT=ROOT/'runs/20261007-companion-priority/pbps-actual-ordered-prefix92/next-boundary-preread93'
def sha(b):return hashlib.sha256(b).hexdigest()
def bind(p):
 p=Path(p);p=p if p.is_absolute() else ROOT/p;b=p.read_bytes();return {'path':p.relative_to(ROOT).as_posix(),'raw_sha256':sha(b),'bytes':len(b)}
def write(n,x):
 p=OUT/n;assert not p.exists();p.write_bytes((json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode());return bind(p)
x=json.loads((OUT/'recommendation93.native.json').read_text());changes=[]
for it in x['exact_reuse_interfaces']:
 p=ROOT/it['module']['path'];lines=p.read_bytes().splitlines(keepends=True)
 actual=next(i+1 for i,line in enumerate(lines) if line.decode().startswith('theorem '+it['declaration']))
 if actual!=it['declaration_line']:changes.append({'declaration':it['declaration'],'old_line':it['declaration_line'],'correct_line':actual})
 it['declaration_line']=actual
 if 'ActualFiniteJumpRecursion' in str(p):
  start=16;end=next(i for i,line in enumerate(lines) if i>15 and line.decode().startswith('set_option maxHeartbeats'))
 elif 'ActualNonaccumulation' in str(p):
  start=15;end=next(i for i,line in enumerate(lines) if i>14 and line.decode().startswith('set_option maxHeartbeats'))
 elif 'UnitExponentialProduct' in str(p):start=17;end=26
 else:continue
 it['statement_region']={'start_line':start,'end_line':end,'raw_sha256':sha(b''.join(lines[start-1:end]))}
x['pointer_correction']={'predecessor':bind(OUT/'recommendation93.native.json'),'changes':changes,'meaning':'Exact line-pointer correction only; all source expectation, mathematical statement and recommendation unchanged. Predecessor preserved.'}
r=write('recommendation93.v2.native.json',x)
old=json.loads((OUT/'closed-RAW93.native.json').read_text());inputs=old['inputs']+old['outputs']+[bind(OUT/'closed-RAW93.native.json')]
m=write('closed-RAW93.v2.native.json',{'record_kind':'closed-bounded-preread-exact-pointer-successor','inputs':inputs,'outputs':[r,bind(OUT/'correct-interface-pointers93.py')],'closure':'All inputs and outputs rehashed; use recommendation93.v2.native.json for exact interface line pointers. All original files immutable. Planning only.'})
for i in inputs+[r,bind(OUT/'correct-interface-pointers93.py')]:assert bind(i['path'])==i
print(json.dumps({'report':r,'manifest':m,'pointer_corrections':changes},indent=2))
