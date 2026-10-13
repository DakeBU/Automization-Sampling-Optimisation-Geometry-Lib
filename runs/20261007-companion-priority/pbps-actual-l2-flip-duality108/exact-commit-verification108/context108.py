"""Exact108 verifier context. Inert until explicit root freeze dispatch is recorded."""
from pathlib import Path
import hashlib,json,subprocess,sys,re,copy
R=Path('E:/Samplinglib');O=Path(__file__).resolve().parent;B=O.parent;PRE=B.parent/'pbps-actual-l2-flip-preread108'
M='AutoSamplingTheory/ExampleCases/ProximalBPS/ActualL2FlipDuality.lean'
L='website/content/declaration_lessons/pbps-actual-l2-flip-duality.json'
P='website/content/publications/pbps-actual-l2-flip-duality.json'
A='research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261012-PBPSActualL2FlipDuality.json'
CELL='research-wiki/frontier-cells/ASTIS-SW-PBPS-actual-l2-flip-duality.json'
D='AutoSamplingTheory.ExampleCases.ProximalBPS.ActualL2FlipDuality.actual_l2_flip_duality'
ID='ASTIS-SA-20261012-PBPSActualL2FlipDuality'
sha=lambda b:hashlib.sha256(b).hexdigest()
canon=lambda v:json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def rel(p):return str(p).replace('\\','/').removeprefix('E:/Samplinglib/')
def load(p):return json.loads((R/rel(p)).read_bytes())
def info(p):
 p=R/rel(p);b=p.read_bytes();return dict(path=rel(p),raw_sha256=sha(b),bytes=len(b))
def save(n,v):
 p=O/n;assert not p.exists(),str(p);p.write_bytes((json.dumps(v,ensure_ascii=False,indent=2)+'\n').encode())
def git(*a):return subprocess.check_output(['git',*a],cwd=R,stderr=subprocess.PIPE)
def head():return git('rev-parse','HEAD').decode().strip()
# Only create this dispatch record after root supplies an immutable science SHA.
FREEZE=O/'freeze-dispatch108.json'
assert FREEZE.exists(), 'Not dispatched: wait for immutable root science commit'
_dispatch=json.loads(FREEZE.read_bytes())
assert _dispatch['explicit_root_dispatch'] is True
C=_dispatch['science_commit']
BASE=_dispatch['baseline_commit']
assert re.fullmatch('[0-9a-f]{40}',C) and C != BASE
