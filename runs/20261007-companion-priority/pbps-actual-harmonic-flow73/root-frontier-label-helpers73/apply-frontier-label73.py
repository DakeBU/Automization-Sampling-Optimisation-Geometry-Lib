from pathlib import Path
import hashlib,json,os,subprocess,sys
sys.path.insert(0,str(Path.cwd()/'tools'))
import astis_publication as pub
import astis_semantic_roundtrip as rt
r=Path('runs/20261007-companion-priority/pbps-actual-harmonic-flow73')
load=lambda p:json.loads(Path(p).read_bytes())
sha=lambda b:hashlib.sha256(b).hexdigest()
can=lambda x:json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def check(z):
 p=Path(z['path']);b=p.read_bytes()
 assert len(b)==z.get('RAW_bytes',z.get('bytes')) and sha(b)==z.get('RAW_sha256',z.get('raw_sha256')),p
 assert sha(b.replace(b'\r\n',b'\n'))==z.get('LF_sha256',z.get('lf_sha256')),p
 return b
def pin(p):
 p=Path(p);b=p.read_bytes();return dict(path=p.as_posix(),RAW_bytes=len(b),RAW_sha256=sha(b),LF_sha256=sha(b.replace(b'\r\n',b'\n')))
def write(p,x):
 p=Path(p);assert not p.exists();p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
head=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()
assert head=='63319104ccad4e81e3a2c59da23ec0009be5e17f'
f=r/'exact-science-verification73';lp=f/'lease.final.json';l=load(lp)
assert sha(lp.read_bytes())=='5bd4f3763314d9f7c9c3ff15a01b2c0a8c01452c21412b3665f7bca4c6103271'
rows=l['all_owned_outputs_except_only_self']
assert l['status']=='CLOSED_LAST' and l['owned_count']==102 and len(rows)==101 and l['all_sessions_closed'] and not l['postclose_owned_writes'] and not l['canonical_ledger_Git_writes']
assert {p.resolve() for p in f.rglob('*') if p.is_file()}=={Path(z['path']).resolve() for z in rows}|{lp.resolve()}
for z in rows:
 check(z);assert Path(z['path']).stat().st_mtime_ns<=lp.stat().st_mtime_ns
run=load(f/'run.json');h=sha(can({k:v for k,v in run.items() if k!='run_sha256'}))
assert h==run['run_sha256']==l['whole_logical_run_sha256']=='86607ca828fc8bb4550c14895c42164dee199d4e5acb39d9e48c98b628ee0d7f'
assert run['checked_commit']==head and not run['VERIFIED'] and not run['accepted_exact_commit'] and run['ledger_unchanged']
check(run['inputs_manifest']);inputs=load(run['inputs_manifest']['path'])
assert inputs['input_count']==len(inputs['inputs'])==49
for z in inputs['inputs']:check(z)
check(run['decision']);check(run['complete_named_RAW_payload']);d=load(run['decision']['path'])
assert d['blocker_class']=='PROCESS_METADATA_SCHEMA' and d['failed_gate']['exit_code']==1 and d['fresh_direct_Lean']['actual_direct_Lean_PID']==36212 and d['blocking_source_deltas']==0 and not d['VERIFIED']
payload=load(run['complete_named_RAW_payload']['path']);assert payload['decision']==d and payload['inputs']==inputs and payload['ledger_after']['VERIFIED_events_appended']==0
write(r/'root.failed-science73.adoption.json',dict(status='ADOPTED_CLOSED102_TYPED_METADATA_OBSTRUCTION_NO_VERIFIED',actual_root_PID=os.getpid(),checked_commit=head,native_files=102,native_lease=pin(lp),native_whole_logical_run_sha256=h,complete_named=run['complete_named_RAW_payload'],all_49_inputs_current_before_overlay=True,blocker_class=d['blocker_class'],old_commit_VERIFIED=False,mathematical_or_source_repair=False,Goal_complete=False))
o=r/'independent-frontier-label-repair73';rlp=o/'lease.final.json';rl=load(rlp)
assert sha(rlp.read_bytes())=='c81c56f71feab546761a2a875b7717e87a187bd658a7783cb364bb4341d4baf0'
assert rl['status']=='CLOSED_LAST' and rl['owned_files']==12
check(rl['manifest']);m=load(rl['manifest']['path']);rr=m['owned_files'];assert len(rr)==10
assert {p.resolve() for p in o.rglob('*') if p.is_file()}=={Path(z['path']).resolve() for z in rr}|{Path(rl['manifest']['path']).resolve(),rlp.resolve()}
for z in rr:
 check(z);assert Path(z['path']).stat().st_mtime_ns<=rlp.stat().st_mtime_ns
rrun=load(o/'run.json');rh=sha(can({k:v for k,v in rrun.items() if k!='run_sha256'}))
assert rh==rrun['run_sha256']==rl['run_sha256']=='b15c8dd9464d6ff8d4d7db010a180b69a895502a1752fd2a2280740b77828559'
assert len(rrun['inputs'])==15 and rrun['no_new_truth_or_canonical_write']
for z in rrun['inputs']:check(z)
check(rl['decision']);check(rl['complete_named']);rd=load(rl['decision']['path'])
assert rd['verdict']=='ACCEPT_EXACT_TWO_STRING_METADATA_REPLACEMENTS' and rd['reviewer']=='/root/header_math72' and rd['proposer']=='/root' and not rd['new_SCI_source_math_VERIFIED_credit'] and rd['native_payloads_equal'] and rd['native_source_packet_exact']
proposal=load(r/'frontier-label-overlay73/proposal.json');check(rd['proposal'])
assert len(rd['exhaustive_changes'])==2 and rd['exact_RAW_only_two_string_tokens']
assert [dict(JSON_pointer=z['pointer'],before=z['before'],after=z['after']) for z in rd['exhaustive_changes']]==proposal['changes']
before=check(rd['approved_before']);after=check(rd['approved_after']);cp=Path(rd['canonical_path'])
assert cp.read_bytes()==before and rd['current_equals_before_RAW']
old,new=proposal['changes'][0]['before'],proposal['changes'][0]['after']
assert before.count(json.dumps(old).encode())==2 and before.replace(json.dumps(old).encode(),json.dumps(new).encode())==after
for z in proposal['unchanged']:check(z)
item=next(x for x in pub.load() if x['id']=='pbps-actual-harmonic-flow')
assert pub.binding_digest(item,item['bindings'][0],pub.inputs())==proposal['binding_sha256']
assert sha(can(pub.review_context(item,item['bindings'][0],pub.inputs())))==proposal['context_sha256']
audit=load('research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261010-PBPSActualHarmonicFlow.json');packet=load(r/'source-review.packet.json');assert rt.semantic_reviewer_packet(audit)==packet and packet['packet_sha256']==proposal['source_packet_sha256']
cp.write_bytes(after)
pub.inputs.cache_clear();pub.load.cache_clear()
item=next(x for x in pub.load() if x['id']=='pbps-actual-harmonic-flow')
assert pub.binding_digest(item,item['bindings'][0],pub.inputs())==proposal['binding_sha256'] and sha(can(pub.review_context(item,item['bindings'][0],pub.inputs())))==proposal['context_sha256']
pub.check_advance(load(r/'publication-plan.json')['mathematical_declarations'],reviewed=True)
for z in proposal['unchanged']:check(z)
write(r/'root.frontier-label-overlay73.adoption.json',dict(status='APPLIED_DISTINCTLY_REVIEWED_TWO_STRING_METADATA_OVERLAY_ONLY',actual_root_PID=os.getpid(),parent_commit=head,failed_SCI_adoption=pin(r/'root.failed-science73.adoption.json'),native_repair_lease=pin(rlp),native_repair_files=12,native_whole_logical_run_sha256=rh,before=proposal['before'],approved_after=proposal['after'],current=pin(cp),changes=proposal['changes'],additional_case_change=rd['additional_case_change_disclosed'],unchanged=proposal['unchanged'],binding_sha256=proposal['binding_sha256'],context_sha256=proposal['context_sha256'],source_packet_sha256=proposal['source_packet_sha256'],new_science_child_and_nonowner_verification_required=True,VERIFIED=False,Goal_complete=False))
print('PASS73 adopted CLOSED102 obstruction/CLOSED12 distinct overlay, applied only two exact cell labels; new SCI child/verification required.')
