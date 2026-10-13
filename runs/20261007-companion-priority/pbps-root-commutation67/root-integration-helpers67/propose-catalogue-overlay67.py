from pathlib import Path
import copy,hashlib,json,sys
root=Path.cwd();sys.path.insert(0,'tools');import astis_publication as pub
r=root/'runs/20261007-companion-priority/pbps-root-commutation67';d=r/'citation-catalogue-overlay67';d.mkdir(exist_ok=False)
load=lambda p:json.loads(p.read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest()
paths=[root/'website/content/publications/real-l2-positive-square-commutation.json',root/'website/content/declaration_lessons/real-l2-positive-square-commutation.json',root/'research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261009-RealL2PositiveSquareCommutation.json']
values=[load(p) for p in paths];after=copy.deepcopy(values)
old='https://arxiv.org/html/2609.06905v1#A2';new='https://arxiv.org/html/2609.06905v1#A4.SS1'
assert after[0]['items'][0]['source']['url']==old;after[0]['items'][0]['source']['url']=new
assert after[1]['units'][0]['sources'][0]['url']==old;after[1]['units'][0]['sources'][0]['url']=new
removed=['ContinuousLinearMap.codRestrict','ContinuousLinearMap.isSelfAdjoint_iff_isSymmetric','IsSelfAdjoint.commute_iff','LinearIsometryEquiv.conjStarAlgEquiv','abs_real_inner_le_norm']
deps=after[1]['units'][0]['mathlib_dependencies'];assert all(x in deps for x in removed)
after[1]['units'][0]['mathlib_dependencies']=[x for x in deps if x not in removed]
data=copy.deepcopy(pub.inputs());item=after[0]['items'][0];data['lessons'][item['bindings'][0]['declaration']]=after[1]['units'][0]
after[2]['publication_binding_sha256']=pub.binding_digest(item,item['bindings'][0],data);after[2]['publication_context']=pub.review_context(item,item['bindings'][0],data)
changes=[]
for i,(p,x) in enumerate(zip(paths,after)):
 b=p.read_bytes();a=(json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode();(d/f'{i}.before.exactraw.snapshot.json').write_bytes(b);(d/f'{i}.after.exactraw.snapshot.json').write_bytes(a)
 changes.append(dict(path=p.relative_to(root).as_posix(),before_raw_sha256=sha(b),after_raw_sha256=sha(a),before_snapshot=f'{i}.before.exactraw.snapshot.json',after_snapshot=f'{i}.after.exactraw.snapshot.json'))
x=dict(status='PROPOSED_NOT_APPLIED_REQUIRES_INDEPENDENT_METADATA_REVIEW',kind='PRECISE_CITATION_AND_USED_API_CATALOGUE_ONLY',changes=changes,exact_source_url_before=old,exact_source_url_after=new,removed_actual_only_catalogue_items=removed,retained_used_Mathlib_catalogue=after[1]['units'][0]['mathlib_dependencies'],before_binding=values[2]['publication_binding_sha256'],proposed_binding=after[2]['publication_binding_sha256'],Lean_statement_proof_BODY_formulas_source_statement_blind_packet_unchanged=True,source_mathematical_repair=False)
(d/'proposal.json').write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
print('Prepared exact generic D1 citation/used-API catalogue proposal; no canonical changes.')
