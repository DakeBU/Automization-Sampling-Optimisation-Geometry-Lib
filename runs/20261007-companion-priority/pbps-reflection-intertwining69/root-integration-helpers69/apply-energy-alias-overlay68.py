from pathlib import Path
import copy,hashlib,json,os,subprocess,sys
root=Path.cwd();sys.path.insert(0,'tools')
import astis_publication as pub,astis_semantic_roundtrip as rt
r=root/'runs/20261007-companion-priority/pbps-sharp-energy68';d=r/'independent-energy-alias-overlay68';proposal_dir=r/'energy-alias-overlay68'
load=lambda p:json.loads(p.read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest()
can=lambda x:json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
enc=lambda x:(json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode()
def check(b,row):
 assert len(b)==row['RAW_bytes'] and sha(b)==row['RAW_sha256'] and sha(b.replace(b'\r\n',b'\n'))==row['LF_sha256']
verification=load(r/'root.exact-verification68.adoption.json')
assert verification['native_verified'] and verification['verified_commit']==subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()
for name in load(r/'claim.json')['proposed_files']:
 assert subprocess.check_output(['git','show',verification['verified_commit']+':'+name])==subprocess.check_output(['git','show','a3191d97ccf78d58c301d024fc86b2a3289fc0a6:'+name])==(root/name).read_bytes()
lease=load(d/'lease.final.json');assert sha((d/'lease.final.json').read_bytes())=='36e61c3fa58d67967e0b7a80cbdef45664e03f6153b9f013228b447c08442465'
assert lease['status']=='CLOSED_LAST' and lease['total_owned_file_count_including_manifest_and_final_lease']==80 and lease['actual_closing_pid']==488
for key in ['complete_named_RAW_review','complete_named_RAW_decision','complete_named_RAW_input_payload','owned_manifest']:check((d/lease[key]['path']).read_bytes(),lease[key])
manifest=load(d/'owned-manifest.json');rows=manifest['rows'];files={p.relative_to(d).as_posix():p for p in d.rglob('*') if p.is_file()}
assert len(rows)==78 and len(files)==80 and set(files)=={row['path'] for row in rows}|{'owned-manifest.json','lease.final.json'}
assert sha(can(rows))==lease['rows_canonical_sha256']
for row in rows:check(files[row['path']].read_bytes(),row)
assert (d/'lease.final.json').stat().st_mtime_ns>=max(p.stat().st_mtime_ns for p in files.values())
run=load(d/'review-run.json');assert sha(can({k:v for k,v in run.items() if k!='run_sha256'}))==run['run_sha256']==lease['whole_logical_run_sha256']=='30b94e11c2a8244e7da91d5fb5823e51c8caee4c3a3bc3c3bd8b2a0bda79c0af'
payload=load(d/'complete-RAW-input-payload.json');assert payload['entry_count']==len(payload['entries'])==32
for row in payload['entries']:
 b=(root/row['source_path']).read_bytes();check(b,row)
 assert (d/row['raw_snapshot']).read_bytes()==b and (d/row['lf_snapshot']).read_bytes()==b.replace(b'\r\n',b'\n')
for key,pid in [('review-energy-alias68',42060),('final-readback68',40204)]:
 receipt=lease['actual_terminal_receipts'][key];assert receipt['actual_child_pid']==pid and receipt['actual_exit_code']==0
decision=load(d/'complete-RAW-decision.json');proposal=load(proposal_dir/'proposal.json')
assert sha((proposal_dir/'proposal.json').read_bytes())==decision['proposal_RAW_sha256']=='901cbad61d84c46c42df8ee5b8613b12ba9fa1c1b4598d1f1a8b85e82d4c5c03'
assert decision['decision']==lease['decision']=='APPROVED_EXACT_ALIAS_PREFIX_AND_REFRESHED_PACKET_BINDING_CONTEXT'
assert decision['verdict']=='equivalent-after-elaboration' and not decision['repairs'] and not decision['blocking_deltas'] and not decision['source_mathematical_repair']
assert decision['review_run_sha256']==run['run_sha256']
assert decision['independent_from_formalizer'] and decision['independent_from_decoder']
lp=root/proposal['changes'][0]['path'];ap=root/proposal['changes'][1]['path']
for i,path in enumerate([lp,ap]):
 assert path.read_bytes()==(proposal_dir/proposal['changes'][i]['before_snapshot']).read_bytes()
lesson=load(proposal_dir/proposal['changes'][0]['proposed_context_snapshot'])
audit=load(proposal_dir/proposal['changes'][1]['proposed_context_snapshot'])
assert audit['state']=='accepted'
audit['source_review']=copy.deepcopy(decision['source_review_refresh_provenance'])
assert rt.semantic_reviewer_packet(audit)==load(proposal_dir/'proposed.reviewer-packet.json')
assert audit['source_review']['reviewer_packet_sha256']==decision['reviewer_packet_sha256']==lease['new_reviewer_packet_sha256']
assert audit['source_review']['review_run_sha256']==run['run_sha256']
assert sha(can(audit['publication_context']))==decision['candidate_context_canonical_sha256']==lease['new_context_canonical_sha256']
assert audit['publication_binding_sha256']==decision['publication_binding_sha256']==lease['new_binding_sha256']
registry=rt.load_registry();registry['audits']=[audit if row['id']==audit['id'] else row for row in registry['audits']]
assert not rt.validate_registry(registry)
data=copy.deepcopy(pub.inputs());data['lessons'][lesson['units'][0]['declaration']]=lesson['units'][0]
item=next(item for item in pub.load() if item['id']=='hilbert-sharp-quadratic-corrector-bound')
assert pub.binding_digest(item,item['bindings'][0],data)==audit['publication_binding_sha256']
assert pub.review_context(item,item['bindings'][0],data)==audit['publication_context']
out=r/'applied-energy-alias-overlay68';out.mkdir(exist_ok=False);maps=[]
for i,(path,value) in enumerate([(lp,lesson),(ap,audit)]):
 before=path.read_bytes();after=enc(value);(out/f'{i}.before.exactraw.snapshot.json').write_bytes(before)
 (out/f'{i}.after.exactraw.snapshot.json').write_bytes(after);path.write_bytes(after)
 maps.append(dict(canonical_path=path.relative_to(root).as_posix(),before_RAW_sha256=sha(before),after_RAW_sha256=sha(after),before_snapshot=(out/f'{i}.before.exactraw.snapshot.json').relative_to(root).as_posix(),after_snapshot=(out/f'{i}.after.exactraw.snapshot.json').relative_to(root).as_posix()))
packet=rt.semantic_reviewer_packet(audit);(r/'source.0.alias-overlay.reviewer-packet.json').write_bytes(enc(packet))
pub.inputs.cache_clear();pub.load.cache_clear();pub.check_advance(load(r/'publication-plan.json')['mathematical_declarations'],reviewed=True)
result=dict(status='INDEPENDENTLY_APPROVED_EXACT_ENERGY_ALIASES_APPLIED_AFTER_SCI68_VERIFICATION',actual_root_writer_pid=os.getpid(),SCI68=verification['verified_commit'],native_owned_files=80,native_whole_logical_run_sha256=run['run_sha256'],native_complete_RAW_decision_sha256=lease['complete_named_RAW_decision']['RAW_sha256'],native_complete_RAW_input_sha256=lease['complete_named_RAW_input_payload']['RAW_sha256'],finite_current_inputs=32,finite_application_maps=maps,new_packet_sha256=packet['packet_sha256'],new_binding=audit['publication_binding_sha256'],historical_SCI68_native_delta_index3_retained_in_audit=True,historical_alias_omission_closed_prospectively_by_this_exact_overlay=True,only_specific_alias_limitation_closed=True,Lean_private_Props_formulas_BODY_and_decoder_reconstructions_unchanged=True,source_review_refreshed_from_exact_native_approval=True,source_mathematical_repair=False,full_Exposition=False,PURIFIED=False,Goal_complete=False)
(r/'root.energy-alias-overlay68.adoption.json').write_bytes(enc(result))
print('PASS68 exact independently approved S,T alias prefix applied; current source packet/binding refreshed; no mathematics/full Exposition/Goal upgrade.')
