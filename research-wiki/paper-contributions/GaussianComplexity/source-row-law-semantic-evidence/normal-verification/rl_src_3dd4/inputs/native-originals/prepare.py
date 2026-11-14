"""Freeze candidate bytes, recursively derive imports, verify actual native environment."""
import json,os,pathlib,platform,re
from run import ROOT,REPO,run,sha
C='d0654e9bbed44ab852fc44598560799949d8bd12'
P='AutoSamplingTheory/ExampleCases/GaussianComplexity/FixedSpectrumSourceRowLaw.lean'
T='Tests/GaussianComplexityFixedSpectrumSourceRowLaw.lean'
E='research-wiki/paper-contributions/GaussianComplexity/source-row-law-semantic-evidence'
files={};modules=[];imports={}
def freeze(p):
    if p in files:return (ROOT/'inputs'/p).read_bytes()
    r=run('freeze-'+str(len(files)),['git','show',C+':'+p]);assert r.returncode==0,p
    d=ROOT/'inputs'/p;d.parent.mkdir(parents=True,exist_ok=True);d.write_bytes(r.stdout)
    files[p]={'sha256':sha(r.stdout),'bytes':len(r.stdout),'worktree_equal':(REPO/p).read_bytes()==r.stdout}
    assert files[p]['worktree_equal'],p
    return r.stdout
def visit(p):
    if p in modules:return
    data=freeze(p).decode();xs=re.findall(r'^import\s+([^\s]+)',data,re.M);imports[p]=xs
    for n in xs:
        if n.startswith(('AutoSamplingTheory.','Tests.')):visit(n.replace('.','/')+'.lean')
    modules.append(p)
visit(P);visit(T)
assert files[P]['sha256']=='c370caf377c5d56c97bdb1012d407049e63b04998011df327de79c46fb2b1201'
assert files[T]['sha256']=='ed2c97bd4d49c9ebcabc7ecf24ce3eba91a972e5e634fb3c694f6eff7a496715'
protocols=['AGENTS.md','CONTRIBUTING.md','docs/contributor-codex-contract.md','docs/theorem-publication-protocol.md','docs/proof-digestion-protocol.md','docs/evidence-routed-memory-protocol.md','.agents/skills/astis-substantive-advance/SKILL.md','.agents/skills/astis-semantic-roundtrip/SKILL.md']
selected=protocols+['lean-toolchain','lake-manifest.json','lakefile.lean','research-wiki/paper-contributions/GaussianComplexity/source-row-law-statement-seal.json',E+'/publication-draft-record.json',E+'/source-lean-map.draft.json','website/content/declaration_lessons/huanjian-gaussian-source-row-law.json','website/content/publications/huanjian-gaussian-source-row-law.json']
for p in selected:freeze(p)
manifest=(ROOT/'inputs/lake-manifest.json').read_bytes();assert sha(manifest)=='b83ca83b9cf7caa85fa8b023c2ff9a3fb7a7cce7e1c332e810c348535ec49c37'
deps=[]
for d in json.loads(manifest)['packages']:
    path=REPO/'.lake/packages'/d['name']
    h=run('package-'+d['name']+'-head',['git','rev-parse','HEAD'],cwd=path)
    s=run('package-'+d['name']+'-clean',['git','status','--porcelain=v1','--untracked-files=all'],cwd=path)
    assert h.returncode==s.returncode==0 and h.stdout.decode().strip()==d['rev'] and not s.stdout,d['name']
    deps.append({'name':d['name'],'head':d['rev'],'clean_including_untracked':True,'cache':str(path/'.lake/build/lib/lean')})
assert len(deps)==9
lean=pathlib.Path.home()/'.elan/toolchains/leanprover--lean4---v4.33.0/bin/lean'
v=run('lean-native-version',[str(lean),'--version']);assert v.returncode==0 and b'4.33.0' in v.stdout and b'd8b18978322de05a8f3dba51ef03cf5461676c17' in v.stdout
f=run('lean-native-file',['file',str(lean)]);assert f.returncode==0 and b'arm64' in f.stdout
h=run('head-initial',['git','rev-parse','HEAD']);assert h.stdout.decode().strip()==C
run('worktree-initial',['git','status','--short','--untracked-files=all'])
scratch=ROOT/'scratch';scratch.mkdir(exist_ok=True)
for p in modules:
    d=scratch/p;d.parent.mkdir(parents=True,exist_ok=True);d.write_bytes((ROOT/'inputs'/p).read_bytes())
oleans=ROOT/'native-olean';oleans.mkdir(exist_ok=True);assert not list(oleans.rglob('*'))
probe=REPO/'.astis/huanjian-gc-source-row-law-20261112/SourceRowLawKernelProbe.lean'
(ROOT/'inputs/SourceRowLawKernelProbe.lean').write_bytes(probe.read_bytes())
(scratch/'SourceRowLawKernelProbe.lean').write_bytes(probe.read_bytes())
files['private:SourceRowLawKernelProbe.lean']={'sha256':sha(probe.read_bytes()),'bytes':probe.stat().st_size,'origin':str(probe.relative_to(REPO))}
m={'candidate_commit':C,'platform':platform.platform(),'modules':modules,'imports':imports,'files':files,'dependencies':deps,'lean_binary':{'path':str(lean),'sha256':sha(lean.read_bytes())},'lean_version':v.stdout.decode().strip(),'lean_path':[str(oleans)]+[d['cache'] for d in deps],'empty_astis_output_before_build':True,'all_ASTIS_sources_from_candidate':True,'no_ASTIS_cached_oleans_copied':True}
(ROOT/'input-manifest.json').write_text(json.dumps(m,indent=2)+'\n')
print(json.dumps({'candidate':C,'closure_modules':modules,'lean':m['lean_binary'],'dependencies':len(deps),'frozen_files':len(files)},indent=2))
