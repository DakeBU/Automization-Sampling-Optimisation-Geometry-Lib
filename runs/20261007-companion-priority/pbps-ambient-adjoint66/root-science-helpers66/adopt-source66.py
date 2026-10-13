from pathlib import Path
import base64,hashlib,json,os,subprocess,sys
root=Path.cwd();sys.path.insert(0,str(root/'tools'))
import astis_publication as pub,astis_semantic_roundtrip as rt
r=Path('runs/20261007-companion-priority/pbps-ambient-adjoint66');d=r/'independent-source66'
load=lambda p:json.loads(p.read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest()
def pin(p):
    b=p.read_bytes();return dict(path=p.as_posix(),bytes=len(b),raw_sha256=sha(b))
def rawcheck(b,x):
    assert len(b)==x['RAW_bytes'] and sha(b)==x['RAW_sha256']
    assert sha(b.replace(b'\r\n',b'\n'))==x['LF_sha256']
def write(p,x):
    assert not p.exists(),p
    p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
lease=load(d/'lease.final.json');manifest=load(d/'owned-manifest.json');run=load(d/'review-run.json');decision=load(d/'decision.json')
assert sha((d/'lease.final.json').read_bytes())=='49c64ed253cf17537d32afde64442714a00c0c1d7cdbb5e37e124030ed5851f9'
assert sha((d/'owned-manifest.json').read_bytes())==lease['manifest_RAW_sha256']=='054946082c832bbe5be10b050415c5d4a1f5add6b8948920d2464bbc74fe108b'
assert lease['status']=='CLOSED_LAST' and lease['last_owned_write'] and lease['owned_file_count']==172
assert not lease['postclose_writes_permitted']
logical=sha(json.dumps({k:v for k,v in run.items() if k!='run_sha256'},sort_keys=True,separators=(',',':'),ensure_ascii=False).encode())
assert logical==run['run_sha256']==lease['whole_logical_run_sha256']=='eeddf8b0c9d573732c527819d20b245c515b65723215c8585bf2299579696704'
expected={'review-run.json':'df3d42e9b9358e451013760af24d0a34ad4c175cb34258a4c760a20aa94222bf','complete-RAW-decision.json':'d2fd10ca129850fd62b00e8ef5c63d871abe9097cae1ff414cd300ad9371947a','RAW-input-payload.json':'9ba9a5b318c2d3953598a9f4a373f102ca43919224e89897184b7a26fdfae7bd'}
for name,h in expected.items():assert sha((d/name).read_bytes())==h
assert {p.name for p in d.iterdir() if p.is_file()}=={x['name'] for x in manifest['regular_file_entries']}|{'owned-manifest.json','lease.final.json'}
assert len(list(d.iterdir()))==172
for x in manifest['regular_file_entries']:rawcheck((d/x['name']).read_bytes(),x)
out=r/'source-adoption66';out.mkdir(exist_ok=False)
post=subprocess.run([sys.executable,'-B',str(d/'postclose-readonly.py')],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
(out/'postclose.stdout.log').write_bytes(post.stdout);(out/'postclose.stderr.log').write_bytes(post.stderr)
assert post.returncode==0,post.stderr.decode(errors='replace')
post_result=json.loads(post.stdout);assert post_result['owned_writes']==0 and post_result['all_owned_files_checked']==172
payload=load(d/'RAW-input-payload.json');assert payload['complete']
for x in payload['inputs']:
    b=base64.b64decode(x['complete_RAW_bytes_base64']);rawcheck(b,x['pin']);assert b==(d/x['name']).read_bytes()
primary=payload['whole_primary'];b=base64.b64decode(primary['complete_RAW_bytes_base64']);rawcheck(b,primary['pin'])
assert sha(b)=='d81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760'
coverage=load(d/'source-coverage.compared.json');body=load(d/'literal-BODY-excerpt-audit.json')
assert coverage['count']==310 and coverage['all_310_classified'] and coverage['all_310_compared'] and coverage['annotation_mismatch']==0
assert body['step_count']==6 and body['all_inside_actual_public_theorem_BODY'] and body['all_step_lean_strings_literal']
for x in body['steps']:
    q=x['source_region'];source=Path(q['path']).read_bytes();lo,hi=x['source_RAW_byte_range_end_exclusive'];span=source[lo:hi]
    assert sha(source)==q['source_raw_sha256'] and sha(span)==q['exact_code_raw_sha256']
    rawcheck(span,x['owned_excerpt']);assert span==Path(x['owned_excerpt']['path']).read_bytes()
assert decision['verdict']=='equivalent-after-elaboration' and not decision['deltas'] and not decision['repairs']
assert decision['independent_from_formalizer'] and decision['independent_from_decoder'] and not decision['source_mathematical_repair']
assert set(decision['semantic_slots'])==set(rt.SEMANTIC_SLOTS)
assert all(x['relation']!='not-audited' and x['evidence'] for x in decision['semantic_slots'].values())
audit=load(Path('research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261009-PBPSAmbientAdjointCorrector.json'))
assert rt.semantic_reviewer_packet(audit)==load(r/'source.1.reviewer-packet.json')
assert decision['reviewer_packet_sha256']=='37333c2bfbc368c26268cda5f12b729feefe5a7ce654c9408911a4553553ab75'
pub.inputs.cache_clear();pub.load.cache_clear();data=pub.inputs();item=next(x for x in pub.load() if x['id']=='pbps-ambient-adjoint-corrector')
assert pub.binding_digest(item,item['bindings'][0],data)==audit['publication_binding_sha256']==decision['publication_binding_sha256']=='3d1d9d97cc4ae200fb0b07584cc5a89e6805851d05d0c640f3d3e4b3106bdc7f'
assert pub.digest(pub.review_context(item,item['bindings'][0],data))==decision['publication_context_sha256']=='d668766750b3e3471ea7b0d50fd3d562a81ec2044cdc8c210891f4671e6ca60b'
for key in ['actual_finalizer_exit','actual_readback_exit','actual_close_validator_exit']:assert lease[key]==0
write(r/'root.source66.adoption.json',dict(status='INDEPENDENT_SOURCE66_ACCEPTED_SELECTED_BOUNDARY',actual_root_pid=os.getpid(),native_whole_logical_run_sha256=logical,native_complete_RAW_review_sha256=expected['review-run.json'],native_complete_RAW_decision_sha256=expected['complete-RAW-decision.json'],separate_complete_RAW_input_sha256=expected['RAW-input-payload.json'],native_owned_files=172,native_lease=pin(d/'lease.final.json'),root_read_only_postclose=post_result,source_items=310,literal_BODY_steps=6,publication_binding_sha256=decision['publication_binding_sha256'],current_publication_context_sha256=decision['publication_context_sha256'],accepted_scope=decision['source_admission'],source_mathematical_repair=False,separate_catalogue_overlay_adoption=pin(r/'presentation-overlay66/applied.json'),TeX_false_positive_retracted=True,full_Exposition=False,PURIFIED=False,VERIFIED=False,Goal_complete=False))
print('PASS source66 CLOSED172: complete RAW review/decision/input,310 selected math items,6 exact BODY spans,7 slots,current packet/binding/context,private literal representation; no full paper/Goal claim.')
