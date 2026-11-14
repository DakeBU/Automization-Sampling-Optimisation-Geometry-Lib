import hashlib,json,pathlib,sys
from record import ROOT,REPO,EXPECTED_HEAD,MATH_HEAD,run,sha
NATIVE=ROOT.parent
def checked(label,argv,cwd=REPO):
    p,receipt=run(label,argv,cwd)
    assert p.returncode==0,(label,p.stdout.decode(),p.stderr.decode())
    return p.stdout,str(receipt.relative_to(ROOT))
head,_=checked('preflight-held-head',['git','rev-parse','HEAD']);assert head.decode().strip()==EXPECTED_HEAD
clean,_=checked('preflight-tracked-clean',['git','status','--porcelain=v1','--untracked-files=no']);assert clean==b''
paths=[
'AutoSamplingTheory/TechnicalLemmas/Probability/RealMatrixPositiveIntegral.lean',
'AutoSamplingTheory/ExampleCases/GaussianComplexity/FixedSpectrumSourceMatrixVariance.lean',
'Tests/RealMatrixPositiveIntegral.lean',
'website/content/declaration_lessons/huanjian-real-matrix-positive-integral.json',
'website/content/declaration_lessons/huanjian-gaussian-source-matrix-variance.json',
'website/content/publications/huanjian-real-matrix-positive-integral.json',
'website/content/publications/huanjian-gaussian-source-matrix-variance.json',
'lean-toolchain','lake-manifest.json']
bytes_results=[]
for p in paths:
    old,oldr=checked('math-blob-'+p.replace('/','_'),['git','show',MATH_HEAD+':'+p])
    held,heldr=checked('held-blob-'+p.replace('/','_'),['git','show',EXPECTED_HEAD+':'+p])
    working=(REPO/p).read_bytes();snapshot=(NATIVE/'candidate'/p).read_bytes()
    assert old==held==working==snapshot,p
    bytes_results.append({'path':p,'bytes':len(old),'sha256':sha(old),'mathematical_commit_equals_held_equals_working_equals_native_snapshot':True,'math_receipt':oldr,'held_receipt':heldr})
native_tool=json.loads((NATIVE/'toolchain.json').read_text())
lean,_=checked('elan-which-lean',['elan','which','lean']);lean=lean.decode().strip();assert lean==native_tool['lean']
version,_=checked('lean-version',[lean,'--version']);machine,_=checked('lean-binary-file',['file',lean])
assert version.decode().strip()==native_tool['lean_version'];assert sha(pathlib.Path(lean).read_bytes())==native_tool['lean_sha256'];assert b'arm64' in machine
assert sha((REPO/'lean-toolchain').read_bytes())==native_tool['toolchain_sha256']
assert sha((REPO/'lake-manifest.json').read_bytes())==native_tool['manifest_sha256']
manifest=json.loads((REPO/'lake-manifest.json').read_text());native_deps={p['name']:p for p in json.loads((NATIVE/'dependencies.json').read_text())};deps=[]
for p in manifest['packages']:
    d=REPO/'.lake/packages'/p['name'];h,hr=checked('dep-head-'+p['name'],['git','rev-parse','HEAD'],d);s,sr=checked('dep-clean-'+p['name'],['git','status','--porcelain=v1','--untracked-files=all'],d)
    actual=h.decode().strip();assert actual==p['rev']==native_deps[p['name']]['actual'];assert s==b''
    deps.append({'name':p['name'],'revision':actual,'matches_manifest_and_native_snapshot':True,'clean':True,'head_receipt':hr,'clean_receipt':sr})
admission=[]
for slug in ['huanjian-real-matrix-positive-integral','huanjian-gaussian-source-matrix-variance']:
    publication=json.loads((REPO/'website/content/publications'/f'{slug}.json').read_text())
    items=publication['items'] if isinstance(publication,dict) else publication
    ids=[b['audit_id'] for item in items for b in item['bindings']]
    auditfile=REPO/'research-wiki/semantic-roundtrip/audits'/f'{slug}.json';obj=json.loads(auditfile.read_text())
    entries=obj.get('audits',[obj]) if isinstance(obj,dict) else obj
    for auditid in ids:
        audit=next(a for a in entries if a.get('audit_id',a.get('id'))==auditid)
        assert audit['state']=='accepted',(auditid,audit.get('state'))
        admission.append({'audit_id':auditid,'path':str(auditfile.relative_to(REPO)),'file_sha256':sha(auditfile.read_bytes()),'state':audit['state'],'use':'Current admission metadata only. No native or source mathematical re-review; no independent source verdict issued by this verifier.'})
result={'expected_held_HEAD':EXPECTED_HEAD,'mathematical_candidate':MATH_HEAD,'tracked_clean':True,'exact_bytes':bytes_results,'native_snapshot_environment_unchanged':True,'lean_binary_sha256':native_tool['lean_sha256'],'lean_version':native_tool['lean_version'],'toolchain_sha256':native_tool['toolchain_sha256'],'manifest_sha256':native_tool['manifest_sha256'],'dependencies':deps,'current_selected_source_admission_metadata':admission,'no_native_browser_source_math_rerun':True}
(ROOT/'preflight-results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'preflight':'PASS','HEAD':EXPECTED_HEAD,'exact_file_count':len(paths),'dependency_count':len(deps),'admission':admission},indent=2))
