from pathlib import Path
import hashlib, importlib.util, json, os, re, sys
sys.dont_write_bytecode = True
sys.stdout.reconfigure(encoding='utf-8')
ROOT=Path('E:/Samplinglib')
OUT=ROOT/'runs/20261007-companion-priority/pbps-recursive-path-preread76'
def sha(b): return hashlib.sha256(b).hexdigest()
def dump(p,o): p.write_bytes((json.dumps(o,ensure_ascii=False,indent=2,sort_keys=True)+'\n').encode())
def pin(p):
 b=p.read_bytes(); l=b.replace(b'\r\n',b'\n')
 return {'path':p.relative_to(ROOT).as_posix(),'RAW_bytes':len(b),'RAW_sha256':sha(b),'LF_bytes':len(l),'LF_sha256':sha(l),'LF_recipe':'Only bytewise CRLF -> LF; preserve all other bytes.'}
def main():
 primary=ROOT/'runs/20261007-companion-priority/phase-pbps-gamma-preread57/primary-pbps.exactraw.snapshot.html'
 b=primary.read_bytes(); assert len(b)==1482128 and sha(b)=='d81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760'
 helper=ROOT/'runs/20261007-companion-priority/pbps-clock-preproof75/independent-source-baseline75/parse_primary75.py'
 spec=importlib.util.spec_from_file_location('readonly_source_parser75',helper); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
 s=b.decode(); p=m.Parser(s)
 wanted=[]
 for n in p.nodes:
  if n.tag=='p' and n.id in ['S1.p1.1','S2.SS2.p1.1']: wanted.append(n)
  if n.tag=='table' and n.id in ['S1.E1','S2.E7','S2.E8']: wanted.append(n)
  if n.tag=='div' and n.id in ['S2.E7','S2.E8']: wanted.append(n)
  if n.tag in ['math','p'] and n.id.startswith(('S2.E7','S2.E8')): print('QY',n.tag,n.id,len(s[:n.start].encode()),len(s[:n.end].encode()),n.text())
 for n in wanted: print('STANDING/QY',n.tag,n.id,len(s[:n.start].encode()),len(s[:n.end].encode()),n.text())
 for n in p.nodes:
  bo=len(s[:n.start].encode()) if n.id and n.tag in ['p','math'] and n.id.startswith('A1.') else -1
  if 534026<=bo and len(s[:n.end].encode())<=564876 and n.tag in ['p','math']:
   print('A1',n.tag,n.id,bo,len(s[:n.end].encode()),n.text())
 dump(OUT/'inspection.receipt.json',{'schema':'actual-foreground-terminal-receipt-v1','actual_PID':os.getpid(),'actual_EXIT':0,'command':'python -B inspect76.py','primary':pin(primary),'read_only_parser':pin(helper),'new_75_body_read':False,'future_76_header_read':False,'writes':'Only this new owned receipt; imported old parser is read-only, bytecode disabled.'})
 print('ACTUAL_PID',os.getpid(),'EXIT0')
if __name__=='__main__':main()
