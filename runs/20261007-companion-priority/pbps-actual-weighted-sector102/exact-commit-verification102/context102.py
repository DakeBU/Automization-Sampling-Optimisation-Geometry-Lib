"""Exact102 verifier context. Inert until explicit root freeze dispatch is recorded."""
from pathlib import Path
import hashlib,json,subprocess,sys,re,copy
R=Path('E:/Samplinglib');O=Path(__file__).resolve().parent;B=O.parent;PRE=B.parent/'pbps-weighted-sector-preread102'
M='AutoSamplingTheory/ExampleCases/ProximalBPS/ActualWeightedSector.lean'
L='website/content/declaration_lessons/pbps-actual-weighted-sector.json'
P='website/content/publications/pbps-actual-weighted-sector.json'
A='research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261012-PBPSActualWeightedSector.json'
CELL='research-wiki/frontier-cells/ASTIS-SW-PBPS-actual-weighted-sector.json'
D='AutoSamplingTheory.ExampleCases.ProximalBPS.ActualWeightedSector.actual_weighted_sector_lintegral'
ID='ASTIS-SA-20261012-PBPSActualWeightedSector'
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
C='320ad09ccfd3bc05a9ec3d909c9c19d236c9a232'
BASE='3e2cf1adc9868c85ad1990fb80d843733598be17'
