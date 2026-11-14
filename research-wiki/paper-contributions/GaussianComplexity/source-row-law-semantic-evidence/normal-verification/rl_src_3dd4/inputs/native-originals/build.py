import json,os,pathlib
from run import ROOT,run,sha
m=json.loads((ROOT/'input-manifest.json').read_text());env=dict(os.environ);env['LEAN_PATH']=os.pathsep.join(m['lean_path']);env.pop('LEAN_SRC_PATH',None)
out=[]
for i,p in enumerate(m['modules']):
    assert all(x.replace('.','/')+'.lean' in m['modules'][:i] for x in m['imports'][p] if x.startswith(('AutoSamplingTheory.','Tests.')))
    dest=ROOT/'native-olean'/pathlib.Path(p).with_suffix('.olean');dest.parent.mkdir(parents=True,exist_ok=True)
    r=run('compile-'+str(i),[m['lean_binary']['path'],'-R',str(ROOT/'scratch'),'-o',str(dest),str(ROOT/'scratch'/p)],cwd=ROOT/'scratch',env=env)
    assert r.returncode==0,p
    out.append({'source':p,'olean':str(dest.relative_to(ROOT)),'sha256':sha(dest.read_bytes())})
(ROOT/'native-build.json').write_text(json.dumps({'candidate':m['candidate_commit'],'outputs':out,'lean_path':m['lean_path']},indent=2)+'\n')
r=run('exact-author-kernel-probe',[m['lean_binary']['path'],'-R',str(ROOT/'scratch'),str(ROOT/'scratch/SourceRowLawKernelProbe.lean')],cwd=ROOT/'scratch',env=env)
assert r.returncode==0
print(json.dumps({'fresh_ASTIS_modules_compiled':len(out),'author_exact_probe_pass':True}))
