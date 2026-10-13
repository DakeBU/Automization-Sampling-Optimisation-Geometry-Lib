from pathlib import Path
import hashlib,json,os,sys
sys.path.insert(0,str(Path.cwd()/'tools'))
import astis_publication as pub
import astis_semantic_roundtrip as rt
r=Path('runs/20261007-companion-priority/pbps-actual-projected-rotation70');o=r/'independent-metadata-repair70'
load=lambda p:json.loads(Path(p).read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest();can=lambda x:json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def check(z):
 b=Path(z['path']).read_bytes();lf=b.replace(b'\r\n',b'\n')
 assert (len(b),sha(b),len(lf),sha(lf))==(z['raw_bytes'],z['raw_sha256'],z['lf_bytes'],z['lf_sha256'])
def pin(p):
 p=Path(p);b=p.read_bytes();lf=b.replace(b'\r\n',b'\n')
 return dict(path=p.resolve().as_posix(),raw_bytes=len(b),raw_sha256=sha(b),lf_bytes=len(lf),lf_sha256=sha(lf))
def new(p,x):
 p=Path(p);assert not p.exists();p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
lease=load(o/'lease.final.json');assert sha((o/'lease.final.json').read_bytes())=='b643806ff683e52ac3df0921e77b1af768590f8d6223f72bc301dc5245878540'
assert lease['status']=='CLOSED_LAST' and lease['last_owned_write'] and not lease['postclose_writes_allowed']
assert lease['actor']=='/root/exact_science63' and sha(can(lease['manifest']))==lease['manifest_logical_sha256']
actual={p.resolve() for p in o.rglob('*') if p.is_file()}
assert len(actual)==lease['owned_file_count']==55
assert actual=={Path(z['path']).resolve() for z in lease['manifest']}|{(o/'lease.final.json').resolve()}
for z in lease['manifest']:
 check(z);assert Path(z['path']).stat().st_mtime_ns<=(o/'lease.final.json').stat().st_mtime_ns
run=load(o/'run.json');h=sha(can({k:v for k,v in run.items() if k!='run_sha256'}))
assert h==run['run_sha256']==lease['whole_logical_run_sha256']=='ba3515f6ad96ab3614e4d515a053fadb37f38841e5dbe6ef530318cdbd1e4be2'
assert run['status']=='APPROVED_EXACT_TWO_FIELD_METADATA_OVERLAY_ONLY'
assert run['complete_named_review']==load(o/'named-review.payload.json')
check(run['named_complete_RAW_payload']);assert run['named_complete_RAW_payload']['raw_sha256']=='155b3440c5c141959f8075ab16295f306166e0fa133d603f8c15d7563b730488'
for z in run['stage_terminals'].values():assert z['terminal_closed'] and z['exit_code']==0
m=load(o/'inputs.manifest.json');assert m['input_count']==len(m['inputs'])==16 and m['exact_snapshot_input_count']==11 and m['closed_native_authority_locator_count']==5
for i,z in enumerate(m['inputs']):
 check(z['original'])
 if i<11:
  for k in ['RAW_snapshot','LF_snapshot']:check(z[k])
  b=Path(z['original']['path']).read_bytes()
  assert b==Path(z['RAW_snapshot']['path']).read_bytes()
  assert b.replace(b'\r\n',b'\n')==Path(z['LF_snapshot']['path']).read_bytes()
 else:assert set(z)=={'original','storage'}
d=load(o/'decision.json');assert d['approved'] and d['approved_change_count']==2 and not d['mathematical_or_source_assumption_repair'] and not d['source_final']
proposal=load(r/'representation-metadata-repair70/proposal.json');assert len(proposal['changes'])==2
ap=Path('research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261009-PBPSActualProjectedRotation.json')
audit=load(ap);assert audit['state']=='blind-reconstructed'
old_audit=ap.read_bytes();old_packet=(r/'source-review.packet.0.json').read_bytes()
for z in proposal['changes']:
 p=Path(z['path']);before=Path(z['before']).read_bytes();after=Path(z['proposed']).read_bytes()
 assert p.read_bytes()==before and sha(before)==z['before_RAW_sha256'] and sha(after)==z['proposed_RAW_sha256']
 assert after==before.replace(z['old'].encode(),z['new'].encode()) and before.count(z['old'].encode())==1
snap=r/'audit.before-metadata-repair70.exactraw.snapshot.json';assert not snap.exists();snap.write_bytes(old_audit)
for z in proposal['changes']:Path(z['path']).write_bytes(Path(z['proposed']).read_bytes())
pub.inputs.cache_clear();pub.load.cache_clear()
item=load('website/content/publications/pbps-actual-projected-rotation.json')['items'][0];binding=item['bindings'][0]
audit['publication_binding_sha256']=pub.binding_digest(item,binding,pub.inputs())
audit['publication_context']=pub.review_context(item,binding,pub.inputs())
ap.write_text(json.dumps(audit,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
new(r/'source-review.packet.1.json',rt.semantic_reviewer_packet(audit))
new(r/'source-review.freeze70.metadata-overlay1.json',dict(status='EXACT_CURRENT_SOURCE_PACKET1_AFTER_INDEPENDENT_METADATA_ONLY_OVERLAY',packet=pin(r/'source-review.packet.1.json'),audit=pin(ap),source_body=pin(audit['lean']['file']),publication=pin('website/content/publications/pbps-actual-projected-rotation.json'),lesson=pin('website/content/declaration_lessons/pbps-actual-projected-rotation.json'),frontier=pin('research-wiki/frontier-cells/ASTIS-SW-PBPS-actual-projected-rotation.json'),source_review=False,VERIFIED=False))
assert (r/'source-review.packet.0.json').read_bytes()==old_packet
new(r/'root.metadata-repair70.adoption.json',dict(status='EXACT_TWO_FIELD_REVIEWED_METADATA_OVERLAY_APPLIED_PACKET1_REFRESHED',actual_root_PID=os.getpid(),native_files=55,native_inputs=16,native_whole_logical_run_sha256=h,native_named_complete_RAW_sha256=run['named_complete_RAW_payload']['raw_sha256'],native_lease_RAW_sha256=sha((o/'lease.final.json').read_bytes()),exact_changes=proposal['changes'],original_packet0_unchanged=True,mathematical_Lean_changed=False,source_verdict=False,VERIFIED=False,full_Exposition_Seal=False))
print('PASS independent CLOSED55/16 inputs; exact two fields applied; publication binding/context and source packet1 refreshed; Lean and packet0 unchanged. Source verdict pending.')
