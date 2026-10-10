from pathlib import Path
import json
r=Path(__file__).parent;x=json.loads((r/'next-source84.readiness.json').read_bytes());assert not x['formalized'] and not x['claim_created']
p=Path('docs/companion-papers-handoff.md');b=p.read_bytes();nl=b'\r\n' if b'\r\n' in b else b'\n'
old='Choose the next bounded edge from the current capsule and exact source anchors.'.encode();assert b.count(old)==1
new='''The next bounded candidate is84: measurability of the actual state-to-clock
expectation and its outer squared-integral limit for bounded continuous tests,
under the internally normalized exact conditional Gibbs position x standard
Gaussian momentum law. This bounded subclass can use finite-probability4M2
domination without presupposing process invariance. Its source-only inventory,
graph and candidate are frozen in pbps-outer-bounded-l2-preread84 and bound by
83 next-source84.readiness.json. Independent topology review and any separately
reviewed exact repair remain required before header/Statement Seal/proof search.
No84 Lean header, proof, claim or theorem credit exists at this checkpoint.
All-L2 contraction/density/invariance remain distinct OPEN dependencies. Select
work from the current capsule and these exact source anchors, not old counts.'''.encode().replace(b'\n',nl)
p.write_bytes(b.replace(old,new,1));print('Canonical handoff points to source-only84 candidate; no84 proof credit')
