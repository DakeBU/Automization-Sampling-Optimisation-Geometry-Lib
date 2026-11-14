import ast,json,pathlib,re,sys,shutil
from record import ROOT,REPO,COMMIT,run,sha
C=ROOT/'candidate'; OUT=ROOT/'bounded-site'; OUT.mkdir(exist_ok=True)
def extract(path):
    p=run('renderer-input-'+path.replace('/','_'),['git','show',COMMIT+':'+path],show=False)
    assert p.returncode==0,path
    d=C/path;d.parent.mkdir(parents=True,exist_ok=True);d.write_bytes(p.stdout);return d
inventory=run('renderer-python-inventory',['git','ls-tree','-r','--name-only',COMMIT,'tools','website/scripts'],show=False).stdout.decode().splitlines()
modulemap={pathlib.Path(p).stem:p for p in inventory if p.endswith('.py')}
seen=set()
def module(name):
    if name in seen or name not in modulemap:return
    seen.add(name);d=extract(modulemap[name]);tree=ast.parse(d.read_text())
    for node in ast.walk(tree):
        if isinstance(node,ast.Import):
            for a in node.names:module(a.name.split('.')[0])
        elif isinstance(node,ast.ImportFrom) and node.module:module(node.module.split('.')[0])
for n in ['astis_site','declaration_lessons','publication_reader']:module(n)
slugs=['huanjian-real-matrix-positive-integral','huanjian-gaussian-source-matrix-variance']
units=[];items=[]
for slug in slugs:
    obj=json.loads(extract('website/content/declaration_lessons/'+slug+'.json').read_text());units.extend(obj['units'] if isinstance(obj,dict) else obj)
    obj=json.loads(extract('website/content/publications/'+slug+'.json').read_text());items.extend(obj['items'] if isinstance(obj,dict) else obj)
sys.path[:0]=[str(C/'tools'),str(C/'website/scripts')]
import astis_site as base,inline_lean,declaration_lessons as lessons,publication_reader as reader,astis_publication as publication,source_lineage
modules,decls=base.scan_project_sources();base._SOURCE_BY_NAME={d.full_name:d for d in decls};base._ALL_MODULES=modules
base._ACTIVE_GIT=base.GitContext(COMMIT,'fixed-candidate','https://github.com/DakeBU/Automization-Sampling-Optimisation-Geometry-Lib','https://github.com/DakeBU/Automization-Sampling-Optimisation-Geometry-Lib',False,False,set())
base._ACTIVE_GATE=base.GateEvidence(False,False,COMMIT,'','','' if False else [],'Bounded fixture; no repository/root gate asserted.')
data={'lessons':{u['declaration']:u for u in units},'audits':{},'cells':{},'declarations':base._SOURCE_BY_NAME}
publication.inputs=lambda:data
paths=[]
base.write_page(OUT,'textbook/index.html',base.page('Bounded fixture theme seed','textbook/index.html','<p>Bounded fixture theme seed only.</p>',extra_head='<link rel="stylesheet" href="../assets/information-architecture.css">'))
for u in units:
    for src in u.get('sources',[]):
        if src.get('path') and not src['path'].startswith('.lake/') and not (C/src['path']).exists():extract(src['path'])
lessons.export_sources(OUT,units)
for m in modules:
    rel='modules/'+base.slugify(m.name)+'.html';base.write_page(OUT,rel,base.render_source_module(m,[]))
    download=OUT/'downloads/lean'/m.source_file;download.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(C/m.source_file,download)
for slug,u in zip(slugs,units):
    rel='lessons/'+slug+'.html';base.write_page(OUT,rel,source_lineage.canonical_shell(base.page(u['title'],rel,lessons.render_unit(u,rel),extra_head='<link rel="stylesheet" href="../assets/proof-readers.css">'),rel,OUT));paths.append({'kind':'lesson','slug':slug,'path':rel,'declaration':u['declaration']})
for slug,item in zip(slugs,items):
    rel='proofs/'+slug+'.html';base.write_page(OUT,rel,source_lineage.canonical_shell(base.page(item['title'],rel,reader.source_card(item,rel),extra_head='<link rel="stylesheet" href="../assets/proof-readers.css">'),rel,OUT));paths.append({'kind':'publication','slug':slug,'path':rel,'id':item['id']})
static=['site.css','site.js','proof-readers.css','math-reader.js','source-lineage.css','library-shelves.css','information-architecture.css']
vendor=run('renderer-vendor-inventory',['git','ls-tree','-r','--name-only',COMMIT,'website/static/vendor/mathjax@3.2.2'],show=False).stdout.decode().splitlines()
for path in ['website/static/'+x for x in static]+vendor:
    source=extract(path);target=OUT/'assets'/path.removeprefix('website/static/');target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(source,target)
style_todo=list((OUT/'assets').glob('*.css')); style_seen=set()
while style_todo:
    sheet=style_todo.pop()
    if sheet in style_seen:continue
    style_seen.add(sheet)
    for raw in re.findall(r'@import\s+(?:url\()?\s*[\'"]([^\'"]+)[\'"]',sheet.read_text()):
        target=(sheet.parent/raw).resolve();relative=target.relative_to(OUT/'assets').as_posix()
        source=extract('website/static/'+relative);target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(source,target);style_todo.append(target)
(ROOT/'renderer-manifest.json').write_text(json.dumps({'commit':COMMIT,'production_python_modules':sorted(seen),'pages':paths,'lesson_count':len(units),'publication_count':len(items),'fixture_limitations':['Bounded fixture uses fixed production render_unit, source_card, page, render_source_module and source export functions.','No full build, canonical navigation/global graph or owner integration certification.','Audit data intentionally empty to preserve independent source-role separation; all publication bindings unverified.','No author/source-fidelity verdict is inferred.']},indent=2)+'\n')
print(json.dumps({'pages':paths,'module_source_pages':len(modules),'python_renderer_modules':len(seen),'vendor_assets':len(vendor)},indent=2))
