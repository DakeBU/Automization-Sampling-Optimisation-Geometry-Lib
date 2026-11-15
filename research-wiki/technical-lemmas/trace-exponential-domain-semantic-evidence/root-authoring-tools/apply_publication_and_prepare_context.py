from pathlib import Path
import json,hashlib,subprocess
r=Path.cwd();w=r/'.astis/huanjian-gc-trace-mgf-domain-20261115'
d=w/'metadata-drafts/publication-v2';e=r/'research-wiki/technical-lemmas/trace-exponential-domain-semantic-evidence'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
expected={
 'lesson':'ef379e3bf9dbd681893bee752eb42820ac0d8c2683690fb8a78ea3703ba3cdbc',
 'publication':'bad17a874c060ef20b260b46781b342b717360dae844d5747043424fc66ceb5d',
 'public_audit':'9a71c8c4b4f1c23ee7afae166a9b1c95c40efb9c04bbec8477455b1df17bfc0e',
 'private_audit':'1a46920c630c81094ef54af7ef9d6a70d31cfc9db3df7c3d8200d1daaf4a3659',
 'private_registry':'16fe8df153ddd0e54ea539a5e7e94beca1346fb4fc5c6b4e1c67e47e6f6c42a3'}
found={}
for key,h in expected.items():
    ps=[p for p in d.glob('*.json') if sha(p)==h];assert len(ps)==1;found[key]=ps[0]
orig=e/'metadata-custody/authored-v2';orig.mkdir(parents=True,exist_ok=True)
for p in found.values():
    dest=orig/p.name;assert not dest.exists();dest.write_bytes(p.read_bytes())
P='AutoSamplingTheory.TechnicalLemmas.Analysis.MatrixTraceExponentialBounds.trace_exp_pos_and_le_card_mul_exp_abs_mul_norm'
assert sha(r/'AutoSamplingTheory/TechnicalLemmas/Analysis/MatrixTraceExponentialBounds.lean')=='1ef6f49fa5f0a8b3b61ba42d31bca1bb744bebb64e433075d0ca25ab82570b76'
assert sha(r/'Tests/GaussianComplexityTraceMgfDomain.lean')=='72311555e65cacc8b129510f2158abc9e2e6a230882a2169f6504e80f394fedb'
native=r/'.astis/semantic-neutral-20261115/trace_exp_native_61e4/native-mathematics-report.v1.json'
assert sha(native)=='51481e488bee3d6de641a61a5dced0bd9bfaa6f7666e64d5c36595f3b0c5c1ca'
old='Local exact-byte builds exist; independent native/source-blind/fresh-source review, reader acceptance, normal PL/V, shared graph/main/site integration and purification remain pending.'
new='Local exact-byte builds and independent immutable301728 native/type+value/kernel checks passed. Source-blind/fresh-source review, reader acceptance, normal PL/V, shared graph/main/site integration and purification remain pending.'
def refresh(x):
    if isinstance(x,dict):return {k:refresh(v) for k,v in x.items()}
    if isinstance(x,list):return [refresh(v) for v in x]
    if isinstance(x,str):return x.replace(old,new)
    return x
lesson=refresh(json.loads(found['lesson'].read_text()));pub=refresh(json.loads(found['publication'].read_text()))
pa=refresh(json.loads(found['public_audit'].read_text()));ta=refresh(json.loads(found['private_audit'].read_text()))
for audit in [pa,ta]:
    assert audit['state']=='draft' and audit['verdict']=='pending' and not audit['reconstruction']
    audit['lean']['compilation_scope']='Root exact-byte focused build in worktree at1db9 before freezing301728; independent native then freshly rebuilt exact301728 ASTIS closure and checked full type/value/kernel/Std3. No future metadata/public commit is retroactively claimed built.'
    audit['lean']['independent_native_evidence']={'file':str(native.relative_to(r)),'sha256':sha(native),'candidate_commit':'30172847ec40c24426f0b39afc4887719810eca0','normal_V_calls':0}
lp=r/'website/content/declaration_lessons/huanjian-trace-exponential-domain.json'
pp=r/'website/content/publications/huanjian-trace-exponential-domain.json'
ap=r/'research-wiki/semantic-roundtrip/audits/huanjian-trace-exponential-domain.json'
regpath=w/'private-consumer-audit.registry.json'
for p,x in [(lp,lesson),(pp,pub),(ap,pa)]:
    assert not p.exists();p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
registry=json.loads(found['private_registry'].read_text());assert len(registry['audits'])==1
registry['audits']=[ta];assert not regpath.exists()
regpath.write_text(json.dumps(registry,ensure_ascii=False,indent=2)+'\n')
raw=subprocess.check_output(['python3','tools/astis_publication.py','review-context','--item','huanjian-trace-exponential-domain','--declaration',P],cwd=r)
context=w/'publication-context.authored-v3.original.json';assert not context.exists();context.write_bytes(raw)
ctx=json.loads(raw)
for audit in [pa,ta]:
    audit['publication_binding_sha256']=ctx['publication_binding_sha256']
    audit['publication_context']=ctx['publication_context']
    audit['binding_status']='ACTUAL_CURRENT_PUBLICATION_CONTEXT_GENERATED; DRAFT_SEMANTIC_REVIEWS_PENDING'
ta['private_module_context']={'file':'Tests/GaussianComplexityTraceMgfDomain.lean','commit':'30172847ec40c24426f0b39afc4887719810eca0','sha256':sha(r/'Tests/GaussianComplexityTraceMgfDomain.lean'),'text':(r/'Tests/GaussianComplexityTraceMgfDomain.lean').read_text()}
ap.write_text(json.dumps(pa,ensure_ascii=False,indent=2)+'\n')
registry['audits']=[ta];regpath.write_text(json.dumps(registry,ensure_ascii=False,indent=2)+'\n')
(e/'private-consumer-audit.draft.v1.json').write_text(json.dumps(ta,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'current_binding_sha256':ctx['publication_binding_sha256'],'context_raw_sha256':sha(context),
 'P_T_immutable_bytes_unchanged':True,'public_audit':'draft','private_audit':'draft','normal_PL_calls':0,'normal_V_calls':0}))
