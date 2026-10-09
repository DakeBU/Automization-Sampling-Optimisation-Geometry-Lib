from pathlib import Path
import json, re, hashlib, html, os, sys
sys.stdout.reconfigure(encoding='utf-8')
ROOT=Path('E:/Samplinglib')
OWN=Path(__file__).resolve().parent
PRE=ROOT/'runs/20261007-companion-priority/pbps-clock-construction-preread75'
PRIMARY=ROOT/'runs/20261007-companion-priority/phase-pbps-gamma-preread57/primary-pbps.exactraw.snapshot.html'
def sha(b): return hashlib.sha256(b).hexdigest()
def dump(p,x): p.write_text(json.dumps(x,ensure_ascii=False,sort_keys=True,indent=2)+'\n',encoding='utf-8',newline='\n')
def textview(s):
 s=re.sub(r'<math\b[^>]*alttext="([^"]*)"[^>]*>[\s\S]*?</math>',lambda m:' $'+html.unescape(m[1])+'$ ',s)
 return re.sub(r'\s+',' ',html.unescape(re.sub(r'<[^>]+>',' ',s))).strip()
def main():
 b=PRIMARY.read_bytes(); assert len(b)==1482128 and sha(b)=='d81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760'
 lease=json.loads((PRE/'lease.final.json').read_bytes()); assert lease['status']=='CLOSED_LAST' and lease['owned_count']==86
 for p in lease['all_owned_outputs_except_only_self']:
  d=(ROOT/p['path']).read_bytes(); assert len(d)==p['RAW_bytes'] and sha(d)==p['RAW_sha256'] and sha(d.replace(b'\r\n',b'\n'))==p['LF_sha256'],p['path']
 regions=json.loads((PRE/'source.regions.json').read_bytes())['regions']
 lines=b.splitlines(keepends=True)
 for r in regions:
  z=b''.join(lines[r['start_line']-1:r['end_line']]); assert z==(ROOT/r['literal_RAW_slice']['path']).read_bytes(),r['anchor']
  s=z.decode(); print('\nREGION',r['anchor'],'start',sum(map(len,lines[:r['start_line']-1])),'math',len(re.findall(r'<math\b',s)))
  for m in re.finditer(r'<p\b[^>]*>[\s\S]*?</p>|<table\b[^>]*class="[^"]*ltx_equation[^"]*"[^>]*>[\s\S]*?</table>|<h[1-6]\b[^>]*>[\s\S]*?</h[1-6]>',s):
   ids=re.findall(r'\bid="([^"]+)"',m[0])
   print('BLOCK',ids[:3],textview(m[0]))
 print('\nSTANDING SEARCH')
 s=b.decode()
 for m in re.finditer(r'<p\b[^>]*>[\s\S]*?</p>|<table\b[^>]*class="[^"]*ltx_equation[^"]*"[^>]*>[\s\S]*?</table>',s):
  v=textview(m[0])
  if ('C^{2}' in v or '\\alpha I' in v or '0<\\alpha' in v or '\\beta\\eta' in v) and m.start()<s.index('id="S3"'):
   print('SUPPLEMENT',re.findall(r'\bid="([^"]+)"',m[0])[:4],m.start(),m.end(),v)
 print(json.dumps({'actual_PID':os.getpid(),'actual_EXIT':0,'CLOSED86_all85members_verified':True,'primary_RAW_sha256':sha(b)},sort_keys=True))
 dump(OWN/'terminal.inspect75.json',{'actual_PID':os.getpid(),'actual_EXIT':0,'CLOSED86_all85members_verified':True,'primary_RAW_sha256':sha(b),'scope':'read only primary and CLOSED86; no future header/body'})
if __name__=='__main__': main()
