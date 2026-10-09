from pathlib import Path
import hashlib,json,os,sys
root=Path.cwd();sys.path.insert(0,str(root/'tools'));import astis_publication as pub,astis_semantic_roundtrip as rt
r=Path('runs/20261007-companion-priority/pbps-b4-corrector-perturbation72');o=r/'reader-status-overlay72.v3'
load=lambda p:json.loads(Path(p).read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest()
def pin(p):
 p=Path(p);b=p.read_bytes();return dict(path=p.as_posix(),RAW_bytes=len(b),RAW_sha256=sha(b),LF_sha256=sha(b.replace(b'\r\n',b'\n')))
def new(p,x):
 p=Path(p);assert not p.exists(),p;p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
dp=Path(sys.argv[1]);d=load(dp);q=load(o/'proposal.json')
assert sha(dp.read_bytes())=='ce7da464bb49166e1576c0cff4f78da77d8aaa500db907d7927d4ca5067bef73'
assert d['decision']=='accept-exact-proposed-metadata-overlay' and d['proposal_RAW_sha256']==sha((o/'proposal.json').read_bytes())
assert d['sixteen_field_claim_checked']==16 and not d['remaining_old_status_occurrences'] and d['math_Lean_BODY_formulas_assumptions_decoder_unchanged']
assert q['status_fields']==16 and q['files']==6 and len(d['rows'])==6 and len(d['packet_mapping'])==2
for z,a in zip(q['rows'],d['rows']):
 assert z['path']==a['path'] and z['before_RAW_sha256']==a['before_RAW_sha256'] and z['proposed_RAW_sha256']==a['approved_proposed_RAW_sha256']
 assert Path(z['path']).read_bytes()==Path(z['before']).read_bytes() and sha(Path(z['proposed']).read_bytes())==z['proposed_RAW_sha256']
 assert q['before'] not in Path(z['proposed']).read_text(encoding='utf8')
for i,(z,a) in enumerate(zip(q['bindings'],d['packet_mapping'])):
 audit=load(z['audit_path']);assert rt.semantic_reviewer_packet(audit)==load(r/f'source-review.packet.{i}.json')
 assert audit['publication_binding_sha256']==z['old_binding']
 packet=load(o/f'source-review.packet.{i+2}.proposed.json')
 assert packet['packet_sha256']==a['approved_packet_sha256']==z['proposed_packet_sha256']
 assert sha((o/f'source-review.packet.{i+2}.proposed.json').read_bytes())==a['approved_packet_raw_sha256']
 assert z['proposed_binding']==a['approved_publication_binding_sha256']
 assert rt.semantic_reviewer_packet(load(o/f'audit.{i}.proposed.json'))==packet
for z in q['rows']:Path(z['path']).write_bytes(Path(z['proposed']).read_bytes())
for i,z in enumerate(q['bindings']):
 Path(z['audit_path']).write_bytes((o/f'audit.{i}.proposed.json').read_bytes())
 target=r/f'source-review.packet.{i+2}.json';assert not target.exists();target.write_bytes((o/f'source-review.packet.{i+2}.proposed.json').read_bytes())
pub.inputs.cache_clear();pub.load.cache_clear();plan=load(r/'publication-plan.json')
for i,slug in enumerate(plan['slugs']):
 item=load(Path('website/content/publications')/(slug+'.json'))['items'][0];audit=load(q['bindings'][i]['audit_path'])
 assert pub.binding_digest(item,item['bindings'][0],pub.inputs())==audit['publication_binding_sha256']
 assert pub.review_context(item,item['bindings'][0],pub.inputs())==audit['publication_context']
pub.check_advance(plan['mathematical_declarations'],reviewed=False)
new(r/'root.reader-status-overlay72.adoption.json',dict(status='EXACT_INDEPENDENTLY_APPROVED_V3_STATUS_OVERLAY_APPLIED_NOT_SOURCE_ADMISSION',actual_root_PID=os.getpid(),independent_decision=pin(dp),proposal=pin(o/'proposal.json'),exact_current=[pin(z['path']) for z in q['rows']],audits=[pin(z['audit_path']) for z in q['bindings']],official_packets=[pin(r/f'source-review.packet.{i+2}.json') for i in range(2)],status_fields=16,mathematical_statement_formula_proof_unchanged=True,review_context_two_status_paths_changed=True,VERIFIED=False))
new(r/'source-review.freeze72.v3.json',dict(status='FINAL_TWO_CURRENT72_OFFICIAL_PACKETS_FROZEN_SOURCE_PENDING',inputs=[pin(z['path']) for z in q['rows']]+[pin(z['audit_path']) for z in q['bindings']]+[pin(r/f'source-review.packet.{i+2}.json') for i in range(2)],source_review=False,VERIFIED=False))
print('PASS exactly approved16 status fields/6 files +2 audit/official packets applied; Lean/math/decoder unchanged; final native source close pending.')
