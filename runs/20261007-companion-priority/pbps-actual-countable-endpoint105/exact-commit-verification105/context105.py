"""Exact105 verifier context. Inert until explicit root freeze dispatch is recorded."""
from pathlib import Path
import hashlib,json,subprocess,sys,re,copy
R=Path('E:/Samplinglib');O=Path(__file__).resolve().parent;B=O.parent;PRE=B.parent/'pbps-countable-endpoint-preread105'
M='AutoSamplingTheory/ExampleCases/ProximalBPS/ActualCountableEndpointLaw.lean'
L='website/content/declaration_lessons/pbps-actual-countable-endpoint-law.json'
P='website/content/publications/pbps-actual-countable-endpoint-law.json'
A='research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261012-PBPSActualCountableEndpointLaw.json'
CELL='research-wiki/frontier-cells/ASTIS-SW-PBPS-actual-normalized-endpoint-sector.json'
D='AutoSamplingTheory.ExampleCases.ProximalBPS.ActualCountableEndpointLaw.actual_countable_endpoint_law'
ID='ASTIS-SA-20261012-PBPSActualCountableEndpointLaw'
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
C='a6060928c393d3efe4c85d4cab2b9af166ab6b37'
BASE='c4f862780fe019fa63be24026e1e4eef9318fcad'
