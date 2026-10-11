from pathlib import Path
import json,hashlib,subprocess,datetime
root=Path.cwd();pre=root/'runs/20261007-companion-priority/pbps-weighted-density-preread101';source=pre.parent/'pbps-actual-prescribed-path-reversal100/next-primary101'
load=lambda p:json.loads(Path(p).read_bytes())
def pin(p):
 p=Path(p);b=p.read_bytes();return dict(path=p.resolve().relative_to(root).as_posix(),raw_sha256=hashlib.sha256(b).hexdigest(),bytes=len(b))
math=pre/'independent-header-math101/header-math-decision101.native.json';src=pre/'independent-header-source101/header-source-decision101.native.json';top=pre/'independent-header-math101/source-topology-decision101.native.json'
assert load(math)['decision']=='ACCEPT_PROVISIONAL_HEADER_MATHEMATICS_AND_TYPE'
assert load(src)['verdict']=='matches-frozen-source-boundary'
assert load(top)['decision']=='ACCEPT_SOURCE_TOPOLOGY_AND_COVERAGE'
header=pre/'Header101.lean';assert pin(header)['raw_sha256']=='95693f5ab9b8da50fabdc4da9deeaf6f4950cc4cdd4d60e0a53e0412bfa31c27'
head=subprocess.check_output(['git','rev-parse','HEAD']).decode().strip();push=load(source.parent/'integration100/postpush-binding100.json');assert head==push['local_head']==push['remote_head']==push['pr']['headRefOid']
checked={}
def refs(v):
 if isinstance(v,dict):
  if 'path' in v and 'raw_sha256' in v:
   q=pin(v['path']);assert q['raw_sha256']==v['raw_sha256'],v['path'];checked[q['path']]=q
  for x in v.values():refs(x)
 elif isinstance(v,list):
  for x in v:refs(x)
inputs={}
for folder in [pre/'independent-header-math101',pre/'independent-header-source101',source]:
 for p in folder.rglob('*.json'):
  refs(load(p));inputs[p.as_posix()]=pin(p)
for f in ['lean-toolchain','lake-manifest.json','research-wiki/process-memory.json']:inputs[f]=pin(f)
d=dict(status='SEALED_BEFORE_PROOF_AFTER_INDEPENDENT_HEADER_AND_TOPOLOGY_AUDITS',sealed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),statement_version=1,owner='companion_root_20261005',baseline_commit=head,header=pin(header),expanded_literal_Prop=header.read_text(encoding='utf8').split('def candidate',1)[1].split('#check',1)[0].strip(),proposed_public_theorem='AutoSamplingTheory.ExampleCases.ProximalBPS.ActualPrescribedWeightedDensity.actual_prescribed_weighted_density_balance',source_revision='arXiv2609.06905v1/Lean4.33.0/Mathlibdb584cd6d46c92f209a44c0f1c829460d327499d',source_anchor='Appendix A.1 Eq A7/A8 actual prescribed trajectory weighted-density matching, target energy Eq3.1',independent_math_header=pin(math),independent_source_header=pin(src),independent_topology=pin(top),source_graph=pin(source/'source-proof-graph-delta101.native.json'),source_coverage=pin(source/'source-coverage-delta101.native.json'),primary=pin(pre.parent/'phase-pbps-gamma-preread57/primary-pbps.exactraw.snapshot.html'),all_review_artifacts_rehashed=list(inputs.values()),all_bound_RAW_inputs_rehashed=list(checked.values()),binder_audit=dict(SOURCE=['hα','hαβ','hV','hH','hη','hβη'],TYPING=['Finite real Hilbert Borel E, rank zero included'],EXCESS=[]),definition_audit='First20 literal actual definitions from94 including rho=q*terminalweight. Six explicit definitions R,U,w,P,I,dReal; actual target U, unnormalized w. No supplied density, reversal, product identity or integrability.',core_delta='Actual finite prescribed trajectory weighted real density and actual ENNReal density match under reversed event times and momentum-reversed terminal state.',actual_producer_plan=['ActualPrescribedPathDensity.actual_prescribed_path_density_rewrite','ActualPrescribedGibbsSurvival.actual_prescribed_gibbs_survival_balance','ActualPrescribedStateReversal.actual_prescribed_state_reversal_and_rate_product','ActualPrescribedPathReversal.actual_prescribed_path_reversal_and_survival'],consumer='Actual weighted-sector substitution using97 measure-preserving endpoint/time map; later normalized stationary averaging. Neither later node is assumed or claimed.',truth_boundary='Pointwise unnormalized weighted-density matching only; no weighted integral/sector, invariant probability, restart/Markovness, hypocoercivity, implementation error, expected cost, main theorem or composition.',proof_search_started=False,sau_claimed=False,Goal_complete=False)
p=pre/'root.statement-seal101.json';assert not p.exists();p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n');print(pin(p))
