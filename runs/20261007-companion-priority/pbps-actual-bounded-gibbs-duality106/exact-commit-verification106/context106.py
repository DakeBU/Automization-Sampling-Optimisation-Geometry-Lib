"""Exact106 verifier context. Inert until explicit root freeze dispatch is recorded."""
from pathlib import Path
import hashlib,json,subprocess,sys,re,copy
R=Path('E:/Samplinglib');O=Path(__file__).resolve().parent;B=O.parent;PRE=B.parent/'pbps-bounded-gibbs-duality-preread106'
M='AutoSamplingTheory/ExampleCases/ProximalBPS/ActualBoundedGibbsDuality.lean'
L='website/content/declaration_lessons/pbps-actual-bounded-gibbs-duality.json'
P='website/content/publications/pbps-actual-bounded-gibbs-duality.json'
A='research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261012-PBPSActualBoundedGibbsDuality.json'
CELL='research-wiki/frontier-cells/ASTIS-SW-PBPS-actual-bounded-gibbs-duality.json'
D='AutoSamplingTheory.ExampleCases.ProximalBPS.ActualBoundedGibbsDuality.actual_bounded_gibbs_duality'
ID='ASTIS-SA-20261012-PBPSActualBoundedGibbsDuality'
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
C='edc917ec4c792bfe1308eee35a5d183c3768703c'
BASE='bd25af52d971654773edcfeb15bc8e09fb9b76ae'
