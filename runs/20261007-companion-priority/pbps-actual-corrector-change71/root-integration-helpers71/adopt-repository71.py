from pathlib import Path
import hashlib,json,os,subprocess,sys
r=Path('runs/20261007-companion-priority/pbps-actual-corrector-change71');o=r/'independent-repository-reader71'
load=lambda p:json.loads(Path(p).read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest()
canonical=lambda x:json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def checked(z):
 p=Path(z['path']);b=p.read_bytes();lf=b.replace(b'\r\n',b'\n')
 assert len(b)==z['RAW_bytes'] and sha(b)==z['RAW_sha256'],p
 assert sha(lf)==z['LF_sha256'],p
 if 'LF_bytes' in z:assert len(lf)==z['LF_bytes'],p
 return b
lp=o/'lease.final71.json';lease=load(lp)
assert sha(lp.read_bytes())=='b0357dd9f788c43a59d97d341e0d4fd2a1895019aedddde6a1001cca5f2db3f1'
assert lease['status']=='CLOSED_LAST' and lease['owned_count']==32 and lease['no_more_owned_writes']
rows=lease['all_owned_outputs_except_only_self'];assert len(rows)==31
assert {p.resolve().as_posix() for p in o.rglob('*') if p.is_file()}=={z['path'] for z in rows}|{lp.resolve().as_posix()}
for z in rows:
 checked(z);assert Path(z['path']).resolve().is_relative_to(o.resolve())
 assert Path(z['path']).stat().st_mtime_ns<=lp.stat().st_mtime_ns,z['path']
checked(lease['owned_manifest']);m=load(o/'owned-manifest71.json');assert m['entry_count']==len(m['entries'])==30
for z in m['entries']:checked(z)
run=load(o/'review-run71.json');logical={k:v for k,v in run.items() if k!='run_sha256'}
assert sha(canonical(logical))==run['run_sha256']==lease['whole_logical_run_sha256']=='e224373c38d20c6d59e6197c74a94808ffec82146926ce20d1c4ac96f6f77638'
checked(lease['complete_named_payload']);payload=load(o/'complete-named-review-decision-input-payload71.json')
assert payload['native_run_complete']==run
mapping={'decision_complete':'decision','bounded_evidence_complete':'evidence','actual_pixel_review_complete':'visual_review','finite_current_and_protocol_inputs_complete':'finite_inputs','fresh_terminal_checks_complete':'fresh_checks'}
for pk,rk in mapping.items():
 checked(run[rk]);assert payload[pk]==load(run[rk]['path'])
assert payload['review_RAW_utf8_complete']==checked(run['review']).decode('utf8')
im=load(o/'input-manifest71.json');assert im['input_count']==len(im['inputs'])==145
for z in im['inputs']:checked(z)
d=load(o/'decision71.json');assert d['actor']=='/root/anonymous_decoder71'
assert d['accept_scoped_aggregate'] and d['accept_scoped_reader'] and not d['blocking_findings'] and not d['required_repairs']
assert len(d['prepared13checks'])==13 and all(z['status']=='pass' for z in d['prepared13checks'])
head=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip();assert head==d['checked_science_commit']=='4e7ce5d2996ffe1d1b0ab570778e02425c6be34e'
checked(d['reviewed_packet']);packet=load(d['reviewed_packet']['path']);assert len(packet['inputs'])==127
for z in packet['inputs']:checked(z)
checks=load(o/'fresh-checks71.json')['checks'];assert len(checks)==4
assert all(z['exit_code']==0 and z['terminal_closed'] for z in checks)
sys.path.insert(0,str(Path('tools').resolve()));sys.path.insert(0,str(Path('website/scripts').resolve()))
import publication_reader
g=load('_site/data/underlying-lean-graph.json');assert g['publication_inputs_sha256']==publication_reader.graph_input_digest()
dest=r/'root.repository71.adoption.json';assert not dest.exists()
result=dict(status='INDEPENDENT_CLOSED32_REPOSITORY_READER71_ADOPTED',actual_root_PID=os.getpid(),accepted_scoped_aggregate=True,accepted_scoped_reader=True,accepted_current_graph=True,exact_science_commit=head,native_owned_files=32,native_finite_inputs=145,current_packet_inputs=127,native_whole_logical_run_sha256=run['run_sha256'],native_lease_RAW_sha256=sha(lp.read_bytes()),native_decision_RAW_sha256=sha((o/'decision71.json').read_bytes()),native_complete_named_RAW_sha256=lease['complete_named_payload']['RAW_sha256'],native_observations=d['reader_debt'],reported_nonowner_writer_PID=5232,reported_nonowner_writer_EXIT=0,reported_nonowner_postclose_readonly_PID=48168,reported_nonowner_postclose_readonly_EXIT=0,native_files_mutated=False,zero_postclose_owned_writes=True,canonical_files_mutated=False,full_Exposition_Seal=False,PURIFIED=False,main_live=False,wholepaper=False,Goal_complete=False)
dest.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
print('PASS independent CLOSED32/145finite/127current/13checks/scoped aggregate and reader71 adopted; no canonical or native mutations.')
