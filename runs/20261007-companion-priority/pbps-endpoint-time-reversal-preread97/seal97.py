from pathlib import Path
import datetime,hashlib,json,subprocess
root=Path.cwd().resolve();pre=Path(__file__).resolve().parent.relative_to(root)
ns=pre.parent/'pbps-actual-phase-reversal-volume96/next-primary97'
load=lambda p:json.loads(Path(p).read_bytes())
def pin(p):
 p=Path(p);b=p.read_bytes();return dict(path=p.resolve().relative_to(root).as_posix(),raw_sha256=hashlib.sha256(b).hexdigest(),bytes=len(b))
checked={}
def visit(v):
 if isinstance(v,dict):
  if 'path' in v and 'raw_sha256' in v:
   q=pin(v['path']);assert q['raw_sha256']==v['raw_sha256'],v['path'];checked[q['path']]=q
  for x in v.values():visit(x)
 elif isinstance(v,list):
  for x in v:visit(x)
math=pre/'independent-header-math97/header-math-decision97.native.json'
source=pre/'independent-header-source97/header-source-review97.native.json'
top=pre/'independent-header-math97/topology97/source-topology-decision97.native.json'
assert load(math)['decision']=='ACCEPT_MATHEMATICALLY_SOUND_EXACT_HEADER_FOR_STATEMENT_SEAL'
assert load(source)['verdict']=='accepted-preproof-source-header'
# Topology filename and exact acceptance are checked against native reviewer output before execution.
assert load(top)['decision']=='ACCEPT_CORRECTED_V2_BOUNDED_SOURCE_TOPOLOGY_AND_COVERAGE'
for folder in [pre/'independent-header-math97',pre/'independent-header-source97',ns]:
 for p in folder.rglob('*manifest*.json'):
  visit(load(p));checked[p.as_posix()]=pin(p)
for p in [math,source,top,pre/'source-proof-graph97.v2.native.json','lean-toolchain','lake-manifest.json','research-wiki/process-memory.json']:
 checked[str(p).replace('\\','/')]=pin(p)
header=pre/'Header97.lean';assert pin(header)['raw_sha256']=='2f27a049026ab398bfc85cecf1b2a450e8fef17c45e3a79e8b492c731343800b'
assert not Path('AutoSamplingTheory/ExampleCases/ProximalBPS/ActualEndpointTimeReversal.lean').exists()
d=dict(status='SEALED_BEFORE_PROOF_AFTER_INDEPENDENT_HEADER_AND_TOPOLOGY_AUDITS',sealed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),statement_version=1,owner='companion_root_20261005',baseline_commit=subprocess.check_output(['git','rev-parse','HEAD']).decode().strip(),header=pin(header),expanded_literal_Prop=header.read_text(encoding='utf8').split('def candidate',1)[1].split('#check',1)[0].strip(),proposed_public_theorem='AutoSamplingTheory.ExampleCases.ProximalBPS.ActualEndpointTimeReversal.actual_endpoint_time_reversal_laws',source_revision='arXiv2609.06905v1/Lean4.33.0/Mathlibdb584cd6d46c92f209a44c0f1c829460d327499d',source_anchor='Appendix A.1 A8 finite prescribed endpoint/time reversal and exact product-volume change of variables',independent_math_header=pin(math),independent_source_header=pin(source),independent_topology=pin(top),source_graph=pin(pre/'source-proof-graph97.v2.native.json'),source_coverage=pin(ns/'source-coverage97.native.json'),primary=pin('runs/20261007-companion-priority/phase-pbps-gamma-preread57/primary-pbps.exactraw.snapshot.html'),all_review_bound_inputs_rehashed=list(checked.values()),binder_audit=dict(SOURCE=['hα','hαβ','hV','hH','hη','hβη'],TYPING=['Finite-dimensional real Hilbert Borel E including rank0'],CONCLUSION_WITNESS=['rho uniquely pinned by coordinate formula; no reversal provider premise'],EXCESS=[]),definition_audit='Thirteen exact inherited actual-path literals c,Phi,S,Rec,Hist,Delta,Prefix,m,zAt,K,Path,Psi,Gamma; literal R,ell; A directly evaluates Gamma(T), Theta=(R A,rho). Strict simplex, exact comap and phase-first ell.prod m.',core_delta='Actual finite prescribed endpoint/time reversal is a jointly Borel measure-preserving involution on phase times the exact strict ordered simplex; terminal Gamma identification, fiber phase volume and reversed endpoint identity are conclusions.',consumer='Unweighted A8 change of variables in each A7 sector; later actual Gibbs density balance and stationary averaging. Restart is independent.',truth_boundary='No pointwise reversal of right-continuous path values at jumps; no Gibbs density balance, stationary initial averaging/invariance, Markovness, hypocoercivity, implementation error, expected costs, main results or composition.',proof_search_started=False,sau_claimed=False,Goal_complete=False)
p=pre/'root.statement-seal97.json';assert not p.exists();p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n');print(json.dumps(dict(seal=pin(p),rehashed=len(checked))))
