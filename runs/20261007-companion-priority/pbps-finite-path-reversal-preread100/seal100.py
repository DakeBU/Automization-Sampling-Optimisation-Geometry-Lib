"""Freeze the reviewed off-event path/integral statement after99 remote delivery."""
from pathlib import Path
import datetime,hashlib,json,subprocess
root=Path.cwd().resolve();pre=Path(__file__).resolve().parent.relative_to(root)
source=pre.parent/'pbps-actual-prescribed-state-reversal99/next-primary100'
load=lambda p:json.loads(Path(p).read_bytes())
def pin(p):
 p=Path(p);b=p.read_bytes();return dict(path=p.resolve().relative_to(root).as_posix(),raw_sha256=hashlib.sha256(b).hexdigest(),bytes=len(b))
head=subprocess.check_output(['git','rev-parse','HEAD']).decode().strip()
push=load(source.parent/'integration99/postpush-binding99.json')
assert push['local_head']==push['remote_head']==push['pr']['headRefOid']==head
assert not Path('AutoSamplingTheory/ExampleCases/ProximalBPS/ActualPrescribedPathReversal.lean').exists()
math=pre/'independent-header-math100/header-math-decision100.native.json'
src=pre/'independent-header-source100/header-source-decision100.native.json'
topology=pre/'independent-header-math100/topology-overlay100/source-topology-admission100.native.json'
assert load(math)['decision']=='ACCEPT_PROVISIONAL_HEADER_MATHEMATICS_AND_TYPE'
assert load(src)['verdict']=='accept-prospective-header-source-boundary'
assert load(topology)['decision']=='ACCEPT_BASE_PLUS_NARROW_OVERLAY_TOPOLOGY_AND_COVERAGE'
assert pin(topology)['raw_sha256']=='c9d26198921eac188fe70226921713e5c3325203ef4724c4634edd149a32f6fc'
header=pre/'Header100.lean';assert pin(header)['raw_sha256']=='94ada767874180a727bfa7627c4e40629da5a77f523895ca30e0d5e0e74008b9'
inputs={}
checked={}
def verify_refs(v):
 if isinstance(v,dict):
  if 'path' in v and 'raw_sha256' in v:
   q=pin(v['path']);assert q['raw_sha256']==v['raw_sha256'],v['path'];checked[q['path']]=q
  for x in v.values():verify_refs(x)
 elif isinstance(v,list):
  for x in v:verify_refs(x)
for folder in [pre/'independent-header-math100',pre/'independent-header-source100',source]:
 for p in folder.rglob('*.json'):
  verify_refs(load(p));inputs[p.as_posix()]=pin(p)
for name in ['lean-toolchain','lake-manifest.json','research-wiki/process-memory.json']:inputs[name]=pin(name)
text=header.read_text(encoding='utf8')
d=dict(status='SEALED_BEFORE_PROOF_AFTER_INDEPENDENT_HEADER_AND_TOPOLOGY_AUDITS',sealed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),statement_version=1,owner='companion_root_20261005',baseline_commit=head,header=pin(header),expanded_literal_Prop=text.split('def candidate',1)[1].split('#check',1)[0].strip(),proposed_public_theorem='AutoSamplingTheory.ExampleCases.ProximalBPS.ActualPrescribedPathReversal.actual_prescribed_path_reversal_and_survival',source_revision='arXiv2609.06905v1/Lean4.33.0/Mathlibdb584cd6d46c92f209a44c0f1c829460d327499d',source_anchor='Appendix A.1 actual prescribed trajectories and A8 off-event reversal, survival integral matching',independent_math_header=pin(math),independent_source_header=pin(src),independent_topology=pin(topology),source_graph=pin(source/'source-slice-delta100.native.json'),source_graph_overlay=pin(source/'graph-refinement100/source-graph-overlay100.native.json'),source_coverage=load(source/'source-slice-delta100.native.json')['unchanged_inventory'],primary=pin(pre.parent/'phase-pbps-gamma-preread57/primary-pbps.exactraw.snapshot.html'),all_review_artifacts_rehashed=list(inputs.values()),all_bound_RAW_inputs_rehashed=list(checked.values()),binder_audit=dict(SOURCE=['hα','hαβ','hV','hH','hη','hβη'],TYPING=['Finite real Hilbert Borel E, rank zero included'],EXCESS=[]),definition_audit='Exact actual c/Phi/S/Rec/Hist/Delta/Prefix/m/zAt/K/Path/Psi/Gamma/R/rate from99. Clamped real-time gamma and barGamma on actual reversed tuple and R(actual terminal). rho exists with coordinate equation; all reversals, regularities and integrability are conclusions/internal dependencies.',core_delta='Actual reversed finite prescribed path equals momentum reversal of the time-reflected original off the finite event set on the whole closed horizon; both scalar rates are interval integrable and their survival integrals equal.',actual_producer_plan=['ActualPrescribedStateReversal.actual_prescribed_state_reversal_and_rate_product','ActualFiniteCountPath.actual_finite_count_path_law','ActualPhaseReversalVolume.actual_phase_reversal_volume_laws','ActualHarmonicFlow.actual_harmonic_flow_laws','ActualPrescribedPathDensity.actual_prescribed_path_density_rewrite'],consumer='Combine with98 Gibbs survival and99 incoming product to close weighted actual density underTheta97; then normalized stationary averaging. Later nodes not assumed.',truth_boundary='No all-time equality at genuine jumps or outside closed horizon; no weighted density/sector, invariant probability, restart/Markovness, hypocoercivity, implementation error, expected cost, main theorem or composition.',proof_search_started=False,sau_claimed=False,Goal_complete=False)
p=pre/'root.statement-seal100.json';assert not p.exists();p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
print(json.dumps(dict(seal=pin(p),bound_artifacts=len(inputs),proof_credit=False)))
