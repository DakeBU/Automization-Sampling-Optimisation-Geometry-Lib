from pathlib import Path
import copy,hashlib,json,sys
sys.path.insert(0,str(Path.cwd()/'tools'))
import astis_publication as pub
r=Path('runs/20261007-companion-priority/pbps-ambient-adjoint66')
d=r/'reuse-plan-metadata-repair66';d.mkdir(exist_ok=False)
p=Path('research-wiki/frontier-cells/ASTIS-SW-PBPS-ambient-adjoint-corrector.json')
raw=p.read_bytes();before=json.loads(raw);after=copy.deepcopy(before)
extra=['AutoSamplingTheory.TechnicalLemmas.Measure.L2Expectation.one','AutoSamplingTheory.TechnicalLemmas.Measure.L2Expectation.inner_one_eq_integral']
assert all(x in before['proof_digestion']['existing_substrate'] for x in extra)
assert all(x not in before['reuse_plan']['reused_declarations'] for x in extra)
after['reuse_plan']['reused_declarations']+=extra
sha=lambda b:hashlib.sha256(b).hexdigest()
load=lambda p:json.loads(p.read_bytes())
failure=load(r/'contributor-precommit66/receipt.json');assert failure['exit_code']==1 and failure['terminal_closed']
approved=load(r/'presentation-overlay66/independent.verdict.exactraw.json');assert approved['status']=='ACCEPTED_EXACT_METADATA_ONLY'
pub.inputs.cache_clear();pub.load.cache_clear();data=pub.inputs();item=next(x for x in pub.load() if x['id']=='pbps-ambient-adjoint-corrector')
binding=pub.binding_digest(item,item['bindings'][0],data);context=pub.digest(pub.review_context(item,item['bindings'][0],data))
(d/'cell.before.exactraw.snapshot.json').write_bytes(raw)
p.write_text(json.dumps(after,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
pub.inputs.cache_clear();pub.load.cache_clear();data=pub.inputs();item=next(x for x in pub.load() if x['id']=='pbps-ambient-adjoint-corrector')
assert pub.binding_digest(item,item['bindings'][0],data)==binding=='3d1d9d97cc4ae200fb0b07584cc5a89e6805851d05d0c640f3d3e4b3106bdc7f'
assert pub.digest(pub.review_context(item,item['bindings'][0],data))==context=='d668766750b3e3471ea7b0d50fd3d562a81ec2044cdc8c210891f4671e6ca60b'
record=dict(status='PROCESS_ONLY_REUSE_PLAN_MIRROR_CORRECTED_EXACT_SCI66_REVIEW_PENDING',changed_field='reuse_plan.reused_declarations',before=before['reuse_plan']['reused_declarations'],after=after['reuse_plan']['reused_declarations'],before_RAW_sha256=sha(raw),after_RAW_sha256=sha(p.read_bytes()),independent_existing_dependency_approval='presentation-overlay66/independent.verdict.exactraw.json',original_contributor_failure='contributor-precommit66/receipt.json',source_mathematical_repair=False,Lean_statement_BODY_or_published_formula_changed=False,publication_binding_unchanged=binding,publication_context_unchanged=context,closed_native_reviews_unchanged=True,independent_exact_commit_verification_pending=True)
(d/'repair.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
print('PASS exact one reuse_plan field mirrored from independently reviewed proof parents; code,source/publication binding/context unchanged. Exact SCI66 verification pending.')
