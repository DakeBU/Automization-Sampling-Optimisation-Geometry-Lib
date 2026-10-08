from pathlib import Path
import json,hashlib,copy,datetime
base=Path('runs/20261007-companion-priority');pre=base/'pbps-l2-macroscopic-mean-preproof55';rr=base/'pbps-l2-macroscopic-mean-topology-review55';og=base/'pbps-l2-macroscopic-mean-sourcegraph55';ov=og/'repair-overlay55';rp=rr/'repair-review55'
j=lambda p:json.loads(Path(p).read_text(encoding='utf-8'));H=lambda b:hashlib.sha256(b).hexdigest();canon=lambda d:json.dumps(d,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
checked=[];mappings={}
def bind(p):
 p=Path(p);b=p.read_bytes();return dict(path=p.as_posix(),bytes=len(b),raw_sha256=H(b),lf_sha256=H(b.replace(b'\r\n',b'\n')))
def check(row):
 p=Path(row['path']);override=mappings.get((str(p.resolve()),row['raw_sha256']));b=(override or p).read_bytes();lf=b.replace(b'\r\n',b'\n')
 assert H(b)==row['raw_sha256'],row['path']
 if 'lf_sha256' in row:assert H(lf)==row['lf_sha256'],row['path']
 for k in ['bytes','raw_bytes']:
  if k in row:assert len(b)==row[k],row['path']
 if 'lf_bytes' in row:assert len(lf)==row['lf_bytes'],row['path']
 checked.append(dict(path=p.as_posix(),override=override.as_posix() if override else None))
def walk(d):
 if isinstance(d,dict):
  if 'path' in d and 'raw_sha256' in d:check(d)
  for v in d.values():walk(v)
 elif isinstance(d,list):
  for v in d:walk(v)
def logical(p):
 d=j(p);c=copy.deepcopy(d);h=c.pop('run_sha256');assert H(canon(c))==h,p;return d
def closed(p,keys):
 d=j(p)
 for k in keys:assert d[k] in ['CLOSED','NOT_STARTED_CLOSED'],(p,k)


paths=[og/'run.json',ov/'run.json',rr/'reviewer.topology.run.json',rp/'reviewer.topology.repaired.run.json'];runs=[logical(p) for p in paths]
for p,keys in [(og/'lease.json',['read','write','python','compiler']),(ov/'lease.json',['read','write','python','compiler']),(rr/'reviewer.topology.lease.json',['read','write','Python','compiler']),(rp/'reviewer.topology.repaired.lease.json',['read','write','Python','compiler'])]:closed(p,keys)
review=j(rp/'source-topology-review.repaired.json');original=j(rr/'source-topology-review.json');lease=j(rp/'reviewer.topology.repaired.lease.json')
assert review['verdict']=='accepted-scoped' and not review['blocking']
assert not review['wrong_before_mapping_found'] and not review['corrective_mapping_needed'] and not review['source_signature_or_mathematical_change']
assert original['blocking'] and not original['source_signature_or_mathematical_change']
for d,field in [(review,'review_run_sha256'),(lease,'lease_run_sha256')]:
 c=copy.deepcopy(d);h=c.pop(field);assert H(canon(c))==h
assert H((rp/'source-topology-review.repaired.json').read_bytes())=='dbda576d84e37ab3937277f6d0b16c94ef136ffd35f6d2446ab01af80f7b8639'
assert H((rp/'reviewer.topology.repaired.lease.json').read_bytes())=='14f626222b28ce8500a278f0eb9903c646aa3cb9143d7ac422329331fe0e7a69'
assert H((pre/'prospective-statement.txt').read_bytes())=='0c4a69c99eb2dc8572af054133619442ccaf8e2e91ca19e130f4b1b5fc4cee3f'
for d in runs:walk(d)
for p in [rr/'source-topology-review.json',rp/'source-topology-review.repaired.json']:walk(j(p))
gp=ov/'source-proof-graph.after.json';assert H(gp.read_bytes())=='9388808bd14ed7db794b6cbcb4516cea4dbcb1425a9f11a2bd0d839247e06563'
paths += [og/'lease.json',ov/'lease.json',rr/'reviewer.topology.lease.json',rp/'reviewer.topology.repaired.lease.json',rr/'source-topology-review.json',rp/'source-topology-review.repaired.json',ov/'operations.json',gp,pre/'statement-seals.accepted.json',pre/'root.statement-proposal.json',pre/'root-sourcegraph-native-preflight55.json',pre/'root-overlay-native-preflight55.json']
o=pre/'topology-seals.accepted.json';assert not o.exists()
o.write_text(json.dumps(dict(status='INDEPENDENT_SOURCE_TOPOLOGY_ACCEPTED_NO_PROOF',utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),review=bind(rp/'source-topology-review.repaired.json'),graph=bind(gp),strict_adoption_bindings=[bind(p) for p in paths],native_pin_checks=len(checked),original_negative=bind(rr/'source-topology-review.json'),repair_operations=bind(ov/'operations.json'),repair_scope='T55-1/2 source-provider typing representation only. Independent exact original-to-successor before/after mappings match; no correction needed. No source premise, signature or mathematical change.',signature_lf_sha256='0c4a69c99eb2dc8572af054133619442ccaf8e2e91ca19e130f4b1b5fc4cee3f',original_and_successor_immutable=True),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('55 independent repaired topology adopted; native checks',len(checked),'actual leases CLOSED.')
