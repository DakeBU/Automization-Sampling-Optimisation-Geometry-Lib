from runner import *
import ast, re
names=set((OUT/'bootstrap-1.stdout').read_text().splitlines())
C=OUT/'candidate'
seen=set()
def take(path):
 p=OUT/'inputs'/path
 b=p.read_bytes() if p.exists() else show(path,'reader-input-'+path.replace('/','__'))
 dest=C/path;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(b)
 return b
def pythonfile(path):
 if path in seen:return
 seen.add(path);b=take(path)
 for n in ast.walk(ast.parse(b.decode())):
  mods=[]
  if isinstance(n,ast.Import):mods=[x.name.split('.')[0] for x in n.names]
  elif isinstance(n,ast.ImportFrom) and n.module:mods=[n.module.split('.')[0]]
  for m in mods:
   for folder in ['website/scripts/','tools/']:
    p=folder+m+'.py'
    if p in names:pythonfile(p);break
for p in ['website/scripts/declaration_lessons.py','website/scripts/publication_reader.py','website/scripts/source_lineage.py']:pythonfile(p)
for kind in ['declaration_lessons','publications']:take(f'website/content/{kind}/huanjian-gaussian-source-matrix-variance.json')
assets=set()
def asset(path):
 if path in assets:return
 assets.add(path);b=take(path)
 if path.endswith('.css'):
  for url in re.findall(r'(?:@import\s+(?:url\()?|url\()\s*[\'\"]?([^\'\"\s);]+)',b.decode()):
   if url.startswith(('data:','http:','https:')):continue
   target=str(Path(path).parent/url.split('?')[0])
   if target in names:asset(target)
for n in ['site.css','information-architecture.css','proof-readers.css','source-lineage.css','site.js','math-reader.js']:
 asset('website/static/'+n)
for path in sorted(names):
 if path.startswith('website/static/vendor/mathjax@3.2.2/'):
  asset(path)
(OUT/'reader-input-inventory.json').write_text(json.dumps({'python_modules':sorted(seen),'assets':sorted(assets),'bounded_theme_seed':['site.css','information-architecture.css','proof-readers.css'],'global_late_overlays_not_executed':True,'audit_and_cell_maps':'empty / unverified; no foreign verdict read'},indent=2))
print(len(seen),'Python modules,',len(assets),'assets')
