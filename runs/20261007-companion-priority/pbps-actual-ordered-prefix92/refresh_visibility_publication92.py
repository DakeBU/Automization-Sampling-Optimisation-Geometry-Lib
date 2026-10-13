from pathlib import Path
import hashlib,json,sys
ROOT=Path('E:/Samplinglib');RUN=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'tools'))
import astis_publication as pub,astis_semantic_roundtrip as rt
read=lambda p:json.loads(p.read_bytes())
sha=lambda b:hashlib.sha256(b).hexdigest()
def save(p,d):p.write_bytes((json.dumps(d,ensure_ascii=False,indent=2)+'\n').encode())
def fresh(p,d):assert not p.exists(),p;save(p,d)
repair=RUN/'statement-helper-visibility92'
module=ROOT/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualOrderedPrefix.lean'
raw=module.read_bytes();assert sha(raw)==read(repair/'change.json')['after_sha256']
receipt=RUN/'independent-visibility92/leaf-build.receipt.native.json'
r=read(receipt);assert r['exit_code']==0 and r['source']['raw_sha256']==sha(raw)
lp=ROOT/'website/content/declaration_lessons/pbps-actual-ordered-prefix.json'
ap=ROOT/'research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261011-PBPSActualOrderedPrefix.json'
pp=ROOT/'website/content/publications/pbps-actual-ordered-prefix.json'
for p,label in [(lp,'lesson')]:
 q=repair/(label+'.before.exactraw.json');assert not q.exists();q.write_bytes(p.read_bytes())
lesson=read(lp);old=read(repair/'lesson.before.exactraw.json')
for s in lesson['units'][0]['steps']:
 reg=s['lean_source_region'];code=b''.join(raw.splitlines(keepends=True)[reg['start_line']-1:reg['end_line']])
 reg['source_raw_sha256']=sha(raw);reg['exact_code_raw_sha256']=sha(code)
 s['lean']=code.decode().rstrip()
save(lp,lesson)
a=read(ap);assert a['state']=='blind-reconstructed'
a['lean']['compiler_evidence']=receipt.relative_to(ROOT).as_posix()
a['lean']['statement_representation']['private_definition']='private '+a['lean']['statement_representation']['private_definition']
a['lean']['statement_representation']['kernel_header_and_literal_expansion_checked']=False
a['lean']['statement_representation'].pop('independent_kernel_evidence',None)
pub.inputs.cache_clear();pub.load.cache_clear();item=read(pp)['items'][0]
a['publication_binding_sha256']=pub.binding_digest(item,item['bindings'][0],pub.inputs())
a['publication_context']=pub.review_context(item,item['bindings'][0],pub.inputs())
assert rt.decoder_packet(a)==read(ROOT/'runs/semantic-roundtrip/anonymous92/input.json')
save(ap,a)
packet=rt.semantic_reviewer_packet(a);fresh(RUN/'anti-anchored.review92.v3.json',packet)
fresh(repair/'refreeze.json',dict(module_raw_sha256=sha(raw),publication_binding_sha256=a['publication_binding_sha256'],
    reviewer_packet_sha256=packet['packet_sha256'],reviewer_packet_raw_sha256=sha((RUN/'anti-anchored.review92.v3.json').read_bytes()),
    anonymous_packet_unchanged=True,public_Prop_unchanged=True,independent_rename_math_pending=True))
pub.check_advance([a['lean']['declaration']],reviewed=False)
print(json.dumps(read(repair/'refreeze.json')))
