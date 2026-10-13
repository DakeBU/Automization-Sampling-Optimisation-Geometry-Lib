from pathlib import Path
import hashlib,json
r=Path(__file__).parent;pre=r.parent/'pbps-transition-kernel-preread85';load=lambda p:json.loads(Path(p).read_bytes())
def pin(p):
 p=Path(p);b=p.read_bytes();return dict(path=p.as_posix(),RAW_sha256=hashlib.sha256(b).hexdigest(),RAW_bytes=len(b))
p=pre/'source-first-run-manifest85.json';assert pin(p)['RAW_sha256']=='e2685c8e1b1ebf4ab292367526da053471100107dd60c32afc418125202d6ef0'
m=load(p);assert m['status']=='closed'
for k in ['raw_inputs','raw_outputs']:
 for x in m[k]:
  q=pin(x['path']);assert q['RAW_sha256']==x['raw_sha256'] and q['RAW_bytes']==x['bytes']
out=r/'next-source85.readiness.json';assert not out.exists()
out.write_text(json.dumps(dict(status='SOURCE_ONLY_NEXT_CANDIDATE_NOT_THEOREM_ADMISSION',manifest=pin(p),raw_outputs=m['raw_outputs'],source_inventory=16,source_nodes=21,source_relations=29,independent_topology_review='pending in a separate owned directory; not part of the closed original source freeze',candidate='Actual finite-time full-phase probability kernel with exact actual-clock pushforward identity, zero-time Dirac law and bounded-Borel integrability/expectation transfer. Retire generic supplied-measurability-only wrappers.',consumer_reason='Real actual-algorithm law/operator interface; not a logically necessary representation of source pathwise invariance proof. Source finite-jump path-law/summability/reversal remains a separate global blocker.',no_header_or_StatementSeal=True,no_proof_or_claim=True,Goal_complete=False),ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
print('Closed original SOURCE-ONLY85 freeze pinned; no scheduling or proof credit')
