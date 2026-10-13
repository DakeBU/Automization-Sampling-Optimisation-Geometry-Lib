from pathlib import Path
import copy,hashlib,json,os,sys
sys.path.insert(0,'tools')
import astis_publication as pub,astis_semantic_roundtrip as rt
root=Path.cwd();r=root/'runs/20261007-companion-priority/pbps-sharp-energy68';d=r/'independent-math68'
resume='--resume-exact-approved-partial' in sys.argv
pdir=r/'prose-and-span-overlay68-v2';dest=r/'applied-prose-span-overlay68'
load=lambda p:json.loads(p.read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest()
can=lambda x:json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def pin(p):
 b=p.read_bytes();lf=b.replace(b'\r\n',b'\n');return dict(path=p.resolve().as_posix(),raw_bytes=len(b),raw_sha256=sha(b),lf_bytes=len(lf),lf_sha256=sha(lf))
def check(z):
 p=Path(z['path']);q=pin(p)
 for k in ['raw_bytes','raw_sha256','lf_bytes','lf_sha256']:assert q[k]==z[k],(p,k)
 return p
def write(p,x):
 assert not p.exists(),p;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
lease=load(d/'lease.final.json');run=load(d/'run.json')
assert sha((d/'lease.final.json').read_bytes())=='8d0141267fa83db5e4f87f0babab3c78ae57ac88b7aedfaddc7c41d337020c47'
assert lease['status']=='CLOSED_LAST' and lease['last_owned_write']=='lease.final.json' and lease['no_owned_writes_after_this_lease']
assert sha(can({k:v for k,v in run.items() if k!='run_sha256'}))==run['run_sha256']==lease['whole_logical_run_sha256']=='7d0517286b063f68773ae6dac765a8585b4f81cb674809fa423384cee142fca4'
files={p.resolve() for p in d.rglob('*') if p.is_file()};rows=lease['all_owned_outputs_except_only_self'];assert len(files)==lease['owned_file_count_including_self']==275
seen=set()
for z in rows:
 p=check(z).resolve();assert p.is_relative_to(d.resolve()) and p not in seen;seen.add(p)
assert files==seen|{(d/'lease.final.json').resolve()} and (d/'lease.final.json').stat().st_mtime_ns>=max(p.stat().st_mtime_ns for p in files)
assert sha((d/'named-mathematical-review.payload.json').read_bytes())=='4f28f8d6fe3aa03ee34ec18f29ef4b4b9e74bf608528c18164a1e2241500af56'
assert sha((d/'mathematical-review.json').read_bytes())=='3de291fea7954c5cbc301598048ed44188c6346e0be2a63314589dc6e2fa381d'
assert sha((d/'final.inputs.manifest.json').read_bytes())=='a9e3b8b66ba57d307c6b2455c50375804fae434a024a70480257a0336a4e015f'
review=load(d/'mathematical-review.json');assert review['status']=='MATHEMATICS_ACCEPTED_WITH_EXPLICIT_PRESENTATION_RESOLUTIONS' and not review['mathematical_blockers']
assert run['all3_standard3'] and run['fake_closure_hits']==0 and run['private_math_providers']==0 and run['final_original_input_rows']==44
resolution=load(d/'finite-input-resolution.json');qualified={z['canonical_path']:z for z in resolution['rows']};assert len(qualified)==2
early_proposal=load(pdir/'proposal.json')
if resume:
 assert sha((pdir/'proposal.json').read_bytes())=='7cf9aa588d6bbbf0843b59b048b6fc58dda10c1dce30f255cf6c3accdadf47b2'
 expected_partial={'0.current-before.exactraw.snapshot.json','0.current-after.exactraw.snapshot.json','1.current-before.exactraw.snapshot.json','failed-adoption.executed-helper.raw.py'}
 assert {p.name for p in dest.iterdir()}==expected_partial
 assert (r/'adopt-math-overlay68/receipt.json').exists() and load(r/'adopt-math-overlay68/receipt.json')['exit_code']==1
input_count=0;distinct=set()
for z in run['inputs_manifests'].values():
 manifest=load(check(z))
 for row in manifest['inputs']:
  input_count+=1;original=row['original'];distinct.add(original['path']);rp=check(row['RAW_snapshot']);lp=check(row['LF_snapshot']);b=rp.read_bytes()
  assert b.replace(b'\r\n',b'\n')==lp.read_bytes() and sha(b)==original['raw_sha256']
  try:check(original)
  except AssertionError:
   if resume and original['path']==(root/early_proposal['changes'][0]['path']).as_posix():
    change=early_proposal['changes'][0];before=(pdir/change['before_snapshot']).read_bytes();after=(pdir/change['after_snapshot']).read_bytes()
    assert sha(before)==original['raw_sha256']==sha(b) and sha(after)==change['after_raw_sha256'] and Path(original['path']).read_bytes()==after
    continue
   q=qualified[original['path']];before=check(q['explicit_before_snapshot']);after=check(q['explicit_after_snapshot']);check(q['current_observed'])
   assert before.read_bytes()==b and after.read_bytes()==Path(original['path']).read_bytes() and q['all_other_fields_exact'] and set(q['only_changed_top_fields'])=={'state','reconstruction'}
assert input_count==run['input_row_count']==76 and len(distinct)==run['distinct_original_input_paths']==72
for checkrun in run['focused_fresh_Lean_checks'].values():
 assert checkrun['terminal_closed'] and checkrun['exit_code']==0 and checkrun['fresh_Lean'];check(checkrun['stdout']);check(checkrun['stderr'])
decision=load(d/'presentation-overlay.decision.json');assert sha((d/'presentation-overlay.decision.json').read_bytes())=='8d00a67ba10de57f5cdc707b730f71679e1833789fec739c92c1587fe09d16ea'
assert decision['decision']=='APPROVED_PROPOSED_V2_NOT_APPLIED' and decision['V2_proposed_strict_RAW_spans']==11
pdir=r/'prose-and-span-overlay68-v2';proposal=load(pdir/'proposal.json');assert sha((pdir/'proposal.json').read_bytes())=='7cf9aa588d6bbbf0843b59b048b6fc58dda10c1dce30f255cf6c3accdadf47b2'
assert proposal['proposed_binding']==decision['proposed_binding']=='dd53a8d89ef3aca6b14d30e4eb6c8284f078050e56f452da0abefc9d4270dd79'
if not resume:dest.mkdir(exist_ok=False)
maps=[]
for i,row in enumerate(proposal['changes']):
 p=root/row['path'];before=(pdir/row['before_snapshot']).read_bytes();approved=(pdir/row['after_snapshot']).read_bytes();current=p.read_bytes()
 assert sha(before)==row['before_raw_sha256'] and sha(approved)==row['after_raw_sha256']
 saved_before=dest/f'{i}.current-before.exactraw.snapshot.json'
 if saved_before.exists():assert resume and saved_before.read_bytes()==(before if i==0 else current)
 else:saved_before.write_bytes(current)
 if i==0:assert current==(approved if resume else before);applied=approved
 else:
  old=json.loads(before);now=json.loads(current);after=json.loads(approved)
  assert now['state']=='blind-reconstructed' and {k:v for k,v in now.items() if k not in ['state','reconstruction']}=={k:v for k,v in old.items() if k not in ['state','reconstruction']}
  merged=copy.deepcopy(now)
  for k in ['publication_binding_sha256','publication_context']:merged[k]=after[k]
  assert merged['reconstruction']==now['reconstruction'] and rt.decoder_packet(merged)==rt.decoder_packet(now)
  applied=(json.dumps(merged,ensure_ascii=False,indent=2)+'\n').encode()
 saved_after=dest/f'{i}.current-after.exactraw.snapshot.json'
 if saved_after.exists():assert resume and saved_after.read_bytes()==applied and p.read_bytes()==applied
 else:p.write_bytes(applied);saved_after.write_bytes(applied)
 maps.append(dict(canonical_path=row['path'],current_before=pin(dest/f'{i}.current-before.exactraw.snapshot.json'),current_after=pin(dest/f'{i}.current-after.exactraw.snapshot.json'),independently_approved_after=pin(pdir/row['after_snapshot']),decoder_state_preserved=i==1))
pub.inputs.cache_clear();pub.load.cache_clear();data=pub.inputs();item=next(x for x in pub.load() if x['id']=='pbps-sharp-corrector-energy');ap=root/proposal['changes'][1]['path'];audit=load(ap)
assert pub.binding_digest(item,item['bindings'][0],data)==audit['publication_binding_sha256']==decision['proposed_binding'] and pub.review_context(item,item['bindings'][0],data)==audit['publication_context']
packet=r/'source.1.reviewer-packet.json';(dest/'source.1.before-overlay.reviewer-packet.exactraw.snapshot.json').write_bytes(packet.read_bytes());packet.write_text(json.dumps(rt.semantic_reviewer_packet(audit),ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
write(r/'root.math68.adoption.json',dict(status='INDEPENDENT_MATHEMATICS68_ACCEPTED_WITH_SEPARATELY_APPROVED_APPLIED_PRESENTATION_V2',actual_adopter_pid=os.getpid(),native_owned_files=275,native_whole_logical_run_sha256=run['run_sha256'],native_lease=pin(d/'lease.final.json'),native_complete_named_RAW_payload=pin(d/'named-mathematical-review.payload.json'),native_mathematical_review=pin(d/'mathematical-review.json'),original_final_frozen_rows=44,all_input_rows=76,distinct_input_paths=72,finite_qualified_decoder_audit_rows=2,original_BODY_strict_RAW=9,original_BODY_negative_blank_LF_boundaries=2,reviewed_V2_BODY_strict_RAW=11,source_verdict=False,VERIFIED_transition=False,full_Exposition=False,PURIFIED=False,whole_paper_complete=False))
write(r/'root.prose-span-overlay68.adoption.json',dict(status='INDEPENDENTLY_APPROVED_V2_OVERLAY_APPLIED',actual_root_writer_pid=os.getpid(),reviewer='/root/exact_science63',native_whole_logical_run_sha256=run['run_sha256'],native_complete_decision=pin(d/'presentation-overlay.decision.json'),proposal=pin(pdir/'proposal.json'),finite_application_maps=maps,final_binding=audit['publication_binding_sha256'],Lean_statement_BODY_formulas_and_decoder_packets_unchanged=True,source_mathematical_repair=False,final_whole_module_source_review_pending=True,exact_partial_resume=resume,retained_root_failure='adopt-math-overlay68/receipt.json' if resume else None))
print('PASS native math68 CLOSED275;76 exact inputs/44 final/2 finite decoder-state maps; separately approved V2 applied preserving blind payload; final source packet refreshed.')
