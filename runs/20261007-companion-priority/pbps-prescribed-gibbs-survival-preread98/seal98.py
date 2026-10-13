from pathlib import Path
import datetime,hashlib,json,subprocess
root=Path.cwd().resolve();pre=Path(__file__).resolve().parent.relative_to(root)
next_source=pre.parent/'pbps-actual-endpoint-time-reversal97/next-primary98'
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
manifests=[pre/'independent-header-math98/closed-RAW-manifest98.native.json',pre/'independent-header-source98/closed-raw-manifest98.native.json',pre/'independent-header-math98/topology98/closed-RAW-topology98.native.json',next_source/'closed-raw-manifest98.native.json']
for p in manifests:visit(load(p));checked[p.as_posix()]=pin(p)
math=pre/'independent-header-math98/header-math-decision98.native.json';source=pre/'independent-header-source98/header-source-review98.native.json';topology=pre/'independent-header-math98/topology98/source-topology-decision98.native.json'
assert load(math)['decision']=='ACCEPT_EXACT_HEADER98_AS_MATHEMATICALLY_CORRECT_AND_FEASIBLE'
assert load(source)['decision']=='accepted-for-source-faithful-proof-attempt' and not load(source)['blocking_findings']
assert load(topology)['decision']=='ACCEPT_EXACT_GRAPH_V3_CORRECTION'
header=pre/'Header98.lean';assert pin(header)['raw_sha256']=='50c6999fe069f4cf648832a804b71bb8e447b7a3aea0f0c42a836f81650c6ad0'
assert not Path('AutoSamplingTheory/ExampleCases/ProximalBPS/ActualPrescribedGibbsSurvival.lean').exists()
for p in ['lean-toolchain','lake-manifest.json','research-wiki/process-memory.json']:checked[p]=pin(p)
text=header.read_text(encoding='utf8')
seal=dict(status='SEALED_BEFORE_PROOF_AFTER_INDEPENDENT_HEADER_AND_TOPOLOGY_AUDITS',sealed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),statement_version=1,owner='companion_root_20261005',baseline_commit=subprocess.check_output(['git','rev-parse','HEAD']).decode().strip(),header=pin(header),expanded_literal_Prop=text.split('def candidate',1)[1].split('#check',1)[0].strip(),proposed_public_theorem='AutoSamplingTheory.ExampleCases.ProximalBPS.ActualPrescribedGibbsSurvival.actual_prescribed_gibbs_survival_balance',source_revision='arXiv2609.06905v1/Lean4.33.0/Mathlibdb584cd6d46c92f209a44c0f1c829460d327499d',source_anchor='Appendix A.1 A4 target-energy derivative and Gibbs/survival identity before A8 weighted substitution',independent_math_header=pin(math),independent_source_header=pin(source),independent_topology=pin(topology),source_graph=pin(pre/'source-proof-graph98.v3.native.json'),source_coverage=pin(next_source/'source-coverage98.native.json'),primary=pin(pre.parent/'phase-pbps-gamma-preread57/primary-pbps.exactraw.snapshot.html'),all_review_bound_inputs_rehashed=list(checked.values()),binder_audit=dict(SOURCE=['hα','hαβ','hV','hH','hη','hβη'],TYPING=['finite-dimensional real Hilbert E with Borel measurable structure'],EXCESS=[]),definition_audit='First thirteen actual path literals identical97; R and positive-part rate literal; U_y=V+norm(x-y)^2/(2 eta)+norm(p)^2/2; real-time clamp identical94. A=Gamma(T), Iplus integrates rate(gamma), Iminus integrates rate(R gamma) along the same path, not reversed time. Exact simplex m retained unused; no normalization hypothesis.',core_delta='Both actual whole-path rate integrabilities, U_y(A)-U_y(z)=Iplus-Iminus, and exp(-U_y(z))*exp(-Iplus)=exp(-U_y(A))*exp(-Iminus) for every finite prescribed tuple and nonnegative horizon.',consumer='Weighted prescribed-sector Theta balance requires this finite Gibbs/survival identity together with separate reverse-arc and event-rate product correspondence, actual94 density and97 volume substitution; Gibbs probability averaging follows later.',truth_boundary='No equality of reversed right-continuous jump values, no reversed-event density balance, weighted Theta preservation, stationary averaging/invariance, Markovness, hypocoercivity, errors, expected cost, main result or composition.',proof_search_started=False,sau_claimed=False,Goal_complete=False)
out=pre/'root.statement-seal98.json';assert not out.exists();out.write_text(json.dumps(seal,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
print(json.dumps(dict(seal=pin(out),rehashed_inputs=len(checked),proved=False)))
