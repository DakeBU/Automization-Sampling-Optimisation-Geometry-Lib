from pathlib import Path
exec((Path(__file__).parent/'source_first_extract.py').read_text(encoding='utf-8-sig').split('metadata=')[0])
for k,a in p.ids.items():
 if a.tag=='table' and ('ltx_equation' in a.attrs.get('class','')) and (k.startswith('S2') or k.startswith('A2')):
  z=re.sub(r'\s+',' ',txt(a))
  if any(t in z for t in ['(2.6)','(2.11)','(2.14)','(B.8)','(B.9)','(B.10)','(B.11)','(B.12)','(B.13)','(B.14)','(B.15)']): print(k,z)
for anchor in ['A2.SS2','S2','S1.p1']:
 a=p.ids[anchor]; fragment=s[a.start:a.end]; b=fragment.encode('utf-8')
 with (T/(anchor+'.balanced.html')).open('wb') as f:f.write(b)
 with (T/(anchor+'.source.txt')).open('w',encoding='utf-8',newline='\n') as f:f.write(txt(a))
 print(anchor,'lines',s.count('\n',0,a.start)+1,s.count('\n',0,a.end)+1,'sha256',sha(b))
