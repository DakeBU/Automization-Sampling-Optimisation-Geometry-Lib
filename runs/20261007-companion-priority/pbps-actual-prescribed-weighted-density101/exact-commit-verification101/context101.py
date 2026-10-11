"""Exact101 verifier context. Inert until explicit root freeze dispatch is recorded."""
from pathlib import Path
import hashlib,json,subprocess,sys,re,copy
R=Path('E:/Samplinglib');O=Path(__file__).resolve().parent;B=O.parent;PRE=B.parent/'pbps-weighted-density-preread101'
M='AutoSamplingTheory/ExampleCases/ProximalBPS/ActualPrescribedWeightedDensity.lean'
L='website/content/declaration_lessons/pbps-actual-prescribed-weighted-density.json'
P='website/content/publications/pbps-actual-prescribed-weighted-density.json'
A='research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261012-PBPSActualPrescribedWeightedDensity.json'
CELL='research-wiki/frontier-cells/ASTIS-SW-PBPS-actual-prescribed-weighted-density.json'
D='AutoSamplingTheory.ExampleCases.ProximalBPS.ActualPrescribedWeightedDensity.actual_prescribed_weighted_density_balance'
ID='ASTIS-SA-20261012-PBPSActualPrescribedWeightedDensity'
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
def frozen_dispatch():
 p=O/'root-freeze-dispatch101.native.json'
 assert p.exists(),'No actual science SHA/final source dispatch recorded; exact verification and admission remain disabled.'
 d=load(p)
 assert d['explicit_root_dispatch'] and d['final_source_and_coverage_ready']
 assert re.fullmatch('[0-9a-f]{40}',d['science_commit']) and head()==d['science_commit']
 return d
