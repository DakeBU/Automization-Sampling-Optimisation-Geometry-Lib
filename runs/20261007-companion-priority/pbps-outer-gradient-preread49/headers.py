# -*- coding: utf-8 -*-
import pathlib,json,hashlib,re,sys,html
sys.stdout.reconfigure(encoding='utf-8');r=pathlib.Path('E:/Samplinglib');d=r/'runs/20261007-companion-priority/pbps-outer-gradient-preread49';H=lambda b:hashlib.sha256(b).hexdigest();p=r/'runs/20261007-companion-priority/next-ready-preread47/primary-pbps.raw.snapshot.html';b=p.read_bytes();lines=b.splitlines(keepends=True);bindings=[]
for name,a,z in [('standing',348,363),('laws',616,650),('reflection-macro',3637,3699),('B8B9',3710,3758),('B13',3761,3791),('compact-reduction',4566,4577),('C2',4653,4669)]:
 part=b''.join(lines[a-1:z]);(d/(name+'.raw.html')).write_bytes(part);(d/(name+'.lf.html')).write_bytes(part.replace(b'\r\n',b'\n'));bindings.append(dict(name=name,path=str(p),span=[a,z],whole_raw_sha256=H(b),whole_lf_sha256=H(b.replace(b'\r\n',b'\n')),fragment_raw_sha256=H(part),fragment_lf_sha256=H(part.replace(b'\r\n',b'\n'))))
 print('\nSOURCE',name,a,z)
 for k,line in enumerate(part.decode('utf-8').splitlines(),a):
  tex=re.findall(r'<annotation encoding="application/x-tex">(.*?)</annotation>',line)
  if tex: print(k,html.unescape(' ; '.join(tex)))
  elif '<p ' in line or '<h6 ' in line:print(k,html.unescape(re.sub(r'<[^>]+>',' ',line))[:1400])
(d/'primary-bindings.json').write_text(json.dumps(bindings,indent=2),encoding='utf-8')
files=['ReflectionL2','MacroscopicRepresentative','GibbsAugmentation','GaussianReflection','GaussianAugmentation','ConditionalGradientVariance']
for name in files:
 p=r/'AutoSamplingTheory/ExampleCases/ProximalBPS'/(name+'.lean');b=p.read_bytes();t=b.decode('utf-8-sig');headers=[]
 for m in re.finditer(r'^theorem\s+([^\s{:(]+)',t,re.M):
  end=t.index(':= by',m.start());frag=t[m.start():end];headers.append(dict(declaration=m.group(1),start_line=t[:m.start()].count('\n')+1,end_line=t[:end].count('\n')+1,signature=frag))
  print('\nHEADER',name,m.group(1));print(frag)
 (d/(name+'.public.json')).write_text(json.dumps(dict(path=str(p),whole_raw_sha256=H(b),whole_lf_sha256=H(b.replace(b'\r\n',b'\n')),headers=headers),indent=2,ensure_ascii=False),encoding='utf-8')
