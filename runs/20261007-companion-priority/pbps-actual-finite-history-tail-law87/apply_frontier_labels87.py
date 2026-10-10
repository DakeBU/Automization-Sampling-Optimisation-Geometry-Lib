from pathlib import Path
import json,hashlib
r=Path(__file__).parent;d=r/'frontier-label-repair87';v=d/'independent-review';sha=lambda b:hashlib.sha256(b).hexdigest();load=lambda p:json.loads(p.read_bytes())
dp=v/'frontier-label-repair87.decision.json';mp=v/'frontier-label-repair87.closed-RAW-manifest.json'
assert sha(dp.read_bytes())=='1c1366863aea2e492189a9137385786f0fa04f8e662651f71b1a1ac3622dfd89'
assert sha(mp.read_bytes())=='c85d35b74c8451fe87e1228511b118fa7bade22c4a6dd06a9a0755c5293972fc'
for group in ['inputs','outputs']:
 for x in load(mp)[group]:
  b=Path(x['path']).read_bytes();assert sha(b)==x['raw_sha256'] and len(b)==x['bytes'],x['path']
n=load(dp);assert n['decision']=='accepted' and n['verdict']=='ACCEPTED_EXACT_FOUR_FIELD_CONTROL_METADATA_REPAIR' and n['independent_from_proposer']
assert n['reviewer']=='/root/fresh_source86';proposal=load(d/'proposal87.json');target=Path(proposal['target'])
assert sha(target.read_bytes())==proposal['original']['raw_sha256']
after=Path(proposal['proposed']['path']).read_bytes();assert sha(after)==proposal['proposed']['raw_sha256']
assert json.loads(after)['status']=='independently_verified';target.write_bytes(after)
p=r/'root.frontier-labels87.adoption.json';assert not p.exists();p.write_text(json.dumps(dict(status='DISTINCT_EXACT_FOUR_FIELD_CONTROL_METADATA_REPAIR_APPLIED',proposal_sha256=n['proposal_sha256'],decision_raw_sha256=sha(dp.read_bytes()),manifest_raw_sha256=sha(mp.read_bytes()),current_cell_raw_sha256=sha(after),normalization='Reviewed exact successor includes 229 CRLF-to-LF line endings; original native snapshot unchanged.',new_mathematical_credit=False,new_VERIFIED=False),indent=2)+'\n',encoding='utf8',newline='\n');print('Applied independently accepted four-label frontier metadata only.')
