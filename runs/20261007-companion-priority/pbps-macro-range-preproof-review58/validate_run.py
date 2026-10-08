import json,hashlib,os,time,ctypes
from pathlib import Path
B=Path('E:/Samplinglib/runs/20261007-companion-priority/pbps-macro-range-preproof-review58')
def h(b):return hashlib.sha256(b).hexdigest()
def rec(p):
    b=Path(p).read_bytes();l=b.replace(b'\r\n',b'\n');return dict(path=str(p).replace('\\','/'),bytes=len(b),raw_sha256=h(b),lf_bytes=len(l),lf_sha256=h(l))
def load(p):return json.loads(Path(p).read_text(encoding='utf-8'))
def selfcheck(o):
    x=o.copy();v=x.pop('content_self_sha256');assert v==h(json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode())
def check(r):
    got=rec(r['path']);assert all(got[k]==r[k] for k in ['bytes','raw_sha256','lf_bytes','lf_sha256']),r['path'];return got
start=time.monotonic();checks=[]
for p in B.glob('*.json'):
    if p.name in ['validator.json','complete.json','lease.json']:continue
    o=load(p)
    if 'content_self_sha256' in o:selfcheck(o)
for e in load(B/'input.manifest.json')['inputs']:
    for k in ['actual_input','exactraw_snapshot','crlf_to_lf_snapshot']:checks.append(check(e[k]))
for r in load(B/'output.manifest.json')['artifacts']:checks.append(check(r))
for n in ['statement-review.json','topology-review.json']:
    for r in load(B/n).get('signature_receipts',{}).values():checks.append(check(r))
run=load(B/'reviewer.run.json');assert run['statement_verdict']=='ACCEPTED_WITH_EXPLICIT_SETTING_EXTENSION' and run['topology_verdict']=='ACCEPTED_SCOPED';assert not run['proof_claim'] and not run['formal_admission']
v=load(B/'coverage-validation.json');assert all(not r['creator_missing_from_parser'] and not r['independent_extra'] for r in v['independent_parser_results']);assert v['all365_creator_span_hashes_match'] and v['inherited596_primary_byte_hashes_match'] and v['inherited10_citation_exact']
out=dict(actor='/root/statement_topology58',status='INDEPENDENT_REVIEW_READBACK_VALIDATION_PASS',raw_lf_actual_readbacks=checks,resource=dict(pid=os.getpid(),cpu_user_seconds=os.times().user,cpu_system_seconds=os.times().system,wall_seconds=time.monotonic()-start),reviewer_run=rec(B/'reviewer.run.json'),selfhash_recipe='Complete object minus only content_self_sha256; sorted compact ensure_ascii=False UTF8 no newline.')
out['content_self_sha256']=h(json.dumps(out,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode());(B/'validator.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(dict(status='PASS',pid=os.getpid(),readbacks=len(checks),wall_seconds=out['resource']['wall_seconds'])))
