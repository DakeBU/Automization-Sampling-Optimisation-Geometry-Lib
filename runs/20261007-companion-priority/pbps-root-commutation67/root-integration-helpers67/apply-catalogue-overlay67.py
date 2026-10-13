from pathlib import Path
import hashlib,json,sys,os
root=Path.cwd();sys.path.insert(0,'tools');import astis_publication as pub,astis_semantic_roundtrip as rt
r=root/'runs/20261007-companion-priority/pbps-root-commutation67';d=r/'citation-catalogue-overlay67'
load=lambda p:json.loads(p.read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest()
proposal=load(d/'proposal.json');vp=r/'independent-source67/citation-catalogue-overlay.verdict.json'
assert sha((d/'proposal.json').read_bytes())=='312d95fce10e80ebf235b74c0612c19b295c1c35323b07eab1208b21667e1b85'
assert sha(vp.read_bytes())=='aa6ad498bab5a4a2217fc4c8e88938051aa3f72a5d7cad1c8157c604457a8dc3'
assert proposal['proposed_binding']=='34ba0bb3a85f58c9dff1405301b46ac15dace416a0dcbc28673f5739adb8742f'
out=r/'applied-reviewed-citation-catalogue67';out.mkdir(exist_ok=False);(out/'independent-open-review-metadata-approval.exactraw.snapshot.json').write_bytes(vp.read_bytes());maps=[]
for i,row in enumerate(proposal['changes']):
 p=root/row['path'];b=p.read_bytes();a=(d/row['after_snapshot']).read_bytes()
 assert sha(b)==row['before_raw_sha256'] and sha(a)==row['after_raw_sha256']
 if i==2:
  before=json.loads(b);after=json.loads(a)
  assert before['reconstruction']==after['reconstruction'] and before['state']==after['state'] and rt.decoder_packet(before)==rt.decoder_packet(after)
 (out/f'{i}.before.exactraw.snapshot.json').write_bytes(b);p.write_bytes(a);(out/f'{i}.after.exactraw.snapshot.json').write_bytes(a)
 maps.append(dict(path=row['path'],before_RAW_sha256=sha(b),after_RAW_sha256=sha(a),before_snapshot=f'{i}.before.exactraw.snapshot.json',after_snapshot=f'{i}.after.exactraw.snapshot.json'))
pub.inputs.cache_clear();pub.load.cache_clear();item=next(x for x in pub.load() if x['id']=='real-l2-positive-square-commutation');audit=load(root/proposal['changes'][2]['path'])
assert pub.binding_digest(item,item['bindings'][0],pub.inputs())==audit['publication_binding_sha256']==proposal['proposed_binding']
packet=r/'source.0.reviewer-packet.json';(out/'source.0.before-catalogue.reviewer-packet.exactraw.snapshot.json').write_bytes(packet.read_bytes());packet.write_text(json.dumps(rt.semantic_reviewer_packet(audit),ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
x=dict(status='EXACT_INDEPENDENTLY_REVIEWED_CITATION_AND_CATALOGUE_FIELDS_APPLIED',actual_root_writer_pid=os.getpid(),finite_maps=maps,independent_approval_RAW_sha256=sha(vp.read_bytes()),approval_owner='/root/independent_source64',final_source67_review_still_OPEN=True,current_binding=audit['publication_binding_sha256'],decoder_packet_unchanged=True,source_mathematical_repair=False,full_Exposition=False)
(out/'applied.json').write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
print('PASS exact reviewed D1 citation and used-API catalogue applied; generic source packet refreshed; final source review remains OPEN.')
