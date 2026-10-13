from pathlib import Path
import hashlib,json,os,sys
r=Path('runs/20261007-companion-priority/pbps-actual-finite-jump-recursion76')
own=r/'integration76/source-communication-qualification76'
load=lambda p:json.loads(Path(p).read_bytes())
sha=lambda b:hashlib.sha256(b).hexdigest()
canon=lambda x:json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def pin(p):
 p=Path(p);b=p.read_bytes();return dict(path=p.as_posix(),RAW_bytes=len(b),RAW_sha256=sha(b),LF_sha256=sha(b.replace(b'\r\n',b'\n')))
def check(z):
 b=Path(z['path']).read_bytes();assert len(b)==z['RAW_bytes'] and sha(b)==z['RAW_sha256'];assert sha(b.replace(b'\r\n',b'\n'))==z['LF_sha256']
def new(p,x):
 assert not p.exists();p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
lease=load(own/'lease.final.json');assert lease['status']=='CLOSED_LAST' and lease['owned_count']==18
assert lease['actor']=='/root/exact_science63' and lease['postclose_owned_writes'] is False
rows=lease['all_owned_outputs_except_only_self']
assert len(rows)==17 and sha(canon(rows))==lease['closure_logical_sha256']
actual={p.as_posix() for p in own.rglob('*') if p.is_file() and p.name!='lease.final.json'}
assert actual=={z['path'] for z in rows}
for z in rows:check(z)
run=load(own/'run.json');h=run.pop('run_sha256');assert sha(canon(run))==h==lease['whole_logical_run_sha256']
assert h=='f0bcdae9864810e4271fcc74533099f78bfe86208d15017f21d38719f486c75a'
for z in load(own/'inputs.manifest.json')['inputs']:check(z)
for field in ['decision','inputs_manifest','complete_named_RAW_payload']:check(run[field])
decision=load(own/'decision.json');addendum=load(own/'qualification.addendum.proposed.json')
assert decision['accepted'] and decision['append_only_qualification_required']
assert not decision['fresh_source_review_required'] and not decision['source_fidelity_admission_invalidated_by_disclosed_notice']
assert decision['mathematics_status_notice_received'] and decision['coordinate_metadata_notice_received']
assert not decision['earlier_semantic_source_verdict_payload_received'] and not decision['new_VERIFIED']
for key in ['source_native_run','source_native_lease','exact_disclosed_notice']:check(addendum[key])
ap=Path('research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261010-PBPSActualFiniteJumpRecursion.json')
audit=load(ap);assert 'communication_provenance_qualification' not in audit['source_review']
sys.path.insert(0,str(Path.cwd()/'tools'))
from astis_semantic_roundtrip_core import semantic_reviewer_packet
oldpacket=semantic_reviewer_packet(audit)
assert oldpacket==load(r/'source-review.clean.packet.json')
(r/'integration76/audit.before-communication-qualification.exactraw.snapshot.json').write_bytes(ap.read_bytes())
audit['source_review']['communication_provenance_qualification']=dict(
 status='APPEND_ONLY_INDEPENDENTLY_REVIEWED_PROVENANCE_QUALIFICATION',
 addendum=pin(own/'qualification.addendum.proposed.json'),decision=pin(own/'decision.json'),
 native_closed_lease=pin(own/'lease.final.json'),whole_logical_run_sha256=h,
 mathematics_status_notice_received=True,coordinate_metadata_notice_received=True,
 earlier_semantic_source_verdict_payload_received=False,
 native_broad_false_flag_not_a_universal_no_communication_claim=True,
 native_source_RAW_preserved=True,new_VERIFIED=False,
 scope=decision['limitations'],reaudit_trigger=decision['strict_reaudit_trigger'])
assert semantic_reviewer_packet(audit)==oldpacket
ap.write_text(json.dumps(audit,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
new(r/'root.communication76.adoption.json',dict(status='ADOPTED_APPEND_ONLY_COMMUNICATION_QUALIFICATION',
 actual_root_PID=os.getpid(),independent_actor=lease['actor'],native_lease=pin(own/'lease.final.json'),
 native_run=pin(own/'run.json'),whole_logical_run_sha256=h,
 decision=pin(own/'decision.json'),addendum=pin(own/'qualification.addendum.proposed.json'),
 canonical_audit=pin(ap),packet_and_binding_unchanged=True,
 native_closed_files_unchanged=True,new_VERIFIED=False,new_math_or_source_verdict=False,
 whole_paper=False,Goal_complete=False))
print('PASS76 CLOSED18 independently reviewed communication qualification adopted; exact semantic packet unchanged; no new VERIFIED.')
