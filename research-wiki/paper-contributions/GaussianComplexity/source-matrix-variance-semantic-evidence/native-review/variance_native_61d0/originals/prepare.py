from runner import *
import re, shutil
CAND=OUT/'candidate'; CAND.mkdir(exist_ok=False)
manifest=json.loads((OUT/'inputs/lake-manifest.json').read_text())
lean=Path.home()/'.elan/toolchains/leanprover--lean4---v4.33.0/bin/lean'
tool={'executable':str(lean),'sha256':sha(lean.read_bytes()),'version':run('lean-version',[lean,'--version']).decode(),'file':run('lean-file',['file',lean]).decode(),'uname':run('uname',['uname','-a']).decode()}
pkgs=[]; deps=[]
for p in manifest['packages']:
 path=ROOT/'.lake/packages'/p['name']
 head=run('pin-'+p['name'],['git','rev-parse','HEAD'],path).decode().strip()
 status=run('clean-'+p['name'],['git','status','--porcelain','--untracked-files=normal'],path).decode()
 assert head==p['rev'] and not status,(p['name'],head,status)
 pkgs.append({'name':p['name'],'head':head,'pin':p['rev'],'clean':not status})
 lib=path/'.lake/build/lib/lean'
 if lib.exists():deps.append(str(lib))
tool['pins']=pkgs;tool['manifest_sha256']=sha((OUT/'inputs/lake-manifest.json').read_bytes())
files={}; order=[]; imports={}
def loadmod(mod):
 if mod in files:return
 path=mod.replace('.','/')+'.lean'
 b=show(path,'source-'+mod)
 files[mod]=b
 # sources here have conventional standalone imports; later --deps verifies actual inputs
 text=b.decode(); im=[]
 for line in text.splitlines():
  m=re.match(r'\s*(?:public\s+|private\s+|meta\s+)?import\s+(.+?)\s*$',line)
  if m:im+=re.findall(r'[A-Za-z_][\w.]*',m.group(1).split('--')[0])
 imports[mod]=im
 for x in im:
  if x.startswith(('AutoSamplingTheory.','Tests.')):loadmod(x)
 p=CAND/path;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
 order.append(mod)
loadmod('Tests.GaussianComplexityFixedSpectrumSourceMatrixVariance')
for p in ('lakefile.lean','lean-toolchain','lake-manifest.json'):(CAND/p).write_bytes((OUT/'inputs'/p).read_bytes())
lib=CAND/'empty-astis-output';lib.mkdir()
env={'LEAN_PATH':os.pathsep.join([str(lib),*deps]),'LEAN_SRC_PATH':str(CAND),'LEAN_NUM_THREADS':'2'}
seal=json.loads((OUT/'inputs/research-wiki/paper-contributions/GaussianComplexity/source-matrix-variance-statement-seal.json').read_text())
assert sha((OUT/'inputs/research-wiki/paper-contributions/GaussianComplexity/source-matrix-variance-statement-seal.json').read_bytes())=='5f905cafe6035238cebdedd4f841e87b703e741b4c8aa204471d89e4c07e8a14'
for k,exp in [('producer','d5ac54443c79ea7b35b09ddcd6b5e3c40bef081bbe4f196cae5ab3ead35aa2ea'),('actual_private_consumer','95e81a02e5302de9a42e3b60038ffad6195315ac2eca99a4e6abb39978609f7e')]:assert sha(seal[k]['signature'].encode())==exp
sources=[{'module':m,'path':m.replace('.','/')+'.lean','bytes':len(files[m]),'sha256':sha(files[m]),'lines':len(files[m].splitlines()),'imports':imports[m]} for m in order]
data={'commit':COMMIT,'toolchain':tool,'order':order,'sources':sources,'lean':str(lean),'env':env,'candidate':str(CAND),'empty_output_initially':not any(lib.rglob('*')),'no_project_olean_read_or_copied':True}
(OUT/'preparation.json').write_text(json.dumps(data,indent=2));print(json.dumps(data,indent=2))
