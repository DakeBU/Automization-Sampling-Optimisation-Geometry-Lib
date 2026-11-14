import json, os, pathlib
from record import ROOT, REPO, run, sha
C=ROOT/'candidate'
closure=json.loads((ROOT/'closure.json').read_text())
toolchain=json.loads((ROOT/'toolchain.json').read_text())
manifest=json.loads((C/'lake-manifest.json').read_text())
search=[str(C/'out')]+[str(REPO/'.lake/packages'/p['name']/'.lake/build/lib/lean') for p in manifest['packages']]
env={'LEAN_PATH':os.pathsep.join(search),'LEAN_SRC_PATH':str(C)}
(ROOT/'lean-env.json').write_text(json.dumps(env,indent=2)+'\n')
results=[]
for mod in closure['topological_order']:
    f=mod.replace('.','/')+'.lean'; out=C/'out'/mod.replace('.','/')
    out.parent.mkdir(parents=True,exist_ok=True)
    dep=run('lean-deps-'+mod,[toolchain['lean'],'--deps',f],cwd=C,env=env,show=False)
    assert dep.returncode==0,(mod,dep.stderr.decode())
    actual=[]
    for line in dep.stdout.decode().splitlines():
        if '/AutoSamplingTheory/' in line or '/Tests/' in line:
            rel=pathlib.Path(line).relative_to(C/'out').with_suffix('')
            actual.append('.'.join(rel.parts))
    expected=[x for x in closure['modules'][mod]['imports'] if x.startswith(('AutoSamplingTheory.','Tests.'))]
    assert sorted(actual)==sorted(expected),(mod,actual,expected)
    p=run('compile-'+mod,[toolchain['lean'],'-o',str(out)+'.olean','-i',str(out)+'.ilean',f],cwd=C,env=env,show=False)
    info={'module':mod,'exit':p.returncode,'source_sha256':sha((C/f).read_bytes()),'actual_direct_ASTIS_imports':actual,'olean_sha256':sha(pathlib.Path(str(out)+'.olean').read_bytes()) if p.returncode==0 else None}
    results.append(info)
    (ROOT/'compile-results.json').write_text(json.dumps(results,indent=2)+'\n')
    print(json.dumps(info),flush=True)
    if p.returncode: raise RuntimeError(p.stdout.decode()+p.stderr.decode())
print('ALL_NINE_MODULES_RECOMPILED_FROM_EMPTY_OUTPUT',flush=True)
