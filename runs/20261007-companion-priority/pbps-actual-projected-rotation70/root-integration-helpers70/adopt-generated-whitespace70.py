from pathlib import Path
import hashlib,json,os
r=Path('runs/20261007-companion-priority/pbps-actual-projected-rotation70');o=r/'independent-generated-whitespace70'
load=lambda p:json.loads(Path(p).read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest();canonical=lambda x:json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def checked(p,z):
 b=Path(p).read_bytes();assert len(b)==z['RAW_bytes'] and sha(b)==z['RAW_sha256'],p
 if z.get('LF_sha256') is not None:assert sha(b.replace(b'\r\n',b'\n'))==z['LF_sha256'],p
 return b
lease=load(o/'lease.final.json');assert sha((o/'lease.final.json').read_bytes())=='d920055d33f4b70bec5aed916cdf9ca14a90cad13d115f8c6a086c1eb3a8045e'
assert lease['status']=='CLOSED_LAST' and lease['no_further_owned_writes'] and lease['owned_count']==32
m=load(o/'owned-manifest.json');assert sha((o/'owned-manifest.json').read_bytes())==lease['manifest_RAW_sha256']=='0190562f3b46aeef211a23ce4971e75f613208c9078d5aecb396d8dea88cf598'
assert len(m['entries'])==m['count']==30 and sha(canonical(m['entries']))==lease['manifest_entries_canonical_sha256']
assert {p.relative_to(o).as_posix() for p in o.rglob('*') if p.is_file()}=={z['path'] for z in m['entries']}|{'owned-manifest.json','lease.final.json'}
for z in m['entries']:checked(o/z['path'],z);assert (o/z['path']).stat().st_mtime_ns<=(o/'lease.final.json').stat().st_mtime_ns
run=load(o/'review.run.json');h=run.pop('run_sha256');assert sha(canonical(run))==h==lease['whole_logical_run_sha256']=='f21a2b3ddac47e24962a4e22023ee21f8fb3dac30d86492fe1ffb264d5422f54'
checked(o/lease['complete_named_payload']['path'],lease['complete_named_payload'])
assert lease['complete_named_payload']['RAW_sha256']=='da590b25905c3732ea62ad1dc71142c45136e206ef20ce1c6e50295220e16c08'
im=load(o/'input-manifest.json');assert len(im['inputs'])==im['count']==13
for z in im['inputs']:checked(z['path'],z)
d=load(o/'overlay.decision.json');assert sha((o/'overlay.decision.json').read_bytes())==lease['decision_RAW_sha256']=='fd80b749a65c1bf2dba41fda707b58b48780058b35a7e82a69f5819b71170daf'
assert d['reviewer']=='/root/independent_primary69' and d['accept_overlay'] and d['preserve_scoped_aggregate_acceptance_under_exact_three_substitutions']
assert not d['blocking_findings'] and not d['required_repairs'] and d['ASCII_bytes_removed_total']==6
proposal=r/'integration70/generated-whitespace/proposal.json';assert sha(proposal.read_bytes())==d['proposal_RAW_sha256']
rows=load(proposal)['rows'];assert len(rows)==3
mapped={Path(z['path']).resolve():z for z in rows}
packet=load(r/'final-reader-repository-packet70.json');other=0
for z in packet['inputs']:
 p=Path(z['path']);x=mapped.get(p.resolve())
 if x:
  assert z['RAW_sha256']==x['before_RAW_sha256']==sha(Path(x['before_snapshot']).read_bytes())
  assert sha(p.read_bytes())==x['after_RAW_sha256']==sha(Path(x['after_snapshot']).read_bytes())
 else:checked(p,z);other+=1
assert other==137
original=r/'independent-repository-reader70';assert sha((original/'lease.final.json').read_bytes())=='44e6685c07f449a5f5a3ee8f697187394775ab507b707992735a105c4653e0c6'
for z in load(original/'owned-manifest.json')['entries']:checked(original/z['path'],z)
dest=r/'root.generated-whitespace70.adoption.json';assert not dest.exists()
dest.write_text(json.dumps(dict(status='INDEPENDENT_CLOSED32_FINITE_GENERATED_WHITESPACE_OVERLAY_ADOPTED',actual_root_PID=os.getpid(),accepted_finite_overlay=True,accepted_scoped_aggregate_under_exact_three_substitutions=True,native_files=32,native_inputs=13,native_whole_logical_run_sha256=h,native_lease_RAW_sha256=sha((o/'lease.final.json').read_bytes()),finite_current_map=rows,other137_unchanged=True,original_CLOSED213_unchanged=True,observed_nonowner_close_PID=1588,observed_nonowner_postclose_PID=38200,observed_close_postclose_EXIT=0,source_mathematics_unchanged=True,full_Exposition=False,PURIFIED=False,main_live=False,Goal_complete=False),ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print('PASS independent CLOSED32 whitespace overlay adopted; three exact substitutions,137 current unchanged, original CLOSED213 preserved.')
