from pathlib import Path
import hashlib, json, sys
ROOT=Path.cwd();sys.path.insert(0,str(ROOT))
from tools.astis_advance import transition_advance
E=ROOT/'research-wiki/paper-contributions/GaussianComplexity/radial-fourth-matrix-semantic-evidence'
OUT=E/'normal-verification/r4_src_6aef'
evidence=json.loads((OUT/'VERIFIED-evidence.full.json').read_bytes())
marker=json.loads((OUT/'transition-attempted.once.json').read_bytes())
assert marker['advance_id']=='ASTIS-SA-20261111-GaussianComplexityRadialFourthMatrix'
assert marker['evidence_sha256']==hashlib.sha256((OUT/'VERIFIED-evidence.full.json').read_bytes()).hexdigest()
assert evidence['verifier_id']=='/root/radial_fourth_fresh_source_6aef'
# Exactly one existing normal transition API call; no replay append or alternate ledger path.
transition_advance('ASTIS-SA-20261111-GaussianComplexityRadialFourthMatrix','VERIFIED',
  worker_id='/root/radial_fourth_fresh_source_6aef',evidence=evidence)
print('Normal transition API completed: ASTIS-SA-20261111-GaussianComplexityRadialFourthMatrix PROVED_LOCAL -> VERIFIED by /root/radial_fourth_fresh_source_6aef.')
