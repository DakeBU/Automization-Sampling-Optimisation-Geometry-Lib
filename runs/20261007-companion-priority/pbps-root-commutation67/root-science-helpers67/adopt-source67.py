from pathlib import Path
import hashlib,json,os,sys
root=Path.cwd();sys.path.insert(0,'tools')
import astis_publication as pub,astis_semantic_roundtrip as rt
r=root/'runs/20261007-companion-priority/pbps-root-commutation67';d=r/'independent-source67'
load=lambda p:json.loads(p.read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest();can=lambda x:json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def pin(p):
 b=p.read_bytes();return dict(path=p.resolve().as_posix(),RAW_bytes=len(b),RAW_sha256=sha(b),LF_sha256=sha(b.replace(b'\r\n',b'\n')))
def rawcheck(b,x):
 assert sha(b)==x['RAW_sha256'] and len(b)==x['RAW_bytes']
 assert sha(b.replace(b'\r\n',b'\n'))==x['LF_sha256']
lease=load(d/'lease.final.json');run=load(d/'review-run.json')
assert sha((d/'lease.final.json').read_bytes())=='d1966351cb176ec4f3cc14a3446f7f6002e031c82b29f004eb1ccfc6230736fc'
assert lease['status']=='CLOSED_LAST' and lease['last_owned_write'] and lease['owned_file_count_including_self']==262
assert sha(can({k:v for k,v in run.items() if k!='run_sha256'}))==run['run_sha256']==lease['whole_logical_run_sha256']=='8b6baf92a68e1161bb574eddcb338fa27c9afc326a185801048e5e0d9d8453f1'
files={p.relative_to(d).as_posix():p for p in d.rglob('*') if p.is_file()}
rows=lease['owned_files_except_this_final_lease'];assert set(files)=={x['relative_path'] for x in rows}|{'lease.final.json'} and len(files)==262
for x in rows:rawcheck(files[x['relative_path']].read_bytes(),x)
assert (d/'lease.final.json').stat().st_mtime_ns>=max(p.stat().st_mtime_ns for p in files.values())
expected={'review-run.json':'244601e3a579a2c318c6a7e72c5d8d4e0ffced155e580a18bd452770f6d23856','complete-RAW-decision.json':'e8d090a434f073d9e7c204edbeebbbdf57c6b472e66603da515af3ea88b259d9','RAW-input-payload.json':'3cc9b4ebc286e80a15e05ae046308c7e593fa23ea93ee3e70fb217c43b612ace','source.0.decision.json':'630a4e478817a2d6cecd00fafea47148fe202bf4ff71a3869ac71a8f5ba1f648','source.1.decision.json':'99a8d13f4864db6238773bc8f4063439164ec09403554771aa68068641ece814','owned.manifest.json':'70e0eaadf9e37a4abbbd36a5e7027bc6f70430667b4ed29b69221178857b7eb4'}
for name,h in expected.items():assert sha((d/name).read_bytes())==h,name
payload=load(d/'RAW-input-payload.json');assert payload['finite_input_count']==94 and len(payload['inputs'])==94
for x in payload['inputs']:
 b=x['complete_original_RAW_UTF8'].encode('utf-8');rawcheck(b,x['original']);assert b==Path(x['RAW_snapshot']['path']).read_bytes();rawcheck(b,x['RAW_snapshot']);rawcheck(Path(x['LF_snapshot']['path']).read_bytes(),x['LF_snapshot'])
primary=Path(payload['whole_primary_pin']['path']);rawcheck(primary.read_bytes(),payload['whole_primary_pin']);assert sha(primary.read_bytes())=='d81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760'
coverage=load(d/'source-coverage-audit.json');body=load(d/'ten-literal-BODY-excerpt-audit.json')
assert coverage['classified_math_items']==344 and coverage['selected_regions']==6 and coverage['graph_preceded_candidate']
for k in ['annotation_mismatches','duplicate_ids','missing_alttext','missing_annotations','missing_items']:assert coverage[k]==0
assert body['counts']==[4,6] and len(body['spans'])==10 and body['all_inside_BODY']
for x in body['spans']:
 q=x['source_region'];b=(root/q['path']).read_bytes();lo,hi=x['exact_RAW_range_end_exclusive'];span=b[lo:hi]
 assert sha(b)==q['source_raw_sha256'] and sha(span)==q['exact_code_raw_sha256'] and x['within_actual_public_theorem_BODY']
 rawcheck(span,x['literal_RAW']);assert span==Path(x['literal_RAW']['path']).read_bytes()
pub.inputs.cache_clear();pub.load.cache_clear();data=pub.inputs();plan=load(r/'publication-plan.json');bindings=[]
for i,(aid,slug) in enumerate(zip(plan['audit_ids'],plan['slugs'])):
 decision=load(d/f'source.{i}.decision.json');audit=load(root/'research-wiki/semantic-roundtrip/audits'/f'{aid}.json');packet=load(r/f'source.{i}.reviewer-packet.json')
 assert rt.semantic_reviewer_packet(audit)==packet and packet['packet_sha256']==decision['reviewer_packet_sha256']
 assert decision['verdict']=='equivalent-after-elaboration' and not decision['repairs']
 assert all(x['blocking'] is False and x['classification']=='explicit-elaboration' for x in decision['deltas'])
 assert decision['independent_from_decoder'] and decision['independent_from_formalizer'] and decision['source_mathematical_repair'] is False
 assert set(decision['semantic_slots'])==set(rt.SEMANTIC_SLOTS) and all(x['evidence'] and x['relation']!='not-audited' for x in decision['semantic_slots'].values())
 assert decision['review_run_sha256']=='' and decision['review_run_sha256_external_binding']
 item=next(x for x in pub.load() if x['id']==slug)
 assert pub.binding_digest(item,item['bindings'][0],data)==audit['publication_binding_sha256']==decision['publication_binding_sha256']
 assert pub.digest(pub.review_context(item,item['bindings'][0],data))==decision['publication_context_sha256']
 bindings.append(dict(declaration=decision['declaration'],packet_sha256=packet['packet_sha256'],publication_binding_sha256=decision['publication_binding_sha256'],publication_context_sha256=decision['publication_context_sha256'],native_decision=pin(d/f'source.{i}.decision.json')))
out=r/'root.source67.adoption.json';assert not out.exists()
out.write_text(json.dumps(dict(status='INDEPENDENT_SOURCE67_ACCEPTED_SELECTED_BOUNDARIES',actual_read_only_adopter_pid=os.getpid(),native_whole_logical_run_sha256=run['run_sha256'],native_complete_RAW_review_sha256=expected['review-run.json'],native_complete_RAW_decision_sha256=expected['complete-RAW-decision.json'],separate_complete_RAW_input_sha256=expected['RAW-input-payload.json'],native_owned_files=262,native_lease=pin(d/'lease.final.json'),source_items=344,literal_BODY_steps=10,decisions=bindings,source_mathematical_repair=False,separately_reviewed_metadata_overlays=['root.attribution-overlay67.adoption.json','applied-reviewed-citation-catalogue67/applied.json','audit-source-url-overlay67/applied.json'],full_Exposition=False,PURIFIED=False,VERIFIED=False,Goal_complete=False),ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
print('PASS source67 CLOSED262: complete native RAW review/decision/input,344 items/10 BODY spans,2 exact packets/current bindings and7 slots each; no mathematical repair.')
