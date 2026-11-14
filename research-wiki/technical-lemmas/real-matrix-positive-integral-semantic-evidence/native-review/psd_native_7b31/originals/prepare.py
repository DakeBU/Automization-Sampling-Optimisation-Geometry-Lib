import json, pathlib, re, shutil, sys
from record import ROOT, REPO, COMMIT, run, sha
C=ROOT/'candidate'; C.mkdir(exist_ok=False)
roots=['AutoSamplingTheory.TechnicalLemmas.Probability.RealMatrixPositiveIntegral','AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumSourceMatrixVariance','Tests.RealMatrixPositiveIntegral']
seen={}; order=[]
def extract(path):
    p=run('git-blob-'+path.replace('/','_'),['git','show',COMMIT+':'+path],show=False)
    if p.returncode: raise RuntimeError(path)
    dest=C/path; dest.parent.mkdir(parents=True,exist_ok=True); dest.write_bytes(p.stdout)
    return p.stdout
def visit(mod):
    if mod in seen: return
    data=extract(mod.replace('.','/')+'.lean'); txt=data.decode()
    imports=re.findall(r'^import\s+([A-Za-z0-9_.]+)',txt,re.M)
    seen[mod]={'sha256':sha(data),'imports':imports}
    for dep in imports:
        if dep.startswith(('AutoSamplingTheory.','Tests.')): visit(dep)
    order.append(mod)
for mod in roots: visit(mod)
for path in ['lean-toolchain','lakefile.lean','lake-manifest.json','AGENTS.md','docs/theorem-publication-protocol.md']:
    extract(path)
seals=[('research-wiki/technical-lemmas/real-matrix-positive-integral-statement-seal.json','a5179ed392ef8e55ab470a3a98ebd542e35301f51472e9cdd7bc168a88bafa26','283e07e3c85b9a5cce5c3c40f574f23f593dfcca5e35be4d3e2800f378208b19'),('research-wiki/paper-contributions/GaussianComplexity/source-matrix-variance-statement-seal.json','5f905cafe6035238cebdedd4f841e87b703e741b4c8aa204471d89e4c07e8a14','d5ac54443c79ea7b35b09ddcd6b5e3c40bef081bbe4f196cae5ab3ead35aa2ea')]
seal_result=[]
for path,digest,sigdigest in seals:
    data=extract(path); assert sha(data)==digest
    obj=json.loads(data); prod=obj['producer']; assert sha(prod['signature'].encode())==sigdigest==prod['signature_sha256']
    module=prod['planned_file']; text=(C/module).read_text(); short=prod['name'].split('.')[-1]
    signature=text.split('theorem '+short+'\n',1)[1].split(':= by',1)[0]
    assert signature==prod['signature'], (module,'signature bytes differ')
    seal_result.append({'path':path,'sha256':digest,'name':prod['name'],'signature_sha256':sigdigest,'exact_source_signature_match':True})
(ROOT/'closure.json').write_text(json.dumps({'commit':COMMIT,'roots':roots,'modules':seen,'topological_order':order,'module_count':len(order),'candidate':str(C),'empty_initial_outputs':not any(C.rglob('*.olean'))},indent=2)+'\n')
(ROOT/'seal-results.json').write_text(json.dumps(seal_result,indent=2)+'\n')
manifest=json.loads((C/'lake-manifest.json').read_text()); deps=[]
for package in manifest['packages']:
    d=REPO/'.lake/packages'/package['name']
    h=run('dep-head-'+package['name'],['git','rev-parse','HEAD'],cwd=d,show=False)
    s=run('dep-status-'+package['name'],['git','status','--porcelain=v1','--untracked-files=all'],cwd=d,show=False)
    assert h.returncode==s.returncode==0
    info={'name':package['name'],'expected':package['rev'],'actual':h.stdout.decode().strip(),'clean':not s.stdout,'status_sha256':sha(s.stdout)}
    deps.append(info); assert info['actual']==info['expected']; assert info['clean'],info
(ROOT/'dependencies.json').write_text(json.dumps(deps,indent=2)+'\n')
lean=run('elan-which-lean',['elan','which','lean'],show=False).stdout.decode().strip()
lake=run('elan-which-lake',['elan','which','lake'],show=False).stdout.decode().strip()
version=run('lean-version',[lean,'--version'],show=False)
machine=run('binary-file',['file',lean],show=False)
assert version.returncode==machine.returncode==0
assert b'4.33.0' in version.stdout and b'arm64' in version.stdout and b'arm64' in machine.stdout
info={'lean':lean,'lean_sha256':sha(pathlib.Path(lean).read_bytes()),'lean_version':version.stdout.decode().strip(),'file':machine.stdout.decode().strip(),'lake':lake,'lake_sha256':sha(pathlib.Path(lake).read_bytes()),'toolchain_sha256':sha((C/'lean-toolchain').read_bytes()),'manifest_sha256':sha((C/'lake-manifest.json').read_bytes())}
(ROOT/'toolchain.json').write_text(json.dumps(info,indent=2)+'\n')
(C/'out').mkdir()
print(json.dumps({'toolchain':info,'dependency_count':len(deps),'closure':order,'seal_results':seal_result},indent=2))
