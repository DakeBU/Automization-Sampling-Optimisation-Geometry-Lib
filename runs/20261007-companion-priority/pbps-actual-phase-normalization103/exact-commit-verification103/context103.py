"""Exact103 verifier context. Inert until explicit root freeze dispatch is recorded."""
from pathlib import Path
import hashlib,json,subprocess,sys,re,copy
R=Path('E:/Samplinglib');O=Path(__file__).resolve().parent;B=O.parent;PRE=B.parent/'pbps-phase-normalization-preread103'
M='AutoSamplingTheory/ExampleCases/ProximalBPS/ActualPhaseNormalization.lean'
L='website/content/declaration_lessons/pbps-actual-phase-normalization.json'
P='website/content/publications/pbps-actual-phase-normalization.json'
A='research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261012-PBPSActualPhaseNormalization.json'
CELL='research-wiki/frontier-cells/ASTIS-SW-PBPS-actual-phase-normalization.json'
D='AutoSamplingTheory.ExampleCases.ProximalBPS.ActualPhaseNormalization.actual_phase_gibbs_normalization'
ID='ASTIS-SA-20261012-PBPSActualPhaseNormalization'
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
C='030f4f70feb3641cafca981ee81c48a2687db1ee'
BASE='86fad532c6217ba512ec0d146a7425338efb1a9c'
