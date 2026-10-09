from pathlib import Path
import hashlib,json,os,subprocess,sys
r=Path('runs/20261007-companion-priority/pbps-actual-projected-rotation70');o=r/'independent-repository-reader70'
load=lambda p:json.loads(Path(p).read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest()
canonical=lambda x:json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def checked(p,z):
 b=Path(p).read_bytes();assert len(b)==z['RAW_bytes'] and sha(b)==z['RAW_sha256'],p
 if z.get('LF_sha256') is not None:
  lf=b.replace(b'\r\n',b'\n');assert sha(lf)==z['LF_sha256'],p
  if z.get('LF_bytes') is not None:assert len(lf)==z['LF_bytes'],p
 return b
lp=o/'lease.final.json';lease=load(lp)
assert sha(lp.read_bytes())=='44e6685c07f449a5f5a3ee8f697187394775ab507b707992735a105c4653e0c6'
assert lease['status']=='CLOSED_LAST' and lease['owned_count']==213 and lease['no_further_owned_writes']
m=load(o/'owned-manifest.json');checked(o/'owned-manifest.json',lease['manifest'])
assert sha((o/'owned-manifest.json').read_bytes())=='854f57a34c776b3cad76c4bb74ac6164b2d4221e05496eec8e1f5865d16cb72e'
rows=m['entries'];assert len(rows)==m['count']==211
assert sha(canonical(rows))==m['entries_canonical_sha256']==lease['manifest']['entries_canonical_sha256']
actual={p.relative_to(o).as_posix() for p in o.rglob('*') if p.is_file()}
assert actual=={z['path'] for z in rows}|{'owned-manifest.json','lease.final.json'}
last=lp.stat().st_mtime_ns
for z in rows:
 p=o/z['path'];assert p.resolve().is_relative_to(o.resolve());checked(p,z);assert p.stat().st_mtime_ns<=last,p
assert (o/'owned-manifest.json').stat().st_mtime_ns<=last
run=load(o/'review.run.json');h=run.pop('run_sha256')
assert sha(canonical(run))==h==lease['whole_logical_run_sha256']=='19365ca83c536e7f2e117d7148363201bf2049c604a7959a9df3499a398e090b'
checked(o/lease['complete_named_payload']['path'],lease['complete_named_payload'])
assert lease['complete_named_payload']['RAW_sha256']=='7ccf1c174555703cb20e25eeab86369e3247931026ff181106054bef451b8392'
im=load(o/'input-manifest70.json');assert len(im['inputs'])==im['count']==802
for z in im['inputs']:checked(z['path'],z)
d=load(o/'repository-reader70.decision.json')
assert sha((o/'repository-reader70.decision.json').read_bytes())==lease['decision_RAW_sha256']=='b2150e5117931fd417264d26afbbe8ba9dd43249e5be4e496fdab9ff7b641412'
assert d['reviewer']=='/root/independent_primary69'
assert d['accept_scoped_aggregate'] and d['accept_scoped_reader'] and not d['blocking_findings'] and not d['required_repairs']
head=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip();assert head==d['checked_science_commit']=='c46af8a55e89419109f654c4553cf527993cbeed'
packet=r/'final-reader-repository-packet70.json';checked(packet,d['reviewed_packet'])
for z in load(packet)['inputs']:checked(z['path'],z)
summary=d['bounded_synthesis']
assert summary['all140_frozen_current_inputs_unchanged'] and summary['all31_earlier_gate_metadata_differences_exactly_accounted']
assert summary['Registry']==518 and summary['native_gate_receipts_EXIT0']==25 and summary['exact_final_scope_gates_EXIT0']==6
sys.path.insert(0,str(Path('tools').resolve()));sys.path.insert(0,str(Path('website/scripts').resolve()))
import publication_reader
g=load('_site/data/underlying-lean-graph.json');assert g['publication_inputs_sha256']==publication_reader.graph_input_digest()
dest=r/'root.repository70.adoption.json';assert not dest.exists()
payload=dict(status='INDEPENDENT_CLOSED213_REPOSITORY_READER70_ADOPTED',actual_root_PID=os.getpid(),accepted_scoped_aggregate=True,accepted_scoped_reader=True,accepted_current_graph=True,exact_science_commit=head,native_owned_files=213,current_packet_inputs=140,finite_native_inputs=802,native_whole_logical_run_sha256=h,native_lease_RAW_sha256=sha(lp.read_bytes()),native_decision_RAW_sha256=lease['decision_RAW_sha256'],native_complete_named_RAW_sha256=lease['complete_named_payload']['RAW_sha256'],native_observations=d['reader_debt'],observed_nonowner_close_PID=36420,observed_nonowner_postclose_readonly_PID=44668,observed_close_and_postclose_EXIT=0,native_files_mutated=False,zero_postclose_owned_writes=True,canonical_files_mutated=False,full_Exposition_Seal=False,PURIFIED=False,main_live=False,wholepaper=False,Goal_complete=False)
dest.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print('PASS independent CLOSED213/802 finite inputs/140 exact current/scoped aggregate and reader70 adopted; no canonical or native mutations.')
