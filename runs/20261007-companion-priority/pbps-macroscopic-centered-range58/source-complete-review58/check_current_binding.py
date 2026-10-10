import json,hashlib,os
from pathlib import Path
R=Path('E:/Samplinglib');T=R/'runs/20261007-companion-priority/pbps-macroscopic-centered-range58';B=T/'source-complete-review58'
def load(p):return json.loads(Path(p).read_text(encoding='utf-8'))
def can(o):return json.dumps(o,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()
def h(b):return hashlib.sha256(b).hexdigest()
def rec(p):
 b=Path(p).read_bytes();l=b.replace(b'\r\n',b'\n');return dict(path=str(p).replace('\\','/'),raw_bytes=len(b),raw_sha256=h(b),lf_bytes=len(l),lf_sha256=h(l))
def write(n,o):(B/n).write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
p=load(T/'source.2.complete.reviewer-packet.json');item=load(R/'website/content/publications/pbps-centered-macro-defect-gap.json')['items'][0];binding=item['bindings'][0];lesson=load(R/'website/content/declaration_lessons/pbps-centered-macro-defect-gap.json')['units'][0]
def digestfile(path):return h((R/path).read_text(encoding='utf-8').encode())
bp=dict(file=digestfile(p['lean']['file']),current_lean_module=(R/p['lean']['file']).read_text(encoding='utf-8'),toolchain=digestfile('lean-toolchain'),dependencies=digestfile('lake-manifest.json'),source=item['source'],statement=item['statement'],formulae=item['formulae'],assumptions=item['assumptions'],obligations=item['obligations'],lesson=lesson,binding={k:v for k,v in binding.items() if k not in {'audit_id','legacy_audit_debt'}})
assert h(can(bp))==p['publication_binding_sha256']
rc=bp.copy();rc['binding']={k:bp['binding'][k] for k in ['declaration','role','supports']};rc['lesson']={k:v for k,v in lesson.items() if k not in {'boundary','source_history_boundary'}};rc['candidate_assumptions']=[{k:r[k] for k in ['source','lean']} for r in binding['assumption_deltas']];assert rc==p['candidate_publication_context']
result=dict(schema_version=1,status='PASS_EXACT_CURRENT_BINDING_AND_CONTEXT',actor='/root/statement_topology58',publication_binding_sha256=h(can(bp)),reviewer_packet_sha256=p['packet_sha256'],canonical_context_equals_packet=True,actual_toolchain_and_manifest_checked=True,inputs=[rec(R/'lean-toolchain'),rec(R/'lake-manifest.json')],method='Independent direct reconstruction of tools/astis_publication.py binding_payload/review_context from current exact canonical publication, lesson, code and fixed toolchain/manifest; no canonical writes or project imports.')
write('current-publication-binding-check.json',result)
m=load(B/'input.manifest.json');m['supplemental_readonly_inputs'].extend(result['inputs']);m['supplemental_input_count']=len(m['supplemental_readonly_inputs']);assert m['supplemental_input_count']==25;write('input.manifest.json',m)
payload=load(B/'source-review-payload.json');payload['supplemental_input_count']=25;payload['current_binding_check']=rec(B/'current-publication-binding-check.json');payload['results'][0]['current_binding_check']=rec(B/'current-publication-binding-check.json');write('source-review-payload.json',payload)
print(json.dumps(dict(pid=os.getpid(),publication_binding_sha256=result['publication_binding_sha256'],root_inputs=57,supplemental_inputs=25,source_review_payload_sha256=h(can(payload)))))
