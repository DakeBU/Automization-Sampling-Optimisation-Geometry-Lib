from pathlib import Path
import json,hashlib
r=Path.cwd();w=r/'.astis/huanjian-gc-matrix-laplace-20261114'
src=r/'.astis/semantic-neutral-20261114/laplace_fresh_source_8d2a'
e=r/'research-wiki/technical-lemmas/matrix-laplace-tail-semantic-evidence/source-review/laplace_fresh_source_8d2a'
e.mkdir(parents=True,exist_ok=True)
def copy(rel):
    p=src/rel;b=p.read_bytes();out=e/rel;out.parent.mkdir(parents=True,exist_ok=True)
    if out.exists():assert out.read_bytes()==b
    else:out.write_bytes(b)
    return str(out.relative_to(r))
for rel in ['phase1/PHASE1_FROZEN.json','phase2/PHASE2_FROZEN.json','phase2/literal_module_static_review.md',
 'phase3/PHASE3_OLD_D38_INPUTS_FROZEN.json','citation_repair_v3/citation-repair.review.json',
 'citation_repair_v3/CITATION_REPAIR_V3_FROZEN.json','phase3_v4/PHASE3_V4_FROZEN.json']:
    copy(rel)
def attach(a,name):
    result_path=copy('phase3_v4/'+name+'.source-review.json')
    run_path=copy('phase3_v4/'+name+'.review-run.json')
    v=json.loads((r/result_path).read_text());run=(r/run_path).read_bytes()
    assert hashlib.sha256(run).hexdigest()==v['review_run_sha256']
    assert v['publication_binding_sha256']==a['publication_binding_sha256']=='159708e68a0601d85a6081464aa654ea80b7b58cbf0fa41ac697a03fcd8e4346'
    assert v['independent_from_formalizer'] is True and v['independent_from_decoder'] is True
    assert v['blocking_delta_count']==0 and v['verdict']=='equivalent-after-elaboration'
    assert v['runtime_reader_acceptance'] is False
    a['state']='source-reviewed';a['semantic_slots']=v['semantic_slots'];a['deltas']=v['deltas']
    a['verdict']=v['verdict'];a['repairs']=v['repairs']
    a['source_review']={'state':'accepted','reviewer':v['reviewer'],
      'independent_from_formalizer':v['independent_from_formalizer'],
      'independent_from_decoder':v['independent_from_decoder'],
      'reviewer_packet_sha256':v['reviewer_packet_sha256'],
      'review_run_sha256':v['review_run_sha256'],'run_artifact':run_path,
      'evidence':v['review_evidence']}
    a['independent_scope_verdict']=v['scope_verdict']
    a['source_review_original_custody']={'original_result':str((src/'phase3_v3'/(name+'.source-review.json')).relative_to(r)),
      'portable_exact_result':result_path,'portable_exact_run':run_path,
      'result_sha256':hashlib.sha256((r/result_path).read_bytes()).hexdigest(),
      'copy_is_not_reauthored_reviewer_evidence':True}
    a['reader_acceptance']='PENDING actual native browser and independent visual review; source review alone is not reader acceptance'
    return a
p=r/'research-wiki/semantic-roundtrip/audits/huanjian-matrix-laplace-tail.json'
a=attach(json.loads(p.read_text()),'P');p.write_text(json.dumps(a,ensure_ascii=False,indent=2)+'\n')
p=w/'private-consumer-audit.registry.json';reg=json.loads(p.read_text());reg['audits'][0]=attach(reg['audits'][0],'T')
base=json.loads((r/'research-wiki/semantic-roundtrip/registry.json').read_text());reg['protocol']=base['protocol']
p.write_text(json.dumps(reg,ensure_ascii=False,indent=2)+'\n')
(r/'research-wiki/technical-lemmas/matrix-laplace-tail-semantic-evidence/private-consumer-audit.source-reviewed.v4.json').write_text(json.dumps(reg['audits'][0],ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'P_and_private_T':'source-reviewed within exact independently declared scoped source restatements',
 'reviewer':'/root/laplace_fresh_source_8d2a','ROOT_source_verdicts':0,'normal_V_calls':0,'actual_browser_acceptance':'pending'}))
