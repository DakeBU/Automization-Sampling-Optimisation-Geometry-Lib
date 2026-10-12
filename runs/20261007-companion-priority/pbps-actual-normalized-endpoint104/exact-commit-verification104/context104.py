"""Exact104 verifier context. Inert until explicit root freeze dispatch is recorded."""
from pathlib import Path
import hashlib,json,subprocess,sys,re,copy
R=Path('E:/Samplinglib');O=Path(__file__).resolve().parent;B=O.parent;PRE=B.parent/'pbps-normalized-endpoint-preread104'
M='AutoSamplingTheory/ExampleCases/ProximalBPS/ActualNormalizedEndpointSector.lean'
L='website/content/declaration_lessons/pbps-actual-normalized-endpoint-sector.json'
P='website/content/publications/pbps-actual-normalized-endpoint-sector.json'
A='research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261012-PBPSActualNormalizedEndpointSector.json'
CELL='research-wiki/frontier-cells/ASTIS-SW-PBPS-actual-normalized-endpoint-sector.json'
D='AutoSamplingTheory.ExampleCases.ProximalBPS.ActualNormalizedEndpointSector.actual_normalized_endpoint_sector_reversal'
ID='ASTIS-SA-20261012-PBPSActualNormalizedEndpointSector'
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
C='403c6ea6bc44847ee50b0225c2da166c37e2b279'
BASE='d42d05408676ef3573e325940a1e09c0fdca176e'
