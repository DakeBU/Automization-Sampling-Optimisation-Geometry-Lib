"""Verifier preparation only: no ledger/cell/staging mutations."""
from pathlib import Path
import hashlib,json,datetime
R=Path('E:/Samplinglib');O=Path(__file__).resolve().parent;B=O.parent
sha=lambda b:hashlib.sha256(b).hexdigest()
load=lambda p:json.loads(p.read_bytes())
def rel(p):return p.relative_to(R).as_posix()
def info(p):return dict(path=rel(p),raw_sha256=sha(p.read_bytes()),bytes=p.stat().st_size)
def write(p,v):p.write_bytes((json.dumps(v,ensure_ascii=False,indent=2)+'\n').encode())
snap=O/'preparation-inputs';snap.mkdir(exist_ok=True)
paths=[B/'independent-whole-math96/whole-math-decision96.native.json',B/'independent-whole-math96/closed-RAW-manifest96.native.json',B/'independent-whole-math96/exposition96/exposition-decision96.native.json',B/'independent-whole-math96/exposition96/closed-RAW-manifest-exposition96.native.json',R/'runs/semantic-roundtrip/anonymous96/decoder/raw-manifest.json',R/'runs/semantic-roundtrip/anonymous96/decoder/decoder-report.json',B.parent/'pbps-phase-reversal-volume-preread96/root.statement-seal96.json',B.parent/'pbps-actual-bounded-path-expansion95/exact-commit-verification95/closed-RAW-manifest95.json']
rows=[]
for i,p in enumerate(paths):
 q=snap/(str(i)+'.'+p.name+'.exactraw');b=p.read_bytes()
 if q.exists():assert q.read_bytes()==b
 else:q.write_bytes(b)
 rows.append(dict(**info(p),snapshot=rel(q)))
collab=load(paths[-1])['preserved_collaborator_inputs'];assert len(collab)==21
for x in collab:assert sha((R/x['path']).read_bytes())==x['raw_sha256'],x['path']
M=R/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualPhaseReversalVolume.lean'
L=R/'website/content/declaration_lessons/pbps-actual-phase-reversal-volume.json'
assert sha(M.read_bytes())=='4b144dfa25d9521803e37518b8a6386fff08396c5804e410e9be593d46833a7b'
assert sha(L.read_bytes())=='af8129aeb3cad23e7a2c98284e986abb90fbeb1da5fb05e1c2e44c8dd56c0951'
assert load(paths[0])['decision']=='ACCEPT_EXACT_PRODUCTION_AND_SEALED_STATEMENT'
assert load(paths[2])['decision']=='ACCEPT_MATHEMATICAL_STATEMENT_AND_SEVEN_PROOF_EXPLANATIONS'
write(O/'prepared96.native.json',dict(status='PREPARED_NOT_VERIFIED',verifier='/root/exact_verifier96',inputs=rows,preserved_collaborator_inputs=collab,production=info(M),lesson=info(L),waiting_for=['native final source acceptance','frozen exact science commit and root dispatch'],no_shared_mutations=True))
print('Prepared independent verifier snapshots; all 21 collaborator RAWs match. No VERIFIED transition.')
