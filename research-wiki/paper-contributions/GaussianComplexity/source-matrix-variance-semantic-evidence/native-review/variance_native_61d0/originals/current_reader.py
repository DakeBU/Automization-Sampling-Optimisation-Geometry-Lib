from runner import *
import shutil
READER='1d0dedf3aac3c2ff72ee96566461e29e38a2eeae'
files=['website/content/declaration_lessons/huanjian-gaussian-source-matrix-variance.json','website/content/publications/huanjian-gaussian-source-matrix-variance.json']
parent=run('reader-parent',['git','rev-parse',READER+'^']).decode().strip();assert parent==COMMIT
diff=run('reader-exact-diff',['git','diff','--no-ext-diff',COMMIT,READER,'--',*files]).decode()
unchanged=run('reader-math-renderer-diff',['git','diff','--no-ext-diff',COMMIT,READER,'--','AutoSamplingTheory','Tests','lean-toolchain','lakefile.lean','lake-manifest.json','website/scripts','website/static','tools/astis_site.py','research-wiki/paper-contributions/GaussianComplexity/source-matrix-variance-statement-seal.json'])
assert not unchanged
changes=[]
def delta(a,b,p=''):
 if isinstance(a,dict) and isinstance(b,dict):
  assert set(a)==set(b)
  for k in a:delta(a[k],b[k],p+'/'+k)
 elif isinstance(a,list) and isinstance(b,list):
  assert len(a)==len(b)
  for i,(x,y) in enumerate(zip(a,b)):delta(x,y,p+'/'+str(i))
 elif a!=b:changes.append({'pointer':p,'before':a,'after':b})
for f in files:
 b=run('reader-current-'+f.replace('/','__'),['git','show',READER+':'+f]);p=OUT/'inputs-reader-1d0'/f;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
 old=json.loads((OUT/'inputs'/f).read_bytes());new=json.loads(b);delta(old,new,f)
 (OUT/'candidate'/f).write_bytes(b)
assert len(changes)==2 and {x['pointer'].split('/')[-1] for x in changes}=={'scope','boundary'},changes
for x in changes:assert 'EXPLORING' not in x['after'] and 'acceptance is pending' not in x['after']
(OUT/'reader-succession.json').write_text(json.dumps({'math_compiled_commit':COMMIT,'reader_commit':READER,'reader_parent':parent,'only_author_delta':changes,'math_renderer_css_seal_manifest_unchanged':True,'author_sha256':{f:sha((OUT/'inputs-reader-1d0'/f).read_bytes()) for f in files}},indent=2))
src=(OUT/'build_reader.py').read_text().replace("SITE=OUT/'reader-site'","SITE=OUT/'reader-site-1d0'").replace("(OUT/'reader-build.json')","(OUT/'reader-build-1d0.json')").replace("'commit':COMMIT","'math_compiled_commit':COMMIT,'reader_commit':'"+READER+"'")
(OUT/'build_reader_1d0.py').write_text(src)
run('reader-build-1d0',['python3',OUT/'build_reader_1d0.py'])
src=(OUT/'check_browser.py').read_text().replace("SITE=OUT/'reader-site';B=OUT/'browser'","SITE=OUT/'reader-site-1d0';B=OUT/'browser-1d0'").replace("OUT/'reader-build.json'","OUT/'reader-build-1d0.json'").replace("run('chrome-version'","run('chrome-version-1d0'").replace("OUT/'browser-report.json'","OUT/'browser-report-1d0.json'").replace("'commit':COMMIT","'math_compiled_commit':COMMIT,'reader_commit':'"+READER+"'")
(OUT/'check_browser_1d0.py').write_text(src)
print('Exact two author string changes; fixed math/renderer/assets unchanged; current fixture generated')
