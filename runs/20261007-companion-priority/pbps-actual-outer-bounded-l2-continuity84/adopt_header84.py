from pathlib import Path
import hashlib,json
r=Path(__file__).parent
pre=Path('runs/20261007-companion-priority/pbps-outer-bounded-l2-preread84')
load=lambda p:json.loads(Path(p).read_bytes())
def pin(p):
 p=Path(p);b=p.read_bytes();return dict(path=p.as_posix(),RAW_bytes=len(b),RAW_sha256=hashlib.sha256(b).hexdigest())
def verify_manifest(p):
 d=load(p)
 for k in ('inputs','outputs','raw_inputs','raw_outputs'):
  for x in d.get(k,[]):
   actual=pin(x['path']); expected=x.get('RAW_sha256',x.get('raw_sha256'))
   assert actual['RAW_sha256']==expected,(p,x)
   assert actual['RAW_bytes']==x.get('RAW_bytes',x.get('bytes')),(p,x)
 return pin(p)
m=r/'header-review84';s=pre/'header-source-review84'
assert pin(m/'decision84.json')['RAW_sha256']=='ca2d787cb7c370edf1d670b4fde61c5f67d24eeaf78451e3fe296e12c4ded2af'
assert pin(s/'header-source.corrected-decision84.json')['RAW_sha256']=='0be52a718f4b715256d3f9db018dfae10e2a350b6c2dd6ff20b07ee236597ee9'
manifests=[verify_manifest(m/'closed-RAW-manifest84.json'),verify_manifest(s/'header-source.corrected-run-manifest84.json')]
math=load(m/'decision84.json');source=load(s/'header-source.corrected-decision84.json')
assert math['syntax_proposal_complete_private_Prop_typechecked']
assert source['verdict']=='ACCEPT_PROSPECTIVE_HEADER_SOURCE_SCOPE'
assert source['repair_verdict']=='ACCEPT_EXACT_SYNTAX_ONLY_PATCH'
assert not source['blocking_deltas'] and not source['additional_required_repairs']
old=(r/'header84.proposed.lean').read_bytes();new=(m/'header84.syntax-only-proposed.lean').read_bytes()
assert hashlib.sha256(old).hexdigest()=='936b76036df8d283acb212f2f1ba780c4446aa2e1c7dc84bfdff0ff9c02f29b0'
assert hashlib.sha256(new).hexdigest()=='5c4e379caa337d1ac903d509eca30ef7db7b1905715c7a65b878afb33f9d2ded'
assert old.count(b'set_option maxHeartbeats 1600000 in\n')==1
assert old.replace(b'set_option maxHeartbeats 1600000 in\n',b'')==new
dest=r/'header84.reviewed.lean';assert not dest.exists();dest.write_bytes(new)
receipt=dict(accepted=True,kind='mechanical-adoption-of-distinct-independent-reviews',header=pin(dest),math_decision=pin(m/'decision84.json'),source_decision=pin(s/'header-source.corrected-decision84.json'),closed_manifests=manifests,original_negative_retained=True,mathematical_statement_changed=False,proof_credit=False,StatementSeal=False)
out=r/'independent-review-adoption84.json';assert not out.exists();out.write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
print('84 full corrected header independently accepted, mechanically adopted; no proof credit')
