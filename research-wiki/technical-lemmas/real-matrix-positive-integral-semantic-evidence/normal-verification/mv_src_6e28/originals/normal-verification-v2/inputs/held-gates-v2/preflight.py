import json,pathlib
from record import ROOT,REPO,EXPECTED_HEAD,PARENT_HEAD,MATH_HEAD,run,sha
NATIVE=ROOT.parent;V1=NATIVE/'held-gates'
def checked(label,argv,cwd=REPO):
    p,r=run(label,argv,cwd);assert p.returncode==0,(label,p.stdout.decode(),p.stderr.decode());return p.stdout,str(r.relative_to(ROOT))
head,_=checked('preflight-head',['git','rev-parse','HEAD']);assert head.decode().strip()==EXPECTED_HEAD
parent,_=checked('preflight-parent',['git','rev-parse',EXPECTED_HEAD+'^']);assert parent.decode().strip()==PARENT_HEAD
status,_=checked('preflight-tracked-clean',['git','status','--porcelain=v1','--untracked-files=no']);assert status==b''
inventory_path=next((ROOT/'receipts').glob('*-diff-inventory.json'));inv=json.loads(inventory_path.read_text());inventory=(inventory_path.parent/inv['stdout_file']).read_bytes();assert sha(inventory)==inv['stdout_sha256']
changes=[row.split('\t',1) for row in inventory.decode().splitlines()]
cell='research-wiki/frontier-cells/ASTIS-SW-GAUSSIAN-COMPLEXITY-source-matrix-variance.json'
assert [p for s,p in changes if s=='M']==[cell]
assert all(s in ['M','A'] for s,p in changes)
before,br=checked('parent-C22',['git','show',PARENT_HEAD+':'+cell]);after,ar=checked('held-C22',['git','show',EXPECTED_HEAD+':'+cell])
old=json.loads(before);new=json.loads(after)
S='AutoSamplingTheory.TechnicalLemmas.Probability.RealMatrixPositiveIntegral.integral_posSemidef'
P='AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumSourceMatrixVariance.actual_source_truncated_matrix_second_moments'
assert old['shared_floor_audit']['canonical_declaration']==S
assert new['shared_floor_audit']['canonical_declaration']==P
normalized=json.loads(after);normalized['shared_floor_audit']['canonical_declaration']=S;assert normalized==old
assert (REPO/cell).read_bytes()==after
prefix='research-wiki/technical-lemmas/real-matrix-positive-integral-semantic-evidence/native-review/psd_native_7b31/held-gates/'
portable=json.loads((V1/'portable-originals-manifest.json').read_text());expected={row['destination']:row for row in portable['entries']}
def expectedfile(source,destination):return {'source':str(source),'destination':destination,'bytes':source.stat().st_size,'sha256':sha(source.read_bytes())}
expected[prefix+'portable-originals-manifest.json']=expectedfile(V1/'portable-originals-manifest.json',prefix+'portable-originals-manifest.json')
for suffix in ['json','stdout','stderr']:
    name='20261112T160904324244Z-freeze-failed-held-gates-phase.'+suffix
    expected[prefix+'post-seal-envelope/'+name]=expectedfile(V1/'receipts'/name,prefix+'post-seal-envelope/'+name)
actual={p for s,p in changes if s=='A' and p.startswith(prefix)};assert actual==set(expected),(actual^set(expected))
custody=[]
for p in sorted(actual):
    data=(REPO/p).read_bytes();assert len(data)==expected[p]['bytes'] and sha(data)==expected[p]['sha256'],p
    custody.append({'path':p,'bytes':len(data),'sha256':sha(data),'matches_v1_original':True})
other=[p for s,p in changes if s=='A' and not p.startswith(prefix)]
snapshot='research-wiki/paper-contributions/GaussianComplexity/source-matrix-variance-semantic-evidence/active-cell-before-canonical-target-correction.original.json'
diagnosis='research-wiki/technical-lemmas/real-matrix-positive-integral-semantic-evidence/consumer-canonical-binding-failure-and-correction.json'
assert set(other)=={snapshot,diagnosis},other
assert (REPO/snapshot).read_bytes()==before
paths=[
'AutoSamplingTheory/TechnicalLemmas/Probability/RealMatrixPositiveIntegral.lean',
'AutoSamplingTheory/ExampleCases/GaussianComplexity/FixedSpectrumSourceMatrixVariance.lean',
'Tests/RealMatrixPositiveIntegral.lean',
'website/content/declaration_lessons/huanjian-real-matrix-positive-integral.json',
'website/content/declaration_lessons/huanjian-gaussian-source-matrix-variance.json',
'website/content/publications/huanjian-real-matrix-positive-integral.json',
'website/content/publications/huanjian-gaussian-source-matrix-variance.json','lean-toolchain','lake-manifest.json']
unchanged=[]
for p in paths:
    data=(REPO/p).read_bytes();original=(NATIVE/'candidate'/p).read_bytes();assert data==original,p
    unchanged.append({'path':p,'bytes':len(data),'sha256':sha(data),'matches_native_math_snapshot':True})
native_tool=json.loads((NATIVE/'toolchain.json').read_text());lean,_=checked('elan-which-lean',['elan','which','lean']);lean=lean.decode().strip();assert lean==native_tool['lean']
version,_=checked('lean-version',[lean,'--version']);assert version.decode().strip()==native_tool['lean_version'];assert sha(pathlib.Path(lean).read_bytes())==native_tool['lean_sha256']
assert sha((REPO/'lean-toolchain').read_bytes())==native_tool['toolchain_sha256'];assert sha((REPO/'lake-manifest.json').read_bytes())==native_tool['manifest_sha256']
manifest=json.loads((REPO/'lake-manifest.json').read_text());previous={p['name']:p for p in json.loads((NATIVE/'dependencies.json').read_text())};deps=[]
for p in manifest['packages']:
    d=REPO/'.lake/packages'/p['name'];h,hr=checked('dep-head-'+p['name'],['git','rev-parse','HEAD'],d);s,sr=checked('dep-clean-'+p['name'],['git','status','--porcelain=v1','--untracked-files=all'],d)
    actual=h.decode().strip();assert actual==p['rev']==previous[p['name']]['actual'] and s==b''
    deps.append({'name':p['name'],'revision':actual,'matches_manifest_and_native':True,'clean':True,'head_receipt':hr,'clean_receipt':sr})
admission=[]
for a in json.loads((V1/'preflight-results.json').read_text())['current_selected_source_admission_metadata']:
    data=(REPO/a['path']).read_bytes();assert sha(data)==a['file_sha256'];obj=json.loads(data);audits=obj.get('audits',[obj]) if isinstance(obj,dict) else obj
    audit=next(x for x in audits if x.get('id',x.get('audit_id'))==a['audit_id']);assert audit['state']=='source-reviewed' and audit['source_review']['state']=='accepted'
    admission.append({'audit_id':a['audit_id'],'path':a['path'],'sha256':sha(data),'state':'source-reviewed','source_review_state':'accepted','use':'Existing admission metadata only; no new source verdict.'})
oldseals={NATIVE/'seal.json':'03dfe1607d2f63743999d17087070253fc05df0a5dafa48161d6974e812e8585',V1/'seal.json':'676e7ebdf582a7a87321937450dbd94dce7e3ccdfb161d9e2d48a4a8f1404320'}
for p,digest in oldseals.items():assert sha(p.read_bytes())==digest
result={'held_HEAD':EXPECTED_HEAD,'parent_failed_held_HEAD':PARENT_HEAD,'mathematical_candidate':MATH_HEAD,'tracked_clean':True,'canonical_pointer_delta':{'path':cell,'json_pointer':'/shared_floor_audit/canonical_declaration','old':S,'new':P,'all_other_JSON_values_unchanged':True,'parent_receipt':br,'held_receipt':ar},'diff_inventory_count':len(changes),'v1_originals_copied_exactly':custody,'additional_provenance_files':[{'path':p,'sha256':sha((REPO/p).read_bytes())} for p in other],'source_author_manifest_files_unchanged':unchanged,'dependencies':deps,'lean_environment_matches_native':True,'selected_source_admission_unchanged':admission,'native_and_v1_seals_unchanged':True,'no_native_browser_source_mathematics_rerun':True}
(ROOT/'preflight-results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'preflight':'PASS','held_HEAD':EXPECTED_HEAD,'canonical_pointer_only_existing_file_delta':True,'exact_v1_originals':len(custody),'added_provenance_files':len(other),'unchanged_code_author_environment_files':len(paths),'dependencies':len(deps)},indent=2))
